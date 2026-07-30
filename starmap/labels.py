"""Star name labels for the shared sky (task 20).

Labels only the brightest star of each constellation, small and unobtrusive.
Labels whose estimated bounding box would collide with an already-placed label
are skipped. Nothing here may raise -- a label module that can fail would put
holes in the time-lapse, so every input is guarded and worst case returns "".

The renderer calls ``labels_svg(width, height, constellations, project)`` if it
supports labels. ``project`` is optional; without it an equirectangular
fallback matching the renderer's own fallback is used.
"""

from __future__ import annotations

import math
from typing import Any, Callable

_CHAR_EM = 0.62  # rough width of one average glyph, in em
_FONT_SIZE = 11.0
_OFFSET = 10.0  # px between star centre and label anchor
_FILL = "#8a93b8"
_OPACITY = "0.75"


def _num(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    result = float(value)
    return None if math.isnan(result) or math.isinf(result) else result


def _fallback_project(ra: float, dec: float, width: int, height: int) -> tuple[float, float]:
    return (ra / 360.0) * width, (0.5 - dec / 180.0) * height


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _brightest_star(constellation: Any):
    """The star with the smallest magnitude value, or None."""
    try:
        stars = list(getattr(constellation, "stars", None) or [])
    except Exception:
        return None
    best = None
    best_mag = None
    for star in stars:
        mag = _num(getattr(star, "mag", None))
        if mag is None:
            continue
        if best_mag is None or mag < best_mag:
            best, best_mag = star, mag
    return best


def _label_text(constellation: Any, star: Any) -> str:
    """A short, unobtrusive label: the constellation name."""
    try:
        name = getattr(constellation, "name", None)
        if isinstance(name, str) and name.strip():
            return name.strip()
    except Exception:
        pass
    return ""


def _boxes_overlap(a: tuple[float, float, float, float], b: tuple[float, float, float, float]) -> bool:
    return a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]


def labels_svg(
    width: int,
    height: int,
    constellations: list,
    project: Callable[[float, float, int, int], tuple[float, float]] | None = None,
) -> str:
    """SVG fragment labelling the brightest star of each constellation.

    Returns only SVG elements, no ``<svg>`` wrapper. Returns ``""`` rather than
    raising on any problem, including an empty constellation list.
    """
    try:
        w = _num(width)
        h = _num(height)
        if w is None or h is None or w <= 0 or h <= 0:
            return ""
        items = list(constellations or [])
    except Exception:
        return ""
    if not items:
        return ""

    if project is None:
        project = _fallback_project

    placed: list[tuple[float, float, float, float]] = []
    parts: list[str] = []

    for constellation in items:
        try:
            star = _brightest_star(constellation)
            if star is None:
                continue
            ra = _num(getattr(star, "ra", None))
            dec = _num(getattr(star, "dec", None))
            if ra is None or dec is None:
                continue
            x, y = project(ra, dec, int(w), int(h))
            x, y = _num(x), _num(y)
            if x is None or y is None:
                continue
            text = _label_text(constellation, star)
            if not text:
                continue

            # Estimated bounding box, anchored left of and above the star.
            est_w = len(text) * _FONT_SIZE * _CHAR_EM
            est_h = _FONT_SIZE * 1.3
            lx, ly = x + _OFFSET, y - _OFFSET
            box = (lx, ly - est_h, lx + est_w, ly)

            # Skip labels that would collide or leave the canvas.
            if box[0] < 0 or box[1] < 0 or box[2] > w or box[3] > h:
                continue
            if any(_boxes_overlap(box, other) for other in placed):
                continue
            placed.append(box)

            parts.append(
                f'<text x="{lx:.1f}" y="{ly:.1f}" font-size="{_FONT_SIZE:.0f}" '
                f'fill="{_FILL}" opacity="{_OPACITY}" '
                f'font-family="Georgia, serif" font-style="italic">'
                f"{_escape(text)}</text>"
            )
        except Exception:
            continue

    return "\n".join(parts)
