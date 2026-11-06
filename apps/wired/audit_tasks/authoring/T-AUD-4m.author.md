# T-AUD-4m — authoring sidecar (Windows Cowork, 2026-11-06)

Rehearsal: `C:/4DApp/recheck/T-AUD-4m/` (`apply_fix.py`, `rehearsal.patch`, `tests/`). T-AUD-4e is split into 4m-4q
(ledger); this is the first slice because it fabricates a measurement the user never entered.

### Verified context ###
1. **F-C5-11 holds** on the base: the payload gets `{1: 40, 2: 0, 3: 0, 4: 0}` for Rough Idle with the untouched
   slider (P1). The audit probe `test_f11_` no longer runs (KeyError `raw_payload`). Observed.
2. **No production reader** of the counts (P2): v1 router only. Observed.
3. **Rehearsal** (`rehearsal.patch`, restored): new file base `2 failed, 1 passed`, fix `3 passed`; ui 38 → 41; wired
   85; mutant (block back) fails `test_rough_idle_sends_no_misfire_counts`; ruff clean. Observed.

### Rulings and the tradeoff that lost ###
- **Remove the fabrication and the slider**, not a "Not known" default. Lost: a technician's observed misfiring
  cylinder; it has no truthful encoding in `per_cylinder_misfire_counts` (a count, not an observation) and no
  production reader. A cylinder observation, if wanted, needs its own field with a named consumer (a new row).
- Plan NONE, difficulty 2 (`--model claude-sonnet-5-5 --effort medium`): deletions only, quoted and rehearsed. Code
  row, so a second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `rehearsal.patch` + the test file: `3 passed`; ui `41 passed` (base 38, new file base `2 failed, 1 passed`) |
| step 2 | SIMULATED | wired `85 passed` (= base) |
| step 3 | SIMULATED | after the patch, no `symptom_misfire_cylinder` or `misfire_cyl` in the two files |
| step 4 | SIMULATED | ruff `All checks passed!`; status clean after restore |

### Exclusivity ###
No other implementer runs. T-AUD-4n follows.

### Progress hook ###
T-AUD-4m: Rough Idle no longer writes fabricated misfire counts into the OBD payload; the slider is removed.

### Cold read ###
own pass 2026-11-06: P1-P4 measured · literals found once (`# Symptom Misfire cylinder counts (slider to
single-cylinder dict)`, `misfire_cyl = None`, `# Rough Idle gets misfire slider`, `"symptom_misfire_cylinder":
misfire_cyl,`, `"symptom_misfire_cylinder": FieldHelp(`) · counts: ui 38 + 3 = 41 · traceability: criteria 1-4 → steps
1-4 · 1 finding patched (step 3 printed `path:0`, which check 14 reads as a citation; now one count). cold read
2026-11-06: not triggered (the 1c hits are a measured fact in P2 and the literal `None`).

### Correction history ###
(none)
