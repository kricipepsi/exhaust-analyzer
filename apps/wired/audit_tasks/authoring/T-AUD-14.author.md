# T-AUD-14 — authoring sidecar (Windows Cowork, 2026-11-06)

Input: `audit/drift/2026-11-05_DRIFT_REPORT_vinlab.md`, `reviews/REVIEW_T-AUD-11c.md`. Rehearsal:
`C:/4DApp/recheck/T-AUD-14/` (`apply_fix.py`, `rehearsal.patch`, `census.sh`); AST check `C:/4DApp/recheck/T-AUD-4t/ast_same.py`.

### Verified context ###
1. **Each upheld finding re-read at its line** on `fix/T-AUD-13`: HLD:50, 96-106, 133-141, 148-151; LLD:116-120,
   143-146, 194-198; DLD:63-65, 128-130, 186-190, 205-208, 255-258, 268-271; VIN_VOCABULARY §4 (it already lists
   `vref_year_out_of_window` and `euro_unknown`; it lacks `wmi_brand_missing`, `vds_engine_ambiguous`). Code:
   `decoder.py` 127 (`_TYPE_CODE_WMIS`, 11 WMIs), 222-225 (four VDS indexes), 373 (BOXER), 384/388 (1996 rule, 2000
   default), 503-510 (0/0), 606-614, 794-817, 878; `tecdoc_query.py:75`; `models.py:242-256`. Observed.
2. **`model_year >= 1996` appears twice in `decoder.py`** (both the downstream-O2 rule); both get the citation. Observed.
3. **Two sites the report missed** carry the "12-13" error: the `decoder.py` docstring (named by REVIEW_T-AUD-11c) and
   LLD:109 (found by Cowork's census). Observed.
4. **Rehearsal** (restored): census base `stale 7`/`cited 0`, after `stale 0`/`cited 2`, the four flags `1 1 1`;
   `ast same` for `decoder.py`; vinlab `376 passed, 8 skipped`; ruff clean; 5 files, 35 insertions / 17 deletions.
   Observed.

### Rulings and the tradeoff that lost ###
- **KR6 is met in code, not relaxed in the PRD:** two comments. Lost: nothing (comment-only, AST-equal).
- **`vref_db1.db` documented as present with no reader,** not removed. Lost: a cleaner data folder (a data-file
  removal is not a docs row).
- Docs row (comments and a docstring only): no second-model review. Plan NONE, difficulty 1.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `stale 0`; `cited 2`; four flags `1 1 1`; `ast same` |
| step 2 | SIMULATED | `376 passed, 8 skipped` |
| step 3 | SIMULATED | ruff `All checks passed!`; status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-14: VINLab docs match the decoder (19 drift findings of 11c + 2 more "12-13" sites).

### Cold read ###
own pass 2026-11-06: P1-P3 measured · `apply_fix.py` exits on any literal count other than 1 (2 for the 1996 lines) ·
traceability: criteria 1-3 → steps 1-3 · patched: census pattern narrowed to the caller line (4 legitimate
"COMLab projector" mentions) · no finding.
cold read 2026-11-06 FOCUSED reader; trigger 1c grep hit (criterion 3 "only"); 0 findings, 0 patched — 1 call.

### Correction history ###
(none)
