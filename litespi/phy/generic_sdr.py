#
# This file is part of LiteSPI
#
# Copyright (c) 2020-2021 Antmicro <www.antmicro.com>
# Copyright (c) 2021 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *

from litex.gen import *

from litespi.common import *
from litespi.clkgen import LiteSPIClkGen
from litespi.cscontrol import LiteSPICSControl

from litex.soc.interconnect import stream
from litex.soc.interconnect.csr import *

from litex.build.io import SDROutput, SDRInput, SDRTristate

# LiteSPI PHY Core ---------------------------------------------------------------------------------

class LiteSPISDRPHYCore(LiteXModule):
    """LiteSPI PHY instantiator

    The ``LiteSPIPHYCore`` class provides a generic PHY that can be connected to the ``LiteSPICore``.

    It supports single/dual/quad/octal output reads from the flash chips.

    The following diagram shows how each clock configuration option relates to outputs and input sampling in DDR mode:

    .. wavedrom:: ../../doc/ddr-timing-diagram.json

    Parameters
    ----------
    pads : Object
        SPI pads description.

    flash : SpiNorFlashModule
        SpiNorFlashModule configuration object.

    device : str
        Device type for use by the ``LiteSPIClkGen``.

    default_divisor : int
        Default frequency divisor for clkgen.

    Attributes
    ----------
    source : Endpoint(spi_phy2core_layout), out
        Data stream.

    sink : Endpoint(spi_core2phy_layout), in
        Control stream.

    cs : Signal(), in
        Flash CS signal.

    clk_divisor : CSRStorage
        Register which holds a clock divisor value applied to clkgen.
    """
    def __init__(self, pads, flash, device, clock_domain, default_divisor, cs_delay, extra_latency=0, **kwargs):
        self.source           = source = stream.Endpoint(spi_phy2core_layout)
        self.sink             = sink   = stream.Endpoint(spi_core2phy_layout)
        self.cs               = Signal().like(pads.cs_n)
        self._spi_clk_divisor = spi_clk_divisor = Signal(8)

        self._default_divisor = default_divisor

        self.clk_divisor      = clk_divisor = CSRStorage(8, reset=self._default_divisor)

        # # #

        # Resynchronize CSR Clk Divisor to LiteSPI Clk Domain.
        self.submodules += ResyncReg(clk_divisor.storage, spi_clk_divisor, clock_domain)

        # Determine SPI Bus width and DQs.
        if hasattr(pads, "mosi"):
            bus_width = 1
        else:
            bus_width = len(pads.dq)
        assert bus_width in [1, 2, 4, 8]

        if flash:
            # Check if number of pads matches configured mode.
            assert flash.check_bus_width(bus_width)
            assert not flash.ddr

        # Clock Generator.
        self.clkgen = clkgen = LiteSPIClkGen(pads, device, extra_latency=extra_latency)

        # CS control.
        self.cs_control = cs_control = LiteSPICSControl(pads, self.cs, cs_delay)

         # Only Clk Divisor when not active.
        self.sync += If(~cs_control.enable, clkgen.div.eq(spi_clk_divisor))

        if hasattr(pads, "mosi"):
            dq_o  = Signal()
            dq_i  = Signal(2)
            dq_oe = Signal() # Unused.
            self.specials += SDROutput(
                i = dq_o,
                o = pads.mosi
            )
            self.specials += SDRInput(
                i = pads.miso,
                o = dq_i[1]
            )
        else:
            dq_o  = Signal().like(pads.dq)
            dq_i  = Signal().like(pads.dq)
            dq_oe = Signal().like(pads.dq)
            self.specials += SDRTristate(
                    io = pads.dq,
                    o  = dq_o,
                    oe = dq_oe,
                    i  = dq_i,
                )

        # Data Shift Registers.
        sr_out_cnt   = Signal(len(sink.len), reset_less=True)
        sr_in_cnt    = Signal(len(sink.len), reset_less=True)
        sr_out_load  = Signal()
        sr_out_shift = Signal()
        sr_out       = Signal().like(sink.data)
        sr_in_shift  = Signal()
        sr_in        = Signal().like(sink.data)

        # Data Out Generation/Load/Shift.
        self.comb += [
            Case(sink.width, {
                1 : dq_o.eq(sr_out[-1:]),
                2 : dq_o.eq(sr_out[-2:]),
                4 : dq_o.eq(sr_out[-4:]),
                8 : dq_o.eq(sr_out[-8:]),
            })
        ]
        self.sync += If(sr_out_load,
            sr_out.eq(sink.data << (len(sink.data) - sink.len)),
            sr_in.eq(0),
        )
        self.sync += If(sr_out_shift,
            sr_out.eq(sr_out << sink.width),
        )

        # Data In Shift.
        self.sync += If(sr_in_shift,
            Case(sink.width, {
                1 : sr_in.eq(Cat(dq_i[1], sr_in)),
                2 : sr_in.eq(Cat(dq_i[:2], sr_in)),
                4 : sr_in.eq(Cat(dq_i[:4], sr_in)),
                8 : sr_in.eq(Cat(dq_i[:8], sr_in)),
            })
        )

        # FSM.
        self.fsm = fsm = FSM(reset_state="WAIT-CMD-DATA")
        fsm.act("WAIT-CMD-DATA",
            # Wait for CS and a CMD from the Core.
            If(cs_control.enable & sink.valid,
                # Load Shift Register Count/Data Out.
                NextValue(sr_out_cnt, sink.len - sink.width),
                NextValue(sr_in_cnt, sink.len),
                NextValue(dq_oe, sink.mask),
                sr_out_load.eq(1),
                # Start XFER.
                NextState("XFER"),
            ),
        )
        fsm.act("XFER",
            # Generate Clk.
            self.clkgen.en.eq(1),

            # Data In Shift.
            If(clkgen.posedge_reg2, sr_in_shift.eq(1)),

            # Data Out Shift.
            If(clkgen.negedge, sr_out_shift.eq(1)),

            # Shift Register Count Update/Check.
            If(clkgen.posedge_reg2,
                NextValue(sr_in_cnt, sr_in_cnt - sink.width),
            ),
            If(self.clkgen.negedge,
                NextValue(sr_out_cnt, sr_out_cnt - sink.width),
                # End XFer.
                If(sr_out_cnt == 0,
                    NextState("XFER-END"),
                ),
            ),

        )
        fsm.act("XFER-END",
            If(sr_in_cnt == 0,
                sink.ready.eq(1),
                # Send Status/Data to Core.
                NextState("SEND-STATUS-DATA"),
            ).Else(
                sr_in_shift.eq(clkgen.posedge_reg2),
                If(clkgen.posedge_reg2,
                    NextValue(sr_in_cnt, sr_in_cnt - sink.width),
                    If(sr_in_cnt == sink.width,
                       sink.ready.eq(1),
                       # Send Status/Data to Core.
                       NextState("SEND-STATUS-DATA"),
                    ),
                ),
            ),
        )
        self.comb += source.data.eq(sr_in)
        fsm.act("SEND-STATUS-DATA",
            # Send Data In to Core and return to WAIT when accepted.
            source.valid.eq(1),
            NextValue(dq_oe, 0),
            If(source.ready,
                NextState("WAIT-CMD-DATA"),
            )
        )
