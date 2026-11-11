#
# This file is part of LiteSPI.
#
# Copyright (c) 2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# Pin-level read test (test/test_flash_model.py): Wishbone reads go through the real LiteSPI and SDR
# PHY to the flash model; the shared DQ lines are split into controller and flash sides, and a bus
# monitor checks that the two sides never drive the same line.

from svgdiag import *


def build():
    d = Diagram(CANVAS_WIDTH, 300)
    d.add(Container(10, 10, 740, 280, title="Migen simulation", title_pos="bl"))
    reads   = d.add(Box(30,  50, 120, 50, label="Wishbone reads", fill=COLOR_FILL))
    core    = d.add(Box(215, 50, 120, 50, label="LiteSPI MMAP", fill=COLOR_ACCENT_LIGHT))
    phy     = d.add(Box(400, 50, 120, 50, label="SDR PHY", fill=COLOR_ACCENT))
    split   = d.add(Box(585, 50, 140, 50, label="Split DQ", fill=COLOR_FILL))
    model   = d.add(Box(585, 180, 140, 50, label="Flash model", fill=COLOR_ACCENT))
    memory  = d.add(Box(400, 180, 120, 50, label="Memory (bytes)", fill=COLOR_FILL))
    monitor = d.add(Box(30, 180, 150, 50, label="Bus monitor\n(oe collision)", fill=COLOR_FILL))
    d.add(Arrow((reads, "r"), (core, "l"), kind="data", heads="both", label="read(n)",
        label_pos=(182, 38)))
    d.add(Arrow((core, "r"), (phy, "l"), kind="data", heads="both", label="transfers (crossbar)",
        label_pos=(367, 38)))
    d.add(Arrow((phy, "r"), (split, "l"), kind="accent", heads="both", label="SCK, CS, DQ",
        label_pos=(552, 38)))
    d.add(Arrow((split, "b"), (model, "t"), kind="accent", heads="both", label="dq_i, dq_o, dq_oe",
        label_pos=(575, 128)))
    d.add(Arrow((memory, "r"), (model, "l"), kind="data", heads="end", label="contents",
        label_pos=(552, 168)))
    d.add(Arrow((655, 150), (105, 180), kind="control", via=[(105, 150)],
        label="oe of both sides", label_pos=(290, 140)))
    return d
