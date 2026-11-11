#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# The flash in the SoC address map: a region the size of the flash, served by the MMAP, next to
# ROM, SRAM and main RAM; the registers of the PHY, MMAP and master sit in the CSR region.

from svgdiag import *


def build():
    d = Diagram(CANVAS_WIDTH, 250)
    d.add(Text(320, 15, "CPU address space", size=15, italic=True))
    cpu = d.add(Box(10, 105, 90, 60, label="CPU", fill=COLOR_FILL))
    x, w, h, y = 240, 160, 40, 35
    regions = [
        ("ROM",       COLOR_FILL),
        ("SRAM",      COLOR_FILL),
        ("Main RAM",  COLOR_FILL),
        ("spiflash",  COLOR_ACCENT),
        ("CSR",       COLOR_ACCENT_LIGHT),
    ]
    boxes = {}
    for i, (label, fill) in enumerate(regions):
        boxes[label] = d.add(Box(x, y + i*h, w, h, label=label, radius=0, fill=fill))
    d.add(Arrow((cpu, "r"), (x, 135), kind="data", label="bus", label_pos=(170, 125)))
    mmap  = d.add(Box(470, 152, 100, 40, label="MMAP", fill=COLOR_ACCENT))
    flash = d.add(Box(640, 152, 110, 40, label="SPI flash", fill=COLOR_HARDWARE))
    regs  = d.add(Box(470, 200, 280, 36, label="PHY, MMAP, master registers", fill=COLOR_ACCENT_LIGHT))
    d.add(Arrow((x + w, 172), (mmap, "l"), kind="accent"))
    d.add(Arrow((mmap, "r"), (flash, "l"), kind="data", heads="both"))
    d.add(Arrow((x + w, 218), (regs, "l"), kind="control"))
    return d
