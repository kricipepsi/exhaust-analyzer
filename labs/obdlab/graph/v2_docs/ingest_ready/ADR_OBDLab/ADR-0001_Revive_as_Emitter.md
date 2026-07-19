> **Context:** OBDLab ADR v2.0 (2026-06-10) · Module: OBDLab · ADR-0001: Revive OBDLab as a perception-channel emitter · Parent document: ADR_OBDLab.md

## ADR-0001: Revive OBDLab as a perception-channel emitter, not a fault classifier

**Status:** Accepted (2026-06-08, owner-ratified — T-OBDV2-0)

### Context

On the available corpus, standalone OBDLab returned `NO_FAULT` for >95% of
cases, which triggered a revive-vs-quarantine review. Investigation showed the
result was a **PID-less-corpus artefact** (the corpus lacked live PID rows), not
a defect in the translation logic. Separately, the 4D architecture assigns
root-cause verdicts to COMLab's system-level causality graph; the parsing labs
(GAS/OBD/DTC) are meant to translate raw metrics into typed perceptions, not to
judge faults (`KGtopic.md`).

### Decision

OBDLab is revived as a **typed perception-channel emitter** feeding COMLab
fusion. It emits its own channels — trims, normalized lambda, VE, sensor
provenance, perception-deltas — and **does not emit fault-family verdicts**.
Standalone OBD fault classification is conceded.

### Consequences

- **Positive:** clear separation of concerns; OBDLab is testable as a pure
  transform; the NO_FAULT non-issue is closed; COMLab owns one verdict surface.
- **Positive:** validates the dead-classifier purge (see ADR-0007).
- **Negative:** OBDLab alone produces no human-facing diagnosis; usefulness
  depends on COMLab consuming its channels (much of which lands at Stage 4).
- **Neutral:** the payload becomes wider (more emitted channels) rather than
  narrower.

### Alternatives Considered

1. **Quarantine OBDLab** — shelve the lab until a PID-rich corpus exists.
   Rejected: the >95% NO_FAULT was a corpus artefact, so quarantine would shelve
   working code for a non-defect.
2. **Keep OBDLab as a standalone classifier** — let it emit fault verdicts.
   Rejected: duplicates COMLab's job, splits the verdict surface across labs, and
   couples OBDLab to cross-lab fault taxonomy.

## Graph relations (explicit)

**ADR-0001** DESCRIBES **Revive OBDLab as emitter** (perception-channel, no fault-family verdicts)
**T-OBDV2-0** DESCRIBES **ADR-0001** (task that carried it)
**OBDLab emitter** OWNED_BY **OBDLab** (typed perception-channel feeding COMLab)
**COMLab** CONSUMES **OBDLivePayload** (fault-atlas router — sole verdict surface)
**ADR-0001** ROUTES_TO **ADR-0007** (dead-classifier purge consequence)
