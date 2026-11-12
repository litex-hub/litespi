# Inside a SPI NOR flash {#flash-primer}

This chapter explains what happens inside a SPI NOR flash when it is read, erased and programmed,
and the registers that configure it. It covers the commands that every flash driver needs: write
enable, busy polling, quad enable, identification and 4-byte addressing. It ends with SPI RAM and
with executing code from the flash.

The previous chapter, [SPI memories in a nutshell](#spi-primer), describes the bus and the read
command. As there, the commands below are the common ones; the datasheet of each chip is the
reference for its details.

## The NOR array {#flash-array}

A NOR flash stores each bit in a floating-gate transistor that keeps its charge without power.
Reading is fast and random: any byte can be read at any address, which is why a CPU can execute
code from a NOR flash. Writing is slow and coarse, and it works in two steps, erase and program.

The array is organised in three levels, as the figure below shows. A *page* is the unit of
programming, usually 256 bytes. A *sector* is the smallest unit of erasing, usually 4 KiB. A
*block* groups sectors, usually 32 KiB or 64 KiB, and can be erased in one command.

![Organisation of a 16 MiB flash such as the W25Q128JV: 256 blocks of 64 KiB, each made of 16
sectors of 4 KiB, each made of 16 pages of 256 bytes.](flash_array.svg)

In LiteSPI, a module class gives the total size and the page size of a chip; 466 of the 481 NOR
flash modules have 256-byte pages. A module can also carry an erase geometry, the erase command
with its size ([The SPI memory database](#modules)).

## Erase and program {#flash-erase}

Erasing sets every bit of a sector or block to 1: an erased flash reads `0xff`. Programming can only
clear bits, from 1 to 0. To write new data, software therefore erases the sectors first, then
programs the pages. On most chips, programming a byte twice without an erase gives the AND of the
two values.

A page program (PP, `0x02`) sends an address and up to one page of data. The chip programs the
bytes into the page of that address. When the data runs past the end of the page, most chips wrap
around to the start of the same page, so software must split its writes on page boundaries. The
`flash_write` command of the BIOS does so only from a page-aligned offset: it programs 256-byte
chunks from the given offset, so an unaligned write wraps inside each page
([BIOS, boot and flash update](#software)).

The table below lists the usual erase commands, as named in the opcode table of LiteSPI.

| Command | Opcode | Erases | Name in the database |
|----------------------|----------|------------------|------------------------|
| Sector erase | `0x20` | 4 KiB | `BE_4K` |
| Block erase | `0x52` | 32 KiB | `BE_32K` |
| Block erase | `0xd8` | 64 KiB | `SE` |
| Chip erase | `0xc7` or `0x60` | whole chip | `CHIP_ERASE`, `CHIP_ERASE_ALT` |

The database follows an older naming, where `SE` is the 64 KiB erase and `BE_4K` the 4 KiB one.

Erasing and programming wear the cells: each sector supports a limited number of erase cycles,
given by the datasheet. Both operations also take far longer than a read. A page program keeps the
chip busy much longer than reading a page, a sector erase longer again, and a chip erase longest.

In LiteSPI, a module may list its erase commands with their sizes. The modules above 16 MiB with
4-byte erase commands list them, 4-byte sector erase `SE_4B` first ([Erase commands](#mod-erase)).
A module that lists none uses the 64 KiB `SE` command with a 3-byte address, or the command given
by `erase_cmd` when the design instantiates it. The BIOS erases and programs through the master, then reads the result back through the MMAP to
verify it ([BIOS, boot and flash update](#software)).

## Write enable and busy polling {#flash-wip}

A flash refuses to erase or program unless it was first told to accept a write. The write enable
command (WREN, `0x06`) sets the *write enable latch* (WEL) of the chip; the next erase, program or
register write uses it, and the chip clears it when that operation completes.

During an erase or a program the chip is busy and ignores most commands. Its status register 1
shows this with the *write in progress* bit (WIP, bit 0). Software reads it with RDSR (`0x05`) until
the bit returns to 0, as the figure below shows.

![Programming a page. WREN sets the write enable latch; PP sends the address and the data; then RDSR
is sent again and again until WIP reads 0. Each command is framed by its own CS low
period.](flash_program.svg)

In LiteSPI, software sequences these commands through the master ([The register master](#master)):
the BIOS sends WREN before each erase and program, and polls WIP with RDSR after it. MMAP flash
writes sequence them in the core ([Writes](#mmap-write)).

## Status registers and quad enable {#flash-qe}

A flash has one or more status and configuration registers. Status register 1 (SR1) holds WIP and
WEL, the block protection bits and, on some chips, the *quad enable* (QE) bit. Other chips keep QE
in a second register, called status register 2 (SR2) or configuration register 1 (CR1), as the
figure below shows. Software writes these registers with WRSR (`0x01`), after WREN.

![Where the quad enable bit lives. On ISSI and Macronix chips, QE is bit 6 of SR1, next to the block
protection bits (BP), WEL and WIP; on Spansion chips, QE is bit 1 of CR1, and many other chips keep
it at bit 1 of SR2.](flash_status.svg)

While QE is 0, DQ2 and DQ3 keep their write protect and hold functions, and quad commands do not
work. Setting QE turns them into data lines. On many chips QE is non-volatile: it is set once and
survives power cycles.

The module database records the method of each chip that needs a known one, with its `quad_enable`
attribute. The BIOS applies it at boot when the design uses the x4 pads, the chosen read uses four
data lines and the module supports `READ_1_1_4`, as the table below shows.

| `quad_enable` | Register, bit | Sequence of the BIOS | Modules |
|----------------------|---------------|---------------------------------------------|-----------|
| `wrsr_sr1_bit6` | SR1, bit 6 | Read SR1, WREN, WRSR with QE set, check | ISSI, Macronix |
| `wrr_cr1_bit1` | CR1, bit 1 | Read SR1 and CR1 (`0x35`), WREN, WRSR with both, check | Spansion |
| not set | | WREN, then WRSR (`0x01`) with the bytes `0x43` and `0x07` | others |

The generic sequence writes SR1 and SR2 in one WRSR. `0x43` sets bit 6 of SR1 and `0x07` sets bit 1
of SR2, so it covers both usual QE positions. It also writes every other bit of both registers: on
SR1 it clears the block protection bits and SRWD (bits 0 and 1, WIP and WEL, are read-only), and on
SR2 it sets bits 0 and 2, whose meaning depends on the chip. Check them in the datasheet, or give
the module a `quad_enable` method.

The opcodes of these registers are not standard: `0x35` reads CR1 on Spansion chips and SR2 on
Winbond chips, but enters QPI mode on Macronix chips. This is why the database stores the method per
chip instead of guessing it.

## QPI mode {#flash-qpi}

In QPI mode (4-4-4), every command, including its opcode, uses four lines. The chip enters it on a
command and stays in it until another command or a reset. The opcode that enters QPI differs
between vendors: `0x35` on Macronix and ISSI chips and on the `APS6404L`, `0x38` on Winbond chips
that have a QPI mode.

In LiteSPI, a module that lists `READ_4_4_4` and is built for that read is *QPI capable*. The BIOS
then sends `0x35` on one line, only after the quad enable succeeded, and the MMAP sends all its
phases on four lines; the master commands of the BIOS stay on one line. QPI is [in
development](#intro-status).

## Identification: JEDEC ID and SFDP {#flash-id}

Nearly all flashes answer the RDID command (`0x9f`) with three bytes: the manufacturer, a memory
type and a capacity code. A W25Q128JV (ordering codes -IQ and -JQ) answers `0xef`, `0x40`, `0x18`:
`0xef` is Winbond, `0x40` gives the memory type, and `0x18`, that is 24, stands for 2^24 bytes, or
16 MiB, on this chip. The -IM and -JM parts answer `0xef`, `0x70`, `0x18`.

In LiteSPI, a module gives the first byte as its `manufacturer_id` and the next two as its
`device_id`: `0x7018` for the `W25Q128JV` module (the -IM/JM value), `0x4018` for the `W25Q128`
module. The BIOS sends RDID at boot but discards the answer, which it prints only in its debug build
([Debugging](#debugging)). Reading `0xff` or `0x00` usually means that the flash does not answer at
all.

Many recent flashes also describe themselves in SFDP tables, read with RDSFDP (`0x5a`) and defined
by the JEDEC standard JESD216. They give the read modes, the dummy cycles, the erase sizes and the
quad enable method. LiteSPI does not read them: the module class of the database gives the same
information when the design is built.

## Addresses above 16 MiB {#flash-4byte}

A 3-byte address reaches 2^24 bytes, that is 16 MiB. Larger flashes need a fourth address byte,
as the figure below shows, and offer one or more of three ways to send it:

- *4-byte opcodes*: separate commands that always take a 4-byte address, such as `0x13` for a slow
  read or `0x6c` for a 1-1-4 read.
- *4-byte mode*: after EN4B (`0xb7`), the usual commands take 4-byte addresses, until EX4B
  (`0xe9`).
- *Extended address register*: a register, written with `0xc5` and read with `0xc8` on Winbond and
  Micron chips, gives the upper address byte of the 3-byte commands; other vendors use other
  opcodes.

![3-byte and 4-byte addresses. Three bytes reach the first 16 MiB of a flash; a 32 MiB flash needs
the fourth byte, A31-A24, to reach the second half, above `0x1000000`.](flash_4byte.svg)

In LiteSPI, a read opcode whose name ends with `_4B`, such as `READ_1_1_4_4B`, makes the MMAP send
4-byte addresses. Nothing in the core enters 4-byte mode or writes the extended address register.
The BIOS erases with the erase command of the module, a 4-byte opcode on the modules above 16 MiB
that list one. It programs with the 4-byte Page Program (`0x12`) when the module is above 16 MiB
and lists `PP_1_1_1_4B`, and with 3-byte addresses otherwise; it then refuses the addresses above
16 MiB. The 4-byte opcodes work whatever the address mode of the chip.

## Write protection {#flash-protect}

Flashes protect their content in two ways. The block protection bits (BP) of SR1 make part of the
array, counted from the top or the bottom, read-only. The status register write disable bit (SRWD)
and the WP# pin together lock the status register itself. In quad modes WP# becomes DQ2, so the pin
protection no longer applies.

The core does not set or clear the protection bits. The BIOS keeps them, except in its generic
quad enable sequence, which writes `0x43` to SR1 and so clears the block protection bits
([Status registers and quad enable](#flash-qe)). On a protected region, an erase or a program is
ignored by the chip, and the BIOS reports the bytes that read back wrong after the operation.

## SPI RAM {#flash-psram}

A SPI PSRAM is a DRAM with a SPI interface and its own refresh. It has no erase: any byte can be
written at any time, and the data is lost at power off. It uses the same read commands as a flash,
and its write commands reuse the page program opcodes.

The `APS6404L` module describes such a chip: 8 MiB, with 1-1-1, 1-4-4 and 4-4-4 reads, and 1-1-1
and 1-4-4 writes.

`add_spi_ram` maps it as read-write memory, with MMAP writes enabled and an L2 cache in front
([Integration in a LiteX SoC](#integration)). SPI RAM support is [in development](#intro-status).

## Executing in place {#flash-xip}

Executing code from the flash (XIP) works because NOR flash reads are random. The cost is the
latency: each read at a new address pays a whole command, with opcode, address and dummy cycles,
before its first byte. Sequential reads are much cheaper, since the flash streams the following
bytes for as long as CS stays low.

LiteSPI's MMAP keeps CS low after each read. When the bus asks for the next word, it reads only the
data; a read elsewhere, or 256 idle cycles, ends the command. A CPU instruction cache or the LiteX
L2 cache turns most CPU fetches into such sequential reads ([Memory-mapped reads and
writes](#mmap)).

## In the code {#flash-code}

| Concept | Where |
|----------------------------------|------------------------------------------------------|
| Erase, program, register opcodes | `litespi/opcodes.py` (`SpiNorFlashOpCodes`) |
| Sizes, erase geometry, QE method | `litespi/spi_nor_flash_module.py`, `litespi/modules/modules.py` |
| Manufacturer identifiers | `litespi/ids.py` (`SpiNorFlashManufacturerIDs`) |
| SPI RAM module | `litespi/modules/ram_modules.py` (`APS6404L`) |
| BIOS erase, program, quad enable | `liblitespi/spiflash.c` of LiteX |

## Where to go next {#flash-next}

[Architecture](#architecture) for the structure of the core; [The SPI memory database](#modules)
for the module classes; [BIOS, boot and flash update](#software) for the boot sequence that uses
these commands.
