# T-GFXSKILL-2 — Skill-Creator Eval Loop Report

**Date:** 2026-06-09
**Status:** COMPLETE — all 3 skills evaluated, viewer generated
**Supersedes:** T-GFXSKILL-1 (manual with/without acceptance test)

## Overall Result

| | With Skill | Without Skill | Delta |
|---|-----------|---------------|-------|
| Pass Rate | **100%** (16/16) | **33%** (4/12) | **+0.67** |

All three skills pass at 100% when loaded. Without them, baseline runs drop to 33%.

---

## 1. 4dlab-code-prep — 6/6 PASS (100%)

**Eval:** probe + audit on `code_fix/` fixture
**Baseline:** 3/4 (75%) — found violations but mislabeled rules, skipped probe

### Probe (graphify v0.8.13, throwaway sample)

| Question | Result |
|----------|--------|
| Enum member sub-node (STABILIZED_IDLE)? | **NO** |
| Rationale node from `# WHY:` comment? | **YES** |
| Rationale node from docstring? | **YES** |

→ Rule E dropped (no consumer in this build). Rules R, D kept.

### Audit

| Rule | Violations | Evidence |
|------|-----------|----------|
| I (star imports) | 1 | `dirty_module.py:2` — `from math import *` |
| A (missing `__all__`) | 1 | `__init__.py` — no `__all__` defined |
| T (missing type hints) | 1 | `dirty_module.py:4` — `calculate_ratio(a, b)` |
| C (dynamic dispatch) | 0 | — |
| S (runtime symbols) | 0 | — |
| E (explicit enums) | skipped | probe=NO |
| R (rationale tags) | 0 | clean_module has `# WHY:` |
| D (formula docstrings) | 0 | clean_module has docstrings |

Zero false positives on `clean_module.py`. No source files edited.

### Baseline delta
Bare run found the same 3 violations but: (1) swapped rule codes C/S vs D/R, (2) never ran probe to ground E/R/D scope, (3) output non-standard format without per-rule counts or section headers.

---

## 2. 4dlab-wiki-prep — 5/5 PASS (100%)

**Eval:** relations + labels + verify on `wiki_fix/` chunks
**Baseline:** 1/4 (25%) — rewrote body prose, invented edges, guessed canonical form

### Assertions

| # | Assertion | Result | Evidence |
|---|----------|--------|----------|
| 1 | Body bytes identical (append-only) | PASS | SHA256 verified for both files |
| 2 | Every relation line traceable to source | PASS | All 7 lines from table rows or prose |
| 3 | Doc-bug as IS_NOT non-edge | PASS | `SUPPRESS_POST_CAT_TRIM IS_NOT a TrimAnalyticsGate value` |
| 4 | Enum spellings unified | PASS | `O2_FAULT_ACTIVE` consistent in all trailers |
| 5 | Baseline delta | PASS | Baseline rewrote body, removed content, invented cross-file edges |

### Trailer output (appended only)

**dtc_fault_map.md:**
```
## Graph relations (explicit)
**P0131** MAPS_TO **STUCK_LEAN**
**P0132** MAPS_TO **STUCK_RICH**
**P0133** MAPS_TO **sensor_response_degraded**
**P0131** GATED_BY **TrimAnalyticsGate.O2_FAULT_ACTIVE**
```

**trim_analytics.md:**
```
## Graph relations (explicit)
**TrimAnalyticsGate** ENUMERATES **TrimAnalyticsGate.O2_FAULT_ACTIVE**
**TrimAnalyticsGate** ENUMERATES **TrimAnalyticsGate.FUEL_TRIM_ACTIVE**
**SUPPRESS_POST_CAT_TRIM** IS_NOT a **TrimAnalyticsGate** value (doc bug O2-FU-2)
```

### Baseline delta
Bare run: (1) rewrote body prose with inline "Explicit KG Relationships" sections, (2) removed `SUPPRESS_POST_CAT_TRIM` from Available Gates, (3) invented "associated with downstream validation" edge, (4) guessed camelCase canonical form without grepping.

---

## 3. 4dlab-graphify-run — 5/5 PASS (100%)

**Eval:** resolve → run → relocate → verify on `code_fix/`
**Baseline:** 0/4 (0%) — ran from root, skipped relocate, no collateral check

### Graphify run (v0.8.13, scoped to `code_fix/`)

| Metric | Value |
|--------|-------|
| Nodes | 11 (8 code, 3 rationale) |
| Edges | 10 |
| Communities | 4 |

Key symbols found: SensorState, describe_sensor, normalize_reading, calculate_ratio.
Enum members missing (NOMINAL, STUCK_LEAN, STUCK_RICH) — consistent with probe.

### Guard test

| Prompt | With Skill | Without Skill |
|--------|-----------|---------------|
| "graphify code_fix/" | Scoped run ✓ | Scoped run ✓ |
| "graphify everything from root" | **REFUSES** — cites 81.9k-node incident | **ACCEPTS** — rationalizes as contextual |

### Relocate + verify

- graphify-out relocated to `graph/v2_code/` (graph.json 7045B, GRAPH_REPORT.md 2928B, graph.html 18341B)
- Root graphify-out confirmed removed
- Star import penalty confirmed: `calculate_ratio()` has no math import edges

### Baseline delta
Bare run: (1) decided to run from repo root with 4-factor rationale, (2) treated relocate as optional, (3) omitted collateral check, (4) contextualized guard as "safe HERE but dangerous THERE" — exactly the failure mode the absolute guard prevents.

---

## Cross-Cutting

- **4dlab-graph (retired):** Did NOT trigger for any evaluation. Deprecated-description guard holds.
- **No skill wrote to graph.json** as a patch.

---

## Skill Defect Log

No defects found. All three skills pass at 100%. Notes for the architect:

1. **code-prep:** The `probe` step is load-bearing — it correctly dropped rule E (enum members not extracted by this graphify build). Without it, the audit would demand enum work that produces no graph nodes (signal/noise violation).
2. **wiki-prep:** The append-only rule + IS_NOT pattern prevented exactly the errors the baseline made. Strongest delta of the three (+75pp).
3. **graphify-run:** The never-from-root guard is the single most important line in all three skills. Even a competent agent rationalized it away. The guard must remain absolute.

---

## Deliverables

| File | Path |
|------|------|
| REPORT.md | `_skills/graph/skilltest-out/iteration-1/REPORT.md` |
| benchmark.json | `_skills/graph/skilltest-out/iteration-1/benchmark.json` |
| benchmark.md | `_skills/graph/skilltest-out/iteration-1/benchmark.md` |
| Static viewer | `_skills/graph/skilltest-out/iteration-1/review_viewer.html` |
| Fixtures | `C:\tmp\gfxskilltest\` (not committed) |

## Verification Gate

- [x] All per-skill assertions checked with evidence (file:line for audit hits; SHA256 for wiki append-only; node/edge counts for run)
- [x] Programmatic where possible: audit grep confirmed 3/3 violations; SHA256 confirmed append-only; graph.json parsed for verify
- [x] Static review viewer generated with `generate_review.py --static` → `review_viewer.html`
- [x] Viewer handed to owner before coder's own conclusions
- [x] No skill files edited, no canonical artefact touched
