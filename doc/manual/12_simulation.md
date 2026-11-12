# Simulation and tests {#simulation}

This chapter describes how LiteSPI is checked without a board: the Migen simulations of the test
suite, the pin-level flash model that exercises the real PHY, the elaboration tests of the vendor
primitives, and a complete SoC with its BIOS in Verilator. It is for contributors who change the
core or the database, and for users who want to try a flash configuration before building.

## Verification strategy {#sim-strategy}

A SPI flash controller fails in ways that a stream-level test cannot see: a sample taken one
cycle early, a DQ line driven during the turnaround, a dummy phase one cycle short. The suite
therefore checks each part at the cheapest level that reaches the bug it guards against, and
keeps one level where the real PHY talks to a model of the chip pin by pin.

| Level | What runs | Flash side | Files |
|---------------|-----------------------|-----------------|------------------------------------------|
| Frontend | MMAP and master alone, in Migen | Generator answering the transfers | `test_spi_mmap.py`, `test_spi_master.py` |
| Pin level, SDR | Wishbone reads, and MMAP flash writes, through `LiteSPI` and the real SDR PHY | Pin-level flash model | `test_flash_model.py`, `test_mmap_write.py` |
| Pin level, 1:2 | 1:2 PHY with simulated DDR I/O | Checks on the pins | `test_phy_ddr.py` |
| PHY details | Startup cycles, CS control, vendor clock backends | Checks on the pins | `test_phy_sdr.py`, `test_cscontrol.py`, `test_phy_xilinx.py` |
| Elaboration | Verilog of the 1:2 PHY and of STARTUPE2/E3 for vendor platforms | None | `test_phy_ddr.py`, `test_phy_xilinx.py` |
| Clock domains | MMAP reads with the SDR PHY in a slower or faster clock domain | Pin-level flash model | `test_cs_cdc.py` |
| Database | Module attributes, opcodes, erase geometry, quad enable | None | `test_flash_module.py`, `test_spi_nor_modules.py` |
| System | SoC with a CPU and the BIOS in Verilator | Stream-level PHY model | `litex_sim`, not in CI |
| Hardware | A board | The flash chip | Not in CI |

