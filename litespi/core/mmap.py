#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *
from migen.genlib.fsm import FSM, NextState

from litex.soc.interconnect import wishbone, stream
from litex.gen.common import reverse_bytes

from litespi.common import *


class LiteSPIMMAP(Module):
    """Memory-mapped SPI Flash controller.

    The ``LiteSPIMMAP`` class provides a Wishbone slave that must be connected to a LiteSPI PHY.

    It supports sequential access so that command and address is only sent when necessary.

    Parameters
    ----------
    endianness : string
        If endianness is set to ``small`` then byte order of each 32-bit word comming from flash will be reversed.

    Attributes
    ----------
    source : Endpoint(spi_phy_ctl_layout), out
        PHY control interface

    sink : Endpoint(spi_phy_data_layout), in
        PHY data interface

    bus : Interface(), out
        Wishbone interface for memory-mapped flash access

    cs_n : Signal(), out
        CS signal for the flash chip, should be connected to cs_n signal of the PHY
    """
    def __init__(self, endianness="big"):
        self.source = source = stream.Endpoint(spi_phy_ctl_layout)
        self.sink   = sink   = stream.Endpoint(spi_phy_data_layout)
        self.bus    = bus    = wishbone.Interface()
        self.cs_n   = cs_n   = Signal()
        curr_addr   = Signal(32)
        bus_read    = Signal()
        cs_cnt      = Signal(16)
        cs_val      = Signal(16)

        self.submodules.fsm = fsm = FSM(reset_state="IDLE")

        self.comb += [
            bus_read.eq(bus.cyc & bus.stb & ~bus.we),
            bus.dat_r.eq(sink.data if endianness == "big" else reverse_bytes(sink.data)),
        ]

        # TODO: make this configurable via CSR
        self.comb += cs_val.eq(10000)

        fsm.act("IDLE",
            cs_n.eq(1),
            If(bus_read,
                NextState("CS_DELAY"),
            )
        )
        fsm.act("CMD",
            source.valid.eq(1),
            source.cmd.eq(CMD),
            source.data.eq(Cat(0, 0, bus.adr)), # convert wb address to bytes
            If(source.ready & source.valid,
                NextValue(curr_addr, bus.adr),
                NextState("READ_REQ"),
            )
        )
        fsm.act("READ_REQ",
            source.valid.eq(1),
            source.cmd.eq(READ),
            If(source.ready & source.valid,
                source.last.eq(1),
                NextState("READ_DAT"),
            )
        )
        fsm.act("READ_DAT",
            sink.ready.eq(bus.stb),
            bus.ack.eq(sink.valid),
            If(sink.ready & sink.valid,
                NextValue(curr_addr, curr_addr+1),
                NextState("READY"),
            )
        )
        fsm.act("READY",
            If(bus_read,
                If(curr_addr == bus.adr, # is the current flash address ok?
                    NextState("READ_REQ"),
                ).Else(
                    NextState("CS_DELAY"),
                )
            )
        )
        fsm.act("CS_DELAY",
            cs_n.eq(1),
            If(cs_cnt < cs_val,
                NextValue(cs_cnt, cs_cnt+1),
            ).Else(
                NextValue(cs_cnt, 0),
                NextState("CMD"),
            )
        )
