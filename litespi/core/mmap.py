#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *
from migen.genlib.misc import WaitTimer

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


        # Burst Control.
        burst_cs      = Signal()
        burst_adr     = Signal(len(bus.adr), reset_less=True)
        burst_timeout = WaitTimer(MMAP_DEFAULT_TIMEOUT)
        self.submodules += burst_timeout

        # FSM.
        self.submodules.fsm = fsm = FSM(reset_state="IDLE")
        fsm.act("IDLE",
            # Keep CS active after Burst for Timeout.
            burst_timeout.wait.eq(1),
            NextValue(burst_cs, burst_cs & ~burst_timeout.done),
            cs.eq(burst_cs),
            # On Bus Read access...
            If(bus.cyc & bus.stb & ~bus.we,
                # If CS is still active and Bus address matches previous Burst address:
                # Just continue the current Burst.
                If(burst_cs & (bus.adr == burst_adr),
                    NextState("BURST-REQ")
                # Otherwise initialize a new Burst.
                ).Else(
                    cs.eq(0),
                    NextState("BURST-CMD")
                )
            )
        )
        fsm.act("BURST-CMD",
            cs.eq(1),
            source.valid.eq(1),
            source.cmd.eq(CMD),
            source.data.eq(Cat(Signal(2), bus.adr)), # Words to Bytes.
            NextValue(burst_cs, 1),
            NextValue(burst_adr, bus.adr),
            If(source.ready,
                NextState("BURST-REQ"),
            )
        )
        fsm.act("BURST-REQ",
            cs.eq(1),
            source.valid.eq(1),
            source.cmd.eq(READ),
            source.last.eq(1),
            If(source.ready,
                NextState("BURST-DAT"),
            )
        )
        fsm.act("BURST-DAT",
            cs.eq(1),
            sink.ready.eq(1),
            bus.dat_r.eq({"big": sink.data, "little": reverse_bytes(sink.data)}[endianness]),
            If(sink.valid,
                bus.ack.eq(1),
                NextValue(burst_adr, burst_adr + 1),
                NextState("IDLE"),
            )
        )
