# Drift report — SymptomLab (2026-11-05, T-AUD-11a)

## labs/symptomlab/README.md
No drift detected.

## labs/symptomlab/docs/PRD_SymptomLab.md
- [MODEL] The documented entry-point signature omits the free_text_notes and allowed_path keyword arguments that resolve() takes. Doc: `labs/symptomlab/docs/PRD_SymptomLab.md:30` "symptomlab.resolve(tier_1, tier_2, *, occurs_during, engine_state, load_state)". Code: `labs/symptomlab/symptomlab/__init__.py:26` "allowed_path: Path | None = None,".
- [DIVERGENCE] The PRD names Python 3.14 as the technology, but the lab package declares support for Python 3.11 and later. Doc: `labs/symptomlab/docs/PRD_SymptomLab.md:149` "Python 3.14 + PyYAML". Code: `labs/symptomlab/pyproject.toml:8` "requires-python".
- [HARDCODED] KR4 says the vocabulary is open and adding a symptom needs no code change, but the validator hard-codes a catalog size of 21, so any added pair fails at construction until the code changes. Doc: `labs/symptomlab/docs/PRD_SymptomLab.md:98` "Tier vocabulary is open (YAML-driven)". Code: `labs/symptomlab/symptomlab/validator.py:36` "if len(self._allowed) != 21:".
- [DIVERGENCE] The PRD lists the oil_consumption symptom as deferred and not in the schema, but the live catalog already ships it as the seventh tier_1. Doc: `labs/symptomlab/docs/PRD_SymptomLab.md:203` "Not in the current schema.". Code: `labs/symptomlab/symptomlab/data/allowed_combinations.yaml:33` "oil_consumption:".

## labs/symptomlab/docs/HLD_SymptomLab.md
- [DIVERGENCE] The HLD shows DNALab assembly as the only caller of resolve(), but apps/wired composition also calls it directly. Doc: `labs/symptomlab/docs/HLD_SymptomLab.md:50` "DNALab assembly.build_vehicle_dna". Code: `apps/wired/wired/composition.py:227` "symptom = resolve_symptom(**{key: triage[key] for key in _TRIAGE_KEYS})".
- [DIVERGENCE] The known-gaps table says oil_consumption is deferred and not in this schema, while the HLD section 4 table and the live catalog both include it. Doc: `labs/symptomlab/docs/HLD_SymptomLab.md:190` "not in this schema". Code: `labs/symptomlab/symptomlab/data/allowed_combinations.yaml:33` "oil_consumption:".

## labs/symptomlab/docs/LLD_SymptomLab.md
- [MODEL] The LLD says to_json() returns a dict, but the code returns a JSON string and the dict comes from to_json_payload(). Doc: `labs/symptomlab/docs/LLD_SymptomLab.md:104` "EnvironmentalConditions.to_json()". Code: `labs/symptomlab/symptomlab/models.py:44` "def to_json(self) -> str:".

## labs/symptomlab/docs/DLD_SymptomLab.md
- [MODEL] The DLD says to_json() returns a dict, but the code returns a JSON string and the dict comes from to_json_payload(). Doc: `labs/symptomlab/docs/DLD_SymptomLab.md:78` "to_json() →". Code: `labs/symptomlab/symptomlab/models.py:44` "def to_json(self) -> str:".
- [UNDOCUMENTED] from_json also rejects a payload or environmental_conditions that is not an object, a structural check the DLD does not describe. Doc: `labs/symptomlab/docs/DLD_SymptomLab.md:92` "Validates **enum membership**". Code: `labs/symptomlab/symptomlab/models.py:93` "if not isinstance(payload, dict):".
- [UNDOCUMENTED] validate() first rejects a non-string tier_1 or tier_2 with SymptomValidationError, a step the DLD list of validate steps omits. Doc: `labs/symptomlab/docs/DLD_SymptomLab.md:124` "not allowed". Code: `labs/symptomlab/symptomlab/validator.py:67` "if not isinstance(tier_1, str) or not isinstance(tier_2, str):".
- [DIVERGENCE] The DLD test-coverage table names test files directly under tests/, but the tests live under tests/unit/. Doc: `labs/symptomlab/docs/DLD_SymptomLab.md:174` "tests/test_models.py". Code: ABSENT (`ls labs/symptomlab/tests/test_models.py` -> ls: cannot access labs/symptomlab/tests/test_models.py: No such file or directory).

## labs/symptomlab/docs/BDD_SymptomLab.md
- [DIVERGENCE] The BDD maps scenarios to tests/test_models.py, but the tests live under tests/unit/. Doc: `labs/symptomlab/docs/BDD_SymptomLab.md:32` "tests/test_models.py". Code: ABSENT (`ls labs/symptomlab/tests/test_models.py` -> ls: cannot access labs/symptomlab/tests/test_models.py: No such file or directory).

## labs/symptomlab/docs/SYMPTOM_VOCABULARY.md
No drift detected.

## labs/symptomlab/graph/v2_docs/ingest_ready/ADR_SymptomLab/02_ADR-0002_Tier_vocabulary_is_open_YAML-validated_not_a_hard-coded_enum.md
- [HARDCODED] The ADR says adding or renaming a symptom is a data edit with no code change, but the validator hard-codes a catalog size of 21. Doc: `labs/symptomlab/graph/v2_docs/ingest_ready/ADR_SymptomLab/02_ADR-0002_Tier_vocabulary_is_open_YAML-validated_not_a_hard-coded_enum.md:15` "Adding or renaming a symptom is a data". Code: `labs/symptomlab/symptomlab/validator.py:36` "if len(self._allowed) != 21:".
