# RULING T-AUD-24o — what to fix from the T-AUD-23i non_starter verdicts (Windows Cowork, 2026-11-16)

Input: `REVIEW_T-AUD-23i.md` (14 CONTRADICTED). Corpus: v7, 314 cases, rule data = `fix/T-AUD-24k`. Base family 224,
code 126, non_starter 5 / right 5. Variants: `C:/4DApp/recheck/T-AUD-24o/run.sh`, `run.txt`.

| group | variant | changed | probe (never passes) |
|---|---|---|---|
| rpm < 600 (5 NS gates) | < 400 | 0 | 0 |
| same + MW-005 rpm > 600 | 400 | 0 | — |
| NS-002 ECT < 30 | < 10 | 0 | 0 |
| NS-001/002 LTFT −1..1 | — | — | 0 |

The corpus does not reach any of these gates. The evidence is the sources and the unit tests.

## Rulings
1. **Fix: no-start speed < 400 rpm, MW-005 running gate > 400 rpm, NS-002 ECT < 10 °C** (the T-AUD-24o task). The
   regulator's idle band starts at 450 rpm (S001), so 600 marks some running engines as not running. 400 is under
   that floor and above any cranking speed. MW-005 moves with it, so the two rules still split at one speed. This
   also settles REVIEW_T-AUD-23i L1, the 23h/23i disagreement over 600. CARB's normal cold-start band is 10-30 °C
   (S027), so "extreme cold" starts below 10. Rehearsal: comlab 614, registry 510/5, wired 1 failed (T-COMA-10)
   237 passed, corpus 0 changed. Lost: no fix because the corpus cannot see it. The sources are a regulator and a
   law, and the change is safe: a real no-start still passes.
2. **No fix: the LTFT −1..1 band.** It is wrong for a real no-start (the ECU keeps learned LTFT, S030), but removing
   the evidence row is a structural change that the corpus cannot test, and the only source is one TRADE text. It
   stays CONTRADICTED as a known weak gate.
3. **No fix: the CO2 gates** (PARTLY; no source gives the cranking-only CO2).
