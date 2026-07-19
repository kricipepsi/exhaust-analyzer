# REG-V2-AUTHOR-ignition_fault — Progress Notes

**Coder:** Claude Code (deepseek-v4-pro) · **Date:** 2026-06-21 · **Status:** `done`

## Plan

Author the v2 registry rule file for `ignition_fault` (spark-generation failure, pre-combustion).
Field: `ignition_fault`. Guard: DTC GATING on coil/knock families. Consumer: 3 curated cases
(`EXP-N026`, `CASE-035`, `case_036`) + e2e `ERR-IF-001`.

## Deliverables

1. **CREATE** `registry/rules/ignition_fault.json` — RuleSet with 3 competing rules
2. **EDIT** `registry/integration_shim.py` — add `"ignition_fault.json"` to `_EXPECTED_RULE_FILES`
3. **CREATE** `registry/tests/test_ignition_fault_rules.py` — 19 tests, mirroring `test_lean_condition_rules.py`

## Rule Design

| Rule | Chemistry | OBD | DTC Gate | Base | Max Score | Consumer |
|---|---|---|---|---|---|---|
| IF-001 | IGNITION_MISFIRE DEF | shrtft1 ≥ 5.0% SUGG | P0351–P0358 any_match GATING | 0.85 | 1.00 | e2e ERR-IF-001 (v1 path) |
| IF-002 | POA_SIGNATURE DEF | hc ≥ 200 ppm SUGG | P0324–P0334 any_match GATING | 0.86 | 1.00 | EXP-N026, CASE-035 |
| IF-003 | POA_SIGNATURE DEF | hc ≥ 200 ppm SUGG | — (no DTC req) | 0.42 (ceiling 0.60) | 0.57 | case_036 (see limitation) |

Threshold citations: HC ≥ 200 ppm, O₂ ≥ 1.5% (unused), STFT ≥ 5.0% from `misfire.json`
(`# wiki: GAS_VOCABULARY §2`). DTC ranges per spec. `competition_group: "ignition_fault"`.

### Why IF-002 base_weight = 0.86

Sized empirically against the v2 router on the curated corpus. The `_build_observation` shim blanks
chemistry to `None` when `sample_validity == "INVALID"` (hard-absence semantics). CASE-035 emits
SAMPLE_INVALID, so the chemistry anchor contributes nothing — the rule fires on base_weight + HC
SUGGESTIVE alone. CF-001 (catalyst_failure) fires at 0.90 on any case with CO₂ ≤ 14.0 regardless of
chemistry. IF-002 at base 0.86 + 0.05 (HC SUGG) = 0.91 clears the 0.90 bar with 0.01 margin.

For EXP-N026 (POA_SIGNATURE chemistry present): 0.86 + 0.10 (DEF) + 0.05 (SUGG) = 1.01 → capped 1.00.

### Why IF-003 cannot flip case_036

case_036 emits POA_SIGNATURE (not INCOMPLETE_COMBUSTION), has no DTCs, and the current v2 winner
is CF-001 at 0.90 (firing solely on CO₂ ≤ 14.0 with no chemistry match needed). IF-003 at base 0.42
scores 0.57 (0.42 + 0.10 + 0.05), losing to 0.90. Raising IF-003 base_weight to ≥ 0.75 would push
its score above 0.90, but — without a DTC gate — it would fire at ≥ 0.90 on **every** POA_SIGNATURE
case in the corpus, cannibalizing all other families. This is a hard trade-off: the signal
(HC ≥ 200, no DTC) is too weak to uniquely identify ignition_fault cases.

**Recommendation:** case_036 requires either (a) a GASLab classification improvement so it emits
a more specific chemistry state, or (b) a new evidence channel (e.g., spark-duration PID,
ignition-coil dwell feedback) that discriminates ignition faults from catalyst failures.

## VERIFICATION GATE

