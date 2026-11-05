# T-AUD-4i — authoring sidecar (Windows Cowork, 2026-11-05)

### Verified context ###
1. **F-C5-3 holds** at the 4d tip: both wideband types send the raw value. Observed (read).
2. **The audit's VIN no longer reproduces**: `WDD1690321J749046` now decodes PARTIAL NARROWBAND (no year, EURO_1).
   `WVWZZZ1KZAP012480` decodes WIDEBAND_AFR (1 of 7 corpus VINs, `C:/4DApp/recheck/T-AUD-4d/afr_census.py`). Observed.
3. **Rehearsal** (`rehearse.py`): base AFR 10/14.7/20 all SF-001; as λ SF-002/EF-004/SF-001. Observed.
4. **Pins** (`apply_fix.py`, restored): P3. Observed.

### Rulings and the tradeoff that lost ###
- Divide by 14.7, the scan-tool AFR scale (λ × 14.7). Lost: GASLab's 14.71 (petrol chemistry; 0.07 % apart) and a
  per-fuel stoich (the fuel blend is not sent, F-C5-10).
- Split from T-AUD-4e (HIGH, one UI line). The 4e remainder is split too: T-AUD-4j (symptom path, F-C5-4/5),
  T-AUD-4k (inbound contract and lab suppression, F-D2-2/9 and the gas_lab_output residual), 4e (census).
- Difficulty 2: one branch. Code row, so a second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | base new file `3 failed, 1 passed`, ui 30; rehearsed fix `4 passed`, ui 34; mutant `3 failed` |
| step 2 | RAN | wired 62 (base and fix) |
| step 3 | RAN | `rehearse.py` on the rehearsed fix: sent = lambda on all three lines |
| step 4 | RAN | ruff `All checks passed!` on the rehearsed fix |

### Exclusivity ###
No other implementer runs. T-AUD-4j follows.

### Progress hook ###
T-AUD-4i: a wideband-AFR reading reaches OBDLab as lambda (AFR / 14.7); the AFR now moves the verdict.

### Cold read ###
own pass 2026-11-05: P1-P4 measured · literals found once (`elif o2_type in ("WIDEBAND_LAMBDA", "WIDEBAND_AFR"):`,
`UPSTREAM_O2_WIDEBAND_AFR_MAX = 20.0`); new names absent at base · counts: ui 30 + 4 = 34; mutant 3 · traceability:
criteria 1-4 → steps 1-4 · no finding. cold read: skipped (the second review covers the code).

### Correction history ###
(none)
