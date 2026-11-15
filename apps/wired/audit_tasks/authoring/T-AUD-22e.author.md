# T-AUD-22e — authoring sidecar (Windows Cowork, 2026-11-15)

Input: ledger row T-AUD-22; T-AUD-22d accepted (be0273d, pushed). Second app row on the Hydrogen lane (difficulty 3
-> gemini-4-hydrogen-high).

### Verified context ###
1. **`check_code_claims.py --group comlab --files 'labs/comlab/comlab/config/kg/*'` prints `CLAIMS FAIL 261 error(s)`.**
   Observed 2026-11-15 on be0273d.
2. **Registry scope: `CLAIMS OK group=comlab scope=labs/comlab/comlab/config/global_fault_registry.json candidates 303
   covered claims 1025`; last row `CK1026`.** Observed.
3. **Step 2 pre-state `schema 22 non_domain 0`.** Observed (the step 2 command, rehearsed from the task file text).
4. **Kinds of the 261 (P5): schema_version 13, _kg_schema.json 9, mechanical_failure_mode 27, list strings 212.**
   Observed (grep over candidates).
5. **The KG files have no `wiki_ref` (grep -c on misfire.json prints 0).** Observed.

### Rulings and the tradeoff that lost ###
- **One row for all 14 KG files** (261, below T-AUD-22d's 303 done in 7 min). Lost: split by family.
- **Step 2 checks the R3 NON_DOMAIN ruling** (schema lines), as T-AUD-22d checked its knobs. Lost: no seed.
- **Lane run: no commit by the implementer**; promote commits on fix/T-AUD-22e. Step 4 reads the working tree.
- Difficulty 3. Survey = facts 1-5. Plan NONE. Docs row: no second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | DEFERRED | pre-state `CLAIMS FAIL 261 error(s)` (P2) |
| step 2 | RAN | pre-state `schema 22 non_domain 0`; post-state needs the rows |
| step 3 | RAN | `CLAIMS OK group=comlab scope=labs/comlab/comlab/config/global_fault_registry.json candidates 303 covered claims 1025` |
| step 4 | DEFERRED | `0` removed lines; the CSV, note and RESULT in status |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-22e: COMLab knowledge-graph literals (261 lines) classified; CLAIMS OK scope=kg/*.

### Cold read ###
cold read 2026-11-15 FOCUSED reader: 0 findings (C:/4DApp/recheck/scratch/T-AUD-22e_coldread.md) — 4 calls

### Correction history ###
- 2026-11-15 (Cowork, after the hand-back B12): `check_code_claims.py` decodes `\uXXXX` escapes in the candidate
  text before NUM_RE (`unescape`, f4f0347); the rules, `*.py`, registry and gaslab scopes stay CLAIMS OK; the 354
  implementer rows pass unchanged. No task-file change.
