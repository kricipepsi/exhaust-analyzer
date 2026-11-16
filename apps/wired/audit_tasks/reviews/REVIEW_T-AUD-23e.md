# REVIEW T-AUD-23e — verify 28 sensor_fault rule values (Windows Cowork, 2026-11-16)

**Verdict: ACCEPT, score 93.** Docs/data row, so no second-model review (CLAUDE.md step 6). Hydrogen lane (high),
11.1 min (lane `.exit` 11:06:54-11:18:02 CET).

## Facts (Cowork re-ran, branch `fix/T-AUD-23e`, after promote)
- Commits after `fix/T-AUD-24j`: `493c1d0` spec, `b0f9205` lane work, `b1c29ec` merge. Name-status: M `sources.csv`,
  `verdicts.csv`; A `sources/S037`-`S040`, the note and the RESULT. No D, no R; no `search/` left.
- `check_verdicts.py`: `VERDICTS OK` for scopes T-AUD-23e (28), T-GASA-17 (20), T-AUD-23a (25), T-AUD-23b (29),
  T-AUD-23d (29). `sources 37 primary 10`. Existing rows removed: `0`.
- Verdicts: CONTRADICTED 21, PARTLY 4, CONFIRMED 3, UNSOURCED 0. New sources: S037 Ford OBD System Operation Summary
  MY2024-25 (OEM), S038 Hot Rod wideband test, S039 Apex Tech Nation P0131, S040 MOTOR 2010 (TRADE).
- Re-derived in the source files: S037:829-830 (FAOS rear-bias limits −0.083/+0.087), S037:85 (secondary O2
  0.45-0.85 V), S038:91, S040:39, S039:55, S024:547, S027:11194, S020:7, S016:126 (LSU 4.9 λ=1 accuracy ±0.007).

## What the verdicts say (for the ruling row)
- **Perception delta ±0.03 (12 CONTRADICTED: CK0626, 0630, 0644, 0645, 0649, 0650, 0654, 0655, 0661, 0662, 0667,
  0668)** and ±0.05 (CK0636, 0637 PARTLY). These gates are used by all eight SF rules.
- **Upstream O2 voltage taken from a freeze-frame sample:** CK0627 `≥ 0.55 V` and CK0631 `≤ 0.35 V` CONTRADICTED.
  A healthy sensor switches 0.1-0.9 V around 0.45 V, so one sample passes either gate about half the time.
  CK0634 `< 0.20 V` (pegged) CONFIRMED. CK0639 and CK0663 `≤ 0.2 V` PARTLY: no duration check.
- **CK0657 downstream `≥ 0.6 V` as contaminated** CONTRADICTED: a healthy rear sensor with a working catalyst
  holds about 0.7 V (S024; Ford 0.45-0.85 V).
- **CK0669-CK0672 SF-008 trims ±5 % STFT and ±3 % LTFT** CONTRADICTED. This is the same finding as T-AUD-23d
  (healthy ±8-10 %).
- **CK0646 MAF `≥ 3.5 g/s`, CK0651 MAP `< 35 kPa`** CONTRADICTED (healthy idle 2-7 g/s, 30-50 kPa).
- CONFIRMED: CK0634, CK0643 (~1 g/s per litre), CK0656 (ECT 60 °C = the CARB 140 °F stuck-cold example).

## Findings
- **M1 (Medium):** the 12 perception-delta CONTRADICTED verdicts rest on TRADE text. S040's ±5 % is the spread of
  engine lambda, not how closely two instruments agree on the same gas. S038's "up to 5 %" is for aftermarket
  widebands. The OEM numbers (S016 ±0.007 at λ = 1, S037's ±2 % UEGO target) put a healthy OBD-to-analyser
  difference near ±0.02-0.03, so a ±0.03 gate sits at the edge of the healthy band, not clearly inside it. PARTLY
  is the stronger reading. The ruling row must not move these gates on the verdict alone: measure the corpus first.
  Score −5.
- **L1 (Low):** CK0636/CK0637 PARTLY compares ±0.05 against Ford's FAOS rear-bias limit (−0.083/+0.087). That is a
  different signal: a downstream trim, not the upstream-to-analyser difference. Score −2.

## What this unblocks
T-AUD-24k (design ruling, measure first): SF over-fires (verdict 37, right 16 of 314). Measure the v7 corpus at
family and code level with each CONTRADICTED group moved to its source band: the freeze-frame O2-voltage gates
(CK0627, CK0631), the downstream gate (CK0657), the SF-008 trims, MAF/MAP. Then measure the perception delta at
±0.05 (M1) before any fix.
