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
