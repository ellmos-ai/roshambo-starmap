# Task 31 — Cost and Usage Management (Skill: cockroachdb-cost-and-usage-management)

- **Skill:** `skills/cockroachdb-cost-and-usage-management`
- **Cluster Type:** CockroachDB Cloud Serverless (Basic)
- **Swarm ID:** `poc-starmap-2026-07-30`

---

## 1. Reale Gemessene Verbrauchswerte (SQL Layer Audit Log)

| Metrik | Gemessener Wert | Anmerkungen |
|---|---|---|
| **Transaktionen / Requests (`poc-starmap-2026-07-30`)** | **3.411** | Exakte Anzahl protokollierter SQL-Aktionen im Swarm |
| **Kumulierte Ausführungszeit (`poc-starmap-2026-07-30`)** | **1.912,50 Sekunden** (~31,88 min) | Summe aller `latency_ms` Werte im `audit_log` |
| **Gesamte Cluster Audit-Events (alle Swarms)** | **4.167** | Gesamtvolumen über die gesamte Datenbank-Lebensdauer |

---

## 2. Nicht messbare Metriken (Begründung)

1. **Request Units (RU) Verbrauch:**
   - **Nicht messbar via SQL, weil:** CockroachDB Serverless misst Request Units (RUs) auf der Cloud-Control-Plane (CockroachDB Cloud Cloud Console / REST API). SQL-System-Tabellen wie `crdb_internal` enthalten auf Serverless-Clustern keine RU-Zähler pro Statement.

2. **Genaue Tabellengröße in Bytes (`pg_relation_size`):**
   - **Nicht messbar via SQL, weil:** Die PostgreSQL-Kompatibilitätsfunktionen `pg_relation_size()`, `pg_database_size()` und `pg_size_pretty()` sind in CockroachDB v25.4.0 Serverless SQL nicht implementiert (`unknown function`).

---

## 3. Kosten-Fazit für den Multi-Agenten-Betrieb

Durch die ausschließliche Nutzung von Point-Lookups (`claims_pkey`) und schlanken Transaction-Statements (`ACQUIRE_SQL`, `RELEASE_SQL`) verbrauchen lease-basierte Claims minimale Rechenzeit pro Request (~388–461 ms RTT inklusive Cloud-Netzwerklatenz nach AWS Frankfurt). Abgewiesene Claims verursachen durch den zwingenden Double-Read (`HOLDER_SQL`) etwa 42% mehr Ausführungszeit.
