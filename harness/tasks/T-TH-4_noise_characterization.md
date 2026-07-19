# T-TH-4 — Noise / fault-injection characterization

### Goal ###

Build a noise / fault-injection characterization capability: starting from each
fault box's centroid (the most-definitely-inside point), apply **seeded** random
perturbation at increasing **amplitude levels**, run each perturbed point through
`descriptor.entry_point`, and measure how the classifier's label **degrades** as
noise grows. Emit an `.md` degradation report — an amplitude-vs-retention curve
per box plus an aggregate curve across all boxes.

This is a **characterization report, not a pass/fail gate** (same posture as the
T-TH-2 overlap analyzer). It measures brittleness to real-world non-ideal
readings — analyzer jitter, sensor drift, sampling noise — which a clean
centroid run never exposes. It does **not** assert a degradation threshold and
must **not** be wired into the inner-loop `pytest` gate as a correctness check;
the only `pytest` cases are structural (generator shape, determinism, report
emission), not "the curve must stay above X%."

Like the boundary generator (T-TH-1), it does **not** use the CSV runner
(`run_suite`). It generates points programmatically, calls
`descriptor.entry_point` directly, and emits its own `.md` report.

### Success criteria ###

Tests-first. Write failing, then pass:

- `tests/test_noise.py::test_noise_generates_expected_count` — for a descriptor
  with N boxes that define all 5 gas dims, with `levels` amplitude steps and
  `samples_per_level` draws, the generator produces
  `N × len(levels) × samples_per_level` perturbed cases (the centroid baseline
  at amplitude 0 is one of the levels, so level 0 yields `samples_per_level`
  identical baseline points — accepted; or document the baseline-dedup choice in
  the test).
- `tests/test_noise.py::test_noise_is_seeded_deterministic` — two runs with the
  same seed produce byte-identical perturbed points and identical per-level
  retention counts; two runs with different seeds differ. Determinism is the
  hard requirement (mirrors the T-TH-2 `random.Random(42)` discipline).
