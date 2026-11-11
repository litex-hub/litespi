#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# Read state machine of LiteSPIMMAP (litespi/core/mmap.py): each phase is a pair of states (send
# the transfer, wait for its return); a read at the next address goes from IDLE straight to the
# data phase while CS is held.

from mmap_helpers import *


def build():
    d = Diagram(CANVAS_WIDTH, 290)
    w, h = 140, 52
    idle  = d.add(Box(20,  120, 120, h, label="IDLE", fill=COLOR_ACCENT))
    cmd   = d.add(Box(200, 30,  w, h, label="BURST-CMD\nCMD-RET"))
    addr  = d.add(Box(400, 30,  w, h, label="BURST-ADDR\nADDR-RET"))
    dummy = d.add(Box(600, 30,  w, h, label="DUMMY\nDUMMY-RET"))
    data  = d.add(Box(400, 220, w, h, label="BURST-REQ\nBURST-DAT", fill=COLOR_ACCENT))
    d.add(Arrow((80, 120), (200, 56), via=[(80, 56)], label="new command",
        label_pos=(140, 47)))
    d.add(Arrow((cmd, "r"), (addr, "l")))
    d.add(Arrow((addr, "r"), (dummy, "l"), label="dummy", label_pos=(570, 47)))
    d.add(Arrow((470, 82), (470, 220), label="no dummy", label_pos=(478, 125),
        label_anchor="start"))
    d.add(Arrow((670, 82), (540, 246), via=[(670, 246)]))
    d.add(Arrow((400, 256), (60, 172), via=[(60, 256)], label="ack word",
        label_pos=(230, 248)))
    d.add(Arrow((140, 146), (430, 220), via=[(430, 146)], kind="accent",
        label="next address, CS held", label_pos=(285, 137)))
    return d
