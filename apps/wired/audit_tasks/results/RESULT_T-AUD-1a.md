# Result

## Status
partial

All code, tests and gates for R0-R7 (with correction 01) are done, but the two R8 commits are not made: `bash_guard`
refuses the commit identity that `AGENTS.md` mandates. One expected-red probe (`C4 test_f3b`) turned falsely green as
a direct consequence of R5. Both are soft spec findings in
`repo/apps/wired/audit_tasks/progress_notes/T-AUD-1a.blocker.json` (validator `OK`).

Remaining work: (1) make the two commits below; (2) rule on `test_f3b_upstream_o2_override_reaches_obdlab`
(criterion 3 vs R5).

## Summary
- R1: `registry` is now an installed comlab package (`registry*` in `packages.find`, `registry.tests*` and
  `registry.tools*` excluded; package-data `registry = ["rules/*.json"]`). Editable `MAPPING` gains `registry`; a wheel
  built from a copy holds the 16 rule files and no tests/tools.
- R0: public `LabPipelineAggregator.abort_incomplete(metadata, error_code, message, *, horizon=None, echo=None)`;
  `_build_fatal_incomplete_output` delegates to it.
- R2-R5 (wired): absent/incomplete/blank triage decodes the VIN with an empty symptom; missing low-idle gas, OBD
  (O₂ key per sensor type, STFT/LTFT B1, RPM, ECT, bank-2 trims for 2 banks) or freeze frame returns
  `GAS_INPUT_INCOMPLETE` / `OBD_INPUT_INCOMPLETE` / `FREEZE_FRAME_INCOMPLETE` naming the fields. Non-starter without
  gas: "Non-start diagnosis without exhaust gas readings is not available yet." K1: public `wired.validate_triage`.
- R3/R5/R6/R7 (UI): `validate_widgets(widgets) -> list[FieldIssue]`; `app.py` shows one `st.warning` per issue and does
  not call `diagnose()`. OBD dict only when a live value is typed; DTC dict only for a valid code, MIL, or valid
  Mode 06 row (K3); DTC tokens split on `[\s,;/]+`, notes dropped, invalid tokens and Monitor IDs listed and omitted;
  high-idle help states all-or-nothing; GASLab untick/re-tick keeps the 12 gas values.

## Files changed
Uncommitted on `fix/T-AUD-1a` (base `f999f42`):
- Commit-1 set: `labs/comlab/pyproject.toml` (M), `labs/comlab/comlab/core/lab_pipeline_aggregator.py` (M),
  `labs/comlab/tests/unit/test_abort_incomplete.py` (new).
- Commit-2 set: `apps/wired/wired/composition.py` (M), `apps/wired/wired/__init__.py` (M), `apps/ui/ui_payload.py` (M),
  `apps/ui/app.py` (M), `apps/wired/tests/test_t_aud_1a_inputs.py` (new), `apps/ui/tests/test_t_aud_1a_validation.py`
  (new).
- Note and record: `apps/wired/audit_tasks/progress_notes/T-AUD-1a.md`, `…/T-AUD-1a.blocker.json`; this RESULT.
- RUNTIME: `C:/4DApp/.venv` (pip reinstall; git-ignored `comlab.egg-info`); `C:/4DApp/recheck/T-AUD-1a/` (census
  script and outputs, comlab copy, wheel, pytest basetemp, two `git show` base copies for comparison).

## Commands executed
See the progress note (`## Baseline`, `## COMLab gate block`, `## Wired gate block`, `## VERIFICATION GATE`). Key:
`timeout 290 $PY -m pip install --no-input -r requirements.txt`; the 9-probe command; `cd apps/ui && … tests`; the
three `audit/scratch/<C1|C4|C5>` commands; the import one-liner; `bash audit/tools/baseline.sh` (exact, then with
`PYTEST_ADDOPTS=--basetemp=…`); `$PY audit/tools/isolation.py`; `py -m ruff`, `py -m pyright`; the G1 census and
`diff`; the G4 wheel listing.

## Validation evidence
- Step 1: `9 passed in 5.80s` (P1 was `9 failed`).
- Step 2: `24 passed in 3.33s` (P2 was `2 failed, 6 passed`; the 2 E2E `ModuleNotFoundError` failures are gone).
- Step 3: C1 `42 failed, 2 passed`; C4 `9 failed, 3 passed`; C5 `13 failed, 6 passed`.
- Step 4: `import ok`.
- Step 5: baseline equal except this row's tests (+4 comlab, +25 wired); `violations: 4`. The exact command shows
  `PermissionError` in 4 suites from the host temp folder; the basetemp re-run gives the counts.
