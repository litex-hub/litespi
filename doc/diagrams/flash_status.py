#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# Status register 1 (ISSI, Macronix layout) and the second register (SR2 or CR1) with the quad
# enable bit: bit 6 of SR1 on some chips, bit 1 of the second register on others.

from primer_helpers import *


def register(d, y, name, labels, accent):
    x, w = 200, 65
    row_name(d, x, y, name)
    for i in range(8):
        d.add(Text(x + i*w + w/2, y - 30, str(7 - i), size=12))
    items = []
    for i, l in enumerate(labels):
        fill = COLOR_ACCENT if i in accent else (COLOR_SHADE if l == "" else COLOR_FILL)
        items.append((w, l, fill))
    cells(d, x, y, items, h=30, size=14)


def build():
    d = Diagram(CANVAS_WIDTH, 170)
    register(d, 50,  "SR1", ["SRWD", "QE", "BP3", "BP2", "BP1", "BP0", "WEL", "WIP"], (1,))
    register(d, 130, "SR2 or CR1", ["", "", "", "", "", "", "QE", ""], (6,))
    return d
