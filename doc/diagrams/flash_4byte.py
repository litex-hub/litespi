#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# 3-byte and 4-byte addresses: 24 bits reach the first 16 MiB; above, a 32 MiB flash needs a
# 4-byte address (4B opcodes, 4-byte mode or an extended address register).

from primer_helpers import *


def build():
    d = Diagram(CANVAS_WIDTH, 220)
    x, w = 200, 110
    row_name(d, x, 30, "3-byte address")
    cells(d, x + w, 30, [(w, "A23-A16", COLOR_ACCENT_LIGHT), (w, "A15-A8", COLOR_ACCENT_LIGHT),
        (w, "A7-A0", COLOR_ACCENT_LIGHT)], h=28)
    row_name(d, x, 75, "4-byte address")
    cells(d, x, 75, [(w, "A31-A24", COLOR_ACCENT), (w, "A23-A16", COLOR_ACCENT_LIGHT),
        (w, "A15-A8", COLOR_ACCENT_LIGHT), (w, "A7-A0", COLOR_ACCENT_LIGHT)], h=28)
    row_name(d, x, 160, "32 MiB flash")
    cells(d, x, 160, [(2*w, "first 16 MiB", COLOR_ACCENT_LIGHT), (2*w, "second 16 MiB", COLOR_ACCENT)],
        h=36)
    tick(d, x + 2*w, 120, 195)
    d.add(Text(x + 2*w, 110, "0x1000000", size=12))
    d.add(Text(x, 200, "0x0", size=12, anchor="start"))
    d.add(Text(x + 4*w, 200, "0x2000000", size=12, anchor="end"))
    return d
