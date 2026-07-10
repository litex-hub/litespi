#
# This file is part of LiteSPI.
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

import unittest

from migen import *
from migen.fhdl.specials import Instance
from migen.sim import run_simulation

from litex.build.xilinx.platform import XilinxPlatform, XilinxUSPlatform

from litespi.phy.generic import LiteSPIXilinxUSPHY
from litespi.phy.generic_sdr import LiteSPISDRPHYCore
from litespi.phy.xilinx import LiteSPISTARTUPE2, LiteSPISTARTUPE3


class _IgnoreInstance:
    @staticmethod
    def lower(instance):
        return Module()


class _LiteSPIXilinxUSDUT(Module):
    def __init__(self, default_divisor=4):
        self.clock_domains.cd_sys = ClockDomain()
        self.submodules.phy = LiteSPIXilinxUSPHY(
            flash           = None,
            default_divisor = default_divisor,
            cs_delay        = 0,
        )


class _S7SPIPads:
    def __init__(self):
        self.cs_n = Signal(reset=1)
        self.mosi = Signal()
        self.miso = Signal()


class _LiteSPIXilinxS7DUT(Module):
    def __init__(self):
        self.clock_domains.cd_sys = ClockDomain()
        self.pads = pads = _S7SPIPads()
        self.submodules.phy = LiteSPISDRPHYCore(
            pads            = pads,
            flash           = None,
            device          = "xc7a35t",
            clock_domain    = "sys",
            default_divisor = 4,
            cs_delay        = 0,
        )
        self.ios = {self.cd_sys.clk, self.cd_sys.rst, pads.cs_n, pads.mosi, pads.miso}


class TestLiteSPISTARTUPE2(unittest.TestCase):
    def test_instance_port_mapping(self):
        dut      = _LiteSPIXilinxS7DUT()
        core     = dut.phy
        fragment = dut.get_fragment()

        self.assertIsInstance(core.clk_io, LiteSPISTARTUPE2)
        self.assertEqual(core.clk_io.startup_cycles, 3)

        instances = [
            special for special in fragment.specials
            if isinstance(special, Instance) and special.of == "STARTUPE2"
        ]
        self.assertEqual(len(instances), 1)

        ports = {
            item.name: item.expr
            for item in instances[0].items
            if hasattr(item, "expr")
        }
        self.assertIs(ports["USRCCLKO"], core.clk_io.clk)

    def test_7series_elaboration(self):
        platform = XilinxPlatform("xc7a35t-csg324-1", [], toolchain="vivado")
        dut      = _LiteSPIXilinxS7DUT()
        verilog  = str(platform.get_verilog(dut, ios=dut.ios, name="top"))
        self.assertEqual(verilog.count("STARTUPE2 STARTUPE2"), 1)
        self.assertIn(".USRCCLKO", verilog)


class TestLiteSPISTARTUPE3(unittest.TestCase):
    def test_registered_dq_mapping(self):
        dut = LiteSPISTARTUPE3()

        def generator():
            self.assertEqual((yield dut.dts), 0xf)
            yield dut.dq_o.eq(0xa)
            yield dut.dq_oe.eq(0x5)
            yield dut.di.eq(0xc)
            yield
            yield
            self.assertEqual((yield dut.do), 0xa)
            self.assertEqual((yield dut.dts), 0xa)
            self.assertEqual((yield dut.dq_i), 0xc)

        run_simulation(
            dut,
            generator(),
            special_overrides = {Instance : _IgnoreInstance},
        )

    def test_instance_port_mapping(self):
        dut       = _LiteSPIXilinxUSDUT()
        core      = dut.phy.spiflash_phy
        io        = core.io
        fragment  = dut.get_fragment()
        instances = [
            special for special in fragment.specials
            if isinstance(special, Instance) and special.of == "STARTUPE3"
        ]
        self.assertEqual(len(instances), 1)

        ports = {
            item.name: item.expr
            for item in instances[0].items
            if hasattr(item, "expr")
        }
        self.assertIs(ports["USRCCLKO"], io.pads.clk)
        self.assertIs(ports["FCSBO"], io.pads.cs_n)
        self.assertIs(ports["DO"], io.do)
        self.assertIs(ports["DTS"], io.dts)
        self.assertIs(ports["DI"], io.di)
        self.assertEqual(len(ports["DO"]), 4)
        self.assertEqual(len(ports["DTS"]), 4)
        self.assertEqual(len(ports["DI"]), 4)

    def test_ultrascale_elaboration(self):
        platform = XilinxUSPlatform("xcku5p-ffvb676-2-e", [], toolchain="vivado")
        verilog  = str(platform.get_verilog(_LiteSPIXilinxUSDUT(), name="top"))
        self.assertEqual(verilog.count("STARTUPE3 STARTUPE3"), 1)
        for port in ["USRCCLKO", "FCSBO", "FCSBTS", "DO", "DTS", "DI"]:
            self.assertIn(f".{port}", verilog)


