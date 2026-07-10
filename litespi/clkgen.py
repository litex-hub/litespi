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

    div_width : int
        Width of the ``div`` input.

    extra_latency : int or float
        Additional input latency in half-system-clock steps.

    Attributes
    ----------
    div : Signal(), in
        Clock divisor. SCK frequency is ``sys_clk_freq/div``.

    en : Signal(), in
        Keep the clock generator active.

    start : Signal(), in
        Start a transfer and latch ``div``.

    posedge : Signal(), out
        Indicates an SCK rising edge at the current system rising edge.

    negedge : Signal(2), out
        Indicates an SCK falling edge before lane 0 or between lanes 0 and 1.

    sample : Signal(), out
        Delayed ``posedge`` used to capture the registered DQ inputs.
    """
    def __init__(self, pads, div_width=8, extra_latency=0):
        self.div      = div      = Signal(div_width)
        self.en       = en       = Signal()
        self.start    = start    = Signal()
        self.posedge  = posedge  = Signal()
        self.negedge  = negedge  = Signal(2)
        self.sample   = sample   = Signal()
        self.clk      = clk      = Signal(2)

        extra_latency_cycles = int(2*extra_latency)
        if (extra_latency < 0) or (extra_latency_cycles != 2*extra_latency):
            raise ValueError("DDR PHY extra_latency must be a non-negative multiple of 0.5")

        active          = Signal()
        level           = Signal(reset=1)
        remaining       = Signal(div_width, reset=1)
        div_latched     = Signal(div_width, reset=1)
        div_start       = Signal(div_width)
        slot1_level     = Signal()
        slot1_remaining = Signal(div_width)
        next_level      = Signal()
        next_remaining  = Signal(div_width)

        self.comb += div_start.eq(Mux(div == 0, 1, div))

        # Consume two SCK half-cycles per system cycle.
        self.comb += [
            slot1_level.eq(level),
            slot1_remaining.eq(remaining - 1),
            If(remaining == 1,
                slot1_level.eq(~level),
                slot1_remaining.eq(div_latched),
            ),
            next_level.eq(slot1_level),
            next_remaining.eq(slot1_remaining - 1),
            If(slot1_remaining == 1,
                next_level.eq(~slot1_level),
                next_remaining.eq(div_latched),
            ),
            clk[0].eq(active & level),
            clk[1].eq(active & slot1_level),
        ]

        # Rising edges stay aligned to system rising edges. Falling edges occur either at the
        # beginning of lane 0 for even divisors or between lanes 0/1 for odd divisors.
        self.comb += [
            posedge.eq(active &  level & (remaining == div_latched)),
            negedge[0].eq(active & ~level & (remaining == div_latched)),
            negedge[1].eq(active &  level & (remaining == 1)),
        ]

        self.sync += If(start,
            active.eq(1),
            level.eq(1),
            remaining.eq(div_start),
            div_latched.eq(div_start),
        ).Elif(active,
            If(en,
                level.eq(next_level),
                remaining.eq(next_remaining),
            ).Else(
                active.eq(0),
                level.eq(1),
                remaining.eq(div_latched),
            )
        )

        # Delay input captures through the IDDR/fabric pipeline. Half-step latency values map to
        # complete system cycles since the DDR path handles two half-cycles per system cycle.
        sample_pipeline = Signal(2 + extra_latency_cycles)
        self.sync += If(start,
            sample_pipeline.eq(0),
        ).Else(
            sample_pipeline.eq(Cat(sample_pipeline[1:], posedge)),
        )
        self.comb += sample.eq(sample_pipeline[0])

        self.specials += DDROutput(i1=clk[0], i2=clk[1], o=pads.clk)


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
        self.mode       = mode       = Signal(2)
        self.en         = en         = Signal()
        self.start      = start      = Signal()
        cnt             = Signal(div_width - 1)
        en_int          = Signal()
        clk             = Signal()
        half            = Signal(div_width - 1)

        self.comb += half.eq((div + 1) >> 1)

        self.comb += [
            posedge.eq( (en | en_int)  & ~clk & (cnt <= 1)),
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
                    i_USRMCLKTS = ResetSignal()
                )
            else:
                raise NotImplementedError
        else:
            self.specials += SDROutput(i=clk, o=pads.clk)
