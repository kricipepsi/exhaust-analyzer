# COMLab v2 — Progress Ledger (Stage 4, LAST)

**Lab:** COMLab — the prune→rank decision/fusion spine (`labs/comlab/README.md`) · **Build stage:** 4 (reworked **last**).
**Cross-lab forward registry:** `labs/comlab/docs/CROSS_LAB_DEPENDENCIES.md` (the source of record for every DEP row).
**Mode:** STRICT (both gates clean before `done`). **Last updated:** 2026-06-21 (architect, Cowork: **reconciled the `T-COMV2-LAMBDAPROJ-1` "contract gap" report** — investigated and rejected; the CoC λ fields ARE present upstream at top level, the task is a pure path re-point and stays `pending`/runnable, NOT blocked; fixed the genuinely-stale `DEP-4` row in `CROSS_LAB_DEPENDENCIES.md` + the spec's Step-1 pointer — see "LAMBDAPROJ contract-gap reconciliation" below). Prior: 2026-06-21 (architect, Cowork: **authored the Stage-4 closeout pack** — `T-COMV2-LAMBDAPROJ-1` (FU-4) + `T-COMV2-FATAL-1` `pending` on disk; activated `T-GV2-2` (gaslab) + authored registry `REG-V2-CHEMSIG-34` (FU-1) + `REG-WIKI`; deferred backlog documented — see "Stage-4 closeout pack" below). Prior: 2026-06-21 (architect, Cowork: **authored the cross-lab consumer-closer pack** — the final 2 cross-lab consumer rows flipped `deferred → pending` with specs on disk: `O2OFFSET-1`, `NOSTART-1` (DEP-7/DEP-8). Both emitter halves are now `done` (`T-OBDV2-4`+`-FIX-2`; `T-DTCV2-NOSTART-1`+`-FIX`), so these close the **last** Stage-4 cross-lab anti-orphan gaps — see "Cross-lab consumer-closer pack" below; the prior "O2OFFSET blocked on T-OBDV2-4 pending" note was stale). Prior: 2026-06-21 (coder: `T-COMV2-ECU-HW-1` done — optional IAT/TPS mirrors + default-off coherent ECU hardware-lie evidence; 488 passed, 4 skipped; ruff/pyright clean). Prior: 2026-06-21 (coder: `T-COMV2-FUELSYS-GATE-1` done — optional OBD-live loop-state mirror + default-off open-loop trim-evidence gate; 472 passed, 4 skipped; ruff/pyright clean). Prior: 2026-06-21 (coder: `T-COMV2-VE-GATE-1` done — dual-sensor VE evidence + single-sensor circularity withholding, 200% mirror drift fixed; 463 passed, 4 skipped; ruff/pyright clean). Prior: 2026-06-21 (architect, Cowork: **authored the perception/gate pack** — the 4 remaining unblocked S4 consumer rows flipped `deferred → pending` with specs now on disk: `ECU-FUSE-1`, `VE-GATE-1`, `FUELSYS-GATE-1`, `ECU-HW-1`; added wiki §2a "ECU-hardware digital-lie signature" band, a `ve_pct` mirror-drift fix, and corrected the `comlab-fusion-consumer` skill's stale "these 4 already have a live reader" note — see "Perception/gate pack" + the out-of-band table below). Prior: 2026-06-21 (architect, Cowork: **authored the orphan-closer pack** — 6 deferred forward-registered rows flipped `deferred → pending` with specs now on disk: `BANK-FUSE-1`, `VPWR-GATE-1`, `MAF-LIN-1`, `LTFT-CELL-1`, `MISFIRE-LOC-1`, `CTXMOD-1`; authored on-demand skill `_comlab_skills/comlab-fusion-consumer` and registered it in `_INDEX.md` — see "Orphan-closer pack" below). Prior: 2026-06-21 (stale-ledger reconciliation on the DELTA chain — see "Ledger reconciliation" below; no task rows changed) + wired `_comlab_skills` Load-skills lines into the remaining runnable tasks. Prior: 2026-06-19 (architect: added COMLab research pack — see below; no task rows changed). Prior: 2026-06-08 (forward-registered DEP-2/DEP-3, then DEP-6/7/8 from the T-OBDV2-2…5 pack, then DEP-9 input-field consumers from the proposal-audit promotions T-OBDV2-6/7).

## Research pack (audit 2026-06-03 — COMLab leg)

Answers to the COMLab Part 3 questions and the Part 1 ceiling diagnosis live in `labs/comlab/research/` (index: `labs/comlab/research/README.md`). Part 3 **Q2/Q6/Q9/Q10** and all of **Part 1** are answered internally; the open external gaps are three project-agnostic web-research prompts (**A** scoring+fusion = Q1/Q3/Q4, **B** calibration+differential+symptom prior = Q5/Q7/Q8, **C** corpus quality+label noise = Part 1 Culprit 3). Read before authoring the Stage-4 specs above — they set the achievable-accuracy target (Q2) and the fusion/ranker direction the rows below implement.

## What this ledger is

COMLab is built **last**, so most of its rows are **forward-registered consumers** of emitter halves shipped
by GASLab/OBDLab/DTCLab at earlier stages. Registering them here now keeps those emitted fields **un-loseable**
and satisfies the anti-orphan gate: per `CROSS_LAB_DEPENDENCIES.md §Gates`, at **Stage-4 close every emitted
field must be `grep`-confirmed read by its named fusion consumer** — these rows are those named consumers.
Full task specs are authored when COMLab's rework starts (Stage 4); until then the rows are placeholders with
named inputs, not runnable.

## Task log — Stage-4 fusion consumers

