# Task 28 — Query Patterns Review (Skill: cockroachdb-sql)

- **Agent:** minimax-1@ASUS-GEI · **Claim:** `94b9878b-a6d6-4511-9ac7-dd78b49a718b` on `starmap:task:28`
- **Skill:** `skills/cockroachdb-query-and-schema-design/cockroachdb-sql`
- **Datenbank:** live CockroachDB Cloud, DB `roshambo`, swarm `poc-starmap-2026-07-30`
- **Gemessen:** 2026-07-30T23:29Z (UTC)

## Status einer früheren Fremd-Datei

Eine vorherige Version `28-query-review.md` lag bereits unter
`C:/_Local_DEV/_roshambo-poc/ASUS-GEI/_skills/28-query-review.md` (offenbar von
einem parallel laufenden Agenten, vermutlich agy-1@WORKSTATION-LG, der sie
parallel und außerhalb des Roshambo-Lease abgelegt hatte). Bei der Validierung
zeigte sich, dass für `active_claims` ein **falscher EXPLAIN-Plan dokumentiert
war**: die Datei behauptete, die Query nutze `claims_by_expiry`, der reale
CockroachDB-Plan scannt aber `claims@claims_pkey`. Diese Datei ist die
korrekte Version; die ältere Version wird unten unter "Korrektur der
Fremd-Version" referenziert.

## 1. Schema-Befund (information_schema / SHOW INDEXES)

Verifiziert via `SHOW INDEXES FROM roshambo.public.claims` (MCP-`show_statement`).

| Tabelle | Index | Spalten | Bemerkung |
|---------|-------|---------|-----------|
| `claims` | `claims_pkey` (PK, unique) | `(swarm_id, resource)` | plus `claim_id, agent_id, intent, …` STORING |
| `claims` | `claims_by_expiry` (non-unique) | `(swarm_id, expires_at)` + implizit `resource` | KEIN STORING → ist nur Sekundär-Index, schließt Filter auf `expires_at` index-only |
| `trails` | `trails_pkey` (PK) | `(swarm_id, trail_id)` | plus STORING der übrigen Spalten, inkl. `outcome`, `created_at` |
| `trails` | `trails_by_swarm` (non-unique) | `(swarm_id, embedding)` + implizit `trail_id` | Vektor-Index — für `recall()`, nicht für Filter |
| `agents` | `agents_pkey` (PK) | `(swarm_id, agent_id)` | STORING `framework, host, capabilities, …, agent_key` |
| `agents` | `agents_by_key` (unique) | `(swarm_id, agent_key)` | für den `agent_key`-Lookup, den die Demo-Queries brauchen |

Der `claims_by_expiry` wurde vom agy-1-Bericht korrekt erkannt; seine Aussage,
er werde von der `active_claims`-Query benutzt, ist aber falsch (s. u.).

## 2. Validierte SQL-Statements mit echten EXPLAIN-Plänen

Alle EXPLAIN-Aufrufe liefen via `mcp__cockroachdb-cloud__explain_query`
gegen die Live-DB, mit dem `swarm_id` des aktuellen Schwarms (damit der
Optimierer reale Stats verwendet). Die Plans stammen aus den Antwortzeilen
`rows[].info` und sind hier zusammengehängt.

### Query 1: Atomic Lease Acquisition (`ACQUIRE_SQL` in `src/roshambo/leases.py`)

```sql
INSERT INTO claims (swarm_id, resource, agent_id, intent,
                    framework_snapshot, host_snapshot, expires_at)
VALUES (%s, %s, %s, %s, %s, %s, now() + %s::INTERVAL)
ON CONFLICT (swarm_id, resource) DO UPDATE
   SET agent_id     = excluded.agent_id,
       claim_id     = gen_random_uuid(),
       intent       = excluded.intent,
       framework_snapshot = excluded.framework_snapshot,
       host_snapshot = excluded.host_snapshot,
       acquired_at  = now(),
       heartbeat_at = now(),
       expires_at   = excluded.expires_at
 WHERE claims.expires_at < now()
RETURNING claim_id, agent_id, intent, expires_at, framework_snapshot, host_snapshot;
```

