"""Title block and legend for the starmap."""

from typing import Any

def legend_svg(width: int, height: int, constellations: list[Any]) -> str:
    """Return an SVG fragment containing title, legend, and magnitude key."""
    if not constellations:
        return ""

    elements = []

    # Title Block (Top-Left)
    elements.append('  <g id="title-block" transform="translate(35, 45)" font-family="sans-serif">')
    elements.append('    <text x="0" y="0" font-size="22" font-weight="bold" fill="#f0f4f8" letter-spacing="1.5">CELESTIAL MAP</text>')
    elements.append('    <text x="0" y="22" font-size="12" fill="#8b9bb4" font-style="italic">This sky is invented — created by independent agents.</text>')
    elements.append('  </g>')

    # Magnitude Key (Top-Left, below title)
    elements.append('  <g id="magnitude-key" transform="translate(35, 95)" font-family="sans-serif" font-size="11" fill="#a0aec0">')
    elements.append('    <text x="0" y="0" font-weight="bold" fill="#cbd5e0">Magnitude Scale:</text>')
    elements.append('    <circle cx="115" cy="-4" r="7" fill="#ffffff" opacity="0.95"/>')
    elements.append('    <text x="127" y="0">Mag -1</text>')
    elements.append('    <circle cx="185" cy="-4" r="4" fill="#ffffff" opacity="0.85"/>')
    elements.append('    <text x="195" y="0">Mag 2</text>')
    elements.append('    <circle cx="245" cy="-4" r="1.5" fill="#ffffff" opacity="0.75"/>')
    elements.append('    <text x="253" y="0">Mag 5</text>')
    elements.append('  </g>')

    # Constellation List (Top-Left, below magnitude key)
    elements.append('  <g id="constellation-legend" transform="translate(35, 135)" font-family="sans-serif" font-size="11" fill="#a0aec0">')
    elements.append('    <text x="0" y="0" font-weight="bold" fill="#cbd5e0">Constellations Present:</text>')

    y_offset = 20
    for c in constellations:
        name = getattr(c, 'name', 'Unknown')
        stars = getattr(c, 'stars', [])
        num_stars = len(stars)
        elements.append(f'    <text x="10" y="{y_offset}">{name} ({num_stars} stars)</text>')
        y_offset += 18

    elements.append('  </g>')

    return "\n".join(elements)