The elaboration level runs the LiteX lowering of each vendor platform to Verilog without the vendor
tools: it proves that the expected primitives are instantiated and connected, not that their
timing is met. The status of each PHY path on hardware is in [the introduction](#intro-status).

## Running the tests {#sim-run}

The tests are Python `unittest` classes in `test/`, collected by pytest. They need Migen and
LiteX, and no simulator besides the Migen one.

```sh
# Whole suite, as the CI runs it
python3 -m pytest -v
# Same, in parallel on every CPU core (needs pytest-xdist)
python3 -m pytest -v -n auto
# One file, or one test
python3 -m pytest -v test/test_flash_model.py
python3 -m pytest -v test/test_spi_mmap.py -k little_endian
```

The suite collects 74 tests; many loop over opcodes, widths or idle times as subtests. The end
of a run of `python3 -m pytest -q` from the repository root reads:

```console
74 passed, 754 subtests passed in 46.22s
```

## The pin-level flash model {#sim-flash-model}

`LiteSPINORFlashModel` (`litespi/flash_model.py`) is a Migen model of a SPI NOR flash seen from
its pins. It decodes the read command of the module given to it, shifts the address in, waits
the dummy cycles and shifts the data out, so that the real PHY, its clock generator and its
sampling delay are exercised exactly as on a board.

| Feature | Model behaviour |
|-------------------------|-------------------------------------------------------------|
| Commands | The read opcode of the module (`flash.read_opcode`); other opcodes are ignored |
| Programming | With `with_program=True` (x1 commands, up to 64 KiB): WREN/WRDI set and clear WEL, the program opcode of the module programs (bits only cleared) when WEL is set, then WIP for `program_cycles` model cycles; RDSR returns WIP and WEL; other commands are ignored while busy |
| Phases | Command, address and data on 1, 2, 4 or 8 lines, SDR only |
| Address | 24 or 32 bits, from the opcode name (`_4B`) |
| Dummy | `dummy_cycles` of the module for a fast read |
| Burst | Continuous read while CS stays low, the address incrementing |
| Contents | `init`, a list of bytes from address 0; other addresses read `0xff`, as an erased flash |
| Pads | `clk`, `cs_n`, and `mosi`/`miso` or `dq`; or split `dq_i`, `dq_o`, `dq_oe` |
| Rejected | DTR opcodes, several chip selects, widths that do not divide the phases |

The figure below shows the bench of `test_flash_model.py`. A generator issues Wishbone reads on the
MMAP of a `LiteSPI` core; the real SDR PHY drives the pins; the DQ lines are split into a
controller side and a flash side, so that the Migen simulator never has to resolve a shared
signal.

![Pin-level read test. Wishbone reads go through the MMAP and the real SDR PHY; the split DQ lines
(x2 and wider) connect the PHY to the flash model, which reads its contents from a byte memory, and
feed the bus monitor. In x1 the model uses the MOSI and MISO pads directly.](sim_model.svg)

The split lines also give the test a bus monitor: a process checks at every cycle that the
controller and the flash never enable their drivers on the same line. A turnaround error
therefore fails the test even when the data happen to be right.

`test_reads_through_real_phy` runs four reads for ten read opcodes, from 1-1-1 to 1-8-8,
including a 4-byte address read and the QPI read 4-4-4. The memory holds the bytes 0 to 127, so
the expected words are fixed: word 0 reads `0x00010203`, word 1 continues the burst with
`0x04050607`, word 16 starts a new command at `0x40414243`, and word 40, beyond the initialized bytes, reads `0xffffffff`.

## The 1:2 PHY and the vendor primitives {#sim-ddr-vendor}

The 1:2 PHY drives SCK and the data through DDR I/O primitives that Migen cannot simulate. The
tests of `test_phy_ddr.py` replace them with small Migen models (`_SimDDROutput`,
`_SimDDRTristate`, passed as `special_overrides`) that register the two edges as the vendor
primitives do, with an optional input latency. The tests then check the output data on each SCK
edge, the input sampling with `extra_latency`, and the turnaround between the address and the
read data.

The same file elaborates the 1:2 PHY for two vendor platforms and looks for the primitives in the
Verilog: `ODDRX1` and `IDDRX1` on a CrossLink-NX, `ODDR` and `IDDR` on an Artix-7.
`test_phy_xilinx.py` does the same for the configuration clock paths: one STARTUPE2 with
`USRCCLKO` connected for a 7-Series device, one STARTUPE3 with its clock, chip select and four
data ports for an UltraScale+ device. In the Migen simulations of these paths, the vendor
instances are replaced by an empty module (`_IgnoreInstance`) and the tests check the transfers
and the startup cycles on the PHY side.

## A SoC with the BIOS: litex_sim {#sim-litex-sim}

`litex_sim` builds a LiteX SoC with a CPU and simulates it in Verilator. With `--with-spi-flash`
it adds a flash region through `SoC.add_spi_flash`, with an S25FL128L module in 1-1-4 mode and the
master, and the BIOS initializes it at boot. This is the quickest way to see the BIOS side of
LiteSPI ([BIOS, boot and flash update](#software)) without a board.

The PHY of this SoC is `LiteSPIPHYModel` (`litespi/phy/model.py`), not the real PHY: a
stream-level model that answers the transfers of the core directly from a memory. It returns the
data of the read opcode of the module and zeros for every other command, after a delay that
depends on the length of each transfer but not on a divisor. It has no divisor register. The
option `--spi_flash-init` loads a binary image into its memory.

```sh
# VexRiscv SoC at 1 MHz with a 16 MiB flash region, BIOS console in the terminal
litex_sim --with-spi-flash
# Same, with an image in the flash
litex_sim --with-spi-flash --spi_flash-init=image.bin
```

The boot log below comes from the first command, run in a scratch directory with
`--output-dir build`, with LiteX and this revision of LiteSPI. It is trimmed to the SoC and
initialization sections, without the colour codes of the terminal:

```console
--================ SoC =================--
CPU:		VexRiscv @ 1MHz
BUS:		wishbone 32-bit data/32-bit addr
CSR:		32-bit data big ordering
ROM:		128.0KiB
SRAM:		8.0KiB
FLASH:		16.0MiB

--=========== Initialization ===========--

Initializing s25fl128l SPI Flash @0x01000000...
Enabling Quad mode...
SPI Flash clk configured to 500 kHz
Memspeed at 0x1000000 (Sequential, 4.0KiB)...
   Read speed: 236.6KiB/s
Memspeed at 0x1000000 (Random, 4.0KiB)...
   Read speed: 76.2KiB/s
[...]
litex>
```

Each line reflects the model, not a chip. The quad enable runs the generic sequence of the BIOS,
since the S25FL128L module names no quad enable method, and the model reports a ready status. The
clock line prints `SPIFLASH_PHY_FREQUENCY`, 500 kHz at a 1 MHz system clock (in kHz, below
1 MHz), because the model has no divisor register to calibrate. The read speeds measure the CPU, the bus and the
fixed latency of the model, and say nothing about a real flash; [Performance and
resources](#performance) gives the cycle counts of the real PHYs.

## Writing a test {#sim-write}

A new read mode or a change to the PHY is tested at the pin level. The bench of
`test_flash_model.py` takes the opcode as its only parameter: add the opcode to the
`supported_opcodes` and, for a fast read, to the `dummy_cycles` of the `_ModelFlash` class of the
test, then to the list of `test_reads_through_real_phy`. The four reads, the expected words and
the bus monitor apply unchanged.

A new module in the database needs no simulation of its own: the PHY does not depend on the chip
beyond the opcode, the widths and the dummy cycles. `test_spi_nor_modules.py` checks the
attributes of every class and counts them; a new class therefore also updates the count asserted
by `test_module_inventory`, 481 on this revision. The checklist for a new chip is in [The SPI
memory database](#modules).

A change to the MMAP is tested at the frontend level, as in `test_spi_mmap.py`: the test records
the transfers that the MMAP emits (data, length, width, mask) and answers each with a data word,
then compares the sequence with the phases expected for the opcode.

## Continuous integration {#sim-ci}

The workflow `.github/workflows/ci.yml` runs on every push and pull request, on Ubuntu 22.04
with Python 3.9. It installs LiteX and its cores with `litex_setup.py`, installs LiteSPI, checks
that the register appendix of this manual matches the gateware ([Register
reference](#registers)), then runs `python3 -m pytest -v`. It runs neither Verilator nor a vendor
toolchain.

A second workflow, `.github/workflows/doc.yml`, checks the figures and the sources of this manual
and publishes it every night when `master` has changed ([Maintaining this manual](#maintenance)).
For a check on a real target before a pull request, `AGENTS.md` adds the elaboration of a
LiteX-Boards target: it generates the Verilog, the headers and the `csr.csv` without compiling the
BIOS or running the vendor tools:

```sh
python3 -m litex_boards.targets.digilent_arty --with-spi-flash --build --no-compile
```

## Where to go next {#sim-next}

[Debugging](#debugging) uses the same tools to narrow down a problem seen on a board;
[Performance and resources](#performance) gives the cycle counts measured with the benches of
this chapter.
