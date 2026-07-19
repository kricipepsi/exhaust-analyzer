# T-DNA-1 progress note

Status: done
Date: 2026-06-11

## Scope Confirm

Replaced the legacy SymptomDNA catalog with the research-revised 6 x 3 catalog from
`labs/dnalab/docs/research/DNAresearch.md` ("Revised Driveability Symptom Catalog"
and "Symptom Questionnaire Changelog"). The bounded enum change is only the
`tier_1_primary_symptom` / `tier_2_subfield_filter` vocabulary. The named
signal/noise consumer is proposed COMLab-A:
`comlab/comlab/core/fault_atlas_router.py:FaultAtlasRouter`, registered in
`labs/comlab/comlab/config/proposals/entries.yaml`. COMLab routing code and prior
probability numbers remain out of scope.

## Changed Files

- `labs/symptomlab/symptomlab/data/allowed_combinations.yaml`
- `labs/symptomlab/tests/test_validator.py`
- `labs/symptomlab/tests/test_models.py`
- `labs/symptomlab/tests/test_drift_guard.py`
- `labs/symptomlab/tests/test_symptomdna_from_json.py`
- `labs/vinlab/VehicleDNA.md`
- `labs/comlab/comlab/config/proposals/entries.yaml`

## Contract Amendment Draft For COMLab/Semantic Sign-Off

Draft replacement for `SEMANTIC_CONTRACT.md` Section 4.2 symptom catalog text:

`SymptomDNA.tier_1_primary_symptom` and `SymptomDNA.tier_2_subfield_filter` use
the revised 18-pair symptom catalog:

```yaml
combinations:
  vehicle_starting_issues:
    - no_crank_silent
    - fast_crank_whining
    - prolonged_crank_hard_start
  rough_idle_shudder:
    - constant_vibration_shudder
    - surging_hunting_idle
    - stalls_on_cold_start
  lack_of_power_hesitation:
    - flat_sluggish_always
    - hesitation_throttle_tip_in
    - sudden_jerk_stumble
  poor_economy_fuel_odor_sound:
    - just_poor_mpg
    - strong_fuel_smell
    - knock_pinging_under_load
  engine_dies_or_stalls:
    - when_coasting_to_stop
    - intermittent_random_cutout
    - backfire_loud_pop
  visible_exhaust_smoke:
    - black_smoke
    - blue_oily_smell
    - white_sweet_smell
```

Example payload update:

```json
{
  "tier_1_primary_symptom": "rough_idle_shudder",
  "tier_2_subfield_filter": "surging_hunting_idle",
  "environmental_conditions": {
    "occurs_during": "cold_only",
    "engine_state": "running"
  },
  "free_text_notes": null
}
```

This is draft text only. The contract remains COMLab/semantic-owned and needs
sign-off before `SEMANTIC_CONTRACT.md` is edited.

## VERIFICATION GATE

- RED check before catalog edit:
  `python.exe -m pytest tests/test_validator.py -x -q --tb=short`
  failed on `test_catalog_matches_revised_research_pairs`, proving the new test
  caught the legacy catalog.
- `python.exe -m ruff check symptomlab tests`: passed.
- `python.exe -m pyright symptomlab`: passed with 0 errors, 0 warnings,
  0 informations. Pyright also printed an update notice for 1.1.410.
- `python.exe -m pytest tests -x -q --tb=short`: passed, 53 tests.
- Validator invariant:
  `SymptomValidator(Path('symptomlab/data/allowed_combinations.yaml'))`: passed.
- Pair-count sanity: YAML has 6 tier_1 categories and 18 total pairs.
- Proposal consumer check: COMLab-A names
  `comlab/comlab/core/fault_atlas_router.py:FaultAtlasRouter` and has 18 mappings.
- Anti-orphan check: YAML pairs and COMLab-A proposal mappings are exactly equal
  as sets (18 == 18, equality true).
- Legacy-string check: no dropped legacy strings remain in live SymptomLab data or
  the VINLab mapping diagram. Remaining legacy strings are only in negative tests
  that assert rejection.
- graphify: skipped per `DNA_TASKS_START_HERE.md` Section 3.

## CODE REVIEW

- Confirmed `SymptomValidator` remains data-driven from
  `allowed_combinations.yaml`; no Python model field or validation shape was
  changed.
- Confirmed the hard invariant remains exactly 18 pairs.
- Confirmed dropped legacy pairs now raise `SymptomValidationError` through the
  validator.
- Confirmed COMLab-A is a proposal registration only; no COMLab routing code was
  changed.
- Confirmed the VINLab diagram no longer declares dropped legacy options.

