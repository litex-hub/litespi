#
# This file is part of LiteSPI.
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause

import unittest

from migen import *
from migen.sim import run_simulation

from litespi import LiteSPI
from litespi.flash_model import LiteSPINORFlashModel
from litespi.ids import SpiNorFlashManufacturerIDs
from litespi.opcodes import SpiNorFlashOpCodes as Codes
from litespi.phy.generic import LiteSPIPHY
from litespi.spi_nor_flash_module import SpiNorFlashModule


class _ProgramFlash(SpiNorFlashModule):
    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id       = 0x1234
    name            = "program"

    total_size  = 512
    page_size   = 256
    total_pages = 2

    supported_opcodes = [
        Codes.READ_1_1_1,
        Codes.PP_1_1_1,
    ]
    dummy_bits = 8


# DUT ----------------------------------------------------------------------------------------------

class _MMAPFlashWriteDUT(Module):
    """MMAP flash writes (with_write="csr") through the real SDR PHY to the programming flash model."""
    def __init__(self):
        self.flash = flash = _ProgramFlash(Codes.READ_1_1_1, program_cmd=Codes.PP_1_1_1)
        self.pads  = pads  = Record([
            ("clk",  1),
            ("cs_n", 1),
            ("mosi", 1),
            ("miso", 1),
        ])
        self.submodules.phy = phy = LiteSPIPHY(
            pads            = pads,
            flash           = flash,
            device          = "sim",
            default_divisor = 4,
            cs_delay        = 0,
        )
        self.submodules.spi = LiteSPI(
            phy             = phy,
            with_master     = False,
            with_csr        = False,
            with_mmap_write = "csr",
        )
        self.submodules.flash_model = LiteSPINORFlashModel(
            pads           = pads,
            flash          = flash,
            init           = [],
            with_program   = True,
            program_cycles = 200,
        )


class TestMMAPFlashWrite(unittest.TestCase):
    def test_mmap_flash_write_sends_wren_and_polls_wip(self):
        dut       = _MMAPFlashWriteDUT()
        mmap      = dut.spi.mmap
        results   = []
        opcodes   = []
        # Words 62, 63 end page 0; word 64 starts page 1 (new program command); word 10 is a new
        # program command at another address.
        writes = [
            (62, 0x11223344),
            (63, 0x55667788),
            (64, 0x99aabbcc),
            (10, 0x0f1e2d3c),
        ]

        def generator():
            yield mmap.write_config.fields.write_enable.eq(1)
            yield
            for address, data in writes:
                yield from mmap.bus.write(address, data)
            yield mmap.write_config.fields.write_enable.eq(0)
            yield
            for address, _ in writes:
                results.append((yield from mmap.bus.read(address)))
            results.append((yield from mmap.bus.read(65)))

        def opcode_monitor():
            # First transfer of each command (CS released in between) at the MMAP output.
            yield "passive"
            new_command = True
            while True:
                if (yield mmap.source.valid) and (yield mmap.source.ready):
                    if new_command:
                        opcodes.append((yield mmap.source.data))
                    new_command = False
                if not (yield mmap.request):
                    new_command = True
                yield

        run_simulation(dut, [generator(), opcode_monitor()])

        self.assertEqual([hex(r) for r in results], [hex(d) for _, d in writes] + ["0xffffffff"])
        # Each program command: WREN, then PP, then RDSR polling before the next command.
        wren, pp, rdsr, read = Codes.WREN.code, Codes.PP_1_1_1.code, Codes.RDSR.code, Codes.READ_1_1_1.code
        self.assertEqual(opcodes, [
            wren, pp,         # Words 62 and 63 (one program command).
            rdsr, wren, pp,   # Word 64 (page boundary).
            rdsr, wren, pp,   # Word 10.
            rdsr, read,       # Reads of words 62 to 64 (one burst).
            read,             # Word 10.
            read,             # Word 65.
        ])


if __name__ == "__main__":
    unittest.main()
