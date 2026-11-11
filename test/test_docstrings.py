#
# This file is part of LiteSPI.
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

import unittest

from litespi import LiteSPI
from litespi.core.mmap import LiteSPIMMAP
from litespi.core.master import LiteSPIMaster
from litespi.phy.generic import LiteSPIPHY
from litespi.phy.generic_sdr import LiteSPISDRPHYCore
from litespi.phy.generic_ddr import LiteSPIDDRPHYCore


class TestDocstrings(unittest.TestCase):
    def test_public_classes_have_docstrings(self):
        for cls in [LiteSPI, LiteSPIMMAP, LiteSPIMaster, LiteSPIPHY, LiteSPISDRPHYCore, LiteSPIDDRPHYCore]:
            with self.subTest(cls=cls.__name__):
                self.assertIsNotNone(cls.__doc__)
                self.assertIn(f"``{cls.__name__}``", cls.__doc__)
