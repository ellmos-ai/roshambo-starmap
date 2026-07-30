# Operator report — Roshambo field run `poc-starmap-2026-07-30`

Written by the orchestrating agent (Claude Code, Anthropic) on ASUS-GEI, 2026-07-31.
This is the coordinator's account: what was set up, what the run produced, and what is
**not** established. Numbers come from `collect_evidence.py` against the live cluster;
nothing here is estimated.

## What ran

Two machines, one CockroachDB Cloud cluster (Frankfurt, database `defaultdb`), one swarm.
Agents held leases through Roshambo and built an invented star chart, committing into one
shared repository.

**27 registered participants across 5 vendors plus scripted bots:**

| Vendor | Participants |
|---|---|
| Google (agy) | agy-1 … agy-6 @ WORKSTATION-LG |
| Anthropic (claude) | claude-code, claude-haiku, claude-sonnet, claude-opus — three model tiers @ ASUS-GEI |
| Moonshot (kimi) | kimi-1, kimi-2 @ ASUS-GEI |
| Zhipu (glm) | glm-1 @ ASUS-GEI |
| MiniMax | minimax-1 @ ASUS-GEI |
| OpenAI (codex) | codex ×2 @ ASUS-GEI |
| — (no model) | BotAgent A–C @ ASUS-GEI, A–E @ WORKSTATION-LG |

The bots are the point of a separate claim: a 200-line script registers, claims, holds,
releases and adapts its rate exactly like an LLM agent. Roshambo coordinates *processes*,
not "AI agents" — anything that speaks the protocol sits at the same table.

## What the run produced

| Measure | Value |
|---|---|
| Audit rows | 3366 |
| Distinct agents | 27 |
| Distinct claim hosts | **2** |
| Work trails | 104 (1 failure) |
| Genuine collisions | **1010** |
| **Cross-host collisions** | **145** across 92 events |
| Denials naming the actual holder | **1020 of 1020** |
| Defects (two live leases) | **3 — unexplained** |
| Star chart tasks completed | 27 of 33 |

A cross-host collision is the thing the July run could not produce: a process on one machine
refused because a process on the *other* machine holds the lease, serialized by a database
transaction. Sample line from the audit log:

```
BotAgent-C@WORKSTATION-LG was refused by BotAgent-B@ASUS-GEI  x5
```

## What is NOT established

**The three defects.** `collect_evidence.py` reports 3 cases of two simultaneously live
leases. They must be explained before anyone writes "no double grants" anywhere. Two things
are known about them: the count stayed at 3 while collisions grew from 162 to 1010, which
points to a single early episode rather than an ongoing fault; and the suspicion is a TTL
expiry with takeover, the same class of problem the July run hit with a 120s TTL.

**Two measurement mistakes happened during this run — both worth recording**, because they
show how easily this kind of claim goes wrong:

1. A bot's own detector reported a CONTRACT VIOLATION. Checked against the server audit log,
   the sequence was correct — the detector's window included the network round trip to
   Frankfurt, making sequential claims look overlapping. Fixed to measure
   `[held_from, held_until]` only.
2. The coordinator (this agent) wrote an ad-hoc checker that counted 134 "overlaps" because
   it failed to recognise releases. It was wrong, not the system. `collect_evidence.py`
   remains the only detector with a verified method.

A third mistake was made by a participating agent: it answered "no simultaneous holders"
using the *denials-naming-a-holder* figure, which measures something else entirely. That
number being 1020/1020 says nothing about overlapping leases.

## A negative finding about the CockroachDB Agent Skills

Tasks 30–32 were written by this coordinator against skill categories
(`cockroachdb-performance-and-scaling`, `-cost-and-usage-management`,
`-resilience-and-disaster-recovery`) that exist as **directories containing only
`.gitkeep`** in `cockroachlabs/cockroachdb-skills`. There is no SKILL.md to follow. The
coordinator listed the folder names without checking their contents; an agent working the
task found it and reported it rather than inventing a procedure. Recorded here as an honest
limitation of the skills collection at this date, and as a coordinator error.

The skills that *do* exist were applied for real — see `docs/EVIDENCE-skills.md` in the
Roshambo repo and `_skills/` in this workspace.

## How the shared repository came about

The first hours produced two *separate* star charts: coordination was shared, artefacts were
not, because each machine had its own workspace with no common remote. Roshambo prevented
duplicate work but nothing merged. The user caught this. A shared remote
(`ellmos-ai/roshambo-starmap`) was added mid-run and both sides pushed into it. Commits from
before that point carry their original timestamps; nothing was replayed or reconstructed.

Related and equally instructive: for a while the two machines wrote to *different databases*
on the same cluster — one DSN ended in `/roshambo`, the other in `/defaultdb`. Identical from
the outside, completely separate in effect. It surfaced only because the agent list on one
side never showed foreign agents.

## Reproducing this

```
python demo/multivendor/collect_evidence.py --swarm poc-starmap-2026-07-30
```
with `ROSHAMBO_DSN_FILE` set and `PYTHONPATH=src`, from the Roshambo repo.

Anyone without database access can reproduce the core property locally in about thirty
seconds and without an LLM key:

```
python demo/multivendor/bot_agent.py --dry-run --bots 3
```
