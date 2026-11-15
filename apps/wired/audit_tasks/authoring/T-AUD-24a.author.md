# T-AUD-24a — authoring sidecar (Windows Cowork, 2026-11-15)

Input: T-AUD-23a (8ae8508) found the fuel-trim bound ±127 CONTRADICTED by SAE J1979 (CK0181, RK0191, RK0192 and their
same_as chains). First fix row; code row on the Hydrogen lane (difficulty 3 -> gemini-4-hydrogen-high); second review
by second_review.py (the lane model implements, so it cannot be the second model).

### Verified context ###
1. **55 lines hold 127 or 254 in the P1 files, OBD_VOCABULARY.md and tests/fixtures/descriptor.py on 319c336; every one
   is a trim bound.** Observed (step 5 pre-state, each line read).
2. **ADR-0006 (T-W-6) claims ECUs report ±127 when a trim saturates.** Read at ADR_OBDLab.md:219-245. False per J1979:
   PIDs 06-09 = (A-128)*100/128. DISPUTE raised to the operator in chat 2026-11-15.
3. **Rail consumers gate at 25 % / -15 %** (fault_atlas_router.py:103, ecu_hardware_checker.py:14,
   perception_contradiction.py:54); no code detects a rail at 127. Observed (grep "rail").
4. **No JSON in labs/ or apps/ (1435 files) holds a trim outside -100..99.22.** Observed (Cowork scan).
5. **Baselines: obdlab 394/2 skipped, comlab 602, wired 186, ui 75 (from apps/ui; from the repo root 15 collection
   errors `No module named 'ui_payload'`).** Observed on 319c336.

### Rulings and the tradeoff that lost ###
- **Narrow to -100..99.22 and reject outside.** Lost: clamp out-of-range values to the rail (hides bad input) and keep
  ±127 (contradicts the standard; T-AUD-23a).
- **99.22, not 99.21875**: matches the existing FF_TRIM_MAX and the wiki. Lost: the exact value (one more literal).
- **Amend ADR-0006, do not delete it**: the "railed trim is a signal" idea stands.
- **Plan NONE**: every edit is named; the risk is test churn, which the suites catch. Lost: a plan round trip.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | baseline `394 passed, 2 skipped` |
| step 2 | RAN | baseline `602 passed` |
| step 3 | RAN | baseline `186 passed` |
| step 4 | RAN | baseline `75 passed` (from apps/ui) |
| step 5 | SIMULATED | pre-state `55` (9 files); with every 127/254 substituted then restored: `0` |
| step 6 | SIMULATED | pre-state `R5 FAIL OBDLiveDataPayload`; same substitution: `R5 OK OBDLiveDataPayload` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-24a: fuel-trim bounds -100..99.22 % (SAE J1979) in OBDLab, COMLab, wired, UI; ADR-0006 amended.

### Cold read ###
cold read 2026-11-15 FULL reader: 1 IMPLICIT (descriptor.py fixture pins ±127, not in scope), 1 DIRECT (step 5 regex
missed uppercase and bare-constant lines, so it did not measure P3; step 6 checked COMLab only), 1 AMBIGUOUS
(OBD_VOCABULARY lines 36-38 besides 148) — all RULED and fixed before dispatch: descriptor.py in P5/R5/Files, ingestion
:499 and OBD_VOCABULARY 36-38/347 in scope, step 5 = plain 127/254 grep over 9 files (pre 55, simulated post 0), step 6
checks both labs (C:/4DApp/recheck/scratch/T-AUD-24a_coldread.md) — 10 calls

### Correction history ###
(none)
