# Assignments — manager-owned (pointers only, NOT specs)

One line per active assignment: `<Coder> → <TaskID>`. One task per coder per session.
The spec lives at `labs/<lab>/tasks/<id>.md`. Never assign the same task ID to both coders.

## Active
Agy → T-V3-P4-C5B   <!-- spec v3/v3_tasks/T-V3-P4-C5B_c5_signal_commit.md · owner go 2026-07-06.
     C5R done + re-audited (Fix-2 provisional, Q-C5-EGR held — see DECISIONS.md). MUTATING commit,
     STRICT dual-gate, one task per session. Firecrawl now auto-authenticated via run-*.sh.
     Coders EXECUTE task files only — never author v3_tasks/ specs (architect lane). -->
<!-- DONE 2026-06-29: all 6 GAS/OBD/DNA/VIN audits 3× + their unions; dtclab T-VLIVE-3c (7e8688a) + comlab RECONCILE-COM (c3e4453). -->

<!-- QUEUED (architect, 2026-07-06, owner to activate — after T-V3-P4-C5B):
     GRAPH ROLLOUT pack · bootstrap planning/graph_rollout/GRAPH_ROLLOUT_START_HERE.md (msg 1)
     ledger planning/graph_rollout/GRAPH_ROLLOUT_PROGRESS.md · order: T-GR-1 → T-GR-2 → GR-3..7
     (docs tiers, one lab/session) → T-GR-8 (MCP pilot, owner go) → T-GR-9 (refresh, owner go).
     CLI (graphify query/explain/affected --graph …) is the baseline access path; MCP optional. -->
## Cross-check (read-only audit — exception to the same-ID rule is intentional)
The Graph-Trust audit is READ-ONLY and each coder writes its own report
`apps/vault/audit/reports/<lab>__<agent>.md`, so the same task ID may run on all three
coders without collision — the redundancy IS the design (union of complementary models
catches more, per EVAL-VLIVE-1). Spec: apps/vault/audit/T-GTA-METHOD.md.
Codex + Agy + Claude → T-GTA-<lab>   <!-- paste T-GTA-METHOD as msg 1; run per the GRAPH_TRUST_AUDIT ledger; do NOT edit maps (discovery only). -->
<!-- Codex → T-OBDV2-7 -->
<!-- Agy   → T-GASV2-3 -->

## History
- STALE-POINTER FIX 2026-07-06 (architect): `Active` had pointed at T-GTA-RECONCILE-GAS/-OBD since
  2026-06-29 although both are **done** per `apps/vault/audit/GRAPH_TRUST_PROGRESS.md`
  (RECONCILE-GAS done · RECONCILE-OBD done b20a80c · RECONCILE-VIN done 14a29c2 · T-WIRE-1 gate cleared).
  Coders read `Active` at session start (identity step 2), so every new session drifted to the stale
  done task before its real work. Root cause: assignments were never flipped after completion.

- Architect (Cowork) → T-COM-GRAPH-AST — **done 2026-06-28** (owner-delegated graph-tooling bring-up; architect lane, not a coder — `lane-guard-no-graphify` blocks coders on the literal `graphify`). Installed `graphifyy 0.8.36` into `.venv-wired`; built `labs/comlab/graph/{v2_code,v2_tests}` (both health GOOD); `v1_baseline` untouched. **Next coder task: T-COM-PATHS-1** (then author-lane T-COM-VAULT).

<!-- SUGGESTED (architect, 2026-06-29, owner to activate): Codex OR Agy -> T-PYSCN-1
     READ-ONLY pyscn eval. spec: planning/code_audit/tasks/T-PYSCN-1_evaluate_pyscn_audit_cli.md -->

<!-- SUGGESTED (architect, 2026-06-29, owner to activate): partitioned doc-conformance audit
     deepseek -> T-DCA-GAS, T-DCA-OBD   (run-deepseek.sh; paste tasks/T-DCA-<LAB>_*.md; run per DOC_CONFORMANCE_PROGRESS ledger)
     spec: planning/doc_conformance/T-DCA-METHOD.md · NOT a wiring gate (quality pass). -->

<!-- SUGGESTED (architect, 2026-06-30, owner to activate): wired-test pack (test the wired app post-wiring).
     Bootstrap (msg 1 of each session): apps/wired/test_tasks/WIRED_TEST_START_HERE.md
     Ledger: apps/wired/test_tasks/TEST_PROGRESS.md · one task per coder session, STRICT dual-gate.
     Run STRICTLY in ledger order (blocked-by chain): only T-WTEST-1 is pending now.
       1) <coder> -> T-WTEST-1   full-suite green baseline (run-only). Unblocks T-WTEST-2 + T-WTEST-3.
       2) Codex   -> T-WTEST-2   pyscn audit of apps/wired (read-only)        [needs T-WTEST-1 done]
          Agy     -> T-WTEST-3   native-Linux Jaeger + .sh env profile        [needs T-WTEST-1 done]
          (T-WTEST-2 and T-WTEST-3 are independent — safe to split across the two coders, no edit race:
           T-WTEST-2 touches test_tasks/ only; T-WTEST-3 touches apps/wired/trace/.)
       3) <coder> -> T-WTEST-4   run oil case under OTel; spans -> Jaeger      [needs T-WTEST-3 done]
       4) <coder> -> T-WTEST-5   extract trace + trace report                 [needs T-WTEST-4 done]
     Never assign the same T-WTEST id to both coders (these are MUTATING, unlike the T-GTA read-only audit). -->

