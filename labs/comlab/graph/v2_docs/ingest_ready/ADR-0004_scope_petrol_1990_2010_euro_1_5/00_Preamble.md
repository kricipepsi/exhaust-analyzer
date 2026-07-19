
> **Context:** ADR-0004 · Module: COMLab · Section: Preamble · Parent document: COMLab HLD v2.0 / COMLab DLD v2.0
# ADR-0004: Scope is petrol 1990–2010 (Euro 1–5); Euro 6+ perks out of scope

**Status:** Accepted

**Context.** The diagnostic domain could be drawn arbitrarily wide. The source
research and the analyser-first, manual-input workflow target older petrol
vehicles. Earlier design drafts described `HORIZON_MODERN` as a "2010–2020,
wideband O₂, GPF, GDI-common" tier and carried equipment fields and routing tags
for post-2010 technology (secondary-air injection / SAI, GPF/DPF inference, LSPI).
Those features were never in the shipped scope and leave orphaned artefacts.

**Decision.** COMLab targets **petrol vehicles 1990–2010, Euro 1–5**, across three
horizon buckets: `HORIZON_LEGACY` (Euro 1–2), `HORIZON_ADAPTIVE` (Euro 3–4), and
`HORIZON_MODERN` (Euro 5, capped at the 1990–2010 window). Post-2010 **Euro 6+**
technology — GPF/DPF inference, LSPI, secondary-air-injection inference — is **out
of scope** and absent from every schema, registry rule, and KG node. GDI and early
turbocharging are in scope only for vehicles sold inside the window; the related
enum values (`FuelDeliveryType.GDI`, `BOOST_HISTORY`, `KNOCK_HISTORY`, wideband O₂
types) stay because in-window vehicles use them. `HORIZON_MODERN` is **not deleted**
— it remains a real era bucket and the safe default.

**Consequences.**
- Positive: a coherent, bounded fault taxonomy; no half-implemented Euro 6+ paths.
- Positive: `secondary_air_equipped` is dropped from `EmissionsConfiguration` and
  all DNA views; `SAI_HISTORY` is absent from `DTCRoutingTag` — no orphaned SAI
  surface.
- Negative: vehicles newer than ~2010 are explicitly unsupported; a future Euro 6+
  expansion is a deliberate, scoped project, not an incidental field add.
- Neutral: a few stale inline comments naming "2010-2020 perks" remain in code
  (`vocabulary.py` Horizon.MODERN comment; `eras_sensitivity_masks.yaml`) and are
  tracked for cleanup; they are descriptive only, not functional.

**Alternatives considered.**
1. *Keep `HORIZON_MODERN` as a full Euro 5–6/GPF/wideband tier.* Rejected — pulls
   in post-2010 technology the engine does not model, creating orphaned fields.
2. *Delete `HORIZON_MODERN` entirely.* Rejected — code and wiki use it as a real
   bucket and the safe default; deletion would diverge docs from code.

**References.** `wiki/04_horizon_eras.md` (scope reminder, binding);
`comlab/schemas/vocabulary.py` (`Horizon`, `EuroEmissionCategory`);
`comlab/schemas/ingestion.py::EmissionsConfiguration` (no `secondary_air_equipped`);
DTCLab ADR-0008 (drop SAI_HISTORY from the routing surface).


## Graph relations (explicit)

**ADR-0004** DESCRIBES **Scope petrol 1990–2010 Euro 1–5**
**comlab/core/horizon_context_injector.py** IMPLEMENTS **ADR-0004**
