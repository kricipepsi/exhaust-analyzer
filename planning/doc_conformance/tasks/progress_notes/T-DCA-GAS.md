# T-DCA-GAS — progress note
Audit gaslab's design/contract docs against code.

## Plan
1. Read gaslab Vocabulary: `labs/gaslab/docs/GAS_VOCABULARY.md` vs code `labs/gaslab/gaslab/contracts.py` and `labs/semantic/vocabul/GAS_VOCABULARY.md`.
2. Read gaslab ADRs: `labs/gaslab/docs/ADR_GASLab.md` vs code.
3. Read gaslab HLD and LLD: `labs/gaslab/docs/HLD_GASLab.md` and `labs/gaslab/docs/LLD_GASLab.md` vs code.
4. Classify all claims as MATCH / DRIFT / UNDOCUMENTED / SUPERSEDED / PENDING (+ DUP-DRIFT).
5. Verify seeded case (ChemicalSignature = 34; 0 WRONG_VALVE_TIMING).
6. Write report to `planning/doc_conformance/reports/gaslab__deepseek.md`.
## VERIFICATION GATE — T-DCA-GAS
* Checked all 4 gaslab doc classes (Vocabulary, ADR, HLD, LLD).
* Enutemated and resolved 30 claims against `gaslab/contracts.py`, `gaslab/brettschneider.py`, `gaslab/validity_gates.py`, `gaslab/rule_engine.py`, `gaslab/resolution.py`, and `gaslab/data/gas_lab_ontology.yaml`.
* Seeded case reproduced: `ChemicalSignature` has exactly 34 members, 0 `WRONG_VALVE_TIMING`, and the three `CAM_TIMING_*` states are present.
* `DUP-DRIFT` detected on `labs/semantic/vocabul/GAS_VOCABULARY.md` (which is version 2.0 while gaslab copy is version 2.2).
* Run `pytest` on `labs/gaslab/tests/` to verify code is completely correct and consistent: 208 passed.
* Report written to `planning/doc_conformance/reports/gaslab__deepseek.md`.

## CODE REVIEW — T-DCA-GAS
* Code is clean and matches the LLD/HLD perfectly.
* Import isolation is verified: 0 cross-lab imports.
* Deterministic candidate specificity scoring is correctly implemented in `rule_engine.py`.
