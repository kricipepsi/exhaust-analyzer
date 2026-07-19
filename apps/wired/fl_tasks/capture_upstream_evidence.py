#!/usr/bin/env python3
"""Capture v7 upstream GASLab/OBDLab evidence for the wired-FL pack."""

from __future__ import annotations

import argparse
import csv
import importlib
import json
import os
import sys
from collections import Counter, defaultdict
from collections.abc import Mapping, Sequence
from copy import deepcopy
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
for relative in (
    "apps/wired",
    "labs/comlab",
    "labs/dnalab",
    "labs/dtclab",
    "labs/gaslab",
    "labs/obdlab",
    "labs/symptomlab",
    "labs/vinlab",
):
    path = str(WORKSPACE_ROOT / relative)
    if path not in sys.path:
        sys.path.insert(0, path)

from dnalab import build_vehicle_dna  # noqa: E402
from vinlab import VINDecodeError  # noqa: E402

from v7.load_corpus import DEFAULT_CSV_PATH, row_to_raw_inputs  # noqa: E402
from wired.composition import (  # noqa: E402
    _as_dict,
    _build_fallback_vin_dna,
    _derive_horizon,
    _run_gaslab,
    _run_obdlab,
    diagnose,
)
from wired.tracing import TRACE_ENV_VAR, is_opentelemetry_sdk_available  # noqa: E402

DEFAULT_RUN_RESULTS = WORKSPACE_ROOT / "apps/wired/v7/runs/20260630_163900/results.json"
DEFAULT_REGISTRY = WORKSPACE_ROOT / "labs/comlab/comlab/config/global_fault_registry.json"
DEFAULT_REPORT = WORKSPACE_ROOT / "apps/wired/fl_tasks/reports/FL_UPSTREAM_2026-06-30.md"
DEFAULT_JSON = WORKSPACE_ROOT / "apps/wired/fl_tasks/reports/FL_UPSTREAM_2026-06-30.json"
DEAD_FAMILIES = ("mechanical_wear", "exhaust_leak", "non_starter")
SPOT_CHECK_FAMILIES = DEAD_FAMILIES
NO_OBD_INPUT = "NOT_RUN_NO_OBD_INPUT"


def _enum_value(value: Any) -> Any:
    """Return enum wire value without depending on a source enum class."""
    return getattr(value, "value", value)


def _read_csv_rows(csv_path: Path) -> list[dict[str, str]]:
    """Return v7 corpus rows keyed exactly as the CSV header names them."""
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _read_run_results(results_path: Path) -> dict[str, dict[str, Any]]:
    """Return the frozen v7 result row by case id."""
    payload = json.loads(results_path.read_text(encoding="utf-8"))
    return {str(row["case_id"]): row for row in payload["results"]}


def _read_registry(registry_path: Path) -> tuple[dict[str, dict[str, Any]], dict[str, set[str]]]:
    """Return registry rows by fault id and family-level required gas states."""
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    by_id: dict[str, dict[str, Any]] = {}
    by_family: dict[str, set[str]] = defaultdict(set)
    for row in payload["registry"]:
        fault_id = str(row["fault_id"])
        matrix = row.get("cross_domain_matrix", {})
        state = matrix.get("gas_lab_state")
        by_id[fault_id] = row
        if state:
            family = _family_from_fault_id(fault_id)
            if family:
                by_family[family].add(str(state))
    return by_id, by_family


def _family_from_fault_id(fault_id: str) -> str | None:
    """Return the canonical family implied by a registry fault id prefix."""
    prefix_map = {
        "ERR-MW-": "mechanical_wear",
        "ERR-EL-": "exhaust_leak",
        "ERR-NS-": "non_starter",
    }
    for prefix, family in prefix_map.items():
        if fault_id.startswith(prefix):
            return family
    return None


def _build_vin_dna(raw_inputs: Mapping[str, Any]) -> dict[str, Any]:
    """Build the same VIN DNA dict the public wired composition path uses."""
    vin = str(raw_inputs.get("vin", ""))
    triage = _as_dict(raw_inputs.get("triage"))
    try:
        vehicle_dna = build_vehicle_dna(vin, triage)
    except VINDecodeError:
        vin_dna = _build_fallback_vin_dna(vin)
    else:
        dna_payload = vehicle_dna.to_json_payload()
        vin_dna = _as_dict(dna_payload["vin_dna"])

    if "resolved_horizon" not in vin_dna:
        vin_dna["resolved_horizon"] = _derive_horizon(
            str(vin_dna.get("euro_emission_category", "EURO_6")),
        )
    return vin_dna


