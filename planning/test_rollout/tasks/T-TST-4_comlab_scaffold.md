# T-TST-4 — Align comlab tests/ to the canonical template

**Status:** completed · **Blocked by:** T-TST-0 · **Pack:** `planning/test_rollout/`

## Goal

Align `labs/comlab/tests/` to the template **without clobbering** what's already
there. COMLab is the fusion/decision spine — its generative harness is thin and
its real gate is the wired e2e path; this task only lays the folder shape.

## Context (disk state)

`labs/comlab/tests/` already has `conftest.py`, `test_router_spans.py`, plus
`e2e/`, `fixtures/`, `unit/`. Code forked: `comlab/{analytics,core,schemas,
observability}/*` (4353 LOC). COMLab is Stage-4 (last). Its input space is upstream
lab **verdicts**, not raw sensors → only combinatorial + fuzz generators apply, and
it consumes the **full** master (no per-lab projection — migration map / T-TST-0).

## Success criteria

1. `labs/comlab/tests/` matches the template additively: keep existing
   `conftest.py`, `e2e/`, `unit/`, `fixtures/`; move `test_router_spans.py` under
   `unit/` if it is a unit test; add `generative/` with **only**
   `test_combinatorial.py` + `test_fuzz.py` stubs; add `descriptor.py` stub under
   `fixtures/`.
2. The COM `descriptor.py` stub documents that its "ranges" are categorical upstream
   verdict states (not numeric boxes) and that the full-master e2e gate lives in
   `apps/wired/` (`T-TH-12`) — so COM's generative layer does not duplicate the
   integration gate.
3. Generative stubs collect as skipped (`reason="blocked: T-TST-10 comlab harness"`);
   existing COM tests still pass unchanged.

## Out of scope

- COM descriptor/generators (T-TST-10). The wired e2e gate (T-TH-12). `comlab/` code.
- Any per-lab COM CSV projection (COM uses the full master — do not invent a subset).

## Signal/noise consumer

`labs/comlab/tests/generative/` (future thin COM suite) + the wired e2e gate as the
true integration consumer; stubs skipped until T-TST-10.

## Files to touch

- `labs/comlab/tests/generative/{test_combinatorial,test_fuzz}.py` (stubs),
  `tests/fixtures/descriptor.py` (stub), and `test_router_spans.py` relocation if unit

## Verification

`pytest -q labs/comlab` passes existing tests + collects new stubs as skipped;
`ruff`/`pyright` clean; confirm no existing COM fixture/test was overwritten.