- `tests/test_noise.py::test_noise_amplitude_clamped_to_envelope` — perturbed
  values are clamped to the per-dimension measurement envelope (`_ENVELOPE`
  bounds, surfaced via the descriptor's `FieldRange.min_/max_`); no perturbed
  point has a negative gas value or exceeds the field max.
- `tests/test_noise.py::test_noise_gaslab_run` — (requires gaslab) runs the
  characterizer against the GASLab descriptor (34 boxes), computes the
  amplitude-vs-retention curve, and writes the report to
  `harness_tasks/progress_notes/T-TH-4_noise_report.md`.
- Inner loop clean on every edited file: `ruff` → `pyright` → `pytest -x -q`.

### Context ###

T-TH-1 (boundary) tested the classifier at box edges; T-TH-3 (combinatorial)
tested multi-dimension corners; T-TH-2 (overlap) showed the discrimination
ceiling is structural (100% of the envelope claimed by ≥1 box, 331/561 pairs
overlapping, 21 identical-gas-signature pairs). Noise characterization asks a
different question: **how far can a reading drift from a clean centroid before
the classifier changes its label?** A box whose centroid label collapses under
small noise is brittle in the field; one that holds under large noise has
margin. This is the robustness dimension the geometric tests structurally cannot
see — they test the box *boundaries*, not stability *around the center*.

"Retention" = the fraction of perturbed points at a given amplitude that still
classify as the **baseline label** (the label the unperturbed centroid produced
for that box). Retention is defined against the *observed centroid label*, not
the box signature — because T-TH-2 proved a centroid may already classify as a
different (overlapping) signature. Defining retention against the box signature
would conflate the overlap ceiling (a T-TH-2 finding) with noise brittleness
(this task's finding); anchoring to the observed centroid label isolates the
noise effect. The report states this anchoring explicitly and carries the
**overlap caveat** (a centroid whose observed label ≠ its box signature is noted,
with a pointer to the T-TH-2 report).

**Named signal/noise consumer:** the GASLab fork, via
`build_gaslab_descriptor()`. Every perturbed point is run through
`descriptor.entry_point(reading, context)` — the live GASLab `process()`. No new
field on any contract, no speculative surface; the report consumes the existing
box table and the live classifier only.

### Design ###

`NoiseCharacterizer` takes a `ModuleDescriptor`, a seed (default `42`), an
amplitude `levels` tuple, and `samples_per_level`. It reuses
`boundary.py::GAS_DIMS` and the descriptor's `FieldRange` bounds (no new
envelope constant — single source of truth).

**Perturbation model** (per perturbed point):

1. Start at the box centroid (mean of min/max per gas dim — same centroid math
   as `boundary.py`).
2. Amplitude is expressed as a **fraction of each dimension's box width**
   `(max − min)`, so a single amplitude level means "perturb each dim by up to
   ±a×width." This normalizes across dimensions whose units and ranges differ by
   orders of magnitude (gas_hc ppm vs gas_co vol%). Default
   `levels = (0.0, 0.1, 0.25, 0.5, 1.0)`.
3. Default noise distribution: **uniform** in `[−a×width, +a×width]` per dim
   (bounded, no long tail — matches a "within ±X% of reading" jitter model).
   Gaussian is offered as a configurable alternative (`dist="gaussian"`,
   σ = a×width, drawn from the same seeded RNG) but uniform is the default and
   the one the GASLab report uses; document the choice in the report header.
4. **Clamp** each perturbed value to `[field.min_, field.max_]` from the
   descriptor's `FieldRange` (the measurement envelope). Re-round int dims
   (`gas_hc`, `gas_nox`) to integers via the same `_build_row` int-format path
   the boundary generator uses.

**Retention curve:**

```
for each box with all 5 gas dims:
    baseline_label = entry_point(centroid).chemical_state.value
    for each amplitude a in levels:
        retained = 0
        for s in range(samples_per_level):
            point = clamp(centroid + uniform(-a*width, +a*width) per dim)
            label = entry_point(point).chemical_state.value   # "ERROR:<Type>" on raise
            if label == baseline_label: retained += 1
        retention[box][a] = retained / samples_per_level
aggregate[a] = mean over boxes of retention[box][a]
```

`entry_point` exceptions are caught and recorded as the literal label
`"ERROR:<ExceptionType>"` (same convention as `boundary.py::run`), which never
equals `baseline_label`, so an error counts as non-retained — surfaced, not
swallowed.

**Seeded RNG** for reproducibility: `random.Random(seed)`, threaded through the
whole run so the test can assert determinism. No `Math.random`-style ambient
randomness.

### Report (`.md`) ###

`write_noise_report(report, output_path)` emits, in order:

1. Header: date, seed, distribution, `levels`, `samples_per_level`, box count.
2. **Aggregate degradation curve** — a table `amplitude | mean retention % |
   boxes fully retained | boxes fully collapsed`.
3. **Per-box retention table** — one row per box: baseline label, retention % at
   each amplitude level, and a `brittle?` flag (e.g. retention < 50% at a=0.25).
4. **Brittle-box callout** — boxes that lose the baseline label fastest, with
   their wiki `source` citation, so the architect can see *which* signatures
   have the least field margin.
5. **Overlap caveat** — note that a centroid whose observed baseline label ≠ its
   own box signature is an overlap artifact (point to
   `T-TH-2_overlap_report.md`), not a noise finding; retention is still measured
   against the observed baseline label.

Reports are `.md` only (project rule — never `.docx`/`.pdf`).

### Isolation (non-negotiable) ###

`harness/generators/noise.py` imports **no lab**. It operates entirely on
`ModuleDescriptor` objects and `boundary.py::GAS_DIMS`. The GASLab import stays
in `descriptor.py` (`build_gaslab_descriptor()`), which is the GASLab fork's own
tooling. This preserves "no cross-lab Python imports."

### Deliverables ###

1. `TestSuite/harness/harness/generators/noise.py` (CREATE) —
   `NoiseCase`, `NoiseReport`, `NoiseCharacterizer`, `write_noise_report()`.
2. `TestSuite/harness/tests/test_noise.py` (CREATE) — 4 tests.

### Files to touch ###

- CREATE: `harness/generators/noise.py`
- CREATE: `tests/test_noise.py`
- EDIT: `HARNESS_PROGRESS.md` (ledger row: `_author at start_` → task file path)

### Out of scope ###

- Any pass/fail degradation threshold. This is characterization only; the curve
  is reported, never asserted as a correctness gate. The `pytest` cases test
  generator shape, determinism, clamping, and report emission — not the curve's
  values.
- Resolving brittleness — the report flags brittle boxes; the architect resolves
  them (wiki/box refinement), same division of labour as T-TH-2.
- Non-gas dimensions (`ctx_*`, `dna_*`) — held at the descriptor's neutral
  defaults. Noise injection on DNA-gated context fields is a follow-up once the
  box table expresses those constraints (same deferral as T-TH-1).
- Distributions beyond uniform/Gaussian (e.g. correlated cross-dim noise,
  heavy-tailed). Single-dim independent perturbation only.
- Sensor-specific noise models (per-instrument error curves) — generic
  fraction-of-width perturbation only.

### Verification ###

Run from the harness package root. The sandbox mount has been unreliable
(T-TH-3 ran the gaslab case via the Windows `.venv-wired`); if the
`gaslab`-dependent test cannot import gaslab in the sandbox, run the three
structural tests in the sandbox and have the user run
`test_noise_gaslab_run` via `.venv-wired` in PowerShell, recording both in the
gate note.

```bash
cd "$HOME/mnt/4DLab/TestSuite/harness"
ruff check harness/generators/noise.py tests/test_noise.py
pyright harness/generators/noise.py tests/test_noise.py
pytest tests/test_noise.py -x -q --tb=short
```

PowerShell (gaslab case, if sandbox import fails):

```powershell
cd C:\Users\muto\claude\4DApp\4DLab\TestSuite\harness
..\..\.venv-wired\Scripts\python.exe -m pytest tests/test_noise.py -x -q --tb=short
```

VERIFICATION GATE + CODE REVIEW blocks must both be clean in
`harness_tasks/progress_notes/T-TH-4.md` before the ledger row flips to `done`.