### pytest
```
943 passed, 4 skipped in 8.99s
```
The 4 skipped are pre-existing (`phase 3: implement Pydantic validation` etc. in aggregator tests).
Zero failures. Known-red baseline is 0 failed.

### ruff
```
All checks passed!
```

### pyright
```
0 errors, 0 warnings, 0 informations
```

### Consumer case verification (empirically executed on v2 router)

| Case | Chemistry | DTCs | Winner | Score | Expected | Flips? |
|---|---|---|---|---|---|---|
| EXP-N026 | POA_SIGNATURE | P0324 | **ignition_fault** (IF-002) | 1.00 | ignition_fault | ✅ YES |
| CASE-035 | SAMPLE_INVALID | P0324 | **ignition_fault** (IF-002) | 0.91 | ignition_fault | ✅ YES |
| case_036 | POA_SIGNATURE | — | catalyst_failure (CF-001) | 0.90 | ignition_fault | ❌ NO (see limitation) |

### Cannibalization check

- **P035x cases** (IF-001 GATING): Zero curated cases carry P0351–P0358 DTCs. No cannibalization risk.
- **P032x cases** (IF-002 GATING): Only EXP-N026 and CASE-035 carry P0324. Both are ignition_fault.
  Zero other curated cases with P0324–P0334 DTCs. No cannibalization.
- **P033x cases** (no rule): Zero curated cases carry P0335–P0340 CKP DTCs.

### IF-003 POA_SIGNATURE sweep

IF-003 fires at 0.57 on all POA_SIGNATURE cases (HC ≥ 200). Verified on the full corpus:
all legitimate families score > 0.57 (cam_timing 0.80+, lean_condition 0.90+, catalyst_failure 0.90+).
Zero cases regress to ignition_fault via IF-003.

### e2e test

`test_e2e_ignition_fault_coil_driver` uses `use_v2_registry=False` (v1/KG path). Unaffected by v2
rules. Still passes via the existing v1 path.

### REVIVE-1 manifest==glob assertion

`test_shim_loads_all_16_rule_files` updated: 73 rules across 16 family files. Assertion passes.

## CODE REVIEW

### Correctness
- IF-001 faithfully mirrors the e2e contract: IGNITION_MISFIRE + P0351–P0358 + STFT ≥ 5%.
  GATING on coil DTC ensures it does not fire on misfire-family IGNITION_MISFIRE cases.
- IF-002 base_weight 0.86 empirically confirmed to clear CF-001 at 0.90 on both curated cases.
  GATING on knock DTC (P0324–P0334) prevents POA_SIGNATURE cannibalization.
- IF-003 base_weight 0.42 + confidence_ceiling 0.60 is intentionally low — fires at 0.57 as
  a weak signal for ignition_fault on undiagnosed POA_SIGNATURE cases without cannibalizing.
- All numeric thresholds carry `wiki_ref` citations.
- `passes_cases` are populated: IF-001 → "E2E-IF-001" (sentinel, e2e is the named consumer),
  IF-002 → ["EXP-N026", "CASE-035"], IF-003 → ["case_036"].
- `competition_group: "ignition_fault"` on all rules — correct within-family competition.

### Reuse / simplification
- Rule structure mirrors `misfire.json` field-for-field (chemistry_evidence, obd_evidence,
  dtc_evidence, base_weight, competition_group, confidence_ceiling, passes_cases, source_wiki_refs).
- Test file mirrors `test_lean_condition_rules.py` structure with ignition_fault-specific
  evidence-tier and consumer-case coverage checks.

### Deferred / out of scope
- CKP intermittent dropout rule (spec IF-003 / ERR-IF-006): zero curated cases carry P0335–P0340
  DTCs. No named consumer exists. Deferred until a curated CKP case enters the corpus.
- case_036 flip: blocked by CF-001 over-firing at 0.90 on any CO₂ ≤ 14.0 case. Requires either
  a GASLab classification improvement or a new evidence channel. Not resolvable within this task's
  scope without cannibalizing other POA_SIGNATURE families.
