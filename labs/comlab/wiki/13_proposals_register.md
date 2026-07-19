---
chunk_id: COMWIKI-13
title: "Proposals Register — signal/noise consumers & code paths"
doc: COM_WIKI
version: v2.0
date: 2026-06-20
status: authoritative
summary: "The consolidated signal/noise register for COMLab v2: every new field/fault/flag this wiki introduces, its named consumer + code path, its proposal ID, and lifecycle status. Mirrors comlab/config/proposals/ and the tasks/PROGRESS.md fusion-consumer rows."
entities_defined: [CONCEPT_PROPOSAL_REGISTER, CONCEPT_GRADUATION]
related_chunks: [COMWIKI-02, COMWIKI-08, COMWIKI-10, COMWIKI-11]
sources: [comlab/config/proposals/{README,proposals,entries}.yaml, tasks/PROGRESS.md, AGENTS.md rule 4]
---

# Proposals Register — signal/noise consumers & code paths

Per `AGENTS.md` rule 4, a new field/fault ships only with a **named consumer + code path**, and
v2-new tokens are registered as **proposals** (in `comlab/config/proposals/`, never silently in
the live KG). This chunk is the wiki-side index of those proposals; the YAML files are the
machine-readable source.

## Lifecycle {#CONCEPT_GRADUATION}

```
[ proposed ]            →  [ pinned ]               →  [ graduated ]
consumer named,            live reader exists in        passes T-SEM-4 gate,
registered in YAML         the codebase                 merged into live registry
```

All entries carry a **dual ISO/SAE citation**: DTC-relevant → `ISO 15031-6 §<clause> / SAE J2012
— <P-code>`; PID-relevant → `ISO 15031-5 §<clause> / SAE J1979 — <PID>`.

## A. Stage-4 fusion consumers (forward-registered) {#CONCEPT_PROPOSAL_REGISTER}

These are the named readers that turn emitted emitter-halves into fused verdicts (`COMWIKI-08`).
Status `pending (forward-registered · S4)` until specs are authored + built at Stage 4. DEP rows
trace to `v2-restructure/CROSS_LAB_DEPENDENCIES.md`.

| Consumer (task ID) | Consumes | Code path | Proposal / DEP |
|---|---|---|---|
| T-COMV2-ECU-FUSE-1 | OBD `lambda_perception_delta` + `_b1`/`_b2` symmetry + GAS `lambda_chem` | `fault_atlas_router.py` | DEP-2 |
| T-COMV2-BANK-FUSE-1 | OBD `per_bank_trim_delta` (±5 % bound) | `fault_atlas_router.py` | DEP-3 |
| T-COMV2-VE-GATE-1 | OBD `ve_pct`/`ve_validity`/`air_metering_strategy` | `fault_atlas_router.py` | DEP-6 |
| T-COMV2-O2OFFSET-1 | OBD `o2_failure_mode == WIDEBAND_OFFSET_CANDIDATE` + GAS `lambda_chem` | `fault_atlas_router.py:_resolve_o2_sensor_fault` | DEP-7 · `EP-OBD-17` |
| T-COMV2-NOSTART-1 | DTC Mode-06 monitor-aborted (MID $A1/TID $53) + FF cut-state | `fault_atlas_router.py` | DEP-8 · `EP-DTC-NOSTART-1` |
| T-COMV2-FUELSYS-GATE-1 | OBD `fuel_system_status` (CL/OL/OL_DRIVE/OL_FAULT) | `fault_atlas_router.py` | DEP-9 · `EP-OBD-IN-03` |
| T-COMV2-ECU-HW-1 | OBD `intake_air_temp_c`+`throttle_pos_pct`+`coolant_temp_c`+bank symmetry | `ecu_hardware_checker.py:ECUHardwareChecker` | DEP-9 · `EP-OBD-IN-08`/`-05`, `EP-COM-04` |
| T-COMV2-VPWR-GATE-1 | OBD `control_module_voltage_v` (+ ΔVPWR) | `perception_contradiction.py:detect` | DEP-10 · `EP-OBD-IN-04`, `EP-FA-05` |
| T-COMV2-MISFIRE-LOC-1 | OBD `per_cylinder_misfire_counts` | `fault_atlas_router.py` | DEP-9 · `EP-OBD-IN-07` |
| T-COMV2-MAF-LIN-1 | OBD `w_theo` + `sensor_error_delta` | `fault_atlas_router.py` | DEP-11 · `EP-OBD-11` |
| T-COMV2-LTFT-CELL-1 | OBD `ltft_cell_vector` | `fault_atlas_router.py` | DEP-12 · `EP-OBD-12` |
| T-COMV2-CTXMOD-1 | SymptomLab `load_state` (cap 65 % trust) | `symptom_router.py` / `fault_atlas_router.py` | DEP-13 · `COMLab-B` |
| T-COMV2-DELTA-1 | two-point frames → `delta_signature` (ΔTrim/Δgas/ΔO₂) | `analytics/delta_engine.py` → `fault_atlas_router.py` Phase 5 | `COMLab-DELTA` (closes OBDLab FU-2) |

