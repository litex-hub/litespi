#
# This file is part of LiteSPI.
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

import sys
import importlib
import unittest
from unittest import mock

from litex.build.xilinx.platform import XilinxPlatform


class TestGen(unittest.TestCase):
    def test_import_without_yaml(self):
        sys.modules.pop("litespi.gen", None)
        with mock.patch.dict(sys.modules, {"yaml": None}):
            importlib.import_module("litespi.gen")

    def test_clk_freq(self):
        from litespi.gen import LiteSPICore, _io
        for mode in ["x1", "x4"]:
            with self.subTest(mode=mode):
                platform = XilinxPlatform(device="", io=_io)
                core     = LiteSPICore(platform, module="S25FL128L", mode=mode, clk_freq="50e6")
                self.assertEqual(core.sys_clk_freq, 50e6)

    def test_4byte_read_above_16mib(self):
        from litespi.gen import LiteSPICore, _io
        from litespi.opcodes import SpiNorFlashOpCodes as Codes
        for module, mode, read_cmd, addr_bits in [
            ("S25FL128L", "x1", Codes.READ_1_1_1,    24), # 16 MiB.
            ("S25FL256L", "x1", Codes.READ_1_1_1_4B, 32), # 32 MiB.
            ("S25FL256L", "x4", Codes.READ_1_1_4_4B, 32),
        ]:
            with self.subTest(module=module, mode=mode):
                platform = XilinxPlatform(device="", io=_io)
                core     = LiteSPICore(platform, module=module, mode=mode)
                flash    = core.spiflash_phy.flash
                self.assertEqual(flash.read_opcode, read_cmd)
                self.assertEqual(flash.addr_bits,   addr_bits)

    def test_default_divisor(self):
        import litespi.gen
        from litespi.gen import LiteSPICore, _io
        for rate, divisor in [("1:1", 2), ("1:2", 1)]:
            with self.subTest(rate=rate):
                platform = XilinxPlatform(device="", io=_io)
                with mock.patch.object(litespi.gen, "LiteSPIPHY", wraps=litespi.gen.LiteSPIPHY) as phy:
                    LiteSPICore(platform, module="S25FL128L", mode="x4", rate=rate)
                self.assertEqual(phy.call_args.kwargs["default_divisor"], divisor)
