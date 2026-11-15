# T-AUD-23a — authoring sidecar (Windows Cowork, 2026-11-15)

Input: T-AUD-22 inventory complete (T-AUD-22h accepted, a5693be). First verification slice of the code-audit
suspects; app row on the Hydrogen lane (difficulty 3 -> gemini-4-hydrogen-high). Cowork file in the spec commit:
`labs/gaslab/audit_tasks/wikiaudit/scope/T-AUD-23a.txt` (25 ids).

### Verified context ###
1. **152 suspects: comlab 75, gaslab 25, rest 52** (C:/4DApp/recheck/scratch/suspects_all.txt). Observed on a5693be.
2. **The 25 scope ids have empty `same_as`; 34 claims name one of them** (CK0181 9, RK0191 10, RK0192 10, RK0082 3,
   CK0179 1, RK0247 1). Observed.
3. **`check_verdicts.py --scope scope/T-AUD-23a.txt` prints `VERDICTS FAIL 25 error(s)`; T-GASA-17 scope `VERDICTS OK
   ... claims 20`.** Observed. The checker accepts GK/CK/RK ids (REGISTERS globs claims_*.csv).
4. **firecrawl search without `--sources web` returns an "Alexandria Tools" catalogue, not web hits; with `--sources web
   --json` the P4 query lists en.wikipedia.org/wiki/OBD-II_PIDs first.** Observed 2026-11-15 (CLI 1.29.0).
5. **eras_sensitivity_masks.yaml: LEGACY (Euro 1 & 2) CO 1.0 / HC 150 / lambda 0.10; ADAPTIVE (Euro 3 & 4) 0.5 / 55 /
   0.05; MODERN (Euro 5 & 6) 0.2 / 15 / 0.02.** Observed (Vault copy read; register path labs/comlab/comlab/config).

### Rulings and the tradeoff that lost ###
- **Slice = the roots an outside standard or law decides** (J1979 scaling, J2012, legal idle limits). Lost: all 152 in
  one row (most are code-vs-own-wiki disagreements that need a design ruling, not a web source; they go to T-AUD-23c).
- **Search output inside the worktree** (`wikiaudit/search/`, deleted before finish) because the lane fence fails on
  any write outside the worktree. Lost: `C:/4DApp/recheck/.firecrawl/` as in T-GASA-17 (a headless claude row).
- **Paywalled standards**: abstract pages count as PRIMARY_STANDARD; secondary sources allowed with a note. Lost:
  UNSOURCED for every J1979 claim (would block the trim fix the evidence already supports).
- Difficulty 3. Survey = facts 1-5. Plan NONE. Docs row: no second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | pre-state `VERDICTS FAIL 25 error(s)` (P2); 25 placeholder UNSOURCED rows appended then restored: `VERDICTS OK scope=T-AUD-23a.txt claims 25` |
| step 2 | RAN | `VERDICTS OK scope=T-GASA-17.txt claims 20` (P3) |
| step 3 | SIMULATED | same simulation: `0` removed lines |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-23a: 25 code-audit roots (J1979 scaling, J2012, era thresholds) verified; VERDICTS OK.

### Cold read ###
cold read 2026-11-15 FOCUSED reader: 0 findings; 1 UNSETTLED (era range CK1384-CK1396 vs 8 scope ids) — RULED: R4 now lists the eight ids (C:/4DApp/recheck/scratch/T-AUD-23a_coldread.md) — 4 calls

### Correction history ###
(none)
