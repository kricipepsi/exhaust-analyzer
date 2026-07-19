#!/usr/bin/env python3
"""Split frozen PRODUCER_GAP cases into classifier-fixable vs signal-required buckets."""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
for relative in (
    "apps/wired",
    "apps/wired/fl_tasks",
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

from capture_upstream_evidence import _build_vin_dna  # noqa: E402
from v7.load_corpus import DEFAULT_CSV_PATH, row_to_raw_inputs  # noqa: E402
from wired.composition import (  # noqa: E402
    _build_gas_dna_view,
    _run_gaslab,
    _run_obdlab,
)

from gaslab.contracts import EngineStateBucket, GasReading  # noqa: E402
from gaslab.ontology_loader import load_ontology  # noqa: E402
from gaslab.rule_engine import (  # noqa: E402
    _calibrate_o2_bias_high_bounds,
    _calibrate_o2_bias_low_bounds,
    _coc_adjust_normal_bounds,
    _definitive_match,
    _matching_fault_candidates,
    _resolve_candidates,
    _signature_values,
)
from gaslab.validity_gates import sample_validity  # noqa: E402

LOCALIZATION_PATH = WORKSPACE_ROOT / "apps/wired/fl_tasks/reports/FL_LOCALIZATION_2026-06-30.md"
UPSTREAM_PATH = WORKSPACE_ROOT / "apps/wired/fl_tasks/reports/FL_UPSTREAM_2026-06-30.json"
DEFAULT_REPORT = WORKSPACE_ROOT / "v3/reports/V3_PRODUCER_GAP_SPLIT_2026-06-30.md"
DEFAULT_JSON = WORKSPACE_ROOT / "v3/reports/V3_PRODUCER_GAP_SPLIT_2026-06-30.json"

CLASSIFIER_FIXABLE = "CLASSIFIER_FIXABLE"
SIGNAL_REQUIRED = "SIGNAL_REQUIRED"
EXPECTED_PRODUCER_GAPS = 25

RESEARCH_CLUSTER_BY_FAMILY = {
    "cam_timing": "Cluster 7 — cam timing / VVT",
    "ecu_fault": "Cluster 3 — ECU/control fault",
    "mechanical_wear": "Cluster 1 — mechanical vs misfire",
    "non_starter": "Cluster 8 — no-start root cause",
    "rich_mixture": "Cluster 2 — rich vs catalyst",
}
RESEARCH_CLUSTER_BY_STATE = {
    "CAM_TIMING_RETARDED_MAP": "Cluster 7 — cam timing / VVT",
    "VVT_FAILURE": "Cluster 7 — cam timing / VVT",
    "COOLANT_LEAK_INTERNAL": "Cluster 1 — mechanical vs misfire",
    "WORN_VALVE_SEALS": "Cluster 1 — mechanical vs misfire",
    "WORN_PISTON_RINGS": "Cluster 1 — mechanical vs misfire",
    "POA_SIGNATURE": "Cluster 1 — mechanical vs misfire",
    "IGNITION_MISFIRE": "Cluster 8 — no-start root cause",
    "INCOMPLETE_COMBUSTION": "Cluster 8 — no-start root cause",
    "LEAN_MIXTURE": "Cluster 8 — no-start root cause",
    "NORMAL_OPERATION": "Cluster 3 — ECU/control fault",
    "RICH_MIXTURE": "Cluster 2 — rich vs catalyst",
}
MISSING_QUANTITY_BY_STATE = {
    "CAM_TIMING_RETARDED_MAP": "idle→2500 cam/VVT discriminator satisfying the retarded-MAP rich-normalising vector",
    "VVT_FAILURE": "cam/VVT phase discriminator or cleaner non-invalid VVT chemistry",
    "NORMAL_OPERATION": "ECU/control evidence with chemically normal exhaust",
    "POA_SIGNATURE": "mechanical-wear high-idle/transient discriminator",
    "WORN_VALVE_SEALS": "mechanical-wear high-idle/transient HC discriminator",
    "WORN_PISTON_RINGS": "mechanical-wear high-idle/load HC discriminator",
    "COOLANT_LEAK_INTERNAL": "positive block-test / coolant-combustion marker",
    "IGNITION_MISFIRE": "non-starter cranking/misfire evidence beyond ambient-air sample",
    "LEAN_MIXTURE": "non-starter live OBD/fuel-air evidence beyond ambient-air sample",
    "INCOMPLETE_COMBUSTION": "non-starter combustion/no-combustion evidence beyond invalid sample",
    "RICH_MIXTURE": "rich-mixture discriminator not present in the single idle chemistry row",
}


@dataclass(frozen=True)
class CaseSplit:
    """One producer-gap classification row."""

    case_id: str
    expected_family: str
    predicted_family: str
    expected_code: str
    required_state: str
    emitted_state: str
    verdict: str
    research_cluster: str | None
    missing_quantity: str | None
    threshold_evidence: str
    emitted_candidates: tuple[str, ...]
    resolved_candidates: tuple[str, ...]


def _enum_value(value: Any) -> str:
    """Return enum wire value without importing a mirror enum."""
    return str(getattr(value, "value", value))


def _read_csv_rows(csv_path: Path) -> dict[str, dict[str, str]]:
    """Load corpus rows by case id."""
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return {row["case_id"]: row for row in csv.DictReader(handle)}


def _producer_gap_case_ids(localization_path: Path) -> list[str]:
    """Return PRODUCER_GAP case ids from the localization table only."""
    case_ids: list[str] = []
    in_table = False
    for line in localization_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Per-case localization table"):
            in_table = True
            continue
        if in_table and line.startswith("---"):
            break
        if not in_table or "| PRODUCER_GAP |" not in line:
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if cells and cells[0] != "case_id":
            case_ids.append(cells[0])
    return case_ids


def _upstream_records(upstream_path: Path) -> dict[str, Mapping[str, Any]]:
    """Load frozen upstream evidence rows by case id."""
    payload = json.loads(upstream_path.read_text(encoding="utf-8"))
    return {str(row["case_id"]): row for row in payload["records"]}


def _gas_readings(gas_inputs: Mapping[str, Any]) -> tuple[GasReading, GasReading | None]:
    """Build idle and optional high-idle readings from raw v7 gas inputs."""
    idle = GasReading(
        hc=int(gas_inputs["hc"]),
        co=float(gas_inputs["co"]),
        co2=float(gas_inputs["co2"]),
        o2=float(gas_inputs["o2"]),
        nox=int(gas_inputs["nox"]),
    )
    high_keys = ("hc_high", "co_high", "co2_high", "o2_high", "nox_high")
    high = None
    if all(gas_inputs.get(key) is not None for key in high_keys):
        high = GasReading(
            hc=int(gas_inputs["hc_high"]),
            co=float(gas_inputs["co_high"]),
            co2=float(gas_inputs["co2_high"]),
            o2=float(gas_inputs["o2_high"]),
            nox=int(gas_inputs["nox_high"]),
        )
    return idle, high


def _signature_for_state(state: str, ontology: Mapping[str, Any], dna: Any) -> Mapping[str, Mapping[str, float]] | None:
    """Return the GASLab bound signature used for a state, including DNA calibration."""
    entry = ontology.get("faults", {}).get(state)
    if not entry:
        return None
    signature = entry["signature"]
    if state == "NORMAL_OPERATION":
        return _coc_adjust_normal_bounds(signature, dna)
    if state == "O2_SENSOR_BIASED_LOW":
        return _calibrate_o2_bias_low_bounds(signature, dna)
    if state == "O2_SENSOR_BIASED_HIGH":
        return _calibrate_o2_bias_high_bounds(signature, dna)
    return signature


def _bound_evidence(state: str, ontology: Mapping[str, Any], reading: GasReading, dna: Any) -> str:
    """Render concise threshold comparisons for the required state."""
    values = _signature_values(reading)
    signature = _signature_for_state(state, ontology, dna)
    if signature is None:
        if state == "COOLANT_LEAK_INTERNAL":
            return (
                "COOLANT_LEAK_INTERNAL grammar: co2<=12.0, hc>=300, block_test_passed=True "
                f"vs co2={reading.co2:g}, hc={reading.hc:g}; block_test is a separate input"
            )
        return f"{state} has no bound-matching signature in GASLab ontology; evaluated by grammar/fallback"

    failed = []
    passed = []
    for gas_key in ("hc", "co", "co2", "o2", "nox", "lambda"):
        bounds = signature[gas_key]
        value = values[gas_key]
        comparison = f"{gas_key}={value:.3g} in [{bounds['min']:g},{bounds['max']:g}]"
        if bounds["min"] <= value <= bounds["max"]:
            passed.append(comparison)
        else:
            failed.append(comparison)
    if failed:
        passed_text = "; ".join(passed[:3])
        suffix = f" (passes {passed_text})" if passed_text else ""
        return "fails " + "; ".join(failed) + suffix
    return "passes required bound signature: " + "; ".join(passed)


def _cluster_for(expected_family: str, required_state: str) -> str:
    """Map a signal-required case to its Phase-4 research cluster."""
    if required_state == "NORMAL_OPERATION" and expected_family == "cam_timing":
        return "Cluster 7 — cam timing / VVT"
    if required_state in RESEARCH_CLUSTER_BY_STATE:
        return RESEARCH_CLUSTER_BY_STATE[required_state]
    return RESEARCH_CLUSTER_BY_FAMILY.get(expected_family, "Cluster TBD — unmapped producer gap")


def _missing_quantity(expected_family: str, required_state: str) -> str:
    """Name the missing physical quantity for a signal-required case."""
    if required_state == "NORMAL_OPERATION" and expected_family == "cam_timing":
        return "cam/VVT evidence that can separate a real timing fault from chemically non-normal exhaust"
    return MISSING_QUANTITY_BY_STATE.get(required_state, "additional physical discriminator for the expected family")


def _split_case(case_id: str, row: Mapping[str, str], upstream: Mapping[str, Any], ontology: Mapping[str, Any]) -> CaseSplit:
    """Replay one raw-input row and classify its producer-gap fork."""
    raw_inputs = row_to_raw_inputs(dict(row))
    vin_dna = _build_vin_dna(raw_inputs)
    gas_inputs = raw_inputs["gas"]
    idle, high = _gas_readings(gas_inputs)
    dna = _build_gas_dna_view(
        vin_dna,
        coc_target_lambda_v112=gas_inputs.get("coc_target_lambda_v112"),
        coc_target_lambda_low=gas_inputs.get("coc_target_lambda_low"),
        coc_target_lambda_high=gas_inputs.get("coc_target_lambda_high"),
        coc_co_low_idle=gas_inputs.get("coc_co_low_idle"),
        coc_co_high_idle=gas_inputs.get("coc_co_high_idle"),
    )
    engine_state = EngineStateBucket(gas_inputs.get("engine_state", "STABILIZED_IDLE"))

    gas_output = _run_gaslab(dict(gas_inputs), vin_dna)
    emitted_state = _enum_value(gas_output.chemical_state)
    if raw_inputs.get("obd") is not None:
        _run_obdlab(dict(raw_inputs["obd"]), vin_dna)

    candidates = _matching_fault_candidates(idle, engine_state, dict(ontology), dna)
    resolved = _resolve_candidates(
        candidates,
        idle,
        dna,
        dict(ontology),
        engine_state,
        high,
        fuel_trim=gas_inputs.get("fuel_trim"),
    )
    definitive = _definitive_match(
        idle,
        dna,
        engine_state,
        dict(ontology),
        block_test_passed=bool(gas_inputs.get("block_test_passed", False)),
        reading_high=high,
        fuel_trim=gas_inputs.get("fuel_trim"),
    )

    required_state = str(upstream["required_gating_state_for_expected_code"])
    expected_family = str(upstream["expected_fault_family"])
    threshold_evidence = _bound_evidence(required_state, ontology, idle, dna)
    required_reachable = required_state in candidates or required_state in resolved
    if required_state == "NORMAL_OPERATION" and definitive is None and not resolved:
        required_reachable = True

    validity = _enum_value(sample_validity(idle))
    if required_reachable:
        verdict = CLASSIFIER_FIXABLE
        research_cluster = None
        missing_quantity = None
        threshold_evidence = f"{threshold_evidence}; sample_validity={validity}; required state reachable from row inputs"
    else:
        verdict = SIGNAL_REQUIRED
        research_cluster = _cluster_for(expected_family, required_state)
        missing_quantity = _missing_quantity(expected_family, required_state)
        high_note = "high-idle present" if high is not None else "high-idle absent"
        threshold_evidence = f"{threshold_evidence}; sample_validity={validity}; {high_note}; required state not reachable from row inputs"

    return CaseSplit(
        case_id=case_id,
        expected_family=expected_family,
        predicted_family=str(upstream["predicted_fault_family"]),
        expected_code=str(upstream["expected_fault_code"]),
        required_state=required_state,
        emitted_state=emitted_state,
        verdict=verdict,
        research_cluster=research_cluster,
        missing_quantity=missing_quantity,
        threshold_evidence=threshold_evidence,
        emitted_candidates=tuple(candidates),
        resolved_candidates=tuple(resolved),
    )


def build_payload(csv_path: Path = DEFAULT_CSV_PATH) -> dict[str, Any]:
    """Build the producer-gap split payload."""
    rows_by_id = _read_csv_rows(csv_path)
    producer_ids = _producer_gap_case_ids(LOCALIZATION_PATH)
    if len(producer_ids) != EXPECTED_PRODUCER_GAPS:
        raise RuntimeError(f"expected {EXPECTED_PRODUCER_GAPS} producer gaps, found {len(producer_ids)}")
    upstream_by_id = _upstream_records(UPSTREAM_PATH)
    ontology = load_ontology()
    cases = [
        _split_case(case_id, rows_by_id[case_id], upstream_by_id[case_id], ontology)
        for case_id in producer_ids
    ]
    counts = Counter(case.verdict for case in cases)
    if counts[CLASSIFIER_FIXABLE] + counts[SIGNAL_REQUIRED] != EXPECTED_PRODUCER_GAPS:
        raise RuntimeError("split counts do not reconcile to 25")
    return {
        "metadata": {
            "task": "T-V3-D2",
            "generated_utc": datetime.now(UTC).isoformat(timespec="seconds"),
            "method": "read-only replay of each PRODUCER_GAP row through GASLab/OBDLab query mode, then bound/grammar inspection of required GASLab state",
            "corpus_csv": str(csv_path.relative_to(WORKSPACE_ROOT)),
            "localization": str(LOCALIZATION_PATH.relative_to(WORKSPACE_ROOT)),
            "upstream_evidence": str(UPSTREAM_PATH.relative_to(WORKSPACE_ROOT)),
            "engine_lab_source_edits": False,
        },
        "summary": {
            "total": len(cases),
            CLASSIFIER_FIXABLE: counts[CLASSIFIER_FIXABLE],
            SIGNAL_REQUIRED: counts[SIGNAL_REQUIRED],
            "research_clusters": dict(Counter(case.research_cluster for case in cases if case.research_cluster)),
        },
        "cases": [case.__dict__ for case in cases],
    }


def _md_cell(value: Any) -> str:
    """Render a Markdown table cell safely."""
    if value is None:
        return "—"
    if isinstance(value, (tuple, list)):
        text = ", ".join(str(item) for item in value) or "—"
    else:
        text = str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def _md_table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    """Render a GitHub-flavored Markdown table."""
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(_md_cell(value) for value in row) + " |")
    return "\n".join(lines)


