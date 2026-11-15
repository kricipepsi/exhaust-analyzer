# T-AUD-22g — authoring sidecar (Windows Cowork, 2026-11-15)

Input: ledger row T-AUD-22; T-AUD-22f accepted (671b347, pushed): GASLab and COMLab covered. First `rest` slice; fourth
app row on the Hydrogen lane (difficulty 3 -> gemini-4-hydrogen-high). Cowork tool output in the spec commit:
`candidates_rest.csv` (first `extract_code_candidates.py --group rest` run) and `claims_rest.csv` (header line only).

### Verified context ###
1. **`extract_code_candidates.py --group rest` prints `files 31 candidates 789 auto_non_domain 249 to_classify 540`.**
   Observed 2026-11-15 on 671b347.
2. **Non-auto by area: apps/ui 280 (`_sample_app_reference.py` 129, `ui_payload.py` 93, `app.py` 58), labs/obdlab 125,
   labs/dtclab 76, apps/wired/wired 41, apps/wired/v7 17, labs/symptomlab 1.** Observed (Counter over the CSV).
3. **`check_code_claims.py --group rest --files 'labs/*'` prints `CLAIMS FAIL 202 error(s)`; the whole group
   `CLAIMS FAIL 540 error(s)`, so after this row `338` (P3).** Observed.
4. **The 20 lab files and their counts (P4 lists the five largest).** Observed.

### Rulings and the tradeoff that lost ###
- **Labs first (202), apps later (338).** The labs hold the domain constants; the apps hold UI and a sample reference
  file whose scope needs a ruling of its own. Lost: one 540-row slice past the 90-minute stop rule's comfort.
- **Step 2 pins the apps remainder** so the row cannot spill into the next slice. Lost: no seed check (no known defect
  seed in these files was measured).
- **Lane run: no commit by the implementer**; promote commits on fix/T-AUD-22g.
- Difficulty 3. Survey = facts 1-4. Plan NONE. Docs row: no second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | DEFERRED | pre-state `CLAIMS FAIL 202 error(s)` (P2) |
| step 2 | DEFERRED | pre-state `CLAIMS FAIL 540 error(s)`; post-state `CLAIMS FAIL 338 error(s)` needs the rows |
| step 3 | DEFERRED | `0` removed lines; the CSV, note and RESULT in status |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-22g: OBDLab, DTCLab and SymptomLab literals (202 lines) classified; CLAIMS OK group=rest scope=labs/*.

### Cold read ###
cold read 2026-11-15 FOCUSED reader: 1 IMPLICIT finding (R6 allowed CK ids in same_as; the checker accepts only W and same-group ids) — RULED: fixed in R6 before dispatch (C:/4DApp/recheck/scratch/T-AUD-22g_coldread.md) — 4 calls

### Correction history ###
(none)
