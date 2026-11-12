# Debugging {#debugging}

This chapter helps when the flash does not answer, answers wrong data, or the BIOS refuses to
calibrate or to write. It gives a method, the messages of the BIOS, a table of symptoms with their
causes, the register sequences to talk to the flash from a host, the signals worth probing with
LiteScope, and the known issues of this revision.

## Method {#debug-method}

Most flash problems are a pin, a clock path or a configuration mismatch between the module and
the chip. They show up at the first command, so the BIOS boot log is the first trace to read, and
the registers come before a logic analyzer.

1. Check the build: the module, the read opcode and the pads in the target, the
   `SPIFLASH_*` constants and the `spiflash_` registers of the `csr.csv`.
2. Read the BIOS initialization lines ([BIOS, boot and flash update](#software)). Rebuild with
   `software_debug=True` in `add_spi_flash` for more detail.
3. Talk to the flash from the host through the master registers: identifier, status register,
   then a read through the memory window.
4. Change one parameter at a time at run time: the divisor, the dummy bits, the SPI mode.
5. Only then probe the PHY with LiteScope, with a trigger on CS.

The same configuration can often be reproduced without a board: the pin-level bench of
[Simulation and tests](#simulation) runs the real PHY against a flash model.

## Messages of the BIOS {#debug-bios}

`software_debug=True` defines `SPIFLASH_DEBUG` in the BIOS: it then prints the four bytes of
each identifier and register read, the dummy bits written to the MMAP, and the CRC of each step
of the frequency calibration. The table lists the messages that point to a problem.

| Message | Meaning |
|------------------------------------------------|----------------------------------------------------|
| First SPI Flash block erased, unable to perform freq test. | The first 256 bytes read as erased; the divisor stays at its build value |
| Unable to read SPI Flash status register. | RDSR returned `0xff` before the quad enable (method `wrsr_sr1_bit6`) |
| Unable to read SPI Flash status/configuration registers. | RDSR or the configuration register read returned `0xff` (method `wrr_cr1_bit1`) |
| SPI Flash quad enable timeout. | WIP stays set after the status register write |
| SPI Flash quad enable failed. | The QE bit reads back as 0 after the write |
| Error: verify failed at [...] | A programmed byte differs on read-back through the MMAP |
| Error: location [...] not erased | A byte is not `0xff` after an erase |
| Error: flash write failed (is the region erased? see flash_erase_range) | `flash_write` or `flash_from_sdcard` saw verify errors |

A module without a `quad_enable` method gets no read-back check: the BIOS writes a fixed
sequence, waits for the ready status, and prints nothing more than `Enabling Quad mode...`.

## Symptoms {#debug-symptoms}

| Symptom | Likely causes | What to check |
|---------------------------|-------------------------------------|-------------------------------------------|
| Identifier or status reads `0xff` or `0x00` | Wrong pins, CS not toggling, no SCK on the clock path, HOLD# low | Pins of the target; CCLK targets use STARTUPE2 and ECP5 MCLK targets USRMCLK; WP# and HOLD# pulled up on the board |
| Calibration message about an erased block | Nothing programmed at offset 0 | Program the bitstream or data first, or build with `SPIFLASH_SKIP_FREQ_INIT` |
| x1 reads correct, quad reads wrong | QE bit not set, wrong dummy cycles, pads not x4 | Status register through the master; `dummy_cycles` of the module against the datasheet; `mode="4x"` and `spiflash4x` pads |
| Correct at a high divisor only | Sampling delay of the board, SCK above the chip limit for the opcode | Raise `mmap_clk_divisor` and `phy_clk_divisor` from the host; `extra_latency` of the PHY; the fast read opcode |
| CPU hangs when running from flash | Dummy bits wrong for the read opcode, the master holding CS | `mmap_dummy_bits`; `master_cs` back to 0; the known issues below |
| Erase or program verify errors | Block protection bits set, region not erased, address above 16 MiB | Status register bits; `flash_erase_range` first; the known issues below |

A flash pauses its output while HOLD# is low, so a floating HOLD# gives reads of a constant value.
The PHY holds WP# and HOLD# high in x1 mode, and DQ2 and DQ3 of x4 pads when the module commands
use at most two lines. With a quad read, DQ2 and DQ3 are data lines that the PHY drives or reads
([SPI memories in a nutshell](#spi-primer)); a board without pull-ups can then see HOLD# low
before the BIOS sets the QE bit.

The 1-1-4 and 1-4-4 modes depend on the QE bit, whose place differs between vendors
([Inside a SPI NOR flash](#flash-primer)). Read the status and configuration registers from the
host to see whether the BIOS sequence set it.

## Talking to the flash from the host {#debug-host}

The master registers let a host run any command through a bridge (UARTBone, JTAGBone or
Etherbone) with `litex_server` and `litex_cli` ([The register master](#master)). Start with the
identifier and the state of the SPI registers:

```sh
# Identifier of the SoC, then the SPI flash registers
litex_cli --ident
litex_cli --regs --filter spiflash
```

`--regs` reads every matching register, `master_rxtx` included: run it only between commands,
since that read pops a word of the RX FIFO.

A command is a sequence of transfers while `master_cs` is 1. `master_phyconfig` gives the length
in bits (bits 5:0), the width (bits 11:8) and the output enable mask (bits 23:16); `0x00010108` is
one byte on one line, sent on DQ0. Each write of `master_rxtx` sends one transfer, and each read
returns what the flash shifted out during it. The sequence below reads the JEDEC identifier
(RDID, `0x9f`): the three reads after the opcode return the manufacturer, the memory type and the
capacity.

```sh
litex_cli --write spiflash_master_phyconfig 0x00010108
litex_cli --write spiflash_master_cs 1
# Opcode, then three dummy bytes; read the RX word after each write
litex_cli --write spiflash_master_rxtx 0x9f
litex_cli --read  spiflash_master_rxtx
litex_cli --write spiflash_master_rxtx 0x00
litex_cli --read  spiflash_master_rxtx
litex_cli --write spiflash_master_rxtx 0x00
litex_cli --read  spiflash_master_rxtx
litex_cli --write spiflash_master_rxtx 0x00
litex_cli --read  spiflash_master_rxtx
litex_cli --write spiflash_master_cs 0
```

The same sequence with RDSR (`0x05`) and one data byte reads the status register: bit 0 is WIP,
bit 1 is WEL, and the block protection bits sit above them. Read the memory window through the
bus with `litex_cli --read` at the base of the `spiflash` region and compare with the image that
was programmed.

The settings of the PHY and of the MMAP can be changed in the same way while the SoC runs. Each
transfer carries the divisor of its frontend (`mmap_clk_divisor`, `master_clk_divisor`), and the
SDR PHY uses its own `phy_clk_divisor` only when that divisor is 0. The BIOS calibration writes
both `phy_clk_divisor` and `mmap_clk_divisor`, so to lower SCK for the MMAP after boot, raise
`mmap_clk_divisor` (or set it to 0 and raise `phy_clk_divisor`). `mmap_dummy_bits` changes the
dummy phase of the next MMAP command. [Register reference](#registers) lists them.

> While `master_cs` is 1, the crossbar gives the PHY to the master and the MMAP waits. A CPU that
> runs from the flash stalls until `master_cs` returns to 0: keep host sequences short on such
> SoCs, and never leave `master_cs` at 1.

## Probing the PHY with LiteScope {#debug-litescope}

When the registers do not explain the problem, a LiteScope capture of the PHY shows each transfer
against SCK. The analyzer runs in the system clock domain, so it sees the clock generator at its
own rate: with the SDR PHY, `posedge` and `negedge` mark the SCK edges, and the transfers are the
`sink` and `source` streams of the PHY. These flags lead the pin: they are high in the cycle
before the internal SCK register toggles, and that register reaches the pin through one more
output register (the SDR output, or the register in front of STARTUPE2 or USRMCLK). The signals
below cover the MMAP and the SDR PHY of a SoC built with `add_spi_flash`.

```python
from litescope import LiteScopeAnalyzer

phy  = self.spiflash.phy.spiflash_phy # LiteSPISDRPHYCore.
mmap = self.spiflash.mmap
analyzer_signals = [
    # MMAP: bus access and state.
    mmap.bus.stb, mmap.bus.ack, mmap.bus.adr, mmap.fsm,
    # PHY: transfers, chip select, SCK edges and state.
    phy.sink.valid, phy.sink.ready, phy.sink.len, phy.sink.width, phy.sink.mask,
    phy.source.valid, phy.source.data,
    phy.cs, phy.cs_control.enable,
    phy.clkgen.en, phy.clkgen.posedge, phy.clkgen.negedge, phy.fsm,
]
self.analyzer = LiteScopeAnalyzer(analyzer_signals, depth=1024, csr_csv="analyzer.csv")
```

Trigger on the rising edge of `phy.cs_control.enable`, the start of a command. A command then
reads as a sequence of transfers: the opcode, the address, the dummy bits with a 0 mask, and the
data with a 0 mask. Compare the `len`, `width` and `mask` of each transfer with the phases of the
opcode ([Architecture](#architecture)), and the data words with the image.

## Known issues {#debug-known}

These behaviours of the code on this revision explain some symptoms. The status of each feature
is in [the introduction](#intro-status).

| Issue | Effect | Workaround |
|--------------------------------|--------------------------------------------|----------------------------------------|
| `extra_latency` of 0.5 | 1:2 PHY: `TypeError` at elaboration, so the Efinix Ti375 and Tz170 targets fail at their default rate, 1:2; SDR PHY: `int()` drops the 0.5 | Rate 1:1, or an integer value |
| Divisor 1023 | The half period, 512, wraps to 0 in its 9-bit counter: SCK runs at system clock / 2 | Use divisors up to 1022 |
| CS with `clock_domain` | CS reaches the PHY domain without a synchronizer, and the MMAP releases it for one `sys` cycle between two commands: a slower PHY clock can miss that release | Keep the PHY clock at least as fast as `sys`; test in simulation first |
| `S25FL128L`, `MX25L12833F` 1-4-4 | The modules give 8 cycles, which depend on a latency setting of the chip ([Dummy cycles](#mod-dummy)) | Check the setting, then `mmap_dummy_bits` |
| BIOS dummy bits constant | `add_spi_flash` never defines this constant ([BIOS constants](#opt-bios)), so the BIOS keeps the reset value of `mmap_dummy_bits` | Change the module default, or add the constant in the target |
| MMAP writes (in development) | The MMAP sends the program opcode without WREN and without status polling; a page boundary starts a new program command without WREN, ignored by a flash | Send WREN with the master before each page |
| MMAP writes, `endianness="big"` | Bytes are programmed in the reverse order of a read: a word reads back byte-reversed | Little endian MMAP (`mmap_endianness`), or swap in software |
| Master `rxtx` write | A write while the TX FIFO is full (`status.tx_ready` at 0) is dropped | Poll `tx_ready` before each write |
| Modules above 16 MiB without `erase_commands` | The erase falls back to SE `0xd8`, 64 KiB, 24-bit address; the BIOS refuses an erase above 16 MiB ([Erase commands](#mod-erase)) | Select the `SE_4B` erase with the `erase_cmd` argument of the module |
| BIOS `flash_write` at an unaligned offset | Each 256-byte page program starts at the offset and wraps inside its page: verify errors | Write from a 256-byte aligned offset |
| Generic quad enable | Modules without `quad_enable`: WREN, then `01 43 07`, with no read-back; it also clears the block protection bits of SR1 | Check the status registers from the host |
| QPI entry | The BIOS sends `0x35` only; the master stays on one line afterwards | Check the QPI entry opcode of the chip |
| `phy_mode` | Only bit 1 (SCK idle level) is used: modes 1 and 2 behave as modes 0 and 3 with the other idle level | Write 0 or 3 |

## Where to go next {#debug-next}

[Register reference](#registers) gives every register used here; [Simulation and
tests](#simulation) reproduces a configuration with the real PHY and a flash model.
