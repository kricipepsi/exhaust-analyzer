# REVIEW T-GASA-16 — WIKIAUDIT vocab + ontology claim inventory (Windows Cowork, 2026-11-14)

**Verdict: ACCEPT, score 97.** Docs/data row: no second-model review (CLAUDE.md step 6).

## Facts (Cowork re-ran, branch `fix/T-GASA-16`)
- Commits after `fix/T-GASA-15`: `d7244d9` spec, `f756425` inventory (`1 file changed, 522 insertions(+)`).
  `git status --porcelain`: only the note and the RESULT.
- `check_claims.py --scope vocab_ontology`: `CLAIMS OK scope=vocab_ontology candidates 488 covered claims 522`; classes
  ANALYSER_SPEC 17, DIAGNOSTIC_THRESHOLD 273, INTERNAL_PARAMETER 73, LEGAL_LIMIT 4, NON_DOMAIN 91, PHYSICAL_CONSTANT 23,
  RULE_OF_THUMB 11, TYPICAL_RANGE 30; suspect 72.
- Wiki scope still `CLAIMS OK … 1171`; `wiki rows unchanged: True`; `seeds flagged 3 of 3`. Time 26.0 min.

## Quality sample
- `same_as`: 244 of 431 domain claims linked. 10 random links read: all the same quantity and condition; two equate a
  `≥` with a `>` at the same number (W1302/W0191, W1335/W1243): accepted, the verification checks the number.
- The suspects that are not carry-overs (about 50) are the row's main result: **the ontology fault boxes that the code
  loads differ from the wiki's own gas vectors for many faults** (e.g. ontology:251-256 HC 0-100 / O2 0-0.5 against wiki
  HC 300-800 / O2 1.5-3.5; ontology:239-244; 381-386; 410-412), plus vocab-internal contradictions (triangle band
  W1253 vs W1326; rule priority W1396 vs W0303) and a stale fault count (W1432: 32, ontology holds 34).

## Findings
- **L1 (Low, not a defect of this row):** `≥`/`>` links. Score −3 for the nit only because the verification rows must
  read the comparator from the line.

## Residual for the verification rows
The ontology-versus-wiki divergences need a source to decide which side is right; they feed T-GASA-F4/F45 and new fix
rows. The register now holds `W0001`-`W1693` (179 suspect).
