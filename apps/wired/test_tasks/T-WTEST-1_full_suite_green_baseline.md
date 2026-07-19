# T-WTEST-1 — Full-suite green baseline (run-only)

**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `pending` · **Blocked by:** —
**Mode:** RUN-ONLY — execute tests + record results; **no source/test edits**. · **Scope owner:** wired-test.
**Load skills:** wired-python (inner loop), wired-verification-loop.

## Objective
Establish the **green baseline** the audit (T-WTEST-2) and trace (T-WTEST-3/4/5)
passes sit on: run the **full pytest suite** across all seven labs **plus**
`apps/wired`, from the shared `.venv-wired`, and pin the per-package pass counts in
one report. A red baseline blocks the whole pack — you cannot trust an audit or a
trace of a suite that does not pass.

## Signal/noise
Adds no domain field or fault, runs no new code. The deliverable's **named
consumer** is the architect's go/no-go for the rest of this pack (a red row stops
T-WTEST-2..5) and the baseline report
`apps/wired/test_tasks/reports/WTEST1_BASELINE_<date>.md`, which T-WTEST-4 reads to
confirm the traced run reproduces the same green suite.

## Pinned facts (verified at authoring, re-confirm in-session)
- Shared interpreter: `/agent_workspace/.venv-wired/bin/python` (Python 3.14.x).
- Editable lab packages resolve only from a **neutral cwd** with the lab paths on
  `pythonpath`. `apps/wired/pyproject.toml` already sets `testpaths`/`pythonpath`
  for the wired suite; each lab carries its own `pyproject.toml`/`conftest.py`.
- Known reference points (from prior ledgers — confirm, do not assume): gaslab
  reported **510 passed** at T-GV2-2; `apps/wired` has 4 test files
  (`test_composition.py`, `test_fatal_gate.py`, `test_oil_cases.py`,
  `test_tracing.py`). `test_tracing.py` **skips** its OTel test if the SDK is
  absent (it is present in `.venv-wired`, so it should run, not skip).

## Scope
**IN:**
- For each target — `labs/gaslab labs/obdlab labs/dtclab labs/comlab labs/dnalab
  labs/vinlab labs/symptomlab` and `apps/wired` — run that package's pytest suite
  from its own directory with `.venv-wired`'s python, capturing **pass / fail /
  skipped / xfail counts and exit code**. Run each independently so one lab's
  failure does not abort the others.
- Record, per target: command run, counts, exit code, and any skipped test with
  its skip reason (especially the `apps/wired` OTel test — it must **run**, not
  skip, given the SDK is installed).
- Write ONE report at `apps/wired/test_tasks/reports/WTEST1_BASELINE_<date>.md`:
  a per-target table (target · pass · fail · skip · xfail · exit) + a one-line
  GREEN/RED verdict + the total passed across all eight targets.

**OUT:** any edit to a lab, COMLab, `apps/wired` source, or any test; fixing a
failing test (if a target is red, record it and hand back `blocked` — do not
patch); `pyright`/`ruff` (that is the inner loop, not this baseline); running under
`WIRED_OTEL`/Jaeger (that is T-WTEST-4); committing `__pycache__`/`.pytest_cache`.

## Steps
1. Confirm `/agent_workspace/.venv-wired/bin/python --version` prints 3.14.x.
2. For each target, from its own dir:
   `cd /agent_workspace/<target> && /agent_workspace/.venv-wired/bin/python -m pytest -q`
   Capture stdout tail + exit code. (If a lab needs extra `pythonpath`, mirror the
   pattern in that lab's `pyproject.toml`; do not invent paths.)
3. Confirm the `apps/wired` `test_tracing.py` OTel test **ran** (not skipped).
4. Aggregate into the report table; compute the GREEN/RED verdict and the total.
5. Fill the gate blocks in `test_tasks/progress_notes/T-WTEST-1.md`; STOP.

## Success criteria
- Every one of the 8 targets has a recorded counts row + exit code; no target is
  silently missing.
- Verdict is GREEN **iff** all 8 exit 0 with zero failures. If any target is red,
  the row is `blocked` with the failing target named — the report still ships.
- `apps/wired` OTel span test ran (skip=0 for that test).
- `git status` shows only new files under `apps/wired/test_tasks/`; no source/test
  changes; no committed `__pycache__`/`.pytest_cache`.

## VERIFICATION GATE — T-WTEST-1
Complete in `test_tasks/progress_notes/T-WTEST-1.md`: paste each target's pytest
tail + exit code; state the total passed and the GREEN/RED verdict.

## CODE REVIEW — T-WTEST-1
Complete in `test_tasks/progress_notes/T-WTEST-1.md`: confirm run-only (no source/
test diffs); no `graphify`; report is `.md`; no generated caches staged.

## Commit (owner, explicit paths)
```bash
cd /agent_workspace
git add \
  apps/wired/test_tasks/reports/WTEST1_BASELINE_<date>.md \
  apps/wired/test_tasks/progress_notes/T-WTEST-1.md \
  apps/wired/test_tasks/TEST_PROGRESS.md
git commit -m "T-WTEST-1: full-suite green baseline (7 labs + apps/wired)"
```
