#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# Flash boot image built by crcfbigen.py -f: a 32-bit length, the CRC32 of the payload, then the
# payload; the BIOS checks both before it copies or jumps.

from svgdiag import *


def build():
    d = Diagram(CANVAS_WIDTH, 130)
    x, y, h = 40, 40, 50
    d.add(Box(x,       y, 130, h, label="Length", radius=0, fill=COLOR_ACCENT))
    d.add(Box(x + 130, y, 130, h, label="CRC32", radius=0, fill=COLOR_ACCENT))
    d.add(Box(x + 260, y, 420, h, label="Payload (firmware binary)", radius=0, fill=COLOR_FILL))
    d.add(Text(x,       y - 14, "+0", size=12, anchor="start"))
    d.add(Text(x + 130, y - 14, "+4", size=12, anchor="start"))
    d.add(Text(x + 260, y - 14, "+8", size=12, anchor="start"))
    d.add(Text(x + 65,  y + h + 16, "32 bits", size=12))
    d.add(Text(x + 195, y + h + 16, "32 bits", size=12))
    d.add(Text(x + 470, y + h + 16, "length bytes", size=12))
    return d
