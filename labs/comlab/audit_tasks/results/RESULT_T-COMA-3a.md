# Result

## Status
completed

## Summary
Added non_starter rule NS-005 (P0335/P0336 any_match GATING, rpm < 600 SUGGESTIVE). case_040 now names NS-005 instead of the NS-NO-RULE abstain.

## Files changed
- labs/comlab/registry/rules/non_starter.json (NS-005 added)
- labs/comlab/registry/tests/test_non_starter_rules.py (4 -> 5 rules, v7 corpus resolver, new NS-005 test)
- labs/comlab/registry/tests/test_integration_shim.py (73 -> 74 rules)
- apps/wired/tests/test_t_coma_3a_crank_sync_no_start.py (new, 3 tests)

## Commands executed
First action; red run of the new file on base; `apply_fix.py`; the `### Verification ###` block steps 1-4.

## Validation evidence
Base: new file `2 failed, 1 passed`; wired `2 failed, 102 passed`; registry `5 failed, 502 passed, 4 deselected`.
Fix: new file `3 passed`; wired `104 passed`; registry `5 failed, 503 passed, 4 deselected`; test_non_starter_rules `30 passed`; comlab `503 passed, 4 skipped, 2 errors`; corpus `corpus 314`, `differ 1` (case_040 -> NS-005); ruff `All checks passed!`.

## Criteria
1. MET: `3 passed`; `104 passed`
2. MET: `5 failed, 503 passed, 4 deselected`; `503 passed, 4 skipped, 2 errors`
3. MET: `differ 1`, the P2 case_040 line
4. MET: ruff clean; commit c596788 on fix/T-COMA-3a after the spec commit; status lists only the note and RESULT

## Decisions the task did not specify
- Commit has no Co-Authored-By trailer: bash_guard refused the commit command with it.
- non_starter.json now ends with a newline (json.dumps); the original had none.

## Pre-existing changes preserved
none (clean tree at start). The 5 registry failures are the base test_build_corpus.py failures.

## Rollback
`git revert c596788` on fix/T-COMA-3a, or reset the branch to f388565.

## Remaining risks or uncertainties
Repo-wide report-only gates (ui, six lab suites) NOT RUN; Cowork runs them.

Branch: fix/T-COMA-3a
```
c596788 fix(T-COMA-3a): NS-005 crank-sync no-start rule (P0335/P0336)
f388565 spec(T-COMA-3a): NS-005 crank-sync no-start (P0335/P0336)
```
