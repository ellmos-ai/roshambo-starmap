import math
import pytest
from starmap.projection import project

def test_centre():
    # dec = +90 should map to the exact centre of the canvas
    width, height = 1600, 900
    x, y = project(0.0, 90.0, width, height)
    assert pytest.approx(x) == width / 2.0
    assert pytest.approx(y) == height / 2.0
    
    # RA variation at North pole should still map to centre
    x2, y2 = project(180.0, 90.0, width, height)
    assert pytest.approx(x2) == width / 2.0
    assert pytest.approx(y2) == height / 2.0

def test_equal_declination_circle():
    width, height = 1000, 1000
    cx, cy = width / 2.0, height / 2.0
    dec = 30.0
    
    # Points at same declination but different RAs should be equidistant from centre
    r_expected = None
    for ra in [0.0, 45.0, 90.0, 135.0, 180.0, 270.0]:
        x, y = project(ra, dec, width, height)
        r = math.hypot(x - cx, y - cy)
        if r_expected is None:
            r_expected = r
        else:
            assert pytest.approx(r, abs=1e-5) == r_expected

def test_guard_and_bounds():
    width, height = 800, 600
    # Guard against extreme / invalid inputs without raising exceptions
    coords_pole = project(0.0, -90.0, width, height)
    assert len(coords_pole) == 2
    assert isinstance(coords_pole[0], float)
    assert isinstance(coords_pole[1], float)
    
    # Check within canvas for dec between -60 and +90
    for dec in [-60.0, 0.0, 45.0, 90.0]:
        for ra in [0.0, 90.0, 180.0, 270.0]:
            x, y = project(ra, dec, width, height)
            assert 0 <= x <= width
            assert 0 <= y <= height
