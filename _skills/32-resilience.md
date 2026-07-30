# Task 32 — Resilience question (skill: cockroachdb-resilience-and-disaster-recovery)

- **Agent:** glm-1@ASUS-GEI (framework glm, host ASUS-GEI)
- **Claim:** `202c31fe-a434-4d81-82f1-e1bb31065c61` on `starmap:task:32`
- **Skill claimed:** `cockroachdb-resilience-and-disaster-recovery`
- **Datum (UTC):** 2026-07-30T23:25Z (Bearbeitung), 23:29:32 Lease-Expiry

## Frage

> What happens to held leases when a node or client dies mid-claim? Inspect the
> schema and the lease TTL, and report what they *actually* guarantee.

## Negativbefund — der Skill fehlt im Repo (vollwertiges Ergebnis)

Die offizielle Skill-Prozedur konnte **nicht** befolgt werden, weil der Skill im
Repo nicht vorliegt. Dies ist ein Befund, kein erfundenes Problem:

```
C:\_Local_DEV\repos\cockroachdb-skills\skills\cockroachdb-resilience-and-disaster-recovery\
    .gitkeep          <- einzige Datei
```

- Kein `SKILL.md`, kein `references/cockroachdb-rules/`, keine Regeldateien.
  Die Kategorie-Ordner für `cockroachdb-performance-and-scaling` (Task 30) und
  `cockroachdb-cost-and-usage-management` (Task 31) sind ebenfalls leer (nur
  `.gitkeep`). `find . -name SKILL.md` findet keinen einzigen Skill in diesen
  drei Kategorien.
