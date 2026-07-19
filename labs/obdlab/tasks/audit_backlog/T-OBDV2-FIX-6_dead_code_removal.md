# T-OBDV2-FIX-6 — Remove dead control flow in checker + ranking (🟡 opacity)

**Status:** `done` — coder-runnable · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Origin:** OBDLab skills-audit 2026-06-08 — findings **UB-4, UB-5** (`audit/AUDIT_02_uncle-bob.md`).
**Blocked by:** —
**Consumer (signal/noise):** n/a — behaviour-preserving dead-code removal. No schema change.

## Why this exists

Two pieces of structure imply behaviour that does not exist:

1. **No-op `try/except` (UB-4).** `SemanticConsistencyChecker.evaluate` wraps each gate in
   `try: gate(); append() ; except SemanticConsistencyError: raise`
   (`core/semantic_consistency_checker.py` L52-74). The `except … : raise` blocks catch and
   immediately re-raise — they do nothing. Gate 4's `except (ValueError, SemanticConsistencyError): raise`
   is the same. A reader must verify each block is inert.
2. **Discarded tier calls (UB-5).** `ranking.py` calls `_evidence_tier(True, count)` at L210
   and L222 and **throws away the return value**; the tier actually used by `_clamp_confidence`
   comes from `_candidate_evidence_tier` (L159). Two competing tier functions, one invoked for
   no effect.

## Scope (pinned)

- Delete the `try/except` scaffolding in `evaluate`; call gates directly and append on success.
- Remove the discarded `_evidence_tier(...)` calls; then delete `_evidence_tier` if unused, or
  make `_candidate_evidence_tier` delegate to it so there is **one** tier definition.

## Success criteria

- `evaluate` has no `try/except`; `ranking` has a single tier function; behaviour identical
  (same gates raise the same errors, same candidate scores/confidences).
- `ruff --select SIM,TRY` clean on the two files; regression + pid_logset gate green;
  inner loop clean (Windows `.venv-wired`).

## Files to touch

- `core/semantic_consistency_checker.py` · `obdlab/ranking.py` · existing tests for both (no new tests).

## Out of scope

No behaviour change. The `ranking.py` consumer question (AR-1) is **T-OBDV2-ARCH-1** — do not
delete the module here. Test-infra build deferred.

## Verification

```bash
cd <repo>/labs/obdlab
ruff check obdlab/ && pyright obdlab/
grep -n "except SemanticConsistencyError:\|_evidence_tier(" obdlab/obdlab/core/semantic_consistency_checker.py obdlab/obdlab/ranking.py
pytest -x -q
```

## Progress hook

`tasks/progress_notes/T-OBDV2-FIX-6.md`: `## Plan` → `VERIFICATION GATE` → `CODE REVIEW`
(identical-behaviour note). PROGRESS.md row → `done`.
