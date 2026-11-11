#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# BIOS in place (XIP): the rom region is a window of the spiflash region at bios_flash_offset, and
# the CPU reset address points to it. On iCE40 and Efinix Trion the bitstream sits below it in the
# same flash; Gowin GW1N devices configure from their internal flash and use an offset of 0.

from svgdiag import *


def build():
    d = Diagram(CANVAS_WIDTH, 280)
    d.add(Text(400, 15, "spiflash region (CPU view)", size=15, italic=True))
    x, w = 300, 200
    bit  = d.add(Box(x,  30, w, 60, label="Bitstream\n(iCE40, Efinix Trion)", radius=0, fill=COLOR_HARDWARE))
    rom  = d.add(Box(x,  90, w, 50, label="rom region (BIOS)", radius=0, fill=COLOR_ACCENT))
    free = d.add(Box(x, 140, w, 90, label="Free", radius=0, fill=COLOR_FILL))
    d.add(Text(290, 30, "origin", size=12, anchor="end"))
    d.add(Text(290, 90, "origin + bios_flash_offset", size=12, anchor="end"))
    d.add(Text(290, 230, "origin + flash size", size=12, anchor="end"))
    cpu = d.add(Box(600, 90, 140, 50, label="CPU", fill=COLOR_FILL))
    d.add(Arrow((cpu, "l"), (rom, "r"), kind="accent", label="reset address", label_pos=(550, 105)))
    d.add(Text(400, 255, "Gowin GW1N: no bitstream in this flash, bios_flash_offset = 0", size=12, italic=True))
    return d
