# T-DNA-6 progress note

Status: done
Date: 2026-06-12

## Scope Confirm

T-DNA-6 registers `fuel_type` as a proposal-only VinDNA context field for the
future GASLab/COMLab `GasLabDnaView` consumer. The named consumer is
`comlab/comlab/schemas/lab_dna_views.py:GasLabDnaView`, feeding GASLab
`lab_dna_views` context for E5/E10/winter-blend lambda-correction handling per
GASLab wiki Section 1.4 `[v2: q9]`. `altitude_band` is deliberately not a
VinDNA schema field: the same wiki marks it session/context only, informational,
and says lambda math is altitude-invariant. No live `VinDNA`, contract, or
Python schema change is in scope.

## Changed Files

- `labs/comlab/comlab/config/proposals/entries.yaml`
- `labs/dnalab/tasks/PROGRESS.md`
- `labs/dnalab/tasks/progress_notes/T-DNA-6.md`

## Decision

Register `fuel_type` as COMLab-E, status `proposed`, with
`vin_dna.fuel_type` marked `proposal-only`. The proposal names
`GasLabDnaView` and GASLab lab DNA context as the consumer path and includes a
draft contract Section 4.1 line for the paired GASLab/COMLab session.

Keep `altitude_band` out of `VinDNA`. It remains session/context metadata, not
a vehicle attribute, because altitude does not relax any GASLab gate and lambda
math is altitude-invariant.

## VERIFICATION GATE

- Environment: `C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe --version`
  printed `Python 3.14.5`.
- Document readability: `Select-String` found no `![][` image placeholders in
  the start file, task ledger, T-DNA-6 task brief, audit, DNA research, or
  GASLab wiki inputs used for this task. The relevant lambda/altitude content
  is visible as text.
- Proposal registry parse: `entries.yaml` loaded successfully as YAML and
  contains `COMLab-E`.
- Proposal proof: `grep`/`Select-String` confirms `fuel_type` appears in
  `labs/comlab/comlab/config/proposals/entries.yaml`.
- Consumer provenance: `grep`/`Select-String` confirms `fuel_type` and
  `altitude_band` appear in
  `labs/gaslab/wiki/01_role_boundaries_dna_ingestion.md` Section 1.4.
- Live-schema guard: `comlab/comlab/schemas/lab_dna_views.py:GasLabDnaView`
  still has no live `fuel_type` or `altitude_band` field.
- Inner loop: not applicable; no `.py` files were edited.
- graphify: skipped per `DNA_TASKS_START_HERE.md` Section 3.

## CODE REVIEW

- Confirmed `fuel_type` is registered as proposal-only, not silently added to
  live `VinDNA`.
- Confirmed the proposal names a concrete proposed consumer and code path.
- Confirmed `altitude_band` is documented as non-schema session/context with
  the altitude-invariance reason.
- Confirmed no `graph/` or `.sandbox-py/` artifacts were touched.
