"""Static archive contract tests for roshambo-starmap GitHub Pages views."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class TestArchiveContract(unittest.TestCase):
    """Verify the static evidence views have no live network calls or backend claims."""

    def test_static_pages_enforce_offline_csp(self):
        for rel in ("replay/index.html", "planetarium.html"):
            with self.subTest(page=rel):
                html = (ROOT / rel).read_text(encoding="utf-8")
                self.assertIn('http-equiv="Content-Security-Policy"', html)
                self.assertIn("connect-src 'none'", html)
                self.assertIn("form-action 'none'", html)
                self.assertIn("archived static simulation", html.lower())
                self.assertIn("ausschließlich", html)

    def test_static_pages_contain_no_network_calls(self):
        forbidden = (
            "fetch(",
            "XMLHttpRequest",
            "WebSocket",
            "EventSource",
            "sendBeacon",
            "lambda-url",
        )
        for rel in ("replay/index.html", "planetarium.html"):
            with self.subTest(page=rel):
                html = (ROOT / rel).read_text(encoding="utf-8")
                for token in forbidden:
                    self.assertNotIn(token, html)

    def test_local_replay_data_files_exist(self):
        self.assertTrue((ROOT / "replay" / "data" / "data.js").is_file())
        self.assertTrue((ROOT / "replay" / "data" / "quotes.js").is_file())

    def test_readme_marks_competition_and_demo_archived(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Archived hackathon evidence", readme)
        self.assertIn("ausschließlich", readme)
        self.assertNotRegex(readme, re.compile(r"^Live demo of the Roshambo", re.MULTILINE))


if __name__ == "__main__":
    unittest.main()
