#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# SDR PHY clock paths: a regular SCK pin through SDROutput, or, for pads without a clock pin, one
# register then the 7-Series STARTUPE2 (CCLK pin) or the ECP5 USRMCLK (MCLK pin) primitive.

from svgdiag import *


def build():
    d = Diagram(CANVAS_WIDTH, 225)
    clk   = d.add(Box(20,  110, 130, 60, label="Clock\ngenerator", fill=COLOR_ACCENT))
    sdr   = d.add(Box(230, 25,  120, 40, label="SDROutput", fill=COLOR_ACCENT_LIGHT))
    reg   = d.add(Box(230, 120, 120, 40, label="Register", fill=COLOR_ACCENT_LIGHT))
    st2   = d.add(Box(420, 95,  120, 40, label="STARTUPE2", fill=COLOR_ACCENT_LIGHT))
    usr   = d.add(Box(420, 165, 120, 40, label="USRMCLK", fill=COLOR_ACCENT_LIGHT))
    pin   = d.add(Box(620, 25,  120, 40, label="SCK pin", fill=COLOR_HARDWARE))
    cclk  = d.add(Box(620, 95,  120, 40, label="CCLK pin", fill=COLOR_HARDWARE))
    mclk  = d.add(Box(620, 165, 120, 40, label="MCLK pin", fill=COLOR_HARDWARE))
    d.add(Arrow((85, 110), (230, 45), via=[(85, 45)], kind="control", label="pads.clk",
        label_pos=(155, 38)))
    d.add(Arrow((150, 140), (230, 140), kind="control", label="no clk pad"))
    d.add(Arrow((350, 140), (420, 115), via=[(385, 140), (385, 115)], kind="control"))
    d.add(Arrow((350, 140), (420, 185), via=[(385, 140), (385, 185)], kind="control"))
    d.add(Arrow((350, 45), (620, 45), kind="control"))
    d.add(Arrow((540, 115), (620, 115), kind="control", label="xc7*"))
    d.add(Arrow((540, 185), (620, 185), kind="control", label="LFE5U*"))
    return d
