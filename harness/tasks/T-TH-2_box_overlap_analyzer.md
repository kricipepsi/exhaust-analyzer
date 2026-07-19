# T-TH-2 — Box-overlap & coverage-gap analyzer

### Goal ###

Build a static-geometry analyzer that, given a `ModuleDescriptor`'s box table,
computes **pairwise box overlaps** and **coverage gaps** in 5-D gas feature
space, then emits a `.md` report. No code execution — this is pure geometry on
the box definitions, targeting the **discrimination ceiling** that boundary and
noise tests cannot see.

Two outputs:

1. **Overlap matrix** — for every unordered pair of boxes, determine whether
   they intersect in all 5 gas dimensions simultaneously.
   Two boxes overlap iff for each dimension d:
   `max(A.min[d], B.min[d]) <= min(A.max[d], B.max[d])`.
   Intersecting pairs are the *ambiguous* regions where the classifier must
   choose between two (or more) signatures using non-gas evidence
   (engine state, DNA, rule ordering) — or guess.

2. **Coverage-gap estimate** — Monte Carlo sample the measurement envelope
   (the bounding box of all plausible gas values per `_ENVELOPE`) and report:
   what fraction of points fall into **no** fault box; what fraction fall
   into exactly one; what fraction fall into 2+. The no-box fraction is the
   unclassifiable hole — points where no signature claims the reading.

### Success criteria ###

Tests-first. Write failing, then pass:

- `tests/test_overlap.py::test_pairwise_overlap_detects_intersection` — two
  boxes known to intersect in all 5 dims are reported as overlapping.
- `tests/test_overlap.py::test_pairwise_overlap_detects_disjoint` — two boxes
  separated by a gap in one dimension are reported as disjoint.
- `tests/test_overlap.py::test_coverage_gap_sampling` — Monte Carlo sample of
  the measurement envelope reports `no_box_pct + single_box_pct +
  multi_box_pct` summing to ~100%, and the stub envelope (two small boxes in
  a large space) shows a substantial no-box fraction.
- `tests/test_overlap.py::test_gaslab_overlap_run` — (requires gaslab) runs
  the analyzer against the GASLab descriptor (34 boxes), identifies overlapping
  pairs, estimates the coverage gap, and writes the report to
  `harness_tasks/progress_notes/T-TH-2_overlap_report.md`.
- Inner loop clean on every edited file: `ruff` → `pyright` → `pytest -x -q`.

### Context ###

The GASLab descriptor (`descriptor.py`) defines 34 fault boxes, each with 5-D
gas bounds. The boundary generator (T-TH-1) showed 41.9% geometric-oracle match
rate against the live classifier — SAMPLE_INVALID and overlapping boxes are the
leading hypotheses for the 58.1% mismatch. Overlap analysis is the **first
static test of the discrimination ceiling**: if two boxes occupy the same
region, the classifier *cannot* separate them on gas chemistry alone, and every
test that falls in that region will look like a failure regardless of
implementation correctness.

This task is analytical — its output is a **report** (`.md`), not a pass/fail
gate. It surfaces structural problems in the box table itself, which the
architect resolves separately (wiki amendments, box refinement). The analyzer
does not edit box definitions.

**Named signal/noise consumer:** the GASLab fork, via the built fault-box table
in `build_gaslab_descriptor()`. Overlap pairs are reported with their wiki
citations so the COMLab fault-atlas routing can be cross-checked. Coverage gaps
are reported with dimensionality detail so the architect knows *which*
dimensions leave holes.

### Design ###

`OverlapAnalyzer` takes a `ModuleDescriptor` and optionally a set of dimension
names (default: the 5 gas dims from `boundary.py::GAS_DIMS`).

**Overlap detection:**

```
for each unordered pair (box_a, box_b):
    overlap = True
    for each dim d:
        a_lo, a_hi = box_a.dimensions[d]
        b_lo, b_hi = box_b.dimensions[d]
        if max(a_lo, b_lo) > min(a_hi, b_hi):
            overlap = False; break
    if overlap: record (sig_a, sig_b, overlap region per dim)
```

The overlap region per dimension is `(max(a_lo, b_lo), min(a_hi, b_hi))` —
this is the sub-box where both signatures claim the point. The report includes
these intersection bounds so a reader can see *how much* two boxes overlap
(not just *whether*).

**Coverage-gap sampling:**

```
envelope = per-dimension (global_min, global_max) from _ENVELOPE
N = 50_000 random uniform samples in 5-D envelope
for each sample point:
    count = number of boxes that contain it
    tally: no_box, exactly_one, multi_box
report percentages
```

Box containment: a point is inside a box if it is within bounds for all 5 dims.
This is the same geometric oracle used in T-TH-1.

**Edge cases handled:**
- **Identical boxes** (same signature mapped to same bounds, e.g.
  `HIGH_COMBUSTION_TEMP` and `TIMING_OVER_ADVANCED` share identical gas bounds;
  `EGR_STUCK_CLOSED` also shares them). These fully overlap — the report calls
  them out explicitly as "identical-gas-signature" pairs where only non-gas DNA
  evidence can disambiguate.
- **SAMPLE_INVALID** box uses the full envelope bounds → it "overlaps" with
  every other box. The report notes this as expected (it's a validity gate
  pre-empt, not a real fault signature) and optionally excludes it from counts.
- **Envelope-only boxes** (`CAM_TIMING_RETARDED_MAP`, etc.) whose bounds are
  the full measurement envelope are flagged with low information value.
- **Dimension subset**: boxes must define all 5 gas dims to participate in
  geometric overlap. Boxes missing a dimension are skipped with a note.

**Seeded RNG** for reproducible Monte Carlo: `random.Random(42)`.

### Isolation (non-negotiable) ###

`harness/generators/overlap.py` imports **no lab**. It operates entirely on
`ModuleDescriptor` objects. The GASLab import stays in `descriptor.py`
(`build_gaslab_descriptor()`), which is the GASLab fork's own tooling.

### Deliverables ###

1. `TestSuite/harness/harness/generators/overlap.py` (CREATE) —
   `OverlapResult`, `OverlapAnalyzer`, `CoverageGapEstimate`,
   `write_overlap_report()`.
2. `TestSuite/harness/tests/test_overlap.py` (CREATE) — 4 tests.

### Files to touch ###

- CREATE: `harness/generators/overlap.py`
- CREATE: `tests/test_overlap.py`
- EDIT: `HARNESS_PROGRESS.md` (ledger row: `_author at start_` → task file path)

### Out of scope ###

- Running generated points through `descriptor.entry_point` — this is purely
  static geometry; the classifier is not invoked.
- Resolving overlaps — the report flags them; the architect resolves them via
  wiki amendments.
- Non-gas dimensions (ctx_*, dna_*) — these are DNA-gated differentiators, not
  part of the geometric overlap in 5-D gas space. The report notes when two
  boxes with identical gas signatures are differentiated by DNA fields (per the
  box source citations).
- Multi-way overlaps (3+ boxes sharing a region) — the pairwise matrix covers
  this by enumeration; no special higher-order treatment.

### Verification ###

```bash
cd /sessions/<vm>/mnt/4DLab/TestSuite/harness
ruff check harness/generators/overlap.py tests/test_overlap.py
pyright harness/generators/overlap.py tests/test_overlap.py
pytest tests/test_overlap.py -x -q --tb=short
```

VERIFICATION GATE + CODE REVIEW blocks must both be clean in
`harness_tasks/progress_notes/T-TH-2.md` before the ledger row flips to `done`.
