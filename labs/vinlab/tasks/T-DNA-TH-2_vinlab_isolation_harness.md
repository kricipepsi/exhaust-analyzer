# T-DNA-TH-2 — vinlab isolation harness

> **Pack home note:** this row belongs to the DNA-family isolation harness sub-pack
> (`labs/dnalab/tasks/PROGRESS.md`, contract in `labs/dnalab/tasks/DNA_ISOLATION_HARNESS.md`).
> The task file lives under `labs/vinlab/tasks/` because the deliverables are vinlab's;
> the coder still bootstraps via `labs/dnalab/tasks/DNA_TASKS_START_HERE.md`.

### Goal ###

Make every `vinlab` module testable in isolation against **controlled, lab-local
minimal fixtures**, instead of the full packaged `vinlab/data/` dataset and the
external corpus CSVs that today make tests `skip` when absent. vinlab already isolates
*config* via the `decode(vin, *, data_dir=…)` seam and `lookup_engine_ref(db_path, …)`,
and `vref.db` is opened read-only by path — so the harness plugs a **tiny fixture
`data_dir`** into those existing seams. No production change.

Close the two concrete gaps the audit found:
1. **Per-module coverage holes** — `overlay/horizon.py`, `overlay/stress_rpm.py`, and
   `overlay/switches.py` have **no dedicated `test_<module>.py`** (only `air_metering`
   and `cylinder_heuristic` do; `horizon` is partly covered inside `test_overlay.py`).
2. **Production-data coupling** — `tests/conftest.py` reads `vinlab/data/` and external
   `vehicle-data/…/vehicles_petrol_specimens.csv` + `cases/csv/cases_petrol_master_v6.csv`,
   and `skip`s when missing. Isolated module tests must run **without** any of those.

Read `DNA_ISOLATION_HARNESS.md` first.

### Mechanism (owner-approved: test-only doubles, NO production change) ###

Build a **minimal fixture data dir** under `tests/fixtures/mini_data/` containing only
the rows needed to decode a handful of known VINs: tiny `wmi.csv`, `vds_engine_map.csv`,
`years.csv`, and a tiny `vref.db` (SQLite, built by a small fixture-builder script from a
checked-in `.sql` seed, so it is reproducible and reviewable — never a committed binary
blob if avoidable; if a binary `vref.db` must be committed, justify in the gate). Tests
pass it via `decode(vin, data_dir=mini_data)`. `decoder.py`, `overlay/*`, `db/tecdoc_query.py`
are **not** edited.

```
test → make_mini_data_dir(tmp_path)  # writes mini csvs + builds tiny vref.db from seed.sql
     → decode("<known VIN>", data_dir=mini)        # decoder + tecdoc_query exercised, offline
     → overlay funcs called directly with crafted inputs   # horizon/stress_rpm/switches
     → assert exact outputs (each cites SEMANTIC_CONTRACT/wiki §)
```

### Named signal/noise consumer ###

No schema field added — field-consumer rule N/A. Anti-orphan (test variant): the
fixture builders (`make_mini_data_dir`, the overlay input builders) and every fixture
row are consumed by named tests in this diff — `tests/unit/test_horizon.py`,
`test_stress_rpm.py`, `test_switches.py`, and the decoder isolation test that uses the
mini data dir. No fixture or builder ships unconsumed.

### Success criteria ###

- `tests/fixtures/mini_data/` (CREATE): minimal `wmi.csv`, `vds_engine_map.csv`,
  `years.csv`, and a small reproducible `vref.db` (+ its `seed.sql` or builder).
  Sized to decode 2–3 known VINs end-to-end — no more.
- `tests/conftest.py` (MODIFY): add a `mini_data_dir` fixture (and/or
  `make_mini_data_dir(tmp_path)` builder) returning the fixture path; add overlay
  input builders as needed. Keep the existing corpus fixtures (`csv_cases`,
  `sample_vins`) for the *integration* suite, but the new **unit** tests must not
  depend on them.
- New dedicated per-module isolation tests under `tests/unit/`:
  - `test_horizon.py` — `euro_to_horizon` (all 7 EuroEmissionCategory values per
    `SEMANTIC_CONTRACT §6.4`) and `_year_to_horizon`; migrate the matching cases out of
    `test_overlay.py` (move, don't duplicate).
  - `test_stress_rpm.py` — the stress/idle-RPM target logic, each expected value cited.
  - `test_switches.py` — the switch/flag overlay logic, each expected value cited.
  - `test_decode_isolation.py` (EXTEND or add a sibling) — at least one case decoding a
    known VIN through the **mini fixture data dir**, asserting the decode path +
    `tecdoc_query` lookup work with zero packaged-data / external-corpus dependency.
- Slim layout: create `tests/unit/` (+ `__init__.py`); **move** the existing flat test
  files into `tests/unit/` (decoder, models, overlay, air_metering, cylinder_heuristic,
  standalone, contract_conformance, csv_suite, patch_regression, vindna_*). Corpus-
  dependent ones keep their `skip`-if-absent guards; the new isolated unit tests must
  not skip.
- Every numeric literal in new fixtures/tests carries a wiki/contract cite, or a
  `# characterization` marker (DNA-pack §2; contract §"Numeric literals").
- Inner loop clean on every edited file; `pytest tests/` green; the isolated subset
  (`pytest tests/unit -k "not (csv or specimen or integration)"`) passes with the
  external corpus folders absent.

### Files to touch ###

- `labs/vinlab/tests/fixtures/mini_data/…` (CREATE — mini csvs + vref.db + seed)
- `labs/vinlab/tests/fixtures/__init__.py` (CREATE)
- `labs/vinlab/tests/conftest.py` (MODIFY — add `mini_data_dir` + overlay builders)
- `labs/vinlab/tests/unit/__init__.py` (CREATE)
- `labs/vinlab/tests/unit/test_horizon.py` (CREATE)
- `labs/vinlab/tests/unit/test_stress_rpm.py` (CREATE)
- `labs/vinlab/tests/unit/test_switches.py` (CREATE)
- `labs/vinlab/tests/unit/…` (MOVE the existing flat test files in)
- `labs/vinlab/tests/test_overlay.py` (MODIFY — remove the horizon cases migrated out)

### Out of scope ###

Editing `decoder.py`, `overlay/*`, `models.py`, or `db/tecdoc_query.py` (no production
change — if isolation seems to need one, STOP and surface it). dnalab/symptomlab trees
(their own rows). Any schema/field change. Re-deriving decode logic; this is test
scaffolding only. The shared `harness/` engine (not imported).

### Blocked-by ###

— (independent; runnable now).

### On completion ###

Both gates clean in `progress_notes/T-DNA-TH-2.md`; flip T-DNA-TH-2 → `done` in
`labs/dnalab/tasks/PROGRESS.md`. STOP (one task per session).

### Verification ###

```bash
cd $HOME/mnt/4DLab/labs/vinlab
ruff check vinlab/ tests/ && pyright vinlab/ tests/
# isolated module tests must pass with no packaged/external corpus reliance:
pytest tests/unit -q --tb=short -k "horizon or stress_rpm or switches"
pytest tests/unit/test_decode_isolation.py -q --tb=short
pytest tests/ -q --tb=short
# anti-orphan: fixture builders are referenced by tests
grep -rn "mini_data_dir\|make_mini_data_dir" tests/
```
