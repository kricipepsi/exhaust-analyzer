# wired-v7 — Progress Ledger (research-built accuracy suite)

**Pack goal:** research the owner's curated **case libraries**, select the cases
**viable for the current wired engine**, and build a fresh **CSV test suite
(`cases_petrol_v7.csv`)** + oracle + driver + report — configured to **catch every
error class the engine can produce** (mis-route, wrong family/code, wrong state,
confidence drift, perception-gap/demotion error, crash, bad-input mishandling). The
suite is named **v7** to distinguish it from the legacy v6 corpus.

**Hard rule — NO OLD ARTEFACTS, fresh from current code state.** Do **not** port,
clone, or read the `ARCHIVE/wired/harness/` driver or the legacy
`cases_petrol_master_v6.csv` (old 60-rule stack, dead `use_v2_registry=` kwarg,
old-taxonomy oracle). Inputs, oracle, and driver are rebuilt.

**Authorized external source (owner-provided, read-only):**
`/home/m/Desktop/casesextra/` — the curated case libraries. **Primary:**
`cases_library_v2.html` (best coverage; cases by root-cause category —
Mechanical / ECU / Sensor / Fuel / Ignition / Emissions — with 5-gas physical-truth
+ OBD-trim tables, tiered confidence, truth-vs-perception gates, and a Missing-Cases
coverage index). **Secondary:** `cases_library.html`, `cases_library_research.html`,
and the curated CSVs (`cases_petrol_era_v1.csv`, `cases/cases_petrol_master_v5.csv`).
The omp coders read this path **natively**; do **not** copy raw library files into the
repo — only the derived `cases_petrol_v7.csv` + citations land in-tree.

**Three load-bearing decisions (read before authoring/coding):**
1. **Oracle = domain truth, not engine output.** Expected verdicts are pinned from
   the lab wikis (rule 2) + current taxonomy
   (`labs/comlab/comlab/schemas/vocabulary.py`, `core/fault_atlas_kg.py`),
   corroborated by the library's documented conclusions — **never** from
   `diagnose()`'s own output (that would make the suite tautological). Cases the wiki
   cannot pin are tagged **characterization / no-crash**, excluded from the accuracy %.
2. **Coverage is the design target ("catch all possible errors").** The suite must
   cover **every reachable fault family** + the negative/edge/invalid classes, and
   score **multiple verdict dimensions** (family, code, state, confidence band,
   perception-gap, demotion-note, crash/abort) — not just the top fault.
3. **Incomplete cases are quarantined, never fabricated.** If a library case lacks an
   input the current contract requires, it goes on the `INCOMPLETE_CASES` list for the
   **owner** to research/fill — the coder does not invent sensor values (signal/noise).

**Tasks dir:** `apps/wired/v7_tasks/` · **Fresh code/data home:** `apps/wired/v7/`
**Mode:** STRICT (dual-gate: VERIFICATION GATE + CODE REVIEW)
**Reads on boot:** `apps/wired/v7_tasks/WIRED_V7_START_HERE.md`
**Last updated:** 2026-06-30 (GLM — T-V7-9 done: same-ruler v1-vs-v2 baseline established; v2 47.96% vs v1-proxy 8.50% family routing, 0 regressed families, 93 v1-crashes on DTC-less input logged as F-V7-V1-DTC-DEREF; tune-or-revert unblocked)

Keep under ~120 lines; bulk gate notes go in `v7_tasks/progress_notes/<id>.md`.

---

## Pre-pack gate

| Item | State | Evidence |
|---|---|---|
| wiring + single-case verification done | **done** | `apps/wired/WIRED_PROGRESS.md` (T-WIRE-*) + `apps/wired/test_tasks/TEST_PROGRESS.md` (T-WTEST-1..5) |
| full suite GREEN baseline | **done** | `apps/wired/test_tasks/reports/WTEST1_BASELINE_2026-06-30.md` (1991 passed) |
| trace tooling reusable | **done** | `apps/wired/trace/` (reuse for the optional traced suite mode) |
| owner case libraries reachable | **yes** | `/home/m/Desktop/casesextra/cases_library_v2.html` (+ siblings) |


