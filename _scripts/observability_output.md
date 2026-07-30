Reading DSN from C:/_Local_DEV/CREDENTIALS/cockroachdb/roshambo.dsn
## Live Validation against CockroachDB Cloud

_Executed by `kimi-1@ASUS-GEI` at 2026-07-30T23:30:11.507609+00:00 UTC_

### Cluster Time Observation
| now() | version() |
| --- | --- |
| 2026-07-30 23:30:12.733064+00:00 | CockroachDB CCL v26.2.1 (x86_64-pc-linux-gnu, built 2026/05/21 21:07:32, go1.25.5) |

> **Note:** The cluster clock was observed to be approximately one day behind wall-clock time. Lease timestamps are consistent relative to database `now()`, so the Roshambo lease mechanism remains functional, but absolute timestamps should not be compared to external clocks.

### System Grants for `roshambo_app`
| grantee | privilege_type | is_grantable |
| --- | --- | --- |

> **Note:** No system grants were returned. The `roshambo_app` user can see its own sessions/queries, but lacks `VIEWACTIVITY` / `VIEWACTIVITYREDACTED`, so cluster-wide activity triage is limited to this user's workload.

### Active Cluster Statements
| query_id | node_id | user_name | application_name | start | running_for | query_preview | distributed | phase |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 18c735259a47e7160000000000000001 | 1 | roshambo_app |  | 2026-07-30 23:30:12.894027+00:00 | -1 day, 23:59:59.839037 | WITH q AS (SHOW CLUSTER STATEMENTS) SELECT query_id, node_id, user_name, application_name, start, now() - start AS runni | False | executing |

### Active Cluster Sessions
| session_id | user_name | application_name | client_address | status | active_query_start | active_queries_preview |
| --- | --- | --- | --- | --- | --- | --- |
| 18c7351e0562cc3a0000000000000001 | roshambo_app |  | 46.114.250.78:29742 | IDLE | NULL |  |
| 18c7351e043d550a0000000000000001 | roshambo_app |  | 46.114.250.78:14800 | IDLE | NULL |  |
| 18c7351e0a6d14200000000000000001 | roshambo_app |  | 46.114.250.78:27102 | IDLE | NULL |  |
| 18c7351e0aa2043f0000000000000001 | roshambo_app |  | 46.114.250.78:28713 | IDLE | NULL |  |
| 18c7351e0a6606380000000000000001 | roshambo_app |  | 46.114.250.78:6680 | IDLE | NULL |  |
| 18c7352583c28c4d0000000000000001 | roshambo_app |  | 46.114.250.78:14398 | ACTIVE | 2026-07-30 23:30:12.955159+00:00 | WITH s AS (SHOW CLUSTER SESSIONS) SELECT session_id, user_name, application_name, client_address, status, active_query_s |

### Active Transactions
| txn_id | node_id | session_id | application_name | start | running_for | num_stmts | num_retries | num_auto_retries | txn_preview |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 249955bf-a9f6-483a-93cb-67c774d48327 | 1 | 18c7352583c28c4d0000000000000001 |  | 2026-07-30 23:30:12.733273 | -1 day, 23:59:59.999791 | 5 | 0 | 0 | "sql txn" meta={id=249955bf key=/Min iso=Serializable pri=0.01921821 epo=0 ts=1785454212.733264467,0 min=1785454212.7332 |

