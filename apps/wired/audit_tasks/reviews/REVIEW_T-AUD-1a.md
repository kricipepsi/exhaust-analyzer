TASK REVIEW — T-AUD-1a_app_usable(4) — 2026-11-03 (Windows Cowork, first review)
════════════════════════════════════════════════════════════
VERDICT: ACCEPT   (score 94) — pending Linux Cowork's second review (code row); not accepted in the ledger yet

Base `f999f42` (audit-r2 = origin/audit-r2). Task branch `fix/T-AUD-1a`: `f37ca11` (commit 1, COMLab), `a9cca59`
(commit 2, wired and UI). Implementer session `3c933fe7` (PID 11512), 50.0 min measured (`session_times.py`).
Status `partial` with a hand-back of 2 soft findings (`progress_notes/T-AUD-1a.blocker.json`, validator `OK`).

MECHANICAL GATE (run by the reviewer before reading the RESULT)
  ✓ deliverables exist           4/4: 2 commits (made by Cowork, see ruling 1), progress note, RESULT
  ✓ NEW tests red on the base    base swap of the 5 source files (git show f999f42:<file>), then byte-identical restore:
                                 comlab unit 3 failed / 1 passed; wired 21 failed / 4 passed; UI 14 failed / 2 passed.
                                 Every test that passes on the base is tagged PIN. The 2 K2 PINs fail on the base only
                                 by ImportError (disclosed in the RESULT).
  ✓ PIN mutants killed           2/2: fault_name "Fatal Abort:" -> "Fatal:" (aggregator) kills
                                 test_fatal_gate_output_fields_pinned; high-idle `all(` -> `any(` (composition.py:293)
                                 kills test_r3_partial_high_idle_is_ignored. mutants: 2/0 guard, 0/0 other
  ✓ changed files in scope       9 files in f999f42..fix/T-AUD-1a, 0 outside Files to touch; untracked: note, RESULT
  ✓ commits on the task branch   `git branch --contains` → fix/T-AUD-1a only, for both
  ✓ effect visible               Verification re-run by the reviewer (below)

VERIFICATION (reviewer re-run, C:/4DApp/repo)
  1. 9 acceptance probes          9 passed (P1 was 9 failed)
  2. apps/ui/tests                24 passed, 0 failed (P2 was 2 failed, 6 passed)
  3. expected-red probes          C1 42 failed / 2 passed; C4 9 failed / 3 passed; C5 13 failed / 6 passed
                                  C4 is 9, not 10: test_f3b turned green (ruling 2)
  4. import one-liner             import ok
  5. baseline.sh                  the exact command gives PermissionError [WinError 5] on the host pytest temp folder in
                                  4 suites (comlab, dtclab, gaslab, vinlab), an ENVIRONMENT fact. With
                                  PYTEST_ADDOPTS=--basetemp=C:/4DApp/recheck/T-AUD-1a/review/pt: comlab 526 passed,
                                  4 skipped, 2 errors; dnalab 27; dtclab 590; gaslab 208 passed, 2 skipped, 4 deselected;
                                  obdlab 388 passed, 2 skipped; symptomlab 63; vinlab 203 passed, 8 skipped; wired 36
                                  = baseline_20261017.txt + 4 comlab + 25 wired. The 2 comlab errors are R0-2 (cited).
                                  isolation: violations: 4
  6. git log audit-r2..HEAD       2 lines (f37ca11, a9cca59); status: the note and the RESULT only

CRITERIA
  1 MET · 2 MET · 3 MET under its own clause ("Any probe that changes colour is named in the progress note with its
  reason": f3b is named, with the reason) · 4 MET · 5 MET (CLEAN-WITH-FINDINGS: R0-2 errors, host temp folder)
  6 MET after ruling 1 (the commits are the implementer's tree, split by R8's paths, no content change)

HAND-BACK RULINGS (corpus B1)
  1. CONTRADICTION, UPHELD, owner ENVIRONMENT (a loop hook, not the spec). Re-derived: `.claude/hooks/bash_guard.py:53-56`
     MOD_LOAD_RE matches `=Claude ` in `-c user.name=Claude` (the `[...=]` prefix class, IGNORECASE), and judge_text
     refuses it when CLAUDE_ROLE=implementer. No implementer can commit with the identity AGENTS.md:119 mandates. The
     implementer declined every bypass. Remedy for this row: Cowork made both R8 commits from the reviewed tree.
     Loop fix: added to T-LOOP-3's scope (loop_tasks/PROGRESS.md).
  2. CONTRADICTION, UPHELD, owner COWORK (the spec). Re-derived: audit/scratch/C4/test_c4_probes.py:117-123 ends in
     `wc.diagnose(ri)` with no assertion, and ri is a partial OBD set for the decoded wideband type, so R5's abort makes
     it pass. F-C4-3 (override never reaches OBDLab) is NOT fixed. P3 pinned C4 at 10 without accounting for R5.
     Ruling: no change to this row; the probe gains a verdict assertion with F-C4-3 in T-AUD-4 (follow-up below).

DECISIONS THE TASK DID NOT SPECIFY (all accepted)
  --basetemp under the RUNTIME scratch (host temp folder denied; no broad cleanup) · test_r5_mode06_row_sends_dtc as PIN ·
  K2 PINs red on base by ImportError · "VIN decoded" asserted through resolved_horizon (process() hard-codes
  vin_confidence) · the warning text is issue.message.

FINDINGS
  NIT  labs/comlab/comlab/core/lab_pipeline_aggregator.py::abort_incomplete rebuilds the echo sentinel that
       _echo_pass_through already builds (two copies of the lld §3.3 sentinel).
  NIT  apps/ui/ui_payload.py::_mode06_rows reports a valid Monitor ID with a non-numeric margin as "Not a valid
       Monitor ID".
  (not scored) The new test files are CRLF in the working copy; git stores LF (warning at commit).

REMAINING RISKS (implementer's, accepted)
  MIL-only or pending-only forms pass UI validation and get FREEZE_FRAME_INCOMPLETE from the engine (C8/K3, approved).
  The UI was exercised headless (AppTest), not in a browser. impl_guard refuses Write-tool files under the RUNTIME
  folder recheck/T-AUD-1a/ (added to T-LOOP-3's scope).

FILED
  T-AUD-1a-b → T-AUD-4: C4 test_f3b asserts nothing about the verdict; give it an override-reaches-OBDLab assertion
  with F-C4-3 (apps/wired/audit_tasks/PROGRESS.md § Unplanned follow-ups)
  T-LOOP-3 scope: bash_guard MOD_LOAD_RE false positive on `user.name=Claude`; impl_guard vs RUNTIME scratch paths

SECOND REVIEW (Linux Cowork, channel 018-cowork.md, 2026-11-03)
  ACCEPT, score 92 (−2 for spec gap S1, owner COWORK). The row's score of record is 94. C5 amendment accepted; B1
  rulings upheld as written. S1: R5's UI freeze-frame clause cannot hold, because dtclab's data_fusion_sanitizer
  extracts the freeze frame on every DTC dict, so pending-only, MIL-only and Mode 06-only forms reach a clean but
  unflagged FREEZE_FRAME_INCOMPLETE. N1: the gas-unticked message should name GASLab. Both filed as T-AUD-1a-c.
  Accepted and closed 2026-11-03.
