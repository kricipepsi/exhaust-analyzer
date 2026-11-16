# T-AUD-24k — authoring sidecar (Windows Cowork, 2026-11-16)

Input: T-AUD-23e verdicts and `reviews/RULING_T-AUD-24k.md` (corpus measured per group, with liveness probes).
Difficulty 2: no survey or cold read beyond the corpus ruling; a code row, so it keeps its second review. Lane:
Hydrogen medium.

### Verified context ###
1. **P1 lines:** 6 × `-0.03`, 6 × `0.03` at the listed lines of `sensor_fault.json` on 368f22f. First action run.
2. **Corpus with R1:** changed 4, family 221 → 224, code 126 → 126, SF 37/16 → 33/16 (`recheck/T-AUD-24k/delta_05.json`).
3. **Rehearsal:** comlab 611 → 614, registry 510/5 equal; new test 2 failed / 1 passed on base, 3 passed with R1
   (`recheck/T-AUD-24k/rehearsal.diff`, `test_t_aud_24k_sf_perception_delta.py`).
4. **No test or doc pins ±0.03** on these gates (grep of `labs/comlab` tests and `*.md`).

### Rulings and the tradeoff that lost ###
- **±0.05, not a wider value:** the band SF-003 already uses for NORMAL. Lost: ±0.08 (Ford's FAOS rear-bias limit),
  which measures a different signal.
- **A data test, not a scoring test:** the corpus already measures the scoring effect. Lost: a `_score_rule` test per
  rule (8 near-copies).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | 614 passed with R1-R2 |
| step 2 | RAN | 510 passed, 5 skipped |
| step 3 | RAN | 3 passed (base: 2 failed, 1 passed) |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-24k: SF perception-delta gates ±0.03 → ±0.05.

### Cold read ###
NONE (difficulty 2, CLAUDE.md process by difficulty).

### Correction history ###
(none)
