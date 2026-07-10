#
# This file is part of LiteSPI.
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *

from litex.gen import *


# Lattice ECP5 USRMCLK -----------------------------------------------------------------------------

class LiteSPIECP5USRMCLK(LiteXModule):
    """Route the registered LiteSPI SDR clock through the ECP5 USRMCLK primitive."""

    startup_cycles = 0

    def __init__(self):
        self.clk = clk = Signal()

        self.specials += Instance("USRMCLK",
            i_USRMCLKI  = clk,
            i_USRMCLKTS = ResetSignal(),
        )
