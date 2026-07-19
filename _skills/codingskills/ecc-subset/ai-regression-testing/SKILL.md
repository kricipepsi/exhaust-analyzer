---
name: ai-regression-testing
description: Regression testing strategies for AI-assisted development. Patterns to catch AI blind spots where the same model writes and reviews code, and to prevent accuracy regressions in ML/diagnostic pipelines.
origin: ECC
---

# AI Regression Testing

Testing patterns specifically designed for AI-assisted development, where the same model writes code and reviews it — creating systematic blind spots that only automated tests can catch.

## When to Activate

- An AI agent has modified engine logic or scoring/ranking logic
- A bug was found and fixed — need to prevent re-introduction
- Running accuracy benchmarks after code changes (Layer-1 or Layer-2)
- Multiple code paths exist that must stay in sync

## The Core Problem

When an AI writes code and then reviews its own work, it carries the same assumptions into both steps:

```
AI writes fix → AI reviews fix → AI says "looks correct" → Bug still exists
```

There are **two** blind spots here, not one:

1. **Re-introduced bugs** — a defect that was found and fixed creeps back because the
   same model makes the same category of mistake again. (The reactive case.)
2. **Untested failure paths** — the boundary the model never exercised while writing
   *or* reviewing: the single-element list, the empty input, the divide-by-zero, the
   off-by-one in row iteration. For AI-written code these unexercised paths are latent
   bugs *before* anyone files a report, because the model that skipped them when writing
   also skips them when reviewing. (The proactive case.)

The pattern for (1): **path inconsistency** is the #1 AI-introduced regression. In
diagnostic engines specifically: fixing the main classification path but forgetting the
fallback path, or fixing the ranking logic but not the tie-breaker.

The pattern for (2): the model writes the happy path, then "tests" the happy path, and
the failure path ships untouched. A test suite that only mirrors the code the model
already wrote cannot catch what the model never wrote. This is the gap that lets a
single-value `stdev` (`StatisticsError` on `len == 1`) or a `rows[0]` vs `rows[1]`
off-by-one survive a "thorough" suite — both are defects the proactive boundary pass
below catches and the reactive-only pass misses.
<!-- Rework basis: skill_eval T-SE-4 (cohort_testcraft_report.md §3). The escaped-defect
     signal for this skill lives entirely in boundary/failure-path mutants on task_02
     (single-value stdev len>1→len>=1; row-iteration rows[0]→rows[1]); the reactive-only
     framing diluted it. Proactive boundary section added to recover that signal. -->

> **Don't aim for 100% coverage, and don't wait for a bug report to test a failure
> path.** Those two ideas are in tension only if you read "regression test" as
> "test written after a bug." Widen it: a boundary the model demonstrably skips *is*
> a regression risk. Test the failure paths proactively, then keep adding bug-named
> tests as real defects surface.

## Strategy: Test Where Bugs Were Found

Don't aim for 100% coverage. Instead:

```
Bug found in lambda calculation     → Write regression test for lambda
Bug found in O2 classification      → Write regression test for O2
Bug found in fault ranking          → Write regression test for ranker
No bug in freeze-frame parsing      → Don't write test yet
```

**Why this works with AI development:**
1. AI tends to make the **same category of mistake** repeatedly
2. Bugs cluster in complex areas (multi-path logic, chemistry calculations, edge weights)
3. Once tested, that exact regression **cannot happen again**

## Regression Test Pattern (pytest)

```python
# Name tests after the bug they prevent
def test_lambda_calculation_not_none_regression():
    """BUG-R1: lambda was None when O2 voltage was 0.0 (not absent)."""
    result = compute_lambda(o2_voltage=0.0, co=1.2, hc=150)
    assert result is not None
    assert 0.5 <= result <= 2.0

def test_specific_fault_ranks_above_generic_regression():
    """BUG-R2: GenericMisfire ranked above CylinderMisfire after T06 refactor."""
    results = rank_faults(["GenericMisfire", "CylinderMisfire"], context={...})
    specific_idx = next(i for i, r in enumerate(results) if r.node == "CylinderMisfire")
    generic_idx  = next(i for i, r in enumerate(results) if r.node == "GenericMisfire")
    assert specific_idx < generic_idx
```

