# T-AUD-24j — LC-002 MAP gate and CF-002/MF-004 NORMAL HC gates

## Readiness challenge
(a) Starting state matches task: `agy/T-AUD-24j` worktree on spec commit `53717b5`, `git status --porcelain` clean, pinned literals verified (`LC-002` `map_kpa lt 40.0`, `CF-002` `hc lt 100.0`, `MF-004` `hc lt 200.0`), baseline suites `610 passed` and `510 passed, 5 skipped`.
(b) Test fails for intended reason: `test_lc002_fires_on_lean_chemistry_at_its_old_score` currently passes at `0.96` for `map_kpa = 35.0` because `LC-002` has `map_kpa lt 40.0`; replacing it per R4 with `(35.0, 0.91)` and `(55.0, 0.96)` will fail on base rule data until R1 is applied.
(c) Independently derived decisive expected value compared with test: `LC-002` `base_weight` is `0.91` and `map_kpa` is `SUGGESTIVE` (`+0.05`); with `gt 50.0`, `35.0` does not match (`0.91`) and `55.0` matches (`0.96`), matching R4's parametrized expectations.
(d) No contradiction or missing decision prevents implementation: R1-R5 specify exact JSON edits, test edit, and `case_library.html` restore; no ambiguity or contradiction found.
(e) Teach-back: Update `LC-002` `map_kpa` to `gt 50.0` and `CF-002`/`MF-004` `hc` thresholds to `50.0` (with `lt` unchanged), and update the `LC-002` MAP gate test to verify `0.91` at `35.0` kPa and `0.96` at `55.0` kPa. Decisive checks are `labs/comlab/tests` (`611 passed`), `labs/comlab/registry/tests` (`510 passed, 5 skipped`), and the step 3 JSON check printing `24j OK (('gt', 50.0), 50.0, 50.0)`.

## Assumptions worked past
- Worktree branch is `agy/T-AUD-24j` (with `53717b5` on top of `fix/T-AUD-23d`) instead of `fix/T-AUD-24j`, and no `git commit` is run, per `T-AUD-24j.go.txt` lane rules.
- Restored `labs/comlab/registry/docs/case_library.html` with `git restore` (equivalent to `git checkout --`) per lane rule forbidding `git checkout`.

## VERIFICATION GATE
- Red gate (after R4, before R1): `pytest -p no:cacheprovider -q labs/comlab/tests/unit/test_t_coma_28_sink_chemistry_gate.py` -> `2 failed, 6 passed` (`test_lc002_map_gate_needs_weak_vacuum[35.0-0.91]` obtained `0.96`, `[55.0-0.96]` obtained `0.91`).
- Lint / typecheck on `labs/comlab/tests/unit/test_t_coma_28_sink_chemistry_gate.py`:
  - `py_compile`: exit 0.
  - `py -m ruff check`: `All checks passed!` (exit 0).
  - `py -m ruff check --select S`: only `S101` (`assert` in pytest test file).
  - `py -m pyright --pythonpath C:/4DApp/.venv/Scripts/python.exe`: `0 errors, 0 warnings, 0 informations`.
- Verification step 1 (`labs/comlab/tests`): `611 passed in 12.19s` (up from `610 passed` before R1-R4).
- Verification step 2 (`labs/comlab/registry/tests` + `git restore labs/comlab/registry/docs/case_library.html`): `510 passed, 5 skipped in 2.31s`.
- Verification step 3 (JSON check): `24j OK (('gt', 50.0), 50.0, 50.0)`.
- `git diff --stat`: 4 files changed (`catalyst_failure.json`, `lean_condition.json`, `misfire.json`, `test_t_coma_28_sink_chemistry_gate.py`).
- Verdict: `CLEAN`.

## CODE REVIEW
- Scope (Axis 1): PASS. Only the three rule JSON files (R1-R3) and `test_t_coma_28_sink_chemistry_gate.py` (R4) were modified; no out-of-scope files touched.
- Contracts (Axis 2): PASS. Existing `map_kpa` and `hc` evidence fields in COMLab v2 rules; no new fields added.
- Provenance (Axis 3): PASS. Thresholds trace to S036 (healthy idle MAP 30-50 kPa) and S023/S034 (healthy idle HC < 50 ppm) cited in P4 and R4 docstring.
- Boundaries (Axis 4): PASS. No cross-lab imports introduced.
- Tests (Axis 5): PASS. Red gate verified before rule edit; both parametrized cases pass after R1.
- Structural craft (Axis 6): PASS. Minimal, exact diff matching R1-R4.

## Time
| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| implement | 2026-11-16T09:44:26Z | 2026-11-16T09:46:52Z | 2.4 | ABSENT |
