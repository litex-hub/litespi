# PHYs {#phys}

The PHY is the only part of LiteSPI that touches the pins: it generates SCK, shifts the bits of
each transfer on the DQ lines and drives CS. This chapter describes the SDR PHY and its divider,
the 1:2 PHY, the vendor backends for configuration flash pins and the notes per FPGA family. See
[The transfer contract](#arch-transfer) for the transfer.

## At a glance {#phys-glance}

| PHY | Class | SCK | Lines | Flash clock |
|-------------------------|---------------------------------|---------------|---------|------------|
| SDR, any family | `LiteSPISDRPHYCore` | PHY clock / divisor | 1 to 8 | SCK pin |
| SDR + STARTUPE2, 7-Series | `LiteSPISDRPHYCore` | PHY clock / divisor | 1 to 8 | CCLK pin |
| SDR + USRMCLK, ECP5 | `LiteSPISDRPHYCore` | PHY clock / divisor | 1 to 8 | MCLK pin |
| SDR + STARTUPE3, UltraScale | `LiteSPIXilinxUSPHY` | PHY clock / divisor | 1 or 4 | CCLK pin |
| 1:2, families with DDR I/O | `LiteSPIDDRPHYCore` | PHY clock / divisor | 1 to 8 | SCK pin |

Designs instantiate `LiteSPIPHY`, which builds the SDR PHY for `rate="1:1"` and the 1:2 PHY for
`rate="1:2"`; the UltraScale PHY is its own class. Which paths are validated on hardware is stated
once, in the [status table](#intro-status) of the introduction.

Both PHYs work in SPI mode 0, the SDR PHY also in mode 3, and both transfer one bit per line per
SCK cycle. They refuse a module whose read opcode is a DTR opcode (`flash.ddr`). The "1:2" of the
second PHY is the rate of the FPGA I/O registers, not a double rate on the flash side.

Both also check that the pads offer at least the data width of the module read mode
(`check_bus_width`). A pad set has either two single lines `mosi` and `miso` (x1) or a `dq` vector
of 1, 2, 4 or 8 lines.

## The SDR PHY {#phys-sdr}

The SDR PHY divides the clock of its domain to make SCK and moves one bit per line per SCK cycle.
It runs on every family, since it only needs the single-rate I/O registers that LiteX provides
everywhere (`SDROutput`, `SDRInput`, `SDRTristate`). It is the PHY that `add_spi_flash` builds by
default.

### Datapath {#phys-sdr-datapath}

The PHY loads each transfer into an output shift register and shifts it out MSB first, `width` bits
per SCK cycle. In parallel, an input shift register collects `width` bits per SCK cycle from the DQ
lines. The clock generator gives both the strobes. The figure below shows the datapath.

![SDR PHY datapath: the output shift register drives the DQ lines through SDRTristate and the
input shift register collects them; the clock generator drives SCK through SDROutput and times the
shift and sample strobes; CS control drives CS.](phy_sdr.svg)

A state machine sequences one transfer in four states:

| State | Action |
|-------------------------|-------------------------------------------------------------------|
| `WAIT-CMD-DATA` | Wait for CS and a transfer; load it, set the output enables from `mask` |
| `XFER` | Run SCK; shift out on falling edges, shift in on sampled rising edges |
| `XFER-END` | SCK stopped; take the last sampled bits |
| `SEND-STATUS-DATA` | Return the input word, release the DQ outputs |

The PHY accepts the transfer as soon as it loads it, so the frontend can prepare the next one
during the shifts. When every line of the transfer is an output (width 2, 4 or 8 with a full mask),
the PHY returns its word without waiting for the last sample.

For x1, the PHY drives DQ0 and reads DQ1, as a single-line SPI controller drives MOSI and reads
MISO. With `mosi` and `miso` pads, the PHY uses one output register and one input register and no
tristate, and MOSI is always driven, whatever the mask.

Most x1 pad sets of LiteX-Boards are of this kind, including those of the Efinix Trion kits.

### The clock divider {#phys-divider}

The clock generator toggles SCK every `ceil(divisor / 2)` cycles of the PHY clock (`LiteSPIClkGen`).
SCK is therefore the PHY clock divided by the divisor rounded up to the next even number:

```text
SCK = f_PHY / (2 * ceil(divisor / 2)),   divisor >= 1
SCK = f_PHY / 2,                         divisor = 0
```

The divisor is 10 bits wide. Divisors go in pairs: 1 and 2 give half the PHY clock, 3 and 4 a
quarter, 5 and 6 a sixth. The table gives SCK for common divisors, computed from the
formula.

| Divisor | SCK at 50 MHz | SCK at 100 MHz |
|---------|---------------|----------------|
| 2 | 25 MHz | 50 MHz |
| 4 | 12.5 MHz | 25 MHz |
| 6 | 8.33 MHz | 16.67 MHz |
| 8 | 6.25 MHz | 12.5 MHz |
| 10 | 5 MHz | 10 MHz |

The divisor comes from the PHY register `clk_divisor`, reset to the `default_divisor` parameter (9
in the class). A transfer with a non-zero `clk_div` field uses that value instead
([The frontends](#arch-frontends)). The PHY reads the divisor between transfers, so a change never
cuts an SCK cycle.

`add_spi_flash` computes the default divisor from its `clk_freq` argument: the system clock divided
by `clk_freq`, rounded up, then up to an even number. With the default 20 MHz, a 50 MHz system
clock gives divisor 4 (12.5 MHz) and a 100 MHz system clock divisor 6 (16.67 MHz).

At boot, the BIOS lowers the divisor while the flash reads back the same data
([BIOS, boot and flash update](#software)).

Every divisor up to 1023, the largest value of the 10-bit field, follows the formula: the half
period counter of the clock generator is as wide as the divisor.

### Sampling and extra latency {#phys-sdr-sampling}

The PHY changes DQ with each falling edge of SCK and reads DQ with each rising edge. The flash does
the reverse: it samples on rising edges and changes its outputs after falling edges. The figure
below shows both edges at divisors 2 and 4.

![SDR PHY timing in mode 0 at divisors 2 and 4, at the pins: SCK is the PHY clock divided by
the divisor, DQ changes on the falling edges of SCK and is sampled on its rising edges (dotted
lines).](phy_sdr_timing.svg)

SCK and DQ leave the FPGA through output registers, and DQ comes back through an input register.
The clock generator delays the sample strobe by 2 cycles of the PHY clock to match these
registers. The PHY then keeps the value that the input register captured at the cycle SCK rose
at the pin.

The `extra_latency` parameter adds whole cycles to this delay, for boards or I/O paths where the
data of the flash arrives later. The SDR PHY truncates it to an integer (`int(extra_latency)`), so
0.5 behaves as 0. Each unit moves the sample point one cycle of the PHY clock later.

### SPI modes {#phys-sdr-modes}

The `mode` register selects the SPI mode, 0 (reset value) or 3. The PHY uses only its bit 1, the
clock polarity: it sets the level of SCK between transfers, low in mode 0 and high in mode 3. At the
start of a transfer SCK goes low in both modes, and the shift and sample edges are the same.

Modes 1 and 2 are not supported, and SPI memories do not use them ([SPI memories in a
nutshell](#spi-primer)).

### Registers {#phys-sdr-registers}

| Register | Width | Reset | Content |
|------------------------|-------|-------------------------|------------------------------|
| `phy_clk_divisor` | 10 | `default_divisor` | SCK divisor |
| `phy_mode` | 2 | 0 | SPI mode, 0 or 3 |

LiteX prefixes them with the name of the flash, `spiflash_` by default. Their addresses and field
descriptions are in the [Register reference](#registers). Both cross into the PHY domain through
`MultiReg` when the PHY has its own clock ([Clock domains](#arch-cdc)).

## The 1:2 PHY {#phys-ddr}

The 1:2 PHY drives SCK and DQ through DDR output registers and reads DQ through DDR input
registers, two half cycles per clock. SCK is the clock of its domain divided by any integer: at a
100 MHz system clock, a divisor of 1 gives 100 MHz, twice the fastest SCK of the SDR PHY.

### Divisor {#phys-ddr-divisor}

The clock generator counts SCK half periods in half cycles of the PHY clock (`DDRLiteSPIClkGen`).
Each half period lasts `divisor` half cycles, so SCK keeps a 50 % duty cycle for odd divisors too:

```text
SCK = f_PHY / divisor,   divisor >= 1
SCK = f_PHY,             divisor = 0
```

The divisor comes from the `clk_divisor` register of the PHY, or from the `clk_div` field of a
transfer when it is not 0, as on the SDR PHY. The PHY latches it when a transfer starts. Its reset
value is the `default_divisor` that `add_spi_flash` computes from `clk_freq`.

| Divisor | SCK at 50 MHz | SCK at 100 MHz |
|---------|---------------|----------------|
| 0 or 1 | 50 MHz | 100 MHz |
| 2 | 25 MHz | 50 MHz |
| 3 | 16.7 MHz | 33.3 MHz |
| 5 | 10 MHz | 20 MHz |

### Datapath and lanes {#phys-ddr-lanes}

SCK is a DDR output: lane 0 gives its level in the first half of a PHY clock cycle, lane 1 in the
second half. Its rising edges always fall on the rising edges of the PHY clock, at the start of
lane 0. Its falling edges fall between the two lanes for odd divisors and at the start of lane 0
for even ones.

The data uses the two lanes of a DDR tristate (`DDRTristate`). The PHY changes the bit on the lane
of each falling edge of SCK and holds it until the next one, so the bit is stable around the rising
edge, where the flash samples it. The figure below shows divisor 1.

![1:2 PHY lanes in mode 0 at divisor 1: SCK is the clock gated by the transfer; lane 1 carries each
new bit in the second half of a cycle and lane 0 repeats it in the first half of the next one, so
each bit at the pin is centred on a rising edge of SCK (dotted lines).](phy_ddr_lanes.svg)

The output enable uses a single lane: the direction of a line does not change within an SCK
period. For x1, the PHY drives MOSI and reads MISO through the same DDR tristate.

On the input side, the PHY takes the first-half lane (`i1`) of each line once per SCK rising edge,
`2 + 2 * extra_latency` PHY clock cycles after it, the delay of the DDR input register and the
fabric pipeline. It shifts in exactly `len` bits and clears the word when the transfer starts.

The PHY accepts a transfer when it starts and latches its width and mask. A transfer that only
drives its lines returns without waiting for the input pipeline.

### What the 1:2 PHY does not have {#phys-ddr-limits}

| Feature | SDR PHY | 1:2 PHY |
|---------------------------|------------------------|------------------------------------|
| SCK divisor | `clk_divisor`, `clk_div`; even values | `clk_divisor`, `clk_div`; any value |
| Registers | `clk_divisor`, `mode` | `clk_divisor` |
| SPI mode 3 | Yes | No: SCK idles low |
| Clock backends | STARTUPE2, USRMCLK | None: needs a `clk` pad |
| `extra_latency` | Integer part | Steps of 0.5 |

Each 0.5 of `extra_latency` delays the input sampling by one PHY clock cycle. Other values raise a
`ValueError` at elaboration.

### The reported frequency {#phys-ddr-frequency}

`add_spi_flash` computes the divisor as `ceil(sys_clk_freq / clk_freq)`, without the rounding to
an even value of the SDR PHY. The PHY uses it as the reset value of its divisor, and the frequency
constant `SPIFLASH_PHY_FREQUENCY` is the system clock divided by it, so the constant is the SCK of
the PHY. The minimum divisor constant is 1.

On the Arty A7 target (100 MHz system clock, `add_spi_flash` default `clk_freq` of 20 MHz), the
divisor is 5 and SCK runs at 20 MHz. The BIOS calibration may then lower the divisor one step at a
time ([BIOS, boot and flash update](#software)).

## Vendor clock and I/O backends {#phys-backends}

On some boards the flash is the configuration flash of the FPGA, wired to dedicated configuration
pins. The fabric cannot drive these pins directly; a vendor primitive hands them over after
configuration. The SDR PHY reaches them through a backend that replaces the clock pad, or the
whole pad set on UltraScale.

### Clock-only backends {#phys-clock-backends}

When the pads have no `clk` signal, the SDR PHY picks a clock backend from the device name. The
figure below shows the three clock paths.

![SDR PHY clock paths: a regular SCK pin through SDROutput, or, for pads without a clk signal, one
register and the STARTUPE2 primitive on 7-Series (xc7 devices) or the USRMCLK primitive on ECP5
(LFE5U devices).](phy_backends.svg)

| Device name | Backend | Primitive input | Startup cycles |
|--------------|---------------------------|--------------------------|----------------|
| `xc7*` | `LiteSPISTARTUPE2` | `USRCCLKO` of STARTUPE2 | 3 |
| `LFE5U*` | `LiteSPIECP5USRMCLK` | `USRMCLKI` of USRMCLK | 0 |
| Other | None: elaboration error | | |

Any other device raises `NotImplementedError` at elaboration.

The backend registers SCK once before the primitive. This register takes the place of the
`SDROutput` of a regular pin, so SCK keeps the same delay against DQ and the sampling of
[Sampling and extra latency](#phys-sdr-sampling) holds unchanged. The CS and DQ lines stay on
regular pads.

`LiteSPIPHY` defaults its `device` argument to `"xc7"`. A design that instantiates the PHY directly
with pads without `clk` therefore gets the STARTUPE2 backend unless it names its device;
`add_spi_flash` passes the device of the platform.

### STARTUPE2 on 7-Series {#phys-startupe2}

On 7-Series FPGAs, the flash clock is the CCLK pin, and user logic reaches it through the
`USRCCLKO` input of STARTUPE2. The primitive needs clock edges on `USRCCLKO` before the pin follows
the user clock. The backend declares three startup cycles for this hand-over.

After reset, the clock generator runs SCK on its own for these three rising edges. The PHY keeps CS
high until they have passed, and only then accepts a transfer. This prevents the first command from
starting with an SCK of uncontrolled phase.

The backend ties the other inputs of STARTUPE2 to constants: `USRCCLKTS` low (clock output
enabled), `USRDONEO` and `USRDONETS` high. Some 7-Series boards also wire the flash clock to a user
pin; their platform then gives a `clk` pad and the regular path applies, as on the Arty A7.

### USRMCLK on ECP5 {#phys-usrmclk}

On ECP5 FPGAs, the flash clock is the MCLK pin, reached through the USRMCLK primitive. The backend
drives `USRMCLKI` with SCK and `USRMCLKTS` with the reset of the PHY domain. The pin is tri-stated
during reset and driven after it. Lattice Diamond also requires `USRMCLKTS` to be a signal rather
than a constant. This backend has no startup cycles.

### STARTUPE3 on UltraScale and UltraScale+ {#phys-startupe3}

On UltraScale and UltraScale+ FPGAs, the clock, the chip select and the four data lines of the
configuration flash all go through STARTUPE3. `LiteSPIXilinxUSPHY` is an SDR PHY whose pads are
the virtual pads of the `LiteSPISTARTUPE3` backend. The figure below shows its structure.

![UltraScale PHY: the SDR PHY core drives SCK and CS through its own output registers and the four
DQ lines through the registers of LiteSPISTARTUPE3, all of them reaching the configuration flash
through STARTUPE3.](phy_us.svg)

| STARTUPE3 port | Driven by |
|----------------|--------------------------------------------------------|
| `USRCCLKO` | SCK |
| `FCSBO` | CS (`cs_n`), reset to 1 |
| `DO` | DQ outputs, registered |
| `DTS` | Inverted output enables, registered, reset to all ones |
| `DI` | DQ inputs, registered |

The backend registers the data in both directions, as the `SDRTristate` of a regular pad would, and
inverts the output enable: STARTUPE3 takes an active-high tristate (`DTS`). It declares three
startup cycles, used as for STARTUPE2.

The class takes the module, an optional clock domain and the keyword arguments of the SDR PHY. It
requests no platform pads and is passed to `add_spi_flash` through `phy`. The XCKU3P board target
uses it as follows (`alibaba_xcku3p.py`).

```python
spiflash_module  = MT25QU256(Codes.READ_1_1_1_FAST_4B, program_cmd=Codes.PP_1_1_1_4B)
spiflash_divisor = math.ceil(sys_clk_freq/20e6)
spiflash_divisor += spiflash_divisor % 2
self.add_spi_flash(mode="1x",
    module      = spiflash_module,
    phy         = LiteSPIXilinxUSPHY(spiflash_module, default_divisor=spiflash_divisor),
    with_master = True)
```

With `phy` given, `add_spi_flash` does not pass its divisor to the PHY, so the target computes
`default_divisor` itself. The data width is always 4 lines; x1 modules read on DQ1 as with any
pad set. The XCKU5P board target uses the same class with a 1-1-4 module.

## Per-family notes {#phys-families}

The SDR PHY reaches every family through the LiteX lowering of `SDROutput`, `SDRInput` and
`SDRTristate`. The 1:2 PHY needs `DDROutput` and `DDRInput` on the family; its elaboration is tested
on CrossLink-NX and Artix-7 ([Simulation and tests](#simulation)). The full list of targets is in
[Supported FPGAs and boards](#boards).

The table gives the clock path of each family and example targets. Most 7-Series and all ECP5
targets reach the flash through the configuration clock pin, with the clock backend.

| Family | Clock path | PHY used by targets | Example boards |
|---------------------------|---------------------|---------------------|---------------------------|
| Xilinx 7-Series, SCK pin | Regular pad | SDR, 1:2 on Arty A7 | Arty A7, Cmod A7 |
| Xilinx 7-Series, CCLK only | STARTUPE2 | SDR | KC705, AC701, Nexys4DDR |
| Xilinx UltraScale+ | STARTUPE3 | UltraScale PHY | XCKU3P, XCKU5P boards |
| Lattice ECP5 | USRMCLK | SDR | ULX3S, ButterStick, Acorn |
| Lattice iCE40 | Regular pad | SDR | iCEBreaker, Fomu |
| Lattice Nexus | Regular pad | SDR | CrossLink-NX EVN |
| Gowin GW1N, GW2A, GW5A | Regular pad | SDR | Tang Nano 9K, Tang Console |
| Efinix Trion | Regular pad | SDR | T8, T20 and T120 kits |
| Efinix Titanium | Regular pad | 1:2 by default | Ti375 C529 kit |
| Cologne Chip GateMate | Regular pad | SDR | GateMate EVB |
| Altera MAX 10 | Regular pad | SDR | MAX 10 board (`trenz_cr00010`) |

On iCE40, the targets drive the configuration flash through regular pads once the FPGA has
configured, and several of them run the BIOS in place from it ([Integration in a LiteX
SoC](#integration)). On the CrossLink-NX EVN and Certus-NX Versa targets, the module reads in QPI
(4-4-4); the QPI command width is a matter of the MMAP, not of the PHY.

## Limitations {#phys-limitations}

- No DTR: both PHYs refuse DTR opcodes, and no PHY clocks data on both SCK edges at the flash.
- No data strobe input and no per-line input delay or calibration: the only timing knobs are the
  divisor and `extra_latency`, in whole cycles of the PHY clock (steps of 0.5 on the 1:2 PHY).
- SPI modes 0 and 3 only on the SDR PHY, mode 0 only on the 1:2 PHY.
- The 1:2 PHY has no mode register and no clock backend: it needs a `clk` pad and keeps SCK low
  between transfers.
- The STARTUPE3 path always has four data lines and no x8.
- `add_spi_flash` requests only `spiflash` (x1) or `spiflash4x` pads; x2 and x8 pad sets need a
  direct instantiation of the PHY.

## In the code {#phys-code}

| Function | File | Classes |
|----------------|------------------------------------------|----------------------------------|
| PHY selection | `litespi/phy/generic.py` | `LiteSPIPHY`, `LiteSPIXilinxUSPHY` |
| SDR PHY | `litespi/phy/generic_sdr.py` | `LiteSPISDRPHYCore` |
| 1:2 PHY | `litespi/phy/generic_ddr.py` | `LiteSPIDDRPHYCore` |
| Clock generators | `litespi/clkgen.py` | `LiteSPIClkGen`, `DDRLiteSPIClkGen` |
| Xilinx backends | `litespi/phy/xilinx.py` | `LiteSPISTARTUPE2`, `LiteSPISTARTUPE3` |
| ECP5 backend | `litespi/phy/lattice.py` | `LiteSPIECP5USRMCLK` |
| CS control | `litespi/cscontrol.py` | `LiteSPICSControl` |

The PHY tests are `test/test_phy_sdr.py` (startup cycles, backend selection),
`test/test_phy_ddr.py` (pin-level edges, extra latency, turnaround, elaboration) and
`test/test_phy_xilinx.py` (STARTUPE2 and STARTUPE3 ports and phases). The divisor and the reported
frequency are computed in LiteX (`add_spi_flash` in `litex/soc/integration/soc.py`).

Where to go next: [Memory-mapped reads and writes](#mmap) for the transfers the MMAP sends,
[Debugging](#debugging) for sampling problems, [Performance](#performance) for the throughput of
each PHY.
