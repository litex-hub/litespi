#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# What add_spi_flash builds in a LiteX SoC: the PHY on the board pads, LiteSPI with its MMAP and
# master, a bus region for the MMAP, registers on the CSR bus and constants for the BIOS.

from svgdiag import *


def build():
    d = Diagram(CANVAS_WIDTH, 300)
    d.add(Container(225, 20, 300, 200, title="LiteSPI", title_pos="br"))
    cpu   = d.add(Box(10, 45, 90, 50, label="CPU"))
    csr   = d.add(Box(10, 135, 90, 50, label="CSR bus", fill=COLOR_ACCENT_LIGHT))
    mmap  = d.add(Box(245, 45, 110, 50, label="MMAP", fill=COLOR_ACCENT))
    mst   = d.add(Box(245, 135, 110, 50, label="Master", fill=COLOR_ACCENT))
    xbar  = d.add(Box(400, 45, 100, 140, label="Crossbar", fill=COLOR_ACCENT_LIGHT))
    phy   = d.add(Box(555, 90, 75, 50, label="PHY", fill=COLOR_ACCENT))
    flash = d.add(Box(665, 90, 85, 50, label="Flash", fill=COLOR_HARDWARE))
    bios  = d.add(Box(10, 235, 120, 50, label="BIOS", fill=COLOR_FILL))
    const = d.add(Box(245, 235, 140, 50, label="Constants", fill=COLOR_ACCENT_LIGHT))
    d.add(Arrow((cpu, "r"), (mmap, "l"), kind="accent", label="spiflash region", label_pos=(170, 55)))
    d.add(Arrow((csr, "r"), (mst, "l"), kind="control", label="registers", label_pos=(170, 145)))
    d.add(Arrow((mmap, "r"), (400, 70), kind="data", heads="both"))
    d.add(Arrow((mst, "r"), (400, 160), kind="data", heads="both"))
    d.add(Arrow((500, 115), (phy, "l"), kind="data", heads="both"))
    d.add(Arrow((phy, "r"), (flash, "l"), kind="data", heads="both", label="pads", label_pos=(647, 80)))
    d.add(Arrow((const, "l"), (bios, "r"), kind="control"))
    return d
