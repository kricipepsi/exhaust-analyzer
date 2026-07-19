# T-GAS-TESTPREP — AST-legibility audit of the GASLab `tests/` tree

**Status:** `void — folded into T-GAS-CODEPREP` · **Pack:** VAULT (GASLab) · completed 2026-06-11 (coder)
Task spec: `Vault/tasks/T-GAS-TESTPREP_*.md` · Pack ledger: `Vault/tasks/GAS_VAULT_TASKS_START_HERE.md`

## Plan

Scope: GASLab `labs/gaslab/tests/` tree only (25 Python files: 21 test modules, 3 `__init__.py`, 1 `conftest.py`). No gaslab/ package, no wiki, no docs, no graphify.

Applied `4dlab-code-prep` per the skill workflow:
1. Probe — reused CODEPREP probe results (same graphify build 0.8.x, 7e2333a): E=NO (dropped), R=YES (kept), D=YES (kept)
2. Audit — machine-checkable rules I/A/T/C/S + R (R/D kept per probe)
3. Report — zero violations across all rules

## VERIFICATION GATE

### Audit findings (before/after)

| Rule | Count | Finding |
|---|---:|---|
| I (star imports) | 0 | No `import *` or `from x import *` in tests/ |
| A (`__all__`) | N/A | Test trees don't expose a public API surface; `__all__` is a package-level concern |
| T (type hints) | 0 | 3 non-test helpers + 1 fixture function all fully typed: `_dna(**overrides: object) -> GasLabDnaView`, `boundary_grid() -> Iterator[GasReading]`, `iter_edge_probes() -> Iterator[GasReading]`, `build_gaslab_descriptor() -> ModuleDescriptor`. 185 `test_*` functions are pytest-collected; typing `-> None` on each is noise (pytest injects fixtures, not a static call graph consumer) |
| C (dynamic dispatch) | 0 | No `getattr()`, `__import__`, or `importlib` calls |
| S (runtime symbols) | 0 | `type(chem).__name__` at `test_validators.py:266` is introspection for an assertion message, not runtime class generation |
| R (rationale comments) | 0 | Test function names + docstrings document the rule they guard (e.g. `test_triangle_valid_band` → `triangle_gate` → `SampleValidity.VALID`); no non-obvious gates in tests |
| D (formula docstrings) | N/A | No formula/validation methods in the test tree |

After counts — zero source edits needed, tree already code-prep clean.

### Inner loop

```
pytest -q   → 207 passed, 2 skipped, 4 deselected in 5.54s
ruff check tests/ → All checks passed!
grep -rn 'import \*' tests/ → 0 matches
pyright tests/ → 5 harness import errors (expected: runtime path via conftest.py, same as AUDIT_2026-06-10), 0 warnings
```

### Spot-confirm: test → rule/field mapping (success criterion 3)

| Test module | Guards |
|---|---|
| `test_validity_gates.py` | `triangle_gate`, `dilution_gate`, `sample_validity` → `SampleValidity` enum |
| `test_rule_engine.py` | `classify`, `_coc_adjust_normal_bounds`, `_matching_fault_candidates` → `ChemicalSignature` values |
| `test_contracts.py` | `ChemicalSignature` (34 values), `LambdaBand`, `GasReading`, `EngineStateBucket`, `GasBehavior`, `CatalystStatus` |
| `test_brettschneider.py` | `lambda_chem` → Brettschneider formula |
| `test_resolution.py` | `find_overlaps`, `apply_differentiators`, `is_resolved` → overlap resolution rules |
| `test_family_map.py` | `CANONICAL_FAMILIES`, `SIGNATURE_TO_FAMILY` → all 34 `ChemicalSignature` values |
| `test_ontology.py` | `load_ontology`, 34 fault entries, validity gates, collision/masking rules |
| `test_validators.py` | `find_uncovered_overlaps`, `parse_vocabulary_thresholds` → audit/validator coverage |

Every test module maps to named GASLab schema/rules — these become `VERIFIES` edges in `graph/v2_tests/`.

### Fold decision

Task spec §7.2: "This task may fold into T-GAS-CODEPREP if the test prep turns out light." CODEPREP needed zero edits (gaslab/ already clean); TESTPREP likewise needs zero edits. Marked `void — folded into T-GAS-CODEPREP` per the task spec.

## CODE REVIEW

PASS. Zero source edits were required:

- **Rule I:** no star imports.
- **Rule T:** all non-test helper functions are fully typed. 185 pytest test functions are collected by name; `-> None` annotations would add no graphify edges (pytest injection is dynamic, not a static call graph).
- **Rule C:** no hidden dispatch.
- **Rule S:** no runtime symbol generation.
- **Harness imports:** the 5 pyright `reportMissingImports` on `harness.*` are expected — `conftest.py` adds the harness root to `sys.path` at collection time. Same pattern documented in AUDIT_2026-06-10. Not a legibility issue.
- **Consumer mapping:** every test module guards named schema/rules (see spot-confirm table). These are ready to become `VERIFIES` edges when T-GAS-GRAPH-AST builds `graph/v2_tests/`.

No behavior logic changed, no schema fields added/removed, no graphify run on canonical source, no graph/* dirs touched.
