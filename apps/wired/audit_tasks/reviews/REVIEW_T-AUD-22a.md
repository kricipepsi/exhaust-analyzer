# REVIEW T-AUD-22a — GASLab code-literal inventory (Windows Cowork, 2026-11-14)

**Verdict: ACCEPT, score 96.** Docs/data row: no second-model review (CLAUDE.md step 6).

## Facts (Cowork re-ran, branch `fix/T-AUD-22a`)
- Commits after `fix/T-GASA-16`: `c9ff31b` spec, `e82f870` register (`1 file changed, 196 insertions(+)`).
  `git status --porcelain`: only the note and the RESULT.
- `check_code_claims.py --group gaslab`: `CLAIMS OK group=gaslab candidates 188 covered claims 195`; classes
  ANALYSER_SPEC 17, DIAGNOSTIC_THRESHOLD 132, INTERNAL_PARAMETER 24, LEGAL_LIMIT 9, NON_DOMAIN 3, PHYSICAL_CONSTANT 7,
  RULE_OF_THUMB 2, TYPICAL_RANGE 1; `suspect 25 same_as_wiki 174`; empty citations 3.
- `seeds flagged 4 of 4`; wiki register `CLAIMS OK scope=all candidates 1168 covered claims 1693` (unchanged).
- Time 13.05 min.

## Quality sample
8 random `same_as` links: same quantity, condition and value, citation matches the linked wiki section. 25 suspects
read: 18 carry-overs (`as W…`), 7 own findings, each re-readable from the cited lines.

## Findings
- **L1 (Low):** three suspect texts cite candidate ids (`as K0087`, `K0060–K0064`) where a claim id (`GK…`) is meant.
  Readable through `candidates_gaslab.csv`. Score −4.

## Confirmed defect outside the row → new row T-GASA-FEURO
GK0078/GK0079/GK0183/GK0184, re-derived by Cowork from `resolution.py:411-415` and `rule_engine.py:400-402`: the
CAM_TIMING_RETARDED_MAP rich fallback bounds the 2500 rpm reading by the Euro legal ceilings (`200 <= hc <= hc_ceiling`,
`co_ceiling <= co <= 4.5`). For Euro 3-5 (`hc_ceiling` 200) the HC window is the single value 200 ppm; the CO floor is
a pass/fail limit, not a fault band (wiki W0703/W0704 give HC 200-600, CO 1.5-4.5 %). Registered in the gasa ledger.
