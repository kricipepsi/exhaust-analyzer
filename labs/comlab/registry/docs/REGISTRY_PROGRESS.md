# Registry — Progress Ledger

**Source prompt:** `4DLabWired/docs/JAEGER_FIX_IMPLEMENTATION_PLAN_2026-05-27.md` §10 (off-mount, historical)
**Tasks dir:** `labs/comlab/registry/docs/registry_tasks/` (repo root `/agent_workspace`)
**Mode:** strict (dual `VERIFICATION GATE` + `CODE REVIEW` to flip a task to `done`)
**Last updated:** 2026-06-28 (architect, Cowork: authored the **vault pack** `T-RVAULT-1..6` — mirror the registry into `Vault/labs/comlab/registry/` via `planning/LAB_TO_VAULT_PIPELINE_GUIDE.md`. Viability-assessed: wiki tier SKIPPED (no domain-prose corpus; rules are the spec), full 6-doc pack SKIPPED (web-research-settled — retroactive design docs unwarranted for shipped self-contained code; ship reconciled curated docs instead), vocabulary SKIPPED (enums mirror GAS/DTC, already homed). Phase-3 graphify REQUIRED — registry has 0 nodes in every comlab graph. Refreshed the Windows-era `REGISTRY_START_HERE.md` + `_INDEX.md` to Linux in-mount paths. See "Vault pack" below.) Prior: 2026-05-29 (REG-V2-INTEGRATE done — cutover gate PASS 45→75)

This is the only file `REGISTRY_START_HERE.md` reads to find the next
task. Keep it under ~120 lines. Bulk notes go to
`registry_tasks/progress_notes/<task-id>.md`.

`registry/` is the rule-data workstream. It is self-contained: rule
authoring and audits live here, and COMLab reads the artefacts at
integration time. No imports from any lab, COMLab, or 4DLabWired.

---

## Task log

