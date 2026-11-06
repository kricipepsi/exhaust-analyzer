# Result

## Status
completed

## Summary
A `will_not_start` session now gets its verdict from the `non_starter` family only (F-C1-7). The registry shim prunes every other family with `prune_reason` `family_gate`. If no `non_starter` rule fires, the shim returns `NS-NO-RULE` (`non_starter`, confidence 0.0), and the router marks it abstained with `abstain_reason` `no_rule`. Running sessions do not change: the 309 running corpus cases are identical on all six recorded fields. The UI shows "ℹ️ No confident non-start verdict:" and "Reason: no non-start rule matches the inputs" for `no_rule` (R4, K4). Golden fixture `case_014` (R5) and wiki 07 (R7) follow. One commit, `208eca3`, on `fix/T-COMA-1`.

| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| plan | 2026-11-06T08:33:11Z | 2026-11-06T08:39:47Z | 6 | ABSENT (no context meter is exposed) |
| implement (redispatch) | 2026-11-06T08:43:38Z | 2026-11-06T08:50:39Z | 7 | ABSENT (no context meter is exposed) |

Branch and log:
```
$ git -C C:/4DApp/repo branch --show-current
fix/T-COMA-1
$ git -C C:/4DApp/repo log --oneline cba05c1..HEAD
208eca3 fix(T-COMA-1): non_starter family gate and NS-NO-RULE abstain (F-C1-7)
```
Base = `cba05c1`, the newest `spec(T-COMA-1):` commit (see Decisions D1).

## Files changed
- `labs/comlab/registry/integration_shim.py`: R1 `_non_starter_gate`, the family-gate prune in `RegistryV2Router.route_case_with_diagnostics`; R2 `NON_STARTER_NO_RULE_CODE` (also in `__all__`), the NS-NO-RULE branch in `_translate_to_output(…, non_starter_gate=False)`.
- `labs/comlab/comlab/core/fault_atlas_router.py`: R3, `no_rule` abstain before the floor/margin checks, using the lazy import.
- `labs/comlab/comlab/schemas/response.py`: R3, `abstain_reason` Literal adds `"no_rule"`.
- `apps/ui/app.py`: R4 caption + K4 info line for `no_rule`. Floor/margin keep their text.
- `labs/comlab/tests/regression/fixtures/case_014_gas_dominant.json`: R5, `expected.top_fault` `NS-NO-RULE`, `fault_family` `non_starter`.
- `labs/comlab/wiki/07_pipeline_stages.md`: R7 text for §RULE_LAB_SUPPRESSION.
- `apps/wired/tests/test_t_coma_1_non_starter_family_gate.py`: R6, the 14 rehearsed tests (imports reordered by ruff, Decisions D2).
- Not committed: `labs/comlab/audit_tasks/progress_notes/T-COMA-1.md`, this RESULT.
- Runtime, outside the clone: `C:/4DApp/recheck/T-COMA-1/pt/*`, `C:/4DApp/recheck/T-COMA-1/impl/{corpus_base_mine.json,corpus_fix.json,probe_fix.txt,isolation_base.txt,isolation_fix.txt}`.

## Commands executed
All commands ran from `C:/4DApp/repo` with `PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1`, `PY=C:/4DApp/.venv/Scripts/python.exe`.
- First action / Preconditions (session 1 and redispatch); `git merge-base --is-ancestor c5371cc HEAD`.
- Base measurements (session 1): the audit probe, the rehearsed test file (`cd apps/wired && PYTHONPATH=tests pytest <recheck file>`), `probe.py`, and the comlab / registry / wired / ui suites.
- `$PY audit/tools/isolation.py` (base, then fix).
- Edits; `C:/4DApp/.venv-loop/Scripts/ruff.exe check [--fix on the new test file]`; `py -m ruff check [--select S]`; `py -m pyright --pythonpath C:/4DApp/.venv/Scripts/python.exe <5 files>`.
- `git add <7 paths>`; `git -C C:/4DApp/repo -c user.name=Claude -c user.email=noreply@anthropic.com commit -m …`.
- Mutants M1-M3 (sed edit → new file run → `git restore <path>` → `git diff --quiet`).
- `### Verification ###` steps 1-6, as written.
- K3 dump: the probe payload, captured from `diagnose()` and re-run through `RegistryV2Router().route_case_with_diagnostics`.
- Deployed-layout import sanity; anti-orphan grep.

