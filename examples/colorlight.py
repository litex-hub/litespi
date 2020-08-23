#!/usr/bin/env python3

#
# This file is part of LiteSPI
#
# Copyright (c) 2015-2019 Florent Kermarrec <florent@enjoy-digital.fr>
# Copyright (c) 2020 Derek Mulcahy
# SPDX-License-Identifier: BSD-2-Clause

import os
import argparse

from migen import *

from litex_boards.platforms import colorlight_5a_75b, colorlight_5a_75e
from litex.build.lattice.trellis import trellis_args, trellis_argdict

from litex.soc.cores.clock import *
from litex.soc.integration.soc import SoCRegion
from litex.soc.integration.soc_core import *
from litex.soc.integration.soc_sdram import *
from litex.soc.integration.builder import *

from litespi.modules import W25Q32JV
from litespi.opcodes import SpiNorFlashOpCodes as Codes
from litespi.phy.generic import LiteSPIPHY
from litespi import LiteSPI

from litex.build.io import DDROutput
from litedram.modules import M12L16161A
from litedram.phy import GENSDRPHY

from liteeth.phy.ecp5rgmii import LiteEthPHYRGMII
from litex.build.generic_platform import *

# CRG ----------------------------------------------------------------------------------------------

class _CRG(Module):
    def __init__(self, platform, sys_clk_freq, with_rst=True):
        self.clock_domains.cd_sys    = ClockDomain()
        self.clock_domains.cd_sys_ps = ClockDomain()

        # # #

        clk25 = platform.request("clk25")
        rst_n = 1 if not with_rst else platform.request("user_btn_n", 0)
        platform.add_period_constraint(clk25, 1e9/25e6)

        self.submodules.pll = pll = ECP5PLL()

        pll.register_clkin(clk25, 25e6)
        pll.create_clkout(self.cd_sys,    sys_clk_freq)
        pll.create_clkout(self.cd_sys_ps, sys_clk_freq, phase=180)
        self.specials += AsyncResetSynchronizer(self.cd_sys, ~pll.locked | ~rst_n)

        # SDRAM clock
        self.specials += DDROutput(1, 0, platform.request("sdram_clock"), ClockSignal("sys_ps"))


# BaseSoC ------------------------------------------------------------------------------------------

ios = [
    # Alternative pins for UART to avoid reset button conflict with user_btn_n and user_led_n
    # Requires modification to the Colorlight board to allow input on rx
    ("uart", 0,
        Subsignal("tx", Pins("j9:1")),
        Subsignal("rx", Pins("j9:0")),
        IOStandard("LVCMOS33")
    )
]

class BaseSoC(SoCCore):
    def __init__(self,
            sys_clk_freq   = int(60e6),
            with_ethernet  = False,
            with_etherbone = False,
            with_spiflash  = False,
            ip_address     = None,
            mac_address    = None,
            **kwargs):

        platform = colorlight_5a_75e.Platform()
        platform.add_extension(ios)

        # SoCCore ----------------------------------------------------------------------------------
        SoCCore.__init__(self, platform,
            clk_freq       = sys_clk_freq,
            ident          = "LiteX LiteSPI SoC",
            ident_version  = True,
            csr_data_width = 32,
            **kwargs)

        # CRG --------------------------------------------------------------------------------------
        self.submodules.crg = _CRG(platform, sys_clk_freq, with_rst=(kwargs["uart_name"] != "serial"))

        # SDRAM ------------------------------------------------------------------------------------
        if not self.integrated_main_ram_size:
            self.submodules.sdrphy = GENSDRPHY(platform.request("sdram"))
            self.add_sdram("sdram",
                phy                     = self.sdrphy,
                module                  = M12L16161A(sys_clk_freq, "1:1"),
                origin                  = self.mem_map["main_ram"],
                size                    = kwargs.get("max_sdram_size", 0x40000000),
                l2_cache_size           = kwargs.get("l2_size", 8192),
                l2_cache_min_data_width = kwargs.get("min_l2_data_width", 128),
                l2_cache_reverse        = True)

        # SPIFlash ---------------------------------------------------------------------------------
        if with_spiflash:
            flash = W25Q32JV(Codes.READ_1_1_1)
            self.submodules.spiflash_phy    = LiteSPIPHY(
                pads    = platform.request("spiflash"),
                flash   = flash,
                device  = platform.device)
            self.submodules.spiflash_mmap   = LiteSPI(
                phy             = self.spiflash_phy,
                clk_freq        = sys_clk_freq,
                mmap_endianness = self.cpu.endianness)
            self.add_csr("spiflash_mmap")
            self.add_csr("spiflash_phy")
            spiflash_region = SoCRegion(
                origin  = self.mem_map.get("spiflash", None),
                size    = flash.total_size,
                cached  = False)
            self.bus.add_slave(
                name    = "spiflash",
                slave   = self.spiflash_mmap.bus,
                region  = spiflash_region)

        # Ethernet ---------------------------------------------------------------------------------
        if with_ethernet:
            self.submodules.ethphy = LiteEthPHYRGMII(
                clock_pads = self.platform.request("eth_clocks"),
                pads       = self.platform.request("eth"))
            self.add_csr("ethphy")
            self.add_ethernet(
                phy         = self.ethphy,
                ip_address  = ip_address,
                mac_address = mac_address)

        # Etherbone --------------------------------------------------------------------------------
        if with_etherbone:
            self.submodules.ethphy = LiteEthPHYRGMII(
                clock_pads = self.platform.request("eth_clocks"),
                pads       = self.platform.request("eth"))
            self.add_csr("ethphy")
            self.add_etherbone(
                phy         = self.ethphy,
                ip_address  = ip_address,
                mac_address = mac_address)

# Build --------------------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="LiteX LiteSPI SoC on Colorlight")
    parser.add_argument("--build", action="store_true", help="Build bitstream")
    parser.add_argument("--load",  action="store_true", help="Load bitstream")
    builder_args(parser)
    soc_sdram_args(parser)
    trellis_args(parser)
    parser.add_argument("--with-ethernet",  action="store_true",      help="Enable Ethernet support")
    parser.add_argument("--with-etherbone", action="store_true",      help="Enable Etherbone support")
    parser.add_argument("--with-spiflash",  action="store_true",      help="Enable SPIFlash support")
    parser.add_argument("--ip-address",     default="192.168.1.20",   help="Ethernet IP address of the board.")
    parser.add_argument("--mac-address",    default="0x726b895bc2e2", help="Ethernet MAC address of the board.")
    args = parser.parse_args()

    assert not (args.with_ethernet and args.with_etherbone)
    soc = BaseSoC(
        with_ethernet  = args.with_ethernet,
        with_etherbone = args.with_etherbone,
        with_spiflash  = args.with_spiflash,
        ip_address     = args.ip_address,
        mac_address    = int(args.mac_address, 0),
        **soc_sdram_argdict(args))
    builder = Builder(soc, **builder_argdict(args))
    builder.build(**trellis_argdict(args), run=args.build)

    if args.load:
        prog = soc.platform.create_programmer()
        prog.load_bitstream(os.path.join(builder.gateware_dir, soc.build_name + ".bit"))

if __name__ == "__main__":
    main()
