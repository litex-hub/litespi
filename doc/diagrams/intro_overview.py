#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# LiteSPI at a glance: the CPU reads the flash through the MMAP (Wishbone) and drives any command
# through the master (registers); the crossbar shares the PHY; the PHY drives the flash pins.

from svgdiag import *


def build():
    d = Diagram(CANVAS_WIDTH, 230)
    d.add(Container(200, 15, 275, 200, title="LiteSPI core", title_pos="bl"))
    cpu   = d.add(Box(10,  40, 80, 135, label="CPU", fill=COLOR_FILL))
    mmap  = d.add(Box(215, 40, 110, 50, label="MMAP", fill=COLOR_ACCENT))
    mstr  = d.add(Box(215, 125, 110, 50, label="Master", fill=COLOR_ACCENT))
    xbar  = d.add(Box(365, 40, 90, 135, label="Crossbar", fill=COLOR_ACCENT))
    phy   = d.add(Box(520, 40, 90, 135, label="PHY", fill=COLOR_ACCENT_LIGHT))
    flash = d.add(Box(655, 40, 95, 135, label="SPI\nflash", fill=COLOR_HARDWARE))
    d.add(Arrow((90, 65), (215, 65), kind="data", heads="both", label="Wishbone"))
    d.add(Arrow((90, 150), (215, 150), kind="control", heads="both", label="CSR bus"))
    d.add(Arrow((325, 65), (365, 65), kind="data", heads="both"))
    d.add(Arrow((325, 150), (365, 150), kind="data", heads="both"))
    d.add(Arrow((xbar, "r"), (phy, "l"), kind="data", heads="both", label="stream",
        label_pos=(497, 95)))
    d.add(Arrow((phy, "r"), (flash, "l"), kind="accent", heads="both", label="pins",
        label_pos=(632, 95)))
    return d
