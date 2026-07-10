#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

import unittest

from litespi import modules
from litespi.spi_nor_flash_module import SpiNorFlashModule, SpiNorFlashEraseCommand
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

    def test_erase_geometry(self):
        class EraseGeometryChip(self.GoodDummyChip):
            erase_commands = [
                SpiNorFlashEraseCommand(Codes.BE_4K,  4 * 1024, 24),
                SpiNorFlashEraseCommand(Codes.SE,    64 * 1024, 24),
                SpiNorFlashEraseCommand(Codes.SE_4B, 64 * 1024, 32),
            ]

        chip = EraseGeometryChip(Codes.READ_1_1_1)
        self.assertEqual(chip.erase_opcode, Codes.BE_4K)
        self.assertEqual(chip.erase_size, 4 * 1024)
        self.assertEqual(chip.erase_addr_bits, 24)
        self.assertEqual(len(chip.erase_commands), 3)

        chip = EraseGeometryChip(Codes.READ_1_1_1, erase_cmd=Codes.SE_4B)
        self.assertEqual(chip.erase_opcode, Codes.SE_4B)
        self.assertEqual(chip.erase_size, 64 * 1024)
        self.assertEqual(chip.erase_addr_bits, 32)

    def test_legacy_erase_geometry(self):
        chip = self.GoodDummyChip(Codes.READ_1_1_1)
        self.assertEqual(chip.erase_opcode, Codes.SE)
        self.assertEqual(chip.erase_size, 64 * 1024)
        self.assertEqual(chip.erase_addr_bits, 24)

        chip = self.GoodDummyChip(Codes.READ_1_1_1, erase_cmd=Codes.BE_32K)
        self.assertEqual(chip.erase_opcode, Codes.BE_32K)
        self.assertEqual(chip.erase_size, 32 * 1024)
        self.assertEqual(chip.erase_addr_bits, 24)

    def test_non_erasable_and_invalid_geometry(self):
        class NonErasableChip(self.GoodDummyChip):
            erase_commands = []

        chip = NonErasableChip(Codes.READ_1_1_1)
        self.assertIsNone(chip.erase_opcode)
        self.assertIsNone(chip.erase_size)
        self.assertIsNone(chip.erase_addr_bits)

        class InvalidEraseSizeChip(self.GoodDummyChip):
            erase_commands = [(Codes.BE_4K, 0, 24)]

        with self.assertRaisesRegex(ValueError, "positive integer"):
            InvalidEraseSizeChip(Codes.READ_1_1_1)

        class InvalidEraseAddressChip(self.GoodDummyChip):
            erase_commands = [(Codes.BE_4K, 4096, 16)]

        with self.assertRaisesRegex(ValueError, "0, 24, or 32"):
            InvalidEraseAddressChip(Codes.READ_1_1_1)

    def test_sr1_bit6_quad_enable_modules(self):
        expected_modules = {
            "IS25LP016D", "IS25LP080D", "IS25LP128", "IS25LP256", "IS25LP512M",
            "IS25LQ040B", "IS25WP032", "IS25WP064", "IS25WP128", "IS25WP256",
            "IS25WP512M", "MX25L12833F", "MX25L25635E", "MX25R1035F", "MX25R1635F",
            "MX25R2035F", "MX25R3235F", "MX25R4035F", "MX25R512F", "MX25R8035F",
            "MX25U12835F", "MX25U1635E", "MX25U25645G", "MX25U3235E", "MX25U3235F",
            "MX25U51245G", "MX25U6435E", "MX25V8035F", "MX66L1G45G", "MX66L1G55G",
            "MX66L51235L", "MX66U51235F",
        }
        manufacturers = {
            SpiNorFlashManufacturerIDs.ISSI,
            SpiNorFlashManufacturerIDs.MACRONIX,
        }
        actual_modules = {
            name for name, module in vars(modules).items()
            if (isinstance(module, type) and
                issubclass(module, SpiNorFlashModule) and
                module is not SpiNorFlashModule and
                module.manufacturer_id in manufacturers and
                Codes.READ_1_1_4 in module.supported_opcodes)
        }

        self.assertEqual(actual_modules, expected_modules)
        for name in sorted(expected_modules):
            with self.subTest(module=name):
                self.assertEqual(getattr(modules, name).quad_enable, "wrsr_sr1_bit6")

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
