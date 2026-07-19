# --=={ 4dlab-code-ingest: labs/symptomlab/tests / probe & audit }==--

## Probe Results
1. Enum member `STABILIZED_IDLE` present as its own node? → **No** (Rule E out of scope)
2. A `file_type: "rationale"` node for the `# WHY:` comment? → **Yes** (Rule R in scope)
3. A `rationale` node carrying the docstring/formula? → **Yes** (Rule D in scope)

**Scope Status for E/R/D:**
- **Rule E (Explicit Enums)**: Out of scope (probed No).
- **Rule R (Rationale Tags)**: In scope (probed Yes).
- **Rule D (Formula Docstrings)**: In scope (probed Yes).

---

## Audit Table

| File & Line | Rule | Found | Fix |
|---|---|---|---|
| `test_models.py:19` | D (Formula Docstrings) | No docstring on `test_symptom_dna_to_json_keys` | Added docstring documenting serialized contract key checks. |
| `test_models.py:37` | D (Formula Docstrings) | No docstring on `test_symptom_dna_preserves_reworked_visible_exhaust_strings` | Added docstring documenting exhaust string checks. |
| `test_models.py:46` | D (Formula Docstrings) | No docstring on `test_symptom_dna_is_frozen` | Added docstring documenting frozen property checks. |
| `test_models.py:59` | D (Formula Docstrings) | No docstring on `test_enum_values` | Added docstring documenting enum mapping checks. |
| `test_symptomdna_from_json.py:13` | T (Type Hints) | Opaque dict type return for helper `_make_full_payload` | Added return type annotation `dict[str, Any]`. |
| `test_symptomdna_from_json.py:28` | D/T (Docstrings/Type Hints) | No docstring or return type on `test_round_trip_full` | Added `-> None` annotation and docstring. |
| `test_symptomdna_from_json.py:39` | T (Type Hints) | No return type on `test_round_trip_minimal` | Added `-> None` annotation. |
| `test_symptomdna_from_json.py:57` | D/T (Docstrings/Type Hints) | No docstring or return type on `test_optional_free_text_notes_when_absent` | Added `-> None` annotation and docstring. |
| `test_symptomdna_from_json.py:64` | D/T (Docstrings/Type Hints) | No docstring or return type on `test_missing_tier_1_raises_keyerror` | Added `-> None` annotation and docstring. |
| `test_symptomdna_from_json.py:68` | D/T (Docstrings/Type Hints) | No docstring or return type on `test_missing_tier_2_raises_validation_error` | Added `-> None` annotation and docstring. |
| `test_symptomdna_from_json.py:75` | D/T (Docstrings/Type Hints) | No docstring or return type on `test_missing_environmental_conditions_raises_validation_error` | Added `-> None` annotation and docstring. |
| `test_symptomdna_from_json.py:80` | D/T (Docstrings/Type Hints) | No docstring or return type on `test_missing_occurs_during_raises_validation_error` | Added `-> None` annotation and docstring. |
| `test_symptomdna_from_json.py:85` | D/T (Docstrings/Type Hints) | No docstring or return type on `test_missing_engine_state_raises_validation_error` | Added `-> None` annotation and docstring. |
| `test_symptomdna_from_json.py:90` | D/T (Docstrings/Type Hints) | No return type on `test_missing_load_state_defaults_to_idle` | Added `-> None` annotation. Prefixed comment with `WHY:` tag. |
| `test_symptomdna_from_json.py:98` | D/T (Docstrings/Type Hints) | No docstring or return type on `test_invalid_occurs_during_raises_validation_error` | Added `-> None` annotation and docstring. |
| `test_symptomdna_from_json.py:105` | D/T (Docstrings/Type Hints) | No docstring or return type on `test_invalid_engine_state_raises_validation_error` | Added `-> None` annotation and docstring. |
| `test_symptomdna_from_json.py:110` | D/T (Docstrings/Type Hints) | No docstring or return type on `test_invalid_load_state_raises_validation_error` | Added `-> None` annotation and docstring. |
| `test_symptomdna_from_json.py:119` | T (Type Hints) | No return type on `test_unknown_pair_accepted` | Added `-> None` annotation. |
| `test_validator.py:57` | D (Formula Docstrings) | No docstring on `test_bad_17_pair_catalog_rejected` | Added docstring. |
| `test_validator.py:61` | D/T (Docstrings/Type Hints) | Opaque parameter `allowed_pairs` and missing docstring | Added type annotation and docstring. |
| `test_validator.py:64` | D/T (Docstrings/Type Hints) | Opaque parameters `validator` and `allowed_pairs`, missing docstring | Added type annotations and docstring. |
| `test_validator.py:76` | D/T (Docstrings/Type Hints) | Opaque parameter `validator` and missing docstring | Added type annotation and docstring. |
| `test_validator.py:86` | D/T (Docstrings/Type Hints) | Opaque parameter `validator` and missing docstring | Added type annotation and docstring. |
| `test_validator.py:95` | D/T (Docstrings/Type Hints) | Opaque parameter `validator` and missing docstring | Added type annotation and docstring. |
| `test_validator.py:105` | D/T (Docstrings/Type Hints) | Opaque parameter `validator` and missing docstring | Added type annotation and docstring. |
| `test_validator.py:112` | D/T (Docstrings/Type Hints) | Opaque parameter `validator` and missing docstring | Added type annotation and docstring. |
| `test_validator.py:119` | D/T (Docstrings/Type Hints) | Opaque parameter `validator` and missing docstring | Added type annotation and docstring. |
| `test_validator.py:127` | D/T (Docstrings/Type Hints) | Opaque parameter `validator`, `tier_1`, `tier_2` and missing docstring | Added type annotations and docstring. |
| `test_validator.py:137` | D/T (Docstrings/Type Hints) | Opaque parameter `validator`, `value` and missing docstring | Added type annotations and docstring. |
| `test_validator.py:145` | D/T (Docstrings/Type Hints) | Opaque parameter `validator`, `value` and missing docstring | Added type annotations and docstring. |
| `test_validator.py:156` | D/T (Docstrings/Type Hints) | Opaque parameter `validator`, `value` and missing docstring | Added type annotations and docstring. |
| `test_validator.py:165` | D/T (Docstrings/Type Hints) | Opaque parameter `validator` and missing docstring | Added type annotation and docstring. |
| `test_validator.py:172` | D/T (Docstrings/Type Hints) | Opaque parameter `validator` and missing docstring | Added type annotation and docstring. |
| `test_validator.py:180` | D/T (Docstrings/Type Hints) | Opaque parameter `validator` and missing docstring | Added type annotation and docstring. |
| `test_validator.py:190` | D/T (Docstrings/Type Hints) | Opaque parameter `validator` and missing docstring | Added type annotation and docstring. |
| `test_validator.py:203` | D/T (Docstrings/Type Hints) | Opaque parameter `validator` and missing docstring | Added type annotation and docstring. |
| `test_validator.py:213` | D (Formula Docstrings) | No docstring on `test_symptom_dna_frozen` | Added docstring. |
| `test_validator.py:226` | D (Formula Docstrings) | No docstring on `test_symptom_dna_hashable` | Added docstring. |
| `test_validator.py:239` | D (Formula Docstrings) | No docstring on `test_environmental_conditions_frozen` | Added docstring. |
| `test_validator.py:248` | D (Formula Docstrings) | No docstring on `test_occurs_during_str_equality` | Added docstring. |

---

## Violation Counts & Summary
- **Rule I (Explicit Imports)**: 0 violations
- **Rule A (Public Surface)**: 0 violations
- **Rule T (Type Hints)**: 25 violations (Fixed)
- **Rule C (Static Call Sites)**: 0 violations
- **Rule S (Statically Named Symbols)**: 0 violations
- **Rule E (Explicit Enums)**: Out of scope
- **Rule R (Rationale Tags)**: 1 violation (Fixed)
- **Rule D (Formula Docstrings)**: 36 violations (Fixed)

**Total violations found**: 62
**Total violations resolved**: 62
**Remaining violations**: 0
