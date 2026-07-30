# Feldversuchsbericht: kimi-2@ASUS-GEI

- **Agent-ID:** kimi-2@ASUS-GEI
- **Framework:** kimi
- **Host:** ASUS-GEI
- **Startzeit (UTC):** 2026-07-31 00:58
- **Endzeit (UTC):** 2026-07-31 01:10

## Aufgaben BEKOMMEN und abgeschlossen

| Task | Gebaut | Commit-Hash | Bemerkung |
|------|--------|-------------|-----------|
| 17 | `data/scatter.json` mit 80 schwachen Hintergrundsternen über die ganze Sphäre | `0058a97` | Eigenständig erstellt, Renderer-Check bestanden (19 constellations, 136 stars, 132 segments, keine Skips). |

## Aufgaben ABGELEHNT / bereits erledigt

| Task | Gehalten von / Status | Bemerkung |
|------|----------------------|-----------|
| 15 | `glm-1@ASUS-GEI` | Erledigt (`05-foundered-ark.json`). |
| 16 | `kimi-2@ASUS-GEI` (abgelaufener Lease) | Task war bereits auf `origin/master` durch `f645d47` erledigt. |
| 18 | `glm-1@ASUS-GEI` / `agy-1@WORKSTATION-LG` | Bereits auf `origin/master` (`9543f4a`, `f8eadde`). |
| 19 | `agy-1@WORKSTATION-LG` | Bereits auf `origin/master` (`a8bf2e9`). |
| 20 | `kimi-2@ASUS-GEI` (abgelaufener Lease) | Bereits auf `origin/master` durch `0563e3d` erledigt. |
| 21 | `glm-1@ASUS-GEI` | Claim wurde gewährt, aber `glm-1` hat `CATALOGUE.md` bereits gepusht (`8dbb220`), bevor ich committen konnte. |
| 22 | `glm-1@ASUS-GEI` | Bereits auf `origin/master` (`9ccc562`). |

## Claim-Versuche

- **Gesamt:** 8
- **Gewonnen:** 2 (Task 17, Task 21)
- **Abgewiesen:** 6 (Task 15, 16, 18, 19, 20, 22 — letztere bereits fertig oder stale Lease auf eigene ID)

## Auffälligkeiten

1. **Abgelaufene Leases auf eigene ID:** Mehrere Tasks (16, 20, 21-Repo) zeigten `held_by=kimi-2@ASUS-GEI` mit abgelaufenem `expires_at`. Offenbar blieben Leases einer früheren Sitzung/Invocation unter derselben Agenten-ID zurück.
2. **Embedding-Credentials fehlen:** `rsb.py recall` und `rsb.py remember` scheiterten mit `NoCredentialsError: Unable to locate credentials`. `ROSHAMBO_EMBEDDING_PROVIDER=placeholder` wäre nötig, um sie offline zu betreiben.
3. **Renderer kennt `scatter.json` / `river.json` nicht:** `render.py` lädt nur `data/constellations/*.json` und optionale `starmap/`-Module. Die Aufgaben 17 und 18 verlangen diese Dateien, aber der Renderer rendert sie nicht — die Dateien müssen trotzdem korrekt angelegt werden.
4. **Salvage-Commit auf lokalem Branch:** Ein lokal committeter Salvage-Commit (`f1f30a1`, Co-Authored-By: Claude Fable 5) löschte `starmap/labels.py`, fügte `data/constellations/23-barnacled-sextant.json` hinzu und brachte `stoersender-*`-Logdateien mit. Um `labels.py` (Task 20) nicht zu verlieren, wurde der Commit per `git revert --no-commit` rückgängig gemacht; die eigenen `CATALOGUE.md`-/`PROVENANCE.md`-Entwürfe wurden danach neu erzeugt.
5. **Zeitstempel im Roshambo-Service:** Die `expires_at`-Werte lagen konsequent ca. zwei Stunden in der Vergangenheit, obwohl `RESULT=GRANTED` zurückgegeben wurde. Heartbeats funktionierten dennoch.

## Report-Commit

Der Versuch, den Bericht zu committen, wurde nach vier Warte-/Retry-Zyklen abgebrochen, weil der `starmap:repo`-Lease durch `glm-1@ASUS-GEI` (`intent=report-final`) gehalten wurde und nicht freigegeben wurde. Der Bericht liegt daher nur lokal vor und wartet darauf, von einem anderen Agenten oder nach Ablauf des Leases gepusht zu werden.

## Git-Status am Ende

Branch `master` ist auf dem Stand von `origin/master`. Der eigene Commit `0058a97` (Task 17) wurde erfolgreich gepusht.
