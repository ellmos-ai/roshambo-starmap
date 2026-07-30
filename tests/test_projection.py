"""Tests for the stereographic projection.

Three things are worth pinning down, and they are the three the task asks for: the pole
lands dead centre, equal declinations land on a common circle, and nothing -- no input at
all -- makes the function raise. The last matters most in practice: the renderer calls
this once per star and treats an exception as a reason to fall back to a flat map, so a
projection that raises on one bad row silently degrades the whole picture.

Imported by path rather than as a package, because the workspace is not installed and the
renderer loads the module the same way.
"""

from __future__ import annotations

import importlib.util
import math
import unittest
from pathlib import Path

_MODULE_PATH = Path(__file__).resolve().parent.parent / "starmap" / "projection.py"
_spec = importlib.util.spec_from_file_location("_test_projection", _MODULE_PATH)
assert _spec is not None and _spec.loader is not None
projection = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(projection)

WIDTH = 1600
HEIGHT = 900


def _distance_from_centre(x: float, y: float, width: int = WIDTH, height: int = HEIGHT) -> float:
    return math.hypot(x - width / 2.0, y - height / 2.0)


class TestCentre(unittest.TestCase):
    """dec = +90 is the point the whole projection is built around."""

    def test_north_pole_is_the_exact_centre(self):
        for ra in (0.0, 90.0, 180.0, 270.0, 359.9):
            with self.subTest(ra=ra):
                x, y = projection.project(ra, 90.0, WIDTH, HEIGHT)
                # Exactly, not approximately: the radius is zero there, so every right
                # ascension has to collapse onto the same pixel.
                self.assertAlmostEqual(x, WIDTH / 2.0, places=9)
                self.assertAlmostEqual(y, HEIGHT / 2.0, places=9)

    def test_centre_holds_on_a_differently_shaped_canvas(self):
        x, y = projection.project(123.0, 90.0, 640, 640)
        self.assertAlmostEqual(x, 320.0, places=9)
        self.assertAlmostEqual(y, 320.0, places=9)


class TestCircles(unittest.TestCase):
    """Equal declinations must fall on a common circle around the centre."""

    def test_one_declination_is_one_circle(self):
        for dec in (60.0, 30.0, 0.0, -30.0, -60.0):
            with self.subTest(dec=dec):
                radii = [
                    _distance_from_centre(*projection.project(ra, dec, WIDTH, HEIGHT))
                    for ra in range(0, 360, 15)
                ]
                spread = max(radii) - min(radii)
                self.assertLess(spread, 1e-9, f"dec={dec} did not land on one circle")

    def test_the_circle_is_the_size_stereographic_projection_says_it_is(self):
        # The known case: the celestial equator. r(0) = tan(45 deg) = 1, against a rim of
        # r(DEC_LIMIT), so the equator sits at that ratio of the full radius.
        rim = min(WIDTH, HEIGHT) / 2.0 * projection.EDGE_INSET
        expected = rim * math.tan(math.radians(45.0)) / math.tan(
            math.radians((90.0 - projection.DEC_LIMIT) / 2.0)
        )
        measured = _distance_from_centre(*projection.project(0.0, 0.0, WIDTH, HEIGHT))
        self.assertAlmostEqual(measured, expected, places=9)

    def test_circles_grow_as_declination_falls(self):
        radii = [
            _distance_from_centre(*projection.project(45.0, dec, WIDTH, HEIGHT))
            for dec in (90.0, 60.0, 30.0, 0.0, -30.0, -60.0)
        ]
        for inner, outer in zip(radii, radii[1:]):
            self.assertLess(inner, outer)

    def test_right_ascension_goes_all_the_way_round(self):
        # A quarter turn of RA must be a quarter turn on the canvas -- if it were not,
        # the "common circle" tests above would still pass on a projection that folded.
        centre = (WIDTH / 2.0, HEIGHT / 2.0)
        top = projection.project(0.0, 0.0, WIDTH, HEIGHT)
        quarter = projection.project(90.0, 0.0, WIDTH, HEIGHT)
        v1 = (top[0] - centre[0], top[1] - centre[1])
        v2 = (quarter[0] - centre[0], quarter[1] - centre[1])
        self.assertAlmostEqual(v1[0] * v2[0] + v1[1] * v2[1], 0.0, places=6)


class TestEverythingFitsOnTheCanvas(unittest.TestCase):
    def test_no_point_in_the_visible_range_leaves_the_canvas(self):
        for dec in (90.0, 60.0, 0.0, -60.0, projection.DEC_LIMIT):
            for ra in range(0, 360, 10):
                x, y = projection.project(float(ra), dec, WIDTH, HEIGHT)
                with self.subTest(ra=ra, dec=dec):
                    self.assertGreaterEqual(x, 0.0)
                    self.assertLessEqual(x, WIDTH)
                    self.assertGreaterEqual(y, 0.0)
                    self.assertLessEqual(y, HEIGHT)

    def test_beyond_the_horizon_is_pinned_to_the_rim_not_flung_off(self):
        rim = min(WIDTH, HEIGHT) / 2.0 * projection.EDGE_INSET
        for dec in (projection.DEC_LIMIT - 1.0, -85.0, -90.0):
            with self.subTest(dec=dec):
                measured = _distance_from_centre(*projection.project(10.0, dec, WIDTH, HEIGHT))
                self.assertAlmostEqual(measured, rim, places=9)


class TestGuards(unittest.TestCase):
    """The renderer calls this for every star and treats a raise as a broken module."""

    def test_the_south_pole_does_not_divide_by_zero(self):
        # tan(90 deg) is where a naive implementation blows up. It must not.
        x, y = projection.project(0.0, -90.0, WIDTH, HEIGHT)
        self.assertTrue(math.isfinite(x) and math.isfinite(y))

    def test_no_input_raises(self):
        awkward = [
            (0.0, 90.0),
            (0.0, -90.0),
            (360.0, 0.0),
            (-45.0, 0.0),  # negative RA
            (1e12, 1e12),  # far out of range
            (float("nan"), 0.0),
            (0.0, float("nan")),
            (float("inf"), float("-inf")),
            (None, None),  # not numbers at all
            ("12", "34"),  # numeric strings
            ([], {}),  # nothing like a number
        ]
        for ra, dec in awkward:
            with self.subTest(ra=ra, dec=dec):
                x, y = projection.project(ra, dec, WIDTH, HEIGHT)
                self.assertTrue(math.isfinite(x), f"x not finite for {ra!r},{dec!r}")
                self.assertTrue(math.isfinite(y), f"y not finite for {ra!r},{dec!r}")

    def test_degenerate_canvas_does_not_raise(self):
        for width, height in ((0, 0), (-100, 50), (1, 1), (0, 900)):
            with self.subTest(width=width, height=height):
                x, y = projection.project(45.0, 30.0, width, height)
                self.assertTrue(math.isfinite(x) and math.isfinite(y))

    def test_returns_a_pair_of_floats(self):
        result = projection.project(10.0, 20.0, WIDTH, HEIGHT)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], float)
        self.assertIsInstance(result[1], float)


if __name__ == "__main__":
    unittest.main()
