# A sky, built together — task list

We are inventing a night sky. **None of this is astronomy.** The constellations do not
exist, the stars do not exist, and no coordinate here claims to describe the real sky.
Right ascension and declination are borrowed only as a convenient way to place a point
on a sphere. Invent freely — but invent something that looks good.

A fixed renderer turns the data into `starmap.svg`. You do not write the renderer and you
must not change it. You add data, and three of the tasks add an optional module the
renderer picks up automatically if it is present.

Tasks are listed in order. **Take the first one that is not yet done.**

---

**Filenames are fixed by task number**, so that anyone can see at a glance which tasks are
already done: a constellation task `NN` creates `data/constellations/NN-<slug>.json`, where
`<slug>` is yours to choose. Task 03 might produce `03-heron.json`. The three module tasks
have fixed names given below.

---

## 01 — Constellation in the band RA 0°–40°

Create `data/constellations/01-<slug>.json`. Invent a name with some character to it — a
lantern, a heron, a broken wheel — not "Constellation One".

```json
{
  "name": "The Lantern",
  "abbr": "Lan",
  "stars": [
    {"id": "lan-a", "ra": 12.4, "dec": 31.0, "mag": 1.2, "spectral": "B"},
    {"id": "lan-b", "ra": 19.8, "dec": 24.6, "mag": 2.8, "spectral": "K"}
  ],
  "lines": [["lan-a", "lan-b"]]
}
```

Rules that keep the picture readable:

- **5 to 8 stars.** Fewer looks empty, more looks like noise.
- **`ra` must stay inside your band**, `dec` between −60 and +60. Every task has its own
  band so the constellations do not pile up on each other.
- `mag` between −1 (very bright) and 5 (faint). Vary it — a figure where every star is
  the same size looks dead.
- `spectral` one of `O B A F G K M`.
- Every `id` unique and prefixed with your abbreviation.
- `lines` connect star ids into a recognisable figure. **A line to an id that does not
  exist is silently dropped**, so check your own ids.

## 02 — Constellation in the band RA 40°–80°

As task 01, different band, different name.

## 03 — Constellation in the band RA 80°–120°

As task 01, different band, different name.

## 04 — The projection (mathematics)

Create `starmap/projection.py` with exactly this function:

```python
def project(ra_deg: float, dec_deg: float, width: int, height: int) -> tuple[float, float]:
    """Map a point on the celestial sphere to pixel coordinates."""
```

Replace the renderer's flat fallback with a real **stereographic projection** about the
north celestial pole, scaled to fit the canvas and centred on it. Standard library only.

This task is about getting the mathematics right:

- The whole visible range must land inside the canvas — nothing off-screen.
- `dec = +90` maps to the exact centre of the canvas.
- Equal declinations must fall on a common circle around that centre.
- The function is called for every star, so it must not raise. Guard the pole and any
  division that could reach zero.

Add `tests/test_projection.py` checking the centre, one known circle, and the guard.

## 05 — Constellation in the band RA 120°–160°

As task 01.

## 06 — Constellation in the band RA 160°–200°

As task 01.

## 07 — Constellation in the band RA 200°–240°

As task 01.

## 08 — The look of the sky (graphic design)

Create `starmap/style.py` with exactly these three functions:

```python
def star_colour(spectral: str) -> str:   # "#rrggbb"
def star_radius(magnitude: float) -> float
def background() -> str:                 # "#rrggbb"
```

This task is about how the map *reads* as an image:

- `star_colour` maps the classes `O B A F G K M` along the real colour progression —
  hot blue-white through to cool orange-red. Return `#rrggbb`, six digits.
- `star_radius` turns magnitude into a radius. Brightness is not linear in the eye;
  a curve reads far better than a straight line. Bright stars around 7–9 px, faint
  ones around 1–2 px. Must return between 0.1 and 40.
- `background()` returns a deep night colour that the star colours sit well against.
  Not pure black — pure black flattens everything on it.

Neither function may raise for any input, including an unknown spectral letter.

## 09 — Constellation in the band RA 240°–280°

As task 01.

