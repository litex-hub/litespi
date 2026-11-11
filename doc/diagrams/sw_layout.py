#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# A typical flash layout: the bitstream the FPGA configures from at offset 0, then the BIOS for
# targets that run it in place, then a boot image for FLASH_BOOT_ADDRESS. Gowin GW1N devices
# configure from their internal flash: their BIOS starts at offset 0 of the external flash.

from svgdiag import *


def build():
    d = Diagram(CANVAS_WIDTH, 160)
    x, y, h = 20, 50, 50
    d.add(Box(x,       y, 240, h, label="Bitstream", radius=0, fill=COLOR_HARDWARE))
    d.add(Box(x + 240, y, 130, h, label="BIOS (XIP)", radius=0, fill=COLOR_ACCENT_LIGHT))
    d.add(Box(x + 370, y, 190, h, label="Boot image", radius=0, fill=COLOR_ACCENT))
    d.add(Box(x + 560, y, 160, h, label="Free", radius=0, fill=COLOR_FILL))
    d.add(Text(x,       y - 14, "0x0", size=12, anchor="start"))
    d.add(Text(x + 240, y - 14, "bios_flash_offset", size=12, anchor="start"))
    d.add(Text(x + 370, y - 14, "FLASH_BOOT_ADDRESS", size=12, anchor="start"))
    d.add(Text(x + 240, y + h + 16, "loaded by the FPGA", size=12, anchor="end"))
    d.add(Text(x + 300, y + h + 16, "run in place", size=12))
    d.add(Text(x + 465, y + h + 16, "copied or run in place", size=12))
    d.add(Text(380, 145, "Gowin GW1N: no bitstream here, the BIOS starts at 0x0", size=12, italic=True))
    return d
