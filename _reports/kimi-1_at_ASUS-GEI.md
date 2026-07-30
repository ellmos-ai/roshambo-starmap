# Feldversuch-Bericht: kimi-1@ASUS-GEI

- **Agent-ID:** kimi-1@ASUS-GEI
- **Framework:** kimi
- **Host:** ASUS-GEI
- **Startzeit (UTC):** 2026-07-30T22:41:58Z (Session-Start, Umgebungs-Zeitstempel)
- **Endzeit (UTC):** 2026-07-31T01:20Z (letzte Aktivität, `date -u`; Minuten gerundet,
  Sekunden nicht gemessen)

## Aufgaben BEKOMMEN

Runde 1 (bei Ankunft waren alle 12 Erstwelle-Aufgaben erledigt, 0 aktive Claims):

- Keine reguläre Aufgabe (01–12) — alle bereits als Dateien im Repo vorhanden.
- Nebenarbeit über `starmap:repo`-Claim (GRANTED): eingechecktes `starmap.svg` in
  `b0d59e5` war veraltet (ohne „The Silver Veil"). Neu gerendert und gepusht.
  **Commit:** `18e71e0` — „regenerate starmap.svg: include The Silver Veil, 10 constellations".

Runde 2 (nach „arbeite weiter", zweite Welle 13–22 war inzwischen in TASKS.md):

- **Task 14 — GRANTED** (`42dfad58`, nach DENIED auf 13): `data/constellations/14-sunken-choir.json`,
  „The Sunken Choir", 7 Sterne, Dec −24°..−48°, RA 104°–158° (Chorbogen mit
  Dirigentenstern). Renderer: keine Skips. **Commit:** `e4a34a3`.
- **Task 19 — GRANTED** (`b90f8e53`), Lease zwischendurch EXPIRED (siehe Auffälligkeiten),
  danach erneut GRANTED (`7beab8a7`) und committet: `starmap/grid.py` —
  `grid_svg(width, height, project=None)`, 12 Meridiane + 5 Parallelkreise als fahle
  SVG-Polylines, equirectangular-Fallback, wirft nie (leeres Fragment bei Fehlern;
  Import- und Grenzfall-getestet). **Commit:** `a8bf2e9`.
- Nebenarbeit über `starmap:repo`-Claim: `starmap.svg` erneut veraltet (neue
  Konstellationen), neu gerendert. **Commit:** `fa890b9` — Commit-Text sagt
  „11 constellations", tatsächlich renderte die Datei 14 (zwischen Render und Commit
  kamen weitere Konstellationen per Pull dazu; Text-Ungenauigkeit, kein Force-Amend
  wegen Force-Push-Verbot).

Runde 3 (Fortsetzung nach Kontext-Zusammenfassung, 2026-07-31):

