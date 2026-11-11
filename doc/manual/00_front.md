```{=latex}
\frontmatter
```

# About this document {.unnumbered}

This manual is the reference of the LiteSPI project: a SPI flash and SPI memory core for FPGAs,
its PHYs for the FPGA families it supports, its memory-mapped and register frontends, its database
of SPI memories and the software that uses it at boot. It is written for FPGA engineers who need a
flash in a design, and it teaches SPI memories along the way.

No prior knowledge of SPI memories is assumed. Part I explains the SPI bus, the commands of a SPI
memory and what is inside a NOR flash, and points at the module that implements each mechanism.
Part II then describes the core: its architecture, the PHYs, the memory-mapped frontend, the
register master and the module database.

Part III is the user guide: the integration in a LiteX SoC, the BIOS and the flash update, the
supported boards, the simulation and the debugging. The appendices hold the register reference,
the build options, the glossary, the performance figures and the maintenance notes of this manual.

| If you want to | Read |
|------------------------------------------|----------------------------------------------|
| Know what the project does and does not | [Introduction](#introduction) |
| Check what is validated on hardware | [Status](#intro-status) |
| Learn how a SPI memory is driven | [SPI memories in a nutshell](#spi-primer) |
| Understand erase, program and quad enable | [Inside a SPI NOR flash](#flash-primer) |
| Check that your FPGA or board is supported | [Supported FPGAs and boards](#boards) |
| Add a flash to your own SoC | [Integration in a LiteX SoC](#integration) |
| Boot from the flash or update it | [BIOS, boot and flash update](#software) |
| Understand a flash that does not answer | [Debugging](#debugging) |

The manual follows the repository: every name, number and default is taken from the source code,
and the manual is generated from it on the date printed on the title page. When the code and the
manual disagree, the code is right and the manual has a bug.

## Conventions {.unnumbered}

- Numbers: `0x` prefix for hexadecimal, `0b` for binary. Flash commands are written with their
  datasheet mnemonic and their opcode, such as RDID (`0x9f`).
- Rates: SCK and system clock frequencies in MHz; throughputs in MB/s (10^6 bytes per second),
  except in BIOS logs, quoted as printed (KiB/s, MiB/s). Sizes in bytes, KiB and MiB.
- A *mode x-y-z* gives the number of data lines of the command, address and data phases, such as
  1-1-4. The opcode names of the module database write it with underscores, such as `READ_1_1_4`.
- *The core* is the `LiteSPI` wrapper, that is the frontends and the crossbar. *The PHY* drives
  the pins. *The SDR PHY* divides the system clock to make SCK; *the 1:2 PHY* runs SCK at the
  system clock with DDR I/O registers. Neither one uses the double transfer rate (DTR) of the flash.
- *The MMAP* is the memory-mapped frontend; *the master* is the register frontend.
- *The module* is a class of the SPI memory database of `litespi/modules/`, such as `W25Q128JV`;
  *the flash* is the physical chip on the board.
- *The BIOS* is the LiteX BIOS and its SPI flash library, `liblitespi`.
- `<target>` stands for the name of a target script of LiteX-Boards without its extension, such as
  `digilent_arty`.
- `<module>` stands for the name of a module class, such as `W25Q128JV`.
- Paths are relative to the repository root. Shell commands are given for a Linux host.
- When the text names a source file, it is the file to open to check or extend the fact.
