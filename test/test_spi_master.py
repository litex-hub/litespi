#
# This file is part of LiteSPI
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

import unittest

from litespi.core.master import LiteSPIMaster


class TestSPIMaster(unittest.TestCase):
    def test_phyconfig_len_matches_stream_width(self):
        dut = LiteSPIMaster()

        self.assertEqual(len(dut._phyconfig.fields.len), len(dut.source.len))
