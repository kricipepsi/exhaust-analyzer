# REVIEW T-AUD-23j — verify 24 values in five small rule files (Windows Cowork, 2026-11-16)

**Verdict: ACCEPT, score 95.** Docs/data row, so no second-model review (CLAUDE.md step 6). Hydrogen lane (high),
7.4 min (lane `.exit` 13:32:07-13:39:29 CET).

## Facts (Cowork re-ran, branch `fix/T-AUD-23j`, after promote)
- Commits after `fix/T-AUD-24o`: `31449b3` spec, `4959747` lane work, `1be6211` merge. Name-status: M `verdicts.csv`;
  A the note and the RESULT. No new source; no D, no R; no `search/` left.
- `check_verdicts.py`: `VERDICTS OK` for T-AUD-23j (24) and the nine earlier scopes. Existing rows removed: `0`.
- Verdicts: CONTRADICTED 11, PARTLY 8, CONFIRMED 5.

## What the verdicts say (for the ruling row)
- **Trims (6 CONTRADICTED: CK0676, 0682, 0683, 0689, 0410, 0401):** inside the ±8-10 % healthy band, as in every
  earlier slice. CK0675 (LTFT ≥ 10) CONFIRMED; CK0688 (≥ 15) PARTLY.
- **CK0677 VL-001 MAP > 40 CONTRADICTED** (inside healthy 30-50 kPa); CK0687 VL-003 > 50 CONFIRMED.
- **Overheating:** CK0597, CK0606 ECT > 105 CONTRADICTED (S037 normal band to 110 °C); CK0601 > 115 PARTLY; CK0593
  rpm > 1000 as an ECU-raised idle CONTRADICTED (S001 idle band to 1,500).
- **CK0406 EL-003 HC ≥ 200 CONTRADICTED, and it points the wrong way:** air entering at a probe or joint dilutes
  the sample and lowers HC, CO and CO2 while O2 rises (S032). Of all the verdicts, this one most clearly shows a
  gate built on the wrong direction.
- CONFIRMED: invalid-input bounds CO2 > 16, O2 > 18, CO2 < 5 (S023, S014, S011).

## Findings
- **L1 (Low):** 7 of the 11 CONTRADICTED rest on TRADE sources (S030, S032, S036). They are disclosed. Score −3.
- **L2 (Low):** CK0412 PARTLY: P0324 is not in S041's list, but SAE J2012 names P0324 "Knock Control System Error"
  (Cowork's knowledge); the range edge is a nit. Score −2.

## What this unblocks
T-AUD-24q (design ruling, measure first): EL-003 HC direction, OV ECT > 105, VL-001 MAP > 40, OV-001 rpm > 1000,
and the trims, each with a liveness probe. exhaust_leak expected 10, right 7.
