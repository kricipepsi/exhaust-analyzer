
> **Context:** GASLab ADR v2.1 (2026-06-10) · Module: GASLab · Section: ADR-0010: Collapse the `target_lambda` low/high pair into a single `target_lambda_v112` window · Parent document: ADR_GASLab.md
## ADR-0010: Collapse the `target_lambda` low/high pair into a single `target_lambda_v112` window

**Status:** Accepted (supersedes the v1 `target_lambda_low` / `target_lambda_high` pair)

**Context.** v1 carried two CoC fields, `target_lambda_low` and `target_lambda_high`, to express a certified lambda band for NORMAL_OPERATION. In practice the certified value is a single centre point, and a two-field band invites inconsistent or inverted inputs.

**Decision.** Replace the pair with a single `target_lambda_v112` (the certified CoC λ centre). `_coc_adjust_normal_bounds` centres the NORMAL λ window on `[v112 − 0.005, v112 + 0.005]`, clamped to `[0.85, 1.15]`. Absent → the generic ±0.005 window centred on 1.000.

**Consequences.**
- Positive: one unambiguous input; no inverted-band failure mode; window half-width is a single owned constant.
- Positive: smaller DNA view (contributes to the 13-field surface).
- Negative: a fixed ±0.005 half-width cannot express an asymmetric certified band — acceptable given the data available.
- Neutral: a breaking change to the DNA-view shape, handled with the cross-lab projection.

**Alternatives considered.**
1. *Keep the low/high pair.* Rejected — two fields for one certified value, with an inversion hazard.
2. *Make the half-width configurable per vehicle.* Rejected — a second field with no current consumer (signal/noise); revisit only when real CoC data demands asymmetry.

**References.** `LLD_GASLab §8`; `DLD_GASLab §5`; `GAS_VOCABULARY §11`; `rule_engine._coc_adjust_normal_bounds`.

---


## Graph relations (explicit)

**ADR-0010: Collapse the `target_lambda` low/high pair into a single `target_lambda_v112` window** DESCRIBES **GASLab ADR v2.1**
**target_lambda_v112** SUPERSEDES **target_lambda_low, target_lambda_high** -- single centre point, +/-0.005 window


