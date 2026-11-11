#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# MMAP read burst: the first bus read sends opcode, address and dummy phases, then the data; the
# reads at the next addresses only clock the data while CS stays low; CS rises after the idle
# timeout. Widths are illustrative, not to scale.

from mmap_helpers import *


def build():
    d = Diagram(CANVAS_WIDTH, 235)
    x0 = 120
    yb, ycs, ydq = 45, 105, 160
    row_name(d, x0, yb,  "Bus")
    row_name(d, x0, ycs, "CS")
    row_name(d, x0, ydq, "DQ")
    # Bus reads: one Wishbone read per 32-bit word.
    cells(d, x0, yb, [(265, "read word N", COLOR_ACCENT_LIGHT), (20, "", None),
        (75, "read N+1", COLOR_ACCENT_LIGHT), (20, "", None), (75, "read N+2", COLOR_ACCENT_LIGHT)])
    # SPI phases of the command, then one data phase per word.
    cells(d, x0 + 5, ydq, [(50, "opcode", COLOR_FILL), (90, "address", COLOR_FILL),
        (55, "dummy", COLOR_FILL), (60, "data N", COLOR_ACCENT), (30, "", None),
        (60, "data N+1", COLOR_ACCENT), (35, "", None), (60, "data N+2", COLOR_ACCENT)])
    end = x0 + 5 + 50 + 90 + 55 + 60 + 30 + 60 + 35 + 60
    level(d, x0, 740, ycs, [(x0 + 5, 700)])
    span(d, end, 700, ydq + 40, "idle timeout", side="below")
    return d
