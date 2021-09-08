#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *
from migen.genlib.misc import WaitTimer

from litespi.common import *
from litespi.clkgen import LiteSPIClkGen

from litex.soc.interconnect import stream
from litex.soc.interconnect.csr import *

from litex.build.io import SDRTristate

from litex.soc.integration.doc import AutoDoc, ModuleDoc

# LiteSPI PHY Core ---------------------------------------------------------------------------------

class LiteSPISDRPHYCore(Module, AutoCSR, AutoDoc, ModuleDoc):
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
    def __init__(self, pads, flash, device, clock_domain, default_divisor, cs_delay):
        self.source           = source = stream.Endpoint(spi_phy2core_layout)
        self.sink             = sink   = stream.Endpoint(spi_core2phy_layout)
        self.cs               = Signal()
        self._spi_clk_divisor = spi_clk_divisor = Signal(8)

        self._default_divisor = default_divisor

        self.clk_divisor      = clk_divisor = CSRStorage(8, reset=self._default_divisor)

        # # #

        # Resynchronize CSR Clk Divisor to LiteSPI Clk Domain.
        self.submodules += ResyncReg(clk_divisor.storage, spi_clk_divisor, clock_domain)

        # Determine SPI Bus width and DQs.
        if hasattr(pads, "miso"):
            bus_width = 1
            pads.dq   = [pads.mosi, pads.miso]
        else:
            bus_width = len(pads.dq)
        assert bus_width in [1, 2, 4, 8]

        # Check if number of pads matches configured mode.
        assert flash.check_bus_width(bus_width)

        self.addr_bits  = addr_bits  = flash.addr_bits
        self.cmd_width  = cmd_width  = flash.cmd_width
        self.addr_width = addr_width = flash.addr_width
        self.data_width = data_width = flash.bus_width
        self.ddr        = ddr        = flash.ddr

        self.command = command = flash.read_opcode.code

        # Clock Generator.
        self.submodules.clkgen = clkgen = LiteSPIClkGen(pads, device, with_ddr=ddr)
        self.comb += [
            clkgen.div.eq(spi_clk_divisor),
            clkgen.sample_cnt.eq(1),
            clkgen.update_cnt.eq(1),
        ]

        # CS control.
        cs_timer = WaitTimer(cs_delay + 1) # Ensure cs_delay cycles between XFers.
        cs_out   = Signal()
        self.submodules += cs_timer
        self.comb += cs_timer.wait.eq(self.cs)
        self.comb += cs_out.eq(cs_timer.done)
        self.comb += pads.cs_n.eq(~cs_out)

        # I/Os.
        data_bits = 32
        cmd_bits  = 8

        dq_o  = Signal(len(pads.dq))
        dq_i  = Signal(len(pads.dq))
        dq_oe = Signal(len(pads.dq))

        for i in range(len(pads.dq)):
            self.specials += SDRTristate(
                io = pads.dq[i],
                o  = dq_o[i],
                oe = dq_oe[i],
                i  = dq_i[i],
            )

        # Data Shift Regsiters.
        sr_cnt = Signal(8, reset_less=True)
        sr_out = Signal(len(sink.data), reset_less=True)
        sr_din = Signal(len(sink.data), reset_less=True)

        # FSM.
        din_width_cases = {1: [NextValue(sr_din, Cat(dq_i[1], sr_din))]}
        for i in [2, 4, 8]:
            din_width_cases[i] = [NextValue(sr_din, Cat(dq_i[0:i], sr_din))]

        dout_width_cases = {}
        for i in [1, 2, 4, 8]:
            dout_width_cases[i] = [dq_o.eq(sr_out[-i:])]

        self.submodules.fsm = fsm = FSM(reset_state="IDLE")
        fsm.act("IDLE",
            If(sink.valid & cs_out,
                NextValue(sr_out,  sink.data << (32-sink.len)),
                NextValue(sr_din,   0),
                NextState("USER")
            )
        )

        def shift_out(width, bits, next_state, trigger=[], op=[]):
            if type(trigger) is not list:
                trigger = [trigger]
                op      = [op]
            res  = [
                self.clkgen.en.eq(1),
                If(self.clkgen.negedge,
                    NextValue(sr_cnt, sr_cnt+width),
                    If(sr_cnt == (bits-width),
                        NextValue(sr_cnt, 0),
                        NextState(next_state),
                    ),
                ),
            ]

            if len(trigger) == len(op):
                for i in range(len(trigger)):
                    res += [If(trigger[i], *op[i])]

            return res

        fsm.act("USER",
            dq_oe.eq(sink.mask),
            Case(sink.width, dout_width_cases),
            shift_out(
                width      = sink.width,
                bits       = sink.len,
                next_state = "USER_END",
                trigger    = [
                    clkgen.posedge_reg2, # data sampling
                    clkgen.negedge,      # data update
                ],
                op = [
                    [Case(sink.width, din_width_cases)],
                    [NextValue(sr_out, sr_out<<sink.width)],
                ])
        )
        fsm.act("USER_END",
            If(spi_clk_divisor > 0,
                # Last data cycle was already captured in the USER state.
                sink.ready.eq(1),
                NextState("SEND_USER_DATA"),
            ).Elif(clkgen.posedge_reg2,
                # Capture last data cycle.
                sink.ready.eq(1),
                Case(sink.width, din_width_cases),
                NextState("SEND_USER_DATA"),
            )
        )
        fsm.act("SEND_USER_DATA",
            source.valid.eq(1),
            source.last.eq(1),
            source.data.eq(sr_din),
            If(source.ready,
                NextState("IDLE"),
            )
        )
