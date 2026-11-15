# T-AUD-24e — authoring sidecar (Windows Cowork, 2026-11-16)

Input: T-AUD-23a CK0535 and T-AUD-23b CK0537, CK0547 CONTRADICTED. Survey and corpus measurement by Cowork
(difficulty 2: no cold read; second review kept). Lane: Hydrogen medium.

### Verified context ###
1. **Corpus (v7, 314 cases; recheck/T-COMA-6/verdicts.py from audit/scratch/C5): tip 221 of 314 by family; with P1
   applied 0 verdicts change; the rules are live (CO ceiling 0 moves 11 verdicts); O2 0.35 loses one correct
   no-fault verdict.** Measured on 489ea94 (recheck/T-AUD-24e/).
2. **Suites with P1 applied: comlab 609, registry 510/5 — equal.** Rehearsed and restored.
3. **No text in no_fault.json states the old values.** grep.

### Rulings and the tradeoff that lost ###
- **CO 0.3** (legal idle limit, all cat cars from 9/2002; 0.5 only for 1995-2002 cars). Lost: an era-dependent
  ceiling (no era input on this rule).
- **O2 0.5** (S023 balanced ceiling). Lost: 0.35 (S023 typical; costs one correct corpus verdict and sits inside the
  0.3-0.7 'not lit' band anyway).
- **NF-002 NOx 50** (NF-001's own idle ceiling; S028 near 0). Lost: a bare guess such as 100.
- **Corpus measured by Cowork after promote, not by the implementer**: worktree runs import the main checkout.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | patch applied: `609 passed` |
| step 2 | SIMULATED | patch applied: `510 passed, 5 skipped` |
| step 3 | SIMULATED | pre `NF FAIL (0.5, 0.6, 300.0)`; patched `NF OK (0.3, 0.5, 50.0)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-24e: no-fault window CO 0.3, O2 0.5, NF-002 NOx 50; corpus 0 changed.

### Cold read ###
none (difficulty 2, process 055).

### Correction history ###
(none)
