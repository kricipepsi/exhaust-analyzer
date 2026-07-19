# T-TH-11 — Retarget harness parity gate to the rebuilt fixture; close T-TH-0

### Goal ###

Point the harness parity gate at the clean `fixtures/gaslab_from_master.csv`
(built in T-TH-10), drop the removed `ctx_secondary_air_injection_active` from
the GASLab descriptor, and redefine T-TH-0's "0 mismatches" criterion so it is
meetable and meaningful. This is the task that unblocks and closes T-TH-0.

### Why T-TH-0 is stuck (verified) ###

`GasLabContext` (`GASLab/gaslab/process.py`) is
`dna, engine_state, lambda_measured, block_test_passed, reading_high` — it has
**no `secondary_air_injection_active`**. The old parity source
`gaslab_suite_with_dna.csv` still carries that column and four labels (H-3..H-6)
that current GASLab no longer emits. So "0 mismatches against that CSV" is
unmeetable without rebuilding the answer key — which T-TH-10 does.

### Changes ###

1. `harness/descriptor.py` — remove the `ctx_secondary_air_injection_active`
   `FieldRange` (line ~312) and its use in `build_args` (line ~401). It maps to
   nothing on the current `GasLabContext`; passing it is the original crash.
2. `tests/test_runner.py::test_parity_replays_existing_csv` — repoint
   `csv_path` from `gaslab_suite_with_dna.csv` to
   `harness/fixtures/gaslab_from_master.csv`.
3. **Redefine the gate (this is now a regression gate, not a runner-parity
   gate):** the rebuilt fixture's `expected_chemical_state` is the master's
   human truth, already drift-adjudicated in T-TH-10. The criterion becomes:
   **0 mismatches against the rebuilt GASLab-decidable fixture.** If a mismatch
   appears here it is a real GASLab regression or an un-adjudicated drift row —
   a true failure, not noise.

### Success criteria ###

- `ctx_secondary_air_injection_active` appears nowhere in `harness/`
  (grep returns 0 hits).
- `test_parity_replays_existing_csv` reads the rebuilt fixture and passes with
  **0 mismatches**.
- Full harness suite green (`pytest -x -q`), `ruff` + `pyright` clean.
- `progress_notes/T-TH-0.md` and the `T-TH-0` ledger row updated: status →
  `done`, with the redefined criterion recorded and pointing at T-TH-11.

### Named signal/noise consumer ###

The parity/regression gate itself — the GASLab fork's CI guard. No new schema
field is introduced; this task only removes a dead field and repoints a path.

### Isolation ###

Harness core stays lab-agnostic. No cross-lab imports. No `gaslab/` runtime
change.

### Deliverables ###

1. `TestSuite/harness/harness/descriptor.py` (EDIT — drop dead ctx field).
2. `TestSuite/harness/tests/test_runner.py` (EDIT — repoint + assert 0).
3. `TestSuite/harness/harness_tasks/progress_notes/T-TH-11.md` — gate blocks.
4. Ledger: flip `T-TH-0` → `done`; mark `T-TH-11` → `done`.

### Out of scope ###

No new generators. No master CSV edit. No non-GASLab descriptor. Do not delete
`gaslab_suite_with_dna.csv` (legacy reference) unless the owner asks; just stop
using it as the parity source.

### Verification ###

```bash
# restore sandbox Python 3.14 first
cd /sessions/<vm>/mnt/4DLab/TestSuite/harness
grep -rn "secondary_air_injection_active" harness/   # must be empty
ruff check harness/ tests/
pyright harness/ tests/
pytest tests/ -x -q --tb=short      # parity = 0 mismatches on rebuilt fixture
```

VERIFICATION GATE + CODE REVIEW both clean in
`harness_tasks/progress_notes/T-TH-11.md` before flipping `T-TH-0`/`T-TH-11` to
`done`.
