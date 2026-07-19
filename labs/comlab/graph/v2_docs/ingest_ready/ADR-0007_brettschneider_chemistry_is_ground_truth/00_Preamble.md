
> **Context:** ADR-0007 · Module: COMLab · Section: Preamble · Parent document: COMLab HLD v2.0 / COMLab DLD v2.0
# ADR-0007: Brettschneider chemistry is ground truth; detect ECU perception contradiction

**Status:** Accepted

**Context.** The ECU reports a *perceived* air-fuel state from O₂-sensor feedback
and fuel trims, which a biased sensor, vacuum leak, or mechanical fault can make
wrong. The 5-gas analyser measures the actual products of combustion. When the two
disagree ("DTC says lean, gas says rich"), COMLab must know which to trust.

**Decision.** COMLab treats GASLab's Brettschneider `lambda_chem` as **ground
truth** and the ECU's `normalized_obd_lambda` as **perception**.
`core/perception_contradiction.py` compares them: when they diverge beyond the
active era's lambda tolerance *while gas chemistry is near-normal* (the
Lambda-Truth filter), COMLab surfaces an `O2_SENSOR_BIASED_LOW`/`_HIGH` verdict
and the signed `lambda_perception_delta`. `select_perception_lambda` prefers OBD
lambda when present and falls back to GASLab's directly-measured λ on no-OBD
sessions; the detector goes inert when neither exists. The contradiction is
surfaced as a *finding*, not used to overrule the chemistry verdict. A
`SECONDARY_FUEL_TRIM` downstream role qualifies in-tolerance agreement as weak
evidence (the downstream loop may be masking drift); an optional VPWR rail gate
rules out a drifting supply before attributing bias.

**Consequences.**
- Positive: a physically grounded answer that survives a lying sensor; clean
  separation of truth (GASLab) from perception (OBDLab).
- Positive: the detector is a pure function — deterministic and unit-testable
  (`tests/unit/test_perception_contradiction.py`, `tests/integration/test_truth_perception.py`).
- Negative: chemistry trust depends on a clean sample, so GASLab's validity gate
  must pass first (Stage A `ERR-ABORT-001`).
- Neutral: COMLab cannot prove intent faults (e.g. cam phase) from chemistry
  alone — those need OBD/CKP corroboration downstream.

**Alternatives considered.**
1. *Trust the ECU and use gas only to corroborate.* Rejected — reproduces the dead
   end the product exists to resolve.
2. *Fuse ECU and gas with a learned weight.* Rejected — a tuning surface with no
   first-principles anchor and hard to make deterministic.

**References.** `wiki/01_role_boundaries_fusion_spine.md`;
`comlab/core/perception_contradiction.py`; GASLab ADR-0001 (producer-side ground
truth); `comlab/schemas/vocabulary.py::DownstreamTrimRole`, `O2FailureMode`.


## Graph relations (explicit)

**ADR-0007** DESCRIBES **Brettschneider gas chemistry priority**
**comlab/core/perception_contradiction.py** IMPLEMENTS **ADR-0007**
