
> **Context:** DTCLab PRD v2.0 (2026-06-11) · Module: DTCLab · Section: Section 1 — Summary · Parent document: PRD_DTCLab.md
## Section 1 — Summary

DTCLab is the fault-history and stored-code processing module of 4DApp. It validates raw DTC
lists, extracts and annotates the freeze-frame PID snapshot, classifies historical fault context,
evaluates Mode $06 continuous-monitor margins, and maps confirmed DTCs to routing tags. The
output `DTCLabPayload` is consumed by COMLab to route fault hypotheses and score confidence. A
second, optional surface — the **Phase-2 scorer** — turns that payload into the top-3
`(fault_family, confidence)` candidates for COMLab's Bayesian fusion. DTCLab covers OBD-II layers
L3 (stored DTCs), L4 (freeze-frame snapshot), and the Mode $06 monitor data.

---


## Graph relations (explicit)

**Section 1 — Summary** DESCRIBES **DTCLab PRD v2.0**
**DTCLab** DESCRIBES **DTC, freeze-frame, and Mode $06 fault-history module** -- L3/L4/Mode06 of 4DApp pipeline
**DTCLabPayload** CONSUMES **COMLab** -- fault-history input
