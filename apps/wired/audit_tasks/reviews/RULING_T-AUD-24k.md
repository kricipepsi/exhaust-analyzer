# RULING T-AUD-24k — what to fix from the T-AUD-23e sensor_fault verdicts (Windows Cowork, 2026-11-16)

Input: `REVIEW_T-AUD-23e.md` (21 CONTRADICTED, 4 PARTLY, 3 CONFIRMED). Corpus: v7, 314 cases, tip `fix/T-AUD-23e`
(rule data = `fix/T-AUD-24j`). Base family 221, code 126, sensor_fault verdict 37 / right 16 (MEASURED,
`C:/4DApp/recheck/T-AUD-24k/base.json`). One variant per group and an extreme (never-fires) probe beside it
(`recheck/T-AUD-24k/run.sh`, `run.txt`, `sfscore.py`).

| group | claims | variant | changed | family | code | SF verdict/right | probe changed |
|---|---|---|---|---|---|---|---|
| perception delta | CK0626 0630 0644 0645 0649 0650 0654 0655 0661 0662 0667 0668 | ±0.03 → ±0.05 | 4 | 221 → 224 | 126 | 37/16 → 33/16 | 21 |
| SF-008 trims | CK0669-CK0672 | STFT ±10, LTFT ±8 | 2 | 221 → 219 | 126 | 37/16 → 35/14 | 2 |
| SF-001/002 O2 voltage | CK0627, CK0631 | ≥ 0.8 / ≤ 0.2 | 0 | 221 | 126 | — | 0 |
| SF-006 downstream | CK0657 | ≥ 0.9 | 0 | 221 | 126 | — | 0 |
| SF-004 MAF | CK0646 | ≥ 7.0 | 0 | 221 | 126 | — | 0 |
| SF-005 MAP | CK0651 | < 25 | 0 | 221 | 126 | — | 0 |

## Rulings
1. **Fix: perception delta ±0.03 → ±0.05 on the 12 gates** (the T-AUD-24k task). The 4 changed cases are EXT-207,
   EXT-208, EXT-213 (SF-002 → CF-001, expected catalyst: right now) and PDF-4G-02 (SF-002 → CF-001, expected misfire:
   wrong before and after). No right SF verdict is lost. ±0.05 is the band SF-003 already uses for NORMAL_OPERATION,
   and it sits above the OEM agreement figures (S016 LSU 4.9 ±0.007 at λ = 1; S037 Ford UEGO ±2 % target) with room
   for analyser error and freeze-frame timing (REVIEW_T-AUD-23e M1). Lost: keeping ±0.03 because the TRADE verdicts
   are weak (it leaves 4 measured false positives in place).
2. **No fix: SF-008 trims.** Moving them to the source band costs 2 right SF verdicts (CSV-025, TC-046 → RM-001).
   Same outcome as the T-AUD-23d trims (RULING_T-AUD-24j). Reopen only with new corpus evidence.
3. **No fix: O2 voltage, downstream, MAF, MAP.** Even the never-fires probe changes 0 of 314, so the corpus does not
   reach these gates as a deciding weight. The sources show the gates fire on healthy readings, but they give no
   value a fix could move to: a single freeze-frame O2 sample cannot show bias, and no source gives a
   contaminated-downstream voltage. A fix would be a guess that nothing can test. They stay CONTRADICTED in
   `verdicts.csv` as known weak gates. Lost: moving them to "outside the healthy band" values that nothing measures.
