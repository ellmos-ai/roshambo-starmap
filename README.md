# A sky, built together — roshambo-starmap

**This is an invented night sky. None of it is astronomy.** Every constellation, every
star, every name here was made up by the agents that built this project. Right ascension
and declination are borrowed only as a convenient way to place a point on a sphere.
Do not look for these stars overhead; you will not find them.

This repository is the **evidence artefact** of a multi-vendor swarm experiment run for
the CockroachDB × AWS Hackathon. The coordination mechanism under test is
[Roshambo](https://github.com/ellmos-ai/roshambo) — leases on named resources, held in a
CockroachDB Cloud cluster. The product the swarm was asked to build together is
deliberately harmless: a star chart of a sky that does not exist.

## What you are looking at

27 registered participants — LLM agents from 5 vendors (Google, Anthropic, Moonshot,
Zhipu, MiniMax) plus scripted 200-line bot agents with no
model at all — ran on **2 machines** (ASUS-GEI and WORKSTATION-LG), claimed tasks through
Roshambo leases, and committed into this one repository. The bots matter as much as the
models: they register, claim, hold, release and adapt their rate exactly like an LLM
agent, because Roshambo coordinates *processes*, not "AI agents".

One name is missing on purpose: two OpenAI Codex instances were meant to be the sixth
vendor. They never made it into the game — a local Windows permission error stopped them
before registration, so they appear nowhere in the audit data. Their absence is part of
the record (`_logs/`), not something we smoothed over.

The result is `starmap.svg`: a stereographic chart of **29 invented constellation
figures, 201 stars**, plus background scatter and a faint river of light — and
`planetarium.html` (tasks 36–39), a walk-in dome view of the same data.

Numbers below are from `collect_evidence.py` against the live cluster, verified
2026-07-31. Nothing here is estimated:

- **4011** audit-log rows · **27** agents · **2** hosts
- **111** work trails (1 failure)
- **1226** genuine collisions (915 contention events), of which **147 cross-host**
  (94 events) — a process on one machine refused because a process on the *other*
  machine holds the lease
- **1245/1245** denials named the actual current holder
- 16 stale denials; 3 defect flags — **investigated and explained: detector artefacts,
  never two simultaneously live leases** (see `docs/EVIDENCE-defects.md` in the
  Roshambo repo)
- Earlier, lower counts in `_reports/` and the `evidence_*.json` snapshots are
  intermediate states of the same growing run, kept unedited on purpose.

## Repository layout

| Path | What it is |
|---|---|
| `starmap.svg` | The curated chart: 29 figures, 201 stars. State at the end of the field run. |
| `render.py` | The fixed renderer. Agents were not allowed to change it; they added data and optional modules. |
| `starmap/` | Optional renderer modules built by agents: projection, style, legend, labels, grid, compass. Each must never raise. |
| `data/constellations/` | One JSON per constellation task. Contains **parallel variants** — several agents were leased the same band at different times (two "Silver Loom"s, two "Obsidian Mirror"s). This is evidence of the coordination under contention, not a curated set. |
| `data/scatter.json`, `data/river.json`, `data/curiosities.json` | Background stars, the faint river, and two curiosities (a double star, a variable). |
| `TASKS.md` | The task list the swarm worked through (tasks 01–39). |
| `CATALOGUE.md` | Index and invented lore of the constellations. |
| `PROVENANCE.md` | Which agent built which task, read from git history. |
| `READING-THE-MAP.md` | Half a page on how to read the chart. |
| `_reports/` | Final reports of the participating agents and the coordinating operator — including the operator's own errors, recorded unedited. |
| `_skills/` | Findings from applying the official CockroachDB Agent Skills against the live cluster (tasks 28–32). |
| `_timelapse/` | 76 SVG frames rebuilt from git history: the sky as it grew, commit by commit. |
| `planetarium.html` | The dome: the same invented sky seen from inside (tasks 36–39). See below. |
| `evidence_*.json`, `bot*.json`, `*intervals*.csv` | Raw evidence snapshots from `collect_evidence.py` and bot runs at various points of the run. `botagent-intervals.csv` merges the adaptive-rate interval logs of both machines. |
| `tests/` | Unit tests for the projection module. |

## Task status (2026-07-31)

- Tasks **01–29 and 33**: built (27 of 33 chart tasks completed during the run, the rest after).
- Tasks **30–32**: **withdrawn by the coordinator.** They were assigned against CockroachDB
  skill directories that contained only `.gitkeep` at assignment time — a coordinator
  error, documented honestly in `_reports/operator_at_ASUS-GEI.md`. Two agents
  nevertheless produced real analyses; they are kept in `_skills/` as artefacts.
- Tasks **34–35**: never written.
- Tasks **36–39**: built — `planetarium.html`.

## The planetarium (`planetarium.html`)

Still an invented sky — now seen from inside. `planetarium.html` is a single
self-contained file: no build step, no CDN, no network. All data is embedded in
the file itself (regenerated from `data/` + git history by
`_scripts/build_planetarium.py`), so it opens by double-clicking, straight off
`file://`. The sphere maths is hand-rolled on a 2D canvas — no 3D library.

- **Look around:** drag with the mouse, zoom with the scroll wheel, turn with
  WASD or the arrow keys. Constellation names float at their centres; hovering a
  star shows its id, magnitude and spectral class.
- **Time and motion:** the sky turns slowly (space pauses it, `H` toggles the
  horizon ring). The horizon is invented too, and says so in the corner.
- **The build, seen from inside:** open `planetarium.html?timelapse=1` — the
  constellations appear in commit order (a slider scrubs the run, play/pause
  included). The mapping is honest: each data file's birth frame is the git
  commit that first added it, mapped into `_timelapse/frames.json`; files
  committed after that run ended are clamped to the last frame and flagged.
- **Video mode** (for pulling film frames, e.g. with headless Edge):
  `planetarium.html?t=30&chromeless=1` renders a deterministic camera flight —
  a slow orbit, then into two or three constellations and back out — where every
  pixel is a pure function of `t` (seconds), so screenshots are reproducible.
  `&dur=` sets the flight length, `&frame=N` pins a timelapse frame,
  `&yaw=&pitch=&fov=` pins the camera for stills. Example:

  ```
  msedge --headless=new --screenshot=frame.png --window-size=1920,1080 ^
    --virtual-time-budget=3000 "file:///.../planetarium.html?t=30&chromeless=1"
  ```

  Note: the dome reads the same data files the chart does — today that is all
  **40** constellation variants (268 stars), not the curated 29/201 of
  `starmap.svg`; the timelapse tops out at the chart's end state because the
  later files arrived after the timelapse run.
- **Morph mode** (the flat chart becomes the world): `planetarium.html?morph=1`
  opens on the flat stereographic chart exactly as `render.py` draws it — same
  projection, same fit, same palette and star sizes — holds it for three
  seconds, then bends it around the viewer (t=3–19) and flows on into the
  dome and the camera flight (t≥28). Every star travels one eased path from
  its chart position to its dome position; nothing is cut and no other data
  appears. With `&t=<s>&chromeless=1` the whole arc — flat, bending, dome,
  close-ups — is a deterministic function of `t`, ready for headless frame
  pulling. One honest caveat: a flat sky map is mirrored against any view from
  inside the sphere, so east and west swap during the bend; the shapes and
  names are the same throughout.

## Two evidence lines, one repository

The run started on two machines with **no common remote**, so the first hours produced
two independent repositories with unrelated histories. A shared remote was added
mid-run; nothing was replayed and no timestamps were rewritten. On 2026-07-31 the
`workstation-lg` line was merged into `master` (`--allow-unrelated-histories`): unique
files from both sides were kept, the workstation's earlier versions of shared code and
docs were superseded by the refined master versions, and the two machines'
`botagent-intervals.csv` logs were concatenated. The workstation branch and its full
history remain in this repository.

Re-running `python render.py` today draws **all** parallel variants from
`data/constellations/`, including the workstation line merged in later — the committed
`starmap.svg` is deliberately kept at the curated end-of-run state.

## Reproduce the coordination evidence

From the [Roshambo](https://github.com/ellmos-ai/roshambo) repository, with
`ROSHAMBO_DSN_FILE` set and `PYTHONPATH=src`:

```
python demo/multivendor/collect_evidence.py --swarm poc-starmap-2026-07-30
```

Anyone with a CockroachDB cluster — a free CockroachDB Cloud tier is enough — and **no
LLM key at all** can reproduce the core property, mutual exclusion with holder-named
denials, in about thirty seconds (the dry-run uses its own throwaway swarm):

```
python demo/multivendor/bot_agent.py --dry-run --bots 3
```

Live demo of the Roshambo coordinator on AWS Lambda:
https://xo7te46ion5mhwi6mhua6va7im0cotkk.lambda-url.eu-central-1.on.aws/

## One more time, for the avoidance of doubt

The sky in this repository is **invented**. It is a safe, neutral work product chosen so
that 27 processes could fight over leases without anything real being at stake. The
astronomy-looking vocabulary is a rendering convenience. The *coordination* is real;
the *stars* are not.

## License

MIT — see [LICENSE](LICENSE). The sky in this repository is invented; the
coordination that built it is not.
