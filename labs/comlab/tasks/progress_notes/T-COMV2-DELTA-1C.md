# T-COMV2-DELTA-1C progress note

Status: done
Date: 2026-06-20

## Scope Confirm

Per-signal profile logic in `delta_engine.py` — `_delta_trim`, `_delta_gas`, `_delta_o2`,
`_assemble` — resolving concrete fault-family profiles with calibrated confidence.
Locked per-signal bands: ΔTrim must be `STRESS_IDLE` or ABSTAIN; Δgas/ΔO₂ must be
`REGULATORY_HIGH_IDLE` or ABSTAIN. Every `target_fault_family` is an existing
`FaultFamilyLit` member. Still NOT wired (1D). Profile code landed in session 1; this
session authored the profile + abstain + architecture-interplay tests.

## Changed Files

- `labs/comlab/comlab/analytics/delta_engine.py` — profile bodies *(session 1; verified)*
- `labs/comlab/tests/unit/test_delta_engine.py` — EXTENDED with profile/abstain families *(this session)*

## Verification Gate — `pytest tests/unit/test_delta_engine.py -q` → 23 passed

Profile/abstain/interplay families (each fixture `# wiki:`-cited to its chunk; numbers
taken verbatim from the delta-relations matrices — no chunk coverage → no fixture):

- **ΔTrim @ STRESS_IDLE (delta-relations/02-05):**
  - vacuum leak: low +20 / elev +2 → ΔTrim −18 → `VACUUM_LEAK` → `vacuum_leak`, conf 0.92 (ch02)
  - fuel starvation: low +3 / elev +20 → ΔTrim +17 → `FUEL_STARVATION` → `lean_condition` (ch03)
  - MAF under-report: low +6 / elev +24 → ΔTrim +18 → `MAF_UNDERREPORT` → `lean_condition` (ch04)
  - exhaust backpressure: low 0 / elev −14 → ΔTrim −14 → `EXHAUST_BACKPRESSURE` → `exhaust_leak` (ch05)
- **Δgas @ REGULATORY_HIGH_IDLE (delta-relations/07):**
  - worn rings: HC 15→180 → `WORN_PISTON_RINGS` → `mechanical_wear` (GAS-WPR-001)
  - worn valve seals: HC 120→15 → `WORN_VALVE_SEALS` → `mechanical_wear` (GAS-WVS-001)
  - flat cam: HC 30→220 + elev O₂ 2.5 → `FLAT_CAM` → `cam_timing` (GAS-FC-001)
  - EGR stuck closed: NOx 1500→2800 → `EGR_STUCK_CLOSED` → `lean_condition` (GAS-ESC-001)
- **Abstain:** trim band-mismatch (frame not STRESS_IDLE); starvation↔MAF ambiguous
  (low-idle +10 in the overlapping band); gas no-signature → `NONE`. All conf 0.0.
- **Architecture interplay (delta-relations/06):** speed-density NULLs a real vacuum
  leak (sign `NULL`, profile `NONE`, conf 0.0); forced induction inverts the sign so a
  −20 % STFT post-turbo leak is NOT misread as an NA negative-ΔTrim leak.

Other gates:
- `ruff check .` — All checks passed.
- `pyright tests/unit/test_delta_engine.py` — 0 errors.
- `pytest -q` — 368 passed, 12 skipped, 2 known-red (`registry` absent — not ours).
- **Not-wired gate:** `grep -rnI compute_delta_signature comlab/core/` → empty (1D wires it).

## Code Review

- Confidence is the primary 0.92 ONLY when a concrete profile resolves AND the frame is
  trusted AND not architecture-nulled; unknown architecture caps at 0.70; everything else
  is 0.0 — verified across the profile vs abstain vs null tests.
- ΔTrim profile takes precedence in `_assemble`; Δgas supplies the family when trim is
  silent — both branches covered (trim tests vs gas tests).
- All resolved families (`vacuum_leak`, `lean_condition`, `exhaust_leak`,
  `mechanical_wear`, `cam_timing`) are confirmed members of `response.FaultFamilyLit`.
- Per-signal band policy (ABSTAIN on mismatch) is asserted, not assumed — the
  band-mismatch test exercises it directly.

## Next

`T-COMV2-DELTA-1D` (Pickup-B) — wire `delta_signature` into `fault_atlas_router` Phase 5
behind the default-off `enable_delta` flag; e2e single-point regression-lock + two-point
activation. The epic row flips → `done` when 1D closes.
---

## LEDGER RECONCILIATION — 2026-06-21 (architect, Cowork)

**Stale-ledger guard cleared.** Earlier snapshots in this note (and the sibling
DELTA-1/1A/1B/1C/1D notes) recorded **2 failing tests**. Those were the **known-red
`registry`-package import failures** captured on 2026-06-20, when the `registry`
package was broken — they were never failures in COMLab delta code.

They were resolved downstream by:
- **`T-REG-REVIVE-1`** (done 2026-06-21) — revived `labs/comlab/registry/`; registry **470 passed**.
- **`T-COMV2-DELTA-2`** (done 2026-06-21) — COMLab **387 passed** + registry **471 passed**; ruff/pyright clean.

**Re-verified 2026-06-21** with the pinned interpreter (`../../.sandbox-py/bin/python3.14`, 3.14.5):
- `pytest -q` → **417 passed, 10 skipped, 0 failed** (10 skips = opentelemetry-not-installed router spans + 1 phase-3 legacy stub).
- `pytest registry/tests/ -q` → **471 passed, 0 failed**.

These rows are correctly `done`; the "2 failed" text above is a historical snapshot,
not a live regression. `T-COMTST-4` (the next `pending` row) is unblocked.
