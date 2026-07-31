# QUOTES-NOTES — Herkunft und Echtheitsnachweis je Zitat

Feldversuch `poc-starmap-2026-07-30`. Alle Pfade relativ zu `C:\_Local_DEV\_roshambo-poc\ASUS-GEI\`.
Zeilenangaben per `grep -n` bzw. Read-Zeilennummern verifiziert. Kürzungen nur mit `…`,
Markups (Backticks, `**`) stehen wie im Original. Zeitstempel nur, wo im Material belegt —
`null` heißt: nicht datierbar, nicht geraten.

**Feld `beat` (Nacharbeits-Auftrag):** kurzer deskriptiver Kommentarvorschlag auf Englisch
für die Video-Einblendung — knapp, rhetorisch, mitfühlend-nüchtern. Jeder beat leitet sich
strikt aus Zitat + dokumentiertem Kontext ab (Report-Abschnitt, run.json, CSV-Zeilen);
nichts ist dazuerfunden. `beat: null` bei rein sachlichen Zitaten ohne Mitfieber-Potenzial
(2 von 61). Beats sind Regie-Vorschläge, keine Zitate — sie stehen nicht im Quellmaterial.

## operator/claude (Koordinator, Claude Code auf ASUS-GEI)

1. `operator_at_ASUS-GEI.md:10` — Eröffnungssatz des Operator-Reports, Abschnitt "What ran". Report ist auf 2026-07-31 datiert (Zeile 3).
2. `operator_at_ASUS-GEI.md:27-28` — Kern-These des Reports: Bots und LLM-Agenten sitzen am selben Tisch. Wörtlich aus "What ran".
3. `operator_at_ASUS-GEI.md:49` — Wörtliche Beispielzeile aus dem Audit-Log, als Codeblock im Report zitiert (Abschnitt "What the run produced"). Erste Cross-Host-Kollision Bot-gegen-Bot über Maschinengrenze.
4. `operator_at_ASUS-GEI.md:63-64` — Messfehler Nr. 1, Abschnitt "What is NOT established": Bot-Detektor meldete CONTRACT VIOLATION, Audit-Log entlastete das System.
5. `operator_at_ASUS-GEI.md:64-65` — Fortsetzung desselben Satzes: Ursache Netzwerk-Roundtrip nach Frankfurt im Messfenster. Der Netzwerklatenz-Fehlmess-Moment.
6. `operator_at_ASUS-GEI.md:67-68` — Messfehler Nr. 2: der 134-Phantom-Detektor. Eigenbekenntnis des Koordinators, wörtlich.
7. `operator_at_ASUS-GEI.md:90-91` — Zwei-Repos-Moment, Abschnitt "How the shared repository came about".
8. `operator_at_ASUS-GEI.md:93-94` — Auflösung: gemeinsames Remote `ellmos-ai/roshambo-starmap` mid-run.
9. `operator_at_ASUS-GEI.md:96-98` — Zwei-Datenbanken-Moment: `/roshambo` vs `/defaultdb` auf demselben Cluster.
10. `operator_at_ASUS-GEI.md:98-99` — Wie es aufflog: Agentenliste zeigte nie fremde Agenten. Kein separater Log mit dieser Agentenliste im ASUS-GEI-Bestand (Lücke, siehe unten).
11. `operator_at_ASUS-GEI.md:81-83` — Leere-Skills-Moment aus Koordinator-Sicht, "A negative finding about the CockroachDB Agent Skills".
12. `README.md:74-75` — Zwei-Repos-Moment in der Repo-README ("Two evidence lines, one repository"); README verweist auf Verifikation 2026-07-31 (Zeile 28).
13. `README.md:110-111` — Schluss-Sentenz "One more time, for the avoidance of doubt".
14. `TASKS.md:3` — Briefing-Eröffnung der Taskliste (Koordinator-Text). Kein Datum im Text → `null`.

## agy-1@WORKSTATION-LG (Google/Antigravity, Gemini)

15. `agy-1_at_WORKSTATION-LG.md:8` — Statuszeile des Reports; Endzeit 2026-07-30T23:36:00Z steht in Zeile 7 desselben Headers.
16. `agy-1_at_WORKSTATION-LG.md:46` — Aufsummierte Cross-Host-Kollisionen, Abschnitt "Ultimative Akkumulierte Beweissicherung". Führendes Listen-Markup `- **` ab Zeilenanfang weggelassen, Rest wörtlich inkl. Emoji. Zeit: Report-Session 2026-07-30 (Header Zeilen 6-7).
17. `agy-1_at_WORKSTATION-LG.md:31` — Denial-Statistik gegen kimi-2, Abschnitt "Aufgaben ABGELEHNT". Der mehrfach-abgelehnte-Moment (13x gegen agy-1 allein).
18. `agy-1_at_WORKSTATION-LG.md:52` — Fazit Punkt 1: Fertigstellungs-Meldung mit Render-Zahlen.
19. `agy-1_at_WORKSTATION-LG.md:53` — Fazit Punkt 2; Mitte (Vendor-Aufzählung) mit `…` gekürzt, Anfang und Ende wörtlich.

## kimi-1@ASUS-GEI (Moonshot)

20. `kimi-1_at_ASUS-GEI.md:17` — Wörtlicher Commit-Text aus "Aufgaben BEKOMMEN", Runde 1. Commit-Zeit nicht im Report → `null`.
21. `kimi-1_at_ASUS-GEI.md:67-68` — Auffälligkeiten: EXPIRED trotz lokaler Uhr vor `expires_at`; Beleg Server-Uhr vs Client-Uhr.
22. `kimi-1_at_ASUS-GEI.md:93-95` — Task 23 schon erledigt: Lease sofort freigegeben, nichts überschrieben. Mitte mit `…` gekürzt.
23. `kimi-1_at_ASUS-GEI.md:112-114` — Runde-4-Nachtrag, dessen Header (Zeile 105) mit 2026-07-30T23:32:51Z datiert ist. DENIED als messbare SQL-Fehlerrate.
24. `kimi-1_at_ASUS-GEI.md:140-142` — Identitäts-Kollision: zweite kimi-1-Invocation unter eigener agent_id. Gleiche Nachtrag-Datierung.
25. `kimi-1_at_ASUS-GEI.md:144` — "Repo-Lease ist der Engpass, nicht die Tasks" — Überschrift der Auffälligkeit, Nachtrag-Datierung.
26. `kimi-1_at_ASUS-GEI.md:148-150` — Welle 4 bei Ankunft fast fertig. Nachtrag-Datierung.

## kimi-2@ASUS-GEI (Moonshot)

27. `kimi-2_at_ASUS-GEI.md:24` — Identitäts-Kollision aus kimi-2-Sicht: eigener 90-Sterne-scatter verworfen, abandoned-Trail. Kein Datum → `null`.
28. `kimi-2_at_ASUS-GEI.md:28` — Leere-Skills-Moment, Punkt 5 der Auffälligkeiten: `.gitkeep`-only-Verzeichnis, Ausweichen auf auditing-table-statistics.
29. `kimi-2_at_ASUS-GEI.md:21` — Claim-Bilanz inkl. "Max. 3 Abweisungen in Folge".
30. `kimi-2_at_ASUS-GEI.md:31` — Endstand: finaler Renderer-Lauf exit 0.
31. `_skills/30-performance-kimi2.md:9-10` — Leere-Skills-Moment auf Englisch, "Skill situation (honest note first)". Datierung aus Zeile 3: "Applied 2026-07-30 ~23:27 UTC" (Tilde = ca.-Angabe im Original).
32. `_skills/30-performance-kimi2.md:54-55` — Scaling-Befund, Finding 2. Gleiche Datierung.
33. `_skills/30-performance-kimi2.md:69` — Verdict-Schlusssatz. Gleiche Datierung.
34. `READING-THE-MAP.md:3` — Task-27-Artefakt; Autorschaft kimi-2 belegt in `kimi-2_at_ASUS-GEI.md:16` (Commit `667903d`).
35. `READING-THE-MAP.md:7` — Schlusssatz des ersten Absatzes, gleiche Autorschaft.

## glm-1@ASUS-GEI (Zhipu)

36. `glm-1_at_ASUS-GEI.md:36` — Erster anbieterübergreifender Koordinations-Beleg (who-has Task 04 → agy-2). Session-Datum 2026-07-30 (Header Zeilen 6-7).
37. `glm-1_at_ASUS-GEI.md:90` — Selbstkorrektur nach Batch-Claim-Hortung (9 Claims auf einmal).
38. `glm-1_at_ASUS-GEI.md:91` — who-has/claim-Diskrepanz mit exaktem DENIED-Halter.
39. `glm-1_at_ASUS-GEI.md:95` — Repo-Lease-Backoff gegen kimi-2s Commit-Serie.
40. `glm-1_at_ASUS-GEI.md:144-145` — Storm-Bot-Beobachtung: Bots halten Leases auf fertige Tasks als Lasttest. Abschnitt "Finaler Abschluss (2026-07-30T23:12:00Z)" (Zeile 127).
41. `glm-1_at_ASUS-GEI.md:148-149` — Fertigstellungs-Meldung: keine offene Bauaufgabe mehr. Gleiche Abschnitts-Datierung.
42. `glm-1_at_ASUS-GEI.md:155-156` — Disclaimer-Satz, Abschluss Phase 1.
43. `glm-1_at_ASUS-GEI.md:173` — Leere-Skills-Negativbefund in der Task-32-Zeile, Phase 2 (2026-07-31, Header Zeile 160).
44. `glm-1_at_ASUS-GEI.md:226-227` — Eingefrorene DB-Cluster-Uhr, Nebenbefund Phase 2.
45. `glm-1_at_ASUS-GEI.md:248-250` — Negativbefund-Formulierung "nicht als erfundenes Problem".

## minimax-1@ASUS-GEI (MiniMax)

46. `minimax-1_at_ASUS-GEI.md:31` — 6/6 GRANTED, Konkurrenz durch parallele Komplettierung statt Denial. Session 2026-07-30 22:55–23:13 UTC (Header Zeilen 6-7).
47. `minimax-1_at_ASUS-GEI.md:38` — Versehentlich fremde Datei mitcommittet, Selbstkritik "Lerneffekt". Mitte gekürzt.
48. `minimax-1_at_ASUS-GEI.md:46` — Zeitfresser pull-rebase-Konflikte im Shared Tree.

## claude-code-1 / claude-code-2 @ASUS-GEI (Anthropic, Round-Logs)

49. `_logs/round01-claude-2.log:7` — Abweisung durch claude-code-1, Reaktion: nicht warten, nächste Aufgabe. Logs ohne Zeitstempel → `null`.
50. `_logs/round01-claude-2.log:11` — "Commit lief ins Leere": fremder `git add -A` hatte die eigene Datei schon eingesammelt.
51. `_logs/round02-claude-1.log:1` — Fremde In-Arbeit-Datei erkannt (projection.py, Task 04).
52. `_logs/round03-claude-1.log:3` — Protokoll-Disziplin: ohne Lease nicht committen.
53. `_logs/round04-claude-1.log:3` — DENIED durch claude-code-2 auf Task 07, dann Task 08 GRANTED. Log-Autor ist claude-code-1 (Dateiname round04-claude-1).
54. `_logs/round04-claude-2.log:1` — "fremde Arbeit wird nicht committet" — claude-code-2 über style.py.

## codex-1 / codex-2 @ASUS-GEI (OpenAI)

55. `_logs/round01-codex-1.log:14` — Windows-Sandbox blockiert Registrierung (error 5). Zeit: ended_at der Invocation in `_logs/run.json` (round 1, codex-1, 2026-07-30T22:37:46.653042+00:00).
56. `_logs/round05-codex-2.log:20` — "I did not touch shared work without RESULT=REGISTERED." Zeit: run.json round 5 codex-2 ended_at 2026-07-30T22:43:08.052801+00:00. Codex kam in allen 6 Runden nie ins System — Charakter-Moment "der Außenseiter".

## BotAgent A/B/C @ASUS-GEI (Skript-Bots, kein Modell)

57. `_logs/storm-1.log:7` — BotAgent B im Storm: 2/10 granted, Backoff auf Maximum 20 s. Storm-Logs undatiert → `null`.
58. `_logs/storm-a4.log:8` — BotAgent C: 0/9 granted, komplette Abweisung, Intervall am Anschlag. Der "wird mehrfach abgelehnt und reagiert"-Moment, maschinell.
59. `_logs/storm-1.log:10` — Detektor-Zeile des Storm-Laufs: keine zwei simultanen Halter.
60. `botagent-crosshost.csv:2` — Erster Cross-Host-Denial-Datensatz mit exaktem UTC-Zeitstempel; Intervall 1.0→1.6 s (adaptiver Backoff beginnt).
61. `botagent-crosshost.csv:10` — Vier Denials später: Intervall auf 13.15 s hochgefahren — Backoff messbar in einer Zeile.

## Bekannte Lücken

- **Zwei-Datenbanken-Moment existiert nur im Operator-Report** (`operator_at_ASUS-GEI.md:96-99`). Kein Log im ASUS-GEI-Bestand enthält die Agentenliste ohne fremde Agenten — die Original-Beobachtung lag auf WORKSTATION-LG-Seite oder im Chat-Verlauf, nicht in diesen Artefakten.
- **Zwei-Repos-Moment** ebenfalls nur Operator-Report + README; kein Agenten-Log dokumentiert den Moment des Remote-Wechsels.
- **134-Phantom-Detektor und Frankfurt-Latenz-Fehlmessung**: nur Operator-Report; der ad-hoc-Checker und der Bot-Detektor-Code liegen nicht in diesem Workspace.
- **Storm-Logs und Claude-Round-Logs** tragen keine Zeitstempel; glm-1 datiert storm-1..8 grob auf 01:01–01:11 lokal (`glm-1_at_ASUS-GEI.md:142-143`), nicht pro Datei.
- **agy-2..6, claude-haiku/sonnet/opus**: keine eigenen Reports im ASUS-GEI-Bestand; nur indirekt über Denial-Tabellen der anderen belegt.
