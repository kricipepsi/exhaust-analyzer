
> **Context:** DTCLab PRD v2.0 (2026-06-11) · Module: DTCLab · Section: Section 2 — Contacts · Parent document: PRD_DTCLab.md
## Section 2 — Contacts

### Name: DTCLab Owner
- **Role**: Module Owner
- **Responsibility**: DTC ingestion, freeze-frame extraction, Mode $06 evaluation, routing-tag mapping, Phase-2 scoring

### Name: COMLab Team
- **Role**: Integration Consumer
- **Responsibility**: Reads `DTCLabPayload`; injects `POA_HISTORY`; forwards freeze-frame PIDs to OBDLab; fuses `classify_top3` output via `combine()`

### Name: 4DApp Engineering Lead
- **Role**: Architecture
- **Responsibility**: Signal/noise rule; T-FX-3 POA injection contract

---


## Graph relations (explicit)

**Section 2 — Contacts** DESCRIBES **DTCLab PRD v2.0**