def render_report(payload: Mapping[str, Any]) -> str:
    """Render the Markdown split report."""
    summary = payload["summary"]
    cases = payload["cases"]
    lines = [
        "# V3_PRODUCER_GAP_SPLIT_2026-06-30 — T-V3-D2",
        "",
        "## Summary",
        "",
        f"- Total PRODUCER_GAP cases: **{summary['total']} / 25**.",
        f"- `{CLASSIFIER_FIXABLE}`: **{summary[CLASSIFIER_FIXABLE]}**.",
        f"- `{SIGNAL_REQUIRED}`: **{summary[SIGNAL_REQUIRED]}**.",
        "- Method: replay each raw v7 row through GASLab/OBDLab query mode, then compare the required GASLab gating state against the row's actual chemistry thresholds.",
        "- Source lock: frozen `FL_LOCALIZATION_2026-06-30` + `FL_UPSTREAM_2026-06-30`; no lab, engine, oracle, CSV, graph, or Vault edits.",
        "",
        "## Research-cluster demand",
        "",
    ]
    cluster_rows = sorted(summary["research_clusters"].items())
    lines.append(_md_table(["Research cluster", "SIGNAL_REQUIRED cases"], cluster_rows))
    lines.extend([
        "",
        "## Per-case split",
        "",
        _md_table(
            [
                "case_id",
                "expected_code",
                "expected_family",
                "required_state",
                "emitted_state",
                "verdict",
                "state / threshold evidence",
                "missing quantity",
                "research cluster",
            ],
            [
                [
                    case["case_id"],
                    case["expected_code"],
                    case["expected_family"],
                    case["required_state"],
                    case["emitted_state"],
                    case["verdict"],
                    case["threshold_evidence"],
                    case["missing_quantity"],
                    case["research_cluster"],
                ]
                for case in cases
            ],
        ),
        "",
        "## Classifier-fixable cases",
        "",
        _md_table(
            ["case_id", "required_state", "emitted_state", "bound candidates", "resolved candidates", "evidence"],
            [
                [
                    case["case_id"],
                    case["required_state"],
                    case["emitted_state"],
                    case["emitted_candidates"],
                    case["resolved_candidates"],
                    case["threshold_evidence"],
                ]
                for case in cases
                if case["verdict"] == CLASSIFIER_FIXABLE
            ],
        ),
        "",
        "## Signal-required cases",
        "",
        _md_table(
            ["case_id", "required_state", "missing physical quantity", "research cluster"],
            [
                [case["case_id"], case["required_state"], case["missing_quantity"], case["research_cluster"]]
                for case in cases
                if case["verdict"] == SIGNAL_REQUIRED
            ],
        ),
        "",
    ])
    return "\n".join(lines)


def write_artifacts(payload: Mapping[str, Any], report_path: Path = DEFAULT_REPORT, json_path: Path = DEFAULT_JSON) -> None:
    """Write deterministic JSON and Markdown artifacts."""
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path.write_text(render_report(payload), encoding="utf-8")


def main() -> int:
    """Regenerate the producer-gap split report."""
    payload = build_payload()
    write_artifacts(payload)
    summary = payload["summary"]
    print(
        "PRODUCER_GAP split: "
        f"{summary['total']} total; "
        f"{CLASSIFIER_FIXABLE}={summary[CLASSIFIER_FIXABLE]}; "
        f"{SIGNAL_REQUIRED}={summary[SIGNAL_REQUIRED]}",
    )
    print(f"Wrote {DEFAULT_REPORT.relative_to(WORKSPACE_ROOT)}")
    print(f"Wrote {DEFAULT_JSON.relative_to(WORKSPACE_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
