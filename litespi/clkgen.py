#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# Copyright (c) 2025 Fin Maaß <f.maass@vogl-electronic.com>
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

        self.specials += DDROutput(i1=en, i2=0, o=pads.clk)


class LiteSPIClkGen(LiteXModule):
    """SPI Clock generator

    The ``LiteSPIClkGen`` class provides a generic SPI clock generator.

    It supports accessing CLK pin on a reserved pin by instantiating device specific modules (currently 7 Series only).

    Parameters
    ----------
    pads : Object
        SPI pads description.

    device : str
        Device type for determining how to get output pin if it was not provided in pads.

    div_width : int
        Width of the ``div`` used for dividing the clock.

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
    """
    def __init__(self, pads, device, div_width=8, extra_latency=0):
        self.div        = div        = Signal(div_width)
        self.posedge    = posedge    = Signal()
        self.negedge    = negedge    = Signal()
        self.en         = en         = Signal()
        cnt             = Signal(div_width - 1)
        en_int          = Signal()
        clk             = Signal()
        half            = Signal(div_width - 1)

        self.comb += half.eq((div + 1) >> 1)

        self.comb += [
            posedge.eq(en & ~clk & (cnt <= 1)),
            negedge.eq(en &  clk & (cnt <= 1)),
        ]

        # Delayed edge to account for IO register delays.
        posedge_reg  = Signal(1 + 1 + int(extra_latency))
        self.posedge_reg2 = posedge_reg2 = Signal()

        self.sync += [
            posedge_reg.eq(Cat(posedge_reg[1:], posedge)),
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
            ).Else(
                clk.eq(0),
                cnt.eq(half),
            )
        ]

        if not hasattr(pads, "clk"):
            # Clock output needs to be registered like an SDROutput.
            clk_reg = Signal()
            self.sync += clk_reg.eq(clk)

            if device.startswith("xc7"):
                cycles = Signal(4)
                self.specials += Instance("STARTUPE2",
                    i_CLK       = 0,
                    i_GSR       = 0,
                    i_GTS       = 0,
                    i_KEYCLEARB = 0,
                    i_PACK      = 0,
                    i_USRCCLKO  = clk_reg,
                    i_USRCCLKTS = 0,
                    i_USRDONEO  = 1,
                    i_USRDONETS = 1,
                )
                # startupe2 needs 3 usrcclko cycles to switch over to user clock
                self.comb += en_int.eq(cycles < 3)
                self.sync += If(en_int & posedge, cycles.eq(cycles+1))
            elif device.startswith("LFE5U"):
                self.specials += Instance("USRMCLK",
                    i_USRMCLKI  = clk_reg,
                    i_USRMCLKTS = 0
                )
            else:
                raise NotImplementedError
        else:
            self.specials += SDROutput(i=clk, o=pads.clk)

class LiteSPIClkGen2(LiteXModule):
    """SPI Clock generator

    The ``LiteSPIClkGen`` class provides a generic SPI DDR clock generator.

    Parameters
    ----------
    pads : Object
        SPI pads description.

    div_width : int
        Width of the ``div`` used for dividing the clock.

    Attributes
    ----------
    div : Signal(8), in
        Clock divisor, output clock frequency will be equal to ``sys_clk_freq/div``.

    posedge : Signal(), out
        Outputs 1 when there is a rising edge on the generated clock, 0 otherwise.

    negedge : Signal(), out
        Outputs 1 when there is a falling edge on the generated clock, 0 otherwise.

    en : Signal(), in
        Clock enable input, output clock will be generated if set to 1, 0 resets the core.
    """
    def __init__(self, pads, div_width=8, extra_latency=0):
        self.div        = div        = Signal(div_width)
        self.posedge    = posedge    = Signal(2)
        self.negedge    = negedge    = Signal(2)
        self.en         = en         = Signal()
        cnt             = Signal(div_width + 1)
        clk             = Signal(2)
        next_clk        = Signal(2)
        next_cnt        = Signal(div_width + 1)

        double_div = Signal(div_width + 1)
        self.comb += double_div.eq(Cat(C(0,1), div))

        self.comb += [
                If(cnt == 2,
                   next_cnt.eq(double_div),
                   next_clk[0].eq(cnt <= div),
                   next_clk[1].eq(1),
               ).Elif(cnt <= 1,
                   next_cnt.eq(double_div - 1),
                   next_clk[0].eq(1),
                   next_clk[1].eq(0),
               ).Else(
                    next_cnt.eq(cnt - 2),
                    next_clk[0].eq(cnt <= div),
                    next_clk[1].eq((cnt - 1) <= div),
                ),
        ]

        self.comb += [
            posedge[0].eq(en & ~clk[1] & next_clk[0]),
            negedge[0].eq(en &  clk[1] & ~next_clk[0]),
            posedge[1].eq(en & ~next_clk[0] & next_clk[1]),
            negedge[1].eq(en &  next_clk[0] & ~next_clk[1]),
        ]

        # Delayed edge to account for IO register delays.
        posedge_reg  = Signal(2 + 2 + 2 + int(extra_latency))
        self.posedge_reg2 = posedge_reg2 = Signal(2)

        self.sync += [
            posedge_reg.eq(Cat(posedge_reg[2:], posedge)),
        ]

        self.comb += posedge_reg2.eq(posedge_reg[:2])

        self.sync += [
            If(en,
                cnt.eq(next_cnt),
                clk.eq(next_clk),
            ).Else(
                clk.eq(0),
                cnt.eq(double_div),
            )
        ]

        self.specials += DDROutput(i1=(en & clk[0]), i2=(en & clk[1]), o=pads.clk)
