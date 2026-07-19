# T-DNA-4 progress note

Status: done
Date: 2026-06-11

## Scope Confirm

Canonical shape decision: CoC empirical fields consumed by GASLab stay top-level
on `VinDNA` as `vin_dna.*`, matching GASLab wiki `01_role_boundaries_dna_ingestion`
lines 89-90 and the live GASLab DNA view. Emissions equipment stays nested under
`vin_dna.emissions.*`: `has_catalyst`, `egr_equipped`, `downstream_o2_present`,
and `downstream_trim_role`. `secondary_air_equipped` is not resurrected; GASLab's
current DLD states it was removed because it has no consumer. The named consumers
are GASLab CoC threshold/Brettschneider logic for `target_lambda_v112`,
`co_low_idle`, and `co_high_idle`, plus GASLab/DTC catalyst and EGR routing for
the emissions flags. The paired COMLab fix remains COMLab-C and is registered as
a proposal; this DNA task does not edit `projection.py`.

## Changed Files

- `labs/vinlab/vinlab/models.py`
- `labs/vinlab/tests/test_models.py`
- `labs/comlab/comlab/config/proposals/entries.yaml`
- `labs/dnalab/tasks/PROGRESS.md`
- `labs/dnalab/tasks/progress_notes/T-DNA-4.md`

## Canonical Shape Decision

- Keep `target_lambda_v112`, `co_low_idle`, and `co_high_idle` as top-level
  `vin_dna.*` fields. COMLab-C must stop reading them from `emissions`.
- Keep `has_catalyst` and `egr_equipped` under `vin_dna.emissions.*`. COMLab-C
  must stop reading them from the top level.
- Keep `downstream_o2_present` and `downstream_trim_role` under
  `vin_dna.emissions.*`; they are part of downstream O2/catalyst strategy.
- Do not add `secondary_air_equipped` back to VINLab or the contract in this
  task. GASLab DLD notes `secondary_air_equipped` was removed because it has no
  consumer.
- Preserve `VinDNA.from_json()` symmetry for nested `has_catalyst`; before this
  task it silently reset `has_catalyst=False` to the default `True`.

## Contract Amendment Draft For COMLab/Semantic Sign-Off

Draft replacement/addition for `SEMANTIC_CONTRACT.md` Section 4.1 `VinDNA`:

```yaml
emissions:
  type: object
  fields:
    upstream_o2_type:
      type: enum
      semantics: upstream oxygen sensor type
    downstream_o2_present:
      type: bool
      semantics: downstream oxygen sensor is physically present
    downstream_trim_role:
      type: enum
      semantics: downstream O2 use, either catalyst-monitor-only or secondary
        fuel-trim capable
    has_catalyst:
      type: bool
      semantics: catalytic converter present; gates catalyst diagnostics and
        healthy-catalyst masking logic
      consumers:
        - GASLab catalyst-gated fault suppression
        - DTCLab CATALYST_HISTORY routing
        - COMLab catalyst analytics
    egr_equipped:
      type: bool
      semantics: EGR equipment present; gates EGR fault routing
      consumers:
        - GASLab EGR_STUCK_* fault suppression
        - DTCLab EGR_HISTORY routing

target_lambda_v112:
  type: float | null
  path: vin_dna.target_lambda_v112
  semantics: certified CoC lambda center value
  consumer: GASLab Brettschneider/CoC lambda window

co_low_idle:
  type: float | null
  path: vin_dna.co_low_idle
  semantics: per-vehicle CoC idle CO ceiling
  consumer: GASLab per-vehicle idle CO threshold

co_high_idle:
  type: float | null
  path: vin_dna.co_high_idle
  semantics: per-vehicle CoC high-idle / 2500 RPM CO ceiling
  consumer: GASLab rich-CO ceiling when confidence is HIGH
```

Fields already present on `VinDNA` but not included above remain unformalized
until a live or paired proposed consumer is named. This avoids converting
unconsumed CoC/type-approval/noise data into contract surface.

## Per-Field Consumer Audit

