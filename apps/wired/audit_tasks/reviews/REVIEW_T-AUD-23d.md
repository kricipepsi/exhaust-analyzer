# REVIEW T-AUD-23d — verify 29 MF/RM/LC/CF rule values (Windows Cowork, 2026-11-16)

**Verdict: ACCEPT, score 95.** Docs/data row, so no second-model review (CLAUDE.md step 6). Hydrogen lane (high),
11.7 min.

## Facts (Cowork re-ran, branch `fix/T-AUD-23d`, after promote)
- Commits after `fix/T-GASA-19`: `f780041` spec, lane work, `221303a` merge. Name-status: M `sources.csv`,
  `verdicts.csv`; A `sources/S029`-`S036`, the note and the RESULT. No D, no R; no `search/` left.
- `check_verdicts.py`: `VERDICTS OK` for scopes T-AUD-23d (29), T-GASA-17 (20), T-AUD-23a (25), T-AUD-23b (29).
  `sources 33 primary 10`. Existing rows removed: `0`.
- Verdicts: CONTRADICTED 14, PARTLY 8, CONFIRMED 7. Sources: one OEM (S029, Toyota 2AZ-FE repair manual), one
  PRIMARY_LAW (S002, 2014/45/EU Annex I), the rest TRADE. The notes say so (R5).
- Re-derived: CK0352, CK0524, CK0445, CK0444. Each quote is in its source file, and each note states the rule's intent
  (rule `description`) against the source band.

## What the verdicts say (for the ruling row)
- **Fuel-trim gates inside the healthy band (9 CONTRADICTED):** CK0442, CK0444, CK0448, CK0516, CK0517, CK0520,
  CK0613, CK0615, CK0619. SUGGESTIVE gates at STFT ±5 % and LTFT +3/+8/−5/−8 % fire on healthy trims. The sources'
  bands are ±8-10 % normal, and the OEM gives ±20 % combined as "functioning".
- **NORMAL_OPERATION HC gates looser than healthy (2):** CK0352 (CF-002 `hc < 100`), CK0524 (MF-004 `hc < 200`).
  "Pristine" chemistry is 0-35 ppm (S023).
- **Airflow and pressure (2):** CK0445 LC-002 `map_kpa < 40` (healthy idle MAP 30-50 kPa; a vacuum leak raises MAP),
  CK0447 LC-003 `maf < 3.5 g/s` (healthy idle 2-7 g/s).
- **Catalyst not lighting off (1):** CK0358 CF-004 `co2 ≥ 13` (healthy 14.5-16 %).
- CONFIRMED: CK0348, CK0351, CK0355, CK0367, CK0441, CK0611 (λ 0.97 = the 2014/45/EU lower bound), CK0612.

## Findings
- **L1 (Low):** 11 of the 14 CONTRADICTED verdicts rest on TRADE sources (S023, S030, S036). They are disclosed, but
  a fix row should weigh them as trade evidence. Score −3.
- **L2 (Low):** CK0622 (`LTFT ≤ −15`) is PARTLY on a single GM bulletin (S031). Score −2.

## What this unblocks
T-AUD-24j (design ruling, measure first): the 14 CONTRADICTED gates. They are SUGGESTIVE weights next to DEFINITIVE
chemistry, so a change shifts scores, not gates. Measure the v7 corpus with each group moved to the source band
before any fix.
