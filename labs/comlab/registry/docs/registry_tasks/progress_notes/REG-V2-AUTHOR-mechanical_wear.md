## VERIFICATION GATE — REG-V2-AUTHOR-mechanical_wear

| Phase | Check | Result | Detail |
|---|---|---|---|
| 1 | ruff lint + JSON parse | PASS | 0 violations; 9 JSON rule files parse OK |
| 2 | pyright | PASS | 0 errors, 0 warnings on registry/ |
| 3 | unit tests | PASS | 268 passed (211 existing + 28 new mechanical_wear + 29 build_corpus), 0 failed |
| 4 | task verification | PASS | schema validate: 6 rules in family mechanical_wear; JSON parse OK; all case refs resolve |
| 5a | rule schema validity | PASS | 9 rule files validate against schema_v2.py (cam_timing, catalyst_failure, ecu_fault, exhaust_leak, lean_condition, mechanical_wear, misfire, rich_mixture, sensor_fault) |
| 5b | case-ID resolution | PASS | 171 case refs across 9 rule files all resolve in corpus_curated.csv; 0 orphan refs |
| 5c | harness side-by-side | N/A | REG-V2-INTEGRATE not yet executed — integration shim and flag-gated wiring pending |
| 6 | scope check | PASS | Only 2 files touched (mechanical_wear.json CREATE, test_mechanical_wear_rules.py CREATE). No out-of-scope edits. No lab/COMLab/4DLabWired imports. All 6 rules carry passes_cases. All numeric thresholds carry wiki_ref citations. |

**Overall: PASS**

## CODE REVIEW — REG-V2-AUTHOR-mechanical_wear

| Section | Item | Result | Note |
|---|---|---|---|
| A | No lab / COMLab / 4DLabWired imports | PASS | Only imports registry.schema_v2 + stdlib in test file; rule file is JSON |
| A | No ARCHIVE / v2 / v6 imports | PASS | No legacy imports |
| A | Rules-as-data discipline | PASS | Rule content in JSON; Python restricted to schema (schema_v2.py) and tests |
| A | No diagnostic logic in Python escape hatches | PASS | No Python evaluation logic; rule logic is declarative evidence-tier JSON |
| B | Every rule has passes_cases list | PASS | All 6 rules carry passes_cases (15 total case refs, all 11 mechanical_wear cases covered) |
| B | Every passes_cases ID resolves in corpus_curated.csv | PASS | 0 orphan refs confirmed by phase 5b |
| B | Every numeric threshold has wiki citation | PASS | ect_c > 95.0 → OBD_VOCABULARY §8; map_kpa < 30.0 → OBD_VOCABULARY §6; rpm > 600 → OBD_VOCABULARY §5; all chemistry states → GAS_VOCABULARY §3; DTC none_present → DTC_VOCABULARY §4 |
| B | No invented enum values | PASS | All ChemistryState, EvidenceTier, FaultFamily, DTCRoutingTag values from schema_v2.py vocabulary |
| B | No solo-survivor rules (≥2 competing rules per family) | PASS | 6 rules in competition_group mechanical_wear; 3 carry confidence_ceiling (MW-002: 0.85, MW-005: 0.85, MW-006: 0.85) |
| C | All lines trace to Deliverables | PASS | Deliverable 1 (mechanical_wear.json) + Deliverable 2 (test_mechanical_wear_rules.py) only |
| C | No scope creep | PASS | No adjacent files modified; no reformatting; no speculative abstractions |
| D | Public functions have tests | PASS | N/A for JSON rule files; test file contains 28 test functions covering all 6 rules |
| D | Every changed rule covered by ≥1 passing case | PASS | All 11 mechanical_wear cases covered by ≥1 rule; MECH-006 and EXT-222 covered by 3 competing rules |

**Blocking findings:** none

**Follow-up rows added to REGISTRY_PROGRESS.md:** none
