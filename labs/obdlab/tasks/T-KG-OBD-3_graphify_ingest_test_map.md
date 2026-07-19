# T-KG-OBD-3 — Graphify ingest of OBDLab tests → separate test-map KG

**Status:** `blocked` — needs the test code finished first · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Lane:** dedicated **KG-lane** task (the permitted graphify exception — scoped run only).
**Blocked by:** `T-TST-6` + `T-TST-8` (the generative harness must exist so the *complete* test
code is captured; the existing unit/integration/regression/pid_logset trees alone are not the whole set).
Run **after** `T-KG-OBD-2` (code map) for consistency.
**Consumer (signal/noise):** architect/coder **coverage & traceability** queries —
`/graphify query "which tests exercise translate()"`, "is `o2_normalizer` tested", test→source mapping.
This is a *different consumer* than the code map's architecture-navigation queries, hence a *different graph*.

## Why this is its own graph (two-graph decision, owner-confirmed 2026-06-09)

Test code is in scope for the KG (owner instruction "test code if it is ingested"; `audit/AUDIT_05_ecc-testing.md`
— canonical KG ingests 41 OBDLab test files → 760 nodes). But merging tests into the **code map**
(`graph/v2_code/`, `T-KG-OBD-2`) would bury every architecture query under ~760 test nodes vs ~18 production
modules — a signal/noise breach. So tests get their **own** graph, queryable independently. Mirrors the
existing wiki-KG vs code-KG separation.

## Scope decision

- **INPUT = `obdlab/tests/`** (unit, integration, regression, pid_logset, generative, fixtures).
- **OUTPUT = new `graph/v2_tests/`** — separate from `graph/v2_code/` (code map) and `graph/v2_wiki/` (wiki).
- **Do NOT merge** into `v2_code/`. Source-only AST of the test tree.

## Procedure

- Scoped run only: `/graphify obdlab/tests` → `graph/v2_tests/`. **Never** `graphify update .` from repo
  root (HARD RULE — a prior PURGE session tripped this; see obdlab PROGRESS incident note).
- Do not touch `graphify-out/` (canonical) or the other per-lab graph dirs.

## Success criteria

1. `graph/v2_tests/` built from `obdlab/tests/` only; `v2_code/` and `v2_wiki/` byte-unchanged (mtime + git).
2. Node count sane vs the test tree; a spot-check query ("tests calling `translate()`") returns the
   pid_logset + generative cases.
3. No root graphify rebuild; `graphify-out/` untouched.

## Out of scope

Production code (that is `T-KG-OBD-2`). Building/altering any test (that is the T-TST track). Merging graphs.

## VERIFICATION GATE / CODE REVIEW
(coder fills in `progress_notes/T-KG-OBD-3.md`, opening with `## Plan`.)
