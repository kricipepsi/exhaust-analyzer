# Metrics Schema — Skill-Eval

**Pack:** `planning/skill_eval/` · **Consumer:** T-SE-2 (runner), T-SE-3..6 (A/B tasks), T-SE-FINAL (aggregation) · **Version:** 1.0 (frozen)

Every A/B trial produces exactly one `TrialRecord`. The eval runner (T-SE-2)
captures these fields; the per-skill tasks (T-SE-3..6) select which are
**primary** for their skill's claim. No field is captured that no consumer reads.

---

## 1. Trial Identity (set before generation)

| Field | Type | Description |
|-------|------|-------------|
| `trial_id` | `str` | Unique ID: `{task_id}__{skill_id}__{arm}__{seed}` |
| `task_id` | `str` | Which coding-task spec was used (e.g. `T-SE-3-T1`) |
| `skill_id` | `str` | Skill under test (from ledger shortlist; `none` for arm A) |
| `arm` | `str` | `A` (baseline, gate ON), `B` (skill, gate ON), or `C` (skill, gate OFF) |
| `seed` | `int` | Random seed fixed for the trial (reproducibility) |
| `model` | `str` | Model identifier + temperature (e.g. `opus-4.7@t=0.0`) |
| `timestamp_utc` | `str` | ISO-8601 trial start time |

## 2. Gate-Invisible Metrics (captured during the coding session)

These are upstream of, or invisible to, the gate (CONTRACT §3).

### 2.1 First-Pass Counts

Measured on the **first** `ruff` / `pyright` / `pytest` run before any fix.

| Field | Type | Description |
|-------|------|-------------|
| `first_ruff_errors` | `int` | `ruff check` error count on first run |
| `first_pyright_errors` | `int` | `pyright` diagnostic count on first run |
| `first_pytest_failures` | `int` | `pytest` failure count on first run (`-x` short-circuit; count the one that stopped it) |
| `first_pytest_errors` | `int` | `pytest` collection/import errors on first run |

### 2.2 Convergence Cost

| Field | Type | Description |
|-------|------|-------------|
| `iterations_to_green` | `int` | Number of edit→check cycles to reach clean gate |
| `total_tokens` | `int` | Total LLM tokens consumed for the task (input + output) |
| `total_time_s` | `float` | Wall-clock seconds from first edit to green gate |

### 2.3 Hallucinated-API Count

| Field | Type | Description |
|-------|------|-------------|
| `hallucinated_imports` | `int` | Import statements that fail `importlib.util.find_spec` |
| `hallucinated_functions` | `int` | Calls to functions/classes not found in the imported module's `__all__` or `dir()` |
| `hallucinated_params` | `int` | Keyword arguments passed to a real function that don't exist in its signature |

Verification method (automated): after the session, grep all `import` / `from X import Y`
lines; resolve each against the environment; count misses. For function/param
hallucinations, grep call sites and check against `inspect.signature` of the target.

## 3. Gate-Invisible Quality Score (Blinded Rubric)

Per rubric.md: 6 axes × 0–3, judged K≥3 times, blinded.

| Field | Type | Description |
|-------|------|-------------|
| `rubric_readability` | `float` | Mean readability score across K passes |
| `rubric_structure` | `float` | Mean structure score |
| `rubric_naming` | `float` | Mean naming score |
| `rubric_cohesion` | `float` | Mean cohesion score |
| `rubric_error_handling` | `float` | Mean error-handling score |
| `rubric_test_meaningfulness` | `float` | Mean test-meaningfulness score |
| `rubric_total` | `float` | Mean total (sum of 6 axes) across K passes |
| `rubric_sd_total` | `float` | SD of total across K passes |
| `rubric_max_axis_sd` | `float` | Max per-axis SD (noisiest axis — governs uncertainty) |
| `rubric_passes` | `int` | K — number of judge passes (must be ≥ 3) |

## 4. Objective Proxies (no judge needed)

| Field | Type | Description |
|-------|------|-------------|
| `cyclomatic_complexity_avg` | `float` | Mean cyclomatic complexity across all functions (radon or similar) |
| `cyclomatic_complexity_max` | `int` | Max cyclomatic complexity in any single function |
| `mutation_score` | `float \| null` | `mutmut` or `mutpy` score (test suites only; `null` if no tests) |
| `type_coverage_pct` | `float` | % of functions/methods with complete type annotations |
| `docstring_coverage_pct` | `float` | % of public functions/classes with docstrings |
| `diff_churn_lines` | `int` | Total lines added + deleted in the final diff |
| `diff_files_touched` | `int` | Number of files modified |

## 5. Python Dataclass Reference

The canonical form for `TrialRecord` in the eval runner:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class TrialRecord:
    # Identity
    trial_id: str
    task_id: str
    skill_id: str
    arm: str                          # "A" | "B" | "C"
    seed: int
    model: str
    timestamp_utc: str

    # First-pass counts
    first_ruff_errors: int
    first_pyright_errors: int
    first_pytest_failures: int
    first_pytest_errors: int

    # Convergence cost
    iterations_to_green: int
    total_tokens: int
    total_time_s: float

    # Hallucinated-API
    hallucinated_imports: int
    hallucinated_functions: int
    hallucinated_params: int

    # Rubric (blinded, K≥3 passes)
    rubric_readability: float
    rubric_structure: float
    rubric_naming: float
    rubric_cohesion: float
    rubric_error_handling: float
    rubric_test_meaningfulness: float
    rubric_total: float
    rubric_sd_total: float
    rubric_max_axis_sd: float
    rubric_passes: int

    # Objective proxies
    cyclomatic_complexity_avg: float
    cyclomatic_complexity_max: int
    mutation_score: float | None
    type_coverage_pct: float
    docstring_coverage_pct: float
    diff_churn_lines: int
    diff_files_touched: int

    # Extensibility
    extra: dict[str, Any] = field(default_factory=dict)
```

## 6. Per-Skill Primary Metric Mapping

Each A/B task selects which fields are **primary** for its skill's claim
(CONTRACT §3 rule: credit only on the skill's own claim's metric).

| Cohort | Task | Skills | Primary Metrics |
|--------|------|--------|-----------------|
| House-style / craft | T-SE-3 | python, uncle-bob-craft, improve-codebase-architecture | `first_ruff_errors`, `first_pyright_errors`, `hallucinated_*`, `rubric_*`, `iterations_to_green` |
| Test-craft | T-SE-4 | python-testing, ai-regression-testing | `mutation_score`, `rubric_test_meaningfulness`, `rubric_error_handling` |
| Gate-overlap | T-SE-5 | verification-loop, code-review-excellence | Arm C: `first_pytest_failures` (no-gate recovery); arm A vs C delta on `rubric_*` |
| Meta/borderline | T-SE-6 | grey-haven-prompt-engineering (1 confirmatory A/B); eval-harness (inspection, no trial) | `rubric_total`, `first_ruff_errors`, `first_pyright_errors` — confirmatory A/B on `task_01` only; eval-harness has no metric (no trial). Pinned at authoring, Q-SE-1 resolved 2026-06-09. |

T-SE-FINAL consumes all primary metrics across all cohorts to produce the
aggregate KEEP/TRIM/CUT table.