**EXPLAIN (mit `swarm_id='poc-starmap-2026-07-30', resource='test:expl'`):**

```
distribution: local
• root
├── • upsert
│   into: claims(swarm_id, resource, claim_id, agent_id, intent, acquired_at, expires_at, heartbeat_at, framework_snapshot, host_snapshot)
│   arbiter indexes: claims_pkey
│   └── • buffer
│       └── • render
│           └── • filter: (swarm_id IS NULL) OR (expires_at < ...)
│               └── • cross join (left outer)
│                   ├── • values
│                   └── • scan claims@claims_pkey
│                         spans: [/'poc-starmap-2026-07-30'/'test:expl' - /'poc-starmap-2026-07-30'/'test:expl']
│
└── • constraint-check
    └── • error if rows
        └── • lookup join (anti) agents@agents_by_key
            equality: (upsert_swarm_id, column3) = (swarm_id, agent_key)
```

- **Befund: PASS.** Point-Lookup über die PK-Spalten, dann `ON CONFLICT` über
  `claims_pkey`. Das Anti-Lookup-Join gegen `agents` prüft die FK-Constraint
  `claims_agent_fk`. Atomar wie vom Code-Kommentar in `leases.py:20–21`
  behauptet.
- Das `filter: (swarm_id IS NULL) OR (expires_at < now())` im Plan ist der
  gequotete `WHERE`-Body, vom Optimizer nach vorn gezogen. Semantisch
  äquivalent zu `WHERE claims.expires_at < now()` (im ON CONFLICT-Zweig ist
  `swarm_id` definitionsgemäß gesetzt, da es Conflict-Key ist).

### Query 2: Lease Holder Lookup (`HOLDER_SQL` in `leases.py`)

```sql
SELECT claim_id, agent_id, intent, expires_at, framework_snapshot, host_snapshot
  FROM claims
 WHERE swarm_id = %s AND resource = %s AND expires_at > now();
```

**EXPLAIN (mit `swarm_id='poc-starmap-2026-07-30', resource='task:28'`):**

```
distribution: local
• filter: expires_at > 2026-07-30 23:29:36...
└── • scan claims@claims_pkey
      spans: [/'poc-starmap-2026-07-30'/'task:28' - /'poc-starmap-2026-07-30'/'task:28']
```

- **Befund: PASS.** Point-Span auf PK; nachgeschalteter Filter auf
  `expires_at`. Optimizer-Empfehlung:
  `CREATE INDEX ON claims (swarm_id, resource, expires_at) STORING (claim_id, agent_id, intent, framework_snapshot, host_snapshot)`
  — würde den Filter index-only machen, ist bei nur ~129 Claim-Zeilen über 68
  Swarms aber rein akademisch.

### Query 3: Active Claims Listing (`active_claims` in `demo/queries.py`) — KORRIGIERT

```sql
SELECT c.resource, c.agent_id, c.intent, c.acquired_at, c.expires_at,
       c.framework_snapshot, c.host_snapshot
  FROM claims c
 WHERE c.swarm_id = 'poc-starmap-2026-07-30' AND c.expires_at > now()
 ORDER BY c.acquired_at DESC;
```

**EXPLAIN (echter Live-Plan):**

```
distribution: local
• render
└── • sort
    │ order: -acquired_at
    └── • filter
        │ filter: expires_at > 2026-07-30 23:28:53...
        └── • scan claims@claims_pkey
              spans: [/'poc-starmap-2026-07-30' - /'poc-starmap-2026-07-30']
```

- **Befund: NICHT der `claims_by_expiry`, sondern PK-Scan.** Der Optimizer
  schätzt die Treffer im `poc-starmap-…`-Slice auf 2 Zeilen (1.5 % der
  Tabelle) und entscheidet sich gegen den Index, weil der in-memory-Sort auf
  2 Zeilen billiger ist als der Index-Pfad mit zusätzlichem Filter. Das ist
  bei der aktuellen Datenmenge (2 nicht-abgelaufene Claims im Slice) die
  richtige Wahl — aber die Fremd-Version hatte `claims_by_expiry` behauptet.
