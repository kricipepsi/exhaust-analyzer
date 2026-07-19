
> **Context:** GASLab ADR v2.1 (2026-06-10) · Module: GASLab · Section: ADR-0001: Brettschneider chemistry is ground truth over ECU perception · Parent document: ADR_GASLab.md
## ADR-0001: Brettschneider chemistry is ground truth over ECU perception

**Status:** Accepted

**Context.** A diagnosis must resolve the "DTC says lean, gas says rich" dead end. The ECU reports a *perceived* air-fuel state derived from O₂-sensor feedback and fuel trims, which can be wrong (biased sensor, vacuum leak, mechanical fault). A 5-gas analyser measures the actual products of combustion. We need one of the two to be authoritative when they conflict.

**Decision.** The Brettschneider lambda computed from tailpipe chemistry (`lambda_chem`) is the **ground truth**. The ECU's lambda is *perception*. GASLab emits `lambda_chem` and (optionally) a directly-measured `lambda_measured`; COMLab compares these against the ECU's `normalized_obd_lambda` to detect perception contradictions. GASLab never adjusts its chemistry verdict to agree with the ECU.

**Consequences.**
- Positive: a physically grounded answer that survives a lying sensor; clean separation of "truth" (GASLab) from "perception" (OBDLab).
- Positive: the lambda formula is a pure function — deterministic, testable in isolation.
- Negative: chemistry quality depends on a clean sample, so the validity gates (ADR-referenced in HLD §3) must run first and can halt a diagnosis.
- Neutral: GASLab cannot, alone, prove *intent* faults (e.g. cam phase) — those need OBD/CKP correlation downstream.

**Alternatives considered.**
1. *Trust the ECU and use gas only to corroborate.* Rejected — it reproduces the dead end the product exists to solve; a biased sensor would poison the verdict.
2. *Fuse ECU and gas with a learned weight.* Rejected for v1/v2 — introduces a tuning surface with no first-principles anchor and is hard to make deterministic.

**References.** `PRD_GASLab` §3–4; `GAS_VOCABULARY §6`; the Truth-vs-Perception override principle in the project context.

---


## Graph relations (explicit)

**ADR-0001: Brettschneider chemistry is ground truth over ECU perception** DESCRIBES **GASLab ADR v2.1**
**lambda_chem** SUPERSEDES **ECU lambda** -- Brettschneider chemistry is ground truth
**validity_gates** CONSUMES **GasReading** -- must gate before chemistry trust


