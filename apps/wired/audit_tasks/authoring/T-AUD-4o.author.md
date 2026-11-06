# T-AUD-4o — authoring sidecar (Windows Cowork, 2026-11-06)

Rehearsal: `C:/4DApp/recheck/T-AUD-4o/` (`apply_fix.py`, `rehearsal.patch`, `tests/`), repro
`C:/4DApp/recheck/scratch/f9_wideband.py`.

### Verified context ###
1. **The audit probe is stale** (passes on the base: its VIN now decodes PARTIAL + NARROWBAND). Observed.
2. **F-C5-9 holds** for `era2_015` (P1, P2): the AFR field shows on a PARTIAL decode, and both choices abort
   `OBD_INPUT_INCOMPLETE`. Observed.
3. **Rehearsal** (restored): P2 fix lines; new file base `3 failed, 1 passed`, fix `4 passed`; ui 45 → 49; wired 85;
   M1 and M2 as P3; ruff clean. Observed.

### Rulings and the tradeoff that lost ###
- **PARTIAL → basic mode in the UI** (FieldMap §1.2 literal). Lost: using a PARTIAL decode's equipment facts in the
  form (they are often right, but the FieldMap rules them out and the labs' re-decode is the same PARTIAL DNA).
- **Basic mode pins only the O2 type** through the existing `overrides` path. Lost: sending the whole basic-mode DNA
  (banks, MAF/MAP, catalyst); only the O2 type aborts a run today, and a full basic-DNA contract is a wider change.
- Plan NONE, difficulty 3 (`--model claude-sonnet-5-5 --effort medium`): two quoted edits, rehearsed with mutants.
  Code row, so a second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `rehearsal.patch` + the test file: `4 passed`; ui `49 passed` (base 45) |
| step 2 | SIMULATED | wired `85 passed` |
| step 3 | SIMULATED | `f9_wideband.py`: volts field 0-1; both lines `EF-004 … mode=FULL_FUSION` |
| step 4 | SIMULATED | ruff `All checks passed!`; status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-4o: a PARTIAL decode is basic mode, and basic mode tells the labs the O2 type the form used.

### Cold read ###
own pass 2026-11-06: P1-P4 measured · literals found once (the `use_decoded_dna = st.checkbox(` line, `    if
overrides:` in `ui_payload.py`) · counts: ui 45 + 4 = 49 · traceability: criteria 1-4 → steps 1-4 · no finding.
cold read 2026-11-06 FOCUSED reader; trigger 1c grep hit ("only" in R1); 0 findings, 0 patched — 3 calls.

### Correction history ###
(none)
