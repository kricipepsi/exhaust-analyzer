# T-AUD-22f — authoring sidecar (Windows Cowork, 2026-11-15)

Input: ledger row T-AUD-22; T-AUD-22e accepted (8355d72, pushed; checker fix f4f0347). Last COMLab slice; third app row
on the Hydrogen lane (difficulty 3 -> gemini-4-hydrogen-high).

### Verified context ###
1. **`check_code_claims.py --group comlab --files 'labs/comlab/comlab/config/*.yaml'` prints `CLAIMS FAIL 213 error(s)`;
   the whole group prints the same `CLAIMS FAIL 213 error(s)`.** Observed 2026-11-15 on 8355d72 (the glob matches the
   `proposals/` files too: fnmatch `*` crosses `/`).
2. **Last row `CK1380`; kg scope `CLAIMS OK ... candidates 261 covered claims 1379`.** Observed.
3. **Step 2 pre-state `era_limits 9 linked 0`.** Observed (the step 2 command, rehearsed from the task file text).
4. **Per file (P5): entries.yaml 147, symptom_prior.yaml 22, proposals.yaml 17, eras_sensitivity_masks.yaml 16,
   taxonomy_backbone.yaml 10, tag_discriminator.yaml 1.** Observed (checker uncovered list).
5. **Era thresholds: LEGACY (1990-2000) CO 1.0 % HC 150 ppm lambda ±0.10; ADAPTIVE (2000-2010) CO 0.5 % HC 55 lambda
   ±0.05; MODERN (2010-2020) CO 0.2 % HC 15 lambda ±0.02. W1109 (CO ≤ 0.30 % natural idle) and W1110 (≤ 0.20 % raised
   idle) are CONFIRMED against DVSA S001 in wikiaudit/verdicts.csv (T-GASA-17).** Observed. -> DISPUTE raised to the
   operator 2026-11-15; R5 makes the row record each as suspect or linked.

### Rulings and the tradeoff that lost ###
- **One row for all six YAML files** (213, below T-AUD-22e's 261). Lost: proposals apart.
- **Step 2 forces the era limits to be compared** with the verified legal limits (linked or suspect). Lost: a count
  check that a bare classification passes.
- **Step 3 is the whole COMLab group**: this slice closes it. Lost: scope-only check.
- **Lane run: no commit by the implementer**; promote commits on fix/T-AUD-22f.
- Difficulty 3. Survey = facts 1-5. Plan NONE. Docs row: no second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | DEFERRED | pre-state `CLAIMS FAIL 213 error(s)` (P2) |
| step 2 | RAN | pre-state `era_limits 9 linked 0`; post-state needs the rows |
| step 3 | RAN | pre-state `CLAIMS FAIL 213 error(s)` (P4) |
| step 4 | DEFERRED | `0` removed lines; the CSV, note and RESULT in status |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-22f: COMLab config YAML literals (213 lines) classified; the COMLab group CLAIMS OK.

### Cold read ###
cold read 2026-11-15 FOCUSED reader: 0 findings (C:/4DApp/recheck/scratch/T-AUD-22f_coldread.md) — 3 calls; its unsettled items (fix/T-AUD-22e exists, W1109/W1110 rows) checked by Cowork

### Correction history ###
(none)
