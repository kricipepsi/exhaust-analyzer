# T-FX-DTCHEX-1 — Progress Note

**Date:** 2026-06-11 · **Coder:** Claude

## Plan

One character class change (`[0-9]{3}` → `[0-9A-F]{3}`) in `vocabulary.py:34` to
bring COMLab's DTC validation pattern in line with its own wiki §2.3 and DTCLab's
already-correct hex form. Four files: the constant, its drift-guard unit test, a
mock docstring, and one new positive test (P244A) in `test_error_codes.py`. No
wiki edits, no DTCLab changes, no corpus changes.

---

## VERIFICATION GATE

```
VERIFICATION GATE — T-FX-DTCHEX-1
==================================
Syntax:         PASS (py_compile clean on all 4 files)
Imports:        PASS (no new imports; all pre-existing)
Type check:     PASS (pyright — 0 new errors; all errors are pre-existing in untouched files)
Lint:           PASS (ruff — all checks passed)
pytest Layer-1: PASS (314 passed, 6 skipped, 1 pre-existing failure [O2FailureMode.SLUGGISH wiki drift])
DTC-specific:   PASS (6/6: drift guard + 3 negative + 1 decimal-positive + 1 hex-positive)
Diff review:    4 files changed, no scope creep, no new schema field, citation comment preserved

Success criteria:
  1. DTC_REGEX == r"^[BCPU][0-3][0-9A-F]{3}$" — PASS
  2. P244A passes validate_payload — PASS (test_hex_tail_dtc_accepted)
  3. BAD_CODE / X9999 / P0xxx still reject — PASS (3 existing negative tests)
  4. Drift guard asserts hex literal — PASS (test_dtc_regex_matches_wiki)
  5. Inner loop green — PASS (ruff clean, pyright 0 new errors, pytest green)

Pythonskill checklist items applied:
  1. Type hints — n/a (no new functions)
  2. Docstrings — applied (new test has docstring)
  3. No mutable defaults — n/a
  4. No bare except — n/a
  5. No magic numbers — n/a
  6. f-strings — n/a
  7. Pathlib — n/a
  8. Context managers — n/a
  9. is None not == None — n/a
  10. Sorted imports — n/a (no new imports)

Status: DONE
```

---

## CODE REVIEW

- **Only the four files in §5 changed:** `vocabulary.py:34`, `test_vocabulary.py:112`,
  `mock_dtc_lab.py:4`, `test_error_codes.py` (new test_hex_tail_dtc_accepted). ✓
- **No new schema field.** This is a pure regex constant fix. ✓
- **Three negative tests still red:** `BAD_CODE`, `X9999`, `P0xxx` all still raise
  `ERR-CONTRACT-001`. ✓
- **Citation comment survived:** `# ISO 15031-6 §5.2 (≡ SAE J2012) / DTC_VOCABULARY §2.3`
  preserved at `vocabulary.py:34`. ✓
- **No wiki edit** — wiki was already correct (hex form). ✓
- **No DTCLab touch** — DTCLab regex was already hex-correct. ✓
- **No corpus changes** — no hex DTCs added to the master. ✓
- **Pre-existing pyright errors untouched** — all errors are in files this task did not
  modify (`fault_atlas_router.py`, `descriptor.py`, `test_fault_atlas_router.py`, etc.). ✓
- **One pre-existing pytest failure** (`test_wiki_drift_guard[O2FailureMode]` —
  `SLUGGISH` not in OBD wiki) — unrelated to DTC_REGEX, not introduced by this diff. ✓

Status: CLEAN
