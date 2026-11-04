# T-VINA-15 — authoring sidecar (Windows Cowork, 2026-11-04)

### Verified context ###
1. Population (P1, `recheck/T-VINA-15/measure.py`): 68 shipped rows store 0/0 (the ledger's "13" was the real-VIN
   count, and it still holds: 13 real C6 VINs reach these rows). None is a carburettor engine.
2. Cause: `tools/build_vref_db.py` writes `bool(e.get("has_maf", False))` (both write sites), so "not stated" becomes 0.
3. Design 1 (NULL the 68 rows in `vref.db`, fix the builder) broke the T-VINA-13b merge tests: they rebuild the
   pre-merge file under `has_maf NOT NULL` and pin a digest of the original rows (26 errors, 1 failure on the copy).
4. Design 2 rehearsed (`rehearse.sh`): vinlab `353 passed, 8 skipped`; new file `9 passed`; M1, M2 `3 failed`, M3
   `1 failed`; downstream and probes equal to the base; 13 real VINs change, all to the heuristic.

### Rulings and the tradeoff that lost ###
- Decoder-side: a stored 0/0 is read as unknown. Lost: correcting the data (design 1), which rewrites rows that the
  T-VINA-13b history pins; the data keeps an ambiguous 0/0, documented at the rule.
- The heuristic result (`DUAL_MAF_MAP_CROSSCHECK` for the 13, via `has_egr = 1`) is accepted as the documented unknown
  path. Lost: per-engine sourcing (no source on this host names each engine's sensors).
- The `is not None` guards stay, pinned by M3: a row with one stated sensor keeps it.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | copy: `353 passed, 8 skipped` |
| step 2 | SIMULATED | copy: `9 passed`; M1-M3 as R3 |
| step 3 | SIMULATED | copy on `PYTHONPATH`: 27, 41, 30 |
| step 4 | SIMULATED | copy: `14 passed, 37 deselected` |
| step 5 | SIMULATED | `effect.py` copy vs archived base: `changed 13`; base vs base `changed 0` |
| step 6 | SIMULATED (ruff) / DEFERRED (commit) | `All checks passed!` |

### Exclusivity ###
No other implementer runs. Built on `fix/T-VINA-19` (`5307de4`).

### Progress hook ###
T-VINA-15: 0/0 vref rows decode via the heuristic; 13 real VINs leave the sensorless MAP_ONLY state.

### Cold read ###
own pass 2026-11-04: anchor `db_map = db_dict.get("has_map")` grep 1 · P1 measured · P2 on the copy · traceability:
criteria 1-4 → steps 1-6 · JUDGEMENT criteria: 0.
cold read 2026-11-04: skipped (Plan: NONE, difficulty 2, rehearsed edits and mutants).

### Correction history ###
- **01 (2026-11-04, Cowork review of round 1 with the second review; not accepted).** Round 1 equals `make_rh.py`
  byte for byte; Cowork's rerun matches P2. Second review (Codex) APPROVE WITH CORRECTIONS: MEDIUM one-sided reset
  mutant (`db_maf = None` only) survives UPHELD → R5.2 (rehearsed M4 `2 failed`); LOW the rule is not scoped to
  injected engines UPHELD → R5.1, R5.3 (M5 `1 failed`). Rehearsed `make_rh2.py`: vinlab `354 passed, 8 skipped`,
  file `10 passed`, real VINs against round 1: 0 changed. Step 5's base pinned to `51566ca`.
