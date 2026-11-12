# The SPI memory database {#modules}

LiteSPI describes each supported chip as a Python class, a *module*, that gives its size, its IDs,
the commands it accepts and their dummy cycles. The MMAP, the PHYs, LiteX and the BIOS build their
commands from it. This chapter explains how a module is written, what its read command sets, and
how to add a chip.

## At a glance {#mod-glance}

| Item | Value |
|---------------------|-------------------------------------------------------------------------|
| Flash modules | 481 classes in `litespi/modules/modules.py` |
| SPI RAM modules | 1 class, `APS6404L`, in `litespi/modules/ram_modules.py` (in development) |
| Base class | `SpiNorFlashModule` (`litespi/spi_nor_flash_module.py`) |
| Opcodes | `SpiNorFlashOpCodes` (`litespi/opcodes.py`) |
| Manufacturer IDs | `SpiNorFlashManufacturerIDs` (`litespi/ids.py`) |
| Size check | `MetaSizes` metaclass: page size times pages equals total size |
| Import | `from litespi.modules import W25Q128JV` |
| Listing | `print_modules()` of `litespi.modules` |
| Discovery | None: the module is chosen at build time; LiteSPI reads no SFDP table |

The flash modules come from 18 manufacturer groups, as the table below shows (counts from the
`manufacturer_id` of each class). The group named non-JEDEC uses ID `0x00`.

| Manufacturer | Modules | Manufacturer | Modules | Manufacturer | Modules |
|--------------|--------:|--------------|--------:|--------------|--------:|
| Macronix | 86 | GigaDevice | 39 | Sanyo | 15 |
| ST | 69 | ISSI | 35 | EON | 12 |
| Atmel | 47 | SST | 28 | Intel | 9 |
| Winbond | 45 | non-JEDEC | 22 | ESMT | 4 |
| Spansion | 43 | AMIC | 21 | Micron, Thomson | 2 each |
| | | | | Fujitsu, Puya | 1 each |

Sizes range from 128 bytes to 256 MiB; 66 modules are larger than 16 MiB and need 4-byte
addresses to be read entirely. 466 modules have 256-byte pages.

