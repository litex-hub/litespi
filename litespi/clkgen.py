#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *

from litex.soc.integration.doc import AutoDoc, ModuleDoc

from litex.build.io import SDROutput


class LiteSPIClkGen(Module, AutoDoc, ModuleDoc):
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

        # Delay signals by 1 cycle due to usage of SDRTristate
        self.sync += [
            posedge.eq(~clk & (cnt == div)),
            negedge.eq(clk & (cnt == div)),
            sample.eq(cnt == sample_cnt),
            update.eq(cnt == update_cnt),
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
            if device.startswith("xc7"):
                cycles = Signal(4)
                self.specials += Instance("STARTUPE2",
                    i_CLK=0,
                    i_GSR=0,
                    i_GTS=0,
                    i_KEYCLEARB=0,
                    i_PACK=0,
                    i_USRCCLKO=clk,
                    i_USRCCLKTS=0,
                    i_USRDONEO=1,
                    i_USRDONETS=1,
                )
                # startupe2 needs 3 usrcclko cycles to switch over to user clock
                self.comb += en_int.eq(cycles < 3)
                self.sync += If(en_int & posedge, cycles.eq(cycles+1))
            elif device.startswith("LFE5U"):
                self.specials += Instance("USRMCLK",
                    i_USRMCLKI  = clk,
                    i_USRMCLKTS = 0
                )
            else:
                raise NotImplementedError
        else:
            self.specials += SDROutput(i=clk, o=pads.clk)

