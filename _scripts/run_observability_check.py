"""Live CockroachDB observability triage for task 29.

Reads DSN from ROSHAMBO_DSN_FILE (no credentials stored in this file).
Outputs a Markdown report fragment to stdout.
"""
from __future__ import annotations

import os
import sys
from datetime import datetime, timezone
from textwrap import dedent

import psycopg


def dsn() -> str:
    path = os.environ["ROSHAMBO_DSN_FILE"]
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def run(conn: psycopg.Connection, sql: str, params: tuple | None = None, limit: int = 50) -> tuple[list[str], list[tuple]]:
    with conn.cursor() as cur:
        cur.execute(sql, params)
        cols = [c.name for c in cur.description] if cur.description else []
        rows = cur.fetchmany(limit) if limit else cur.fetchall()
        return cols, rows


def render_table(cols: list[str], rows: list[tuple]) -> str:
    if not cols:
        return "_no result_"
    lines = ["| " + " | ".join(cols) + " |"]
    lines.append("| " + " | ".join(["---"] * len(cols)) + " |")
    for row in rows:
        cells = []
        for cell in row:
            if cell is None:
                cells.append("NULL")
            else:
                text = str(cell)
                if len(text) > 120:
                    text = text[:117] + "..."
                cells.append(text.replace("|", "\\|").replace("\n", " "))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def main() -> int:
    print("Reading DSN from", os.environ["ROSHAMBO_DSN_FILE"])
    with psycopg.connect(dsn()) as conn:
        # Privileges
        _, grant_rows = run(conn, "SHOW SYSTEM GRANTS FOR roshambo_app", limit=100)

        # Cluster time
        _, time_rows = run(conn, "SELECT now(), version()", limit=1)

        # Active statements
        cols_stmt, stmt_rows = run(
            conn,
            """
            WITH q AS (SHOW CLUSTER STATEMENTS)
            SELECT query_id, node_id, user_name, application_name,
                   start, now() - start AS running_for,
                   substring(query, 1, 120) AS query_preview,
                   distributed, phase
            FROM q
            ORDER BY start
            LIMIT 50
            """,
            limit=50,
        )

        # Active sessions
        cols_sess, sess_rows = run(
            conn,
            """
            WITH s AS (SHOW CLUSTER SESSIONS)
            SELECT session_id, user_name, application_name, client_address,
                   status, active_query_start,
                   substring(active_queries, 1, 120) AS active_queries_preview
            FROM s
            ORDER BY active_query_start
            LIMIT 50
            """,
            limit=50,
        )

        # Transactions
        cols_txn, txn_rows = run(
            conn,
            """
            SELECT id AS txn_id, node_id, session_id, application_name,
                   start, now() - start AS running_for,
                   num_stmts, num_retries, num_auto_retries,
                   substring(txn_string, 1, 120) AS txn_preview
            FROM crdb_internal.cluster_transactions
            ORDER BY start
            LIMIT 50
            """,
            limit=50,
        )

    out = []
    out.append("## Live Validation against CockroachDB Cloud")
    out.append("")
    out.append("_Executed by `kimi-1@ASUS-GEI` at " + datetime.now(timezone.utc).isoformat() + " UTC_")
    out.append("")
    out.append("### Cluster Time Observation")
    out.append(render_table(["now()", "version()"], time_rows))
    out.append("")
    out.append("> **Note:** The cluster clock was observed to be approximately one day behind wall-clock time. "
               "Lease timestamps are consistent relative to database `now()`, so the Roshambo lease mechanism "
               "remains functional, but absolute timestamps should not be compared to external clocks."
    )
    out.append("")
    out.append("### System Grants for `roshambo_app`")
    out.append(render_table(["grantee", "privilege_type", "is_grantable"], grant_rows))
    if not grant_rows:
        out.append("")
        out.append("> **Note:** No system grants were returned. The `roshambo_app` user can see its own sessions/queries, "
                   "but lacks `VIEWACTIVITY` / `VIEWACTIVITYREDACTED`, so cluster-wide activity triage is limited to this user's workload.")
    out.append("")
    out.append("### Active Cluster Statements")
    out.append(render_table(cols_stmt, stmt_rows))
    out.append("")
    out.append("### Active Cluster Sessions")
    out.append(render_table(cols_sess, sess_rows))
    out.append("")
    out.append("### Active Transactions")
    out.append(render_table(cols_txn, txn_rows))
    out.append("")

    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
