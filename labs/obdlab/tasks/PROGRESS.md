# OBDLabV2 — Progress Ledger

**Stage:** 2 (follows GASLab) · **Research spine:** `docs/reference/audit_2026-06-03/4DLAB_CAPABILITY_AUDIT_AND_RESEARCH_QUESTIONS.md` → **OBDLab §** (the 10 questions).
**Mode:** STRICT (both gates clean before `done`). **Last updated:** 2026-06-09 (T-KG-OBD-3 done - separate test-map ingest).

## Workflow (owner) — research-first, same for every lab

**(A) Research** — the owner answers the **10 OBDLab audit questions** (external research / standards /
data). → **(B) Author** — the architect turns each answered question into a *runnable* task spec. →
**(C) Code** — the coder implements (inner loop → verification gate → code review). **Coding starts only
after** the scope decision and the relevant research answers are in. Cross-lab obligations are tracked in
`4DLab/v2-restructure/CROSS_LAB_DEPENDENCIES.md`.

## North-star scope gate (blocks everything)

**RESOLVED 2026-06-08 → `revive` (emitter role).** See `tasks/T-OBDV2-0_revive_emitter_decision.md`. The
>95% NO_FAULT was a **PID-less-corpus** artefact, not a code defect; OBDLab is revived as a typed
*perception-channel emitter* feeding COMLab fusion (it does **not** emit fault-family verdicts — that is
COMLab's job, per `KGtopic.md` division-of-labor). Standalone OBD classification is conceded (validates
T-OBDV2-PURGE-1). The gate is open; rows below are unblocked except where they carry their own research gate.
First proof task: **T-OBDV2-1 PID-logset wiring gate** (un-quarantine proof).

## Task log

