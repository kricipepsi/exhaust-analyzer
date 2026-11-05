# T-AUD-4f — authoring sidecar (Windows Cowork, 2026-11-05)

### Verified context ###
1. **F-C3-1 holds** at the 4c tip: the frozen branch sets `normalized_lambda = 1.0  # wiki: stoich default when frozen`;
   OBDLab's payload requires a float; COMLab's ingestion takes `float | None`. Observed (read).
2. **Rehearsal** (`rehearse.py`, `rehearse.out`): as-is 2 of 297 runs are frozen (0 changes); at ECT 40, 296 frozen,
   21 verdict changes, 0 new exceptions. Several move NF-001 → a fault: the made-up stoich λ made a cold engine look
   healthy. Observed.
3. **Pins** (Cowork's edit on the working copy, restored): exactly 5 obdlab tests fail (P3); wired, ui, dnalab
   unchanged. Observed.

### Rulings and the tradeoff that lost ###
- None, not 1.0, when frozen (wiki §4.1 blocks lambda analytics). Lost: keep 1.0 and rely on T-AUD-4g's gate (COMLab
  would still read a made-up perception value wherever the gate is not consulted).
- Plan NONE: the 5 changed pins are measured. Lost: a plan gate (≈ 10 % context for a 3-line change).
- Difficulty 3; code row, so a second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | base obdlab `390 passed, 2 skipped`; rehearsed fix `5 failed, 385 passed` (the P3 pins) |
| step 2 | RAN | wired 46, ui 30, dnalab 27 (base and rehearsed fix) |
| step 3 | RAN | comlab `526 passed, 4 skipped, 2 errors` |
| step 4 | SIMULATED | `rehearse.py` patches the COMLab payload in memory: P2 |
| step 5 | DEFERRED | ruff and the log are the observables |

### Exclusivity ###
No other implementer runs. T-AUD-4g follows (COMLab gate reader).

### Progress hook ###
T-AUD-4f: frozen OBDLab emits no lambda (None, not 1.0); 21 cold-case verdicts change; 5 frozen pins updated.

### Cold read ###
own pass 2026-11-05: P1-P4 measured · literals found once (`normalized_lambda = 1.0  # wiki: stoich default when frozen`,
`normalized_obd_lambda: float = Field(ge=0.7, le=1.3)`, `if cmd_lambda is not None:`) · counts: 390 + 1 = 391 ·
traceability: criteria 1-4 → steps 1-5. cold read: skipped (the second review covers the code).

### Correction history ###
(none)
