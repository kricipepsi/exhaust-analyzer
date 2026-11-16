# REVIEW T-AUD-23f — verify 24 ecu_fault and no_fault rule values (Windows Cowork, 2026-11-16)

**Verdict: ACCEPT, score 95.** Docs/data row, so no second-model review (CLAUDE.md step 6). Hydrogen lane (high),
9.8 min (lane `.exit` 11:42:08-11:51:55 CET).

## Facts (Cowork re-ran, branch `fix/T-AUD-23f`, after promote)
- Commits after `fix/T-AUD-24k`: `347028b` spec, `8fb4968` lane work, `661b16d` merge. Name-status: M `sources.csv`,
  `verdicts.csv`; A `sources/S041.md`, the note and the RESULT. No D, no R; no `search/` left.
- `check_verdicts.py`: `VERDICTS OK` for T-AUD-23f (24) and the five earlier scopes (20, 25, 29, 29, 28).
  `sources 38 primary 11`. Existing rows removed: `0`.
- Verdicts: CONTRADICTED 10, CONFIRMED 8, PARTLY 6. New source: S041 Delaware DMV DTC list (PRIMARY_REGULATOR).
- Re-derived in the source files: S041:44, S023:38, S037:790 and :1262, S040:73, S002 (λ 1 ± 0,03).

## What the verdicts say (for the ruling row)
- **Perception delta (4 CONTRADICTED):** EF-001/EF-002 `±0.02` (CK0377, CK0382) and EF-003 `±0.03` (CK0387,
  CK0388), all DEFINITIVE. This is the same finding as T-AUD-23e: the gates sit at the edge of healthy agreement.
- **EF-003 frozen-trim band −5..5 (4 CONTRADICTED, CK0389-CK0392):** the band holds healthy closed-loop trims (S037's
  STFT monitor-entry range is ±5 %; S030 gives LTFT 5-8 %). It is not evidence of frozen trims.
- **CK0397 triangle band 14-16 % vol CONTRADICTED:** healthy samples reach 16.3-16.8 % (S040, S023). This agrees with
  the T-AUD-23c suspect (GAS_VOCABULARY §10.6: < 14 and ≥ 18).
- **CK0544 NF-002 CO ≤ 0.05 % CONTRADICTED:** below the OIML R 99 Class I CO error (±0.06 %, S014).
- PARTLY: the EF-001/002 saturation gates (CK0378, 0379, 0383, 0384; OEMs set P0171/P0172 at LTFT > 25 % or ±35 %
  combined), CK0395 (J2012 P06xx = computer and auxiliary outputs, not only "ECU internal"), CK0538 NOx ≤ 50.
- CONFIRMED: NF-001/002 OBD λ 0.97-1.03 (2014/45/EU 1 ± 0.03), CO2 ≥ 14.5/14.6, HC ≤ 30, O2 ≤ 0.5.

## Findings
- **L1 (Low):** CK0544 cites Walker (S023, TRADE) "0.1-0.45 % CO at idle" as healthy. A modern catalyst car usually
  reads under 0.1 % at warm idle (Cowork's own knowledge), so that band overstates healthy CO. The verdict stands on
  the OIML MPE argument, but the ruling row must not move the gate to 0.45. Score −3.
- **L2 (Low):** 6 of the 10 CONTRADICTED rest on TRADE sources (S030, S038, S040, S023). They are disclosed. Score −2.

## What this unblocks
T-AUD-24l (design ruling, measure first): ECU-fault misses 17 of 31 corpus cases. Measure family and code accuracy
with the EF perception delta at ±0.05, the EF-003 band narrowed (frozen = |trim| ≤ 1-2 %), the triangle band at the
vocabulary's [14, 18), and NF-002 CO at 0.1. Use liveness probes beside each.
