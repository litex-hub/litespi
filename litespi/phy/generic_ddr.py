#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *
from migen.genlib.cdc import MultiReg
from migen.genlib.misc import WaitTimer

from litespi.common import *
from litespi.clkgen import DDRLiteSPIClkGen

from litex.soc.interconnect import stream
from litex.soc.interconnect.csr import *

from litex.build.io import DDRTristate

from litex.soc.integration.doc import AutoDoc, ModuleDoc


# LiteSPI DDR PHY Core -----------------------------------------------------------------------------

class LiteSPIDDRPHYCore(Module, AutoCSR, AutoDoc, ModuleDoc):
    """LiteSPI PHY DDR instantiator

    The ``DDRLiteSPIPHYCore`` class provides a generic PHY that can be connected to the ``LiteSPICore``.

    It supports single/dual/quad/octal output reads from the flash chips.

    You can use this class only with devices that supports the DDR primitives.

    The following diagram shows how each clock configuration option relates to outputs and input sampling in DDR mode:

    .. wavedrom:: ../../doc/ddr-timing-diagram.json

    Parameters
    ----------
    pads : Object
        SPI pads description.

    flash : SpiNorFlashModule
        SpiNorFlashModule configuration object.

    Attributes
    ----------
    source : Endpoint(spi_phy2core_layout), out
        Data stream.

    sink : Endpoint(spi_core2phy_layout), in
        Control stream.

    cs : Signal(), in
        Flash CS signal.
    """
    def __init__(self, pads, flash, cs_delay, extra_latency=0):
        self.source = source = stream.Endpoint(spi_phy2core_layout)
        self.sink   = sink   = stream.Endpoint(spi_core2phy_layout)
        self.cs     = Signal()

        if hasattr(pads, "miso"):
            bus_width = 1
            pads.dq   = [pads.mosi, pads.miso]
        else:
            bus_width = len(pads.dq)

        assert bus_width in [1, 2, 4, 8]

        # Check if number of pads matches configured mode.
        assert flash.check_bus_width(bus_width)

        self.addr_bits  = addr_bits  = flash.addr_bits
        self.ddr        = ddr        = flash.ddr

        assert not ddr

        # Clock Generator.
        self.submodules.clkgen = clkgen = DDRLiteSPIClkGen(pads)

        # CS control.
        cs_timer  = WaitTimer(cs_delay + 1) # Ensure cs_delay cycles between XFers.
        cs_enable = Signal()
        self.submodules += cs_timer
        self.comb += cs_timer.wait.eq(self.cs)
        self.comb += cs_enable.eq(cs_timer.done)
        self.comb += pads.cs_n.eq(~cs_enable)

        # I/Os.
        data_bits = 32

        dq_o1  = Signal(len(pads.dq))
        dq_o2  = Signal(len(pads.dq))
        dq_i1  = Signal(len(pads.dq))
        dq_i2  = Signal(len(pads.dq))
        dq_oe1 = Signal(len(pads.dq))
        dq_oe2 = Signal(len(pads.dq))

        for i in range(len(pads.dq)):
            self.specials += DDRTristate(
                io  = pads.dq[i],
                o1  = dq_o1[i],
                o2  = dq_o2[i],
                oe1 = dq_oe1[i],
                oe2 = dq_oe2[i],
                i1  = dq_i1[i],
                i2  = dq_i2[i]
            )

        # FSM.
        shift_cnt = Signal(8, reset_less=True)

        usr_dout  = Signal(len(sink.data),  reset_less=True)
        usr_din   = Signal(len(sink.data),  reset_less=True)

        clk_en = Signal()

        self.comb += self.clkgen.en.eq(clk_en)

        din_width_cases = {1: [
                 NextValue(usr_din, Cat(dq_o1[1], usr_din)),
            ]
        }
        for i in [2, 4, 8]:
            din_width_cases[i] = [
                NextValue(usr_din, Cat(dq_o1[0:i], usr_din))
            ]

        dout_width_cases = {}
        for i in [1, 2, 4, 8]:
            dout_width_cases[i] = [
                dq_i2.eq(usr_dout[-i:]),
                NextValue(dq_i1, dq_i2)
            ]

        self.submodules.fsm = fsm = FSM(reset_state="WAIT-CMD-DATA")
        fsm.act("WAIT-CMD-DATA",
            NextValue(clk_en, 0),
            If(cs_enable & sink.valid,
                NextValue(usr_dout,  sink.data << (32-sink.len)),
                NextValue(usr_din,   0),
                Case(sink.width, dout_width_cases),
                NextState("XFER")
            )
        )

        fsm.act("XFER",
            NextValue(clk_en, 1),
            dq_oe2.eq(sink.mask),
            NextValue(dq_oe1, dq_oe2),

            Case(sink.width, dout_width_cases),
            Case(sink.width, din_width_cases),
            NextValue(usr_dout, usr_dout<<sink.width),

            NextValue(shift_cnt, shift_cnt+sink.width),
            If(shift_cnt == (sink.len-sink.width),
                NextValue(shift_cnt, 0),
                NextState("XFER-END"),
            ),
        )
        fsm.act("XFER-END",
            NextValue(clk_en, 0),
            Case(sink.width, din_width_cases),
            NextValue(dq_i1, 0),
            NextValue(shift_cnt, shift_cnt+sink.width),
            If(shift_cnt == ((2+2*extra_latency)*sink.width),
                sink.ready.eq(1),
                NextValue(shift_cnt, 0),
                NextState("SEND-STATUS-DATA"),
            ),
        )
        fsm.act("SEND-STATUS-DATA",
            source.valid.eq(1),
            source.last.eq(1),
            source.data.eq(usr_din),
            If(source.ready,
                NextState("WAIT-CMD-DATA"),
            )
        )