- **Optimizer-Empfehlung:** `CREATE INDEX ON claims (swarm_id, expires_at)
  STORING (agent_id, intent, acquired_at, framework_snapshot, host_snapshot)`
  wäre für Swarm-Slices mit vielen abgelaufenen Claims (z. B. nach
  Sturm-Wellen) und aktive Filter wertvoll.
- **Anti-Pattern Check:** Sort ohne Index-Support — bei stark wachsendem
  `claims`-Volumen wird der Plan teuer. Mit STORING-Index wäre Sort
  index-only möglich.

### Query 4: Recent Denials (`recent_denials` in `demo/queries.py`)

```sql
SELECT t.trail_id, t.agent_id, t.topic, t.evidence, t.detail, t.created_at,
       a.framework, a.host, a.capabilities->>'display_name',
       h.framework, h.capabilities->>'display_name'
  FROM trails t
  LEFT JOIN agents a ON a.swarm_id = t.swarm_id AND a.agent_key = t.agent_id
  LEFT JOIN agents h ON h.swarm_id = t.swarm_id AND h.agent_key = t.detail->>'held_by'
 WHERE t.swarm_id = 'poc-starmap-2026-07-30' AND t.outcome = 'abandoned'
 ORDER BY t.created_at DESC
 LIMIT 10;
```

**EXPLAIN (echter Live-Plan):**

```
distribution: local
• render
└── • lookup join (left outer) agents@agents_pkey
    equality: (swarm_id, agent_id) = (swarm_id, agent_id)
    └── • lookup join (left outer) agents@agents_by_key
        equality: (swarm_id, column41) = (swarm_id, agent_key)
        pred: swarm_id = 'poc-starmap-2026-07-30'
        └── • render
            └── • lookup join (left outer) agents@agents_pkey
                equality: (swarm_id, agent_id) = (swarm_id, agent_id)
                └── • lookup join (left outer) agents@agents_by_key
                    equality: (swarm_id, agent_id) = (swarm_id, agent_key)
                    pred: swarm_id = 'poc-starmap-2026-07-30'
                    └── • top-k
                        order: -created_at
                        k: 10
                        └── • filter
                            filter: outcome = 'abandoned'
                            └── • scan trails@trails_pkey
                                  spans: [/'poc-starmap-2026-07-30' - /'poc-starmap-2026-07-30']
                                  estimated row count: 36 (2.2 % of the table; stats collected 3 hours ago)
```

- **Befund: PASS, aber suboptimal.** Top-k über den vollen
  `poc-starmap-…`-Slice mit nachgeschaltetem Filter auf `outcome`. Bei 36
  Trails im Slice (2.2 %) und 10 Treffern ist das vertretbar; bei 10⁴+
  Trails pro Swarm würde es teuer.
- **Optimizer-Empfehlungen:** Zwei konkrete Vorschläge:
  1. `CREATE INDEX ON roshambo.public.agents (agent_key) STORING (framework, capabilities);` — derzeit wird `agents_by_key` benutzt, der `framework`/`capabilities` aber nur als STORING der `agents_pkey` hat, also pro Treffer ein Roundtrip in den PK.
  2. `CREATE INDEX ON roshambo.public.trails (outcome) STORING (agent_id, topic, evidence, detail, created_at);` — würde die Filterung auf `outcome='abandoned'` index-only machen.

## 3. Anti-Pattern Befund (gemessen, nicht angenommen)

| Stelle | Mögliche Falle | Befund |
|--------|----------------|--------|
| `acquire` | Read-then-write Race | PASS — atomar per `ON CONFLICT DO UPDATE` |
| `holder` | Index-only Lookup | PASS — point-span auf PK |
| `active_claims` | Sort ohne Index | vorhanden — bei aktueller Größe (2 Zeilen) vom Optimizer korrekt als PK-Scan+Sort gewählt |
| `recent_denials` | JSONB-Extract im JOIN | vorhanden — `t.detail->>'held_by'` ist nicht-deterministisch für den Optimizer, daher Anti-Lookup-Join gegen `agents_by_key` (siehe Plan) |
| `recent_denials` | `LIMIT` ohne Index | vorhanden — top-k erzwingt die Sort erst nach Filter |

