# T-DNA-10 — Rename `EngineState` wire value `won_not_start` → `will_not_start` (both ends) + schema bump

**Authored:** 2026-06-12 (architect). **Source:** tri-module audit
`labs/dnalab/docs/audits/AUDIT_2026-06-12_trimodule_dna_vin_symptom.md` §3.2 (S2).
**Owner decision (2026-06-12):** new value = `will_not_start`; **bump** `VehicleDNA.schema_version`.

### Goal ###

`EngineState.WONT_START` ships the awkward wire string `"won_not_start"`. It is **not** a
free typo fix — the value is a JSON-boundary contract string mirrored verbatim in COMLab
(`symptom_router._ENGINE_STATE_NON_STARTER`). Rename it to `"will_not_start"` **on both
ends in one coordinated change**, and bump the envelope `schema_version` because the wire
format changes. This is a clean break: payloads carrying the old value will be rejected by
the existing `VehicleDNA.from_json_payload` version guard (intended — no silent alias).

### Named signal/noise consumer ###

`comlab/comlab/core/symptom_router.py::route_symptom` — the **existing live consumer** of
`engine_state`. It compares the value to `_ENGINE_STATE_NON_STARTER` to set
`suppress_gaslab` / `suppress_obd_live_pids` / `suppress_mode06_ui`. The rename keeps that
exact code path live with the new string; no new field is added.

### Success criteria ###

- `symptomlab/models.py`: `EngineState.WONT_START = "will_not_start"`.
- `comlab/core/symptom_router.py`: `_ENGINE_STATE_NON_STARTER = "will_not_start"` and the
  docstring rule lines updated.
- `comlab/schemas/vocabulary.py`: the 6 reason-doc comments that say `won_not_start` updated
  (the `LabRoutingDirectiveReason` member **names** do not change — comments only).
- `dnalab/models.py`: `SCHEMA_VERSION = "1.2"` (was `"1.1"`).
- Every test asserting the old value or `"1.1"` updated: `symptomlab/tests/unit/test_models.py`,
  `test_validator.py`; `comlab/tests/unit/test_symptom_router.py`;
  `dnalab/tests/unit/test_assembly.py`, `test_models.py` (the `schema_version == "1.1"` and
  `SCHEMA_VERSION == "1.1"` asserts → `"1.2"`).
- `SEMANTIC_CONTRACT.md` §4.2 engine_state vocabulary + §4.3 schema_version updated.
- A whole-repo `grep` for the literal `won_not_start` and `"1.1"` (schema context) returns
  **zero** live hits outside changelog/progress notes, including any JSON fixtures under
  `*/tests/fixtures/`.
- Inner loop clean (`ruff`/`pyright`/`pytest -x -q`) in **symptomlab, comlab, and dnalab**.

### Files to touch ###

- `labs/symptomlab/symptomlab/models.py` (MODIFY — enum value)
- `labs/symptomlab/tests/unit/test_models.py`, `test_validator.py` (MODIFY — asserts/params)
- `labs/comlab/comlab/core/symptom_router.py` (MODIFY — mirror constant + docstring)
- `labs/comlab/comlab/schemas/vocabulary.py` (MODIFY — 6 doc comments only)
- `labs/comlab/tests/unit/test_symptom_router.py` (MODIFY — 4 literal occurrences)
- `labs/dnalab/dnalab/models.py` (MODIFY — `SCHEMA_VERSION` 1.1 → 1.2)
- `labs/dnalab/tests/unit/test_assembly.py`, `test_models.py` (MODIFY — version asserts)
- `SEMANTIC_CONTRACT.md` §4.2/§4.3 (MODIFY — vocabulary + version)

### Out of scope ###

No back-compat alias for the old value (owner chose a clean break + bump). No other
`EngineState` member changes. No symptom-catalog (T-DNA-8) or `oil_consumption` (T-DNA-9) work.

### Verification ###

```bash
cd $HOME/mnt/4DLab/4DLabV2
grep -rIn --include=*.py --include=*.yaml --include=*.json --include=*.md \
  "won_not_start" labs/symptomlab labs/comlab labs/dnalab | grep -vE "progress_notes|audits|won_not_start →"
for L in symptomlab comlab dnalab; do (cd labs/$L && ruff check . && pyright . && pytest tests -x -q); done
```

### On completion ###

Both gates clean in `progress_notes/T-DNA-10.md`; flip the ledger row → `done`. STOP.
This task spans three labs but is **one** coder session (small, mechanical edits).
