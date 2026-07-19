# OBDLab audit — Lens 2/5: `uncle-bob-code-craftsmanship`

**Date:** 2026-06-08 · **Auditor role:** architect (read + report; no code edits) ·
**Skill:** `_skills/codingskills/uncle-bob-code-craftsmanship` (Clean Architecture
Dependency Rule, SOLID-in-context, code smells: rigidity / fragility / immobility /
viscosity / needless complexity / needless repetition / opacity; design-pattern use vs misuse).
**Subject:** `4DLabV2/labs/obdlab/obdlab/` (18 modules, ~2,119 LOC).

> Method caveat (shared across all five reports): sandbox static analysis ran against a
> **truncated mirror** and was discarded; findings are from the real source. See
> `AUDIT_01_pythonskill.md` for detail.

This lens is about **structure and design**, not lint/style. Findings are named by the
smell vocabulary and each carries one or two concrete refactors.

---

## Findings — Uncle Bob lens

### 🔴 UB-1 Fragility + hidden temporal coupling — stateful orchestrator
**Smell: fragility / opacity.** `SensorSignalTranslator` keeps mutable instance state
for the two-point MAF linearity check: `self._last_stabilized_idle` / `self._last_stress_idle`
(`sensor_signal_translator.py` L62-64, written L206-209, read L212-218).

`translate()` is presented as a pure request→`OBDLivePayload` function, but its output for
`sensor_error_delta`/`w_theo` **depends on prior calls** to the same instance. A translator
reused across two vehicles (or across a stabilized-idle then stress-idle reading of the
same vehicle) silently carries the first vehicle's `(maf, w_theo)` into the second's
delta. This is the classic Clean Code "function with a hidden history" — a small change
in call order changes the answer with no signal at the interface.

- **Refactor:** make the two-point pairing an **explicit input** — accept the prior band's
  `(maf, w_theo)` as an argument, or expose a small `LinearityAccumulator` value object the
  caller owns and threads through. The orchestrator should be stateless per `translate()`.

### 🔴 UB-2 Dead gate = needless complexity that looks like a safety feature
**Smell: opacity / needless complexity.** `SemanticConsistencyChecker._physics_gate_3`
reads `sanitized_pids["calculated_ve"]` (L144), but in the live pipeline VE is computed
**after** the semantic checker runs (`translate()` order: [3] semantic → [4] VE), and
`translate()` never writes `calculated_ve`. So gate 3 always hits the `is None` early
return (L147). It reads as an active NA-engine VE-ceiling check; it is inert.
(Cross-listed in `AUDIT_03` CR-1 and `AUDIT_05` E-2.)

- **Refactor:** the architect must decide — either move the VE-ceiling check **after** VE
  computation (where `VEEngine._classify_validity` already produces `FAULT_VE_SENSOR_SKEW`,
  raising a possible *duplication* question), or delete gate 3 and rely on the VEValidity
  path. A gate that never fires is worse than no gate: it implies coverage that isn't there.

