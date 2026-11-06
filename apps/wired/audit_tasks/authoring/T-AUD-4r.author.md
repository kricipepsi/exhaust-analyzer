# T-AUD-4r — authoring sidecar (Windows Cowork, 2026-11-06)

Rehearsal: `C:/4DApp/recheck/T-AUD-4r/` (`apply_fix.py`, `rehearsal.patch`, `tests/`, `cw/corpus.json`).

### Verified context ###
1. **Readers** (P1): `grep -rn "free_text_notes" --include=*.py apps labs` → only SymptomLab's model and validator;
   `composition.py` calls `resolve_symptom(**{key: triage[key] for key in _TRIAGE_KEYS})`. `second_operating_point`
   has no producer in `apps/wired` or `apps/ui`; `fault_atlas_router.py` `enable_delta_v2: bool = False`. DTCLab
   `data_fusion_sanitizer.py` takes `MID → margin_pct` and `mode06_evaluator.py` is the margin tri-state classifier.
   GASLab `ranking.py` passes `block_test_passed` to `_definitive_match`; DLD line "coolant (87) … → COOLANT_LEAK_INTERNAL".
   Observed.
2. **The block-test tooltip was wrong:** "tailpipe exhaust backpressure test". Observed.
3. **Rehearsal** (restored): new file base `4 failed, 1 passed`, fix `5 passed`; ui 52 → 57; wired 101; corpus 0/314
   differ; ruff clean; `git apply --check` passes on the base. Observed.

### Rulings and the tradeoff that lost ###
- **Remove notes, the OBD high-idle panel and the result-state choice.** Lost: wiring each. Notes have no diagnostic
  reader (only an echo-audit pass-through would carry them); the high-idle panel needs a second-operating-point
  producer and the delta flags on (design work, verdict movement); the result state duplicates DTCLab's own margin
  classification and could contradict it.
- **Wire the block test.** GASLab already reads it; only the widget was missing. Lost: keeping it hard-coded `False`
  (hides a definitive coolant-leak path from the technician).
- `gas_engine_state` stays the constant: the low-idle panel's caption fixes the state.
- Plan NONE, difficulty 2 (`--model claude-sonnet-5-5 --effort medium`). Code row, so a second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `5 passed`; ui `57 passed` |
| step 2 | SIMULATED | wired `101 passed` |
| step 3 | SIMULATED | `corpus 314`; `differ 0` |
| step 4 | SIMULATED | ruff `All checks passed!`; status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-4r: every form input reaches a reader; notes, the OBD high-idle panel and the result-state choice go; the block
test is wired.

### Cold read ###
own pass 2026-11-06: P1-P4 measured · every `apply_fix.py` literal matched once (the script exits otherwise) · counts:
ui 52 + 5 = 57 · traceability: criteria 1-4 → steps 1-4 · no finding.
cold read 2026-11-06 FOCUSED reader; trigger 1c grep hit (criterion 4 "only"); 0 findings, 0 patched — 3 calls.

### Correction history ###
(none)
