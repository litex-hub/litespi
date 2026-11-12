#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# MMAP flash write across a page boundary: WREN, then the last word of a page byte by byte after the
# program opcode and the address; the next word starts a new command because it is the first word
# of the next page, after RDSR polling (until WIP reads 0) and a new WREN. Each command has its own
# CS low period. Widths are illustrative, not to scale.

from mmap_helpers import *


def build():
    d = Diagram(CANVAS_WIDTH, 200)
    x0 = 100
    yb, ycs, ydq = 60, 115, 165
    gap = 14
    row_name(d, x0, yb,  "Bus")
    row_name(d, x0, ycs, "CS")
    row_name(d, x0, ydq, "DQ")
    program = [(36, "PP", COLOR_FILL), (60, "address", COLOR_FILL), (100, "bytes 0-3", COLOR_ACCENT)]
    commands = [
        [(50, "WREN", COLOR_FILL)],
        program,
        [(80, "RDSR, WIP", COLOR_FILL)],
        [(50, "WREN", COLOR_FILL)],
        program,
    ]
    x, lows = x0 + 5, []
    for command in commands:
        w = sum(c[0] for c in command)
        cells(d, x, ydq, command)
        lows.append((x, x + w))
        x += w + gap
    end = x - gap
    first_end  = lows[1][1]
    second_beg = lows[2][0]
    cells(d, lows[0][0], yb, [(first_end - lows[0][0], "write last word of page", COLOR_ACCENT_LIGHT)])
    cells(d, second_beg, yb, [(end - second_beg, "write first word of next page", COLOR_ACCENT_LIGHT)])
    level(d, x0 - 5, end + 5, ycs, lows)
    xp = first_end + gap/2
    d.add(Text(xp, 22, "page boundary", size=12))
    d.add(Bus([(xp, 32), (xp, ydq + 15)], dash="2,3", color="#9a9a9a"))
    return d
