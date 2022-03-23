#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *
from migen.genlib.misc import WaitTimer

from litex.soc.interconnect import wishbone, stream
from litex.gen.common import reverse_bytes
from litex.soc.interconnect.csr import *

from litespi.common import *
from migen.genlib.cdc import MultiReg

cmd_oe_mask  = {
    1: 0b00000001,
    2: 0b00000011,
    4: 0b00001111,
    8: 0b11111111,
}
addr_oe_mask = {
    1: 0b00000001,
    2: 0b00000011,
    4: 0b00001111,
    8: 0b11111111,
}

class LiteSPIMMAP(Module, AutoCSR):
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

    dummy_bits : CSRStorage
        Register which hold a number of dummy bits to send during transmission.
    """
    def __init__(self, flash, clock_domain="sys", endianness="big", with_csr=True):
        self.source = source = stream.Endpoint(spi_core2phy_layout)
        self.sink   = sink   = stream.Endpoint(spi_phy2core_layout)
        self.bus    = bus    = wishbone.Interface()
        self.cs     = cs     = Signal()

        # Burst Control.
        burst_cs      = Signal()
        burst_adr     = Signal(len(bus.adr), reset_less=True)
        burst_timeout = WaitTimer(MMAP_DEFAULT_TIMEOUT)
        self.submodules += burst_timeout

        cmd_bits  = 8
        data_bits = 32

        if flash.cmd_width == 1:
            self._default_dummy_bits = flash.dummy_bits if flash.fast_mode else 0
        elif flash.cmd_width == 4:
            self._default_dummy_bits = flash.dummy_bits * 3 if flash.fast_mode else 0
        else:
            raise NotImplementedError(f'Command width of {flash.cmd_width} bits is currently not supported!')

        self._spi_dummy_bits = spi_dummy_bits = Signal(8)

        if with_csr:
            self.dummy_bits = dummy_bits = CSRStorage(8, reset=self._default_dummy_bits)
            if clock_domain != "sys":
                self.specials += MultiReg(dummy_bits.storage, spi_dummy_bits, clock_domain)
            else:
                self.comb += spi_dummy_bits.eq(dummy_bits.storage)
        else:
            self.comb += spi_dummy_bits.eq(self._default_dummy_bits)

        dummy = Signal(data_bits, reset=0xdead)

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
            source.data.eq(flash.read_opcode.code), # send command.
            source.len.eq(cmd_bits),
            source.width.eq(flash.cmd_width),
            source.mask.eq(cmd_oe_mask[flash.cmd_width]),
            NextValue(burst_adr, bus.adr),
            If(source.ready,
                NextState("CMD-RET"),
            )
        )

        fsm.act("CMD-RET",
            cs.eq(1),
            sink.ready.eq(1),
            If(sink.valid,
                NextState("BURST-ADDR"),
            )
        )

        fsm.act("BURST-ADDR",
            cs.eq(1),
            source.valid.eq(1),
            source.width.eq(flash.addr_width),
            source.mask.eq(addr_oe_mask[flash.addr_width]),
            source.data.eq(Cat(Signal(2), bus.adr)), # send address.
            source.len.eq(flash.addr_bits),
            NextValue(burst_cs, 1),
            NextValue(burst_adr, bus.adr),
            If(source.ready,
                NextState("ADDR-RET"),
            )
        )

        fsm.act("ADDR-RET",
            cs.eq(1),
            sink.ready.eq(1),
            If(sink.valid,
                If(spi_dummy_bits == 0,
                    NextState("BURST-REQ"),
                ).Else(
                    NextState("DUMMY"),
                )
            )
        )

        fsm.act("DUMMY",
            cs.eq(1),
            source.valid.eq(1),
            source.width.eq(flash.addr_width),
            source.mask.eq(addr_oe_mask[flash.addr_width]),
            source.data.eq(dummy),
            source.len.eq(spi_dummy_bits),
            If(source.ready,
                NextState("DUMMY-RET"),
            )
        )

        fsm.act("DUMMY-RET",
            cs.eq(1),
            sink.ready.eq(1),
            If(sink.valid,
                NextState("BURST-REQ"),
            )
        )

        fsm.act("BURST-REQ",
            cs.eq(1),
            source.valid.eq(1),
            source.last.eq(1),
            source.width.eq(flash.bus_width),
            source.len.eq(data_bits),
            source.mask.eq(0),
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
