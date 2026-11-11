# Memory-mapped reads and writes {#mmap}

This chapter describes the MMAP: the frontend that maps the flash into the address space of the
SoC, so that the CPU reads it like a ROM and can execute code from it (XIP). Read it to know what
a bus read costs on the SPI side, to tune the dummy cycles or the divisor, or to enable writes.
Its commands are explained in [SPI memories in a nutshell](#spi-primer).

## At a glance {#mmap-glance}

| Item | Value |
|----------------------|-------------------------------------------------------------------|
| Class | `LiteSPIMMAP` (`litespi/core/mmap.py`), built by `LiteSPI` when the PHY has a module |
| Bus | Wishbone slave, 32-bit words, read-only by default |
| Read command | The read command of the module, chosen at instantiation ([The SPI memory database](#modules)) |
| Phases | Opcode, address (24 or 32 bits), dummy (optional), data |
| Bursts | Reads at consecutive addresses share one command while CS stays low |
| End of a burst | Another address, a write, or 256 idle `sys` cycles |
| Prefetch, cache | None inside the MMAP: the next word is clocked only when the bus asks for it |
| Byte order | `mmap_endianness`, set to the CPU endianness by `add_spi_flash` |
| Writes | `with_mmap_write`: `False` (default), `True` (SPI RAM), `"csr"` (flash, under software control) |
| Registers | `mmap_clk_divisor`, `mmap_dummy_bits`, `mmap_write_config` |
| Status | Reads and XIP validated, writes in development: see [status](#intro-status) |

## From a bus read to a SPI command {#mmap-read}

The MMAP turns each Wishbone read into the phases of a SPI read command. Each phase is one transfer
on the core-to-PHY stream: the MMAP sends the transfer, then waits for the word the PHY returns
before it sends the next one ([Architecture](#architecture)). The words returned during the opcode,
address and dummy phases carry no data and are dropped.

The figure below shows the read state machine. Each box is a pair of states: the first sends the
transfer, the second waits for its return. A read that follows the previous one goes from IDLE
straight to the data phase.

![Read state machine of the MMAP. Follow the cyan path: a read at the address that follows the
previous read skips the opcode, address and dummy phases while CS is still
low.](mmap_fsm.svg)

The phases take their lengths and widths from the module, as the table below shows. The opcode is
always 8 bits; the address is 24 bits, or 32 bits for a read command whose name ends in `_4B`.

| Phase | States | Bits | Lines | DQ outputs |
|---------|-----------------------|------------------------|----------------|---------|
| Opcode | `BURST-CMD`, `CMD-RET` | 8 | `cmd_width` | Driven |
| Address | `BURST-ADDR`, `ADDR-RET` | `addr_bits` (24 or 32) | `addr_width` | Driven |
| Dummy | `DUMMY`, `DUMMY-RET` | `mmap_dummy_bits` | `addr_width` | Released |
| Data | `BURST-REQ`, `BURST-DAT` | 32 | `bus_width` | Released |

The address is a byte address: four times the Wishbone word address. Reads are therefore always
aligned 32-bit words, and a byte or half-word load by the CPU fetches the whole word. The dummy
phase is skipped when the dummy register is 0.

The address phase sends only the low `addr_bits` bits. With a 3-byte read command, the MMAP
reaches the first 16 MiB of the chip, and a larger region shows that part again above 16 MiB.
The MMAP never sends the enter 4-byte mode command: a chip above 16 MiB needs a `_4B` read command
([Inside a SPI NOR flash](#flash-primer)).

## Bursts {#mmap-burst}

After each word, the MMAP keeps CS low and remembers the next word address. When the next read
asks for that address, the MMAP sends only a new data phase. The flash streams the following
bytes as long as CS stays low, so sequential reads cost one command, then one data phase per
word.

The figure below shows a burst of three words. SCK stops between two words: the PHY clocks the
next data phase only when the bus asks for it, and the flash waits.

![A read burst. Look at the second and third reads: only the data phase goes out, and CS stays low
from the opcode to the idle timeout.](mmap_burst.svg)

A burst ends in three cases. A read at another address releases CS for one cycle and starts a new
command; the CS control of the PHY then keeps CS high for its minimum time
([Architecture](#architecture)). A write ends the read burst too. Finally, CS rises after 256
consecutive `sys` cycles in IDLE without a request.

The timeout also frees the PHY for the register master. While its burst holds CS low, the MMAP
keeps the grant of the crossbar, so a master command waits until the timeout expires
([Sharing the PHY with the MMAP](#master-sharing)). The timeout is the constant
`MMAP_DEFAULT_TIMEOUT` of `litespi/common.py`, not a parameter.

### What a burst costs {#mmap-burst-cost}

The table below counts the SCK cycles of each phase for common read commands: the first word pays
the whole command, the next words only their data phase. These counts are computed from the phase
lengths of the code; they leave out the per-transfer handshakes of the PHY and the bus cycles.

| Read command | Opcode | Address | Dummy | Data | First word | Next word |
|------------------------------|---------:|----------:|---------:|--------:|---------:|---------:|
| `READ_1_1_1` | 8 | 24 | 0 | 32 | 64 | 32 |
| `READ_1_1_1_FAST` | 8 | 24 | 8 | 32 | 72 | 32 |
| `READ_1_1_2` | 8 | 24 | 8 | 16 | 56 | 16 |
| `READ_1_1_4` | 8 | 24 | 8 | 8 | 48 | 8 |
| `READ_1_1_4_4B` | 8 | 32 | 8 | 8 | 56 | 8 |
| `READ_1_4_4` | 8 | 6 | 4 | 8 | 26 | 8 |
| `READ_4_4_4` | 2 | 6 | 6 | 8 | 22 | 8 |

The rows use 8 dummy cycles, the value of most modules, except the 1-4-4 row (4 cycles, the
database value of `W25Q128JV`, see [Dummy cycles](#mmap-dummy)) and the 4-4-4 row (6 cycles of
`MX25L12833F`).

A wide data path pays off on sequential reads, where the next word costs 8 SCK cycles at x4
against 32 at x1. On scattered reads, the command dominates. Cycle counts simulated with the PHY
are in [Performance](#performance).

## Dummy cycles {#mmap-dummy}

Fast read commands need dummy cycles between the address and the data, while the flash fetches the
first bytes ([SPI memories in a nutshell](#spi-primer)). The MMAP sends them as one transfer with
all DQ outputs released. Its length is in bits at the address width: dummy cycles times address
lines.

The default comes from the module: `dummy_cycles * addr_width` for a fast read command, and 0
otherwise. A command is fast when its name contains `FAST` or when its data uses more than one
line. The table below gives the defaults that `LiteSPIMMAP` computes for `W25Q128JV`.

| Read command | Dummy cycles | Address lines | Default dummy bits |
|-------------------|-------------:|--------------:|-------------------:|
| `READ_1_1_1` | none | 1 | 0 |
| `READ_1_1_1_FAST` | 8 | 1 | 8 |
| `READ_1_1_4` | 8 | 1 | 8 |
| `READ_1_4_4` | 4 | 4 | 16 |

These are the values of the database. The datasheet of the W25Q128JV counts 2 mode-bit cycles plus
4 dummy cycles between the address and the data of a 1-4-4 read, and 4 mode-bit cycles of a 1-2-2
read, 6 and 4 cycles in total. Since the MMAP sends the whole gap as one dummy phase, the module
values of 4 and 0 would make the data phase start early and the words read shifted. No LiteX-Boards
target uses these two reads; check the module against the datasheet before using them ([Dummy
cycles](#mod-dummy)).

With `with_csr=True` (the default), the 8-bit register `mmap_dummy_bits` holds the value and
software can change it, for instance after it changes the latency setting of the flash. The dummy
transfer copies it into the 6-bit length field of the transfer, so only values up to 63 are sent as
such; larger ones are truncated (the largest module default is 32). With
`with_csr=False`, the value is a constant of the gateware. The LiteX BIOS writes the register only
when a `SPIFLASH_MODULE_DUMMY_BITS` constant is defined, which `add_spi_flash` does not do.

The dummy phase drives no line. On a 1-2-2 or 1-4-4 read, the cycles that the flash uses for mode
bits are therefore left undriven: the flash reads whatever level the lines float to or the pull-ups
give, and a pattern that happens to select continuous read mode would make it expect the next
command without its opcode. The MMAP does not use continuous read mode and sends the opcode with
every command.

## Byte order {#mmap-endianness}

The flash returns bytes in address order, most significant bit first, and the PHY assembles them
into a 32-bit word with the first byte in bits 31:24. The `endianness` parameter of the MMAP
(`mmap_endianness` of `LiteSPI`) decides where that byte ends up on the bus.

| `endianness` | Byte at the lowest address | Use |
|--------------|----------------------------|----------------------------------------|
| `"big"` | Bits 31:24 | Default of `LiteSPI`, big-endian CPUs |
| `"little"` | Bits 7:0 | Little-endian CPUs |

`add_spi_flash` passes the endianness of the CPU, so that a byte load at offset N of the region
returns byte N of the flash on every CPU. A design that instantiates `LiteSPI` directly sets it to
match its bus masters.

## Clock divisor {#mmap-divisor}

Every transfer carries a divisor for the SDR PHY. The MMAP sends the value of its register
`mmap_clk_divisor`; 0, the reset value, tells the PHY to use its own register `phy_clk_divisor`.
The MMAP and the master can therefore read at different SCK frequencies. The divisor formula is in
[PHYs](#phys).

The BIOS frequency calibration writes both the PHY and the MMAP divisors
([BIOS, boot and flash update](#software)). The 1:2 PHY ignores the divisor: SCK runs at the PHY
clock, and the register exists but has no effect.

## Writes {#mmap-write}

MMAP writes are in development ([status](#intro-status)). They send Wishbone writes to the memory
as program commands. The `with_mmap_write` parameter of `LiteSPI` selects them:

| `with_mmap_write` | Bus | Writes |
|----------------------|------------|-----------------------------------------------|
| `False` (default) | Read-only | Not acknowledged: the bus timeout of the SoC ends the access with an error |
| `True` | Read-write | Always sent: meant for SPI RAM, used by `add_spi_ram` |
| `"csr"` | Read-write | Sent while `write_enable` is 1, otherwise acknowledged and dropped |

The code reserves `True` for RAM: a flash must be erased before it is programmed, and only
software can decide when. With `"csr"`, software erases the area through the master, sets the
`write_enable` bit of `mmap_write_config`, writes, then clears the bit.

### What a write sends {#mmap-write-command}

A write uses the program command of the module (`program_cmd`, `PP_1_1_1` by default) with the
widths and the address length of its name. Each selected byte of the word is one 8-bit transfer,
byte lane 0 (bits 7:0) first, at the byte address of the word.

Sequential full-word writes continue the same command, like read bursts. A new command starts in
the following cases:

- the write is not at the address that follows the previous write;
- byte lane 0 of the word is not selected;
- the word is the first word of a page (page size a power of two and a multiple of 4 bytes);
- the previous access was a read, or the burst timed out.

The figure below shows the page case: the last word of a page completes its command, and the first
word of the next page starts a new one.

![A write across a page boundary. Look at CS: it rises between the two words, and the second word
starts with its own program opcode and address, without a write enable: on a flash, software must
send one before each command.](mmap_write.svg)

Unselected bytes are skipped. Leading unselected bytes only advance the address; an unselected byte
after a selected one ends the command, and the next selected byte of the word starts a new command
at its own address.

### What a write does not do {#mmap-write-limits}

The MMAP sends neither the write enable command nor the status polling that a flash needs around
each program command, and it never erases. With a flash, software provides them through the master:
write enable, MMAP writes within one page, then status polling once the MMAP has released CS. A
SPI RAM needs none of them.

The page restart above therefore only works on a SPI RAM. A flash clears its write enable latch at
the end of each program command, so on a flash the second command of the figure is ignored unless
software sends a new write enable first.

Writes always send byte lane 0 to the lowest address. This matches the read order of
`endianness="little"` only: with `"big"`, a word read back has its bytes in the reverse order of the
word written. This also applies to `add_spi_ram`, which passes the endianness of the CPU, on a
big-endian CPU.

## Caches in front of the MMAP {#mmap-cache}

The MMAP has no prefetch, read buffer or cache. Code executed from flash relies on the caches of
the CPU: an instruction cache refills a line with reads at consecutive addresses, which the MMAP
serves as one burst. `add_spi_flash` adds no cache of its own.

`add_spi_ram` places a LiteX Wishbone L2 cache (`l2_cache_size`, 8192 bytes by default) between
the bus and the MMAP, since SPI RAM takes both reads and writes ([Integration in a LiteX
SoC](#integration)). After software programs the flash through the master, the CPU data cache can
hold stale words: the BIOS invalidates the range before it verifies it.

## Registers {#mmap-registers}

| Register | Bits | Reset | Role |
|--------------------------|-----:|---------------|----------------------------------|
| `mmap_clk_divisor` | 10 | 0 | Divisor of the MMAP transfers, 0: use the PHY register |
| `mmap_dummy_bits` | 8 | From the module | Length of the dummy phase, in bits at the address width |
| `mmap_write_config` | 1 | 0 | Bit 0 `write_enable`, with `with_mmap_write="csr"` only |

The full names carry the prefix of the core, `spiflash_` in a LiteX SoC. Offsets and field
descriptions are in the [Register reference](#registers).

## In the code {#mmap-code}

| Item | File | Name |
|----------------|------------------------------|--------------------------------|
| Read and write frontend | `litespi/core/mmap.py` | `LiteSPIMMAP` |
| Burst timeout | `litespi/common.py` | `MMAP_DEFAULT_TIMEOUT` |
| Instantiation | `litespi/__init__.py` | `LiteSPI`: `with_mmap`, `mmap_endianness`, `with_csr`, `with_mmap_write`, `mmap_cs_mask` |
| Tests | `test/test_spi_mmap.py` | Reads, dummy cycles, 4-byte addresses, writes, byte selects, page boundaries |

Where to go next: [The register master](#master) for the other frontend, [Integration in a LiteX
SoC](#integration) to map the flash in a SoC, [Performance](#performance) for simulated cycle
counts.
