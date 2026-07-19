# REG-V2-AUTHOR-sensor_fault — Progress Note

**Date:** 2026-05-27

## VERIFICATION GATE — REG-V2-AUTHOR-sensor_fault

| Phase | Check | Result | Detail |
|---|---|---|---|
| 1 | ruff lint + JSON parse | PASS | 0 violations; 1 JSON file (7 rules) parses |
| 2 | pyright | PASS | 0 errors, 0 warnings, 0 informations |
| 3 | unit tests | PASS | 183 passed, 0 failed (33 new + 150 existing) |
| 4 | task verification | PASS | All commands from task spec exited 0 |
| 5a | rule schema validity | PASS | 7 rules validated against RuleSet model |
| 5b | case-ID resolution | PASS | 19/19 case refs resolve in corpus_curated.csv |
| 5c | harness side-by-side | N/A | Integration shim not yet built (REG-V2-INTEGRATE) |
| 6 | scope check | PASS | 2 files touched (CREATE only); no out-of-scope edits |

**Overall: PASS**

### Phase 6 detail
- 2 files created: `registry/rules/sensor_fault.json`, `registry/tests/test_sensor_fault_rules.py`
- No files outside task scope modified
- No imports from any lab, COMLab, or 4DLabWired
- Every rule has `passes_cases` list (19 distinct case IDs across 7 rules)
- Every numeric threshold has `wiki_ref` citation
- No invented enum values

### Task spec deviations (documented)
- 6 rules → 7 rules: SF-007 added for O2 heater circuit faults (P0053) per OBD_VOCABULARY §12.4 O2FailureMode taxonomy. SF-001/SF-002 cover bias drift only.
- SF-004 chemistry_evidence: [] — TIMING_RETARDED dropped. GAS_VOCABULARY §7.13 describes knock-avoidance, not MAF error path. No wiki support.
- SF-004 perception_flag dropped — MAF_UNDER_READING not in ChemistryState enum; would be dead routing in fault_atlas_router.py.
- SF-005 perception_flag dropped — MAP_DRIFT not in ChemistryState enum.
- case_046 (P0190 fuel rail pressure) not assigned to any rule — no KG node matches. Flagged as follow-up.
- `ect_c` used per schema_v2.py:160 convention instead of `ect`.
- `o2_voltage` documented as freeze-frame sourced (not in OBDLivePayload) via `precondition` field.

---

## CODE REVIEW — REG-V2-AUTHOR-sensor_fault

| Section | Item | Result | Note |
|---|---|---|---|
| A | No lab / COMLab / 4DLabWired imports | PASS | Registry self-contained; only schema_v2 + stdlib |
| A | No ARCHIVE / v2 / v6 imports | PASS | |
| A | Rules-as-data discipline | PASS | Rules in JSON; Python is test only |
| A | No diagnostic logic in Python escape hatches | N/A | No Python evaluation code in this task |
| B | Every rule has passes_cases list | PASS | 7/7 rules, 19 distinct case IDs |
| B | Every passes_cases ID resolves in corpus_curated.csv | PASS | 19/19 resolve |
| B | Every numeric threshold has wiki citation | PASS | All OBD + chemistry + DTC evidence carries wiki_ref |
| B | No invented enum values | PASS | All ChemistryState + EvidenceTier values valid |
| B | No solo-survivor rules (≥2 competing rules per family) | PASS | 7 rules in competition_group "sensor_fault"; 5 carry confidence_ceiling |
| C | All lines trace to Deliverables | PASS | 2 files, both in task spec |
| C | No scope creep | PASS | No files outside "Files to touch" |
| D | Public functions have tests | PASS | RuleSet validation tested; all OBD PID + chemistry + DTC coverage tested |
| D | Every changed rule covered by ≥1 passing case | PASS | 19/19 case refs resolve |

**Blocking findings:** none

**Follow-up rows added to REGISTRY_PROGRESS.md:** case_046 (P0190 fuel rail pressure sensor) — no matching KG node in current 7-rule set. Needs dedicated pressure-sensor rule or ecu_fault coverage.
