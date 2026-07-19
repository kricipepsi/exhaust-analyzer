---
title: "DEFERRED DECISION — output dataset becomes two-tier (full | basic), no PARTIAL"
lab: dnalab
role: deferred-decision
status: marked-down (NOT yet scoped, NOT a task)
date: 2026-06-12
owner: 4DApp owner
needs: dedicated research + planning before any task is authored
---

# DEFERRED — collapse output dataset confidence to two tiers: `full` | `basic`

## The decision (owner direction, 2026-06-12)

In a future build, the DNA / VehicleDNA output dataset will have **exactly two
output possibilities — `full` and `basic`. `PARTIAL` is retired.** Today the
VIN-decode channel emits `confidence = PARTIAL` almost uniformly (see
`DNA10.md` Q2 and the trace note "Traces show `confidence=PARTIAL` uniformly"),
plus `FULL`. The future model removes the middle `PARTIAL` rung entirely.

## Why this is only marked down, not started

This is **not a small rename.** It needs its own research + planning pass before
any task file is written, because at minimum it forces answers to:

- **What defines `full` vs `basic`?** Which decoded fields (engine_code,
  induction, fuel delivery, O2 config, CoC fill) must be present for `full`,
  and what is the minimum `basic` floor? This is exactly the open empirical
  question in `DNA10.md` Q2 (realistic VIN-decode resolution for 1990–2010) and
  Q3 (CoC fill, currently ~62–65%).
- **Where does the tier live?** Today it is a VINLab-produced field on
  `VinDNA`. The two-tier model may move/rename it — a schema change governed by
  `SEMANTIC_CONTRACT.md §4.x` and a `SCHEMA_VERSION` bump (currently `1.2`).
- **Who consumes the tier?** Per the signal/noise rule, a `full`/`basic` tier
  only ships if a COMLab consumer reads it (e.g. how hard COMLab leans on the
  identity/prior channel when the dataset is `basic`). That consumer + code path
  must be named before the field changes.
- **Migration:** legacy `PARTIAL` payloads already on disk / in traces — reject,
  or remap to `basic`? `from_json_payload` currently rejects any non-matching
  `schema_version`, so this interacts with the version guard.

## Disposition

Logged as a **deferred decision**, not a proposal and not a task. When the owner
greenlights it, the first step is a research note answering the `full`/`basic`
boundary + the named COMLab consumer; only then does a task file get authored.
Cross-references: `DNA10.md` Q2/Q3, `vinlab` decode-confidence field,
`SEMANTIC_CONTRACT.md` schema + version guard.