| ID | Task file | Status | Blocked by (emitter halves) | Consumes (signal/noise inputs) | Notes |
|---|---|---|---|---|---|
| **T-COMV2-ECU-FUSE-1** | `tasks/T-COMV2-ECU-FUSE-1_ecu_perception_reality_fuse.md` (**authored 2026-06-21**) | `done` — verification + review recorded 2026-06-21 | `T-OBDV2-ECU-PERCEPT-1` (OBD perception, **done**) · `T-GV2-6d` (GAS reality, **done**) | OBD `lambda_perception_delta` + bank symmetry (`total_trim_correction_delta` vs `total_trim_correction_delta_b2`) + GAS `lambda_chem` | **DEP-2.** Fuses ECU perception vs gas reality → the `ecu_fault` verdict (OBD/GAS emit halves; COMLab judges). This is the **named reader** that closes anti-orphan on `lambda_perception_delta` (and finally consumes the today-orphaned `_b2` symmetry) at S4. OBD research gate Q1/Q4 **closed** (`obdlab/research/AUDIT_ANSWERS_OBDLab.md`). |
| **T-COMV2-BANK-FUSE-1** | `tasks/T-COMV2-BANK-FUSE-1_per_bank_asymmetry_verdict.md` (**authored 2026-06-21**) | `done` — verification + review recorded 2026-06-21 | `T-OBDV2-BANK-ASYM-1` (OBD per-bank, **done**) | OBD `per_bank_trim_delta` + vehicle identity (2-bank) | **DEP-3.** Applies the **±5 %** asymmetry bound (Q2) + pre-2001 confidence caveat (Q6) to the OBD delta → bank-asymmetry verdict. Named reader that closes anti-orphan on `per_bank_trim_delta` at S4. OBD research gate Q2/Q6 **closed**. Single-bank engines emit `None` upstream → no verdict. |
| **T-COMV2-VE-GATE-1** | `tasks/T-COMV2-VE-GATE-1_ve_evidence_circularity_gate.md` (**authored 2026-06-21**) | `done` — verification + review recorded 2026-06-21 | `T-OBDV2-2` (OBD already emits the signals, **done**) | OBD `ve_pct` + `ve_validity` + `air_metering_strategy` (+ `maf_status`/`map_status`) | **DEP-6.** Treats a VE fault as **independent evidence only when `air_metering_strategy == DUAL_MAF_MAP_CROSSCHECK`** (Q5); single-air-sensor VE is circular → routes to **P0068 MAF/MAP/TPS rationality + IAC/idle-MAP**, not VE. Named reader that closes the `ve_pct`/`ve_validity` orphan at S4. OBD research gate Q5 **closed**. |
| **T-COMV2-O2OFFSET-1** | `tasks/T-COMV2-O2OFFSET-1_wideband_offset_confirm.md` (**authored 2026-06-21**) | `done` — verification + review recorded 2026-06-21 | `T-OBDV2-4` (OBD `WIDEBAND_OFFSET_CANDIDATE`, **done**) · `T-GV2-6d`/`T-GV2-3` (GAS `lambda_chem`, **done**) | OBD `o2_failure_mode == WIDEBAND_OFFSET_CANDIDATE` + GAS `lambda_chem` | **DEP-7 · proposal `EP-OBD-17`.** Confirms the OBD candidate against gas-truth λ (stoich band 0.97–1.03 per wiki/02) → promotes the `sensor_fault` family (wideband-calibration); inert when gas reads a real lean/rich. `o2_failure_mode` already mirrored (`ingestion.py:402`) → **reader-only** orphan-closer. OBD research gate Q9 **closed**; emitter `T-OBDV2-4`(+`-FIX-2`) **done** (the prior "blocked on T-OBDV2-4 pending" note was stale). |
| **T-COMV2-NOSTART-1** | `tasks/T-COMV2-NOSTART-1_no_start_branch.md` (**authored 2026-06-21**) | `done` — verification + review recorded 2026-06-21 | `T-DTCV2-NOSTART-1` (+`-FIX`, DTCLab `MONITOR_ABORTED` + `ff_fuel_spark_cut_at_crank`, **done**) | DTCLab `Mode06MonitorState.MONITOR_ABORTED` + FF `ff_fuel_spark_cut_at_crank` | **DEP-8 · proposal `EP-DTC-NOSTART-1`.** fault_atlas **no-start branch**: (MONITOR_ABORTED + FF fuel/spark-cut) → **security-lockout (`ERR-NS-005`) vs mechanical (`ERR-NS-001/2/3/4`)** routing. Mirrors **both** orphaned signals (the missing enum value + the missing FF flag) then wires the reader. **CAN-era gated at the emitter** (router request has no VinDNA → COMLab does not re-gate). Audit Q8 **closed**. |
| **T-COMV2-FUELSYS-GATE-1** | `tasks/T-COMV2-FUELSYS-GATE-1_fuel_system_status_gate.md` (**authored 2026-06-21**) | `done` — verification + review recorded 2026-06-21 | `T-OBDV2-6` (OBD `fuel_system_status` field, **done**) | OBD `fuel_system_status` (CL/OL/OL_DRIVE/OL_FAULT) | **DEP-9 · proposal `EP-OBD-IN-03`.** Stage-A gate: down-weight/abort trim routing when not closed-loop; reads the raw status + the CL→OL_FAULT-across-RPM Δ-signature. OBD's internal `OPEN_LOOP` gate already consumes loop state; this is the **COMLab-facing** reader. Owner must-have (RQ-D). |
| **T-COMV2-ECU-HW-1** | `tasks/T-COMV2-ECU-HW-1_ecu_hardware_lie_checker.md` (**authored 2026-06-21**) | `done` — verification + review recorded 2026-06-21 | `T-OBDV2-7` (OBD `intake_air_temp_c` + `throttle_pos_pct`, **done**) · `T-OBDV2-ECU-PERCEPT-1` (**done**) | OBD `intake_air_temp_c` + `throttle_pos_pct` + `coolant_temp_c` + bank symmetry | **DEP-9 · proposals `EP-OBD-IN-08`/`EP-OBD-IN-05` (+ `EP-COM-04`).** ECU-hardware-fault checker: the **named consumer** ECU-PERCEPT deferred TPS/IAT to. Reads the Mode-4 digital-lie signature (IAT/ECT/TPS = −40/−40/100) + railed-trim/bank-symmetry → internal-ECU fault nodes. |
| **T-COMV2-VPWR-GATE-1** | `tasks/T-COMV2-VPWR-GATE-1_rail_health_precheck.md` (**authored 2026-06-21**) | `done` — verification + review recorded 2026-06-21 | `T-OBDV2-8` (OBD `control_module_voltage_v`, **done**) | OBD `control_module_voltage_v` (+ `ΔVPWR`) | **DEP-10 · proposal `EP-OBD-IN-04` (+`EP-FA-05`).** Electrical-health pre-check in `perception_contradiction`: suppress/down-weight sensor-fault routing when rail `<12.0 V`/`>15.0 V`; `ΔVPWR` signatures feed the alternator-AC-ripple node. Rules out a bad rail before blaming air/fuel sensors. |
| **T-COMV2-MISFIRE-LOC-1** | `tasks/T-COMV2-MISFIRE-LOC-1_misfire_localiser_gate.md` (**authored 2026-06-21**) | `done` — verification + review recorded 2026-06-21 | `T-OBDV2-9` (OBD misfire counts, **done**) | OBD `per_cylinder_misfire_counts` | **DEP-9 · proposal `EP-OBD-IN-07`.** misfire localiser: reads the counts to separate single-cylinder fault from global starvation, feeds `misfire_vs_fuelling` gate. |
| **T-COMV2-MAF-LIN-1** | `tasks/T-COMV2-MAF-LIN-1_maf_linearity_ladder.md` (**authored 2026-06-21**) | `done` — verification + review recorded 2026-06-21 | `T-OBDV2-10` (OBD MAF linearity, **done**) | OBD `w_theo` + `sensor_error_delta` | **DEP-11 · proposal `EP-OBD-11`.** reads `w_theo` and `sensor_error_delta`, applies the 5–12 / >12 % ladder, routes to / sharpens `ERR-LC-002` vs open-circuit `P0102`. OBD research gate closed (new wiki `pids-protocol/05`). |
| **T-COMV2-LTFT-CELL-1** | `tasks/T-COMV2-LTFT-CELL-1_load_cell_classification.md` (**authored 2026-06-21**) | `done` — verification + review recorded 2026-06-21 | `T-OBDV2-11` (OBD load-cell vector, **done**) | OBD `ltft_cell_vector` | **DEP-12 · proposal `EP-OBD-12`.** reads `ltft_cell_vector`, classifies idle-only / part-throttle-only / global, feeds `fault_atlas_router` family selection. OBD research gate closed (new wiki `fuel-trim/13`). |
| **T-COMV2-CTXMOD-1** | `tasks/T-COMV2-CTXMOD-1_symptom_prior_context_modifier.md` (**authored 2026-06-21**) | `done` — verification + review recorded 2026-06-21 | `T-DNA-2` (symptomlab `load_state`, **done**) | SymptomLab `load_state` | **DEP-13 · proposal `COMLab-B`.** Consume `SymptomDNA.environmental_conditions.load_state` as context modifier for the COMLab symptom prior and cap symptom-prior weighting at 65% trust. |
| **T-COMV2-DELTA-1** *(EPIC — not directly assignable)* | `tasks/T-COMV2-DELTA-1_cross_lab_delta_module.md` (**authored 2026-06-19 · split into 1A–1D 2026-06-20**) | `done` — 1A–1D closed 2026-06-20; **Gate-1 still gates live value** | two-point capture (Gate-1, product) + emitter two-point emission (not yet) | per-state frames at low + elevated idle → `delta_signature` (ΔTrim/Δgas/ΔO₂) | **proposal `COMLab-DELTA` · closes OBDLab FU-2 · DEP-14.** Default-off v1 consumer is live in Phase 5; single-point path regression-locked. Live activation remains a separate Gate-1 follow-up. |
| **T-COMV2-DELTA-1A** | `tasks/T-COMV2-DELTA-1A_schema_foundations.md` (**authored 2026-06-20**) | `done` — verification + review recorded 2026-06-20 | — (first in chain) | `SINGLE_POINT` mode + `DegradationLit` widen + `SecondOperatingPointFrame` + request field; registers `COMLab-DELTA` | **1/4.** Inert input surface, default-`None`; proposal-bounded consumer completed in 1D. |
| **T-COMV2-DELTA-1B** | `tasks/T-COMV2-DELTA-1B_engine_models_and_gates.md` (**authored 2026-06-20**) | `done` — 23-test engine suite green 2026-06-20 | 1A schema models | `delta_engine.py` output models + architecture/validity gates + single-point sentinel | **2/4.** Standalone pure-math gates verified before wiring. |
| **T-COMV2-DELTA-1C** | `tasks/T-COMV2-DELTA-1C_engine_profiles.md` (**authored 2026-06-20**) | `done` — 23-test engine suite green 2026-06-20 | 1B engine skeleton | `_delta_trim`/`_delta_gas`/`_delta_o2`/`_assemble` + profile/abstain fixtures (`delta-relations` wiki-cited) | **3/4.** Per-signal bands and ABSTAIN-on-mismatch verified. |
| **T-COMV2-DELTA-1D** | `tasks/T-COMV2-DELTA-1D_router_wiring.md` (**authored 2026-06-20**) | `done` — consumer/read + e2e gates green 2026-06-20 | working engine (1C) + request field (1A) | `enable_delta` flag + Phase 5 read (`max(score, conf)`) + aggregator thread + e2e | **4/4.** Consumer meets field and closes signal/noise. Default-off; single-point byte-identical; trusted two-point fixture promotes the target family and emits `delta_signature_applied`. |
| **T-REG-REVIVE-1** | `tasks/T-REG-REVIVE-1_registry_revival_cleanup.md` (**authored 2026-06-21**) | `done` — verification + review recorded 2026-06-21 | — | revived `labs/comlab/registry/` (canonical; ARCHIVE copy is stale) | Registry import root cleaned; stale bytecode purged; empty `ignition_fault` stub removed; manifest==rules assertion live; docs relocated; COMLab 378 passed + registry 470 passed; ruff/pyright clean. `T-COMV2-DELTA-2` unblocked. |
| **REG-V2-AUTHOR-ignition_fault** | `tasks/REG-V2-AUTHOR-ignition_fault.md` (**authored 2026-06-21**) | `done` — verification + review recorded 2026-06-21 | `T-REG-REVIVE-1` deletes the empty stub first | 3 corpus cases (`EXP-N026`, `CASE-035`, `case_036`) + e2e `ERR-IF-001` | **Author the missing v2-registry rule** for spark-generation failure. 3 rules (IF-001 coil-driver, IF-002 knock-weak-spark, IF-003 late-timing). EXP-N026 + CASE-035 flip to ignition_fault (confirmed on executed v2 router). case_036 blocked: requires base ≥ 0.75 on POA_SIGNATURE/no-DTC rule which would cannibalize all POA_SIGNATURE families. 943 passed, ruff/pyright clean. |
| **T-COMV2-DELTA-2** | `tasks/T-COMV2-DELTA-2_v2_registry_delta_activation.md` (**authored 2026-06-20**) | `done` — verification + review recorded 2026-06-21; Gate-1 still gates live value | `T-COMV2-DELTA-1D` (**done**) + `T-REG-REVIVE-1` (**done**); Gate-1 open (live value) | `delta_signature` → v2-registry `scored_rules` re-rank (prod default `USE_V2_REGISTRY=1`) | **proposal `COMLab-DELTA-V2` · DEP-14.** Independent default-off `enable_delta_v2` gate is live on the production-default path; shared `DeltaEngine` policy keeps v1/v2 parity. Flag-off, single-point, band-mismatch, speed-density null, and forced-induction inversion are regression-locked. COMLab 387 passed + registry 471 passed; ruff/pyright clean. |