- Step 6: `git log --oneline audit-r2..HEAD` → empty.
- G1 corpus census: 314 cases, 311 ok, before/after diff empty. G4 wheel: 16 `registry/rules/*.json`, 0 tests, 0 tools.

## Criteria
| # | verdict | evidence |
|---|---|---|
| 1 | MET | Verification step 1 → `9 passed` |
| 2 | MET | `cd apps/ui && … tests` → `24 passed` (0 failed) |
| 3 | NOT MET (C4) | C1 42 and C5 13 held; C4 is 9, not 10: `test_f3b_upstream_o2_override_reaches_obdlab` red → green, a false pass caused by R5 (named in the note; blocker finding 2) |
| 4 | MET | NEW/PIN tags in all three test files; `labs/comlab/tests/unit/test_abort_incomplete.py` has 3 NEW; R2, R3, R5, R6 each have NEW tests in `apps/wired/tests/` or `apps/ui/tests/`; red-gate runs recorded in the note (3 failed/1 passed; 21/4; 14/2) |
| 5 | MET for the code gates | task-end gate items 1-10 clean (pyright 0 errors, ruff clean, S110 pre-existing, `violations: 4`); the note's overall verdict is BLOCKED only by criteria 3 and 6 |
| 6 | NOT MET | no commits: `bash_guard` refuses `-c user.name=Claude` (blocker finding 1) |

## Decisions the task did not specify
- `--basetemp` under `C:/4DApp/recheck/T-AUD-1a/pt/` for suites that use `tmp_path`, because the host's default pytest
  temp folder raises `PermissionError: [WinError 5]`. I did not clean the user temp folder.
- `test_r5_mode06_row_sends_dtc` is tagged PIN (it passes on the base, which sends a DTC dict whenever DTCLab is
  ticked).
- The K2 PIN tests fail on the base only by `ImportError` (the wired constants they compare are new).
- "VIN decoded" is asserted through `resolved_horizon`, because `process()` hard-codes `vin_confidence="HIGH"`
  (`lab_pipeline_aggregator.py:518`, `:589`; not edited, out of scope).
- The UI warning text is `issue.message`, which includes the field's human label.

## Pre-existing changes preserved
At the base, `git status --porcelain` showed only this row's untracked progress note. Nothing else existed to preserve.
`labs/comlab/registry/docs/case_library.html` was restored after each registry suite run.

## Rollback
Nothing is committed. `git -C C:/4DApp/repo restore <path>` for the 6 modified files, and delete the 3 new test files,
returns the tree to `f999f42`. Then rerun `$PY -m pip install --no-input -r requirements.txt` to drop `registry` from
the editable mapping.

## Remaining risks or uncertainties
- **False green:** C4 `test_f3b` now passes without F-C4-3 being fixed (the override still does not reach OBDLab).
- MIL-only or pending-only forms pass UI validation and then return `FREEZE_FRAME_INCOMPLETE` from the engine (plan
  C8, as approved).
- The UI behaviour was exercised headless (AppTest), not in a browser.
- `impl_guard` refuses Write-tool files under the RUNTIME folder `C:/4DApp/recheck/T-AUD-1a/`; Bash-produced
  runtime files there are accepted. Cowork may want the guard and the task's RUNTIME line to agree.

## Git
```
$ git -C C:/4DApp/repo branch --show-current
fix/T-AUD-1a
$ git -C C:/4DApp/repo log --oneline f999f42..HEAD
(empty: no commits, blocker finding 1)
```

Commands for Cowork to make the two R8 commits from the working tree (paths are disjoint, so the order and split are
exact):
```bash
cd C:/4DApp/repo
git add labs/comlab/pyproject.toml labs/comlab/comlab/core/lab_pipeline_aggregator.py labs/comlab/tests/unit/test_abort_incomplete.py
git -c user.name=Claude -c user.email=noreply@anthropic.com commit -m "fix(T-AUD-1a): package registry in comlab and add LabPipelineAggregator.abort_incomplete" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git add apps/wired/wired/composition.py apps/wired/wired/__init__.py apps/ui/ui_payload.py apps/ui/app.py apps/wired/tests/test_t_aud_1a_inputs.py apps/ui/tests/test_t_aud_1a_validation.py
git -c user.name=Claude -c user.email=noreply@anthropic.com commit -m "fix(T-AUD-1a): input-incomplete aborts in wired and UI field validation" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
git log --oneline audit-r2..HEAD   # expect exactly 2 lines
```
