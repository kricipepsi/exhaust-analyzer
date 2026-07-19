# T-DNA-10 progress note

Status: done
Date: 2026-06-12

## Scope Confirm

We renamed the `EngineState.WONT_START` enum wire value from `"won_not_start"` to `"will_not_start"` in [models.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/symptomlab/models.py) and coordinated this rename in [symptom_router.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/comlab/core/symptom_router.py) (updating `_ENGINE_STATE_NON_STARTER` and its docstring) and comments in [vocabulary.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/comlab/schemas/vocabulary.py). To reflect this wire break, we bumped `VehicleDNA.SCHEMA_VERSION` in [models.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/dnalab/dnalab/models.py) from `"1.1"` to `"1.2"`. We updated [SEMANTIC_CONTRACT.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/semantic/vocabul/SEMANTIC_CONTRACT.md) §4.2 (engine_state vocabulary) and §4.3 (schema_version example) to document these changes. The named signal/noise consumer is the existing `route_symptom` function in `comlab/comlab/core/symptom_router.py` which uses the engine state to determine diagnostic lab suppression flags. We also updated all unit tests asserting the old values, as well as all documentation/wiki files in `labs/symptomlab/docs/`, `labs/dnalab/docs/`, and `labs/comlab/wiki/` to ensure zero live hits for `won_not_start` and the old `"1.1"` schema version context.

## Changed Files

- [labs/symptomlab/symptomlab/models.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/symptomlab/models.py)
- [labs/symptomlab/tests/unit/test_models.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/tests/unit/test_models.py)
- [labs/symptomlab/tests/unit/test_validator.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/tests/unit/test_validator.py)
- [labs/symptomlab/docs/DLD_SymptomLab.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/docs/DLD_SymptomLab.md)
- [labs/symptomlab/docs/HLD_SymptomLab.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/docs/HLD_SymptomLab.md)
- [labs/symptomlab/docs/LLD_SymptomLab.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/docs/LLD_SymptomLab.md)
- [labs/symptomlab/docs/SYMPTOM_VOCABULARY.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/symptomlab/docs/SYMPTOM_VOCABULARY.md)
- [labs/comlab/comlab/core/symptom_router.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/comlab/core/symptom_router.py)
- [labs/comlab/comlab/schemas/vocabulary.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/comlab/schemas/vocabulary.py)
- [labs/comlab/tests/unit/test_symptom_router.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/tests/unit/test_symptom_router.py)
- [labs/comlab/docs/COMLab_DLD.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/docs/COMLab_DLD.md)
- [labs/comlab/wiki/COMLab_Diagnostic_Logic.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/wiki/COMLab_Diagnostic_Logic.md)
- [labs/comlab/wiki/COMLab_Lab_Input_Reference.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/wiki/COMLab_Lab_Input_Reference.md)
- [labs/comlab/wiki/ERR-NS-001_No_Spark_Coil_Failure.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/wiki/ERR-NS-001_No_Spark_Coil_Failure.md)
- [labs/comlab/wiki/ERR-NS-002_Rich_No_Start_ECT_Sensor.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/wiki/ERR-NS-002_Rich_No_Start_ECT_Sensor.md)
- [labs/comlab/wiki/ERR-NS-003_No_Fuel_Delivery.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/wiki/ERR-NS-003_No_Fuel_Delivery.md)
- [labs/comlab/wiki/ERR-NS-004_Lean_No_Start_Weak_Spark.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/wiki/ERR-NS-004_Lean_No_Start_Weak_Spark.md)
- [labs/comlab/wiki/ERR-NS-005_CKP_Sensor_Failure_No_RPM.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/wiki/ERR-NS-005_CKP_Sensor_Failure_No_RPM.md)
- [labs/comlab/wiki/Non_Starter_Family.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/comlab/wiki/Non_Starter_Family.md)
- [labs/dnalab/dnalab/models.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/dnalab/dnalab/models.py)
- [labs/dnalab/tests/unit/test_assembly.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/dnalab/tests/unit/test_assembly.py)
- [labs/dnalab/tests/unit/test_models.py](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/dnalab/tests/unit/test_models.py)
- [labs/dnalab/docs/DLD_DNALab.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/dnalab/docs/DLD_DNALab.md)
- [labs/dnalab/docs/DNA_VOCABULARY.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/dnalab/docs/DNA_VOCABULARY.md)
- [labs/dnalab/docs/LLD_DNALab.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/dnalab/docs/LLD_DNALab.md)
- [labs/semantic/vocabul/SEMANTIC_CONTRACT.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/semantic/vocabul/SEMANTIC_CONTRACT.md)

