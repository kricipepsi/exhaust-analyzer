# Result

## Status
completed

## Summary
`apps/wired/audit_tasks/codeaudit/claims_gaslab.csv` lists every numeric literal in `labs/gaslab/gaslab/*.py` that
`candidates_gaslab.csv` marks for classification: 195 claims (`GK0001`-`GK0195`) over the 188 non-auto candidates.
Each claim carries the citation the code gives. 174 claims link by `same_as` to the wiki-register claim they copy.
25 are `suspect`: 6 are own findings where the code value differs from the cited register claim, 4 are the R5 seeds,
and 15 inherit a suspect register claim. Nothing was verified on the web, and no code, ontology, wiki or register file
was edited. A full list of suspects, stale citations and the other findings is in the progress note.

Time: first action → verification after commit, 2026-11-14T09:00:14Z → 2026-11-14T09:13:17Z, 13.05 min, context ABSENT
(no meter exposed). The RESULT was written at 09:14:45Z.

## Files changed
- `repo/apps/wired/audit_tasks/codeaudit/claims_gaslab.csv`: CREATE, committed `e82f870`.
- `repo/apps/wired/audit_tasks/progress_notes/T-AUD-22a.md`: CREATE, untracked.
- `repo/apps/wired/audit_tasks/results/RESULT_T-AUD-22a.md`: CREATE, untracked.
- `repo/apps/wired/audit_tasks/codeaudit/candidates_gaslab.csv`: re-written byte-identical by the first action (no diff).

## Commands executed
- First action (exact task block) and the Preconditions loop.
- Read-only inspection: `check_code_claims.py`, both READMEs, the cited code regions (`sed -n`), and wiki headings
  (`grep -n "^#"`). Register claims were read by section with `awk` over a dump of `wikiaudit/claims.csv`.
- CSV build: the spec was written to `claims_gaslab.csv`, then rewritten in place by a stdin Python script (it copies the
  class from the linked claim, extracts citations from the line comment, adds `as W<id>` for suspect links and numbers
  the claims in candidates order).
- `git add apps/wired/audit_tasks/codeaudit/claims_gaslab.csv`, then
  `git -c user.name=Claude -c user.email=noreply@anthropic.com commit -m "docs(T-AUD-22a): …"`.
- `### Verification ###` steps 1-4, exact.

## Validation evidence
```
# 1.
classes ANALYSER_SPEC=17 DIAGNOSTIC_THRESHOLD=132 INTERNAL_PARAMETER=24 LEGAL_LIMIT=9 NON_DOMAIN=3 PHYSICAL_CONSTANT=7 RULE_OF_THUMB=2 TYPICAL_RANGE=1
suspect 25 same_as_wiki 174
CLAIMS OK group=gaslab candidates 188 covered claims 195
# 2.
seeds flagged 4 of 4
# 3.
CLAIMS OK scope=all candidates 1168 covered claims 1693
# 4.
e82f870 docs(T-AUD-22a): GASLab code-literal register claims_gaslab.csv (188 candidates, 195 claims)
c9ff31b spec(T-AUD-22a): code-literal register tools; GASLab code inventory
 1 file changed, 196 insertions(+)
?? apps/wired/audit_tasks/progress_notes/T-AUD-22a.md
```
The full step-1 run has 0 `ERROR` lines (`| grep -c ERROR` → 0). P2's previous decisive failure, `CLAIMS FAIL 188
error(s)` (all uncovered), is absent. The RESULT was written after step 4, so it is now untracked too.

Branch and log:
```
$ git -C repo branch --show-current
fix/T-AUD-22a
$ git -C repo log --oneline fix/T-GASA-16..HEAD
e82f870 docs(T-AUD-22a): GASLab code-literal register claims_gaslab.csv (188 candidates, 195 claims)
c9ff31b spec(T-AUD-22a): code-literal register tools; GASLab code inventory
```

## Criteria
| # | status | evidence |
|---|---|---|
| 1 | MET | step 1: `CLAIMS OK group=gaslab candidates 188 covered claims 195`, 0 `ERROR` lines |
| 2 | MET | step 2: `seeds flagged 4 of 4` |
| 3 | MET | step 3: `CLAIMS OK scope=all candidates 1168 covered claims 1693` (P3 unchanged) |
| 4 | MET | note § Step 1 figures (classes, `suspect 25`, `same_as_wiki 174`, empty citation 6 of 195) and § Suspect claims (all 25 with reasons) |
| 5 | MET | step 4: one commit `e82f870` after spec `c9ff31b`, `1 file changed` = `claims_gaslab.csv` |

## Decisions the task did not specify
1. **Stale citations** (`GAS_WIKI §6.1/§6.2/§7.7/§4.4/§8.4-§8.7`, `GASWIKI-05 §7.14/§7.15`): no `GAS_WIKI` document
   exists, and the v2 sections with those numbers are missing or hold other topics. The citation is copied as written;
   `same_as` takes R4's no-citation branch (the first matching register claim). The reason: a link to an unrelated
   section would be false.
2. **Band edges**: a code literal that is one edge of a cited band links to that band claim (for example 100 → W1290
   `35 – 100`, 0.45 → W1298 `0.1 – 0.45`). `<` against `≤` on the same number counts as the same value.
3. **Citation for comment-less lines** inside a multi-line condition: the comment of the first line of that condition,
   else the nearest enclosing comment that names a document (see note, assumption 3).
4. **Class of a linked claim** is copied from the register claim, so one verdict covers both.
5. **Operationalised qualitative values** (wiki "→ 1.0", "≈ 0", "~ unchanged", "λ mismatch" turned into numeric
   windows) get no `same_as` and no `suspect`: they do not contradict the wiki, and the note lists them.
6. **Inherited suspect text** is `as W<id>` naming the directly linked claim (as the register does), with the own
   reason after a colon where there is one.

## Pre-existing changes preserved
The baseline `git status --porcelain` in `repo/` was empty. The `C:/4DApp` master working-tree changes
(`LOOP_STATE.md`, launch scripts, handoff) were not touched.

## Rollback
On the task branch only: `git -C C:/4DApp/repo revert e82f870`. The note and RESULT are untracked files and can be
removed separately.

## Remaining risks or uncertainties
- Link judgement: 174 `same_as` links were chosen by hand under decisions 1-2. A different reading of "the claim the
  citation points to" would re-point some links (mostly the defaults in `rule_engine.py` toward the ontology rows
  W1445-W1473 instead of the first wiki-04 rows). This is detectable and fixable from the CSV alone.
- Own-finding suspects (K0087/K0193 HC window collapse to 200 ppm for Euro 3-5; K0088/K0194 CO lower bound; K0100;
  K0103) are logic and value findings for the verification and fix rows. They are not verified here.
- Scratch dumps were left in `C:/4DApp/recheck/T-AUD-22a/`, outside the clone (note, assumption 6).
