
> **Context:** GASLab ADR v2.1 (2026-06-10) · Module: GASLab · Section: ADR-0005: DNA gates are strict and unconditional, not confidence-weighted · Parent document: ADR_GASLab.md
## ADR-0005: DNA gates are strict and unconditional, not confidence-weighted

**Status:** Accepted

**Context.** A fault that is physically impossible for a vehicle (a catalyst fault on a catless car) must never be emitted. The DNA view carries a `confidence` field; one design option is to weaken gates when DNA confidence is low.

**Decision.** DNA gates are applied **strictly and unconditionally** in `resolution.apply_differentiators`: if a candidate's gate field does not match the DNA view, the candidate is removed, regardless of `confidence`. Equipment we are unsure about does not earn a fault a second chance through a softened gate.

**Consequences.**
- Positive: no false positives from impossible faults; the gate is simple equality, trivially testable.
- Positive: deterministic — the verdict does not depend on a confidence heuristic.
- Negative: a wrong/missing DNA field can suppress a real fault; correctness of the verdict leans on DNA-projection quality upstream.
- Neutral: `confidence` is still carried for COMLab and used in one narrow, explicit place (ADR-0011).

**Alternatives considered.**
1. *Confidence-weighted gates (relax when DNA is PARTIAL/NONE).* Rejected for the canonical pipeline — it trades a clear, testable rule for a tunable heuristic and risks emitting impossible faults.
2. *Top-N ranked output that keeps gated candidates as low-confidence options.* Exists only in the out-of-scope `ranking.py` (GASLabSimple), not on the `process()` path.

**References.** `LLD_GASLab §7`; `HLD_GASLab §5`; `resolution.py`.

---


## Graph relations (explicit)

**ADR-0005: DNA gates are strict and unconditional, not confidence-weighted** DESCRIBES **GASLab ADR v2.1**
**resolution.dna_gate** GATED_BY **strict equality, not confidence** -- unconditional fault suppression
**GasLabDnaView.confidence** CONSUMES **resolution._rich_co_ceiling()** -- only narrow exception (ADR-0011)


