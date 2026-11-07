# T-COMA-9 — authoring sidecar (Windows Cowork, 2026-11-07)

Input: Linux 053 (`C:/Cowork/files/MERGE_REVIEW_4DApp_main_20261107b.md`, "Non-passing tests"). Rehearsal:
`C:/4DApp/recheck/T-COMA-9/`.

### Verified context ###
1. **On Windows at `3974488`:** `v7/tests/test_oracle_repin.py` from `apps/wired` `8 failed` (relative `CSV_PATH`),
   from the repo root `1 failed` (`test_corpus_validates`: `/agent_workspace` python); `test_build_corpus.py`
   `5 failed, 24 passed` (`_jaeger/runs/.../FAILURE_BLUEPRINT.md`, `harness/data/cases_petrol_master_v6.csv` absent,
   neither tracked). Observed.
2. **The validator was broken:** `load_corpus.py --validate` → `TypeError: _run_dtclab() missing ... 'vin_dna'`
   (the composition signature gained `vin_dna`; the dev script was not updated). Observed.
3. **The yardstick test fails on a real hash change:** `cases_petrol_v7.csv` sha256 `82780e0b…` ≠ locked `8ec81201…`;
   the last change is T-COMA-3c (`2a3b0d6`, REAL-002 relabel). → T-COMA-10. Observed.
4. **Rehearsal** (restored): validator `314/314`; oracle `8 passed` from both directories; build-corpus `24 passed,
   5 skipped`; comlab `510 passed, 4 skipped`, wired `123`, ui `70` (equal); mutant (old `_run_dtclab` call) `1 failed,
   7 passed`; ruff clean; `3 files changed, 15 insertions(+), 4 deletions(-)`. Observed.

### Rulings and the tradeoff that lost ###
- **Skip on absent data, fix the path bugs.** Lost: vendoring a small fixture of the Jaeger blueprint and master CSV
  (unknown provenance and size; Linux offered both, skip is the smaller change).
- **Yardstick out (T-COMA-10).** Lost: re-pinning the hash here (a yardstick rename is a policy decision with its own
  record).
- Plan NONE, difficulty 1. Code row (a dev tool and tests): second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `314/314`; `8 passed`; `8 passed` |
| step 2 | SIMULATED | `24 passed, 5 skipped` |
| step 3 | SIMULATED | `510 passed, 4 skipped`; `123 passed`; `70 passed` |
| step 4 | SIMULATED | ruff `All checks passed!`; `3 files changed, 15 insertions(+), 4 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-9: v7 validator runs again; oracle tests run from any dir; build-corpus tests skip without local data.

### Cold read ###
own pass 2026-11-07: P1-P2 measured (facts 1, 4) · `apply_fix.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-4 and R5 · cold read: not triggered (d1, scripted) · no finding.

### Correction history ###
(none)
