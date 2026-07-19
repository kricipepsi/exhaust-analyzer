# T-DNA-7 — Bump `VehicleDNA` schema_version + round-trip new fields

### Goal ###

After the field-adding tasks land, raise the umbrella `VehicleDNA` schema version
once and make sure the composition round-trips every new field cleanly. This is the
single coordinating task that closes the schema migration; it runs **last**.

`dnalab/models.py` pins `SCHEMA_VERSION = "1.0"` and `from_json_payload` raises on any
mismatch — so the moment SymptomDNA (load_state) or VinDNA (rated_rpm, CoC, fuel_type)
change shape, the version must move in lockstep or deserialization breaks.

### Named signal/noise consumer ###

COMLab `OrchestratorInboundRequest.vehicle_dna` ingestion (the `VehicleDNA` JSON is the
contract surface COMLab consumes). The version bump is what lets COMLab distinguish a
v1.1 payload (new fields present) from a legacy v1.0 one.

### Success criteria ###

- `SCHEMA_VERSION` bumped `1.0` → `1.1`; `from_json_payload` accepts `1.1` and gives a
  clear error on a true mismatch.
- `to_json_payload()` / `from_json_payload()` round-trip all landed new fields:
  `load_state` (via `symptom_dna`), and `rated_rpm` / any formalized CoC paths /
  `fuel_type` if landed (via `vin_dna`). Delegation to each model's `to_json`/`from_json`
  stays intact.
- `assembly.build_vehicle_dna()` passes `load_state` from the `triage` dict to
  `symptomlab.resolve()` (extend `required` keys + the call), matching T-DNA-2's
  validator signature.
- A legacy v1.0 payload path: decide and test (reject with a clear message, or
  upgrade-on-read) — documented in the progress note.
- `tests/` (dnalab): round-trip test covering a full v1.1 `VehicleDNA` with the new
  fields; assembly test covering `load_state` pass-through.
- Draft `SEMANTIC_CONTRACT.md` §4.3 note (schema_version 1.1) — flagged for COMLab.
- Inner loop clean on every edited file.

### Files to touch ###

- `labs/dnalab/dnalab/models.py` (MODIFY — `SCHEMA_VERSION`, round-trip)
- `labs/dnalab/dnalab/assembly.py` (MODIFY — `load_state` pass-through)
- `labs/dnalab/tests/` (MODIFY/CREATE — round-trip + assembly tests)

### Out of scope ###

Re-deciding any field shape (locked by T-DNA-1..6). COMLab ingestion code. Adding
fields not already landed by an earlier task — if T-DNA-6 stayed proposal-only,
`fuel_type` is **not** in scope here.

### Blocked-by ###

T-DNA-1, T-DNA-2, T-DNA-3, T-DNA-4, T-DNA-6. Run only once its upstreams are `done`;
include only the fields those tasks actually landed.

### On completion ###

Both gates clean in `progress_notes/T-DNA-7.md`; flip T-DNA-7 → `done`. This closes the
DNA-family pack. STOP.

### Verification ###

```bash
cd $HOME/mnt/4DLab/labs/dnalab
ruff check dnalab/ && pyright dnalab/
python3.14 -c "from dnalab.models import SCHEMA_VERSION; print('version', SCHEMA_VERSION)"
pytest tests/ -x -q --tb=short
```
