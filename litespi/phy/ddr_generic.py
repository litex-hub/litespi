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


# LiteSPI PHY DDR Core ---------------------------------------------------------------------------------

class DDRLiteSPIPHYCore(Module, AutoCSR, AutoDoc, ModuleDoc):
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
    def __init__(self, pads, flash, cs_delay):
        self.source              = source = stream.Endpoint(spi_phy2core_layout)
        self.sink                = sink   = stream.Endpoint(spi_core2phy_layout)
        self.cs                  = Signal()

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
        cs_timer = WaitTimer(cs_delay + 1) # Ensure cs_delay cycles between XFers.
        cs_out   = Signal()
        self.submodules += cs_timer
        self.comb += cs_timer.wait.eq(self.cs)
        self.comb += cs_out.eq(cs_timer.done)
        self.comb += pads.cs_n.eq(~cs_out)

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
        addr      = Signal(addr_bits if not ddr else addr_bits + addr_width, reset_less=True)
        data      = Signal(data_bits, reset_less=True)

        usr_dout  = Signal(len(sink.data),  reset_less=True)
        usr_din   = Signal(len(sink.data),  reset_less=True)
        usr_len   = Signal(len(sink.len),   reset_less=True)
        usr_width = Signal(len(sink.width), reset_less=True)
        usr_mask  = Signal(len(sink.mask),  reset_less=True)

        new_din   = Signal(len(sink.data),  reset_less=True)
        new_dout  = Signal(len(sink.data),  reset_less=True)

        clk_en = Signal()

        self.comb += self.clkgen.en.eq(clk_en)

        new_din_cases = {1: [
                new_din.eq(Cat(dq_o1[1], usr_din)),
            ]
        }

        for i in [2, 4, 8]:
            new_din_cases[i] = [
                new_din.eq(Cat(dq_o1[0:i], usr_din))
            ]

        new_dout_cases = {}
        for i in [1, 2, 4, 8]:
            new_dout_cases[i] = [
                dq_i2.eq(new_dout[-i:]),
            ]

        self.sync += [
            dq_i1.eq(dq_i2),
            dq_oe1.eq(dq_oe2),
        ]

        def shift_out(mask, data, data_new, width):
            return [
                dq_oe2.eq(mask),
                new_dout.eq(data),
                Case(width, new_dout_cases),
                NextValue(data_new, data<<width),
            ]

        self.submodules.fsm = fsm = FSM(reset_state="IDLE")
        fsm.act("IDLE",
            sink.ready.eq(cs_out),
            NextValue(clk_en, 0),
            If(sink.valid & sink.ready,
                Case(sink.cmd, {
                    USER: [
                        shift_out(sink.mask, sink.data << (32-sink.len), usr_dout, sink.width),
                        NextValue(usr_din,   0),
                        NextValue(usr_len,   sink.len-sink.width),
                        NextValue(usr_width, sink.width),
                        NextValue(usr_mask,  sink.mask),

                        NextValue(clk_en, 1),
                        NextState("USER")
                    ]
                })
            )
        )

        fsm.act("USER",
            shift_out(usr_mask, usr_dout, usr_dout, usr_width),
            Case(usr_width, new_din_cases),
            NextValue(usr_din, new_din),

            NextValue(shift_cnt, shift_cnt+usr_width),
            If(shift_cnt == (usr_len-usr_width),
                NextValue(shift_cnt, 0),
                NextState("USER_END"),
            ),
        )

        return_data = [
                source.valid.eq(1),
                source.last.eq(1),
                source.data.eq(new_din),
        ]

        fsm.act("USER_END",
            NextValue(clk_en, 0),
            Case(usr_width, new_din_cases),

            NextValue(usr_din, new_din),
            NextValue(shift_cnt, shift_cnt+usr_width),

            If(shift_cnt == (2*usr_width),
                return_data,
                If(source.ready,
                    NextState("IDLE"),
                ).Else(
                    NextState("SEND_USER_DATA"),
                ),
                NextValue(shift_cnt, 0),
            ),
        )
        fsm.act("SEND_USER_DATA",
            return_data,
            If(source.ready,
                NextState("IDLE"),
            )
        )
