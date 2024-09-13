#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# Copyright (c) 2024 Matthias Breithaupt <m.breithaupt@vogl-electronic.com>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *

from litex.gen import *

from litex.gen.genlib.misc import WaitTimer

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

class LiteSPIMMAP(LiteXModule):
    """Memory-mapped SPI Flash controller.

    The ``LiteSPIMMAP`` class provides a Wishbone slave that must be connected to a LiteSPI PHY.

    It supports sequential accesses so that command and address is only sent when necessary.

    Parameters
    ----------
    endianness : string
        If endianness is set to ``little`` then byte order of each 32-bit word coming from flash will be reversed.

    with_csr : bool
        The number of dummy bits can be configure when set to True.

    with_write : bool or string "csr"
        MMAP writes are supported when set to True or "csr". When set to "csr", they are disabled by default but
        can be enabled on demand using a CSR.

        Please note that only False and "csr" should be used with flash chips! True is only meant for RAM.

        When using "csr" with a flash chip, make sure to erase the corresponding pages of the flash beforehand
        using the LiteSPI master. It is also recommended to disable mmap writing once it is not required anymore.

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
        Register which holds the number of dummy bits to send during transmission.

    write_config : CSRStorage
        Optional register holding configuration bits for the write mode.
    """
    def __init__(self, flash, clock_domain="sys", endianness="big", with_csr=True, with_write=False):
        self.source = source = stream.Endpoint(spi_core2phy_layout)
        self.sink   = sink   = stream.Endpoint(spi_phy2core_layout)
        self.bus    = bus    = wishbone.Interface()
        self.cs     = cs     = Signal()
        self.offset = offset = Signal(len(bus.adr))

        # Burst Control.
        burst_cs      = Signal()
        burst_adr     = Signal(len(bus.adr), reset_less=True)
        self.burst_timeout = burst_timeout = WaitTimer(MMAP_DEFAULT_TIMEOUT)

        write = Signal()
        write_enabled = Signal()
        write_mask = Signal(len(bus.sel))

        cmd_bits  = 8
        data_bits = 32

        self._default_dummy_bits = flash.dummy_cycles * flash.addr_width if flash.fast_mode else 0

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

        if with_write and with_write == "csr":
            self.write_config = write_config = CSRStorage(fields=[
                CSRField("write_enable", size=1, reset=0, description="MMAP write enable"),
            ])
            if clock_domain != "sys":
                self.specials += MultiReg(write_config.fields.write_enable, write_enabled, clock_domain)
            else:
                self.comb += write_enabled.eq(write_config.fields.write_enable)
        else:
            self.comb += write_enabled.eq(Constant(with_write == True))

        self.byte_count = byte_count = Signal(2, reset_less=True)
        self.data_write = Signal(32)

        # FSM.
        self.fsm = fsm = FSM(reset_state="IDLE")
        fsm.act("IDLE",
            # Keep CS active after Burst for Timeout.
            burst_timeout.wait.eq(1),
            NextValue(burst_cs, burst_cs & ~burst_timeout.done),
            cs.eq(burst_cs),
            If(bus.cyc & bus.stb,
                NextValue(byte_count, 0),
                # On Bus Read access...
                If(~bus.we,
                    # If CS is still active, Bus address matches previous Burst address and previous access was reading:
                    # Just continue the current Burst.
                    If(burst_cs & (bus.adr == burst_adr) & (~write_enabled | ~write),
                        NextState("BURST-REQ")
                    # Otherwise initialize a new Burst.
                    ).Else(
                        cs.eq(0),
                        NextState("BURST-CMD")
                    ),
                    NextValue(write, 0)
                # On Bus Write access (if enabled)...
                ).Elif(write_enabled,
                    # If CS is still active, Bus address matches previous Burst address and previous access was writing:
                    # Just continue the current Burst.
                    NextValue(write_mask, bus.sel),
                    NextValue(self.data_write, bus.dat_w),
                    If(burst_cs & (bus.adr == burst_adr) & bus.sel[0] & write,
                        NextState("WRITE")
                    # Otherwise initialize a new Burst.
                    ).Else(
                        cs.eq(0),
                        NextState("PRE-BURST-CMD-WRITE"),
                    ),
                    NextValue(write, 1)
                )
            )
        )

        fsm.act("PRE-BURST-CMD-WRITE",
            cs.eq(0),
            If(write_mask[0],
               NextState("BURST-CMD"),
               NextValue(write, 1)
            ).Elif(byte_count == 3,
                bus.ack.eq(1),
                NextValue(burst_adr, burst_adr + 1),
                NextState("IDLE"),
                NextValue(write, 0)
            ).Else(
                NextValue(byte_count, byte_count + 1),
                NextValue(write_mask, Cat(write_mask[1:len(bus.sel)], Signal(1))),
            )
        )

        fsm.act("BURST-CMD",
            cs.eq(1),
            source.valid.eq(1),
            If(write_enabled & write,
                source.data.eq(flash.program_opcode.code), # send command.
            ).Else(
                source.data.eq(flash.read_opcode.code), # send command.
            ),
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
            source.data.eq(Cat(byte_count, bus.adr - offset)), # send address.
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
                If(write_enabled & write,
                    NextState("WRITE"),
                ).Elif(spi_dummy_bits == 0,
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
            source.mask.eq(0),
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

        fsm.act("WRITE",
            cs.eq(1),
            source.valid.eq(1),
            source.width.eq(flash.addr_width),
            source.mask.eq(addr_oe_mask[flash.bus_width]),
            source.data.eq(self.data_write),
            source.len.eq(8),
            If(source.ready,
                NextState("WRITE-RET"),
            )
        )

        fsm.act("WRITE-RET",
            cs.eq(1),
            sink.ready.eq(1),
            If(sink.valid,
                If(byte_count != 3,
                    NextValue(write_mask, Cat(write_mask[1:len(bus.sel)], Signal(1))),
                    NextValue(byte_count, byte_count + 1),
                    NextValue(self.data_write, self.data_write >> 8),
                    If(write_mask[1],
                        NextState("WRITE"),
                    ).Else(
                        cs.eq(0),
                        NextValue(write, 0),
                        NextState("PRE-BURST-CMD-WRITE"),
                    ),

                ).Else(
                    bus.ack.eq(1),
                    NextValue(burst_adr, burst_adr + 1),
                    NextState("IDLE"),
                ),
            )
        )
