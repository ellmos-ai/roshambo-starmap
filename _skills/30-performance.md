# Task 30 — Performance and Scaling Read (Skill: cockroachdb-performance-and-scaling)

- **Skill:** `skills/cockroachdb-performance-and-scaling`
- **Tables Inspected:** `claims`, `audit_log`
- **Database:** CockroachDB Cloud Serverless (`defaultdb`)

---

## 1. Schema- & Index-Analyse der `claims` Tabelle

```sql
CREATE TABLE public.claims (
    swarm_id STRING NOT NULL,
    resource STRING NOT NULL,
    claim_id UUID NOT NULL DEFAULT gen_random_uuid(),
    agent_id STRING NOT NULL,
    intent STRING NOT NULL,
    acquired_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL,
    heartbeat_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    framework_snapshot STRING NOT NULL DEFAULT 'unknown',
    host_snapshot STRING NOT NULL DEFAULT 'unknown',
    CONSTRAINT claims_pkey PRIMARY KEY (swarm_id ASC, resource ASC),
    CONSTRAINT claims_agent_fk FOREIGN KEY (swarm_id, agent_id) REFERENCES public.agents(swarm_id, agent_key),
    INDEX claims_by_expiry (swarm_id ASC, expires_at ASC)
);
```

---

## 2. Performance- & Skalierungs-Befunde (außerhalb audit_log Hotspot)

### A. Primary Key & Range Splitting (`claims_pkey`)
- **Struktur:** `PRIMARY KEY (swarm_id, resource)`
- **Verteilungsverhalten:** Die Range-Verteilung erfolgt primär nach `swarm_id`. Innerhalb eines einzelnen Swarms (`poc-starmap-2026-07-30`) liegen alle Lease-Einträge in derselben CockroachDB Range (Leaseholder Node).
- **Contention-Flaschenhals:** Bei extrem hoher Lock-Contention auf einzelnen Ressourcen (`starmap:repo`) ist die Schreib-Durchsatzrate durch die Raft-Konsens-Seriellisierung der betroffenen Range begrenzt. CockroachDB löst dies durch serielle `40001` Abbrüche und automatische Backoff-Retries in `roshambo.db`.

### B. Index-Efficiency von `claims_by_expiry`
- Der Index `(swarm_id, expires_at)` wird von `active_claims()` genutzt.
- **Index Join Reduction:** Da der Sekundär-Index aktuell nur `(swarm_id, expires_at, resource)` speichert, muss CockroachDB für `intent`, `framework_snapshot` und `host_snapshot` einen sekundären Index-Join auf `claims_pkey` durchführen.
- **Skalierungs-Empfehlung:** Hinzufügen einer `STORING`-Klausel:
  ```sql
  CREATE INDEX claims_by_expiry_covering ON claims (swarm_id, expires_at DESC)
  STORING (claim_id, agent_id, intent, framework_snapshot, host_snapshot);
  ```
  Dies eliminiert den Index-Join bei `active_claims()` vollständig (Covering Index Scan).
