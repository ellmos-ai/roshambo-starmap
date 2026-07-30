"""Coordinate grid for the invented sky (task 19).

Optional module, mirroring the renderer's other drop-in modules. It exposes
``grid_svg(width, height, project=None)`` which returns an SVG fragment of
faint meridians and parallels meant to sit behind everything else. If no
projection function is supplied, a plain equirectangular mapping (the
renderer's own fallback) is used.

Nothing here is astronomy; RA/dec are only a convenient way to place points.
The module must never raise: any internal error yields an empty fragment.
"""

from __future__ import annotations

_GRID_COLOUR = "#2a3a5c"
_GRID_OPACITY = "0.35"
_GRID_WIDTH = "0.6"
_SAMPLES_PER_LINE = 72


def _fallback_project(ra: float, dec: float, width: int, height: int) -> tuple[float, float]:
    return (ra / 360.0) * width, (0.5 - dec / 180.0) * height


def _polyline(points: list[tuple[float, float]]) -> str:
    pts = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return (
        f'<polyline points="{pts}" fill="none" stroke="{_GRID_COLOUR}" '
        f'stroke-width="{_GRID_WIDTH}" opacity="{_GRID_OPACITY}"/>'
    )


def grid_svg(width: int, height: int, project=None) -> str:
    """Return faint meridians and parallels as an SVG fragment.

    ``project`` may be a callable ``(ra_deg, dec_deg, width, height) -> (x, y)``;
    without one the equirectangular fallback is used. Returns ``""`` rather
    than raising on any problem.
    """
    try:
        w = float(width)
        h = float(height)
        if not (w > 0 and h > 0):
            return ""
        proj = project if callable(project) else _fallback_project

        parts: list[str] = []

        # Meridians: one per 30 degrees of RA, dec swept from -90 to +90.
        for ra in range(0, 360, 30):
            pts = []
            for i in range(_SAMPLES_PER_LINE + 1):
                dec = -90.0 + 180.0 * i / _SAMPLES_PER_LINE
                x, y = proj(float(ra), dec, w, h)
                pts.append((float(x), float(y)))
            parts.append(_polyline(pts))

        # Parallels: one per 30 degrees of dec from -60 to +60, RA swept 0-360.
        for dec in range(-60, 61, 30):
            pts = []
            for i in range(_SAMPLES_PER_LINE + 1):
                ra = 360.0 * i / _SAMPLES_PER_LINE
                x, y = proj(ra, float(dec), w, h)
                pts.append((float(x), float(y)))
            parts.append(_polyline(pts))

        return '<g id="grid">' + "".join(parts) + "</g>"
    except Exception:
        return ""