| ID | Task file | Status | Blocked by | Consumer (signal/noise) | Notes |
|---|---|---|---|---|---|
| **T-OBDV2-0** | `T-OBDV2-0_revive_emitter_decision.md` | **done — revive (emitter)** | — | — | **THE scope gate.** Resolved `revive` 2026-06-08 (owner-ratified). Quarantine cause was PID-less corpus, not code. Next proof: T-OBDV2-1. |
| **T-OBDV2-1a** | `T-OBDV2-1a_pid_logset_authoring.md` | **done** | — | T-OBDV2-1b (the gate) | **Un-quarantine proof — data half.** 38 sourced cases across 8 matrix cells + 7 families; post-PURGE DNA contract (no emissions/number_of_banks); estimated cases quarantined; all parse. Files changed: 4. |
| **T-OBDV2-1b** | `T-OBDV2-1b_pid_logset_wiring_gate.md` | **done** | T-OBDV2-1a | live `translate()` discriminating output (the gate is the consumer) | **Un-quarantine proof — code half.** Gate green: all 8 cells exercised, 100 % sourced cases moved their channel, rejections raise typed errors, 4.76 % default-shape — OBDLab un-quarantined as an emitter. Files changed: 1. |
| **T-OBDV2-ECU-PERCEPT-1** | `T-OBDV2-ECU-PERCEPT-1_ecu_perception_delta_channel.md` | **done** | — | COMLab `T-COMV2-ECU-FUSE-1` (S4) | **Inherited (DEP-2).** lambda_perception_delta emitted under WIDEBAND/0x44 guard; emitter-only (no verdict); T-COMV2-ECU-FUSE-1 forward-registered; Stage-2 green (anti-orphan closes at Stage 4). Files changed: 4. |
| **T-OBDV2-BANK-ASYM-1** | `T-OBDV2-BANK-ASYM-1_per_bank_trim_emit.md` | **done** | — (Q2/Q6 answered) | COMLab `T-COMV2-BANK-FUSE-1` (S4) | per_bank_trim_delta emitted under bank-2-presence gate; emitter-only; T-COMV2-BANK-FUSE-1 forward-registered (±5 % bound, pre-2001 caveat); Stage-2 green. Files changed: 6. |
| **T-OBDV2-2** | `T-OBDV2-2_ve_air_strategy_gate.md` | **done** | — (Q5 answered) | COMLab `T-COMV2-VE-GATE-1` (S4) | **Q5.** VE-as-evidence gate frozen (DUAL_MAF_MAP_CROSSCHECK only; single-sensor → P0068); T-COMV2-VE-GATE-1 forward-registered; no OBD source change; orphan ve_pct/ve_validity closes at Stage 4. Files changed: 6. |
| **T-OBDV2-3** | `T-OBDV2-3_downstream_role_close.md` | **done** | — | **live** — `comlab perception_contradiction.detect` | **Q7 closed.** Verification gate green: masking signal verified on existing DNA role consumer (`perception_contradiction.detect`). No new OBD channel added. O2-FU-2 doc-bug logged. |
| **T-OBDV2-4** | `T-OBDV2-4_wideband_offset_proposal.md` | **done** | — (Q9 answered) | COMLab `T-COMV2-O2OFFSET-1` (S4) | **Q9 / O2-FU-1.** WIDEBAND_OFFSET_CANDIDATE emitted under WIDEBAND_LINEAR + persistent `\|λ−1\|>0.05`; candidate-only (no verdict); proposal EP-OBD-17 + T-COMV2-O2OFFSET-1 forward-registered; Stage-2 green. Files changed: 4. |
| **T-OBDV2-5** | `T-OBDV2-5_mode06_nostart_proposal.md` | **done** | — (Q8 answered) | COMLab `T-COMV2-NOSTART-1` + DTCLab `T-DTCV2-NOSTART-1` | Q8 dispositioned cross-lab: EP-DTC-NOSTART-1 registered; T-DTCV2-NOSTART-1 (producer) + T-COMV2-NOSTART-1 (reader) forward-registered; CAN-era gated; no OBDLab code. |
| **T-OBDV2-6** | `T-OBDV2-6_fuel_system_status_input.md` | **done** | — | **live** — `analytics_preconditions` + `semantic_consistency_checker`; COMLab `T-COMV2-FUELSYS-GATE-1` (S4) | fuel_system_status dropdown added (FuelSystemStatus mirror, no import); 2 internal consumers migrated string→enum; T-COMV2-FUELSYS-GATE-1 forward-registered; Stage-2 green. |
| **T-OBDV2-7** | `T-OBDV2-7_iat_tps_input_pair.md` | **done** | — (run after T-OBDV2-6) | IAT **live** in `ve_engine`; COMLab `T-COMV2-ECU-HW-1` (S4) | **Proposals EP-OBD-IN-08 + EP-OBD-IN-05.** intake_air_temp_c + throttle_pos_pct added; IAT feeds live ve_engine; T-COMV2-ECU-HW-1 forward-registered; Stage-2 green. Files changed: 14. |
| **T-OBDV2-8** | `T-OBDV2-8_vpwr_input.md` | **done** | — | COMLab `T-COMV2-VPWR-GATE-1` (S4) | control_module_voltage_v added; field-only (no verdict); T-COMV2-VPWR-GATE-1 forward-registered; chunk ecu-diagnosis/09 authored; Stage-2 green. |
| **T-OBDV2-9** | `T-OBDV2-9_per_cylinder_misfire_counts.md` | **done** | — | COMLab `T-COMV2-MISFIRE-LOC-1` (S4) | **Proposal EP-OBD-IN-07.** per_cylinder_misfire_counts ferried (optional, CAN-era); emitter-only; EP-OBD-IN-07 + T-COMV2-MISFIRE-LOC-1 forward-registered; Stage-2 green. Files changed: 9. |
| **T-OBDV2-10** | `T-OBDV2-10_maf_linearity_theoretical_airflow.md` | **done** | — (IAT/MAP present; T-OBDV2-7 done) | COMLab `T-COMV2-MAF-LIN-1` (S4) | **Proposal EP-OBD-11.** w_theo + sensor_error_delta emitted under two-point guard; emitter-only; EP-OBD-11 + T-COMV2-MAF-LIN-1 forward-registered; Stage-2 green. Files changed: 8. |
| **T-OBDV2-11** | `T-OBDV2-11_ltft_load_cell_vector.md` | **done** | — | COMLab `T-COMV2-LTFT-CELL-1` (S4) | **Proposal EP-OBD-12 (LTFT load-cell vector).** ltft_cell_vector ferried (optional, platform-gated); emitter-only; EP-OBD-12 + T-COMV2-LTFT-CELL-1 forward-registered; Stage-2 green. Files changed: 8. |
| **T-OBDV2-PURGE-1** | `T-OBDV2-PURGE-1_dead_classifier_purge.md` | done | — | — (removal) | Files changed: 5 (all deletions). Verification: dead classifier removed; surface intact; suite green. |
| **T-OBDV2-PURGE-2** | `T-OBDV2-PURGE-2_orphan_era_fields.md` | done | — | — (removal) | Files changed: 8 (dna_view + 7 tests building ObdLabDnaView; required-field removal forced the extra test edits). Suite green. |
| **T-OBDV2-PURGE-3** | `T-OBDV2-PURGE-3_fixture_key_cleanup.md` | done | — | — (removal) | Files changed: 5 (fixtures). Verification: emissions and resolved_horizon keys removed from 5 fixtures; JSON valid; suite green. |
| **T-KG-OBD-1** | `T-KG-OBD-1_graphify_ingest_enhanced_wiki.md` | **done** | — | KG artefact — architect KG-query / fault-atlas-design reference (not a schema field) | **KG-lane task.** Brand-new **directed** wiki KG built from the 63 enhanced chunks → `graph/v2_wiki/` (`451 nodes / 494 links / 9 hyperedges / 62 communities`; 408 EXTRACTED / 84 INFERRED / 2 AMBIGUOUS). EXTRACTED spot-check 5/5 green (`P0131→STUCK_LEAN`, `VACUUM_LEAK→DELTA_TRIM`, `TOTAL_TRIM↔STFT/LTFT`, `control_module_voltage_v→COMLab electrical pre-check`). `v2_current`/`v1_baseline` untouched (git + mtime verified); no root-level build. Note: `progress_notes/T-KG-OBD-1.md`. |
| **T-KG-OBD-2-PREP** | `T-KG-OBD-2-PREP_code_prep_obdlab_source.md` | **done** | — | code-map legibility — **no schema field** (field-rule does not bite); each source edit ties to a named graphify Pass-1 consumer (`imports`/`calls` edge set, god-node ranking, type-reference edges) | **Done 2026-06-09.** `4dlab-code-prep` probe/audit/fix/report complete on production `obdlab/` source only. Package version changed to graphifyy `0.8.35`; permitted `C:\tmp\gfx_probe` probe re-derived answers: enum-member=NO → rule E dropped; `# WHY:`=YES and docstring=YES → rules R+D kept. Shipped rule A (`__all__` in `core`/`schemas`) + rule T (`PIDIngestionValidator.__init__ -> None`); I/S clean; C advisory left unchanged as legitimate config DNA-field lookup. Inner loop green: ruff, pyright, pytest `384 passed, 6 skipped`. No real code-map build; no `graph/*` writes. Note: `progress_notes/T-KG-OBD-2-PREP.md`. |
| **T-KG-OBD-2** | `T-KG-OBD-2_graphify_ingest_code_map.md` | **done** | — | code-map artefact — architect/coder repo-navigation (`/graphify query`); separate from the wiki KG | **Done 2026-06-09.** Production-only AST code map built from prepped `obdlab/` source → `graph/v2_code/` (`188 nodes / 492 links / 0 hyperedges / 11 communities`; graphifyy `0.8.35`; directed mode `no`). Scope was 16 `.py` files only: no tests, research, wiki, graph dirs, semantic extraction, or root `graphify update .`. Spot-check 5/5 green (`o2_normalizer`, `translate`, `OBDLivePayload`, `O2FailureMode`, `TrimAnalyticsGate`). `v1_baseline`/`v2_current`/`v2_wiki` untouched; pre-existing `graphify-out/` preserved; no source files changed. Note: `progress_notes/T-KG-OBD-2.md`. |
| **T-KG-OBD-3** | `T-KG-OBD-3_graphify_ingest_test_map.md` | **done** | T-TST-6, T-TST-8 | coverage/traceability queries — **separate graph** from the code map | **Done 2026-06-09.** Separate AST-only test map built from `obdlab/tests/` -> `graph/v2_tests/` (`878 nodes / 1196 links / 0 hyperedges / 61 communities`; graphifyy `0.8.35`; directed mode `no`). Scope was 41 test-side source files only: no production source, research, wiki, other graph dirs, semantic extraction, root graphify rebuild, or `tests/graphify-out/`. Query spot-check green for `SensorSignalTranslator.translate` coverage (`pid_logset`, `regression`, translator import tests), plus `o2_normalizer`, `obdlab_cases.csv`, and generative nodes present. `v1_baseline`/`v2_current`/`v2_wiki`/`v2_code` untouched; pre-existing `graphify-out/` preserved. Note: `progress_notes/T-KG-OBD-3.md`. |
| **T-OBDV2-ARCH-1** | `audit_backlog/T-OBDV2-ARCH-1_ranking_consumer_decision.md` | **done** | — | — (removal; consumer `OBDLabSimple→COMLabSimple` archived, not live) | 🟡 Excise `ranking.py` + `family_map.py` + 3 unit tests (`test_ranking`/`test_classify_top3`/`test_family_map`). Verified: only OBDLab's own tests import them; COMLab fusion takes the full payload, not top-3. **Coupling:** removes `O2FailureMode.DEAD`'s only reader → DEAD becomes orphan; ARCH-2 re-specced after this lands. |
| **T-OBDV2-FIX-1** | `audit_backlog/T-OBDV2-FIX-1_physics_gate_3_dead.md` | **done — Option B** | — | §4 semantic-gate contract → COMLab fault-atlas routing | 🔴 Removed Physics Gate 3 and rely on `FAULT_VE_SENSOR_SKEW` (Option B). 5 files changed. Verification: `pytest` green; `calculated_ve` dead-read grep clean; `pid_case_38` verified. |
| **T-OBDV2-FIX-2** | `audit_backlog/T-OBDV2-FIX-2_wideband_offset_dead.md` | **done** | — | `WIDEBAND_OFFSET_CANDIDATE` → COMLab `T-COMV2-O2OFFSET-1` (already registered) | 🔴 T-OBDV2-6 string→enum migration **missed `o2_normalizer`**; `fuel_status == "Closed_Loop"` always False → T-OBDV2-4 detector dead. Also single-sources the fuel-status map (UB-3). Files changed: 7. |
| **T-OBDV2-FIX-3** | `audit_backlog/T-OBDV2-FIX-3_destate_orchestrator_linearity.md` | **done** | — | `w_theo`/`sensor_error_delta` → COMLab `T-COMV2-MAF-LIN-1` (recompute only) | 🔴 Two-point linearity uses translator **instance state** → `sensor_error_delta` depends on call order; not thread-safe. Thread the prior band explicitly. Files changed: 4. |
| **T-OBDV2-FIX-4** | `audit_backlog/T-OBDV2-FIX-4_number_of_banks_default.md` | **done** | — | bank-2 fields → COMLab (T-OBDV2-BANK-ASYM-1); default-fix only | 🟡 Standardised on default 1 bank across validator, aggregator, and translator. Files changed: 3. |
| **T-OBDV2-FIX-5** | `audit_backlog/T-OBDV2-FIX-5_exception_taxonomy.md` | **done** | — | COMLab fusion error-handling path (run_cases.py / app.py) | 🟡 Unified exception root to `ObdLabError(Exception)` and reparented subclasses. Updated Physics Gate 4 to raise `SemanticConsistencyError`. Files changed: 3. |
| **T-OBDV2-FIX-6** | `audit_backlog/T-OBDV2-FIX-6_dead_code_removal.md` | **done** | (after ARCH-1 if touching ranking) | — (behaviour-preserving) | 🟡 No-op `try/except` in `evaluate` removed; ranking cleanups moot (excised in ARCH-1). Files changed: 2. |
| **T-OBDV2-ARCH-2** | `audit_backlog/T-OBDV2-ARCH-2_orphan_members_proposal_or_prune.md` | **done** | — | per-member (removal) | 🟡 Orphans VERoutingMode, cylinder_count, and O2FailureMode.{SLUGGISH,DEAD,WRONG_CENTERLINE,HEATER_FAULT} pruned. Files changed: 13. |
| **T-OBDV2-FIX-7** | `audit_backlog/T-OBDV2-FIX-7_code_hygiene_bundle.md` | **done** | — | — (internal) | 🟢 Code hygiene bundle (exception chaining, shared thresholds, dead parameter removal, deferred YAML, doc/code alignment). Files changed: 6. |







