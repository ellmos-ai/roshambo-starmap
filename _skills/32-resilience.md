# Task 32 — Resilience and Disaster Recovery Analysis (Skill: cockroachdb-resilience-and-disaster-recovery)

- **Skill:** `skills/cockroachdb-resilience-and-disaster-recovery`
- **Focus:** Verhalten von Leases bei Client-Abstürzen & Knoten-Ausfällen
- **Database:** CockroachDB Cloud Serverless (`defaultdb`)

---

## 1. Szenario A: Client-Absturz während aktiver Lease (Client Crash mid-claim)

### Verhalten & TTL-Garantie
Wenn ein Agent-Prozess mitten in der Arbeit abstürzt (z. B. Prozessabbruch `SIGKILL`, Netzwerkausfall):
1. **Kein verwaister Lock (Automatische Freigabe nach TTL):**
   Der Eintrag in `claims` bleibt unverändert mit `expires_at = acquired_at + TTL` (z. B. 300s).
2. **Abweisung anderer Agenten während TTL:**
   Versucht ein anderer Agent die Ressource vor Ablauf der TTL zu claimen, schlägt `ACQUIRE_SQL` fehl, da die Bedingung `WHERE claims.expires_at < now()` nicht erfüllt ist. `rsb.py` nennt den verstorbenen Agenten korrekt als Lease-Halter.
3. **Atomare Übernahme nach TTL-Ablauf:**
   Sobald `now() > expires_at` eintritt, greift `ACQUIRE_SQL` beim nächsten `claim`-Versuch atomar (`ON CONFLICT DO UPDATE ... WHERE claims.expires_at < now()`).
4. **Schutz vor Zombie-Reaktivierung durch `claim_id` Regeneration:**
   Bei einer Übernahme wird `claim_id = gen_random_uuid()` neu generiert. Erwacht der alte (totgeglaubte) Client später wieder und versucht ein verspätetes `heartbeat()` oder `release()`, schlägt dieses fehl (`WHERE claim_id = %s`), da seine alte `claim_id` ungültig wurde.

---

## 2. Szenario B: CockroachDB Knoten- / Netzwerkausfall (Node Failure mid-transaction)

### Verhalten & Serielle Transaktionssicherheit
1. **Raft Konsens & Range Leaseholder Failover:**
   CockroachDB repliziert Tabellen-Ranges via Raft (3-Wege-Replika). Fällt ein Knoten aus, wählt der Cluster innerhalb von Millisekunden einen neuen Range-Leaseholder.
2. **Serialisierungsfehler (`SQLSTATE 40001`):**
   Laufende explizite Transaktionen auf dem ausgefallenen Knoten werden mit `40001 SerializationFailure` abgebrochen.
3. **Automatische Client-Retry-Logik (`retry_on_serialization_failure`):**
   In `roshambo.db` fängt `retry_on_serialization_failure()` den Fehler `40001` ab und wiederholt die atomare Statement-Ausführung automatisch mit exponentiellem Backoff (Basis 20 ms, bis zu 8 Versuche).