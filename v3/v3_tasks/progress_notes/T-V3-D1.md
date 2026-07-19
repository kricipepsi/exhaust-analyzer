# T-V3-D1 — progress note (OUTRANKED deciding-term map)

**Task:** `T-V3-D1_outranked_deciding_term.md` · **Status:** done · **Author:** Codex · **Date:** 2026-07-01
**Report:** `v3/reports/V3_OUTRANKED_MAP_2026-06-30.md`
**JSON:** `v3/reports/V3_OUTRANKED_MAP_2026-06-30.json`

## Plan

Build a read-only map for every `OUTRANKED` case from frozen on-disk artefacts only:
1. Parse `FL_LOCALIZATION_2026-06-30.md` for the 107 per-case `OUTRANKED` labels and localization evidence.
2. Parse `apps/wired/trace/runs/V7_TRACE_20260630/traces-raw.json` `phase.rank` spans for `rule_scored`, `router.winner_id`, `router.winner_score`, `router.candidates_in`, and `router.threshold_miss`.
3. Join registry rule metadata from `labs/comlab/registry/rules/*.json` to resolve rule family and base weight.
4. Emit per case: best expected-family rule, score, rank, winner rule/family/score, score margin, deciding-term text with direct trace citation and `[inferred]` markers for base-weight/uplift interpretation, and FREE/TUNABLE/HARD bucket.

Deliverables: `v3/outranked_map.py`, `v3/reports/V3_OUTRANKED_MAP_2026-06-30.md`, `v3/reports/V3_OUTRANKED_MAP_2026-06-30.json`.

## VERIFICATION GATE

```
Phase 1 Syntax/compile : PASS (`/agent_workspace/.venv-wired/bin/python -m py_compile v3/outranked_map.py`)
Phase 2 Lint           : PASS (`/agent_workspace/.venv-wired/bin/python -m ruff check v3/outranked_map.py` -> OK)
Phase 3 Types          : PASS (`/agent_workspace/.venv-wired/bin/python -m pyright v3/outranked_map.py` -> 0 errors)
Phase 4 Tests          : PASS (`/agent_workspace/.venv-wired/bin/python v3/outranked_map.py` -> FREE=38 TUNABLE=20 HARD=49; report+json written)
Phase 5 Contract       : PASS (JSON total_out_ranked=107; FREE+TUNABLE+HARD=107; FREE=38 matches T-V3-0 OUTRANKED-in-top-3 cross-check; report lists all per-case rows with citations)
Phase 6 Anti-orphan    : N-A (read-only analysis; no new field/enum/fault and no producer/consumer mapping)
Result: CLEAN
```

## CODE REVIEW

```
Scope         : PASS (new mapper plus the two contracted report artefacts; no engine/oracle/scorer/CSV edits)
Composition   : PASS (no apps/wired runtime edits, no labs/ edits, no cross-lab imports, no graphify, no Vault edits)
Consumers     : PASS (N/A for new mapped fields; output consumer is deferred rank-recovery task T-V3-4 and architect finalizing T-V3-3)
Literals      : PASS (107 and FREE=38 are cross-check constants from task/T-V3-0; 0.15 TUNABLE margin is documented report bucket semantics, not runtime logic)
Docstrings    : PASS (module and helper docstrings present)
Craft (WARN)  : depth: single read-only script with parsing/report seams only; deletion: no unused CLI options or dead fallback path; seam: no mapping logic leaks into engine/scorer; interface: public command `python v3/outranked_map.py` regenerates both artefacts
Result: CLEAN
```
