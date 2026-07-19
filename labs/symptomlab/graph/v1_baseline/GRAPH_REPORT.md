# Graph Report - DNALab\SymptomLab  (2026-06-06)

## Corpus Check
- 29 files · ~10,569 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 250 nodes · 311 edges · 26 communities (25 shown, 1 thin omitted)
- Extraction: 76% EXTRACTED · 24% INFERRED · 0% AMBIGUOUS · INFERRED: 75 edges (avg confidence: 0.6)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f7544224`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]

## God Nodes (most connected - your core abstractions)
1. `EnvironmentalConditions` - 22 edges
2. `SymptomDNA` - 21 edges
3. `OccursDuring` - 16 edges
4. `EngineState` - 15 edges
5. `_make_full_payload()` - 11 edges
6. `TestSymptomDNAFromJsonMissingRequired` - 11 edges
7. `Findings` - 11 edges
8. `SymptomValidationError` - 10 edges
9. `SymptomValidator` - 10 edges
10. `TestSymptomDNAFromJsonRoundTrip` - 9 edges

## Surprising Connections (you probably didn't know these)
- `TestSymptomDNAFromJsonRoundTrip` --uses--> `SymptomValidationError`  [INFERRED]
  tests/test_symptomdna_from_json.py → symptomlab/models.py
- `TestSymptomDNAFromJsonMissingRequired` --uses--> `SymptomValidationError`  [INFERRED]
  tests/test_symptomdna_from_json.py → symptomlab/models.py
- `TestSymptomDNAFromJsonInvalidEnum` --uses--> `SymptomValidationError`  [INFERRED]
  tests/test_symptomdna_from_json.py → symptomlab/models.py
- `TestSymptomDNAFromJsonRoundTrip` --uses--> `OccursDuring`  [INFERRED]
  tests/test_symptomdna_from_json.py → symptomlab/models.py
- `TestSymptomDNAFromJsonMissingRequired` --uses--> `OccursDuring`  [INFERRED]
  tests/test_symptomdna_from_json.py → symptomlab/models.py

## Communities (26 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (15): EnvironmentalConditions, The 4-field Part B payload, per SEMANTIC_CONTRACT.md §4.2.      No routing field, Serialize to the JSON shape from contract §4.2., SymptomDNA, Sanity tests for SymptomLab models., test_symptom_dna_is_frozen(), test_symptom_dna_to_json_keys(), SymptomDNA with no free_text_notes should round-trip. (+7 more)

### Community 1 - "Community 1"
Cohesion: 0.16
Nodes (12): StrEnum, EngineState, from_json(), OccursDuring, Raised when (tier_1, tier_2) is not one of the 18 allowed combinations,     or e, SymptomValidationError, SymptomValidator, validator() (+4 more)

### Community 2 - "Community 2"
Cohesion: 0.11
Nodes (18): code:python (class EngineState(StrEnum):), code:python (if len(self._allowed) != 18:), Findings, H1 — `StrEnum` requires Python 3.11; `pyproject.toml` declares `>=3.10`, H2 — `black_sooty_rich` in the YAML contradicts `black_smoke` in both spec documents, L1 — No drift guard linking the YAML catalog to VehicleDNA.md, L2 — Hardcoded `18` in the startup invariant guard is untestable, L3 — `PROGRESS.md` source-step coverage table names a non-existent file (+10 more)

### Community 3 - "Community 3"
Cohesion: 0.15
Nodes (15): _get_validator(), SymptomLab — Part B symptom-triage module for the 4DLab DNA system., Return a SymptomValidator for `allowed_path`. Cached per distinct path., Validate a triage selection and package it as a SymptomDNA.      Per SEMANTIC_CO, resolve(), _clear_validator_cache(), Clear the lru_cache after each test to release resources., Calls with the same allowed_path reuse the cached validator instance. (+7 more)

### Community 4 - "Community 4"
Cohesion: 0.19
Nodes (6): _make_full_payload(), Tests for SymptomDNA.from_json deserialization., from_json must reject payloads with invalid enum strings., TestSymptomDNAFromJsonInvalidEnum, TestSymptomDNAFromJsonMissingRequired, TestSymptomDNAFromJsonRoundTrip

### Community 5 - "Community 5"
Cohesion: 0.18
Nodes (10): ARCHITECTURE ###, code:block1 (User selection ──► SymptomLab.resolve(tier_1, tier_2, env, n), code:block2 (SymptomLab/), CONSTRAINTS — do not violate ###, CONTEXT — READ THESE FIRST ###, MODULE LAYOUT ###, ROLE ###, SUCCESS CRITERIA ### (+2 more)

### Community 6 - "Community 6"
Cohesion: 0.20
Nodes (9): code:json ({), code:block2 (SymptomLab/), code:python (from symptomlab import resolve), Layout (will be created by task files), Next session, Quickstart (after tasks T-SL-1..T-SL-4), Strict naming (locked), SymptomLab (+1 more)

### Community 7 - "Community 7"
Cohesion: 0.22
Nodes (8): code:toml (requires-python = ">=3.11"), code:yaml (visible_exhaust_smoke:), code:python (class EngineState(StrEnum):), Context ###, Deliverables ###, Goal ###, Out of scope ###, Verification ###

### Community 8 - "Community 8"
Cohesion: 0.22
Nodes (8): code:toml ([tool.pyright]), code:python (if len(self._allowed) != 18:), code:python ("""Drift guard: allowed_combinations.yaml must match Vehicle), Context ###, Deliverables ###, Goal ###, Out of scope ###, Verification ###

### Community 9 - "Community 9"
Cohesion: 0.25
Nodes (7): CODE REVIEW — T-SL-5, code:block1 (Phase 1 (syntax):       PASS — python -m compileall symptoml), Explicit verification checks, Files changed (T-SL-5 scope), Immediate Checklist items applied, T-SL-5 — Spec Alignment (Audit H1, H2, M1, L3, L4), VERIFICATION GATE — T-SL-5

### Community 10 - "Community 10"
Cohesion: 0.25
Nodes (7): code:block1 (SymptomLab/), code:python (from dataclasses import dataclass, asdict), code:block3 (# Runtime), Deliverables ###, Goal ###, Out of scope ###, Verification ###

### Community 11 - "Community 11"
Cohesion: 0.25
Nodes (7): code:python (from pathlib import Path), code:python (from pathlib import Path), Context ###, Deliverables ###, Goal ###, Out of scope ###, Verification ###

### Community 12 - "Community 12"
Cohesion: 0.25
Nodes (7): code:python (@classmethod), code:python (class TestSymptomDNAFromJsonNoPairValidation:), Context ###, Deliverables ###, Goal ###, Out of scope ###, Verification ###

### Community 13 - "Community 13"
Cohesion: 0.29
Nodes (6): Changes, CODE REVIEW, code:block1 (VERIFICATION GATE — T-SL-6), T-SL-6 — Progress Notes, Verification, VERIFICATION GATE

### Community 14 - "Community 14"
Cohesion: 0.29
Nodes (6): Changes, CODE REVIEW, code:block1 (VERIFICATION GATE — T-SL-7), T-SL-7 — Progress Notes, Verification, VERIFICATION GATE

### Community 15 - "Community 15"
Cohesion: 0.29
Nodes (6): Mandatory bootstrap (in this exact order, before doing anything else) ###, Now do step 1 of the bootstrap. ###, Prerequisites ###, Role ###, Session-end checklist ###, Working rules (apply throughout) ###

### Community 16 - "Community 16"
Cohesion: 0.29
Nodes (6): code:block1 (T-SL-1 (decision table YAML) ──┐), Execution order, Source-step coverage, SymptomLab — Progress Ledger, Task log, Unplanned follow-ups

### Community 17 - "Community 17"
Cohesion: 0.29
Nodes (6): code:yaml (# Source: VehicleDNA.md §"Complete Universal Triage & Diagno), Context ###, Deliverables ###, Goal ###, Out of scope ###, Verification ###

### Community 18 - "Community 18"
Cohesion: 0.38
Nodes (6): _load_yaml_pairs(), Drift guard: allowed_combinations.yaml must match VehicleDNA.md §"Complete Unive, Every pair in the YAML must be in the VehicleDNA.md reference table., Every pair in the VehicleDNA.md reference table must be in the YAML., test_vehicledna_reference_matches_yaml(), test_yaml_matches_vehicledna_reference()

### Community 19 - "Community 19"
Cohesion: 0.33
Nodes (5): Coverage details, Pythonskill checklist, Summary, T-SL-4 — Tests, Verification

### Community 20 - "Community 20"
Cohesion: 0.40
Nodes (4): Pythonskill checklist, Summary, T-SL-1 — Decision Table YAML, Verification

### Community 21 - "Community 21"
Cohesion: 0.40
Nodes (4): Pythonskill checklist, Summary, T-SL-2 — Module Scaffold, Verification

### Community 22 - "Community 22"
Cohesion: 0.40
Nodes (4): Pythonskill checklist, Summary, T-SL-3 — Dispatcher (resolve), Verification

### Community 23 - "Community 23"
Cohesion: 0.40
Nodes (4): Deliverables ###, Goal ###, Out of scope ###, Verification ###

## Knowledge Gaps
- **104 isolated node(s):** `ROLE ###`, `CONTEXT — READ THESE FIRST ###`, `code:block1 (User selection ──► SymptomLab.resolve(tier_1, tier_2, env, n)`, `TASK ###`, `code:block2 (SymptomLab/)` (+99 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `SymptomValidator` connect `Community 1` to `Community 0`, `Community 3`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **Why does `_get_validator()` connect `Community 3` to `Community 1`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Why does `SymptomDNA` connect `Community 0` to `Community 1`, `Community 4`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 19 inferred relationships involving `EnvironmentalConditions` (e.g. with `SymptomValidator` and `TestSymptomDNAFromJsonRoundTrip`) actually correct?**
  _`EnvironmentalConditions` has 19 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `SymptomDNA` (e.g. with `SymptomValidator` and `TestSymptomDNAFromJsonRoundTrip`) actually correct?**
  _`SymptomDNA` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 13 inferred relationships involving `OccursDuring` (e.g. with `SymptomValidator` and `TestSymptomDNAFromJsonRoundTrip`) actually correct?**
  _`OccursDuring` has 13 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `EngineState` (e.g. with `SymptomValidator` and `TestSymptomDNAFromJsonRoundTrip`) actually correct?**
  _`EngineState` has 12 INFERRED edges - model-reasoned connections that need verification._