#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# Read of the JEDEC ID with the register master: software selects the chip, then each write of
# rxtx sends one 8-bit transfer and each read of rxtx returns the 8 bits shifted in during it.

from mmap_helpers import *


def build():
    rows = 8
    d  = Diagram(CANVAS_WIDTH, 16 + 46 + 40*(rows + 0.3) + 10)
    ll = Lifelines(d, ["Software", "Master and PHY", "Flash"], [110, 400, 670],
        [COLOR_ACCENT_LIGHT, COLOR_ACCENT, COLOR_HARDWARE], rows=rows, bw=160)
    ll.msg(0, 0, 1, "phyconfig: len 8, width 1, mask 1")
    ll.msg(1, 0, 1, "cs = 1")
    ll.msg(1, 1, 2, "CS low")
    ll.msg(2, 0, 1, "rxtx = 0x9f")
    ll.msg(2, 1, 2, "opcode, 8 SCK", kind="data")
    ll.msg(3, 1, 0, "status.rx_ready, read rxtx")
    ll.msg(4, 0, 1, "rxtx = 0x00")
    ll.msg(4, 2, 1, "manufacturer ID", kind="data")
    ll.msg(5, 1, 0, "read rxtx: first ID byte")
    ll.msg(6, 0, 1, "two more bytes")
    ll.msg(6, 2, 1, "type, capacity", kind="data")
    ll.msg(7, 0, 1, "cs = 0")
    ll.msg(7, 1, 2, "CS high")
    return d