| ID | Task file | Status | Blocked by | Date | Commit | Verification | Notes |
|---|---|---|---|---|---|---|---|
| AUDIT-CORPUS | `registry_tasks/AUDIT-CORPUS_curate_v2_corpus.md` | done | — | 2026-05-27 | `0ef7652` | Curated 252 cases (241 kept, 40 dropped, 11 new); meta+csv contract OK; 46 cvsgaps dispositions addressed; wired suite green (70/70). | `CORPUS_AUDIT.md` + `corpus_curated.csv` + `corpus_meta.json` + `build_corpus.py`. |
| AUDIT-REG | `registry_tasks/AUDIT-REG_inventory_v1_rules.md` | done | AUDIT-CORPUS | 2026-05-27 | `d8cd35f` | 57 rule IDs inventoried; 12 orphan KG nodes (21%) found; 2/5 top chemistries have zero rules; ecu_fault family (28 cases) has zero rules. Decision: REBUILD v2. | `REGISTRY_AUDIT.md` — full inventory, firing matrix, patch-vs-rebuild analysis. |
| AUDIT-CHEM | `registry_tasks/AUDIT-CHEM_chemistry_matrix.md` | done | AUDIT-CORPUS | 2026-05-27 | `e85c89c` | Chemistry × fault-family matrix complete; 14-family prioritized authoring order ready for REG-V2-SCHEMA. | `CHEMISTRY_COVERAGE.md` — 32 chemistry states × 16 families; TIMING_RETARDED (~64 cases) and SAMPLE_INVALID (~17) identified as top gaps; ecu_fault (28 cases, zero rules) flagged as critical. |
| REG-V2-SCHEMA | `registry_tasks/REG-V2-SCHEMA_define_rule_schema.md` | done | AUDIT-REG, AUDIT-CHEM | 2026-05-27 | `3b5bc5f` | 52 tests (23 schema + 29 existing); pyright 0 errors; 32 ChemistryState + 16 FaultFamily + 20 DTCRoutingTag enums; SCHEMA_V2_SPEC.md with worked example. | `schema_v2.py` (Pydantic v2, 4 enums + 6 models), `SCHEMA_V2_SPEC.md`, `__init__.py`, `test_schema_v2.py`. Next: REG-V2-AUTHOR-lean_condition. |
| REG-V2-AUTHOR-lean_condition | `registry_tasks/REG-V2-AUTHOR-lean_condition.md` | done | REG-V2-SCHEMA | 2026-05-27 | `8f2fc89` | 3 rules (LC-001/002/003); 13 passes_cases all resolve; TIMING_RETARDED gap closed; 66 tests green; ruff 0 / pyright 0. | `rules/lean_condition.json` + `test_lean_condition_rules.py`. Next: REG-V2-AUTHOR-rich_mixture. |
| REG-V2-AUTHOR-rich_mixture | `registry_tasks/REG-V2-AUTHOR-rich_mixture.md` | done | REG-V2-SCHEMA | 2026-05-27 | `b1931d9` | 4 rules (RM-001/002/003/004); 16 tests green; 82 full suite green; ruff 0 / pyright 0. | `rules/rich_mixture.json` + `test_rich_mixture_rules.py`. Next: REG-V2-AUTHOR-misfire. |
| REG-V2-AUTHOR-misfire | `registry_tasks/REG-V2-AUTHOR-misfire.md` | done | REG-V2-SCHEMA | 2026-05-27 | `7d2534a` | 6 rules (MF-001..006); 34 passes_cases all resolve; SAMPLE_INVALID + TIMING_RETARDED gaps closed; ghost-misfire + ECU-blindness covered; 105 full suite green; ruff 0 / pyright 0. | `rules/misfire.json` + `test_misfire_rules.py`. Next: REG-V2-AUTHOR-catalyst_failure. |
| REG-V2-AUTHOR-catalyst_failure | `registry_tasks/REG-V2-AUTHOR-catalyst_failure.md` | done | REG-V2-SCHEMA | 2026-05-27 | `95c2801` | 7 rules (CF-001..007); 25 passes_cases all resolve; TIMING_RETARDED gap closed; 129 full suite green; ruff 0 / pyright 0. | `rules/catalyst_failure.json` + `test_catalyst_failure_rules.py`. Next: REG-V2-AUTHOR-exhaust_leak. |
| REG-V2-AUTHOR-exhaust_leak | `registry_tasks/REG-V2-AUTHOR-exhaust_leak.md` | done | REG-V2-SCHEMA | 2026-05-27 | `91addf6` | 3 rules (EL-001/002/003); 5/5 case refs resolve; 150 tests green; ruff 0 / pyright 0. | `rules/exhaust_leak.json` + `test_exhaust_leak_rules.py`. |
| REG-V2-AUTHOR-sensor_fault | `registry_tasks/REG-V2-AUTHOR-sensor_fault.md` | done | REG-V2-SCHEMA | 2026-05-27 | `88b47c4` | 7 rules (SF-001..007); 19/19 case refs resolve; 183 tests green; ruff 0 / pyright 0. SF-007 added for P0053 heater faults. case_046 (P0190) flagged as follow-up. | `rules/sensor_fault.json` + `test_sensor_fault_rules.py`. Next: REG-V2-AUTHOR-ecu_fault. |
| REG-V2-AUTHOR-ecu_fault | `registry_tasks/REG-V2-AUTHOR-ecu_fault.md` | done | REG-V2-SCHEMA | 2026-05-27 | `3badd85` | 5 rules (EF-001..005), 28/28 cases covered, 35 case refs resolve, 211 tests green, ruff 0 / pyright 0. | `rules/ecu_fault.json` + `test_ecu_fault_rules.py`. Next: REG-V2-AUTHOR-cam_timing. |
| REG-V2-AUTHOR-cam_timing | `registry_tasks/REG-V2-AUTHOR-cam_timing.md` | done | REG-V2-SCHEMA | 2026-05-27 | `93b2903` | 6 rules (CT-001..006); 13 case refs resolve; 8/9 cases covered (EXP-N023 uncoverable); 240 tests green; ruff 0 / pyright 0. | TIMING_RETARDED gap closed; non-VVT path expanded (CT-001). EXP-N023 logged as follow-up. Next: REG-V2-AUTHOR-mechanical_wear. |
| REG-V2-AUTHOR-mechanical_wear | `registry_tasks/REG-V2-AUTHOR-mechanical_wear.md` | done | REG-V2-SCHEMA | 2026-05-27 | `f109d91` | 6 rules (MW-001..006); 11/11 cases covered; TIMING_RETARDED gap closed; 28 tests green; 268 full suite; ruff 0 / pyright 0. | `rules/mechanical_wear.json` + `test_mechanical_wear_rules.py`. Next: REG-V2-AUTHOR-non_starter. |
| REG-V2-AUTHOR-non_starter | `registry_tasks/REG-V2-AUTHOR-non_starter.md` | done | REG-V2-SCHEMA | 2026-05-27 | `dce0c63` | 4 rules (NS-001..004); 7/7 case refs resolve; LEAN_MISFIRE + RICH_MISFIRE + INCOMPLETE_COMBUSTION + DTC paths; 29 tests green; 297 full suite; ruff 0 / pyright 0. | `rules/non_starter.json` + `test_non_starter_rules.py`. Next: REG-V2-AUTHOR-vacuum_leak. |
| REG-V2-AUTHOR-vacuum_leak | `registry_tasks/REG-V2-AUTHOR-vacuum_leak.md` | done | REG-V2-SCHEMA | 2026-05-27 | `a8715c0` | 3 rules (VL-001/002/003); 4/4 case refs resolve; 4 placeholder cases populated with realistic gas/OBD values; 30 tests green; 327 full suite; ruff 0 / pyright 0. | `rules/vacuum_leak.json` + `test_vacuum_leak_rules.py`. New family per cvsgaps.md. Next: REG-V2-AUTHOR-overheating. |
| REG-V2-AUTHOR-overheating | `registry_tasks/REG-V2-AUTHOR-overheating.md` | done | REG-V2-SCHEMA | 2026-05-28 | `e474977` | 4 rules (OV-001..004); 4/4 case refs resolve; 4 placeholder cases populated; 32 tests green; 359 full suite; ruff 0 / pyright 0; Phase 5a 58/58 rules validate, 5b 186/186 refs resolve. | `rules/overheating.json` + `test_overheating_rules.py`. OBD-primary family: 3/4 rules chemistry-empty; OV-003 only carries COOLANT_LEAK_INTERNAL SUGGESTIVE. New family per cvsgaps.md. Next: REG-V2-AUTHOR-charging_system. |
| REG-V2-AUTHOR-charging_system | `registry_tasks/REG-V2-AUTHOR-charging_system.md` | done | REG-V2-SCHEMA | 2026-05-28 | `29b1d05` | 2 rules (CS-001/CS-002); 3/3 case refs resolve; 3 placeholder cases populated (P0562/P0563/P0300 only — P0620-P0626 dropped as not in DTC_VOCABULARY §15); 21 tests green; 380 full suite; ruff 0 / pyright 0; Phase 5a 60/60 rules validate, 5b 189/189 refs resolve. | `rules/charging_system.json` + `test_charging_system_rules.py`. DTC-only family; CS-002 introduces first `NORMAL_OPERATION`-GATING in the registry; MF-004 dominated by double-GATING + ceiling 0.75 > 0.70. New family per cvsgaps.md. Last REG-V2-AUTHOR-*; next: REG-V2-INTEGRATE. |
| REG-V2-INTEGRATE | `registry_tasks/REG-V2-INTEGRATE_wire_to_comlab.md` | done | all REG-V2-AUTHOR-* | 2026-05-29 | `4af93a0` | v1 PASS=45 (16.0% baseline) → v2 PASS=75 (26.7%); cutover gate PASS; CS-002 router-assumption gate PASS. Files=6 (5 planned + `registry/shim/payload_mirrors.py` schema-drift fix). | v2 wired into `fault_atlas_router.py` behind `USE_V2_REGISTRY`. 6-step shim algorithm + side-by-side wrapper. Gates in `progress_notes/REG-V2-INTEGRATE.md`. ⚠ Commit-scope hazard: COMLab submodule working tree has unrelated wiki rewrites (`COMLAB-WIKI-DRIFT-DTC-OBD`) — scope the commit. |
| REG-V2-CHEMSIG-34 | `registry_tasks/REG-V2-CHEMSIG-34_chemistry_state_reconcile.md` | done | REG-V2-SCHEMA | 2026-06-21 | `fba3b96` | registry ChemistryState 34-value, parity with GASLab; WRONG_VALVE_TIMING re-pointed in cam_timing.json; 490 tests green. | Paired with T-GV2-2. |
| REG-WIKI | `registry_tasks/REG-WIKI_render_case_library.md` | done | AUDIT-CORPUS | 2026-06-21 | `8ef2d91` | case_library.html renders 252 curated cases grouped by family; counts match corpus_meta.json; deterministic; tests green. | Emits case_library.html under registry/docs/. |

