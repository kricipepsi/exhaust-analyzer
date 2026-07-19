# ADR 0001 — Naming Contract: VinDNA / SymptomDNA / VehicleDNA

## Status

Accepted

## Date

2026-05-17

## Context

The three labs produce structured payloads that flow into one combined diagnostic object. Before this ADR, the naming convention existed in README files and docstrings but was not recorded as a load-bearing decision. The architecture audit on 2026-05-17 flagged the risk of vocabulary drift — without a locked decision, future contributors could introduce "VehicleDTO," "PartAPayload," or "SymptomRecord" as alternative names, splitting the shared vocabulary across files and breaking the architecture skill's ability to reason about the codebase.

## Decision

**Part A** (the decoded vehicle physical profile from VINLab) is named **`VinDNA`**.
**Part B** (the validated symptom triage from SymptomLab) is named **`SymptomDNA`**.
**Combined** (Part A + Part B + session metadata from DNALab) is named **`VehicleDNA`**.

All three labs, all documentation, and all downstream consumers use these three names exclusively. No synonyms are allowed.

## Consequences

- **Positive:** Shared vocabulary across all three labs — every maintainer, every architecture audit, and every LLM session reads the same names. Downstream labs import `VinDNA` and `SymptomDNA` under their canonical names. The architecture skill's domain-glossary feature can index types unambiguously.
- **Positive:** Future ADRs that reference these types (e.g., serialization contracts, import rules) have stable anchors.
- **Negative:** Requires discipline in code review to reject alternative names. New contributors may initially reach for "DTO" or "record" — the glossary in `CONTEXT.md` is the enforcement point.

## Sources

- `DNALab/README.md` — strict naming table (lines 9–13)
- `VINLab/README.md` — VINLab → VinDNA (line 4)
- `SymptomLab/README.md` — strict naming table (lines 23–25)
- `vinlab/__init__.py` — `__all__ = ["decode", "VinDNA", "VINDecodeError"]`
- `symptomlab/__init__.py` — `__all__ = ["resolve", "SymptomDNA", "EnvironmentalConditions", "SymptomValidationError"]`
- `dnalab/__init__.py` — `__all__ = ["build_vehicle_dna", "VehicleDNA"]`
- `VINLab/VehicleDNA.md` — Part A / Part B / Combined payload structure (lines 79–116)
