#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# Opcode name READ_1_1_4_4B split into its fields, and the module attribute each field sets when
# the opcode is the read command of a module (SpiNorFlashModule.read_opcode).

from mmap_helpers import *


def build():
    d = Diagram(CANVAS_WIDTH, 185)
    x0, y, h = 40, 30, 44
    w = 136
    fields = [("READ", COLOR_FILL), ("1", COLOR_ACCENT), ("1", COLOR_ACCENT),
        ("4", COLOR_ACCENT), ("4B", COLOR_ACCENT_LIGHT)]
    notes = [("operation", "read data"), ("cmd_width", "opcode lines"),
        ("addr_width", "address lines"), ("bus_width", "data lines"),
        ("addr_bits = 32", "4-byte address")]
    for i, ((label, fill), (attr, what)) in enumerate(zip(fields, notes)):
        x = x0 + i*w
        d.add(Box(x, y, w, h, label=label, radius=0, fill=fill, size=18))
        cx = x + w/2
        d.add(Arrow((cx, y + h), (cx, y + h + 50)))
        d.add(Text(cx, y + h + 68, attr, size=15))
        d.add(Text(cx, y + h + 92, what, size=13))
    return d
