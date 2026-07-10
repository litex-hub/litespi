#
# This file is part of LiteSPI.
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

import unittest

from migen import *
from migen.fhdl.specials import Tristate
from migen.sim import run_simulation

from litex.build.io import SDRTristate

from litespi import LiteSPI
from litespi.flash_model import LiteSPINORFlashModel
from litespi.ids import SpiNorFlashManufacturerIDs
from litespi.opcodes import SpiNorFlashOpCodes as Codes
from litespi.phy.generic import LiteSPIPHY
from litespi.spi_nor_flash_module import SpiNorFlashModule


class _ModelFlash(SpiNorFlashModule):
    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id       = 0x1234
    name            = "model"

    total_size  = 256
    page_size   = 256
    total_pages = 1

    supported_opcodes = [
        Codes.READ_1_1_1,
        Codes.READ_1_1_1_FAST,
        Codes.READ_1_1_1_4B,
        Codes.READ_1_1_2,
        Codes.READ_1_2_2,
        Codes.READ_1_1_4,
        Codes.READ_1_4_4,
        Codes.READ_4_4_4,
        Codes.READ_1_1_8,
        Codes.READ_1_8_8,
        Codes.PP_1_1_1,
    ]
    dummy_cycles = {
        Codes.READ_1_1_1_FAST : 8,
        Codes.READ_1_1_2      : 8,
        Codes.READ_1_2_2      : 6,
        Codes.READ_1_1_4      : 8,
        Codes.READ_1_4_4      : 6,
        Codes.READ_4_4_4      : 6,
        Codes.READ_1_1_8      : 8,
        Codes.READ_1_8_8      : 4,
    }


# Quad I/O simulation ------------------------------------------------------------------------------

class _SPIBus:
    def __init__(self, width):
        self.controller_o  = Signal(width)
        self.controller_oe = Signal(width)
        self.flash_o       = Signal(width)
        self.flash_oe      = Signal(width)


class _SimSDRTristateImpl(Module):
    def __init__(self, dr, bus):
        controller_o  = Signal.like(dr.o)
        controller_oe = Signal.like(dr.oe)

        self.sync += [
            controller_o.eq(dr.o),
            controller_oe.eq(dr.oe),
            dr.i.eq(bus.flash_o & bus.flash_oe),
        ]
        self.comb += [
            bus.controller_o.eq(controller_o),
            bus.controller_oe.eq(controller_oe),
        ]


class _SimSDRTristate:
    bus = None

    @classmethod
    def lower(cls, dr):
        return _SimSDRTristateImpl(dr, cls.bus)


# DUT ----------------------------------------------------------------------------------------------

class _LiteSPIFlashModelDUT(Module):
    def __init__(self, opcode):
        self.flash = flash = _ModelFlash(opcode)
        init = list(range(128))

        if flash.bus_width == 1:
            self.pads = pads = Record([
                ("clk",  1),
                ("cs_n", 1),
                ("mosi", 1),
                ("miso", 1),
            ])
            self.bus = None
            model_pads = pads
        else:
            io_width = max(4, flash.cmd_width, flash.addr_width, flash.bus_width)
            self.pads = pads = Record([
                ("clk",  1),
                ("cs_n", 1),
                ("dq",   io_width),
            ])
            self.bus = bus = _SPIBus(io_width)
            model_pads = Record([
                ("clk",  1),
                ("cs_n", 1),
                ("dq_i", io_width),
                ("dq_o", io_width),
                ("dq_oe", io_width),
            ])
            self.comb += [
                model_pads.clk.eq(pads.clk),
                model_pads.cs_n.eq(pads.cs_n),
                model_pads.dq_i.eq(bus.controller_o),
                bus.flash_o.eq(model_pads.dq_o),
                bus.flash_oe.eq(model_pads.dq_oe),
            ]

        self.submodules.phy = phy = LiteSPIPHY(
            pads            = pads,
            flash           = flash,
            device          = "sim",
            default_divisor = 4,
            cs_delay        = 0,
        )
        self.submodules.spi = spi = LiteSPI(
            phy         = phy,
            with_master = False,
            with_csr    = False,
        )
        self.submodules.flash_model = LiteSPINORFlashModel(
            pads  = model_pads,
            flash = flash,
            init  = init,
        )


class TestLiteSPINORFlashModel(unittest.TestCase):
    def _run_reads(self, opcode):
        dut        = _LiteSPIFlashModelDUT(opcode)
        results    = []
        collisions = []

        def monitor():
            yield "passive"
            while True:
                if dut.bus is not None:
                    if (yield dut.bus.controller_oe & dut.bus.flash_oe):
                        collisions.append(1)
                yield

        def generator():
            results.append((yield from dut.spi.bus.read(0)))
            results.append((yield from dut.spi.bus.read(1)))
            results.append((yield from dut.spi.bus.read(16)))
            results.append((yield from dut.spi.bus.read(40)))

        special_overrides = {}
        if dut.bus is not None:
            _SimSDRTristate.bus = dut.bus
            special_overrides[SDRTristate] = _SimSDRTristate

        run_simulation(
            dut,
            [generator(), monitor()],
            special_overrides = special_overrides,
        )
        return results, collisions

    def test_reads_through_real_phy(self):
        for opcode in [
            Codes.READ_1_1_1,
            Codes.READ_1_1_1_FAST,
            Codes.READ_1_1_1_4B,
            Codes.READ_1_1_2,
            Codes.READ_1_2_2,
            Codes.READ_1_1_4,
            Codes.READ_1_4_4,
            Codes.READ_4_4_4,
            Codes.READ_1_1_8,
            Codes.READ_1_8_8,
        ]:
            with self.subTest(opcode=opcode.desc):
                results, collisions = self._run_reads(opcode)
                self.assertEqual(results, [0x00010203, 0x04050607, 0x40414243, 0xffffffff])
                self.assertEqual(collisions, [])

    def test_rejects_non_byte_initialization(self):
        flash = _ModelFlash(Codes.READ_1_1_1)
        pads  = Record([
            ("clk",  1),
            ("cs_n", 1),
            ("mosi", 1),
            ("miso", 1),
        ])
        with self.assertRaisesRegex(ValueError, "byte values"):
            LiteSPINORFlashModel(pads, flash, init=[0x100])

    def test_regular_dq_pad_mapping(self):
        flash = _ModelFlash(Codes.READ_1_1_4)
        pads  = Record([
            ("clk",  1),
            ("cs_n", 1),
            ("dq",   4),
        ])
        dut = LiteSPINORFlashModel(pads, flash)
        fragment = dut.get_fragment()
        tristates = [special for special in fragment.specials if isinstance(special, Tristate)]
        tristates.sort(key=lambda special: special.target.start)

        self.assertEqual(len(tristates), 4)
        for n, special in enumerate(tristates):
            self.assertIs(special.target.value, pads.dq)
            self.assertEqual((special.target.start, special.target.stop), (n, n + 1))

    def test_rejects_ddr_commands(self):
        class _DDRModelFlash(_ModelFlash):
            supported_opcodes = _ModelFlash.supported_opcodes + [Codes.READ_1_1_1_DTR]

        flash = _DDRModelFlash(Codes.READ_1_1_1_DTR)
        pads  = Record([
            ("clk",  1),
            ("cs_n", 1),
            ("mosi", 1),
            ("miso", 1),
        ])
        with self.assertRaisesRegex(ValueError, "only supports SDR"):
            LiteSPINORFlashModel(pads, flash)


if __name__ == "__main__":
    unittest.main()
