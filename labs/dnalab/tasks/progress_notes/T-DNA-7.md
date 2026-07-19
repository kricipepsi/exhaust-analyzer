# T-DNA-7 progress note

Status: done
Date: 2026-06-12

## Scope Confirm

T-DNA-7 bumps the DNALab `VehicleDNA` umbrella `schema_version` from `1.0` to
`1.1`, keeps strict reject-on-mismatch deserialization, and round-trips only
fields already landed upstream: SymptomDNA `environmental_conditions.load_state`
and VinDNA `rated_rpm` plus the live top-level CoC fields. `fuel_type` is
excluded because T-DNA-6 registered it as proposal-only and did not add it to
live `VinDNA`. The named consumer is COMLab
`OrchestratorInboundRequest.vehicle_dna` ingestion.

## Changed Files

- `labs/dnalab/dnalab/models.py`
- `labs/dnalab/dnalab/assembly.py`
- `labs/dnalab/pyproject.toml`
- `labs/dnalab/tests/conftest.py`
- `labs/dnalab/tests/test_assembly.py`
- `labs/dnalab/tests/test_models.py`
- `labs/dnalab/tests/test_vehicledna_roundtrip.py`
- `labs/dnalab/tasks/PROGRESS.md`
- `labs/dnalab/tasks/progress_notes/T-DNA-7.md`

## Decision

Legacy v1.0 payloads are rejected, not upgraded on read. `from_json_payload()`
continues to raise `ValueError` with the expected and incoming versions, now
expecting `1.1`. This keeps the boundary explicit for COMLab: v1.1 means the
umbrella payload can carry the new sibling-lab fields, while v1.0 is a true
contract mismatch.

`build_vehicle_dna()` now requires `load_state` in the triage dict and passes it
to `symptomlab.resolve()`, matching the T-DNA-2 resolver signature.

`pyproject.toml` now points Pyright at the actual sibling lab directories
(`../vinlab`, `../symptomlab`) instead of the old `VINLab`/`SymptomLab` names, so
the required DNALab type-check command works from the lab root.

## SEMANTIC_CONTRACT.md Section 4.3 draft note

Flagged for COMLab/semantic sign-off, not directly authored in this DNALab task:

> VehicleDNA schema_version `1.1` is the umbrella payload version for the landed
> DNA-family field set: `symptom_dna.environmental_conditions.load_state`,
> `vin_dna.rated_rpm`, and the live top-level VinDNA CoC fields. Consumers must
> reject true schema mismatches rather than silently upgrade v1.0 payloads. The
> `vin_dna.fuel_type` field remains proposal-only until the paired COMLab/GASLab
> consumer lands.

## VERIFICATION GATE

- Environment: `C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe --version`
  printed `Python 3.14.5`.
- TDD red: after updating tests first, focused pytest failed on
  `TestVehicleDNASerialization.test_schema_version_value` because live DNALab
  still emitted `1.0` instead of expected `1.1`.
- Focused green: `python -m pytest tests\test_models.py tests\test_assembly.py tests\test_vehicledna_roundtrip.py -x -q --tb=short`
  passed: `26 passed`.
- Ruff: `python -m ruff check dnalab\ tests\` passed.
- Pyright: `python -m pyright dnalab\` passed: `0 errors, 0 warnings`.
- Version probe: `python -c "from dnalab.models import SCHEMA_VERSION; print('version', SCHEMA_VERSION)"`
  printed `version 1.1`.
- Full DNALab tests: `python -m pytest tests\ -x -q --tb=short` passed:
  `26 passed`.
- Anti-orphan check: `rg` confirms COMLab `OrchestratorInboundRequest` has a
  `vehicle_dna` ingestion field; COMLab projection reads `vehicle_dna_json` and
  `rated_rpm`; COMLab proposals register `load_state`, CoC path correction, and
  proposal-only `fuel_type`.
- graphify: skipped per `DNA_TASKS_START_HERE.md` Section 3.

## CODE REVIEW

- Confirmed `SCHEMA_VERSION` is `1.1` and the mismatch path still rejects legacy
  `1.0` payloads with a clear `ValueError`.
- Confirmed `build_vehicle_dna()` now requires and forwards `load_state`.
- Confirmed umbrella round-trip tests cover `load_state`, `rated_rpm`, and all
  live top-level VinDNA CoC fields without adding proposal-only `fuel_type`.
- Confirmed no `graph/` or `.sandbox-py/` artifacts were touched.
