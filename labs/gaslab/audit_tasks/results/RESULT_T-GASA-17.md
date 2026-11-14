# Result

## Status
completed

## Summary
Each of the 20 root claims in `wikiaudit/scope/T-GASA-17.txt` has one verdict. Each verdict quotes a source file
fetched with firecrawl, and all 8 sources are primary. Verdicts: CONFIRMED 7, CONTRADICTED 5, PARTLY 7,
CITATION_WRONG 1, UNSOURCED 0. The CO "normal with cat" maximum of 0.45 % (W0185, and its tier copy W1303) is
CONTRADICTED by the 0.3 % legal idle limit (gov.uk MOT manual §8; DVSA In-Service Emission Standards). Most of the wiki's
Euro ceiling table holds UK in-service (MOT) values with Euro or type-approval labels. Euro 4 idle 0.2 % is the
fast-idle value, and the true idle limit is 0.3 %. Euro 2 HC 1200 ppm is CONTRADICTED by 200 ppm. Euro 5 2009–2010 is
PARTLY, because all new cars came under Euro 5 from 1 Jan 2011. The UK MOT table in wiki 11 §11.2.3 is CONFIRMED
(4 of 4). The verdict table and the Disputes list are in `progress_notes/T-GASA-17.md`.

## Files changed
- `repo/labs/gaslab/audit_tasks/wikiaudit/sources.csv` (8 rows: S001, S002, S004, S005, S007, S008, S009, S011)
- `repo/labs/gaslab/audit_tasks/wikiaudit/verdicts.csv` (20 rows)
- `repo/labs/gaslab/audit_tasks/wikiaudit/sources/S001.md`, `S002.md`, `S004.md`, `S005.md`, `S007.md`, `S008.md`,
  `S009.md`, `S011.md` (firecrawl `-o` output)
- `repo/labs/gaslab/audit_tasks/progress_notes/T-GASA-17.md` (untracked, created)
- `repo/labs/gaslab/audit_tasks/results/RESULT_T-GASA-17.md` (untracked, this file)
- Runtime only, outside the clone: `C:/4DApp/recheck/.firecrawl/T-GASA-17/` (2 search JSONs, 5 uncited scrapes)

## Commands executed
- First action and Preconditions (as written in the task).
- `firecrawl scrape "<url>" -o labs/gaslab/audit_tasks/wikiaudit/sources/S<NNN>.md` for each source, with the key
  exported inside the same command (R2). It was run singly or through `xargs -P 2`.
- `firecrawl search "…" -o C:/4DApp/recheck/.firecrawl/T-GASA-17/<name>.json --json` (2 searches, listed in the note).
- Verification steps 1–3 (as written in the task).
- `git add <3 paths>`; `git -c user.name=Claude -c user.email=noreply@anthropic.com commit -m "audit(T-GASA-17): …"`.

## Validation evidence
```
verdicts CITATION_WRONG=1 CONFIRMED=7 CONTRADICTED=5 PARTLY=7
sources 8 primary 8
VERDICTS OK scope=T-GASA-17.txt claims 20
CLAIMS OK scope=all candidates 1168 covered claims 1693
CLAIMS OK group=gaslab candidates 188 covered claims 195
9df583d audit(T-GASA-17): verdicts for 20 legal-limit and CO 0.45 roots; 8 primary sources
527680e spec(T-GASA-17): verify legal-limit and CO 0.45 roots; verdict checker and format
      1 labs/gaslab/audit_tasks/wikiaudit/sources.csv
      8 labs/gaslab/audit_tasks/wikiaudit/sources/S*.md
      1 labs/gaslab/audit_tasks/wikiaudit/verdicts.csv
?? labs/gaslab/audit_tasks/progress_notes/T-GASA-17.md
```
Step 1 prints no `ERROR` line. The previous decisive failure, `VERDICTS FAIL 20 error(s)` (P2, seen at First action),
is gone.

Branch and log:
```
$ git -C repo branch --show-current
fix/T-GASA-17
$ git -C repo log --oneline fix/T-AUD-22a..HEAD
9df583d audit(T-GASA-17): verdicts for 20 legal-limit and CO 0.45 roots; 8 primary sources
527680e spec(T-GASA-17): verify legal-limit and CO 0.45 roots; verdict checker and format
```

## Criteria
| # | status | evidence |
|---|---|---|
| 1 | MET | step 1: `VERDICTS OK scope=T-GASA-17.txt claims 20`, no `ERROR` |
| 2 | MET | step 2: `CLAIMS OK … covered claims 1693`; `CLAIMS OK group=gaslab … covered claims 195` |
| 3 | MET | note: `## Verdicts` (step 1 lines and the 20-row table), `## Searches` (no UNSOURCED verdict; both searches listed), `## Disputes` (4 items) |
| 4 | MET | step 3: one commit `9df583d` after `527680e`; it changes only `sources.csv`, `verdicts.csv`, `sources/S*.md` (8) |

## Decisions the task did not specify
- **Verdict rule when both CONTRADICTED and PARTLY fit.** If a source states a value for the claim's own quantity
  and condition and that value differs, the verdict is CONTRADICTED (W0129, W0131). PARTLY is used only when the value
  is right for some other condition or attribution and the source gives no different value for the stated one.
- **W0118 is CITATION_WRONG, not CONFIRMED.** The band is right, but one of the two cited sources (SAE J1667) is a
  diesel smoke procedure. The verdict names the wrong citation, and the note names the right source (40 CFR 85.2215).
- **W0185, W1303 and W1083 are judged against the 0.3 % band**, because the wiki states its thresholds for a Euro 4
  baseline. The 0.5 % band (cat cars 1995–Aug 2002) is recorded under Disputes.
- **The EU law texts come from legislation.gov.uk copies**, because EUR-Lex returned the OJ front page or a 404 for
  every CELEX URL. They are classed `PRIMARY_LAW`.
- **The CFR text is the 2011 edition of § 85.2215 (govinfo)**, because the current eCFR Part 85 Subpart W no longer
  holds the idle tests.
- **Source ids have gaps** (S003, S006, S010 were fetched, not cited, and moved out per R3). The cited files were not
  renamed.
- **The CSVs were written by hand.** `impl_guard` denied a generator script under `C:/4DApp/recheck/T-GASA-17/`.

## Pre-existing changes preserved
None in `repo/`: the tree was clean at First action. The `C:/4DApp` workspace changes (`LOOP_STATE.md`, launchers,
handoff) were not touched.

## Rollback
On `fix/T-GASA-17`: `git -C repo reset --hard 527680e` (task branch only; never `main`). Delete the untracked note and
RESULT if required.

## Remaining risks or uncertainties
- 2014/45 footnote (7) as carried on legislation.gov.uk ties the 0.3 % / 0.2 % pair to Euro 5 type-approval. I could
  not check this against the EUR-Lex original (Disputes 3). The W0131 verdict does not depend on it.
- The W0119 quote `2500 ±300 rpm` sits in the section before § 85.2215 on the same CFR page (Disputes 4).
- The BAR Two-Speed Idle citation in W0118 was not fetched.
- UK in-service bands go by date of first use, not by Euro class. A Euro-keyed threshold table (T-GASA-FEURO) can only
  approximate them; W0127 records the Euro 3 overlap.
- Elapsed time 10 min from the clock (09:20:57Z → 09:31:47Z). Context use: ABSENT, because this session has no meter.
