# ADR-0005: DNALab pre-resolves the horizon; COMLab never parses the VIN

**Status:** Accepted

**Context.** The architecture horizon (LEGACY/ADAPTIVE/MODERN) drives registry
pruning, and it derives from the vehicle's emission category, which derives from
the VIN. The question is *where* the VIN→horizon resolution happens. Under the
horizontal-DNA architecture, `VehicleDNA` already reaches every lab on input with
the heavy decode done once by DNALab.

**Decision.** DNALab pre-computes `resolved_horizon` (and `euro_emission_category`,
`cylinder_count`, etc.) and ships them in `VehicleDNA`. COMLab is a **read-only
consumer**: `horizon_context_injector.HorizonContextInjector.from_vehicle_dna`
reads `vin_dna.resolved_horizon` and loads the era-sensitivity threshold mask — it
does **not** string-slice the VIN. A `_horizon_from_euro()` fallback exists only
to derive the horizon from `euro_emission_category` when an older payload omits
`resolved_horizon`; it is a defensive default, not a decode.

**Consequences.**
- Positive: VIN-decode logic lives in exactly one place (DNALab); COMLab cannot
  drift from it.
- Positive: `horizon_context_injector.py` collapses to a thin reader + mask
  lookup — small and trivially testable.
- Negative: COMLab depends on DNALab populating `resolved_horizon` correctly; a
  bad upstream value mis-prunes the registry (mitigated by the euro fallback and
  the `MODERN` safe default).
- Neutral: the v1.0 idea of renaming the file to `horizon_resolver.py` was not
  taken — the name is kept so test imports do not churn.

**Alternatives considered.**
1. *Parse the VIN inside COMLab.* Rejected — duplicates DNALab and reintroduces a
   decode surface the architecture deliberately centralised.
2. *Require `resolved_horizon` and hard-fail when absent.* Rejected for
   resilience — the euro fallback keeps older payloads serviceable; a missing
   horizon degrades gracefully rather than aborting.

**References.** `wiki/03_vehicle_dna_pruning.md`, `wiki/04_horizon_eras.md`;
`comlab/core/horizon_context_injector.py`; `comlab/projection.py::_horizon_from_euro`.
