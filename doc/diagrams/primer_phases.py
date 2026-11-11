#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# One 1-1-1 FAST_READ (0x0b) command: CS low, opcode and address shifted out on DQ0, dummy cycles
# with no line driven, then data shifted in on DQ1, one bit per SCK cycle.

from primer_helpers import *


def build():
    d = Diagram(CANVAS_WIDTH, 200)
    x0, c, lead = 130, 10, 20
    t = lambda n: x0 + lead + n*c
    n = 8 + 24 + 8 + 16
    row_name(d, x0, 55, "CS")
    level(d, x0, t(n) + 25, 55, [(x0 + 10, t(n) + 10)])
    row_name(d, x0, 95, "SCK")
    clock(d, x0, 95, c, n, h=12, lead=lead, tail=25)
    row_name(d, x0, 135, "DQ0 (MOSI)")
    cells(d, t(0), 135, [(8*c, "0x0b", COLOR_ACCENT), (24*c, "address", COLOR_ACCENT_LIGHT),
        (8*c, "dummy", COLOR_SHADE)])
    row_name(d, x0, 175, "DQ1 (MISO)")
    cells(d, t(32), 175, [(8*c, "", None), (8*c, "byte 0", COLOR_ACCENT),
        (8*c, "byte 1", COLOR_ACCENT_LIGHT)])
    span(d, t(0),  t(8),  20, "8 cycles")
    span(d, t(8),  t(32), 20, "24 cycles")
    span(d, t(32), t(40), 20, "8 cycles")
    span(d, t(40), t(56), 20, "8 cycles per byte")
    return d