**Status values:** `pending` · `in_progress` · `done` · `blocked`
**Blocked by:** comma-separated task IDs that must reach `done` first, or `—`.

**Task spec authoring rule:** only AUDIT-CORPUS has a full spec at
bootstrap time. Every other row above is a queued ledger entry; its
spec file is written at the start of its own session (per the
coding-bootstrap anti-pattern: do not author runaway task packs up
front). See `_skills/coding-bootstrap/SKILL.md` Step 3.

---

## Vault pack (`T-RVAULT-*`) — registry → Obsidian vault

The registry is the **last unmirrored COMLab item**: `Vault/labs/comlab/` has
code/docs/wiki/tests but **no registry tier**. This pack carries the registry
through `planning/LAB_TO_VAULT_PIPELINE_GUIDE.md` (Phases 1D→4), viability-assessed
to skip what the registry doesn't need. Each row is one ≤½-session task; specs are on
disk (authored 2026-06-28). Runnability: `pending` = runnable now; `blocked` rows wait
on their Blocked-by.

| ID | Task file | Status | Blocked by | Lane | Notes |
|---|---|---|---|---|---|
| `T-RVAULT-1` | `registry_tasks/T-RVAULT-1_docs_reconcile_list.md` | done | — | author | 2026-06-28: docs tier list pinned + reconciled to 16/34/252 in VAULT_DOCS_MANIFEST.md. |
| `T-RVAULT-2` | `registry_tasks/T-RVAULT-2_code_test_prep.md` | done | — | coder | 2026-06-28: code+test prep clean; 494 green; ruff/pyright 0. |
| `T-RVAULT-3` | `registry_tasks/T-RVAULT-3_doc_prep_explicit.md` | done | T-RVAULT-1 | author | 2026-06-28: doc-prep ingest_ready built; relations EXTRACTED; 0 orphans. |
| `T-RVAULT-4` | `registry_tasks/T-RVAULT-4_graph_ast_build.md` | done | — | coder | 2026-06-28: v2_code + v2_tests graphs built; eval-code-graph GOOD; 0 isolated / 0 dangling. |
| `T-RVAULT-5` | `registry_tasks/T-RVAULT-5_graph_docs_build.md` | done | T-RVAULT-3 | author | 2026-06-28: v2_docs graph built; eval GOOD; 100% EXTRACTED (992 edges); 0 isolated / 0 dangling; no collateral. |
| `T-RVAULT-6` | `registry_tasks/T-RVAULT-6_vault_build.md` | done | T-RVAULT-4, T-RVAULT-5 | author | 2026-06-28: registry mirrored to `Vault/labs/comlab/registry/`; 53 framed docs; 107 files; bases render via frontmatter; idempotent dry-run; targeted unresolved=0. |

