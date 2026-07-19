## VERIFICATION GATE — REG-V2-AUTHOR-exhaust_leak

| Phase | Check | Result | Detail |
|---|---|---|---|
| 1 | ruff lint + JSON parse | PASS | ruff 0 violations; 6 JSON files parse OK (5 rule files + corpus_meta.json) |
| 2 | pyright | PASS | 0 errors, 0 warnings, 0 informations |
| 3 | unit tests | PASS | 150 passed, 0 failed, 1 warning (pre-existing pytest.mark.integration) |
| 4 | task verification | PASS | All commands from task file Verification section executed and passed |
| 5a | rule schema validity | PASS | 5 rule files, all RuleSets validate against schema_v2 |
| 5b | case-ID resolution | PASS | All 5 case refs resolve (CSV-095, TC-048, YAML-CSV95, case_045, PDF-HI-007) |
| 5c | harness side-by-side | N/A | Integration shim not yet implemented — belongs to REG-V2-INTEGRATE |
| 6 | scope check | PASS | Only 2 files created (both in Files to touch); no out-of-scope edits; no lab/COMLab/4DLabWired imports; every rule has passes_cases; every numeric threshold has wiki_ref |

**Overall: PASS**

---

## CODE REVIEW — REG-V2-AUTHOR-exhaust_leak

| Section | Item | Result | Note |
|---|---|---|---|
| A | No lab / COMLab / 4DLabWired imports | PASS | Test file imports only schema_v2 + stdlib |
| A | No ARCHIVE / v2 / v6 imports | PASS | No legacy imports |
| A | Rules-as-data discipline | PASS | Rules are JSON; Python is schema + tests only |
| A | No diagnostic logic in Python escape hatches | N/A | No Python evaluation code — rules are pure data |
| B | Every rule has passes_cases list | PASS | EL-001 (3), EL-002 (1), EL-003 (1) — all non-empty |
| B | Every passes_cases ID resolves in corpus_curated.csv | PASS | 5/5 case refs resolve |
| B | Every numeric threshold has wiki_ref citation | PASS | Verified by test_no_bare_numeric_thresholds |
| B | No invented enum values | PASS | Verified by test_no_invented_chemistry_states + test_no_invented_evidence_tiers |
| B | No solo-survivor rules (>=2 competing rules per family) | PASS | 3 rules in exhaust_leak competition group; EL-002 (wt 0.75, ceiling 0.85), EL-003 (wt 0.65, ceiling 0.80), EL-001 (wt 0.80, no ceiling needed — 3 rules > 1) |
| C | All lines trace to Deliverables | PASS | exhaust_leak.json + test_exhaust_leak_rules.py match task spec |
| C | No scope creep | PASS | 2 files created, both in Files to touch |
| D | Public functions have tests | N/A | No new Python functions — rules are JSON data |
| D | Every changed rule covered by >=1 passing case | PASS | All 5 curated exhaust_leak cases assigned to rules |

**Blocking findings:** none

**Follow-up rows added to REGISTRY_PROGRESS.md:** none

---

## Task summary

- Collapsed v1's 6 redundant LTFT-threshold rules (ERR-EL-001/002/003/005) into EL-001 (pre-cat, EXHAUST_AIR_LEAK + LTFT + P0171)
- Added EL-002 (post-cat, EXHAUST_AIR_LEAK + P2096 + downstream O2) — no v1 equivalent for P2096 path
- Replaced ERR-EL-004 (NORMAL_OPERATION, false-positive risk) and ERR-EL-006 (chemistry-only, too weak) with EL-003 (probe-tip, EXHAUST_AIR_LEAK + HC + O2)
- 21 new tests; 150 full suite green; ruff 0; pyright 0
