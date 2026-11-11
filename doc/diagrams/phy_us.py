#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# UltraScale PHY (LiteSPIXilinxUSPHY): the SDR PHY core drives SCK and CS (registered in the core)
# and four DQ lines (registered in LiteSPISTARTUPE3) through the STARTUPE3 primitive to the
# configuration flash.

from svgdiag import *


def build():
    d = Diagram(CANVAS_WIDTH, 190)
    d.add(Container(205, 15, 370, 160, title="LiteSPISTARTUPE3", title_pos="bl"))
    core  = d.add(Box(20,  35, 140, 100, label="SDR PHY\ncore", fill=COLOR_ACCENT))
    regs  = d.add(Box(225, 80, 130, 55, label="DQ\nregisters", fill=COLOR_ACCENT_LIGHT))
    st3   = d.add(Box(425, 35, 130, 100, label="STARTUPE3", fill=COLOR_ACCENT_LIGHT))
    flash = d.add(Box(640, 35, 105, 100, label="Config\nflash", fill=COLOR_HARDWARE))
    d.add(Arrow((160, 55), (425, 55), kind="control", label="SCK, CS"))
    d.add(Arrow((160, 110), (225, 110), kind="data", heads="both"))
    d.add(Arrow((355, 110), (425, 110), kind="data", heads="both", label="DO, DTS, DI"))
    d.add(Arrow((555, 55), (640, 55), kind="control"))
    d.add(Arrow((555, 110), (640, 110), kind="data", heads="both", label="DQ0-DQ3",
        label_pos=(612, 100)))
    return d