## Failure-localization pack close-out

| Report | Role |
|---|---|
| `apps/wired/fl_tasks/reports/FL_YARDSTICK_2026-06-30.md` | Frozen v3 yardstick: 133/294 = 45.24% as-pinned family+state; 143/294 = 48.64% adjudicated. |
| `apps/wired/fl_tasks/reports/FL_UPSTREAM_2026-06-30.md` | Per-case GASLab/OBDLab upstream states for all 314 rows. |
| `apps/wired/fl_tasks/reports/FL_LOCALIZATION_2026-06-30.md` | Per-case failure mode and first-divergence target list for v3. |
| `apps/wired/fl_tasks/reports/FL_SCOREBOARD_README_2026-06-30.md` | One-command before/after scoreboard; v3 acceptance command. |

## Task log

| ID | Task file | Status | Blocked by | Date | Commit | Verification | Notes |
|---|---|---|---|---|---|---|---|
| T-V7-1 | `T-V7-1_library_research_and_viability.md` | done | — | 2026-06-30 | 4564a62 | CLEAN: report + progress gates | Wrote `reports/V7_1_RESEARCH_2026-06-30.md`; 314 viable CSV candidates, 22 CSV incomplete (`gas.nox`), 2 source-level incomplete, all reachable families covered; `ignition_fault`/`non_starter` low-support. |
| T-V7-2 | `T-V7-2_build_v7_csv.md` | done | T-V7-1 | 2026-06-30 | owner-run pending | CLEAN: --validate passes | Wrote `v7/data/cases_petrol_v7.csv` and `v7/load_corpus.py`. Mapped 314 viable cases (259 v5, 55 era_v1). Dynamic O2 voltages and OBD/FF defaults mapped. |
| T-V7-3 | `T-V7-3_rederive_oracle.md` | done | T-V7-2 | 2026-06-30 | owner-run pending | CLEAN: verify + validate passes | Filled expected_* oracle columns for all 314 cases, fully vocabulary-compliant, validated against FaultAtlasKG. Created ORACLE_TRIAGE_2026-06-30.md. |
| T-V7-4 | `T-V7-4_driver_and_multidim_scorer.md` | done | T-V7-3 | 2026-06-30 | 033f4e3 | CLEAN: tests + full smoke run | Wrote `v7/run_suite.py` and `v7/tests/test_run_suite.py`; full corpus executed 314/314, wrote untracked `v7/runs/20260630_161827/results.json`, reported 0 crashes and per-dimension failures. |
| T-V7-5 | `T-V7-5_run_coverage_accuracy_report.md` | done | T-V7-4 | 2026-06-30 | owner-run pending | CLEAN: suite 314/314, report written | Ran full corpus (run `20260630_163900`): 0 crashes, 0/294 overall accuracy gated by two single-root defects (`fault_code` ID-namespace 294/294, `confidence` saturation 273/294); **48.0 % family routing** is the real signal. Wrote `reports/V7_ACCURACY_2026-06-30.md`; 10 follow-ups logged below. |
| T-V7-6 | `T-V7-6_jaeger_full_corpus_trace.md` | done | — | 2026-06-30 | owner-run pending | CLEAN: 314/314 traced, 0/314 verdict diffs, 12/12 families REST-checked | Ran full corpus under `--trace` (run `20260630_190651`); verdicts byte-identical to untraced `20260630_163900` (0 diffs, 0 crashes). Trace verdict: **every §5 cluster + dead-routing family diverges at `phase.rank`** (`threshold_miss=False`, `candidates_out=1` on 294/294; 0 prune wipeouts). Wrote `reports/V7_TRACE_2026-06-30.md`; cross-linked V7_ACCURACY §6; raw JSON gitignored. READ-ONLY on engine. |
| T-V7-7 | `T-V7-7_investigate_fault_code_namespace.md` | done | — | 2026-06-30 | owner-run pending | CLEAN: READ-ONLY memo, both gates clean | READ-ONLY investigation by GLM. Wrote `reports/V7_CODE_NS_DECISION_2026-06-30.md`. **Recommendation = Option B**: the v2 default path emits the short `rule_id` (`MF-001`); no live consumer depends on the `ERR-` prefix for named faults; the 73 v2 `rule_id`s are globally unique (0 collisions); there is **no** short→`ERR-` resolution (v2 path bypasses the KG — passthrough-default enrichment). Re-pin the oracle `expected_fault_code` to short for **named-fault rows only** — KEEP `ERR-ABORT-*` abort rows and `OPTIMAL_HEALTH` (a blanket `s/^ERR-//` would corrupt the abort rows). Zero engine change. Separate defect surfaced: v2 orphans KG `fault_enrichment` → suggest `F-V7-ENRICH-ORPHAN`. **Awaiting owner sign-off** to author the `F-V7-CODE-NS` fix task. |
| T-V7-8 | `T-V7-8_investigate_confidence_semantics.md` | done | — | 2026-06-30 | owner-run pending | CLEAN: READ-ONLY memo, both gates clean | READ-ONLY investigation by GLM. Wrote `reports/V7_CONF_DECISION_2026-06-30.md`. **Recommendation = Option B** (oracle reband): `confidence_score` is a **bounded additive evidence-accumulation rank score** (`base_weight + 0.10/DEFINITIVE + 0.05/SUGGESTIVE`, clamped at `min(confidence_ceiling,1.0)`) — **not** a calibrated posterior; the wiki (`09_calibration_confidence.md`) states the calibration layer is an **unbuilt rework** gated on a Gate-Data subset that does not yet exist, current numbers being "expert-set priors, flagged as such". Saturation ≥0.95 is therefore **by design** (ceiling = "evidence complete", not "100% certain"). Re-pin oracle `expected_confidence_*` to the live scorer's **per-family** distribution (run `20260630_163900`), **named-fault rows only** — KEEP `ERR-ABORT-*`/`OPTIMAL_HEALTH`/`no_fault` bands (same discipline as T-V7-7). Zero engine change, zero consumer/threshold impact (only hard gate is the 0.70 tier-label step; no continuous-probability consumer). Memo also corrects the task's pinned fact: L2204 is the legacy assembly; v7 runs the v2 shim (`integration_shim.py:792`) — both raw-passthrough, conclusion unchanged. **Awaiting owner sign-off** to author the `F-V7-CONF-SAT` fix task. Option A (engine calibration) split out as `F-V7-CONF-CALIB` (deferred — gated on Gate-Data). |
| T-V7-9 | `T-V7-9_v1_baseline_on_v7_suite.md` | done | — | 2026-06-30 | owner-run pending | CLEAN: v1 proxy 25/294 fam (93 crashes) vs v2 141/294 (0 crashes); toggle changes 263/314 | Ran the suite under `USE_V2_REGISTRY=0` vs default `=1` (runs `20260630_205310`/`20260630_205235`, git-excluded). Step 0 fidelity: engine v1-native `global_fault_registry.json` is 98/100 byte-identical to `/home/m/Desktop/4dV1` archived copy → **HIGH**-fidelity proxy. **Same-ruler result: v2 routes 141/294 = 47.96% family vs v1 proxy 25/294 = 8.50% (+116, +39.5 pts); 0 regressed families, 8 improved, 4 unchanged (the dead-routing + ecu_fault families already open). v1 crashes 93× `AttributeError 'NoneType' has no attribute 'confirmed_dtcs'` (unguarded DTC-less deref — recorded, not patched). v2 reproduces T-V7-5's 48.0%. Wrote `reports/V7_V1_BASELINE_2026-06-30.md`; logged `F-V7-V1V2` + `F-V7-V1-DTC-DEREF`. READ-ONLY engine. |

