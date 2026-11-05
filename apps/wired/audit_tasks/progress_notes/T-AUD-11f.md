# Progress note — T-AUD-11f (OBDLab drift report)

## Readiness challenge
- (a) Starting state matches the task. Branch `fix/T-AUD-11f`. HEAD `3d84b0dde27ae71ef65efe690affa370e0029f54` (`spec(T-AUD-11f)`), a descendant of `474032c` (`git merge-base --is-ancestor 474032c HEAD` printed `descendant`). Base for the RESULT: `3d84b0d`. `git status --porcelain` printed nothing. The Preconditions command printed only `checked`. P2 holds 16 `.py` files and 2,055 lines (`find labs/obdlab/obdlab -name '*.py' | xargs wc -l`).
- (b) The checker failed before the report existed, for the intended reason: `FileNotFoundError: audit\drift\2026-11-05_DRIFT_REPORT_obdlab.md`.
- (c) Expected value, derived from P1 before the first edit: 8 `##` sections in P1 order, and `refs ok N/N` with both N equal. I did not know N in advance. N is two refs for each finding with a Code quote, and one for each ABSENT finding.
- (d) No contradiction or missing decision blocks the work. Stops (a)-(d) checked: the 8 P1 documents, the 16 P2 files, the two config files, `composition.py` and the checker all exist and match the task.
- (e) Teach-back. The deliverable is one drift report, `audit/drift/2026-11-05_DRIFT_REPORT_obdlab.md`, with one section per P1 document and one quoted bullet per difference between a document and the code. The decisive check is Verification step 1: the checker prints `sections 8/8`, equal `refs ok N/N` and `REPORT OK`.

## Assumptions worked past
- Mode $06 (README line 4): the lab package has no Mode $06 code, and `apps/wired/wired/composition.py` passes the Mode $06 fields through. I did not report Mode $06 as MISSING. I report only the O2 masking half of that role line.
- The `trim_analytics_suspect` flag (HLD section 3, DLD section 8): the checker computes it and the translator never reads it. The documents promise a non-blocking flag, not a payload field. Not reported.
- HLD section 5 says three O2 sensor types map to two code paths. The code has three methods with one voltage map and different mode values. Treated as presentation. Not reported.
- VOCABULARY PID ranges (`engine_rpm` 0-16383.75, `coolant_temp_c` -40-215) are protocol ranges, and the lab bounds are narrower. Not reported.
- VOCABULARY sections 5.3 and 5.4 describe COMLab schemas (`COMLab/comlab/schemas/ingestion.py`), outside P2. Not reported.
- Claims about tests (`test_vocabulary.py`, the import audit) are out of scope (`tests/` is excluded). I report only what the same claims say about `obdlab/` text.
- `HIGH_IDLE_LOAD` claims: I read `obdlab/` as the package directory `labs/obdlab/obdlab/`. It holds the YAML config, and the YAML note at line 40 names the token. If the test scans only `.py` files, the claim holds for code and fails for config. I report the difference in 5 documents (PRD, HLD, LLD, DLD, BDD).
- The `normalized_obd_lambda` frozen value (1.0 in the documents, None in the code) appears in PRD, HLD, LLD, DLD and BDD. I report it once for each document.
- The wiring facts for `freeze_frame_pids` come from `apps/wired/wired/composition.py` (P2). `grep -n freeze_frame_pids` shows lines 438, 439 and 494 only, so the composition never writes the key into the OBD inputs.
- Doc line numbers for the PRD are file lines. My first listing joined README and PRD with one `cat -n`, which shifted the PRD numbers by 13. The checker caught it (4 bad refs) and I corrected them.

## Time
| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| First action, reading, report, commit | 2026-11-05T21:14:23Z | 2026-11-05T21:20:30Z | 6.1 (clock) | ABSENT |

## VERIFICATION GATE
Run from `C:/4DApp/repo` in Git Bash after the commit.
- Step 1: `sections 8/8, findings 33, refs ok 63/63` then `REPORT OK`, exit 0. The previous decisive failure (4 bad PRD refs, `REPORT BAD`, exit 1) is absent.
- Step 2: `git diff --name-only HEAD~1 HEAD` printed `audit/drift/2026-11-05_DRIFT_REPORT_obdlab.md` only.
- Step 3: `git log --oneline -3` printed `42327ec` (my commit), `3d84b0d` (spec), `474032c`. `git status --porcelain` printed only the note (`?? apps/wired/audit_tasks/progress_notes/T-AUD-11f.md`) before the RESULT existed.
- ABSENT commands, rerun from the repo root: `grep -rniE 'mask' labs/obdlab/obdlab --include=*.py`, `grep -rniE 'euro' labs/obdlab/obdlab --include=*.py` and `grep -rn 'fuel_trim_invalid' labs/obdlab/obdlab` each print nothing and exit 1.
- No test suite ran. The row writes a report only.

VERDICT: CLEAN

## CODE REVIEW
Scope: one new Markdown file. No document, code, test or data file changed (R3).
- Scope (blocking): the commit holds one path, the report. Clean.
- Contracts and boundaries: no code touched. Clean.
- Evidence: the checker confirms that every quote is on its cited line. I also read each cited code line against its claim. I checked these by hand: `normalized_lambda: float | None = None` (translator line 151) against the five lambda findings, `raise ValueError` (ve_engine line 95), `_CUTOFF_ECT_COLD = 75` (semantic checker line 21), and `value: [10.0, 60.0]` (YAML line 39).
- Counts: README 1, PRD 4, HLD 6, LLD 6, DLD 4, BDD 2, VOCABULARY 9, ADR 1. Total 33.
- Finding classes (`grep -o '^- \[[A-Z]*\]' audit/drift/2026-11-05_DRIFT_REPORT_obdlab.md | sort | uniq -c`): DIVERGENCE 21, MODEL 5, MISSING 3, UNDOCUMENTED 4. Total 33.

Open concern: the commit message has no attribution trailer. `bash_guard` refused the commit when the message held the trailer text, so I committed without it.
