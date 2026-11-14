# REVIEW T-GASA-15 — WIKIAUDIT claim inventory of the wiki (Windows Cowork, 2026-11-14)

**Verdict: ACCEPT, score 92.** Docs/data row: no second-model review (CLAUDE.md step 6).

## Facts (Cowork re-ran, branch `fix/T-GASA-15`)
- Commits on the branch after `fix/T-GASA-14`: `9cc058d` spec, `a6145dd` inventory, `7387acd` correction 1, `7696b61`
  repair. `git status --porcelain`: only the note and the RESULT.
- `check_claims.py --scope wiki` (with the correction 1 encoding check): `CLAIMS OK scope=wiki candidates 680 covered
  claims 1171`; classes ANALYSER_SPEC 19, DIAGNOSTIC_THRESHOLD 625, INTERNAL_PARAMETER 94, LEGAL_LIMIT 18,
  NON_DOMAIN 202, PHYSICAL_CONSTANT 58, RULE_OF_THUMB 69, TYPICAL_RANGE 86; suspect 107.
- Seeds: `seeds flagged 4 of 4`. Repair: `content equal after decode: True`; `484 insertions(+), 484 deletions(-)`.
- Time: build 21.6 min (note `## Time`); correction about 3 min.

## Quality sample
25 random domain claims, 12 NON_DOMAIN rows and all 18 LEGAL_LIMIT rows read against the line text: class, quantity,
value and condition right in each. Suspects add real leads beyond the seed: wiki 02's Euro table (Euro 1 "CO 4.5 % idle
with cat", Euro 2 "HC 1200 ppm" — pre-cat MOT and type-approval figures mixed), Euro 4/5 idle CO 0.2 % (the fast-idle
limit), the J1667 citation on the high-idle band (a diesel smoke procedure).

## Findings
- **F1 (Medium, corrected): 570 fields on 484 lines double-encoded** in `a6145dd`. Author gap shared: the checker had no
  encoding check. Correction 1 added it (fails `a6145dd`, passes `7696b61`). Score −8.

## Residual
None for this row. T-GASA-16 (vocab + ontology inventory) continues the W ids from `W1172`.
