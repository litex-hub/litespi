#
# This file is part of LiteSPI
#
# Copyright (c) 2021 George Hilliard <thirtythreeforty@gmail.com>
# SPDX-License-Identifier: BSD-2-Clause

import unittest

from migen import *

from litespi.crossbar import LiteSPICrossbar
from litespi.common import *


class TestCrossbar(unittest.TestCase):
    def test_cs_mux(self):
        dut = LiteSPICrossbar('sys')
        dut.comb += dut.master.source.ready.eq(True)

        a_cs, b_cs, c_cs = Signal(), Signal(), Signal()
        port_a = dut.get_port(a_cs)
        port_b = dut.get_port(b_cs)
        port_c = dut.get_port(c_cs)

        def process():
            yield

            self.assertEqual((yield dut.cs), 0)

            yield a_cs.eq(True)
            yield

            self.assertEqual((yield dut.cs), 1)
            self.assertEqual((yield port_a.sink.ready), True)
            self.assertEqual((yield port_b.sink.ready), False)
            self.assertEqual((yield port_c.sink.ready), False)

            yield a_cs.eq(False)
            yield b_cs.eq(True)
            yield # beat to allow cs to fall

            self.assertEqual((yield dut.cs), 0)

            yield
            self.assertEqual((yield dut.cs), 1)
            self.assertEqual((yield port_a.sink.ready), False)
            self.assertEqual((yield port_b.sink.ready), True)
            self.assertEqual((yield port_c.sink.ready), False)

            yield a_cs.eq(True)
            yield b_cs.eq(False)
            yield # beat to allow cs to fall

            self.assertEqual((yield dut.cs), 0)

            yield

            self.assertEqual((yield dut.cs), 1)
            self.assertEqual((yield port_a.sink.ready), True)
            self.assertEqual((yield port_b.sink.ready), False)
            self.assertEqual((yield port_c.sink.ready), False)

        run_simulation(dut, process())

    def test_cs_multiple(self):
        dut = LiteSPICrossbar('sys')
        dut.comb += dut.master.source.ready.eq(True)

        out1 = dut.add_output_cs()
        out2 = dut.add_output_cs()
        out3 = dut.add_output_cs()

        all_out = Cat(out1, out2, out3)

        a_cs = Signal(2)
        b_cs = Signal()
        c_cs = Signal()
        d_cs = Signal(2)

        port_a = dut.get_port(a_cs, output_cs=Cat(out1, out2))
        port_b = dut.get_port(b_cs)  # legacy (dut.cs)
        port_c = dut.get_port(c_cs, output_cs=out3)  # explicit single
        port_d = dut.get_port(d_cs, output_cs=Cat(out1, out2))

        def process():
            self.assertEqual((yield all_out), 0x0)

            yield a_cs.eq(0b01)  # select out1
            yield

            self.assertEqual((yield all_out), 0x1)
            self.assertEqual((yield port_a.sink.ready), True)
            self.assertEqual((yield port_b.sink.ready), False)
            self.assertEqual((yield port_c.sink.ready), False)
            self.assertEqual((yield port_d.sink.ready), False)

            yield a_cs.eq(0b10)  # select out2
            yield

            self.assertEqual((yield all_out), 0x2)
            self.assertEqual((yield port_a.sink.ready), True)
            self.assertEqual((yield port_b.sink.ready), False)
            self.assertEqual((yield port_c.sink.ready), False)
            self.assertEqual((yield port_d.sink.ready), False)

            yield a_cs.eq(0)
            yield d_cs.eq(0b10)  # select out2
            yield  # beat to allow cs to fall
            yield

            self.assertEqual((yield all_out), 0x2)
            self.assertEqual((yield port_a.sink.ready), False)
            self.assertEqual((yield port_b.sink.ready), False)
            self.assertEqual((yield port_c.sink.ready), False)
            self.assertEqual((yield port_d.sink.ready), True)

        run_simulation(dut, process(), vcd_name='xbar.vcd')

    def test_invalid_output_cs(self):
        dut = LiteSPICrossbar('sys')
        with self.assertRaises(AssertionError):
            dut.get_port(Signal(1), output_cs=Signal(2))
