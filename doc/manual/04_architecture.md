```{=latex}
\part{The core}
```

```{=html}
<h1 class="part">Part II. The core</h1>
```

# Architecture {#architecture}

LiteSPI splits SPI memory access in two halves. The core turns bus accesses and software requests
into a list of transfers; the PHY turns each transfer into SCK edges and DQ bits. This chapter
describes the core, the transfer between core and PHY, and the clock and chip select rules of
every PHY. The PHYs are in [PHYs](#phys).

## At a glance {#arch-glance}

| Block | Class | Role | Clock domain |
|----------------|----------------------------|------------------------------------|----------------|
| Wrapper | `LiteSPI` | Builds and connects the blocks below | sys |
| MMAP | `LiteSPIMMAP` | Wishbone slave: flash reads as memory | sys |
| Master | `LiteSPIMaster` | Register-driven transfers for software | sys |
| Crossbar | `LiteSPICrossbar` | Shares the PHY, optional clock crossing | sys and PHY |
| PHY | `LiteSPIPHY` | SCK, DQ and CS at the pins | PHY domain |
| CS control | `LiteSPICSControl` | Minimum CS high time, CS output register | PHY domain |

The PHY domain is `sys` unless the design gives LiteSPI its own clock domain
([Clock domains](#arch-cdc)). The registers of each block are listed in the
[Register reference](#registers).

## Blocks {#arch-blocks}

Two frontends produce transfers: the MMAP for the CPU bus and the master for software. The
crossbar lets one of them use the PHY at a time and forwards the chip select of that frontend. The
figure below shows the blocks and the path of a transfer.

![LiteSPI blocks: the MMAP (Wishbone) and the master (CSR bus) share the PHY through the
crossbar. The blue path carries the transfers, with an optional clock domain crossing. Inside the
PHY, the shift registers drive DQ, the clock generator SCK and CS control the chip
select.](arch_blocks.svg)

The core never sees an SPI pin. It knows the flash only through the module object that the PHY
carries (`phy.flash`): the read opcode, the widths of each phase, the dummy cycles and the page
size ([The SPI memory database](#modules)). Without a module, LiteSPI builds no MMAP.

## The transfer contract {#arch-transfer}

The one idea of the core is the transfer. A transfer is one element of the stream from the core
to the PHY: it asks the PHY to clock out some bits on some lines and to return the bits it sampled
meanwhile. The table below lists its fields (`spi_core2phy_layout`).

| Field | Bits | Meaning |
|-----------|------|----------------------------------------------------------------------|
| `data` | 32 | Bits to send, right-aligned: the PHY sends the `len` low bits, MSB first |
| `len` | 6 | Number of bits of the transfer, at most 32 |
| `width` | 4 | Number of DQ lines used: 1, 2, 4 or 8 |
| `mask` | 8 | Output enable per DQ line; 0 releases the line so the flash can drive it (ignored on `mosi`/`miso` pads) |
| `clk_div` | 10 | SCK divisor for this transfer; 0 uses the PHY register |

For each transfer, the PHY returns one 32-bit word (`spi_phy2core_layout`) holding the bits it
shifted in, the last one in bit 0. Only the low `len` bits are meaningful; both PHYs return the
other ones at 0. Every transfer returns a word,
even a pure write, and the frontend drops the words it does not need. One transfer lasts
`len / width` SCK cycles.

A command is a sequence of transfers while the frontend keeps CS active. The MMAP reads one 32-bit
word with up to four transfers: opcode, address, dummy (skipped when the dummy length is 0) and
data. The figure below shows them for a read
in mode 1-1-4 on a flash with 8 dummy cycles; the phases themselves are explained in
[SPI memories in a nutshell](#spi-primer).

![One MMAP read in mode 1-1-4 as four transfers: each phase is one transfer with its own length,
width and output mask. CS stays low across the four, and only the word of the data transfer goes
back to the bus.](arch_transfer.svg)

The dummy transfer has an output mask of 0: the PHY clocks SCK without driving any line, so the
flash can turn the lines around. Its length is the MMAP dummy bits register, counted in bits at the
address width: 8 dummy cycles in mode 1-1-4 are 8 bits. Its default is in
[Memory-mapped reads and writes](#mmap).

A burst repeats only the last transfer. When the next bus read follows the previous address and
CS is active, the MMAP sends one more data transfer, without opcode or address. A transfer
never spans two commands: the frontend alone decides when CS goes high.

Since the PHY accepts any length, width and mask, the same PHY serves 1-1-1 reads, quad page
programs and QPI commands. Only the frontends know what a command means. The master exposes the
transfer fields as registers, so software can build any command made of 32-bit transfers
([The register master](#master)).

## The frontends {#arch-frontends}

The MMAP is a 32-bit Wishbone slave, read-only unless `with_mmap_write` enables writes. It requests
the PHY from the start of a command to the end of its burst. A burst ends on a non-sequential
access or after 256 idle cycles (`MMAP_DEFAULT_TIMEOUT`). The details are in
[Memory-mapped reads and writes](#mmap).

The master turns register writes into transfers: software sets the chip select register, the
transfer fields and the data, then reads the returned word. It requests the PHY while its chip
select register is not zero. The details are in [The register master](#master).

Both frontends carry a divisor register. A non-zero value goes into the `clk_div` field of their
transfers and overrides the PHY divisor for those transfers only. The reset value, 0, keeps the PHY
divisor. Only the SDR PHY uses this field ([The clock divider](#phys-divider)).

## The crossbar {#arch-crossbar}

The crossbar has one port per frontend: the MMAP first, then the master. A round-robin arbiter
grants the PHY to one port and keeps the grant until that port drops its request (`RoundRobin`,
withdraw policy). The transfers of the granted port go to the PHY, its returned words come back to
it, and its chip select drives the PHY.

Two rules follow for the user. While the MMAP holds a burst, a master command waits until the
burst ends. While software holds the master chip select, the MMAP waits too, instruction fetches
from the flash included. Code that drives the master must therefore not run from the flash it
talks to.

## Chip select control {#arch-cs}

CS control sits in the PHY and owns the CS pins. It holds CS high for a minimum time between two
commands, and it drives `cs_n` through the output register of the family (`SDROutput`). The table
lists its parameters, given as keyword arguments of the PHY.

| Parameter | Default | Effect |
|-----------------|---------|------------------------------------------------------------|
| `cs_delay` | 10 | PHY clock cycles of CS high before a new command can start |
| `with_sdr_cs` | True | Drive `cs_n` through `SDROutput`; False drives it directly |

The delay restarts when CS goes high, and the PHY accepts the first transfer of the next command
only once it has elapsed. Transfers inside one command do not wait. A flash with a 20 ns minimum CS
high time (GD25LQ128D) at a 75 MHz system clock needs 2 cycles instead of 10.

The SDR PHY also keeps CS high until its vendor clock backend has finished its startup cycles
([Vendor clock and I/O backends](#phys-backends)).

### Several chip selects {#arch-multi-cs}

The width of the CS pad (`cs_n`) sets the number of chip selects; the crossbar, the frontends and
CS control take that width. The MMAP drives the lines set in `mmap_cs_mask`, the first one by
default. The master drives the lines set in its chip select register.

With several lines, CS control skips the delay when the new command selects another line than
the previous one: only the same chip needs its minimum CS high time. The MMAP reads one chip, the
one its module describes; the master reaches the others.

## The LiteSPI wrapper {#arch-litespi}

`LiteSPI` builds the crossbar, adds the frontends and connects them to the PHY passed as its first
argument. The LiteX SoC builds it from `add_spi_flash` ([Integration in a LiteX SoC](#integration));
a design without LiteX SoC instantiates it directly. The table lists its parameters.

| Parameter | Default | Effect |
|------------------------------|---------|----------------------------------------------|
| `phy` | | PHY with `sink`, `source`, `cs` and `flash` |
| `clock_domain` | `"sys"` | Clock domain of the PHY; another value adds the CDC |
| `with_mmap` | True | Add the MMAP (needs `phy.flash`) |
| `mmap_endianness` | `"big"` | `"little"` reverses the bytes of each word |
| `with_mmap_write` | False | True (SPI RAM) or `"csr"` (flash, enable register) |
| `mmap_cs_mask` | 1 | Chip selects driven by the MMAP |
| `with_csr` | True | Add the MMAP dummy bits register |
| `with_master` | True | Add the master |
| `master_tx_fifo_depth` | 1 | Transfers queued in the master |
| `master_rx_fifo_depth` | 1 | Returned words queued in the master |
| `master_with_irq` | False | Interrupt when a returned word is ready |

`add_spi_flash` sets `mmap_endianness` from the CPU endianness. It passes its other keyword
arguments to both the PHY and `LiteSPI`, so `cs_delay` or `with_master=False` can be given there.
The complete list of options is in [Build options](#build-options).

## Clock domains {#arch-cdc}

By default the whole core and the PHY run on the system clock. With `clock_domain` set to another
domain, the PHY runs in that domain and the crossbar adds two asynchronous FIFOs, one per
direction. The frontends, the crossbar and every register stay in `sys`, as the figure below
shows.

![Separate LiteSPI clock domain: the frontends and the crossbar stay in sys, two AsyncFIFOs carry
the transfers and the returned words, the PHY register values cross through MultiReg, and the CS of
the crossbar drives the PHY directly.](arch_cdc.svg)

| Signal | Crossing |
|---------------------------------|---------------------------------------------------|
| Transfers | `stream.AsyncFIFO`, 32 entries, `sys` to PHY domain |
| Returned words | `stream.AsyncFIFO`, 32 entries, PHY domain to `sys` |
| PHY divisor and mode registers | `MultiReg` (`ResyncReg`) |
| CS of the crossbar | None: wired to the PHY |

The PHY and `LiteSPI` must receive the same domain name; `add_spi_flash` passes `clock_domain` to
both. The design creates the clock domain itself. Both PHYs divide their clock, so a separate
domain is only needed for an SCK that no divisor of `sys` gives ([The 1:2 PHY](#phys-ddr)).

The CS of the crossbar reaches the PHY domain without a synchronizer. A frontend raises CS in the
cycle it sends its first transfer, which then spends several cycles in the FIFO, and keeps CS until
its last returned word is back. Between two reads that do not follow each other, however, the MMAP
releases CS for a single `sys` cycle. A PHY clock slower than `sys` can miss that release and send
the next opcode inside the previous command, so a separate domain has to run at least as fast as
`sys`. No LiteX-Boards target uses a separate domain; test it in simulation first. The path crosses
between two clocks and the design has to declare it in its timing constraints.

## In the code {#arch-code}

| Function | File | Classes |
|--------------------|-----------------------------------|-----------------------------------|
| Wrapper | `litespi/__init__.py` | `LiteSPI` |
| Transfer layouts | `litespi/common.py` | `spi_core2phy_layout`, `spi_phy2core_layout` |
| Crossbar, CDC | `litespi/crossbar.py` | `LiteSPICrossbar` |
| MMAP | `litespi/core/mmap.py` | `LiteSPIMMAP` |
| Master | `litespi/core/master.py` | `LiteSPIMaster` |
| CS control | `litespi/cscontrol.py` | `LiteSPICSControl` |

CS control is covered by `test/test_cscontrol.py`, the frontends by `test/test_spi_mmap.py` and
`test/test_spi_master.py` ([Simulation and tests](#simulation)).

Where to go next: [PHYs](#phys) for the other side of the transfer,
[Memory-mapped reads and writes](#mmap) and [The register master](#master) for the frontends.
