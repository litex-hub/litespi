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

import argparse
import os
import yaml

from migen import *

from litex.build.generic_platform import *
from litex.build.xilinx.platform import XilinxPlatform

from litex.soc.interconnect import wishbone
from litex.soc.interconnect import axi
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *
from litex.soc.integration.soc import SoCRegion

import inspect
import litespi.modules
from litespi.spi_nor_flash_module import SpiNorFlashModule

# module database
module_classes = inspect.getmembers(litespi.modules, inspect.isclass)
devices_dict = {name: cls for name, cls in module_classes if issubclass(cls, SpiNorFlashModule)}


# IOs ----------------------------------------------------------------------------------------------

_io = [
    # Clk / Rst
    ("sys_clock", 0, Pins(1)),
    ("sys_reset", 1, Pins(1)),

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

class SPICore(SoCMini):
    def __init__(self, platform, core_config):

        # SoC parameters ---------------------------------------------------------------------------
        soc_args = {}
        if "soc" in core_config:
            soc_config = core_config["soc"]

            for arg in soc_config:
                if arg in ("csr_map", "interrupt_map", "mem_map"):
                    getattr(self, arg).update(soc_config[arg])
                else:
                    soc_args[arg] = soc_config[arg]

        # SoCMini ----------------------------------------------------------------------------------
        SoCMini.__init__(self, platform, clk_freq=int(1e6), **soc_args)

        # CRG --------------------------------------------------------------------------------------
        self.submodules.crg = CRG(platform.request("sys_clock"), platform.request("sys_reset"))

        device = core_config["device"]
        mode = core_config["mode"]
        if not device in devices_dict:
            raise ValueError(f"Unsupported SPI device:", device)
        
        assert mode in ["x1", "x4"]
        requested_bus_width = {
          "x1" : 1,
          "x4" : 4,
          }[mode]
        
        rate = core_config["rate"] if "rate" in core_config else "1:1"
        divisor = int(core_config["divisor"]) if "divisor" in core_config else 1
        
        # PHY --------------------------------------------------------------------------------------
        from litespi.opcodes import SpiNorFlashOpCodes as Codes
        module_class = devices_dict[device]
        opcode = module_class.supported_opcodes[0] #use any opcode to get the instance
        spiflash_module = module_class(opcode)
        if not spiflash_module.check_bus_width(width=requested_bus_width):
            raise ValueError(f"SPI device doesn't support {requested_bus_width}-bit bus with")

        #SIM:
        #from litespi.phy.model import LiteSPIPHYModel
        #self.submodules.spiflash_phy = spiflash_phy = LiteSPIPHYModel(spiflash_module, init=None)  #no init
        pads = self.platform.request("spiflash" if mode == "1x" else "spiflash4x")
        from litespi.phy.generic import LiteSPIPHY
        spiflash_phy = LiteSPIPHY(pads, spiflash_module, device=self.platform.device,
          default_divisor=divisor, rate=rate)
        self.submodules += spiflash_phy

        from litespi import LiteSPI
        spiflash_core = LiteSPI(spiflash_phy, mmap_endianness=self.cpu.endianness,
          with_master=True, with_mmap=True, with_csr=True) #FIXME: parametrize endianness
        self.submodules += spiflash_core
        
        bus_standard = core_config["bus_standard"]
        assert bus_standard in ["wishbone", "axi-lite"]

        # Wishbone.
        if bus_standard == "wishbone":
            platform.add_extension(spiflash_core.bus.get_ios("bus"))
            platform_bus = self.platform.request("bus")
            self.comb += spiflash_core.bus.connect_to_pads(platform_bus, mode="slave")

        # AXI-Lite.
        if bus_standard == "axi-lite":
            # LiteSPI is in Wishbone, converter to AXI-Lite and expose the AXI-Lite Bus.
            axil_bus = axi.AXILiteInterface(address_width=32, data_width=32)
            platform.add_extension(axil_bus.get_ios("bus"))
            self.submodules += axi.Wishbone2AXILite(spiflash_core.bus, axil_bus)
            self.comb += axil_bus.connect_to_pads(self.platform.request("bus"), mode="slave")

# Build --------------------------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="LiteSPI standalone core generator")
    builder_args(parser)
    parser.set_defaults(output_dir="build")
    parser.add_argument("--vendor",       default="xilinx",  help="FPGA Vendor.")
    parser.add_argument("--device",       default="",  help="FPGA device (required for 1:2 rate)")
    parser.add_argument("config", help="YAML config file")
    args = parser.parse_args()
    core_config = yaml.load(open(args.config).read(), Loader=yaml.Loader)

    # Convert YAML elements to Python/LiteX --------------------------------------------------------
    for k, v in core_config.items():
        replaces = {"False": False, "True": True, "None": None}
        for r in replaces.keys():
            if v == r:
                core_config[k] = replaces[r]

    # Generate core --------------------------------------------------------------------------------
    # Convert/Check Arguments ----------------------------------------------------------------------
    platform_cls = {
        "xilinx"  : XilinxPlatform,
    }[args.vendor]
    platform = platform_cls(device=args.device, io=_io)
    platform.add_extension(_io)

    if core_config["bus_standard"] in ["wishbone", "axi-lite"]:
        soc = SPICore(platform, core_config)
    else:
        raise ValueError("Unknown bus standard: {}".format(core_config["bus_standard"]))

    builder_arguments = builder_argdict(args)
    builder_arguments["compile_gateware"] = False
    if builder_arguments["csr_csv"] is None:
        builder_arguments["csr_csv"] = os.path.join(builder_arguments["output_dir"], "csr.csv")

    builder = Builder(soc, **builder_arguments)
    builder.build(build_name="litespi_core")

if __name__ == "__main__":
    main()
