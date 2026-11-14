# T-AUD-22c — authoring sidecar (Windows Cowork, 2026-11-14)

Input: ledger row T-AUD-22; T-AUD-22b and T-AUD-22-RESYNC accepted. Tool changes by Cowork in the spec commit:
`extract_code_candidates.py` data filter skips `\u00a7 N`, other `\uXXXX` escapes and digit-holding identifiers;
`resync_register.py` strips the text of changed lines (3 wiki rows, 2 gaslab rows re-written stripped; both checkers OK).

### Verified context ###
1. **Filter change: ids and shas stable (3794 rows), 1146 data rows flipped to auto, 0 Python rows, 0 to domain;
   to_classify 2574 -> 1428.** Observed (compare to the committed candidates).
2. **Slices after the filter: rules a-l 132 + m-z 226 = 358 (16 files); global registry 303; KG 261; config YAML 213;
   proposals 174.** Observed (fnmatch counts).
3. **P2 `CLAIMS FAIL 358`; step 2 pre-state `knobs 130 internal 0`; P4 `CLAIMS OK ... *.py 293 ... 301`.** Observed.
4. **609 double-encoded escapes (`\u00e2\u20ac…`) in `global_fault_registry.json` and 9 KG JSON files.** Observed
   (grep -F). -> row T-COMA-31.

### Rulings and the tradeoff that lost ###
- **Both rules halves in one row** (358, near T-AUD-22b's 293 done in 13 min). Lost: two rows of ~180.
- **No knowledge seed; step 2 checks the R3 knob ruling instead.** The candidate seeds (lean λ > 1.03, CO2 ~16 %
  ceiling, knock DTCs P0324-P0334) agree with the register or are approximate. Lost: a weak seed that tests nothing.
- **Extractor filter tightened before the row** so the implementer classifies values, not ids. Lost: leave the 1146
  noise rows for the implementer (cheap NON_DOMAIN rows, but ~45 % of the time).
- Difficulty 3, Opus 5.5 medium per roster. Survey = facts 1-4. Plan NONE. Docs row: no second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | DEFERRED | pre-state `CLAIMS FAIL 358 error(s)` (P2) |
| step 2 | RAN | pre-state `knobs 130 internal 0`; post-state needs the rows |
| step 3 | RAN | `CLAIMS OK group=comlab scope=*.py candidates 293 covered claims 301` |
| step 4 | DEFERRED | the spec commits plus one commit, `1 file changed`, `0` removed lines |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-22c: COMLab registry rules literals (358 lines) classified, citation-checked; CLAIMS OK scope=rules.

### Cold read ###
cold read 2026-11-14 FOCUSED reader: 0 findings (C:/4DApp/recheck/scratch/T-AUD-22c_coldread.md) — 5 calls

### Correction history ###
(none)
