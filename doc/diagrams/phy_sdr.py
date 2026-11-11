#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# SDR PHY datapath: the output shift register drives the DQ lines through SDRTristate, the input
# shift register collects them, the clock generator drives SCK through SDROutput and gives the
# shift and sample strobes, CS control drives CS.

from svgdiag import *


def build():
    d = Diagram(CANVAS_WIDTH, 345)
    out_sr = d.add(Box(110, 40,  140, 50, label="Output\nshift register", fill=COLOR_ACCENT))
    in_sr  = d.add(Box(110, 130, 140, 50, label="Input\nshift register", fill=COLOR_ACCENT))
    tri    = d.add(Box(370, 40,  120, 140, label="SDRTristate", fill=COLOR_ACCENT_LIGHT))
    clkgen = d.add(Box(110, 220, 140, 50, label="Clock\ngenerator", fill=COLOR_ACCENT_LIGHT))
    sdrout = d.add(Box(370, 220, 120, 50, label="SDROutput", fill=COLOR_ACCENT_LIGHT))
    csc    = d.add(Box(110, 295, 140, 40, label="CS control", fill=COLOR_ACCENT_LIGHT))
    flash  = d.add(Box(640, 40, 100, 295, label="SPI\nflash", fill=COLOR_HARDWARE))
    d.add(Arrow((10, 65), (110, 65), kind="accent", label="sink"))
    d.add(Arrow((110, 155), (10, 155), kind="accent", label="source"))
    d.add(Arrow((250, 65), (370, 65), kind="accent", label="DQ out"))
    d.add(Arrow((370, 155), (250, 155), kind="accent", label="DQ in"))
    d.add(Arrow((490, 110), (640, 110), kind="data", heads="both", label="DQ0-DQ7"))
    d.add(Arrow((250, 255), (370, 255), kind="control", label="SCK"))
    d.add(Arrow((490, 255), (640, 255), kind="control", label="SCK"))
    d.add(Arrow((250, 315), (640, 315), kind="control", label="CS"))
    # Strobes: sample (input register) and shift (output register).
    d.add(Arrow((180, 220), (180, 180), kind="control", label="sample", label_side="right"))
    d.add(Arrow((250, 228), (230, 90), via=[(345, 228), (345, 112), (230, 112)], kind="control"))
    d.add(Text(351, 200, "shift", size=12, anchor="start"))
    return d
