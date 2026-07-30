"""Stereographic projection about the north celestial pole.

The sky here is invented, so this is not astronomy -- but the mathematics is the real
thing. Right ascension and declination name a point on a sphere, and this maps that
sphere onto the flat canvas the way a planisphere does: put the eye at the south pole,
put a plane across the north pole, and draw the line between the eye and the point. Where
that line crosses the plane is where the point goes.

The whole construction collapses to one radius:

    r(dec) = tan((90 - dec) / 2)

which is zero at the north pole and grows without bound towards the south one. Two
properties fall straight out of that and are worth stating, because they are what makes
the picture read as a sky rather than a scatter plot:

  * `r` depends on declination alone, so every star at one declination lands on one
    circle around the centre -- the parallels stay parallel.
  * The map is conformal: small shapes keep their angles, so a constellation drawn near
    the rim is stretched but not sheared, and still looks like itself.

The divergence at the south pole is the one thing a real chart cannot draw, and every
planisphere handles it the same way: it stops. `DEC_LIMIT` is that stopping point -- the
horizon of this map. Inside it the projection is exact; a point below it is pinned to the
rim rather than flung off the canvas, which keeps the promise that nothing lands
off-screen without pretending the pole is reachable.

Framing is deliberately not done here. The renderer rescales the finished drawing to fill
the canvas, and it can only do that faithfully because this returns a shape, not a
layout: one uniform scale and one translation away from its final position.
"""

from __future__ import annotations

import math

# The horizon of the map. Declinations below this are pinned to the rim, because
# r(dec) diverges at dec = -90 and no finite canvas can hold it. Chosen with room to
# spare below the -60 the constellation data uses, so real stars are projected exactly
# and only genuinely out-of-range ones are clamped.
DEC_LIMIT = -70.0

# The rim sits fractionally inside the shorter half-axis rather than exactly on it, so a
# star drawn at the very edge keeps its full disc on the canvas instead of half of it.
EDGE_INSET = 0.98

# r(DEC_LIMIT): the projected radius the rim corresponds to, in units of the tangent
# formula above. Everything is scaled by this, so it must never be zero.
_R_LIMIT = math.tan(math.radians((90.0 - DEC_LIMIT) / 2.0))


def _finite(value: float) -> float | None:
    """Coerce to a finite float, or None if that is not possible.

    Called for every star, including whatever a hand-written data file happens to
    contain, so it swallows the type errors rather than letting them reach the renderer.
    """
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(result) or math.isinf(result) else result


def polar_radius(dec_deg: float) -> float:
    """The stereographic radius for a declination, normalised so the rim is 1.0.

    Exposed separately because it is the whole of the projection's mathematics: the
    angular part below is just a rotation. Monotonically increasing as declination falls,
    0.0 at the north pole, 1.0 at `DEC_LIMIT` and clamped there below it.
    """
    dec = _finite(dec_deg)
    if dec is None:
        return 0.0
    # Clamp before the tangent rather than after: at dec = -90 the argument is exactly
    # 90 degrees, where tan is undefined and floating point returns a huge number rather
    # than raising. Guarding the input keeps the failure impossible instead of merely
    # unlikely.
    dec = max(DEC_LIMIT, min(90.0, dec))
    if _R_LIMIT <= 0.0:  # unreachable while DEC_LIMIT > -90, but the division below is
        return 0.0  # only safe because of this
    return math.tan(math.radians((90.0 - dec) / 2.0)) / _R_LIMIT


def project(ra_deg: float, dec_deg: float, width: int, height: int) -> tuple[float, float]:
    """Map a point on the celestial sphere to pixel coordinates."""
    w = _finite(width)
    h = _finite(height)
    if w is None or h is None or w <= 0.0 or h <= 0.0:
        # No canvas to speak of. Returning the origin is meaningless but harmless, and
        # the contract is that this never raises.
        return 0.0, 0.0

    centre_x = w / 2.0
    centre_y = h / 2.0

    ra = _finite(ra_deg)
    if ra is None:
        return centre_x, centre_y

    radius = polar_radius(dec_deg) * min(w, h) / 2.0 * EDGE_INSET

    # Right ascension increases anticlockwise on the canvas, which is what you see
    # looking up at the pole rather than down at a globe. RA = 0 points to the top.
    angle = math.radians(ra % 360.0)
    x = centre_x - radius * math.sin(angle)
    y = centre_y - radius * math.cos(angle)
    return x, y
