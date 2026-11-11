#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# The same read in 1-1-4 (0x6b) and 1-4-4 (0xeb): wider address and data phases cut the number
# of SCK cycles; the gap of 1-4-4, mode bits plus dummy cycles, is given per chip by its datasheet.

from primer_helpers import *


def panel(d, y, name, opcode, addr_x4, gap, gap_label="dummy"):
    x0, c = 150, 12
    t = lambda n: x0 + n*c
    title(d, 15, y, name)
    row_name(d, x0, y + 35, "DQ0")
    row_name(d, x0, y + 61, "DQ1-DQ3")
    a = 6 if addr_x4 else 24
    size = 13 if gap_label == "dummy" else 10
    for row, first in ((y + 35, (8*c, opcode, COLOR_ACCENT)), (y + 61, (8*c, "", None))):
        address = (a*c, "address", COLOR_ACCENT_LIGHT) if (addr_x4 or row == y + 35) else (a*c, "", None)
        cells(d, t(0), row, [first, address], h=26)
        cells(d, t(8 + a), row, [(gap*c, gap_label, COLOR_SHADE)], h=26, size=size)
        cells(d, t(8 + a + gap), row, [(8*c, "data", COLOR_ACCENT)], h=26)
    return t, a


def build():
    d = Diagram(CANVAS_WIDTH, 250)
    t, a = panel(d, 20, "1-1-4", "0x6b", False, 8)
    span(d, t(0), t(8), 102, "8", side="below")
    span(d, t(8), t(8 + a), 102, "24", side="below")
    span(d, t(8 + a), t(16 + a), 102, "8", side="below")
    span(d, t(16 + a), t(24 + a), 102, "8: 4 bytes", side="below")
    t, a = panel(d, 140, "1-4-4", "0xeb", True, 6, "mode + dummy")
    span(d, t(0), t(8), 222, "8", side="below")
    span(d, t(8), t(8 + a), 222, "6", side="below")
    span(d, t(8 + a), t(14 + a), 222, "per chip", side="below")
    span(d, t(14 + a), t(22 + a), 222, "8: 4 bytes", side="below")
    return d
