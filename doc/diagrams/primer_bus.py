#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# The SPI memory bus: one controller, one chip select per memory, a clock and up to eight data
# lines; in single-line SPI, DQ0 and DQ1 are MOSI and MISO; in quad SPI, WP# and HOLD# become DQ2/DQ3.

from svgdiag import *


def build():
    d = Diagram(CANVAS_WIDTH, 290)
    ctrl  = d.add(Box(20, 20, 160, 250, label="Controller\n(FPGA)", fill=COLOR_ACCENT))
    flash = d.add(Box(580, 20, 160, 250, label="SPI flash", fill=COLOR_HARDWARE))
    lines = [
        ("CS",              "end",  "control"),
        ("SCK",             "end",  "control"),
        ("DQ0 (MOSI)",      "both", "data"),
        ("DQ1 (MISO)",      "both", "data"),
        ("DQ2 (WP#)",       "both", "data"),
        ("DQ3 (HOLD#)",     "both", "data"),
        ("DQ4-DQ7 (octal)", "both", "feedback"),
    ]
    for i, (label, heads, kind) in enumerate(lines):
        y = 50 + i*33
        d.add(Arrow((180, y), (580, y), kind=kind, heads=heads, label=label))
    return d
