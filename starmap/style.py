"""Graphic design module for starmap rendering - Task 08."""


def star_colour(spectral: str) -> str:
    """Map spectral classes O B A F G K M along the real colour progression.
    
    Hot blue-white through to cool orange-red. Return #rrggbb hex string.
    Must not raise for unknown inputs.
    """
    if not isinstance(spectral, str):
        return "#ffffff"
    
    code = spectral.strip()[:1].upper()
    colours = {
        "O": "#9bb0ff",  # Deep blue-white
        "B": "#bbccff",  # Blue-white
        "A": "#f8f9ff",  # White
        "F": "#ffffed",  # Yellow-white
        "G": "#fff2a3",  # Yellow (Sun-like)
        "K": "#ffc58d",  # Light orange
        "M": "#ff8e6b",  # Cool orange-red
    }
    return colours.get(code, "#ffffff")


def star_radius(magnitude: float) -> float:
    """Turn magnitude into a radius using a non-linear curve.
    
    Bright stars (mag ~ -1 to 0) around 7-9 px, faint ones (mag ~ 5) around 1-2 px.
    Must return float between 0.1 and 40.0. Must not raise for invalid/unexpected inputs.
    """
    try:
        mag = float(magnitude)
    except (TypeError, ValueError):
        mag = 3.0

    # Exponential mapping for perception: r = A * exp(-B * mag)
    # Bright (mag = -1) -> ~8.5 px, faint (mag = 5) -> ~1.4 px
    r = 5.2 * (0.74 ** mag)
    
    # Ensure within safe bounds [0.1, 40.0]
    return max(0.1, min(40.0, float(r)))


def background() -> str:
    """Return a deep night celestial background colour (#rrggbb)."""
    return "#060913"
