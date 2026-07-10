#
# This file is part of LiteSPI.
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

import unittest

from migen import *

from litex.build.io import DDROutput, DDRTristate
from litex.build.lattice.platform import LatticePlatform
from litex.build.xilinx.platform import XilinxPlatform

from litespi.phy.generic_ddr import LiteSPIDDRPHYCore


# DDR I/O simulation -------------------------------------------------------------------------------

class _DDRBus:
    def __init__(self, width, input_latency=0):
        self.i             = Signal(width)
        self.o             = Signal(width)
        self.oe            = Signal(width)
        self.input_latency = input_latency


class _SimDDROutputImpl(Module):
    def __init__(self, dr):
        i1 = Signal.like(dr.i1)
        i2 = Signal.like(dr.i2)

        self.sync += [
            i1.eq(dr.i1),
            i2.eq(dr.i2),
        ]
        self.comb += dr.o.eq(Mux(dr.clk, i1, i2))


class _SimDDROutput:
    @staticmethod
    def lower(dr):
        return _SimDDROutputImpl(dr)


class _SimDDRTristateImpl(Module):
    def __init__(self, dr, bus):
        o1  = Signal.like(dr.o1)
        o2  = Signal.like(dr.o2)
        oe1 = Signal.like(dr.oe1)
        oe2 = Signal.like(dr.oe1)
        # Match the registered DDR input path and model optional platform I/O latency.
        i1_pipeline = [Signal.like(dr.i1) for _ in range(1 + 2*bus.input_latency)]
        i2_pipeline = [Signal.like(dr.i2) for _ in range(1 + 2*bus.input_latency)]

        self.sync += [
            o1.eq(dr.o1),
            o2.eq(dr.o2),
            oe1.eq(dr.oe1),
            i1_pipeline[0].eq(bus.i),
            dr.i1.eq(i1_pipeline[-1]),
            dr.i2.eq(i2_pipeline[-1]),
        ]
        for i in range(1, len(i1_pipeline)):
            self.sync += i1_pipeline[i].eq(i1_pipeline[i - 1])
            self.sync += i2_pipeline[i].eq(i2_pipeline[i - 1])
        self.sync.sys_n += i2_pipeline[0].eq(bus.i)

        if dr.oe2 is None:
            self.comb += bus.oe.eq(oe1)
        else:
            self.sync += oe2.eq(dr.oe2)
            self.comb += bus.oe.eq(Mux(dr.clk, oe1, oe2))

        self.comb += bus.o.eq(Mux(dr.clk, o1, o2))


class _SimDDRTristate:
    bus = None

    @classmethod
    def lower(cls, dr):
        return _SimDDRTristateImpl(dr, cls.bus)


# DDR PHY DUT --------------------------------------------------------------------------------------

class _LiteSPIDDRPHYDUT(Module):
    def __init__(self, width, extra_latency):
        self.clock_domains.cd_sys_n = ClockDomain(reset_less=True)

        if width == 1:
            self.pads = pads = Record([
                ("clk",  1),
                ("cs_n", 1),
                ("mosi", 1),
                ("miso", 1),
            ])
            io_width = 2
        else:
            self.pads = pads = Record([
                ("clk",  1),
                ("cs_n", 1),
                ("dq",   width),
            ])
            io_width = width

        self.bus = _DDRBus(io_width, input_latency=extra_latency)
        self.submodules.phy = LiteSPIDDRPHYCore(
            pads           = pads,
            flash          = None,
            extra_latency  = extra_latency,
            cs_delay       = 0,
            with_sdr_cs    = False,
        )


class _LiteSPIDDRPHYElaborationDUT(Module):
    def __init__(self, width):
        self.clock_domains.cd_sys = ClockDomain()

        if width == 1:
            self.pads = pads = Record([
                ("clk",  1),
                ("cs_n", 1),
                ("mosi", 1),
                ("miso", 1),
            ])
            pads_ios = {pads.clk, pads.cs_n, pads.mosi, pads.miso}
        else:
            self.pads = pads = Record([
                ("clk",  1),
                ("cs_n", 1),
                ("dq",   width),
            ])
            pads_ios = {pads.clk, pads.cs_n, pads.dq}

        self.submodules.phy = LiteSPIDDRPHYCore(
            pads     = pads,
            flash    = None,
            cs_delay = 0,
        )
        self.ios = pads_ios | {self.cd_sys.clk, self.cd_sys.rst}


# DDR PHY Tests ------------------------------------------------------------------------------------