## 10 — Constellation in the band RA 280°–320°

As task 01.

## 11 — Constellation in the band RA 320°–360°

As task 01.

## 12 — Title block and legend (structure and wording)

Create `starmap/legend.py` with exactly this function:

```python
def legend_svg(width: int, height: int, constellations: list) -> str:
```

It returns a fragment of SVG that is dropped into the finished image. Each item in
`constellations` has `.name`, `.abbr`, `.stars` (each with `.mag` and `.spectral`) and
`.slug`.

This task is about structure and wording rather than drawing:

- A title block in the top-left: a title, and one line stating plainly that this sky is
  invented.
- A list of the constellations present, with the number of stars in each.
- A small key for the magnitude scale — three example dots, labelled.
- Keep it inside the canvas and clear of the middle, where the map is.
- Return `""` rather than raising if the list is empty.

Return only SVG elements, no `<svg>` wrapper and no `<?xml?>` header.

---

# Third wave

## 23 — Constellation in the far south, Dec below -50°
Create `data/constellations/23-<slug>.json`. The circumpolar south — invent something that
belongs to a sky no one in the north ever sees.

## 24 — Constellation in the far south, second one
Create `data/constellations/24-<slug>.json`. Different character to task 23.

## 25 — A double star and a variable
Create `data/curiosities.json` — two or three individual stars with a note each: one that is
really two, one whose brightness changes. Invented, like the rest of the sky.

## 26 — Compass rose and horizon marks (optional module)
Create `starmap/compass.py`. Cardinal marks around the edge of the map, restrained. The
renderer picks it up automatically if present. Must never raise.

## 27 — A reader's note
Create `READING-THE-MAP.md` — half a page explaining to a newcomer how to read this chart:
what the bands mean, why the sky is invented, what the magnitude key shows. Plain language,
no jargon, no invented astronomy.

---

# Fourth wave — using the CockroachDB Agent Skills

These tasks require the official skills repo at `C:\_Local_DEV\repos\cockroachdb-skills`
(clone it if missing: `git clone https://github.com/cockroachlabs/cockroachdb-skills.git`).
Read the SKILL.md of the skill you use, follow its own procedure, and validate against the
LIVE database — not from memory. Write findings into `_skills/` in this workspace.

Connect with the same DSN the agents use. Never paste credentials into a file.

## 28 — Query patterns review (skill: cockroachdb-sql)
Apply `skills/cockroachdb-query-and-schema-design/cockroachdb-sql` to the queries this
project runs (see `demo/queries.py` and `src/roshambo/` in the Roshambo repo, read-only).
Write `_skills/28-query-review.md`: which rule from `references/cockroachdb-rules/` you
applied, what you checked against the live DB, what passed, what did not. Negative results
are results — "nothing to fix, here is why" is a valid outcome if you show the evidence.

## 29 — Observability pass (skill: cockroachdb-observability-and-diagnostics)
Follow that skill against the live cluster. Write `_skills/29-observability.md`: what you
measured (real numbers), what it says about a swarm under contention.

## 30 — Performance and scaling read (skill: cockroachdb-performance-and-scaling)
Apply it to the `claims` and `audit_log` tables. Write `_skills/30-performance.md`.
Note: a known hotspot on `audit_log` is already documented in the Roshambo repo under
`docs/EVIDENCE-skills.md` — read it first and do NOT repeat it; look for something else.

## 31 — Cost and usage (skill: cockroachdb-cost-and-usage-management)
This ran on a Basic cluster with a request-unit budget. Apply the skill, write
`_skills/31-cost.md`: what this experiment actually consumed, measured, not estimated.
If a number is not measurable, say so instead of guessing.

## 32 — Resilience question (skill: cockroachdb-resilience-and-disaster-recovery)
What happens to held leases if a node or a client dies mid-claim? Apply the skill, check
what the schema and the lease TTL actually guarantee. Write `_skills/32-resilience.md`.

## 33 — Constellation in the far south, Dec below -50°
Still open from the third wave: create `data/constellations/23-<slug>.json`.
(Yes, file number 23 — the task list numbering and the file numbering are independent here.)
