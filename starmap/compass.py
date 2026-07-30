"""Compass rose and horizon marks for the shared sky (task 26).

Cardinal marks around the edge of the map, restrained: short ticks and one
letter per cardinal direction, tucked against the frame so they never fight
the map itself. Pure chart furniture -- the sky here is invented, and the
marks orient the reader, not the sky.

The renderer calls ``compass_svg(width, height)`` if it supports a compass.
Nothing in this module may raise; any problem returns "".
"""

from __future__ import annotations

import math
from typing import Any

_TICK = 14.0       # px, cardinal tick length
_SUBTICK = 7.0     # px, intercardinal tick length
_FONT_SIZE = 13.0
_INSET = 26.0      # px, letter distance from the edge
_STROKE = "#5a6488"
_FILL = "#6d77a0"
_OPACITY = "0.8"


def _num(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    result = float(value)
    return None if math.isnan(result) or math.isinf(result) else result


def compass_svg(width: int, height: int) -> str:
    """SVG fragment with cardinal marks around the map edge.

    Returns only SVG elements, no ``<svg>`` wrapper. Returns ``""`` rather
    than raising on any problem.
    """
    try:
        w = _num(width)
        h = _num(height)
        if w is None or h is None or w <= 2 * _INSET or h <= 2 * _INSET:
            return ""
    except Exception:
        return ""

    try:
        cx, cy = w / 2.0, h / 2.0
        parts: list[str] = []

        # Cardinal ticks: (letter, letter x, letter y, tick x1, y1, x2, y2, anchor)
        cardinals = [
            ("N", cx, _INSET, cx, 2.0, cx, 2.0 + _TICK, "middle"),
            ("S", cx, h - _INSET + _FONT_SIZE, cx, h - 2.0, cx, h - 2.0 - _TICK, "middle"),
            ("W", _INSET, cy, 2.0, cy, 2.0 + _TICK, cy, "middle"),
            ("E", w - _INSET, cy, w - 2.0, cy, w - 2.0 - _TICK, cy, "middle"),
        ]
        for letter, lx, ly, x1, y1, x2, y2, anchor in cardinals:
            parts.append(
                f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                f'stroke="{_STROKE}" stroke-width="1.5" opacity="{_OPACITY}"/>'
            )
            parts.append(
                f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="{_FONT_SIZE:.0f}" '
                f'fill="{_FILL}" opacity="{_OPACITY}" text-anchor="{anchor}" '
                f'font-family="Georgia, serif">{letter}</text>'
            )

        # Intercardinal subticks, no letters -- restrained.
        for sx, sy, ex, ey in [
            (2.0, 2.0, 2.0 + _SUBTICK, 2.0 + _SUBTICK),
            (w - 2.0, 2.0, w - 2.0 - _SUBTICK, 2.0 + _SUBTICK),
            (2.0, h - 2.0, 2.0 + _SUBTICK, h - 2.0 - _SUBTICK),
            (w - 2.0, h - 2.0, w - 2.0 - _SUBTICK, h - 2.0 - _SUBTICK),
        ]:
            parts.append(
                f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
                f'stroke="{_STROKE}" stroke-width="1" opacity="{_OPACITY}"/>'
            )

        return "\n".join(parts)
    except Exception:
        return ""
