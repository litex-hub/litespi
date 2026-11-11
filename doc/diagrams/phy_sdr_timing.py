#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# SDR PHY at divisors 2 and 4 (mode 0, x1, at the pins, I/O register delays left out): SCK is the
# system clock divided by the divisor, the PHY changes DQ on each falling edge of SCK and samples
# it on each rising edge (dotted markers).

from phy_helpers import *


def build():
    d  = Diagram(CANVAS_WIDTH, 250)
    x0 = 190
    p  = 40              # px per sys clock cycle.
    n  = 13              # sys clock cycles shown.
    x1 = x0 + n*p
    # sys clock.
    row_name(d, x0, 30, "sys clock")
    wave(d, x0, x1, 30, [(x0 + k*p, x0 + k*p + p/2) for k in range(n)])
    # Divisor 2: SCK period = 2 sys cycles, first rising edge one sys cycle after the start.
    for (y_sck, y_dq, div, label) in ((85, 125, 2, "divisor 2"), (185, 225, 4, "divisor 4")):
        half  = div*p//2
        rises = [x0 + half + k*div*p for k in range(n) if x0 + half + k*div*p + half <= x1 - p]
        row_name(d, x0, y_sck, f"SCK, {label}")
        wave(d, x0, x1, y_sck, [(r, r + half) for r in rises])
        row_name(d, x0, y_dq, "DQ")
        items = [(div*p, f"D{k}", COLOR_ACCENT if k % 2 == 0 else COLOR_ACCENT_LIGHT) for k in range(len(rises))]
        cells(d, x0, y_dq, items)
        for r in rises:
            tick(d, r, y_sck - 14, y_dq + 16)
    return d
