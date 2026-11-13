# T-COMA-15 — authoring sidecar (Windows Cowork, 2026-11-13)

Input: `audit/reports/R1_D2_20261017.md` F-D2-1; `labs/comlab/comlab/core/perception_contradiction.py`;
`labs/comlab/registry/rules/sensor_fault.json`; `labs/comlab/comlab/schemas/vocabulary.py`; `COMLab_BDD.md`; GASLab
atlas (`labs/gaslab/wiki/05_fault_atlas_part_a.md`, `06b_...`). Rehearsal: `C:/4DApp/recheck/T-COMA-15/`.

### Verified context ###
1. **Still open on `68dd691`:** `delta > tol` (OBD leaner) returns `O2_SENSOR_BIASED_HIGH`. The vocabulary says
   HIGH = "sensor reads artificially rich", the BDD says biased-lean is LOW, and the GASLab atlas says LOW = "chem
   rich, ECU perceives lean". SF-001 (HIGH) pairs `o2_voltage ≥ 0.55` (the sensor reports rich) with
   `lambda_perception_delta > 0.03` (OBD reads lean): the rule contradicts itself. SF-002 mirrors it. Observed.
2. **Referee** (`referee.py`): the 5 corpus cases GASLab classifies `O2_SENSOR_BIASED_HIGH` and that have a delta
   outside the band all have a rich delta (−0.09 to −0.11). None has a lean delta. Observed.
3. **Rehearsal** (restored): new test `6 passed`, base `4 failed, 2 passed`; mutants A (labels) and B (rule rows)
   `2 failed` each. comlab `510 passed, 4 skipped`, after re-pinning 13 tests (11 perception unit tests, 2 e2e label
   asserts). wired `170 → 176`, after 2 oil-case pins move SF-001 → SF-002. ui `70`. Corpus: 18 codes change
   (SF-001↔SF-002, plus EXP-N005 CF-001 → SF-001, where GASLab says `O2_SENSOR_BIASED_HIGH` with a rich delta).
   Family accuracy 216 equal. ruff clean. `5 files changed, 36 insertions(+), 35 deletions(-)` plus the 40-line test.
   Observed.

### Rulings and the tradeoff that lost ###
- **Fix the direction at both ends (label and rule rows).** Lost: swapping only the label. That would leave SF-001
  firing on lean deltas under a "biased high" name, and its chemistry and delta rows would still disagree.
- **Re-pin the tests that encoded the inversion** (23 tokens in the unit file, 2 e2e asserts, 2 oil pins). These
  tests pinned the observed behaviour, not a specification: the BDD, the vocabulary and the atlas all say the
  opposite.
- **Mock names and rule-description wording stay** (out of scope, recorded): renaming the e2e mocks is test churn
  with no behaviour change.
- Plan NONE, difficulty 2 (a domain-direction ruling, but scripted and rehearsed). Code row: second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `510 passed, 4 skipped`; `176 passed`; `70 passed` |
| step 2 | SIMULATED | `6 passed`; base `4 failed, 2 passed` |
| step 3 | SIMULATED | LOW line, then HIGH line |
| step 4 | SIMULATED | `vs before 18 of 314`; `vs expected 0 of 314` |
| step 5 | SIMULATED | ruff `All checks passed!`; `6 files changed, 76 insertions(+), 35 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-15: O2 bias direction (lean reading = BIASED_LOW) in the label and the SF-001/SF-002 rows (F-D2-1).

### Cold read ###
own pass 2026-11-13: P1-P3 measured (facts 1, 3) · `rehearse.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-5 and R5 · cold read: not triggered (d2, scripted) · no finding.

### Correction history ###
- **Correction 1 (2026-11-13), after the second review of `e8f1e84`** (`C:/4DApp/recheck/codex/T-COMA-15_review.md`,
  ds-flash, APPROVE WITH CORRECTIONS). Medium upheld: `rule.description` becomes `fault_name`, `display_headline` and
  `ui_diagnostic_string` (140 characters), and SF-001's text said "(sensor reads falsely lean, ECU over-fuels)" while
  SF-001 now fires when the sensor reads rich; SF-002 is the mirror image. The old text used the λ-value meaning of
  "high". The two parentheticals are swapped. Low upheld: the test now pins each delta row's value and tier, and that
  the description names the same direction. Rehearsed (`correction1.patch`): the corrected test goes 2 failed to
  6 passed; comlab, wired 176, ui, corpus (0 of 314 against expected) and ruff are equal. Lost: accepting with a
  follow-up row, which would ship user-facing text that contradicts the verdict.
