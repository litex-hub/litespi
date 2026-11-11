#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# Shared helpers of the frontend and module figures (mmap_*.py, master_*.py, mod_*.py); no
# build(): not a figure.
#
# Timing rows: one horizontal row per signal (a name on the left, adjoining cells on a common time
# axis), chip select as a level line and spans for durations. Exchange lanes: vertical lifelines
# with horizontal messages between them.

from svgdiag import *


def row_name(d, x, y, name, size=13):
    """Signal name, right-aligned, left of a row whose cells start at x and are centred on y."""
    d.add(Text(x - 10, y, name, size=size, anchor="end"))


def cells(d, x, y, items, h=26, size=13):
    """Row of adjoining square cells: items is a list of (width, label, fill); fill None = gap."""
    out = []
    for w, label, fill in items:
        if fill is not None:
            out.append(d.add(Box(x, y - h/2, w, h, label=label, radius=0, fill=fill, size=size)))
        x += w
    return out


def level(d, x0, x1, y, lows, h=14):
    """Active-low strobe (CS): high from x0 to x1 except during the (start, end) spans of lows."""
    hi, lo = y - h/2, y + h/2
    pts = [(x0, hi)]
    for a, b in lows:
        pts += [(a, hi), (a, lo), (b, lo), (b, hi)]
    pts.append((x1, hi))
    d.add(Bus(pts, kind="control"))


def span(d, x0, x1, y, label, side="above"):
    """Double-headed horizontal arrow from x0 to x1 at y, with its label above or below."""
    d.add(Arrow((x0, y), (x1, y), heads="both", label=label, label_side=side))


class Lifelines:
    """Vertical lifelines with a title box on top of each; messages are horizontal arrows between
    two of them, one per row, the label above the arrow."""
    def __init__(self, d, titles, xs, fills, top=16, row=40, rows=4, bw=170):
        self.d, self.xs, self.row = d, xs, row
        self.y0 = top + 46 + row*0.75
        bottom  = top + 46 + row*(rows + 0.3)
        for title, x, fill in zip(titles, xs, fills):
            d.add(Box(x - bw/2, top, bw, 46, label=title, fill=fill))
            d.add(Bus([(x, top + 46), (x, bottom)], dash="4,3"))

    def y(self, n):
        return self.y0 + n*self.row

    def msg(self, n, a, b, label, kind="control"):
        """Message on row n from lifeline a to lifeline b (indexes)."""
        y  = self.y(n)
        xa = self.xs[a] + (4 if b > a else -4)
        xb = self.xs[b] + (-4 if b > a else 4)
        self.d.add(Arrow((xa, y), (xb, y), kind=kind, label=label,
            label_pos=((xa + xb)/2, y - 9), label_size=12))
