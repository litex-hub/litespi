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

        dq_o  = Array([Signal(len(pads.dq)) for _ in range(2)])
        dq_i  = Array([Signal(len(pads.dq)) for _ in range(2)])
        dq_oe = Array([Signal(len(pads.dq)) for _ in range(2)])

        for i in range(len(pads.dq)):
            self.specials += DDRTristate(
                io  = pads.dq[i],
                o1  = dq_o[0][i],   o2 = dq_o[1][i],
                oe1 = dq_oe[0][i], oe2 = dq_oe[1][i],
                i1  = dq_i[0][i],  i2  = dq_i[1][i]
            )

        # Data Shift Registers.
        sr_cnt       = Signal(8, reset_less=True)
        sr_out_load  = Signal()
        sr_out_shift = Signal()
        sr_out       = Signal(len(sink.data), reset_less=True)
        sr_in_shift  = Signal()
        sr_in        = Signal(len(sink.data), reset_less=True)

        # Data Out Shift.
        self.comb += [
            Case(sink.width, {
                1:  dq_i[1].eq(sr_out[-1:]),
                2:  dq_i[1].eq(sr_out[-2:]),
                4:  dq_i[1].eq(sr_out[-4:]),
                8:  dq_i[1].eq(sr_out[-8:]),
            })
        ]
        self.sync += If(sr_out_load,
            sr_out.eq(sink.data << (len(sink.data) - sink.len))
        )
        self.sync += If(sr_out_shift, dq_i[0].eq(dq_i[1]))

        # Data In Shift.
        self.sync += If(sr_in_shift,
            Case(sink.width, {
                1 : sr_in.eq(Cat(dq_o[0][1],  sr_in)), # 1: pads.miso
                2 : sr_in.eq(Cat(dq_o[0][:2], sr_in)),
                4 : sr_in.eq(Cat(dq_o[0][:4], sr_in)),
                8 : sr_in.eq(Cat(dq_o[0][:8], sr_in)),
            })
        )

        # FSM.
        self.submodules.fsm = fsm = FSM(reset_state="WAIT-CMD-DATA")
        fsm.act("WAIT-CMD-DATA",
            NextValue(clkgen.en, 0),
            If(cs_enable & sink.valid,
                sr_out_load.eq(1),
                NextState("XFER")
            )
        )

        fsm.act("XFER",
            NextValue(clkgen.en, 1),
            dq_oe[1].eq(sink.mask),
            NextValue(dq_oe[0], dq_oe[1]),
            sr_in_shift.eq(1),
            sr_out_shift.eq(1),
            NextValue(sr_out, sr_out<<sink.width),
            NextValue(sr_cnt, sr_cnt+sink.width),
            If(sr_cnt == (sink.len-sink.width),
                NextValue(sr_cnt, 0),
                NextState("XFER-END"),
            ),
        )
        fsm.act("XFER-END",
            NextValue(clkgen.en, 0),
            sr_in_shift.eq(1),
            NextValue(dq_i[0], 0),
            NextValue(sr_cnt, sr_cnt+sink.width),
            If(sr_cnt == ((2+2*extra_latency)*sink.width),
                sink.ready.eq(1),
                NextValue(sr_cnt, 0),
                NextState("SEND-STATUS-DATA"),
            ),
        )
        fsm.act("SEND-STATUS-DATA",
            source.valid.eq(1),
            source.last.eq(1),
            source.data.eq(sr_in),
            If(source.ready,
                NextState("WAIT-CMD-DATA"),
            )
        )