## Proactive Boundary & Failure-Path Pattern

Before any bug is reported, enumerate the inputs the implementation *can* mishandle and
write a test for each. These are the failure paths an AI writer-reviewer pair systematically
skips. For a typical numeric/collection function, walk this checklist — it is short on
purpose, because the same handful of boundaries account for most escaped defects:

| Boundary | Why the model skips it | Test to write |
|---|---|---|
| Empty collection (`[]`, `""`, no rows) | Happy path assumes ≥1 element | Assert the documented behaviour (raise, or return a defined empty result) — never a bare `IndexError` |
| Single element (`len == 1`) | Aggregations like `stdev`/`variance` need ≥2 | Assert it raises *or* returns the defined value — not a stray `StatisticsError` |
| Zero / division-by-zero | Denominators are assumed non-zero | Assert the guarded result, not `ZeroDivisionError` |
| First/last index, off-by-one (`rows[0]` vs `rows[1]`) | Header/row boundary is invisible in the happy case | Use a multi-row fixture where row 0 and row 1 differ, so an off-by-one fails |
| `None` / `NaN` propagation | Model tests with clean values | Assert the function neither crashes nor silently returns `None` on a boundary input |

```python
import pytest

def test_stdev_single_value_is_defined():
    """Single-value input must not leak a raw StatisticsError."""
    with pytest.raises(ValueError):       # or assert the defined return — pick one and pin it
        column_stdev([42.0])

def test_row_iteration_uses_all_rows():
    """Off-by-one guard: rows[0] vs rows[1] must change the result."""
    two_rows = [{"v": 1.0}, {"v": 9.0}]
    assert summarize(two_rows) != summarize(two_rows[:1])
```

The point is not ceremony — it is that these five boundaries are where AI-written code
most often hides a defect that survives self-review. Spend the test budget here first.

## Parity Test Pattern

When the engine has multiple paths (e.g. petrol vs. fallback, Layer-1 vs. Layer-2), assert both return the same contract:

```python
REQUIRED_OUTPUT_FIELDS = ["node_id", "confidence", "severity", "layer_source"]

def test_layer1_and_layer2_output_same_shape():
    case = load_test_case("petrol_lean_misfire_001")
    l1 = engine.run_layer1(case)
    l2 = engine.run_layer2(case)
    for field in REQUIRED_OUTPUT_FIELDS:
        assert field in l1[0]
        assert field in l2[0]
```

## Integrating with the Layer-2 Accuracy Gate

The Layer-2 corpus replay (`run_dual_engine_comparison.py`) is your macro regression gate. Complement it with micro regression tests in pytest for specific bugs found during the rebuild:

```
Layer-1 pytest (seconds) → catches regressions in individual functions
Layer-2 corpus replay (minutes) → catches accuracy regressions across 234 cases
```

Never skip Layer-2 for tasks that touch model output (T05–T09, T12, T13).

## Common AI Regression Patterns in Diagnostic Engines

| Pattern | Test Strategy | Priority |
|---|---|---|
| Path mismatch (main vs. fallback) | Assert same output shape from both paths | High |
| Missing field after refactor | Assert all required fields present | High |
| Generic-over-specific ranking inversion | Assert specific node ranks above generic | High |
| Null chemistry value on edge input | Assert value is not None on boundary inputs | Medium |
| Attractor node creeping back | Assert attractor nodes not in top-K results | Medium |

## DO / DON'T

**DO:**
- Write regression tests immediately after finding a bug
- Name tests after the bug: `test_<symptom>_regression`
- Run pytest as the **first step** of every bug-check, before any AI review
- Keep regression tests fast (milliseconds each)
- Cover the boundary/failure paths proactively (empty, single-element, zero, off-by-one,
  `None`/`NaN`) — for AI-written code these are latent regressions even with no bug filed yet

**DON'T:**
- Trust AI self-review as a substitute for automated tests
- Skip regression tests for "obvious" fixes — the AI will re-introduce them
- Mistake "the happy path passes" for a thorough suite — a suite that only exercises the
  code the model already wrote cannot catch the failure path the model never wrote
