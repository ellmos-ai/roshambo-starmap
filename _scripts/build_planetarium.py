"""Regenerate the embedded data block of planetarium.html.

Reads the SAME data files render.py reads (data/constellations/*.json via
render.parse_constellation, so the dome shows exactly the stars the flat chart
shows, including the same forgiving skip rules), plus data/scatter.json,
data/river.json, data/curiosities.json, and _timelapse/frames.json.

Timelapse method (documented honestly, also in a comment inside planetarium.html):

  For every data file we ask git for the commit that first added it
  (`git log --diff-filter=A -- <file>`), then map that commit hash to a frame
  index in _timelapse/frames.json (which records one commit per frame).
  A constellation is visible in timelapse frame N iff its first-commit maps to
  a frame <= N. Edits after the first commit are ignored -- appearance order is
  what the timelapse shows.

  11 constellation files were committed AFTER the timelapse run ended
  (2026-07-30 23:35 UTC, frame 76), so their first commit has no frame. They
  are clamped to the final frame and flagged "after_timelapse": true -- they
  only appear at the very end of the run. This is why the dome's timelapse tops
  out at the chart's 29 constellations / 201 stars and the last frame adds the
  remaining files.

The script rewrites only the block between the GENERATED DATA markers in
planetarium.html. Everything else in that file is hand-written.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from render import parse_constellation  # noqa: E402  (same rules as the chart)

HTML = ROOT / "planetarium.html"
BEGIN = "<!-- BEGIN GENERATED DATA"
END = "<!-- END GENERATED DATA -->"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=ROOT, capture_output=True, text=True, check=True
    ).stdout.strip()


def first_commit(relpath: str) -> str | None:
    out = git("log", "--diff-filter=A", "--format=%H", "--", relpath)
    return out.split("\n")[-1] if out else None


def main() -> int:
    frames_raw = json.loads((ROOT / "_timelapse" / "frames.json").read_text(encoding="utf-8"))
    frames = [
        {
            "i": f["index"],
            "sha": f["sha"][:7],
            "at": f["committed_at"],
            "subject": f["subject"],
            "author": f["author"],
            "n_constellations": f["constellations"],
            "n_stars": f["stars"],
        }
        for f in frames_raw["frames"]
    ]
    sha2idx = {f["sha"]: f["index"] for f in frames_raw["frames"]}
    last_frame = frames[-1]["i"]

    def birth(relpath: str) -> tuple[int, bool]:
        sha = first_commit(relpath)
        if sha and sha in sha2idx:
            return sha2idx[sha], False
        return last_frame, True  # committed after the timelapse run

    constellations = []
    for path in sorted((ROOT / "data" / "constellations").glob("*.json")):
        parsed = parse_constellation(path)
        if parsed is None:
            continue
        frame, after = birth(f"data/constellations/{path.name}")
        constellations.append(
            {
                "slug": parsed.slug,
                "name": parsed.name,
                "abbr": parsed.abbr,
                "frame": frame,
                "after": after,
                "stars": [
                    {"id": s.id, "ra": s.ra, "dec": s.dec, "mag": s.mag, "sp": s.spectral}
                    for s in parsed.stars
                ],
                "lines": [list(line) for line in parsed.lines],
            }
        )

    def plain(relpath: str):
        data = json.loads((ROOT / relpath).read_text(encoding="utf-8"))
        frame, after = birth(relpath)
        return data, frame, after

    scatter, sc_frame, sc_after = plain("data/scatter.json")
    river, rv_frame, rv_after = plain("data/river.json")
    curiosities, cu_frame, cu_after = plain("data/curiosities.json")

    sky = {
        "method": (
            "birth frame = git first-add commit mapped into _timelapse/frames.json; "
            "files committed after the timelapse run are clamped to the last frame "
            "(after=true). See _scripts/build_planetarium.py."
        ),
        "last_frame": last_frame,
        "frames": frames,
        "constellations": constellations,
        "scatter": {"frame": sc_frame, "after": sc_after, "stars": scatter},
        "river": {"frame": rv_frame, "after": rv_after, "stars": river["stars"]},
        "curiosities": {
            "frame": cu_frame,
            "after": cu_after,
            "stars": [
                {
                    "id": c["id"],
                    "name": c["name"],
                    "ra": c["ra"],
                    "dec": c["dec"],
                    "mag": c["mag"],
                    "sp": c["spectral"],
                    "note": c["note"],
                }
                for c in curiosities
            ],
        },
    }

    html = HTML.read_text(encoding="utf-8")
    block = (
        f"{BEGIN} -- do not edit by hand; run _scripts/build_planetarium.py -->\n"
        f"<script>window.SKY_DATA = {json.dumps(sky, separators=(',', ':'))};</script>\n"
        f"{END}"
    )
    pre, rest = html.split(BEGIN, 1)
    _, post = rest.split(END, 1)
    HTML.write_text(pre + block + post, encoding="utf-8")

    n_after = sum(1 for c in constellations if c["after"])
    print(
        f"planetarium.html data block: {len(constellations)} constellations "
        f"({n_after} after timelapse), {sum(len(c['stars']) for c in constellations)} stars, "
        f"{len(scatter)} scatter, {len(river['stars'])} river, "
        f"{len(curiosities)} curiosities, {len(frames)} frames"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
