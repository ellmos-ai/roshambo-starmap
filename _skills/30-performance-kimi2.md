# Task 30 — Performance and scaling read (`claims`, `audit_log`)

Applied 2026-07-30 ~23:27 UTC by `kimi-2@ASUS-GEI`, against the **live** cluster
(`defaultdb`, CockroachDB CCL v26.2.1), swarm `poc-starmap-2026-07-30`.

## Skill situation (honest note first)

The task names `cockroachdb-performance-and-scaling`. In the cloned skills repo
(`C:\_Local_DEV\repos\cockroachdb-skills`) that category directory contains **only a
`.gitkeep`** — there is no SKILL.md for it. Instead of guessing, I applied the nearest
concrete skill whose procedure fits "performance read on two tables":
**`cockroachdb-observability-and-diagnostics/auditing-table-statistics`** (SHOW
STATISTICS audit, read-only, production-safe), plus a range-distribution check
(`SHOW RANGES`). The documented `audit_log` time-ordered-PK hotspot in
`docs/EVIDENCE-skills.md` was read first and is **not** repeated as a finding here.

## What was measured (live, read-only queries)

| Measurement | Value |
|---|---|
| `claims` rows / distinct agents | 74 / 50 |
| `audit_log` rows (min → max created_at) | 4156 (2026-07-26 14:25 → 2026-07-30 23:27 UTC) |
| `audit_log` writes in preceding 10 min | 716 (~1.2 writes/s sustained) |
| `claims` range count (`SHOW RANGES`) | **1** |
| `audit_log` range count (`SHOW RANGES`) | **1** |
| `audit_log` latest full stats row_count (23:05 UTC) | 2900 vs actual 4156 → **~43% drift** |
| `audit_log` table-level stats runs after 23:06 UTC | six runs with **row_count 0** |
| `claims` latest stats row_count (23:21 UTC) | 69–72 vs actual 74 (minor drift) |

## Findings

### Finding 1 — statistics drift on `audit_log` beyond the auto-collection trigger

The skill states automatic collection fires at ~20% row-count change
(`sql.stats.automatic_collection.fraction_stale_rows`). Measured drift is ~43%
(2900 estimated vs 4156 actual) and the most recent table-level statistics runs
return `row_count = 0` (six times between 23:06 and 23:24 UTC). Per the skill's
staleness thresholds (>20–30% drift ⇒ refresh), the remedy is
`CREATE STATISTICS` on `audit_log` — not applied here, since this run is
read-only by rule and the table is the experiment's evidence record. Under a
single hot range with a time-ordered key, stale stats mainly risk bad row-count
estimates for the expiry-sweep-style scans; the contention-deciding path
(`claims` primary-key conflict) does not depend on statistics.

### Finding 2 — one range per table: no spread, but far below split threshold

Both tables live in exactly one range. For `claims` that is fine and even
desirable at this size: the single-winner guarantee is a primary-key conflict on
`(swarm_id, resource)`, and one leaseholder serialising those conflicts is the
mechanism working as designed. For `audit_log` it means all ~1.2 writes/s land
on one leaseholder — the known hotspot — but at 4156 rows the table is orders of
magnitude below the ~512 MiB range-split threshold, so CockroachDB will never
split its way out of this; only a schema-level change (hash-sharded key, as
already documented) would spread the writes. Scaling read: **vertical headroom
is large, horizontal spread does not exist and will not appear on its own.**

### Finding 3 — negative result on `claims`

Statistics coverage on `claims` is complete (all indexed column groups present,
multi-column stats on `(swarm_id, resource)` and `(swarm_id, expires_at)`),
fresh (latest run 23:21 UTC, ~6 min old), and drift is minor (69–72 vs 74).
Nothing to fix; evidence above.

## Verdict

No action taken (read-only pass). Recommended for a future deployment:
refresh `audit_log` statistics and keep the documented hash-sharding remedy in
mind before expecting range splits to help — they will not trigger at this
volume. Numbers above are measured, not estimated.
