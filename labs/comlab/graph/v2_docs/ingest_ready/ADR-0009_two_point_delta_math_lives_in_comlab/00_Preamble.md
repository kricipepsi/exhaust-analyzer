
> **Context:** ADR-0009 · Module: COMLab · Section: Preamble · Parent document: COMLab HLD v2.0 / COMLab DLD v2.0
# ADR-0009: Two-operating-point Δ math lives in COMLab; additive with a single-point fallback

**Status:** Accepted

**Context.** Several faults are indistinguishable from one operating point but
separate cleanly across two (low idle vs an elevated/stress point) — the
discriminating information is *how* trims, gas, and O₂ change between states. The
emitter labs are deliberately stateless and single-point. Putting cross-state
memory into them would break that property.

**Decision.** The cross-state Δ math lives in COMLab as a **stateless** engine,
`analytics/delta_engine.py`. When `OrchestratorInboundRequest.second_operating_point`
(a `SecondOperatingPointFrame`) is present, `DeltaEngine.compute_delta_signature`
differences it against the primary low-idle channels and emits a typed
`DeltaSignature` that the router's Phase 5 reads as a **primary** rank term (a
Δ-matched fault family is promoted above the base-weighted static signatures).
When the frame is absent, the path is **byte-identical** to the single-point path
and the session carries the `SINGLE_POINT` degradation mode. Two mandatory gates
run before any ΔTrim profile applies: an **architecture gate** (MAP-only nulls
ΔTrim for a real leak; forced induction inverts ΔTrim sign) and a **validity
gate** (per-frame sample validity, dilution, RPM-settled); each band check
ABSTAINs on an `rpm_state_bucket` mismatch rather than differencing across regimes.

**Consequences.**
- Positive: emitters stay single-point and stateless; the optional second reading
  unlocks stronger separation without duplicating fault tables.
- Positive: fully additive — single-reading callers are unaffected; the feature is
  gated by `enable_delta` and the optional payload field.
- Negative: the strongest separations need the technician to take a second reading;
  without it some pairs stay ambiguous (honest `SINGLE_POINT` signalling).
- Neutral: the engine carries both single- and dual-frame code paths.

**Alternatives considered.**
1. *Make the emitters two-point/stateful.* Rejected — breaks their stateless,
   single-point contract and scatters cross-state memory.
2. *Always require two readings.* Rejected — breaks the common quick-check
   workflow and single-reading callers.

**References.** `wiki/11_two_point_delta.md`; `comlab/analytics/delta_engine.py`;
`comlab/schemas/ingestion.py::SecondOperatingPointFrame`;
`comlab/schemas/vocabulary.py::DegradationMode.SINGLE_POINT`.


## Graph relations (explicit)

**ADR-0009** DESCRIBES **Two-point delta logic inside COMLab**
**comlab/analytics/delta_engine.py** IMPLEMENTS **ADR-0009**
