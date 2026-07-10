#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *

from litex.gen import *

from litex.build.io import SDROutput, DDROutput

class DDRLiteSPIClkGen(LiteXModule):
    """SPI Clock generator

    The ``DDRLiteSPIClkGen`` class provides a generic SPI clock generator.

    The class can be combined with DDR PHY Core.

    Parameters
    ----------
    pads : Object
        SPI pads description.

    Attributes
    ----------
    en : Signal(), in
        Clock enable input, output clock will be generated if set to 1, 0 resets the core.
    """
    def __init__(self, pads):
        self.en         = en         = Signal()

        # Keep SCK rising/falling edges aligned with sys rising/falling edges respectively.
        self.specials += DDROutput(i1=en, i2=0, o=pads.clk)


class LiteSPIClkGen(LiteXModule):
    """SPI Clock generator

    The ``LiteSPIClkGen`` class provides a generic SPI clock generator.

    Device-specific clock routing is provided by a backend exposing a virtual ``clk`` pad.

    Parameters
    ----------
    pads : Object
        SPI pads description.

    device : str
        Retained for API compatibility. Device-specific selection is handled by the PHY.

    div_width : int
        Width of the ``div`` used for dividing the clock.

    startup_cycles : int
        Number of clock rising edges required before a transfer can start.

    clk_io : LiteXModule or None
        Optional clock-only backend accepting an already registered clock signal.

    Attributes
    ----------
    div : Signal(8), in
        Clock divisor, output clock frequency will be equal to ``sys_clk_freq/(2*((div + 1)//2))``.
        It's ``sys_clk_freq/div``, but div is rounded up to the nearest even number.

    posedge : Signal(), out
        Outputs 1 when there is a rising edge on the generated clock, 0 otherwise.

    negedge : Signal(), out
        Outputs 1 when there is a falling edge on the generated clock, 0 otherwise.

    en : Signal(), in
        Clock enable input, output clock will be generated if set to 1, 0 resets the core.

    ready : Signal(), out
        Indicates that vendor-specific clock startup is complete and a transfer can start.
    """
    def __init__(self, pads, device, div_width=8, extra_latency=0, startup_cycles=0, clk_io=None):
        if not isinstance(startup_cycles, int) or startup_cycles < 0:
            raise ValueError("SPI clock startup_cycles must be a non-negative integer")
        if not hasattr(pads, "clk") and clk_io is None:
            raise ValueError("LiteSPIClkGen requires a physical clk pad or a clock-only backend")

        self.div        = div        = Signal(div_width)
        self.posedge    = posedge    = Signal()
        self.negedge    = negedge    = Signal()
        self.mode       = mode       = Signal(2)
        self.en         = en         = Signal()
        self.start      = start      = Signal()
        self.ready      = ready      = Signal()
        cnt             = Signal(div_width - 1)
        en_int          = Signal()
        clk             = Signal()
        half            = Signal(div_width - 1)

        self.comb += half.eq((div + 1) >> 1)

        self.comb += [
            posedge.eq((en | en_int) & ~clk & (cnt <= 1)),
            negedge.eq(clk & (cnt <= 1)),
        ]

        # Delayed edge to account for IO register delays.
        posedge_reg  = Signal(1 + 1 + int(extra_latency))
        self.posedge_reg2 = posedge_reg2 = Signal()

        self.sync += [
            posedge_reg.eq(Cat(posedge_reg[1:], posedge)),
            If(start,
                posedge_reg.eq(0),
            ),
        ]

        self.comb += posedge_reg2.eq(posedge_reg[:1])

        self.sync += [
            If(en | en_int,
                If(cnt <= 1,
                    clk.eq(~clk),   # 50 % duty-cycle toggle.
                    cnt.eq(half)    # reload count.
                ).Else(
                    cnt.eq(cnt - 1) # simple down-count.
                )
            ).Elif(start,
                clk.eq(0),
                cnt.eq(half),
            ).Else(
                clk.eq(mode[1]),
                cnt.eq(half),
            )
        ]

        if clk_io is not None:
            # Match the register previously used directly in front of vendor clock primitives.
            clk_reg = Signal()
            self.sync += clk_reg.eq(clk)
            self.comb += clk_io.clk.eq(clk_reg)
        else:
            self.specials += SDROutput(i=clk, o=pads.clk)

        if startup_cycles:
            cycles        = Signal(max=startup_cycles + 1)
            startup_ready = Signal()
            self.comb += en_int.eq(cycles < startup_cycles)
            self.sync += If(en_int & posedge, cycles.eq(cycles + 1))
            # Account for the register between the internal clock and its output.
            self.sync += startup_ready.eq(~en_int)
            self.comb += ready.eq(startup_ready)
        else:
            self.comb += [
                en_int.eq(0),
                ready.eq(1),
            ]
