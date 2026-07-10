#
# This file is part of LiteSPI.
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *
from migen.fhdl.specials import Tristate

from litex.gen import *


# SPI NOR Flash Model ------------------------------------------------------------------------------

class LiteSPINORFlashModel(LiteXModule):
    """Pin-level SPI NOR flash read model.

    The model implements the read command selected by ``flash.read_opcode`` and is intended to
    exercise the real LiteSPI PHY in Migen simulations. It supports SDR commands with x1/x2/x4/x8
    command, address, and data phases, 24-bit or 32-bit addresses, dummy cycles, and continuous
    reads while chip select remains active.

    ``init`` contains byte values starting at flash address zero. Uninitialized locations read as
    the erased NOR value, ``0xff``.

    The model accepts regular LiteSPI pads (``clk``, ``cs_n`` and either ``mosi``/``miso`` or
    ``dq``). Simulations can instead provide split ``dq_i``, ``dq_o`` and ``dq_oe`` signals to
    avoid resolving bidirectional signals in the simulator.
    """

    def __init__(self, pads, flash, init=None):
        if flash.ddr:
            raise ValueError("LiteSPINORFlashModel only supports SDR read commands")
        if len(pads.cs_n) != 1:
            raise ValueError("LiteSPINORFlashModel requires exactly one chip-select signal")

        init = [] if init is None else list(init)
        if len(init) > flash.total_size:
            raise ValueError("SPI NOR model initialization exceeds the flash size")
        if any(not isinstance(value, int) or value < 0 or value > 0xff for value in init):
            raise ValueError("SPI NOR model initialization must contain byte values")

        cmd_width    = flash.cmd_width
        addr_width   = flash.addr_width
        data_width   = flash.bus_width
        addr_bits    = flash.addr_bits
        dummy_cycles = flash.dummy_cycles if flash.fast_mode else 0

        if any(width not in [1, 2, 4, 8] for width in [cmd_width, addr_width, data_width]):
            raise ValueError("SPI NOR model phase widths must be 1, 2, 4, or 8")
        if 8 % cmd_width or addr_bits % addr_width or 8 % data_width:
            raise ValueError("SPI NOR model phase lengths must be divisible by their bus widths")

        # Normalize regular and split SPI pads to the flash-side DQ signals. DQ0 carries serial
        # input and DQ1 carries serial output in x1 mode.
        if hasattr(pads, "mosi"):
            if any(width != 1 for width in [cmd_width, addr_width, data_width]):
                raise ValueError("Separate MOSI/MISO pads only support x1 phases")
            dq_i  = Signal(2)
            dq_o  = Signal(2)
            dq_oe = Signal(2)
            self.comb += [
                dq_i[0].eq(pads.mosi),
                pads.miso.eq(Mux(dq_oe[1], dq_o[1], 1)),
            ]
        elif all(hasattr(pads, name) for name in ["dq_i", "dq_o", "dq_oe"]):
            if len({len(pads.dq_i), len(pads.dq_o), len(pads.dq_oe)}) != 1:
                raise ValueError("Split SPI NOR model DQ signals must have matching widths")
            dq_i  = Signal(len(pads.dq_i))
            dq_o  = Signal(len(pads.dq_o))
            dq_oe = Signal(len(pads.dq_oe))
            self.comb += [
                dq_i.eq(pads.dq_i),
                pads.dq_o.eq(dq_o),
                pads.dq_oe.eq(dq_oe),
            ]
        elif hasattr(pads, "dq"):
            dq_i  = Signal(len(pads.dq))
            dq_o  = Signal(len(pads.dq))
            dq_oe = Signal(len(pads.dq))
            for n in range(len(pads.dq)):
                self.specials += Tristate(pads.dq[n], dq_o[n], dq_oe[n], dq_i[n])
        else:
            raise ValueError("SPI NOR model requires MOSI/MISO, DQ, or split DQ pads")

        required_width = 2 if data_width == 1 else max(cmd_width, addr_width, data_width)
        if len(dq_i) < required_width:
            raise ValueError("SPI NOR model pads are too narrow for the configured read command")

        self.dq_i  = dq_i
        self.dq_o  = dq_o
        self.dq_oe = dq_oe

        # Store only initialized bytes; the remainder of the modeled flash reads as erased. This
        # keeps simulations of large flash modules lightweight.
        mem = Memory(8, max(2, len(init)), init=init or [0xff, 0xff])
        read_port      = mem.get_port(async_read=True)
        read_next_port = mem.get_port(async_read=True)
        self.specials += mem, read_port, read_next_port
        self.mem = mem

        read_addr      = Signal(max=flash.total_size)
        read_next_addr = Signal.like(read_addr)
        read_data      = Signal(8)
        read_next_data = Signal(8)
        self.read_addr = read_addr
        self.comb += If(read_addr == (flash.total_size - 1),
            read_next_addr.eq(0),
        ).Else(
            read_next_addr.eq(read_addr + 1),
        )
        if init:
            self.comb += [
                read_port.adr.eq(Mux(read_addr < len(init), read_addr, 0)),
                read_next_port.adr.eq(Mux(read_next_addr < len(init), read_next_addr, 0)),
                read_data.eq(Mux(read_addr < len(init), read_port.dat_r, 0xff)),
                read_next_data.eq(Mux(read_next_addr < len(init), read_next_port.dat_r, 0xff)),
            ]
        else:
            self.comb += [
                read_port.adr.eq(0),
                read_next_port.adr.eq(0),
                read_data.eq(0xff),
                read_next_data.eq(0xff),
            ]

        # Detect the externally generated SPI clock edges in the simulation clock domain.
        clk_d       = Signal()
        clk_posedge = Signal()
        clk_negedge = Signal()
        self.sync += clk_d.eq(pads.clk)
        self.comb += [
            clk_posedge.eq( pads.clk & ~clk_d),
            clk_negedge.eq(~pads.clk &  clk_d),
        ]

        command       = Signal(8)
        command_next  = Signal(8)
        address       = Signal(addr_bits)
        address_next  = Signal(addr_bits)
        phase_count   = Signal(max=max(addr_bits, 8) + 1)
        dummy_count   = Signal(max=max(dummy_cycles, 1) + 1)
        data_count    = Signal(max=8)
        data_shift    = Signal(8)
        data_sampled  = Signal()
        self.command  = command

        self.sync += If(pads.cs_n,
            command.eq(0),
            address.eq(0),
            read_addr.eq(0),
            phase_count.eq(0),
            dummy_count.eq(0),
            data_count.eq(0),
            data_shift.eq(0),
            data_sampled.eq(0),
        )

        self.comb += [
            command_next.eq(Cat(dq_i[:cmd_width], command)[:8]),
            address_next.eq(Cat(dq_i[:addr_width], address)[:addr_bits]),
            dq_o.eq(0),
            dq_oe.eq(0),
        ]

        self.submodules.fsm = fsm = ResetInserter()(FSM(reset_state="COMMAND"))
        self.comb += fsm.reset.eq(pads.cs_n)

        if dummy_cycles:
            after_address = [
                NextValue(dummy_count, 0),
                NextState("DUMMY"),
            ]
        else:
            after_address = [NextState("DATA-LOAD")]

        fsm.act("COMMAND",
            If(clk_posedge,
                NextValue(command, command_next),
                If(phase_count == (8 - cmd_width),
                    NextValue(phase_count, 0),
                    If(command_next == flash.read_opcode.code,
                        NextState("ADDRESS"),
                    ).Else(
                        NextState("IGNORE"),
                    ),
                ).Else(
                    NextValue(phase_count, phase_count + cmd_width),
                ),
            ),
        )

        fsm.act("ADDRESS",
            If(clk_posedge,
                NextValue(address, address_next),
                If(phase_count == (addr_bits - addr_width),
                    NextValue(phase_count, 0),
                    NextValue(read_addr, address_next),
                    *after_address,
                ).Else(
                    NextValue(phase_count, phase_count + addr_width),
                ),
            ),
        )

        if dummy_cycles:
            fsm.act("DUMMY",
                If(clk_posedge,
                    If(dummy_count == (dummy_cycles - 1),
                        NextValue(dummy_count, 0),
                        NextState("DATA-LOAD"),
                    ).Else(
                        NextValue(dummy_count, dummy_count + 1),
                    ),
                ),
            )

        fsm.act("DATA-LOAD",
            NextValue(data_shift, read_data),
            NextValue(data_count, 0),
            NextValue(data_sampled, 0),
            NextState("DATA"),
        )

        output_mask = 0b10 if data_width == 1 else 2**data_width - 1
        output_start = 7 if data_width == 1 else 8 - data_width
        fsm.act("DATA",
            dq_oe.eq(output_mask),
            dq_o.eq(data_shift[output_start:8] << (1 if data_width == 1 else 0)),
            If(clk_posedge,
                NextValue(data_sampled, 1),
            ),
            If(clk_negedge & data_sampled,
                NextValue(data_sampled, 0),
                If(data_count == (8 - data_width),
                    NextValue(read_addr, read_next_addr),
                    NextValue(data_shift, read_next_data),
                    NextValue(data_count, 0),
                ).Else(
                    NextValue(data_count, data_count + data_width),
                    NextValue(data_shift, data_shift << data_width),
                ),
            ),
        )

        # Unknown commands are ignored until the controller releases chip select.
        fsm.act("IGNORE")
