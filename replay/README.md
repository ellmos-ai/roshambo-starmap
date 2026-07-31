# Roshambo field-run replay — poc-starmap-2026-07-30

Deterministic replay of the real field run: 27 registered participants (5 vendors +
scripted BotAgents) on two machines (ASUS-GEI laptop, WORKSTATION-LG) coordinating
through CockroachDB leases while building an **invented** star chart. Every event on
screen comes from exported data — nothing is staged. The star chart itself is fiction
(see `TASKS.md`: "None of this is astronomy"); the coordination data is real.

## Play

Open `index.html` in any browser — double-click works (`file://`), a local web server
works too. Data loads via `<script src="data/data.js">` (a `window.ROSHAMBO_DATA`
bundle), so no fetch/CORS issues exist under `file://`.

Controls: Play/Pause (or Space), speed 1×/10×/60×/240×, seek slider, chapter jump
buttons. Total replay time: 5498.6 s (22:04:03 → 23:35:41 UTC, 2026-07-30).

## Render frames (deterministic, for filming)

`index.html?t=<seconds>&chromeless=1` renders exactly the state at sim-time t
(sim-time 0 = first audit line, 2026-07-30T22:04:03.032Z), no controls, no animations.

```bat
"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --headless --disable-gpu ^
  --screenshot="C:\_Local_DEV\_roshambo-assets\video2\sim\out.png" ^
  --window-size=1920,1080 --virtual-time-budget=5000 ^
  "file:///C:/_Local_DEV/_roshambo-assets/video2/sim/index.html?t=1192&chromeless=1"
```

Useful t values: `10` (start) · `1192` (first cross-host denial, 22:23:49 + a few
seconds) · `4716` (skill chapter begins, task 30 first granted 23:22:59) · `5498`
(end, last audit line 23:35:41). JS errors surface as a red banner at the top of the
frame itself (window.onerror overlay), so broken renders are visible in the PNG.

## What is on screen

- **Machine panels** (left ASUS-GEI, right WORKSTATION-LG): agent tokens with vendor
  colour (Anthropic orange, Google blue, Moonshot green, Zhipu grey-blue, MiniMax red,
  OpenAI cyan, all BotAgents yellow) and a live grant counter. Conflict flashes:
  winner glows green, refused agent red, at the same moment.
- **The judge** (centre top): CockroachDB; the ring pulses with each claim decision
  in the last 2 sim-seconds.
- **Task manager**: 37 task boxes (01–33, 36–39). Granted boxes travel to the
  claimer's token; released + trail-remembered tasks land in the green done strip.
- **Activity lanes** (bottom): one lane per agent (plus the `field-run (operator)`
  commit lane). Line height = state: 0 not joined / denial dip · 1 in the claim game ·
  2 request in flight (min. 2 sim-s display window, real latency otherwise) ·
  3 grant spike · 4 productive hold (grant → release or lease-expiry: last
  heartbeat + 300 s TTL) · 5 commit/push (25 s window; author matched to agent id,
  `roshambo field run` → operator lane).
- **Live feed**: time-sorted event lines from the same data. `data/quotes.js`
  (`window.ROSHAMBO_QUOTES`, built by `../build_quotes_js.py` from
  `data/quotes.json`) merges real quotes in — the 14 with precise in-window
  timestamps at their real time, plus 6 curated ones with editorial `sim_t`
  (directing decision, documented in the build script).
- **Beat overlay**: curated quotes with a `beat` field and `sim_t` appear as a
  quiet lower-third caption (~640 sim-s ≈ 4 s at 160×, fade in/out,
  non-overlapping queue) — built for the video-2 film.
- **Chapter band**: current phase from `phases.json`; chapter boundaries are also
  drawn on the lanes.
- **Sky counter**: constellation/star/segment counts from `_timelapse/frames.json`
  as committed at that moment.

## Data provenance (sim/data/)

| File | Source | Rows |
|---|---|---|
| `audit.json` | CockroachDB `audit_log`, swarm `poc-starmap-2026-07-30`, verbs claim/release/heartbeat/register_agent, chronological | 3791 |
| `memory.json` | same table, verbs remember/recall | 220 |
| `commits.json` | `git log --all` in `C:\_Local_DEV\_roshambo-poc\ASUS-GEI` (original timestamps kept, incl. pre-shared-remote commits) | 104 |
| `frames.json` | copy of `_timelapse/frames.json` from that repo | 76 frames |
| `tasks.json` | headings of `TASKS.md` (01–12, 23–33, 36–39) + wave-2 tasks 13–22 recovered from commit `c50fb07` | 37 |
| `agents.json` | distinct `agent_id` + `host_snapshot` from audit, vendor groups by name prefix | 27 |
| `phases.json` | computed chapter boundaries (see below) | 3 + post-window note |
| `data.js` | bundle of all of the above as `window.ROSHAMBO_DATA` | — |

Regenerate: `export_data.py` (needs `ROSHAMBO_DSN_FILE` + `PYTHONPATH=src` in the
roshambo repo, resolves the DSN via `demo/multivendor/rsb.py`; never prints it),
`build_meta.py` (tasks/agents/phases), `build_data_js.py` (bundle).

## Chapter boundaries (computed, then re-verified against raw rows)

1. **Two databases, one illusion** — 22:04:03.032Z (first audit row) → 22:23:49.112Z.
   Until then only ASUS-GEI agents appear in this database (first WORKSTATION-LG
   registration: BotAgent-C 22:22:51.441Z).
2. **First contact across machines** — from 22:23:49.112Z: the first claim denial
   whose holder sits on the OTHER machine — `BotAgent-C@WORKSTATION-LG`
   (host_snapshot WORKSTATION-LG) refused on `starmap:task:01`, reason
   `held by BotAgent-B@ASUS-GEI`. Verified by scanning all 1245 denials in order.
3. **Skills join the work** — from 23:22:59.084Z: first grant of `starmap:task:30`
   (to BotAgent-A@ASUS-GEI). No remember/recall row mentions "skill" in resource or
   reason, so the task-30 fallback defined in the brief applies. Runs to the last
   audit line, 23:35:41.625Z.

**Post-window note:** the brief defines the "two repos" era as ending at merge commit
`179a4fa` — but that merge happened 2026-07-31T00:06:43Z, ~31 min AFTER the last
audit line. It is documented in `phases.json` (`post_window`) and intentionally not a
playable chapter; the replay window follows the brief's rule "end = last audit line".

## Known gaps / honest limits

- OpenAI/codex: the operator report lists "codex ×2 @ ASUS-GEI", but no codex
  agent_id ever wrote to this swarm's audit_log — the roster is the audit truth (27).
  The cyan group exists but is empty.
- Release rows carry `resource = NULL`; task-release pairing is FIFO per agent over
  normalised task resources (`starmap:task:NN`, plus the variants agents actually
  used: `task:NN`, `task-NN`, bare `NN`). `starmap:repo` and `storm:task:*` claims
  appear in lanes/feed but not in the task panel.
- Lease holding uses TTL = 300 s (from the evidence files) with heartbeat renewal.
- Quotes: `data/quotes.js` exists (built 2026-07-31 by `../build_quotes_js.py`);
  the feed shows real quotes, and 6 curated beats render as lower-third overlays.
- Commits before sim-time 0 (two "an empty sky" commits) appear at the very start.
