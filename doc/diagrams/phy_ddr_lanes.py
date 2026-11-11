#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# 1:2 PHY (mode 0, at the DDR I/O, register delays left out): SCK is the system clock gated by the
# transfer, lane 1 (o2, falling half) carries the new bit, lane 0 (o1, rising half) repeats it one
# cycle later, so the bit at the pin changes on SCK falling edges and is stable around each rising
# edge, where the flash samples it (dotted markers).

from phy_helpers import *


def build():
    d  = Diagram(CANVAS_WIDTH, 250)
    x0 = 190
    p  = 60              # px per sys clock cycle.
    n  = 9               # sys clock cycles shown.
    x1 = x0 + n*p
    row_name(d, x0, 30, "sys clock")
    wave(d, x0, x1, 30, [(x0 + k*p, x0 + k*p + p/2) for k in range(n)])
    # SCK: high during the first half of cycles 1 to 4 (four bits).
    row_name(d, x0, 75, "SCK")
    wave(d, x0, x1, 75, [(x0 + k*p, x0 + k*p + p/2) for k in range(1, 5)])
    # Lane 1 (o2): bit k in cycle k. Lane 0 (o1): bit k in cycle k + 1.
    fills = [COLOR_ACCENT, COLOR_ACCENT_LIGHT]
    row_name(d, x0, 120, "lane 1, o2")
    cells(d, x0, 120, [(p, f"D{k}", fills[k % 2]) for k in range(4)])
    row_name(d, x0, 160, "lane 0, o1")
    cells(d, x0 + p, 160, [(p, f"D{k}", fills[k % 2]) for k in range(4)])
    # Pin: o1 on the high half, o2 on the low half: bit k from mid cycle k to mid cycle k + 1.
    row_name(d, x0, 205, "DQ at pin")
    cells(d, x0 + p/2, 205, [(p, f"D{k}", fills[k % 2]) for k in range(4)])
    for k in range(1, 5):
        tick(d, x0 + k*p, 60, 220)
    return d
