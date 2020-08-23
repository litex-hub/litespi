#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause

import enum


class CFIManufacturerIDs(enum.Enum):
    """Manufacturer IDs from the CFI standard.

    Common Flash Interface (CFI) is a standard introduced by the Joint Electron
    Device Engineering Council (JEDEC) to allow in-system or programmer reading
    of flash device characteristics, which is equivalent to having data sheet
    parameters located in the device.
    """
    AMD      = 0x0001
    AMIC     = 0x0037
    ATMEL    = 0x001F
    EON      = 0x001C
    ESMT     = 0x008C
    FUJITSU  = 0x0004
    HYUNDAI  = 0x00AD
    INTEL    = 0x0089
    ISSI     = 0x009D
    MACRONIX = 0x00C2
    NEC      = 0x0010
    PMC      = 0x009D
    SAMSUNG  = 0x00EC
    SANYO    = 0x0062
    SHARP    = 0x00B0
    SST      = 0x00BF
    ST       = 0x0020 # STMicroelectronics
    MICRON   = 0x002C
    THOMSON  = 0x00BA
    TOSHIBA  = 0x0098
    WINBOND  = 0x00DA


class SpiNorFlashManufacturerIDs(enum.Enum):
    """Manufacturer IDs for SPI NOR flash chips.

    The first byte returned from the flash after sending opcode SPINor_OP_RDID.
    Sometimes these are the same as CFI IDs, but sometimes they aren't.
    """
    AMIC       = CFIManufacturerIDs.AMIC.value
    ATMEL      = CFIManufacturerIDs.ATMEL.value
    EON        = CFIManufacturerIDs.EON.value
    ESMT       = CFIManufacturerIDs.ESMT.value
    FUJITSU    = CFIManufacturerIDs.FUJITSU.value
    GIGADEVICE = 0xc8
    INTEL      = CFIManufacturerIDs.INTEL.value
    ISSI       = CFIManufacturerIDs.ISSI.value
    ST         = CFIManufacturerIDs.ST.value
    MICRON     = CFIManufacturerIDs.MICRON.value
    MACRONIX   = CFIManufacturerIDs.MACRONIX.value
    SPANSION   = CFIManufacturerIDs.AMD.value
    SANYO      = CFIManufacturerIDs.SANYO.value
    SST        = CFIManufacturerIDs.SST.value
    THOMSON    = CFIManufacturerIDs.THOMSON.value
    WINBOND    = 0xef # Also used by some Spansion

    NONJEDEC   = 0x0
