## VERIFICATION GATE — REG-V2-AUTHOR-vacuum_leak

| Phase | Check | Result | Detail |
|---|---|---|---|
| 1 | ruff lint + JSON parse | PASS | 0 violations; 15 JSON files parse OK (12 rule files + corpus_meta + corpus_curated.csv) |
| 2 | pyright | PASS | 0 errors |
| 3 | unit tests | PASS | 327 passed, 0 failed (30 new vacuum_leak tests + 297 existing) |
| 4 | task verification | PASS | 4 vacuum_leak cases populated with gas/OBD values; all rule thresholds have 5%+ margin over case values |
| 5a | rule schema validity | PASS | 12 rule files validate against schema_v2.py RuleSet model |
| 5b | case-ID resolution | PASS | 182 case refs across all rule files resolve in corpus_curated.csv; 0 orphan refs |
| 5c | harness side-by-side | N/A | Integration shim does not exist yet — belongs to REG-V2-INTEGRATE |
| 6 | scope check | PASS | All changes trace to 4 deliverables; no files outside scope touched; no lab/COMLab/4DLabWired imports; every rule has passes_cases and wiki_refs |

**Overall: PASS**

---

## CODE REVIEW — REG-V2-AUTHOR-vacuum_leak

| Section | Item | Result | Note |
|---|---|---|---|
| A | No lab / COMLab / 4DLabWired imports | PASS | schema_v2.py + test file use only stdlib + Pydantic |
| A | No ARCHIVE / v2 / v6 imports | PASS | |
| A | Rules-as-data discipline | PASS | Rules in JSON; Python restricted to schema + tests only |
| A | No diagnostic logic in Python escape hatches | PASS | N/A — no rule evaluation code written |
| B | Every rule has passes_cases list | PASS | VL-001: 2 cases, VL-002: 1 case, VL-003: 1 case |
| B | Every passes_cases ID resolves in corpus_curated.csv | PASS | 4 refs, 0 orphans |
| B | Every numeric threshold has wiki citation | PASS | All OBD + chemistry + DTC thresholds carry wiki_ref |
| B | No invented enum values | PASS | LEAN_MIXTURE ∈ ChemistryState; DEFINITIVE/SUGGESTIVE/GATING ∈ EvidenceTier; vacuum_leak ∈ FaultFamily; P0171/P0174 ∈ known DTC codes |
| B | No solo-survivor rules (≥2 competing rules per family) | PASS | 3 rules, all carry confidence_ceiling (0.80 or 0.85) |
| C | All lines trace to Deliverables | PASS | 4 files touched, all in spec |
| C | No scope creep | PASS | No adjacent changes; no other families touched |
| D | Public functions have tests | PASS | N/A — no new public functions (data-only task) |
| D | Every changed rule covered by ≥1 passing case | PASS | VL-001: 2 cases, VL-002: 1 case, VL-003: 1 case; all 4 curated cases covered |

**Blocking findings:** none

**Follow-up rows added to REGISTRY_PROGRESS.md:** none

---

## Threshold-to-case-data margin audit

| Rule | Threshold | Case | Case Value | Margin |
|---|---|---|---|---|
| VL-001 | longft1 ge 10.0 | NEW-vacuum_leak-01 | 15.0 | 50% |
| VL-001 | shrtft1 ge 5.0 | NEW-vacuum_leak-01 | 8.0 | 60% |
| VL-001 | map_kpa gt 40.0 | NEW-vacuum_leak-01 | 48 | 20% |
| VL-001 | map_kpa gt 40.0 | NEW-vacuum_leak-04 | 50 | 25% |
| VL-002 | longft1 ge 8.0 | NEW-vacuum_leak-02 | 12.0 | 50% |
| VL-002 | shrtft1 ge 3.0 | NEW-vacuum_leak-02 | 5.0 | 67% |
| VL-003 | map_kpa gt 50.0 | NEW-vacuum_leak-03 | 60 | 20% |
| VL-003 | longft1 ge 15.0 | NEW-vacuum_leak-03 | 25.0 | 67% |
| VL-003 | shrtft1 ge 10.0 | NEW-vacuum_leak-03 | 20.0 | 100% |

All margins ≥ 10%, no measurement-tolerance faults. The tightest boundary (VL-001 MAP > 40 with NEW-vacuum_leak-02 at 44 kPa, 10% margin) is DTC-gated by VL-002 for that case — VL-002's P0171 GATING provides the primary path.