## Validation evidence
- Step 1: new file `14 passed in 2.57s`; comlab `531 passed, 4 skipped, 2 errors in 9.75s`.
- Step 2: registry `5 failed, 502 passed, 4 deselected` (the 5 `test_build_corpus.py` failures, the same names as the base); wired `79 passed`; ui `38 passed`.
- Step 3: `15`; `['REAL-002', 'REAL-003', 'case_006', 'case_007', 'case_040']`. My `impl/corpus_fix.json` equals Cowork's rehearsed `corpus_fix.json` (`f==c: True`). The changes:
  ```
  REAL-002 ['misfire', 'MF-001', True, True, 'margin', 0.951] -> ['non_starter', 'NS-NO-RULE', True, True, 'no_rule', 0.0]
  REAL-003 ['misfire', 'MF-001', True, True, 'margin', 0.951] -> ['non_starter', 'NS-NO-RULE', True, True, 'no_rule', 0.0]
  case_006 ['invalid_input', 'II-002', True, True, 'margin', 0.96] -> ['non_starter', 'NS-004', True, False, None, 0.85]
  case_007 ['misfire', 'MF-001', True, True, 'margin', 0.951] -> ['non_starter', 'NS-NO-RULE', True, True, 'no_rule', 0.0]
  case_040 ['invalid_input', 'II-002', True, True, 'margin', 1.0] -> ['non_starter', 'NS-NO-RULE', True, True, 'no_rule', 0.0]
  ```
- Step 4: `1 passed, 10 deselected`; `suppress_gaslab: True verdict: NS-NO-RULE non_starter 0.0`. Base: `1 failed`, `assert 'rich_mixture' != 'rich_mixture'`.
- Step 5: `All checks passed!`.
- Step 6: `208eca3 fix(T-COMA-1)… / cba05c1 spec… / e0d09ab spec… / 8092b4c spec…`. Porcelain: `?? labs/comlab/audit_tasks/progress_notes/` (then also `?? labs/comlab/audit_tasks/results/` once this file exists).
- The previous decisive failure is gone. On the base, the new file gave `13 failed, 1 passed` (EF-004 / CF-001 / MF-001 / II-002 won the non-starter sessions), and the audit probe was red. Both are now green.
- P5 mutants: M1 gate off `13 failed, 1 passed`; M2 router `no_rule` off `12 failed, 2 passed`; M3 abstain verdict off `12 failed, 2 passed`. The failing names are in the note, `## Mutants`.
- K2: the isolation output is identical to the base (`diff` empty). Its 4 lines are `test_abstain_margin_002.py:20`, `test_tunable_reweight.py:23`, `:24`, `:25`.
- K3, the shim output for the `stoich` / `prolonged_crank_hard_start` probe payload (`winner_rule_id __NONE__`, 0 scored, 69 of 73 pruned with `family_gate` / `engine_state:will_not_start`; the other 4 are the `non_starter` rules, pruned by normal attribution):
  ```json
  "diagnostic_verdict": {"is_fault_detected": true, "fault_code": "NS-NO-RULE",
    "fault_name": "Engine does not start: no non-start rule matches the inputs", "fault_family": "non_starter",
    "display_headline": "Engine does not start: no non-start rule matches the inputs", "confidence_score": 0.0,
    "actionable_remediation": "Read the stored DTCs and the freeze frame, then check fuel delivery, spark and crank sensing.",
    "differential_siblings": []},
  "fault_id": "NS-NO-RULE", "ui_diagnostic_string": "Engine does not start: no non-start rule matches the inputs", "confidence": 0.0,
  "fault_enrichment": {"component_group": "engine", "impacted_subsystems": [],
    "mechanical_failure_mode": "Engine does not start: no non-start rule matches the inputs",
    "ui_remediation_steps": ["Read the stored DTCs and the freeze frame, then check fuel delivery, spark and crank sensing."],
    "editor_severity_hint": null},
  "performance_analytics.severity_level": "WARNING_DEGRADED_PERFORMANCE",
  "execution_meta.processing_confidence_rating": "DEGRADED_ASSURANCE"
  ```
  Every field equals R2.
- pyright: `0 errors, 0 warnings, 0 informations`. System ruff: `All checks passed!`. `--select S`: only the pre-existing S110 at `app.py:139` and S101 in the test file. Import sanity: `import ok`.

## Criteria
| # | status | evidence |
|---|---|---|
| 1 | MET | new file `14 passed`; comlab `531 passed, 4 skipped, 2 errors` (= P6). Mutants equal P5, and each fails the tests named in the note `## Mutants` |
| 2 | MET | registry `5 failed, 502 passed, 4 deselected`; wired `79 passed`; ui `38 passed` (= P6) |
| 3 | MET | `15` probes `NS-NO-RULE', True, True, 'no_rule', 0.0` (P3). The corpus diff is exactly the 5 `will_not_start` cases, with the values of P4. The 309 running cases are equal on all six fields |
| 4 | MET | audit probe `1 passed, 10 deselected` (P7) |
| 5 | MET | ruff `All checks passed!`. `208eca3` sits on `fix/T-COMA-1` after the spec commit `cba05c1`. Porcelain lists only the note and the RESULT (no `.blocker.json`; no hand-back) |

