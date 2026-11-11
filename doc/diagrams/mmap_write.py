#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# MMAP write across a page boundary: the last word of a page goes out byte by byte after the
# program opcode and the address; the next word starts a new command (CS high, opcode, address)
# because it is the first word of the next page. Widths are illustrative, not to scale.

from mmap_helpers import *


def build():
    d = Diagram(CANVAS_WIDTH, 200)
    x0 = 100
    yb, ycs, ydq = 60, 115, 165
    bw = 46
    row_name(d, x0, yb,  "Bus")
    row_name(d, x0, ycs, "CS")
    row_name(d, x0, ydq, "DQ")
    cmd = [(40, "PP", COLOR_FILL), (80, "address", COLOR_FILL)]
    data = [(bw, f"byte {i}", COLOR_ACCENT) for i in range(4)]
    first  = x0 + 5
    second = first + 40 + 80 + 4*bw + 30
    cells(d, first,  ydq, cmd + data)
    cells(d, second, ydq, cmd + data)
    word = 40 + 80 + 4*bw + 10
    cells(d, first - 5,  yb, [(word, "write last word of page", COLOR_ACCENT_LIGHT)])
    cells(d, second - 5, yb, [(word, "write first word of next page", COLOR_ACCENT_LIGHT)])
    hi, lo = ycs - 7, ycs + 7
    d.add(Bus([(x0 - 5, hi), (first, hi), (first, lo), (second - 15, lo), (second - 15, hi),
        (second, hi), (second, lo), (second + word, lo)]))
    d.add(Text(second - 22, 22, "page boundary", size=12))
    d.add(Bus([(second - 22, 32), (second - 22, ydq + 15)], dash="2,3", color="#9a9a9a"))
    return d
