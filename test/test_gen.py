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