## B. COMLab-owned EP-* proposals (in `proposals.yaml`)

| ID | Family | Consumer (code path) | Status |
|---|---|---|---|
| `EP-COM-05` | cross-cutting | `perception_contradiction.py:detect` (semantic-coherence) | proposed |
| `EP-COM-04` | P06XX | `ecu_hardware_checker.py:ECUHardwareChecker` | proposed |
| `EP-COM-06` | cross-cutting | `fault_atlas_router.py:FaultAtlasRouter._discriminator_table` (signature matrix) | proposed |
| `EP-COM-15` | cross-cutting | `tests/integration/test_truth_perception.py:test_cases` (truth-perception corpus) | proposed |
| `COMLab-A` | symptom-prior-routing | `fault_atlas_router.py:FaultAtlasRouter` (tier_1/tier_2 → fault-family keys) | proposed |
| `COMLab-B` | symptom-prior-routing | `T-COMV2-CTXMOD-1` (`load_state` context modifier) | proposed |
| `COMLab-DELTA` | cross-lab-delta | `analytics/delta_engine.py` (`T-COMV2-DELTA-1`) | proposed · Gate-Capture-gated |
| `COMLab-OIL-KG-NODES` | fault-atlas-kg | `proposals/entries.yaml` (5 oil-burn nodes, proposal-only) | proposed · live verdict stays MW-001..003 |

## C. v2-new tokens introduced by this wiki

Each names its consumer in the same change (no orphans):

| Token (chunk) | Consumer | Status |
|---|---|---|
| provenance flags (`COMWIKI-02` `CONCEPT_PROVENANCE`) | eval harness + Stage-A gates + calibration split | proposal · ships with Gate-Data |
| freeze-frame as conditional evidence (`COMWIKI-02`) | `T-COMV2-NOSTART-1` + fusion intermittent-fault branch | proposal · `EP-DTC-NOSTART-1` |
| `delta_signature` / Δ noise floors / abstain set (`COMWIKI-11`) | `analytics/delta_engine.py`, `tests/unit/test_delta_engine.py` | proposal · `COMLab-DELTA` |
| posterior/LR confidence tiers (`COMWIKI-09`) | `schemas/vocabulary.py` tier defs + calibrator | proposal · ships with Gate-Data |
| top-k differential as primary output (`COMWIKI-10`) | `schemas/response.py` `DifferentialSiblingOut` (already emitted) | pinned-on-build |

## Inherited / cross-lab proposals consumed here

`EP-DTC-02` (graduated, taxonomy backbone), `EP-DTC-01`, `EP-OBD-14`, plus the OBD input-field
promotions (`EP-OBD-IN-*`). See `proposals.yaml` for the authoritative list and owning ledgers.

## High-risk index (from the engine proposal §9)

| HR | Conflict | Mapped proposals |
|---|---|---|
| HR-1 | sensor_fault component-vs-system | `EP-COM-05`, `EP-COM-04`, `EP-OBD-14`, `EP-OBD-17` |
| HR-2 | lean/rich cross-layer drift | `EP-COM-05`, `EP-COM-03`, `EP-COM-15` |
| HR-3 | VVT/cam_timing strategy separation | `EP-COM-06`, `EP-DTC-02` |

## Graph relations (explicit)

**13 fusion consumers** REGISTERED_IN **tasks/PROGRESS.md** AS **named readers** (anti-orphan)
**EP-\* / COMLab-\* proposals** REGISTERED_IN **comlab/config/proposals/** (never live KG)
**CONCEPT_GRADUATION** proposed → pinned → graduated VIA **T-SEM-4 gate**
**provenance flags / posterior tiers / delta_signature** ARE **v2-new tokens** WITH **named consumers**

## Core Entities

- **CONCEPT_PROPOSAL_REGISTER** — Register of v2-new proposal tokens and config definitions. Consumer: `comlab/config/proposals/ (proposed)`.
- **CONCEPT_GRADUATION** — Proposed-to-graduated lifecycle gating via T-SEM-4. Consumer: `COMLab lifecycle`.
