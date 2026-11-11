#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# Architecture: the two frontends, the crossbar, the optional clock domain crossing, the PHY
# (shift registers, clock generator, CS control) and the flash.

from svgdiag import *


def build():
    d = Diagram(CANVAS_WIDTH, 262)
    d.add(Container(115, 20, 365, 225, title="LiteSPI", title_pos="bl"))
    d.add(Container(500, 20, 145, 225, title="PHY", title_pos="bl"))
    mmap   = d.add(Box(135, 50,  105, 50, label="MMAP", fill=COLOR_ACCENT))
    master = d.add(Box(135, 130, 105, 50, label="Master", fill=COLOR_ACCENT))
    xbar   = d.add(Box(280, 50,  90, 130, label="Crossbar", fill=COLOR_ACCENT_LIGHT))
    cdc    = d.add(Box(395, 50,  70, 50, label="CDC\noptional"))
    sr     = d.add(Box(515, 45,  120, 50, label="Shift\nregisters", fill=COLOR_ACCENT_LIGHT))
    clk    = d.add(Box(515, 105, 120, 45, label="Clock\ngenerator", fill=COLOR_ACCENT_LIGHT))
    csc    = d.add(Box(515, 160, 120, 40, label="CS control", fill=COLOR_ACCENT_LIGHT))
    flash  = d.add(Box(690, 40, 60, 165, label="SPI\nflash", fill=COLOR_HARDWARE))
    d.add(Arrow((10, 75), (135, 75), kind="data", label="Wishbone"))
    d.add(Arrow((10, 155), (135, 155), kind="control", label="CSR bus"))
    d.add(Arrow((240, 75), (280, 75), kind="data", heads="both"))
    d.add(Arrow((240, 155), (280, 155), kind="data", heads="both"))
    d.add(Arrow((370, 75), (395, 75), kind="accent", heads="both"))
    d.add(Arrow((465, 70), (515, 70), kind="accent", heads="both"))
    d.add(Arrow((370, 175), (515, 175), kind="control", label="CS", label_pos=(445, 168)))
    d.add(Arrow((635, 70), (690, 70), kind="data", heads="both", label="DQ"))
    d.add(Arrow((635, 128), (690, 128), kind="control", label="SCK"))
    d.add(Arrow((635, 180), (690, 180), kind="control", label="CS"))
    return d