| Field | Consumer proof | Disposition |
|---|---|---|
| `target_lambda_v112` | `gaslab/rule_engine.py` reads `dna.target_lambda_v112`; GASLab wiki line 123 says consumed by Brettschneider mixture evaluation. | Keep, contract top-level |
| `co_low_idle` | `gaslab/rule_engine.py` reads `dna.co_low_idle`; GASLab wiki line 124 says consumed by per-vehicle CoC threshold tables. | Keep, contract top-level |
| `co_high_idle` | `gaslab/resolution.py` reads `dna.co_high_idle`; GASLab docs tie it to the 2500 RPM/rich-CO ceiling. | Keep, contract top-level |
| `has_catalyst` | GASLab docs/vocabulary gate catalyst faults; DTCLab wiki gates `CATALYST_HISTORY`; COMLab analytics reads `has_catalyst`. | Keep, nested under `emissions` |
| `egr_equipped` | GASLab docs/vocabulary gate EGR faults; DTCLab wiki gates `EGR_HISTORY`. | Keep, nested under `emissions` |
| `downstream_o2_present` | COMLab ingestion and catalyst analytics read it; paired with downstream O2 strategy. | Keep, nested under `emissions` |
| `downstream_trim_role` | COMLab ingestion validates it and perception contradiction logic consumes it. | Keep, nested under `emissions` |
| `co_type_approval` | GASLab vocabulary lists intended threshold use, but `rg` found no live code read in GASLab/COMLab/DTC/OBD. | Proposal-only; do not formalize yet |
| `hc_type_approval` | GASLab vocabulary lists intended threshold use, but `rg` found no live code read in GASLab/COMLab/DTC/OBD. | Proposal-only; do not formalize yet |
| `nox_type_approval` | GASLab vocabulary lists intended threshold use, but `rg` found no live code read in GASLab/COMLab/DTC/OBD. | Proposal-only; do not formalize yet |
| `target_rpm_u2` | No live consumer found by `rg` across GASLab/COMLab/DTC/OBD. | Prune/proposal later; not contract |
| `idle_rpm_low` | No live consumer found by `rg` across GASLab/COMLab/DTC/OBD. | Prune/proposal later; not contract |
| `hc_nox_type_approval` | No live consumer found by `rg` across GASLab/COMLab/DTC/OBD. | Prune/proposal later; not contract |
| `co2_type_approval` | No live consumer found by `rg` across GASLab/COMLab/DTC/OBD. | Prune/proposal later; not contract |
| `noise_stationary_dba` | No live consumer found by `rg` across GASLab/COMLab/DTC/OBD. | Prune/proposal later; not contract |
| `noise_rpm` | No live consumer found by `rg` across GASLab/COMLab/DTC/OBD. | Prune/proposal later; not contract |
| `noise_driving_dba` | No live consumer found by `rg` across GASLab/COMLab/DTC/OBD. | Prune/proposal later; not contract |
| `secondary_air_equipped` | GASLab DLD says removed because no consumer; no VINLab field exists. | Pruned; do not add |

## COMLab-C Registration

`labs/comlab/comlab/config/proposals/entries.yaml` now contains `COMLab-C` with
path fixes for:

- `target_lambda_v112`: `vin_dna.emissions.target_lambda_v112` -> `vin_dna.target_lambda_v112`
- `co_low_idle`: `vin_dna.emissions.co_low_idle` -> `vin_dna.co_low_idle`
- `co_high_idle`: `vin_dna.emissions.co_high_idle` -> `vin_dna.co_high_idle`
- `has_catalyst`: `vin_dna.has_catalyst` -> `vin_dna.emissions.has_catalyst`
- `egr_equipped`: `vin_dna.egr_equipped` -> `vin_dna.emissions.egr_equipped`

## VERIFICATION GATE

- RED check before implementation:
  `python3.14 -m pytest tests\test_models.py::test_vin_dna_to_json_uses_canonical_coc_and_emissions_paths -q --tb=short`
  failed on `assert True is False` for `round_tripped.emissions.has_catalyst`,
  proving the test caught the missing nested round-trip field.
- Targeted GREEN check:
  `python3.14 -m pytest tests\test_models.py::test_vin_dna_to_json_uses_canonical_coc_and_emissions_paths -q --tb=short`:
  passed, 1 test.
- Syntax:
  `python3.14 -m py_compile vinlab\models.py tests\test_models.py`: passed.
- Ruff:
  `python3.14 -m ruff check vinlab tests\test_models.py`: passed.
- Pyright:
  `python3.14 -m pyright vinlab`: passed with 0 errors, 0 warnings, 0 informations.
- Targeted model suite:
  `python3.14 -m pytest tests\test_models.py -x -q --tb=short`: passed, 16 tests.
- Full VINLab test suite:
  `python3.14 -m pytest tests\ -x -q --tb=short`: passed, 170 tests, 3 skipped.
- Serialized path smoke:
  `python3.14 -c "... VinDNA(...).to_json() ..."` confirmed top-level CoC `True`,
  nested CoC `False`, top-level catalyst `False`, emissions nested `True`, and
  round-trip catalyst false `True`.
- Proposal parse:
  `python3.14 -c "... yaml.safe_load(... entries.yaml) ..."` loaded 12 entries and
  confirmed `COMLab-C True`.
- Consumer proof:
  `rg -n "target_lambda_v112|co_low_idle|co_high_idle|has_catalyst|egr_equipped" labs/gaslab labs/dtclab`
  found live GASLab code/docs and DTCLab wiki consumers, including
  `gaslab/rule_engine.py`, `gaslab/resolution.py`, `gaslab/dna_view.py`, and
  `dtclab/wiki/07_catalyst_egr_evap.md`.
- graphify: skipped per `DNA_TASKS_START_HERE.md` Section 3.

## CODE REVIEW

- Confirmed the production diff is minimal: `VinDNA.from_json()` now preserves
  nested `emissions.has_catalyst`; no schema field was moved.
- Confirmed `VinDNA.to_json()` already emitted CoC fields top-level and emissions
  flags nested; the new test pins that contract against future drift.
- Confirmed COMLab-C is registration only and does not edit out-of-scope
  `projection.py`.
- Confirmed no `graph/` or `.sandbox-py/` artifacts were touched.
- Confirmed existing unrelated dirty worktree changes were not reverted or staged.