## Test-suite harness pack (`T-COMTST-*`) — authored 2026-06-20

**Python: 3.14 ONLY** — run every `python`/`pytest` via the repo sandbox interpreter `.sandbox-py/bin/python3.14` (3.14.5). Do **not** use system `python3` (3.10 → `StrEnum` ImportError) or any 3.11/3.12/3.13; no mixing. If a stale `__pycache__/*.pyc` shadows an edit, purge `__pycache__` before re-running.

The COMLab lab-local test harness the emitter labs already have (`descriptor.py` + `<lab>_cases.csv` + `test_cases.py` + generative + `regression/`). **Closes the reserved `T-TST-10` "comlab harness" placeholder** referenced in the skipped generative stubs. COMLab-specific shape: **no master-row projection script** — COMLab consumes the four labs' *verdicts* (`ingestion.py`), so the fixture is assembled upstream payloads; full-chain master-row eval lives in `apps/wired/harness/` (`T-TH-12`) and is not duplicated. **Accuracy/scoring is out of this pack** — it is gated on Phase-0 **F1** (registry consolidation) + **GATE_DATA** per `wiki/12_corpus_eval_discipline.md`.

| ID | Task file | Status | Blocked by | Date | Commit | Verification | Notes |
|---|---|---|---|---|---|---|---|
| `T-COMTST-1` | `T-COMTST-1_descriptor_verdict_fixtures.md` | done | — | 2026-06-21 | — | descriptor categorical (`15` fields, `boxes=0`) + `comlab_cases.csv` 24 rows load; 387 passed | Real categorical descriptor, assembled Gas/OBD/DTC/SymptomDNA verdict cases, healthy round-trip, GAS_DOMINANT and invalid-input coverage. |
| `T-COMTST-2` | `T-COMTST-2_csv_characterization_net.md` | done | `T-COMTST-1` | 2026-06-21 | — | 24 characterization cases passed; full suite 411 passed, 6 skipped | `tests/test_cases.py` characterization net (no-crash + schema-valid + fail-closed; records observed verdict). |
| `T-COMTST-3` | `T-COMTST-3_generative_combinatorial_fuzz.md` | done | `T-COMTST-1` | 2026-06-21 | — | generative combinatorial+fuzz un-skipped and green; 12 passed; T-TST-10 reservation closed | Categorical product: 192 cases; malformed/sentinel fuzz: 11 cases. |
| `T-COMTST-4` | `T-COMTST-4_regression_golden_pin.md` | done | `T-COMTST-2` | 2026-06-21 | — | 7 regression fixtures pinned; regression 8 passed; full suite 431 passed, 4 skipped; negative control verified | Current verdict drift detector covers FULL_FUSION, GAS_DOMINANT, 4 routed families, and malformed-input contract rejection. |