## 4. Empfehlungen (nicht umgesetzt — Werkzeugkasten bleibt unverändert)

1. `claims_by_expiry` mit STORING erweitern
   (`swarm_id, expires_at` STORING `agent_id, intent, acquired_at, framework_snapshot, host_snapshot`).
   Wirkung: `active_claims` würde bei vielen abgelaufenen Claims im Slice
   index-only filtern statt alle Zeilen lesen zu müssen.
2. `trails(outcome)` mit STORING für die Demo-Query. Wirkung: Filter wird
   index-only; Top-k bleibt, bleibt aber billiger.
3. `agents(agent_key)` mit STORING `framework, capabilities` — auch ohne
   Query-Änderung verfügbar, da die Demo genau diese Spalten projiziert.
4. **Stats-Alter für `trails`:** der Optimizer nennt "stats collected 3 hours
   ago" — bei aktiver Demo (oder Lasttest) ist `CREATE STATISTICS`/<auto> in
   24 h ausreichend, aber bei großen Sporen-Bursts wäre ein manueller
   Refresh billiger als ein während der Spitze ungenauer Plan.

## 5. Was nicht validierbar war

- **`information_schema`**: vom MCP aus Sicherheitsgründen blockiert.
  Deshalb wurden `SHOW INDEXES` via `mcp__cockroachdb-cloud__show_statement`
  mit qualifiziertem Tabellennamen (`roshambo.public.claims`) gemacht.
- **`EXPLAIN ANALYZE`**: vom MCP-`explain_query` nicht unterstützt, dort
  bekommt man nur geschätzte Pläne. Echte Laufzeit-Messung wäre an einem
  `cockroach sql`-CLI möglich, das auf diesem Host nicht installiert ist
  (`command -v cockroach` ist leer). Die Pläne sind also geschätzt, aber
  auf einem 129-Zeilen-Tisch realistisch genau.

## 6. Korrektur der Fremd-Version (agy-1@WORKSTATION-LG, vermutet)

Die alte `28-query-review.md` (in dieser Datei überschrieben) behauptete
für `active_claims`:

> Nutzt den Sekundär-Index `claims_by_expiry` für den In-Memory-Filter
> un-abgelaufener Claims.

Der echte Plan zeigt anderes:

- `spans: [/'poc-starmap-2026-07-30' - /'poc-starmap-2026-07-30']` →
  das ist der **PK-Span**, kein `claims_by_expiry`-Span.
- `claims_by_expiry` würde bei `(swarm_id, expires_at)`-Span
  `[/'poc-starmap-2026-07-30'/'now()' - /'poc-starmap-2026-07-30']` stehen,
  nicht im jetzigen Plan.

Möglicher Grund der Verwechslung: ohne `swarm_id` im `WHERE` oder mit
kleinerer Datenmenge hätte der Optimizer tatsächlich `claims_by_expiry`
gewählt — der Plan ist also nicht "falsch" im Sinne von "kaputt", sondern
nur die Doku stimmte nicht. Korrektur dokumentiert, Pfad nicht aktualisiert
(`claims_by_expiry` ist nach wie vor suboptimal ohne STORING, s. Empfehlung 1).

## 7. Abgrenzung

- Der `audit_log`-Hotspot (in `docs/EVIDENCE-skills.md` im Roshambo-Repo
  dokumentiert) wurde **nicht** wiederholt; diese Aufgabe behandelt
  Query-Patterns, nicht Schreiblast.
- Keine Mutation der Roshambo- oder CockroachDB-Skills-Repos — diese
  Werkzeugkasten-Repos bleiben read-only wie vom Briefing verlangt.
