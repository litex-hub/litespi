#
# This file is part of LiteSPI
#
# Copyright (c) 2021 George Hilliard <thirtythreeforty@gmail.com>
# SPDX-License-Identifier: BSD-2-Clause

import unittest

from migen import *

from litespi.core.master import LiteSPIMaster
from litespi.common import *


class TestSPIMaster(unittest.TestCase):
    def test_spi_txrx_loopback(self):
        dut = LiteSPIMaster()
        dut.comb += dut.source.ready.eq(dut.sink.ready)
        dut.comb += dut.sink.valid.eq(dut.source.valid)
        dut.comb += dut.sink.data.eq(dut.source.data)

        dut.comb += dut._rxtx.we.eq(dut._status.fields.rx_ready)

        write_seq = list(range(0x20))
        read_seq = []

        def do_write():
            write_iter = iter(write_seq)
            byte = next(write_iter)
            cycles = 0

            while write_seq != read_seq:
                # write to queue
                if (yield dut._status.fields.tx_ready) == 1 and byte is not None:
                    yield dut._rxtx.re.eq(1)
                    yield dut._rxtx.r.eq(byte)
                    try:
                        byte = next(write_iter)
                    except StopIteration:
                        byte = None
                else:
                    yield dut._rxtx.re.eq(0)

                # read from queue, .we is comb connected to .rx_ready
                if (yield dut._status.fields.rx_ready) == 1:
                    read_seq.append((yield dut._rxtx.w))

                yield

                cycles += 1
                if cycles == 40:
                    return

        run_simulation(dut, do_write())
        self.assertListEqual(write_seq, read_seq)
