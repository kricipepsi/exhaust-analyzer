# T-OBDV2-FIX-5 — Unify the exception taxonomy (🟡 boundary contract)

**Status:** `done` — coder-runnable **after** the COMLab catch-site consumer is named ·
**Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** OBDLab skills-audit 2026-06-08 — finding **UB-6** (`audit/AUDIT_02_uncle-bob.md`).
**Blocked by:** — (name the COMLab consumer first; see below)
**Consumer (signal/noise):** the COMLab fusion error-handling path that catches OBDLab
exceptions across the JSON/exception boundary — **must be named in the plan** before this ships.

## Why this exists

Three error types cross the `translate()` boundary with no common root:

- `PIDValidationError(ValueError)` (`core/exceptions.py` L4)
- `SemanticConsistencyError(AssertionError)` (`core/exceptions.py` L8) — subclassing
  `AssertionError` is risky: asserts are stripped under `python -O`, and the choice signals
  "internal invariant", which a public contract error is not.
- `Physics_Gate_4` raises a **bare `ValueError`** (`core/semantic_consistency_checker.py`
  L196) while gates 1-3 raise `SemanticConsistencyError`.

`translate()`'s docstring promises `SemanticConsistencyError` for gate violations, but the
gate-4 path emits `ValueError`; an `except ValueError` caller catches gate 4 but not gates 1-3.

## Scope (pinned)

- Introduce `ObdLabError(Exception)` as the OBDLab exception root.
- Reparent `PIDValidationError` and `SemanticConsistencyError` under `ObdLabError`
  (keep `PIDValidationError`'s `ValueError` lineage only if a named caller relies on it —
  otherwise drop it). Stop subclassing `AssertionError`.
- `Physics_Gate_4` raises `SemanticConsistencyError`, matching gates 1-3 and the docstring.

## Success criteria

- A gate-4 violation surfaces `SemanticConsistencyError` from `translate()` (matches docstring).
- The named COMLab catch-site still handles both error classes (grep/confirm the consumer).
- Regression + pid_logset gate green; inner loop clean (Windows `.venv-wired`).

## Files to touch

- `core/exceptions.py` · `core/semantic_consistency_checker.py` (gate 4) ·
  tests asserting on the raised type (`tests/unit/test_semantic_consistency_checker.py`,
  `test_pid_ingestion_validator.py`) · the named COMLab catch-site (confirm only).

## Out of scope

No change to *when* gates fire. Test-infra build deferred.

## Verification

```bash
cd <repo>/labs/obdlab
ruff check obdlab/ && pyright obdlab/
grep -n "AssertionError\|raise ValueError" obdlab/obdlab/core/semantic_consistency_checker.py \
  obdlab/obdlab/core/exceptions.py   # expect none after the change
pytest -x -q
```

## Progress hook

`tasks/progress_notes/T-OBDV2-FIX-5.md`: `## Plan` (name the COMLab catch-site consumer) →
`VERIFICATION GATE` → `CODE REVIEW`. PROGRESS.md row → `done`.
