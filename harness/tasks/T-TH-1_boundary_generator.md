# T-TH-1 — Boundary / edge-point generator

### Goal ###

Build the first generative capability: a boundary/edge-point generator that, for
each dimension of each fault box in a `ModuleDescriptor`, generates six test
points (`min−ε, min, min+ε, max−ε, max, max+ε`) with a geometric box-membership
oracle. Run against the GASLab fork and produce an `.md` report of
classification-vs-geometry agreement.

The generator does **not** use the CSV runner (`run_suite`). It generates points
programmatically, calls `descriptor.entry_point` directly, checks the geometric
oracle, and emits its own `.md` report. This keeps the boundary logic
self-contained — it tests the classifier against the box geometry, not against
hand-authored expected values.

### Success criteria ###

Tests-first. Write failing, then pass:

- `tests/test_boundary.py::test_boundary_generates_six_per_dim_per_box` — for a
  descriptor with N boxes, the generator produces N × 5 × 6 = 30N boundary cases
  (5 gas dimensions × 6 positions each).
- `tests/test_boundary.py::test_boundary_geometric_oracle_correct` — for a known
  box, the inside/outside labels match the geometry: centroid is inside,
  min−ε is outside, min+ε is inside, max+ε is outside.
- `tests/test_boundary.py::test_boundary_gaslab_run` — (requires gaslab)
  generates boundary cases from the GASLab descriptor, runs each through
  `descriptor.entry_point`, checks geometric oracle, and writes the report to
  `harness_tasks/progress_notes/T-TH-1_boundary_report.md`.
- Inner loop clean on every edited file: `ruff` → `pyright` → `pytest -x -q`.

### Context ###

The GASLab descriptor (`descriptor.py`) already exposes 34 fault boxes, each
with 5 gas-dimension `(min, max)` bounds. The boundary generator is the first
consumer of that box table. It varies one dimension at a time while holding
others at the box centroid — the most-definitely-inside point — so boundary
cases are as unambiguous as possible without the overlap analysis (T-TH-2).

**Named signal/noise consumer:** the GASLab fork, via the
`build_gaslab_descriptor()` descriptor. Every boundary case is run through
`descriptor.entry_point(reading, context)` — the live GASLab `process()`
function. No new field, no speculative surface.

**Overlap caveat:** points geometrically inside Box A may also fall inside
Box B (overlap analysis is T-TH-2). The boundary report flags cases where the
classifier disagrees with the geometric oracle; overlap may explain some of
these. The report includes an explicit caveat to this effect.

### Design ###

`BoundaryGenerator` takes a `ModuleDescriptor` and per-dimension epsilon values.
For each box and each of the 5 gas dimensions, it:

1. Computes the centroid of the box (mean of min/max per dimension).
2. For each of 6 positions (`min−ε`, `min`, `min+ε`, `max−ε`, `max`, `max+ε`):
   - Sets the target dimension to the boundary value.
   - Sets the other 4 dimensions to their centroid values.
   - Checks geometric oracle: is the point inside ALL FIVE box dimensions?
   - Builds the full `(GasReading, GasLabContext)` args via
     `descriptor.build_args(row)`.
3. Calls `descriptor.entry_point(*args)` to get the classifier's answer.
4. Compares: `(oracle == "inside") <=> (actual.chemical_state == box.signature)`.

**Epsilon defaults** (per-dimension, configurable):

| Dimension | Type | ε | Rationale |
|---|---|---|---|
| `gas_hc` | int (ppm) | 1 | smallest integer step |
| `gas_co` | float (vol%) | 0.01 | 0.01 vol% is the measurement resolution |
| `gas_co2` | float (vol%) | 0.01 | same |
| `gas_o2` | float (vol%) | 0.01 | same |
| `gas_nox` | int (ppm) | 1 | smallest integer step |

**Computed values:**

| Column | Value |
|---|---|
| `case_id` | `TH-BND-{box_sig}-{dim}-{pos}` (truncated to fit) |
| `description` | `{box_sig}: {dim} at {pos}` |
| `expected_chemical_state` | box signature if inside, blank if outside |
| `expected_error` | blank (all boundary points are structurally valid) |
| `gt_method` | `spec` |
| `gt_source` | box.source citation |

All non-gas columns (ctx_*, dna_*) use the same neutral defaults as the GASLab
descriptor's `build_args` path.

### Isolation (non-negotiable) ###

`harness/generators/boundary.py` imports **no lab**. It operates entirely on
`ModuleDescriptor` objects. The GASLab import stays in `descriptor.py`
(`build_gaslab_descriptor()`), which is the GASLab fork's own tooling.
This preserves "no cross-lab Python imports."

### Deliverables ###

1. `TestSuite/harness/harness/generators/__init__.py` (CREATE) — package init.
2. `TestSuite/harness/harness/generators/boundary.py` (CREATE) —
   `BoundaryGenerator` + `BoundaryCase` + `write_boundary_report()`.
3. `TestSuite/harness/tests/test_boundary.py` (CREATE) — 3 tests.

### Files to touch ###

- CREATE: `harness/generators/__init__.py`
- CREATE: `harness/generators/boundary.py`
- CREATE: `tests/test_boundary.py`
- EDIT: `HARNESS_PROGRESS.md` (ledger row: `_author at start_` → task file path)

### Out of scope ###

- Overlap analysis (T-TH-2). The boundary report may show mismatches caused by
  overlapping boxes; it flags these with the overlap caveat but does not
  resolve them.
- Combinatorial / t-wise generation (T-TH-3).
- Noise / fault-injection sweeps (T-TH-4).
- Non-gas dimensions (ctx_*, dna_*) — these are held at neutral defaults.
  Boundary testing of context-dependent gates (SAI, catalyst, EGR) is deferred
  to a follow-up that can vary those dimensions once the box table expresses
  DNA-gated constraints.

### Verification ###

```bash
cd /sessions/<vm>/mnt/4DLab/TestSuite/harness
ruff check harness/generators/ tests/test_boundary.py
pyright harness/generators/ tests/test_boundary.py
pytest tests/test_boundary.py -x -q --tb=short
```

VERIFICATION GATE + CODE REVIEW blocks must both be clean in
`harness_tasks/progress_notes/T-TH-1.md` before the ledger row flips to `done`.