The read commands that the modules list are counted in the table below. Every module accepts the
single-line read `READ_1_1_1` and the page program `PP_1_1_1`. The QPI and octal commands are in
development ([status](#intro-status)).

| Read command | Modules | Read command | Modules |
|----------------------|--------:|----------------------|--------:|
| `READ_1_1_1` | 481 | `READ_1_4_4` | 6 |
| `READ_1_1_1_FAST` | 228 | `READ_1_2_2` | 5 |
| `READ_1_1_4` | 110 | `READ_1_2_2_4B` | 4 |
| `READ_1_1_2` | 89 | `READ_4_4_4` | 3 |
| `READ_1_1_1_4B` | 35 | `READ_1_1_8` | 3 |
| `READ_1_1_1_FAST_4B` | 34 | `READ_1_4_4_4B` | 3 |
| `READ_1_1_4_4B` | 18 | `READ_4_4_4_4B` | 2 |
| `READ_1_1_2_4B` | 17 | `READ_1_1_8_4B` | 2 |

The three QPI modules are `IS25WP512M`, `MX25L12833F` and `MX25U25645G`; the three octal ones are
`MT35XU02G`, `MT35XU512ABA` and `MX25LM51245`.

## A module class {#mod-class}

A module is a subclass of `SpiNorFlashModule` with class attributes only. The listing below is the
`W25Q128JV` class of the database, a 16 MiB Winbond flash.

```python
class W25Q128JV(SpiNorFlashModule):

    manufacturer_id = SpiNorFlashManufacturerIDs.WINBOND
    device_id = 0x7018
    name = "w25q128jv"

    total_size  =   16777216   # bytes
    page_size   =        256   # bytes
    total_pages =      65536

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.PP_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_1_FAST,
        SpiNorFlashOpCodes.READ_1_1_2,
        SpiNorFlashOpCodes.PP_1_1_2,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.PP_1_1_4,
        SpiNorFlashOpCodes.READ_1_2_2,
        SpiNorFlashOpCodes.READ_1_4_4,
    ]
    dummy_bits = 8

    dummy_cycles = {
        SpiNorFlashOpCodes.READ_1_2_2: 0,
        SpiNorFlashOpCodes.READ_1_4_4: 4,
    }
```

The attributes have the following roles. The constructor asserts that the mandatory ones exist.

| Attribute | Mandatory | Role |
|----------------------------|------------|---------------------------------------------------------|
| `manufacturer_id` | Yes | First byte of the JEDEC ID, from `SpiNorFlashManufacturerIDs` |
| `device_id` | Yes | Next two bytes of the JEDEC ID (memory type, capacity) |
| `name` | Yes | Lower-case name, printed by the BIOS (`SPIFLASH_MODULE_NAME`) |
| `total_size` | Two of three | Size in bytes |
| `page_size` | Two of three | Largest page program, in bytes |
| `total_pages` | Two of three | Number of pages |
| `supported_opcodes` | Yes | Commands the chip accepts: reads and programs |
| `dummy_bits` | One of two | Dummy cycles of the fast reads (an SCK cycle count, despite its name) |
| `dummy_cycles` | One of two | Dummy cycles per read command (a dictionary) |
| `quad_enable` | No | How the BIOS sets the QE bit ([Quad enable](#mod-quad-enable)) |
| `erase_commands` | No | Erase geometry ([Erase commands](#mod-erase)) |

The `MetaSizes` metaclass computes the missing one of the three sizes when the class is defined,
and stops with a table of the provided and computed values when they disagree. The JEDEC ID itself
is described in [Inside a SPI NOR flash](#flash-primer).

## Choosing the read command {#mod-read-cmd}

A module class becomes a configuration when it is instantiated with the read command that the MMAP
will use. The target script picks it:

```python
from litespi.modules import W25Q128JV
from litespi.opcodes import SpiNorFlashOpCodes as Codes

self.add_spi_flash(mode="4x", module=W25Q128JV(Codes.READ_1_1_4))
```

The constructor takes the following arguments:

| Argument | Default | Role |
|--------------------------|-------------|-------------------------------------------------------|
| `default_read_cmd` | (required) | Read command of the MMAP; sets the widths of the module |
| `read_cmds` | `None` | Other read commands, checked against the chip only |
| `program_cmd` | `PP_1_1_1` | Program command, used by MMAP writes |
| `erase_cmd` | `None` | Erase command to select among the erase commands |
| `erase_commands` | `None` | Erase geometry, overriding the class attribute |

The constructor raises an error when a read or program command is not in `supported_opcodes`. It
then derives the widths from the name of the read command, as the figure below shows: each field of
the name sets one attribute of the module.

![Name of an opcode. Read it field by field: the operation, then the lines used by the opcode,
the address and the data, then the optional suffixes FAST (fast read), DTR (double transfer rate)
and 4B (4-byte address).](mod_name.svg)

The attributes it sets are listed below. `fast_mode` decides whether the MMAP sends dummy cycles
([Dummy cycles](#mmap-dummy)).

| Attribute | Value |
|--------------|---------------------------------------------------------------------|
| `cmd_width` | Lines of the opcode (first number of the name) |
| `addr_width` | Lines of the address and dummy cycles (second number) |
| `bus_width` | Lines of the data (third number) |
| `addr_bits` | 32 when the name ends in `_4B`, else 24 |
| `fast_mode` | True when the name contains `FAST` or the data uses more than one line |
| `ddr` | True when the name contains `DTR` |

The PHYs check that the pads have at least `bus_width` data lines and refuse a module with `ddr`
set: both PHYs run the flash at single transfer rate ([PHYs](#phys)). The session below
instantiates `W25Q128JV` for 1-4-4 reads and prints what the constructor computed.

```console
$ python3 - <<'EOF'
from litespi.modules import W25Q128JV
from litespi.opcodes import SpiNorFlashOpCodes as Codes

flash = W25Q128JV(Codes.READ_1_4_4)
print(flash.name, flash.total_size, flash.page_size)
print(flash.cmd_width, flash.addr_width, flash.bus_width, flash.addr_bits)
print(flash.fast_mode, flash.dummy_cycles, hex(flash.erase_opcode.code), flash.erase_size)
EOF
w25q128jv 16777216 256
1 4 4 24
True 4 0xd8 65536
```

The 4 dummy cycles printed are the value of the database, which leaves out the mode-bit cycles of
this read ([Dummy cycles](#mod-dummy)).

## Dummy cycles {#mod-dummy}

A module gives its dummy cycles in one of two ways. `dummy_bits` is one number for every fast read;
all 481 flash modules set it to 8, which the code uses as a number of SCK cycles. `dummy_cycles`
is a dictionary from read command to cycles, for chips whose commands need different counts.

The constructor resolves the dictionary for the chosen read command. A command missing from the
dictionary falls back to `dummy_bits`, or to 0 when the class has none. Six modules carry a
dictionary:

| Module | Commands in the dictionary (cycles) |
|---------------|------------------------------------------------------------------------|
| `W25Q128JV` | 1-2-2 (0), 1-4-4 (4) |
| `W25Q128JW` | 1-1-2 (8), 1-2-2 (4), 1-1-4 (32), 1-4-4 (6) |
| `W25Q256JW` | as `W25Q128JW`, plus the `_4B` variants |
| `MX25L12833F` | 1-1-1 fast (8), 1-2-2 (8), 1-4-4 (8), 4-4-4 (6) |
| `MX25U25645G` | 1-1-1 fast (8), 1-1-2 (8), 1-2-2 (4), 1-1-4 (8), 1-4-4 (6), 4-4-4 (6), and `_4B` variants |
| `IS25WP512M` | 1-1-1 fast (8), 1-1-2 (8), 1-2-2 (4), 1-1-4 (8), 1-4-4 (6), 4-4-4 (6), and `_4B` variants |

The count must match the configuration of the chip. Many flashes have a programmable latency:
check the datasheet table for the command and the SCK frequency used. The MMAP sends the whole gap
between the address and the data as one dummy phase, with no line driven ([SPI memories in a
nutshell](#spi-primer)). On 1-2-2 and 1-4-4 reads, the module count is therefore the whole gap:
the mode-bit cycles plus the dummy cycles of the datasheet. The MMAP turns the count into its
`mmap_dummy_bits` register, which software can still change ([Dummy cycles](#mmap-dummy)).

Some values of the database do not follow this rule, as listed below; no LiteX-Boards target uses
these read commands.

- `W25Q128JV`: 1-4-4 (4) and 1-2-2 (0) leave out the mode-bit cycles. The datasheet gap is 2
  mode-bit cycles plus 4 dummy cycles on 1-4-4, and 4 mode-bit cycles on 1-2-2, that is 6 and 4:
  with the module values, these reads would return shifted data.
- `W25Q128JW` and `W25Q256JW`: 1-1-4 (32, and its `_4B` variant on `W25Q256JW`) is four times the
  8 dummy cycles of the Winbond quad output read, as if counted in bits on four lines. The MMAP
  sends 32 SCK cycles, and the data comes out shifted.
- `W25Q512JV`, `S25FL128L` and `MX25L12833F`: their 1-4-4 (and 1-2-2 on `W25Q512JV` and
  `MX25L12833F`) reads use 8 cycles, from `dummy_bits` or the dictionary. These values are to
  check against the latency table of each datasheet and the latency setting of the chip.

## Quad enable {#mod-quad-enable}

Most quad-capable flashes ignore the quad commands until a Quad Enable (QE) bit is set in a status
or configuration register ([Inside a SPI NOR flash](#flash-primer)). The `quad_enable` attribute
names the method that sets it; the BIOS implements the methods ([BIOS, boot and flash
update](#software)).

| `quad_enable` | Register write | Modules |
|-------------------------|-----------------------------------------|------------------------------|
| `"wrsr_sr1_bit6"` | Status register 1, bit 6, with WRSR (`0x01`) | 32: Macronix (21), ISSI (11) |
| `"wrr_cr1_bit1"` | Configuration register 1, bit 1, with WRR (`0x01`) | 6: Spansion |
| absent | Generic sequence of the BIOS | the other 443 |

`add_spi_flash` exports the method as a constant (`SPIFLASH_MODULE_QUAD_ENABLE_WRSR_SR1_BIT6`,
for example) when the flash is wired in 4x mode, the read command uses four data lines and the
module supports `READ_1_1_4`. A test checks
that every ISSI and Macronix module with `READ_1_1_4` declares `"wrsr_sr1_bit6"`.

## Erase commands {#mod-erase}

The erase geometry tells software which erase command to use and how much it erases. It is a list
of `SpiNorFlashEraseCommand(opcode, size, addr_bits)`, the first entry being the default; an
address length of 0 is for a chip erase without address.

The modules above 16 MiB whose datasheet gives 4-byte erase commands define `erase_commands`, the
4-byte sector erase first, as the table below shows. Each list ends with the 3-byte versions, so
that `erase_cmd=Codes.SE` still selects the 3-byte erase.

| Modules | Erase commands, in order |
|----------------------------------------------|------------------------------------------------|
| `MT25QL256`, `MT25QL512`, `MT25QU256`, `MT25QU512` and their `A` variants | `SE_4B`, `BE_4K_4B`, `SE`, `BE_4K` (64 and 4 KiB) |
| `W25Q256`, `W25Q256FV`, `W25Q256JV`, `W25Q256JVM`, `W25Q256JW`, `W25Q512JV` | as above |
| `IS25LP256`, `IS25LP256D`, `IS25LP512M`, `IS25WP256`, `IS25WP256D`, `IS25WP512M` | as above |
| `MX25L25645G`, `MX25L51245G`, `MX25U25645G`, `MX25U51245G` | as above |
| `S25FL512S`, `S70FL01GS` | `SE_4B`, `SE` (256 KiB sectors) |

The other modules fall back to the sector erase `SE` (`0xd8`): 64 KiB with a 24-bit address.
`erase_cmd` selects another erase command, which the constructor translates when its geometry is
unambiguous:

| Opcode name | Code | Size | Address bits |
|----------------------|--------|-----------:|-------------:|
| `SE` (default) | `0xd8` | 64 KiB | 24 |
| `BE_4K` | `0x20` | 4 KiB | 24 |
| `BE_4K_PMC` | `0xd7` | 4 KiB | 24 |
| `BE_32K` | `0x52` | 32 KiB | 24 |
| `BE_256` | `0xdb` | 256 bytes | 24 |
| `SE_4B` | `0xdc` | 64 KiB | 32 |
| `BE_4K_4B` | `0x21` | 4 KiB | 32 |
| `BE_32K_4B` | `0x5c` | 32 KiB | 32 |
| `CHIP_ERASE` | `0xc7` | whole chip | 0 |
| `CHIP_ERASE_ALT` | `0x60` | whole chip | 0 |
| `CHIP_ERASE_ATMEL` | `0x62` | whole chip | 0 |

`add_spi_flash` exports the selected command as `SPIFLASH_MODULE_ERASE_OPCODE`, `_SIZE` and
`_ADDR_BITS`, which the BIOS erase routine uses. On a chip larger than 16 MiB without a list, the
24-bit default reaches only the first 16 MiB, and the BIOS refuses an erase above it: such a chip
needs a 4-byte erase command, given with `erase_cmd` or `erase_commands`.

## Opcodes {#mod-opcodes}

`SpiNorFlashOpCodes` names every command code with a tuple of its code and a description. The name
encodes the mode: `<OP>_<cmd>_<addr>_<data>[_FAST][_DTR][_4B]`, the three numbers being the lines
of the opcode, address and data ([SPI memories in a nutshell](#spi-primer)). Only the commands
used as read or program commands of a module need a name of this form.

The same code can appear under two names: `READ_1_4_4` and `READ_4_4_4` are both `0xeb`, sent on
one line or on four. The name, not the code, gives the mode. The main codes are:

| Group | Names (code) |
|----------------|-------------------------------------------------------------------------------|
| Reads | `READ_1_1_1` (`0x03`), `READ_1_1_1_FAST` (`0x0b`), `READ_1_1_2` (`0x3b`), `READ_1_2_2` (`0xbb`), `READ_1_1_4` (`0x6b`), `READ_1_4_4` (`0xeb`), `READ_4_4_4` (`0xeb`), `READ_1_1_8` (`0x8b`), `READ_1_8_8` (`0xcb`) |
| 4-byte reads | `READ_1_1_1_4B` (`0x13`), `READ_1_1_1_FAST_4B` (`0x0c`), `READ_1_1_2_4B` (`0x3c`), `READ_1_1_4_4B` (`0x6c`), `READ_1_4_4_4B` (`0xec`) |
| Programs | `PP_1_1_1` (`0x02`), `PP_1_1_2` (`0xa2`), `PP_1_1_4` (`0x32`), `PP_1_4_4` (`0x38`), `PP_1_1_1_4B` (`0x12`), `PP_1_1_4_4B` (`0x34`) |
| Registers | `WREN` (`0x06`), `RDSR` (`0x05`), `WRSR` (`0x01`), `RDCR` (`0x35`), `RDFSR` (`0x70`) |
| Identification | `RDID` (`0x9f`), `RDSFDP` (`0x5a`), `RDUID` (`0x4b`) |
| 4-byte mode | `EN4B` (`0xb7`), `EX4B` (`0xe9`), `RDEAR` (`0xc8`), `WREAR` (`0xc5`) |

The class also defines DTR reads (from `0x0d`), which neither PHY accepts, and short aliases such
as `FAST_READ` and `PP`. `RDSFDP` is a name only: no code of LiteSPI reads the SFDP table.

## Manufacturer IDs {#mod-ids}

`SpiNorFlashManufacturerIDs` lists the first byte that the chip returns to the JEDEC ID command
(`0x9f`). The values below are the ones of `litespi/ids.py`.

| Name | ID | Name | ID | Name | ID |
|--------------|--------|--------------|--------|-------------|--------|
| `AMIC` | `0x37` | `GIGADEVICE` | `0xc8` | `SANYO` | `0x62` |
| `ATMEL` | `0x1f` | `INTEL` | `0x89` | `SPANSION` | `0x01` |
| `EON` | `0x1c` | `ISSI` | `0x9d` | `SST` | `0xbf` |
| `ESMT` | `0x8c` | `MACRONIX` | `0xc2` | `ST` | `0x20` |
| `FUJITSU` | `0x04` | `MICRON` | `0x2c` | `THOMSON` | `0xba` |
| `PUYA` | `0x85` | `NONJEDEC` | `0x00` | `WINBOND` | `0xef` |

The Micron MT25Q modules use `ST` (`0x20`), the ID that these parts return. LiteSPI does not
compare the ID read from the chip with the module: a wrong module shows up as wrong reads, not as
an error ([Debugging](#debugging)).

## The SPI RAM module {#mod-psram}

`APS6404L` describes an 8 MiB SPI PSRAM, for use with `add_spi_ram`; this path is in development
([status](#intro-status)). The class follows the flash format with RAM-specific values:

| Item | Value |
|---------------------|----------------------------------------------------------------------|
| ID | `NONJEDEC` manufacturer, `device_id` 0 |
| Size | 8 MiB in 65536 pages of 128 bytes |
| Reads | `READ_1_1_1`, `READ_1_1_1_FAST` (8), `READ_1_4_4` (6), `READ_4_4_4_LOW` (4), `READ_4_4_4` (6) |
| Programs | `PP_1_1_1`, `PP_1_4_4` |
| Quad enable | None declared |
| Erase | The default geometry, which the MMAP never uses |

The comments of the class give the maximum SCK frequency of each command. A RAM accepts writes at
any time, so `add_spi_ram` builds the MMAP with writes always on and an L2 cache in front
([Writes](#mmap-write)).

## Adding a chip {#mod-add}

A new chip is a new class in `litespi/modules/modules.py`, written from its datasheet. The
checklist below covers what the code and the tests expect:

1. Name the class after the part number and set `name` to its lower-case form; both must be
   unique in the database.
2. Set `manufacturer_id` and `device_id` from the JEDEC ID table of the datasheet.
3. Give two of `total_size`, `page_size` and `total_pages`.
4. List in `supported_opcodes` the reads and page programs of the chip, with the `_4B` variants
   for chips above 16 MiB.
5. Set `dummy_bits = 8` or the cycle count of the datasheet; add a `dummy_cycles` dictionary when
   the commands differ. On 1-2-2 and 1-4-4 reads, count the mode-bit cycles too.
6. Set `quad_enable` when the chip has a QE bit handled by one of the two methods.
7. Add `erase_commands` when the chip has 4 KiB erases or 4-byte erase commands.
8. Put the datasheet URL in the docstring of the class.
9. Update the inventory count of `test/test_spi_nor_modules.py`, then run the tests.
10. Check that the BIOS handles the quad enable of the chip, and build a target with it.

The template below shows a quad flash above 16 MiB with its erase geometry. The part and the
values are placeholders: take every number from the datasheet.

```python
class MYFLASH256(SpiNorFlashModule):
    """MYFLASH256

    Datasheet: <URL of the datasheet>
    """

    manufacturer_id = SpiNorFlashManufacturerIDs.MACRONIX
    device_id = 0x0000 # Memory type and capacity bytes of the JEDEC ID.
    name = "myflash256"

    total_size  =   33554432   # bytes
    page_size   =        256   # bytes
    total_pages =     131072

    supported_opcodes = [
        SpiNorFlashOpCodes.READ_1_1_1,
        SpiNorFlashOpCodes.READ_1_1_4,
        SpiNorFlashOpCodes.READ_1_1_4_4B,
        SpiNorFlashOpCodes.PP_1_1_1,
    ]
    dummy_bits  = 8
    quad_enable = "wrsr_sr1_bit6"

    erase_commands = [
        SpiNorFlashEraseCommand(SpiNorFlashOpCodes.SE_4B,    64*1024, 32),
        SpiNorFlashEraseCommand(SpiNorFlashOpCodes.BE_4K_4B,  4*1024, 32),
    ]
```

`SpiNorFlashEraseCommand` is imported from `litespi.spi_nor_flash_module`. The tests check the
types and ranges of every attribute, the uniqueness of the names and the count of classes:

```sh
python3 -m pytest -v test/test_spi_nor_modules.py test/test_flash_module.py
python3 -m litex_boards.targets.digilent_arty --with-spi-flash --build --no-compile
```

A board can also define its module in its target script, as a subclass of `SpiNorFlashModule`;
two LiteX-Boards targets do so for chips that are not in the database. Adding the chip to the
database makes it available to every design.

## Listing the database {#mod-list}

`print_modules()` prints, for every module, the size table that `MetaSizes` checks: page size,
number of pages and total size, provided and computed, in decimal and hexadecimal.

```sh
python3 -c "from litespi.modules import print_modules; print_modules()"
```

Look for the class name at the head of each table and for `==` between the provided and computed
values. To find a chip, search the output or `litespi/modules/modules.py` for its part number.

The database lives in one hand-maintained file, consolidated from data that earlier generator tools
extracted from other open-source flash databases.

## In the code {#mod-code}

The files below are under `litespi/`, the tests under `test/`.

| Item | File | Name |
|---------|-----------------------------------------|-----------------------------------------|
| Base class | `spi_nor_flash_module.py` | `SpiNorFlashModule`, `SpiNorFlashEraseCommand` |
| Size check | `spi_nor_flash_metasizes.py` | `MetaSizes` |
| Flash modules | `modules/modules.py` | 481 classes |
| SPI RAM module | `modules/ram_modules.py` | `APS6404L` |
| Package, listing | `modules/__init__.py` | `print_modules` |
| Opcodes | `opcodes.py` | `SpiNorFlashOpCodes` |
| Vendor IDs | `ids.py` | `SpiNorFlashManufacturerIDs` |
| Feature flags | `spi_nor_features.py` | `SpiNorFeatures`, not used by the core |
| Database tests | `test_spi_nor_modules.py` | Inventory, attributes, erase descriptors |
| Module tests | `test_flash_module.py` | Configuration, erase geometry, quad enable |

Where to go next: [Memory-mapped reads and writes](#mmap) for the use of the read command,
[Integration in a LiteX SoC](#integration) to pass a module to `add_spi_flash`, [BIOS, boot and
flash update](#software) for the quad enable and erase routines.
