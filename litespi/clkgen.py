#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *

from litex.soc.integration.doc import AutoDoc, ModuleDoc

from litex.build.io import SDROutput, DDROutput

class DDRLiteSPIClkGen(Module, AutoDoc):
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


class LiteSPIClkGen(Module, AutoDoc):
    """SPI Clock generator

    The ``LiteSPIClkGen`` class provides a generic SPI clock generator.

    It supports accessing CLK pin on a reserved pin by instantiating device specific modules (currently 7 Series only).

    Parameters
    ----------
    pads : Object
        SPI pads description.

    device : str
        Device type for determining how to get output pin if it was not provided in pads.

    cnt_width : int
        Width of the internal counter ``cnt`` used for dividing the clock.

    with_ddr : bool
        Generate additional ``sample`` and ``update`` signals.

    Attributes
    ----------
    div : Signal(8), in
        Clock divisor, output clock frequency will be equal to ``sys_clk_freq/(2*(1+div))``.

    posedge : Signal(), out
        Outputs 1 when there is a rising edge on the generated clock, 0 otherwise.

    negedge : Signal(), out
        Outputs 1 when there is a falling edge on the generated clock, 0 otherwise.

    en : Signal(), in
        Clock enable input, output clock will be generated if set to 1, 0 resets the core.

    sample : Signal(), out
        Outputs 1 when ``sample_cnt==cnt``, can be used to sample incoming DDR data.

    sample_cnt : Signal(8), in
        Controls generation of the ``sample`` signal.

    update : Signal(), out
        Outputs 1 when ``update_cnt==cnt``, can be used to update outgoing DDR data.

    update_cnt : Signal(8), in
        Controls generation of the ``update`` signal.
    """
    def __init__(self, pads, device, cnt_width=8, with_ddr=False):
        self.div        = div        = Signal(cnt_width)
        self.sample_cnt = sample_cnt = Signal(cnt_width)
        self.update_cnt = update_cnt = Signal(cnt_width)
        self.posedge    = posedge    = Signal()
        self.negedge    = negedge    = Signal()
        self.sample     = sample     = Signal()
        self.update     = update     = Signal()
        self.en         = en         = Signal()
        cnt             = Signal(cnt_width)
        en_int          = Signal()
        clk             = Signal()

        self.comb += [
            posedge.eq(en & ~clk & (cnt == div)),
            negedge.eq(en & clk & (cnt == div)),
            sample.eq(cnt == sample_cnt),
            update.eq(cnt == update_cnt),
        ]

        # Delayed edge to account for IO register delays.
        self.posedge_reg  = posedge_reg  = Signal()
        self.posedge_reg2 = posedge_reg2 = Signal()

        self.sync += [
            posedge_reg.eq(posedge),
            posedge_reg2.eq(posedge_reg),
        ]

        self.sync += [
            If(en | en_int,
                If(cnt < div,
                    cnt.eq(cnt+1),
                ).Else(
                    cnt.eq(0),
                    clk.eq(~clk),
                )
            ).Else(
                clk.eq(0),
                cnt.eq(0),
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
