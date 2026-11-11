#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# The steps of spiflash_init() in the LiteX BIOS, left to right; the master-based steps are
# skipped when the SoC has no master, quad and QPI steps when the module is not capable. A failed
# quad enable stops the initialization: no QPI entry, no calibration, no memspeed.

from svgdiag import *


def build():
    d = Diagram(CANVAS_WIDTH, 240)
    steps = [
        ("Print\nmodule",     COLOR_FILL),
        ("Send RDID",         COLOR_ACCENT_LIGHT),
        ("Quad\nenable",      COLOR_ACCENT_LIGHT),
        ("QPI\nentry",        COLOR_ACCENT_LIGHT),
        ("Clock\ncalibration", COLOR_ACCENT),
        ("memspeed",          COLOR_FILL),
    ]
    w, gap, x0, y = 100, 28, 10, 50
    boxes = []
    for i, (label, fill) in enumerate(steps):
        boxes.append(d.add(Box(x0 + i*(w + gap), y, w, 60, label=label, fill=fill)))
    for a, b in zip(boxes, boxes[1:]):
        d.add(Arrow((a, "r"), (b, "l"), kind="data"))
    d.add(Text(x0 + 1.5*(w + gap) + w/2 + w/2 + gap/2, 18, "master required", size=12, italic=True))
    d.add(Bus([(x0 + w + gap, 32), (x0 + 4*(w + gap) - gap, 32)], kind="control"))
    xq = x0 + 2*(w + gap)
    stop = d.add(Box(xq, 160, w, 50, label="Error,\nstop", fill=COLOR_FILL))
    d.add(Arrow((boxes[2], "b"), (stop, "t"), kind="control", label="fails", label_pos=(xq + w/2 + 26, 140)))
    return d
