# Performance and resources {#performance}

This appendix gives the clock rates, the bandwidths and the read latencies of LiteSPI, and the
few measurements recorded in public repositories. Each number is labelled: *computed* from the
formulas of the code, *computed in simulation* with the script given here, or *recorded*, quoted
from a public commit with its board. The repository records no throughput, frequency or resource
measurement of its own.

## SCK of the SDR PHY {#perf-sck}

The clock generator of the SDR PHY toggles SCK every `ceil(div / 2)` system cycles, so SCK is
`sys / (2 x ceil(div / 2))`, and `sys / 2` for a divisor of 0 to 2. An odd divisor gives the
same SCK as the next even one. The 1:2 PHY divides by any integer: its SCK is `sys / div`, `sys`
for a divisor of 0 or 1 ([The 1:2 PHY](#phys-ddr)).

| Divisor | SCK at 50 MHz | SCK at 100 MHz |
|-----------------------|--------------------------------------|--------------------------------------|
| 0 to 2 | 25 MHz | 50 MHz |
| 4 | 12.5 MHz | 25 MHz |
| 6 | 8.33 MHz | 16.7 MHz |
| 8 | 6.25 MHz | 12.5 MHz |
| 10 | 5 MHz | 10 MHz |

Computed. `add_spi_flash` sets the divisor to `ceil(sys / clk_freq)`, rounded up to an even value
for the SDR PHY. With the default `clk_freq` of 20 MHz, it gives a divisor of 4 at 50 MHz and of
6 at 100 MHz. The BIOS calibration may then lower it ([BIOS, boot and flash update](#software)).

## Raw bandwidth {#perf-raw}

The data phase moves one bit per line per SCK cycle, so its bandwidth is SCK times the number of
data lines, divided by 8. The table gives it at a 100 MHz system clock; it is the upper bound of
any read, before the command, the address and the dummy cycles.

| PHY and SCK | x1 | x2 | x4 | x8 |
|---------------------------------|-----------------|----------------|----------------|----------------|
| SDR, divisor 4, 25 MHz | 3.1 MB/s | 6.3 MB/s | 12.5 MB/s | 25 MB/s |
| SDR, divisor 2, 50 MHz | 6.3 MB/s | 12.5 MB/s | 25 MB/s | 50 MB/s |
| 1:2, divisor 1, 100 MHz | 12.5 MB/s | 25 MB/s | 50 MB/s | 100 MB/s |

Computed. SCK must also stay under the limit of the chip for the opcode, given in its datasheet;
the slow read (`0x03`) has a lower limit than the fast reads ([SPI memories in a
nutshell](#spi-primer)).

## Cycles per read {#perf-cycles}

The MMAP reads one 32-bit word per bus access and holds CS between consecutive addresses
([Memory-mapped reads and writes](#mmap)). A read therefore costs a full command when it starts a
burst, and only the data phase plus a few cycles of handshake when it continues one. The table
gives both, in system cycles, from a Migen simulation of the test benches.

| Opcode | SDR div 2, first | SDR div 2, next | SDR div 4, first | SDR div 4, next | 1:2 div 1, first | 1:2 div 1, next |
|-----------------------------------|-----------|----------|-----------|----------|-----------|----------|
| `READ_1_1_1` | 138 | 68 | 263 | 131 | 73 | 37 |
| `READ_1_1_1_FAST` | 157 | 68 | 297 | 131 | 85 | 37 |
| `READ_1_1_2` | 125 | 36 | 233 | 67 | 69 | 21 |
| `READ_1_1_4` | 109 | 20 | 201 | 35 | 61 | 13 |
| `READ_1_4_4` | 68 | 20 | 121 | 35 | 41 | 13 |
| `READ_1_1_8` | 101 | 12 | 185 | 19 | 57 | 9 |

Computed in simulation. "First" is the first read after reset, a new command; "next" is the
average of reads 3 to 16 of a burst of 16 back-to-back Wishbone reads, handshake included. The
dummy cycles are those of the module of the test bench: 8 for the fast 1-1-1, 1-1-2, 1-1-4 and
1-1-8 reads, 6 for 1-4-4. The CS delay is 0, against 10 cycles by default; [Cost of a new
command](#perf-command) gives what the default adds.

The same counts give the throughput of a long burst, 4 bytes per word:

| Data lines | SDR div 2, 100 MHz | SDR div 4, 100 MHz | 1:2 div 1, 100 MHz |
|----------------|----------------------------|----------------------------|--------------------------|
| x1 | 5.9 MB/s | 3.1 MB/s | 10.8 MB/s |
| x2 | 11.1 MB/s | 6.0 MB/s | 19.0 MB/s |
| x4 | 20.0 MB/s | 11.4 MB/s | 30.8 MB/s |
| x8 | 33.3 MB/s | 21.1 MB/s | 44.4 MB/s |

Computed in simulation, at a 100 MHz system clock; the value scales with the system clock for a
given divisor. A data word costs 32 bits of data phase plus a fixed overhead of 3 to 4 cycles
with the SDR PHY and of 5 cycles with the 1:2 PHY, which is why the wide modes stay below their
raw bandwidth.

## Cost of a new command {#perf-command}

A read that does not continue a burst pays the command: opcode, address and dummy phases, then CS
high for `cs_delay` cycles before the next command. The difference between the "first" and "next"
columns is that cost with `cs_delay=0`: 70 cycles for a 1-1-1 read at divisor 2, 89 for 1-1-4, 48 for 1-4-4, whose
address goes on four lines. The default `cs_delay` of 10 adds up to 11 cycles when a command
follows another one. A burst ends when the next bus read is not at the next address, when
a write comes, or after 256 system cycles without a read.

Sequential code and data fetched by a CPU cache, a line at a time, mostly stay in bursts. Random
reads of single words pay the command every time: with a 1-1-4 read at divisor 2, about 109
cycles per word, plus the CS delay, instead of 20. A cache in front of the MMAP, the CPU cache or the LiteX L2 cache,
therefore matters more than the width ([Integration in a LiteX SoC](#integration)).

## The measurement script {#perf-script}

The counts above come from this script, which reuses the benches of `test/test_flash_model.py`
(real SDR PHY and flash model) and `test/test_phy_ddr.py` (1:2 PHY with simulated DDR I/O; no
flash model, so only the timing is meaningful). Run from the repository root with
`PYTHONPATH=. python3 read_cycles.py`, it prints the first and next counts of the three PHY
settings for each opcode.

```python
# Cycles per MMAP read: SDR PHY (divisors 2 and 4), 1:2 PHY. Run from the repo root.
from migen import *
from migen.sim import run_simulation
from litex.build.io import SDRTristate, DDROutput, DDRTristate
import test.test_flash_model as tf
import test.test_phy_ddr as td
from litespi import LiteSPI
from litespi.phy.generic import LiteSPIPHY
from litespi.opcodes import SpiNorFlashOpCodes as Codes

def run(dut, n=16, **kwargs):
    cycles, marks = [0], []
    def counter():
        yield "passive"
        while True:
            cycles[0] += 1
            yield
    def reads():
        marks.append(cycles[0])
        for i in range(n):
            yield from dut.spi.bus.read(i)
            marks.append(cycles[0])
    run_simulation(dut, [reads(), counter()], **kwargs)
    return marks[1] - marks[0], (marks[-1] - marks[2])/(n - 2)

def sdr(opcode, divisor):
    phy = tf.LiteSPIPHY
    tf.LiteSPIPHY = lambda **kw: phy(**{**kw, "default_divisor": divisor})
    dut = tf._LiteSPIFlashModelDUT(opcode)
    tf.LiteSPIPHY = phy
    overrides = {}
    if dut.bus is not None:
        tf._SimSDRTristate.bus = dut.bus
        overrides[SDRTristate] = tf._SimSDRTristate
    return run(dut, special_overrides=overrides)

class DDRDUT(Module):
    def __init__(self, opcode):
        self.clock_domains.cd_sys_n = ClockDomain(reset_less=True)
        flash = tf._ModelFlash(opcode)
        if flash.bus_width == 1:
            pads = Record([("clk", 1), ("cs_n", 1), ("mosi", 1), ("miso", 1)])
        else:
            pads = Record([("clk", 1), ("cs_n", 1), ("dq", max(4, flash.bus_width))])
        self.bus = td._DDRBus(max(2, len(pads) - 2))
        self.submodules.phy = LiteSPIPHY(pads=pads, flash=flash, rate="1:2", cs_delay=0)
        self.submodules.spi = LiteSPI(self.phy, with_master=False, with_csr=False)

def ddr(opcode):
    dut = DDRDUT(opcode)
    td._SimDDRTristate.bus = dut.bus
    return run(dut, clocks={"sys": 10, "sys_n": (10, 5)}, special_overrides={
        DDROutput: td._SimDDROutput, DDRTristate: td._SimDDRTristate})

for name in ["READ_1_1_1", "READ_1_1_1_FAST", "READ_1_1_2", "READ_1_1_4", "READ_1_4_4",
             "READ_1_1_8"]:
    opcode = getattr(Codes, name)
    results = [sdr(opcode, 2), sdr(opcode, 4), ddr(opcode)]
    print(f"{name:16s}", "  ".join(f"{f:4d} {s:5.1f}" for f, s in results))
```

Its output on this revision:

```console
READ_1_1_1        138  68.0   263 131.0    80  38.0
READ_1_1_1_FAST   157  68.0   297 131.0    93  38.0
READ_1_1_2        125  36.0   233  67.0    77  22.0
READ_1_1_4        109  20.0   201  35.0    69  14.0
READ_1_4_4         68  20.0   121  35.0    49  14.0
READ_1_1_8        101  12.0   185  19.0    65  10.0
```

## Recorded results {#perf-recorded}

Public commits of LiteX-Boards record a few results on boards. They were taken on earlier
revisions of LiteSPI, LiteX and the BIOS, and they measure the whole system: CPU, bus and flash.
The BIOS `memspeed` test reads 4 KiB from the flash window through the CPU, sequentially and at
random, and prints MiB/s and KiB/s, units of 2^20 and 2^10 bytes per second.

Efinix Trion T20 MIPI Dev Kit, VexRiscv at 100 MHz, W25Q32JV read in 1-1-1 on x1 pads
(LiteX-Boards commit `b6c5a85b`). The BIOS of that time printed the quad enable line even for this
x1 SoC. The calibration was skipped because the first block was erased:

```console
Initializing W25Q32JV SPI Flash @0x00400000...
Enabling Quad mode...
First SPI Flash block erased, unable to perform freq test.
Memspeed at 0x400000 (Sequential, 4.0KiB)...
   Read speed: 2.6MiB/s
Memspeed at 0x400000 (Random, 4.0KiB)...
   Read speed: 1.5MiB/s
```

Tang Nano 4K (Gowin GW1NSR-4C), VexRiscv_Lite at 27 MHz, W25Q32 read in 1-1-1 on x1 pads
(LiteX-Boards commit `376a8365`). 13 MHz is the 27 MHz system clock divided by 2, printed in whole
MHz:

```console
Initializing W25Q32 SPI Flash @0x80000000...
SPI Flash clk configured to 13 MHz
Memspeed at 0x80000000 (Sequential, 4.0KiB)...
   Read speed: 1.3MiB/s
Memspeed at 0x80000000 (Random, 4.0KiB)...
   Read speed: 521.9KiB/s
```

## Resources {#perf-resources}

The only public resource figure comes from the commit that added LiteSPI test code to the
iCEBreaker (iCE40UP5K) target, with execution in place from x1 and x4 flash (LiteX-Boards commit
`0f648ac4`). It compares the whole SoC with the earlier LiteX SPI flash core and with LiteSPI:

```console
Resource usage using SPI(1X) and actual LiteX SPI Flash core:
Info: Device utilisation:
Info: 	         ICESTORM_LC:  2016/ 5280    38%
[...]
Resource usage using LiteSPI:
Info: Device utilisation:
Info: 	         ICESTORM_LC:  3964/ 5280    75%
```

Recorded. The other lines of both reports are identical: 2 block RAMs, 15 I/Os and the 4 SPRAMs.
The commit states that both x1 and x4 execution in place worked, and that the resource usage was
then too high to make LiteSPI the default. The core has changed since; the logic of a design
depends on the device, the toolchain, the modes and the frontends, and a build of the target gives
the figure for a given configuration.
