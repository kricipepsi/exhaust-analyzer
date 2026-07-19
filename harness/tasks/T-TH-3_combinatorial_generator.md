# T-TH-3 — t-wise (pairwise) combinatorial corner generator

### Goal ###

Build the third generative capability: a **pairwise (2-wise) combinatorial corner
generator** that, for each fault box in a `ModuleDescriptor`, takes every pair of
the box's gas dimensions and places that pair at their four `{min, max}` corners
while holding the other dimensions at the box centroid. Each generated point
carries a geometric box-membership oracle. Run against the GASLab fork and
produce an `.md` report of classification-vs-geometry agreement.

This catches **multi-dimension interaction bugs** that the per-axis boundary
sweep (T-TH-1) structurally cannot: T-TH-1 moves one dimension at a time with
every other dimension at centroid, so a defect that only fires when two
thresholds are crossed *together* (e.g. a collision rule keyed on `co` AND `o2`
simultaneously) is invisible to it. Pairwise corners exercise exactly those
2-dimension boundary interactions.

Like T-TH-1, the generator does **not** use the CSV runner (`run_suite`). It
generates points programmatically, calls `descriptor.entry_point` directly,
checks the geometric oracle, and emits its own `.md` report.

### Why pairwise, not full-grid ###

The full corner grid of a 5-dimension box is `2^5 = 32` corners per box; with all
dimensions free that is the combinatorial explosion the proposal (`§4`) flags.
**Pairwise (t=2)** coverage holds `t`=2 dimensions at their corners and the rest
at centroid: `C(5,2) = 10` dimension-pairs × `2^2 = 4` corners = **40 points per
box**, a fixed, bounded count that still exercises every 2-dimension corner
interaction at least once. This is the standard t-wise reduction: most
interaction bugs are low-order (pairwise), so pairwise coverage finds them
without paying for the full grid. Higher t (3-wise+) and full-grid are explicitly
out of scope.

### Success criteria ###

Tests-first. Write failing, then pass:

- `tests/test_combinatorial.py::test_pairwise_count_per_box` — for a descriptor
  with N boxes each defining all 5 gas dims, the generator produces
  `N × C(5,2) × 4 = 40N` cases (10 dim-pairs × 4 corners each).
- `tests/test_combinatorial.py::test_pairwise_corners_cover_all_combos` — for a
  single dim-pair, the four generated points are exactly the `{min,max}×{min,max}`
  corner set; the non-paired dimensions sit at the box centroid.
- `tests/test_combinatorial.py::test_combinatorial_geometric_oracle_inside` —
  for a box, all pairwise corner points are geometrically **inside** (corners of
  a box are on its boundary, which the closed-interval oracle counts as inside);
  oracle = "inside" for every generated case on a well-formed box.
- `tests/test_combinatorial.py::test_combinatorial_run_with_stub` — `run()`
  executes every case through `descriptor.entry_point`, compares predicted
  membership to the oracle, and tallies pass/fail (stub returns a fixed
  signature, so inside-corners that match the stub signature pass).
- `tests/test_combinatorial.py::test_write_combinatorial_report_is_markdown` —
  `write_combinatorial_report()` writes a `.md` file starting with the report
  header and containing the summary line.
- `tests/test_combinatorial.py::test_write_combinatorial_report_with_failures` —
  the report includes a `## Failures` section when mismatches exist.
- `tests/test_combinatorial.py::test_combinatorial_gaslab_run` — (requires
  gaslab) generates pairwise cases from the GASLab descriptor (34 boxes →
  `34 × 40 = 1360` cases), runs each through `descriptor.entry_point`, checks the
  geometric oracle, and writes the report to
  `harness_tasks/progress_notes/T-TH-3_combinatorial_report.md`. Every verdict
  has a non-empty `actual` (no crashes); `report.passes > 0`.
- Inner loop clean on every edited file: `ruff` → `pyright` → `pytest -x -q`.

### Context ###

The GASLab descriptor (`descriptor.py`) exposes 34 fault boxes, each with 5
gas-dimension `(min, max)` bounds. T-TH-1 (boundary) and T-TH-2 (overlap) are the
two prior consumers of that box table. The combinatorial generator reuses:

- `GAS_DIMS` and the geometric box-membership notion from `boundary.py`.
- The `_build_row` int/float formatting convention (ints without `.0`).
- The `descriptor.build_args(row)` → `descriptor.entry_point(*args)` path.
- The `.md` report shape and `_today()` helper convention from `boundary.py` /
  `overlap.py`.

**Named signal/noise consumer:** the GASLab fork, via `build_gaslab_descriptor()`.
Every pairwise case is run through the live GASLab `process()` function. No new
field, no speculative surface.

