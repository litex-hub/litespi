#
# This file is part of LiteSPI.
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *

from litex.gen import *


# Xilinx UltraScale STARTUPE3 ----------------------------------------------------------------------

class LiteSPISTARTUPE3(LiteXModule):
    """Route registered LiteSPI SDR signals through the UltraScale STARTUPE3 primitive."""

    data_width     = 4
    startup_cycles = 3

    def __init__(self):
        self.pads  = pads  = Record([("clk", 1), ("cs_n", 1)])
        pads.cs_n.reset = 1
        self.dq_o  = dq_o  = Signal(self.data_width)
        self.dq_oe = dq_oe = Signal(self.data_width)
        self.dq_i  = dq_i  = Signal(self.data_width)

        self.do  = do  = Signal(self.data_width)
        self.dts = dts = Signal(self.data_width, reset=2**self.data_width - 1)
        self.di  = di  = Signal(self.data_width)

        # Match the registered generic SDR I/O path. STARTUPE3 uses active-high DTS while
        # LiteSPI uses active-high output enable.
        self.sync += [
            do.eq(dq_o),
            dts.eq(~dq_oe),
            dq_i.eq(di),
        ]

        self.specials += Instance("STARTUPE3",
            i_GSR       = 0,
            i_GTS       = 0,
            i_KEYCLEARB = 0,
            i_PACK      = 0,
            i_USRCCLKO  = pads.clk,
            i_USRCCLKTS = 0,
            i_USRDONEO  = 1,
            i_USRDONETS = 1,
            i_FCSBO     = pads.cs_n,
            i_FCSBTS    = 0,
            i_DO        = do,
            i_DTS       = dts,
            o_DI        = di,
        )
