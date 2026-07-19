# Progress Notes — REG-V2-AUTHOR-cam_timing

**Date:** 2026-05-27
**Commit:** (pending)

---

## VERIFICATION GATE — REG-V2-AUTHOR-cam_timing

| Phase | Check | Result | Detail |
|---|---|---|---|
| 1 | ruff lint + JSON parse | PASS | ruff 0 violations; 9 JSON files parsed OK (8 existing + cam_timing.json) |
| 2 | pyright | PASS | 0 errors on touched files; 1 pre-existing error in test_build_corpus.py:14 (unrelated import) |
| 3 | unit tests | PASS | 240 passed (182 existing + 29 cam_timing + 29 build_corpus); 1 pre-existing pytest warning |
| 4 | task verification | PASS | All commands from task spec executed; py_compile ok; schema validate ok; case-ID resolve ok; targeted tests 29/29; full regression 240/240 |
| 5a | rule schema validity | PASS | 6 rules validated against schema_v2.py RuleSet model |
| 5b | case-ID resolution | PASS | All 13 case refs resolve to curated corpus; all 8 coverable cam_timing cases claimed; EXP-N023 excluded per spec |
| 5c | harness side-by-side | N/A | Integration shim not yet built; REG-V2-INTEGRATE is pending |
| 6 | scope check | PASS | 2 files created (exactly matching Files to touch); no out-of-scope edits; no imports from labs/COMLab/4DLabWired; every rule has passes_cases + wiki_refs; 4 rules carry confidence_ceiling |

**Overall: PASS**

---

## CODE REVIEW — REG-V2-AUTHOR-cam_timing

| Section | Item | Result | Note |
|---|---|---|---|
| A | No lab / COMLab / 4DLabWired imports | PASS | rules file is JSON (no imports); test file imports only stdlib + registry.schema_v2 |
| A | No ARCHIVE / v2 / v6 imports | PASS | No legacy imports |
| A | Rules-as-data discipline | PASS | All 6 rules are JSON data; no Python evaluation logic |
| A | No diagnostic logic in Python escape hatches | N/A | No Python rule logic; all evidence is structured data |
| B | Every rule has passes_cases list | PASS | CT-001: 1 case, CT-002: 6 cases, CT-003: 2 cases, CT-004: 1 case, CT-005: 1 case, CT-006: 2 cases |
| B | Every passes_cases ID resolves in corpus_curated.csv | PASS | All 13 case refs resolve |
| B | Every numeric threshold has wiki citation | PASS | All OBD thresholds carry wiki_ref; all chemistry evidence carries wiki_ref; all DTC evidence carries wiki_ref |
| B | No invented enum values | PASS | All ChemistryState, EvidenceTier, FaultFamily values are valid schema_v2 members |
| B | No solo-survivor rules (≥2 competing rules per family) | PASS | 6 rules in cam_timing competition group; 4 have confidence_ceiling (CT-003: 0.85, CT-004: 0.85, CT-005: 0.85, CT-006: 0.85) |
| C | All lines trace to Deliverables | PASS | 2 files created — both in task spec Deliverables list |
| C | No scope creep | PASS | No files outside Files to touch modified; no reformatting of adjacent code |
| D | Public functions have tests | PASS | 29 targeted tests covering structure, chemistry evidence, OBD evidence, DTC evidence, contract integrity, competition group, case coverage, enum validity |
| D | Every changed rule covered by ≥1 passing case | PASS | All 6 rules have passes_cases with curated case IDs; all 13 refs resolve |

**Blocking findings:** none

**Follow-up rows added to REGISTRY_PROGRESS.md:** EXP-N023-uncoverable

---

## Unplanned follow-ups

| ID | One-liner | Status |
|---|---|---|
| EXP-N023-uncoverable | EXP-N023 (VVT solenoid resistance drift 8→40Ω, no DTC, no MAP, no RPM) is uncoverable with the current OBD PID set. Solenoid resistance is not among the captured PIDs. Needs richer OBD capture (solenoid current/resistance PID) before a rule can claim it. | pending |

## Scope note

CT-005 was narrowed during scoping: the original MAP/RPM gate was dropped because all 9 cam_timing cases have empty `map` and `rpm` columns in the curated CSV. CT-005 is now DTC-primary (VVT_HISTORY range as GATING) with trim-near-zero OBD as SUGGESTIVE. EXP-N023 is explicitly excluded from all passes_cases and logged as the follow-up above.
