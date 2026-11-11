```
              __   _ __      _______  ____
             / /  (_) /____ / __/ _ \/  _/
            / /__/ / __/ -_)\ \/ ___// /
           /____/_/\__/\__/___/_/  /___/

    Copyright (c) 2020-2024, LiteSPI Developers
```
[![](https://github.com/litex-hub/litespi/workflows/ci/badge.svg)](https://github.com/litex-hub/litespi/actions) ![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg) [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/litex-hub/litespi)

[> Intro
--------
LiteSPI provides a small footprint and configurable SPI core.

LiteSPI is part of LiteX libraries whose aims are to lower entry level of
complex FPGA cores by providing simple, elegant and efficient implementations of components used in
today's SoC such as Ethernet, SATA, PCIe, SDRAM Controller...

Using Migen to describe the HDL allows the core to be highly and easily configurable.

LiteSPI can be used as LiteX library or can be integrated with your standard
design flow by generating the verilog rtl that you will use as a standard core.

[> Features
-----------
PHY:
  - Portable/Generic.
  - Single/Dual/Quad/Octal SPI Bus support.
  - Dynamic Clk frequency configuration and auto-calibration.
  - Pin-level SPI NOR flash read model for simulation.

Core:
  - Dynamic Crossbar.
  - MMAP read accesses.
  - CSR-based read/write accesses.

[> Documentation
----------------
The **SPI Flash & SPI Memory Core manual** is the reference of LiteSPI: a nightly
[PDF](https://github.com/litex-hub/litespi/releases/download/manual-nightly/litespi_manual.pdf)
and [HTML page](https://github.com/litex-hub/litespi/releases/download/manual-nightly/litespi_manual.html)
are published on the [manual-nightly](https://github.com/litex-hub/litespi/releases/tag/manual-nightly)
release. Sources in [doc/manual](doc/manual/README.md) (build: `python3 doc/manual/build.py`, outputs in
`build/doc/`; pandoc, XeLaTeX and the fonts listed in the README of `doc/manual`):

- **Understand**: [introduction](doc/manual/01_introduction.md), [SPI memories in a nutshell](doc/manual/02_spi_primer.md)
  (bus, modes, x-y-z widths, command phases), [inside a SPI NOR flash](doc/manual/03_flash_primer.md)
  (erase and program, status registers, QE bit, 4-byte addressing, XIP).
- **The core**: [architecture](doc/manual/04_architecture.md), [PHYs](doc/manual/05_phys.md),
  [memory-mapped reads and writes](doc/manual/06_mmap.md), [register master](doc/manual/07_master.md),
  [SPI memory database](doc/manual/08_modules.md).
- **Use it**: [integration in a LiteX SoC](doc/manual/09_integration.md), [BIOS, boot and flash update](doc/manual/10_software.md),
  [supported FPGAs and boards](doc/manual/11_boards.md), [simulation and tests](doc/manual/12_simulation.md),
  [debugging](doc/manual/13_debugging.md).
- **Appendices**: [registers](doc/manual/A_registers.md), [build options](doc/manual/B_build_options.md),
  [glossary](doc/manual/C_glossary.md), [performance and resources](doc/manual/D_performance.md),
  [maintaining this manual](doc/manual/E_maintenance.md) (for contributors).

[> Getting started
------------------

Examples of integration can be found on various supported boards of [LiteX-Boards](https://github.com/litex-hub/litex-boards) repository.

[> Tests
--------
Unit tests are available in ./test/.
To run all the unit tests:
  python3 -m pytest -v
Tests can also be run individually:
  python3 -m pytest -v test/test_name.py

[> License
----------
LiteSPI is released under the very permissive two-clause BSD license. Under
the terms of this license, you are authorized to use LiteSPI for closed-source
proprietary designs.
Even though we do not require you to do so, those things are awesome, so please
do them if possible:
 - tell us that you are using LiteSPI
 - cite LiteSPI in publications related to research it has helped
 - send us feedback and suggestions for improvements
 - send us bug reports when something goes wrong
 - send us the modifications and improvements you have done to LiteSPI.
