# Glossary {#glossary}

The terms of SPI memories and of LiteSPI used in this manual, in alphabetical order. Each entry
points to the chapter that explains it.

| Term | Meaning |
|------------------|---------------------------------------------------------------------------------|
| 1:2 PHY | The PHY built with `rate="1:2"` (`LiteSPIDDRPHYCore`): SCK runs at the PHY clock (the system clock unless `clock_domain` is set) through DDR I/O, with SDR data on the flash side. See [PHYs](#phys) |
| 4-byte addressing | Addresses of 32 bits, needed above 16 MiB; opcodes whose name ends in `_4B`. See [Inside a SPI NOR flash](#flash-primer) |
| BIOS | The LiteX BIOS and its `liblitespi` library, which initialize, calibrate, program and boot from the flash. See [BIOS, boot and flash update](#software) |
| Block | Erase unit of 32 or 64 KiB of a NOR flash. See [Inside a SPI NOR flash](#flash-primer) |
| Burst | MMAP reads at consecutive addresses served under one command, CS held low between them. See [Memory-mapped reads and writes](#mmap) |
| Calibration | BIOS step that lowers the divisor while the CRC of the first 256 bytes stays the same. See [BIOS, boot and flash update](#software) |
| CCLK | Configuration clock pin of a Xilinx FPGA; the flash on it is clocked through STARTUPE2 or STARTUPE3. See [PHYs](#phys) |
| Command | Everything between CS going low and CS going high: opcode, address, dummy and data phases. See [SPI memories in a nutshell](#spi-primer) |
| CPHA | Clock phase: the SCK edge on which the data is sampled. See [SPI memories in a nutshell](#spi-primer) |
| CPOL | Clock polarity: the level of SCK while idle. See [SPI memories in a nutshell](#spi-primer) |
| Crossbar | `LiteSPICrossbar`: shares the PHY between the MMAP and the master, one command at a time. See [Architecture](#architecture) |
| CS | Chip select, active low (`cs_n`): selects the flash and frames a command. See [SPI memories in a nutshell](#spi-primer) |
| CS control | `LiteSPICSControl`: drives `cs_n` and keeps CS high for `cs_delay` cycles between commands. See [Architecture](#architecture) |
| Divisor | Value that sets SCK of the SDR PHY from the system clock (`clk_divisor`). See [PHYs](#phys) |
| DQ0 to DQ7 | Data lines of the flash; in x1 mode DQ0 is MOSI and DQ1 is MISO. See [SPI memories in a nutshell](#spi-primer) |
| DTR | Double transfer rate: data on both SCK edges on the flash side. Not supported by the PHYs. See [SPI memories in a nutshell](#spi-primer) |
| Dummy cycles | SCK cycles between the address and the data of a fast read, while the flash prepares the data. The MMAP sends the whole gap as one dummy phase, so the count of a module must include the mode-bit cycles. See [SPI memories in a nutshell](#spi-primer) |
| Erase | Command that sets every bit of a sector, block or the whole chip to 1. See [Inside a SPI NOR flash](#flash-primer) |
| Flash model | `LiteSPINORFlashModel`: pin-level model of a SPI NOR read, for Migen simulations. See [Simulation and tests](#simulation) |
| JEDEC ID | Manufacturer, memory type and capacity bytes returned by RDID (`0x9f`). See [Inside a SPI NOR flash](#flash-primer) |
| Master | `LiteSPIMaster`: frontend that sends transfers written to registers, for any command. See [The register master](#master) |
| MISO, MOSI | The data input and output of single-line SPI, seen from the controller. See [SPI memories in a nutshell](#spi-primer) |
| MMAP | `LiteSPIMMAP`: frontend that serves bus reads, and optional writes, as flash commands. See [Memory-mapped reads and writes](#mmap) |
| Mode bits | Bits after the address of some fast reads that can keep the chip in a continuous read mode; LiteSPI sends none, its outputs are off during the dummy phase. See [Inside a SPI NOR flash](#flash-primer) |
| Mode x-y-z | Lines used for the command, the address and the data, such as 1-1-4. See [SPI memories in a nutshell](#spi-primer) |
| Module | A class of the database describing one chip, such as `W25Q128JV`. See [The SPI memory database](#modules) |
| NOR flash | Non-volatile memory read like a memory and written by page program after an erase. See [Inside a SPI NOR flash](#flash-primer) |
| OPI | Octal mode with the command on eight lines (8-8-8); the opcode table defines no such command. See [SPI memories in a nutshell](#spi-primer) |
| Page | Program unit of a NOR flash, 256 bytes on most chips. See [Inside a SPI NOR flash](#flash-primer) |
| Page program | Command (PP, `0x02`) that clears bits in up to one page. See [Inside a SPI NOR flash](#flash-primer) |
| Phase | One part of a command: command (opcode), address, dummy or data. See [SPI memories in a nutshell](#spi-primer) |
| PHY | `LiteSPIPHY` and its implementations: turn transfers into pin activity. See [PHYs](#phys) |
| PHY model | `LiteSPIPHYModel`: stream-level replacement of the PHY backed by a memory, used by `litex_sim`. See [Simulation and tests](#simulation) |
| PSRAM | Pseudo-static RAM with a SPI interface (SPI RAM), such as `APS6404L`. See [Inside a SPI NOR flash](#flash-primer) |
| QE bit | Quad enable bit of a status or configuration register, needed by quad reads. See [Inside a SPI NOR flash](#flash-primer) |
| QPI | Mode in which the command, the address and the data use four lines (4-4-4), entered by a command. See [Inside a SPI NOR flash](#flash-primer) |
| QSPI | Quad SPI: four data lines, DQ0 to DQ3. See [SPI memories in a nutshell](#spi-primer) |
| SCK | Serial clock driven by the controller. See [SPI memories in a nutshell](#spi-primer) |
| SDR | Single data rate: one bit per line per SCK cycle on the flash side. See [SPI memories in a nutshell](#spi-primer) |
| SDR PHY | The PHY built with `rate="1:1"` (`LiteSPISDRPHYCore`): SCK divided from the system clock. See [PHYs](#phys) |
| Sector | Smallest erase unit of a NOR flash, 4 KiB on most chips. See [Inside a SPI NOR flash](#flash-primer) |
| SFDP | Serial Flash Discoverable Parameters (`0x5a`): tables in the chip describing its commands; not read by LiteSPI. See [Inside a SPI NOR flash](#flash-primer) |
| SPI | Serial Peripheral Interface: one controller, a clock, a chip select per device, and data lines. See [SPI memories in a nutshell](#spi-primer) |
| SPI mode 0, 3 | CPOL and CPHA both 0, or both 1; the two modes of SPI memories. See [SPI memories in a nutshell](#spi-primer) |
| STARTUPE2, STARTUPE3 | Xilinx primitives that reach the configuration flash pins: CCLK on 7-Series; CCLK, CS and DQ on UltraScale+. See [PHYs](#phys) |
| Transfer | One element of the core-to-PHY stream: data, length, width, mask and divisor. See [Architecture](#architecture) |
| USRMCLK | ECP5 primitive that drives the MCLK configuration pin. See [PHYs](#phys) |
| WEL | Write enable latch: status bit set by WREN (`0x06`), needed before a program or an erase. See [Inside a SPI NOR flash](#flash-primer) |
| WIP | Write in progress: status bit set while a program or an erase runs. See [Inside a SPI NOR flash](#flash-primer) |
| x1, x2, x4, x8 | Data width of a PHY or a pad set. See [PHYs](#phys) |
| XIP | Execute in place: the CPU runs code directly from the memory-mapped flash. See [Integration in a LiteX SoC](#integration) |