<!-- SUGGESTED (architect, 2026-06-30, owner to activate): wired-v7 research-built accuracy pack.
     Bootstrap (msg 1 of each session): apps/wired/v7_tasks/WIRED_V7_START_HERE.md
     Ledger: apps/wired/v7_tasks/V7_PROGRESS.md · one task per coder session, STRICT dual-gate.
     HARD RULES: no ARCHIVE artefacts; case SOURCE = owner libraries at /home/m/Desktop/casesextra/
       (primary cases_library_v2.html); oracle from wiki/atlas (not engine output, not library-over-wiki);
       incomplete cases -> Owner action queue, never fabricated; suite scores MULTIPLE dimensions (catch all errors).
     STRICTLY SEQUENTIAL (each blocks the next) — only T-V7-1 is pending now:
       1) <coder> -> T-V7-1   library research + viability map (read-only)         bounds the suite
       2) <coder> -> T-V7-2   build cases_petrol_v7.csv inputs from shortlist      [needs T-V7-1]
       3) <coder> -> T-V7-3   fill oracle from wiki/atlas                          [needs T-V7-2]
       4) <coder> -> T-V7-4   driver + multi-dimension scorer vs live diagnose()  [needs T-V7-3]
       5) <coder> -> T-V7-5   run suite + coverage/accuracy + error taxonomy      [needs T-V7-4]
     Chain is linear: each task consumes the prior task's artifact. (Supersedes the earlier v6 draft, re-keyed to v7.) -->

<!-- SUGGESTED (architect, 2026-06-30, owner to activate): wired-v7 post-run pack (after T-V7-5 audit).
     Ledger: apps/wired/v7_tasks/V7_PROGRESS.md · STRICT dual-gate · one task per coder session.
     All THREE are pending now, no blockers, INDEPENDENT — safe to split across coders (no edit race:
       T-V7-6 -> v7_tasks/ + apps/wired/trace/ ; T-V7-7 and T-V7-8 are read-only memos):
       <coder> -> T-V7-6   full 314-case corpus under Jaeger --trace (the pass T-V7-5 §6 did not run).
                           Needs the T-WTEST-3 native collector up. Resolves F-V7-TRACE.
       <coder> -> T-V7-7   READ-ONLY: decide canonical fault_code surface (engine ERR- vs oracle short). Memo only.
       <coder> -> T-V7-8   READ-ONLY: decide confidence_score semantics (engine recalibrate vs oracle reband). Memo only.
       <coder> -> T-V7-9   **PRIORITY** first same-ruler v1-vs-v2 number on the v7 suite (USE_V2_REGISTRY=0 proxy).
                           Step 0 = fidelity diff vs /home/m/Desktop/4dV1/registry/. Answers "did the rebuild move routing?".
                           Gates tune-or-revert. (51%/48% are different rulers — not comparable; this makes them comparable.)
     The engine/oracle FIX tasks for F-V7-CODE-NS / F-V7-CONF-SAT are intentionally NOT authored yet —
       they wait on the T-V7-7/T-V7-8 memos + owner sign-off. Routing fixes wait on the T-V7-6 trace.
     Tuning/revert is BLOCKED until T-V7-9 gives a same-ruler baseline (owner: establish baseline before tuning). -->

<!-- SUGGESTED (architect, 2026-06-30, owner to activate): wired-fl failure-localization pack.
     PURPOSE: pinpoint the exact failure point + mode of every failing v7 case, and freeze a
       before/after yardstick, so the planned v3 rebuild targets the real constraint and is
       measured honestly (not another incomparable headline). READ-ONLY on the engine.
     Bootstrap (msg 1 of each session): apps/wired/fl_tasks/WIRED_FL_START_HERE.md
     Ledger: apps/wired/fl_tasks/FL_PROGRESS.md · STRICT dual-gate · one task per coder session.
     Context to read first: apps/wired/v7_tasks/reports/V7_REBUILD_FAILURE_AUDIT_2026-06-30.md
     Order (blocked-by chain):
       <coder> -> T-FL-1   lock true v2 baseline (family+state) + freeze v3 yardstick   [runnable now]
       <coder> -> T-FL-2   capture per-case GASLab/OBDLab upstream states (read-only)    [runnable now]
                           (T-FL-1 and T-FL-2 are independent — safe to split across the two coders)
       <coder> -> T-FL-3   classify each failing case -> mode + stage of divergence      [needs T-V7-6 + T-FL-2]
       <coder> -> T-FL-4   one-command v3 before/after scoreboard on the yardstick        [needs T-FL-1 + T-FL-3]
     v3 is then BUILT against FL_LOCALIZATION (target list) and JUDGED by the T-FL-4 scoreboard
       against the FL_YARDSTICK freeze. Do not start v3 before T-FL-3 lands the target list. -->



