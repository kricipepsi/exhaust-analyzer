# Drift report — DNALab (2026-11-05, T-AUD-11b)

## labs/dnalab/README.md
- [DIVERGENCE] The README says the lab has no cross-lab Python imports, but the assembly imports the sibling labs symptomlab and vinlab. Doc: `labs/dnalab/README.md:8` "no cross-lab Python imports". Code: `labs/dnalab/dnalab/assembly.py:7` "from symptomlab import resolve as _resolve_symptom".
- [DIVERGENCE] The README gives the lab a VIN decode role, but the dnalab package defines no decoder and only calls the vinlab decoder. Doc: `labs/dnalab/README.md:3` "operator-symptom predictiveness + VIN decode". Code: ABSENT (`grep -rn 'def decode' labs/dnalab/dnalab` -> no output, exit 1).

## labs/dnalab/docs/PRD_DNALab.md
- [MODEL] KR2 lists four required triage keys, but the code requires five, with load_state added. Doc: `labs/dnalab/docs/PRD_DNALab.md:86` "Missing triage keys (`tier_1`, `tier_2`, `occurs_during`, `engine_state`)". Code: `labs/dnalab/dnalab/assembly.py:32` "required = (".
- [MODEL] The P0 pre-validation feature lists four required keys, but the code also requires load_state. Doc: `labs/dnalab/docs/PRD_DNALab.md:128` "`engine_state`) checked first". Code: `labs/dnalab/dnalab/assembly.py:30` "load_state) is missing from the triage dict.".
- [DIVERGENCE] The PRD says the composition calls resolve with the whole triage dict, but the code passes five named keys, so any other triage key is dropped. Doc: `labs/dnalab/docs/PRD_DNALab.md:126` "`symptomlab.resolve(**triage)`". Code: `labs/dnalab/dnalab/assembly.py:41` "symptomatic = _resolve_symptom(".

## labs/dnalab/docs/HLD_DNALab.md
- [DIVERGENCE] The architecture diagram forwards the whole triage dict to resolve, but the code forwards five named keys and drops free_text_notes (as HLD section 3 itself says). Doc: `labs/dnalab/docs/HLD_DNALab.md:52` "symptomlab.resolve(**triage)". Code: `labs/dnalab/dnalab/assembly.py:41` "symptomatic = _resolve_symptom(".
- [DIVERGENCE] The HLD says to_json_payload delegates to each model's to_json, but the code calls to_json_payload on each model (to_json returns a JSON string). Doc: `labs/dnalab/docs/HLD_DNALab.md:106` "delegating `vin_dna.to_json()` and". Code: `labs/dnalab/dnalab/models.py:74` "vin_dna.to_json_payload(),".

## labs/dnalab/docs/LLD_DNALab.md
- [DIVERGENCE] The LLD says the nested keys come from each model's to_json, but the code calls to_json_payload on each model. Doc: `labs/dnalab/docs/LLD_DNALab.md:74` "model's `to_json()`". Code: `labs/dnalab/dnalab/models.py:75` "symptom_dna.to_json_payload(),".

## labs/dnalab/docs/DLD_DNALab.md
- [DIVERGENCE] The method table says to_json_payload delegates to vin_dna.to_json and symptom_dna.to_json, but the code calls to_json_payload on both. Doc: `labs/dnalab/docs/DLD_DNALab.md:70` "delegates `vin_dna.to_json()` / `symptom_dna.to_json()`". Code: `labs/dnalab/dnalab/models.py:74` "vin_dna.to_json_payload(),".
- [MODEL] The required-key step lists four keys, but the code requires five, with load_state added. Doc: `labs/dnalab/docs/DLD_DNALab.md:107` "required-key check". Code: `labs/dnalab/dnalab/assembly.py:32` "required = (".
- [MODEL] The Part B step passes four arguments to resolve, but the code also passes load_state. Doc: `labs/dnalab/docs/DLD_DNALab.md:109` "symptomlab.resolve(tier_1, tier_2, occurs_during, engine_state)". Code: `labs/dnalab/dnalab/assembly.py:46` "load_state=triage".

## labs/dnalab/docs/BDD_DNALab.md
No drift detected.

## labs/dnalab/docs/DNA_VOCABULARY.md
No drift detected.

## labs/dnalab/adr/0001-naming-contract.md
No drift detected.
