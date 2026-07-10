#
# This file is part of LiteSPI.
#
# SPDX-License-Identifier: BSD-2-Clause

import ast
import inspect
import unittest
from pathlib import Path

from litespi import modules
from litespi.ids import SpiNorFlashManufacturerIDs
from litespi.opcodes import SpiNorFlashOpCode
from litespi.spi_nor_flash_module import SpiNorFlashEraseCommand, SpiNorFlashModule
import litespi.modules.modules as nor_modules


class TestSpiNorModules(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module_classes = [
            module for _, module in inspect.getmembers(nor_modules, inspect.isclass)
            if (issubclass(module, SpiNorFlashModule) and
                module is not SpiNorFlashModule and
                module.__module__ == nor_modules.__name__)
        ]

    def test_module_inventory(self):
        tree = ast.parse(Path(nor_modules.__file__).read_text())
        class_names = [node.name for node in tree.body if isinstance(node, ast.ClassDef)]

        self.assertEqual(len(class_names), 481)
        self.assertEqual(len(class_names), len(set(class_names)))
        self.assertEqual(len(self.module_classes), len(class_names))
        for module in self.module_classes:
            self.assertIs(getattr(modules, module.__name__), module)

    def test_module_attributes(self):
        names = set()
        for module in self.module_classes:
            with self.subTest(module=module.__name__):
                self.assertIsInstance(module.manufacturer_id, SpiNorFlashManufacturerIDs)
                self.assertIs(type(module.device_id), int)
                self.assertGreaterEqual(module.device_id, 0)
                self.assertLessEqual(module.device_id, 0xffff)

                self.assertIsInstance(module.name, str)
                self.assertTrue(module.name)
                self.assertNotIn(module.name, names)
                names.add(module.name)

                self.assertIs(type(module.total_size), int)
                self.assertIs(type(module.page_size), int)
                self.assertGreater(module.total_size, 0)
                self.assertGreater(module.page_size, 0)
                self.assertEqual(module.total_size % module.page_size, 0)
                self.assertEqual(module.total_pages, module.total_size // module.page_size)

                self.assertIsInstance(module.supported_opcodes, list)
                self.assertTrue(module.supported_opcodes)
                self.assertEqual(
                    len(module.supported_opcodes),
                    len(set(module.supported_opcodes)),
                )
                for opcode in module.supported_opcodes:
                    self.assertIsInstance(opcode, SpiNorFlashOpCode)

                if hasattr(module, "dummy_bits"):
                    self.assertIs(type(module.dummy_bits), int)
                    self.assertGreaterEqual(module.dummy_bits, 0)
                else:
                    self.assertIn("dummy_cycles", module.__dict__)

                if "dummy_cycles" in module.__dict__:
                    self.assertIsInstance(module.dummy_cycles, dict)
                    for opcode, cycles in module.dummy_cycles.items():
                        self.assertIsInstance(opcode, SpiNorFlashOpCode)
                        self.assertIs(type(cycles), int)
                        self.assertGreaterEqual(cycles, 0)

                if "quad_enable" in module.__dict__:
                    self.assertIn(module.quad_enable, {"wrsr_sr1_bit6", "wrr_cr1_bit1"})

                if "erase_commands" in module.__dict__:
                    self.assertIsInstance(module.erase_commands, list)
                    for command in module.erase_commands:
                        self.assertIsInstance(command, SpiNorFlashEraseCommand)
                        self.assertIsInstance(command.opcode, SpiNorFlashOpCode)
                        self.assertGreater(command.size, 0)
                        self.assertIn(command.addr_bits, {0, 24, 32})


if __name__ == "__main__":
    unittest.main()