**Unplanned follow-ups / incidents:** PURGE-1 & PURGE-2 runs invoked `graphify update .` from repo root (regenerated `graphify-out/` ~81.9k nodes) — **violates the no-graph-rebuild rule**; not a deliverable, exclude from commits. Guardrail added to `coding-bootstrap` task template + START_HERE. The per-lab `graph/v2_current/graph.json` was untouched.

| FU | Finding (source: ECU-PERCEPT-1 audit 2026-06-08) | Disposition | Consumer (signal/noise) | Notes |
|---|---|---|---|---|
| **FU-ECU-1** | Docstring field-counts stale after `lambda_perception_delta` added | coder cleanup (bundle with FU-ECU-2 so the inner loop re-runs once) | — (doc-only, non-functional) | `payload.py` module + class docstrings say "21 canonical fields / 15"; surface is now 22. `sensor_signal_translator.py` docstring still says "all 15 canonical fields populated". No behaviour change. |
| **FU-ECU-2** | PID 0x44 `commanded_equivalence_ratio` ingested **unbounded** | follow-up task — owner ratifies the bound first | COMLab `T-COMV2-ECU-FUSE-1` (S4) — a sane commanded-λ is what makes `lambda_perception_delta` meaningful to the fusion verdict | Validator passes 0x44 through with only an `isinstance` numeric check (`pid_ingestion_validator._validate_bounds`); a wild value (e.g. 50.0) yields a garbage delta. Robustness guard, **not** a new emitted field ⇒ not a KG proposal. Proposed range ≈ 0.5–1.5 λ is **indicative only** — pin the exact bound from `OBDLab_KG_Wiki.md` PID 0x44 and add the wiki-citation comment per the numeric-literal rule before it ships. |