**Status values:** `pending` · `in_progress` · `done` · `blocked` · `deferred`
**Runnability:** `pending` = runnable now (blockers `done`). **No `pending` rows remain**
— all T-V7-1..9 are `done`. The engine/oracle *fix* tasks for `F-V7-CODE-NS` and
`F-V7-CONF-SAT` are **not yet authored** — they wait on owner sign-off of the
[[V7_CODE_NS_DECISION_2026-06-30]] (Option B: oracle re-pin to short, named-faults-only)
and [[V7_CONF_DECISION_2026-06-30]] (Option B: oracle reband to per-family distribution)
memos. Routing fix tasks (`F-V7-ECU-ROUTE`/`F-V7-DEAD-ROUTE`/`F-V7-SENSOR-MISS`) wait on
the T-V7-6 trace pass (done). **T-V7-9** established the same-ruler baseline
([[V7_V1_BASELINE_2026-06-30]]): 0 regressed families → tune-or-revert is now unblocked
and should target the 4 unchanged families, not a v1 revert.

---

## Unplanned follow-ups

Logged by T-V7-5 from the full-corpus run (`runs/20260630_163900`). Hypotheses, not
verdicts — owner/architect dispositions. Detail + evidence in
`reports/V7_ACCURACY_2026-06-30.md` §4–§7.

