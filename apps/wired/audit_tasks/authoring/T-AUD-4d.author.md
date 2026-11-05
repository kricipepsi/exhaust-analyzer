# T-AUD-4d — authoring sidecar (Windows Cowork, 2026-11-05)

### Verified context ###
1. **F-C3-2 holds** at the 4h tip: `_run_dtclab` builds `DataFusionSanitizer()` with no view. Observed (read).
2. **HIGH probe** (`probe_high.py`): the audit VIN with P0401 drops `EGR_HISTORY` with the view; verdict LC-002 both.
   Observed.
3. **Corpus** (`rehearse.py`, `corpus_check.py`): no case decodes HIGH (172 PARTIAL built, 27 without year, 8 NONE);
   the digest is identical on base and the rehearsed fix. Observed.
4. **Pins** (`apply_fix.py`, restored): P3. Observed.

### Rulings and the tradeoff that lost ###
- The composition builds the view (as for OBDLab and GASLab). Lost: COMLab's `project(..., target='dtc')`, which
  DTCLab rejects (F-D2-10) and which reads a flat shape (F-D2-11); both go to T-AUD-4e's contract census.
- A required field unknown → no view (≡ NONE, today's behaviour). Lost: a placeholder `model_year` (0), which would
  invent data for a field DTCLab does not read.
- `model` stays `""`: VINLab has no model field and DTCLab reads none.
- Plan NONE, difficulty 3. Code row, so a second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | rehearsed fix: new file `13 passed`, wired `62 passed` (base 49); mutants 2/1/1 failed |
| step 2 | RAN | dtclab 590, ui 30, comlab `526/4/2 errors` (base and fix) |
| step 3 | RAN | `git status --porcelain` empty after the suites |
| step 4 | RAN | `corpus_check.py` digest `f5414b25634aae41` on base and fix |
| step 5 | RAN | ruff `All checks passed!` on the rehearsed fix |

### Exclusivity ###
No other implementer runs. T-AUD-4e follows.

### Progress hook ###
T-AUD-4d: DTCLab gets its DNA view; HIGH EGR-less cars lose the false EGR_HISTORY tag; de_cat reaches DTCLab.

### Cold read ###
own pass 2026-11-05: P1-P4 measured · literals found once (`DataFusionSanitizer().sanitize(`, `def _run_dtclab`,
`dtc_output = _run_dtclab(`, `from dtclab import DataFusionSanitizer`); new names absent at base · counts: wired
49 + 13 = 62, mutants 2 + 1 + 1 · traceability: criteria 1-4 → steps 1-5 · no finding. cold read: skipped (the second
review covers the code).

### Correction history ###
(none)
