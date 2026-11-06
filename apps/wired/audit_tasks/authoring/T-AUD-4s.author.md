# T-AUD-4s — authoring sidecar (Windows Cowork, 2026-11-06)

Survey: `C:/4DApp/recheck/scratch/survey_T-AUD-4p.md` § 4-5, `C:/4DApp/recheck/T-AUD-4s/bounds.py`. Rehearsal:
`C:/4DApp/recheck/T-AUD-4s/` (`apply_fix.py`, `composition.fix.py`, `rehearsal.patch`, `tests/`, `cw/corpus_fix.json`).

### Verified context ###
1. **F-C4-8 holds:** 31 numeric raw channels copied with bare `float()`/`int()` (P1); audit f7 probe `3 failed`. Observed.
2. **The UI form bounds every channel** (`ui_payload.py` constants; `mode06_min_margin_pct` an `app.py` literal), so a
   form user cannot send a bad value; a JSON caller can. Observed.
3. **Corpus is inside the ranges** (P2: 0 of all present values outside). Observed.
4. **Rehearsal** (restored): new files base `9 failed, 3 passed` / `3 failed`, fix `12 passed` / `3 passed`; wired
   89 → 101; ui 49 → 52; comlab 525/4/2; registry 5F/502P (= base); corpus 0/314 differ; f7 probe `3 passed`; M1
   `2 failed, 10 passed`; ruff clean. Observed.

### Rulings and the tradeoff that lost ###
- **Abort with `OBD_INPUT_OUT_OF_RANGE`** (the `_incomplete_input` pattern). Lost: dropping a bad channel to `None` and
  running on (keeps the session alive, but hides a wrong reading from the technician and changes the evidence silently).
- **The UI form's ranges are the table.** Lost: J1979 scaling ranges (wider: trims -100..99.2, DTC count 0..127) or
  the mirror's `Field` bounds (absent for most). The form ranges are the product's stated ranges, and one table that a
  test pins to the form keeps them from drifting.
- **Plan NONE, difficulty 3** (`--model claude-sonnet-5-5 --effort medium`). Lost: the handoff's "REQUIRED" marker, set
  while the design was open; every ruling is now made and rehearsed with a mutant. Code row, so a second review.
- **v1 `o2_downstream` moves to T-AUD-4t** (v1-only after T-AUD-4p's labelling).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `12 passed`; `3 passed`; wired `101 passed`; ui `52 passed` |
| step 2 | SIMULATED | comlab `525 passed, 4 skipped, 2 errors` |
| step 3 | SIMULATED | `corpus 314`; `differ 0`; f7 `3 passed, 9 deselected` |
| step 4 | SIMULATED | ruff `All checks passed!`; status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-4s: the 31 raw OBD channels are range-checked with the form's ranges; a bad value aborts with a named verdict.

### Cold read ###
own pass 2026-11-06: P1-P5 measured · `apply_fix.py` literals each matched once, the regex 31 times · counts: wired
89 + 12 = 101, ui 49 + 3 = 52 · traceability: criteria 1-4 → steps 1-4 · 1c hits (R1 "each", R3 "each", "every") name
the P1 set, defined once in `apply_fix.py` · no finding.
cold read 2026-11-06 FOCUSED reader; trigger 1c grep hit (R1, R3); 0 findings, 0 patched — tokens ABSENT (not in the hand-back), 3 calls.

### Correction history ###
(none)
