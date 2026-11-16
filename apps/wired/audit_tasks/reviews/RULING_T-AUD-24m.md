# RULING T-AUD-24m — what to fix from the T-AUD-23g cam_timing verdicts (Windows Cowork, 2026-11-16)

Input: `REVIEW_T-AUD-23g.md` (14 CONTRADICTED). Corpus: v7, 314 cases, tip `fix/T-AUD-23g` (rule data =
`fix/T-AUD-24k`). Base family 224, code 126, cam_timing verdict 9 / right 7 (MEASURED; a no-op variant reproduces
`recheck/T-AUD-24k/promoted.json`). Variants and probes: `C:/4DApp/recheck/T-AUD-24m/run.sh`, `run.txt`.

| group | claims | variant | changed | family | code | CT verdict/right |
|---|---|---|---|---|---|---|
| low-NOx gates (CT-003 `:96`, CT-007 `:328`, CT-008 `:404`) | CK0309, 0334, 0342 | never passes | 2 | 224 → 222 | 126 → 124 | 9/7 → 7/5 |
| same | same | always passes | 3 | 224 → 223 | 126 | 9/7 → 12/8 |
| trims (`:48`, `:104`, `:148`, `:156`) | CK0307, 0310, 0316, 0317 | ±8 (source band) | 0 | 224 | 126 | 9/7 |
| same | same | never passes | 0 | 224 | 126 | 9/7 |
| CT-008 O2 window (`:395-396`) | CK0340, 0341 | 0-1.0 % | 1 | 224 → 223 | 126 | 9/7 → 10/7 |
| same | same | never passes | 0 | 224 | 126 | 9/7 |
| CT-008 CO2 window (`:386-387`) | CK0338 | lower edge 12.0 | 0 | 224 | 126 | 9/7 |
| same | same | never passes | 1 | 224 | 126 | 9/7 → 8/7 (wrong → wrong) |

CK0304-CK0306 and CK0313/CK0314 are values in the CT-002/CT-004 description text, not gates. CT-002 has no NOx gate.

## Rulings
1. **No fix: the low-NOx gates.** The sources show idle NOx is near 0 ppm on a healthy engine, so the gate does not
   single out a cam fault. But it carries the two right CT-007 verdicts (CASE-018, EXT-210): without it they go to
   CF-001. Letting it always pass adds 3 CT-008 verdicts, of which 1 is right. The gate stays CONTRADICTED as a weak
   discriminator. Lost: dropping it on the evidence (−2 family, −2 code).
2. **No fix: the trim gates.** The corpus does not reach them, even with a never-passes probe. Lost: moving them to
   ±8 with nothing to test the move.
3. **No fix: the CT-008 O2 and CO2 windows.** Moving O2 to the source's healthy band costs 1 (era2_012 → CT-008,
   expected sensor_fault); CO2 at 12.0 changes 0. CT-008 is by its description "tightly bounded to the observed
   non-VVT gas window", so a window fitted to observed cases is its design, not a domain claim.
4. **Description text** (CK0304-0306, 0313, 0314, and CK0320/CK0329's DTC ranges, PARTLY): changing it moves no
   verdict, so it is too small for a row of its own. Lost: a docs row for three description strings.
