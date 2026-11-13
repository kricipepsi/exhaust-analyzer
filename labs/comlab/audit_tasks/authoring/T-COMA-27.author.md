# T-COMA-27 — authoring sidecar (Windows Cowork, 2026-11-13)

Input: F-C1-2 (`repo/audit/reports/R1_C1_20261017.md`); `labs/gaslab/gaslab/family_map.py`; the 16 REG-V2 rule
files. Rehearsal and survey: `C:/4DApp/recheck/T-COMA-27/`, `C:/4DApp/recheck/F-C1-2/`.

### Verified context ###
1. **12 states are still unrouted on `d8495f9`**, each giving LC-002 at 0.86 in the probe. Observed (step 3 on base).
2. **Corpus census** (`recheck/F-C1-2/states.py`): only INCOMPLETE_OXIDATION (15 cases), EVAP_CANISTER_SATURATED (4)
   and FLAT_CAMSHAFT (4) occur in the 314-case v7 corpus. The other 9 occur in no case. Observed.
3. **GASLab names a family for all 12** (`family_map.py` lines 36-60), and each family has a REG-V2 file. Observed.
4. **Label check:** INCOMPLETE_OXIDATION → catalyst_failure, but none of its 15 labels is catalyst_failure, and 7 of them
   score correct today. FLAT_CAMSHAFT → cam_timing, but its labels are lean, catalyst x2 and rich (3 correct today).
   Observed.
5. **Weight:** at base 0.8 a new rule loses to LC-002 (0.86, fires on normal map_kpa). At 0.9 it wins: the probe then
   routes 10 states to their new rules. Observed.
6. **Rehearsal** (restored; `rehearse.py` round-trips): comlab `563`, wired `186`, ui `75`, registry
   `508 passed, 5 skipped`, reweight `2`, new test `21`, corpus `changed 0 of 314`, diff stat
   `10 files changed, 309 insertions(+), 6 deletions(-)`. Observed.
7. **NF-001 ignores the chemical state** and wins on healthy gas numbers. The new test therefore uses the probe's
   gas numbers (CO 0.3 %), which keep NF-001 out. Observed.

### Rulings and the tradeoff that lost ###
- **Route by GASLab's own family map.** Lost: per-state rule design with OBD/DTC evidence. No corpus case exists for
  9 of the 10 states, so richer evidence could not be measured; the GASLab map is the documented authority.
- **Base 0.9.** Lost: fixing the LC-002/MF-005 sink mechanism (F-C1-2's F2 half). That is a scoring change with corpus
  risk; it stays a residual.
- **Exclude FLAT_CAMSHAFT and INCOMPLETE_OXIDATION.** Lost: full closure of the probe. Fact 4 shows a rule would cost
  up to 10 correct verdicts. Residual: a data ruling on those two labels.
- **Text insertion, not a JSON rewrite.** The rule files mix escaped and raw non-ASCII; a rewrite churned 217 lines.
- Difficulty 2 (data plus test pins, scripted). Roster 2026-11-13: Opus 5.5 medium. Plan NONE; code row: second-model
  review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `563 passed`; `186 passed`; `75 passed` |
| step 2 | SIMULATED | `508 passed, 5 skipped`; `2 passed`; `21 passed` |
| step 3 | SIMULATED | `unrouted chemical states: 2 [...]`; `3 failed, 10 passed, 3 deselected` |
| step 4 | SIMULATED | `changed 0 of 314` |
| step 5 | SIMULATED | diff stat as P2; ruff to be confirmed by the implementer |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-27: 10 unrouted GASLab states get REG-V2 rules in GASLab's family; 2 excluded by corpus labels.

### Cold read ###
own pass 2026-11-13: P1-P2 measured (facts 1, 6) · `rehearse.py` exits on a dirty tree or a failed apply ·
traceability: criteria 1-2 → steps 1-5 · cold read: not run (difficulty 2, process by difficulty, 055) · no finding.

### Correction history ###
(none)
