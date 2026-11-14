# T-GASA-16 — authoring sidecar (Windows Cowork, 2026-11-14)

Input: T-GASA-WIKIAUDIT umbrella; T-GASA-15 accepted (`REVIEW_T-GASA-15.md`). Same register and checker.

### Verified context ###
1. **488 non-auto candidates are outside `wiki/`: 234 vocabulary, 254 ontology.** Observed (`candidates.csv` count).
2. **The CO 0.45 maximum sits at C1021 (vocab:367 `normal_with_cat: { min: 0.1, max: 0.45 }`), C1222 (ontology:44
   `co_tier_max: 0.45`), C1255 (ontology:98 NORMAL `co: { min: 0.1, max: 0.45 }`).** Observed (grep of `candidates.csv`).
3. **On `e4967bd`: wiki scope `CLAIMS OK … 1171`; vocab_ontology scope `CLAIMS FAIL 488 error(s)`; last id `W1171`;
   the prefix-equality check prints `wiki rows unchanged: True` (1172 lines with header).** Observed.
4. **`check_claims.py` counts a scope's claims by `file`, so appended rows leave the wiki line unchanged.** Observed
   (code read: `in_scope`).

### Rulings and the tradeoff that lost ###
- **`same_as` to the first wiki claim; a differing value gets a suspect, not a link.** That is the drift the operator
  cares about: the ontology runs. Lost: linking by quantity only (would hide a changed value).
- **Wiki suspects carry over as `as W<id>`**, so the verification rows see one reason per value.
- Difficulty 3, Opus 5.5 medium. Survey = facts 1-4. Plan NONE. Docs row: no second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | DEFERRED | `CLAIMS OK scope=vocab_ontology candidates 488`; pre-state `CLAIMS FAIL 488 error(s)` (P3) |
| step 2 | RAN | `CLAIMS OK scope=wiki candidates 680 covered claims 1171`; `wiki rows unchanged: True` on the base |
| step 3 | DEFERRED | `seeds flagged 3 of 3`; pre-state 0 of 3 (no rows for those candidates) |
| step 4 | DEFERRED | the spec commit plus one commit, `1 file changed` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-GASA-16: vocab + ontology 488 lines classified, same_as linked to wiki claims; CLAIMS OK both scopes.

### Cold read ###
own pass 2026-11-14: seeds C1021/C1222/C1255 hold 0.45 · closed sets: R2 scope = non-auto vocab + ontology rows; R4 same_as range W0001-W1171; R5 suspect set · counts 488 = P1 = P3 · steps 2 RAN on base · traceability criteria 1-5 → steps 1-4 and the note · no finding.
cold read 2026-11-14 FOCUSED reader; trigger grep hit (R2-R5); 0 findings — 6 calls

### Correction history ###
(none)
