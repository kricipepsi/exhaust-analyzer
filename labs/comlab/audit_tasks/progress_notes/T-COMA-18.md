# T-COMA-18 progress note

## Readiness
(a) Start state matches: branch fix/T-COMA-18, one spec commit 206f21b over 24d265b, `git status --porcelain` empty; all preconditions files present.
(b) New test fails on base for the intended reason: R4 base run (patched .py files stashed) must give `5 failed, 4 passed`; recorded below.
(c) Decisive expected values come from the task's P2/P3 pins (9 passed; 5 failed/4 passed on base; LEGACY rich line without RM-004; changed 0 of 314). Not rederived from the rehearsal run.
(d) No contradiction found: R1/R2 text matches rehearsal.patch hunks read in full.
(e) Deliverable: RM-004 is pruned as `hardware_gate` on a non-GDI, non-MODERN car, with fuel_delivery_type plumbed wired -> SessionMetadata -> aggregator -> shim. Decisive check: new test `9 passed` (base `5 failed, 4 passed`), probes `3 passed, 7 deselected`, corpus `changed 0 of 314`.

## Assumptions worked past
The commit trailer from the session attribution reminder was refused by bash_guard (hook error on the commit text); I committed without it.

## R4 results
| run | result |
|---|---|
| base (4 .py files stashed) | 5 failed, 4 passed |
| patched | 9 passed |
| mutant A (`if False:` for the gate call) | 3 failed, 6 passed |
| mutant B (GDI check off) | 1 failed, 8 passed |
| mutant C (drop `horizon is not None`) | 1 failed, 8 passed |
| mutant D (aggregator line deleted) | 1 failed, 8 passed |
Each mutant was restored from a copy of the patched file. `git diff --stat` after restore: 4 files, 32 insertions(+), same as before the mutants.

## VERIFICATION GATE
- step 1: comlab `517 passed, 4 skipped`; wired `185 passed`; ui `73 passed`; test_tunable_reweight `2 passed`.
- step 2: `9 passed`.
- step 3: `LEGACY rich -> ['RM-001', ('LC-002', 0.86...), ...]` (no RM-004); `3 passed, 7 deselected`.
- step 4: `changed 0 of 314`.
- step 5: `All checks passed!`; `5 files changed, 112 insertions(+)`; log shows spec commit 206f21b and 2a3ccd1; porcelain showed only the note (the RESULT is written after).
Verdict: CLEAN. py_compile, pyright and `--select S` were not in the task's Verification: NOT RUN.

## CODE REVIEW
Scope: every changed line is in `### Files to touch ###`. Contracts: both new fields carry a `consumer:` comment naming `_hardware_gate`. Boundaries: no cross-lab import. Orphan check: `fuel_delivery_type` is read by the shim gate through the aggregator metadata. No findings.

## Time
phase | start | end | minutes | context at end
all | 2026-11-13T14:38:32Z | 2026-11-13T14:40:07Z | 1.6 | ABSENT

## Correction 1
Start 2026-11-13T14:46:02Z. First action matched (branch fix/T-COMA-18, log 15cc332, 2a3ccd1, 206f21b; porcelain only the note and RESULT). Preconditions: no MISSING.
R5: `git apply correction1.patch`; `cmp` of the test against `..._c1.py` identical. Step 2 on the patched tree: `10 passed`.
R6 mutant E (`"prune_reason": "x",` in the gate's `pruned_rules.append`, line 1451): `1 failed, 9 passed`. Restored by hand; `cmp` against a copy of the patched shim identical; step 2 again `10 passed`.
Commit a556cb6 (shim + test only).

### VERIFICATION GATE (correction 1)
- step 1: comlab `517 passed, 4 skipped`; wired `186 passed`; ui `73 passed`; test_tunable_reweight `2 passed`.
- step 2: `10 passed`.
- step 3: `LEGACY rich -> ['RM-001', ('LC-002', 0.86...), ...]` (no RM-004); `3 passed, 7 deselected`.
- step 4: `changed 0 of 314`.
- step 5: `All checks passed!`; `5 files changed, 121 insertions(+)`; log: 206f21b, 2a3ccd1, 15cc332, a556cb6; porcelain only the note and the RESULT.
Verdict: CLEAN. py_compile, pyright, `--select S` NOT RUN (not in Verification).

### CODE REVIEW (correction 1)
Scope: two files changed, both in `### Files to touch ###`. Tests now assert `"RM-004" not in` the verdict and the prune record. No findings.

### Time (correction 1)
phase | start | end | minutes | context at end
correction 1 | 2026-11-13T14:46:02Z | 2026-11-13T14:47:25Z | 1.4 | ABSENT
