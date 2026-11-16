# T-AUD-24i — Align three COMLab values with their own vocabulary

## Readiness challenge
- **(a) Starting state matches task:** Branch `agy/T-AUD-24i` (per `.go.txt` lane rule, with `9b79bcb spec(T-AUD-24i): COMLab data to own vocabulary` above `fix/T-AUD-24h`), `git status --porcelain` clean, `overheating.json:13-14` has `"operator": "gt"` and `"value": 110.0`, `delta_engine.py:178` has `_FLATCAM_ELEV_O2_MIN: float = 2.0`, `lean_condition.json:8` has `lambda > 1.03 with`, `test_overheating_rules.py:150-158` has `test_ov001_ect_definitive_110` asserting `gt` `110.0`, and baseline suites pass at P2 (`610 passed`; `510 passed, 5 skipped`).
- **(b) Test fails for intended reason:** `test_ov001_ect_definitive_110` currently asserts `gt` `110.0`, which will fail once `overheating.json` OV-001 `ect_c` is updated to `ge` `108.0`; step 3 currently evaluates to `24i FAIL (('gt', 110.0), '2.0', False)` for the exact three unaligned values.
- **(c) Independently derived decisive expected value compared with test:** Per R1–R4 and the cited vocabularies (`OBD_VOCABULARY` `OVERHEATING_THRESHOLD` ≥ 108°C, `delta-relations/07` GAS-FC-001 O2 ≥ ~2.5, `gas_lab_ontology.yaml` `LEAN_MIXTURE` λ ≥ 1.05), the decisive expected values are `('ge', 108.0)`, `'2.5'`, and `True` (`lambda >= 1.05` in LC-001 description), matching step 3 `24i OK (('ge', 108.0), '2.5', True)` and `test_ov001_ect_definitive_108`.
- **(d) No contradiction or missing decision prevents implementation:** All four file edits (R1–R4), exclusions, and verification steps are unambiguous; lane overrides in `T-AUD-24i.go.txt` cleanly govern branch name, no-commit, and Python/cache rules.
- **(e) Teach-back:** Update OV-001 `ect_c` in `overheating.json` to `ge 108.0` (and its test `test_ov001_ect_definitive_108` in `test_overheating_rules.py`), `_FLATCAM_ELEV_O2_MIN` in `delta_engine.py` to `2.5`, and LC-001's description in `lean_condition.json` to `lambda >= 1.05`. The decisive check is both COMLab pytest suites passing at P2 (`610 passed` and `510 passed, 5 skipped`, `0 failed`) and Verification step 3 printing `24i OK (('ge', 108.0), '2.5', True)`.

## Assumptions worked past
- Lane rules in `T-AUD-24i.go.txt` override the task header's branch name (`agy/T-AUD-24i` instead of `fix/T-AUD-24i`), forbid git commits/checkouts of branches, and skip pasting git branch/log into `RESULT_T-AUD-24i.md`.
- `git checkout -- labs/comlab/registry/docs/case_library.html` is explicitly required by R5 / Verification step 2 to restore the CRLF-rewritten tracked file after running `labs/comlab/registry/tests` (it is a path restore, not a branch checkout).

## VERIFICATION GATE
- **Step 1 (`labs/comlab/tests`):** `C:/4DApp/.venv/Scripts/python.exe -m pytest -p no:cacheprovider -q labs/comlab/tests` -> `610 passed in 12.21s` (`0 failed`, matches P2).
- **Step 2 (`labs/comlab/registry/tests` + restore):** `C:/4DApp/.venv/Scripts/python.exe -m pytest -p no:cacheprovider -q labs/comlab/registry/tests` -> `510 passed, 5 skipped in 2.19s` (`0 failed`, matches P2); `git checkout -- labs/comlab/registry/docs/case_library.html` restored CRLF-rewritten HTML.
- **Step 3 (value check):** `C:/4DApp/.venv/Scripts/python.exe -I -c "..."` -> `24i OK (('ge', 108.0), '2.5', True)`.
- **Inner loop (`py_compile`, `ruff`, `pyright`):** `py_compile` passed (exit 0); `ruff check` on `delta_engine.py` and `test_overheating_rules.py` passed (`All checks passed!`); `ruff check --select S` clean on `delta_engine.py` (39 pre-existing `S101` assert warnings in `test_overheating_rules.py`); `pyright` 0 errors on `test_overheating_rules.py` and 12 pre-existing `reportOptionalMemberAccess` errors in `delta_engine.py` (lines 326-329, 485-490, unrelated to line 178).
- **Git scope:** `git diff --stat` touches only the 4 code/data/test files (`delta_engine.py`, `lean_condition.json`, `overheating.json`, `test_overheating_rules.py`); `git status --porcelain` shows only those 4 plus `progress_notes/T-AUD-24i.md`.

## CODE REVIEW
- **Scope:** PASS — only R1–R4 changes in the 4 declared files plus progress note and result file.
- **Contracts:** PASS — OV-001 `ect_c` aligns with `OBD_VOCABULARY §23.1` (`ge 108.0`), `_FLATCAM_ELEV_O2_MIN` aligns with `delta-relations/07` (`2.5`), LC-001 description aligns with `GAS_VOCABULARY §3` (`lambda >= 1.05`).
- **Provenance:** PASS — `delta_engine.py:178` retains `# wiki: delta-relations/07 — flat cam breathing misfire, elevated O2 ≥ ~2.5`; JSON rules retain `wiki_ref`.
- **Boundaries:** PASS — no cross-lab imports added or modified.
- **Tests:** PASS — `test_ov001_ect_definitive_108` asserts `ge` `108.0` with exact required message; all 610 + 510 tests pass (`0 failed`).

## Time
| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| implement & verify | 2026-11-16T08:49:14Z | 2026-11-16T08:50:40Z | 1.45 | ABSENT |
