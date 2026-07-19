# T-OBDV2-FIX-3 — De-state the orchestrator's two-point MAF linearity (🔴 fragility)

**Status:** `done` — coder-runnable · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** OBDLab skills-audit 2026-06-08 — finding **UB-1 / AR/UB-1**
(`audit/AUDIT_02_uncle-bob.md`, `AUDIT_04_architecture.md`).
**Blocked by:** —
**Consumer (signal/noise):** `w_theo` + `sensor_error_delta` already ship and are consumed
by COMLab's payload mirror (per `schemas/payload.py` docstring; COMLab `T-COMV2-MAF-LIN-1`).
This changes **how** they are computed, not the field set. No new field.

## Why this exists

`SensorSignalTranslator` carries mutable instance state for the two-point linearity check:
`self._last_stabilized_idle` / `self._last_stress_idle`
(`core/sensor_signal_translator.py` L62-64, written L206-209, read L212-218). `translate()`
is presented as a pure request→`OBDLivePayload` call, but `sensor_error_delta`/`w_theo`
**depend on prior calls to the same instance**. A translator reused across two vehicles —
or across a stabilized-idle then stress-idle reading — silently carries the first reading's
`(maf, w_theo)` into the second's delta. Hidden temporal coupling: call order changes the
answer with no signal at the interface, and it is not thread-safe.

## Scope (pinned)

Make the two-point pairing an **explicit input**, not instance state:

- Remove `_last_stabilized_idle` / `_last_stress_idle` from `__init__` and `translate()`.
- Accept the prior band's `(maf, w_theo)` as an argument to `translate()` (e.g.
  `prior_band: tuple[str, float, float] | None = None`) **or** introduce a small
  caller-owned `LinearityAccumulator` value object that the caller threads across the two
  readings. Pick the lighter option that the wired app's call site can supply.
- `translate()` becomes stateless per call: same inputs → same payload, any order.

## Success criteria

- Two `translate()` calls in **either order** on two different inputs produce order-independent
  `sensor_error_delta`; a new unit assertion confirms no state leaks between two instances or
  two sequential calls.
- The existing two-point behaviour (emit delta only once both bands captured) is preserved when
  the caller supplies the prior band.
- Regression + pid_logset gate green; inner loop clean (Windows `.venv-wired`).

## Files to touch

- `core/sensor_signal_translator.py` · `core/maf_linearity.py` (if the accumulator lives here) ·
  `tests/unit/test_maf_linearity.py` / `tests/unit/test_sensor_signal_translator.py` ·
  the wired app call site **iff** the signature changes (name it in the plan before editing).

## Out of scope

No change to the linearity *formula* (`maf_linearity.py` math is correct). Test-infra build
deferred. No new field.

## Verification

```bash
cd <repo>/labs/obdlab
ruff check obdlab/ && pyright obdlab/
# no surviving instance-state for the two-point cache:
grep -n "_last_stabilized_idle\|_last_stress_idle" obdlab/obdlab/core/sensor_signal_translator.py \
  && echo "FAIL: orchestrator still stateful" || echo "OK stateless"
pytest -x -q
```

## Progress hook

`tasks/progress_notes/T-OBDV2-FIX-3.md`: `## Plan` (chosen signature/accumulator) →
`VERIFICATION GATE` → `CODE REVIEW` (order-independence proof). PROGRESS.md row → `done`.
