# T-AUD-17 — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/drift/2026-11-05_DRIFT_REPORT_obdlab.md` (33 bullets), `reviews/REVIEW_T-AUD-11f.md`, `audit/FINDINGS.md`
F-C4-10. Rehearsal: `C:/4DApp/recheck/T-AUD-17/` (`apply_fix.py`, `tests/`, `census.sh`, `stale_patterns.txt`,
`rehearsal.patch`, `corpus_fix.json`).

### Verified context ###
1. **Code facts on `fix/T-AUD-20`** (source read): the translator's frozen branch sets `normalized_lambda = None`;
   `ve_engine.py` ends `compute_ve` with a bare `ValueError`; `analytics_preconditions.py` `ECT_WARM_THRESHOLD = 70`;
   `semantic_consistency_checker.py` `_CUTOFF_ECT_COLD = 75`, the YAML cold bucket `value: 75.0`; the translator fills
   `intake_air_temp_c` 25.0, `throttle_pos_pct` / `calculated_engine_load_pct` / `shrtft1` / `longft1` 0.0, voltage
   14.0; `ObdEmissionsView` exported by `schemas/__init__.py`, read by nothing. Observed.
2. **F-C4-10 measured:** field-name diff of `OBDLivePayload` (31) against COMLab `OBDLiveDataPayload` (58): absent from
   the mirror `calculated_engine_load_pct`, `engine_rpm`, `longft2`, `maf_status`, `map_status`, `shrtft2`. Observed
   (venv import). The FINDINGS row says four; the measured name diff is six, and the docstring names the six.
3. **`test_vocabulary.py::test_high_idle_load_is_forbidden`** scans `*.py` only; the YAML note was the one token.
   Observed.
4. **32 of 33 quotes live;** LLD:303 is gone. Observed (quote search).
5. **Rehearsal** (restored): census base `stale 20 / notes 0 / highidle 1`, after `0 / 19 / 0`; obdlab base with the new
   test `2 failed, 392 passed, 2 skipped`, after `394 passed, 2 skipped`; ruff clean (the import sits in the
   first-party block); `ast same` for `payload.py`; corpus `differ 0`; wired 106; comlab `503 passed, 4 skipped,
   2 errors` on both (`--continue-on-collection-errors`; without it pytest stops at the 2 collection errors). Observed.

### Rulings and the tradeoff that lost ###
- **R1/R3 docs follow the code.** Lost: removing the silent defaults (a behaviour change for every partial input).
- **R2 both ECT values documented; T-AUD-21 registered.** Lost: picking one now (verdicts for ECT 70-75 would move
  without a corpus check).
- **R4 a named subclass.** Lost: raising `ObdLabError` itself (a subclass lets a caller tell this case apart).
- **YAML comment reworded.** Lost: widening six doc claims to "except the YAML note".
- Code row (a raise and a class): second-model review at acceptance. Plan NONE, difficulty 2: Sonnet medium.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `stale 0`; `notes 19`; `highidle 0`; `ast same` |
| step 2 | SIMULATED | `394 passed, 2 skipped`; ruff clean |
| step 3 | SIMULATED | `corpus 314`; `differ 0`; `106 passed`; `503 passed, 4 skipped, 2 errors` |
| step 4 | SIMULATED | status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-17: OBDLab docs match the code (32 live bullets of 11f + F-C4-10); ValueError → AirMeteringStrategyError.

### Cold read ###
own pass 2026-11-07: P1-P4 measured (fact 5) · `apply_fix.py` exits on any literal count other than 1 · traceability: criteria 1-4 → steps 1-4 · 1c hits: R1 "every upheld finding" = the 32 live bullets (fact 4); R4 "No other executable line" = the raise and the new class; criterion 4 "only" = note + RESULT · test coupling: `test_vocabulary.py` scans *.py (fact 3) · no finding.
cold read 2026-11-07 FOCUSED reader; trigger 1c grep hit (R1 "every"); 0 findings, 0 patched — 3 calls.

### Correction history ###
(none)
