# T-VINA-10 — authoring sidecar (Windows Cowork, 2026-11-04)

### Verified context ###
1. **Euro is almost never known** on real VINs: 27 of 1,131 (applied in-window row with a recognised `euro_norm`).
   Observed (`C:/4DApp/recheck/scratch/survey_T-VINA-10.md` § 1).
2. **COMLab reads `resolved_horizon` first** and derives it from the euro only when it is absent
   (`comlab/projection.py`, `comlab/core/horizon_context_injector.py`). Observed (survey § 3). So the horizon fix needs no
   contract change.
3. **The rule moves 416 real VINs** LEGACY → ADAPTIVE and stress 3000 → 3500; 1 corpus run, 0 verdicts. Observed
   (survey § 1, § 2).
4. **The comlab era table overlaps** at 2001 and 2011; EU dates settle both edges (Euro 3 all registrations
   2001-01-01, 98/69/EC; Euro 5 2011-01-01, Reg. 715/2007). The dates are Cowork's knowledge, not measured here: the
   plan review and the second review check them.

### Rulings and the tradeoff that lost ###
- Emitted euro stays EURO_1 when unknown, with a confidence flag. Lost: an UNKNOWN enum value (a cross-lab contract
  change in SEMANTIC_CONTRACT §6.4 and COMLab's schemas).
- No year and no euro stays LEGACY. Lost: a guessed era for 438 real VINs.
- The citation goes in VINLab's own wiki (§10.8). Lost: an edit of COMLab's wiki table (another lab's page).
- The `>= 1996` literal stays with T-VINA-4 (O₂).
- Difficulty 4, plan REQUIRED: decoder behaviour across 416 real VINs and snapshot fixtures.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | base `297 passed, 8 skipped` (Cowork, T-VINA-14 review, `2ff9211`) |
| step 2 | DEFERRED | `test_euro_unknown_horizon.py` does not exist |
| step 3 | RAN | `27 passed`, `41 passed`, `30 passed` (T-VINA-14 review) |
| step 4 | SIMULATED | on the base the two `f1_` probes fail (P4); `rehearse.py` prints 416 changes on the base, and 0 is the observable on the build |
| step 5 | DEFERRED | the files do not exist or are unchanged |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-VINA-10: era from model year when euro unknown (416 real VINs to ADAPTIVE), flag euro_unknown, cited §10.8.

### Cold read ###
own pass 2026-11-04: P1-P4 measured · literals found once (`Used only when euro_emission_category is unknown.`,
`_EURO_MAP: dict[str, str] = {`, `def test_f1_horizon_follows_year_when_euro_unknown`, LLD `## 9. Stress-Idle RPM`;
`## 10.8` absent) · 1c: R1 "only when" defines the set; R2's three cases are exhaustive · rehearsal on a built decoder is
a no-op (step 4 observable 0) · authoring checks: 2 wording findings patched (gate baseline, 1996 restated) ·
traceability: criteria 1-4 → steps 1-5 · JUDGEMENT: 0.
cold read 2026-11-04: skipped, plan-gated (Plan: REQUIRED; the plan review and its second-model review cover it).

### Correction history ###
- **01 (2026-11-04, plan review; Plan: APPROVED with C1-C4).** Plan reproduces P1-P4; 3 snapshots change (horizon,
  stress). Cowork C1: `euro_unknown` row in VIN_VOCABULARY § 4. Second review (codex): APPROVE WITH CORRECTIONS, F1 HIGH
  (known-euro path untested), F2 MED (wiki MODERN wording), F3 MED (helper call untested) upheld as C2-C4; F4 LOW not
  upheld (the script adds the key only on a difference). Dates 98/69/EC and 715/2007 confirmed by the second review.
  Record: `corrections/T-VINA-10_plan_correction_20261104.md`.