def _capture_upstream_for_row(
    row: Mapping[str, str],
    result: Mapping[str, Any],
    registry_by_id: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    """Replay GASLab/OBDLab inputs for one row and return classifier-ready evidence."""
    raw_inputs = row_to_raw_inputs(dict(row))
    vin_dna = _build_vin_dna(raw_inputs)

    try:
        gas_output = _run_gaslab(_as_dict(raw_inputs.get("gas")), vin_dna)
        gas_state = str(_enum_value(gas_output.chemical_state))
    except Exception as exc:  # noqa: BLE001 - capture invalid-row live stage failures
        gas_state = f"GASLAB_ERROR:{type(exc).__name__}"

    obd_inputs = raw_inputs.get("obd")
    if obd_inputs is None:
        obd_o2_failure_mode = NO_OBD_INPUT
    else:
        try:
            obd_output = _run_obdlab(_as_dict(obd_inputs), vin_dna)
            obd_o2_failure_mode = str(_enum_value(obd_output.o2_failure_mode))
        except Exception as exc:  # noqa: BLE001 - capture invalid-row live stage failures
            obd_o2_failure_mode = f"OBDLAB_ERROR:{type(exc).__name__}"

    verdict = result.get("verdict") or {}
    expected_code = row.get("expected_fault_code", "").strip()
    required_state = _registry_gas_state(registry_by_id, expected_code)
    return {
        "case_id": row["case_id"],
        "tag": row["tag"],
        "source_category": row["source_category"],
        "expected_fault_family": row.get("expected_fault_family", ""),
        "expected_fault_code": expected_code,
        "predicted_fault_family": verdict.get("fault_family"),
        "predicted_fault_code": verdict.get("fault_code"),
        "fault_family_dimension": (result.get("dimensions") or {}).get("fault_family"),
        "state_dimension": (result.get("dimensions") or {}).get("state"),
        "gas_chemistry_states": [gas_state],
        "obd_o2_failure_mode": obd_o2_failure_mode,
        "required_gating_state_for_expected_code": required_state,
    }


def _registry_gas_state(
    registry_by_id: Mapping[str, Mapping[str, Any]],
    fault_id: str,
) -> str | None:
    """Return the registry-required gas state for one expected fault id."""
    row = registry_by_id.get(fault_id)
    if row is None:
        return None
    state = row.get("cross_domain_matrix", {}).get("gas_lab_state")
    return str(state) if state else None


def capture_records(
    csv_path: Path,
    results_path: Path,
    registry_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, set[str]]]:
    """Capture upstream evidence for every v7 corpus row."""
    rows = _read_csv_rows(csv_path)
    results_by_case = _read_run_results(results_path)
    registry_by_id, required_by_family = _read_registry(registry_path)

    records = []
    for row in rows:
        case_id = row["case_id"]
        records.append(_capture_upstream_for_row(row, results_by_case[case_id], registry_by_id))
    return records, required_by_family


def _install_in_memory_exporter() -> Any:
    """Install an in-memory OpenTelemetry exporter for span proof spot-checks."""
    if not is_opentelemetry_sdk_available():
        raise RuntimeError("opentelemetry-sdk is not installed in .venv-wired")

    trace_module = importlib.import_module("opentelemetry.trace")
    sdk_trace_module = importlib.import_module("opentelemetry.sdk.trace")
    sdk_export_module = importlib.import_module("opentelemetry.sdk.trace.export")
    in_memory_module = importlib.import_module(
        "opentelemetry.sdk.trace.export.in_memory_span_exporter",
    )

    exporter = in_memory_module.InMemorySpanExporter()
    provider = sdk_trace_module.TracerProvider()
    provider.add_span_processor(sdk_export_module.SimpleSpanProcessor(exporter))
    trace_module.set_tracer_provider(provider)
    return exporter


