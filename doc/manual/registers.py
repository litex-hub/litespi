#
# This file is part of LiteSPI project.
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# Register appendix of the manual: which designs tools/csr_doc.py elaborates and which register banks
# it documents (the engine is generic, part of the manual kit).

import json
import os
import sys
import tempfile

# Configurations: name -> parameters of the reference design below (shown in the appendix table).
# Both designs add a S25FL128L flash in 1-1-4 mode with SoC.add_spi_flash on the Arty A7 platform,
# with every optional register of the core: MMAP writes under register control and the master
# interrupt. The first uses the SDR PHY (divisor and mode registers), the second the 1:2 PHY (divisor
# register).
CONFIGS = {
    "sdr" : ['rate="1:1"', 'mode="4x"', "S25FL128L(READ_1_1_4)", "clk_freq=25e6",
             'with_mmap_write="csr"', "master_with_irq=True"],
    "ddr" : ['rate="1:2"', 'mode="4x"', "S25FL128L(READ_1_1_4)", "clk_freq=25e6",
             'with_mmap_write="csr"', "master_with_irq=True"],
}

# Banks documented in the appendix (prefix match on the bank name), in order, with their title and
# the Python class that defines them. SoC.add_spi_flash puts the whole core in one bank named after
# its `name` argument, `spiflash` by default.
BANKS = [
    ("spiflash", "SPI flash", "LiteSPI", "litespi/__init__.py"),
]

# Descriptions of the LiteSPI registers. Most registers are declared without a description in the
# gateware, so they are given here and attached to the elaborated registers before the dump; a
# description declared in the gateware takes precedence. Keys: (bank, register).
DESCRIPTIONS = {
    ("spiflash", "mmap_clk_divisor")   : "Divisor of the MMAP commands, sent with each transfer. 0: use `phy_clk_divisor`.",
    ("spiflash", "mmap_dummy_bits")    : "Dummy phase of the MMAP read command, in bits at the address width (dummy cycles x address lines). The reset value is `dummy_cycles` x `addr_width` of the module for a fast read, else 0. Present with `with_csr=True` (default).",
    ("spiflash", "mmap_write_config")  : "Bit 0 `write_enable`: 1 sends the Wishbone writes to the chip as page programs (`program_cmd` of the module), 0 acknowledges and drops them. The MMAP sends no write enable (WREN) itself. Present with `with_mmap_write=\"csr\"`.",
    ("spiflash", "master_cs")          : "Chip select of the master, one bit per CS line: 1 selects the chip (CS low) and holds the PHY through the crossbar, 0 ends the command.",
    ("spiflash", "master_rxtx")        : "Write: push one transfer of `phyconfig.len` bits, right aligned, to the TX FIFO. Read: pop the 32-bit word shifted in during one transfer from the RX FIFO.",
    ("spiflash", "master_clk_divisor") : "Divisor of the master transfers, sent with each transfer. 0: use `phy_clk_divisor`.",
    ("spiflash", "phy_clk_divisor")    : "SCK divisor of the PHY. SDR PHY: SCK = sys / (2 x ceil(div / 2)), sys / 2 for div 0 to 2. 1:2 PHY: SCK = sys / div, sys for div 0 or 1. The reset value is the `default_divisor` of the PHY, computed by `add_spi_flash` from `clk_freq`. Used when a transfer carries a 0 divisor.",
}

# Notes printed after the title of a bank family: what the register descriptions do not say.
NOTES = {
    "spiflash": [
        "The registers come from three blocks of the core, named by their prefix: `phy_` for the",
        "SDR PHY ([PHYs](#phys)), `mmap_` for the memory-mapped frontend ([Memory-mapped reads",
        "and writes](#mmap)) and `master_` for the register master ([The register master](#master)).",
        "Which registers a build has depends on its configuration:",
        "",
        "| Registers | Present when |",
        "|------------------------------------|----------------------------------------------------|",
        "| `phy_clk_divisor` | Both PHYs (also `LiteSPIXilinxUSPHY`) |",
        "| `phy_mode` | SDR PHY (`rate=\"1:1\"`, also `LiteSPIXilinxUSPHY`); absent with the 1:2 PHY |",
        "| `mmap_clk_divisor` | MMAP present (`with_mmap=True` and a module given) |",
        "| `mmap_dummy_bits` | MMAP present and `with_csr=True` (default) |",
        "| `mmap_write_config` | MMAP present and `with_mmap_write=\"csr\"` |",
        "| `master_cs` to `master_clk_divisor` | `with_master=True` (default) |",
        "| `master_ev_status`, `_pending`, `_enable` | `with_master=True` and `master_with_irq=True` (set by `add_spi_flash` when the CPU has an interrupt named after the core) |",
        "",
        "The table below gives the offsets of the `sdr` configuration. The 1:2 PHY of the `ddr`",
        "configuration has no `phy_mode` register, so the offsets of the other registers differ:",
        "software uses the names of the `csr.csv` of its own build, never these offsets.",
        "",
        "`phy_mode`: the clock generator uses bit 1 only, as the idle level of SCK",
        "(`litespi/clkgen.py`); write 0 for mode 0 and 3 for mode 3. In both modes the PHY",
        "changes its outputs on the falling edge of SCK and samples on the rising edge.",
        "",
        "`master_rxtx` is a LiteX `CSR`, a register with separate write and read data: the",
        "Access column shows `wo` for its type, but software also reads it to pop the RX FIFO.",
        "",
        "The `master_ev_` registers hold one event, `rx_ready` (bit 0): its pending bit is set",
        "when the RX FIFO goes from empty to holding a word.",
    ],
}

