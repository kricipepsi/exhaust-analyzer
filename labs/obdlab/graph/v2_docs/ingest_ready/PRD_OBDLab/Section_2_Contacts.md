> **Context:** OBDLab PRD v2.0 (2026-06-10) · Module: OBDLab · Section 2 Contacts · Parent document: PRD_OBDLab.md

## Section 2 — Contacts

### Entity: Contacts

- **OBDLab Owner** — Module Owner · Responsibility: PID ingestion, VE engine, O2 normaliser, trim analytics gate, MAF linearity
- **COMLab Team** — Integration Consumer · Responsibility: Reads `OBDLivePayload`; populates `freeze_frame_pids` before calling OBDLab; consumes perception delta, bank asymmetry, VE evidence, O2 failure mode
- **4DApp Engineering Lead** — Architecture · Responsibility: Signal/noise rule; cross-lab JSON contract; emitter-vs-judge division of labor

## Graph relations (explicit)

**OBDLab Owner** OWNED_BY **OBDLab** (PID ingestion, VE engine, O2 normaliser, trim analytics gate, MAF linearity)
**COMLab Team** CONSUMES **OBDLivePayload** (populates freeze_frame_pids, reads perception delta, bank asymmetry, VE evidence, O2 failure mode)
**4DApp Engineering Lead** ENUMERATES **signal/noise rule, cross-lab JSON contract, emitter-vs-judge division**
