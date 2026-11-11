#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *
from migen.genlib.cdc import MultiReg

# Core <-> PHY Layouts -----------------------------------------------------------------------------

"""
Stream layout for LiteSPICore->PHY connection:
data - flash byte address when cmd=1, data to transmit when cmd=2, unused in cmd=0
len - xfer length (in bits)
width - xfer width (1/2/4/8)
mask - dq output enable control (1 enables a output on a particular pin)
"""
spi_core2phy_layout = [
    ("data", 32),
    ("len",   6),
    ("width", 4),
    ("mask",  8),
    ("clk_div", 10),
]
"""
Stream layout for PHY->LiteSPICore connection
data - 32-bits of data from flash
"""
spi_phy2core_layout = [
    ("data", 32),
]

MMAP_DEFAULT_TIMEOUT = 256


# Helpers ------------------------------------------------------------------------------------------

class ResyncReg(Module):
    def __init__(self, src, dst, clock_domain):
        if clock_domain == "sys":
            self.comb += dst.eq(src)
        else:
            self.specials += MultiReg(src, dst, clock_domain)


# WP#/HOLD# ----------------------------------------------------------------------------------------

def _opcode_widths(opcode):
    from litespi.opcodes import SpiNorFlashOpCodes
    cfg      = SpiNorFlashOpCodes()
    cfg.name = SpiNorFlashOpCodes.name_from_value(SpiNorFlashOpCodes, opcode)
    return [int(cfg.cmd_width), int(cfg.addr_width), int(cfg.data_width)]

def spi_wp_hold_x1(pads):
    """Hold the WP#/HOLD# pads of x1 pads high (write protect and hold released): x1 transfers never
    use them."""
    return [getattr(pads, name).eq(1) for name in ["wp", "hold"] if hasattr(pads, name)]

def spi_wp_hold_x4_mask(bus_width, flash):
    """Mask of the DQ lines to hold high on x4 pads: DQ2/DQ3 are WP#/HOLD# when the read and program
    commands of the module use 1 or 2 lines only (quad enable never set). 0 when the module is
    unknown or uses DQ2/DQ3 for data."""
    if (bus_width != 4) or (flash is None):
        return 0
    widths = _opcode_widths(flash.read_opcode)
    if getattr(flash, "program_opcode", None) is not None:
        widths += _opcode_widths(flash.program_opcode)
    return 0b1100 if max(widths) <= 2 else 0
