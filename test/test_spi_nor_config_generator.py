#
# This file is part of LiteSPI
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

import unittest

import litespi.modules.generated_modules as generated_modules
from litespi.opcodes import SpiNorFlashOpCodes as Codes
from tools.spi_nor_config_generator.flash_module_template import generate_class
from tools.spi_nor_config_generator.override_cfg import (
    apply_output_overrides,
    apply_source_overrides,
    override_chip_cfg,
)


def _opcode(name):
    return getattr(Codes, name.rsplit(".", 1)[-1])


class TestSpiNorConfigGenerator(unittest.TestCase):
    def test_source_and_output_override_stages(self):
        entry = {
            "quad_support": False,
            "supported_commands": [
                "SpiNorFlashOpCodes.READ_1_1_1",
                "SpiNorFlashOpCodes.PP_1_1_1",
            ],
        }
        override = {
            "quad_support": True,
            "supported_opcodes_add": ["READ_1_1_4", "READ_1_1_4"],
            "supported_opcodes_remove": ["PP_1_1_1"],
            "dummy_cycles": {"READ_1_1_4": 8},
            "quad_enable": "wrsr_sr1_bit6",
        }

        apply_source_overrides(entry, override)
        self.assertTrue(entry["quad_support"])
        self.assertNotIn("quad_enable", entry)

        apply_output_overrides(entry, override)
        self.assertEqual(entry["supported_commands"], [
            "SpiNorFlashOpCodes.READ_1_1_1",
            "SpiNorFlashOpCodes.READ_1_1_4",
        ])
        self.assertEqual(entry["dummy_cycles"], {
            "SpiNorFlashOpCodes.READ_1_1_4": 8,
        })
        self.assertEqual(entry["quad_enable"], "wrsr_sr1_bit6")

    def test_complete_opcode_override_and_validation(self):
        entry = {"supported_commands": ["SpiNorFlashOpCodes.READ_1_1_1"]}
        apply_output_overrides(entry, {
            "supported_opcodes": ["READ_1_1_2", "PP_1_1_1"],
        })
        self.assertEqual(entry["supported_commands"], [
            "SpiNorFlashOpCodes.READ_1_1_2",
            "SpiNorFlashOpCodes.PP_1_1_1",
        ])

        with self.assertRaisesRegex(ValueError, "cannot be combined"):
            apply_output_overrides(entry, {
                "supported_opcodes": ["READ_1_1_1"],
                "supported_opcodes_add": ["READ_1_1_4"],
            })
        with self.assertRaisesRegex(ValueError, "Unknown SPI NOR opcode"):
            apply_output_overrides(entry, {"supported_opcodes_add": ["READ_UNKNOWN"]})
        with self.assertRaisesRegex(ValueError, "non-negative integer"):
            apply_output_overrides(entry, {"dummy_cycles": {"READ_1_1_1": -1}})

    def test_template_emits_explicit_module_attributes(self):
        source = generate_class(
            vendor_id="SpiNorFlashManufacturerIDs.ISSI",
            device_id=0x1234,
            chip_name="test-flash",
            total_size=4096,
            page_size=256,
            total_pages=16,
            dummy_bits=8,
            supported_commands=["SpiNorFlashOpCodes.READ_1_1_4"],
            dummy_cycles={"SpiNorFlashOpCodes.READ_1_1_4": 6},
            quad_enable="wrsr_sr1_bit6",
        )

        compile(source, "<generated-module>", "exec")
        self.assertIn('quad_enable = "wrsr_sr1_bit6"', source)
        self.assertIn("SpiNorFlashOpCodes.READ_1_1_4: 6", source)

    def test_checked_in_modules_include_output_overrides(self):
        modules_by_name = {
            module.name: module
            for module in vars(generated_modules).values()
            if isinstance(module, type) and hasattr(module, "name")
        }

        for name, override in override_chip_cfg.items():
            output_keys = {
                "supported_opcodes",
                "supported_opcodes_add",
                "supported_opcodes_remove",
                "dummy_cycles",
                "quad_enable",
            }
            if not output_keys.intersection(override):
                continue

            with self.subTest(module=name):
                self.assertIn(name, modules_by_name)
                module = modules_by_name[name]

                if "supported_opcodes" in override:
                    self.assertEqual(
                        module.supported_opcodes,
                        [_opcode(opcode) for opcode in override["supported_opcodes"]],
                    )
                for opcode in override.get("supported_opcodes_add", []):
                    self.assertIn(_opcode(opcode), module.supported_opcodes)
                for opcode in override.get("supported_opcodes_remove", []):
                    self.assertNotIn(_opcode(opcode), module.supported_opcodes)

                if "dummy_cycles" in override:
                    expected = {
                        _opcode(opcode): cycles
                        for opcode, cycles in override["dummy_cycles"].items()
                    }
                    self.assertEqual(module.dummy_cycles, expected)
                if "quad_enable" in override:
                    self.assertEqual(module.quad_enable, override["quad_enable"])


if __name__ == "__main__":
    unittest.main()