**Skipped by assessment (do not author):** wiki tier + `4dlab-wiki-prep` + `v2_wiki`
(no chunked domain corpus); full HLD/DLD/LLD/ADR/BDD/PRD authoring (unwarranted —
registry decision already in `comlab/docs/adr/ADR-0006`); registry vocabulary +
`--vocab` (enums mirror GAS/DTC, already homed in `Vault/_vocabulary/`).

**First runnable:** `T-RVAULT-1` or `T-RVAULT-2` (independent; either may go first).

---

## Unplanned follow-ups

Bugs and refactors discovered mid-task. Logged here, not fixed in the
session that found them.

| ID | Discovered in | One-liner | Status |
|---|---|---|---|
| case_046-P0190 | REG-V2-AUTHOR-sensor_fault | case_046 (P0190 fuel rail pressure sensor) not covered by current 7-rule sensor_fault set — no matching KG node. Needs dedicated pressure-sensor rule or ecu_fault coverage. | pending |
| EXP-N023-uncoverable | REG-V2-AUTHOR-cam_timing | EXP-N023 (VVT solenoid resistance drift 8→40Ω, no DTC, no MAP, no RPM) uncoverable with current OBD PID set. Needs richer OBD capture before a rule can claim it. | pending |
| CS-002-router-assumption | REG-V2-AUTHOR-charging_system | CS-002 `NORMAL_OPERATION`-GATING assumes COMLab router treats missing chemistry as "rule does not fire" (hard-absence), not "default to NORMAL" (imputation). Verify at REG-V2-INTEGRATE: harness must include a "missing chemistry + charging DTC" case and assert CS-002 does NOT fire. If imputation is used, CS-002 must be revised. | **closed** (REG-V2-INTEGRATE 2026-05-29) — hard-absence implemented in shim step 1; `test_cs_002_no_fire_on_missing_chemistry` (real registry) + `test_cs_002_fires_on_normal_chemistry` (synthetic) both PASS. |
| charging-system-alternator-gap | REG-V2-AUTHOR-charging_system | Alternator/regulator field-circuit faults (P0620–P0626) not covered — DTC_VOCABULARY §15 does not list these codes. Requires a wiki-update task (DTCLab) before a REG-V2-AUTHOR-charging_system-v2 can ship. | pending |
| REG-V2-INTEGRATE-SCHEMA-DRIFT | REG-V2-INTEGRATE | Shim output contract vs `OrchestratorFinalUIOutput` acceptance contract were not aligned (shim built against input payload shape, not output schema): `session_id` (UUID4-required) and `user_input_echo_audit` (non-null-required) failed reconstruction. Fixed via `registry/shim/payload_mirrors.py` (Option a — validate at boundary, stable sentinel UUID, never per-call/model_construct). Future shim work must verify both ends. | closed (fixed this task) |
| REG-V2-INTEGRATE-SPEC-PATCH | REG-V2-INTEGRATE | Spec §Context step 1 was silent on rules with zero GATING entries (~60% of rules) — literal reading fires them on every payload incl. empty. Firing predicate clarified (Option 1): a rule fires iff every GATING entry satisfied AND ≥1 evidence row of any tier satisfied. Documented in shim docstring; spec text edit pending. | pending (non-blocking — doc edit) |
| COMLAB-WIKI-DRIFT-DTC-OBD | REG-V2-INTEGRATE (verification) | COMLab submodule working tree has uncommitted rewrites to `docs/wiki/DTC_VOCABULARY.md` (866 lines) + `docs/wiki/OBD_VOCABULARY.md` (61 lines) + `_comlab_skills/comlab-python/SKILL.md` from a different (vocabulary/T-DOC) workstream. Drops `REQUIRE_MATCH` from DTC wiki → `test_wiki_drift_guard[DTCFallbackStrategy]` FAILS in working tree (passes at HEAD). Unrelated to REG-V2-INTEGRATE diff; never touches the router. Owner: COMLab/T-DOC. Also a commit-scope hazard for `git add -A`. | pending (COMLab) |
| wired-registry-guard-rule-count-drift | REG-V2-CHEMSIG-34 | Expected rule count in apps/wired/wired/registry_guard.py is 68, but the rules actually sum to 73 rules on disk, causing RegistryActivationError when running the side-by-side harness. Needs to be bumped to 73. | pending |

