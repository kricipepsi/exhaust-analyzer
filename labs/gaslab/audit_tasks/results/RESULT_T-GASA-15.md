# Result

## Status
completed

## Summary
`labs/gaslab/audit_tasks/wikiaudit/claims.csv` lists every in-scope wiki candidate as at least one classified claim:
680 of 680 non-auto `wiki/` candidates, 1171 rows (969 domain claims, 202 `NON_DOMAIN`). 107 claims carry a `suspect`
text, including all four CO 0.1–0.45 % seeds. 340 rows carry `same_as`. Nothing was verified on the web (R5). No wiki,
vocabulary, ontology or code value was edited.

Correction 1 (R6): `a6145dd` held 570 double-encoded fields on 484 lines. Commit `7696b61` repairs them by a
whole-file cp1252 round-trip and changes `claims.csv` only. `check_claims.py --scope wiki` now prints `CLAIMS OK`
(it printed `CLAIMS FAIL 570 error(s)` before), and step 4 confirms the content is unchanged.

## Files changed
- `repo/labs/gaslab/audit_tasks/wikiaudit/claims.csv` (created `a6145dd`; encoding repaired `7696b61`)
- `repo/labs/gaslab/audit_tasks/progress_notes/T-GASA-15.md` (untracked; correction 1 sections appended, 91 mojibake
  lines in the earlier sections repaired the same way)
- `repo/labs/gaslab/audit_tasks/results/RESULT_T-GASA-15.md` (this file, untracked, rewritten)
- `candidates.csv`: not changed (no diff).

## Commands executed
- First action (as specified): `fix/T-GASA-15`; log `7387acd`, `a6145dd`, `9cc058d`; `CLAIMS FAIL 570 error(s)`.
  Preconditions: `checked`.
- Dry run: `git show a6145dd:./claims.csv` → `.encode('cp1252').decode('utf-8')`: whole file succeeds, 484 lines
  differ, line count kept.
- Repair: the same transform written to `claims.csv` with `newline=''`; `git add` of that path; a separate
  `git -C C:/4DApp/repo … commit` → `7696b61`.
- Verification steps 1–4 (output below).

## Validation evidence
```
# 1.
classes ANALYSER_SPEC=19 DIAGNOSTIC_THRESHOLD=625 INTERNAL_PARAMETER=94 LEGAL_LIMIT=18 NON_DOMAIN=202 PHYSICAL_CONSTANT=58 RULE_OF_THUMB=69 TYPICAL_RANGE=86
suspect 107
CLAIMS OK scope=wiki candidates 680 covered claims 1171
exit 0
# 2.
seeds flagged 4 of 4
# 3.
7696b61 fix(T-GASA-15): repair double-encoded UTF-8 in claims.csv (R6; 484 lines, content unchanged)
7387acd spec(T-GASA-15): correction 1 — claims.csv encoding (R6); checker rejects double-encoded fields
a6145dd docs(T-GASA-15): WIKIAUDIT claim inventory of the 14 wiki files (680 candidates, 1171 claims, 107 suspect)
9cc058d spec(T-GASA-15): WIKIAUDIT claim inventory of the wiki; register tools and candidates
 1 file changed, 484 insertions(+), 484 deletions(-)
?? labs/gaslab/audit_tasks/progress_notes/
?? labs/gaslab/audit_tasks/results/
# 4.
content equal after decode: True
```
The previous decisive failure (`CLAIMS FAIL 570 error(s)`) is gone, and step 1 prints no `ERROR` line.
`git diff --name-only HEAD~1 HEAD` = `labs/gaslab/audit_tasks/wikiaudit/claims.csv`.

## Criteria
| # | verdict | evidence |
|---|---|---|
| 1 | MET | step 1: `CLAIMS OK scope=wiki candidates 680 covered claims 1171`, 680 = P1 wiki count, no `ERROR` |
| 2 | MET | step 2: `seeds flagged 4 of 4` |
| 3 | MET | note § Step 1 disclosure and § VERIFICATION GATE (correction 1) give the `classes` and `suspect 107` lines; § Suspect claims lists all 107 with reasons (now in correct UTF-8) |
| 4 | MET | step 3: `a6145dd` plus one repair commit `7696b61` after the spec commits; `1 file changed`, claims.csv only |
| 5 | MET | step 4: `content equal after decode: True` |

## Decisions the task did not specify
- First dispatch decisions: see the note § Decisions the task did not specify (class choices, `same_as` on exact matches
  only, condition-only 2500 rpm folded into `condition`, word numbers not claimed, unitless NOx 20–60 taken as ppm, no
  R2 additions, scratch tools kept in the note).
- Correction 1: the repair is one whole-file transform (`cp1252` encode, `utf-8` decode), which is exactly the inverse
  that step 4 checks. No field was edited by hand.
- Correction 1: the note's own mojibake (91 lines, copied from the bad file) was repaired with the same transform per
  line. The note is in my write scope and holds no claim data of record.

## Pre-existing changes preserved
The clone was clean at the start apart from the untracked note and RESULT from the first dispatch. The `C:/4DApp`
workspace changes (LOOP_STATE.md, launchers, handoff) were not touched.

## Rollback
`git -C C:/4DApp/repo revert 7696b61` (or `git -C C:/4DApp/repo reset --hard 7387acd` on `fix/T-GASA-15` only)
undoes the repair. Delete the untracked note and RESULT to undo them.

## Remaining risks or uncertainties
- Classification and suspect texts are bounded judgement from domain knowledge without web checks (R5). The
  verification rows decide each value.
- `same_as` misses repeats whose wording differs (empty, not wrong).
- `suspect` cites UK MOT and Euro-standard facts from memory: Euro 5 dates, Euro 3 start, MOT idle/fast-idle split, the
  Brettschneider defaults, TWC light-off temperature. These are the first items the verification rows should source.

## Time
| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| first dispatch total | 2026-11-14T07:59:57Z | 2026-11-14T08:21:33Z | 21.6 | ABSENT |
| correction 1: first action → repair, commit, verification | 2026-11-14T08:25:03Z | 2026-11-14T08:26:11Z | 1.1 | ABSENT |
| note and RESULT | 2026-11-14T08:26:11Z | 2026-11-14T08:27:03Z | 0.9 | ABSENT |
| correction 1 total | 2026-11-14T08:25:03Z | 2026-11-14T08:27:03Z | 2.0 | ABSENT |

## Branch and log
```
$ git -C repo branch --show-current
fix/T-GASA-15
$ git -C repo log --oneline fix/T-GASA-14..HEAD
7696b61 fix(T-GASA-15): repair double-encoded UTF-8 in claims.csv (R6; 484 lines, content unchanged)
7387acd spec(T-GASA-15): correction 1 — claims.csv encoding (R6); checker rejects double-encoded fields
a6145dd docs(T-GASA-15): WIKIAUDIT claim inventory of the 14 wiki files (680 candidates, 1171 claims, 107 suspect)
9cc058d spec(T-GASA-15): WIKIAUDIT claim inventory of the wiki; register tools and candidates
```
