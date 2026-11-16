# RULING T-AUD-24l — what to fix from the T-AUD-23f ecu_fault and no_fault verdicts (Windows Cowork, 2026-11-16)

Input: `REVIEW_T-AUD-23f.md` (10 CONTRADICTED). Corpus: v7, 314 cases, tip `fix/T-AUD-23f` (rule data =
`fix/T-AUD-24k`). Base family 224, code 126, ecu_fault verdict 16 / right 14 (MEASURED; a no-op variant reproduces
`recheck/T-AUD-24k/promoted.json`). Variants and probes: `C:/4DApp/recheck/T-AUD-24l/run.sh`, `run.txt`.

| group | claims | variant | changed | family | code | EF verdict/right | probe changed |
|---|---|---|---|---|---|---|---|
| EF perception delta | CK0377, 0382, 0387, 0388 | ±0.02/±0.03 → ±0.05 | 3 | 224 → 221 | 126 | 16/14 → 13/11 | 6 (never: 218) |
| EF-003 frozen band | CK0389-CK0392 | −5..5 → −2..2 | 0 | 224 | 126 | 16/14 | 3 (never: 221) |
| NF-002 CO | CK0544 | ≤ 0.05 → ≤ 0.1 | 2 | 224 | 126 | — | always: same 2 |
| triangle band (GASLab) | CK0397 (description), W0281 | upper 16 → 18 | 0 | 224 | 126 | — | upper 10: 0 |

## Rulings
1. **No fix: EF perception delta.** At ±0.05 the row loses CSV-045, YAML-CSV45 and YAML-TC47: EF-003 → CF-001, all
   three expected ECU-001. These DEFINITIVE gates carry the only right EF-003 verdicts. The SF fix (T-AUD-24k) gained
   because SF over-fires; EF under-fires, and the same move costs it. Lost: one delta value across all families
   (consistent, but 3 right verdicts lost).
2. **No fix: EF-003 frozen band.** At ±2 the corpus does not change (the right cases already have |trim| ≤ 2), so a
   narrower band is a guess with nothing to test it. The verdict stays CONTRADICTED as a known weak gate. Lost:
   narrowing it on the source reading alone.
3. **No fix: NF-002 CO.** At ≤ 0.1 two lean-condition cases (CSV-068, YAML-CSV68) move from EL-001 to NF-002. Both
   were wrong before, and no-fault is the worse wrong answer: it tells the owner that nothing is broken.
   REVIEW_T-AUD-23f L1 already warns against the Walker 0.1-0.45 band. Lost: the move to the OIML MPE floor.
4. **No fix here: the triangle band.** CK0397 is EF-005 description text. The gate itself is GASLab's
   `sum_valid_min/max` (`gas_lab_ontology.yaml:22-23`, `rule_engine.py:169-170`; wiki root W0281, no verdict yet).
   The corpus does not reach it (even an upper edge of 10 changes 0 of 314). It belongs to a GASLab verification
   slice (W0281), not a COMLab fix.
