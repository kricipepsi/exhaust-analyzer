# REVIEW T-AUD-23g — verify 28 cam_timing rule values (Windows Cowork, 2026-11-16)

**Verdict: ACCEPT, score 96.** Docs/data row, so no second-model review (CLAUDE.md step 6). Hydrogen lane (high),
14.9 min (lane `.exit` 12:01:57-12:16:52 CET).

## Facts (Cowork re-ran, branch `fix/T-AUD-23g`, after promote)
- Commits after `fix/T-AUD-24l`: `5e8f441` spec, `a856b3a` lane work, `86201c2` merge. Name-status: M `verdicts.csv`;
  A the note and the RESULT. No new source (all reused); no D, no R; no `search/` left.
- `check_verdicts.py`: `VERDICTS OK` for T-AUD-23g (28) and the six earlier scopes. Existing rows removed: `0`.
  The checker confirms each quote in its fetched file (whitespace-normalised).
- Verdicts: CONTRADICTED 14, PARTLY 10, CONFIRMED 4. Re-derived: S028:34, S032:3, :262, :276, S037:2746, :2777-2778,
  S030:135.

## What the verdicts say (for the ruling row)
- **Low-NOx gates (5: CK0304, 0309, 0334, 0342 CONTRADICTED; CK0305 > 800 PARTLY):** healthy warm-idle NOx is
  near 0 ppm (S028, S035), so "NOx < 80" (or < 40) passes on every healthy idle and does not single out a VVT fault.
  This matches Cowork's own knowledge: idle NOx with a working catalyst is near zero.
- **Trim gates ≥ 2 / ≤ −5 (8 CONTRADICTED: CK0306, 0307, 0310, 0313, 0314, 0316, 0317):** inside the ±8-10 % healthy
  band. This is the same finding as T-AUD-23d/23e.
- **CT-008 gas window (CK0338 CO2 ≥ 12.5, CK0340/0341 O2 1.5-2.0 CONTRADICTED):** S032 gives no O2 change for
  retarded timing, and healthy O2 under 1 %.
- **DTC ranges (CK0320, CK0329 PARTLY):** J2012 camshaft codes run P0010-P0025 (S037 lists P0024/P0025). Each rule
  description drops some codes.
- CONFIRMED: CK0321, 0323, 0324 (STFT −5..5 = Ford's entry range), CK0333 (CO2 < 13: S032 < 12 = lack of combustion,
  within 20 %).

## Findings
- **L1 (Low):** the trim and gas verdicts rest on TRADE sources (S030, S032, S028); S037 (Ford OEM) carries the DTC
  and the STFT entry range. They are disclosed. Score −3.
- **L2 (Low):** CK0305's PARTLY ("NOx > 800 as the lean discriminator") cites "near 0 at idle even when lean". That
  makes the gate unreachable at idle, which is closer to CONTRADICTED. Score −1.

## What this unblocks
T-AUD-24m (design ruling, measure first): cam_timing expected 11, right 7. Measure the low-NOx gates with a
never-fires probe, the trims at the source band, and the CT-008 O2 window, each with a liveness probe.
