# Skill-Eval — Ledger

> **Session start → read `SKILL_EVAL_START_HERE.md` first** (coder bootstrap). This
> ledger is the source of truth for *which* task and each skill's disposition;
> `SKILL_EVAL_CONTRACT.md` is *how* to measure.

**Pack home:** `planning/skill_eval/` · **Author:** architect · **Date:** 2026-06-09
**Mode:** STRICT (VERIFICATION GATE + CODE REVIEW before `done`)
**Goal:** per-skill verdict — does loading it improve produced code, or only burn context/tokens?

## Task log

| ID | Task file | Status | Blocked by | Deliverable |
|---|---|---|---|---|
| T-SE-0 | `tasks/T-SE-0_methodology_and_rubric.md` | **done** | — | `rubric.md` + `metrics_schema.md` + `SKILL_EVAL_CONTRACT.md` §5 frozen (Cohen's d ≥ 1.0). |
| T-SE-1 | `tasks/T-SE-1_static_triage.md` | **done** | — | Inventory all `SKILL.md`; mark `DEAD`/`OUT-OF-SCOPE`; emit the in-scope shortlist. Cheap wins, no trials. |
| T-SE-2 | `tasks/T-SE-2_eval_runner_and_corpus.md` | **done** | — | `runner.py` + `test_runner.py` + `corpus/` (5 tasks) + smoke run validated. |
| T-SE-3 | `tasks/T-SE-3_cohort_housestyle.md` | **done** | T-SE-0, T-SE-1, T-SE-2 | House-style/craft cohort: python=KEEP, uncle-bob-craft=KEEP, improve-codebase-architecture=KEEP. 60 trials, K=3 judge passes. Report: `results/cohort_housestyle_report.md`. |
| T-SE-4 | `tasks/T-SE-4_cohort_testcraft.md` | **done** | T-SE-0, T-SE-1, T-SE-2 (all done) | Test-craft cohort A/B (python-testing, ai-regression-testing). 27 trials; `mutation_score` populated via new runner `_mutation_score` (FU-SE-5 closed). python-testing **KEEP** (Axis 6 +0.63σ→d=1.35); ai-regression-testing **TRIM** (escaped-defect +ve, sub-bar at N=3). Report: `cohort_testcraft_report.md`. Indicative (N=3). |
| T-SE-5 | `tasks/T-SE-5_cohort_gateoverlap.md` | **done** | T-SE-0, T-SE-1, T-SE-2 (all done) | Gate-overlap cohort (verification-loop, code-review-excellence). **Arm C only** (no arm B — gate-clone null by construction). Closes FU-SE-4 runner gap. code-review-excellence **KEEP** (+3.2σ recovery clears 2.48 bar); verification-loop **TRIM** (+1.0σ recovery sub-1.92 bar). 45 trials, commit `16c9631`. |
| T-SE-6 | `tasks/T-SE-6_meta_borderline.md` | **done** | T-SE-0, T-SE-1 (both done) | Meta/borderline. prompt-engineering → OUT-OF-SCOPE confirmed (inspection + confirmatory A/B null, overturn rule not triggered); eval-harness → OUT-OF-SCOPE (inspection, circular). Report: `meta_borderline_report.md`. |
| T-SE-FINAL | `tasks/T-SE-FINAL_aggregate.md` | **done** | — | `skill_eval_final_report.md`: verdict table (5 KEEP / 2 TRIM / 0 CUT / 18 OUT-OF-SCOPE / 11 DEAD, 37 files) + recommended default coder load-set + caveats register. Independent §5.5 recompute (uncle-bob-craft) matches cohort report. |

**Execution order:** T-SE-0 → T-SE-1 (cheap, parallel) → T-SE-2 → T-SE-3..6 → FINAL.

## Per-skill disposition (the "all skills" coverage)

Track `T` = static triage (T-SE-1, by inspection). Track `AB` = empirical A/B.
`path` is under `_skills/`.

| Skill | Path | Track | Cohort | Primary metric / verdict-intent |
|---|---|---|---|---|
| python | `codingskills/pythonskill/python` | AB | SE-3 | **KEEP** (rubric_structure +1.37σ; hallucinated-API prevents trap-lib usage) |
| uncle-bob-craft | `codingskills/uncle-bob-code-craftsmanship` | AB | SE-3 | **KEEP** (rubric_total +1.43σ; rubric_structure +3.03σ; rubric_cohesion +1.36σ) |
| improve-codebase-architecture | `codingskills/Improve Codebase Architecture` | AB | SE-3 | **KEEP** (rubric_structure +1.79σ; rubric_total +0.98σ sub-bar) |
| python-testing | `codingskills/ecc-subset/python-testing` | AB | SE-4 | **KEEP** (rubric_test_meaningfulness +0.63, d=1.35, bar cleared; mutation_score null at N=3). Indicative N=3. |
| ai-regression-testing | `codingskills/ecc-subset/ai-regression-testing` | AB | SE-4 | **TRIM** (escaped-defect +ve: mutation +0.083, task_02 +0.250 vs baseline; Axis 6 +0.59 d=1.12 sub-bar; all sub-bar at N=3). Indicative N=3. |
| verification-loop | `codingskills/ecc-subset/verification-loop` | AB | SE-5 | **TRIM** (oracle recovery +1.0 vs C_no_skill mean=4.4; bar=1.92 not cleared). Gate-clone: with gate off and single-shot its loop cannot run. |
| code-review-excellence | `codingskills/code-reviev` | AB | SE-5 | **KEEP** (oracle recovery +3.2 vs C_no_skill mean=4.4; clears 2.48 bar). Arrests edge-case/error-handling/structure defects. Judge-bias caveat: rubric inflated (self-preference), verdict rests on objective oracle_failures. |
| prompt-engineering-master | `prompt-engineering-master` | T + 1×AB | SE-6 | OUT-OF-SCOPE by inspection + 1 confirmatory A/B on task_01 (Q-SE-1 resolved). Primary: `rubric_total` + first-pass counts. Overturn-if-bar-cleared. |
| eval-harness | `codingskills/ecc-subset/eval-harness` | — | SE-6 | tool used *by* the pack; OUT-OF-SCOPE as a code skill |
| coding-bootstrap | `coding-bootstrap` | T | — | OUT-OF-SCOPE (builds infra, not code) |
| improve-codebase-architecture (dup) | `Improve Codebase Architecture` (top-level) | T | — | **DEDUPE** vs codingskills copy |
| python-redirect | `pythonskill/python` | T | — | **DEAD** (redirect stub; "do not load") |
| md-prep / create-prd / feature-spec / hld-reviewer | `doc/*` | T | — | OUT-OF-SCOPE (doc authoring) |
| Excel Analysis ×2 / xlsx | `excel/*` | T | — | OUT-OF-SCOPE (+ DEDUPE the two Analysis copies) |
| pdf-to-markdown | `pdf-to-markdown-converter-5` | T | — | OUT-OF-SCOPE |
| firecrawl | `firecrawl-web-scraping-search` | T | — | OUT-OF-SCOPE |
| 4dlab-graph / stats / graph / kg-construction / remember / understand-chat | `graph/*`, `mcpmarket*` | T | — | OUT-OF-SCOPE (KG tooling) |
| sync ×4 | `graph/mcpmarket*/.../sync` | T | — | **DEAD** (stub duplicates) |
| FolderStruct / doc template / nameless graph entries | various | T | — | **DEAD** (empty/no `name:`) |

T-SE-1 pins exact counts and byte-duplicate proofs; the table above is the authored intent.

## Unplanned follow-ups

| ID | Finding | Status |
|---|---|---|
| FU-SE-1 | `_skills` carries duplicates (improve-arch ×2, Excel Analysis ×2) + 4 `sync` stubs + ≥6 nameless files. Pure context waste, independent of A/B results. | route to T-SE-1 (cut/dedupe by inspection) |
| FU-SE-2 | `pythonskill/python` redirect stub coexists with the real `codingskills/pythonskill/python`; bootstrap docs must cite the real one (already fixed in test_rollout). | logged |
| FU-SE-3 | Test-craft cohort (T-SE-4) has only 3 corpus tasks that elicit a fresh test suite ({01,02,03}), below the frozen §5.1 N≥5. Verdict is "indicative" until 2+ test-craft corpus tasks are added. | route to a corpus-extension task (not T-SE-4's diff) |
| FU-SE-4 | `runner.py:capture_metrics` skips all gate counts under `no_gate=True` and never calls `_run_oracle`, so arm-C single-shot quality is unmeasured. T-SE-5 must wire `_run_oracle` + measure-only pytest into the `no_gate` branch, recording into `extra` (no new schema field). | owned by T-SE-5 (in-scope) |
| FU-SE-5 | `runner.py` defines `mutation_score` but never computes it (stays `None`). It is T-SE-4's primary metric, so T-SE-4 must add a `_mutation_score` producer (mutmut/mutpy) and call it in `capture_metrics`. Populates an existing field; no new field. | **CLOSED (T-SE-4)** — `_mutation_score` added (self-contained AST engine, equivalent to mutmut kill ratio), wired into `capture_metrics`; 27/27 trials populated, 0 null. |
| FU-SE-6 | Equivalent mutants flatten absolute `mutation_score`: on task_02, 6/8 mutants are `round(x,4)`→`round(x,5)` (unkillable by any suite); task_01 hits the 1.0 ceiling. A killable-mutant filter (drop mutants no arm kills) would sharpen discrimination. **Metric change — outside the frozen contract**; do not apply inside a cohort diff. | route to a contract-amendment task (not T-SE-4's diff) |

## Open questions

| # | Question | Owner | Before | Resolution |
|---|---|---|---|---|
| Q-SE-1 | Scope boundary (CONTRACT §7): confirm the in-scope set, and whether any OUT-OF-SCOPE skill should be promoted with its own metric. | user | T-SE-1 done | **RESOLVED 2026-06-09** — in-scope set confirmed (8 skills). `prompt-engineering-master`: OUT-OF-SCOPE by inspection **+ 1 confirmatory A/B** (T-SE-6), with an overturn-if-bar-cleared rule. No other OUT-OF-SCOPE skill promoted. |
| Q-SE-2 | Trial budget: N tasks × K trials × arms × cohorts is token-heavy. Confirm N≥5/K≥3, or set a cap. | user | T-SE-2 | **Closed by frozen CONTRACT §5.1** (N≥5, K≥3, J≥3). Caveat: T-SE-4's test-craft subset is N=3 (FU-SE-3). |
