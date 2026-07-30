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

# Second wave — the southern sky and the finishing touches

The first twelve tasks are done. These continue the same sky. Same rules: nothing here is
astronomy, invent freely, do not change the renderer. Filenames stay fixed by task number.

## 13 — Constellation in the band Dec -20° to -50°, RA 0°–90°
Create `data/constellations/13-<slug>.json`. Southern sky: give it a different mood than
the northern ones — something heavier, older, or stranger.

## 14 — Constellation in the band Dec -20° to -50°, RA 90°–180°
Create `data/constellations/14-<slug>.json`.

## 15 — Constellation in the band Dec -20° to -50°, RA 180°–270°
Create `data/constellations/15-<slug>.json`.

## 16 — Constellation in the band Dec -20° to -50°, RA 270°–360°
Create `data/constellations/16-<slug>.json`.

## 17 — A faint scattering: unnamed background stars
Create `data/scatter.json` — a list of 60 to 120 faint stars with no constellation lines,
spread across the whole sphere. They give the sky depth. Keep magnitudes dim so they do
not compete with the named constellations.

## 18 — The river: a broad diffuse band
Create `data/river.json` — a wide, soft band of very faint stars following a curve across
the sky, the way a galaxy's disc would look from inside it. Invented, like everything else.

## 19 — Coordinate grid (optional module)
Create `starmap/grid.py`. The renderer picks it up automatically if present. Draw meridians
and parallels faintly, behind everything else. Must not raise on any input.

## 20 — Star names (optional module)
Create `starmap/labels.py`. Label only the brightest star of each constellation, small and
unobtrusive. Skip labels that would collide. Must not raise on any input.

## 21 — A catalogue page
Create `CATALOGUE.md` — one line per constellation: name, band, number of stars, and one
sentence of invented lore. Read the data files, do not guess what is in them.

## 22 — Provenance note
Create `PROVENANCE.md` — which agent built which task, read from the git history
(`git log --format='%h %an %s'`). Plain table, no interpretation, no invented entries.
