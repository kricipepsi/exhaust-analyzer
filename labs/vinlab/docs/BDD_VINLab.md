# BDD — VINLab (v2)

**Status:** Current (scenarios grounded in the decoder behaviour + test fixtures)
**Reference:** HLD_VINLab v2.0 / DLD_VINLab v2.0 / LLD_VINLab v2.0
**Date:** 2026-06-11

Behaviour specification for VINLab's single public behaviour: **decode a 17-character
VIN into a typed `VinDNA`**. Scenarios are declarative (diagnostic/identity focus). The
truth is the decoder source + `tests/`; these scenarios capture executable-spec intent.

Ubiquitous language: *decode* = run `vinlab.decode()`; *in-scope* = petrol, model year
1990–2020; *graded* = assigned a `VinConfidence`; *passthrough* = a year character that
maps to `model_year = None`.

---

## Feature: Decode happy path

```gherkin
Feature: A well-formed in-scope VIN decodes to a graded VinDNA

  Scenario: A clean petrol VIN with full reference data
    Given a 17-character VIN that passes charset and checksum
      And the WMI, year, and engine code all resolve from reference data
      And the engine row is present in vref.db with no NULL CoC fields
    When the VIN is decoded
    Then a VinDNA is returned
      And confidence = HIGH
      And induction_type, fuel_delivery_type and air_metering_strategy are enum-typed
      And the VinDNA serialises to JSON and reloads unchanged
```
*Maps to:* decoder happy-path fixtures under `tests/fixtures/`.

---

## Feature: Structural validation

```gherkin
Feature: Malformed input is rejected before any resolution

  Scenario: Input is not 17 characters
    Given an input string of length 15
    When the VIN is decoded
    Then a ChassisNumberError is raised (a VINDecodeError subclass)

  Scenario: Visually ambiguous characters are recovered before validation
    Given a VIN containing the letters I and O
    When the VIN is decoded
    Then I is substituted with 1 and O with 0 before the charset check

  Scenario: An invalid character set is rejected
    Given a cleaned VIN containing a Q
    When the VIN is decoded
    Then a VINDecodeError is raised (invalid characters)
```
*Maps to:* `pre_clean_vin`, length guard, `_VIN_PATTERN` check.

---

## Feature: Checksum with market-aware bypass

```gherkin
Feature: The NHTSA checksum guards North American VINs but bypasses non-NHTSA markets

  Scenario: A North American VIN with a wrong check digit fails
    Given a VIN whose WMI country is the USA and whose position-9 digit is wrong
    When the VIN is decoded
    Then a VINDecodeError is raised (checksum validation failed)

  Scenario: A European VIN without a check digit is accepted
    Given a VIN whose WMI country is in the European set
    When the checksum is validated
    Then validation is bypassed and decoding continues

  Scenario: A known OPSI corrupt-prefix VIN is accepted
    Given a VIN beginning with 3MZ, 3MD, or 3MV
    When the checksum is validated
    Then validation is bypassed (corrupt pos-9 in the source data)
```
*Maps to:* `validate_vin_checksum` (three bypass paths).

---

## Feature: WMI and low-volume manufacturers

```gherkin
Feature: WMI resolves standard and low-volume manufacturers

  Scenario: A standard manufacturer resolves from positions 1-3
    Given a VIN whose first three characters are a known WMI
    When the WMI is resolved
    Then the brand and country are taken from that WMI record

  Scenario: A low-volume manufacturer uses the extended WMI
    Given a VIN whose third character is 9
    When the WMI is resolved
    Then the 6-character key (positions 1-3 + 12-14) is tried first

  Scenario: An unknown WMI is a decode failure
    Given a VIN whose WMI is not in the registry
    When the WMI is resolved
    Then a VINDecodeError is raised (WMI not found)
```
*Maps to:* `_resolve_wmi`.

---

## Feature: Model-year resolution and the L collision

```gherkin
Feature: Year resolution handles passthrough characters and the 1990/2020 collision

  Scenario: A passthrough year character yields an unknown year
    Given a VIN whose position-10 character is 0, U, or Z
    When the year is resolved
    Then model_year is None (unknown, not an error)

  Scenario Outline: The L year is disambiguated by the WMI era hint
    Given a VIN with year code L and WMI era_hint = <hint>
    When the year is resolved
    Then model_year = <year>

    Examples:
      | hint    | year |
      | legacy  | 1990 |
      | modern  | 2020 |

  Scenario: A year outside the supported window is out of scope
    Given a resolved model_year of 2023
    When the scope guard runs
    Then a VINDecodeError is raised (year out of supported scope 1990-2020)
```
*Maps to:* `_resolve_year`, H2 guard.

