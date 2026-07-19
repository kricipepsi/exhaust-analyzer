# T-DNA-TH-1 — dnalab assembly isolation harness

### Goal ###

Give `dnalab` its own lab-local test harness so `assembly.build_vehicle_dna` and
`models.VehicleDNA` can be tested **without the real `vinlab.decode` or
`symptomlab.resolve`**. Today `tests/conftest.py` builds its `sample_dna` fixture by
running the whole real pipeline, so any sibling-lab or data-file fault (e.g. the live
17-vs-18 symptom-catalog mismatch) reds every dnalab test. Isolate assembly's own
logic — the required-key guard, the compose step, error propagation, and the
`VehicleDNA` round-trip — behind fakes plugged into the **existing** module seams.

Read `DNA_ISOLATION_HARNESS.md` first — it defines the slim template, the plugin/seam
rule, and the no-production-change constraint that governs this task.

### Mechanism (owner-approved: test-only doubles, NO production change) ###

`assembly.py` already imports its siblings under module-level names
(`_decode_vin = vinlab.decode`, `_resolve_symptom = symptomlab.resolve`). Tests
replace those names with `monkeypatch.setattr("dnalab.assembly._decode_vin", fake)` /
`("dnalab.assembly._resolve_symptom", fake)`. The fakes return directly-constructed
`VinDNA` / `SymptomDNA` instances (the assembly's outputs), so **no** VIN data dir and
**no** symptom YAML are read. `assembly.py` and `models.py` are **not** edited.

```
test → monkeypatch _decode_vin   → make_vin_dna(**overrides)      (no data_dir read)
     → monkeypatch _resolve_symptom → make_symptom_dna(**overrides) (no yaml read)
     → build_vehicle_dna(vin, triage) → assert ONLY assembly logic
```

### Named signal/noise consumer ###

No schema field is added, so the field-consumer rule is N/A. Anti-orphan (test
variant): every builder/fake added is consumed by a named test in this diff —
`make_vin_dna` / `make_symptom_dna` / `fake_decode_*` / `fake_resolve_*` are each read
by the new `tests/unit/test_assembly.py` isolation cases. No helper ships unconsumed.

### Success criteria ###

- New `tests/conftest.py` builders: `make_vin_dna(**overrides)` and
  `make_symptom_dna(**overrides)` that construct valid sibling dataclasses directly
  (sensible defaults; keyword overrides) — **no** call to `decode`/`resolve`, **no**
  data-dir/YAML read. (Constructing a `VinDNA`/`SymptomDNA` is the allowed
  `dnalab → vinlab + symptomlab` import direction.)
- Slim layout per the contract: create `tests/unit/` and `tests/fixtures/` (+ their
  `__init__.py`); **move** the existing flat `test_assembly.py`, `test_models.py`,
  `test_vehicledna_roundtrip.py` into `tests/unit/`. Move, do not rewrite their
  assertions.
- `tests/unit/test_assembly.py` covers, with both siblings faked via monkeypatch:
  - happy path composes a `VehicleDNA` from the two fakes (asserts the fakes' fields
    flow through, not real-decode values);
  - the missing-triage-key guard raises `SymptomValidationError` **before** `resolve`
    is reached (assert the fake resolve was **not** called);
  - error propagation: a fake `_decode_vin` that raises `VINDecodeError` propagates;
    a fake `_resolve_symptom` that raises `SymptomValidationError` propagates;
  - `session_id` / `timestamp` shape from `VehicleDNA.new` (already covered — keep).
- Keep **one** thin end-to-end test that still runs the real pipeline (rename clearly,
  e.g. `tests/unit/test_assembly_integration.py` or a `@pytest.mark.integration`), so
  the real-wiring contract is not lost — but it is no longer the only coverage and no
  longer the default fixture. It may `skip` if sibling data is unavailable; the
  isolated tests must **never** skip.
- `tests/unit/test_models.py` round-trips a full `VehicleDNA` built from the fakes
  (`to_json_payload`/`from_json_payload`, `SCHEMA_VERSION` mismatch path) with no
  pipeline run.
- Inner loop clean on every edited file; full `pytest tests/` green; isolated cases
  pass even if `symptomlab/data/allowed_combinations.yaml` is in its known-broken state
  (prove this in the gate — it is the whole point).

### Files to touch ###

- `labs/dnalab/tests/conftest.py` (MODIFY — add `make_vin_dna`/`make_symptom_dna`
  builders + fake-callable helpers; keep `sample_vin`/`sample_triage`; demote the
  real-pipeline `sample_dna` to the integration test only)
- `labs/dnalab/tests/unit/__init__.py` (CREATE)
- `labs/dnalab/tests/fixtures/__init__.py` (CREATE)
- `labs/dnalab/tests/unit/test_assembly.py` (MOVE from flat + ADD isolated cases)
- `labs/dnalab/tests/unit/test_models.py` (MOVE from flat)
- `labs/dnalab/tests/unit/test_vehicledna_roundtrip.py` (MOVE from flat)
- `labs/dnalab/tests/unit/test_assembly_integration.py` (CREATE — the one real-pipeline test)

### Out of scope ###

Editing `assembly.py` or `models.py` (no DI seam, no new params — if isolation seems
to require it, STOP and surface it). vinlab/symptomlab test trees (their own TH rows).
Any schema/field/vocabulary change. The shared `harness/` engine (not imported here).

### Blocked-by ###

— (independent; runnable now).

### On completion ###

Both gates clean in `progress_notes/T-DNA-TH-1.md`; flip T-DNA-TH-1 → `done` in
`PROGRESS.md`. STOP (one task per session).

### Verification ###

```bash
cd $HOME/mnt/4DLab/labs/dnalab
ruff check dnalab/ tests/ && pyright dnalab/ tests/
# isolated tests must pass with the real symptom catalog deliberately unavailable:
pytest tests/unit/ -x -q --tb=short -k "not integration"
pytest tests/ -q --tb=short
# anti-orphan: every builder/fake is referenced by a test
grep -rn "make_vin_dna\|make_symptom_dna\|fake_decode\|fake_resolve" tests/unit/
```
