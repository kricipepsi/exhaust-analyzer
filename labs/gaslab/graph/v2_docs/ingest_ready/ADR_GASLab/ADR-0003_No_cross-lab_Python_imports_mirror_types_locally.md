
> **Context:** GASLab ADR v2.1 (2026-06-10) · Module: GASLab · Section: ADR-0003: No cross-lab Python imports — mirror types locally · Parent document: ADR_GASLab.md
## ADR-0003: No cross-lab Python imports — mirror types locally

**Status:** Accepted

**Context.** GASLab, OBDLab, DTCLab, and COMLab must evolve independently. A direct `import` from one lab into another couples their release cycles and lets a change in one silently break another.

**Decision.** GASLab performs **zero** cross-lab Python imports. Types it shares with COMLab are **mirrored locally**: `GasLabDnaView` (the 13-field slice COMLab projects), the `ChemicalSignature` enum, the `GasLabPayload` shape, and `family_map.SIGNATURE_TO_FAMILY`. The cross-lab contract is the **JSON values**, not the Python classes. Two independent declarations of the same enum are intentional and accepted.

**Consequences.**
- Positive: each lab is a fully isolated codebase; the boundary is a typed JSON document.
- Positive: enforceable mechanically (the import-isolation audit fails CI on a cross-lab import).
- Negative: shared enums/shapes are declared twice and can drift — which is why a coordinated cross-lab change is required when the contract changes (see ADR-0007).
- Neutral: COMLab owns its own mirror and validates incoming payloads against it.

**Alternatives considered.**
1. *A shared `common` package of contract types.* Rejected — reintroduces the coupling and a shared release cadence we are avoiding.
2. *Generate mirrors from a single schema file at build time.* Deferred — adds a build step; the hand-maintained mirror plus the drift guard is sufficient at current scale.

**References.** `README.md` boundary note; `GAS_VOCABULARY §13` invariant 6; `SEMANTIC_CONTRACT.md §1`.

---


## Graph relations (explicit)

**ADR-0003: No cross-lab Python imports — mirror types locally** DESCRIBES **GASLab ADR v2.1**
**gaslab/** GATED_BY **import-isolation** -- zero cross-lab Python imports, mirror types locally


