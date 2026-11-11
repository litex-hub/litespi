#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# One MMAP read in mode 1-1-4 (8 dummy cycles) as four transfers on the core-to-PHY stream: the
# phase, the len/width/mask fields of each transfer and what the PHY returns. Cell widths follow
# the SCK cycles of each phase.

from phy_helpers import *


def build():
    d  = Diagram(CANVAS_WIDTH, 280)
    x0 = 170
    u  = 9 # px per SCK cycle.
    phases = [
        # (SCK cycles, phase, len, width, mask, returned, SCK cycles label)
        (8,  "Opcode",  "8",  "1", "0x01", "unused", "8"),
        (24, "Address", "24", "1", "0x01", "unused", "24"),
        (8,  "Dummy",   "8",  "1", "0x00", "unused", "8"),
        (8,  "Data",    "32", "4", "0x00", "word",   "8"),
    ]
    widths = [n*u for n, *_ in phases]
    x1 = x0 + sum(widths)
    # CS: high, low during the command, high again.
    row_name(d, x0 - 20, 30, "CS")
    d.add(Bus([(x0 - 20, 23), (x0, 23), (x0, 37), (x1, 37), (x1, 23), (x1 + 20, 23)], kind="control"))
    rows = [("Phase", 1), ("len", 2), ("width", 3), ("mask", 4), ("SCK cycles", 6), ("PHY returns", 5)]
    for i, (name, k) in enumerate(rows):
        y = 70 + 34*i
        row_name(d, x0, y, name)
        items = []
        for (n, *fields), w in zip(phases, widths):
            fill = COLOR_ACCENT if fields[0] == "Data" else COLOR_ACCENT_LIGHT
            items.append((w, fields[k - 1], fill if k in (1, 5) else COLOR_FILL))
        cells(d, x0, y, items)
    return d