---

## Feature: Petrol-only scope guard (H1)

```gherkin
Feature: Non-petrol vehicles are out of scope

  Scenario: A diesel fuel keyword in the CSV row is rejected
    Given an engine row whose fuel_system_type contains DIESEL
    When the VIN is decoded
    Then a VINDecodeError is raised (fuel type out of scope)

  Scenario: A non-petrol fuel keyword in the vref.db row is rejected
    Given a vref.db row whose fuel_delivery_type contains LPG, CNG, E85, HYBRID, or ELECTRIC
    When the VIN is decoded
    Then a VINDecodeError is raised (fuel type out of scope)
```
*Maps to:* `_is_non_petrol` (CSV + vref.db checks).

---

## Feature: Two-path engine resolution

```gherkin
Feature: Engine resolves from the modern VDS or the legacy position-8 fallback

  Scenario: Modern five-character VDS match
    Given a VIN whose brand + positions 4-8 match a vds_full key
    When the engine is resolved
    Then the full-VDS row is returned

  Scenario: Legacy single-character position-8 fallback
    Given no vds_full match but a brand + position-8 match
    When the engine is resolved
    Then the pos_8_only row is returned

  Scenario: No engine match downgrades confidence to NONE
    Given neither path matches
    When the VIN is decoded
    Then engine_not_in_csv is flagged and confidence = NONE
```
*Maps to:* `_resolve_engine`, confidence grading.

---

## Feature: Overlay derivations

```gherkin
Feature: Derived fields come from deterministic overlay rules

  Scenario Outline: Air metering is classified once into both labels
    Given has_maf = <maf> and has_map = <map>
    When air metering is classified
    Then primary_load_calculation = <plc> and air_metering_strategy = <strategy>

    Examples:
      | maf  | map  | plc            | strategy                 |
      | true | true | HYBRID_MAF_MAP | DUAL_MAF_MAP_CROSSCHECK  |
      | true | false| MAF_ONLY       | MAF_ONLY                 |
      | false| true | MAP_ONLY       | MAP_ONLY_SPEED_DENSITY   |
      | false| false| MAP_ONLY       | MAP_ONLY_SPEED_DENSITY   |

  Scenario: Stress-idle RPM is targeted by era + induction + fuel
    Given a EURO_1 naturally-aspirated engine
    When the stress-idle RPM is derived
    Then stress_idle_rpm_target = 3000

  Scenario: Cylinder count is inferred only when unresolved
    Given cylinder_count is still 0 after CSV and vref.db
      And a recognised brand + engine code
    When the cylinder heuristic runs
    Then a brand-rule cylinder count is applied
    But it never overwrites a non-zero CSV or vref.db count
```
*Maps to:* `classify_air_metering`, `stress_idle_rpm`, `infer_cylinder`.

---

## Feature: Offline + isolation guarantees (CI-level behaviour)

```gherkin
Feature: VINLab stays offline and isolated

  Scenario: Decoding makes no network or MySQL call
    Given the vinlab package and baked vinlab/data/
    When a VIN is decoded
    Then only local CSV reads and a read-only vref.db query occur

  Scenario: No cross-lab Python imports exist
    Given the vinlab package
    When the import-isolation audit runs
    Then there are no imports from gaslab, obdlab, dtclab, comlab, or symptomlab

  Scenario: All SQL is confined to the db layer
    Given the vinlab package
    When the SQL-isolation audit runs
    Then SQL strings appear only in db/tecdoc_query.py
```
*Maps to:* offline-runtime constraint, DNA-family boundary, H8.

---

## Traceability summary

| Behaviour area | Primary location |
|----------------|------------------|
| End-to-end decode | `decode()` / `decode_vin_payload`, `tests/fixtures/` |
| Structural validation | `pre_clean_vin`, length/charset guards |
| Checksum + bypass | `validate_vin_checksum` |
| WMI / year resolution | `_resolve_wmi`, `_resolve_year` |
| Scope guards (H1/H2) | `_is_non_petrol`, year bound |
| Engine resolution | `_resolve_engine` |
| Overlays | `overlay/air_metering`, `horizon`, `stress_rpm`, `switches`, `cylinder_heuristic` |
| Confidence grading | decoder flag collection |
| Isolation / SQL | DNA-family boundary, `db/tecdoc_query.py` |
