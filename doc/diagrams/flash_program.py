#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# Programming a page: WREN sets the write enable latch, PP sends the address and up to a page of
# data, then RDSR is repeated until the write-in-progress bit returns to 0.

from primer_helpers import *


def build():
    d = Diagram(CANVAS_WIDTH, 165)
    x0 = 120
    g  = 12
    cmds = []
    x = x0 + 10
    # (DQ0 cells, DQ1 cells): each command is a list of (width, label, fill).
    seq = [
        ([(50, "WREN", COLOR_ACCENT)], []),
        ([(40, "PP", COLOR_ACCENT), (60, "address", COLOR_ACCENT_LIGHT), (90, "data", COLOR_ACCENT_LIGHT)], []),
        ([(45, "RDSR", COLOR_FILL)], [(45, "WIP=1", COLOR_SHADE)]),
        ([(45, "RDSR", COLOR_FILL)], [(45, "WIP=1", COLOR_SHADE)]),
        ([(45, "RDSR", COLOR_FILL)], [(45, "WIP=0", COLOR_ACCENT)]),
    ]
    lows = []
    for out, inp in seq:
        start = x
        cells(d, x, 70, out)
        x += sum(w for w, _, _ in out)
        cells(d, x, 110, inp)
        x += sum(w for w, _, _ in inp)
        lows.append((start - 5, x + 5))
        cmds.append((start, x))
        x += g
    row_name(d, x0, 30, "CS")
    level(d, x0, x + 10, 30, lows)
    row_name(d, x0, 70, "DQ0")
    row_name(d, x0, 110, "DQ1")
    span(d, cmds[2][0], cmds[4][1], 142, "WIP polling", side="below")
    return d
