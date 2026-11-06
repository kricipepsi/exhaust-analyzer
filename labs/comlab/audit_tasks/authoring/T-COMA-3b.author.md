# T-COMA-3b — authoring sidecar (Windows Cowork, 2026-11-06)

Design input: `T-COMA-3.design.md` (same folder), § "T-COMA-3b survey". Rehearsal: `C:/4DApp/recheck/T-COMA-3b/`
(`apply_fix.py`, `rehearsal.patch`, `tests/`, `cw/corpus.json`).

### Verified context ###
1. **Every cranking corpus sample is INVALID on the base.** REAL-002 (CO2 2.98, O2 16.75), REAL-003 (CO 3.24, CO2 1.16,
   O2 14.54), case_006/case_040 (CO2 0.04, O2 20.9), case_007 (CO2 4.0, O2 16.0): CO+CO2 ≤ 6 or the triangle sum is out
   of [14, 18]. The shim drops `chemistry_state` on `INVALID`. Observed.
2. **COMLab's `GasLabPayload` carries no engine state** (`comlab/schemas/ingestion.py`), so the new bucket needs no
   COMLab mirror. COMLab's `EngineStateBucket` is OBD's `rpm_state_bucket` (`RpmStateBucket = EngineStateBucket`).
   Observed.
3. **The shim adds +0.10 for the non_starter symptom prior** (`fault_atlas_router.py`, symptom_prior v2): NS shim score
   0.85 → displayed 0.95, 0.9 → 1.0. 203 of 314 corpus verdicts already show 1.0. Observed.
4. **Rehearsal 1 (bucket only, no R4):** case_040 NS-005 → NS-001 and case_006 NS-004 → NS-001 (NS-001 0.85 beats the
   0.7/0.8 DTC rules). **Rehearsal 2 (no CO2 ≥ 8 guard):** the idle-rich sample under will_not_start gave NS-002 and the
   default stoich sample gave NS-003. Both led to rulings below. Observed.
5. **Final rehearsal** (restored): gaslab 208 → 215; wired 104 → 106; registry 5F/503P → 5F/504P; non_starter tests
   30 → 31; comlab 503/4/2; ui 57; corpus differ 5 (P2); NEW tags fail on the base (GASLab 6F/1P, wired 3F/2P); ruff
   clean. Observed.

### Rulings and the tradeoff that lost ###
- **A GASLab-only `CRANKING` bucket set by the composition from triage `will_not_start`.** Lost: a context flag outside
  the enum (smaller, but invisible in the vocabulary); retiring NS-001..NS-003 (smaller still, but a no-start without a
  DTC would abstain for ever); GAS_VOCABULARY §7's "identical to OBDLab" (now: the first four values).
- **Triage `cranking` keeps the gas form's bucket.** Its engine runs, and the non_starter family gate does not apply, so
  `LEAN_MISFIRE` would feed running-engine families. Lost: cranking chemistry for those sessions.
- **CO2 ≥ 8 % under `CRANKING` stays `SAMPLE_INVALID`.** A running-engine burn contradicts the no-start; the session
  keeps the T-COMA-1 abstain. Lost: a verdict from a mislabelled session.
- **Thresholds from GAS_VOCABULARY §10:** CO 1.5 (`clear_rich.min`), CO2 5.0 (`total_quench.max`); 8.0 is NS-003's CO2
  ceiling. Lost: a measured cranking calibration (the corpus has five cranking samples).
- **A component DTC outranks the generic chemistry rule** (NS-004/NS-005 0.8/0.9 > NS-001 ceiling 0.85). The DTC names
  the part to replace; NS-001 names the symptom. Lost: NS-004's "fallback below chemistry" design note, written when
  chemistry could not reach these rules.
- **Plan NONE, difficulty 3** (`--model claude-sonnet-5-5 --effort medium`): every edit is Cowork's rehearsed script,
  so an implementer plan has no design to review; the design gets the second-model review at code review. Lost: the
  handoff's REQUIRED marker (precedent: T-AUD-4s).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `7 passed`; gaslab `215 passed, 2 skipped, 4 deselected` |
| step 2 | SIMULATED | `5 passed`; `106 passed`; `5 failed, 504 passed, 4 deselected`; `31 passed`; `503 passed, 4 skipped, 2 errors`; `57 passed` |
| step 3 | SIMULATED | `corpus 314`; `differ 5`; the P2 lines |
| step 4 | SIMULATED | ruff `All checks passed!`; status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-3b: a will_not_start gas sample is a cranking sample; NS-001..003 can name the no-start.

### Cold read ###
own pass 2026-11-06: P1-P4 measured · `apply_fix.py` exits on any literal count other than 1 · counts: gaslab 208 + 7 =
215, wired 104 + 5 - 3 = 106, registry 503 + 1 = 504, non_starter 30 + 1 = 31 · traceability: criteria 1-4 → steps 1-4 ·
patched: `apply_fix.py` run from `C:/4DApp/repo` (relative paths) · no finding.
cold read 2026-11-06 FOCUSED reader; trigger 1c grep hit (R1 "GASLab-only", criterion 4 "only"); 0 findings, 0 patched — 3 calls.

### Correction history ###
(none)
