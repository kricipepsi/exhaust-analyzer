# T-AUD-22a — authoring sidecar (Windows Cowork, 2026-11-14)

Input: ledger row T-AUD-22 (operator order 2026-11-13); wiki register accepted in T-GASA-15/16. Draft tools rehearsed
in `C:/4DApp/recheck/T-AUD-22/`.

### Verified context ###
1. **Production numeric literals (ast, tests/tasks/graph/docs excluded): gaslab 205 lines (188 to classify, 9 files),
   comlab 3794 (2574), rest 789 (551).** VINLab excluded (parked). Observed (`extract_code_candidates.py`).
2. **Seeds: K0099 `resolution.py:448` `reading_high.co <= 0.45`; K0184 `rule_engine.py:370` `co_tier_max` default 0.45;
   K0060/K0061 `_EURO_THRESHOLDS` Euro 1 `(4.5, None)`, Euro 2 `(0.5, 1200)` citing `GASWIKI-02 §2.8`** — the wiki rows
   T-GASA-15 flagged (W0124, W0126). Observed (grep of the candidates).
3. **Header-only claims file: `CLAIMS FAIL 188 error(s)`; wiki register `CLAIMS OK scope=all candidates 1168 covered
   claims 1693`.** Observed.

### Rulings and the tradeoff that lost ###
- **Branch from `fix/T-GASA-16`, not `audit-r2`** (the audit ledger's branch rule): the row links to the wiki register,
  which exists only on the gasa chain. Lost: the pack's rule (the register would be missing).
- **One inventory slice per lab group; GASLab first** (smallest, and its values are the operator's seed). COMLab 2574
  lines will split again (rules / kg / config+code). Lost: one cross-lab row (past a session).
- **Line-level candidates for code too**, so the verification rows treat both registers the same way.
- Difficulty 3, Opus 5.5 medium. Survey = facts 1-3. Plan NONE. Docs row: no second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | DEFERRED | `CLAIMS OK group=gaslab candidates 188`; pre-state `CLAIMS FAIL 188 error(s)` (P2) |
| step 2 | DEFERRED | `seeds flagged 4 of 4`; pre-state: no claims file, the command raises |
| step 3 | RAN | `CLAIMS OK scope=all candidates 1168 covered claims 1693` |
| step 4 | DEFERRED | the spec commit plus one commit, `1 file changed` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-22a: GASLab code literals (188 lines) classified, cited and linked to the wiki register; CLAIMS OK.

### Cold read ###
own pass 2026-11-14: seeds K0099/K0184/K0060/K0061 hold 0.45/0.45/4.5/1200 · closed sets: R2 scope = non-auto candidates_gaslab rows; R4 same_as range W0001-W1693; R5 suspect set · counts 188 = P1 to_classify = P2 · step 3 RAN · traceability criteria 1-5 → steps 1-4 and the note · no finding.
cold read 2026-11-14 FOCUSED reader; trigger grep hit (R2-R5); 0 findings, 1 UNSETTLED (criterion 1 "P1 count" names two numbers) patched as wording (P1 to_classify); cold read of the patch skipped, patch is wording — 3 calls

### Correction history ###
(none)
