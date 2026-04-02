#
# This file is part of LiteSPI
#
# Copyright (c) 2020-2021 Antmicro <www.antmicro.com>
# Copyright (c) 2021 Florent Kermarrec <florent@enjoy-digital.fr>
# Copyright (c) 2025 Fin Maaß <f.maass@vogl-electronic.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *

from litex.gen import *

from litespi.common import *
from litespi.clkgen import LiteSPIClkGen2
from litespi.cscontrol import LiteSPICSControl

from litex.soc.interconnect import stream
from litex.soc.interconnect.csr import *

from litex.build.io import DDRTristate


# LiteSPI PHY Core ---------------------------------------------------------------------------------

class LiteSPIDDRPHYCore2(LiteXModule):
    """LiteSPI PHY instantiator

    The ``LiteSPIPHYCore`` class provides a generic PHY that can be connected to the ``LiteSPICore``.

    It supports single/dual/quad/octal output reads from the flash chips.

    You can use this class only with devices that supports the DDR primitives.

    Parameters
    ----------
    pads : Object
        SPI pads description.

    flash : SpiNorFlashModule
        SpiNorFlashModule configuration object.

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
    def __init__(self, pads, flash, clock_domain, default_divisor=9, extra_latency=0, **kwargs):
        self.source           = source = stream.Endpoint(spi_phy2core_layout)
        self.sink             = sink   = stream.Endpoint(spi_core2phy_layout)
        self.cs               = Signal().like(pads.cs_n)
        self._spi_clk_divisor = spi_clk_divisor = Signal(len(sink.clk_div))

        self._default_divisor = default_divisor

        self.clk_divisor      = clk_divisor = CSRStorage(len(sink.clk_div), reset=self._default_divisor)

        # # #

        # Resynchronize CSR Clk Divisor to LiteSPI Clk Domain.
        self.submodules += ResyncReg(clk_divisor.storage, spi_clk_divisor, clock_domain)

        if hasattr(pads, "miso"):
            bus_width = 1
            dq_len    = 2
            pads.dq   = [pads.mosi, pads.miso]
        else:
            bus_width = dq_len = len(pads.dq) if not hasattr(pads.dq, "o") else len(pads.dq.o)

        assert bus_width in [1, 2, 4, 8]

        if flash:
            # Check if number of pads matches configured mode.
            assert flash.check_bus_width(bus_width)
            assert not flash.ddr

        # Clock Generator.
        self.clkgen = clkgen = LiteSPIClkGen2(pads, div_width=len(sink.clk_div), extra_latency=2*extra_latency)

        # CS control.
        self.cs_control = cs_control = LiteSPICSControl(pads, self.cs, **kwargs)

        spi_clk_divisor_delayed = Signal(len(sink.clk_div))

        self.comb += clkgen.div.eq(spi_clk_divisor_delayed)

        dq_o  = Array([Signal(dq_len, name="dq_o"+str(n)) for n in range(2)])
        dq_i  = Array([Signal(dq_len, name="dq_i"+str(n)) for n in range(2)])
        dq_oe = Signal(dq_len)
        last_dq_oe = Signal(dq_len)

        self.specials += DDRTristate(
            io  = pads.dq,
            o1  =  dq_o[0],  o2 =  dq_o[1],
            i1  =  dq_i[0],  i2 =  dq_i[1],
            oe1 =  dq_oe,
        )

        # Data Shift Registers.
        sr_out_cnt   = Signal(len(sink.len), reset_less=True)
        sr_in_cnt    = Signal(len(sink.len), reset_less=True)
        sr_out_load  = Signal()
        sr_out_shift = Signal(2)
        sr_out       = Signal(len(sink.data), reset_less=True)
        sr_out_shifted = Signal(len(sink.data), reset_less=True)
        sr_out_loaded  = Signal(len(sink.data), reset_less=True)
        sr_in_shift  = Signal(2)
        sr_in        = Signal(len(sink.data), reset_less=True)

        no_read = Signal()
        last_sink_width = Signal.like(sink.width)

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

        # Data Out Shift.
        self.comb += [
            dq_oe.eq(last_dq_oe),
            Case(last_sink_width, {
                1:  dq_o[1].eq(sr_out[-1:]),
                2:  dq_o[1].eq(sr_out[-2:]),
                4:  dq_o[1].eq(sr_out[-4:]),
                8:  dq_o[1].eq(sr_out[-8:]),
            }),
            sr_out_shifted.eq(sr_out << last_sink_width),
            sr_out_loaded.eq(sink.data << (len(sink.data) - sink.len))
        ]
        self.sync += If(sr_out_load,
            sr_in.eq(0),
            sr_out.eq(sr_out_loaded),
            Case(sink.width, {
                1:  dq_o[0].eq(sr_out_loaded[-1:]),
                2:  dq_o[0].eq(sr_out_loaded[-2:]),
                4:  dq_o[0].eq(sr_out_loaded[-4:]),
                8:  dq_o[0].eq(sr_out_loaded[-8:]),
            }),
            sr_out_cnt.eq(sink.len - sink.width),
            sr_in_cnt.eq(sink.len),
        ).Elif(sr_out_shift[0],
            Case(last_sink_width, {
                1:  dq_o[0].eq(sr_out_shifted[-1:]),
                2:  dq_o[0].eq(sr_out_shifted[-2:]),
                4:  dq_o[0].eq(sr_out_shifted[-4:]),
                8:  dq_o[0].eq(sr_out_shifted[-8:]),
            }),
            sr_out.eq(sr_out_shifted),
            sr_out_cnt.eq(sr_out_cnt - last_sink_width),
        ).Elif(sr_out_shift[1],
            dq_o[0].eq(dq_o[1]),
            sr_out.eq(sr_out_shifted),
            sr_out_cnt.eq(sr_out_cnt - last_sink_width),
        ).Else(
            dq_o[0].eq(dq_o[1]),
        )

        # Data In Shift.
        self.sync += If(sr_in_shift[0],
            Case(last_sink_width, {
                1 : sr_in.eq(Cat(dq_i[0][1],  sr_in)), # 1: pads.miso
                2 : sr_in.eq(Cat(dq_i[0][:2], sr_in)),
                4 : sr_in.eq(Cat(dq_i[0][:4], sr_in)),
                8 : sr_in.eq(Cat(dq_i[0][:8], sr_in)),
            }),
            sr_in_cnt.eq(sr_in_cnt - last_sink_width),
        ).Elif(sr_in_shift[1],
            Case(last_sink_width, {
                1 : sr_in.eq(Cat(dq_i[1][1],  sr_in)), # 1: pads.miso
                2 : sr_in.eq(Cat(dq_i[1][:2], sr_in)),
                4 : sr_in.eq(Cat(dq_i[1][:4], sr_in)),
                8 : sr_in.eq(Cat(dq_i[1][:8], sr_in)),
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
                NextValue(last_sink_width, sink.width),
                NextValue(last_dq_oe, sink.mask),
                dq_oe.eq(sink.mask),
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
            sr_in_shift.eq(clkgen.posedge_reg2),

            # Data Out Shift.
            sr_out_shift.eq(clkgen.negedge),

            # Shift Register Count Update/Check.
            If((self.clkgen.negedge != 0) & (sr_out_cnt == 0),
                self.clkgen.en.eq(0),
                NextState("XFER-END"),
                If(no_read | (sr_in_cnt == 0) | ((clkgen.posedge_reg2 != 0) & (sr_in_cnt == last_sink_width)),
                    NextState("SEND-STATUS-DATA"),
                ),
            ),

        )
        fsm.act("XFER-END",
            sr_in_shift.eq(clkgen.posedge_reg2),
            If((clkgen.posedge_reg2 != 0) & (sr_in_cnt == last_sink_width),
                # Send Status/Data to Core.
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
