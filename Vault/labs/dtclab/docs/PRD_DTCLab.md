---
node_type: "prd"
lab: "dtclab"
module: "dtclab"
subsystem: "requirements"
implements: []
consumers:
  - "hld: labs/dtclab/docs/HLD_DTCLab.md"
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py DTCLabPayload ingestion"
drift_guards: []
tags: [dtclab, finished, prd]
source: "labs/dtclab/docs/PRD_DTCLab.md"
---
# PRD — DTCLab
**Status:** Approved
**Version:** 2.0
**Date:** 2026-06-11
**Scope:** Petrol-only, v2 — DTC / freeze-frame / Mode $06 processing + Phase-2 candidate scoring

> **v2.0 reconciliation note.** Refreshed to the shipped `dtclab/` package (PRD-refresh model).
> Changes from v1.0: routing surface is **18** tags; **5** DNA-gated routing entries; the
> **Phase-2 scorer** (`ranking.py` → top-3 fault families for COMLab fusion) is now a shipped
> P0 feature; `SAI_HISTORY` removed; `EP-DTC-NOSTART-1` recorded as a labelled proposal (§8).

---

## Section 1 — Summary

DTCLab is the fault-history and stored-code processing module of 4DApp. It validates raw DTC
lists, extracts and annotates the freeze-frame PID snapshot, classifies historical fault context,
evaluates Mode $06 continuous-monitor margins, and maps confirmed DTCs to routing tags. The
output `DTCLabPayload` is consumed by COMLab to route fault hypotheses and score confidence. A
second, optional surface — the **Phase-2 scorer** — turns that payload into the top-3
`(fault_family, confidence)` candidates for COMLab's Bayesian fusion. DTCLab covers OBD-II layers
L3 (stored DTCs), L4 (freeze-frame snapshot), and the Mode $06 monitor data.

---

## Section 2 — Contacts

| Name | Role | Responsibility |
|------|------|----------------|
| DTCLab Owner | Module Owner | DTC ingestion, freeze-frame extraction, Mode $06 evaluation, routing-tag mapping, Phase-2 scoring |
| COMLab Team | Integration Consumer | Reads `DTCLabPayload`; injects `POA_HISTORY`; forwards freeze-frame PIDs to OBDLab; fuses `classify_top3` output via `combine()` |
| 4DApp Engineering Lead | Architecture | Signal/noise rule; T-FX-3 POA injection contract |

---

## Section 3 — Background

**Context.** OBD-II stores up to three DTC lists: confirmed (mode `$03`), pending (mode `$07`),
permanent (mode `$0A`). Each confirmed DTC carries a freeze-frame snapshot of PIDs captured when
the fault was set. Mode $06 continuous monitors provide a margin percentage showing how close each
system is to failing its test.

**Why now.** The 32-entry `routing_tag_map.yaml` (27 ungated + 5 DNA-gated) covers all major
petrol powertrain DTC families. The 33-MID `mode_06_hex_dictionary.json` covers universal CAN MIDs
for 2008+ vehicles. The Phase-2 scorer lets DTC evidence feed COMLab's Bayesian fusion as ranked
candidates rather than raw tags.

**What recently became possible.** Two cross-field signatures (`COOLANT_SYSTEM_MALFUNCTION`,
`CYLINDER_FLUID_MISFIRE`) read DTC + fuel-system status together to flag fluid-intrusion faults
that no single DTC names.

---

## Section 4 — Objective

**Business benefit.** Translate raw DTC lists into structured, confidence-weighted routing tags
and ranked fault-family candidates that COMLab can dispatch and fuse, reducing manual
DTC-to-fault mapping from minutes to milliseconds.

**Customer benefit.** Technicians receive a clear historical fault context, a Mode $06 margin
table that surfaces impending failures before a full DTC sets, and a ranked candidate list.

**Key Results:**

- **KR1:** `DataFusionSanitizer.sanitize()` returns a valid `DTCLabPayload` for all named
  regression fixtures with zero structural failures.
- **KR2:** Zero cross-lab Python imports (import-isolation audit in `test_dna_view.py`).
- **KR3:** All **5** DNA-gated routing entries suppress correctly on non-equipped vehicles
  (verified in `test_routing_tag_mapper.py` + integration tests).
- **KR4:** `POA_HISTORY` is never emitted by `RoutingTagMapper` — COMLab's responsibility (T-FX-3).
- **KR5:** `classify_top3()` returns ≤ 3 deduplicated `(family, confidence∈[0,1])` candidates,
  sorted `(-confidence, family)`, with no sum-1 normalisation (left to COMLab `combine()`).

---

## Section 5 — Market Segment

**Advanced workshop technician (DTC specialist):** professionals who retrieve stored DTCs,
freeze-frame data, and Mode $06 monitor results and need a tool that cross-references them, scores
confidence, and routes them to the correct diagnostic path — without manually consulting a DTC
reference database.

---

## Section 6 — Value Proposition

