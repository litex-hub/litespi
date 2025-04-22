#
# This file is part of LiteSPI
#
# Copyright (c) 2024 Fin Maaß <f.maass@vogl-electronic.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *

from litex.gen import *
from litex.gen.genlib.misc import WaitTimer
from litex.build.io import SDROutput

class LiteSPICSControl(LiteXModule):
    def __init__(self, pads, cs, cs_delay):
        self.enable = enable = Signal()
        cs_n = Signal().like(pads.cs_n)

        self.timer = timer  = WaitTimer(cs_delay + 1) # Ensure cs_delay cycles between XFers.
        
        self.comb += timer.wait.eq(cs != 0)
        self.comb += enable.eq(timer.done)
        self.comb += cs_n.eq(~(Replicate(enable, len(pads.cs_n)) & cs))

        self.specials += SDROutput(
            i = cs_n,
            o = pads.cs_n
        )
