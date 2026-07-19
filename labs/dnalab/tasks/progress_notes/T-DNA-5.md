# T-DNA-5 progress note

Status: done
Date: 2026-06-11

## Scope Confirm

T-DNA-5 measures whether `D3_commercial_name` / model adds diagnostic signal
beyond `P15_engine_code` by grouping `DBS/docs/vehicles_petrol_specimens.csv`
on `P15_engine_code` and checking within-code spread for `V112_lambda`,
`V101_CO_low_idle`, `V111_CO_high_idle`, and `P14_rated_rpm`. The named
consumer is DTCLab's local `DtcLabDnaView.model` requirement; if variance does
not justify a new field, `VinDNA` stays model-free and COMLab-D carries the
mirror relaxation.

## Changed Files

- `labs/dnalab/docs/research/Q8_model_variance.md`
- `labs/comlab/comlab/config/proposals/entries.yaml`
- `labs/dnalab/tasks/PROGRESS.md`
- `labs/dnalab/tasks/progress_notes/T-DNA-5.md`

## Decision

KEEP-EMPTY. No `VinDNA.model` field is added.

The contracted specimen file has 7,079 rows with non-empty `P15_engine_code`
and 7,079 unique non-empty engine-code values, so there are no repeated
engine-code groups from which to compute within-code CoC variance. This does
not prove zero variance; it means DBS provides no empirical basis for adding a
new model field. Under the signal/noise rule, the absence of variance evidence
blocks ADD and keeps the canonical COMLab/DNALab shape model-free.

COMLab-D is registered to relax or drop DTCLab's required mirror field.

## VERIFICATION GATE

- Environment: `C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe --version`
  printed `Python 3.14.5`.
- Document readability: `Select-String` found no `![][` image placeholders in
  the audit or DNA research inputs; DNAresearch equations were visible as text.
- DBS variance analysis:
  - `vehicles_petrol_specimens.csv`: 7,079 rows with non-empty
    `P15_engine_code`; 7,079 unique non-empty `P15_engine_code` values.
  - `V112_lambda`: 1,223 filled rows; 0 engine-code groups with more than 3
    filled specimens; median within-code stdev `n/a`.
  - `V101_CO_low_idle`: 1,043 filled rows; 0 groups with more than 3 filled
    specimens; median within-code stdev `n/a`.
  - `V111_CO_high_idle`: 1,134 filled rows; 0 groups with more than 3 filled
    specimens; median within-code stdev `n/a`.
  - `P14_rated_rpm`: 3,420 filled rows; 0 groups with more than 3 filled
    specimens; median within-code stdev `n/a`.
- Task snippet equivalent:
  - `engine_codes w/ >3 specimens: 0`
  - `median within-code lambda stdev: n/a`
- Registry cross-check:
  - `vehicles_petrol_M1_1990_2020.csv`: 551,988 rows with non-empty
    `P15_engine_code`; 7,063 unique codes; 3,014 codes have more than one
    `D3_commercial_name`, but this file has no CoC target columns.
- Consumer proof:
  - `dtclab/dtclab/schemas/dna_view.py:DtcLabDnaView` requires `model: str`.
  - `comlab/comlab/schemas/lab_dna_views.py:DtcLabDnaView` has no `model`.
  - `COMLab-D` now registers the paired mirror relaxation.
- Proposal parse:
  - `entries.yaml` loaded successfully and contains `COMLab-D`.
- graphify: skipped per `DNA_TASKS_START_HERE.md` Section 3.

## CODE REVIEW

- Confirmed the result is an analysis/proposal decision only; no production
  Python or `VinDNA` schema file was edited.
- Confirmed `Q8_model_variance.md` distinguishes the DBS limitation from a
  false "zero variance" proof.
- Confirmed COMLab-D names the exact DTCLab mirror consumer and keeps the
  canonical COMLab view unchanged.
- Confirmed no `graph/` or `.sandbox-py/` artifacts were touched.
- Pythonskill checklist: production-code items were not applicable because this
  task made no Python code changes; the one-off Python analysis used typed
  helpers, `pathlib`, context managers, specific parsing, and no bare `except`.
