# ADR 0004 — Enum-Typed Fields

## Status

Accepted

## Supersedes

0003 (String-Typed Enum Fields)

## Date

2026-05-17

## Context

`VinDNA` and `SymptomDNA` contain fields whose values come from a fixed vocabulary. Local `StrEnum` classes (`InductionType`, `FuelDeliveryType`, `EuroEmissionCategory`, `VinConfidence`, `AirMeteringStrategy`, `PrimaryLoadCalculation`, `UpstreamO2Type`, `OccursDuring`, `EngineState`) were defined in `vinlab/models.py` and `symptomlab/models.py` but the dataclass fields themselves were typed as `str`, not as their corresponding `StrEnum` types. ADR 0003 codified this as a deliberate trade-off — no compile-time guarantee of value-set membership in exchange for avoiding coupling to a not-yet-existent `comlab.schemas.vocabulary` module.

The `comlab.schemas.vocabulary` module does not exist yet and its shipping date in Phase 0b is unbounded. Meanwhile, the absence of enum-typed fields means:

- A typo in decoder logic (e.g., `"TURBOCHARGD"`) passes type checking and only surfaces at runtime in COMLab.
- Two sources of truth for each vocabulary — the `StrEnum` members and the actual set of strings accepted by runtime code — can drift apart.
- The `from_json` deserialization path accepts any string, with no validation that the string is a member of the expected vocabulary.

The user confirmed on 2026-05-17 that the lock recorded in ADR 0003 should be broken now, as part of the DNALab Architecture Fixes pack (T-FX-5).

## Decision

Every enum-shaped field on `VinDNA`, `AirMeteringArchitecture`, `Emissions`, `SymptomDNA`, and `EnvironmentalConditions` is typed as its corresponding `StrEnum` instead of `str`. The decoder, overlay modules, and `from_json` constructors all produce and validate enum members.

`tier_1_primary_symptom` and `tier_2_subfield_filter` on `SymptomDNA` remain typed as `str` — they represent open vocabularies validated by the YAML symptom catalog, not a fixed enum. Adding a symptom to the catalog must not require a code change.

The enum definitions themselves remain in `vinlab/models.py` and `symptomlab/models.py`. The future cut-over to `from comlab.schemas.vocabulary import ...` is a one-line import swap — no schema or wire-format change occurs when that happens.

## Consequences

- **Positive:** Pyright now catches invalid enum assignments at development time. A typo like `InductionType("TURBOCHARGD")` raises `ValueError` the moment it is constructed, not silently downstream.
- **Positive:** `from_json` validates incoming enum strings against the `StrEnum` value set. Passing `"TUNA_SALAD"` for `fuel_delivery_type` raises `ValueError`.
- **Positive:** The JSON wire format is unchanged. `StrEnum.value` is the same string that was previously stored in the `str`-typed field (`EuroEmissionCategory.EURO_6.value == "EURO_6"`). Round-trip tests against fixtures captured before this change remain byte-identical.
- **Positive:** Callers that compare enum fields against string literals continue to work — `StrEnum` instances compare equal to their string value (`InductionType.NATURALLY_ASPIRATED == "NATURALLY_ASPIRATED"` is `True`).
- **Negative:** The `StrEnum` constructor raises `ValueError` on unrecognized input. If vref.db or CSV data contains an unexpected value for an enum-shaped field, the decoder will raise at that point rather than silently propagating the bad value. This is acceptable because the data is controlled and a `ValueError` is a clear failure signal (fail-fast) rather than a silent data corruption path.

## Future cut-over to comlab.schemas.vocabulary

When `comlab.schemas.vocabulary` ships in Phase 0b:

1. Replace each local `class Foo(StrEnum)` with `from comlab.schemas.vocabulary import Foo`.
2. Remove the local enum definitions from `vinlab/models.py` and `symptomlab/models.py`.
3. No field type, default, constructor call, or test needs to change — the enum members are identical.

## Sources

- `vinlab/models.py` — enum definitions, VinDNA/AirMeteringArchitecture/Emissions field types, `from_json`
- `symptomlab/models.py` — OccursDuring/EngineState usage, docstring note on tier_1/tier_2
- `vinlab/decoder.py` — decoder assignments using enum members
- `vinlab/overlay/air_metering.py` — `AirMeteringClassification` with enum-typed fields
- `vinlab/overlay/switches.py` — `derive_upstream_o2_type` returning `UpstreamO2Type`
- ADR 0003 — previous decision to defer enum typing, now superseded
- T-FX-5 task prompt in `architecture_fixes/task_files/T-FX-5_enum_typed_fields.md`
