# T-OBDV2-FIX-7 — Code-hygiene bundle (🟢 low priority, one pass)

**Status:** `done` — coder-runnable · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** OBDLab skills-audit 2026-06-08 — findings **P-2, P-3, P-4, P-5, ARCH-3**
(`audit/AUDIT_01_pythonskill.md`, `AUDIT_04_architecture.md`).
**Blocked by:** —
**Consumer (signal/noise):** n/a — internal correctness/clarity. No schema change.

> Bundled because each item is a few lines; one inner-loop pass covers them. None is urgent.

## Items (pinned)

1. **P-2 — restore exception chaining.** `core/pid_ingestion_validator.py`: add `from exc`
   (preserve) or `from None` (suppress) at the four `raise PIDValidationError(...)` sites
   inside `except (ValueError, TypeError)` — L83, L90, L131, L139.
2. **P-3 — single-source duplicated thresholds.** `_ECT_WARM_THRESHOLD = 70` and
   `_WOT_THROTTLE_THRESHOLD = 90` are defined identically in `core/o2_normalizer.py`
   (L37, L40) and `core/analytics_preconditions.py` (L35, L38). Hoist to one home with the
   single wiki citation; import from there.
3. **P-4 — drop the dead `total_trim` param.** `O2Normalizer.normalize` (`core/o2_normalizer.py`
   L55-60) accepts `total_trim` but the only caller passes 2 args (`sensor_signal_translator.py`
   L147). Remove the parameter and its docstring line.
4. **P-5 — defer import-time YAML I/O.** `core/state_bucketing.py` L23-24 loads/parses
   `obd_translation_rules.yaml` at module import. Wrap in a `_load_rules()` called on first
   `compute_bucket`, matching `PIDIngestionValidator`'s `__init__` load pattern.
5. **ARCH-3 — fix doc-vs-code drift.** `schemas/vocabulary.py` L52 says
   `FAULT_VE_SENSOR_SKEW` = "VE > 85% at idle", but code uses **90** (`ve_engine.py`
   `_CUTOFF_VE_SKEW = 90.0`; `semantic_consistency_checker.py` `_CUTOFF_VE_NA = 90`). Confirm
   the wiki §6.4 truth, then align the docstring (or the code) to one cited cutoff.

## Success criteria

- All five items applied; no behaviour change except (1) traceback clarity and (5) the doc/code
  agreeing on one cited number.
- `ruff --select B904` clean (once `B` is enabled, see P-1 — optional here); regression +
  pid_logset gate green; inner loop clean (Windows `.venv-wired`).

## Files to touch

- `core/pid_ingestion_validator.py` · `core/o2_normalizer.py` · `core/analytics_preconditions.py`
  · `core/state_bucketing.py` · `schemas/vocabulary.py` (+ `core/ve_engine.py` iff code-side for item 5)

## Out of scope

P-1 (ruff/pyright ruleset tightening) is a **verification-gate** change — defer it to the
GASLab-parity test-infra task, not here. Test-infra build deferred.

## Verification

```bash
cd <repo>/labs/obdlab
ruff check obdlab/ && pyright obdlab/
grep -rn "_ECT_WARM_THRESHOLD\|_WOT_THROTTLE_THRESHOLD" obdlab/obdlab   # one definition each
grep -n "total_trim" obdlab/obdlab/core/o2_normalizer.py               # gone
pytest -x -q
```

## Progress hook

`tasks/progress_notes/T-OBDV2-FIX-7.md`: `## Plan` (list the 5 items) → `VERIFICATION GATE`
→ `CODE REVIEW`. PROGRESS.md row → `done` with Files changed.
