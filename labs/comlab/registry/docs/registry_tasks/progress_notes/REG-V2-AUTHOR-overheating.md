# REG-V2-AUTHOR-overheating — Progress Notes

**Date:** 2026-05-28
**Task file:** `registry_tasks/REG-V2-AUTHOR-overheating.md`
**Files changed:** 4
- `registry/rules/overheating.json` (CREATE — 4 rules OV-001..OV-004)
- `registry/tests/test_overheating_rules.py` (CREATE — 32 tests)
- `registry/corpus_curated.csv` (MODIFY — 4 rows NEW-overheating-01..04 populated)
- `registry/corpus_meta.json` (MODIFY — 4 `notes` fields plus `dtcs`/`chemistry_signature` updates for OV-02/03)

**Headline:** 4 rules authored covering 4 distinct overheating etiologies (thermostat stuck, thermostat-with-DTC, head gasket, silent fan failure); 4/4 placeholder cases populated; 4/4 case refs resolve; 32 new tests green; 359/359 full registry suite green; ruff 0, pyright 0; schema 5a+5b clean across all 12 rule files (58 rules, 186 case refs).

---

## VERIFICATION GATE — REG-V2-AUTHOR-overheating

| Phase | Check | Result | Detail |
|---|---|---|---|
| 1 | ruff lint + JSON parse | PASS | `ruff check registry/` all checks passed; 13/13 JSON files parse OK |
| 2 | pyright | PASS | 0 errors, 0 warnings, 0 informations |
| 3 | unit tests | PASS | 359 passed, 1 warning (pre-existing unknown `pytest.mark.integration` in `test_build_corpus.py`, unrelated to this task) |
| 4 | task verification | PASS | All commands from task `### Verification ###` exit 0; all 4 NEW-overheating rows populated; 4 case refs resolve; RuleSet validates as `family=overheating, rules=4` |
| 5a | rule schema validity | PASS | 12 rule files, 58 rules total validate against `RuleSet` model |
| 5b | case-ID resolution | PASS | 186 case refs across all rule files resolve; 0 orphans |
| 5c | harness side-by-side | N/A | REG-V2-INTEGRATE not yet started — no integration shim exists |
| 6 | scope check | PASS | Only the 4 declared files modified; no banned imports; OV-001/002/004 carry empty `chemistry_evidence`; OV-003 carries COOLANT_LEAK_INTERNAL SUGGESTIVE; every numeric threshold cites OBD_VOCABULARY §23.1/§23.2 or DTC_VOCABULARY §4 or GAS_VOCABULARY §3 |

**Overall: PASS**

---

## CODE REVIEW — REG-V2-AUTHOR-overheating

| Section | Item | Result | Note |
|---|---|---|---|
| A | No lab / COMLab / 4DLabWired imports | PASS | Test imports only `registry.schema_v2`; rule JSON has no Python imports |
| A | No ARCHIVE / v2 / v6 imports | PASS | None present |
| A | Rules-as-data discipline | PASS | All rule content in `rules/overheating.json`; no Python evaluation logic added |
| A | No diagnostic logic in Python escape hatches | PASS | No callbacks or eval blocks anywhere |
| B | Every rule has passes_cases list | PASS | All 4 rules carry ≥ 1 case ID |
| B | Every passes_cases ID resolves in corpus_curated.csv | PASS | 4/4 refs resolve (Phase 5b) |
| B | Every numeric threshold has wiki citation | PASS | ECT thresholds → `OBD_VOCABULARY §23.1`; RPM → `OBD_VOCABULARY §23.2`; DTCs → `DTC_VOCABULARY §4`; chemistry → `GAS_VOCABULARY §3` |
| B | No invented enum values | PASS | `overheating` family + `COOLANT_LEAK_INTERNAL` chemistry + DTC strings/operators all exist in `schema_v2.py` |
| B | No solo-survivor rules (≥2 competing rules per family) | PASS | 4 rules in `competition_group="overheating"`; all 4 carry `confidence_ceiling` (0.70, 0.82, 0.85, 0.85) |
| C | All lines trace to Deliverables | PASS | Each of the 4 changed files is named in the task's `### Files to touch ###` and matches a Deliverable item |
| C | No scope creep | PASS | No edits outside the declared files; placeholder note updates kept inline with the existing `notes` field |
| D | Public functions have tests | PASS | No new public Python functions added; the new test file is the test surface |
| D | Every changed rule covered by ≥1 passing case | PASS | OV-001↔NEW-overheating-01, OV-002↔-02, OV-003↔-03, OV-004↔-04 |

**Blocking findings:** none

**Follow-up rows added to REGISTRY_PROGRESS.md:** none

---

## Design notes

- **OBD-primary, chemistry-light family.** The task spec correctly identified that classic overheating at idle does not raise NOx to `HIGH_COMBUSTION_TEMP` (1500 ppm per GAS_VOCABULARY §10.5) on a street engine — engines at idle produce negligible NOx regardless of coolant temperature. Three of four rules carry empty `chemistry_evidence`, matching the pattern in `ecu_fault.json` (EF-001/002/003).
- **OV-003 chemistry is SUGGESTIVE, not DEFINITIVE.** Head-gasket / coolant-loss cases produce a recognisable gas fingerprint (CO₂ displaced by steam, NOx suppressed, HC raised — GAS_WIKI §7.32 pattern) but emission of `COOLANT_LEAK_INTERNAL` by GASLab's rule engine is not guaranteed at the synthetic values used in NEW-overheating-03; ceiling lowered to 0.82 accordingly.
- **OV-004 ceiling 0.70.** The fan-failure rule has the weakest signal set (ELEVATED_TEMP ECT only, RPM lt 1000 as the discriminator from OV-001). The lowered ceiling reflects that this rule fires on circumstantial evidence rather than a definitive overheat threshold.
- **OBD PID conventions.** Used `ect_c` (matching the `schema_v2.OBDEvidence.pid` docstring example and the existing `mechanical_wear.json` / `non_starter.json` usage) and `rpm` (no unit suffix, matching all 5 existing rule-file uses).
- **CSV column-count integrity.** All 4 modified rows parse via `csv.DictReader` with the expected 66-column header — no field-count drift introduced by the inline replacement.

## What was skipped

Nothing in the checklist was skipped. Phase 5c is N/A because REG-V2-INTEGRATE has not been started yet — same N/A status as every prior REG-V2-AUTHOR-* task.

## Open follow-ups discovered (none added to ledger this session)

None. The task scope was self-contained and produced no incidental findings.
