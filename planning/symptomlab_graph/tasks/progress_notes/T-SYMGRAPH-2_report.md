# --=={ 4dlab-code-ingest: labs/symptomlab/symptomlab / probe & audit }==--

## Probe Results
1. Enum member `STABILIZED_IDLE` present as its own node? → **No** (Governs Rule E)
2. A `file_type: "rationale"` node for the `# WHY:` comment? → **Yes** (Governs Rule R)
3. A `rationale` node carrying the docstring/formula? → **Yes** (Governs Rule D)

**Scope Status for E/R/D:**
- **Rule E (Explicit Enums)**: Out of scope (probed No).
- **Rule R (Rationale Tags)**: In scope (probed Yes).
- **Rule D (Formula Docstrings)**: In scope (probed Yes).

---

## Audit Table

| File & Line | Rule | Found | Fix |
|---|---|---|---|
| `models.py:100` | R (Rationale Tags) | `# Pre-load_state...` | Prefixed comment block with `WHY:` tag to mark schema migration reasoning. |
| `validator.py:16` | D (Formula Docstrings) | No docstring on class `SymptomValidator` | Added class-level docstring documenting the validator purpose. |
| `validator.py:17` | D (Formula Docstrings) | No docstring on `__init__` | Added function-level docstring with parameters and raises documentation. |
| `validator.py:25` | R (Rationale Tags) | `# 7 tier_1 × 3...` | Prefixed count-check comment with `WHY:` tag to clarify 21 combinations constraint. |
| `validator.py:31` | D (Formula Docstrings) | No docstring on `validate` | Added detailed parameter-naming docstring explaining validation rules. |
| `validator.py:40` | R (Rationale Tags) | No comment/tag for validation rejection | Added `# WHY:` comment documenting rejection of unauthorized symptom pairs. |
| `__init__.py:18` | D (Formula Docstrings) | Incomplete parameter detail in `resolve` | Updated docstring to list and explain all arguments. |

---

## Violation Counts & Summary
- **Rule I (Explicit Imports)**: 0 violations
- **Rule A (Public Surface)**: 0 violations
- **Rule T (Type Hints)**: 0 violations
- **Rule C (Static Call Sites)**: 0 violations
- **Rule S (Statically Named Symbols)**: 0 violations
- **Rule E (Explicit Enums)**: Out of scope
- **Rule R (Rationale Tags)**: 3 violations (Fixed)
- **Rule D (Formula Docstrings)**: 4 violations (Fixed)

**Total violations found**: 7
**Total violations resolved**: 7
**Remaining violations**: 0
