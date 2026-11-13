# T-COMA-28 — authoring sidecar (Windows Cowork, 2026-11-13)

Input: F-C1-2 (its F2 half: the probe `test_mechanism_lc002_and_mf005_fire_on_normal_values_only`); REVIEW_T-COMA-27
(L1, L3, L4). Survey and rehearsal: `C:/4DApp/recheck/F-C1-2/sink_variants.py`, `C:/4DApp/recheck/T-COMA-28/`.

### Verified context ###
1. **The engine fires a rule on one satisfied row when no GATING row fails** (`_score_rule_raw`). On the probe's normal
   values, LC-002 scores 0.86 (`map_kpa < 40`) and MF-005 0.80 (`none_present`), with no chemistry match. Observed.
2. **Variants measured on the corpus** (rules patched in memory; accuracy vs `expected_fault_family`): base 216; LC-002
   and MF-005 with every chemistry row GATING 219 (but LC-002 then needs two states at once and can never fire);
   one GATING row each 219 (+8 −5); a chemistry match required for every rule 153 (rejected). Observed.
3. **With base +0.10** (the lost DEFINITIVE bonus) the real edit gives 221 of 314, 32 verdicts changed, +9 −4.
   LC-002's three `passes_cases` are won by other rules on the base and after. Observed.
4. **Four pins held only through a sink**, each re-derived:
   - differential surfacing: the request's gas never reached the shim (chemistry `None`), and the only sibling was
     MF-005 firing with no chemistry. With the gas passed through: LC-001 0.95 and five runtime siblings;
   - tunable reweight: era3_007's gas is SAMPLE_INVALID; lean reached its top 3 only through LC-002;
   - T-COMA-11: CASE-013 and CASE-016 become CF-001 at 1.0, their labelled family;
   - T-COMA-6: LC-002 is now pruned by its chemistry gate; LC-003 is still weak-support only.
   Observed.
5. **Rehearsal** (restored; `rehearse.py` round-trips): comlab `569`, wired `186`, ui `75`, registry
   `508 passed, 5 skipped`, targeted `29`, probe mechanism test passes, ruff clean, `9 files changed, 77 insertions(+),
   13 deletions(-)`. Observed.

### Rulings and the tradeoff that lost ###
- **One GATING chemistry row per sink, base +0.10.** Lost: GATING with no weight change (219, and it lowers a genuine
  LC-002 or MF-005 score by 0.10); an engine-wide chemistry requirement (153).
- **Accept 4 losses for 9 gains.** The 4 lost cases were right only because a sink fired without its chemistry.
- **Fold REVIEW_T-COMA-27's three Lows in here.** They edit the same test files; a separate row would cost a cycle.
- **`rehearse.py` admits this task's note and RESULT** (the T-COMA-27 spec defect, fixed).
- Difficulty 2 (scripted). Roster: Opus 5.5 medium. Plan NONE; code row: second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `569 passed`; `186 passed`; `75 passed` |
| step 2 | SIMULATED | `508 passed, 5 skipped`; `29 passed` |
| step 3 | SIMULATED | `LC-002 score: None MF-005 score: None map_kpa: 35.0`; `1 failed, 13 passed, 2 deselected` |
| step 4 | SIMULATED | `changed 32 of 314`; `family accuracy 221 of 314 (before 216)`; `gained 9 lost 4` |
| step 5 | SIMULATED | ruff `All checks passed!`; `9 files changed, 77 insertions(+), 13 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-28: LC-002 and MF-005 gate on their own chemistry; corpus 216 → 221 of 314.

### Cold read ###
own pass 2026-11-13: P1-P2 measured (facts 3, 5) · `rehearse.py` exits on an unexpected dirty file or a missing
anchor · traceability: criteria 1-2 → steps 1-5 · cold read: not run (difficulty 2, process by difficulty, 055) ·
no finding.

### Correction history ###
(none)
