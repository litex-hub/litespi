# The register master {#master}

This chapter describes the register master: the frontend through which software sends any SPI
command, one transfer at a time. The LiteX BIOS uses it to identify, configure, erase and program
the flash. Read it to drive the flash from firmware or from a host script; the commands are
explained in [Inside a SPI NOR flash](#flash-primer).

## At a glance {#master-glance}

| Item | Value |
|------------------|---------------------------------------------------------------------------|
| Class | `LiteSPIMaster` (`litespi/core/master.py`), built by `LiteSPI` with `with_master=True` (default) |
| Control | Five registers: `cs`, `phyconfig`, `rxtx`, `status`, `clk_divisor` |
| Transfer | Up to 32 bits per write of `rxtx`, on 1, 2, 4 or 8 lines, with an output enable per DQ line |
| Return | One 32-bit word per transfer: the bits shifted in during it |
| Chip select | Held by software for the whole command, one bit per CS line |
| FIFOs | TX and RX, depth 1 by default (`master_tx_fifo_depth`, `master_rx_fifo_depth`) |
| Interrupt | Optional, on RX data available (`master_with_irq`) |
| Sharing | Round-robin crossbar with the MMAP |
| Status | Validated on hardware: see [status](#intro-status) |

## Registers {#master-registers}

The master has five registers. In a LiteX SoC their names carry the prefix of the core and of the
master, `spiflash_master_`; offsets are in the [Register reference](#registers).

| Register | Bits | Access | Role |
|-----------------|------:|------------|----------------------------------------------|
| `cs` | 1 per CS line | Read-write | 1 selects the chip (CS low) and claims the PHY, 0 ends the command |
| `phyconfig` | 24 | Read-write | Settings of the next transfers: `len`, `width`, `mask` |
| `rxtx` | 32 | Write, read | Write: push one transfer. Read: pop one returned word |
| `status` | 2 | Read-only | Bit 0 `tx_ready` (TX FIFO not full), bit 1 `rx_ready` (RX FIFO not empty) |
| `clk_divisor` | 10 | Read-write | Divisor of the master transfers, 0: use the PHY register |

The fields of `phyconfig` describe one transfer, as the table below shows.

| Field | Bits | Meaning |
|---------|-------:|----------------------------------------------------------------------|
| `len` | 5:0 | Number of bits of the transfer, 1 to 32 |
| `width` | 11:8 | Number of DQ lines per SCK cycle: 1, 2, 4 or 8 |
| `mask` | 23:16 | Output enable per DQ line, bit n for DQn: 1 drives the line, 0 releases it |

## One transfer step by step {#master-transfer}

A transfer is one element of the core-to-PHY stream ([Architecture](#architecture)). Software
builds it from the registers in the following order:

1. Write `phyconfig` with the length, width and mask of the transfer.
2. Write `cs` with 1: CS goes low once the master holds the PHY.
3. Write the data to `rxtx` while `status.tx_ready` is 1: a write to a full TX FIFO is dropped
   without notice. The master pushes it into the TX FIFO with the current `phyconfig` and
   `clk_divisor`, so `phyconfig` can change before the next write.
4. The PHY clocks `len / width` SCK cycles. It sends the low `len` bits of the data, most
   significant first, and shifts in the same number of bits.
5. `status.rx_ready` rises. Reading `rxtx` returns the bits shifted in, the last one in bit 0,
   and pops them. Only the low `len` bits are meaningful: the 1:2 PHY leaves bits of earlier
   transfers above them.
6. Repeat from step 1 or 3 for the next phase; write `cs` with 0 to end the command.

Every transfer returns a word, even when nothing is read: software pops it. With the default
RX FIFO depth of 1, an unread word holds the PHY, and the next transfer waits until software reads
it.

On one line, a transfer drives the data on DQ0 (MOSI) and samples DQ1 (MISO). On 2, 4 or 8 lines,
the same lines carry both directions, and the mask decides which ones the FPGA drives. The figure
below shows a JEDEC ID read built from 8-bit transfers.

![JEDEC ID read with the master. Look at the rhythm: each write of rxtx sends 8 bits and returns 8
bits, which software reads before the next write; CS stays low from cs = 1 to
cs = 0.](master_seq.svg)

## A complete command from software {#master-software}

The C functions below drive the master through the accessors that LiteX generates in `csr.h`. The
helper `spi_xfer` runs one transfer and returns the word shifted in. The other functions build the
usual flash commands from it, as listed in [Inside a SPI NOR flash](#flash-primer).

```c
#include <generated/csr.h>

#define TX_READY (1 << CSR_SPIFLASH_MASTER_STATUS_TX_READY_OFFSET)
#define RX_READY (1 << CSR_SPIFLASH_MASTER_STATUS_RX_READY_OFFSET)

static uint32_t spi_xfer(uint32_t data, int len, int width, int mask)
{
    spiflash_master_phyconfig_write(
        (len   << CSR_SPIFLASH_MASTER_PHYCONFIG_LEN_OFFSET)   |
        (width << CSR_SPIFLASH_MASTER_PHYCONFIG_WIDTH_OFFSET) |
        (mask  << CSR_SPIFLASH_MASTER_PHYCONFIG_MASK_OFFSET));
    while (!(spiflash_master_status_read() & TX_READY));
    spiflash_master_rxtx_write(data);
    while (!(spiflash_master_status_read() & RX_READY));
    return spiflash_master_rxtx_read();
}

/* JEDEC ID (0x9f): opcode and three ID bytes in one 32-bit transfer. */
uint32_t flash_read_id(void)
{
    uint32_t id;
    spiflash_master_cs_write(1);
    id = spi_xfer(0x9f000000, 32, 1, 0x1) & 0xffffff;
    spiflash_master_cs_write(0);
    return id; /* Manufacturer, memory type, capacity. */
}

/* Status register 1 (0x05): bit 0 is WIP (write in progress). */
uint8_t flash_read_status(void)
{
    uint8_t sr;
    spiflash_master_cs_write(1);
    sr = spi_xfer(0x0500, 16, 1, 0x1) & 0xff;
    spiflash_master_cs_write(0);
    return sr;
}

/* Write enable (0x06): needed before each erase and each page program. */
void flash_write_enable(void)
{
    spiflash_master_cs_write(1);
    spi_xfer(0x06, 8, 1, 0x1);
    spiflash_master_cs_write(0);
}

/* 64 KiB sector erase (0xd8), 3-byte address. */
void flash_erase_sector(uint32_t addr)
{
    flash_write_enable();
    spiflash_master_cs_write(1);
    spi_xfer((0xd8 << 24) | (addr & 0xffffff), 32, 1, 0x1);
    spiflash_master_cs_write(0);
    while (flash_read_status() & 1);
}

/* Page program (0x02): at most one page, within one page. */
void flash_page_program(uint32_t addr, const uint8_t *buf, int len)
{
    flash_write_enable();
    spiflash_master_cs_write(1);
    spi_xfer((0x02 << 24) | (addr & 0xffffff), 32, 1, 0x1);
    for (int i = 0; i < len; i++)
        spi_xfer(buf[i], 8, 1, 0x1);
    spiflash_master_cs_write(0);
    while (flash_read_status() & 1);
}
```

The 32-bit transfers pack the opcode in the top byte, so that it goes out first. In the ID read,
the first 8 bits shifted in arrive during the opcode and land in bits 31:24, which the mask removes.
The LiteX BIOS library `liblitespi` uses the same registers with 8-bit transfers
([BIOS, boot and flash update](#software)).

From a host, the same sequence runs through a LiteX bridge (UART, Ethernet or PCIe) and the
`RemoteClient` of LiteX, which names the registers from the `csr.csv` of the build. The script
below reads the JEDEC ID; it expects `litex_server` to run and `csr.csv` in the current directory.

```python
from litex import RemoteClient

bus = RemoteClient()
bus.open()

def spi_xfer(data, length=8, width=1, mask=0x1):
    bus.regs.spiflash_master_phyconfig.write(length | (width << 8) | (mask << 16))
    bus.regs.spiflash_master_rxtx.write(data)
    while not (bus.regs.spiflash_master_status.read() & 0x2):
        pass
    return bus.regs.spiflash_master_rxtx.read()

bus.regs.spiflash_master_cs.write(1)
jedec_id = spi_xfer(0x9f000000, length=32) & 0xffffff
bus.regs.spiflash_master_cs.write(0)
print(f"JEDEC ID: 0x{jedec_id:06x}")

bus.close()
```

## Widths and masks for wide commands {#master-widths}

A command on several lines is a sequence of transfers with different widths, one per phase. The
mask releases the lines the flash drives: during the dummy cycles and the data of a read. The table
below gives the transfers of a 1-1-4 read (`0x6b`) and of a 1-1-4 page program (`0x32`) with 8
dummy cycles.

| Command | Phase | `len` | `width` | `mask` |
|------------------|--------------|------:|--------:|-------:|
| 1-1-4 read | Opcode | 8 | 1 | `0x01` |
| | Address | 24 | 1 | `0x01` |
| | Dummy | 8 | 1 | `0x00` |
| | Data, 4 bytes | 32 | 4 | `0x00` |
| 1-1-4 program | Opcode | 8 | 1 | `0x01` |
| | Address | 24 | 1 | `0x01` |
| | Data, 4 bytes | 32 | 4 | `0x0f` |

The length is a multiple of the width, and a dummy phase on 4 lines lasts `len / 4` cycles. The
wide modes need the `dq` pads (`spiflash4x` in LiteX) and a flash with quad mode enabled
([Inside a SPI NOR flash](#flash-primer)). QPI and octal commands are in development
([status](#intro-status)).

## FIFO depth and interrupt {#master-fifo-irq}

The TX and RX FIFOs hold one transfer each by default. `master_tx_fifo_depth` and
`master_rx_fifo_depth` of `LiteSPI` make them deeper, so that software can push several transfers
before it reads the results; each transfer still returns one word to pop.

With `master_with_irq=True`, the master raises an event when the RX FIFO becomes non-empty, with
the usual LiteX event registers (`master_ev_status`, `master_ev_pending`, `master_ev_enable`).
`add_spi_flash` sets it when the SoC has interrupts and an interrupt location named after the core.

## Sharing the PHY with the MMAP {#master-sharing}

The master and the MMAP reach the PHY through a round-robin crossbar
([Architecture](#architecture)). A frontend keeps the PHY as long as it requests it: the master
while `cs` is not 0, the MMAP while its burst holds CS low. This has three consequences:

- A master command can wait up to the burst timeout of the MMAP, 256 `sys` cycles after the last
  flash read ([Bursts](#mmap-burst)).
- While `cs` is 1, MMAP reads wait. Code that drives the master must not be fetched from the same
  flash at that time: it runs from RAM or from the CPU cache.
- After an erase or a program, the CPU caches can hold old flash content: software invalidates the
  range before it reads it back through the MMAP.

Each frontend has its own divisor register, so the master and the MMAP can run at different SCK
frequencies.

## In the code {#master-code}

| Item | File | Name |
|----------------|--------------------------------|--------------------------------|
| Register master | `litespi/core/master.py` | `LiteSPIMaster` |
| Instantiation | `litespi/__init__.py` | `LiteSPI`: `with_master`, `master_tx_fifo_depth`, `master_rx_fifo_depth`, `master_with_irq` |
| Arbitration | `litespi/crossbar.py` | `LiteSPICrossbar` |
| BIOS driver | LiteX `liblitespi/spiflash.c` | `spiflash_master_write`, `transfer_cmd` |
| Tests | `test/test_spi_master.py` | Width of the `len` field |

Where to go next: [Memory-mapped reads and writes](#mmap) for the other frontend, [BIOS, boot and
flash update](#software) for the BIOS commands built on the master, [Debugging](#debugging) for
register pokes from a host.
