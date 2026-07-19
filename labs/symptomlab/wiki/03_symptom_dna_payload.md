---
chunk_id: SYMWIKI-03
title: "The SymptomDNA Part-B Payload Contract"
lab: symptomlab
node_type: wiki
module: symptomlab
subsystem: payload-contract
implements:
  - "labs/symptomlab/symptomlab/models.py"
consumers:
  - "dnalab: labs/dnalab/dnalab/models.py SymptomDNA.from_json -> VehicleDNA.symptom_dna"
  - "dnalab: labs/dnalab/dnalab/assembly.py resolve() -> VehicleDNA Part B"
  - "comlab: labs/comlab/comlab/core/symptom_router.py route_symptom (SymptomDNA dict payload)"
drift_guards:
  - "labs/symptomlab/tests/unit/test_models.py"
  - "labs/symptomlab/tests/unit/test_symptomdna_from_json.py"
tags: [symptomlab, wiki, payload-contract]
source: "labs/symptomlab/wiki/03_symptom_dna_payload.md"
doc: SYMPTOM_WIKI
version: v2.0
date: 2026-06-12
kg_ingestion: extract
disposition: live
summary: "The four-field, routing-free SymptomDNA payload SymptomLab emits as its Part-B contribution to VehicleDNA. Prose mirror of models.py SymptomDNA + EnvironmentalConditions. Deliberately carries no routing/scoring fields — those are COMLab's."
related_chunks: [SYMWIKI-00, SYMWIKI-01, SYMWIKI-02]
mirrors_code:
  - "symptomlab/symptomlab/models.py:SymptomDNA"
  - "symptomlab/symptomlab/models.py:EnvironmentalConditions"
consumer: "symptomlab/symptomlab/validator.py:SymptomValidator.validate"
sources:
  - "labs/symptomlab/symptomlab/models.py"
  - "SEMANTIC_CONTRACT.md §4.2"
---

# 3. The SymptomDNA Part-B Payload Contract

> **Chunk summary.** `SymptomDNA` is the typed object SymptomLab hands to DNALab as
> the "Part B" (driver-reported) slice of VehicleDNA. It has exactly **four
> fields** and is **routing-free by design**: it states *what the driver reported*,
> never *what to do about it*. This note mirrors the dataclass in `models.py`.

## 3.1 The four fields {#CONCEPT_PAYLOAD_FIELDS}

| Field | Type | Meaning |
|---|---|---|
| `tier_1_primary_symptom` | `str` | The Tier-1 category id (open vocabulary, validated against the catalog — SYMWIKI-01). |
| `tier_2_subfield_filter` | `str` | The Tier-2 sub-filter id, validated as a pair with `tier_1`. |
| `environmental_conditions` | `EnvironmentalConditions` | The three context axes (SYMWIKI-02): `occurs_during`, `engine_state`, `load_state`. |
| `free_text_notes` | `str | None` | Optional technician free text; defaults to `None`. |

The two tier ids are typed `str` (not `StrEnum`) on purpose: the catalog is an
**open vocabulary** validated by the YAML, so adding a symptom is a data change,
not a code change. The three context axes *are* `StrEnum`s, because they are a
fixed, closed set (SYMWIKI-02).

# source: labs/symptomlab/symptomlab/models.py (SymptomDNA, EnvironmentalConditions)

## 3.2 The JSON boundary {#CONCEPT_PAYLOAD_JSON}

`SymptomDNA.to_json_payload()` serialises to the shape in SEMANTIC_CONTRACT.md
§4.2; `from_json()` deserialises an already-validated payload at the JSON boundary.

```
{
  "tier_1_primary_symptom": "rough_idle_shudder",
  "tier_2_subfield_filter": "surging_hunting_idle",
  "environmental_conditions": {
    "occurs_during": "cold_only",
    "engine_state":  "running",
    "load_state":    "idle"
  },
  "free_text_notes": null
}
```

Two validation depths exist, and the distinction matters:

```
 raw user input ──► SymptomValidator.validate()  ──► checks the (tier_1, tier_2)
                                                      pair IS in the 21-pair catalog
                                                      + axis enums  ──► SymptomDNA

 stored payload ──► SymptomDNA.from_json()        ──► checks field presence + axis
                                                      enum membership ONLY
                                                      (NOT catalog membership)
```

`from_json()` validates field presence and axis-enum membership but does **not**
re-check catalog membership — that invariant is owned by `validate()` and the
resolve entry point. DNALab must construct via `validate()` (or equivalent) from
user input; `from_json()` is only for re-reading a payload already validated.

# source: labs/symptomlab/symptomlab/models.py (SymptomDNA.from_json, to_json_payload)

## 3.3 Why there are no routing fields {#CONCEPT_PAYLOAD_ROUTING_FREE}

`SymptomDNA` carries **no** mode-suppression list, no mode-ranking list, no
`target_backend_equation`, scoring weight, or fault-family verdict. Those are
routing decisions, and routing lives in COMLab, downstream of the JSON boundary
(per DNALab_TO_COMLab_FLOW.md §4). SymptomLab's job ends at producing a clean,
validated description of the complaint; COMLab consumes it through the proposals in
the registry (COMLab-A / COMLab-B / COMLab-F / COMLab-G). Keeping the payload
routing-free is the same signal/noise boundary that keeps numbers out of this wiki.

# source: labs/symptomlab/symptomlab/data/allowed_combinations.yaml (header: "Routing ... lives in COMLab")
# source: labs/comlab/comlab/config/proposals/entries.yaml


## Graph relations (explicit)

**SymptomDNA** HAS_FIELD **tier_1_primary_symptom**, **tier_2_subfield_filter**, **environmental_conditions**, **free_text_notes**
**SymptomDNA** CONSUMES **EnvironmentalConditions**
**SymptomValidator.validate** PRODUCES **SymptomDNA**
**SymptomDNA.to_json_payload** SERIALIZES **SymptomDNA** (contract §4.2 shape)
**SymptomDNA.from_json** DESERIALIZES **SymptomDNA** (structural validation only — no catalog re-check)
**SymptomDNA** ROUTES_TO **DNALab VehicleDNA assembly** (Part-B payload)
**SymptomDNA** IS_ROUTING_FREE (routing decisions live in COMLab — see COMLab-A, COMLab-B, COMLab-F, COMLab-G)
**tier_1_primary_symptom** VALIDATED_AGAINST **allowed_combinations.yaml** (via SymptomValidator.validate)
**tier_2_subfield_filter** VALIDATED_AGAINST **allowed_combinations.yaml** (via SymptomValidator.validate)
**from_json** DOES_NOT re-validate **catalog membership** (validate() owns that invariant)


## Core Entities

- **SymptomDNA** (dataclass, live) — CONSUMED_BY **DNALab VehicleDNA assembly** (symptomlab/symptomlab/models.py)
- **SymptomValidator.validate** (live) — CONSUMED_BY **DNALab resolve entrypoint** (symptomlab/symptomlab/validator.py)
- **SymptomDNA.to_json_payload** (live) — CONSUMED_BY **JSON boundary** (symptomlab/symptomlab/models.py)
- **SymptomDNA.from_json** (live) — CONSUMED_BY **JSON boundary** (symptomlab/symptomlab/models.py)
