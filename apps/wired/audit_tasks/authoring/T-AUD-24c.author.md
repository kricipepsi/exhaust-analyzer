# T-AUD-24c — authoring sidecar (Windows Cowork, 2026-11-15)

Input: T-AUD-23a verdict CK0482 CONTRADICTED (SAE J2012: P0301-P0312 cylinder misfire codes). Survey by Cowork
(difficulty 2: no cold read; code row keeps its second review). Lane: Hydrogen medium.

### Verified context ###
1. **15 lists end their cylinder sweep at P0304** (global_fault_registry 8, rules/misfire 6, rules/mechanical_wear 1).
   Observed (step 3 pre-state `MISFIRE FAIL 15 15`).
2. **Only MW-007's description states the range in text** (grep over comlab code, rules, docs, wiki). Observed.
3. **No corpus or data file mentions P0305-P0312** except generated graph caches and the verdicts. Observed (scan).
4. **Rehearsal (recheck/T-AUD-24c/rehearsal.patch, lists only): comlab 608, registry 510/5, step 3 `MISFIRE OK 15 0`;
   registry baseline on ffb12fd 510/5.** Observed and restored.

### Rulings and the tradeoff that lost ###
- **Extend to P0312**, the SAE J2012 cylinder range. Lost: a P030X prefix match in code (a design change to the
  matcher, larger blast radius).
- **corpus_meta.json left alone** (generated). Lost: hand-editing a generated file.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | rehearsal patch applied: `608 passed` |
| step 2 | SIMULATED | rehearsal patch applied: `510 passed, 5 skipped` |
| step 3 | SIMULATED | pre `MISFIRE FAIL 15 15`; patched `MISFIRE OK 15 0` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-24c: cylinder-misfire lists P0300-P0312 (15 lists); MW-007 text.

### Cold read ###
none (difficulty 2, process 055).

### Correction history ###
(none)
