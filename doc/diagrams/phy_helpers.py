#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# Shared helpers of the architecture and PHY figures (no build(): not a figure).
#
# Timing rows: one horizontal row per signal (a name on the left, adjoining cells on a common time
# axis), clock rows drawn as square waves from explicit high intervals, and dotted time markers.

from svgdiag import *


def row_name(d, x, y, name, size=13):
    """Signal name, right-aligned, left of a row whose cells start at x and are centred on y."""
    d.add(Text(x - 10, y, name, size=size, anchor="end"))


def cells(d, x, y, items, h=24, size=13):
    """Row of adjoining square cells: items is a list of (width, label, fill); fill None = gap."""
    out = []
    for w, label, fill in items:
        if fill is not None:
            out.append(d.add(Box(x, y - h/2, w, h, label=label, radius=0, fill=fill, size=size)))
        x += w
    return out


def wave(d, x0, x1, y, highs, h=14):
    """Digital level from x0 to x1 centred on y: high during each (start, end) of highs."""
    hi, lo = y - h/2, y + h/2
    pts = [(x0, lo)]
    for a, b in highs:
        pts += [(a, lo), (a, hi), (b, hi), (b, lo)]
    pts.append((x1, lo))
    clean = [pts[0]]
    for p in pts[1:]:
        if abs(p[0] - clean[-1][0]) > 0.5 or abs(p[1] - clean[-1][1]) > 0.5:
            clean.append(p)
    d.add(Bus(clean, kind="control"))


def tick(d, x, y0, y1):
    """Dotted vertical marker (a time reference) from y0 to y1."""
    d.add(Bus([(x, y0), (x, y1)], dash="2,3", color="#9a9a9a"))
