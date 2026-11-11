# SPI memories in a nutshell {#spi-primer}

This chapter explains how a controller talks to a SPI memory, for an FPGA engineer who has never
read a flash datasheet. It starts from the bus and its clock, adds data lines, then builds a read
command phase by phase. The next chapter, [Inside a SPI NOR flash](#flash-primer), covers what
happens inside the chip: erase, program, status registers and addressing.

Each section gives the idea, then the mechanism, and ends with the part of LiteSPI that implements
it. There is no single standard for SPI memories: the commands below are the ones most flashes
share, and the datasheet of each chip is the reference for its details.

## The SPI bus {#primer-bus}

SPI is a synchronous serial bus between one controller and one or more devices. The controller
drives a clock, SCK, and selects one device at a time with its chip select, CS. CS is active low:
the device listens while CS is low and ignores the bus while CS is high. Each device has its own
CS, and the other lines are shared.

In its original form, SPI has two data lines. The controller sends on MOSI and the device answers
on MISO, one bit per SCK cycle, most significant bit first. SPI memories call these lines DQ0 and
DQ1, because wider modes use them both ways, as the figure below shows.

![The SPI memory bus. The controller drives CS and SCK; the data lines DQ0 to DQ3 go both ways in
wide modes. In single-line SPI, DQ0 is MOSI and DQ1 is MISO, and DQ2 and DQ3 are the write protect
(WP#) and hold (HOLD#) inputs of the chip. Octal memories add DQ4 to DQ7.](primer_bus.svg)

A transaction with a memory is a *command*: CS goes low, the controller sends an opcode and its
arguments, data moves, and CS goes high. A command ends when CS rises: a read stops there, and a
program, erase or register write starts only then. CS must stay low for the whole command and go
high between two commands.

In LiteSPI, the PHY drives CS, SCK and the data lines. The LiteX platform files of LiteX-Boards
describe the pins as a `spiflash` pad set with `cs_n`, `clk`, `mosi` and `miso` for single-line
use, and as a `spiflash4x` pad set with `cs_n`, `clk` and a 4-bit `dq` for quad use
([PHYs](#phys)).

## Clock polarity and phase {#primer-modes}

SPI defines four *SPI modes*, from two settings. The clock polarity (CPOL) gives the level of SCK
when idle; the clock phase (CPHA) gives the edge that samples the data. SPI memories support SPI
mode 0 (SCK idles low) and SPI mode 3 (SCK idles high). In both, the data changes on the falling
edge of SCK and is sampled on the rising edge, as the figure below shows.

![SPI modes 0 and 3. Only the idle level of SCK differs; the rising edges, where both sides sample
the data, fall at the same instants, and the data changes on the falling edges.](primer_modes.svg)

The memory samples the controller's bits on the rising edge, and drives its own bits after the
falling edge. The controller samples them on the next rising edge. Half an SCK period is thus left
for the output delay of the memory, the board traces and the input delay of the FPGA: this sets the
highest usable SCK frequency of a board.

In LiteSPI, the SDR PHY supports SPI mode 0 and SPI mode 3, chosen by its `mode` register. It
changes its outputs on the falling edge of SCK and samples its inputs on the rising edge, delayed
by its I/O registers ([PHYs](#phys)). The 1:2 PHY has no `mode` register and always uses SPI mode
0.

## More data lines {#primer-lines}

A single data line moves one bit per SCK cycle. To read faster without raising SCK, memories use
the data lines in parallel: two lines (dual), four lines (quad) or eight lines (octal). In quad
mode the chip gives up its write protect and hold inputs, which become DQ2 and DQ3. Most flashes
need a configuration bit, the QE bit, before they accept this ([Status registers and quad
enable](#flash-qe)).

When the data lines go both ways, the controller and the memory take turns on the same wires. Both
must never drive a line at the same time: the controller releases the lines before the memory
starts to answer.

In LiteSPI, a PHY handles 1, 2, 4 or 8 data lines. With the x1 pad set, the SDR PHY uses the
separate `mosi` and `miso` pins; with the x4 pad set, single-line transfers drive DQ0 and read DQ1.
In both cases it does not drive WP# and HOLD# during single-line transfers, so the board must keep
them inactive with pull-ups. With more lines, it drives the `dq` pins through tristate buffers and
sets the output enable of each line for each part of a command.

## The x-y-z notation {#primer-notation}

A read command has three parts that can use different widths: the opcode, the address and the
data. Datasheets and LiteSPI write a mode as three numbers, the lines used by each part: *1-1-4*
sends the opcode and the address on one line and receives the data on four. The table below lists
the read commands of the opcode table of LiteSPI (`litespi/opcodes.py`), with their usual opcode.
Not every chip supports every mode, and no module of the database lists 1-8-8.

| Mode | Opcode | Name in the database | Command | Address | Data |
|-------------|----------|----------------------------|----------|----------|----------|
| 1-1-1 | `0x03` | `READ_1_1_1` | 1 line | 1 line | 1 line |
| 1-1-1, fast | `0x0b` | `READ_1_1_1_FAST` | 1 line | 1 line | 1 line |
| 1-1-2 | `0x3b` | `READ_1_1_2` | 1 line | 1 line | 2 lines |
| 1-2-2 | `0xbb` | `READ_1_2_2` | 1 line | 2 lines | 2 lines |
| 1-1-4 | `0x6b` | `READ_1_1_4` | 1 line | 1 line | 4 lines |
| 1-4-4 | `0xeb` | `READ_1_4_4` | 1 line | 4 lines | 4 lines |
| 4-4-4 | `0xeb` | `READ_4_4_4` | 4 lines | 4 lines | 4 lines |
| 1-1-8 | `0x8b` | `READ_1_1_8` | 1 line | 1 line | 8 lines |
| 1-8-8 | `0xcb` | `READ_1_8_8` | 1 line | 8 lines | 8 lines |

The 4-4-4 mode is called QPI: even the opcode uses four lines. A flash enters QPI mode on a command
and stays there until told otherwise, so every later command must also use four lines. Octal
memories have the same 8-8-8 mode, called OPI.

In LiteSPI, the name of the read opcode chosen for a module sets the width of each phase: the
module class reads `READ_1_1_4` as a 1-line opcode, a 1-line address and 4-line data
([The SPI memory database](#modules)).

## A read command, phase by phase {#primer-command}

A read command is made of up to four *phases*: the opcode, the address, the dummy cycles and the
data. The figure below shows a fast read (`0x0b`) in 1-1-1 mode.

![A fast read (`0x0b`) in 1-1-1 mode. With CS low, the controller sends the opcode and a 3-byte
address on DQ0; after 8 dummy cycles the flash sends the data on DQ1, one byte every 8 SCK cycles,
for as long as CS stays low.](primer_phases.svg)

The opcode is one byte, most significant bit first. The address follows, usually three bytes,
also most significant byte first. The flash needs some time to fetch the data at that address,
so a fast read leaves a number of *dummy cycles*, SCK cycles where no one drives the data lines.
In wide modes, these cycles also give the controller time to release the lines.

Then the data comes out, one byte after the other, from consecutive addresses. The flash keeps
sending as long as SCK runs and CS stays low, so a single command can read the whole chip. A new
address costs a new command: CS high, opcode, address and dummy cycles again.

The number of dummy cycles depends on the chip, the read mode and sometimes the SCK frequency.
The datasheet gives it, and each module of the database stores it. The `W25Q128JV` module, for
example, gives 8 dummy cycles for its 1-1-1 fast read and its 1-1-2 and 1-1-4 reads.

In LiteSPI, each phase is one *transfer* from the core to the PHY: a data word, its length in bits,
its width in lines and an output enable mask. A command is the sequence of transfers sent while CS
is held low ([Architecture](#architecture)). The MMAP keeps CS low after a read, so that the next
sequential word costs only its data cycles ([Memory-mapped reads and writes](#mmap)).

## Wider phases {#primer-widths}

Wider phases take fewer SCK cycles. The figure below compares the same read in 1-1-4 and in 1-4-4
mode. In 1-1-4, only the data uses four lines: two SCK cycles per byte instead of eight. In 1-4-4,
the address also uses four lines, and takes 6 cycles instead of 24.

![The same 4-byte read in 1-1-4 (`0x6b`) and 1-4-4 (`0xeb`) mode. In 1-1-4 the opcode and the
address use DQ0 only; in 1-4-4 the address uses all four lines, which saves 18 cycles. The number
of cycles between the address and the data, mode bits and dummy cycles, is given by the datasheet
of each chip.](primer_widths.svg)

In 1-2-2 and 1-4-4 mode, many flashes read the first cycles after the address as *mode bits*. A
given value of these bits keeps the chip in a continuous read mode, where the next command has no
opcode. The remaining cycles are dummy cycles. The datasheet gives both counts.

LiteSPI drives no mode bits: the MMAP sends the whole gap between the address and the data as one
dummy phase, with its outputs disabled. The module count must therefore include the mode-bit
cycles: a W25Q128JV 1-4-4 read (`0xeb`), for example, needs 2 mode cycles plus 4 dummy cycles, that
is 6. The module stores the number of cycles, per read opcode when it differs: the `APS6404L` SPI
RAM, which has no mode bits, uses 6 cycles for its 1-4-4 read and 8 for its 1-1-1 fast read.

This is a limitation of the database as it is. The `W25Q128JV` module gives 4 cycles for its 1-4-4
read and 0 for its 1-2-2 read, the dummy counts of the datasheet without the mode-bit cycles (6 and
4 in total). With these values the MMAP would start the data phase too early and return shifted
data. No LiteX-Boards target uses these two reads. The 1-4-4 and 1-2-2 counts of the `W25Q512JV`,
`S25FL128L` and `MX25L12833F` modules (8 cycles) are to be checked against their datasheets
([Dummy cycles](#mod-dummy)).

## Speed limits {#primer-speed}

A flash has two plain reads. The slow read (`0x03`) has no dummy cycles, so the data must be ready
half an SCK cycle after the last address bit: it only works at low SCK frequencies. The fast read
(`0x0b`) adds dummy cycles and runs at the full SCK frequency of the chip. All wide reads have a gap
between the address and the data too: dummy cycles, and mode bits on the x-2-2 and x-4-4 reads.

The datasheet gives the highest SCK frequency of each read command. The `APS6404L` module, for
example, notes 33 MHz for the slow read and 84 MHz for the fast and quad reads. The board then adds
its own limit: the trace delays and the I/O delays of the FPGA, within half an SCK period.

In LiteSPI, the module class records whether the chosen read is a fast read (`fast_mode`); the MMAP
adds the dummy cycles only then. The SDR PHY divides its clock to make SCK, and its divisor
can be lowered at run time; the LiteX BIOS searches the fastest divisor that reads the flash
correctly ([BIOS, boot and flash update](#software)).

## SDR and DTR {#primer-dtr}

Most SPI memories move one bit per line per SCK cycle, on the rising edge: this is single transfer
rate (SDR). Some chips also offer double transfer rate (DTR) commands, which move a bit on each
edge of SCK. Octal chips use DTR in their 8-8-8 mode (OPI), often with a data strobe from the
memory.

LiteSPI supports SDR commands only. The opcode table lists DTR opcodes, such as
`READ_1_4_4_DTR`, but both PHYs refuse a module configured for one.

The 1:2 PHY of LiteSPI uses the DDR registers of the FPGA I/O to run SCK at its own clock, the
system clock by default. That
double rate is on the FPGA side: the flash sees SDR commands ([PHYs](#phys)).

## Bytes, words and addresses {#primer-bytes}

A flash address is a byte address. The bits of each byte go out most significant bit first, and a
read returns the bytes in increasing address order. A 3-byte address reaches 16 MiB; larger chips
use 4-byte addresses ([Addresses above 16 MiB](#flash-4byte)).

The MMAP serves 32-bit bus words. It reads four flash bytes for each word, and its endianness sets
where the first byte lands. With `big`, the default of the core, the byte at the lowest address is
the most significant byte of the word; with `little`, it is the least significant byte.
`add_spi_flash` passes the endianness of the CPU, so that the CPU sees the bytes at the same
addresses as in the flash.

## In the code {#primer-code}

| Concept | Where |
|----------------------------------|------------------------------------------------------|
| Opcodes, modes and their names | `litespi/opcodes.py` (`SpiNorFlashOpCodes`) |
| Width of each phase, fast read | `litespi/spi_nor_flash_module.py` (`read_opcode`) |
| Dummy cycles of a chip | `dummy_bits` or `dummy_cycles` of a class of `litespi/modules/` |
| SPI mode, edges, pins | `litespi/phy/generic_sdr.py`, `litespi/clkgen.py` |
| Phases of a read | `litespi/core/mmap.py` (`LiteSPIMMAP`) |

## Where to go next {#primer-next}

[Inside a SPI NOR flash](#flash-primer) for erase, program and quad enable; [Architecture](#architecture)
for how LiteSPI turns these commands into transfers; [PHYs](#phys) for the pins and the clock.
