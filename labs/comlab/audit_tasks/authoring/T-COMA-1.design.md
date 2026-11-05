# T-COMA-1 design input (Windows Cowork, 2026-11-05 23:20 CET) — F-C1-7, with the T-AUD-4e residual

Measured on `fix/T-AUD-11h` (`2e07e9c`) with Cowork's scripts in `C:/4DApp/recheck/T-AUD-4e1/` (read-only on the clone).

## Facts
1. **The gas reading decides every non-starter verdict; the symptom does not.** `gas_invariance.py non_starter
   fast_crank_whining no_crank_silent prolonged_crank_hard_start` (UI shape: `csv_primary_symptom=non_starter`,
   `engine_state=will_not_start`): idle-stoich gas → `ecu_fault` EF-004, rich → `catalyst_failure` CF-001, lean →
   `misfire` MF-001, for all three tier_2 values. The symptom prior is applied to the non_starter family but never wins.
2. **No non-starter reaches the `non_starter` family today**, even with a cranking-style sample (`cranking.py`: CO₂ 2-6 %,
   O₂ 10-18 %): `misfire` MF-001 for lean, rich and incomplete samples.
3. **Excluding suppressed gas at the shim** (`rehearse.py`: `_build_sanitized_payload` sets `gas_lab_output=None` when
   `directive.suppress_gaslab`): the non-starter verdict becomes gas-invariant (`misfire` MF-005 for all 9 probes), all
   309 running corpus cases are unchanged, and the 5 `will_not_start` corpus cases move to `sensor_fault` SF-001/SF-002
   (`rehearse.out`). MF-005 and SF-00x are not non-starter verdicts either.
4. **The two design sources conflict.** Wiki `07_pipeline_stages.md` §RULE_LAB_SUPPRESSION: `will_not_start`
   suppresses GASLab, OBD and Mode $06, and "excludes its data from the matrix". Registry
   `labs/comlab/registry/rules/non_starter.json`: NS-001/002/003 are GATED on chemistry states (LEAN_MISFIRE,
   RICH_MISFIRE, INCOMPLETE_COMBUSTION) with cranking evidence (rpm < 600, CO₂ < 5-8 %); only NS-004 is DTC-gated
   (P0230, P0087, P0190). Wiki `06_fault_atlas_families.md` §CONCEPT_FAM_NONSTART: decided from Mode $06 + freeze-frame
   cut-state (`_no_start_branch`, which abstains without them).
5. `gas_lab_output` is mandatory in `OrchestratorInboundRequest` (`ingestion.py:562`), and the composition aborts a
   non-starter without gas with `GAS_INPUT_INCOMPLETE` "not available yet" (`composition.py:265-270`, T-AUD-1a R4).

## The ruling the row needs (Cowork, before authoring)
- **A (wiki literal):** exclude gas and OBD for `will_not_start`; verdict from DTC (NS-004), the no-start branch, or an
  abstain. Lost: NS-001..003 become unreachable (cranking chemistry is real evidence).
- **B (family gate):** keep gas (optional) for non-starters, but restrict candidates to the `non_starter` family; no NS
  rule scores → abstain (`DiagnosticVerdict.abstained`). Lost: the wiki line; it must be amended in the same row.
- Either way: gas becomes optional for a non-starter (the T-AUD-4e residual), running cases stay byte-identical
  (309/309), and idle-gas families (EF, CF, MF, RM, LC) can no longer win a non-starter session.

## Gates the spec should pin
- Probe: for every non-start tier_2 and every gas sample (and no gas), the verdict family is `non_starter` or abstained.
- Corpus: 309 running cases unchanged; the 5 `will_not_start` cases listed with their new verdicts.
- `test_t_aud_1a_inputs.py::test_r4_non_starter_without_gas_aborts_with_message` changes meaning (R4 of T-AUD-1a):
  the spec names it as a test the row rewrites.
