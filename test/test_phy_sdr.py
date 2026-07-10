#
# This file is part of LiteSPI.
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

import unittest

from migen import *
from migen.fhdl.specials import Instance
from migen.sim import run_simulation

from litespi.clkgen import LiteSPIClkGen
from litespi.phy.generic_sdr import LiteSPISDRPHYCore


class _SPIPads:
    def __init__(self):
        self.cs_n = Signal(reset=1)
        self.mosi = Signal()
        self.miso = Signal()


class _ClockPads:
    def __init__(self, with_clk):
        if with_clk:
            self.clk = Signal()


class _LiteSPISDRPHYDUT(Module):
    def __init__(self):
        self.pads = _SPIPads()
        self.submodules.phy = LiteSPISDRPHYCore(
            pads            = self.pads,
            flash           = None,
            device          = "xc7a35t",
            clock_domain    = "sys",
            default_divisor = 8,
            cs_delay        = 10,
        )


class _IgnoreInstance:
    @staticmethod
    def lower(instance):
        return Module()


class TestLiteSPISDRPHY(unittest.TestCase):
    def test_startup_cycles_validation(self):
        for startup_cycles in [-1, 0.5]:
            with self.subTest(startup_cycles=startup_cycles):
                with self.assertRaisesRegex(ValueError, "non-negative integer"):
                    LiteSPIClkGen(
                        pads           = _ClockPads(with_clk=True),
                        device         = None,
                        startup_cycles = startup_cycles,
                    )

    def test_startup_ready_without_startupe2(self):
        for device, with_clk in [("xc7a35t", True), ("LFE5U-45F", False)]:
            with self.subTest(device=device, with_clk=with_clk):
                dut = Module()
                dut.submodules.clkgen = LiteSPIClkGen(
                    pads   = _ClockPads(with_clk),
                    device = device,
                )

                def generator():
                    self.assertEqual((yield dut.clkgen.ready), 1)
                    yield
                    self.assertEqual((yield dut.clkgen.ready), 1)

                run_simulation(
                    dut,
                    generator(),
                    special_overrides = {Instance : _IgnoreInstance},
                )

    @staticmethod
    def _run_first_transfer(idle_cycles):
        dut       = _LiteSPISDRPHYDUT()
        completed = []

        def generator():
            yield dut.phy.clk_divisor.storage.eq(8)
            yield dut.phy.source.ready.eq(1)
            for _ in range(idle_cycles):
                yield

            yield dut.phy.cs.eq(1)
            yield dut.phy.sink.data.eq(0x9f)
            yield dut.phy.sink.len.eq(8)
            yield dut.phy.sink.width.eq(1)
            yield dut.phy.sink.mask.eq(1)
            yield dut.phy.sink.valid.eq(1)

            accepted = False
            for cycle in range(200):
                if (yield dut.phy.sink.ready):
                    accepted = True
                    yield dut.phy.sink.valid.eq(0)

                if (yield dut.phy.source.valid):
                    completed.append((accepted, cycle))
                    break
                yield

        run_simulation(
            dut,
            generator(),
            special_overrides = {Instance : _IgnoreInstance},
        )
        return completed

    def test_first_transfer_waits_for_startup(self):
        # Sweep the first request across startup and an entire SCK period. This includes the
        # boundary where transfer start previously coincided with the last STARTUPE2 edge.
        for idle_cycles in range(64):
            with self.subTest(idle_cycles=idle_cycles):
                completed = self._run_first_transfer(idle_cycles)
                self.assertTrue(completed)
                self.assertTrue(completed[0][0])

    def test_cs_stays_inactive_during_startup(self):
        dut          = _LiteSPISDRPHYDUT()
        accepted     = []
        cs_errors    = []
        ready_errors = []

        def generator():
            yield dut.phy.clk_divisor.storage.eq(8)
            yield dut.phy.cs.eq(1)
            yield dut.phy.sink.data.eq(0x9f)
            yield dut.phy.sink.len.eq(8)
            yield dut.phy.sink.width.eq(1)
            yield dut.phy.sink.mask.eq(1)
            yield dut.phy.sink.valid.eq(1)

            for cycle in range(64):
                startup_ready = yield dut.phy.clkgen.ready
                if not startup_ready and not (yield dut.pads.cs_n):
                    cs_errors.append(cycle)
                if (yield dut.phy.sink.ready):
                    accepted.append(cycle)
                    if not startup_ready:
                        ready_errors.append(cycle)
                    break
                yield

        run_simulation(
            dut,
            generator(),
            special_overrides = {Instance : _IgnoreInstance},
        )
        self.assertTrue(accepted)
        self.assertEqual(cs_errors, [])
        self.assertEqual(ready_errors, [])
