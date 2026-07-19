# T-TH-3 — progress note (pairwise combinatorial corner generator)

**Task file:** `harness_tasks/T-TH-3_combinatorial_generator.md`
**Date:** 2026-06-04
**Mode:** STRICT (dual-gate: VERIFICATION GATE + CODE REVIEW)

---

## Plan (executed)

TDD. Authored the task file + flipped the ledger row atomically (`_author at
start_` → file path, status `in_progress`). Wrote `tests/test_combinatorial.py`
first, watched it fail (`ModuleNotFoundError: harness.generators.combinatorial`
— correct RED reason), then implemented
`harness/generators/combinatorial.py` minimally to pass.

**Capability:** for each fault box, every unordered pair of its 5 gas dimensions
is placed at the 4 `{min,max}×{min,max}` corners with the other 3 dims at the box
centroid. `C(5,2)=10` pairs × 4 corners = **40 points/box**. Geometric
box-membership oracle (closed interval, all-dims AND). `run()` calls the live
`descriptor.entry_point` per point, compares predicted membership to the oracle,
emits a `.md` report with the T-TH-1 overlap caveat.

**Consumer:** GASLab fork via `build_gaslab_descriptor()` — every case runs
through the live `process(GasReading, GasLabContext)`. No new field, no
speculative surface; same consumer as T-TH-1/T-TH-2.

**Why it earns its place over T-TH-1:** T-TH-1 moves one dimension at a time
(others at centroid), so a defect that fires only when two thresholds are crossed
*together* is invisible to it. Pairwise corners exercise exactly those
2-dimension boundary interactions.

---

## Environment note (inner loop ran via .venv-wired, not bash)

The sandbox Linux mount did not materialize the harness tree this session:
`os.listdir` from the bash VM showed `tests/` and `harness_tasks/` as
non-existent and `harness/generators` as empty, while the Read/Write/Glob tools
(real Windows FS) worked normally. Per `4DLab/CLAUDE.md → Windows tools`, the
inner loop was run on the Windows `.venv-wired` (Python 3.14.5; ruff 0.15.14,
pyright 1.1.409, pytest 9.0.3 all present). This is the documented fallback, not
a silent drop to Python 3.10.

The four `gaslab-*` skills named in `HARNESS_START_HERE §2` are not present as
files anywhere in the workspace or `~/.claude` (confirmed by glob + find). Their
discipline (tests-first, ruff→pyright→pytest inner loop, dual-gate, wiki-cited
box bounds) is spelled out explicitly in the START_HERE and task files and was
honored directly — the same path T-TH-0/1/2 took.

---

## VERIFICATION GATE — CLEAN

Commands (PowerShell, `.venv-wired`):

```
PYTHONPATH = TestSuite/harness ; GASLab
cd TestSuite/harness
ruff check  harness/generators/combinatorial.py tests/test_combinatorial.py  → All checks passed!
pyright     harness/generators/combinatorial.py tests/test_combinatorial.py  → 0 errors, 0 warnings, 0 informations
pytest tests/test_combinatorial.py -x -q                                     → 11 passed in 56.81s
```

Full-suite regression check (`pytest tests/ -q`): **54 passed, 1 failed**.

The single failure is `test_runner.py::test_parity_replays_existing_csv` —
the **pre-existing T-TH-0 parity-gate drift**, verbatim the four cases already
logged as H-3..H-6 in `HARNESS_PROGRESS.md`:

- GAS-EAL-001 expected EXHAUST_AIR_LEAK, actual RICH_MISFIRE (H-3)
- GAS-IOX-001 expected INCOMPLETE_OXIDATION, actual INCOMPLETE_COMBUSTION (H-4)
- GAS-WVT-001 expected WRONG_VALVE_TIMING, actual RICH_MISFIRE (H-5)
- GAS-ESO-001 expected EGR_STUCK_OPEN, actual INCOMPLETE_COMBUSTION (H-6)

This is in a file T-TH-3 did not touch and is GASLab CSV drift, not a regression
from this task. T-TH-0 was marked `done` with this exact 4-mismatch state on
record. **No new failure introduced by T-TH-3.**

GASLab integration run wrote `progress_notes/T-TH-3_combinatorial_report.md`:
1360 cases, **174 PASS / 1186 FAIL (12.8% match)**. The low agreement is the
expected signal, not a gate breach — pairwise corners push points deep into the
overlapping regions T-TH-2 measured (≈100% discrimination ceiling from
SAMPLE_INVALID + 5 envelope-only boxes claiming the whole space). The report
carries the overlap caveat. Analytical generators emit reports, not pass/fail
gates (proposal §4).

## CODE REVIEW — CLEAN

- **Isolation:** `combinatorial.py` imports only `ModuleDescriptor`/`FaultBox`
  from `harness.descriptor`, `GAS_DIMS` from `harness.generators.boundary`, and
  stdlib. No lab import. ✓
- **Convention reuse:** mirrors `boundary.py` exactly — `_build_row` int/float
  formatting, `run()` shape (`ERROR:<Type>` capture, predicted-vs-oracle tally),
  `.md` report layout, `_today()`. No divergence from the established pattern. ✓
- **No orphans:** every `CombinatorialCase` field (`dim_pair`, `corner`,
  `point`, `geometric_oracle`, `source`) is read in `run()` or the report
  writer. `t` is read in `__init__` (rejects `t != 2`). No field defined and
  read nowhere. ✓
- **Determinism:** `itertools.combinations` + fixed corner-label order ⇒ stable
  case order; no RNG. ✓
- **Counts proven by test:** 40/box (stub), 1360 for 34-box GASLab. ✓
- **Reports are `.md` only.** ✓

Both gates clean → ledger row flips to `done`.

---

## Follow-ups discovered

None new. The 12.8% match rate is fully explained by the existing H-series /
T-TH-2 discrimination-ceiling findings; no new H-row warranted.
