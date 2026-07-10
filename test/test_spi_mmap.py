#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

import unittest

from migen import *

from litespi.core.mmap import LiteSPIMMAP
from litespi.common import *
from litespi.opcodes import SpiNorFlashOpCodes as Codes
from litespi.spi_nor_flash_module import SpiNorFlashModule
from litespi.ids import SpiNorFlashManufacturerIDs


class TestSPIMMAP(unittest.TestCase):
    class DummyChip(SpiNorFlashModule):

        manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
        device_id = 0x0204
        name = "dummychip1"

        total_size  =    2097152   # bytes
        page_size   =        256   # bytes
        total_pages =       8192

        supported_opcodes = [
            Codes.READ_1_1_1,
            Codes.PP_1_1_1
        ]
        dummy_bits = 8

    class WideProgramDummyChip(DummyChip):
        supported_opcodes = [
            Codes.READ_1_1_1,
            Codes.PP_1_1_1,
            Codes.PP_1_1_4,
            Codes.PP_1_4_4,
        ]

    class WideReadDummyChip(DummyChip):
        supported_opcodes = [
            Codes.READ_1_1_1,
            Codes.READ_1_1_1_FAST,
            Codes.READ_1_1_4,
            Codes.READ_1_4_4,
            Codes.READ_1_1_8,
            Codes.PP_1_1_1,
        ]

    class FourByteAddressDummyChip(DummyChip):
        supported_opcodes = [
            Codes.READ_1_1_1,
            Codes.READ_1_1_1_4B,
            Codes.PP_1_1_1,
            Codes.PP_1_1_1_4B,
        ]

    @staticmethod
    def _record_spi_transfers(dut, transfers, transfer_count=None, cycles=256):
        yield dut.sink.valid.eq(0)
        yield dut.source.ready.eq(1)

        for _ in range(cycles):
            if (yield dut.source.valid):
                transfers.append({
                    "data"  : (yield dut.source.data),
                    "len"   : (yield dut.source.len),
                    "width" : (yield dut.source.width),
                    "mask"  : (yield dut.source.mask),
                })
                yield
                yield dut.sink.valid.eq(1)
                yield
                yield dut.sink.valid.eq(0)
                if transfer_count is not None and len(transfers) >= transfer_count:
                    break
            else:
                yield

        yield dut.sink.valid.eq(0)

    @staticmethod
    def _write_with_timeout(dut, addr, data, sel=0xf, cycles=64):
        acked = []

        def generator():
            yield dut.bus.adr.eq(addr)
            yield dut.bus.dat_w.eq(data)
            yield dut.bus.sel.eq(sel)
            yield dut.bus.we.eq(1)
            yield dut.bus.cyc.eq(1)
            yield dut.bus.stb.eq(1)
            yield

            for _ in range(cycles):
                if (yield dut.bus.ack):
                    acked.append(True)
                    break
                yield

            yield dut.bus.cyc.eq(0)
            yield dut.bus.stb.eq(0)
            yield dut.bus.we.eq(0)

        return acked, generator()

    def test_spi_mmap_core_syntax(self):
        spi_mmap = LiteSPIMMAP(flash=self.DummyChip(Codes.READ_1_1_1, []))
        spi_write_mmap = LiteSPIMMAP(flash=self.DummyChip(Codes.READ_1_1_1, [], program_cmd=Codes.PP_1_1_1), with_write=True)

    def test_spi_mmap_write_test(self):
        opcode = Codes.PP_1_1_1
        dut = LiteSPIMMAP(flash=self.DummyChip(Codes.READ_1_1_1, [], program_cmd=opcode), with_write=True)

        def wb_gen(dut, addr, data):
            dut.done = 0

            yield from dut.bus.write(addr, data)

            dut.done = 1

        def phy_gen(dut, addr, data):
            dut.addr_ok = 0
            dut.opcode_ok = 0
            dut.cmd_ok = 0
            dut.data_ok = 0
            yield dut.sink.valid.eq(0)
            yield dut.source.ready.eq(1)

            while (yield dut.source.valid) == 0:
                yield


            # WRITE CMD
            if (yield dut.source.data) == opcode.code: # cmd ok
                dut.opcode_ok = 1

            yield
            yield dut.sink.valid.eq(1)
            while (yield dut.source.valid) == 0:
                yield
            yield dut.sink.valid.eq(0)

            # WRITE ADDR
            if (yield dut.source.data) == (addr<<2): # address cmd
                dut.addr_ok = 1

            yield
            yield dut.sink.valid.eq(1)
            while (yield dut.source.valid) == 0:
                yield
            yield dut.sink.valid.eq(0)

            # WRITE DATA
            if (yield dut.source.data) == (data): # data ok
                dut.data_ok = 1

            yield
            yield dut.sink.valid.eq(1)
            yield
        addr = 0xcafe
        data = 0xdeadbeef

        run_simulation(dut, [wb_gen(dut, addr, data), phy_gen(dut, addr, data)])
        self.assertEqual(dut.done, 1)
        self.assertEqual(dut.addr_ok, 1)
        self.assertEqual(dut.opcode_ok, 1)
        self.assertEqual(dut.data_ok, 1)

    def test_spi_mmap_program_opcode_widths(self):
        opcode = Codes.PP_1_4_4
        dut = LiteSPIMMAP(
            flash      = self.WideProgramDummyChip(Codes.READ_1_1_1, [], program_cmd=opcode),
            with_write = True,
        )
        addr      = 0xcafe
        data      = 0xdeadbeef
        transfers = []

        def wb_gen():
            yield from dut.bus.write(addr, data, sel=0b0001)

        run_simulation(dut, [
            wb_gen(),
            self._record_spi_transfers(dut, transfers, transfer_count=3),
        ])

        self.assertEqual(transfers, [
            {"data" : opcode.code, "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : addr << 2,   "len" : 24, "width" : 4, "mask" : 0b1111},
            {"data" : data,        "len" : 8,  "width" : 4, "mask" : 0b1111},
        ])

    def test_spi_mmap_csr_disabled_write_acks_without_spi_transfer(self):
        dut = LiteSPIMMAP(
            flash      = self.DummyChip(Codes.READ_1_1_1, [], program_cmd=Codes.PP_1_1_1),
            with_write = "csr",
        )
        transfers = []
        acked, wb_gen = self._write_with_timeout(dut, addr=0xcafe, data=0xdeadbeef)

        run_simulation(dut, [
            wb_gen,
            self._record_spi_transfers(dut, transfers, cycles=64),
        ])

        self.assertEqual(acked, [True])
        self.assertEqual(transfers, [])

    def test_spi_mmap_write_sel_skips_unselected_bytes(self):
        opcode = Codes.PP_1_1_1
        dut = LiteSPIMMAP(
            flash      = self.DummyChip(Codes.READ_1_1_1, [], program_cmd=opcode),
            with_write = True,
        )
        addr      = 0xcafe
        data      = 0xaabbccdd
        transfers = []

        def wb_gen():
            yield from dut.bus.write(addr, data, sel=0b1010)

        run_simulation(dut, [
            wb_gen(),
            self._record_spi_transfers(dut, transfers, transfer_count=6),
        ])

        self.assertEqual(transfers, [
            {"data" : opcode.code,       "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : (addr << 2) | 1,   "len" : 24, "width" : 1, "mask" : 0b0001},
            {"data" : data >> 8,         "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : opcode.code,       "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : (addr << 2) | 3,   "len" : 24, "width" : 1, "mask" : 0b0001},
            {"data" : data >> 24,        "len" : 8,  "width" : 1, "mask" : 0b0001},
        ])

    def test_spi_mmap_read_after_csr_write_disable_starts_new_burst(self):
        read_opcode  = Codes.READ_1_1_1
        write_opcode = Codes.PP_1_1_1
        dut = LiteSPIMMAP(
            flash      = self.DummyChip(read_opcode, [], program_cmd=write_opcode),
            with_write = "csr",
        )
        addr      = 0xcafe
        data      = 0x44332211
        transfers = []

        def wb_gen():
            yield dut.write_config.fields.write_enable.eq(1)
            yield
            yield from dut.bus.write(addr, data)
            yield dut.write_config.fields.write_enable.eq(0)
            yield
            yield from dut.bus.read(addr + 1)

        run_simulation(dut, [
            wb_gen(),
            self._record_spi_transfers(dut, transfers, transfer_count=9, cycles=512),
        ])

        self.assertEqual(transfers, [
            {"data" : write_opcode.code, "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : addr << 2,         "len" : 24, "width" : 1, "mask" : 0b0001},
            {"data" : data,              "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : data >> 8,         "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : data >> 16,        "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : data >> 24,        "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : read_opcode.code,  "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : (addr + 1) << 2,   "len" : 24, "width" : 1, "mask" : 0b0001},
            {"data" : 0,                 "len" : 32, "width" : 1, "mask" : 0b0000},
        ])

    def test_spi_mmap_sequential_write_continues_data_burst_then_read_restarts(self):
        read_opcode  = Codes.READ_1_1_1
        write_opcode = Codes.PP_1_1_1
        dut = LiteSPIMMAP(
            flash      = self.DummyChip(read_opcode, [], program_cmd=write_opcode),
            with_write = True,
        )
        addr       = 0xcafe
        first_data = 0x44332211
        next_data  = 0x88776655
        transfers  = []

        def wb_gen():
            yield from dut.bus.write(addr, first_data)
            yield from dut.bus.write(addr + 1, next_data)
            yield from dut.bus.read(addr + 2)

        run_simulation(dut, [
            wb_gen(),
            self._record_spi_transfers(dut, transfers, transfer_count=13, cycles=768),
        ])

        self.assertEqual(transfers, [
            {"data" : write_opcode.code, "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : addr << 2,         "len" : 24, "width" : 1, "mask" : 0b0001},
            {"data" : first_data,        "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : first_data >> 8,   "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : first_data >> 16,  "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : first_data >> 24,  "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : next_data,         "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : next_data >> 8,    "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : next_data >> 16,   "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : next_data >> 24,   "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : read_opcode.code,  "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : (addr + 2) << 2,   "len" : 24, "width" : 1, "mask" : 0b0001},
            {"data" : 0,                 "len" : 32, "width" : 1, "mask" : 0b0000},
        ])

    def test_spi_mmap_write_restarts_at_page_boundary(self):
        write_opcode = Codes.PP_1_1_1
        dut = LiteSPIMMAP(
            flash      = self.DummyChip(Codes.READ_1_1_1, [], program_cmd=write_opcode),
            with_write = "csr",
        )
        page_words = self.DummyChip.page_size // 4
        addr       = 0x1000 + page_words - 1
        first_data = 0x44332211
        next_data  = 0x88776655
        transfers  = []

        def wb_gen():
            yield dut.write_config.fields.write_enable.eq(1)
            yield
            yield from dut.bus.write(addr, first_data)
            yield from dut.bus.write(addr + 1, next_data)

        run_simulation(dut, [
            wb_gen(),
            self._record_spi_transfers(dut, transfers, transfer_count=12, cycles=768),
        ])

        self.assertEqual(transfers, [
            {"data" : write_opcode.code, "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : addr << 2,         "len" : 24, "width" : 1, "mask" : 0b0001},
            {"data" : first_data,        "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : first_data >> 8,   "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : first_data >> 16,  "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : first_data >> 24,  "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : write_opcode.code, "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : (addr + 1) << 2,   "len" : 24, "width" : 1, "mask" : 0b0001},
            {"data" : next_data,         "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : next_data >> 8,    "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : next_data >> 16,   "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : next_data >> 24,   "len" : 8,  "width" : 1, "mask" : 0b0001},
        ])

    def test_spi_mmap_read_test(self):
        opcode = Codes.READ_1_1_1
        dut = LiteSPIMMAP(flash=self.DummyChip(opcode, []))

        def wb_gen(dut, addr, data):
            dut.data_ok = 0

            dat = yield from dut.bus.read(addr)

            if dat == data:
                dut.data_ok = 1

        def phy_gen(dut, addr, data):
            dut.addr_ok = 0
            dut.opcode_ok = 0
            dut.cmd_ok = 0
            dut.no_dummy = 0
            yield dut.sink.valid.eq(0)
            yield dut.source.ready.eq(1)

            while (yield dut.source.valid) == 0:
                yield


            # READ CMD
            if (yield dut.source.data) == opcode.code: # cmd ok
                dut.opcode_ok = 1

            yield
            yield dut.sink.valid.eq(1)
            while (yield dut.source.valid) == 0:
                yield
            yield dut.sink.valid.eq(0)

            # READ ADDR
            if (yield dut.source.data) == (addr<<2): # address cmd
                dut.addr_ok = 1

            yield
            yield dut.sink.valid.eq(1)
            while (yield dut.source.valid) == 0:
                yield
            yield dut.sink.valid.eq(0)

            # NO DUMMY, mask should be 0 cause we attept to read data
            if (yield dut.source.mask) == 0:
                dut.no_dummy = 1

            # SEND DATA
            yield dut.source.ready.eq(0)
            yield
            yield dut.sink.data.eq(data)
            yield dut.sink.valid.eq(1)

            while (yield dut.sink.ready) == 0:
                yield

            yield
            yield dut.sink.valid.eq(0)
            yield
        addr = 0xcafe
        data = 0xdeadbeef

        run_simulation(dut, [wb_gen(dut, addr, data), phy_gen(dut, addr, data)])
        self.assertEqual(dut.data_ok, 1)
        self.assertEqual(dut.addr_ok, 1)
        self.assertEqual(dut.opcode_ok, 1)
        self.assertEqual(dut.no_dummy, 1)

    def test_spi_mmap_fast_read_dummy_cycles(self):
        cases = [
            (Codes.READ_1_1_1_FAST, 1, 1, 1, 8),
            (Codes.READ_1_1_4,      1, 1, 4, 8),
            (Codes.READ_1_4_4,      1, 4, 4, 32),
            (Codes.READ_1_1_8,      1, 1, 8, 8),
        ]

        for opcode, cmd_width, addr_width, data_width, dummy_bits in cases:
            with self.subTest(opcode=opcode):
                dut = LiteSPIMMAP(flash=self.WideReadDummyChip(opcode, []))
                addr      = 0xcafe
                transfers = []

                def wb_gen():
                    yield from dut.bus.read(addr)

                run_simulation(dut, [
                    wb_gen(),
                    self._record_spi_transfers(dut, transfers, transfer_count=4),
                ])

                self.assertEqual(transfers, [
                    {"data" : opcode.code, "len" : 8,          "width" : cmd_width,  "mask" : (1 << cmd_width) - 1},
                    {"data" : addr << 2,   "len" : 24,         "width" : addr_width, "mask" : (1 << addr_width) - 1},
                    {"data" : 0xdead,      "len" : dummy_bits, "width" : addr_width, "mask" : 0b0000},
                    {"data" : 0,           "len" : 32,         "width" : data_width, "mask" : 0b0000},
                ])

    def test_spi_mmap_4byte_address_phases(self):
        addr = 0x12345678

        read_dut = LiteSPIMMAP(
            flash = self.FourByteAddressDummyChip(Codes.READ_1_1_1_4B, []),
        )
        read_transfers = []

        def read_wb_gen():
            yield from read_dut.bus.read(addr)

        run_simulation(read_dut, [
            read_wb_gen(),
            self._record_spi_transfers(read_dut, read_transfers, transfer_count=3),
        ])

        self.assertEqual(read_transfers, [
            {"data" : Codes.READ_1_1_1_4B.code, "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : addr << 2,                "len" : 32, "width" : 1, "mask" : 0b0001},
            {"data" : 0,                        "len" : 32, "width" : 1, "mask" : 0b0000},
        ])

        write_dut = LiteSPIMMAP(
            flash      = self.FourByteAddressDummyChip(
                Codes.READ_1_1_1_4B, [],
                program_cmd = Codes.PP_1_1_1_4B,
            ),
            with_write = True,
        )
        write_transfers = []
        data            = 0xdeadbeef

        def write_wb_gen():
            yield from write_dut.bus.write(addr, data, sel=0b0001)

        run_simulation(write_dut, [
            write_wb_gen(),
            self._record_spi_transfers(write_dut, write_transfers, transfer_count=3),
        ])

        self.assertEqual(write_transfers, [
            {"data" : Codes.PP_1_1_1_4B.code, "len" : 8,  "width" : 1, "mask" : 0b0001},
            {"data" : addr << 2,              "len" : 32, "width" : 1, "mask" : 0b0001},
            {"data" : data,                   "len" : 8,  "width" : 1, "mask" : 0b0001},
        ])
