#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

import unittest

from litespi.spi_nor_flash_module import SpiNorFlashModule
from litespi.opcodes import SpiNorFlashOpCodes as Codes
from litespi.ids import SpiNorFlashManufacturerIDs


class TestFlashModule(unittest.TestCase):
    class GoodDummyChip(SpiNorFlashModule):

        manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
        device_id = 0x0204
        name = "dummychip1"

        total_size  =    2097152   # bytes
        page_size   =        256   # bytes
        total_pages =       8192

        supported_opcodes = [
            Codes.READ_1_1_1,
            Codes.READ_1_1_1_FAST,
            Codes.READ_1_1_2_4B,
            Codes.READ_1_4_4_DTR_4B,
            Codes.READ_1_1_8,
            Codes.PP_1_1_1,
        ]
        dummy_bits = 8


    def test_spi_nor_flash_module_configuration(self):
        # Configure to slow mode
        chip = self.GoodDummyChip(Codes.READ_1_1_1)
        self.assertEqual(chip.cmd_width, 1)
        self.assertEqual(chip.addr_width, 1)
        self.assertEqual(chip.bus_width, 1)
        self.assertEqual(chip.addr_bits, 24)
        self.assertEqual(chip.fast_mode, False)
        self.assertEqual(chip.ddr, False)

        # Reconfigure to fast mode
        chip.read_opcode = Codes.READ_1_1_1_FAST
        self.assertEqual(chip.cmd_width, 1)
        self.assertEqual(chip.addr_width, 1)
        self.assertEqual(chip.bus_width, 1)
        self.assertEqual(chip.addr_bits, 24)
        self.assertEqual(chip.fast_mode, True)
        self.assertEqual(chip.ddr, False)

        # Reconfigure to dual, 32-bit address
        chip.read_opcode = Codes.READ_1_1_2_4B
        self.assertEqual(chip.cmd_width, 1)
        self.assertEqual(chip.addr_width, 1)
        self.assertEqual(chip.bus_width, 2)
        self.assertEqual(chip.addr_bits, 32)
        self.assertEqual(chip.fast_mode, True)
        self.assertEqual(chip.ddr, False)

        # Reconfigure to quad, addr_width=4, 32-bit address with DTR
        chip.read_opcode = Codes.READ_1_4_4_DTR_4B
        self.assertEqual(chip.cmd_width, 1)
        self.assertEqual(chip.addr_width, 4)
        self.assertEqual(chip.bus_width, 4)
        self.assertEqual(chip.addr_bits, 32)
        self.assertEqual(chip.fast_mode, True)
        self.assertEqual(chip.ddr, True)

        # Reconfigure to octal
        chip.read_opcode = Codes.READ_1_1_8
        self.assertEqual(chip.cmd_width, 1)
        self.assertEqual(chip.addr_width, 1)
        self.assertEqual(chip.bus_width, 8)
        self.assertEqual(chip.addr_bits, 24)
        self.assertEqual(chip.fast_mode, True)
        self.assertEqual(chip.ddr, False)

        # Nonsupported mode
        with self.assertRaises(ValueError):
            chip = self.GoodDummyChip(Codes.READ_1_8_8)

    def test_meta_sizes(self):
        with self.assertRaises(AssertionError):
            class BadSizesChip(SpiNorFlashModule):

                manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
                device_id = 0x21ab
                name = "dummychip2"

                total_size  =    2097152   # bytes
                page_size   =        256   # bytes
                total_pages =       8191   # inconsistent total_pages

                supported_opcodes = [
                    Codes.READ_1_1_1,
                    Codes.PP_1_1_1,
                ]

                dummy_bits = 8

    def test_spi_nor_flash_module_missing_attr(self):
        class MissingAttrChip(SpiNorFlashModule):

            manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
            device_id = 0x37cd
            name = "dummychip3"

            total_size  =    2097152   # bytes
            page_size   =        256   # bytes
            total_pages =       8192

            supported_modes = [
                Codes.READ_1_1_1,
                Codes.PP_1_1_1,
            ]

            # missing dummy_bits

        with self.assertRaises(AssertionError):
            chip = MissingAttrChip(Codes.READ_1_1_1)

