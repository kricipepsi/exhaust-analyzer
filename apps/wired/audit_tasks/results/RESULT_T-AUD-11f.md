# Result

## Status
completed

## Summary
The report `audit/drift/2026-11-05_DRIFT_REPORT_obdlab.md` lists 33 differences between the 8 OBDLab design documents and the current code. Counts by document: README 1, PRD 4, HLD 6, LLD 6, DLD 4, BDD 2, OBD_VOCABULARY 9, ADR 1. Counts by class: DIVERGENCE 21, MODEL 5, MISSING 3, UNDOCUMENTED 4. The checker prints `REPORT OK`.

The most repeated findings:
- Five documents (PRD, HLD, LLD, DLD, BDD) state that a frozen engine emits `normalized_obd_lambda = 1.0` or type the field as a plain `float`. The code emits `None` (`sensor_signal_translator.py:151`, `payload.py:74`).
- Five documents state that `HIGH_IDLE_LOAD` appears nowhere in `obdlab/`. The YAML note at `obd_translation_rules.yaml:40` names it.
- Three documents say COMLab fills `freeze_frame_pids` from DTCLab before the OBDLab call. The composition copies only the DTC codes (`composition.py:691`).

## Files changed
- `audit/drift/2026-11-05_DRIFT_REPORT_obdlab.md` (created, committed as `42327ec`)
- `apps/wired/audit_tasks/progress_notes/T-AUD-11f.md` (created, not committed)
- `apps/wired/audit_tasks/results/RESULT_T-AUD-11f.md` (created, not committed)

## Commands executed
- `cd C:/4DApp/repo && git branch --show-current && git log --oneline -1 && git status --porcelain` (First action)
- The Preconditions loop (`test -f` on 5 paths, `test -e` on the report)
- `find labs/obdlab/obdlab -name '*.py' | xargs wc -l`
- `cat -n` on the 8 P1 documents, 16 P2 `.py` files and the 2 config files; `grep -n` on `apps/wired/wired/composition.py`
- `grep` checks: `HIGH_IDLE_LOAD`, `euro`, `calculated_ve`, `fuel_trim_invalid`, `mask`, `ObdEmissionsView`
- Verification steps 1, 2 and 3 (see below)
- `git add audit/drift/2026-11-05_DRIFT_REPORT_obdlab.md`, then the local commit by explicit path

## Validation evidence
Step 1 (`check_report.py`, after the commit): `sections 8/8, findings 33, refs ok 63/63` then `REPORT OK`, exit 0.
The previous decisive failure is absent. The first run of the checker printed `refs ok 59/63` and `REPORT BAD`, with 4 PRD refs past the end of the file (`PRD_OBDLab.md:140`, `:220`, `:120`, `:243`). The cause was a joined `cat -n` listing of README and PRD, which shifted the PRD line numbers by 13. I corrected them to `:127`, `:207`, `:107` and `:230` before the commit.
Step 2 (`git diff --name-only HEAD~1 HEAD`): `audit/drift/2026-11-05_DRIFT_REPORT_obdlab.md` only.
Step 3 (`git log --oneline -3; git status --porcelain`): `42327ec docs(T-AUD-11f): ...`, `3d84b0d spec(T-AUD-11f): ...`, `474032c review(T-AUD-11e): ...`. Status printed only the note before this RESULT existed.
Three ABSENT commands, run from the repo root, print nothing and exit 1: `grep -rniE 'mask' labs/obdlab/obdlab --include=*.py`, `grep -rniE 'euro' labs/obdlab/obdlab --include=*.py`, `grep -rn 'fuel_trim_invalid' labs/obdlab/obdlab`.

## Criteria
| # | Verdict | Evidence |
|---|---|---|
| 1 | MET | Step 1 printed `sections 8/8`, `refs ok 63/63` (both N equal) and `REPORT OK`. |
| 2 | MET | Step 2 listed only `audit/drift/2026-11-05_DRIFT_REPORT_obdlab.md`. |
| 3 | MET | `42327ec` sits on `fix/T-AUD-11f` after the spec commit `3d84b0d`. `git status --porcelain` lists only the note and this RESULT. No `.blocker.json` exists, because I did not hand back. |

## Decisions the task did not specify
- I report each repeated drift once for each document that carries it (lambda 1.0 in 5 documents, `HIGH_IDLE_LOAD` in 5, `freeze_frame_pids` in 2). R2 asks for findings per document, and Cowork turns each into a fix row.
- `obdlab/` in the documents means the package directory `labs/obdlab/obdlab/`, which includes the YAML config. Under that reading the YAML note at line 40 breaks the `HIGH_IDLE_LOAD` claims.
- Findings that cite `apps/wired/wired/composition.py` (P2 caller) cover claims about what COMLab does before or after the OBDLab call.
- I did not report as drift: Mode $06 (the composition passes it through), protocol PID ranges in the vocabulary, COMLab schema tables (VOCABULARY sections 5.3 and 5.4), and claims about tests. The note lists the reasons under `Assumptions worked past`.
- I committed without the attribution trailer that the session reminder asks for. `bash_guard` refused the commit command with the trailer in the message. The commit message follows `AGENTS.md` (`docs(T-AUD-11f): ...`).

## Pre-existing changes preserved
`git status --porcelain` was empty at the start of the row, so I had nothing to preserve in `repo/`. I did not touch the untracked files that exist under `C:/4DApp` (launchers, handoff, `LOOP_STATE.md`).

## Rollback
Run `git revert 42327ec` on `fix/T-AUD-11f`. The note and this RESULT are untracked files that Cowork can delete.

## Remaining risks or uncertainties
- The checker proves that each quote sits on its cited line. It does not prove that each finding is a real drift. Cowork must review the claim in each bullet.
- Four findings rest on a reading call: the two `HIGH_IDLE_LOAD` readings (package directory or `.py` only), the VOCABULARY `total_trim_correction_delta` range (the document also states 254 at line 148), the `freeze_frame_pids` population (I found no write in the composition by `grep`), and the HLD DNA-view fallback (UNDOCUMENTED by my reading of line 52).
- Four ABSENT or MISSING claims cover only the paths that their commands search (`labs/obdlab/obdlab`).
- The Mode $06 half of the README role line is not reported (see Decisions).

Branch and log:
```
$ git -C repo branch --show-current
fix/T-AUD-11f
$ git -C repo log --oneline 3d84b0d..HEAD
42327ec docs(T-AUD-11f): OBDLab drift report, 33 findings in 8 documents
```
