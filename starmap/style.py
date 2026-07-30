def star_colour(spectral: str) -> str:
    """Map spectral class (O, B, A, F, G, K, M) to hex colour (#rrggbb)."""
    if not isinstance(spectral, str):
        return "#ffffff"
    c = spectral.strip().upper()
    if not c:
        return "#ffffff"
    first = c[0]
    colours = {
        "O": "#9bb0ff",
        "B": "#aabfff",
        "A": "#cad7ff",
        "F": "#f8f7ff",
        "G": "#fff4ea",
        "K": "#ffd2a1",
        "M": "#ffcc6f",
    }
    return colours.get(first, "#ffffff")


def star_radius(magnitude: float) -> float:
    """Turn magnitude into radius between 0.1 and 40."""
    try:
        mag = float(magnitude)
    except (ValueError, TypeError):
        mag = 2.5

    # Non-linear mapping: brighter stars (lower mag) are larger.
    # Mag around -1 => ~8.5px, Mag 0 => ~7.0px, Mag 2.5 => ~3.5px, Mag 5 => ~1.2px
    r = 7.0 * (10.0 ** (-0.15 * mag))
    return max(0.1, min(40.0, r))


def background() -> str:
    """Return a deep night colour for the background."""
    return "#0b0e14"

