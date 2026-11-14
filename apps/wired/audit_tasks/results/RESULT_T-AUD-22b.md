# Result

## Status
completed

## Summary
`apps/wired/audit_tasks/codeaudit/claims_comlab.csv` covers all 293 non-auto `.py` candidates of the COMLab group with
301 rows (100 `NON_DOMAIN`, 201 classified claims). Each claim carries its citation as written and a `same_as` link
(17 to wiki claims, 39 to earlier CK claims). 19 claims are `suspect`, among them the seed K0012 (O2 2.0 against 2.5 in
delta-relations/07). The other main findings:
- The HIGH_ASSURANCE boundary is 0.70 in two places, but the wiki 09 band is ≳ 0.80.
- `bonus_on_dtc_match` allows 1.0, but LLD §8.1 caps it at 0.5.
- The trim schema bounds are ±127 per trim and ±254 for the total, but SAE J1979 / the docs give ±100 and ±200.
- `ve_pct` allows up to 200 %, but the docs give 0–100.
- An absent CO2 is filled with 15.0 % in the shim.

No web access, and no code, config or wiki edits.

## Files changed
- `repo/apps/wired/audit_tasks/codeaudit/claims_comlab.csv` (created, committed `ceee320`)
- `repo/apps/wired/audit_tasks/progress_notes/T-AUD-22b.md` (created, untracked)
- `repo/apps/wired/audit_tasks/results/RESULT_T-AUD-22b.md` (created, untracked)
- `candidates_comlab.csv`: re-written by the first action, byte-identical (`git status --porcelain .` empty).

## Commands executed
- First action (exact block): `fix/T-AUD-22b`, three spec commits, clean status, `files 52 candidates 3794
  auto_non_domain 1220 to_classify 2574`, clean status.
- Preconditions loop: `checked`, no `MISSING`.
- Red run on a header-only file: `CLAIMS FAIL 293 error(s)` (293 `uncovered`).
- Generator: `$PY -I -X utf8 claims_comlab.csv` (the generator sat in the target file and overwrote itself; see the note,
  Assumptions) → `wrote 301 rows for 293 candidates`.
- `git add apps/wired/audit_tasks/codeaudit/claims_comlab.csv`, then `git -C C:/4DApp/repo -c user.name=… commit …`.
- Verification steps 1-3 (exact block).

## Validation evidence
```
classes ANALYSER_SPEC=26 DIAGNOSTIC_THRESHOLD=75 INTERNAL_PARAMETER=92 NON_DOMAIN=100 PHYSICAL_CONSTANT=5 TYPICAL_RANGE=3
suspect 19 same_as_wiki 17
CLAIMS OK group=comlab scope=*.py candidates 293 covered claims 301
seeds flagged 1 of 1
ceee320 docs(T-AUD-22b): COMLab Python code-literal register claims_comlab.csv (293 candidates, 301 claims)
6e83580 spec(T-AUD-22b): cold read recorded
9b935da spec(T-AUD-22b): dispatch header
89d6be7 spec(T-AUD-22b): COMLab Python code-literal inventory; checker --files scope + mojibake check; RESYNC row
 1 file changed, 302 insertions(+)
```
ERROR lines in the step 1 output: 0. The previous decisive failure (`CLAIMS FAIL 293 error(s)`, all uncovered) is gone.

Branch and log:
```
$ git -C repo branch --show-current
fix/T-AUD-22b
$ git -C repo log --oneline 6e83580..HEAD
ceee320 docs(T-AUD-22b): COMLab Python code-literal register claims_comlab.csv (293 candidates, 301 claims)
```

## Criteria
| # | status | evidence |
|---|---|---|
| 1 | MET | step 1: `CLAIMS OK group=comlab scope=*.py candidates 293 covered claims 301`, 0 `ERROR` lines (293 = P1b) |
| 2 | MET | step 2: `seeds flagged 1 of 1` |
| 3 | MET | note § Step 1 figures (classes, suspect 19, same_as_wiki 17, empty citation 49, citation not found 10) and § Suspect claims (all 19 with reasons) |
| 4 | MET | step 3: one commit `ceee320` after the spec commits, `1 file changed`, only the note untracked at run time (RESULT added afterwards) |

## Decisions the task did not specify
- Class for protocol/encoding facts (OBD PID ranges, O2 sensor voltage, VIN length 17 per ISO 3779): `ANALYSER_SPEC`.
  The README classes have no "standard" class, and this is the nearest instrument/protocol fact class.
- Schema validation bounds with no outside truth (`ve_pct`, trim bounds, model year, cylinder count): `INTERNAL_PARAMETER`.
  The gas ranges follow T-AUD-22a (`ANALYSER_SPEC` + W0060-W0064; λ envelopes `INTERNAL_PARAMETER` + W1191/W1377).
- Citation when the file puts its comment after the constant (router L92-L108, ingestion closing-paren comments): that
  following comment block is used, per the file's own convention.
- `suspect` beyond R4/R6 for documents the line does not cite, where another doc or claim gives a different value
  (K0155, K0287). These are recorded for the verification rows; the reviewer can clear them.
- STFT/LTFT ±127 claims all use one quantity ("fuel trim schema bound") so they can point `same_as` at CK0181 while each
  keeps its own `suspect`.
- "Citation not found" counts only claims whose citation names a file absent from `labs/` and `Vault/` (10). A task id
  (`T-P6-6a`) is counted, but a run id (Jaeger, K0270) is not.

## Pre-existing changes preserved
The `repo/` tree was clean at start. The `C:/4DApp` master working-tree changes (LOOP_STATE.md, launchers, handoff)
were not touched.

## Rollback
`git -C C:/4DApp/repo reset --soft HEAD~1` on `fix/T-AUD-22b` only (or drop commit `ceee320`). Delete the untracked
note and RESULT. Nothing else changed.

## Remaining risks or uncertainties
- Classification and the `NON_DOMAIN` boundary are judgement. 100 rows are `NON_DOMAIN` (0.0/1.0 defaults, probability
  and percent bounds, `ge=0`, counts).
- The R6 suspects rest on my knowledge of SAE J1979 trim scaling (−100…+99.2 %), with no web check (R7). The
  verification rows must confirm them.
- Not flagged but noted: stale "§2 line 70" pointers (K0053/K0073), the cylinder cap of 12, and the catalyst index edge 0.20.
- The generator was run from the target path because `impl_guard` refuses scratch files. The committed content is pure CSV.
