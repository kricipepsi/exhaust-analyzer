# REVIEW T-AUD-23i — verify 25 non_starter rule values (Windows Cowork, 2026-11-16)

**Verdict: ACCEPT, score 95.** Docs/data row, so no second-model review (CLAUDE.md step 6). Hydrogen lane (high),
15.6 min (lane `.exit` 12:41:11-12:56:47 CET).

## Facts (Cowork re-ran, branch `fix/T-AUD-23i`, after promote)
- Commits after `fix/T-AUD-24n`: `4d7a160` spec, `09f50cc` lane work, `5bb6e4f` merge. Name-status: M `verdicts.csv`;
  A the note and the RESULT. No new source; no D, no R; no `search/` left.
- `check_verdicts.py`: `VERDICTS OK` for T-AUD-23i (25) and the eight earlier scopes. Existing rows removed: `0`.
- Verdicts: CONTRADICTED 14, PARTLY 11. Re-derived: S001:261 (idle 450-1,500 rpm, DVSA), S027:3456 (CARB cold start
  10-30 °C), S030:23 and :25 (open loop, LTFT kept in memory).

## What the verdicts say (for the ruling row)
- **rpm < 600 as "cranking" (8 CONTRADICTED):** the DVSA idle band (S001, regulator) starts at 450 rpm, so a running
  engine can idle below 600.
- **ECT < 30 °C as "extreme cold enrichment" (CK0564, CK0569 CONTRADICTED):** CARB's normal cold-start band is
  10-30 °C (S027).
- **LTFT −1..1 at a no-start (CK0559, 0560, 0572, 0573 CONTRADICTED):** the ECU keeps learned LTFT in memory while it
  cranks (S030), so a real no-start shows the stored value, not 0. STFT −1..1 is PARTLY (open loop holds STFT at 0).
- **CO2 gates (PARTLY):** S032 puts lack of combustion at < 12 %; no source gives the cranking-only CO2.

## Findings
- **L1 (Low, across slices):** T-AUD-23h CONFIRMED CK0472/CK0473 (MW-005 `rpm > 600` as running) from Ford's monitor
  entry (S037). This row CONTRADICTS the same 600 boundary from the regulator's idle band (S001). The regulator text
  is the stronger source, so the 23h verdicts read better as PARTLY. They stay as written (accepted rows are not
  edited); the ruling row weighs both. Score −3.
- **L2 (Low):** the LTFT verdicts rest on one TRADE text (S030). Score −2.

## What this unblocks
T-AUD-24o (design ruling, measure first): non_starter expected 6, right 5. Measure rpm < 400 (and MW-005 > 400), ECT
< 10, and the LTFT band dropped, each with a liveness probe.
