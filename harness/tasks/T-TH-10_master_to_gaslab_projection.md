# T-TH-10 — Master→GASLab fixture: extraction script + filtered projection

### Goal ###

Stop driving GASLab's parity gate from the stale `gaslab_suite_with_dna.csv`
(it still carries `ctx_secondary_air_injection_active`, a field removed from
`GasLabContext`, and four drifted labels H-3..H-6). Instead, **derive** a clean
GASLab fixture from the canonical master corpus
`TestSuite/cases_petrol_master_v6.csv` by projecting to the columns GASLab
consumes and the rows GASLab can decide alone.

The master CSV is **not modified** by this task. It stays the canonical
integration fixture (consumed at the wired seam in T-TH-12).

### Approach (TestProp.md §1, §3–5, adapted) ###

Write `TestSuite/harness/tools/extract_lab_cases.py` (lab-parameterised; GASLab
is the first and only lab built here). It reads the master CSV and emits
`TestSuite/harness/fixtures/gaslab_from_master.csv` with:

1. **Row filter (GASLab-decidable only):** keep a master row iff
   - `expected_top_fault` is a member of `ChemicalSignature`, AND
   - `expected_perception_gap` is `False`.
   Rows whose verdict depends on OBD lambda / DTC presence / fuel-trim
   contradiction are dropped — those belong to COMLab integration (T-TH-12),
   not the GASLab unit gate.
2. **Column projection (GASLab-consumed only):** map master columns →
   `gas_*` (hc,co,co2,o2,nox), `ctx_*` (engine_state, lambda_measured,
   block_test_passed, reading_high from the `*_2500` columns), and `dna_*`
   (from `vin_*`, `bank_config`, `emission_class`, `induction_type`,
   `fuel_type`, etc.). Every mapping is documented in a `# map:` comment naming
   the source master column — no invented columns.
3. **Expected:** `expected_chemical_state = expected_top_fault`;
   `expected_sample_validity` derived from the validity rule. This carries the
   master's human-authored truth into the GASLab fixture (independent oracle),
   it does **not** snapshot current GASLab output.

### Drift adjudication (DECISION STEP — do not silently absorb) ###

After building the fixture, run its rows through current `gaslab.process` and
list every mismatch. For each, classify as exactly one of:
  - **GASLab bug** — current code is wrong; the master label stands → log as a
    new Unplanned follow-up (a real GASLab defect, not a harness concern).
  - **Intended change** — GASLab behaviour deliberately changed (e.g.
    `WRONG_VALVE_TIMING` enum removed, H-5); the **master cell is stale**.
    Record it in `progress_notes/T-TH-10.md`. **Do not edit the master here** —
    master reconciliation is T-TH-12 and needs owner sign-off. If the row is no
    longer GASLab-decidable, drop it from the projection with a cited reason.

This step is where H-3..H-6 get a verdict instead of a shrug.

### Success criteria ###

- `tools/extract_lab_cases.py` runs, emits `fixtures/gaslab_from_master.csv`,
  is deterministic (same input → byte-identical output).
- Every output column traces to a `# map:` source-column comment.
- `tests/test_extract.py::test_projection_is_gaslab_decidable` — no output row
  has `expected_perception_gap=True` ancestry; every `expected_chemical_state`
  is a valid `ChemicalSignature`.
- `tests/test_extract.py::test_projection_deterministic` — re-run is identical.
- The drift table in `progress_notes/T-TH-10.md` accounts for every mismatch
  with a {bug | intended-change} verdict.
- Inner loop clean on every edited file: `ruff` → `pyright` → `pytest -x -q`.

### Named signal/noise consumer ###

`fixtures/gaslab_from_master.csv` is consumed by the harness parity/regression
gate (`tests/test_runner.py::test_parity_replays_existing_csv`, retargeted in
T-TH-11) and by fault-atlas routing checks for GASLab-decidable rows. No field
ships without that consumer.

### Isolation ###

`extract_lab_cases.py` is GASLab-fork tooling and may import `gaslab` for the
adjudication run. The harness core (`descriptor.py`/`runner.py`/`report.py`)
stays lab-agnostic. No cross-lab imports.

### Deliverables ###

1. `TestSuite/harness/tools/extract_lab_cases.py` (CREATE).
2. `TestSuite/harness/fixtures/gaslab_from_master.csv` (GENERATED, committed).
3. `TestSuite/harness/tests/test_extract.py` (CREATE).
4. `TestSuite/harness/harness_tasks/progress_notes/T-TH-10.md` — column map +
   drift adjudication table + gate blocks.

### Out of scope ###

No edit to `cases_petrol_master_v6.csv`. No edit to `gaslab/` runtime. No
retarget of the parity test yet (that is T-TH-11). No projection for any
non-GASLab lab (that is T-TH-13). Off-scope discoveries → Unplanned follow-ups.

### Verification ###

```bash
# restore sandbox Python 3.14 first (4DLab/CLAUDE.md § Sandbox Python)
cd /sessions/<vm>/mnt/4DLab/TestSuite/harness
ruff check tools/ tests/
pyright tools/ tests/
pytest tests/test_extract.py -x -q --tb=short
python3.14 tools/extract_lab_cases.py --lab gaslab   # emits the fixture
```

VERIFICATION GATE + CODE REVIEW both clean in
`harness_tasks/progress_notes/T-TH-10.md` before the ledger row flips to `done`.
