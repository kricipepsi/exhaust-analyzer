#!/usr/bin/env python3
"""Split frozen DATA_GAP cases into corpus-fill vs acquisition-gap buckets."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
LOCALIZATION_PATH = WORKSPACE_ROOT / "apps/wired/fl_tasks/reports/FL_LOCALIZATION_2026-06-30.md"
UPSTREAM_PATH = WORKSPACE_ROOT / "apps/wired/fl_tasks/reports/FL_UPSTREAM_2026-06-30.json"
CSV_PATH = WORKSPACE_ROOT / "apps/wired/v7/data/cases_petrol_v7.csv"
OWNER_QUEUE_PATH = WORKSPACE_ROOT / "apps/wired/v7_tasks/V7_PROGRESS.md"
DEFAULT_REPORT = WORKSPACE_ROOT / "v3/reports/V3_DATA_GAP_SPLIT_2026-06-30.md"
DEFAULT_JSON = WORKSPACE_ROOT / "v3/reports/V3_DATA_GAP_SPLIT_2026-06-30.json"

CORPUS_FILL = "CORPUS_FILL"
ACQUISITION_GAP = "ACQUISITION_GAP"
EXPECTED_DATA_GAPS = 19

FAILED_KEY_RE = re.compile(r"failed_gating_key=([^;]+)")
PRUNED_RULE_RE = re.compile(r"rule_pruned ([A-Z]+-[0-9]+)")

CLUSTER_BY_KEY_OR_FAMILY = {
    "lean_condition": "Cluster 5 — lean-condition root cause",
    "sensor_fault": "Cluster 6 — sensor fault under-detection",
    "no_fault": "Cluster 9 — confirming no-fault reliably",
    "non_starter": "Cluster 8 — non-starter",
}

MISSING_BY_CLUSTER = {
    "Cluster 5 — lean-condition root cause": (
        "live STFT/LTFT and lean-history DTC/freeze-frame evidence across idle, 2500 rpm, and load"
    ),
    "Cluster 6 — sensor fault under-detection": (
        "O2/MAF sensor dynamics or plausibility evidence: switch rate, forced rich-lean response, "
        "heater/circuit DTC, or Mode 06 sensor monitor"
    ),
    "Cluster 8 — non-starter": (
        "cranking fuel-pressure / injector-pulse / spark evidence; a warm-idle gas row cannot separate no-start roots"
    ),
    "Cluster 9 — confirming no-fault reliably": (
        "OBD readiness and no-fault confirmation bundle: monitors complete, no pending/permanent DTCs, trims in band, "
        "sensor dynamics nominal"
    ),
}

CSV_FIELD_BY_FAILED_KEY = {
    "obd:hc": "OBD no-fault evidence bundle (not a current v7 CSV scalar column)",
    "obd:obd_lambda": "OBD lambda / sensor-dynamics evidence bundle",
    "obd:co2": "OBD no-fault evidence bundle (not a current v7 CSV scalar column)",
    "no_evidence_satisfied": "rule-specific corroborating OBD/DTC evidence",
}

SOURCE_CONFIRMATION = (
    "owner-confirm: original source-library file is not in-tree; current v7 corpus row and frozen reports "
    "confirm only the populated inputs used here"
)


@dataclass(frozen=True)
class OwnerQueueRow:
    """One quarantined source-library row from the v7 owner-fill queue."""

    case_ref: str
    library_source: str
    missing_input: str
    status: str


@dataclass(frozen=True)
class LocalizationRow:
    """One DATA_GAP row from the frozen localization report."""

    case_id: str
    expected_family: str
    predicted_family: str
    stage: str
    evidence: str


@dataclass(frozen=True)
class DataGapSplit:
    """One DATA_GAP classification row."""

    case_id: str
    expected_code: str
    expected_family: str
    predicted_family: str
    stage: str
    pruned_rule: str
    failed_gating_key: str
    missing_input: str
    verdict: str
    source_ref: str
    source_confirmation: str
    action: str
    missing_physical_quantity: str
    research_cluster: str
    owner_queue_ref: str
    populated_evidence: str
    localization_evidence: str


def _read_csv_rows(csv_path: Path) -> dict[str, dict[str, str]]:
    """Load v7 corpus rows keyed by case id."""
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return {row["case_id"]: row for row in csv.DictReader(handle)}


def _data_gap_rows(localization_path: Path) -> list[LocalizationRow]:
    """Return unique DATA_GAP rows from the localization table only."""
    rows: list[LocalizationRow] = []
    seen: set[str] = set()
    in_table = False
    for line in localization_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Per-case localization table"):
            in_table = True
            continue
        if in_table and line.startswith("---"):
            break
        if not in_table or "| DATA_GAP |" not in line:
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) != 6 or cells[0] in {"case_id", "---"} or cells[0] in seen:
            continue
        seen.add(cells[0])
        rows.append(
            LocalizationRow(
                case_id=cells[0],
                expected_family=cells[1],
                predicted_family=cells[2],
                stage=cells[3],
                evidence=cells[5],
            )
        )
    return rows


def _upstream_records(upstream_path: Path) -> dict[str, Mapping[str, Any]]:
    """Load frozen upstream-evidence records keyed by case id."""
    payload = json.loads(upstream_path.read_text(encoding="utf-8"))
    return {str(row["case_id"]): row for row in payload["records"]}


def _owner_queue(owner_queue_path: Path) -> dict[str, OwnerQueueRow]:
    """Parse the v7 owner-fill queue keyed by exact case ref."""
    rows: dict[str, OwnerQueueRow] = {}
    in_queue = False
    for line in owner_queue_path.read_text(encoding="utf-8").splitlines():
        if line.startswith("## Owner action queue"):
            in_queue = True
            continue
        if in_queue and line.startswith("---"):
            break
        if not in_queue or not line.startswith("|"):
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        if len(cells) != 4 or cells[0] in {"Case ref", "---"}:
            continue
        rows[cells[0]] = OwnerQueueRow(
            case_ref=cells[0],
            library_source=cells[1],
            missing_input=cells[2],
            status=cells[3],
        )
    return rows


def _regex_group(pattern: re.Pattern[str], text: str, default: str) -> str:
    """Return the first regex capture group or a default marker."""
    match = pattern.search(text)
    return match.group(1) if match else default


def _cluster_for(row: LocalizationRow) -> str:
    """Map a DATA_GAP row to its Phase-4 research cluster."""
    if row.case_id == "REAL-002":
        return "Cluster 8 — non-starter"
    return CLUSTER_BY_KEY_OR_FAMILY.get(row.expected_family, "Cluster TBD — data-gap discriminator")


def _populated_evidence(row: Mapping[str, str], upstream: Mapping[str, Any]) -> str:
    """Render compact evidence showing what the current corpus row already contains."""
    gas = (
        f"gas hc={row.get('gas_hc', '—')}, co={row.get('gas_co', '—')}, co2={row.get('gas_co2', '—')}, "
        f"o2={row.get('gas_o2', '—')}, nox={row.get('gas_nox', '—')}, "
        f"lambda={row.get('gas_lambda_measured', '—')}"
    )
    obd_bits = [
        f"shrtft1={row.get('obd_shrtft1') or 'blank'}",
        f"longft1={row.get('obd_longft1') or 'blank'}",
        f"o2_pid={row.get('obd_pid_oxygen_sensor_volts') or 'blank'}",
        f"dtc={row.get('dtc_confirmed_json') or '[]'}",
        f"obd_o2={upstream.get('obd_o2_failure_mode', '—')}",
    ]
    return gas + "; " + ", ".join(obd_bits)


def _split_case(
    loc: LocalizationRow,
    row: Mapping[str, str],
    upstream: Mapping[str, Any],
    owner_rows: Mapping[str, OwnerQueueRow],
) -> DataGapSplit:
    """Classify one DATA_GAP case as corpus-fill or acquisition-gap."""
    failed_key = _regex_group(FAILED_KEY_RE, loc.evidence, "unrecorded")
    pruned_rule = _regex_group(PRUNED_RULE_RE, loc.evidence, "unrecorded")
    owner_row = owner_rows.get(loc.case_id)
    cluster = _cluster_for(loc)
    missing_quantity = MISSING_BY_CLUSTER.get(cluster, "additional discriminating measurement")
    if owner_row is not None:
        verdict = CORPUS_FILL
        missing_input = owner_row.missing_input
        owner_ref = f"{owner_row.case_ref} ({owner_row.status})"
        action = f"Use existing owner-fill queue row `{owner_row.case_ref}`; do not duplicate."
        research_cluster = "—"
    else:
        verdict = ACQUISITION_GAP
        missing_input = CSV_FIELD_BY_FAILED_KEY.get(failed_key, failed_key)
        owner_ref = "—"
        action = f"Phase-4 acquisition: {cluster}."
        research_cluster = cluster
    return DataGapSplit(
        case_id=loc.case_id,
        expected_code=row.get("expected_fault_code", ""),
        expected_family=loc.expected_family,
        predicted_family=loc.predicted_family,
        stage=loc.stage,
        pruned_rule=pruned_rule,
        failed_gating_key=failed_key,
        missing_input=missing_input,
        verdict=verdict,
        source_ref=row.get("source_ref", ""),
        source_confirmation=SOURCE_CONFIRMATION,
        action=action,
        missing_physical_quantity=missing_quantity,
        research_cluster=research_cluster,
        owner_queue_ref=owner_ref,
        populated_evidence=_populated_evidence(row, upstream),
        localization_evidence=loc.evidence,
    )


def build_payload() -> dict[str, Any]:
    """Build the DATA_GAP split payload from frozen on-disk artefacts."""
    rows_by_id = _read_csv_rows(CSV_PATH)
    data_gap_rows = _data_gap_rows(LOCALIZATION_PATH)
    if len(data_gap_rows) != EXPECTED_DATA_GAPS:
        raise RuntimeError(f"expected {EXPECTED_DATA_GAPS} DATA_GAP rows, found {len(data_gap_rows)}")
    upstream_by_id = _upstream_records(UPSTREAM_PATH)
    owner_rows = _owner_queue(OWNER_QUEUE_PATH)
    cases = [
        _split_case(loc, rows_by_id[loc.case_id], upstream_by_id[loc.case_id], owner_rows)
        for loc in data_gap_rows
    ]
    counts = Counter(case.verdict for case in cases)
    if counts[CORPUS_FILL] + counts[ACQUISITION_GAP] != EXPECTED_DATA_GAPS:
        raise RuntimeError("DATA_GAP split counts do not reconcile to 19")
    return {
        "metadata": {
            "task": "T-V3-D3",
            "generated_utc": datetime.now(UTC).isoformat(timespec="seconds"),
            "method": (
                "read-only split of frozen DATA_GAP rows using localization evidence, upstream evidence, "
                "current v7 corpus rows, and the v7 owner-fill queue"
            ),
            "corpus_csv": str(CSV_PATH.relative_to(WORKSPACE_ROOT)),
            "localization": str(LOCALIZATION_PATH.relative_to(WORKSPACE_ROOT)),
            "upstream_evidence": str(UPSTREAM_PATH.relative_to(WORKSPACE_ROOT)),
            "owner_queue": str(OWNER_QUEUE_PATH.relative_to(WORKSPACE_ROOT)),
            "engine_lab_source_edits": False,
        },
        "summary": {
            "total": len(cases),
            CORPUS_FILL: counts[CORPUS_FILL],
            ACQUISITION_GAP: counts[ACQUISITION_GAP],
            "research_clusters": dict(Counter(case.research_cluster for case in cases if case.research_cluster != "—")),
        },
        "cases": [asdict(case) for case in cases],
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
    """Render the DATA_GAP split report."""
    summary = payload["summary"]
    cases = payload["cases"]
    corpus_fill_cases = [case for case in cases if case["verdict"] == CORPUS_FILL]
    acquisition_cases = [case for case in cases if case["verdict"] == ACQUISITION_GAP]
    lines = [
        "# V3_DATA_GAP_SPLIT_2026-06-30 — T-V3-D3",
        "",
        "## Summary",
        "",
        f"- Total DATA_GAP cases: **{summary['total']} / 19**.",
        f"- `{CORPUS_FILL}`: **{summary[CORPUS_FILL]}**.",
        f"- `{ACQUISITION_GAP}`: **{summary[ACQUISITION_GAP]}**.",
        "- Method: compare the frozen DATA_GAP list against the current corpus row and the v7 owner-fill queue.",
        "- Source lock: frozen `FL_LOCALIZATION_2026-06-30` + `FL_UPSTREAM_2026-06-30`; no corpus, lab, engine, oracle, graph, or Vault edits.",
        "- Owner-fill cross-check: no exact DATA_GAP case id is already present in the v7 owner action queue; all 19 are acquisition-scope until the owner confirms an out-of-tree source row has the missing signal.",
        "",
        "## Research-cluster demand",
        "",
        _md_table(["Research cluster", "ACQUISITION_GAP cases"], sorted(summary["research_clusters"].items())),
        "",
        "## Per-case split",
        "",
        _md_table(
            [
                "case_id",
                "expected_code",
                "expected_family",
                "predicted_family",
                "failed gating key",
                "verdict",
                "missing input",
                "source ref",
                "action",
            ],
            [
                [
                    case["case_id"],
                    case["expected_code"],
                    case["expected_family"],
                    case["predicted_family"],
                    case["failed_gating_key"],
                    case["verdict"],
                    case["missing_input"],
                    case["source_ref"],
                    case["action"],
                ]
                for case in cases
            ],
        ),
        "",
        "## CORPUS_FILL cases",
        "",
    ]
    if corpus_fill_cases:
        lines.append(
            _md_table(
                ["case_id", "missing column/field", "owner queue ref", "source confirmation"],
                [
                    [
                        case["case_id"],
                        case["missing_input"],
                        case["owner_queue_ref"],
                        case["source_confirmation"],
                    ]
                    for case in corpus_fill_cases
                ],
            )
        )
    else:
        lines.append(
            "No `CORPUS_FILL` cases. Exact DATA_GAP case ids do not appear in the v7 owner-fill queue; "
            "do not file duplicate owner-fill rows from this task."
        )
    lines.extend(
        [
            "",
            "## ACQUISITION_GAP cases",
            "",
            _md_table(
                ["case_id", "missing physical quantity", "research cluster", "source confirmation"],
                [
                    [
                        case["case_id"],
                        case["missing_physical_quantity"],
                        case["research_cluster"],
                        case["source_confirmation"],
                    ]
                    for case in acquisition_cases
                ],
            ),
            "",
            "## Evidence detail",
            "",
            _md_table(
                ["case_id", "populated evidence", "localization evidence"],
                [
                    [case["case_id"], case["populated_evidence"], case["localization_evidence"]]
                    for case in cases
                ],
            ),
            "",
        ]
    )
    return "\n".join(lines)


def write_artifacts(
    payload: Mapping[str, Any],
    report_path: Path = DEFAULT_REPORT,
    json_path: Path = DEFAULT_JSON,
) -> None:
    """Write deterministic JSON and Markdown artifacts."""
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report_path.write_text(render_report(payload) + "\n", encoding="utf-8")


def main() -> int:
    """Regenerate the DATA_GAP split report."""
    payload = build_payload()
    write_artifacts(payload)
    summary = payload["summary"]
    print(
        "DATA_GAP split: "
        f"{summary['total']} total; "
        f"{CORPUS_FILL}={summary[CORPUS_FILL]}; "
        f"{ACQUISITION_GAP}={summary[ACQUISITION_GAP]}",
    )
    print(f"Wrote {DEFAULT_REPORT.relative_to(WORKSPACE_ROOT)}")
    print(f"Wrote {DEFAULT_JSON.relative_to(WORKSPACE_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
