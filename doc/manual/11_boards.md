# Supported FPGAs and boards {#boards}

This chapter lists the FPGA families that LiteSPI runs on, the LiteX-Boards targets that use it,
and what a board of your own needs to get its flash working. Read it before choosing a PHY for a
board, or when you add the flash to a new target. The status of each PHY and mode is in the
[status table](#intro-status); this chapter records usage, not validation.

## At a glance {#boards-glance}

LiteSPI has one generic PHY for every family, plus clock backends for the configuration flash of
some FPGAs ([PHYs](#phys)). The table below counts the LiteX-Boards targets that call
`add_spi_flash`, per family, and gives the PHY path they take.

| FPGA family | Targets | PHY path | Pads (x1 / x4) | Reads used |
|----------------------|-------------|-------------------------------------|----------------|-----------------------------|
| Xilinx 7-Series | 28 | SDR; STARTUPE2 for 25; 1:2 on Arty | 2 / 26 | 1-1-1, 1-1-4, 1-1-4 4-byte |
| Xilinx UltraScale+ | 2 | SDR, STARTUPE3 (full I/O) | 1 / 1 | 1-1-1 fast 4-byte, 1-1-4 4-byte |
| Lattice iCE40 | 12 | SDR, flash clock on a pin | 9 / 3 | 1-1-1, 1-1-4 |
| Lattice ECP5 | 9 | SDR, USRMCLK for all 9 | 3 / 6 | 1-1-1, 1-1-4 |
| Lattice Nexus | 3 | SDR | 0 / 3 | 1-1-4, 4-4-4 (QPI) |
| Gowin GW1N, GW2A, GW5A | 9 | SDR | 7 / 2 | 1-1-1, 1-1-4 |
| Efinix Trion, Titanium, Topaz | 9 | SDR; 1:2 by default on Ti375, Tz170 | 6 / 3 | 1-1-1, 1-1-4, 1-1-4 4-byte |
| Cologne Chip GateMate | 2 | SDR | 0 / 2 | 1-1-1, 1-1-4 |
| Altera MAX 10 | 1 | SDR | 1 / 0 | 1-1-1 |

The counts come from LiteX-Boards (75 targets, 76 files, one of which has the call commented out).
"STARTUPE2" and "USRMCLK" mark targets whose platform declares the flash pads without `clk`: the
PHY then routes SCK through the configuration clock pin. No target uses the dual (1-1-2, 1-2-2),
1-4-4 or octal reads.

The most used modules are the `W25Q128JV` (8 targets), the `W25Q32` (6), and the `MT25QL128` and
`IS25LP128` (5 each). A few targets pick the module from the board or its revision, such as the
Colorlight targets; the Fomu target takes it as an argument of its SoC class (`AT25SF161` by
default).

## Representative boards {#boards-representative}

The boards below cover every PHY path and every read used in LiteX-Boards. Each one has a target,
listed in the second table; build it with `--with-spi-flash` when the flash is optional.

| Board | FPGA | Module, read | PHY path |
|-----------------------|----------------------|-----------------------------------|------------------------|
| Arty A7 | Artix-7 | `S25FL128L`, 1-1-4 | 1:2, flash clock pin |
| KC705 | Kintex-7 | `N25Q128A13`, 1-1-4 | SDR, STARTUPE2 |
| XCKU3P board | Kintex UltraScale+ | `MT25QU256`, 1-1-1 fast 4-byte | STARTUPE3 |
| ULX3S | ECP5 | `IS25LP128`, 1-1-4 | SDR, USRMCLK |
| Acorn Baseboard | ECP5 | `W25Q128JV`, 1-1-4 | SDR, USRMCLK |
| iCEBreaker | iCE40 UP5K | `W25Q128JV`, 1-1-4, BIOS XIP | SDR, no master |
| Tang Nano 9K | Gowin GW1NR-9 | `W25Q32`, 1-1-1, BIOS XIP | SDR, no master |
| CrossLink-NX EVN | LIFCL-40 | `MX25L12833F`, 4-4-4 | SDR, 100 kHz at reset |
| TEL0025 | Certus-NX | `MT25QL256A`, 1-1-4 | SDR, no master |
| T120 F576 kit | Efinix Trion T120 | `W25Q128JV`, 1-1-4 | SDR |
| Ti375 C529 kit | Efinix Titanium | `IS25WP512M`, 1-1-4 4-byte | 1:2 or SDR |

The target scripts of these boards are:

| Board | Target script |
|-----------------------|------------------------------------------|
| Arty A7 | `digilent_arty` |
| KC705 | `xilinx_kc705` |
| XCKU3P board | `alibaba_xcku3p` |
| ULX3S | `radiona_ulx3s` |
| Acorn Baseboard | `litex_acorn_baseboard` |
| iCEBreaker | `icebreaker` |
| Tang Nano 9K | `sipeed_tang_nano_9k` |
| CrossLink-NX EVN | `lattice_crosslink_nx_evn` |
| TEL0025 | `trenz_tel0025` |
| T120 F576 kit | `efinix_t120_f576_dev_kit` |
| Ti375 C529 kit | `efinix_ti375_c529_dev_kit` |

A few of these deserve a note:

- **Arty A7.** The only 7-Series target with the 1:2 PHY. Its pads keep a regular `clk` pin, which
  the 1:2 PHY needs.
- **CrossLink-NX EVN and Certus-NX Versa.** Both request the QPI read at `clk_freq=100_000`,
  100 kHz. This is the reset divisor: both keep the master, so the BIOS calibration lowers it on a
  programmed flash. The BIOS sends the QPI entry command at boot ([BIOS
  initialization](#sw-init)).
- **Ti375 C529 and Tz170 J484 kits.** The targets default to `--spi-flash-rate 1:2` with
  `extra_latency=0.5`. The 1:2 PHY delays its input sampling by one PHY clock cycle for each 0.5
  of `extra_latency`. The SDR PHY (`--spi-flash-rate 1:1`) truncates `extra_latency` to an
  integer, so 0.5 has no effect there.
- **TEL0025 and iCEBreaker.** Both read in 1-1-4 without the master, so the BIOS cannot set the QE
  bit: it must already be set in the chip.

The photo below shows the TEL0025, a small Certus-NX module whose target maps its 32 MiB flash
through LiteSPI. Its 1-1-4 read uses 3-byte addresses, so only the first 16 MiB read correctly;
the upper half of the region aliases the lower one.

![The TEL0025 module (Lattice Certus-NX). Its QSPI flash is read in 1-1-4 by LiteSPI with the
`trenz_tel0025` target.](boards_tel0025.jpg)

## Boards that run the BIOS from the flash {#boards-xip}

Nineteen targets have no BIOS ROM in block RAM: the CPU executes the BIOS in place from the flash
([Running the BIOS from the flash](#integ-xip)). All of them are small FPGAs:

| Family | Targets |
|-----------------|------------------------------------------------------------------------------------|
| Lattice iCE40 | `icebreaker`, `icebreaker_bitsy`, `kosagi_fomu`, `lattice_ice40up5k_evn`, `muselab_icesugar`, `ice_v_wireless`, `signaloid_c0_microsd`, `alchitry_cu`, `fpgawars_alhambra2`, `machdyne_krote`, `qwertyembedded_beaglewire`, `tinyfpga_bx` |
| Gowin GW1N | `sipeed_tang_nano_4k`, `sipeed_tang_nano_9k`, `trenz_tec0117`, `brisbaneSilicon_brs_100_gw1nr9` |
| Efinix Trion | `efinix_t8_f81_dev_kit`, `efinix_xyloni_dev_kit`, `jungle_electronics_fireant` |

The Tang Nano 4K does it with its default CPU (not with the Gowin EMCU), and the Tang Nano 9K
unless built with `--with-integrated-rom`. On the Gowin GW1N targets the BIOS sits at offset 0 of
the external flash, since the FPGA configures from its internal flash. Elsewhere, the `--flash`
option, where the target has one, writes the bitstream and the BIOS together. The
iCEBreaker commit that introduced LiteSPI on this board states that "both XiP from SPI(1X) or
QSPI(4X) are working" (litex-boards commit `0f648ac4`); [Performance and resources](#performance)
gives the resource figures it recorded.

## Hardware records {#boards-records}

A few commits of the repositories record hardware results. They are listed here as records, with
their source; the [status table](#intro-status) gives the maintainers' status.

| Board | Record | Source |
|------------------------|----------------------------------------------------------------|----------------------------|
| Efinix T20 MIPI kit | BIOS init (x1, 1-1-1) and memspeed | litex-boards `b6c5a85b` |
| Tang Nano 4K | BIOS init at 13 MHz and memspeed | litex-boards `376a8365` |
| AX7035B (Artix-7) | STARTUPE2 deadlock on cold boots, fixed in LiteSPI `6dbbc66` | `alinx_ax7035` target comment |
| MYC-J7A100T | 32 MiB read in 1-1-4 4-byte, CRC of the flashed bitstream | litex-boards `c25f60b8` |
| Ti375 C529 kit | `IS25WP512M` opcodes and dummy cycles fixed for this board | LiteSPI `edda46b` |

The two BIOS logs are reproduced in [Recorded results](#perf-recorded). The ULX3S commit of the
USRMCLK backend (LiteSPI `8c75b24`) records a successful build at 50 MHz, not a hardware run.

## Adding the flash to a new board {#boards-new}

A board needs four things: the pads in its platform, a module, a mode, and the call in its
target. Check them in this order.

1. **Pads.** Declare `spiflash4x` (`cs_n`, `clk`, `dq` of 4 lines) when the four data lines reach
   the FPGA, else `spiflash` (`cs_n`, `clk`, `mosi`, `miso`). For the configuration flash of a
   7-Series or ECP5 device, leave `clk` out: the PHY uses STARTUPE2 or USRMCLK
   ([Pads](#integ-pads)).
2. **Module.** Find the chip in the database by its part number (`litespi/modules/modules.py`).
   If it is missing, add it from the datasheet ([The SPI memory database](#modules)).
3. **Mode.** Start with `READ_1_1_1` and the SDR PHY at the default 20 MHz. Move to `READ_1_1_4`
   once the 1-1-1 read works, with the master kept so that the BIOS sets the QE bit. Check that
   the module names a `quad_enable` method ([BIOS initialization](#sw-init)); without one, the BIOS
   writes fixed status register values, so set the QE bit with a programmer first.
4. **Target.** Call `add_spi_flash` behind a `--with-spi-flash` option, as the targets above do.

Then check the result in steps, from build to hardware:

```sh
# Elaborate without vendor tools: catches parameter and pad errors
python3 -m litex_boards.targets.<target> --with-spi-flash --build --no-compile
# Build and load the bitstream in the FPGA (volatile)
python3 -m litex_boards.targets.<target> --with-spi-flash --build --load
```

At boot, look for the `Initializing <module> SPI Flash` line and for the clock line
([BIOS initialization](#sw-init)). Then compare `crc` of the start of the flash with the CRC of
the file written there, as in [Reading the flash from the console](#sw-console). A flash that
does not answer (all `0xff` or `0x00`), a refused calibration or a wrong CRC are covered in
[Debugging](#debugging).

## Where to go next {#boards-next}

[Integration in a LiteX SoC](#integration) for the parameters of each target; [PHYs](#phys) for
the clock backends; [Debugging](#debugging) when a new board does not read its flash.