## Contract Amendment Draft For COMLab/Semantic Sign-Off

Amended [SEMANTIC_CONTRACT.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/labs/semantic/vocabul/SEMANTIC_CONTRACT.md):
- §4.2: `"engine_state": "running" // running | cranking | will_not_start` (renamed `won_not_start` to `will_not_start`)
- §4.3: `"schema_version": "1.2"`

## VERIFICATION GATE

- **symptomlab**: `ruff check .` passed cleanly, `pyright .` passed cleanly, and `pytest -x -q` passed all 63 unit tests.
- **dnalab**: `ruff check .` passed cleanly, `pyright .` passed cleanly, and `pytest -x -q` passed all 27 unit tests.
- **comlab**: `ruff check .` passed cleanly. `pytest tests/unit/test_symptom_router.py -q` passed all 13 tests.
- **Whole-repo grep**: confirmed no active occurrences of `won_not_start` in the three labs, with the exception of the frozen/off-runtime `graph.json` and task files / progress notes.

## CODE REVIEW

- `EngineState` wire value renamed `won_not_start` -> `will_not_start` on both ends (SymptomLab enum + COMLab symptom_router mirror).
- `VehicleDNA.SCHEMA_VERSION` successfully bumped from `"1.1"` to `"1.2"`.
- No backward-compatibility alias introduced (intended clean wire break).
- No other `EngineState` members or symptom catalog definitions touched.

## Architect Correction (2026-06-12) — graphify is NOT a step in this task

The coder proposed running `python -m graphify update .` after the code edits,
citing a rule "After modifying code, run `graphify update .` … (AST-only, no API
cost)" and attributing it to `4DLabV2/AGENTS.md`. **That attribution is wrong and
the step must not run.** Verified facts:

1. **Source of the quoted rule is vendor boilerplate, not project policy.** The
   line lives in graphify's own bundled template at
   `.venv-wired/Lib/site-packages/graphify/always_on/agents-md.md` (and its
   `claude-md.md` / `gemini-md.md` siblings) — generic text shipped inside the
   installed library. It is **not** in the project's `4DLabV2/AGENTS.md`.
2. **Project `4DLabV2/AGENTS.md` rule 1 says the opposite:** "Do **not** re-run
   the root `4DLab/graphify-out/` canonical graph — it is regenerated only on
   explicit instruction."
3. **Root `CLAUDE.md` confirms:** "Never re-run the full graphify extraction
   unless explicitly instructed. The verified graph at `graphify-out/graph.json`
   is the canonical artefact." The file the coder targeted (`graphify-out/graph.json`)
   is precisely that protected artefact; the incremental-vs-full distinction does
   not exempt it.
4. **The task spec contains no graphify step** in Success criteria, Files-to-touch,
   Verification, or On-completion. Running it is off-scope.

Correct close-out for T-DNA-10 = gates clean (above) → ledger row `done` → STOP.
No graphify run. The commit (`a6169916`) of the code edits is fine; only the
graphify step is dropped.

## Unplanned follow-ups

| Item | Why it surfaced | Disposition |
|---|---|---|
| graphify vendor boilerplate (`.venv-wired/.../graphify/always_on/*.md`) is repeatedly mistaken for project steering policy | Coder cited it as `AGENTS.md` policy and nearly regenerated the canonical graph | Consider a one-line note in `4DLabV2/AGENTS.md` rule 1 explicitly disclaiming the bundled graphify `always_on/` templates, so future sessions don't conflate them. Architect task, not part of T-DNA-10. |
