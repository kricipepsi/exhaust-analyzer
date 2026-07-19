# GAS Lab Wiki — v2.1 Timing-Taxonomy Revision

**Date:** 2026-06-03
**Scope:** petrol 1990–2010 (Euro 1–5) — unchanged. No post-2010 / Euro 6–7 "modern-era" signatures were added.
**Source ingested:** `docs/GASLab/q1&7/Advanced Engineering Analysis of Petrol Engine Timings (1990–2010).md` (the one document missed in the v2 update).
**Trigger:** user request to seat five timing states as first-class entries, with new enum + fault records ("apply this semantic across all labs later").

## What changed

The single cam-timing value `WRONG_VALVE_TIMING` was **retired** and replaced by three system-specific states. The two ignition-timing values were retained (their numbers already matched the source) and retitled for the five-state family. Contract surface **32 → 34**.

| # | Timing state (as requested) | `chemical_state` | Status |
|---|---|---|---|
| 1 | Over-Advanced Ignition Timing | `TIMING_OVER_ADVANCED` | retained, retitled, cross-linked |
| 2 | Retarded Ignition Timing | `TIMING_RETARDED` | retained, retitled, cross-linked |
| 3 | Retarded Cam Timing (MAP System) | `CAM_TIMING_RETARDED_MAP` | **new** |
| 4 | Retarded Cam Timing (MAF System) | `CAM_TIMING_RETARDED_MAF` | **new** |
| 5 | Advanced Cam Timing (Both Systems) | `CAM_TIMING_ADVANCED` | **new** |

Design choices (surfaced, not assumed):

- **`dna_gate: none`** on all three cam states. There is no DNA field for MAF-vs-MAP air metering (only `fuel_delivery_type`); inventing one would add a field with no consumer (signal/noise violation). The MAP-vs-MAF distinction rides the gas-direction discriminator (Speed-Density → rich; MAF → lean), corroborated by OBD trims (OBDLab).
- **`match_class: SPECIFIC`** (not DEFINITIVE). Tailpipe gas cannot prove cam *phase*; that needs CKP/CMP correlation (OBDLab/DTCLab). `RULE_WVT` was retargeted accordingly.
- **Named consumer (per architecture constraint):** all three route to COMLab `chemical_state` / fault-atlas (GASWIKI-06B). Gas vectors are transcribed verbatim from the source 5-gas signature table.

## Files touched (deliverables)

- `q1&7/…Timings (1990–2010)_prepped.md` + `_PREP_REPORT.md` — md-prep Archetype-B reconstruction (gate: CLEAN).
- `GAS_VOCABULARY.md` — §3 enum, §3.1 DNA-gate table, §17 anchors, priority table, §21 change-log row.
- `06b_…valvetrain_egr_combustion.md` — 3 new fault records replace the WVT record; front-matter; 6B.1 enum table.
- `05_fault_atlas_part_a.md` — ignition entries retitled + cross-linked.
- `04_…grammar_validity_gates.md` — `RULE_WVT` retargeted to the cam-timing family.
- `00_index.md`, `01_…`, `09_…`, `10_…`, `11_…` — count, manifest, era-table, scope list, glossary, appendix.
- `GAS_WIKI.md` — assembled single-file mirror (no build script; hand-maintained). **[Retired 2026-06-10: the single file was archived; the chunks `00`–`11` are now the sole canonical form. Row kept as historical record of what the v2.1 task touched.]**

## VERIFICATION GATE — clean

- **Readability gate (source doc):** `![][` 0; no Read truncation; 36 `$$` LaTeX blocks present; box-drawing chars 0; headings ≤ 3. `diagnose_wall.py` → `CLEAN`.
- **Enum integrity:** `ChemicalSignature` StrEnum = **34** members; 06B enum table = **34** rows incl. the 3 `CAM_TIMING_*`; **no** `WRONG_VALVE_TIMING` row; GAS_WIKI mirror = 34 / 3 CAM.
- **No stale routing:** zero `→ FAULT_WRONG_VALVE_TIMING` references; every remaining `WRONG_VALVE_TIMING` string is an intentional retirement / change-log / cross-lab-follow-up note.
- **Anchor resolution:** `{#FAULT_CAM_TIMING_RETARDED_MAP|_MAF|_ADVANCED}` all defined; all `→` references resolve.
- **Count consistency:** every "32-value/32-entry" enum-count phrasing updated to 34, except the deliberate note that `OBD_VOCABULARY.md §17` is *still 32 upstream* (mirror pending).
- **Source fidelity:** all 3 cam-timing gas vectors (idle + 2500 RPM) match the source 5-gas table exactly.
- **Scope:** 1990–2010 only; no modern-era signatures introduced.
- **Caveat:** the bash sandbox served a stale/truncated mount view during verification; integrity was confirmed with the Read file-tool (authoritative), not the shell.

## CODE REVIEW — clean (docs-only)