- **Jobs addressed:** DTC validation, freeze-frame extraction, historical-context classification,
  Mode $06 evaluation, routing-tag generation, fault-family candidate ranking.
- **Gains created:** 18 routing tags automatically extracted; historical context adds a temporal
  dimension; Mode $06 tri-state surfaces impending failures; freeze-frame symptom flags
  pre-annotate the snapshot; the Phase-2 scorer delivers ranked candidates ready for fusion.
- **Pains relieved:** eliminates manual DTC-to-fault mapping; DNA-gated suppression removes false
  positives automatically (e.g. `CATALYST_HISTORY` only on catalyst-equipped vehicles).
- **Competitive advantage:** cross-field coolant/fluid signatures catch faults no single DTC names;
  `DTC_CONFIDENCE_WEIGHTS` provide a ready-made scoring scheme.

---

## Section 7 — Solution

### Key Features (all P0)

- P0: DTC format validation (`^[BCPU][0-3][0-9A-F]{3}$`) for modes `$03`, `$07`, `$0A`.
  Fail-fast on first invalid code.
- P0: Freeze-frame extraction (12 mandatory PIDs, 7 optional, 6 derived symptom flags).
- P0: Historical fault-context classification (4 states, strict priority order).
- P0: Mode $06 margin tri-state evaluation (33-MID dictionary, LRU-cached load).
- P0: DTC routing-tag mapping — 30 entries (27 ungated + 3 DNA-gated).
- P0: Cross-field coolant/fluid signatures (step 5b) → `COOLANT_SYSTEM_MALFUNCTION`,
  `CYLINDER_FLUID_MISFIRE`.
- P0: DNA confidence three-branch (HIGH strict / PARTIAL log+emit / NONE emit).
- P0: `DTCLabPayload` Pydantic output model (9 fields).
- P0: **Phase-2 scorer** (`ranking.py`) — `rank_candidates` / `classify_top3` → top-3
  `(family, confidence)` for COMLab Bayesian fusion (FU-1), via the Wired adapter (T-DTW-1).
- P0: `DTC_CONFIDENCE_WEIGHTS` published for COMLab aggregator use.

### Technology

- Python 3.14 (workspace standard; `StrEnum` requires ≥ 3.11). Pydantic ≥ 2.5. PyYAML.
  `functools.lru_cache`. No cross-lab imports.
- Package: `dtclab`, standalone `pyproject.toml`.
- Entry point: `dtclab.DataFusionSanitizer.sanitize(...) → DTCLabPayload`.
- Optional surface: `dtclab.ranking.classify_top3(payload, dna_view=...) → list[(family, conf)]`.

### Assumptions

| Assumption | Validation |
|-----------|-----------|
| `DTC_CONFIDENCE_WEIGHTS` values are correct for COMLab aggregation and Phase-2 scoring | Sourced from `DTC_VOCABULARY.md §16`; no drift-guard test yet (open issue) |
| `mode_06_hex_dictionary.json` covers needed universal CAN MIDs | 33 entries from `§13.2`; manufacturer-specific MIDs deferred |
| `dtc_severity_map.yaml` not required | `DTCSeverityClass` enum defined (reserved); severity logic deferred |
| Phase-2 scorer needs no new numeric literal | All confidence from §16 weights × §14.2 DNA factor |

---

## Section 8 — Release

### v2 Scope

All P0 features above, including the Phase-2 scorer and the two cross-field coolant/fluid tags.

### Proposals (labelled — not shipped; consumer nameable)

| ID | Proposal | Named consumer + code path | Disposition |
|---|---|---|---|
| **EP-DTC-NOSTART-1** | Surface Mode $06 monitor-aborted / Incomplete state (MID $A1 / TID $53) and freeze-frame fuel/spark-cut state for no-start diagnosis. CAN-era gated. | COMLab `T-COMV2-NOSTART-1` reads the new monitor state; extends `mode06_evaluator.py` + Mode-06 schemas. Registered by `T-OBDV2-5`; tracked as `T-DTCV2-NOSTART-1`. | **PROPOSAL** (ships with its consumer as a future task; not in current code) |

Wiki `11_proposals_register.md` carries the broader DTCLab proposal slate (P-DTC-1 misfire
Type A/B severity, P-DTC-2 monitor-readiness trust gate, P-DTC-3 FMEM trust flag). Those remain
wiki-side proposals and do not ship here.

### Explicitly Deferred (v2 backlog)

- `dtc_severity_map.yaml` and severity-based DTC ranking.
- Manufacturer-specific Mode $06 MID overlays.
- `DTC_CONFIDENCE_WEIGHTS` wiki drift-guard test.



### Success Criteria

1. KR1–KR5 all pass in CI.
2. `test_dtclab_pipeline.py` passes its integration scenarios including catalyst/EGR DNA gate suppression.
3. `test_vocabulary.py` drift guard confirms the enum counts vs `DTC_VOCABULARY.md` (18-tag
   `DTCRoutingTag`).
4. `test_classify_top3.py` / `test_rank_candidates.py` confirm scorer ordering, clamp, and DNA factor.