## Other Stage-4 consumer obligations (detail in `CROSS_LAB_DEPENDENCIES.md`)

These are already registered in the cross-lab table; listed here so the S4 ledger is complete. Specs authored at Stage 4.

| ID | Dep | Consumes | Status |
|---|---|---|---|
| `T-GV2-2` + `FU-1` | DEP-1 | `ChemicalSignature` 34-value mirror + registry `schema_v2` 32→34 + `cam_timing.json` | **specs authored + activated 2026-06-21** — `T-GV2-2` `pending` (gaslab ledger) + `REG-V2-CHEMSIG-34` `pending` (registry ledger); **pair-land** (consistency guard) |
| `FU-4` | DEP-4 | `projection.py`/`lab_dna_views.py` λ in/out reconcile (`target_lambda_v112`, `co_high_idle`) | **spec authored 2026-06-21** → `T-COMV2-LAMBDAPROJ-1` (`pending`, closeout pack below) |
| `T-RMW-MIRROR` | DEP-5 | wired type-mirror isolation (local mirrors of lab types) | **void 2026-07-07 (T-SHIP-4)** — stale: the 34-value mirror is live (`comlab/schemas/vocabulary.py:241`, verified 34 members) and `WRONG_VALVE_TIMING` has no live reference; wired crosses via JSON + entry-point imports per D-V2-9, no 30-value mirror exists. Strict type-mirror isolation remains out of scope unless owner requests (D-V2-9). |

