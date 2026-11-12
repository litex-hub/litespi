# Build options {#build-options}

This appendix lists the parameters of every part of LiteSPI, of the LiteX methods that add it to
a SoC, of the generator and of the simulation, and the BIOS constants that change its behaviour.
The chapters explain when to use them; this appendix gives their names and defaults.

## SoC methods {#opt-soc}

`SoC.add_spi_flash()` and `SoC.add_spi_ram()` (LiteX, `soc/integration/soc.py`) build the PHY and
the core, map the memory region and add the constants of the BIOS
([Integration in a LiteX SoC](#integration)).

| Parameter | Default | Meaning |
|--------------------------|-------------------|-----------------------------------------------------|
| `name` | `"spiflash"` | Name of the core, its region, its register bank and its constants; `"spiram"` for `add_spi_ram` |
| `mode` | `"4x"` | `"1x"` requests the pads `name`, `"4x"` the pads `name` + `4x` |
| `clk_freq` | `20e6` | Requested SCK in Hz; sets the divisor `ceil(sys / clk_freq)`, rounded up to even with the SDR PHY |
| `module` | `None` | Module instance, such as `W25Q128JV(Codes.READ_1_1_4)`; required for the memory region |
| `phy` | `None` | A PHY built by the caller, such as `LiteSPIXilinxUSPHY`; the pads are then not requested |
| `rate` | `"1:1"` | `"1:1"` for the SDR PHY, `"1:2"` for the 1:2 PHY |
| `software_debug` | `False` | Adds the `SPIFLASH_DEBUG` constant (`<NAME>_DEBUG`) |
| `number` | `None` | Index of the pads in the platform, for a second flash |
| `**kwargs` | | Passed to both `LiteSPIPHY` and `LiteSPI` (tables below) |

`add_spi_ram` takes the same parameters, always enables MMAP writes and adds a Wishbone L2 cache in
front of the core:

| Parameter | Default | Meaning |
|---------------------------------------------|--------------|----------------------------------------|
| `l2_cache_size` | `8192` | Cache size in bytes, rounded to a power of two; 0 connects the bus without a cache |
| `l2_cache_reverse` | `False` | `reverse` of the LiteX `wishbone.Cache` |
| `l2_cache_full_memory_we` | `True` | Wraps the cache with `FullMemoryWE` |

`add_spi_flash` sets `master_with_irq=True` when the CPU has an interrupt named after the core.

## Core {#opt-core}

`LiteSPI` (`litespi/__init__.py`) holds the crossbar, the MMAP and the master.

| Parameter | Default | Meaning |
|---------------------------------------|--------------|---------------------------------------------|
| `phy` | required | The PHY; its `cs` width sets the number of chip selects |
| `clock_domain` | `"sys"` | Domain of the PHY; another domain adds two asynchronous FIFOs of 32 entries |
| `with_mmap` | `True` | Adds the MMAP, when the PHY carries a module (`phy.flash`) |
| `mmap_endianness` | `"big"` | `"little"` reverses the bytes of each word; `add_spi_flash` passes the CPU endianness; MMAP writes with `"big"` are byte-reversed ([Known issues](#debug-known)) |
| `with_master` | `True` | Adds the master |
| `master_tx_fifo_depth` | `1` | Depth of the TX FIFO of the master |
| `master_rx_fifo_depth` | `1` | Depth of the RX FIFO of the master |
| `master_with_irq` | `False` | Adds the `rx_ready` event and its interrupt |
| `with_csr` | `True` | Adds the `mmap_dummy_bits` register; otherwise the dummy phase is fixed |
| `with_mmap_write` | `False` | `True` enables MMAP writes (SPI RAM); `"csr"` adds `mmap_write_config` to enable them at run time (flash) |
| `mmap_cs_mask` | `1` | Chip selects driven by the MMAP, one bit per line |

## PHYs {#opt-phy}

`LiteSPIPHY(pads, flash, device="xc7", clock_domain="sys", rate="1:1", **kwargs)`
(`litespi/phy/generic.py`) builds the SDR PHY or the 1:2 PHY and passes the other parameters to
it ([PHYs](#phys)). `device` selects the clock backend of the SDR PHY when the pads have no
`clk`: STARTUPE2 for `xc7*`, USRMCLK for `LFE5U*`; `add_spi_flash` passes the device of the
platform.

| Parameter | PHY | Default | Meaning |
|------------------------------|---------|-------------|----------------------------------------------|
| `default_divisor` | SDR | `9` | Reset value of `phy_clk_divisor`; `add_spi_flash` computes it from `clk_freq` |
| `extra_latency` | SDR, 1:2 | `0` | Extra sampling delay in PHY clock cycles (SDR: `int()` of the value; 1:2: two pipeline stages per unit, integers only, 0.5 fails at elaboration) |
| `cs_delay` | SDR, 1:2 | `10` | System cycles with CS high between two commands to the same chip |
| `with_sdr_cs` | SDR, 1:2 | `True` | Registers `cs_n` in an I/O register (`SDROutput`) |
| `io` | SDR | `None` | Full I/O backend (`LiteSPISTARTUPE3`); exclusive with `clk_io` |
| `clk_io` | SDR | `None` | Clock-only backend, chosen from `device` when the pads have no `clk` |

`LiteSPIXilinxUSPHY(flash, clock_domain="sys", **kwargs)` is the SDR PHY of the UltraScale+
configuration flash: it creates its STARTUPE3 backend and takes the SDR parameters above. It is
passed to `add_spi_flash` through `phy`.

The pads are `clk`, `cs_n` and either `mosi` and `miso` (x1) or `dq` of 2, 4 or 8 lines. `cs_n`
can be wider than one line: each line is a chip select.

## Frontends {#opt-frontends}

`LiteSPI` builds its frontends from its own parameters; the classes can also be used alone.

| Class | Parameters (defaults) |
|------------------------------------|---------------------------------------------------------------|
| `LiteSPIMMAP` | `flash`, `clock_domain="sys"`, `endianness="big"`, `with_csr=True`, `with_write=False`, `cs_width=1`, `cs_mask=1` |
| `LiteSPIMaster` | `cs_width=1`, `tx_fifo_depth=1`, `rx_fifo_depth=1`, `with_irq=False` |
| `LiteSPICSControl` | `pads`, `cs`, `cs_delay=10`, `with_sdr_cs=True` |
| `LiteSPICrossbar` | `cd`, `cs_width=1` |

The registers that these parameters add or remove are listed in [Register
reference](#registers).

## Module instance {#opt-module}

A module class of the database is instantiated with the read command, which sets the widths, the
address size and the dummy phase ([The SPI memory database](#modules)).

| Parameter | Default | Meaning |
|----------------------------------|-------------------|---------------------------------------------|
| `default_read_cmd` | required | Read opcode used by the MMAP, such as `Codes.READ_1_1_4` |
| `read_cmds` | `None` | Other read opcodes accepted by the module |
| `program_cmd` | `PP_1_1_1` | Program opcode used by MMAP writes |
| `erase_cmd` | `None` | Erase opcode chosen among the erase commands |
| `erase_commands` | `None` | Erase geometry, overriding the class attribute |

## Standalone generator {#opt-gen}

`litespi_gen` (`litespi/gen.py`) writes a Verilog core with a Wishbone or AXI-Lite bus for a
non-LiteX design, in `build/gateware/` of the working directory.

| Option | Default | Meaning |
|----------------------------------|--------------------|--------------------------------------------|
| `--module` | `S25FL128L` | Module class name; an unknown name lists the database |
| `--mode` | `x1` | `x1` (READ_1_1_1) or `x4` (READ_1_1_4); the `_4B` read on a chip above 16 MiB when the module lists it |
| `--rate` | `1:1` | `1:1` SDR PHY or `1:2` PHY |
| `--divisor` | `2` at 1:1, `1` at 1:2 | Reset value of the divisor of the PHY; the SDR PHY rounds an odd divisor up (1 and 2 both give SCK = system clock / 2) |
| `--bus-standard` | `wishbone` | `wishbone` or `axi-lite` |
| `--bus-endianness` | `big` | Byte order of the memory bus |
| `--with-master` | off | Exposes a second bus to the master registers |
| `--vendor` | `xilinx` | `xilinx`, `altera`, `intel` or `lattice`: the I/O primitives |
| `--sim` | off | Replaces the PHY by `LiteSPIPHYModel` |
| `--clk-freq` | `100e6` | Parsed but not used: the core is built at a fixed 1 MHz |

```sh
litespi_gen --bus-standard=wishbone --module=S25FL256L --mode=x4 --rate=1:1
```

## Simulation {#opt-sim}

| Tool | Option | Meaning |
|-----------------------|--------------------------------------|--------------------------------------|
| `litex_sim` | `--with-spi-flash` | Adds an S25FL128L in 1-1-4 mode with the PHY model and the master |
| `litex_sim` | `--spi_flash-init` | Binary image loaded into the flash model |

[Simulation and tests](#simulation) describes both.

## BIOS constants {#opt-bios}

The BIOS reads these constants from the generated `soc.h`. `add_spi_flash` adds the
`SPIFLASH_PHY_*` constants and the `SPIFLASH_MODULE_*` ones of the module (name, sizes, erase,
quad and QPI capability); a target adds the others, including `SPIFLASH_MODULE_DUMMY_BITS`, with
`self.add_constant()`.

| Constant | Effect |
|-------------------------------------------------|--------------------------------------------------|
| `SPIFLASH_DEBUG` | Prints identifier and register reads, dummy bits and calibration steps (`software_debug=True`) |
| `SPIFLASH_SKIP_FREQ_INIT` | Skips the frequency calibration at boot |
| `SPIFLASH_MODULE_DUMMY_BITS` | Writes this value to `mmap_dummy_bits` at boot; never set by `add_spi_flash` |
| `FLASH_BOOT_ADDRESS` | Enables the boot from flash: address of the boot image in the CPU address space |
| `FLASH_BOOT_DISABLE` | Removes the flash from the automatic boot sequence; the `flashboot` command stays |
| `FLASH_BOOT_PRIORITY` | Rank of the flash in the automatic boot sequence, 10 by default |
| `SPIRAM_SKIP_FREQ_INIT` | Skips the calibration of the SPI RAM |

The boot from flash and the image format are described in [BIOS, boot and flash
update](#software).
