# T-COMA-3c — authoring sidecar (Windows Cowork, 2026-11-07)

Input: channel 048 (operator ruling, option 1: relabel REAL-002 to `non_starter`; the lean root cause goes into the
case's note; record the old label and the reason), `authoring/T-COMA-3.design.md` item 7. Rehearsal:
`C:/4DApp/recheck/T-COMA-3c/` (`apply_fix.py`, `rehearsal.patch`, `score_real002.py`, `corpus_fix.json`).

### Verified context ###
1. **REAL-002 on `fix/T-AUD-16`:** `triage_engine_state` `will_not_start`; labels `lean_condition` / `ERR-LC-003` /
   `05_fault_taxonomy.md#CONCEPT_TAXONOMY_TABLE`; `viability_note` "No-start lean; fuel starvation"; the app returns
   `non_starter NS-001` at 0.95 (T-COMA-3b corpus). Observed (csv read, `corpus_impl.json`).
2. **Code space:** the 5 other non-starter rows carry `ERR-NS-001/003/004` and `06_fault_atlas_families.md#CONCEPT_FAMILIES`;
   `global_fault_registry.json` names `ERR-NS-003` `fuel_delivery_failure_no_start` and `ERR-LC-003`
   `fuel_pump_low_pressure` (wiki 05 table). Observed.
3. **Readers of the CSV:** `apps/wired/v7/tests` `2 failed, 47 passed` and registry `test_non_starter_rules.py`
   `31 passed`, equal on base and fix; `labs/comlab/tests/unit/test_tunable_reweight.py` `1 error` on both (left out of
   the gates). `test_oracle_repin.py` checks no family snapshot. Observed.
4. **Verdicts:** probe on the fix, `differ 0` of 314 against `T-COMA-3b/cw/corpus_impl.json` (labels do not feed
   `diagnose`). `score_case` REAL-002: `fault_family` FAIL → PASS, the rest unchanged. Observed.
5. **Other REAL-002 copies:** `labs/comlab/registry/corpus_curated.csv`, `corpus_meta.json`, `graph/v2_docs/graph.json`,
   `rules/lean_condition.json` `passes_cases`. Built registry artefacts (T-COMA-3a: cannot be rebuilt here). Observed.

### Rulings and the tradeoff that lost ###
- **R1 `ERR-NS-003`.** Lost: `NS-001`, the app's rule id (would pass the `fault_code` dimension, but it names a rule,
  not a fault, and differs from the other five non-starter rows).
- **R2 note in `viability_note`.** Lost: a new column (a schema change for one row).
- **R3 v7 row only.** Lost: editing the curated registry copies (built artefacts; a hand edit diverges from their
  build tool). `source_category` / `library_conclusion` kept as v5 provenance. Lost: a fully consistent row.
- Data row: no code changes, so no second-model review. Plan NONE, difficulty 1.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | P1 after-values; numstat `1 1` (working-tree diff) |
| step 2 | SIMULATED | `fault_family PASS`, rest as P3 |
| step 3 | SIMULATED | `corpus 314`, `differ 0` |
| step 4 | SIMULATED | `2 failed, 47 passed`; `31 passed` |
| step 5 | SIMULATED | status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-3c: REAL-002 labelled non_starter ERR-NS-003 (channel 048); lean root cause kept in viability_note.

### Cold read ###
own pass 2026-11-07: P1-P5 measured (rehearsal, facts 3-4) · `apply_fix.py` exits unless each old value occurs once in the row · traceability: criteria 1-3 → steps 1-5 · 1c hits: "only" in P2/criterion 3 = one CSV file, note + RESULT · test coupling (047 §3 habit 1): `rg` of the old label in tests finds no REAL-002 pin · no finding.
cold read 2026-11-07 FOCUSED reader; trigger 1c grep hit ("only"); 0 findings, 0 patched — 20582 tok, 4 calls.

### Correction history ###
(none)
