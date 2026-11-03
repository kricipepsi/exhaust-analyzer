# T-VINA-8 progress note

## Readiness challenge
(a) Starting state matches: branch `fix/T-VINA-8`, HEAD `eeeeaa9` (spec commit, child of `22a6e98`; base = `eeeeaa9`), `git status --porcelain` empty. Preconditions printed `checked`. Loop HEAD `git -C C:/4DApp rev-parse HEAD` = `78ca4e5` (not a loop row; recorded only).
(b) Tests fail for the intended reason: base symptomlab suite `63 passed`; probes `-k "f12_ or f13_"` `3 failed` (both match P1). The new tests are run red before the code edits (see below).
(c) Decisive expected values derived independently: P4 = 7 tier_1 x 3 tier_2 = 21 (yaml + validator); symptomlab 63 base + 5 new cases = 68 (the renamed test adds none); probes 3 passed.
(d) No contradiction or missing decision found. Base `22a6e98` code matches the cited anchors (`env.get("load_state", ...)` at models.py:102, "18 allowed" at models.py:9 and 86).
(e) Teach-back: make `load_state` required in `from_json`, refuse a non-string tier in `validate`, and state 21 pairs in code docstrings and docs, plus ADR-0008 superseding ADR-0003. Decisive check: step 1-5 counts `68 passed`, `5 passed`, probes `3 passed`, step 5 prints `0 0 1 1`.

## Assumptions worked past
none yet.
Red gate: before the code edits `tests/test_t_vina_8.py` gave `4 failed, 1 passed` (the 4 non-string-tier cases; round-trip passes by design).

## Assumptions worked past
- R5 covers the "7" side of P4 where the old text said "6 tier_1" / "six" / "6x3" (BDD, HLD, LLD, PRD, SYMPTOM_VOCABULARY); I changed those to 7.
- `SYMPTOM_VOCABULARY.md` §5 said the oil pairs were "proposals only" to keep the 18-pair invariant. That claim is false for the catalog, so I reworded the lead sentence: the pairs are in the live 21-pair catalog; their routing stays proposal-only. Table unchanged.
- `PRD_SymptomLab.md` "Landed" bullet said T-DNA-8 reconciled "to the full 18 pairs". It states a size, so I removed the size there rather than write 21 (history goes only in ADR-0008).
- LLD §6 literal block: added `oil_consumption` to the tier_1 list and its three tier_2 values after "see HLD §4".
- Commit trailer: the contract's attribution line was used; the commit ran as its own command (`bash_guard` refused the first attempt, which chained `git log` after it; no state changed).

## Mutants (R4)
MR1 (`env.get("load_state", LoadState.IDLE)`): `1 failed, 67 passed`; failed `test_missing_load_state_raises_validation_error`. models.py restored from `recheck/T-VINA-8/mut/`, `cmp` identical.
MR2 (`if False:`): `4 failed, 64 passed`; the 4 `test_non_string_tier_is_validation_error` cases. validator.py restored, `cmp` identical.

## VERIFICATION GATE
CLEAN. Step 1 `68 passed`; step 2 `5 passed`; step 3 dnalab `27 passed`, wired `41 passed`, ui `30 passed`, comlab `526 passed, 4 skipped, 2 errors` (the known R0-2 collection errors, same as P1); step 4 `3 passed, 48 deselected`; step 5 `0`, `0`, `1`, `1`; step 6 ruff `All checks passed!`. pyright and bandit: NOT RUN (not in this task's Verification).

## CODE REVIEW
Scope: every changed line is in `### Files to touch ###`. Diff re-read: models.py (R1 `env["load_state"]`, 2 docstrings), validator.py (R2 isinstance guard before the catalog lookup), the PIN test, the NEW test, docs. No finding. Anti-orphan: no new name beyond the test function names. The R2 text matches `must be strings` (test) and the R1 `KeyError` handler gives "Missing required field: 'load_state'".

## Time
phase | start | end | minutes | context at end
all | 2026-11-03T22:20:55Z | 2026-11-03T22:24:10Z | 3.3 | ABSENT

## Round 2
Correction 01 (spec commit `3f72ac1`). First action and Preconditions not re-run, as the correction says. Round-1 commit `4d6ee41` stays.
- R7.1 DLD `from_json` bullet and LLD `from_json` lines: `load_state` is required; a missing one raises `SymptomValidationError("Missing required field: 'load_state'")`.
- R7.2 LLD: "The 21 catalog pairs (7 tier_1 and 21 tier_2 strings)"; the live-file note now says "the catalog totals 21 pairs".
- R7.3 ADR-0008 Consequences: the "expand beyond 18" rejection is named as ADR-0007's alternative 2.
- R7.4 `models.py::from_json`: non-dict payload or non-dict `environmental_conditions` raises `SymptomValidationError("payload and environmental_conditions must be objects")`, inside the `try`, as `make_rh2.py`. 4 cases appended to `tests/test_t_vina_8.py`.

Mutant MR3 (`if not isinstance(env, dict):` made `if False:`): `3 failed, 69 passed`; the 3 `test_from_json_non_object_env_is_validation_error` cases. models.py restored from `recheck/T-VINA-8/mut/models_r2.py`, `cmp` identical.

Verification: step 1 `72 passed`; step 2 `9 passed`; step 3 `27`, `41`, `30 passed`, comlab `526 passed, 4 skipped, 2 errors`; step 4 `3 passed, 48 deselected`; step 5 `0 0 1 1` then `0 0 0 0`; step 6 ruff `All checks passed!`. Commit: round 2 on top of `4d6ee41`.
Assumptions worked past: none new. The ADR sentence was reworded so "Its rejection of" no longer appears (step 5 counts it).

### Time (round 2)
phase | start | end | minutes | context at end
round 2 | 2026-11-03T22:24:10Z (round-1 end; start not clock-read) | 2026-11-03T22:34:21Z | ABSENT | ABSENT
