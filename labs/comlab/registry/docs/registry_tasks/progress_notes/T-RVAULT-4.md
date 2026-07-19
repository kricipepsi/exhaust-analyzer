# T-RVAULT-4 — progress note

**Status:** `done` · **Pack:** VAULT (Registry) · completed 2026-06-28
Task spec: `labs/comlab/registry/docs/registry_tasks/T-RVAULT-4_graph_ast_build.md` · Ledger: `labs/comlab/registry/docs/REGISTRY_PROGRESS.md`

## Plan

Build the Pass-1 AST graphs for the registry package and its test suite:
- Scoped package: `labs/comlab/registry/` (excluding `tests/`, `docs/`, and `graph/`) → `labs/comlab/registry/graph/v2_code/`
- Scoped test suite: `labs/comlab/registry/tests/` → `labs/comlab/registry/graph/v2_tests/`
Relocate outputs, verify using `eval_code_graph.py` to ensure both return a `GOOD` verdict (0 dangling, 0 isolated), and clean up all staging resources.

---

## VERIFICATION GATE — T-RVAULT-4

| Phase | Check | Result | Detail |
|---|---|---|---|
| 1 | ruff lint + JSON parse | PASS | 0 violations; 18 JSON files successfully parsed |
| 2 | pyright | PASS | 0 errors |
| 3 | unit tests | PASS | 494 passed / 0 failed |
| 4 | task verification | PASS | Verification bash script ran clean; both graphs present, no root graphify-out, no collateral |
| 5a | rule schema validity | PASS | 18 rulesets validated successfully against schema_v2 via s.RuleSet.model_validate_json |
| 5b | case-ID resolution | PASS | Verified by unit tests (test_every_passes_case_resolves across all rule suites; 0 orphan refs) |
| 5c | harness side-by-side | N/A | Graph build task only; no registry router integration changes |
| 6 | scope check | PASS | Only touched the registry files and graph folders; no out-of-scope files modified |

**Overall: PASS**

---

## CODE REVIEW — T-RVAULT-4

| Section | Item | Result | Note |
|---|---|---|---|
| A | No lab / COMLab / 4DLabWired imports | PASS | No imports from other labs or app |
| A | No ARCHIVE / v2 / v6 imports | PASS | Checked __init__.py files, no legacy imports |
| A | Rules-as-data discipline | PASS | Additions restricted to docstrings in package/test markers |
| A | No diagnostic logic in Python escape hatches | PASS | No python logic modified |
| B | Every rule has passes_cases list | N/A | No rules modified in this task |
| B | Every passes_cases ID resolves in corpus_curated.csv | N/A | No rules modified in this task |
| B | Every numeric threshold has wiki citation | N/A | No rule files modified |
| B | No invented enum values | N/A | No rule files modified |
| B | No solo-survivor rules (≥2 competing rules per family) | N/A | No rule files modified |
| C | All lines trace to Deliverables | PASS | Touched files trace to isolated-node docstring fix and graph builds |
| C | No scope creep | PASS | Task completed strictly in-scope |
| D | Public functions have tests | N/A | No public functions created in this task |
| D | Every changed rule covered by ≥1 passing case | N/A | No rule files changed |

**Blocking findings:** none

**Follow-up rows added to REGISTRY_PROGRESS.md:** none

---

## Lane and Isolated-Node Resolutions

- **Package and test marker isolated node resolution:** The first code and test graph builds reported isolated nodes for `init` (`registry/__init__.py`), `tools_init` (`registry/tools/__init__.py`), and `init` (`tests/__init__.py`). Following the established project pattern in `T-COM-GRAPH-AST`, we resolved this by adding inert module docstrings referencing a wiki source (e.g. `wiki: labs/comlab/registry/docs/REGISTRY_START_HERE.md`), which allows `graphify` to link the nodes via a `rationale_for` edge, reaching `Condition: GOOD` / 0 isolated nodes for both graphs.
- **Offline extraction recipe:** Both extractions were run in isolation via `graphify update` on temporary directories under `/tmp/` to ensure no cross-contamination or inclusion of `docs`/`tests` in `v2_code`. The outputs were then relocated to the final destinations inside the repository.
