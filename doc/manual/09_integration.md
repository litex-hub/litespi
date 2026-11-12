```{=latex}
\part{Use it}
```

```{=html}
<h1 class="part">Part III. Use it</h1>
```

# Integration in a LiteX SoC {#integration}

This chapter adds a SPI flash to a LiteX SoC: the one call that does it, the choices it asks for
(module, read mode, PHY rate, clock), the BIOS run in place from the flash, and the ways to use
LiteSPI outside a LiteX SoC. Read it when you write or change a target; the software side is in
[BIOS, boot and flash update](#software).

## At a glance {#integ-glance}

`SoC.add_spi_flash` of LiteX builds everything a target needs from a module and a set of pads.
The figure below shows what it adds to the SoC.

![What `add_spi_flash` adds to a SoC. Follow the cyan path: the CPU reads the flash through the
`spiflash` bus region and the MMAP; software reaches the master through registers on the CSR bus;
the constants tell the BIOS which chip it drives.](integ_soc.svg)

| Item | What `add_spi_flash` does |
|---------------------|------------------------------------------------------------------|
| PHY | `LiteSPIPHY` on the `spiflash` or `spiflash4x` pads, or the `phy` you pass |
| Core | `LiteSPI` with the MMAP, the master unless disabled, the crossbar |
| Bus region | `spiflash`, size of the module, mode `rx` (`rwx` with MMAP writes) |
| Registers | PHY, MMAP and master registers under the `spiflash` prefix |
| Interrupt | Master `rx_ready` interrupt when the SoC has an IRQ slot named `spiflash` |
| Constants | Frequency, module name, sizes, erase geometry, quad and QPI flags |

A target enables it with a few lines. The Arty A7 target, for example, adds its S25FL128L in
mode 1-1-4 with the 1:2 PHY and the master:

```python
from litespi.modules import S25FL128L
from litespi.opcodes import SpiNorFlashOpCodes as Codes
self.add_spi_flash(mode="4x", module=S25FL128L(Codes.READ_1_1_4), rate="1:2", with_master=True)
```

The flash region then appears in the memory map of the SoC, and the BIOS initializes the flash at
boot. Without a board, `litex_sim --with-spi-flash` builds the same kind of SoC with a model of the
PHY ([A SoC with the BIOS: litex_sim](#sim-litex-sim)).

## The parameters {#integ-params}

The table below lists the parameters of `add_spi_flash`. Any other keyword goes to `LiteSPI`, and
also to `LiteSPIPHY` when `add_spi_flash` builds the PHY (not when you pass `phy`); [Build
options](#build-options) lists them.

| Parameter | Default | Meaning |
|--------------------|--------------|----------------------------------------------------|
| `name` | `"spiflash"` | Name of the pads, region, registers and constants |
| `mode` | `"4x"` | `"1x"` (pads `spiflash`) or `"4x"` (pads `spiflash4x`) |
| `clk_freq` | `20e6` | Requested SCK frequency in Hz |
| `module` | `None` | Module instance, which carries the read mode |
| `phy` | `None` | A PHY of your own instead of `LiteSPIPHY` |
| `rate` | `"1:1"` | `"1:1"` SDR PHY or `"1:2"` 1:2 PHY |
| `software_debug` | `False` | Adds `SPIFLASH_DEBUG`: the BIOS prints its steps |
| `number` | `None` | Index of the pads, for a board with several flashes |

The keywords that matter most are `with_master` (default `True` in `LiteSPI`), `with_mmap_write`
(see [Memory-mapped reads and writes](#mmap)), `extra_latency` (see [PHYs](#phys)) and
`clock_domain` ([A separate SPI clock domain](#integ-clock-domain)).

A module is required as soon as the MMAP is present, which is the default: the region takes the
size of the module. A `phy` without a module is accepted only without the MMAP.

## What it computes {#integ-computed}

The divisor of the PHY comes from the system clock and `clk_freq`. LiteX takes the smallest
integer divisor that does not exceed the requested frequency. For the SDR PHY, whose SCK is the
system clock divided by an even number, it rounds the divisor up to the next even number. The
frequency it records is the system clock divided by this divisor.

| System clock | `clk_freq` | Rate | Divisor | Constant `PHY_FREQUENCY` |
|--------------|------------|-------|---------|--------------------------|
| 100 MHz | 20 MHz | 1:1 | 6 | 16666666 |
| 100 MHz | 20 MHz | 1:2 | 5 | 20000000 |
| 50 MHz | 20 MHz | 1:1 | 4 | 12500000 |
| 1 MHz | 20 MHz | 1:1 | 2 | 500000 |

These rows are computed from the code of `add_spi_flash`; the last one is the `litex_sim` SoC.
The divisor is the reset value of the `clk_divisor` register of the PHY, which the BIOS can lower
at boot ([BIOS initialization](#sw-init)). The 1:2 PHY divides by any integer, so it skips the
rounding ([The 1:2 PHY](#phys-ddr)).

The constants below go to the generated `soc.h` and drive the BIOS. Each one starts with the
upper-case `name`, `SPIFLASH_` by default.

| Constant | Value |
|---------------------------|----------------------------------------------------------|
| `PHY_FREQUENCY` | System clock divided by the divisor |
| `PHY_MIN_DIVISOR` | 2 at 1:1, 1 at 1:2: the lowest divisor of the calibration |
| `MODULE_NAME` | Name of the module, such as `s25fl128l` |
| `MODULE_TOTAL_SIZE` | Size of the flash in bytes |
| `MODULE_PAGE_SIZE` | Program page in bytes |
| `MODULE_ERASE_*` | Opcode, size and address bits of the erase command |
| `MODULE_QUAD_CAPABLE` | Mode `"4x"`, a read command with 4 data lines, and the module lists `READ_1_1_4` |
| `MODULE_QUAD_ENABLE_*` | The quad enable method of the module, when it names one |
| `MODULE_QPI_CAPABLE` | Command width 4 and the module lists `READ_4_4_4` |
| `DEBUG` | `software_debug=True` |

The bus handler places the region at a free cached address, unless the memory map of the SoC
names `spiflash`. The MMAP byte order follows the CPU (`mmap_endianness`), so the CPU reads the
bytes of the flash in their order.

## Pads {#integ-pads}

The PHY takes the pads from the platform by name. A x1 flash uses separate data in and out lines;
a x4 flash uses a 4-bit bidirectional `dq` bus, the same pins with WP# and HOLD# as DQ2 and DQ3
([More data lines](#primer-lines)). The Arty A7 platform declares both on the same
pins:

```python
("spiflash", 0,
    Subsignal("cs_n", Pins("L13")),
    Subsignal("clk",  Pins("L16")),
    Subsignal("mosi", Pins("K17")),
    Subsignal("miso", Pins("K18")),
    Subsignal("wp",   Pins("L14")),
    Subsignal("hold", Pins("M14")),
    IOStandard("LVCMOS33"),
),
("spiflash4x", 0,
    Subsignal("cs_n", Pins("L13")),
    Subsignal("clk",  Pins("L16")),
    Subsignal("dq",   Pins("K17 K18 L14 M14")),
    IOStandard("LVCMOS33")
),
```

The PHY holds `wp` and `hold` high in x1 mode when the pads have them: write protect and hold stay
released without pull-ups on the board. A `dq` of 2 or 8 lines gives a x2 or x8 PHY when a target
builds the PHY itself; `add_spi_flash` only knows the `1x` and `4x` pad names.

When the pads have no `clk`, the flash clock leaves through a dedicated configuration pin. The PHY
then picks a clock backend from the FPGA device name:

| Device | Clock backend | Flash clock pin |
|------------------|--------------------------|------------------------------------|
| `xc7*` | `LiteSPISTARTUPE2` | CCLK, through the STARTUPE2 primitive |
| `LFE5U*` | `LiteSPIECP5USRMCLK` | MCLK, through the USRMCLK primitive |
| Other devices | none | `NotImplementedError` at build time |

[PHYs](#phys) describes both backends. On UltraScale+ the configuration flash is reached through
STARTUPE3, a full I/O backend that the target passes as `phy` ([A PHY of your own](#integ-phy)).

Several flashes on one board use `number`, which picks the pads of that index, and a different
`name` for each core. The Efinix Ti375 C529 target selects flash 0 or 1 with
`--spi-flash-number`.

## Choosing mode, read command, rate and clock {#integ-choices}

Four choices define the flash interface. The read mode lives in the module instance: the opcode
given to the module sets the number of lines of the command, address and data phases ([The SPI
memory database](#modules)).

| Choice | Options | Choose |
|-------------------|-------------------------------|---------------------------------------------------|
| Pads (`mode`) | `"1x"`, `"4x"` | `"4x"` when the four DQ lines reach the FPGA |
| Read command | `READ_1_1_1`, `READ_1_1_4` | The fastest read the module lists for those pads |
| 4-byte opcodes | `_4B` variants | Required to read beyond 16 MiB |
| Rate (`rate`) | `"1:1"`, `"1:2"` | `"1:1"` first; `"1:2"` for SCK up to the system clock |
| SCK (`clk_freq`) | Hz | Within the read limits of the datasheet |

Mode `"4x"` with a 1-1-1 read is valid: the PHY then uses DQ0 and DQ1 only. Several Artix-7 and
Kintex-7 targets do this, such as `qmtech_xc7a35t` and `qmtech_kintex7_devboard`, which read their
MT25QL128 in 1-1-1. The read does not use four data lines, so `QUAD_CAPABLE` is not defined and
the BIOS does not set the QE bit. As in x1 mode, the PHY then holds DQ2 and DQ3 high as WP# and
HOLD#: it does so when neither the read nor the program command of the module uses more than two
lines. In this configuration, master commands on four lines are not possible: DQ2 and DQ3 always
drive a high level.

A quad read needs the QE bit of the flash set ([Status registers and quad enable](#flash-qe)). The
BIOS sets it at boot when the master is present and the read uses four data lines. Without the
master, the bit must already be set in the chip: the iCEBreaker target, for example, has no master
and reads in 1-1-4.

At divisor 1 the 1:2 PHY moves one bit per line per PHY clock cycle, twice the best SDR rate. Its input
timing then depends on the board and the FPGA I/O, and `extra_latency` moves the sampling point.
The status of each PHY is in the [status table](#intro-status); the cycle counts are in
[Performance and resources](#performance).

## A PHY of your own {#integ-phy}

The `phy` argument replaces `LiteSPIPHY`. The PHY must provide the `sink` and `source` streams,
the `cs` signal and a `flash` attribute (the module), as `LiteSPIPHY` does. Two PHYs are used this
way:

- `LiteSPIXilinxUSPHY`, for the configuration flash of UltraScale+ devices, through STARTUPE3.
- `LiteSPIPHYModel`, the stream-level model of `litex_sim`.

The XCKU3P target (`alibaba_xcku3p`) builds its PHY this way, with its own divisor:

```python
spiflash_module  = MT25QU256(Codes.READ_1_1_1_FAST_4B, program_cmd=Codes.PP_1_1_1_4B)
spiflash_divisor = math.ceil(sys_clk_freq/20e6)
spiflash_divisor += spiflash_divisor % 2
self.add_spi_flash(mode="1x",
    module      = spiflash_module,
    phy         = LiteSPIXilinxUSPHY(spiflash_module, default_divisor=spiflash_divisor),
    with_master = True)
```

The divisor passed to the PHY is the one that counts: `add_spi_flash` uses its own only for the
constants. Compute both from the same frequency, as above. STARTUPE3 is in development (see the
[status table](#intro-status)).

## SPI RAM: add_spi_ram {#integ-spi-ram}

`SoC.add_spi_ram` uses the same PHY and core for a SPI PSRAM, such as the `APS6404L`, the only
RAM module of the database. It turns MMAP writes on and maps a region in mode `rwx`. A Wishbone L2
cache sits between the bus and the MMAP: 8192 bytes by default (`l2_cache_size`, rounded down to
a power of two, at least 8; 0 removes it), so the CPU sees an ordinary read/write memory.

```python
from litespi.modules.ram_modules import APS6404L
from litespi.opcodes import SpiNorFlashOpCodes as Codes
self.add_spi_ram(mode="4x", module=APS6404L(Codes.READ_1_1_4))
```

Its name is `spiram` by default, and the BIOS calibrates and tests it at boot (`spiram.c` in the
`liblitespi` library of LiteX). No LiteX-Boards target calls it, and it is in development (see the
[status table](#intro-status)): check the read and write commands of the module against your chip
first.

## Running the BIOS from the flash {#integ-xip}

Small FPGAs lack the block RAM for a BIOS ROM. Their targets place the `rom` region inside the
flash region and set the CPU reset address there: the CPU executes the BIOS in place (XIP)
through the MMAP. The figure below shows the address map.

![The BIOS run in place. The `rom` region is a window of the `spiflash` region at
`bios_flash_offset`; the CPU resets into it. On iCE40 and Efinix Trion boards the bitstream occupies
the start of the same flash; Gowin GW1N devices configure from their internal flash and place the
BIOS at offset 0.](integ_xip.svg)

The iCEBreaker target does it with the integrated ROM and SRAM disabled:

```python
self.add_spi_flash(mode="4x", module=W25Q128JV(Codes.READ_1_1_4), with_master=False)
self.bus.add_region("rom", SoCRegion(
    origin = self.bus.regions["spiflash"].origin + bios_flash_offset,
    size   = 32 * KILOBYTE,
    linker = True)
)
self.cpu.set_reset_address(self.bus.regions["rom"].origin)
```

The BIOS binary must then be written into the flash at `bios_flash_offset`, beside the bitstream.
The `--flash` option of the iCEBreaker target writes both. It first checks that the bitstream ends
before the offset (0x40000 by default, `--bios-flash-offset`) and that the BIOS fits the region.
Other targets choose other offsets, from 0x20000 to 0x200000 on iCE40 boards; the Gowin GW1N
targets use 0.

Nineteen LiteX-Boards targets use this layout, all on iCE40, Gowin GW1N or Efinix Trion FPGAs
([Supported FPGAs and boards](#boards)). Each instruction fetch that misses the CPU cache becomes
a flash read, so the BIOS runs slower than from block RAM; sequential fetches continue the same
command ([Bursts](#mmap-burst)).

## A separate SPI clock domain {#integ-clock-domain}

The `clock_domain` keyword runs the PHY in another clock domain. `add_spi_flash` passes it to
both the PHY and `LiteSPI`: the crossbar then inserts asynchronous FIFOs between the frontends,
which stay in `sys`, and the PHY. The divisor register of the SDR PHY is resynchronized to the new
domain.

The target must create the clock domain before the call. No LiteX-Boards target uses this option:
it serves when the flash needs a SCK that the system clock and an even divisor cannot give.

Only the data crosses through the FIFOs: the CS of the crossbar reaches the PHY domain without a
synchronizer. Between two non-sequential reads, the MMAP releases CS for a single `sys` cycle,
which a slower PHY clock can miss. Use a PHY clock at least as fast as `sys`, declare the crossing
in the timing constraints, and test the design in simulation first.

## Without the LiteX SoC {#integ-direct}

LiteSPI is a set of Migen modules, and a design can build them directly. The lines below make a
x4 PHY and a core with the MMAP only; `spiflash.bus` is a 32-bit Wishbone slave addressed in
words from the start of the flash.

```python
from litespi.modules import W25Q128JV
from litespi.opcodes import SpiNorFlashOpCodes as Codes
from litespi.phy.generic import LiteSPIPHY
from litespi import LiteSPI

module = W25Q128JV(Codes.READ_1_1_4)
self.spiflash_phy = LiteSPIPHY(platform.request("spiflash4x"), module,
    device=platform.device, default_divisor=4)
self.spiflash     = LiteSPI(self.spiflash_phy, with_master=False, mmap_endianness="little")
```

Nothing sets the QE bit in this case: write it once into the flash, or keep the master and send
the command from software ([The register master](#master)).

## Standalone Verilog: litespi_gen {#integ-gen}

`litespi_gen` writes LiteSPI as a Verilog module for a design that does not use LiteX. It builds a
minimal SoC with the core, puts the pads and the bus on top-level ports, and stops before any
vendor tool. Its options are below.

| Option | Default | Meaning |
|------------------------|--------------|---------------------------------------------------|
| `--module` | `S25FL128L` | Module class name from the database |
| `--mode` | `x1` | `x1` or `x4`; the read is `READ_1_1_1` or `READ_1_1_4`, its `_4B` variant above 16 MiB |
| `--rate` | `1:1` | `1:1` SDR PHY or `1:2` 1:2 PHY |
| `--divisor` | `2` at 1:1, `1` at 1:2 | Reset divisor of the PHY; the SDR PHY rounds an odd divisor up |
| `--bus-standard` | `wishbone` | `wishbone` or `axi-lite` (through a converter) |
| `--bus-endianness` | `big` | Byte order of the MMAP words |
| `--with-master` | off | Adds a second bus port, for the registers |
| `--vendor` | `xilinx` | `xilinx`, `altera`, `intel` or `lattice` primitives |
| `--sim` | off | Uses `LiteSPIPHYModel` instead of the PHY |

`--clk-freq` is accepted but not used, and the docstring of `gen.py` mentions a YAML file that the
command does not read. The MMAP of this core has no dummy bits register (`with_csr=False`): the
dummy cycles of the module are fixed.

The command below generates a x4 Wishbone core. It writes `build/gateware/litespi_core.v` and the
register map in `build/csr.csv`. On a chip larger than 16 MiB, such as the 32 MiB `S25FL256L` of
this example, the generator selects the 4-byte address read (`READ_1_1_4_4B` here) when the module
lists it, so the core reads the whole chip. Otherwise it prints a warning and keeps the 3-byte
read, which reaches the first 16 MiB only.

```sh
litespi_gen --module=S25FL256L --mode=x4 --bus-standard=wishbone
```

The ports of the module it wrote, with this revision of LiteSPI and LiteX, are:

```verilog
module litespi_core (
    output wire          bus_ack,
    input  wire   [29:0] bus_adr,
    input  wire    [1:0] bus_bte,
    input  wire    [2:0] bus_cti,
    input  wire          bus_cyc,
    output wire   [31:0] bus_dat_r,
    input  wire   [31:0] bus_dat_w,
    output wire          bus_err,
    input  wire    [3:0] bus_sel,
    input  wire          bus_stb,
    input  wire          bus_we,
    input  wire          clk,
    input  wire          rst,
    output reg           spiflash4x_clk,
    output reg           spiflash4x_cs_n,
    inout  wire    [3:0] spiflash4x_dq
);
```

`bus_adr` is a word address within the flash. The `inout` port needs a tristate pin in the design
above it. Keep the `clk`, `cs_n` and `dq` registers close to the pins, in the I/O cells where the
family allows it, for the timing the PHY assumes.

## A real SoC {#integ-example}

The diagram below comes from an Enjoy-Digital design on the Efinix Ti375 C529 development kit.
The QSPI flash stores both the bitstream and the firmware; LiteSPI reads it at 25 MHz in this
design (the LiteX-Boards target asks for 112 MHz), and the BIOS boots the firmware from it before
the rest of the system starts.

![A LiteX SoC on the Efinix Ti375 C529 development kit. Look at the left: the QSPI flash
holds the bitstream and the firmware, and LiteSPI connects it to the CPU for the BIOS flash
boot.](integ_ti375_soc.jpg)

## Timing notes {#integ-timing}

The MMAP read path decides the timing on small FPGAs: rebuild the boards you target after
changing it. The SDR PHY registers its outputs and inputs, and its sampling point depends on the
I/O delays of the family; `extra_latency` adds whole system clock cycles to it ([PHYs](#phys)).

The quickest check of a change is an elaboration of a target without vendor tools. It writes the
Verilog and the register map, and fails on a parameter error before any synthesis:

```sh
python3 -m litex_boards.targets.digilent_arty --with-spi-flash --build --no-compile
```

## Where to go next {#integ-next}

[BIOS, boot and flash update](#software) for the software side; [Supported FPGAs and
boards](#boards) for working targets; [PHYs](#phys) and [Memory-mapped reads and writes](#mmap)
for the blocks behind each parameter; [Debugging](#debugging) when the flash does not answer.
