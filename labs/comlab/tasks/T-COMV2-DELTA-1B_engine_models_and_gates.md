# T-COMV2-DELTA-1B — delta_engine models + gates (standalone, not wired)

**Authored:** 2026-06-20 (architect, Cowork). **Stage:** 4. **Type:** new analytics module (gates only). **Sub-task 2 of 4** of epic `T-COMV2-DELTA-1`.
**Blocked by:** `T-COMV2-DELTA-1A` (uses `SecondOperatingPointFrame` + `OrchestratorInboundRequest.second_operating_point`).
**Parent / decisions:** `tasks/T-COMV2-DELTA-1_cross_lab_delta_module.md`. **Source:** `research/deltaImplPlan.md` (step 4 — models + entry + architecture/validity/sentinel; profile bodies stubbed).
**Drill:** boot order → parent epic → **this file** → scope-confirm before code.

> **One-line scope:** create `comlab/analytics/delta_engine.py` — the typed output models, the `compute_delta_signature` entry point, the **architecture gate**, the **validity gate**, and the **single-point sentinel** — mirroring `PowerLossAnalytics` style (static-only, pure math, pydantic I/O, constants as `# wiki:`/`# lld:`-cited class attrs). The per-signal **profile** methods (`_delta_trim`/`_delta_gas`/`_delta_o2`/`_assemble`) are **stubbed to ABSTAIN** in this task and filled in 1C. The module is fully unit-tested for everything it implements but is **not wired into the router** (that's 1D).

## What to build

**Models:** `DeltaSignature` (the output) + sub-models `DeltaTrimResult`, `DeltaGasResult`, `DeltaO2Result`, `DeltaValidityVerdict`, `ArchitectureGateVerdict`. `DeltaSignature` carries the **byte-identity contract**: `present: bool` (`False` == no frame == single-point) and `confidence: float` (`0.0` when absent/untrusted/nulled). `target_fault_family` maps **only** to existing `FaultFamilyLit` members.

**Entry point — gate order is architecture → validity → (profiles, stubbed):**

```
compute_delta_signature(request) -> DeltaSignature
  frame None            → _single_point_sentinel()   # present=False, conf=0.0, SINGLE_POINT
  _architecture_gate    # chunk 06: MAP_ONLY_SPEED_DENSITY → trim_nulled; TURBO/SC → trim_inverted;
                        #            both None → permissive + confidence cap (never apply NA profile blind)
  _validity_gate        # chunk 08: per-frame vsum 14–18, dilution CO+CO₂>6, rpm_stable, sample_validity ok
                        #            untrusted → present=True, conf=0.0 (Phase-5 fallback)
  _delta_trim   → ABSTAIN (stub; real logic in 1C)
  _delta_gas    → ABSTAIN (stub; real logic in 1C)
  _delta_o2     → passthrough/empty (stub; real logic in 1C)
  _assemble     → with all profiles abstaining, returns present=True, conf=0.0
```

The stubs must be **safe**: with profiles abstaining, `_assemble` yields `present=True, confidence=0.0` — i.e. a frame was seen but no concrete profile resolved, so Phase 5 (once wired in 1D) would fall back to the static signature. This keeps 1B independently shippable.

**Constants** (carry forward to 1C; cite now where the gates use them): vsum 14–18, dilution CO+CO₂ ≤ 6, primary-delta confidence ≈ 0.92 — each `# wiki:`-cited to its chunk.

## Tests — `tests/unit/test_delta_engine.py` (NEW; gate families only)

- **Sentinel:** no second frame → `present=False`, `SINGLE_POINT`, `conf 0`.
- **Architecture (chunk 06, mandatory):** `MAP_ONLY_SPEED_DENSITY` → `trim_nulled` (conf 0); `TURBOCHARGED` → `trim_inverted` flag set; both-`None` → permissive with confidence cap.
- **Validity (chunk 08):** vsum dilution reject (CO+CO₂ ≤ 6); vsum out-of-band reject (<14); rpm-unstable reject — each → `present=True, conf=0.0`.

(Profile-resolution + abstain-on-band-mismatch fixtures are **1C's** suite.)

## Success criteria (done = all)

- `tests/unit/test_delta_engine.py` green for the gate/sentinel families above.
- Module imports cleanly; `ruff check .` → `pyright comlab/` → `pytest -x -q` clean.
- **No router/aggregator change** — engine is standalone; existing `tests/` suite untouched and green.
- `VERIFICATION GATE` + `CODE REVIEW` filled in `progress_notes/T-COMV2-DELTA-1B.md`; ledger row → `done`. **STOP.**

## Files to touch

`comlab/analytics/delta_engine.py` (**ADD**) · `tests/unit/test_delta_engine.py` (**ADD**, gate families) · `tasks/PROGRESS.md` · `progress_notes/T-COMV2-DELTA-1B.md`.

## Out of scope

- Per-signal profile logic (1C) — leave `_delta_trim`/`_delta_gas`/`_delta_o2`/`_assemble` profile bodies as ABSTAIN stubs.
- Any router/aggregator wiring (1D).

## Verification

```bash
cd labs/comlab
ruff check . && pyright comlab/ && pytest -x -q
pytest tests/unit/test_delta_engine.py -q -k "sentinel or architecture or validity"
grep -nI "compute_delta_signature" comlab/core/   # MUST be empty — not wired yet
```
