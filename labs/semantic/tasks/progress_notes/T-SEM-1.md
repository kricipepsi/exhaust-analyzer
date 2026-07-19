# T-SEM-1 — progress note

## Plan
We will update `comlab/comlab/schemas/vocabulary.py`, `labs/semantic/vocabul/OBD_VOCABULARY.md`, and `labs/semantic/vocabul/DTC_VOCABULARY.md` to establish dual-anchor ISO-primary standards citations. The existing `comlab` pytest suite verifies the edits are non-semantic (zero value or enum churn), and the signal/noise consumer is the upcoming `T-SEM-4` conformance gate which parses the standards citations.

## VERIFICATION GATE
- **Comment-only diff validation:** Ran `git diff` on `vocabulary.py` and manually checked that only comment lines and docstrings were modified. No class or variable names, member names, or string literal values were altered.
- **Ruff check:** Ran `ruff check comlab/` and verified that all checks passed.
- **Pytest execution:** Ran `pytest -x -q` and confirmed that all 332 tests passed (6 skipped), matching the baseline.

## CODE REVIEW
- **comlab/comlab/schemas/vocabulary.py:** Added ISO 15031-6 (≡ SAE J2012) citations to all 18 `DTCRoutingTag` members while keeping the original P-code comments. Updated `DTC_REGEX`, `DTCSeverityClass`, and `DTCState` docstrings/comments to cite ISO-primary standards.
- **labs/semantic/vocabul/OBD_VOCABULARY.md:** Reordered the standards anchored table in §1 to be ISO-primary. Added the `ISO 15031-5 PID` column to the minimalist PID table in §2 and the extended PID table in §16.1.
- **labs/semantic/vocabul/DTC_VOCABULARY.md:** Reordered the standards anchored table in §1 to be ISO-primary. Cited ISO 15031-6 in §2 header and §5 `DTCSeverityClass` description.