def _span_attributes(span: Any) -> dict[str, Any]:
    """Return a JSON-friendly attribute dict from an OpenTelemetry span."""
    return {str(key): value for key, value in getattr(span, "attributes", {}).items()}


def _span_events(span: Any) -> list[dict[str, Any]]:
    """Return JSON-friendly event records from an OpenTelemetry span."""
    events = []
    for event in getattr(span, "events", ()):  # pragma: no branch - SDK shape is stable
        events.append({
            "name": str(event.name),
            "attributes": {
                str(key): value for key, value in getattr(event, "attributes", {}).items()
            },
        })
    return events


def _spot_check_candidates(
    records: Sequence[Mapping[str, Any]],
    family: str,
) -> list[Mapping[str, Any]]:
    """Return dead-family miss candidates for live prune-span spot checks."""
    return [
        record for record in records
        if record.get("expected_fault_family") == family
        and record.get("fault_family_dimension") == "FAIL"
        and record.get("required_gating_state_for_expected_code")
    ]

def _span_rule_ids(expected_code: str) -> set[str]:
    """Return possible router span rule ids for an oracle fault code."""
    ids = {expected_code}
    if expected_code.startswith("ERR-"):
        ids.add(expected_code.removeprefix("ERR-"))
    return ids



def _find_pruned_event(
    prune_spans: Sequence[Any],
    expected_rule_ids: set[str],
) -> tuple[dict[str, Any] | None, bool]:
    """Return a matching rule-pruned event and whether it matched the expected rule."""
    fallback_event = None
    for span in prune_spans:
        for event in _span_events(span):
            attrs = event["attributes"]
            if attrs.get("rule_id") in expected_rule_ids:
                return event, True
            if attrs.get("failed_gating_key") == "gas_lab_state" and fallback_event is None:
                fallback_event = event
    return fallback_event, False


def _trace_spot_check_record(
    record: Mapping[str, Any],
    rows_by_case: Mapping[str, Mapping[str, str]],
    exporter: Any,
) -> dict[str, Any]:
    """Trace one case and return its prune-span proof row."""
    exporter.clear()
    case_id = str(record["case_id"])
    raw_inputs = row_to_raw_inputs(dict(rows_by_case[case_id]))
    diagnose(deepcopy(raw_inputs), enable_fatal_gates=(record.get("tag") == "invalid"))
    spans = exporter.get_finished_spans()
    prune_spans = [span for span in spans if span.name == "phase.prune"]
    expected_code = str(record.get("expected_fault_code") or "")
    matching_event, matched_expected = _find_pruned_event(
        prune_spans,
        _span_rule_ids(expected_code),
    )
    return {
        "case_id": case_id,
        "expected_fault_family": record.get("expected_fault_family"),
        "expected_fault_code": expected_code,
        "emitted_gas_state": record.get("gas_chemistry_states", [None])[0],
        "required_gating_state": record.get("required_gating_state_for_expected_code"),
        "phase_prune_spans": len(prune_spans),
        "phase_prune_attrs": [_span_attributes(span) for span in prune_spans],
        "matched_expected_rule": matched_expected,
        "matching_rule_pruned_event": matching_event,
    }



def trace_spot_checks(records: Sequence[Mapping[str, Any]], csv_path: Path) -> list[dict[str, Any]]:
    """Run selected cases through live diagnose() and extract prune-span proof."""
    exporter = _install_in_memory_exporter()
    rows_by_case = {row["case_id"]: row for row in _read_csv_rows(csv_path)}
    os.environ[TRACE_ENV_VAR] = "1"
    os.environ["OTEL_TRACES_EXPORTER"] = "otlp"
    try:
        checks = []
        for family in SPOT_CHECK_FAMILIES:
            fallback_check = None
            for record in _spot_check_candidates(records, family):
                check = _trace_spot_check_record(record, rows_by_case, exporter)
                if check["matched_expected_rule"]:
                    checks.append(check)
                    break
                if fallback_check is None:
                    fallback_check = check
            else:
                if fallback_check is not None:
                    checks.append(fallback_check)
        return checks
    finally:
        os.environ.pop(TRACE_ENV_VAR, None)
        os.environ.pop("OTEL_TRACES_EXPORTER", None)