### 🟡 UB-3 Needless repetition — fuel-status mapping triplicated
**Smell: needless repetition (DRY).** The identical `{"Closed_Loop": FuelSystemStatus.CL, ...}`
string→enum map appears verbatim in three modules:
`pid_ingestion_validator.py` L166-175, `semantic_consistency_checker.py` L233-242,
`analytics_preconditions.py` L75-84. Three copies of one idea; the second reason to change
(Uncle Bob's "introduce at the second axis of change") is already here.

- **Refactor:** add `FuelSystemStatus.from_wire(value) -> FuelSystemStatus | None`
  classmethod on the enum (or a single `coerce_fuel_status` helper in `schemas/vocabulary.py`).
  Each call site delegates. One source of truth for the wire vocabulary.

### 🟡 UB-4 SRP / opacity — no-op `try/except` control flow
**Smell: opacity, viscosity.** `SemanticConsistencyChecker.evaluate` wraps each gate in
`try: gate(); gates_passed.append(...) ; except SemanticConsistencyError: raise` (L52-74).
The `except ... : raise` blocks do nothing — they catch and immediately re-raise. Gate 4's
`except (ValueError, SemanticConsistencyError): raise` is the same. This is structure that
implies error handling where there is none; a reader must verify each block does nothing.

- **Refactor:** delete the `try/except` scaffolding; call the gates directly and append on
  success. If the intent was "record which gates passed before the throw", capture that by
  ordering, not by dead handlers.

### 🟡 UB-5 SRP / opacity — two competing tier functions, one a no-op
**Smell: needless complexity / opacity.** `ranking.py` defines both `_candidate_evidence_tier`
(L159, the one actually used by `_clamp_confidence`) and `_evidence_tier` (L226). The
corroboration counters call `_evidence_tier(True, count)` (L210, L222) and **discard the
return value** — pure dead calls. A reader cannot tell which tier logic is authoritative.

- **Refactor:** remove the discarded `_evidence_tier(...)` calls; then either delete
  `_evidence_tier` or make `_candidate_evidence_tier` delegate to it so there is one
  definition of "tier".

### 🟡 UB-6 Inconsistent error taxonomy across a seam
**Smell: fragility.** Three error types cross the same `translate()` boundary with no
unifying base: `PIDValidationError(ValueError)`, `SemanticConsistencyError(AssertionError)`,
and `Physics_Gate_4` raising a **bare `ValueError`** (`semantic_consistency_checker.py`
L196) while gates 1-3 raise `SemanticConsistencyError`. `translate()`'s docstring promises
`SemanticConsistencyError` for gate violations, but the gate-4 path emits `ValueError`.
Subclassing `AssertionError` is the riskiest part: under `python -O` asserts are stripped
(the class survives but the choice signals "internal invariant", which a public contract
error is not), and `except ValueError` callers will catch gate-4 but not gates 1-3.

- **Refactor:** give OBDLab one exception root (`ObdLabError(Exception)`) with
  `PIDValidationError` and `SemanticConsistencyError` under it; make gate 4 raise
  `SemanticConsistencyError`; stop subclassing `AssertionError`. This is a boundary
  contract, so the change is load-bearing for COMLab's error handling.

### 🟢 UB-7 Design-pattern use is appropriately restrained (positive)
The polymorphic routing in `VEEngine.compute_ve` and `O2Normalizer.normalize`
(strategy-by-enum dispatch) is justified by real behavioural variation (§10.2 / §11) — not
cargo-cult Strategy classes. Dataclass `CandidateScore` is a clean value object. The
Dependency Rule is respected at the lab seam: `schemas/dna_view.py` is an OBDLab-owned
mirror with an explicit "never import from comlab/dnalab/vinlab" docstring, and no
cross-lab Python import exists. Good adherence — call it out so it is preserved.

---

## Draft task specs (Uncle Bob lens)

> Several items here are cross-cutting; the **primary** spec lives in the most relevant
> report and is referenced, not duplicated.

### T-OBDV2-AUDIT-UB-1 — De-state the orchestrator's two-point linearity (UB-1)
- **Files:** `core/sensor_signal_translator.py`, `core/maf_linearity.py`, plus
  `tests/unit/test_maf_linearity.py` / `test_sensor_signal_translator.py`
- **Change:** remove `_last_stabilized_idle` / `_last_stress_idle` instance state; thread the
  prior band's `(maf, w_theo)` explicitly (argument or caller-owned accumulator).
- **Success:** two `translate()` calls in either order on two different inputs produce
  order-independent `sensor_error_delta`; a new unit test asserts no state leaks between
  instances; `pytest -x -q` green.
- **Consumer (signal/noise):** `w_theo` + `sensor_error_delta` already ship and are
  consumed by COMLab's payload mirror (per `payload.py` docstring); this changes *how* they
  are computed, not the field set. No new field.

### T-OBDV2-AUDIT-UB-2 — Resolve Physics Gate 3 (UB-2) → see `AUDIT_03` T-OBDV2-AUDIT-CR-1
Architect decision required (move-after-VE vs delete vs merge with `FAULT_VE_SENSOR_SKEW`).
Primary spec in the code-review report.

### T-OBDV2-AUDIT-UB-3 — Single-source fuel-status coercion + drop dead handlers + tier no-ops (UB-3, UB-4, UB-5)
- **Files:** `schemas/vocabulary.py` (add `from_wire`), `core/pid_ingestion_validator.py`,
  `core/semantic_consistency_checker.py`, `core/analytics_preconditions.py`, `obdlab/ranking.py`
- **Change:** centralise the wire→enum map; delete the no-op `try/except` blocks in
  `evaluate`; delete the discarded `_evidence_tier(...)` calls (and the orphan function if
  unused after).
- **Success:** one fuel-status map; `evaluate` has no `try/except`; `ranking` has one tier
  function; `pytest -x -q` green; `ruff --select SIM,TRY` clean.
- **Consumer:** internal refactor; no schema change.

### T-OBDV2-AUDIT-UB-4 — Unify the exception taxonomy (UB-6)
- **Files:** `core/exceptions.py`, `core/semantic_consistency_checker.py` (gate 4), and any
  COMLab mirror that catches these (architect to confirm the consumer).
- **Change:** introduce `ObdLabError(Exception)` root; reparent `SemanticConsistencyError`
  off `AssertionError`; gate 4 raises `SemanticConsistencyError`.
- **Success:** `translate()` raising on a gate-4 violation surfaces `SemanticConsistencyError`,
  matching the docstring; COMLab's catch site (named in the spec) still handles both.
- **Consumer:** COMLab fusion error-handling path — **must be named in the task file** before
  this ships (it crosses the JSON/exception boundary).
