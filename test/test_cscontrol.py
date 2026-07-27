#
# This file is part of LiteSPI.
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

import unittest

from migen import *

from litespi.cscontrol import LiteSPICSControl


class _LiteSPICSControlDUT(Module):
    def __init__(self, cs_delay=4):
        self.pads = pads = Record([
            ("cs_n", 2),
        ])
        self.cs = cs = Signal(2)

        self.submodules.cs_control = LiteSPICSControl(
            pads        = pads,
            cs          = cs,
            cs_delay    = cs_delay,
            with_sdr_cs = False,
        )


class TestLiteSPICSControl(unittest.TestCase):
    def test_first_selection_stays_asserted(self):
        for cs, cs_n in [(0b01, 0b10), (0b10, 0b01)]:
            with self.subTest(cs=cs):
                dut = _LiteSPICSControlDUT()

                def generator():
                    yield dut.cs.eq(cs)
                    for _ in range(8):
                        yield
                        self.assertEqual((yield dut.pads.cs_n), cs_n)

                run_simulation(dut, generator())

    def test_different_selection_stays_asserted(self):
        for first_cs, second_cs, second_cs_n in [
            (0b01, 0b10, 0b01),
            (0b10, 0b01, 0b10),
        ]:
            with self.subTest(first_cs=first_cs, second_cs=second_cs):
                dut = _LiteSPICSControlDUT()

                def generator():
                    # Complete a transfer and start the inter-transfer delay.
                    yield dut.cs.eq(first_cs)
                    for _ in range(8):
                        yield
                    yield dut.cs.eq(0)
                    yield

                    # A different chip can be selected immediately and must remain selected.
                    yield dut.cs.eq(second_cs)
                    for _ in range(8):
                        yield
                        self.assertEqual((yield dut.pads.cs_n), second_cs_n)

                run_simulation(dut, generator())

    def test_same_selection_observes_delay(self):
        dut = _LiteSPICSControlDUT()

        def generator():
            yield dut.cs.eq(0b01)
            for _ in range(8):
                yield
            yield dut.cs.eq(0)
            yield

            yield dut.cs.eq(0b01)
            yield
            self.assertEqual((yield dut.pads.cs_n), 0b11)

            for _ in range(8):
                yield
            self.assertEqual((yield dut.pads.cs_n), 0b10)

        run_simulation(dut, generator())
