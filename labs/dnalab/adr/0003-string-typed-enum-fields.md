# ADR 0003 — String-Typed Enum Fields

## Status

Superseded by 0004

## Date

2026-05-17

## Context

`VinDNA` and `SymptomDNA` contain fields whose values come from a fixed vocabulary — `induction_type` ("NATURALLY_ASPIRATED", "TURBOCHARGED", "SUPERCHARGED"), `fuel_delivery_type` ("GDI", "PORT_INJECTION", "CARBURETOR"), `euro_emission_category` ("EURO_1" through "EURO_7"), `confidence` ("HIGH", "PARTIAL", "NONE"), etc. Local `StrEnum` classes exist for every one of these vocabularies (`InductionType`, `FuelDeliveryType`, `EuroEmissionCategory`, `VinConfidence`, etc.), defined in `vinlab/models.py` and `symptomlab/models.py`. However, the dataclass fields themselves are typed as `str`, not as their corresponding `StrEnum` types.

The original plan was to cut over to `from comlab.schemas.vocabulary import ...` once `comlab/schemas/vocabulary.py` shipped in Phase 0b. As of 2026-05-17, that module does not yet exist, and the field types remain `str`.

## Decision

Fields that are logically enumerations (`induction_type`, `fuel_delivery_type`, `euro_emission_category`, `air_metering_strategy`, `confidence`, `primary_load_calculation`, `upstream_o2_type` on `VinDNA`; `tier_1_primary_symptom`, `tier_2_subfield_filter`, `occurs_during`, `engine_state` on `SymptomDNA` and `EnvironmentalConditions`) remain typed as `str`. The parallel `StrEnum` classes are defined locally for documentation and validation but are not used as field types.

This decision will be revisited in T-FX-5, which will replace `str` fields with their `StrEnum` types and record the supersession as ADR 0004.

## Consequences

- **Positive:** Stable JSON serialization — `str` fields serialize as plain strings with no `.value` unwrapping needed. Downstream consumers see the same JSON keys and values regardless of the internal type.
- **Positive:** No compile-time coupling to `comlab.schemas.vocabulary` before that module exists. Each lab is self-contained.
- **Negative:** No compile-time guarantee that a `VinDNA.induction_type` value is one of the three valid strings. A typo in decoder logic (e.g., `"TURBOCHARGD"`) would pass type checking and only surface at runtime in COMLab.
- **Negative:** Two sources of truth for each vocabulary — the `StrEnum` members and the actual set of strings accepted by runtime code. These can drift apart if an enum gains a member that no code path ever produces, or if a code path writes a string that is not an enum member.

## Sources

- `vinlab/models.py` — `TODO(post-vocabulary.py)` block (line 19), `VinDNA` dataclass fields typed as `str` (lines 147–148, 159, 165, 168)
- `symptomlab/models.py` — `SymptomDNA.tier_1_primary_symptom: str`, `tier_2_subfield_filter: str` (lines 37–38)
- `SymptomLab/README.md` — "the (now-superseded) lock on string-typed enum fields awaiting comlab.schemas.vocabulary" per T-FX-1 task context
- `vinlab/decoder.py` — writes string values into VinDNA fields (e.g., `dna.induction_type = raw_ind.strip().upper()` at line 234, `dna.confidence = VinConfidence.HIGH` at line 343 — note: enum member assigned to str-typed field)