## Ledger reconciliation — 2026-06-21 (architect, Cowork)

The stale-ledger guard tripped at the `T-COMTST-4` pickup: the DELTA notes
(`T-COMV2-DELTA-1`/`1A`/`1B`/`1C`/`1D`, all `done`) recorded **2 failing tests**.
Those were the **known-red `registry`-package import failures** snapshotted on
2026-06-20 (registry package broken at the time) — **not** failures in COMLab delta
code. They were fixed downstream by `T-REG-REVIVE-1` (registry 470 passed) and
`T-COMV2-DELTA-2` (COMLab 387 + registry 471 passed), both `done` 2026-06-21.
**Re-verified 2026-06-21** (`../../.sandbox-py/bin/python3.14` 3.14.5):
`pytest -q` → **417 passed, 10 skipped, 0 failed**; `pytest registry/tests/ -q` →
**471 passed**. The DELTA rows are correctly `done`; a reconciliation footer was
appended to each of the five DELTA progress notes. **`T-COMTST-4` is unblocked.**

## Orphan-closer pack — 2026-06-21 (architect, Cowork)

Six forward-registered consumer rows promoted `deferred → pending` (specs authored):
`BANK-FUSE-1`, `VPWR-GATE-1`, `MAF-LIN-1`, `LTFT-CELL-1`, `MISFIRE-LOC-1`, `CTXMOD-1`.
**Why these six:** each consumes an emitted field with **zero live COMLab reads today**
(`per_bank_trim_delta`, `control_module_voltage_v`, `w_theo`/`sensor_error_delta`,
`ltft_cell_vector`, `per_cylinder_misfire_counts`, `load_state`) — the genuine Stage-4
anti-orphan gaps. Each spec is one shape: **mirror the emitted field at the emitter's
exact type → wire its named reader behind a default-off flag → prove the read with two
greps.** New on-demand skill `_comlab_skills/comlab-fusion-consumer` captures that shape
(registered in `_INDEX.md`; named on each task's Load-skills line). Manager assigns one;
the guard picks the first `pending` row top-to-bottom (`BANK-FUSE-1` **done 2026-06-21**; next pending = `VPWR-GATE-1`). **Not promoted**
(still `deferred`): `ECU-FUSE-1`/`VE-GATE-1`/`FUELSYS-GATE-1`/`ECU-HW-1` (their fields
already have a live reader → "verify-what-exists" specs, a separate pack), `O2OFFSET-1`
(blocked: `T-OBDV2-4` pending), `NOSTART-1` (DTC cross-stage). *(Update 2026-06-21: all four perception/gate
rows shipped `done`; `O2OFFSET-1`+`NOSTART-1` since promoted to `pending` once their emitters landed — see
"Cross-lab consumer-closer pack" below. This note is the point-in-time orphan-closer snapshot.)*

## Perception/gate pack — 2026-06-21 (architect, Cowork)

The four remaining unblocked S4 consumer rows promoted `deferred → pending` (specs authored):
`ECU-FUSE-1`, `VE-GATE-1`, `FUELSYS-GATE-1`, `ECU-HW-1`. **Correction to the orphan-closer note:**
those rows had been deferred as "verify-what-exists (fields already have a live reader)", but a code
read shows otherwise — `ecu_hardware_checker.py` is an **empty stub** (`pass`), there is **no live
COMLab read** of `fuel_system_status` (OBD-live), `ve_pct`/`ve_validity`, or `total_trim_correction_delta_b2`,
and the `ecu_fault` verdict does not exist yet. The "live reader" the prior note meant was OBD-**internal**
(in the obdlab package), not a COMLab-side reader, so from COMLab's anti-orphan view these are genuine
orphan-closers of the same router-reader shape as the six already shipped. Each spec: **mirror the emitted
field at the emitter's exact type → wire its named reader behind a default-off flag → prove the read with
two greps.** Only `ECU-FUSE-1` carries a "verify the existing perception-axis read first" half (the
`perception_contradiction.detect` divergence is already live; it adds the `ecu_fault` discrimination on top
and consumes the orphaned `_b2`). Manager assigns one; the guard picks the first `pending` row
top-to-bottom. **Still deferred** (not in this pack): `O2OFFSET-1` and `NOSTART-1` — **since promoted to `pending`
2026-06-21 in the "Cross-lab consumer-closer pack" below** once their emitters landed `done` — and the registry-side
rows `T-GV2-2`+`FU-1` / `FU-4` / `T-RMW-MIRROR` (registry/wired boundary, still deferred).

## Cross-lab consumer-closer pack — 2026-06-21 (architect, Cowork)

The **final two** cross-lab consumer rows promoted `deferred → pending` (specs authored): `O2OFFSET-1`, `NOSTART-1`.
**Why these two now:** both were forward-registered consumers blocked on an emitter half; both emitter halves have since
landed `done` — `T-OBDV2-4`(+`T-OBDV2-FIX-2`) emits `O2FailureMode.WIDEBAND_OFFSET_CANDIDATE`, and
`T-DTCV2-NOSTART-1`(+`-FIX`) emits `Mode06MonitorState.MONITOR_ABORTED` + `ff_fuel_spark_cut_at_crank` — so they are
genuinely runnable. They are the **last** cross-lab consumer orphans (DEP-7, DEP-8); closing them completes the
Stage-4 anti-orphan gate for every cross-lab emitted field. Same fusion-consumer shape (load `comlab-fusion-consumer`),
both default-off, evidence-not-override, two-grep anti-orphan gate:
- **`O2OFFSET-1`** is **reader-only** — `o2_failure_mode` is already mirrored (`ingestion.py:402`); it only wires the
  Phase-5 `sensor_fault` promote (`_resolve_o2_sensor_fault`, the symbol `EP-OBD-17` already names).
- **`NOSTART-1`** mirrors **two** missing signals first (add `MONITOR_ABORTED` to `Mode06Status`; add
  `ff_fuel_spark_cut_at_crank` to COMLab `FreezeFrameRecord`), then wires the Phase-5 no-start branch
  (security `ERR-NS-005` vs mechanical `ERR-NS-001/2/3/4`). CAN-era is already gated at the emitter; the router request
  carries no VinDNA (`ingestion.py:452`), so COMLab does **not** re-gate on era.

Manager assigns one; the guard picks the first `pending` row top-to-bottom (both rows sit in the Stage-4 table above).
**Not in this pack** (no cross-lab consumer left to close): the registry/wired-boundary rows `T-GV2-2`+`FU-1` / `FU-4` /
`T-RMW-MIRROR` — a separate registry-reconciliation pack.

## Stage-4 closeout pack — 2026-06-21 (architect, Cowork)

The remaining **runnable** Stage-4 reconcile/production tasks, authored so the coder
queue stays full behind the cross-lab consumer-closers. These are **not** cross-lab
fusion consumers (no `comlab-fusion-consumer`) — they close known divergences /
reach dead-but-tested code. Load the mandatory 3 skills only.

| ID | Task file | Status | Type | Notes |
|---|---|---|---|---|
| **T-COMV2-LAMBDAPROJ-1** | `tasks/T-COMV2-LAMBDAPROJ-1_dna_view_lambda_reconcile.md` (**authored 2026-06-21**) | `done` — verification + review recorded 2026-06-21 | contract reconcile (FU-4 / DEP-4) | `projection.py::project` reads `target_lambda_v112`/`co_high_idle` from the wrong `VinDNA` level → `GasLabDnaView` gets `None`. Re-point per proposal `vehicle-dna-projection-paths` (`entries.yaml:251`). Closes DEP-4. No flag (bug-fix), regression-tested. |
| **T-COMV2-FATAL-1** | `tasks/T-COMV2-FATAL-1_fatal_gate_wiring.md` (**authored 2026-06-21**) | `done` — verification + review recorded 2026-06-21 | production wiring | `process()` (`:356`) calls `route_symptom` directly, never `run_fatal_gates_and_routing()` (`:235`) → no reachable `FATAL_INCOMPLETE` verdict. Wire it behind default-off `enable_fatal_gates`, add a `FATAL_INCOMPLETE` output builder, update the `T-COMTST-4` pin. Closes the "fatal terminal wiring" follow-up. |

### LAMBDAPROJ contract-gap reconciliation — 2026-06-21 (architect, Cowork)

A coder pickup of `T-COMV2-LAMBDAPROJ-1` reported a **contract gap** and recommended marking the
row `blocked` on an upstream `T-DNA-*` (claim: `target_lambda_v112`/`co_high_idle`/`co_low_idle` are
"absent from `VinDNA` at any level"). **Investigated — false positive. The row stays `pending`/runnable.**

- The claim inspected `comlab/schemas/ingestion.py::VinDNA` (a Pydantic model). That model is **off the
  projection path** — `project()` is dict-based (`vehicle_dna_json["vin_dna"]`, `projection.py:51`) and
  never imports/validates through it. So its field set is irrelevant to what the projection reads.
- The **upstream source COMLab mirrors** — `labs/vinlab/vinlab/models.py::VinDNA` — declares all three
  CoC fields at **top level** (`:228/:231/:232`) and parses them from the **top level** of the payload
  (`payload.get("target_lambda_v112")` … `:301/:304/:305`); only equipment flags sit under nested
  `emissions`. The DNALab fixture (`labs/dnalab/tests/conftest.py:59–63`) confirms the same JSON shape.
- Therefore the raw `vin_dna` dict the projection receives **does carry** these at top level. The defect
  is exactly the proposal's `from → to`: `projection.py:79–81` reads `emissions.get(...)` (wrong key) →
  always `None`. **Fix = re-point to `vin.get(...)`. Pure path correction, no schema change, no upstream
  block** — precisely the spec's "What to build §1".

The spec's Step-1 pointer (which sent the coder to the off-path Pydantic mirror) has been corrected, and
`CROSS_LAB_DEPENDENCIES.md` DEP-4 (which still read "divergent until S4") now points at this runnable task.

**Companion specs authored same day in sibling ledgers** (this pack's cross-package partners):
`T-GV2-2` (COMLab `ChemicalSignature` 32→34 mirror — **activated `pending`** in `gaslab/tasks/PROGRESS.md`) and
`REG-V2-CHEMSIG-34` / **FU-1** (registry `schema_v2` 32→34 — **`pending`** in `registry/docs/REGISTRY_PROGRESS.md`).
These two **pair-land** (the cross-package `ChemicalSignature` consistency guard checks both enum sets). And
`REG-WIKI` (registry HTML case library) — spec written, `pending` in the registry ledger.

### Remaining backlog — deferred, NOT authored (and why)

Per the bootstrap discipline (don't author blocked/owner-decision/runaway tasks), these are **not** turned into
coder specs yet:

- **`T-RMW-MIRROR`** (DEP-5, wired type-mirror isolation) — the `apps/wired` app is stuck at
  `ChemicalSignature==30` (two splits behind); isolating its lab-type imports *and* a 30→34 reconcile is bigger
  than one half-session and belongs to the **wired** workstream's own ledger. Needs a wired-side scoping pass first.
- **F1 — registry consolidation** (`global_fault_registry.json` ↔ REG-V2 shim, `wiki/12 §CONCEPT_PHASE0`) — a
  Phase-0 architecture decision gated on **GATE_DATA**; owner call, not a mechanical task.
- **Additive-vs-Bayesian ranker rework** (ROADMAP Stage-4 open question) — gated on F1 + GATE_DATA; authoring it
  now is the V1 weight-nudging anti-pattern.
- **DELTA Gate-1 live activation** (`enable_delta`/`enable_delta_v2` default-on) — gated on a two-point **capture**
  product gate, not coder-runnable (corpus is single-point today).
- **Registry coverage gaps** — `case_046-P0190` (needs a pressure-sensor KG node), `EXP-N023` (needs richer OBD
  capture), `charging-system-alternator-gap` (needs a DTCLab wiki update for P0620–P0626 first). All blocked upstream.
- **Doc-syncs (architect out-of-band, not coder tasks)** — `FU-2` (`OBD_VOCABULARY §17` 32→34), the
  `REG-V2-INTEGRATE-SPEC-PATCH` text edit, `COMLAB-WIKI-DRIFT-DTC-OBD` (a T-DOC/commit-hygiene item).
- **case_036** (ignition_fault) — known-blocked; the real lever is CF-001 anchor-gating, folded into the scoring
  rework, not a one-case patch (see the `REG-V2-AUTHOR-ignition_fault` note).

- **Stage-4 complexity & clone debt (pyscn/deptry sweep, 2026-06-29)** — `fault_atlas_router`
  complexity (cc 144 / cog 785; `route` 31) + undeclared `opentelemetry` in `observability/`; address during
  this lab's rework, not before (D-V2-9: refactor after contracts freeze). Full inventory (incl. VINLab core
  duplication + deptry false-positive caveats): `planning/code_audit/STAGE4_COMPLEXITY_INPUTS.md`. Not coder-runnable now.

## Architect-level out-of-band patches

Wiki/skill edits applied directly by the architect (not via a coder task):

| Date | File | Change | Why |
|---|---|---|---|
| 2026-06-21 | `wiki/02_lab_input_contract.md` | Added **§2a "ECU-hardware digital-lie signature"** band — COMLab-local thresholds for `T-COMV2-ECU-HW-1` (IAT/ECT −40 °C floor + TPS 100 % rail + railed, bank-symmetric trim → `ecu_fault`). | Single-lab isolation: the ECU-HW checker cites a COMLab-local band, never `obdlab/research/` at diagnostic time. Mirrors how the orphan-closer pack added §2a bands. |
| 2026-06-21 | `_comlab_skills/comlab-fusion-consumer/SKILL.md` + `_INDEX.md` | Corrected the stale "Not for `ECU-FUSE-1`/`VE-GATE-1`/`FUELSYS-GATE-1`/`ECU-HW-1` — those already have a live reader" note; added the four to the When-to-load table (with the ECU-FUSE "verify-existing-read first" caveat). | The claim was inaccurate (see "Perception/gate pack"); these four ARE fusion-consumer tasks of the same shape, so they load the skill. |
| 2026-06-21 | `T-COMV2-VE-GATE-1` spec + implementation | Flagged and fixed the `ve_pct` mirror drift: COMLab `OBDLiveDataPayload.ve_pct` widened from `le=100.0` to the emitter's `le=200.0` thermal-shock range; added the optional `SessionMetadata.air_metering_strategy` DNA token consumed by the VE gate. | Type/bounds fidelity to the emitter is the JSON-contract source of record (fusion-consumer skill §1); both additive input-contract changes are default-compatible and regression-tested. |
| 2026-06-21 | `progress_notes/REG-V2-AUTHOR-ignition_fault.md` + `COMLAB_TASKS_START_HERE.md` | Normalised the note's opening header `## Scope` → `## Plan` (content was already the plan-at-top); clarified the stale-ledger-guard wording to accept `## Plan` / `## Scope Confirm` / `## Plan / Scope Confirm` as equivalent plan-at-top headings. | A coder pickup tripped the guard on the bare `## Scope` heading (both gate blocks were present and clean — a heading-convention mismatch, not a real gap). 7 other `done` notes already use `## Scope Confirm`; the clarification stops the literal-"Plan" check from re-tripping on them. Architect normalises the heading; the coder correctly did not silently fix. |
| 2026-06-21 | `wiki/02_lab_input_contract.md` | Added **§2a `{#CONCEPT_OBD_CONSUMER_BANDS}`** — COMLab-local mirror of the MAF/VPWR/LTFT/misfire bands (v2.0→v2.1). | **Single-lab isolation:** a consumer reads thresholds from the COMLab wiki, never reaches into `obdlab/research/` at diagnostic time (an upstream lab may not run — no DTC → no DTCLab). The 4 specs now cite §2a; the OBD chunk is provenance-only. |
| 2026-06-21 | `_comlab_skills/comlab-fusion-consumer/SKILL.md` | Added the "Single-lab isolation" section + repointed the bands citation to §2a. | Bake the isolation invariant into the skill that gates the orphan-closer pack. |
| 2026-06-21 | `T-COMV2-BANK-FUSE-1` spec + note | Resolved coder blocker: `model_year` → `resolved_horizon == HORIZON_LEGACY`; fixed the pre-2001 cite (wiki/04 §CONCEPT_LEGACY). | Router carries `resolved_horizon`, not `model_year`; the original cite was the ADAPTIVE row. (BANK-FUSE-1 subsequently shipped `done`.) |
| 2026-06-21 | `wiki/11_two_point_delta.md` | Added **§CONCEPT_DELTA_BANDS** — COMLab-local mirror of every numeric DELTA profile band (ΔTrim/Δgas/architecture/validity/confidence) now in `delta_engine.py` (v2.0→v2.1). | Same single-lab isolation, applied to the `done` DELTA engine: its thresholds had a source of truth only in `obdlab/research/delta-relations/*`. The `delta-relations/NN` tags remain as per-row provenance. |

## Unplanned follow-ups
- **`T-COM-CAMTIMING-MAF-1` (deferred — forward-registered 2026-06-28, Cowork):** add `_MAF`-variant
  cam-timing registry rules so MAF-equipped vehicles route. T-GV2-2 retired `WRONG_VALVE_TIMING` and
  re-pointed both existing cam-timing rules (`ERR-CT-001` chain-stretch, `ERR-CT-003` VVT full-retard)
  in `comlab/config/global_fault_registry.json` to `CAM_TIMING_RETARDED_MAP` (owner-approved minimal
  re-point). GASLab emits `CAM_TIMING_RETARDED_MAF` for MAF-air-metered cars and `CAM_TIMING_ADVANCED`
  for advanced phasing — neither has a registry rule yet, so those cases currently fall through the
  cam-timing family. Add `ERR-CT-001b`/`ERR-CT-003b` (keyed on `CAM_TIMING_RETARDED_MAF`) and decide
  whether `CAM_TIMING_ADVANCED` needs its own rule. Surfaces in wired `T-WIRE-2` if a MAF cam case is run.

- **COMLab fatal terminal wiring:** `COM-013` is rejected at Pydantic ingestion,
  while the rows labeled `fatal_incomplete` currently emit non-fatal verdicts.
  `LabPipelineAggregator.process()` does not call
  `run_fatal_gates_and_routing()`, so the harness has no reachable
  `FATAL_INCOMPLETE` UI output to pin. Author a separate production task before
  changing this behavior; `T-COMTST-4` pins the current contract rejection only.

- **DELTA code-comment repoint (optional, comment-only):** `delta_engine.py` (+ `ingestion.py`,
  `response.py`, `vocabulary.py`) carry ~30 `# wiki: delta-relations/NN` provenance comments
  pointing into `obdlab/research/`. The bands are now mirrored COMLab-local in
  `wiki/11 §CONCEPT_DELTA_BANDS`, so these could be repointed to `COMWIKI-11` (keeping the
  `delta-relations/NN` as parenthetical provenance). Deferred — comment-only, no behavior change,
  on a regression-locked `done` module; fold into the next DELTA-touching task rather than churn
  it alone. Runtime isolation already holds (no cross-lab import); this is cosmetic provenance.

## Notes / guardrails

- **OBDLab is never blocked on COMLab.** The OBD emitter halves ship at Stage 2 under the frozen contract and
  are independently green there; "divergent-until-consumer" is acceptable until S4 (`CROSS_LAB_SEQUENCING.md §2`).
- **No cross-lab Python imports.** COMLab mirrors each lab's types locally (README boundary rule).
- **Anti-orphan is a Stage-4-close gate**, not a per-row blocker: a field emitted at S2 with its consumer
  forward-registered here is compliant; the `grep`-confirm runs when these specs are authored + built at S4.

**Status values:** `pending` · `in_progress` · `done` · `blocked` · `deferred` · `void`.

**Runnability convention (so the stale-ledger guard and the manager-assigns-one-task workflow stay aligned):**
`pending` means **genuinely runnable now** — spec authored, dependencies met. A forward-registered row whose
task file is not yet authored (`_authored at S4_`) carries **`deferred (forward-registered · S4 — spec unauthored;
author when assigned)`**, NOT `pending`. Promote `deferred → pending` only when its spec is authored and its
blockers are `done`. Therefore the guard may safely treat **the first `pending` row top-to-bottom as the next
runnable task**; `deferred`/`blocked` rows are skipped. (Do not reintroduce a `pending (forward-registered)`
status — that string is what made the guard pick unauthored placeholders.)