## Decisions the task did not specify
- D1. Base commit: Cowork committed `cba05c1 spec(T-COMA-1): file the second plan review` at 08:43:46Z, 8 s after this session started. It adds only a plan-review file. It is the newest spec commit, so I take it as the base. My commit's parent is `cba05c1`.
- D2. The rehearsed test file failed ruff `I001`. I applied ruff `--fix`, which only reorders the imports, and changed no test.
- D3. The plan's C1-C4 and C6-C8, approved by Cowork. In short: named prune constants; enrichment locals set per branch (C2, outputs unchanged for no-fault and winner); `NON_STARTER_NO_RULE_CODE` in `__all__`; the router keys on `fault_code`; the mutants are in-tree edits undone with `git restore`; the wiki text re-wrapped to ≤ 120 chars.
- D4. Commit command: `bash_guard` refuses a commit chained after `cd … &&` that holds the word Claude. I ran `git -C C:/4DApp/repo … commit` as one command.
- D5. I ran the rehearsed file on the base from `recheck/` with `PYTHONPATH=tests` (A2), so I did not copy it into the clone before the red check.

## Pre-existing changes preserved
None in the clone at the start: porcelain was empty in session 1, and at redispatch it held only my own session-1 note. The 4 base isolation violations and the 5 registry / 2 comlab pre-existing failures are unchanged.

## Rollback
`git -C C:/4DApp/repo revert 208eca3` on `fix/T-COMA-1`, or drop the commit before Cowork pushes the branch. Nothing is pushed.

## Remaining risks or uncertainties
- `_non_starter_gate` reads the directive with `getattr` (R1). A dict-shaped `routing_directive` would turn the gate off silently. No producer in the repo builds one (`lab_pipeline_aggregator.py:652`, `:676` pass the `LabRoutingDirective` object).
- NS-001..003 still never score, because GASLab marks cranking samples INVALID (P2), and case_040's P0335 is not in NS-004's list. Those sessions now abstain honestly with `no_rule` instead of a wrong family. T-COMA-3 owns this.
- F-C1-10 is unchanged: the prior re-sort can still write another rule's score into the verdict, now only among `non_starter` rules. T-AUD-2 keeps it.
- The out-of-repo Jaeger analyser will see the new `prune_reason` `family_gate`. This is telemetry only.
- No AppTest covers the R4/K4 UI branch. By ruling, it is checked by the ui suite (`38 passed`) and the diff review.
- The repo-wide lab suites and `baseline.sh` are NOT RUN. They are report-only, and Cowork runs them at review. This row edits none of those labs.
- The audit probe's docstring still quotes the old wiki sentence. Probes are not edited (skill rule).

## Revision 02

Task § R9 (spec commit `d6bdda5`). Only `apps/wired/tests/test_t_coma_1_non_starter_family_gate.py` changes:
- `test_running_session_is_not_gated` now asserts `(v.fault_family, v.fault_code) == ("ecu_fault", "EF-004")` and `not v.abstained`, in place of `!= "non_starter"`.
- `test_non_starter_dtc_rule_wins` also asserts `v.confidence_score == pytest.approx(0.85)`, `v.abstained is False` and `v.abstain_reason is None`.

Start: `fix/T-COMA-1` HEAD `d6bdda5`; porcelain held only the untracked note and RESULT. Commit: `2ba854b test(T-COMA-1): pin the running EF-004 verdict and the NS-004 score (R9)`, parent `d6bdda5`.

| step | command | expected | observed |
|---|---|---|---|
| 1 | `cd apps/wired && pytest -q -p no:cacheprovider tests/test_t_coma_1_non_starter_family_gate.py --basetemp=C:/4DApp/recheck/T-COMA-1/pt/r2new` | `14 passed` | `14 passed in 2.56s` |
| 2 (wired) | `cd apps/wired && pytest -q -p no:cacheprovider --basetemp=C:/4DApp/recheck/T-COMA-1/pt/r2wired` | `79 passed` | `79 passed in 5.20s` |
| 5 | `C:/4DApp/.venv-loop/Scripts/ruff.exe check <the 5 .py files>` | `All checks passed!` | `All checks passed!` |
| extra | pyright 1.1.410 on the test file | 0 errors | `0 errors, 0 warnings, 0 informations` |
| M1 | `_non_starter_gate` → `return False`, then `git restore` | `13 failed, 1 passed` | `13 failed, 1 passed`: the 12 `test_non_starter_without_a_matching_rule_abstains[…]` + `test_non_starter_dtc_rule_wins` |
| M2 / M3 | as in `## Mutants` | (not required by R9) | `12 failed, 2 passed` each, the same 12 tests as before |

After the mutants, `git diff --quiet` printed `restored` each time. `test_running_session_is_not_gated` passes under all three mutants. The new assertions pass on the fix, and they are pins of measured values, so they are not red-first tests. No production file changed in this revision.

Revision 02 time: | revision 02 | 2026-11-06T08:53:24Z | 2026-11-06T08:54:54Z | 1 | ABSENT (no context meter is exposed) |

Branch and log after revision 02:
```
$ git -C C:/4DApp/repo branch --show-current
fix/T-COMA-1
$ git -C C:/4DApp/repo log --oneline cba05c1..HEAD
2ba854b test(T-COMA-1): pin the running EF-004 verdict and the NS-004 score (R9)
d6bdda5 spec(T-COMA-1): revision 02 (R9): tighten two tests after the second review
208eca3 fix(T-COMA-1): non_starter family gate and NS-NO-RULE abstain (F-C1-7)
```
Status stays `completed`.