# Opening paragraph of the appendix and the sentence that ends the access paragraph.
INTRO = ["This appendix lists the registers of LiteSPI. It is generated from the register",
         "definitions of the gateware, elaborated on two reference designs for the Arty A7",
         "platform without running an FPGA toolchain: these configurations are elaborated only,",
         "not built nor run on hardware. Both add a flash with `SoC.add_spi_flash`; the first",
         "uses the SDR PHY, the second the 1:2 PHY. Offsets are in bytes from the base of the",
         "bank; the base addresses depend on the SoC and are in the `csr.csv` of a build. A",
         "LiteX SoC names the bank after the `name` argument of `add_spi_flash`, `spiflash` by",
         "default."]
USAGE = ["The BIOS",
         "and `liblitespi` use these names through the generated `csr.h`",
         "(`spiflash_phy_clk_divisor_write()`, for example), so they never need the offsets."]
MAIN_BANK = "Registers of the top-level `main` bank of the SoC."


def _describe(soc):
    """Attach the descriptions of DESCRIPTIONS to the registers that have none in the gateware."""
    for bank, region in soc.csr.regions.items():
        if not isinstance(region.obj, list):
            continue
        for csr in region.obj:
            desc = DESCRIPTIONS.get((bank, csr.name))
            if desc and not (getattr(csr, "description", None) or "").strip():
                csr.description = desc


def _reference_soc(rate):
    """Reference design: SoCMini on the Arty A7 platform with a quad SPI flash."""
    from migen.genlib.io import CRG
    from litex.soc.integration.soc_core import SoCMini
    from litex_boards.platforms import digilent_arty
    from litespi.modules import S25FL128L
    from litespi.opcodes import SpiNorFlashOpCodes as Codes

    class ReferenceSoC(SoCMini):
        def __init__(self):
            platform = digilent_arty.Platform()
            self.crg = CRG(platform.request("clk100"))
            SoCMini.__init__(self, platform, clk_freq=100e6)
            self.add_spi_flash(mode="4x", module=S25FL128L(Codes.READ_1_1_4), rate=rate,
                clk_freq        = 25e6,
                with_mmap_write = "csr",
                master_with_irq = True)

    return ReferenceSoC()


def elaborate(name, repo_root):
    """Elaborate a reference design with a Builder that runs no toolchain; return
    (soc, csr_json, module, argv)."""
    # The LiteSPI of this repository, not an installed one.
    sys.path.insert(0, repo_root)
    from litex.soc.integration.builder import Builder
    rate = {"sdr": "1:1", "ddr": "1:2"}[name]
    old_cwd = os.getcwd()
    with tempfile.TemporaryDirectory() as tmp:
        os.chdir(tmp)
        try:
            soc     = _reference_soc(rate)
            builder = Builder(soc, output_dir=tmp, csr_csv=os.path.join(tmp, "csr.csv"),
                csr_json=os.path.join(tmp, "csr.json"), compile_software=False,
                compile_gateware=False)
            builder.build(run=False)
            csr_json = json.load(open(os.path.join(tmp, "csr.json")))
        finally:
            os.chdir(old_cwd)
    # Memories mapped on the CSR bus have no register definitions: keep the register banks only.
    for bank, region in list(soc.csr.regions.items()):
        if not isinstance(region.obj, list):
            del soc.csr.regions[bank]
    _describe(soc)
    return soc, csr_json, "digilent_arty", CONFIGS[name]
