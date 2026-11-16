# T-AUD-24o — authoring sidecar (Windows Cowork, 2026-11-16)

Input: T-AUD-23i verdicts and `reviews/RULING_T-AUD-24o.md`. Difficulty 2: no survey or cold read beyond the corpus
ruling; a code row, so it keeps its second review. Lane: Hydrogen medium.

### Verified context ###
1. **P1 edits:** `C:/4DApp/recheck/T-AUD-24o/apply.py` applies all 27 on d9b1ce0 (each old text found exactly once).
2. **Rehearsal on d9b1ce0:** comlab 614, registry 510/5, wired 1 failed (T-COMA-10) 237 passed; corpus 0 changed
   (`recheck/T-AUD-24o/rehearsal.json`). Step 4: `24o FAIL` on base, `24o OK` with R1-R3.
3. **Wired suite run** (MEMORY.md: rule-data rows run apps/wired); no wired test pins 600 rpm or 30 °C (grep).

### Rulings and the tradeoff that lost ###
- **400 rpm, not 450:** a margin under the regulator's idle floor. Lost: 450 exactly (an engine at the floor would sit
  on the boundary).
- **MW-005 moves too:** one split speed for the two rules. Lost: leaving MW-005 at 600 (a 400-600 gap where neither
  the no-start nor the running gate passes).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | 614 passed |
| step 2 | RAN | 510 passed, 5 skipped |
| step 3 | RAN | 1 failed (T-COMA-10), 237 passed |
| step 4 | RAN | 24o FAIL on base; 24o OK with R1-R3 |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-24o: no-start rpm < 400, MW-005 > 400, NS-002 ECT < 10.

### Cold read ###
NONE (difficulty 2, CLAUDE.md process by difficulty).

### Correction history ###
(none)
