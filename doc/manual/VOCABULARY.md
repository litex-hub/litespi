# Vocabulary of the LiteSPI manual

Project-specific writing rules, completing the generic `STYLE.md` of the manual kit.

## Names of the parts

- *the core* is the `LiteSPI` wrapper: the frontends and the crossbar, without the PHY. *the PHY*
  is `LiteSPIPHY` and its implementations; *the SDR PHY* is the `rate="1:1"` PHY
  (`LiteSPISDRPHYCore`, divided clock) and *the 1:2 PHY* is the `rate="1:2"` PHY
  (`LiteSPIDDRPHYCore`, SCK at the system clock through DDR I/O). Never write "DDR flash" or "DDR
  mode" for the 1:2 PHY: the double rate is on the FPGA I/O, not on the flash.
- *the MMAP* is the memory-mapped frontend (`LiteSPIMMAP`); *the master* is the register frontend
  (`LiteSPIMaster`); *a frontend* is either of them; *the crossbar* is `LiteSPICrossbar`; *CS
  control* is `LiteSPICSControl`, inside the PHY; *the clock generator* is `LiteSPIClkGen` (SDR
  PHY) or `DDRLiteSPIClkGen` (1:2 PHY).
- *the module* is a class of the SPI memory database (`litespi/modules/`), such as `W25Q128JV`;
  *the database* is the set of these classes. *the flash* or *the SPI memory* is the chip on the
  board; *SPI RAM* is a SPI PSRAM chip (`APS6404L`).
- *a transfer* is one element of the core-to-PHY stream (data, length, width, mask, divisor): one
  phase or part of a phase. *a command* is everything between CS going low and CS going high.
  *a burst* is a series of MMAP reads served under one command.
- *the divisor* is the SCK divider value of the SDR PHY (`clk_divisor` register, `clk_div` field).
- *the BIOS* is the LiteX BIOS with its `liblitespi` library; *the generator* is `litespi_gen`.
- *target* is a target script of LiteX-Boards (`litex_boards/targets/<target>.py`); *board* is the
  hardware.
- *register* in prose, never "CSR", except for the bus name "CSR bus". The registers of the flash
  chip are *status registers* and *configuration registers* (SR1, SR2, CR1).

## Protocol names

- Signals as *SCK* (serial clock), *CS* (chip select, active low, pin `cs_n`), *DQ0* to *DQ7*
  (data lines); *MOSI* and *MISO* only for single-line SPI, where they are DQ0 and DQ1.
- *mode x-y-z*: the number of lines used for the command, the address and the data, written with
  hyphens ("1-1-4", "1-4-4", "4-4-4"). Opcode names of the database write it with underscores
  (`READ_1_1_4`). *x1*, *x2*, *x4*, *x8* name the data width of a PHY or of a pad set.
- *phase*: command (the opcode), address, dummy, data. *dummy cycles* are SCK cycles; *dummy bits*
  is used only for the MMAP register and the module attribute of that name.
- *SPI mode 0* and *SPI mode 3* for the clock polarity and phase (CPOL, CPHA).
- *SDR* and *DTR* for the flash side (one or two bits per line per SCK cycle); *QPI* for the 4-4-4
  mode entered by a command; *OPI* for 8-8-8; *XIP* for executing code from the flash.
- Flash commands by their datasheet mnemonic in capitals with the opcode in code font: WREN
  (`0x06`), RDSR (`0x05`), RDID (`0x9f`), PP (`0x02`), SE (`0xd8`), READ (`0x03`), FAST_READ
  (`0x0b`).
- *QE bit* (quad enable), *WEL* (write enable latch), *WIP* (write in progress).
- Standards cited by number (JESD216 for SFDP), and only when sure.

## Placeholders

- `<target>` is a LiteX-Boards target name without `.py`, such as `digilent_arty`; `<module>` is a
  module class name, such as `W25Q128JV`. Both are defined once in the Conventions of the front
  matter.

## Hardware names

- FPGA families: Xilinx 7-Series (Artix-7, Kintex-7), Xilinx UltraScale+, Lattice iCE40, Lattice
  ECP5, Lattice Nexus (CrossLink-NX, Certus-NX), Gowin GW1N/GW2A/GW5A, Efinix Trion, Titanium and
  Topaz (Tz170), Cologne Chip GateMate, Altera MAX 10.
- Vendor primitives as the vendor names them: STARTUPE2, STARTUPE3, USRMCLK; the configuration
  clock pin CCLK.
- Boards as LiteX-Boards names them (Arty A7, KC705, ULX3S, iCEBreaker, Tang Nano 9K). A target
  whose name contains a company name is described by its board or FPGA name in prose; its file
  name is allowed as a code identifier.
- Flash vendors as the database names them: Winbond, Macronix, Micron, ISSI, GigaDevice, Spansion.
