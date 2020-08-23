#
# This file is part of LiteSPI
#
# Copyright (c) 2020 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: BSD-2-Clause


import enum

class SpiNorFeatures(enum.Flag):
    FEATURE_ERASED_ZERO     = enum.auto()
    """Erasing flash ends up with 0x00 rather than 0xff."""

    FEATURE_NO_ERASE        = enum.auto()
    """Chip does not support erase commands."""

    FEATURE_OTP             = enum.auto()
    """Has a one time programming area."""

    FEATURE_WRSR_EWSR       = enum.auto()
    """Before sending the WRSR instruction the Enable-Write-Status-Register must be written too."""

    FEATURE_WRSR_WREN       = enum.auto()
    """Before sending WRSR instruction, the Write Enable (WREN) instruction must be decoded and executed to set the Write Enable Latch (WEL) bit in advance."""

    FEATURE_WRSR_EITHER     = FEATURE_WRSR_EWSR | FEATURE_WRSR_WREN

    FEATURE_QPI             = enum.auto()
    """Supports Quad-SPI-mode - ???"""

    FEATURE_4BA_ENTER       = enum.auto()
    """Can enter/exit 4BA mode with instructions 0xb7/0xe9 w/o WREN."""

    FEATURE_4BA_ENTER_WREN  = enum.auto()
    """Can enter/exit 4BA mode with instructions 0xb7/0xe9 after WREN."""

    FEATURE_4BA_ENTER_EAR7  = enum.auto()
    """Can enter/exit 4BA mode by setting bit7 of the ext addr reg."""

    FEATURE_4BA_EXT_ADDR    = enum.auto()
    """Regular 3-byte operations can be used by writing the most significant address byte into an extended address register."""

    FEATURE_4BA_READ        = enum.auto()
    """Native 4BA read instruction (0x13) is supported."""

    FEATURE_4BA_FAST_READ   = enum.auto()
    """Native 4BA fast read instruction (0x0c) is supported."""

    FEATURE_4BA_WRITE       = enum.auto()
    """Native 4BA byte program (0x12) is supported."""

    # 4BA Shorthands
    FEATURE_4BA_NATIVE	= (FEATURE_4BA_READ | FEATURE_4BA_FAST_READ | FEATURE_4BA_WRITE)
    FEATURE_4BA		= (FEATURE_4BA_ENTER | FEATURE_4BA_EXT_ADDR | FEATURE_4BA_NATIVE)
    FEATURE_4BA_WREN	= (FEATURE_4BA_ENTER_WREN | FEATURE_4BA_EXT_ADDR | FEATURE_4BA_NATIVE)
    FEATURE_4BA_EAR7	= (FEATURE_4BA_ENTER_EAR7 | FEATURE_4BA_EXT_ADDR | FEATURE_4BA_NATIVE)

