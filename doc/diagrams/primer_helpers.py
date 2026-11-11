#
# This file is part of LiteSPI.
#
# Copyright (c) 2020-2026 Florent Kermarrec <florent@enjoy-digital.fr>
# SPDX-License-Identifier: BSD-2-Clause
#
# Shared helpers of the primer figures (no build(): not a figure).
#
# Timing rows: one horizontal row per signal (a name on the left, adjoining cells on a common time
# axis), clock rows drawn as square waves, chip select as a level line, and spans (double-headed
# arrows) for the phase lengths.

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


def _clean(pts):
    """Drop consecutive duplicate points (zero-length segments)."""
    out = [pts[0]]
    for p in pts[1:]:
        if abs(p[0] - out[-1][0]) > 0.5 or abs(p[1] - out[-1][1]) > 0.5:
            out.append(p)
    return out


def clock(d, x, y, period, n, h=14, idle_high=False, lead=0, tail=0):
    """SCK: lead px idle, n periods, tail px idle. Idle low (mode 0) or idle high (mode 3).

    In both modes the data is sampled on the rising edges; a mode 0 period starts with its rising
    edge, a mode 3 period with its falling edge."""
    hi, lo = y - h/2, y + h/2
    idle = hi if idle_high else lo
    pts  = [(x, idle), (x + lead, idle)]
    t    = x + lead
    for i in range(n):
        a = t + i*period
        b = a + period/2
        if idle_high:
            pts += [(a, hi), (a, lo), (b, lo), (b, hi)]
        else:
            pts += [(a, lo), (a, hi), (b, hi), (b, lo)]
    end = t + n*period
    pts += [(end, idle), (end + tail, idle)]
    d.add(Bus(_clean(pts), kind="control"))


def level(d, x0, x1, y, lows, h=14):
    """Active-low strobe (CS): high from x0 to x1 except during the (start, end) spans of lows."""
    hi, lo = y - h/2, y + h/2
    pts = [(x0, hi)]
    for a, b in lows:
        pts += [(a, hi), (a, lo), (b, lo), (b, hi)]
    pts.append((x1, hi))
    d.add(Bus(_clean(pts), kind="control"))


def span(d, x0, x1, y, label, kind="control", side="above"):
    """Double-headed horizontal arrow from x0 to x1 at y, with its label above or below."""
    d.add(Arrow((x0, y), (x1, y), kind=kind, heads="both", label=label, label_side=side))


def tick(d, x, y0, y1):
    """Dotted vertical marker (a time reference) from y0 to y1."""
    d.add(Bus([(x, y0), (x, y1)], dash="2,3", color="#9a9a9a"))


def title(d, x, y, text):
    """Italic panel title, left-aligned."""
    d.add(Text(x, y, text, size=15, italic=True, anchor="start"))