No Python changed this session (ruff/pyright/pytest N/A). The wiki is the spec; code mirrors it in the cross-lab session below. `RULE_WVT` rule id and `rule_wrong_valve_timing` were intentionally retained to avoid premature code churn, annotated as pending rename.

## Unplanned follow-ups (deferred to a coordinated cross-lab session)

| Item | Where | Note |
|---|---|---|
| Mirror the new enum (retire `WRONG_VALVE_TIMING`, add 3 `CAM_TIMING_*`) | `COMLab/docs/wiki/OBD_VOCABULARY.md §17` (canonical) | GASLab side is intentionally divergent until this lands |
| Coordinate the breaking enum change | `COMLab/docs/wiki/SEMANTIC_CONTRACT.md` + COMLab schema (`comlab/schemas/vocabulary.py`) | breaking change per GAS_VOCABULARY §18.2 |
| Re-bind the rule | `resolution.py` / `gas_lab_ontology.yaml` WVT rule | emit 3 `CAM_TIMING_*` + rich-branch RPM-normalisation discriminator; supersedes T-DOC-13 row 18 |
| `ChemicalSignature` StrEnum in code | GASLab + COMLab enums | add 3 values, remove 1 |
| Tests referencing `WRONG_VALVE_TIMING` | test suites | update fixtures/asserts |
| Stray temp file could not be deleted | `_skills/doc/md-prep/timings_config.py` (+ `.pyc`) | skill-dir mount blocked unlink from the sandbox; remove manually in PowerShell |

## Graph relations (explicit)

**WRONG_VALVE_TIMING** RETIRED_BY **v2.1 timing-taxonomy revision**
**CAM_TIMING_RETARDED_MAP** ADDED_BY **v2.1** — Speed-Density system, rich branch, CO 3.5–7.0 %, λ 0.75–0.88
**CAM_TIMING_RETARDED_MAF** ADDED_BY **v2.1** — MAF system, lean branch, O₂ 2.0–4.5 %, λ 1.08–1.18
**CAM_TIMING_ADVANCED** ADDED_BY **v2.1** — both load systems, mild-lean idle, NOₓ rises at 2500 RPM
**TIMING_OVER_ADVANCED** RETITLED_BY **v2.1** — retained, cross-linked to cam-timing family
**TIMING_RETARDED** RETITLED_BY **v2.1** — retained, cross-linked to cam-timing family
**ChemicalSignature** enum count CHANGED_FROM **32** TO **34** — v2.1 surface change
**ChemicalSignature** CONSUMED_BY **gaslab.contracts.ChemicalSignature** (StrEnum, 34 members)
**RULE_WVT** RETARGETED_BY **v2.1** — from single WRONG_VALVE_TIMING to three CAM_TIMING_* branches
**RULE_WVT** GATED_BY **match_class: SPECIFIC** — tailpipe gas cannot prove cam phase (needs CKP/CMP from OBDLab/DTCLab)
**dna_gate: none** DESIGNED_FOR **all three CAM_TIMING_*** — no DNA field for MAF-vs-MAP; discriminator is gas-direction + OBD trims
**v2.1 revision** DESCRIBES coordinated cross-lab follow-up: **OBD_VOCABULARY.md §17**, **SEMANTIC_CONTRACT.md**, **COMLab schema**, **resolution.py**, **gas_lab_ontology.yaml**
**GAS_WIKI.md single-file** RETIRED_TO **ARCHIVE** (2026-06-10) — chunks 00–11 are sole canonical form

## Core Entities

- **v2.1 timing-taxonomy revision** — retired WRONG_VALVE_TIMING, added three CAM_TIMING_* states, contract surface 32 → 34. Consumer: `gaslab.contracts.ChemicalSignature` enum.
- **CAM_TIMING_RETARDED_MAP** — new v2.1, Speed-Density rich branch. Consumer: `rule_engine._definitive_match` (RULE_WVT priority 82/40).
- **CAM_TIMING_RETARDED_MAF** — new v2.1, MAF lean branch. Consumer: `rule_engine._definitive_match` (RULE_WVT priority 82).
- **CAM_TIMING_ADVANCED** — new v2.1, both systems mild-lean. Consumer: `rule_engine._definitive_match` (RULE_WVT priority 82).
- **TIMING_OVER_ADVANCED** — retained/retitled. Consumer: `rule_engine._matching_fault_candidates`.
- **TIMING_RETARDED** — retained/retitled. Consumer: `rule_engine._matching_fault_candidates`.
- **WRONG_VALVE_TIMING** — retired v1 value, not in current enum. Consumer: none (intentional retirement).
- **Cross-lab follow-up** — OBD_VOCABULARY §17 mirror, SEMANTIC_CONTRACT.md, COMLab schema, resolution.py rebinding, test suite update. Consumer: coordinated cross-lab session (GAS_VOCABULARY §21).
