#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# Copyright (c) 2025-2026 Fin Maaß <f.maass@vogl-electronic.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *

from litex.gen import *

from litespi.common import *
from litespi.clkgen import DDRLiteSPIClkGen
from litespi.cscontrol import LiteSPICSControl

from litex.soc.interconnect import stream
from litex.soc.interconnect.csr import *

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

    extra_latency : int or float
        Additional input pipeline latency. Each 0.5 adds one system-clock cycle.

    clock_domain : str
        Name of the LiteSPI clock domain.

    default_divisor : int
        Default SCK divisor.

    Attributes
    ----------
    source : Endpoint(spi_phy2core_layout), out
        Data stream.

    sink : Endpoint(spi_core2phy_layout), in
        Control stream.

    cs : Signal(), in
        Flash CS signal.

    clk_divisor : CSRStorage
        Register which holds the default SCK divisor.
    """
    def __init__(self, pads, flash, extra_latency=0, clock_domain="sys", default_divisor=1, **kwargs):
        self.source           = source = stream.Endpoint(spi_phy2core_layout)
        self.sink             = sink   = stream.Endpoint(spi_core2phy_layout)
        self.cs                        = Signal().like(pads.cs_n)
        self._spi_clk_divisor = spi_clk_divisor = Signal(len(sink.clk_div))

        self._default_divisor = default_divisor
        self.clk_divisor      = CSRStorage(
            len(sink.clk_div),
            reset=self._default_divisor,
            description="SPI clock divisor.",
        )

        # # #

        # Resynchronize CSR Clock Divisor to LiteSPI Clock Domain.
        self.submodules += ResyncReg(self.clk_divisor.storage, spi_clk_divisor, clock_domain)

        if hasattr(pads, "miso"):
            bus_width = 1
            dq        = Cat(pads.mosi, pads.miso)
        else:
            bus_width = len(pads.dq)
            dq        = pads.dq

        assert bus_width in [1, 2, 4, 8]

        if flash:
            # Check if number of pads matches configured mode.
            assert flash.check_bus_width(bus_width)
            assert not flash.ddr

        # Clock Generator.
        self.clkgen = clkgen = DDRLiteSPIClkGen(
            pads          = pads,
            div_width     = len(sink.clk_div),
            extra_latency = extra_latency,
        )
        self.comb += clkgen.div.eq(spi_clk_divisor)

        # CS control.
        self.cs_control = cs_control = LiteSPICSControl(pads, self.cs, **kwargs)

        # Lane 0 is output while sys is high and lane 1 while sys is low.
        dq_o  = Array([Signal(len(dq)) for _ in range(2)])
        dq_i  = Array([Signal(len(dq)) for _ in range(2)])
        dq_oe = Signal(len(dq))

        self.specials += DDRTristate(
            io  = dq,
            o1  =  dq_o[0],  o2 =  dq_o[1],
            oe1 = dq_oe,
            i1  =  dq_i[0],  i2 =  dq_i[1]
        )

        # Data Shift Registers.
        sr_out_cnt     = Signal(len(sink.len), reset_less=True)
        sr_in_cnt      = Signal(len(sink.len), reset_less=True)
        sr_out_load    = Signal()
        sr_out_shift   = Signal()
        sr_out         = Signal(len(sink.data), reset_less=True)
        sr_out_shifted = Signal(len(sink.data), reset_less=True)
        sr_in_shift    = Signal()
        sr_in          = Signal(len(sink.data), reset_less=True)
        current_data   = Signal(len(dq))
        next_data      = Signal(len(dq))
        last_width     = Signal.like(sink.width)
        no_read        = Signal()

        # Determine if the transfer only drives DQ and can skip the input-pipeline drain.
        self.sync += If(sr_out_load,
            Case(sink.width, {
                "default" : no_read.eq(0),
                1 : no_read.eq(sink.mask[0]),
                2 : no_read.eq(sink.mask[:2] == 0b11),
                4 : no_read.eq(sink.mask[:4] == 0b1111),
                8 : no_read.eq(sink.mask == 0xff),
            })
        )

        # Keep DQ stable until SCK falls. For odd divisors SCK falls between the two DDR lanes;
        # for even divisors it falls at the beginning of lane 0.
        self.comb += [
            sr_out_shifted.eq(sr_out << last_width),
            Case(last_width, {
                1 : [current_data.eq(sr_out[-1:]), next_data.eq(sr_out_shifted[-1:])],
                2 : [current_data.eq(sr_out[-2:]), next_data.eq(sr_out_shifted[-2:])],
                4 : [current_data.eq(sr_out[-4:]), next_data.eq(sr_out_shifted[-4:])],
                8 : [current_data.eq(sr_out[-8:]), next_data.eq(sr_out_shifted[-8:])],
            }),
            dq_o[0].eq(Mux(clkgen.negedge[0], next_data, current_data)),
            dq_o[1].eq(Mux(clkgen.negedge != 0, next_data, current_data)),
        ]

        self.sync += If(sr_out_load,
            sr_out.eq(sink.data << (len(sink.data) - sink.len)),
            sr_in.eq(0),
            sr_out_cnt.eq(sink.len),
            sr_in_cnt.eq(sink.len),
        ).Elif(sr_out_shift,
            sr_out.eq(sr_out_shifted),
            sr_out_cnt.eq(sr_out_cnt - last_width),
        )

        # SCK rising edges are always aligned to lane 0.
        self.sync += If(sr_in_shift,
            Case(last_width, {
                1 : sr_in.eq(Cat(dq_i[0][1],  sr_in)), # 1: pads.miso
                2 : sr_in.eq(Cat(dq_i[0][:2], sr_in)),
                4 : sr_in.eq(Cat(dq_i[0][:4], sr_in)),
                8 : sr_in.eq(Cat(dq_i[0][:8], sr_in)),
            }),
            sr_in_cnt.eq(sr_in_cnt - last_width),
        )

        # FSM.
        self.fsm = fsm = FSM(reset_state="WAIT-CMD-DATA")
        fsm.act("WAIT-CMD-DATA",
            # Wait for CS and a command from the Core.
            If(cs_control.enable & sink.valid,
                clkgen.start.eq(1),
                NextValue(last_width, sink.width),
                NextValue(dq_oe, sink.mask),
                sr_out_load.eq(1),
                sink.ready.eq(1),
                If(sink.clk_div > 0,
                    clkgen.div.eq(sink.clk_div),
                ),
                NextState("XFER"),
            )
        )
        fsm.act("XFER",
            clkgen.en.eq(1),

            # Capture registered input data after each delayed SCK rising edge.
            If(clkgen.sample,
                sr_in_shift.eq(1),
            ),

            # Advance output data after each SCK falling edge.
            If(clkgen.negedge != 0,
                sr_out_shift.eq(1),
                If(sr_out_cnt == last_width,
                    clkgen.en.eq(0),
                    NextValue(dq_oe, 0),
                    If(no_read | (sr_in_cnt == 0) | (clkgen.sample & (sr_in_cnt == last_width)),
                        NextState("SEND-STATUS-DATA"),
                    ).Else(
                        NextState("XFER-END"),
                    )
                )
            )
        )
        fsm.act("XFER-END",
            # Drain input events that are still crossing the IDDR/fabric pipeline.
            If(clkgen.sample,
                sr_in_shift.eq(1),
                If(sr_in_cnt == last_width,
                    NextState("SEND-STATUS-DATA"),
                )
            )
        )
        self.comb += source.data.eq(sr_in)
        fsm.act("SEND-STATUS-DATA",
            source.valid.eq(1),
            If(source.ready,
                NextState("WAIT-CMD-DATA"),
            )
        )
