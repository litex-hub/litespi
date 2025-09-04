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
    def __init__(self, pads, cs, cs_delay=10, with_sdr_cs=True, **kwargs):
        self.enable = enable = Signal()
        cs_n = Signal().like(pads.cs_n)
        last_cs = Signal()

        self.timer = timer  = WaitTimer(cs_delay + 1) # Ensure cs_delay cycles between XFers.

        if len(pads.cs_n) > 1:
            # Remember last active CS when multiple CS lines are used, so we only wait when
            # the same CS line is active again
            last_active_cs = Signal(len(cs))
            self.sync += If(enable, last_active_cs.eq(cs))

            enable_cond = timer.done | (last_active_cs != cs)
        else:
            enable_cond = timer.done

        self.sync += last_cs.eq(cs != 0)

        self.comb += timer.wait.eq(~((cs == 0) & last_cs)) # Reset wait on falling edge of cs
        self.comb += enable.eq((cs != 0) & enable_cond)
        self.comb += cs_n.eq(~(Replicate(enable, len(pads.cs_n)) & cs))

        if with_sdr_cs:
            self.specials += SDROutput(
                i = cs_n,
                o = pads.cs_n
            )
        else:
            self.comb += pads.cs_n.eq(cs_n)
