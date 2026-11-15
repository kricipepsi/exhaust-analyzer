# T-AUD-22d — authoring sidecar (Windows Cowork, 2026-11-15)

Input: ledger row T-AUD-22; T-AUD-22c, T-COMA-31 and T-COMA-32 accepted. First app row after the loop repair program
(058); first app row on the Hydrogen lane (difficulty 3 -> gemini-4-hydrogen-high, operator 2026-11-15).

### Verified context ###
1. **`check_code_claims.py --group comlab --files 'labs/comlab/comlab/config/global_fault_registry.json'` prints
   `CLAIMS FAIL 303 error(s)`.** Observed 2026-11-15 on `44c3d27`.
2. **Rules scope: `CLAIMS OK group=comlab scope=labs/comlab/registry/rules/* candidates 357 covered claims 691`;
   last row `CK0692`.** Observed (`tail -1 claims_comlab.csv`).
3. **Step 2 pre-state `knobs 208 internal 0`.** Observed (the step 2 command).
4. **Kinds of the 303 (P5): base_weight 104, bonus_on_dtc_match 104, ui_diagnostic_string 35, value 32, bare array
   number 8, fault_wiki_page 1, remediation_map entry 19 (file lines > 2772).** Observed (awk over candidates).
5. **`resync_register.py --base 3f545af` for comlab-code, gaslab-code and wiki: moved 0 changed 0 gone 0.** Observed
   (dry run). A fresh `extract_code_candidates.py` rewrites 768 lines of `candidates_comlab.csv` (id renumbering after
   the T-COMA-32 resync): the first action no longer runs the extractor. Observed, then restored with git checkout.
6. **The registry has no `wiki_ref` (0 matches).** Observed (`grep -c wiki_ref`).

### Rulings and the tradeoff that lost ###
- **One row for the whole file** (303, near T-AUD-22c's 358 done in 7 min). Lost: split knobs and text.
- **No extractor in the first action** (fact 5). Lost: regenerate candidates and resync again, which re-labels ids
  for no gain.
- **Lane run: no commit by the implementer.** The lane forbids commits; promote commits the worktree's changes on
  `fix/T-AUD-22d`. Step 4 reads the working tree. Lost: the claude launcher (Opus fallback), used only when agyloop
  is down.
- Difficulty 3. Survey = facts 1-6. Plan NONE. Docs row: no second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | DEFERRED | pre-state `CLAIMS FAIL 303 error(s)` (P2) |
| step 2 | RAN | pre-state `knobs 208 internal 0`; post-state needs the rows |
| step 3 | RAN | `CLAIMS OK group=comlab scope=labs/comlab/registry/rules/* candidates 357 covered claims 691` |
| step 4 | DEFERRED | `0` removed lines; the CSV, note and RESULT in status |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-22d: COMLab global fault registry literals (303 lines) classified; CLAIMS OK scope=global_fault_registry.json.

### Cold read ###
cold read 2026-11-15 FOCUSED reader: 0 findings (C:/4DApp/recheck/scratch/T-AUD-22d_coldread.md) — 5 calls

### Correction history ###
(none)
