# BIOS, boot and flash update {#software}

This chapter covers the software that drives LiteSPI: the initialization the LiteX BIOS runs at
boot, the console commands that read, erase and write the flash, the boot from an image in the
flash, and the ways to update the flash contents. The code lives in LiteX, in the `liblitespi`
library and the BIOS; the chapter describes the LiteX revision named in [Maintaining this
manual](#maintenance).

## At a glance {#sw-glance}

| Function | Where in LiteX | Needs |
|----------------------------|--------------------------------------------|---------------------------------|
| Initialization at boot | `liblitespi/spiflash.c`, `spiflash_init()` | Any `add_spi_flash` SoC |
| Quad enable, QPI entry | `spiflash.c` | The master and a quad module |
| Clock calibration | `spiflash.c`, `spiflash_freq_init()` | SDR PHY divisor register, a programmed flash |
| Flash commands | `bios/cmds/cmd_spiflash.c` | The master |
| `flashboot` | `bios/boot.c` | `FLASH_BOOT_ADDRESS` defined |
| Reads from the console | `mem_read`, `crc`, `mem_speed` | The MMAP region |

The BIOS knows the flash through the constants that `add_spi_flash` writes into the generated
headers ([What it computes](#integ-computed)). It never reads the JEDEC ID to choose a behaviour:
the module chosen at build time decides everything.

## BIOS initialization {#sw-init}

At boot, after the SoC summary, the BIOS calls `spiflash_init()`. The figure below shows its
steps; each one is skipped when the SoC or the module lacks what it needs.

![The initialization of the flash by the BIOS. Read the steps left to right; the three steps
under the line send commands through the master and are skipped without it; a failed quad enable
stops the sequence; the calibration (cyan) needs the divisor register of the SDR PHY.](sw_init.svg)

1. **Print the module.** `Initializing <module> SPI Flash @<base>...`, the base being the address
   of the `spiflash` region.
2. **Send RDID.** The master sends RDID (`0x9f`). The BIOS discards the answer: it prints it
   only with `SPIFLASH_DEBUG`, for debugging.
3. **Quad enable.** When `SPIFLASH_MODULE_QUAD_CAPABLE` is defined (mode `"4x"`, a read with
   four data lines and a module that lists `READ_1_1_4`), the BIOS prints `Enabling Quad mode...`
   and sets the QE bit with the method of the module (table below).
4. **QPI entry.** When the quad enable succeeded and `SPIFLASH_MODULE_QPI_CAPABLE` is defined, it
   prints `Switching to QPI mode...` and sends `0x35`.
5. **Clock calibration.** It searches the lowest working divisor ([Clock
   calibration](#sw-calibration)), unless `SPIFLASH_SKIP_FREQ_INIT` is defined.
6. **memspeed.** It measures sequential and random reads of 4 KiB at the start of the flash.

The quad enable method comes from the `quad_enable` attribute of the module, exported as the
constant `SPIFLASH_MODULE_QUAD_ENABLE_<method>` ([Status registers and quad enable](#flash-qe)):

| Method | Sequence | Check |
|------------------------------|--------------------------------------------------------|---------------------|
| `wrsr_sr1_bit6` | Read SR1; if bit 6 is clear, WREN, then WRSR with bit 6 set | SR1 bit 6 read back |
| `wrr_cr1_bit1` | Read SR1 and CR1 (`0x35`), WREN, then WRR writing SR1 and CR1 with bit 1 set | CR1 bit 1 read back |
| None | WREN, then the fixed bytes `01 43 07` | None |

The generic sequence, for a module without a method, writes SR1 and SR2 in one WRSR (`0x01`):
`0x43` sets bit 6 of SR1 and `0x07` sets bit 1 of SR2, so it covers both usual QE positions. It
also writes the other bits of both registers: on chips with the usual SR1 layout, it clears the
block protection bits and SRWD, and the other bits of SR2 are vendor specific (check them in the
datasheet). The two named methods keep the other bits.

After the write, the BIOS polls the WIP bit for up to about one second. If a status read returns
`0xff`, the write times out or the check fails, it prints an error and stops the initialization:
no QPI entry, no calibration and no memspeed follow. A module without a method is safest with its
QE bit already set.

The QPI entry sends `0x35` only, the Enable QPI command of some vendors; other chips use another
opcode ([QPI mode](#flash-qpi)). After it, the master still sends commands on one line. QPI is in
development (see the [status table](#intro-status)).

`litex_sim --with-spi-flash` shows these lines without a board; its boot log and the meaning of
each line are in [A SoC with the BIOS: litex_sim](#sim-litex-sim).

## Clock calibration {#sw-calibration}

The calibration finds the fastest SCK that still reads the flash correctly. It runs only when the
PHY has a `clk_divisor` register, that is with the SDR PHY and the 1:2 PHY. With the model PHY, the
BIOS only prints `SPIFLASH_PHY_FREQUENCY` in whole MHz.

The algorithm reads the first 256 bytes of the flash through the MMAP and keeps their CRC32 as the
reference. It then lowers the divisor step by step (by 2 for the SDR PHY, by 1 for the 1:2 PHY), flushes the caches and
reads the block again, until the CRC changes or the divisor reaches its minimum. It steps back to
the last divisor that matched, writes it into the PHY and MMAP divisor registers, and prints:

```console
SPI Flash clk configured to <MHz> MHz (div: <divisor>)
```

The reference must come from a programmed flash. An erased block, all `0xff`, gives the CRC32
`0xfea8a821` and the BIOS refuses to calibrate:

```console
First SPI Flash block erased, unable to perform freq test.
```

The divisor then stays at its reset value. The calibration adds no margin: it keeps the lowest
divisor that read the block once without error. Define `SPIFLASH_SKIP_FREQ_INIT` with
`soc.add_constant("SPIFLASH_SKIP_FREQ_INIT")` to keep the divisor of the build, for example when
the first block changes at run time.

## Boot logs from boards {#sw-hw-logs}

Two public boot logs from LiteX-Boards commits show this initialization on hardware, with the BIOS
of their time (2021) and its memspeed results: the Efinix Trion T20 MIPI development kit, with a
W25Q32JV read in 1-1-1 on x1 pads (litex-boards commit `b6c5a85b`), and the Tang Nano 4K, with a
W25Q32 read in 1-1-1 (litex-boards commit `376a8365`). [Recorded results](#perf-recorded) quotes
both logs and explains them.

## Reading the flash from the console {#sw-console}

The flash region is ordinary memory for the BIOS: `mem_list` shows it, and `mem_read` and `crc`
read it through the MMAP. The session below was captured on `litex_sim --with-spi-flash`, with a
4 KiB image whose first page holds a line of text followed by the bytes `0x00` to `0xff`:

```sh
litex_sim --with-spi-flash --spi_flash-init flash_init.bin
```

```console
litex> mem_list
Available memory regions:
Region   Origin     End        Size 
ROM      0x00000000 0x0001ffff 0x20000 
SRAM     0x10000000 0x10001fff 0x2000 
SPIFLASH 0x01000000 0x01ffffff 0x1000000 
CSR      0xf0000000 0xf000ffff 0x10000 
litex> mem_read 0x01000000 64
Memory dump:
0x01000000  4c 69 74 65 53 50 49 20 66 6c 61 73 68 20 6d 6f  LiteSPI flash mo
0x01000010  64 65 6c 3a 20 66 69 72 73 74 20 70 61 67 65 20  del: first page 
0x01000020  6f 66 20 74 68 65 20 69 6e 69 74 20 66 69 6c 65  of the init file
0x01000030  2e 0a 00 01 02 03 04 05 06 07 08 09 0a 0b 0c 0d  ................
litex> crc 0x01000000 256
CRC32: 3ebcafae
```

The bytes appear in the order of the file: the MMAP swaps the bytes of each word for the
little-endian CPU ([Byte order](#mmap-endianness)). The CRC32 of the first 256 bytes, computed on
the host with Python `binascii.crc32`, is also `0x3ebcafae`. This is the block the calibration
uses, and the same check verifies a flash written from the host.

## Erasing and writing from the BIOS {#sw-commands}

Three BIOS commands change the flash. They exist only when the SoC has the master, and `help` lists
them in their own group; the lines below are from the same simulated SoC:

```console
flash_erase_range        - Erase flash range
flash_from_sdcard        - Write file from SD card to flash
flash_write              - Write to flash
```

| Command | Arguments | Action |
|------------------------------|---------------------------------|----------------------------------------|
| `flash_erase_range` | `<offset>` `<count>` | Erases every erase block that overlaps the range |
| `flash_write` | `<offset>` `<mem_addr>` `[count]` | Programs `count` bytes (default 1) from memory |
| `flash_from_sdcard` | `<filename>` | Programs a file of the SD card FAT partition at offset 0; erase the range first |

The offsets are byte offsets in the flash, not CPU addresses. A session that updates 64 KiB at
offset 1 MiB from data already in main RAM at `0x40000000` reads as follows:

```console
litex> flash_erase_range 0x100000 0x10000
litex> flash_write 0x100000 0x40000000 0x10000
litex> crc 0x01100000 0x10000
```

The last address assumes the flash region at `0x01000000`; check it with `mem_list`. Compare the
CRC with the one of the source data, from `crc 0x40000000 0x10000` or the host.

`flash_erase_range` sends one erase command per block, with the opcode, size and address width
of the module: the first erase command of the module, `0xdc` with a 4-byte address on the modules
above 16 MiB that list it ([The SPI memory database](#modules)), 64 KiB `0xd8` with a 24-bit
address on the others, or the `erase_cmd` given to the module. It prints `Erase SPI Flash @<address>`, polls WIP, then reads the block back
through the MMAP and reports every byte that is not `0xff`.

`flash_write` programs pages of up to 256 bytes with Page Program, `0x12` with a 4-byte address on
a module above 16 MiB that lists `PP_1_1_1_4B`, `0x02` with a 3-byte address otherwise. It polls
WIP, then reads each page back and compares it. On a mismatch it prints `Error: verify
failed at <address>`, and finally a reminder that the region may not be erased. It does not erase
by itself: program only erased blocks.

Start `flash_write` at a multiple of 256 bytes. It programs 256-byte chunks from the offset and
does not split them at page boundaries: from an unaligned offset, each chunk crosses a page and
wraps inside it ([Erase and program](#flash-erase)), and the verify reports errors.
`flash_from_sdcard` starts at offset 0 and is not affected.

With 3-byte commands, the BIOS assumes the chip in its default 3-byte address mode and refuses a
program or erase above 16 MiB, with an error message. The 4-byte erase of the module list and the
4-byte Page Program reach the whole chip, in either address mode. On a module without them,
program and erase the upper part through the master with 4-byte opcodes, or build the module with
`erase_cmd=Codes.SE_4B`. Reads through a `_4B` opcode cover the whole chip.

## Booting from an image in the flash {#sw-flashboot}

The BIOS can boot an application stored in the flash. The boot method exists when the constant
`FLASH_BOOT_ADDRESS` is defined: a CPU address inside the flash region. No LiteX or LiteX-Boards
code defines it, so a target adds it itself:

```python
self.add_constant("FLASH_BOOT_ADDRESS", self.bus.regions["spiflash"].origin + 0x100000)
```

The image starts with a header of two 32-bit words, its length and the CRC32 of the payload, as
the figure below shows.

![A flash boot image. The BIOS reads the length and the CRC32 at the start of the image, checks
the payload, then copies it or jumps into it.](sw_image.svg)

`crcfbigen.py` of LiteX builds the image from a binary with `-f`. It writes the header big-endian
by default, while the BIOS reads it as native words: use `-l` for a little-endian CPU such as
VexRiscv, as the LiteX demo application does.

```sh
python3 -m litex.soc.software.crcfbigen firmware.bin -o firmware.fbi --fbi --little
```

At boot, or with the `flashboot` command, the BIOS checks the length (at least 32 bytes, at most
the main RAM size or 16 MiB) and that the image fits the flash region. It then checks the CRC over
the flash. With a main RAM, it copies the payload there and jumps to it; without one, it executes
the payload in place, 8 bytes after `FLASH_BOOT_ADDRESS`.

The flash boot has priority 10: the BIOS tries it after the serial boot (0) and before the ROM
(20) and SD card (30) boots. `FLASH_BOOT_PRIORITY` and `FLASH_BOOT_DISABLE` change this, as for
the other boot methods.

## Flash layout {#sw-layout}

One flash usually holds several images: the bitstream the FPGA configures from at offset 0, the
BIOS for targets that run it in place, and an application. The figure below shows the usual
order; each offset is a choice of the target.

![A flash layout. The bitstream starts at 0 because the FPGA reads it from there; the BIOS of a
XIP target follows at `bios_flash_offset`; a boot image sits at the offset of
`FLASH_BOOT_ADDRESS`.](sw_layout.svg)

Gowin GW1N devices configure from their internal flash: on their targets the external flash holds
no bitstream and the BIOS starts at offset 0.

The size of an uncompressed bitstream depends on the FPGA, not on the design, so the next offset
must leave room for the largest bitstream of the device. Erase blocks are 64 KiB with the modules of the
database: align every image on 64 KiB, or an update of one image erases the start of the next.

A board can also keep a fallback image that is never rewritten, such as a DFU loader in the
upper half of the flash.

## Writing the flash from the host {#sw-host}

Most targets write their bitstream into the flash with `--flash`, through the programmer of the
platform (JTAG, a vendor tool or a USB loader). The LiteX wiki page *Load and Flash* lists the
programmers. Targets that run the BIOS in place, such as the iCEBreaker, write the BIOS at
`bios_flash_offset` in the same step ([Running the BIOS from the flash](#integ-xip)).

From a running SoC, the BIOS commands above update the flash without a programmer: load the data
into RAM or onto the SD card, erase, write, and compare CRCs. Keep a way back, such as a JTAG
cable or a fallback image, before rewriting the bitstream area: an interrupted write leaves an
FPGA that no longer configures.

## Beyond the BIOS {#sw-firmware}

An application can call `liblitespi` itself: `spiflash_erase_range()`,
`spiflash_write_stream()` and `spiflash_erase_4k_sector()` (`0x20`, 4 KiB, 24-bit address) are
declared in `liblitespi/spiflash.h`. `spiflash_write_stream()` returns the number of bytes written
and verified, or -1 after a verify error. Reads need no function: the flash is memory at
`SPIFLASH_BASE`.

These functions use the master, one byte per register access, so writing is slow compared with
reading. Under Linux, the linux-on-litex-vexriscv project documents the flash as an MTD device,
`/dev/mtd0`, read and erased with the usual MTD tools.

## Where to go next {#sw-next}

[Integration in a LiteX SoC](#integration) for the constants the BIOS reads; [The register
master](#master) for the transfers behind each command; [Inside a SPI NOR flash](#flash-primer)
for erase, program and status registers; [Debugging](#debugging) when an init line reports an
error.
