#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *
from migen.genlib.fsm import FSM, NextState

from litex.soc.interconnect import stream

from litespi.common import *

class LiteSPIPHYModelCore(Module):
    def __init__(self, flash, init=None, latency=4):
        self.source     = source = stream.Endpoint(spi_phy2core_layout)
        self.sink       = sink   = stream.Endpoint(spi_core2phy_layout)
        self.dummy_bits = Signal(8)
        self.cs         = Signal()

        mem         = Memory(32, flash.total_size//4, init=init)
        read_addr   = Signal(32)

        read_port   = mem.get_port(async_read=True)

        self.specials += mem, read_port

        self.comb   += read_port.adr.eq(read_addr)

        cmd_bits    = 8

        delay_cnt   = Signal(8)
        xfer_len    = Signal(8)
        xfer_width  = Signal(8)

        def delay_gen(next_state, width=xfer_width, bits=xfer_len, op=[]):
            res = [
                If(delay_cnt == (bits - width + latency*width),
                    source.valid.eq(1),
                    If(source.ready,
                        NextValue(delay_cnt, 0),
                        NextState(next_state),
                        *op,
                    ),
                ).Else(
                    NextValue(delay_cnt, delay_cnt + width),
                )
            ]

            return res

        def wait_gen(next_state, op=[]):
            res = [
                sink.ready.eq(1),
                If(sink.valid,
                    NextValue(xfer_len, sink.len),
                    NextValue(xfer_width, sink.width),
                    NextState(next_state),
                    *op,
                )
            ]

            return res

        self.submodules.fsm = fsm = FSM(reset_state="IDLE")
        fsm.act("IDLE",
            sink.ready.eq(self.cs),
            NextValue(read_addr, 0),
            NextValue(delay_cnt, 0),
            If(sink.valid & sink.ready,
                NextValue(xfer_len, sink.len),
                NextValue(xfer_width, sink.width),
                If((sink.len == cmd_bits) & (sink.data == flash.read_opcode.code),
                    NextState("CMD-DELAY"),
                ).Else(
                    NextState("OTHER-DELAY"),
                )
            )
        )

        fsm.act("OTHER-DELAY",
            delay_gen("OTHER-WAIT"),
            If(~self.cs,
                NextState("IDLE")
            )
        )
        fsm.act("OTHER-WAIT",
            wait_gen("OTHER-DELAY"),
            If(~self.cs,
                NextState("IDLE")
            )
        )

        fsm.act("CMD-DELAY",
            delay_gen("ADDR-WAIT")
        )
        fsm.act("ADDR-WAIT",
            wait_gen("ADDR-DELAY", op=[NextValue(read_addr, sink.data[2:])]),
        )
        fsm.act("ADDR-DELAY",
            If(self.dummy_bits != 0, 
                delay_gen("DUMMY-WAIT")
            ).Else(
                delay_gen("DATA-WAIT")
            )
        )
        fsm.act("DUMMY-WAIT",
            wait_gen("DUMMY-DELAY"),
        )
        fsm.act("DUMMY-DELAY",
            delay_gen("DATA-WAIT"),
        )
        fsm.act("DATA-WAIT",
            If(~self.cs,
                NextState("IDLE")
            ),
            wait_gen("DATA-DELAY"),
        )
        fsm.act("DATA-DELAY",
            If(~self.cs,
                NextState("IDLE")
            ),
            source.data.eq(read_port.dat_r),
            delay_gen("DATA-WAIT", op=[NextValue(read_addr, read_addr+1)]),
        )

class LiteSPIPHYModel(Module):
    """LiteSPI PHY simulation model.

    The ``LiteSPIPHYModel`` class provides a simulation model that can be used instead of the real PHY.

    init : []
        Initialization data for the flash contents.

    Attributes
    ----------
    source : Endpoint(spi_phy2core_layout), out
        Data stream.

    sink : Endpoint(spi_core2phy_layout), in
        Control stream.

    cs : Signal()
        Dummy flash CS signal.
    """
    def __init__(self, flash, clock_domain="sys", init=None):
        self.phy        = LiteSPIPHYModelCore(flash, init=init)
        self.dummy_bits = self.phy.dummy_bits
        self.source     = self.phy.source
        self.sink       = self.phy.sink
        self.cs         = self.phy.cs
        self.flash      = flash

        # # #

        if clock_domain != "sys":
            self.clock_domains.cd_litespi = ClockDomain()
            self.phy = ClockDomainsRenamer("litespi")(self.phy)
            self.comb += self.cd_litespi.clk.eq(ClockSignal(clock_domain))
            self.comb += self.cd_litespi.rst.eq(ResetSignal(clock_domain))

        self.submodules.spiflash_phy = self.phy
