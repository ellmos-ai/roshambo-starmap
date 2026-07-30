import math

def project(ra_deg: float, dec_deg: float, width: int, height: int) -> tuple[float, float]:
    """Map a point on the celestial sphere to pixel coordinates."""
    # Clamp / normalise inputs safely
    # dec = +90 is north celestial pole, mapped to exact centre (width / 2, height / 2)
    # stereographic projection from South Pole (or standard polar stereographic projection down to equator / dec bounds):
    # Co-latitude theta = 90 - dec (in degrees). At North Pole dec=90, theta=0.
    # Radius r = R * tan(theta / 2), where theta = (90 - dec) in radians.
    # For dec = +90: theta = 0 => r = 0.
    # For dec = -60 (the lower bound of stars): theta = 150 deg => tan(75 deg) ~= 3.732.
    # To fit within canvas (min dimension = min(width, height)):
    # Let max radius fit within half of the canvas min dimension with some padding, e.g., radius_at_dec_minus_60 = min(width, height) * 0.45
    # Then R = radius_at_dec_minus_60 / tan(75 deg).
    
    # Ensure declination is safely handled (-90 <= dec <= 90)
    dec_clamped = max(-90.0, min(90.0, float(dec_deg)))
    ra_float = float(ra_deg) % 360.0
    
    cx = width / 2.0
    cy = height / 2.0
    
    # Avoid division by zero or tan near 180 deg (dec = -90 is south pole)
    # theta in radians from North Pole (dec = 90)
    theta_rad = math.radians(90.0 - dec_clamped) / 2.0
    
    # Max theta for dec >= -60 is (90 - (-60))/2 = 75 deg = 1.308996 rad
    # We choose scale factor so that dec = -60 maps to ~45% of min(width, height)
    max_radius = min(width, height) * 0.45
    tan_max = math.tan(math.radians(75.0)) # ~3.73205
    scale = max_radius / tan_max
    
    r = scale * math.tan(theta_rad)
    
    # Convert RA to angle in radians. standard: RA increases counter-clockwise or clockwise
    ra_rad = math.radians(ra_float)
    
    # Standard orientation: North top, East left (or standard polar map)
    # x = cx - r * sin(ra_rad)
    # y = cy + r * cos(ra_rad)
    x = cx - r * math.sin(ra_rad)
    y = cy + r * math.cos(ra_rad)
    
    return (x, y)