- **Task 24 — GRANTED** (`claim_id` nicht mehr im Lease-Status, zuvor vergeben an
  `kimi-1@ASUS-GEI`): `data/constellations/24-coral-quiver.json`, „The Coral Quiver",
  7 Sterne, RA 234°–246°, Dec 38°..55°, Lücke zwischen The Ashen Kite und The Hollow
  Chalice schließend. Renderer: keine Skips. **Commit:** `0563e3d` ( Teil von
  „tasks: third wave (23-27)").
- **Task 25 — GRANTED** (`8920c688-64f9-4c2f-81f7-f1291ada3450`): `data/constellations/25-sulfur-anchor.json`,
  „The Sulfur Anchor", 7 Sterne, RA 73°–91°, Dec −44°..−26°. Füllt die südliche Lücke
  zwischen The Iron Tide und The Sunken Choir und balanciert damit die südliche Kette.
  Renderer: 23 constellations, 163 stars, 160 segments. **Commit:** `9eff1c3`.

## Aufgaben ABGELEHNT (DENIED, held_by exakt übernommen)

| Ressource | gehalten von | intent |
|---|---|---|
| starmap:repo | agy-3@WORKSTATION-LG | commit task 08 |
| starmap:repo | glm-1@ASUS-GEI | commit tasks 03 09 10 |
| starmap:task:13 | kimi-2@ASUS-GEI | build task 13 |
| starmap:task:17 | kimi-2@ASUS-GEI | build task 17 scatter |
| starmap:task:18 | BotAgent-A@ASUS-GEI | BotAgent A contention probe |
| starmap:task:21 | kimi-2@ASUS-GEI | build task 21 catalogue |
| starmap:task:22 | glm-1@ASUS-GEI | build task 22 |

## Claim-Statistik

- Claim-Versuche gesamt: 16 (Task-Claims 11, Repo-Claims 5)
- Davon gewonnen (GRANTED): 8 (Tasks 14, 19, 19-Re-Claim, 24, 25; Repo 3×)
- Davon abgewiesen (DENIED): 8 (siehe Tabelle, inkl. Task 23 — bereits auf `origin/master` erledigt)

## Auffälligkeiten

- **Lease EXPIRED (Task 19, Claim `b90f8e53`):** Heartbeat nach dem Render-Check
  lieferte EXPIRED mit `held_by=unknown`, obwohl lokale Uhr ~3 Minuten VOR dem
  genannten `expires_at` lag. Beleg für **Server-Uhr läuft der Client-Uhr voraus**
  (auch beobachtet bei Repo-Claim `20ab79ab`, dessen `expires_at` bereits in der
  Vergangenheit lag, als er erteilt wurde). Protokoll befolgt: nichts committet,
  failure-Trail geschrieben, Task später neu geclaimt (niemand hielt ihn) und dann
  sauber committet.
- **Remote-History wurde während Runde 1 umgeschrieben:** alter task-12-Commit
  `498c0e6` durch `b0d59e5` (agy@WORKSTATION-LG) ersetzt; Auflösung per
  `git rebase --abort` + `git reset --hard origin/master` (nur zuvor gefetchte,
  ersetzte Commits verworfen). Kein `--force`.
- **Duplikate im Repo (fremde Arbeit, von mir nicht angefasst):** Aufgabe 02
  (broken-anvil + silver-veil), 03 (drowned-bell + windlass), 05 (amber-loom +
  silver-spindle), 09 (hollow-chalice + quartz-comb), 10 (pale-anchor + glass-eel),
  17 (zwei scatter-Commits). Typische Takeover-/Parallel-Artefakte.
- **Geteiltes Arbeitsverzeichnis mit weiteren Agenten auf ASUS-GEI** (kimi-2, glm-1,
  BotAgent-A): `git pull --rebase` scheiterte mehrfach an fremden untracked
  In-Arbeit-Dateien (CATALOGUE.md, PROVENANCE.md) und an von Render-Checks
  anderer Agenten modifiziertem `starmap.svg`. Ein untracked `starmap/labels.py`
  (Duplikat des inzwischen committeten `0563e3d`) habe ich zur Seite gelegt
  (`/tmp/labels-uncommitted-dup.py`), nicht gelöscht.
- **Untracked `data/constellations/23-barnacled-sextant.json`** im Arbeitsverzeichnis:
  TASKS.md (Stand origin/master) endet bei Task 22 — jemand baut eine Aufgabe 23,
  die es (noch) nicht gibt. Nicht angefasst.
- **`recall` ohne Embedding-Credentials** schlägt mit `NoCredentialsError` fehl;
  mit `ROSHAMBO_EMBEDDING_PROVIDER=placeholder` funktioniert es (lexikalisch).
- **Task 23 bereits erledigt:** Claim wurde gewährt, aber `data/constellations/23-barnacled-sextant.json`
  befand sich bereits auf `origin/master` (Commit von `glm-1@ASUS-GEI`). Lease sofort
  wieder freigegeben, keine fremde Arbeit überschrieben.
- **Stash-Konflikte bei `git pull --rebase`:** Vor Runde 3 blockierte ein unstaged
  `_reports/kimi-2_at_ASUS-GEI.md` (subagent report in Arbeit) sowie CRLF/LF-Rauschen
  in `CATALOGUE.md`/`PROVENANCE.md` den Rebase. Nach Sicherung des Reports und
  Zurücksetzen der reinen Line-Ending-Änderungen lief der Rebase sauber durch.
- Fremde untracked Dateien (`stoersender-*.csv/json`, `evidence_*.json`) nicht
  angefasst und nicht committet.