def _coverage(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Return coverage counters for the captured evidence."""
    gas_count = sum(1 for row in records if row.get("gas_chemistry_states"))
    obd_count = sum(1 for row in records if row.get("obd_o2_failure_mode"))
    return {
        "total": len(records),
        "gas_states_captured": gas_count,
        "obd_modes_populated": obd_count,
    }


def _dead_family_rows(records: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    """Return all dead-family case rows for emitted-vs-required comparison."""
    return [row for row in records if row.get("expected_fault_family") in DEAD_FAMILIES]


def _state_counts(records: Sequence[Mapping[str, Any]]) -> dict[str, dict[str, int]]:
    """Return gas-state frequency by expected family."""
    counts: dict[str, Counter[str]] = defaultdict(Counter)
    for record in records:
        family = str(record.get("expected_fault_family") or "")
        states = record.get("gas_chemistry_states") or []
        for state in states:
            counts[family][str(state)] += 1
    return {family: dict(counter) for family, counter in sorted(counts.items())}


def _required_state_summary(required_by_family: Mapping[str, set[str]]) -> dict[str, list[str]]:
    """Return sorted required registry states for the dead families."""
    return {
        family: sorted(required_by_family.get(family, set()))
        for family in DEAD_FAMILIES
    }


def build_payload(
    records: Sequence[dict[str, Any]],
    required_by_family: Mapping[str, set[str]],
    spot_checks: Sequence[Mapping[str, Any]],
    csv_path: Path,
    results_path: Path,
    registry_path: Path,
) -> dict[str, Any]:
    """Build the machine-readable FL upstream evidence payload."""
    return {
        "metadata": {
            "task": "T-FL-2",
            "generated_utc": datetime.now(UTC).isoformat(timespec="seconds"),
            "method": "read-only replay of GASLab/OBDLab stages using v7.load_corpus.row_to_raw_inputs and wired.composition lab helpers",
            "corpus_csv": str(csv_path.relative_to(WORKSPACE_ROOT)),
            "run_results": str(results_path.relative_to(WORKSPACE_ROOT)),
            "registry": str(registry_path.relative_to(WORKSPACE_ROOT)),
            "engine_lab_source_edits": False,
        },
        "coverage": _coverage(records),
        "required_gating_states_by_dead_family": _required_state_summary(required_by_family),
        "gas_state_counts_by_expected_family": _state_counts(records),
        "spot_checks": list(spot_checks),
        "dead_family_records": list(_dead_family_rows(records)),
        "records": list(records),
    }


def _md_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    """Render a simple Markdown table."""
    lines = ["| " + " | ".join(headers) + " |"]
    lines.append("|" + "|".join("---" for _ in headers) + "|")
    for row in rows:
        lines.append("| " + " | ".join(_md_cell(value) for value in row) + " |")
    return "\n".join(lines)


def _md_cell(value: Any) -> str:
    """Render one Markdown table cell without breaking pipe delimiters."""
    if value is None:
        return ""
    if isinstance(value, list):
        text = ", ".join(str(item) for item in value)
    else:
        text = str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def render_report(payload: Mapping[str, Any]) -> str:
    """Render the Markdown report consumed by T-FL-3."""
    coverage = payload["coverage"]
    records = payload["records"]
    dead_records = payload["dead_family_records"]
    spot_checks = payload["spot_checks"]
    required = payload["required_gating_states_by_dead_family"]
    state_counts = payload["gas_state_counts_by_expected_family"]

    dead_summary_rows = []
    for family in DEAD_FAMILIES:
        emitted = state_counts.get(family, {})
        emitted_text = ", ".join(f"{state}={count}" for state, count in sorted(emitted.items()))
        dead_summary_rows.append((family, emitted_text, required.get(family, [])))

    spot_rows = []
    for check in spot_checks:
        event = check.get("matching_rule_pruned_event") or {}
        attrs = event.get("attributes", {}) if isinstance(event, Mapping) else {}
        spot_rows.append((
            check.get("case_id"),
            check.get("expected_fault_family"),
            check.get("expected_fault_code"),
            check.get("emitted_gas_state"),
            check.get("required_gating_state"),
            check.get("phase_prune_spans"),
            attrs.get("rule_id"),
            attrs.get("prune_reason"),
            attrs.get("failed_gating_key"),
        ))

    dead_rows = [
        (
            row.get("case_id"),
            row.get("expected_fault_family"),
            row.get("expected_fault_code"),
            row.get("predicted_fault_family"),
            row.get("gas_chemistry_states"),
            row.get("required_gating_state_for_expected_code"),
            row.get("obd_o2_failure_mode"),
        )
        for row in dead_records
    ]

    all_rows = [
        (
            row.get("case_id"),
            row.get("tag"),
            row.get("expected_fault_family"),
            row.get("expected_fault_code"),
            row.get("predicted_fault_family"),
            row.get("predicted_fault_code"),
            row.get("gas_chemistry_states"),
            row.get("obd_o2_failure_mode"),
        )
        for row in records
    ]

    return "\n\n".join([
        "# FL_UPSTREAM_2026-06-30 — per-case upstream GASLab/OBDLab evidence",
        "**Task:** [[T-FL-2_capture_upstream_evidence]]  \n"
        "**Mode:** read-only measurement; no engine/lab/oracle/wiki/source edits.  \n"
        "**Consumer:** [[T-FL-3_classify_failure_modes]].",
        "## Method",
        "This harness replays the exact per-row sanitized inputs produced by "
        "`apps/wired/v7/load_corpus.py::row_to_raw_inputs()` through the same wired "
        "composition seam helpers used by `diagnose()`: `_run_gaslab()` and `_run_obdlab()`. "
        "It does not change the final engine schema; it captures the upstream lab states that "
        "the final `OrchestratorFinalUIOutput` omits. The live-pipeline proof uses in-memory "
        "OpenTelemetry, calls public `diagnose()`, and reads the COMLab `phase.prune` span events.",
        "## Coverage",
        _md_table(
            ["Metric", "Value"],
            [
                ("Total corpus rows", coverage["total"]),
                ("GASLab chemistry states captured", f"{coverage['gas_states_captured']}/{coverage['total']}"),
                ("OBDLab O2 mode/status field populated", f"{coverage['obd_modes_populated']}/{coverage['total']}"),
            ],
        ),
        "## Live-pipeline spot checks",
        _md_table(
            [
                "case_id",
                "expected family",
                "expected code",
                "emitted GASLab state",
                "required state",
                "phase.prune spans",
                "pruned rule",
                "prune reason",
                "failed gating key",
            ],
            spot_rows,
        ),
        "## Dead-family emitted-vs-required summary",
        _md_table(
            ["Expected family", "Emitted GASLab states", "Registry-required GASLab states"],
            dead_summary_rows,
        ),
        "## Dead-family case rows",
        _md_table(
            [
                "case_id",
                "expected family",
                "expected code",
                "predicted family",
                "emitted GASLab state",
                "required state for expected code",
                "OBDLab O2 mode",
            ],
            dead_rows,
        ),
        "## Per-case upstream evidence",
        _md_table(
            [
                "case_id",
                "tag",
                "expected family",
                "expected code",
                "predicted family",
                "predicted code",
                "gas_chemistry_states[]",
                "obd_o2_failure_mode",
            ],
            all_rows,
        ),
        "",
    ])


def write_artifacts(payload: Mapping[str, Any], report_path: Path, json_path: Path) -> None:
    """Write deterministic JSON plus Markdown report artifacts."""
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_report(payload), encoding="utf-8")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV_PATH)
    parser.add_argument("--results", type=Path, default=DEFAULT_RUN_RESULTS)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--json", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--no-write", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    """Capture upstream evidence and emit the FL report artifacts."""
    args = parse_args(argv)
    records, required_by_family = capture_records(args.csv, args.results, args.registry)
    spot_checks = trace_spot_checks(records, args.csv)
    payload = build_payload(
        records,
        required_by_family,
        spot_checks,
        args.csv,
        args.results,
        args.registry,
    )
    if not args.no_write:
        write_artifacts(payload, args.report, args.json)
    coverage = payload["coverage"]
    print(
        "Captured upstream evidence: "
        f"gas={coverage['gas_states_captured']}/{coverage['total']} "
        f"obd={coverage['obd_modes_populated']}/{coverage['total']} "
        f"spot_checks={len(spot_checks)}",
    )
    if not args.no_write:
        print(f"Wrote {args.report}")
        print(f"Wrote {args.json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
