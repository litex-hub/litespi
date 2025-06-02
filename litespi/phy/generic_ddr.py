#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *

from litex.gen import *

from litex.gen.genlib.misc import WaitTimer

from litespi.common import *
from litespi.clkgen import DDRLiteSPIClkGen
from litespi.cscontrol import LiteSPICSControl

from litex.soc.interconnect import stream

from litex.build.io import DDRTristate

# LiteSPI DDR PHY Core -----------------------------------------------------------------------------

class LiteSPIDDRPHYCore(LiteXModule):
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
        self.cs              = Signal().like(pads.cs_n)

        if hasattr(pads, "miso"):
            bus_width = 1
            pads.dq   = [pads.mosi, pads.miso]
        else:
            bus_width = len(pads.dq)

        assert bus_width in [1, 2, 4, 8]

        if flash:
            # Check if number of pads matches configured mode.
            assert flash.check_bus_width(bus_width)
            assert not flash.ddr

        # Clock Generator.
        self.clkgen = clkgen = DDRLiteSPIClkGen(pads)

        # CS control.
        self.cs_control = cs_control = LiteSPICSControl(pads, self.cs, cs_delay)

        dq_o  = Array([Signal(len(pads.dq)) for _ in range(2)])
        dq_i  = Array([Signal(len(pads.dq)) for _ in range(2)])
        dq_oe = Array([Signal(len(pads.dq)) for _ in range(2)])

        self.specials += DDRTristate(
            io  = pads.dq,
            o1  =  dq_o[0],  o2 =  dq_o[1],
            oe1 = dq_oe[0], oe2 = dq_oe[1],
            i1  =  dq_i[0],  i2 =  dq_i[1]
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
            dq_oe[1].eq(sink.mask),
            Case(sink.width, {
                1:  dq_o[1].eq(sr_out[-1:]),
                2:  dq_o[1].eq(sr_out[-2:]),
                4:  dq_o[1].eq(sr_out[-4:]),
                8:  dq_o[1].eq(sr_out[-8:]),
            })
        ]
        self.sync += If(sr_out_load,
            sr_out.eq(sink.data << (len(sink.data) - sink.len))
        )
        self.sync += If(sr_out_shift,
            dq_oe[0].eq(dq_oe[1]),
            dq_o[0].eq(dq_o[1]),
            Case(sink.width, {
                1 : sr_out.eq(Cat(Signal(1), sr_out)),
                2 : sr_out.eq(Cat(Signal(2), sr_out)),
                4 : sr_out.eq(Cat(Signal(4), sr_out)),
                8 : sr_out.eq(Cat(Signal(8), sr_out)),
            })
        )

        # Data In Shift.
        self.sync += If(sr_in_shift,
            Case(sink.width, {
                1 : sr_in.eq(Cat(dq_i[0][1],  sr_in)), # 1: pads.miso
                2 : sr_in.eq(Cat(dq_i[0][:2], sr_in)),
                4 : sr_in.eq(Cat(dq_i[0][:4], sr_in)),
                8 : sr_in.eq(Cat(dq_i[0][:8], sr_in)),
            })
        )

        # FSM.
        self.fsm = fsm = FSM(reset_state="WAIT-CMD-DATA")
        fsm.act("WAIT-CMD-DATA",
            # Stop Clk.
            NextValue(clkgen.en, 0),
            # Wait for CS and a CMD from the Core.
            If(cs_control.enable & sink.valid,
                # Load Shift Register Count/Data Out.
                NextValue(sr_cnt, sink.len - sink.width),
                sr_out_load.eq(1),
                # Start XFER.
                NextState("XFER")
            )
        )

        fsm.act("XFER",
            # Generate Clk.
            NextValue(clkgen.en, 1),

            # Data In Shift.
            sr_in_shift.eq(1),

            # Data Out Shift.
            sr_out_shift.eq(1),

            # Shift Register Count Update/Check.
            NextValue(sr_cnt, sr_cnt - sink.width),
            # End XFer.
            If(sr_cnt == 0,
                NextValue(sr_cnt, (2 + 2*extra_latency)*sink.width), # FIXME: Explain magic numbers.
                NextState("XFER-END"),
            ),
        )
        fsm.act("XFER-END",
            # Stop Clk.
            NextValue(clkgen.en, 0),

            # Data In Shift.
            sr_in_shift.eq(1),

            # Shift Register Count Update/Check.
            NextValue(sr_cnt, sr_cnt - sink.width),
            If(sr_cnt == 0,
                sink.ready.eq(1),
                NextState("SEND-STATUS-DATA"),
            ),
        )
        self.comb += source.data.eq(sr_in)
        fsm.act("SEND-STATUS-DATA",
            # Send Data In to Core and return to WAIT when accepted.
            source.valid.eq(1),
            If(source.ready,
                NextState("WAIT-CMD-DATA"),
            )
        )
