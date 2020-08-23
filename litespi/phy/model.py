#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *
from migen.genlib.fsm import FSM, NextState

from litex.soc.interconnect import stream

from litespi.common import *

class LiteSPIPHYModel(Module):
    """LiteSPI PHY simulation model.

    The ``LiteSPIPHYModel`` class provides a simulation model that can be used instead of the real PHY.

    Parameters
    ----------
    size : int
        Simulated flash memory size.

    init : []
        Initialization data for the flash contents.

    Attributes
    ----------
    source : Endpoint(spi_phy_data_layout), out
        Data stream.

    sink : Endpoint(spi_phy_ctl_layout), in
        Control stream.

    cs_n : Signal()
        Dummy flash CS signal.
    """
    def __init__(self, size, init=None):
        self.source = source = stream.Endpoint(spi_phy_data_layout)
        self.sink   = sink   = stream.Endpoint(spi_phy_ctl_layout)
        mem         = Memory(32, size//4, init=init)
        read_addr   = Signal(32)
        self.cs_n   = Signal()

        read_port   = mem.get_port(async_read=True)
        self.comb  += read_port.adr.eq(read_addr)

        self.specials += mem, read_port

        commands = {
            CMD: [NextValue(read_addr, sink.data[2:31])], # word addressed memory
            READ: [NextState("DATA")],
        }

        self.submodules.fsm = fsm = FSM(reset_state="IDLE")
        fsm.act("IDLE",
            sink.ready.eq(1),
            If(sink.ready & sink.valid,
                Case(sink.cmd, commands),
            ),
        )
        fsm.act("DATA",
            source.valid.eq(1),
            source.data.eq(read_port.dat_r),
            If(source.ready & source.valid,
                NextValue(read_addr, read_addr+1),
                NextState("IDLE"),
            ),
        )
