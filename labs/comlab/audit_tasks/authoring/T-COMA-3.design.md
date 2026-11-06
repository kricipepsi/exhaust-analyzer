# T-COMA-3 design input and split (Windows Cowork, 2026-11-06)

Measured on `fix/T-AUD-4r` (`53d6ce3`). Scripts: `C:/4DApp/recheck/T-COMA-3a/` (`apply_fix.py`,
`rehearsal_partial.patch`, `cw/corpus.json`). The clone was restored after each run.

## Facts
1. **Four items, four owners.** GASLab's sample validity (cranking samples), a registry rule (P0335), the shim's DTC
   source (OBD `active_dtcs`) and a corpus label (REAL-002). No item depends on another.
2. **OBD `active_dtcs` alone: no product path.** In all 207 v7 corpus cases with OBD DTCs, they are a subset of
   `dtc_confirmed_json` (0 OBD-only, 0 extra). The UI's only OBD DTC source is the DTCLab panel
   (`composition._with_user_dtcs`, T-AUD-4h). Ruling: no row (too small); a JSON caller that sends OBD DTCs without
   DTCLab is the only exposure.
3. **P0335 has no non_starter rule.** NS-004 is fuel delivery (P0230, P0087, P0190). case_040 (P0335 in both lists,
   `will_not_start`) gives `NS-NO-RULE` abstain since T-COMA-1.
4. **A new NS-005 works on the live path.** Rehearsal (`apply_fix.py`): NS-005 = P0335/P0336 any_match GATING, rpm < 600
   SUGGESTIVE, no chemistry, base 0.7, ceiling 0.8. Corpus: exactly one case moves, case_040 `NS-NO-RULE` abstain →
   `non_starter` `NS-005` 0.85; 313 unchanged. comlab `503/4/2` unchanged.
5. **Two registry pins block NS-005 as rehearsed.** `test_non_starter_rules.py::test_all_case_ids_resolve`: `passes_cases`
   must name a case in `registry/corpus_curated.csv` (252 cases), and case_040 is `disposition: drop` ("duplicate
   baseline", `corpus_meta.json`); no curated case carries P0335/P0336. `test_integration_shim.py::
   test_shim_loads_all_16_rule_files` pins 73 rules. `test_build_corpus.py` already fails 5 tests on the base.
6. **v2 verdicts need no KG node:** `fault_id = rule_id`, `fault_name = description` (`integration_shim.py:53`). The
   KG's `ERR-NS-00x` ids are a different space (KG `ERR-NS-005` is "non_starter_invalid_sample"); no collision.
7. **REAL-002** is `will_not_start` but labelled `lean_condition` / `ERR-LC-003`. Under T-COMA-1 ruling B a non-starter
   session is decided by the `non_starter` family only, so the app cannot meet this label by design.

## Split
| row | scope | plan | owner question |
|---|---|---|---|
| T-COMA-3a | NS-005 (P0335/P0336) + keep case_040 in the curated corpus (blueprint `keep`, regenerate) + rule-count pin 73 → 74 | NONE if the blueprint regenerates cleanly; else REQUIRED | none (Cowork) |
| T-COMA-3b | GASLab: a cranking sample (rpm < 600, `will_not_start`) is not judged by the running-engine CO+CO₂+O₂ window, so NS-001..003 can score; the composition passes a cranking engine state | REQUIRED (cross-lab design) | none (Cowork) |
| T-COMA-3c | REAL-002's label vs ruling B | — | corpus-label owner: relabel to `non_starter`, or drop from the non-starter scoring set (channel question to Linux Cowork) |

## Rulings (Cowork)
- NS-005, not P0335 added to NS-004: NS-004 is fuel delivery; a crank-sync loss stops spark and injection both.
  Lost: one fewer rule. P0340 (CMP) stays out: many engines start on crank sync alone.
- OBD-only DTCs: no row (fact 2).
- Order: 3a (smallest, one verdict move), then 3b, then 3c after the answer.

## T-COMA-3b survey (2026-11-06, on fix/T-COMA-3a 9ff27c0)
- `labs/gaslab/gaslab/validity_gates.py` `triangle_gate`: CO+CO2+O2 < 14 or > 18 → `INVALID` (GAS_WIKI §6.1, "a clean
  petrol burn"); `dilution_gate`: CO+CO2 ≤ 6 % fails. A no-combustion cranking sample is near air (O2 ≈ 20.9 %, CO2 ≈ 0),
  so both gates reject every cranking sample; the shim then drops `chemistry_state` (`sample_validity == "INVALID"`) and
  NS-001..003 are pruned.
- `gaslab/contracts.py` `EngineStateBucket` has STABILIZED_IDLE, REGULATORY_HIGH_IDLE, STRESS_IDLE,
  COLD_OPEN_LOOP_INVALID: no cranking state. The UI hard-codes `gas_engine_state` STABILIZED_IDLE (T-AUD-4r kept it).
- The design the row needs (plan REQUIRED): a cranking state from the composition when `triage.engine_state` is
  `will_not_start` (GASLab bucket + COMLab mirror), and cranking-specific validity in GASLab (no triangle/dilution
  gate; classify LEAN_MISFIRE / RICH_MISFIRE / INCOMPLETE_COMBUSTION from the cranking chemistry NS-001..003 already
  gate on: rpm < 600, CO2 < 5-8 %). Wiki first: GAS_WIKI §6 has no cranking clause.
