"""Generic test-suite runner for the generative harness.

Lab-agnostic: operates on a ModuleDescriptor + CSV path.  Reuses the
per-module CSV conventions (gt_method / gt_source governance columns) from
PER_MODULE_TESTSUITE_DESIGN_SPEC.md so generated cases are first-class.
"""

from __future__ import annotations

import csv
import time
from pathlib import Path
from typing import Any

from harness.descriptor import ModuleDescriptor


def run_suite(
    descriptor: ModuleDescriptor,
    csv_path: Path,
) -> tuple[int, int, dict[str, str], list[dict[str, Any]]]:
    """Run a CSV suite through a ModuleDescriptor.

    Returns (passes, failures, actual_states, results) where:
        actual_states: case_id -> chemical_state (or other primary output label)
        results: list of per-row result dicts for the report emitter
    """
    passes = 0
    failures = 0
    actual_states: dict[str, str] = {}
    results: list[dict[str, Any]] = []

    with csv_path.open("r", encoding="utf-8", errors="replace", newline="") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            case_id = row["case_id"]
            t0 = time.perf_counter()

            expected = descriptor.extract_expected(row)
            expected_error = expected.get("error", "")

            # --- Build args (may raise ValueError for invalid rows) ---
            try:
                args = descriptor.build_args(row)
            except ValueError:
                if expected_error == "ValueError":
                    passes += 1
                    results.append({
                        "case_id": case_id,
                        "verdict": "PASS",
                        "detail": "ValueError raised as expected",
                        "duration_ms": round((time.perf_counter() - t0) * 1000, 2),
                    })
                else:
                    failures += 1
                    results.append({
                        "case_id": case_id,
                        "verdict": "FAIL",
                        "detail": f"unexpected ValueError (expected_error={expected_error!r})",
                        "duration_ms": round((time.perf_counter() - t0) * 1000, 2),
                    })
                continue

            # --- Expected an error but none was raised ---
            if expected_error:
                failures += 1
                results.append({
                    "case_id": case_id,
                    "verdict": "FAIL",
                    "detail": f"expected {expected_error} but no exception was raised",
                    "duration_ms": round((time.perf_counter() - t0) * 1000, 2),
                })
                continue

            # --- Invoke entry point ---
            actual = descriptor.entry_point(*args)

            # Record primary state for delta computation
            state = getattr(actual, "chemical_state", None)
            if state is not None:
                actual_states[case_id] = state.value if hasattr(state, "value") else str(state)

            mismatches = descriptor.diff(actual, expected)
            dt_ms = round((time.perf_counter() - t0) * 1000, 2)

            if mismatches:
                failures += 1
                results.append({
                    "case_id": case_id,
                    "verdict": "FAIL",
                    "detail": "; ".join(mismatches),
                    "duration_ms": dt_ms,
                })
            else:
                passes += 1
                label = actual_states.get(case_id, "")
                results.append({
                    "case_id": case_id,
                    "verdict": "PASS",
                    "detail": label,
                    "duration_ms": dt_ms,
                })

    return passes, failures, actual_states, results
