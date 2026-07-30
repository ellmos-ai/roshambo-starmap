"""How the invented sky reads as a picture: colour, size, and the dark behind them.

The renderer draws every star as one filled circle, so these three functions carry the
whole visual language of the map. Two ideas shape them.

The first is that colour follows the temperature order O B A F G K M, from a hot
blue-white down to a cool orange-red, and that the ramp must stay *pale*. Stars are small
and bright against a dark field, and saturated hues at that size read as coloured
confetti rather than as light. So each class keeps a high floor on the channels it is not
using and shifts only as far as it has to; the sequence reads as one family seen at
different temperatures rather than as seven unrelated dots.

The second is that brightness is not linear in the eye. A straight line from magnitude to
radius makes the bright stars look timid and the faint ones look like a rash. The curve
below eases the fall instead: the first magnitudes separate strongly, where the figure of
a constellation is actually carried, and the faint tail settles gently onto a floor that
is still visible rather than vanishing.

Nothing here raises. The renderer feeds these functions whatever survived parsing --
an unknown spectral letter, a magnitude it had to invent -- and a picture that comes out
plainly is worth more than one that is correct and missing.

This sky is invented. The colours borrow the real temperature sequence only because the
eye already knows how to read it.
"""

from __future__ import annotations

import math

# The main sequence, hot to cool. Values are high and saturation is low on purpose:
# these are lights, not paint.
_SEQUENCE = {
    "O": "#8fb2ff",  # searing blue-white
    "B": "#a6c1ff",
    "A": "#c6d6ff",
    "F": "#eaeeff",  # the near-white hinge of the ramp
    "G": "#fff3dd",
    "K": "#ffc98a",
    "M": "#ff9564",  # cool orange-red, the far end
}

# Letters outside those seven, folded onto the nearest temperature so that a data file
# using them still draws something sensible instead of falling back to bare white.
_KINDRED = {
    "W": "#93b6ff",  # hotter than O, but the ramp has nowhere hotter to go
    "R": "#ff8f5e",
    "N": "#ff8858",
    "S": "#ff9d70",
    "C": "#ff8352",  # carbon: the reddest thing anyone in this sky claims to have seen
    "L": "#ef7a63",
    "T": "#d3707f",
    "Y": "#a86c99",  # barely a star at all; a bruise-coloured ember
}

# Anything unrecognised: a neutral white that sits between F and G, so an unclassified
# star looks like an ordinary one rather than like an error.
_UNCLASSIFIED = "#f4f5ff"

# Deep indigo rather than black. Pure black gives the eye no depth to sit in and flattens
# every colour placed on it; a night with a little blue left in it lets the cool stars
# stay cool and the warm ones glow.
_NIGHT = "#0b1026"

# The magnitude window the curve is drawn across, and the radii at its ends.
_MAG_BRIGHTEST = -1.5
_MAG_FAINTEST = 6.0
_RADIUS_MIN = 1.0
_RADIUS_MAX = 9.2

# Below 1.0 the fall is slower at the bright end and faster at the faint end than a
# straight line -- which is the way round that keeps the leading stars of a figure apart.
_CURVE = 1.35

# What an unreadable magnitude gets: the size of a thoroughly unremarkable star.
_RADIUS_DEFAULT = 3.4

# The renderer only accepts a radius inside this range, so the curve is clamped to it.
_RADIUS_FLOOR = 0.1
_RADIUS_CEILING = 40.0


def star_colour(spectral: str) -> str:
    """Return ``#rrggbb`` for a spectral class; neutral white for anything unknown.

    Only text is read as a class. Anything else is unclassified rather than coerced --
    ``str(None)`` begins with an N, and a missing class should not quietly become a
    carbon star.
    """
    if not isinstance(spectral, str):
        return _UNCLASSIFIED
    try:
        letter = spectral.strip()[:1].upper()
    except Exception:
        return _UNCLASSIFIED
    return _SEQUENCE.get(letter) or _KINDRED.get(letter) or _UNCLASSIFIED


def star_radius(magnitude: float) -> float:
    """Turn a magnitude into a circle radius in pixels, on an eased curve.

    Brighter is bigger, but not proportionally: magnitude -1 comes out near 8.5 px and
    magnitude 5 near 1.5 px, with the difference concentrated at the bright end where it
    does the drawing work. Values outside the window are clamped rather than refused.
    """
    try:
        mag = float(magnitude)
    except (TypeError, ValueError, OverflowError):
        return _RADIUS_DEFAULT
    if math.isnan(mag) or math.isinf(mag):
        return _RADIUS_DEFAULT

    span = _MAG_FAINTEST - _MAG_BRIGHTEST
    brightness = (_MAG_FAINTEST - mag) / span
    brightness = min(1.0, max(0.0, brightness))

    radius = _RADIUS_MIN + (_RADIUS_MAX - _RADIUS_MIN) * (brightness**_CURVE)
    return min(_RADIUS_CEILING, max(_RADIUS_FLOOR, radius))


def background() -> str:
    """Return the deep night the whole map is drawn on."""
    return _NIGHT
