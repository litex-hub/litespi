#
# This file is part of LiteSPI.
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

from migen import *
from migen.fhdl.specials import Tristate

from litex.gen import *


# Helpers ------------------------------------------------------------------------------------------

def _opcode_name(opcode):
    from litespi.opcodes import SpiNorFlashOpCodes
    return SpiNorFlashOpCodes.name_from_value(SpiNorFlashOpCodes, opcode)

def _opcode_widths(opcode):
    from litespi.opcodes import SpiNorFlashOpCodes
    cfg      = SpiNorFlashOpCodes()
    cfg.name = _opcode_name(opcode)
    return int(cfg.cmd_width), int(cfg.addr_width), int(cfg.data_width)

# SPI NOR Flash Model ------------------------------------------------------------------------------

class LiteSPINORFlashModel(LiteXModule):
    """Pin-level SPI NOR flash read model.

    The model implements the read command selected by ``flash.read_opcode`` and is intended to
    exercise the real LiteSPI PHY in Migen simulations. It supports SDR commands with x1/x2/x4/x8
    command, address, and data phases, 24-bit or 32-bit addresses, dummy cycles, and continuous
    reads while chip select remains active.

    ``init`` contains byte values starting at flash address zero. Uninitialized locations read as
    the erased NOR value, ``0xff``.

    With ``with_program=True`` (x1 commands only), the model also implements the write sequence of
    a NOR flash: WREN (``0x06``) and WRDI (``0x04``) set and clear the write enable latch (WEL) at
    the CS release, the program command of ``flash.program_opcode`` is ignored unless WEL is set
    and programs its bytes (a NOR program clears bits only, the address wraps inside the page),
    and its CS release starts a busy period of ``program_cycles`` model cycles. While busy, the
    write in progress bit (WIP) is set and every command but RDSR (``0x05``) is ignored; WIP and
    WEL clear at the end. RDSR returns the status register (WIP bit 0, WEL bit 1) on DQ1 for as
    long as CS stays low. The memory then covers the whole flash (``total_size`` up to 64 KiB).

    The model accepts regular LiteSPI pads (``clk``, ``cs_n`` and either ``mosi``/``miso`` or
    ``dq``). Simulations can instead provide split ``dq_i``, ``dq_o`` and ``dq_oe`` signals to
    avoid resolving bidirectional signals in the simulator.
    """

    def __init__(self, pads, flash, init=None, with_program=False, program_cycles=64):
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

        if with_program:
            pp_cmd_width, pp_addr_width, pp_data_width = _opcode_widths(flash.program_opcode)
            pp_addr_bits = 32 if "4B" in _opcode_name(flash.program_opcode) else 24
            if cmd_width != 1 or pp_cmd_width != 1:
                raise ValueError("SPI NOR model programming only supports x1 commands")
            if flash.total_size > 2**16:
                raise ValueError("SPI NOR model programming only supports flashes up to 64 KiB")
            if pp_data_width not in [1, 2, 4, 8] or pp_addr_bits % pp_addr_width:
                raise ValueError("SPI NOR model program phase widths must be 1, 2, 4, or 8")

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
        # keeps simulations of large flash modules lightweight. Programming needs the whole flash.
        if with_program:
            init = init + [0xff]*(flash.total_size - len(init))
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
        phase_count   = Signal(max=max(addr_bits, 32 if with_program else 0, 8) + 1)
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

        # Write Sequence (WREN/WEL, program, WIP).
        if with_program:
            cs_n_d       = Signal(reset=1)
            wel          = Signal()
            wip          = Signal()
            wip_count    = Signal(max=max(program_cycles, 1) + 1)
            cmd_wren     = Signal()
            cmd_wrdi     = Signal()
            programmed   = Signal()
            pp_address   = Signal(max=flash.total_size)
            pp_shift     = Signal(8)
            pp_count     = Signal(max=8 + 1)
            status       = Signal(8)
            self.wel     = wel
            self.wip     = wip
            self.comb += status.eq(Cat(wip, wel))
            self.sync += [
                cs_n_d.eq(pads.cs_n),
                # Commands take effect at the CS release.
                If(pads.cs_n & ~cs_n_d,
                    If(cmd_wren, wel.eq(1)),
                    If(cmd_wrdi, wel.eq(0)),
                    If(programmed,
                        wip.eq(1),
                        wip_count.eq(program_cycles),
                    ),
                    cmd_wren.eq(0),
                    cmd_wrdi.eq(0),
                    programmed.eq(0),
                ).Elif(wip,
                    If(wip_count == 0,
                        wip.eq(0),
                        wel.eq(0),
                    ).Else(
                        wip_count.eq(wip_count - 1),
                    ),
                ),
            ]

            # Program: NOR programming clears bits (AND), the address wraps inside the page.
            write_port = mem.get_port(write_capable=True, async_read=True)
            self.specials += write_port
            pp_byte = Signal(8)
            self.comb += [
                pp_byte.eq(Cat(dq_i[:pp_data_width], pp_shift)[:8]),
                write_port.adr.eq(pp_address),
                write_port.dat_w.eq(write_port.dat_r & pp_byte),
            ]
            pp_page_mask = flash.page_size - 1

        if dummy_cycles:
            after_address = [
                NextValue(dummy_count, 0),
                NextState("DUMMY"),
            ]
        else:
            after_address = [NextState("DATA-LOAD")]

        decode = [If(command_next == flash.read_opcode.code,
            NextState("ADDRESS"),
        ).Else(
            NextState("IGNORE"),
        )]
        if with_program:
            # Every command but RDSR is ignored while busy.
            decode = [If(command_next == 0x05,
                NextState("STATUS-LOAD"),
            ).Elif(wip,
                NextState("IGNORE"),
            ).Elif(command_next == 0x06,
                NextValue(cmd_wren, 1),
                NextState("IGNORE"),
            ).Elif(command_next == 0x04,
                NextValue(cmd_wrdi, 1),
                NextState("IGNORE"),
            ).Elif((command_next == flash.program_opcode.code) & wel,
                NextState("PP-ADDRESS"),
            ).Else(*decode)]

        fsm.act("COMMAND",
            If(clk_posedge,
                NextValue(command, command_next),
                If(phase_count == (8 - cmd_width),
                    NextValue(phase_count, 0),
                    *decode,
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

        if with_program:
            pp_address_shift = Signal(pp_addr_bits)
            pp_address_next  = Signal(pp_addr_bits)
            self.comb += pp_address_next.eq(Cat(dq_i[:pp_addr_width], pp_address_shift)[:pp_addr_bits])
            fsm.act("PP-ADDRESS",
                If(clk_posedge,
                    NextValue(pp_address_shift, pp_address_next),
                    If(phase_count == (pp_addr_bits - pp_addr_width),
                        NextValue(phase_count, 0),
                        NextValue(pp_address, pp_address_next),
                        NextValue(pp_count, 0),
                        NextState("PP-DATA"),
                    ).Else(
                        NextValue(phase_count, phase_count + pp_addr_width),
                    ),
                ),
            )
            fsm.act("PP-DATA",
                If(clk_posedge,
                    NextValue(pp_shift, pp_byte),
                    If(pp_count == (8 - pp_data_width),
                        NextValue(pp_count, 0),
                        write_port.we.eq(1),
                        NextValue(programmed, 1),
                        NextValue(pp_address, (pp_address & ~pp_page_mask) | ((pp_address + 1) & pp_page_mask)),
                    ).Else(
                        NextValue(pp_count, pp_count + pp_data_width),
                    ),
                ),
            )

            # RDSR: status register on DQ1, MSB first, read again for as long as CS stays low.
            fsm.act("STATUS-LOAD",
                NextValue(data_shift, status),
                NextValue(data_count, 0),
                NextValue(data_sampled, 0),
                NextState("STATUS"),
            )
            fsm.act("STATUS",
                dq_oe.eq(0b10),
                dq_o.eq(data_shift[7] << 1),
                If(clk_posedge,
                    NextValue(data_sampled, 1),
                ),
                If(clk_negedge & data_sampled,
                    NextValue(data_sampled, 0),
                    If(data_count == 7,
                        NextValue(data_shift, status),
                        NextValue(data_count, 0),
                    ).Else(
                        NextValue(data_count, data_count + 1),
                        NextValue(data_shift, data_shift << 1),
                    ),
                ),
            )

        # Unknown commands are ignored until the controller releases chip select.
        fsm.act("IGNORE")
