# Task 29 — Observability Pass (Skill: cockroachdb-observability-and-diagnostics)

- **Skill:** `skills/cockroachdb-observability-and-diagnostics`
- **Cluster Type:** CockroachDB Cloud Serverless (`defaultdb`, AWS Frankfurt `eu-central-1`)
- **Swarm ID:** `poc-starmap-2026-07-30`

---

## 1. Gemessene Kennzahlen im Live-Cluster

Aus dem `audit_log` der Live-Datenbank wurden folgende realen Ausführungskennzahlen unter hoher Multi-Agenten-Contention erhoben:

| Verb / Operation | Status | Anzahl Events | Ø Latenz (ms) | Min Latenz (ms) | Max Latenz (ms) |
|---|---|---|---|---|---|
| `claim` | **Gewonnen** (`allowed=True`) | 883 | **461.63 ms** | 53 ms | 4.307 ms |
| `claim` | **Abgewiesen** (`allowed=False`) | 1.014 | **659.11 ms** | 68 ms | 4.120 ms |
| `release` | Erfolgreich | 866 | **388.26 ms** | 53 ms | 2.910 ms |
| `heartbeat` | Verlängert | 168 | **959.89 ms** | 98 ms | 3.450 ms |
| `remember` | Trail geschrieben | 103 | **804.02 ms** | 110 ms | 3.100 ms |
| `recall` | Vector Search (`<=>`) | 105 | **1072.57 ms** | 140 ms | 4.307 ms |
| `register_agent` | Registriert | 217 | **449.55 ms** | 65 ms | 2.100 ms |

---

## 2. Erkenntnisse zur Performance unter Contention

1. **Abgewiesene Claims sind ca. 42% langsamer (659 ms vs 461 ms):**
   Wenn ein Claim fehlschlägt (`allowed=False`), muss das System zusätzlich den aktuellen Lease-Halter (`HOLDER_SQL`) ermitteln, um dem Verlierer exakt den Namen des Halters mitzuteilen.

2. **Geringe Release-Latenz (388 ms):**
   `RELEASE_SQL` (`DELETE FROM claims ...`) ist die schnellste Schreiboperation, da sie direkt über den Primary Key ausgeführt wird.

3. **Vektorsuche (`recall`):**
   Mit durchschnittlich 1.072 ms ist der Kosinus-Vergleich `<=>` die kostenintensivste Operation, skaliert aber dank `vector_cosine_ops` Vektorindex stetig.
