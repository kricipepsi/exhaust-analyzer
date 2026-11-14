# T-GASA-17 — authoring sidecar (Windows Cowork, 2026-11-14)

Input: T-GASA-WIKIAUDIT and T-AUD-22 umbrellas; registers accepted in T-GASA-15, T-GASA-16, T-AUD-22a.

### Verified context ###
1. **The 31 `LEGAL_LIMIT` claims (wiki 18, vocab/ontology 4, code 9) and the 14 suspect CO `0.45` claims resolve
   through `same_as` to 20 roots** (W0118, W0119, W0124-W0133, W0185, W1027, W1083, W1109-W1112, W1303). Observed
   (same_as walk over both registers).
2. **firecrawl works from Git Bash with the key read inside the command**: the MOT manual section 8 scrape returned
   598 lines with `CO up to 0.3% at idle (450rpm to 1,500rpm)` at line 271. Observed (`recheck/.firecrawl/t17/mot8.md`).
3. **`check_verdicts.py` rejects** an unknown source kind, a non-http url, a missing fetched file, a duplicate verdict,
   a quote absent from its file, a CONTRADICTED with no source value, an UNSOURCED with no note, an unknown verdict,
   and every scope claim with no verdict; it accepts the real MOT quote. Observed (crafted rows, removed).
4. **Header-only CSVs: `VERDICTS FAIL 20 error(s)`.** Observed.
5. **The implementer settings deny WebFetch and WebSearch only; Bash may run the firecrawl CLI.** Observed
   (`.claude/roles/implementer.settings.json` deny list).

### Rulings and the tradeoff that lost ###
- **Legal limits first** (20 roots): they decide T-GASA-F45 and T-GASA-FEURO, the operator's own seed. Lost: the
  COMLab code inventory first (completeness before evidence; it can follow).
- **Quotes are machine-checked against committed fetched files.** Lost: URL-only citations (unverifiable at review).
- **Fetched files live in the repo** (`wikiaudit/sources/`), so the fix rows cite them. Lost: `recheck/.firecrawl/`
  (git-ignored).
- Difficulty 3 (bounded research, quotes checked). Opus 5.5 medium. Survey = facts 1-5. Plan NONE. Docs row: no
  second-model review; Cowork re-reads every CONTRADICTED and PARTLY quote at review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | DEFERRED | `VERDICTS OK scope=T-GASA-17.txt claims 20`; pre-state `VERDICTS FAIL 20 error(s)` (P2) |
| step 2 | RAN | `CLAIMS OK scope=all candidates 1168 covered claims 1693`; `CLAIMS OK group=gaslab candidates 188 covered claims 195` |
| step 3 | DEFERRED | the spec commit plus one commit touching only the three named paths |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-GASA-17: 20 legal-limit and CO-0.45 roots verified against fetched primary sources; VERDICTS OK.

### Cold read ###
own pass 2026-11-14: scope file 20 ids = P1 roots · MOT quote present (fact 2) · closed sets: R3 cited-source set; R4 root ids = scope file · traceability criteria 1-4 → steps 1-3 and the note · no finding.
cold read 2026-11-14 FOCUSED reader; trigger grep hit (R3, R4); 0 findings — 4 calls

### Correction history ###
(none)
