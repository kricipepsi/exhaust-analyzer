# T-DNA-2 progress note

Status: done
Date: 2026-06-11

## Scope Confirm

Added the `load_state` environmental axis to SymptomDNA using the four
DNAresearch values from "Expanding Environmental Context Axes" and
"Conclusions": `idle`, `steady_cruise`, `transient_acceleration`, and
`coasting_deceleration`. The bounded enum change is
`SymptomDNA.environmental_conditions.load_state`, matching the draft
`SEMANTIC_CONTRACT.md` Section 4.2 JSON shape. The named signal/noise consumer is
proposed COMLab-B:
`comlab/comlab/core/fault_atlas_router.py:FaultAtlasRouter.execute_triage_loop`,
registered in `labs/comlab/comlab/config/proposals/entries.yaml` for the
context-modifier prior and 65% symptom-prior trust cap. Live COMLab arithmetic
remains out of scope.

## Changed Files

- `labs/symptomlab/symptomlab/models.py`
- `labs/symptomlab/symptomlab/validator.py`
- `labs/symptomlab/symptomlab/__init__.py`
- `labs/symptomlab/tests/test_models.py`
- `labs/symptomlab/tests/test_validator.py`
- `labs/symptomlab/tests/test_symptomdna_from_json.py`
- `labs/symptomlab/tests/test_resolve_isolation.py`
- `labs/comlab/comlab/config/proposals/entries.yaml`
- `labs/dnalab/tasks/PROGRESS.md`
- `labs/dnalab/tasks/progress_notes/T-DNA-2.md`

## Contract Amendment Draft For COMLab/Semantic Sign-Off

Draft replacement for `SEMANTIC_CONTRACT.md` Section 4.2
`environmental_conditions` block:

```json
{
  "tier_1_primary_symptom": "lack_of_power_hesitation",
  "tier_2_subfield_filter": "sudden_jerk_stumble",
  "environmental_conditions": {
    "occurs_during": "hot_only",
    "engine_state": "running",
    "load_state": "transient_acceleration"
  },
  "free_text_notes": null
}
```

`load_state` enum values:

```yaml
load_state:
  - idle
  - steady_cruise
  - transient_acceleration
  - coasting_deceleration
```

Deserialization note: pre-`load_state` payloads default to `idle` in
`SymptomDNA.from_json()` so old serialized SymptomDNA remains deterministic until
T-DNA-7 bumps the umbrella `VehicleDNA.schema_version`.

This is draft text only. The contract remains COMLab/semantic-owned and needs
sign-off before `SEMANTIC_CONTRACT.md` is edited.

## VERIFICATION GATE

- RED check before model/validator edit:
  `python.exe -m pytest tests/test_models.py tests/test_validator.py tests/test_symptomdna_from_json.py tests/test_resolve_isolation.py -x -q --tb=short`
  failed at collection with `ImportError: cannot import name 'LoadState' from
  'symptomlab.models'`, proving the tests caught the missing enum/field.
- Targeted GREEN check:
  `.venv-wired\Scripts\python.exe -m pytest tests/test_models.py tests/test_validator.py tests/test_symptomdna_from_json.py tests/test_resolve_isolation.py -x -q --tb=short`:
  passed, 58 tests.
- `.venv-wired\Scripts\python.exe -m ruff check symptomlab tests`: passed.
- `.venv-wired\Scripts\python.exe -m pyright symptomlab`: passed with 0 errors,
  0 warnings, 0 informations. Pyright also printed an update notice for 1.1.410.
- `.venv-wired\Scripts\python.exe -m pytest tests -x -q --tb=short`: passed,
  60 tests.
- Anti-orphan check:
  `rg -n "load_state" symptomlab` shows `load_state` read in
  `symptomlab/validator.py`, passed through `symptomlab/__init__.py:resolve()`,
  serialized in `symptomlab/models.py`, and migrated in `SymptomDNA.from_json()`.
- Validator smoke:
  `SymptomValidator(...).validate(..., "transient_acceleration")` returned
  `environmental_conditions.load_state == "transient_acceleration"` and
  `to_json()["environmental_conditions"]["load_state"] == "transient_acceleration"`.
- Proposal check: COMLab-B parses from `entries.yaml`, names
  `FaultAtlasRouter.execute_triage_loop`, carries the four enum values, and
  records `max_symptom_prior_weight: 0.65`.
- graphify: skipped per `DNA_TASKS_START_HERE.md` Section 3.

## CODE REVIEW

- Confirmed `LoadState` values are transcribed verbatim from DNAresearch and are
  enforced by `SymptomValidator.validate()`.
- Confirmed `EnvironmentalConditions.to_json()` emits `load_state` and
  `SymptomDNA.from_json()` rejects invalid `load_state` strings.
- Confirmed missing `load_state` deserialization is deterministic (`idle`) and
  documented for the T-DNA-7 schema-version handoff.
- Confirmed `resolve()` accepts and forwards `load_state`, avoiding a stranded
  public API boundary.
- Confirmed COMLab-B is proposal registration only; no live COMLab routing or
  prior arithmetic was changed.