**Follow-ups surfaced authoring the T-OBDV2-2…5 pack (2026-06-08):**

| FU | Finding | Disposition | Consumer (signal/noise) | Notes |
|---|---|---|---|---|
| **FU-OBD-ORPHAN-1** | `ve_pct`, `ve_validity`, `o2_failure_mode`, `maf_status`, `map_status` are carried in COMLab `OBDLiveDataPayload` ingestion but **read by no live COMLab path** | named consumers land at Stage 4 (T-OBDV2-2 → `T-COMV2-VE-GATE-1`; T-OBDV2-4 → `T-COMV2-O2OFFSET-1`) — same emit-S2/consume-S4 pattern as ECU-PERCEPT | S4 COMLab readers above | Expected divergence, not a defect; recorded so the Stage-4 anti-orphan grep is scoped. The fields are **not** dropped — they are pre-frozen contract surface. |
| **FU-OBD-DOC-1** | `comlab/comlab/schemas/ingestion.py` lines ~312–316 docstring claims `fault_atlas_router.py` consumes `ve_pct`/`ve_validity`/`o2_failure_mode`/`maf_status`/`map_status` — it does **not** (stale/aspirational) | COMLab-owned doc cleanup (bundle with the S4 VE/O2 consumer tasks so the inner loop re-runs once) | — (doc-only) | Tighten the docstring to the real readers when `T-COMV2-VE-GATE-1` / `T-COMV2-O2OFFSET-1` land. No behaviour change. |
| **O2-FU-2** (re-logged) | `SUPPRESS_POST_CAT_TRIM` is **not** a `TrimAnalyticsGate` value (`o2-logic/06` doc bug) | doc-truth fix, COMLab/wiki-owned | — | Surfaced in research; touched by T-OBDV2-3's Q7 close (logged, not fixed). |
| **O2-FU-3** (re-logged) | O₂-delta stress band inconsistent (2500 vs 3500–4500 RPM across chunks) | research-doc reconciliation | — | Surfaced in research; relevant to the wideband-offset persistent-band guard (T-OBDV2-4). Log only. |
| **FU-OBD-DOC-2** | `vocabulary.py` L52 comment mismatch ("VE > 85%" vs 90.0 constant) | doc comment fix (stale comment) | — (doc-only) | Comment mismatch, actual threshold is 90.0. Fix when next touching `vocabulary.py`. |

**Status values:** `pending` · `pending (research-gated)` · `in_progress` · `done` · `blocked` · `deferred` · `void`.
**Research-gated** = authored intent + named consumer, but **not coder-runnable** until its audit
questions are answered and T-OBDV2-0 = `revive`. The architect authors runnable scope at that point;
the coder never writes the spec (owner authoring model).
**Audit answers (2026-06-08):** all 10 OBDLab audit questions are answered in
`research/AUDIT_ANSWERS_OBDLab.md`. The research gate is **closed** — ECU-PERCEPT-1 (Q1/Q4) and
BANK-ASYM-1 (Q2/Q6) are now runnable specs with pinned bounds.

> **Sequencing note:** OBDLab emits only its *own* channels (trims, O₂, perception-delta). The cross-lab
> *verdicts* (ecu_fault, bank-asymmetry) are COMLab **fusion** products built last — OBDLab is never
> blocked on COMLab, and COMLab consumes OBD's frozen-contract output at Stage 4
> (`CROSS_LAB_SEQUENCING.md` §2).
