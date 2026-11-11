#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# Organisation of a 16 MiB SPI NOR flash: 256 blocks of 64 KiB, each made of 16 sectors of 4 KiB,
# each made of 16 pages of 256 bytes.

from primer_helpers import *


def row(d, y, name, labels, accent):
    x, w = 170, 125
    row_name(d, x, y, name)
    items = [(w, l, COLOR_ACCENT if i == accent else COLOR_FILL) for i, l in enumerate(labels)]
    cells(d, x, y, items, h=32, size=14)
    return x, w


def build():
    d = Diagram(CANVAS_WIDTH, 250)
    x, w = row(d, 40,  "Chip, 16 MiB",   ["block 0", "block 1", "...", "block 255"], 1)
    row(d, 125, "Block, 64 KiB", ["sector 0", "sector 1", "...", "sector 15"], 0)
    row(d, 210, "Sector, 4 KiB", ["page 0", "page 1", "...", "page 15"], 0)
    # Zoom lines: the accented cell of a row expands into the next row.
    tick(d, x + w,   56,  109)
    tick(d, x + 2*w, 56,  109)
    tick(d, x,       141, 194)
    tick(d, x + w,   141, 194)
    d.add(Text(x + 4*w + 15, 210, "256 B", size=13, anchor="start"))
    return d
