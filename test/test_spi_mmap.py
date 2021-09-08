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

    def test_spi_mmap_core_syntax(self):
        spi_mmap = LiteSPIMMAP(flash=self.DummyChip(Codes.READ_1_1_1, []))

    def test_spi_mmap_read_test(self):
        opcode = Codes.READ_1_1_1
        dut = LiteSPIMMAP(flash=self.DummyChip(opcode, []))

        def wb_gen(dut, addr, data):
            dut.data_ok = 0

            yield dut.bus.adr.eq(addr)
            yield dut.bus.we.eq(0)
            yield dut.bus.cyc.eq(1)
            yield dut.bus.stb.eq(1)

            while (yield dut.bus.ack) == 0:
                yield
            print((yield dut.bus.dat_r))
            if (yield dut.bus.dat_r) == data:
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
