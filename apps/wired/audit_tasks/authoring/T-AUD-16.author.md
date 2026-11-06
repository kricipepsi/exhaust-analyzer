# T-AUD-16 — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/drift/2026-11-05_DRIFT_REPORT_gaslab.md` (47 bullets), `reviews/REVIEW_T-AUD-11e.md`. Rehearsal:
`C:/4DApp/recheck/T-AUD-16/` (`apply_fix.py`, `rehearsal.patch`, `census.sh`, `stale_patterns.txt`).
Canary row of T-LOOP-19 (authoring SKILL.md First action / Context cells; channel 047 §4).

### Verified context ###
1. **Code facts re-measured on `fix/T-AUD-15`:** 4 `signature_type: catch_all` (POA_SIGNATURE, VVT_FAILURE,
   EVAP_CANISTER_SATURATED, INCOMPLETE_OXIDATION); `len(GasLabPayload.model_fields)` 15 (venv import); 6 `dna_gate:`;
   1 `requires_dtc: true` (EGR_DILUTION_MISFIRE), 0 readers in `gaslab/*.py`; `process.py` calls `load_ontology()`
   per call and `ontology_loader.load_ontology` has no cache; `confidence` read by `resolution._rich_co_ceiling` and
   `ranking._dna_tier`; collision `co_tier_max` default 0.45 from the YAML; `target_lambda_v112` / `co_low_idle`
   applied without a confidence check (`rule_engine.py` signature adjuster); worn rings `hc > 300`. Observed.
2. **46 of the 47 quotes still present;** the NOx `min: 1500` quote is gone. Observed (quote search over the report).
3. **Cold bucket probe:** `process()` with `EngineStateBucket.COLD_OPEN_LOOP_INVALID` on a normal reading returns
   `NORMAL_OPERATION` / `VALID`; with `STABILIZED_IDLE` the same reading returns a fault. The app sends only
   `STABILIZED_IDLE` (UI `gas_engine_state`) or `CRANKING` (`composition.py`, T-COMA-3b). Observed. Registered as
   T-AUD-20 (code row).
4. **Test coupling (047 §3 habit 1):** `test_validators.py::test_dna_gate_count_matches_wiki` counts §3.1 gate cells
   that do not start with `none` and pins 7. The first rehearsal wrote the two edges as gate values and failed it
   (wiki 9); the cells now start with `none (no `dna_gate`)`. Observed.
5. **Line endings:** the index holds LF for all 8 files; two working-tree copies were CRLF before a checkout
   normalised them. `apply_fix.py` keeps whatever ending each file has. Observed (`git ls-files --eol`).
6. **Rehearsal** (restored): census base `stale 31 / notimpl 0 / unread 0 / eol 8 w/lf`, after `0 / 9 / 3 / 8 w/lf`;
   gaslab `215 passed, 2 skipped, 4 deselected`; 8 files changed. Observed.

### Rulings and the tradeoff that lost ###
- **R1 docs follow the code.** Lost: code follows the docs (each promised feature is a new behaviour and needs its own
  row and corpus check).
- **R2 YAML reload documented.** Lost: an `lru_cache` (a code change for a 10 ms read; tests that write a temp YAML
  would need a cache reset).
- **R3 literals documented as cited.** Lost: moving them into `reasoning_grammar` (new YAML keys, the drift guard and
  its parser would change).
- **R4 not-implemented markers.** Lost: deleting the sections (loses the design intent the next row reads).
- **R5 edges as notes in `none` cells.** Lost: listing them as gates and editing the pinned test (a docs row editing a
  test).
- Docs row: no second-model review. Plan NONE, difficulty 1.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `stale 0`; `notimpl 9`; `unread 3`; `eol 8 w/lf`; 8 files in `git diff --stat` |
| step 2 | SIMULATED | `215 passed, 2 skipped, 4 deselected` |
| step 3 | SIMULATED | status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-16: GASLab docs match the shipped package (46 live bullets of 11e; docs follow code, 9 not-implemented marks).

### Cold read ###
own pass 2026-11-07: P1-P3 measured (rehearsal) · `apply_fix.py` exits on any literal count other than 1 · counts from venv import and grep (fact 1) · traceability: criteria 1-3 → steps 1-3 · 1c hits: R1 "every upheld finding" = the 46 live bullets (fact 2); "only the note and the RESULT" = criterion 3 · patched before the read: gate cells (fact 4) · no finding.
cold read 2026-11-07 FOCUSED reader; trigger 1c grep hit (R1 "every"); 0 findings, 0 patched — 20170 tok, 4 calls.

### Correction history ###
(none)
