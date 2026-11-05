# T-AUD-4d progress note

## Readiness
(a) Start matches: branch fix/T-AUD-4d, base spec commit a830148 (descendant of f57207a), `git status --porcelain` empty, preconditions print `checked`.
(b) Test fails for the intended reason: to be recorded below after the red run with composition.py restored to base.
(c) Decisive expected value: P2 VIN VF7SA5FR8AW511081 (HIGH, egr_equipped False) with $03 P0401: base tags `('EGR_HISTORY',)`, fixed `()`; corpus digest f5414b25634aae41.
(d) No contradiction found; all cited paths exist.
(e) Teach-back: composition builds a DtcLabDnaView from vin_dna (after overrides) and passes it to DataFusionSanitizer, so HIGH-confidence gates drop EGR_HISTORY for an EGR-less vehicle and de_cat reaches DTCLab. Decisive check: the 13-test file fails on base and passes with the fix, wired 62 passed, corpus digest unchanged.

## Assumptions worked past
- I follow the shape of Cowork's apply_fix.py (task allows it).

(b) recorded: with composition.py at base the new test file fails at collection, `ImportError: cannot import name '_build_dtc_dna_view'` (intended reason: the helper does not exist).

## Assumptions worked past
- Pyright (task-end gate 2) rejected Cowork's str-for-enum arguments (5 errors). I wrapped them in `DtcAirMeteringStrategy`, `ResolvedHorizon`, `EuroEmissionCategory`, `DtcVinConfidence`, `DtcEmissionsView`. The DTC enums are aliased because composition already imports COMLab's `AirMeteringStrategy` and `VinConfidence`. Behaviour is the same (suites and digest equal).

## Mutants (R4)
| mutant | failing tests |
|---|---|
| no view (`DataFusionSanitizer()`) | test_high_egr_less_vehicle_drops_egr_history, test_de_cat_override_reaches_dtclab (2 failed) |
| HORIZON_ADAPTIVE -> HORIZON_MODERN | test_enum_mapping[resolved_horizon-HORIZON_ADAPTIVE-HORIZON_CLASSIC] (1 failed) |
| `model_year is None` check removed | test_unknown_required_field_gives_no_view[change0] (1 failed) |
Mutants ran against the pre-pyright-fix file; the file was restored from a copy after each.

## VERIFICATION GATE
CLEAN. new file 13 passed; wired 62 passed; dtclab 590 passed; ui 30 passed; comlab 526 passed, 4 skipped, 2 errors (R0-2); corpus `cases 207 exceptions 1`, `tag sets 206 digest f5414b25634aae41`; ruff All checks passed; ruff --select S only S101 on test asserts; pyright 0 errors; deployed-layout import ok.

## CODE REVIEW
Scope: composition.py and the new test only. Contract: `# consumer:` comment on confidence names routing_tag_mapper gates. Provenance: both tables cite DTC_VOCABULARY.md section 14.1. Anti-orphan: `_build_dtc_dna_view` read by `_run_dtclab`. No findings.

## Time
| phase | start | end | minutes | context |
|---|---|---|---|---|
| all | 2026-11-05T16:53:52Z | 2026-11-05T16:57:42Z (code commit; RESULT after) | 3.8 | ABSENT |
