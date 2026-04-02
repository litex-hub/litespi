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
    def __init__(self, pads, flash, device, clock_domain, default_divisor=9, extra_latency=0, **kwargs):
        self.source           = source = stream.Endpoint(spi_phy2core_layout)
        self.sink             = sink   = stream.Endpoint(spi_core2phy_layout)
        self.cs               = Signal().like(pads.cs_n)
        self._spi_clk_divisor = spi_clk_divisor = Signal(len(sink.clk_div))

        self._default_divisor = default_divisor

        self.clk_divisor      = clk_divisor = CSRStorage(len(sink.clk_div), reset=self._default_divisor)

        self.mode = mode = CSRStorage(2, reset=3, description="SPI mode (CPOL/CPHA). Curently only mode 0 and 3 are supported.") 

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
        self.clkgen = clkgen = LiteSPIClkGen(pads, device, div_width=len(sink.clk_div), extra_latency=extra_latency)

        self.submodules += ResyncReg(mode.storage, clkgen.mode, clock_domain)

        # CS control.
        self.cs_control = cs_control = LiteSPICSControl(pads, self.cs, **kwargs)

        spi_clk_divisor_delayed = Signal(len(sink.clk_div))

        self.comb += clkgen.div.eq(spi_clk_divisor_delayed)

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

        no_read = Signal()
        last_sink_width = Signal.like(sink.width)

        if not hasattr(pads, "mosi"):
            # Determine if no read is expected based on mask for current transfer width,
            # so we can skip waiting for data in the case of write-only transfers.
            self.sync += If(sr_out_load,
                Case(sink.width, {
                    "default" : no_read.eq(0),
                    2 : no_read.eq(sink.mask == 0b00000011),
                    4 : no_read.eq(sink.mask == 0b00001111),
                    8 : no_read.eq(sink.mask == 0b11111111),
                })
            )

        # Data Out Generation/Load/Shift.
        self.comb += [
            Case(last_sink_width, {
                1 : dq_o.eq(sr_out[-1:]),
                2 : dq_o.eq(sr_out[-2:]),
                4 : dq_o.eq(sr_out[-4:]),
                8 : dq_o.eq(sr_out[-8:]),
            })
        ]
        self.sync += If(sr_out_load,
            sr_out.eq(sink.data << (len(sink.data) - sink.len)),
            sr_in.eq(0),
            sr_out_cnt.eq(sink.len - sink.width),
            sr_in_cnt.eq(sink.len),
        )
        self.sync += If(sr_out_shift,
            sr_out.eq(sr_out << last_sink_width),
            sr_out_cnt.eq(sr_out_cnt - last_sink_width),
        )

        # Data In Shift.
        self.sync += If(sr_in_shift,
            Case(last_sink_width, {
                1 : sr_in.eq(Cat(dq_i[1], sr_in)),
                2 : sr_in.eq(Cat(dq_i[:2], sr_in)),
                4 : sr_in.eq(Cat(dq_i[:4], sr_in)),
                8 : sr_in.eq(Cat(dq_i[:8], sr_in)),
            }),
            sr_in_cnt.eq(sr_in_cnt - last_sink_width),
        )

        # FSM.
        self.fsm = fsm = FSM(reset_state="WAIT-CMD-DATA")
        fsm.act("WAIT-CMD-DATA",
            NextValue(spi_clk_divisor_delayed, spi_clk_divisor),
            # Wait for CS and a CMD from the Core.
            If(cs_control.enable & sink.valid,
                self.clkgen.start.eq(1),
                NextValue(dq_oe, sink.mask),
                NextValue(last_sink_width, sink.width),
                sr_out_load.eq(1),
                sink.ready.eq(1),
                If(sink.clk_div > 0,
                    clkgen.div.eq(sink.clk_div),
                    NextValue(spi_clk_divisor_delayed, sink.clk_div),
                ),
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
            If(self.clkgen.negedge,
                sr_out_shift.eq(1),
                # End XFer.
                If(sr_out_cnt == 0,
                    self.clkgen.en.eq(0),
                    NextState("XFER-END"),
                    If(no_read | (sr_in_cnt == 0) | (clkgen.posedge_reg2 & (sr_in_cnt == last_sink_width)),
                        NextState("SEND-STATUS-DATA"),
                    ),
                ),
            ),

        )
        fsm.act("XFER-END",
            If(clkgen.posedge_reg2,
                sr_in_shift.eq(1),
                If(sr_in_cnt == last_sink_width,
                    # Send Status/Data to Core.
                    NextState("SEND-STATUS-DATA"),
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
