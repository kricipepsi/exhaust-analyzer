#!/usr/bin/env python3
"""Fresh driver and multi-dimension scorer for the wired-v7 petrol suite.

Runs petrol cases through wired.diagnose() and scores outcomes across six
independent dimensions: fault_family, fault_code, state, confidence,
perception_gap, and demotion_note_contains.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Bootstrap lab paths so editable packages resolve correctly
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WORKSPACE_ROOT / "apps/wired"))
for relative in (
    "labs/comlab",
    "labs/obdlab",
    "labs/dtclab",
    "labs/dnalab",
    "labs/vinlab",
):
    path = str(WORKSPACE_ROOT / relative)
    if path not in sys.path:
        sys.path.insert(0, path)

from v7.load_corpus import DEFAULT_CSV_PATH, row_to_raw_inputs  # noqa: E402
from wired.composition import diagnose  # noqa: E402
from wired.tracing import TRACE_ENV_VAR  # noqa: E402

# OpenTelemetry imports (only needed if tracing is requested)
try:
    from opentelemetry import context, trace
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.trace import set_span_in_context
    OTEL_AVAILABLE = True
except ImportError:
    trace = None
    OTLPSpanExporter = None
    Resource = None
    TracerProvider = None
    BatchSpanProcessor = None
    context = None
    set_span_in_context = None
    OTEL_AVAILABLE = False


def _install_provider(endpoint: str, service: str) -> Any:
    """Register one OTLP provider for this process if OTel is available."""
    if not OTEL_AVAILABLE or TracerProvider is None or Resource is None or BatchSpanProcessor is None or OTLPSpanExporter is None or trace is None:
        return None
    provider = TracerProvider(resource=Resource.create({"service.name": service}))
    provider.add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True))
    )
    trace.set_tracer_provider(provider)
    return provider


def check_demotion_note(res_dict: dict[str, Any], expected_substring: str) -> bool:
    """Check if the expected demotion note substring exists in any text output field."""
    if not expected_substring:
        return True

    verdict = res_dict.get("diagnostic_verdict", {})
    enrichment = res_dict.get("fault_enrichment", {})
    meta = res_dict.get("execution_meta", {})

    texts: list[str] = [
        verdict.get("fault_name", ""),
        verdict.get("display_headline", ""),
        verdict.get("actionable_remediation", ""),
        enrichment.get("mechanical_failure_mode", ""),
    ]
    texts.extend(enrichment.get("ui_remediation_steps", []))

    reasons = meta.get("lab_routing_directive", {}).get("reasons", [])
    texts.extend([str(r) for r in reasons])

    target = expected_substring.lower()
    return any(target in str(text).lower() for text in texts)


def score_case(
    result_dict: dict[str, Any] | None,
    oracle_row: dict[str, str],
    raised_exception: Exception | None = None,
) -> dict[str, str]:
    """Score a single case output against its oracle row expectations.

    Returns a dict mapping dimension name to outcome ("PASS", "FAIL", "NA").
    """
    outcomes = {
        "fault_family": "NA",
        "fault_code": "NA",
        "state": "NA",
        "confidence": "NA",
        "perception_gap": "NA",
        "demotion_note_contains": "NA",
    }

    expected_family = oracle_row.get("expected_fault_family", "").strip()
    expected_code = oracle_row.get("expected_fault_code", "").strip()
    expected_state = oracle_row.get("expected_state", "").strip()
    expected_conf_min_str = oracle_row.get("expected_confidence_min", "").strip()
    expected_conf_max_str = oracle_row.get("expected_confidence_max", "").strip()
    expected_pg_str = oracle_row.get("expected_perception_gap", "").strip()
    expected_demotion_str = oracle_row.get("expected_demotion_note_contains", "").strip()
    expected_crash_abort = oracle_row.get("expected_crash_abort", "none").strip()

    # Determine crash/abort status
    actual_crash_abort = "none"
    if raised_exception is not None:
        actual_crash_abort = "validation_error"
    elif result_dict is not None:
        degradation = result_dict.get("execution_meta", {}).get("degradation_mode", "")
        if degradation == "FATAL_INCOMPLETE":
            actual_crash_abort = "fatal_incomplete"

    # If the case crashed with an unexpected exception (we expected "none")
    if raised_exception is not None and expected_crash_abort == "none":
        return {k: "FAIL" for k in outcomes}

    # If we expected a crash/abort outcome
    if expected_crash_abort != "none":
        outcome = "PASS" if actual_crash_abort == expected_crash_abort else "FAIL"
        return {k: outcome for k in outcomes}

    # If we expected "none" but got an abort without exception
    if actual_crash_abort != "none":
        return {k: "FAIL" for k in outcomes}

    if result_dict is None:
        return {k: "FAIL" for k in outcomes}

    verdict = result_dict.get("diagnostic_verdict", {})
    actual_family = verdict.get("fault_family", "")
    actual_code = verdict.get("fault_code", "")
    actual_is_fault = verdict.get("is_fault_detected", False)
    actual_confidence = verdict.get("confidence_score", 0.0)

    # 1. fault_family
    if expected_family:
        outcomes["fault_family"] = "PASS" if actual_family.lower() == expected_family.lower() else "FAIL"

    # 2. fault_code
    if expected_code and expected_code.lower() != "null":
        outcomes["fault_code"] = "PASS" if actual_code.lower() == expected_code.lower() else "FAIL"

    # 3. state
    if expected_state:
        if not actual_is_fault:
            actual_state = "insufficient_evidence"
        else:
            if expected_state in ("named_fault", "warning"):
                actual_state = expected_state
            else:
                actual_state = "named_fault"
        outcomes["state"] = "PASS" if actual_state == expected_state else "FAIL"

    # 4. confidence
    if expected_conf_min_str and expected_conf_max_str:
        try:
            c_min = float(expected_conf_min_str)
            c_max = float(expected_conf_max_str)
            outcomes["confidence"] = "PASS" if c_min <= actual_confidence <= c_max else "FAIL"
        except ValueError:
            outcomes["confidence"] = "FAIL"

    # 5. perception_gap
    if expected_pg_str:
        expected_pg = (expected_pg_str.lower() == "true")
        pa = result_dict.get("performance_analytics", {})
        actual_pg = (pa.get("o2_sensor_bias_verdict") is not None)
        outcomes["perception_gap"] = "PASS" if actual_pg == expected_pg else "FAIL"

    # 6. demotion_note_contains
    if expected_demotion_str:
        outcomes["demotion_note_contains"] = (
            "PASS" if check_demotion_note(result_dict, expected_demotion_str) else "FAIL"
        )

    return outcomes


def run_suite(
    csv_path: Path,
    case_filter: str | None = None,
    family_filter: str | None = None,
    category_filter: str | None = None,
    trace_enabled: bool = False,
    otlp_endpoint: str = "http://localhost:4317",
    service_name: str = "4dlab-wired-harness",
) -> int:
    """Run the suite of test cases, reporting outcomes and aggregates."""
    provider = None
    if trace_enabled:
        if not OTEL_AVAILABLE:
            print("Error: OpenTelemetry is not installed. Tracing is disabled.")
            trace_enabled = False
        else:
            provider = _install_provider(otlp_endpoint, service_name)
            os.environ[TRACE_ENV_VAR] = "1"

    # Read cases from CSV
    cases = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cases.append(row)

    results = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Aggregate stats counters
    total_run = 0
    accuracy_cases_count = 0
    accuracy_cases_passed = 0
    characterization_cases_count = 0
    characterization_ran_count = 0
    characterization_error_count = 0

    per_family_total: dict[str, int] = {}
    per_family_passed: dict[str, int] = {}
    per_dimension_failures = {
        "fault_family": 0,
        "fault_code": 0,
        "state": 0,
        "confidence": 0,
        "perception_gap": 0,
        "demotion_note_contains": 0,
    }
    crash_count = 0

    tracer = None
    if trace_enabled and OTEL_AVAILABLE and trace is not None:
        tracer = trace.get_tracer("run_suite")

    for row in cases:
        case_id = row["case_id"]
        tag = row["tag"]
        category = row["source_category"]
        expected_family = row["expected_fault_family"]
        accuracy_excluded = (row["accuracy_excluded"].lower() == "true")

        # Apply filters
        if case_filter and case_id.lower() != case_filter.lower():
            continue
        if family_filter and expected_family.lower() != family_filter.lower():
            continue
        if category_filter and category.lower() != category_filter.lower():
            continue

        raw_inputs = row_to_raw_inputs(row)
        result_dict = None
        raised_exception = None
        outcome = "FAIL"

        # Diagnose within OTel span if enabled
        if trace_enabled and tracer and context is not None and set_span_in_context is not None:
            span = tracer.start_span("suite.case")
            span.set_attribute("case_id", case_id)
            token = context.attach(set_span_in_context(span))
            try:
                res = diagnose(raw_inputs, enable_fatal_gates=(tag == "invalid"))
                result_dict = res.model_dump()
            except Exception as e:
                raised_exception = e
            finally:
                # We will set the outcome attribute on the span below
                pass
        else:
            try:
                res = diagnose(raw_inputs, enable_fatal_gates=(tag == "invalid"))
                result_dict = res.model_dump()
            except Exception as e:
                raised_exception = e

        # Score the case
        outcomes = score_case(result_dict, row, raised_exception)

        # Classify overall outcome
        crashed = (raised_exception is not None and row.get("expected_crash_abort", "none").strip() == "none")
        if crashed:
            outcome = "CRASH"
            crash_count += 1
        elif tag == "invalid":
            # For invalid cases, overall matches if expected crash/abort matched
            outcome = "PASS" if all(val == "PASS" for val in outcomes.values()) else "FAIL"
        elif accuracy_excluded:
            # Characterization cases
            outcome = "RAN" if raised_exception is None else "ERROR"
            if outcome == "RAN":
                characterization_ran_count += 1
            else:
                characterization_error_count += 1
        else:
            # Accuracy cases
            outcome = "PASS" if all(val != "FAIL" for val in outcomes.values()) else "FAIL"

        # Update OTel span outcome
        if trace_enabled and tracer and context is not None:
            span.set_attribute("outcome", outcome)
            span.end()
            context.detach(token)

        # Update aggregate stats
        total_run += 1
        if tag == "invalid":
            pass
        elif accuracy_excluded:
            characterization_cases_count += 1
        else:
            accuracy_cases_count += 1
            if outcome == "PASS":
                accuracy_cases_passed += 1

            # Update per-family tallies
            fam = expected_family or "unspecified"
            per_family_total[fam] = per_family_total.get(fam, 0) + 1
            if outcome == "PASS":
                per_family_passed[fam] = per_family_passed.get(fam, 0) + 1

            # Update per-dimension failure counts
            for dim, result_val in outcomes.items():
                if result_val == "FAIL":
                    per_dimension_failures[dim] = per_dimension_failures.get(dim, 0) + 1

        results.append({
            "case_id": case_id,
            "category": category,
            "tag": tag,
            "accuracy_excluded": accuracy_excluded,
            "crashed": crashed,
            "outcome": outcome,
            "dimensions": outcomes,
            "verdict": result_dict.get("diagnostic_verdict") if result_dict else None,
        })

    # Provider cleanup
    if provider:
        provider.shutdown()
        os.environ.pop(TRACE_ENV_VAR, None)

    # Reporting
    print("\n" + "=" * 60)
    print("WIRED-V7 ACCURACY SUITE RUN SUMMARY")
    print("=" * 60)
    print(f"Timestamp: {timestamp}")
    print(f"Total Cases Run: {total_run}")
    print(f"Accuracy Cases: {accuracy_cases_passed}/{accuracy_cases_count} passed", end="")
    if accuracy_cases_count > 0:
        accuracy_pct = (accuracy_cases_passed / accuracy_cases_count) * 100
        print(f" ({accuracy_pct:.2f}%)")
    else:
        print(" (N/A)")
    print(f"Characterization Cases: {characterization_ran_count} ran, {characterization_error_count} errored")
    print(f"Total Engine Crashes: {crash_count}")

    print("\nPER-FAMILY ACCURACY (Accuracy cases only):")
    for fam in sorted(per_family_total.keys()):
        total = per_family_total[fam]
        passed = per_family_passed.get(fam, 0)
        pct = (passed / total) * 100
        print(f"  {fam:<24} : {passed}/{total} passed ({pct:.2f}%)")

    print("\nPER-DIMENSION FAILURE COUNTS (Accuracy cases only):")
    for dim, failures in per_dimension_failures.items():
        print(f"  {dim:<24} : {failures} failures")

    # Write machine-readable JSON
    run_dir = Path(__file__).parent / "runs" / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)
    results_path = run_dir / "results.json"
    with open(results_path, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": timestamp,
            "total_run": total_run,
            "accuracy": {
                "total": accuracy_cases_count,
                "passed": accuracy_cases_passed,
                "pct": (accuracy_cases_passed / accuracy_cases_count * 100) if accuracy_cases_count > 0 else 0,
            },
            "characterization": {
                "total": characterization_cases_count,
                "ran": characterization_ran_count,
                "error": characterization_error_count,
            },
            "crashes": crash_count,
            "failures_by_dimension": per_dimension_failures,
            "results": results,
        }, f, indent=2)

    print(f"\nWritten results to untracked results file: {results_path}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the v7 petrol case suite.")
    parser.add_argument("--case", help="Filter by case ID.")
    parser.add_argument("--family", help="Filter by expected fault family.")
    parser.add_argument("--category", help="Filter by source category.")
    parser.add_argument("--trace", action="store_true", help="Enable OTLP Jaeger tracing.")
    parser.add_argument("--otlp-endpoint", default="http://localhost:4317", help="OTLP endpoint for Jaeger.")
    parser.add_argument("--service", default="4dlab-wired-harness", help="OTel service name.")
    args = parser.parse_args()

    sys.exit(run_suite(
        DEFAULT_CSV_PATH,
        case_filter=args.case,
        family_filter=args.family,
        category_filter=args.category,
        trace_enabled=args.trace,
        otlp_endpoint=args.otlp_endpoint,
        service_name=args.service,
    ))
