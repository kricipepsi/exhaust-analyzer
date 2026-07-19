> **Context:** OBDLab HLD v2.0 (2026-06-10) · Module: OBDLab · Section 1 Responsibility · Parent document: HLD_OBDLab.md · Boundary contract: SEMANTIC_CONTRACT §4.4

## 1. Responsibility

OBDLab is the **electronic-perception channel** of the 4D petrol diagnostic
pipeline (the L5 live-PID layer). It validates and transforms a raw OBD-II PID
dict into a typed `OBDLivePayload` that represents **the ECU's perception** of
engine state.

OBDLab is an **emitter, not a judge.** It emits its own channels — trims,
normalized lambda, VE, perception-deltas, sensor provenance — and does **not**
produce fault-family verdicts. Cross-referencing OBD perception against GASLab
chemical truth, and rendering the final root-cause verdict, is COMLab's job
(see `KGtopic.md` division-of-labor). This emitter role was ratified in
**T-OBDV2-0 (`revive`, 2026-06-08)**: the >95% NO_FAULT result that prompted the
quarantine review was a **PID-less-corpus artefact**, not a code defect.

Truth-vs-perception: the ECU is *perception*, gas chemistry (GASLab
Brettschneider lambda) is *ground truth*.

## Graph relations (explicit)

**HLD_OBDLab v2.0** SUPERSEDES **HLD_OBDLab v1.0** (2026-05-22)
**OBDLab emitter** OWNED_BY **OBDLab**
**COMLab fault_atlas_router** CONSUMES **OBDLivePayload**
**KGtopic.md division-of-labor** MIRRORS_CONTRACT_IN **SEMANTIC_CONTRACT §4.4**
