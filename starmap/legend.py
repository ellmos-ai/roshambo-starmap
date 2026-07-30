"""Title block, constellation list, and legend SVG module for starmap."""

from __future__ import annotations


def legend_svg(width: int, height: int, constellations: list) -> str:
    """Render title block, constellation index, and magnitude key SVG elements.

    Returns an SVG fragment string (no root <svg> tag). Returns "" if constellations is empty.
    """
    if not constellations:
        return ""

    elements = []

    # 1. Title Block (top-left)
    elements.append('  <!-- Title Block -->')
    elements.append('  <g class="title-block">')
    elements.append(
        '    <text x="35" y="45" font-family="sans-serif" font-size="22" font-weight="bold" '
        'fill="#e2e8f0" letter-spacing="1.5">CELESTIAL STAR MAP</text>'
    )
    elements.append(
        '    <text x="35" y="66" font-family="sans-serif" font-size="11" font-style="italic" '
        'fill="#94a3b8">An invented nocturnal sky constructed by multi-agent coordination</text>'
    )
    elements.append('  </g>')

    # 2. Constellation Index (left column, below title)
    elements.append('  <!-- Constellation Index -->')
    elements.append('  <g class="constellation-list">')
    elements.append(
        '    <text x="35" y="100" font-family="sans-serif" font-size="13" font-weight="bold" '
        'fill="#cbd5e1">RECORDED CONSTELLATIONS</text>'
    )

    start_y = 120
    row_height = 18
    for idx, c in enumerate(constellations):
        y_pos = start_y + (idx * row_height)
        name = getattr(c, "name", "Unknown")
        abbr = getattr(c, "abbr", "???")
        stars_cnt = len(getattr(c, "stars", []))
        label = f"{abbr} — {name} ({stars_cnt} stars)"
        elements.append(
            f'    <text x="35" y="{y_pos}" font-family="sans-serif" font-size="11" '
            f'fill="#94a3b8">{label}</text>'
        )
    elements.append('  </g>')

    # 3. Magnitude Key (bottom-left)
    key_y = height - 40
    elements.append('  <!-- Magnitude Key -->')
    elements.append('  <g class="magnitude-key">')
    elements.append(
        f'    <text x="35" y="{key_y - 20}" font-family="sans-serif" font-size="12" '
        f'font-weight="bold" fill="#cbd5e1">MAGNITUDE SCALE</text>'
    )

    # Three sample magnitude dots: Mag 0 (r=6), Mag 2.5 (r=3.5), Mag 5 (r=1.5)
    dots = [
        (35 + 10, key_y, 6.0, "Mag 0.0"),
        (35 + 110, key_y, 3.5, "Mag 2.5"),
        (35 + 210, key_y, 1.5, "Mag 5.0"),
    ]

    for cx, cy, r, text_label in dots:
        elements.append(f'    <circle cx="{cx}" cy="{cy}" r="{r}" fill="#f8fafc" opacity="0.9"/>')
        elements.append(
            f'    <text x="{cx + 14}" y="{cy + 4}" font-family="sans-serif" font-size="10" '
            f'fill="#94a3b8">{text_label}</text>'
        )

    elements.append('  </g>')

    return "\n".join(elements)
