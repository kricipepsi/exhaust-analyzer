# T-COMV2-DELTA-1C — delta_engine per-signal profiles + assemble

**Authored:** 2026-06-20 (architect, Cowork). **Stage:** 4. **Type:** analytics module completion. **Sub-task 3 of 4** of epic `T-COMV2-DELTA-1`.
**Blocked by:** `T-COMV2-DELTA-1B` (fills the ABSTAIN stubs it left in `delta_engine.py`).
**Parent / decisions:** `tasks/T-COMV2-DELTA-1_cross_lab_delta_module.md`. **Source:** `research/deltaImplPlan.md` (step 4 — profiles + assemble; step 8 profile tests).
**Drill:** boot order → parent epic → **this file** → scope-confirm before code.

> **One-line scope:** replace the ABSTAIN stubs from 1B with the real per-signal logic — `_delta_trim`, `_delta_gas`, `_delta_o2`, `_assemble` — so the engine resolves concrete fault-family profiles with calibrated confidence. **Per-signal bands** (the locked decision): ΔTrim must be `STRESS_IDLE` or ABSTAIN; Δgas/ΔO₂ must be `REGULATORY_HIGH_IDLE` or ABSTAIN. Still **not wired** into the router (1D).

## What to build (replace 1B stubs)

```
_delta_trim   # band must == STRESS_IDLE else ABSTAIN; apply invert/null flags from the architecture gate;
              #   match profile by Δ-sign + low-idle band; starvation↔MAF ambiguous → ABSTAIN
_delta_gas    # band must == REGULATORY_HIGH_IDLE else ABSTAIN; rings / valve / flat-cam / EGR / rich profiles
_delta_o2     # subtraction-only passthrough; never sets a profile (ΔO₂ not yet quantified)
_assemble     # ΔTrim profile precedence; Δgas corroborates; map to existing FaultFamilyLit;
              #   confidence = primary (~0.92) ONLY when a concrete profile resolved AND trusted AND not nulled
```

**Numeric constants — each `# wiki:`-cited class attr:** ΔTrim leak ≤ −10 / supply ≥ +10 / backpressure ≤ −10; low-idle bands +15..+25 / 0..+5 / 0..+8; turbo invert ≈ −20; ΔHC rings ≥ +100, valve ≤ −50; ΔNOx EGR ≥ +800. (vsum/dilution/confidence constants already added in 1B — reuse, don't re-derive.)

## Tests — extend `tests/unit/test_delta_engine.py` (profile + abstain families)

- **ΔTrim (STRESS_IDLE):** `vacuum_leak` (low +20/elev +2 → `vacuum_leak`, ch02); `fuel_starvation` (low +3/elev +20 → `lean_condition`, ch03); `maf_underreport` (low +6/elev +24, ch04); `exhaust_backpressure` (low 0/elev −14 → `exhaust_leak`, ch05).
- **Δgas (REGULATORY_HIGH_IDLE):** `worn_piston_rings` (HC 15→180 → `mechanical_wear`, ch07); `worn_valve_seals` (HC 120→15, ch07); `flat_cam` (HC 30→220 + O₂ 0.4→2.5, ch07); `egr_stuck_closed` (NOx 1500→2800, ch07).
- **Abstain:** trim band-mismatch (frame not STRESS_IDLE); starvation↔MAF ambiguous; gas no-signature.
- **Architecture interplay (ch06):** speed-density nulls a real leak (`MAP_ONLY` → `trim_nulled`, conf 0); forced induction inverts sign (`TURBOCHARGED`, elev STFT ≈ −20 → `trim_inverted`, **not** misread as an NA leak).

Each fixture `# wiki:`-cites its chunk; **no chunk coverage → no fixture** (fixtures are provisional pending the prompt-D master table — see parent).

## Success criteria (done = all)

- Full `tests/unit/test_delta_engine.py` green (gate families from 1B + profile/abstain families here).
- Every numeric literal carries a `# wiki:` citation; every resolved `target_fault_family` is an existing `FaultFamilyLit` member.
- `ruff check .` → `pyright comlab/` → `pytest -x -q` clean; **no router/aggregator change**; existing `tests/` suite untouched.
- `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/T-COMV2-DELTA-1C.md`; ledger row → `done`. **STOP.**

## Files to touch

`comlab/analytics/delta_engine.py` (**MODIFY** — fill stubs) · `tests/unit/test_delta_engine.py` (**EXTEND**) · `tasks/PROGRESS.md` · `progress_notes/T-COMV2-DELTA-1C.md`.

## Out of scope

- Router/aggregator wiring + e2e (1D). The engine still must not be imported by `comlab/core/` at the end of this task.
- Any band-policy change (locked: per-signal bands, ABSTAIN on mismatch).

## Verification

```bash
cd labs/comlab
ruff check . && pyright comlab/ && pytest -x -q
pytest tests/unit/test_delta_engine.py -q
grep -nI "compute_delta_signature" comlab/core/   # STILL empty — wiring is 1D
```
