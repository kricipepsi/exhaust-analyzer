> **Context:** VINLab ADR v2.0 (2026-06-12) | Module: VINLab | Section: ADR-0007: Cylinder-count heuristic is a gated last resort, never an override | Parent document: ADR_VINLab.md

## ADR-0007: Cylinder-count heuristic is a gated last resort, never an override

**Status:** Accepted (T-VL-7)

### Context

CSV and `vref.db` do not always supply a cylinder count, but downstream routing
(bank-2 contract, UI field gating) needs one. Brand-aware engine-code rules can infer
it — but they must never override authoritative data.

### Decision

`overlay/cylinder_heuristic.infer_cylinder` fires **only** when `cylinder_count == 0`
after CSV + `vref.db`. It returns a `CylinderHint(count=0)` when it cannot resolve, and
the rule table must not be expanded without a follow-up task.

### Consequences

- **Positive:** more vehicles get a usable cylinder count without risking real data.
- **Negative:** heuristic values are lower-confidence; they ride the same `VinDNA` field
  as authoritative values (provenance is in the heuristic's `source`, not on `VinDNA`).

### Alternatives Considered

1. **Always run the heuristic and reconcile.** Rejected: risks overwriting real data.
2. **Leave `cylinder_count = 0` when unknown.** Rejected: breaks bank/UI gating that
   needs a positive count.

---

## Graph relations (explicit)

**ADR-0007: Cylinder-count heuristic is a gated last resort, never an override** DESCRIBES **VINLab ADR v2.0 (2026-06-12)**
**vinlab.overlay.cylinder_heuristic.infer_cylinder** IMPLEMENTS **ADR-0007**
**labs/vinlab/tests/unit/test_cylinder_heuristic.py** VERIFIES **vinlab.overlay.cylinder_heuristic.infer_cylinder**