class TestLiteSPIDDRPHY(unittest.TestCase):
    # sys_n provides the falling half-cycle used by the behavioral DDR input model.
    clocks = {
        "sys"   : 10,
        "sys_n" : (10, 5),
    }

    special_overrides = {
        DDROutput   : _SimDDROutput,
        DDRTristate : _SimDDRTristate,
    }

    @staticmethod
    def _transfer(phy, data, length, width, mask):
        yield phy.sink.data.eq(data)
        yield phy.sink.len.eq(length)
        yield phy.sink.width.eq(width)
        yield phy.sink.mask.eq(mask)
        yield phy.sink.valid.eq(1)

        while not (yield phy.sink.ready):
            yield

        yield phy.sink.valid.eq(0)
        while not (yield phy.source.valid):
            yield

        result = yield phy.source.data
        yield
        return result

    def _run(self, dut, generators):
        _SimDDRTristate.bus = dut.bus
        run_simulation(
            dut,
            generators,
            clocks            = self.clocks,
            special_overrides = self.special_overrides,
        )

    def test_output_data_and_clock_edges(self):
        for width in [1, 2, 4, 8]:
            with self.subTest(width=width):
                dut    = _LiteSPIDDRPHYDUT(width=width, extra_latency=0)
                phy    = dut.phy
                groups = [i & (2**width - 1) for i in range(1, 32//width + 1)]
                data   = 0
                trace  = []

                for group in groups:
                    data = (data << width) | group

                def monitor():
                    yield "passive"
                    while True:
                        yield
                        if (yield dut.pads.clk):
                            trace.append(((yield dut.bus.oe), (yield dut.bus.o)))

                def generator():
                    yield phy.source.ready.eq(1)
                    yield phy.cs.eq(1)
                    for _ in range(3):
                        yield

                    yield from self._transfer(
                        phy    = phy,
                        data   = data,
                        length = 32,
                        width  = width,
                        mask   = 1 if width == 1 else 2**width - 1,
                    )

                    yield phy.cs.eq(0)
                    for _ in range(3):
                        yield

                    self.assertEqual((yield dut.pads.clk), 0)

                self._run(dut, {
                    "sys"   : generator(),
                    "sys_n" : monitor(),
                })

                output_mask = 1 if width == 1 else 2**width - 1
                self.assertEqual(len(trace), 32//width)
                self.assertEqual([oe & output_mask for oe, _ in trace], [output_mask]*len(trace))
                self.assertEqual([data & (2**width - 1) for _, data in trace], groups)

    def test_input_data_with_extra_latency(self):
        for width in [1, 2, 4, 8]:
            for extra_latency in [0, 1]:
                with self.subTest(width=width, extra_latency=extra_latency):
                    dut      = _LiteSPIDDRPHYDUT(width=width, extra_latency=extra_latency)
                    phy      = dut.phy
                    expected = 0x12345678
                    groups   = [
                        (expected >> shift) & (2**width - 1)
                        for shift in range(32 - width, -1, -width)
                    ]
                    edges    = []

                    def flash_model():
                        yield "passive"
                        index = 0
                        value = groups[index] << (1 if width == 1 else 0)
                        yield dut.bus.i.eq(value)

                        while True:
                            yield
                            if (yield dut.pads.clk):
                                edges.append(1)
                                index += 1
                                if index < len(groups):
                                    value = groups[index] << (1 if width == 1 else 0)
                                    yield dut.bus.i.eq(value)

                    def generator():
                        yield phy.source.ready.eq(1)
                        yield phy.cs.eq(1)
                        for _ in range(3):
                            yield

                        result = yield from self._transfer(
                            phy    = phy,
                            data   = 0,
                            length = 32,
                            width  = width,
                            mask   = 0,
                        )
                        self.assertEqual(result, expected)

                    self._run(dut, {
                        "sys"   : generator(),
                        "sys_n" : flash_model(),
                    })
                    self.assertEqual(len(edges), 32//width)

    def test_command_address_read_turnaround(self):
        dut          = _LiteSPIDDRPHYDUT(width=4, extra_latency=1)
        phy          = dut.phy
        command      = 0x6b
        address      = 0x123456
        expected     = 0x89abcdef
        input_groups = [(expected >> shift) & 0xf for shift in range(28, -1, -4)]
        output_bits  = []
        input_edges  = []
        read_active  = [False]

        def flash_model():
            yield "passive"
            input_index = 0

            while True:
                if read_active[0] and input_index == 0:
                    yield dut.bus.i.eq(input_groups[0])

                yield
                if not (yield dut.pads.clk):
                    continue

                if (yield dut.bus.oe) & 0x1:
                    output_bits.append((yield dut.bus.o) & 0x1)
                elif read_active[0]:
                    input_edges.append(1)
                    input_index += 1
                    if input_index < len(input_groups):
                        yield dut.bus.i.eq(input_groups[input_index])

        def generator():
            yield phy.source.ready.eq(1)
            yield phy.cs.eq(1)
            for _ in range(3):
                yield

            yield from self._transfer(phy, command, 8, 1, 0x1)
            self.assertEqual((yield dut.pads.cs_n), 0)

            yield from self._transfer(phy, address, 24, 1, 0x1)
            self.assertEqual((yield dut.pads.cs_n), 0)

            read_active[0] = True
            yield
            result = yield from self._transfer(phy, 0, 32, 4, 0)
            self.assertEqual(result, expected)

            yield phy.cs.eq(0)
            for _ in range(3):
                yield

            self.assertEqual((yield dut.pads.clk), 0)
            self.assertEqual((yield dut.pads.cs_n), 1)

        self._run(dut, {
            "sys"   : generator(),
            "sys_n" : flash_model(),
        })

        output = 0
        for bit in output_bits:
            output = (output << 1) | bit

        self.assertEqual(len(output_bits), 32)
        self.assertEqual(output, (command << 24) | address)
        self.assertEqual(len(input_edges), 8)


class TestLiteSPIDDRPHYElaboration(unittest.TestCase):
    @staticmethod
    def _get_verilog(platform, width):
        dut = _LiteSPIDDRPHYElaborationDUT(width=width)
        return str(platform.get_verilog(dut, ios=dut.ios))

    def test_lattice_nx_quad_io(self):
        platform = LatticePlatform("LIFCL-40", [], toolchain="radiant")
        verilog  = self._get_verilog(platform, width=4)

        self.assertIn("ODDRX1", verilog)
        self.assertIn("IDDRX1", verilog)
        self.assertIn("OFD1P3BX", verilog)

    def test_xilinx_7series_single_io(self):
        platform = XilinxPlatform("xc7a35t-csg324-1", [], toolchain="vivado")
        verilog  = self._get_verilog(platform, width=1)

        self.assertIn("ODDR", verilog)
        self.assertIn("IDDR", verilog)


if __name__ == "__main__":
    unittest.main()
