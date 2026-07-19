# T-DTC-COMMENT-FIX — Progress Note

**Date:** 2026-06-11 · **Lane:** coder

## Plan

Two exact docstring edits:
1. `dtclab/schemas/vocabulary.py` line 19: `17-value canonical form` → `18-value canonical form`
2. `dtclab/family_map.py` line 3: `19-value surface` → `18-value surface`

No code, no enum members, no behaviour change.

## VERIFICATION GATE

1. **Both docstrings = 18-value:** vocabulary.py line 19 `18-value canonical form`, family_map.py line 3 `18-value surface`
2. **grep clean:** `grep -rn '17-value\|19-value' dtclab/` returns no matches for the routing enum
3. **Inner loop green:**
   - `ruff check dtclab tests` — All checks passed
   - `pyright dtclab tests` — 0 new errors (4 pre-existing in tests/, none in dtclab/ source)
   - `pytest -x -q` — 576 passed in 2.35s
4. **Enum untouched:** `git diff --stat` shows 2 files, 2 insertions, 2 deletions — comment lines only

## CODE REVIEW

- Diff is comment/docstring text only — no behaviour change, no logic, no test expectation changes
- Both counts now match ground truth (`DTC_VOCABULARY.md §4` = 18)
- No stale count references remain in the dtclab/ code tree
- Ready for CODEPREP (no docstring-count flag)
