#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# SPI modes 0 and 3: SCK idles low (mode 0) or high (mode 3); in both, the data changes on the
# falling edge and is sampled on the rising edge, so both modes sample at the same instants.

from primer_helpers import *


def build():
    d = Diagram(CANVAS_WIDTH, 230)
    x0, lead, p, n = 170, 40, 60, 8
    t = x0 + lead
    row_name(d, x0, 50, "CS")
    level(d, x0, t + n*p + 30, 50, [(x0 + 15, t + (n - 1)*p + p/2 + 10)])
    row_name(d, x0, 95, "SCK, mode 0")
    clock(d, x0, 95, p, n, lead=lead, tail=30)
    row_name(d, x0, 140, "SCK, mode 3")
    clock(d, x0, 140, p, n, idle_high=True, lead=lead - p/2, tail=30 + p/2)
    row_name(d, x0, 190, "DQ")
    cells(d, t - p/2, 190, [(p, f"bit {7 - i}", COLOR_ACCENT if i % 2 == 0 else COLOR_ACCENT_LIGHT)
        for i in range(n)])
    for i in range(n):
        tick(d, t + i*p, 72, 175)
    d.add(Text(t, 18, "sample on rising edges", size=12, anchor="start"))
    return d
