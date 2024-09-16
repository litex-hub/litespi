#!/usr/bin/env python3

#
# This file is part of LiteSPI.
#
# Copyright (c) 2015-2022 Florent Kermarrec <florent@enjoy-digital.fr>
# Copyright (c) 2022 Victor Suarez Rovere <suarezvictor@gmail.com>
# SPDX-License-Identifier: BSD-2-Clause

"""
LiteSPI standalone core generator

LiteSPI aims to be directly used as a python package when the SoC is created using LiteX. However,
for some use cases it could be interesting to generate a standalone verilog file of the core:
- integration of the core in a SoC using a more traditional flow.
- need to version/package the core.
- avoid Migen/LiteX dependencies.
- etc...

The standalone core is generated from a YAML configuration file that allows the user to generate
easily a custom configuration of the core.

"""

import os
import yaml
import argparse
import inspect

from migen import *

from litex.build.generic_platform import *
from litex.build.sim import SimPlatform
from litex.build.xilinx.platform import XilinxPlatform
from litex.build.altera.platform import AlteraPlatform
from litex.build.lattice.platform import LatticePlatform

from litex.soc.interconnect import wishbone
from litex.soc.interconnect import axi
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.integration.soc import SoCRegion

import litespi.modules
from litespi.spi_nor_flash_module import SpiNorFlashModule
from litespi.opcodes import SpiNorFlashOpCodes as Codes

from litespi import LiteSPI
from litespi.phy.generic import LiteSPIPHY

# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("clk", 0, Pins(1)),
    ("rst", 1, Pins(1)),

    # SPI-Flash (X1).
    ("spiflash", 0,
        Subsignal("cs_n", Pins(1)),
        Subsignal("clk",  Pins(1)),
        Subsignal("mosi", Pins(1)),
        Subsignal("miso", Pins(1)),
        Subsignal("wp",   Pins(1)),
        Subsignal("hold", Pins(1)),
    ),

    # SPI-Flash (X4).
    ("spiflash4x", 0,
        Subsignal("cs_n", Pins(1)),
        Subsignal("clk",  Pins(1)),
        Subsignal("dq",   Pins(4)),
    ),
]

# LiteSPI Core -------------------------------------------------------------------------------------

