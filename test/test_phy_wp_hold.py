#
# This file is part of LiteSPI.
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

import unittest

from migen import *

from litex.build.io import SDROutput, SDRInput, SDRTristate, DDROutput, DDRTristate

from litespi.modules import S25FL128L
from litespi.opcodes import SpiNorFlashOpCodes as Codes
from litespi.phy.generic import LiteSPIPHY

# Helpers ------------------------------------------------------------------------------------------

class _Observed:
    o  = None
    oe = None

class _SimSDROutputImpl(Module):
    def __init__(self, dr):
        self.sync += dr.o.eq(dr.i)

class _SimSDROutput:
    @staticmethod
    def lower(dr):
        return _SimSDROutputImpl(dr)

class _SimIgnore:
    @staticmethod
    def lower(dr):
        return Module()

class _SimTristateImpl(Module):
    def __init__(self, o, oe):
        self.comb += [
            _Observed.o.eq(o),
            _Observed.oe.eq(oe),
        ]

class _SimSDRTristate:
    @staticmethod
    def lower(dr):
        return _SimTristateImpl(dr.o, dr.oe)

class _SimDDRTristate:
    @staticmethod
    def lower(dr):
        return _SimTristateImpl(dr.o1, dr.oe1)

def _x1_pads():
    return Record([("clk", 1), ("cs_n", 1), ("mosi", 1), ("miso", 1), ("wp", 1), ("hold", 1)])

def _x4_pads():
    return Record([("clk", 1), ("cs_n", 1), ("dq", 4)])

def _run(dut, generator):
    run_simulation(dut, generator, special_overrides={
        SDROutput   : _SimSDROutput,
        SDRInput    : _SimIgnore,
        SDRTristate : _SimSDRTristate,
        DDROutput   : _SimIgnore,
        DDRTristate : _SimDDRTristate,
    })

# WP#/HOLD# Tests ----------------------------------------------------------------------------------

class TestLiteSPIWPHold(unittest.TestCase):
    def test_x1_wp_hold_high(self):
        for rate in ["1:1", "1:2"]:
            with self.subTest(rate=rate):
                dut       = Module()
                dut.pads  = pads = _x1_pads()
                dut.submodules.phy = LiteSPIPHY(pads, S25FL128L(Codes.READ_1_1_1), device="xc7a35t", rate=rate)
                _Observed.o  = Signal(2)
                _Observed.oe = Signal(2)
                levels = []

                def generator():
                    yield
                    levels.append(((yield pads.wp), (yield pads.hold)))

                _run(dut, generator())
                self.assertEqual(levels, [(1, 1)])

    def test_x4_dq2_dq3(self):
        for rate in ["1:1", "1:2"]:
            for read_cmd, program_cmd, high in [
                (Codes.READ_1_1_1, Codes.PP_1_1_1, 0b1100), # DQ2/DQ3 are WP#/HOLD#: driven high.
                (Codes.READ_1_1_4, Codes.PP_1_1_1, 0b0000), # Quad read: DQ2/DQ3 are data.
                (Codes.READ_1_1_1, Codes.PP_1_1_4, 0b0000), # Quad program: DQ2/DQ3 are data.
            ]:
                with self.subTest(rate=rate, read=read_cmd.code, program=program_cmd.code):
                    dut       = Module()
                    dut.pads  = pads = _x4_pads()
                    flash     = S25FL128L(read_cmd, program_cmd=program_cmd)
                    dut.submodules.phy = LiteSPIPHY(pads, flash, device="xc7a35t", rate=rate)
                    _Observed.o  = Signal(4)
                    _Observed.oe = Signal(4)
                    levels = []

                    def generator():
                        yield
                        levels.append(((yield _Observed.o) & 0b1100, (yield _Observed.oe) & 0b1100))

                    _run(dut, generator())
                    self.assertEqual(levels, [(high, high)])


if __name__ == "__main__":
    unittest.main()
