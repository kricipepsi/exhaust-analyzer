# T-AUD-23b — authoring sidecar (Windows Cowork, 2026-11-15)

Input: T-AUD-23a accepted (8ae8508): 25 roots verified. Second verification slice of the code-audit suspects; app row
on the Hydrogen lane (difficulty 3 -> gemini-4-hydrogen-high). Cowork file in the spec commit:
`labs/gaslab/audit_tasks/wikiaudit/scope/T-AUD-23b.txt` (29 ids).

### Verified context ###
1. **The 29 scope ids have empty `same_as`; 8 claims name one of them** (CK0859 2, CK1021 2, CK1022 1, RK0268 1, RK0269
   1, RK0275 1). Observed on 8ae8508.
2. **`check_verdicts.py --scope scope/T-AUD-23b.txt` prints `VERDICTS FAIL 29 error(s)`; T-GASA-17 20 and T-AUD-23a 25
   `VERDICTS OK`.** Observed.
3. **26 of the 29 are flagged suspects; RK0275 (downstream O2 1.5 V), RK0362/RK0365 (CO2/O2 input max 22 %) are not**
   (named as candidates in REVIEW_T-AUD-22h). Observed.
4. **`sources.csv` ends at S013.** Observed.

### Rulings and the tradeoff that lost ###
- **Slice = sensor and gas values decided by a maker, OEM or physics.** Lost: the code-vs-own-wiki suspects (T-AUD-23c,
  Cowork rulings, no web) mixed in, which need no source.
- **Search output inside the worktree** (`wikiaudit/search/`, deleted before finish): the lane fence. As T-AUD-23a.
- Difficulty 3. Survey = facts 1-4. Plan NONE. Docs row: no second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | pre-state `VERDICTS FAIL 29 error(s)` (P2); 29 placeholder UNSOURCED rows appended then restored: `VERDICTS OK scope=T-AUD-23b.txt claims 29` |
| step 2 | RAN | `VERDICTS OK scope=T-GASA-17.txt claims 20`; `VERDICTS OK scope=T-AUD-23a.txt claims 25` (P3) |
| step 3 | SIMULATED | `0` removed lines (same simulation) |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-23b: 29 code-audit roots (O2, ECT, MAF, VE, gas values) verified; VERDICTS OK.

### Cold read ###
cold read 2026-11-15 FOCUSED reader: 0 findings; Routing typo (base named fix/T-AUD-23b) fixed before dispatch; reader wrote no scratch file (report in chat) — 3 calls

### Correction history ###
(none)
