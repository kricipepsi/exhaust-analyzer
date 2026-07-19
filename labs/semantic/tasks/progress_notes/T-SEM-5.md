# T-SEM-5 — Progress Note

**Task:** Reconcile OBD_VOCABULARY (§12.4, §5.2) to shipped code + re-sync all copies
**Date:** 2026-06-10
**Coder:** Claude Code

## Plan

1. Read code ground truth: `obdlab/obdlab/schemas/vocabulary.py` O2FailureMode (4 members) + FuelSystemStatus (4 members)
2. Edit canonical `semantic/vocabul/OBD_VOCABULARY.md`:
   - Status v1.1 → v1.2
   - Changelog: add v1.2 entry
   - §12.4: replace 7-value O2FailureMode with 4-value (matching code)
   - §5.2: add FuelSystemStatus enum
3. Apply identical edits to `obdlab/docs/OBD_VOCABULARY.md` and `comlab/docs/wiki/OBD_VOCABULARY.md`
4. Fix `comlab/docs/wiki/SEMANTIC_CONTRACT.md` §4.4 o2_failure_mode comment 7→4

## VERIFICATION GATE

### 1. md-only diff
PASS — all 4 touched files are `.md`. Pre-existing uncommitted files in `obdlab/research/sources/` are not from this task.

### 2. §12.4 roster + §5.2 FuelSystemStatus
PASS — all 3 copies:
- WIDEBAND_OFFSET_CANDIDATE present
- SLUGGISH, DEAD, WRONG_CENTERLINE, HEATER_FAULT enum members pruned (case-sensitive check)
- FuelSystemStatus class present

### 3. Single-source invariant
PASS — all 3 OBD_VOCABULARY.md copies MD5-identical: `B14AFE095EC0C2765B6FAEC2D23CA851`

### 4. SEMANTIC_CONTRACT §4.4 synced
PASS — "4 values: NO_FAULT, STUCK_LEAN, STUCK_RICH, WIDEBAND_OFFSET_CANDIDATE"

### 5. T-SEM-4 conformance gate
PASS — 3 passed in 0.23s (`test_vocabulary_sae_iso_conformance.py`)

## CODE REVIEW

4 files changed, 13 total edits:

- `semantic/vocabul/OBD_VOCABULARY.md` [canonical] — Status v1.2, changelog v1.2, §12.4 7→4, §5.2 +FuelSystemStatus
- `obdlab/docs/OBD_VOCABULARY.md` — identical edits, byte-identical to canonical
- `comlab/docs/wiki/OBD_VOCABULARY.md` — identical edits, byte-identical to canonical
- `comlab/docs/wiki/SEMANTIC_CONTRACT.md` — §4.4 comment 7→4 values

All 5 success criteria met. No `.py` files touched. Surgical: only §12.4 roster, §5.2 addition, changelog, status, and §4.4 comment changed.

## Out-of-scope

- `TestSuite/COM/SEMANTIC_CONTRACT.md` (frozen harness fixture) — not touched (owner decision needed, Unplanned #4)
- FU-OBD-DOC-3 (`vocabulary.py` docstring "7 StrEnums"→8) — separate coder follow-up