- Die User-Vorgabe ("SKILL.md des jeweiligen Skills LESEN und dessen eigene
  Prozedur befolgen … nicht aus dem Gedächtnis") ist damit nicht erfüllbar: es
  gibt keine Prozedur zu befolgen.
- Stattdessen wird hier die Resilience-Frage best-effort aus dem
  Roshambo-Quellcode (read-only, Werkzeugkasten nicht verändert) **und** gegen
  die Live-Datenbank validiert. Der Quellcode ist die kanonische Quelle für das
  Lease-Schema und die TTL-Logik.

## Code-Befund — Lease-Schema und TTL-Logik (read-only)

Quelle: `C:/_Local_DEV/repos/roshambo/src/roshambo/leases.py` (Werkzeugkasten,
nur gelesen, nicht verändert). Zeilennummern als Beleg.

### acquire (`ACQUIRE_SQL`, Zeile 29–41)

```sql
INSERT INTO claims (swarm_id, resource, agent_id, intent,
                    framework_snapshot, host_snapshot, expires_at)
VALUES (%s, %s, %s, %s, %s, %s, now() + %s::INTERVAL)
ON CONFLICT (swarm_id, resource) DO UPDATE
   SET acquired_at  = now(),
       agent_id     = excluded.agent_id,
       intent       = excluded.intent,
       heartbeat_at = now(),
       expires_at   = excluded.expires_at
 WHERE claims.expires_at < now()        -- Zeile 40
RETURNING claim_id, agent_id, intent, expires_at, framework_snapshot, host_snapshot
```

Der Kommentar des Autors (Zeile 20–21) ist bereits die halbe Antwort:

> Row exists and is still valid  -> ON CONFLICT fires, the WHERE fails, zero rows back.
> Row exists and has expired      -> ON CONFLICT fires, the WHERE holds, we take it over.

Ein abgestürzter Halter hinterlässt eine Zeile mit `expires_at` in der
Vergangenheit. Der nächste `acquire` nimmt sie atomar über
(`ON CONFLICT DO UPDATE WHERE expires_at < now()`). CockroachDB läuft im
serializable Isolation — es gibt kein Fenster, in dem zwei Agents gleichzeitig
als Halter gelten.

### read / who-has (`CURRENT_HOLDER_SQL`, Zeile 45–47)

```sql
SELECT claim_id, agent_id, intent, expires_at, ...
  WHERE swarm_id = %s AND resource = %s AND expires_at > now()   -- Zeile 47
```

Abgelaufene Claims werden **als free angezeigt** — die Lese-Query filtert sie
weg. Das ist die "Garbage Collection": sie existiert nicht als eigener Prozess,
sondern lazily in jeder Lese-Query über das `expires_at > now()`-Prädikat.

### release (`RELEASE_SQL`, Zeile 57)

```sql
DELETE FROM claims WHERE swarm_id = %s AND claim_id = %s
```

`release` ist ein hartes `DELETE`. Ein Client, der mid-claim stirbt, ruft nie
`release` auf — die Zeile bleibt physisch in der Tabelle, bis ein anderer Agent
sie per `acquire` (ON CONFLICT) überschreibt. Es gibt keinen eigenen
Reaper/Sweeper, der abgelaufene Zeilen löscht; sie werden bei Übernahme
überschrieben, nicht gelöscht.

### heartbeat (`HEARTBEAT_SQL`, Zeile 51–54)

```sql
UPDATE claims SET heartbeat_at = now(), expires_at = now() + %s::INTERVAL
  WHERE swarm_id = %s AND claim_id = %s AND expires_at > now()
```

Heartbeat verlängert `expires_at` nur, solange der Claim noch nicht abgelaufen
ist. Ein abgestürzter Client kann nicht mehr heartbeat-en; sein Claim verfällt
nach der ursprünglichen TTL.

## Live-Validierung gegen die Datenbank (Echtwerte)

Zur Zeit der Bearbeitung hielten zwei Stör-Bots (aus den `storm-*.log` /
`bot-w3.json`-Lasttests bekannte BotAgent A/B contention probes) Claims, die sie
nicht aktiv freigaben:

| Task | Halter (vor Expiry) | `expires_at` (UTC) | `who-has` nach Expiry | Ergebnis |
|------|---------------------|--------------------|------------------------|----------|
| 30 | BotAgent-A@ASUS-GEI | 2026-07-30 23:24:31 | `free=true` | TTL hat freigegeben |
| 33 | BotAgent-B@ASUS-GEI | 2026-07-30 23:24:43 | `free=true` | TTL hat freigegeben |

Beide BotAgents haben kein `release` aufgerufen (Stör-Bots, die Claims als
Lasttest halten und dann sterben). Beide Ressourcen sind nach Ablauf von
`expires_at` als `free=true` ausgewiesen — ohne manuelles Eingreifen. Das ist
der empirische Beleg, dass die TTL die automatische Wiederherstellung ist.

Messung: `rsb who-has starmap:task:30` / `…:33` (Echtwerte aus der Live-DB,
nicht geschätzt).

## Was actually guaranteed

1. **Maximale Blockierung = TTL (300 s).** Eine von einem abgestürzten Client
   gehaltene Ressource ist nach spätestens `ttl_seconds` (hier 300) wieder
   verfügbar. Kein manueller Eingriff nötig.
2. **Kein doppelter Halter.** Die Übernahme erfolgt atomar über
   `ON CONFLICT DO UPDATE WHERE expires_at < now()` unter CockroachDB
   serializable. Zwei gleichzeitig startende Agents sehen nicht beide "free"
   und gewinnen — genau einer bekommt `GRANTED`, der andere `DENIED held_by=…`.
3. **Crash des Lease-Servers (DB-Node) ist kein Lease-Verlust.** Die Claims
   leben in CockroachDB, nicht im Client. Ein DB-Node-Failover unter
   serializable erhält die Zeile; `expires_at` ist ein Spaltenwert, kein
   In-Memory-Timer.

## Was NICHT guaranteed

1. **Keine vorzeitige Freigabe bei nachgewiesenem Absturz.** Es gibt keine
   Liveness-Erkennung, die eine hängende Lease vor Ablauf der vollen TTL
   freigibt. Selbst wenn der Halter nachweislich tot ist, bleibt die Ressource
   bis `expires_at` blockiert.
2. **Heartbeat kann unendig blockieren.** Ein Client, der `heartbeat`
   wiederholt aufruft ohne `release`, verlängert `expires_at` beliebig oft —
   die Ressource wird nie frei. TTL ist nur eine Wiederherstellung gegen
   *Client-Ausfall*, nicht gegen *Client-Misbehavior*.
3. **Abgelaufene Zeilen werden nicht aktiv gelöscht.** Es gibt keinen Sweeper.
   Eine nie übernommene, abgelaufene Claim-Zeile bleibt in der Tabelle (nur
   Lese-Queries blenden sie aus). Ob die Tabelle über lange Zeit wächst, wurde
   nicht gemessen (nicht task-spezifisch).

## Messbarkeit

- **Gemessen (Echtwerte aus Live-DB):** `expires_at`-Zeitstempel der
  BotAgent-Claims 30/33; `free=true` nach Ablauf.
- **Gelesen (Quellcode, read-only):** `leases.py`-SQL-Zeilen 29–57.
- **Nicht gemessen:** Physisches Löschen abgelaufener Zeilen (kein Sweeper im
  Code erkennbar); DB-Node-Failover-Verhalten (kein Failover im Versuch
  ausgelöst — wäre ein eigenes Experiment, außerhalb dieser Aufgabe).

## Abgrenzung zum bekannten Hotspot

Der in `docs/EVIDENCE-skills.md` dokumentierte `audit_log`-Hotspot wurde
gelesen und hier **nicht** wiederholt. Diese Aufgabe betrachtet Lease-TTL bei
Client-/Node-Ausfall, nicht die `audit_log`-Schreiblast.

## Fazit

Die Lease-Schicht garantiert **automatische Wiederherstellung nach
Client-Absturz innerhalb der TTL (300 s)**, implementiert als lazily
`expires_at > now()`-Prädikat in jeder Lese-Query plus atomarer
`ON CONFLICT … WHERE expires_at < now()`-Übernahme. Sie garantiert **keine**
vorzeitige Freigabe bei nachgewiesenem Absturz und **keinen** Schutz gegen
Heartbeat-Misbehavior. Der offizielle CockroachDB-Skill für die Kategorie fehlt
im Skills-Repo (leerer Ordner) — dokumentiert als Negativbefund, die Analyse
erfolgte best-effort aus Code und Live-DB.