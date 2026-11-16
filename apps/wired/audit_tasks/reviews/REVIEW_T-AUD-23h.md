# REVIEW T-AUD-23h — verify 30 mechanical_wear rule values (Windows Cowork, 2026-11-16)

**Verdict: ACCEPT, score 93.** Docs/data row, so no second-model review (CLAUDE.md step 6). Hydrogen lane (high),
9.3 min (lane `.exit` 12:25:53-12:35:09 CET).

## Facts (Cowork re-ran, branch `fix/T-AUD-23h`, after promote)
- Commits after `fix/T-AUD-24m`: `9105e57` spec, `7ca1576` lane work, `3920fc5` merge. Name-status: M `verdicts.csv`;
  A the note and the RESULT. No new source; no D, no R; no `search/` left.
- `check_verdicts.py`: `VERDICTS OK` for T-AUD-23h (30) and the seven earlier scopes. Existing rows removed: `0`.
- Verdicts: PARTLY 16, CONFIRMED 10, CONTRADICTED 4. Re-derived: S037:780 (ECT 70-110 °C monitor band), S037:165
  (engine speed 600 rpm entry), S040:263 (misfire O2 about 4.0 %).

## What the verdicts say (for the ruling row)
- **CK0464 MW-003 `ect_c > 95` CONTRADICTED** (and CK0465 `> 90`, v1 description): the normal warm ECT band runs to
  110 °C (S037 Ford), so a healthy engine at 96-105 °C passes the coolant-in-chamber gate.
- **CK0487 MW-007 `nox < 80` CONTRADICTED:** idle NOx is near 0 (S028, S035). This is the same finding as T-AUD-23g.
- **CK0502 MW-009 `co < 0.15` CONTRADICTED:** see M1.
- PARTLY (16): the HC ≥ 200 / ≥ 500 oil-burning gates (the sources give a direction, not a boundary), O2 ≥ 1.5, the
  MW-008/MW-009 lambda bands, and the high-idle HC discriminators (S001 fast-idle limit 200 ppm).
- CONFIRMED (10): CO2 < 13 / < 12 (S032), rpm > 600 (S037), P0010-P0025 (S037), O2 < 4.0 misfire (S040), STFT ±10.

## Findings
- **M1 (Medium):** CK0502 is a "not rich" discriminator: MW-009 says combustion stays stoichiometric while oil cracks
  in the exhaust. A gate that passes healthy CO is by design here; it is paired with HC ≥ 500. The CONTRADICTED
  rests on Walker's 0.1-0.45 % (S023, TRADE). The lane's own S040 shows a clean late-model car at 0.02 %, and Cowork's
  knowledge agrees: a modern car with a working catalyst usually reads under 0.1 % CO at idle. PARTLY at most. The
  ruling row must not act on it. Score −5.
- **L1 (Low):** CK0465 (`> 90`) is a v1 description value next to the live CK0464. A verdict on it is harmless but
  moves nothing. Score −2.

## What this unblocks
T-AUD-24n: the family never wins a corpus verdict (0 of 4 expected). A stricter MW gate can only lower MW scores, so
the corpus cannot get worse. CK0464 → `ect_c > 110` is the only CONTRADICTED gate with a source boundary.
