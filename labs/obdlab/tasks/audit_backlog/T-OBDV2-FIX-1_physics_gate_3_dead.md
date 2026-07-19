# T-OBDV2-FIX-1 — Physics Gate 3 never fires in the live pipeline (🔴 correctness)

**Status:** `done` — **disposition RATIFIED = (B)** 2026-06-09; coder-runnable ·
**Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** OBDLab skills-audit 2026-06-08 — finding **CR-1 / UB-2** (`audit/AUDIT_03_code-review.md`, `AUDIT_02_uncle-bob.md`).
**Blocked by:** — (decision-bearing; see "Disposition")
**Consumer (signal/noise):** the §4 semantic-gate contract read by COMLab fault-atlas routing
(a gate violation drives COLD/INVALID handling). No new schema field.

## Why this exists

`SemanticConsistencyChecker._physics_gate_3` (`core/semantic_consistency_checker.py` L144)
reads `sanitized_pids["calculated_ve"]`, but `translate()` runs the semantic checker at
**step [3]**, *before* VE is computed at **step [4]** (`core/sensor_signal_translator.py`
L114 vs L137), and never writes `calculated_ve`. The gate therefore always hits its
`is None` early-return (L147). It is exercised **only** by
`tests/unit/test_semantic_consistency_checker.py`, which injects `calculated_ve` directly
(L52, L127-188). The unit suite is green; the integration gate is dead.

Note a near-duplicate already operates: `VEEngine._classify_validity` emits
`VEValidity.FAULT_VE_SENSOR_SKEW` for the **same** condition (VE > 90 % ∧ NA ∧
STABILIZED_IDLE, `core/ve_engine.py` L266-272) — but as a soft *flag*, where gate 3
*raises*.

## Disposition — RATIFIED (B), 2026-06-09

**Decision: (B) remove Physics Gate 3.** Decisive reason: a hard `raise` that aborts
payload assembly is a *verdict*, and OBDLab's role is owner-ratified emitter-only
(`T-OBDV2-0` = revive/emitter, done; `OBDLAB_TASKS_START_HERE.md`: "Emitter-only … **no**
fault verdicts"). Option A would re-introduce a raise on the emitter path and contradict
that gate — rejected on contract grounds, not merely line count.

**Coverage parity confirmed (no signal lost):** gate 3's `_CUTOFF_VE_NA = 90`
(`semantic_consistency_checker.py` L25) and `_CUTOFF_VE_SKEW = 90.0` (`ve_engine.py` L49)
are the **same threshold** under the **same condition** (VE>90 ∧ NA ∧ STABILIZED_IDLE).
The §4 band gate 3 guarded surfaces identically as the `ve_validity = FAULT_VE_SENSOR_SKEW`
soft flag, which is already emitted (`payload.py` L84, set `sensor_signal_translator.py`
L241) and has a **live consumer** (`ranking.py` L208/218) plus the COMLab fault-atlas
contract. So removing the dead gate drops no coverage.

**Coder note (not a blocker):** `vocabulary.py` L52 comment says "VE > 85%" but the
constant is 90.0 — stale comment, not behaviour. Fix it in this diff *only if* you touch
that line; otherwise log it to Unplanned follow-ups. Do not change the 90 threshold.

- **Recommended → (B) remove Physics Gate 3** and rely on `VEValidity.FAULT_VE_SENSOR_SKEW`.
  Rationale: T-OBDV2-0 revived OBDLab as a *perception-channel emitter* that "does not emit
  fault verdicts." A hard `raise` that aborts payload assembly on a perception anomaly is
  verdict-like behaviour that belongs to COMLab; the soft `ve_validity` flag is the
  emitter-correct surface and already works. **Owner must ratify removing a wiki §4 gate.**
- **Alternative → (A) keep the gate but move it after VE compute** (feed it `ve_pct`), if
  the wiki §4 hard-stop is load-bearing. More code; reintroduces a raise on the emitter path.

## Scope (pinned to whichever option is ratified)

Option B: delete `_physics_gate_3` + its `_CUTOFF_VE_NA` constant; drop the `Physics_Gate_3`
append in `evaluate`; update the gate-count coupling (`semantic_gates_passed == 4` →
`== 3`, `core/sensor_signal_translator.py` L162). Option A: pass `ve_pct` into a
post-VE check; remove the dead `calculated_ve` read.

## Success criteria

- The §4 NA VE-ceiling behaviour is exercised by a path that runs in `translate()` (not only
  a unit test that injects `calculated_ve`). Anti-orphan grep: `calculated_ve` is either
  written in a live path (option A) or fully removed (option B).
- Existing regression (`tests/regression/`) and the pid_logset wiring gate stay green.
- Inner loop (`ruff`/`pyright`/`pytest -x -q`) clean — run in Windows `.venv-wired`
  (sandbox mirror is truncated; see `audit/AUDIT_01`).

## Files to touch

- `core/semantic_consistency_checker.py` (gate 3 + `evaluate`)
- `core/sensor_signal_translator.py` (gate-count coupling; option A: pass `ve_pct`)
- `tests/unit/test_semantic_consistency_checker.py` (update the now-misleading injected-VE cases)

## Out of scope

Test-infrastructure build (generative/eval) — deferred to the GASLab-parity test-infra task.
Do not touch unrelated gates. No new schema field.

## Verification

```bash
cd <repo>/labs/obdlab
ruff check obdlab/ && pyright obdlab/
# the gate's input is not a dead read:
grep -n "calculated_ve" obdlab/obdlab/core/semantic_consistency_checker.py \
  obdlab/obdlab/core/sensor_signal_translator.py
pytest -x -q
```

## Progress hook

`tasks/progress_notes/T-OBDV2-FIX-1.md`: `## Plan` (ratified option + why), `VERIFICATION GATE`,
`CODE REVIEW`. PROGRESS.md row → `done` with Files changed + the chosen disposition.
