# T-OBDV2-FIX-4 — Align the `number_of_banks` default across the pipeline (🟡 correctness)

**Status:** `done` — coder-runnable · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** OBDLab skills-audit 2026-06-08 — finding **CR-4** (`audit/AUDIT_03_code-review.md`).
**Blocked by:** —
**Consumer (signal/noise):** the bank-2 fields (`shrtft2`/`longft2`/`total_trim_correction_delta_b2`)
already ship to COMLab (T-OBDV2-BANK-ASYM-1). This only fixes default agreement; no new field.

## Why this exists

When `number_of_banks` is absent, the two halves of the pipeline disagree:

- `pid_ingestion_validator._validate_bounds` L232 → default **2**
- `pid_ingestion_validator._enforce_bank2_contract` L302 → default **2**
- `trim_vector_aggregator.aggregate` L45 → default **1**
- `sensor_signal_translator` (payload assembly) L221 → default **1**

So the validator treats an omitted-bank input as a **2-bank** engine while the aggregator
and payload assembly treat it as **1-bank** (`shrtft2`/`longft2` → `None`). Same vehicle,
two interpretations.

## Scope (pinned)

Standardise on default **1** (petrol-inline assumption, matches the emitter's common case)
at the two `pid_ingestion_validator` sites. Confirm aggregator/assembly already use 1.
*Owner may instead choose "require the field"* — if so, the validator raises a typed
`PIDValidationError` on absence; pick one and state it in the plan.

## Success criteria

- An input omitting `number_of_banks` produces a **self-consistent single-bank** payload:
  `shrtft2`/`longft2` = `None`, no bank-2 validation applied, no bank-2 contract raise.
- A new regression fixture (omitted-bank input) locks the behaviour.
- Regression + pid_logset gate green; inner loop clean (Windows `.venv-wired`).

## Files to touch

- `core/pid_ingestion_validator.py` (L232, L302)
- `tests/regression/fixtures/` (+1 fixture) · a unit case in `tests/unit/test_pid_ingestion_validator.py`

## Out of scope

No change to the bank-2 null contract semantics when `number_of_banks == 2`. Test-infra build deferred.

## Verification

```bash
cd <repo>/labs/obdlab
ruff check obdlab/ && pyright obdlab/
grep -n 'number_of_banks", *2\|number_of_banks", *1' obdlab/obdlab/core/*.py   # confirm single default
pytest -x -q
```

## Progress hook

`tasks/progress_notes/T-OBDV2-FIX-4.md`: `## Plan` (chosen default) → `VERIFICATION GATE` →
`CODE REVIEW`. PROGRESS.md row → `done` with Files changed.
