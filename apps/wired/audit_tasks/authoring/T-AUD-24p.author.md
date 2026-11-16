# T-AUD-24p — authoring sidecar (Windows Cowork, 2026-11-16)

Input: a regression of the accepted T-AUD-24k, found while rehearsing T-AUD-24o (`REVIEW_T-AUD-24k.md` § Correction).
Difficulty 1: no survey or cold read. A code row (test), so it keeps its second review. Lane: Hydrogen medium.

### Verified context ###
1. **P1 lines** read on 9029d2f (`sed -n '27,28p;30p'`).
2. **Wired before:** `3 failed, 235 passed` on 9029d2f; on `fix/T-AUD-24j` `1 failed, 237 passed` (the yardstick lock
   only). So the two SF cases are T-AUD-24k's.
3. **Rehearsal:** R1 gives `1 failed, 237 passed`; the test file `6 passed` (`C:/4DApp/recheck/T-AUD-24p/rehearsal.diff`).
4. **The yardstick failure is T-COMA-10** (deferred 2026-11-07; csv sha 82780e0b vs locked 8ec81201 since T-COMA-3c).

### Rulings and the tradeoff that lost ###
- **A revision row, not a silent fix inside T-AUD-24o.** CLAUDE.md step 6. Lost: folding 3 lines into 24o (it would
  hide a regression in an unrelated row).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | 1 failed (T-COMA-10), 237 passed |
| step 2 | RAN | 6 passed |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-24p: repin the wired SF delta tests.

### Cold read ###
NONE (difficulty 1, CLAUDE.md process by difficulty).

### Correction history ###
(none)