---

## Architect-level out-of-band patches

Wiki / skill / convention edits the architect applied directly outside
the per-task diff.

| Date | File | Patch | Reason |
|---|---|---|---|
| 2026-05-27 | `registry/_registry_skills/` (3 universal + `_INDEX.md`) | CREATE | Bootstrap of registry workstream per `_skills/coding-bootstrap/SKILL.md`. |
| 2026-05-27 | `registry/REGISTRY_START_HERE.md`, `REGISTRY_PROGRESS.md` | CREATE | Bootstrap. |
| 2026-05-27 | `4DLab/CLAUDE.md` § Session bootstrap table | APPEND row | Ignition pointer — adds registry workstream to the bootstrap map. |
| 2026-06-28 | `registry_tasks/T-RVAULT-1..6` + this ledger's "Vault pack" section | CREATE | Authored the registry→vault pack (Cowork architect). |
| 2026-06-28 | `REGISTRY_START_HERE.md`, `_registry_skills/_INDEX.md` | REWRITE | De-Windowsed: replaced `C:\Users\muto\...` / off-mount paths + "separate sandbox python3.14" with in-mount Linux paths (`labs/comlab/registry/docs/...`) + shared `/agent_workspace/.venv-wired`. Stale-flag removed. |

---

## Accuracy / quality checkpoints

| Checkpoint | When | Curated corpus PASS | v1 (uncurated) baseline |
|---|---|---|---|
| Pre-rebuild | post-AUDIT-CORPUS | TBD (projection: > 16% as noise drops out) | 16.0 % (281 cases, HARNESS_REPORT.md 2026-05-27) |
| Post-REG-V2-INTEGRATE cutover gate | post-REG-V2-INTEGRATE | must be ≥ v1 PASS count on curated corpus | — |
| Final target | post-REG-V2-INTEGRATE | ≥ 75 % (analysis projection — to be re-targeted by AUDIT-REG) | — |
