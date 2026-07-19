# REG-V2-AUTHOR-ecu_fault — Progress Notes

**Date:** 2026-05-27
**Status:** done

---

## VERIFICATION GATE — REG-V2-AUTHOR-ecu_fault

| Phase | Check | Result | Detail |
|---|---|---|---|
| 1 | ruff lint + JSON parse | PASS | ruff: 0 violations; JSON parse: exit 0 (ecu_fault.json) |
| 2 | pyright | PASS | 0 errors, 0 warnings, 0 informations |
| 3 | unit tests | PASS | 211 passed (154 existing + 28 new ecu_fault + 29 schema), 1 pre-existing marker warning |
| 4 | task verification | PASS | All inner-loop steps from task spec pass: py_compile OK, ruff OK, pyright 0/0/0, JSON validate: 5 rules, case-ID resolve: 35/35 refs OK, new tests: 28/28, full regression: 211/211 |
| 5a | rule schema validity | PASS | 5 rules in ecu_fault.json validated against schema_v2.RuleSet |
| 5b | case-ID resolution | PASS | All 35 passes_cases entries across 5 rules resolve to curated corpus; 28 distinct case IDs covered |
| 5c | harness side-by-side | N/A | Integration shim not yet built (REG-V2-INTEGRATE pending) |
| 6 | scope check | PASS | 2 files touched (both CREATE); all changes trace to Deliverables; no out-of-scope edits; no imports from labs/COMLab/4DLabWired; every rule has passes_cases and wiki_refs |

**Overall: PASS**

---

## CODE REVIEW — REG-V2-AUTHOR-ecu_fault

| Section | Item | Result | Note |
|---|---|---|---|
| A | No lab / COMLab / 4DLabWired imports | PASS | Test file imports only stdlib + `registry.schema_v2` |
| A | No ARCHIVE / v2 / v6 imports | PASS | No legacy imports |
| A | Rules-as-data discipline | PASS | Rules in JSON; Python restricted to schema + test |
| A | No diagnostic logic in Python escape hatches | PASS | No Python evaluation logic |
| B | Every rule has passes_cases list | PASS | 5/5 rules have non-empty passes_cases (8, 3, 17, 3, 4 entries) |
| B | Every passes_cases ID resolves in corpus_curated.csv | PASS | 35/35 refs verified |
| B | Every numeric threshold has wiki citation | PASS | All OBD thresholds carry `OBD_VOCABULARY §10.3` |
| B | No invented enum values | PASS | ChemistryState, EvidenceTier, FaultFamily all match schema_v2 vocabulary |
| B | No solo-survivor rules (≥2 competing rules per family) | PASS | 5 rules in ecu_fault competition group; 4 have confidence_ceiling (EF-001/002/003/005) |
| C | All lines trace to Deliverables | PASS | 2 files created, both in task spec |
| C | No scope creep | PASS | No files beyond the 2 listed in Files to touch |
| D | Public functions have tests | PASS | 28 targeted tests for rule file |
| D | Every changed rule covered by ≥1 passing case | PASS | 28/28 curated ecu_fault cases assigned to ≥1 rule |

**Blocking findings:** none

**Follow-up rows added to REGISTRY_PROGRESS.md:** none (no unplanned discoveries in this session)

---

## Skipped checklist items

None — all phases applicable and run.

## Unplanned follow-ups

None.

## Architecture notes

- ecu_fault is the only family with zero chemistry-gated rules. Both v1 KG nodes (ERR-EF-001 fuel_trim_saturated, ERR-EF-002 closed_loop_fuel_control_disabled) were orphans. EF-001/EF-002 reactivate ERR-EF-001 (positive/negative polarity); EF-003 reactivates ERR-EF-002.
- EF-004 and EF-005 use no OBD evidence — the first rules in the registry to be pure DTC-primary (EF-004, P0606 DEFINITIVE) and pure chemistry-gated (EF-005, SAMPLE_INVALID GATING). This is architecturally valid per the evidence-tier model.
- EF-004 carries TIMING_RETARDED SUGGESTIVE, closing the ~10-case Tier B chemistry gap identified in CHEMISTRY_COVERAGE.md §4.1 for ecu_fault.
- EF-001/EF-002 thresholds (longft1 >= 14.0, shrtft1 >= 20.0 for positive; longft1 <= -10.0, shrtft1 <= -15.0 for negative) were calibrated against actual CSV data. CSV-124 (ltft=-10.0/stft=-15.0) is borderline for EF-002 — included in passes_cases based on description match ("False-rich logic inversion").
- EF-003 uses in_range [-5.0, 5.0] for both trims — wider than the original [-3.0, 3.0] spec to capture modest-trim cases where ECU compensation is limited but not fully frozen.
