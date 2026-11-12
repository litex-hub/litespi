#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# Separate LiteSPI clock domain: the frontends and the crossbar stay in sys, two asynchronous FIFOs
# carry the transfers (with the CS changes) and the returned words, and the PHY register values are
# resynchronized.

from svgdiag import *


def build():
    d  = Diagram(CANVAS_WIDTH, 300)
    xb = 385 # Clock domain boundary.
    d.add(Text(20,  25, "sys clock domain", size=15, italic=True, anchor="start"))
    d.add(Text(740, 25, "LiteSPI clock domain", size=15, italic=True, anchor="end"))
    fe    = d.add(Box(20,  60, 110, 150, label="Frontends", fill=COLOR_ACCENT_LIGHT))
    xbar  = d.add(Box(165, 60, 100, 150, label="Crossbar", fill=COLOR_ACCENT_LIGHT))
    tx    = d.add(Box(325, 60, 120, 50, label="AsyncFIFO\nTX and CS"))
    rx    = d.add(Box(325, 130, 120, 50, label="AsyncFIFO\nRX"))
    regs  = d.add(Box(165, 235, 100, 45, label="PHY\nregisters"))
    sync  = d.add(Box(325, 235, 120, 45, label="MultiReg"))
    phy   = d.add(Box(495, 60, 110, 220, label="PHY", fill=COLOR_ACCENT))
    flash = d.add(Box(650, 60, 90, 220, label="SPI\nflash", fill=COLOR_HARDWARE))
    d.add(Arrow((130, 135), (165, 135), kind="data", heads="both"))
    d.add(Arrow((265, 85), (325, 85), kind="accent"))
    d.add(Arrow((445, 85), (495, 85), kind="accent"))
    d.add(Arrow((495, 155), (445, 155), kind="data"))
    d.add(Arrow((325, 155), (265, 155), kind="data"))
    d.add(Arrow((265, 257), (325, 257), kind="control"))
    d.add(Arrow((445, 257), (495, 257), kind="control"))
    d.add(Arrow((605, 170), (650, 170), kind="data", heads="both"))
    for y0, y1 in ((35, 58), (112, 128), (182, 232), (282, 298)):
        d.add(Bus([(xb, y0), (xb, y1)], dash="1,3"))
    return d