| ID | Discovered in | One-liner | Status |
|---|---|---|---|
| F-V7-CODE-NS | T-V7-5 | verdict `fault_code` (`MF-001`) ≠ canonical KG id (`ERR-MF-001`); 294/294 code-dim FAIL — engine-bug or oracle-correction (P0, gates accuracy %) | **investigated → T-V7-7**: **Option B (oracle re-pin to short)** recommended, awaiting owner sign-off. Named-fault rows → short `rule_id`; `ERR-ABORT-*` abort rows + `OPTIMAL_HEALTH` kept. Memo: `reports/V7_CODE_NS_DECISION_2026-06-30.md`. |
| F-V7-CONF-SAT | T-V7-5 | `confidence_score` saturates ≥0.95 (172 cases =1.0) vs mid-band oracle windows; 273/294 FAIL (P0) | **investigated → T-V7-8**: **Option B (oracle reband to the live scorer's per-family distribution)** recommended, awaiting owner sign-off. `confidence_score` is a bounded additive rank score, not a calibrated posterior; wiki says calibration layer is unbuilt (gated on Gate-Data). Re-pin `expected_confidence_*` per-family, named-fault rows only; KEEP abort/`OPTIMAL_HEALTH`/`no_fault` bands. Zero engine change. Memo: `reports/V7_CONF_DECISION_2026-06-30.md`. |
| F-V7-CONF-CALIB (new) | T-V7-8 memo | engine-side post-hoc calibration layer (wiki `COMWIKI-09` B.Q1): Platt/temperature map fused score → calibrated posterior; redefine tiers as posterior bands. This is **Option A** of the T-V7-8 memo — the real architectural fix. | **deferred** — gated on the Gate-Data measured-real eval subset (`COMWIKI-12`) which does not yet exist; calibration on synthetic labels is "meaningless" per the wiki. Large blast radius (every verdict + 0.70 gate + tier label). Author only after Gate-Data lands; do NOT block the v7 suite on it (the Option B reband unblocks accuracy %). |
| F-V7-ECU-ROUTE | T-V7-5 | `ecu_fault` routing dispersed (4/31) across lean/rich/sensor/catalyst (P1) | open |
| F-V7-DEAD-ROUTE | T-V7-5 | dead routing: `exhaust_leak` 0/10, `mechanical_wear` 0/14, `non_starter` 0/5 never selected (P1) | open |
| F-V7-SENSOR-MISS | T-V7-5 | `sensor_fault → no_fault` (6) under-detection / missed fault (P1) | open |
| F-V7-PGAP | T-V7-5 | perception_gap mismatch 100/294 (O2-bias verdict presence vs oracle) (P2) | open |
| F-V7-FATALGATE | T-V7-5 | 3 invalid cases (`CASE-043`,`RULE-NOx-1`,`YAML-PDF_HI_007`) not aborted though oracle expects `fatal_incomplete` (P2) | open |
| F-V7-STATE | T-V7-5 | 19 `state`-dim FAIL — fault/no-fault boundary (P3) | open |
| F-V7-DEMOTE | T-V7-5 | 5 `demotion_note_contains` substring drift (P3) | open |
| F-V7-V1V2 | T-V7-9 | same-ruler v1-vs-v2 baseline: **0 regressed families**; v2 +116 cases (+39.5 pts, 8.50%→47.96% family routing). Tune/revert targets = the 4 unchanged families (`ecu_fault`,`exhaust_leak`,`mechanical_wear`,`non_starter`) already open as `F-V7-ECU-ROUTE`/`F-V7-DEAD-ROUTE`. No "revert to v1" path improves routing. (P1, gates tune-or-revert) | **reported → [[V7_V1_BASELINE_2026-06-30]]**: baseline established; tune-or-revert now unblocked. |
| F-V7-V1-DTC-DEREF | T-V7-9 | v1 native path crashes 93× on DTC-less input: `AttributeError 'NoneType' has no attribute 'confirmed_dtcs'` (unguarded `dtc_lab_output.confirmed_dtcs` deref; v2 registry shim guards it). Engine-side v1-path defect. (P2) | open — surfaced, NOT patched (OUT of T-V7-9 scope); engine fix = its own spec if owner activates. |

## Owner action queue (incomplete cases needing research)

Cases the libraries reference but that lack an input the current contract needs.
Populated by T-V7-1/T-V7-2; the **owner** fills these, then the case re-enters the corpus.

| Case ref | Library source | Missing essential input | Status |
|---|---|---|---|
| case_012 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_024 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_025 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_026 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_029 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_030 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_031 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_032 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_033 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_035 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_036 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_037 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_038 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_039 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_041 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_042 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_043 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_045 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_047 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_048 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_049 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| case_050 | `cases/cases_petrol_master_v5.csv` | `gas.nox` required by live `_run_gaslab` | owner-fill |
| RESEARCH-REAL-006 | `cases_library_research.html §3` | missing actual measured retarded-timing-rich case row: 5-gas, OBD trims/DTC, citation | owner-fill |
| V2-ECU-GROUND-OFFSET | `cases_library_v2.html ECU / Electronic` | missing simultaneous sensor readings, control-module voltage, trims, DTC/freeze-frame if present | owner-fill |

---

## Deferred (named for later)

| ID | Item | Why deferred |
|---|---|---|
| T-V7-SKILL | a `wired-v7-accuracy` on-demand skill (CSV schema + multi-dim scoring contract) | author once T-V7-2..4 settle the schema |
| T-V7-CI | gate the suite in CI with a per-family + per-error-dimension floor | needs a first measured baseline (T-V7-5) |

---

## Architect-level out-of-band patches

| Date | File | Patch | Reason |
|---|---|---|---|
| 2026-06-30 | `apps/wired/v7_tasks/**` | Re-keyed the fresh accuracy pack v6→**v7**; pointed it at the owner case libraries (`casesextra/cases_library_v2.html`); made the deliverable a CSV; added multi-dimension error-catching scoring + an incomplete-case owner queue. | Owner directive: research the curated libraries, build a v7 suite for the current code state that catches all error classes. |
| 2026-06-30 | `v7_tasks/T-V7-6..8`, ledger, `.agent/assignments.md` | Audited T-V7-5 run (verified both P0 root causes against engine source + KG ids + run JSON; confirmed Jaeger pass never ran). Authored **T-V7-6** (full-corpus Jaeger `--trace`), **T-V7-7**/**T-V7-8** (READ-ONLY P0 investigations). Did **not** author engine/oracle fixes. | Owner dispositioned both P0s *investigate-first* and the trace pass *full 314-case*. Fixes gate on the memos + sign-off; routing fixes gate on the trace. |
