# T-COMA-18 — authoring sidecar (Windows Cowork, 2026-11-13)

Input: `audit/reports/R1_C1_20261017.md` F-C1-6; `labs/comlab/wiki/04_horizon_eras.md` §RULE_HORIZON_PRUNE;
`labs/comlab/registry/rules/*.json` (`precondition`); `labs/vinlab/vinlab/decoder.py` (fuel delivery);
`apps/wired/wired/composition.py::_build_metadata`. Rehearsal: `C:/4DApp/recheck/T-COMA-18/`; survey
`C:/4DApp/recheck/F-C1-6/survey.py`.

### Verified context ###
1. **Still open on `24d265b`:** the three probes fail; `LEGACY rich -> ['RM-001', ('RM-004', 0.9), ...]`. Observed.
2. **Preconditions in the rule data:** 9 rules carry one; only RM-004 (`gdi_equipped: true`) and CT-001
   (`vvt_equipped: false OR vvt_equipped: unknown`) are hardware. The other 7 are PID-sourcing notes. Observed
   (`grep -rho '"precondition": *"[^"]*"' labs/comlab/registry/rules/ | sort | uniq -c`).
3. **No hardware fact reached COMLab:** `_build_metadata` sends horizon, cylinders, VIN confidence and air
   metering only; in the v7 corpus `vehicle_dna` is absent in all 311 runnable cases. Observed (survey).
4. **The decode default:** `VinDNA.fuel_delivery_type` defaults to `PORT_INJECTION`; the decoder sets `GDI` only
   from vref.db or the engine CSV. The fallback VIN DNA also says `PORT_INJECTION`. Observed (models.py,
   decoder.py, composition.py `_build_fallback_vin_dna`).
5. **Corpus effect:** RM-004 is never a winner; it is a differential sibling in 32 cases (31 LEGACY, 1 MODERN)
   before, 1 (era3_001, MODERN) after. Verdicts `changed 0 of 314`. Observed (survey with the patch applied, then
   restored).
6. **Rehearsal** (restored; `git apply --check` passes): comlab `517` (equal, `test_router_spans` held by the
   no-era clause); wired `176 → 185`; ui `73`; `test_tunable_reweight` `2 passed`; probes `3 passed`; new test base
   `5 failed, 4 passed`; mutants A `3 failed`, B/C/D `1 failed` each; ruff clean; `5 files changed, 112
   insertions(+)`. Observed.

### Rulings and the tradeoff that lost ###
- **GDI decode or MODERN era keeps RM-004.** Lost: trusting a decoded PORT_INJECTION to prune (it is also the
  unknown default, so a real GDI car with a thin decode would lose the rule). Lost too: allowing ADAPTIVE (some
  2002-2010 cars are GDI); the wiki names MODERN, and a GDI decode still keeps the rule on any era.
- **No era sent = unknown = no prune.** Lost: pruning a direct router call; that would break the
  `test_router_spans` pin, and the aggregator always sends an era.
- **Only RM-004 now.** Lost: a per-rule horizon scope for all REG-V2 rules (the wiki table uses v1 IDs; it needs
  rule-data authoring) and CT-001 (no VVT field exists).
- **`metadata` path only.** Lost: the `vehicle_dna` validator line (no production caller and no test reaches it).
- Plan NONE, difficulty 2 (schema + gate, scripted). Code row: second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `517 passed, 4 skipped`; `186 passed`; `73 passed`; `2 passed` |
| step 2 | SIMULATED | `10 passed` (correction 1); base `5 failed, 4 passed` |
| step 3 | SIMULATED | `LEGACY rich -> ['RM-001', ('LC-002', 0.86...`; `3 passed, 7 deselected` |
| step 4 | SIMULATED | `changed 0 of 314` |
| step 5 | SIMULATED | ruff `All checks passed!`; `5 files changed, 121 insertions(+)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-18: RM-004 (GDI-only) needs a GDI decode or the MODERN era (F-C1-6).

### Cold read ###
own pass 2026-11-13: P1-P3 measured (facts 1, 6) · patch applies clean · traceability: criteria 1-2 → steps 1-5
and R4 · cold read: not triggered (d2, scripted patch) · no finding.

### Correction history ###
- **Correction 1 (2026-11-13, second review of `2a3ccd1`, ds-pro APPROVE WITH CORRECTIONS).** Upheld after
  re-derivation: (M) the GDI-chemistry test checked only the winner; (M) no test asserted the `hardware_gate`
  prune record; (L) the docstring's "PORT_INJECTION alone never prunes" read as a contradiction on LEGACY. Not
  upheld: (M) criteria evidence not in the prompt (Cowork re-ran the gates; the note holds R4 and step 5); (L)
  module-level `logging.disable` (the pattern of every T-COMA test). Rehearsed: test `10 passed`; mutant E
  `1 failed, 9 passed`; wired `186`; ruff clean; `5 files changed, 121 insertions(+)` from `24d265b`.
