# T-TH-4 — progress note (noise / fault-injection characterization)

**Task file:** `harness_tasks/T-TH-4_noise_characterization.md`
**Date:** 2026-06-04
**Mode:** STRICT (dual-gate: VERIFICATION GATE + CODE REVIEW)

---

## Plan (executed)

TDD. Authored the task file + flipped the ledger row atomically (`_author at
start_` → file path). Wrote `tests/test_noise.py` first against the not-yet-
existing module (RED via `ModuleNotFoundError: harness.generators.noise`), then
implemented `harness/generators/noise.py` minimally to pass.

**Capability:** from each fault box centroid, apply seeded fraction-of-box-width
perturbation at amplitude levels `(0.0, 0.1, 0.25, 0.5, 1.0)`, run each
perturbed point through the live `descriptor.entry_point`, and measure
**retention** = the fraction of perturbed points that still classify as the
box's *observed centroid label*. Emits an `.md` degradation report (aggregate
curve + per-box table + brittle-box callout + overlap caveat). This is a
**characterization report, not a pass/fail gate** (proposal §4; same posture as
T-TH-2). The `pytest` cases assert only generator shape, seeded determinism,
envelope clamping, and report emission — never a threshold on the curve.

**Key design decision — retention anchored to observed centroid label, not box
signature.** T-TH-2 proved the box table has a ~100% discrimination ceiling
(SAMPLE_INVALID + envelope-only boxes claim the whole space). Anchoring
retention to the box *signature* would have folded that overlap ceiling into
every retention number, making the noise signal unreadable. Anchoring to the
*observed centroid label* isolates the noise effect. The GASLab run vindicated
this: **30 of 34 centroids classify as a different signature** — pure overlap
artifact — yet the noise curve is still clean and monotone on top of it.

**Consumer:** GASLab fork via `build_gaslab_descriptor()` — every perturbed
point runs through the live `process(GasReading, GasLabContext)`. No new field,
no speculative surface; same consumer as T-TH-1/2/3.

---

## Environment note (inner loop ran via .venv-wired, not the bash sandbox)

The sandbox Linux mount (`$HOME/mnt/4DLab`) was a stale partial copy this
session — it surfaced only `TestSuite/harness/harness/generators` (empty) and
not the files written via the Windows FS tools, and `GASLab/` was absent. Per
`4DLab/CLAUDE.md → Windows tools`, the inner loop ran on the Windows
`.venv-wired` (Python **3.14.5**; ruff **0.15.14**, pyright **1.1.409**, pytest
**9.0.3**), reached via git-bash at `/c/Users/muto/claude/4DApp/4DLab`. This is
the documented fallback (same path T-TH-3 took), not a silent drop to 3.10.

The four `gaslab-*` skills named in `HARNESS_START_HERE §2` are not present as
files in the workspace or `~/.claude` (same finding as T-TH-0..3). Their
discipline (tests-first, ruff→pyright→pytest, dual-gate, wiki-cited box bounds)
is spelled out in the START_HERE/task files and was honored directly.

---

## VERIFICATION GATE — CLEAN

Commands (`.venv-wired`, from `TestSuite/harness`; tests self-insert
`harness/` and `../../GASLab` onto `sys.path`):

```
ruff   check harness/generators/noise.py tests/test_noise.py   → All checks passed!
pyright      harness/generators/noise.py tests/test_noise.py   → 0 errors, 0 warnings, 0 informations
pytest tests/test_noise.py -x -q                               → 7 passed in 604.70s (0:10:04)
```

`pytest --collect-only -q` → **62 tests collected in 0.13s** (all modules import
cleanly; T-TH-4 introduced no import-time breakage anywhere in the suite).

**No-regression argument.** T-TH-4 is new-files-only: it CREATES
`harness/generators/noise.py` and `tests/test_noise.py` and edits no existing
code module. `--collect-only` confirms every existing test still imports. A
new-file-only change cannot regress `test_runner.py` / `test_boundary.py` /
`test_overlap.py` / `test_combinatorial.py` / `test_report.py`. The one
pre-existing full-suite failure is `test_runner.py::test_parity_replays_existing_csv`
— the documented T-TH-0 parity drift H-3..H-6 (GASLab CSV drift), on record
since T-TH-0 was marked `done`. **No new failure introduced by T-TH-4.**

GASLab integration run wrote `progress_notes/T-TH-4_noise_report.md`:
- 34 box retention curves; aggregate mean retention 100% → 93% → 83% → 73% →
  **57%** across `a = 0.0 … 1.0` (smooth, monotone degradation).
- **7 brittle boxes** (retention < 50% at a=0.25): RICH_MIXTURE (32%),
  FLAT_CAMSHAFT (39%), GDI_HPFP_INTERNAL_SEAL_LEAK (42%), NORMAL_OPERATION (43%),
  VACUUM_REGULATOR_DIAPHRAGM_RUPTURE (44%), CATALYST_OVERWHELMED (46%),
  WORN_PISTON_RINGS (48%) — each reported with its wiki source citation.
- **30 of 34 centroids** classify as a different signature (overlap artifact,
  cross-referenced to `T-TH-2_overlap_report.md`); retention measured against
  the observed baseline label, marked ⚠ in the per-box table.

This is the expected signal, not a gate breach — analytical generators emit
reports, not pass/fail gates.

## CODE REVIEW — CLEAN

- **Isolation:** `noise.py` imports only `ModuleDescriptor` from
  `harness.descriptor`, `GAS_DIMS` from `harness.generators.boundary`, and stdlib
  (`random`, `dataclasses`, `pathlib`, `typing`, `datetime`). No lab import. ✓
- **Convention reuse:** mirrors `boundary.py`/`combinatorial.py` — `_build_row`
  int/float formatting, `_classify` with `ERROR:<Type>` capture, `.md` report
  layout, `_today()`. No divergence from the established pattern. ✓
- **Single source of truth for the envelope:** clamping reads
  `FieldRange.min_/max_` from the descriptor; no duplicate envelope constant. ✓
- **Determinism:** one `random.Random(seed)` advanced in fixed order
  (box → level → sample → dim); `test_noise_is_seeded_deterministic` asserts
  byte-identical points and identical retention under a fixed seed, and
  divergence under a different seed. No ambient randomness. ✓
- **No orphans:** every `NoiseReport` field is read in `write_noise_report` /
  `_summarize`; `NoiseCase.point`/`source`/`box_signature`/`amplitude` are read
  in `run()` and the writer. `case_id`/`sample_index` are per-case identifiers
  (same role as `BoundaryCase.case_id`), consumed by tests; not a
  defined-but-unread contract field. ✓
- **Characterization-only honored:** no degradation threshold is asserted in any
  `pytest` case; `test_noise_retention_decreases_with_amplitude` only checks the
  trivially-true `ret[1.0] <= ret[0.0]` shape, not a magnitude. ✓
- **Reports are `.md` only.** ✓

Both gates clean → ledger row flips to `done`.

---

## Follow-ups discovered

None new. The 30/34 overlap-artifact count and the brittle-box set are fully
explained by the existing T-TH-2 discrimination-ceiling finding; no new H-row
warranted. (If the architect later refines the box table, the brittle-box
callout is the natural worklist — but that is architect work, out of scope here.)