**Overlap caveat (carried from T-TH-1):** a corner point geometrically inside
Box A may also fall inside Box B (overlap is T-TH-2's subject). The report flags
classifier-vs-oracle mismatches and includes an explicit caveat that overlap may
explain a mismatch where the oracle says "inside" but the classifier returns a
different (also-valid) signature.

### Design ###

`CombinatorialGenerator` takes a `ModuleDescriptor` and an optional `t` (fixed at
2 for this task; the signature accepts it so a later task can raise it without a
rewrite, but `t != 2` is rejected here as out of scope).

For each box:

1. Determine `box_dims` = the gas dimensions the box defines (in `GAS_DIMS`
   order). Skip boxes that define none.
2. Compute the centroid per dimension (mean of min/max), as in `boundary.py`.
3. For each unordered **pair** `(d1, d2)` of `box_dims` (`itertools.combinations`,
   deterministic order):
   - For each of the 4 corners `(c1, c2) ∈ {min,max} × {min,max}`:
     - Build the point: `d1=c1`, `d2=c2`, every other box dim at its centroid.
     - Geometric oracle: inside iff the point lies within **all** of the box's
       dimensions (closed interval `lo <= v <= hi`). Corners of a well-formed box
       are inside by this definition.
     - Emit a `CombinatorialCase`.

**Computed values:**

| Column | Value |
|---|---|
| `case_id` | `TH-CMB-{box_sig[:18]}-{d1}-{d2}-{c1lbl}{c2lbl}` (`c?lbl` ∈ `mn`/`mx`) |
| `description` | `{box_sig}: ({d1},{d2}) at ({c1lbl},{c2lbl})` |
| `dim_pair` | `(d1, d2)` |
| `corner` | `(c1lbl, c2lbl)` e.g. `("mn","mx")` |
| `point` | dict of all 5 gas dims → value |
| `geometric_oracle` | `"inside"` / `"outside"` |
| `source` | box.source citation |

`run()` mirrors `BoundaryGenerator.run()`: build row, call entry point, catch
exceptions into `actual = "ERROR:<Type>"`, compare `predicted_inside =
(actual_state == box_signature)` to `oracle_inside`, tally, and produce a summary
with the overlap caveat when failures exist.

`write_combinatorial_report()` mirrors `write_boundary_report()`: `.md` only,
header + date + totals + summary + a per-case results table + a `## Failures`
section when any mismatch exists.

### Isolation (non-negotiable) ###

`harness/generators/combinatorial.py` imports **no lab**. It imports only
`ModuleDescriptor` and the shared `GAS_DIMS` constant from `boundary.py`, and
stdlib (`itertools`, `dataclasses`, `pathlib`, `datetime`). It operates entirely
on `ModuleDescriptor` objects. The GASLab import stays in `descriptor.py`
(`build_gaslab_descriptor()`), the GASLab fork's own tooling. This preserves
"no cross-lab Python imports."

### Deliverables ###

1. `TestSuite/harness/harness/generators/combinatorial.py` (CREATE) —
   `CombinatorialGenerator` + `CombinatorialCase` + `CombinatorialReport` +
   `write_combinatorial_report()`.
2. `TestSuite/harness/tests/test_combinatorial.py` (CREATE) — the tests above.
3. `harness_tasks/progress_notes/T-TH-3_combinatorial_report.md` — written by the
   gaslab integration test (GASLab run output).

### Files to touch ###

- CREATE: `harness/generators/combinatorial.py`
- CREATE: `tests/test_combinatorial.py`
- CREATE: `harness_tasks/T-TH-3_combinatorial_generator.md` (this file)
- CREATE: `harness_tasks/progress_notes/T-TH-3.md` (gate + review)
- EDIT: `HARNESS_PROGRESS.md` (ledger row: `_author at start_` → this file path)

### Out of scope ###

- Higher-order coverage (3-wise+) and full-grid `2^5` corners. Pairwise only.
- Noise / fault-injection sweeps (T-TH-4).
- Metamorphic / monotonicity properties (T-TH-5).
- Overlap resolution — mismatches caused by overlapping boxes are flagged with
  the overlap caveat, not resolved (that is T-TH-2's report).
- Non-gas dimensions (`ctx_*`, `dna_*`) — held at the descriptor's neutral
  defaults via `build_args`, never varied. Combinatorial coverage of DNA-gated
  context is deferred to the same follow-up T-TH-1 named.

### Verification ###

Sandbox-bash note: if the Linux mount does not materialize the harness tree
(`tests/`, `harness_tasks/` missing under the VM), run the inner loop via the
Windows `.venv-wired` instead (CLAUDE.md → Windows tools). Commands (PowerShell):

```powershell
$venv = "C:\Users\muto\claude\4DApp\4DLab\.venv-wired\Scripts\python.exe"
$env:PYTHONPATH = "C:\Users\muto\claude\4DApp\4DLab\TestSuite\harness;C:\Users\muto\claude\4DApp\4DLab\GASLab"
cd C:\Users\muto\claude\4DApp\4DLab\TestSuite\harness
& $venv -m ruff check harness/generators/combinatorial.py tests/test_combinatorial.py
& $venv -m pyright harness/generators/combinatorial.py tests/test_combinatorial.py
& $venv -m pytest tests/test_combinatorial.py -x -q
```

Bash equivalent (when the mount works): `cd .../TestSuite/harness` then
`ruff check ...` / `pyright ...` / `pytest tests/test_combinatorial.py -x -q`.

VERIFICATION GATE + CODE REVIEW blocks must both be clean in
`harness_tasks/progress_notes/T-TH-3.md` before the ledger row flips to `done`.
