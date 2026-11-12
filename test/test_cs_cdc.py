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


class _CDCFlash(SpiNorFlashModule):
    manufacturer_id = SpiNorFlashManufacturerIDs.NONJEDEC
    device_id       = 0x1234
    name            = "cdc"

    total_size  = 256
    page_size   = 256
    total_pages = 1

    supported_opcodes = [
        Codes.READ_1_1_1,
        Codes.PP_1_1_1,
    ]
    dummy_bits = 8


# DUT ----------------------------------------------------------------------------------------------

class _LiteSPICDCDUT(Module):
    """MMAP and real SDR PHY with the PHY (and the flash model) in a separate "spi" clock domain."""
    def __init__(self):
        self.clock_domains.cd_spi = ClockDomain()

        self.flash = flash = _CDCFlash(Codes.READ_1_1_1)
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
            clock_domain    = "spi",
            default_divisor = 4,
            cs_delay        = 0,
        )
        self.submodules.spi = LiteSPI(
            phy          = phy,
            clock_domain = "spi",
            with_master  = False,
            with_csr     = False,
        )
        self.submodules.flash_model = ClockDomainsRenamer("spi")(LiteSPINORFlashModel(
            pads  = pads,
            flash = flash,
            init  = list(range(128)),
        ))


class TestLiteSPICSCDC(unittest.TestCase):
    def _run(self, sys_period, spi_period):
        dut         = _LiteSPICDCDUT()
        results     = []
        cs_selects  = []
        # Non-sequential word addresses: each read is a new command, after a CS release of one
        # sys cycle in the MMAP.
        addresses = [0, 8, 1, 2, 16]

        def generator():
            for address in addresses:
                results.append((yield from dut.spi.bus.read(address)))

        def cs_monitor():
            yield "passive"
            cs_n_d = (yield dut.pads.cs_n)
            while True:
                cs_n = (yield dut.pads.cs_n)
                if cs_n_d and not cs_n:
                    cs_selects.append(1)
                cs_n_d = cs_n
                yield

        run_simulation(dut,
            generators = {"sys": [generator()], "spi": [cs_monitor()]},
            clocks     = {"sys": sys_period, "spi": spi_period},
        )
        expected = [int.from_bytes(bytes(range(4*a, 4*a + 4)), "big") for a in addresses]
        return results, expected, len(cs_selects)

    def _check(self, sys_period, spi_period):
        # Every CS release between two commands reaches the pads (one CS selection per command)
        # and every word reads correctly.
        results, expected, cs_selects = self._run(sys_period, spi_period)
        self.assertEqual([hex(r) for r in results], [hex(e) for e in expected])
        # 4 commands (5 reads, 1 -> 2 is sequential): 4 CS selections on the pads.
        self.assertEqual(cs_selects, 4)

    def test_cs_release_phy_slower_than_sys(self):
        self._check(sys_period=10, spi_period=37)

    def test_cs_release_phy_as_fast_as_sys(self):
        self._check(sys_period=10, spi_period=10)

    def test_cs_release_phy_faster_than_sys(self):
        self._check(sys_period=37, spi_period=10)


if __name__ == "__main__":
    unittest.main()
