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

    It supports sequential accesses so that command and address is only sent when necessary.

    Parameters
    ----------
    endianness : string
        If endianness is set to ``little`` then byte order of each 32-bit word coming from flash will be reversed.

    Attributes
    ----------
    source : Endpoint(spi_core2phy_layout), out
        PHY control interface.

    sink : Endpoint(spi_phy2core_layout), in
        PHY data interface.

    bus : Interface(), out
        Wishbone interface for memory-mapped flash access.

    cs : Signal(), out
        CS signal for the flash chip, should be connected to cs signal of the PHY.
    """
    def __init__(self, endianness="big"):
        self.source = source = stream.Endpoint(spi_core2phy_layout)
        self.sink   = sink   = stream.Endpoint(spi_phy2core_layout)
        self.bus    = bus    = wishbone.Interface()
        self.cs     = cs     = Signal()

        # # #

        addr    = Signal(32, reset_less=True)
        read    = Signal()
        timeout = Signal(max=MMAP_DEFAULT_TIMEOUT)

        # Decode Bus Read Commands.
        self.comb += read.eq(bus.cyc & bus.stb & ~bus.we)

        # Map Bus Read Datas.
        self.comb += bus.dat_r.eq({"big": sink.data, "little": reverse_bytes(sink.data)}[endianness])

        # FSM.
        self.submodules.fsm = fsm = FSM(reset_state="IDLE")
        fsm.act("IDLE",
            If(read,
                NextState("CMD"),
            )
        )
        fsm.act("CMD",
            cs.eq(1),
            source.valid.eq(1),
            source.cmd.eq(CMD),
            source.data.eq(Cat(Signal(2), bus.adr)), # Words to Bytes.
            If(source.ready,
                NextValue(addr, bus.adr),
                NextState("READ-REQ"),
            )
        )
        fsm.act("READ-REQ",
            cs.eq(1),
            source.valid.eq(1),
            source.cmd.eq(READ),
            If(source.ready,
                source.last.eq(1),
                NextState("READ-DAT"),
            )
        )
        fsm.act("READ-DAT",
            cs.eq(1),
            sink.ready.eq(bus.stb),
            bus.ack.eq(sink.valid),
            If(sink.valid & sink.ready,
                NextValue(addr, addr + 1),
                NextState("READY"),
                NextValue(timeout, MMAP_DEFAULT_TIMEOUT - 1),
            )
        )
        fsm.act("READY",
            cs.eq(1),
            If(timeout == 0,
                NextState("IDLE"),
            ).Else(
                NextValue(timeout, timeout - 1),
            ),
            If(read,
                # If Bus Address matches Current Address: We can do the access directly in current SPI Burst.
                If(bus.adr == addr,
                    NextState("READ-REQ"),
                # Else we have to initiate another SPI Burst.
                ).Else(
                    NextState("IDLE"),
                )
            )
        )
