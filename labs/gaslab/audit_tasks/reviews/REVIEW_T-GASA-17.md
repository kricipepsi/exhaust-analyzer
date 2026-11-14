# REVIEW T-GASA-17 — verify legal-limit and CO 0.45 roots (Windows Cowork, 2026-11-14)

**Verdict: ACCEPT, score 98.** Docs/data row: no second-model review (CLAUDE.md step 6).

## Facts (Cowork re-ran, branch `fix/T-GASA-17`)
- Commits after `fix/T-AUD-22a`: `527680e` spec, `9df583d` verdicts. Changed names: `sources.csv`, `verdicts.csv`,
  8 × `sources/S*.md` only. `git status --porcelain`: only the note and the RESULT.
- `check_verdicts.py --scope scope/T-GASA-17.txt`: `verdicts CITATION_WRONG=1 CONFIRMED=7 CONTRADICTED=5 PARTLY=7`;
  `sources 8 primary 8`; `VERDICTS OK scope=T-GASA-17.txt claims 20`. Both registers unchanged (`1693`, `195`).
- Time 10 min. Sources 1.3 MB (S009, the DVSA 19th-edition PDF text, 872 kB).

## Re-derivation (Cowork read the source lines)
- S005 (91/441/EEC) 5.3.2.2: idle CO "must not exceed 3.5 % at the setting used for the type I test and must not exceed
  4.5 % within the range of adjustments" → W0124 PARTLY holds.
- S009 tables: 1200 ppm HC only for non-cat cars first used before 1/8/95 (lines 434-436, 462-463) → W0126
  CONTRADICTED holds.
- S007 Art. 10(3) "With effect from 1 January 2011" → W0133 PARTLY holds.
- S001 / S002: idle CO 0.3 %, high idle 0.2 % (from 1/9/2002) → W0129, W0131, W0185, W1303 CONTRADICTED hold.
- Disputes (note § Disputes) ruled correctly: 0.45 % is legal only for cat cars first used 1995-2002 (0.5 % band); the
  wiki's stated baseline is Euro 4, in the 0.3 % band.

## Findings
- **L1 (Low):** S009 at 872 kB is large for the app repo; a trimmed extract would serve. Not a defect of the spec.
  Score −2.

## What this unblocks
- **T-GASA-F45**: CO normal-with-cat maximum and `co_tier_max` 0.45 → 0.3 (W0185, W1303 CONTRADICTED; W1083's lower
  edge with it). Corpus impact measured 2026-11-13: 0 of 314.
- **T-GASA-FEURO**: `_EURO_THRESHOLDS` is a mislabelled table: Euro 1 4.5 (PARTLY), Euro 2 HC 1200 (CONTRADICTED),
  Euro 4/5 idle CO 0.2 (CONTRADICTED, fast-idle value). UK limits band by date of first use, not Euro class.
- W0118: re-cite 40 CFR 85.2215 in place of SAE J1667 (docs fix).