class TestLiteSPIXilinxUSPHY(unittest.TestCase):
    @staticmethod
    def _transfer(core, data, length, width, mask):
        yield core.sink.data.eq(data)
        yield core.sink.len.eq(length)
        yield core.sink.width.eq(width)
        yield core.sink.mask.eq(mask)
        yield core.sink.valid.eq(1)

        while not (yield core.sink.ready):
            yield
        yield core.sink.valid.eq(0)

        while not (yield core.source.valid):
            yield
        return (yield core.source.data)

    def test_first_transfer_phases(self):
        for idle_cycles in range(32):
            with self.subTest(idle_cycles=idle_cycles):
                dut       = _LiteSPIXilinxUSDUT()
                core      = dut.phy.spiflash_phy
                completed = []

                def generator():
                    yield core.source.ready.eq(1)
                    for _ in range(idle_cycles):
                        yield
                    yield core.cs.eq(1)
                    yield from self._transfer(core, 0xa, 4, 4, 0xf)
                    completed.append(1)

                run_simulation(
                    dut,
                    generator(),
                    special_overrides = {Instance : _IgnoreInstance},
                )
                self.assertEqual(completed, [1])

    def test_output_data_and_direction(self):
        cases = [
            (1, 0xa5, 8, 0x1, [1, 0, 1, 0, 0, 1, 0, 1], 0xe),
            (4, 0x12345678, 32, 0xf, list(range(1, 9)), 0x0),
        ]
        for width, data, length, mask, expected, expected_dts in cases:
            with self.subTest(width=width):
                dut       = _LiteSPIXilinxUSDUT()
                core      = dut.phy.spiflash_phy
                io        = core.io
                edges     = []
                cs_errors = []

                def monitor():
                    yield "passive"
                    previous = 0
                    while True:
                        yield
                        clk = yield io.pads.clk
                        if not (yield core.clkgen.ready) and not (yield io.pads.cs_n):
                            cs_errors.append(1)
                        if not previous and clk and not (yield io.pads.cs_n):
                            edges.append(((yield io.do), (yield io.dts)))
                        previous = clk

                def generator():
                    yield core.source.ready.eq(1)
                    yield core.cs.eq(1)
                    yield from self._transfer(core, data, length, width, mask)

                run_simulation(
                    dut,
                    [generator(), monitor()],
                    special_overrides = {Instance : _IgnoreInstance},
                )
                self.assertEqual([value & (2**width - 1) for value, _ in edges], expected)
                self.assertEqual([dts for _, dts in edges], [expected_dts]*len(expected))
                self.assertEqual(cs_errors, [])

    def test_input_data_and_direction(self):
        for width in [1, 4]:
            with self.subTest(width=width):
                dut      = _LiteSPIXilinxUSDUT()
                core     = dut.phy.spiflash_phy
                io       = core.io
                expected = 0x89abcdef
                groups   = [
                    (expected >> shift) & (2**width - 1)
                    for shift in range(32 - width, -1, -width)
                ]
                edges    = []
                result   = []

                def flash_model():
                    yield "passive"
                    previous   = 0
                    index      = 0
                    saw_rising = False
                    value      = groups[0] << (1 if width == 1 else 0)
                    yield io.di.eq(value)

                    while True:
                        yield
                        clk = yield io.pads.clk
                        if not previous and clk and not (yield io.pads.cs_n):
                            saw_rising = True
                            edges.append((yield io.dts))
                        if saw_rising and previous and not clk and not (yield io.pads.cs_n):
                            index += 1
                            if index < len(groups):
                                value = groups[index] << (1 if width == 1 else 0)
                                yield io.di.eq(value)
                        previous = clk

                def generator():
                    yield core.source.ready.eq(1)
                    yield core.cs.eq(1)
                    result.append((yield from self._transfer(core, 0, 32, width, 0)))

                run_simulation(
                    dut,
                    [generator(), flash_model()],
                    special_overrides = {Instance : _IgnoreInstance},
                )
                self.assertEqual(result, [expected])
                self.assertEqual(edges, [0xf]*len(groups))