class LiteSPICore(SoCMini):
    def __init__(self, platform, module, mode="x4", rate="1:1", divisor="1",
        bus_standard   = "wishbone",
        bus_endianness = "big",
        with_master    = False,
        sim            = False
    ):
        # CRG --------------------------------------------------------------------------------------
        self.crg = CRG(platform.request("clk"), platform.request("rst"))

        # SoCMini ----------------------------------------------------------------------------------
        SoCMini.__init__(self, platform, clk_freq=int(1e6))

        # SPI Flash Module -------------------------------------------------------------------------

        # Get available modules.
        modules_cls = inspect.getmembers(litespi.modules, inspect.isclass)
        modules     = {name: cls for name, cls in modules_cls if issubclass(cls, SpiNorFlashModule)}

        # Check that selected module is supported.
        def print_supported_modules():
            r = ""
            i = 0
            modules_per_line = 8
            modules_interval = 24
            for name, module in modules.items():
                r += f"{name}{' '*(modules_interval-len(name))}"
                if (i%modules_per_line) == (modules_per_line-1):
                    r += "\n"
                i += 1
            return r

        if not module in modules:
            raise ValueError(f"Unsupported SPI module {module}, supported:\n{print_supported_modules()}")

        # Check that selected width is supported in module.
        assert mode in ["x1", "x4"]
        module_width = {
          "x1" : 1,
          "x4" : 4,
        }[mode]
        spiflash_module_cls = modules[module]
        spiflash_module     = spiflash_module_cls(getattr(Codes, f"READ_1_1_{module_width}"))

        # SPI Flash PHY ----------------------------------------------------------------------------

        if sim:
            from litespi.phy.model import LiteSPIPHYModel
            self.spiflash_phy = spiflash_phy = LiteSPIPHYModel(spiflash_module, init=[i for i in range(16)]) # FIXME: Allow custom init?
        else:
            pads = self.platform.request("spiflash" if mode == "x1" else "spiflash4x")
            self.spiflash_phy = spiflash_phy = LiteSPIPHY(
                pads            = pads,
                flash           = spiflash_module,
                device          = platform.device,
                default_divisor = int(divisor),
                rate            = rate
            )

        # SPI Flash Core / MMAP --------------------------------------------------------------------

        assert bus_standard in ["wishbone", "axi-lite"]

        self.spiflash_core = spiflash_core = LiteSPI(
            phy             = spiflash_phy,
            mmap_endianness = bus_endianness,
            with_master     = with_master,
            with_mmap       = True,
            with_csr        = False
        )

        # Wishbone.
        if bus_standard == "wishbone":
            # LiteSPI is already in Wishbone, just expose the Bus.
            platform.add_extension(spiflash_core.bus.get_ios("bus"))
            self.comb += spiflash_core.bus.connect_to_pads(platform.request("bus"), mode="slave")

            # Expose Ctrl Bus.
            if with_master:
                master_bus = wishbone.Interface(address_width=32, data_width=32)
                platform.add_extension(master_bus.get_ios("master"))
                self.comb += master_bus.connect_to_pads(self.platform.request("master"), mode="slave")
                self.bus.add_master(master=master_bus)

        # AXI-Lite.
        if bus_standard == "axi-lite":
            # LiteSPI is in Wishbone, converter to AXI-Lite and expose the AXI-Lite Bus.
            axil_bus = axi.AXILiteInterface(address_width=32, data_width=32)
            platform.add_extension(axil_bus.get_ios("bus"))
            self.submodules += axi.AXILite2Wishbone(axil_bus, spiflash_core.bus)
            self.comb += axil_bus.connect_to_pads(platform.request("bus"), mode="slave")

            # Expose Ctrl Bus.
            if with_master:
                master_bus = axi.AXILiteInterface(address_width=32, data_width=32)
                platform.add_extension(master_bus.get_ios("master"))
                self.comb += master_bus.connect_to_pads(self.platform.request("master"), mode="slave")
                self.bus.add_master(master=master_bus)

# Build --------------------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="LiteSPI standalone core generator.")
    parser.add_argument("--clk-freq",       default="100e6",      help="Input Clk Frequency.")
    parser.add_argument("--vendor",         default="xilinx",     help="FPGA Vendor.")
    parser.add_argument("--module",         default="S25FL128L",  help="SPI Flash Module.")
    parser.add_argument("--mode",           default="x1",         help="SPI Mode (x1, x4).")
    parser.add_argument("--rate",           default="1:1",        help="SPI Flash Core rate (1:1, 1:2).")
    parser.add_argument("--divisor",        default="1",          help="SPI PHY Clk Divisor.")
    parser.add_argument("--bus-standard",   default="wishbone",   help="Bus Standard (wishbone, axi-lite).")
    parser.add_argument("--bus-endianness", default="big",        help="Bus Endianness (big, little).")
    parser.add_argument("--with-master",    action='store_true',  help="Enable Master (For Control & Writes).")
    parser.add_argument("--sim",            action='store_true',  help="Integrate LiteSPIPHYModel in core for simulation.")
    args = parser.parse_args()

    # Generate core --------------------------------------------------------------------------------
    platform_cls = {
        "xilinx"  : XilinxPlatform,
        "altera"  : AlteraPlatform,
        "intel"   : AlteraPlatform,
        "lattice" : LatticePlatform
    }[args.vendor]
    platform = platform_cls(device="", io=_io)
    core     = LiteSPICore(platform,
        module         = args.module,
        mode           = args.mode,
        rate           = args.rate,
        divisor        = args.divisor,
        bus_standard   = args.bus_standard,
        bus_endianness = args.bus_endianness,
        with_master    = args.with_master,
        sim            = args.sim,
    )
    builder  = Builder(core, output_dir="build")
    builder.build(build_name="litespi_core", run=False)

if __name__ == "__main__":
    main()
