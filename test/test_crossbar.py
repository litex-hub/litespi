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
