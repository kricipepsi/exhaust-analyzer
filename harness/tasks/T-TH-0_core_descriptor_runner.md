# T-TH-0 — Harness core: ModuleDescriptor + generic runner + report emitter

### Goal ###

Stand up the lab-agnostic harness skeleton under `TestSuite/harness/` and prove
it against the **built GASLab fork** with zero behaviour change. No generators
yet — this task delivers the plug and a parity proof, so every later generator
(T-TH-1..7) has a foundation with a real, named consumer.

Three pieces (`HARNESS_PROPOSAL.md §3`):
1. `descriptor.py` — `ModuleDescriptor`: per-field plausible ranges, the
   fault-box table `{signature: {dim: (min, max)}}`, the entry-point callable,
   and the oracle hook (`spec` = box membership; `characterization` = recorded
   run). Plus a concrete **GASLab descriptor** built from `gaslab/contracts.py` +
   the `ChemicalSignature` box table.
2. `runner.py` — generic *generate → invoke entry point → diff vs oracle →
   collect*, reusing the existing per-module runner's `gt_method`/`gt_source`
   governance columns so generated cases are first-class.
3. `report.py` — `.md` emitter (project rule: reports are `.md`).

### Success criteria ###

Tests-first. Write failing, then pass:

- `tests/test_descriptor.py::test_gaslab_descriptor_loads` — the GASLab
  `ModuleDescriptor` loads, exposes one box per `ChemicalSignature` member, and
  every box dimension has a `(min, max)` with `min <= max`.
- `tests/test_runner.py::test_parity_replays_existing_csv` — **the parity
  gate.** Driving the existing `gaslab_suite_with_dna.csv` rows through the
  descriptor + runner reproduces the current runner's verdicts with **0
  mismatches**. The harness must not change a single existing classification.
- `tests/test_report.py::test_report_is_markdown` — the emitter writes valid
  `.md` (no `.docx`/`.pdf`), with a header row count matching cases run.
- Inner loop clean on every edited file: `ruff` → `pyright` → `pytest -x -q`.

### Context ###

The fork model (`PER_MODULE_TESTSUITE_DESIGN_SPEC.md`) already gives each lab a
suite bound to its own input schema; GASLab's is built (T-GAS-5..15, T-CUR-1).
Those suites are hand-authored CSVs + a thin diff runner. This task adds the
descriptor abstraction the *generative* capabilities will consume — but ships it
behind a parity gate so it is provably a no-op refactor on day one.

**Named signal/noise consumer:** the GASLab fork (`gaslab_suite_runner.py` +
`gaslab_suite_with_dna.csv`). The descriptor's only job in T-TH-0 is to re-drive
that existing, consumed suite. No new field, no new output, no speculative
surface — the parity gate is the proof.

**H-1 (resolve here):** the GASLab fault-box table is currently spread across
`GAS_VOCABULARY` + per-signature wiki pages. Define the single artefact the
descriptor reads boxes from (extract once into a descriptor input), and **cite
each box's source** per `gaslab-wiki-provenance`. Do not invent bounds.

### Isolation (non-negotiable) ###

`TestSuite/harness/` imports **no lab**. The GASLab descriptor module may import
GASLab (it is the GASLab fork's own tooling), but `descriptor.py` / `runner.py` /
`report.py` core stay lab-agnostic — they receive a `ModuleDescriptor`, never an
import. This preserves "no cross-lab Python imports".

### Deliverables ###

1. `TestSuite/harness/harness/descriptor.py` — `ModuleDescriptor` + GASLab
   descriptor builder (cite box sources).
2. `TestSuite/harness/harness/runner.py` — generic runner.
3. `TestSuite/harness/harness/report.py` — `.md` emitter.
4. `TestSuite/harness/tests/test_descriptor.py` (CREATE).
5. `TestSuite/harness/tests/test_runner.py` (CREATE — parity gate).
6. `TestSuite/harness/tests/test_report.py` (CREATE).

### Out of scope ###

No generators (boundary/combinatorial/noise/overlap/metamorphic/fuzz/regression
— those are T-TH-1..7). No descriptor for any non-GASLab lab (T-TH-8). No change
to `gaslab/` runtime, the existing GASLab CSVs, or `gaslab_suite_runner.py`. No
new schema field. Surgical-change rule: every changed line traces to a
Deliverable; adjacent issues → `HARNESS_PROGRESS.md` "Unplanned follow-ups".

### Verification ###

```bash
# restore sandbox Python 3.14 first (4DLab/CLAUDE.md § Sandbox Python)
cd /sessions/<vm>/mnt/4DLab/TestSuite/harness   # or C:\...\TestSuite\harness on Windows
ruff check harness/ tests/
pyright harness/ tests/
pytest tests/ -x -q --tb=short          # parity gate must show 0 mismatches
```

VERIFICATION GATE + CODE REVIEW blocks must both be clean in
`harness_tasks/progress_notes/T-TH-0.md` before the ledger row flips to `done`.
