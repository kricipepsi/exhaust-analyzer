# T-FL-4 — progress note

**Task:** [[T-FL-4_v3_scoreboard]]  
**Date:** 2026-06-30  
**Harness:** `apps/wired/fl_tasks/score_v3_yardstick.py`  
**README:** [[FL_SCOREBOARD_README_2026-06-30]]  
**Mode:** STRICT, measure-only.

## Work completed

- Added a one-command scoreboard harness under `apps/wired/fl_tasks/score_v3_yardstick.py`.
- Reused the existing v7 scorer contract by importing `v7.run_suite.score_case` and the public `wired.composition.diagnose` path; no scorer fork and no v3-specific expectation.
- Bound the command to [[FL_YARDSTICK_2026-06-30]] via the frozen CSV, oracle-subset, and scorer SHA-256 values.
- Joined scored rows to [[FL_LOCALIZATION_2026-06-30]] so before/after output reports per-family movement and per-mode remaining primary misses.
- Wrote [[FL_SCOREBOARD_README_2026-06-30]] with commands, hash-lock behavior, the explicit new-yardstick override path, and null-result interpretation.
- No engine, oracle, lab, wiki, CSV, trace, or v7 run JSON edits.

## Baseline reproduction output

Command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score
```

Observed live current-engine output (noise suppressed by default):

```text
Hash lock: PASS
Result source: current installed wired engine
Build: git_sha=3341e42d2aa8d2ebc201014a08e6a1591e3291d4 env=(USE_V2_REGISTRY=<unset>, WIRED_OTEL=<unset>) label=current-engine

OVERALL PRIMARY ROUTING
  family+state: 133/294 = 45.24 %
  family only : 141/294 = 47.96 %
  state only  : 275/294 = 93.54 %
  adjudicated : 143/294 = 48.64 % (ORACLE_SUSPECT +10)
```

Per-mode baseline reproduction:

| Mode | Bucket | Primary pass | Remaining miss |
|---|---:|---:|---:|
| SURFACE_DEFECT | 133 | 133 | 0 |
| ORACLE_SUSPECT | 10 | 0 | 10 |
| PRODUCER_GAP | 25 | 0 | 25 |
| PRUNED_OTHER | 0 | 0 | 0 |
| OUTRANKED | 107 | 0 | 107 |
| DATA_GAP | 19 | 0 | 19 |

Surface-dimension reproduction uses the T-FL-1 non-fail convention (`PASS + NA`): `fault_code` 0/294 non-fail, `confidence` 21/294 non-fail, `perception_gap` 194/294 non-fail, `demotion_note_contains` 289/294 non-fail.

## Self-comparison output

Command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py compare \
  --before apps/wired/v7/runs/20260630_163900/results.json \
  --after apps/wired/v7/runs/20260630_163900/results.json
```

Observed:

```text
OVERALL DELTA (primary family+state; higher is better)
  133/294 (45.24 %) -> 133/294 (45.24 %); Δ +0 cases / +0.00 pp
```

All per-family rows showed `Δ cases +0` / `Δ pp +0.0`; all per-mode rows showed `Δ misses 0`.

## Hash-lock refusal output

A temporary CSV copy with one extra trailing newline was written at `/tmp/cases_petrol_v7_hash_mismatch.csv` and used only to prove refusal.

Command:

```bash
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score \
  --csv /tmp/cases_petrol_v7_hash_mismatch.csv \
  --results apps/wired/v7/runs/20260630_163900/results.json
```

Observed exit code: `2`.

```text
ERROR: hash-lock refusal: FL_YARDSTICK_2026-06-30 mismatch (csv_sha256: expected a94a7731bcc55a1ab826bdc46d5c9658d47dd86984902e3c93d7bab3be02a2ae observed 0e2aa8d2f8825a6e931187e9fe247737a8d377193563351ffe33ed1470aabae5). Create a new named yardstick or rerun with --allow-new-yardstick NAME.
```

## VERIFICATION GATE — T-FL-4

1. Compile : PASS  (`/agent_workspace/.venv-wired/bin/python -m py_compile apps/wired/fl_tasks/score_v3_yardstick.py`)
2. Lint    : PASS  (`/agent_workspace/.venv-wired/bin/python -m ruff check apps/wired/fl_tasks/score_v3_yardstick.py` -> OK)
3. Types   : PASS  (`/agent_workspace/.venv-wired/bin/python -m pyright apps/wired/fl_tasks/score_v3_yardstick.py` -> 0 errors, 0 warnings, 0 informations)
4. Tests   : PASS  (`score` live current engine -> 133/294 = 45.24%; `score --results 20260630_163900` -> 133/294 = 45.24%; `compare` baseline against itself -> all-zero deltas; hash-lock mismatch -> refused with exit code 2)
5. Contract: PASS  (command prints overall primary routing, per-family routing, per-mode remaining misses, surface dimensions, and build identity; compare prints overall, per-family, and per-mode deltas; hash lock enforces frozen CSV/oracle/scorer hashes)
6. Orphan  : N-A   (no mapped lab field or COMLab consumer added; named consumers are v3 reviewer/coders via reports)
Result: CLEAN

## CODE REVIEW — T-FL-4

Scope         : PASS  (changed files are limited to `apps/wired/fl_tasks/score_v3_yardstick.py`, `apps/wired/fl_tasks/reports/FL_SCOREBOARD_README_2026-06-30.md`, this progress note, and FL/V7 ledger close-out links)  
Composition   : PASS  (no engine/lab/oracle/wiki/CSV edits; no cross-lab source imports beyond the existing wired harness path; no deferred path; no `ARCHIVE` import; no `graphify`)  
Consumers     : PASS  (no mapped lab field added; report consumers are v3 reviewer/coders and the owner acceptance review)  
Literals      : PASS  (hash constants are frozen T-FL-1 artefact values; no diagnostic boundary literal added)  
Docstrings    : PASS  (new public CLI/helper functions carry docstrings)  
Craft (WARN)  : depth=single harness seam under `fl_tasks/`; deletion=output JSON writer is only used behind `--write-results`; seam=reuses `diagnose`, `row_to_raw_inputs`, and `score_case` rather than forking v7 scoring; interface=verified through CLI commands against frozen result JSON and live current engine.  
Result: CLEAN
