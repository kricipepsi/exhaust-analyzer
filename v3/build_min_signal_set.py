"""Build the v3 Phase-4 minimum added-signal-set report.

Read-only inverter for T-V3-P4-2. It consumes the T-V3-P4-1 acquisition
spec JSON, groups its corpus columns into concrete shop actions, and emits the
owner-facing acquisition ordering. It does not import or mutate the engine,
registry, corpus, or labs.
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "v3" / "reports"
SPEC_JSON = REPORTS / "V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json"
OUT_MD = REPORTS / "V3_MIN_SIGNAL_SET_2026-07-01.md"
OUT_JSON = REPORTS / "V3_MIN_SIGNAL_SET_2026-07-01.json"

CASE_039_COLUMNS = (
    "koeo_map_baro_delta_kpa",
    "module_voltage_loaded_v",
    "dlc_signal_ground_drop_v",
    "gas_obd_lambda_delta",
    "lambda_perception_delta",
    "bidirectional_fuel_response_ok_bool",
)

C4_SHARED_COLUMNS = (
    "stft_idle_pct",
    "ltft_idle_pct",
    "stft_2500_pct",
    "ltft_2500_pct",
    "stft_load_pct",
    "ltft_load_pct",
    "calc_load_wot_pct",
    "maf_gps_idle",
    "maf_gps_2500",
    "mode06_o2_response_margin_pct",
    "o2_rich_to_lean_ms",
    "o2_lean_to_rich_ms",
    "maf_actual_calc_delta_pct_idle",
    "maf_actual_calc_delta_pct_2500",
    "calc_airflow_gps_idle",
    "calc_airflow_gps_2500",
    "fuel_rail_pressure_load_kpa",
    "wideband_lambda_wot",
)

COST_BY_TIER = {"a": 1, "b": 2, "c": 3, "d": 5}
CORRECTED_CLUSTER_ORDER = ("C2", "C3", "C6", "C9", "C4", "C5", "C8", "C1", "C7")


@dataclass(frozen=True)
class ShopAction:
    """Concrete data-acquisition action and the columns it returns."""

    action_id: str
    name: str
    tier: str
    cost: int
    columns: tuple[str, ...]
    notes: str
    research_basis: str


SHOP_ACTIONS = (
    ShopAction(
        action_id="A1_TRIMS",
        name="Enable live fuel trims at idle and 2500 rpm",
        tier="a",
        cost=COST_BY_TIER["a"],
        columns=("stft_idle_pct", "ltft_idle_pct", "stft_2500_pct", "ltft_2500_pct"),
        notes="Shared OBD Mode $01 start point; reaches C2/C4/C5/C9 but is not alone decisive for any cluster.",
        research_basis="RESEARCH_PROMPT output item 3; cluster4.md §1.7; cluster5.md §Multi-Point Diagnostic Acquisition Protocol",
    ),
    ShopAction(
        action_id="A2_MODE06_EMISSIONS",
        name="Read Mode $06 catalyst, O2, no-fault, and misfire monitors",
        tier="a",
        cost=COST_BY_TIER["a"],
        columns=(
            "mode06_catalyst_margin_pct",
            "catalyst_index_ratio",
            "mode06_min_margin_pct",
            "mode06_o2_response_margin_pct",
            "mode06_misfire_counts_json",
            "misfire_cold_start_seconds",
        ),
        notes="Cheap scan-tool read before any code clear; decisive only when paired with each cluster's corroborating columns.",
        research_basis="cluster2.md §Instrumentation Feasibility Tiers; cluster6.md §Question One Answer; cluster1.md §On-Board Diagnostics Mode 06",
    ),
    ShopAction(
        action_id="A3_OBD_HEALTH",
        name="Capture OBD health/readiness and reset-age counters",
        tier="a",
        cost=COST_BY_TIER["a"],
        columns=(
            "readiness_supported_complete_bool",
            "stored_dtc_count",
            "pending_dtc_count",
            "permanent_dtc_count",
            "warmup_cycles_since_clear",
            "miles_since_clear",
        ),
        notes="No-fault gate; supports C9 only, and unsupported/freshly reset vehicles remain abstained.",
        research_basis="cluster9.1.md §Bottom Line/Decision Rule and cluster9.2.md §Recommended decision rule",
    ),
    ShopAction(
        action_id="A4_MAF_LOAD",
        name="Log MAF/load/airflow plausibility at idle, 2500 rpm, and load",
        tier="a",
        cost=COST_BY_TIER["a"],
        columns=(
            "maf_gps_idle",
            "maf_gps_2500",
            "calc_airflow_gps_idle",
            "calc_airflow_gps_2500",
            "maf_actual_calc_delta_pct_idle",
            "maf_actual_calc_delta_pct_2500",
            "calc_load_wot_pct",
            "stft_load_pct",
            "ltft_load_pct",
            "wideband_lambda_wot",
        ),
        notes="Shared OBD live-PID action for lean/sensor/exhaust-leak splits; WOT/load parts are safety- and vehicle-dependent.",
        research_basis="cluster5.md §Bottom Line Diagnostic Recommendation; cluster6.md §Question Three/Four Answers",
    ),
    ShopAction(
        action_id="A5_CONTROL_PLAUSIBILITY",
        name="Run KOEO MAP/BARO plus control-module voltage/lambda plausibility",
        tier="a/b/c",
        cost=COST_BY_TIER["c"],
        columns=CASE_039_COLUMNS,
        notes="C3 decisive bundle; includes Tier-a/b observations but true confirmation may need DMM/breakout or bidirectional response.",
        research_basis="cluster3.md §Acquisition Protocols/Quantitative Diagnostic Signature Mapping; V3_P4_CLASSIFIER_FIXABLE_RECHECK CASE-039 reroute",
    ),
    ShopAction(
        action_id="A6_TWO_POINT_5GAS",
        name="Use existing 5-gas analyzer differently: two-point/delta/pre-post catalyst/headspace",
        tier="b",
        cost=COST_BY_TIER["b"],
        columns=(
            "pre_post_cat_hc_delta_ppm",
            "pre_post_cat_co_delta_pct",
            "gas_delta_hc_ppm",
            "gas_delta_co_pct",
            "gas_delta_co2_pct",
            "gas_delta_o2_pct",
            "gas_obd_lambda_delta",
            "lambda_perception_delta",
            "cooling_headspace_hc_ppm",
            "two_point_hc_delta_ppm",
            "tailpipe_o2_2500_pct",
        ),
        notes="Reuses the gas bench; completes parts of C1/C2/C3/C9 that static idle gas cannot decide.",
        research_basis="cluster1.md §Comparative Framework; cluster2.md §Protocol; cluster3.md §Quantitative Diagnostic Signature Mapping",
    ),
    ShopAction(
        action_id="A7_CRANKING_BUNDLE",
        name="Collect cranking no-start evidence bundle",
        tier="a/c",
        cost=COST_BY_TIER["c"],
        columns=(
            "crank_rpm",
            "cranking_vacuum_inhg",
            "koeo_fuel_pressure_kpa",
            "cranking_fuel_pressure_kpa",
            "injector_pulse_ms",
            "spark_present_bool",
            "immobilizer_active_bool",
            "relative_compression_min_pct",
        ),
        notes="Special-case no-start workflow; warm-idle gas cannot exist for these rows.",
        research_basis="cluster8.md §Diagnostic Acquisition Protocol/Signature Table",
    ),
    ShopAction(
        action_id="A8_COMPRESSION_LEAKDOWN",
        name="Compression/leak-down or relative-compression mechanical check",
        tier="c",
        cost=COST_BY_TIER["c"],
        columns=("relative_compression_min_pct", "leakdown_pct"),
        notes="Expensive but needed for mechanical-loss separation when Mode $06/headspace/two-point gas is insufficient.",
        research_basis="cluster1.md §Comparative Framework/Critical Signal Evaluation",
    ),
    ShopAction(
        action_id="A9_O2_SCOPE_FALLBACK",
        name="Scope or active rich↔lean O2 response fallback",
        tier="c",
        cost=COST_BY_TIER["c"],
        columns=("o2_rich_to_lean_ms", "o2_lean_to_rich_ms"),
        notes="Escalation when Mode $06 O2 dynamics are absent/equivocal or scan-tool timing is too coarse.",
        research_basis="cluster6.md §Question One/Three/Four Answers",
    ),
    ShopAction(
        action_id="A10_VVT_CAM",
        name="VVT command/actual, cam correlation, and loaded VE capture",
        tier="a/c",
        cost=COST_BY_TIER["c"],
        columns=(
            "vvt_command_deg",
            "vvt_actual_deg",
            "vvt_tracking_error_deg",
            "cam_crank_correlation_deg",
            "ve_idle_pct",
            "ve_2500_load_pct",
            "maf_gps_2500_load",
        ),
        notes="Low-yield but decisive for the cam/VVT residuals; may require OEM tool or scope on generic-PID-poor vehicles.",
        research_basis="cluster7.md §Evaluation/Acquisition Protocol",
    ),
    ShopAction(
        action_id="A11_FUEL_PRESSURE_LOAD",
        name="Fuel-pressure-under-load confirmation where rail PID is absent",
        tier="c",
        cost=COST_BY_TIER["c"],
        columns=("fuel_rail_pressure_load_kpa",),
        notes="Escalates C5/C4 lean-source cases when live PIDs cannot prove fuel delivery shortfall.",
        research_basis="cluster5.md §Multi-Point Diagnostic Acquisition Protocol/Signal Evaluation",
    ),
    ShopAction(
        action_id="A12_BIDIRECTIONAL_RESPONSE",
        name="Bidirectional fuel-response check if passive C3 evidence is contradictory",
        tier="c",
        cost=COST_BY_TIER["c"],
        columns=("bidirectional_fuel_response_ok_bool",),
        notes="Already included in C3 full bundle; listed separately so costly escalation is visible.",
        research_basis="cluster3.md §Evaluation and Ranking of Diagnostic Candidates",
    ),
)


def load_spec() -> dict[str, Any]:
    """Load the P4-1 acquisition spec JSON."""

    return json.loads(SPEC_JSON.read_text(encoding="utf-8"))


def case_rows(spec: dict[str, Any]) -> list[dict[str, Any]]:
    """Return spec rows plus the CASE-039 C3 overlay disclosed by P4-0A."""

    rows = []
    for row in spec["case_unlocks"]:
        copied = dict(row)
        if copied["cluster"] == "C4" and not copied["unlock_columns"]:
            copied["unlock_columns"] = list(C4_SHARED_COLUMNS)
            copied["source_detail"] = f"{copied['source_detail']}; C4 shared C5/C6 columns filled by T-V3-P4-2"
        rows.append(copied)
    rows.append(
        {
            "abstain_if_absent": True,
            "bucket": "PRODUCER_GAP_SIGNAL_REQUIRED",
            "case_id": "CASE-039",
            "cluster": "C3",
            "expected_family": "ecu_fault",
            "predicted_family": "sensor_fault",
            "source_detail": "P4-0A re-bucketed from classifier-fixable to ECU/control signal; winner rich_mixture, expected-family rank absent",
            "source_report": "V3_P4_CLASSIFIER_FIXABLE_RECHECK_2026-07-01.md",
            "unlock_columns": list(CASE_039_COLUMNS),
            "unlock_verdict": "unlockable",
        }
    )
    return rows


def build_column_index(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Invert rows into column -> clusters/cases/actions served."""

    by_column: dict[str, dict[str, Any]] = defaultdict(lambda: {"clusters": set(), "cases": set(), "actions": set()})
    action_by_column = defaultdict(set)
    for action in SHOP_ACTIONS:
        for column in action.columns:
            action_by_column[column].add(action.action_id)

    for row in rows:
        for column in row["unlock_columns"]:
            entry = by_column[column]
            entry["clusters"].add(row["cluster"])
            entry["cases"].add(row["case_id"])
            entry["actions"].update(action_by_column[column])

    return [
        {
            "column": column,
            "clusters": sorted(entry["clusters"]),
            "case_count": len(entry["cases"]),
            "cases": sorted(entry["cases"]),
            "actions": sorted(entry["actions"]),
        }
        for column, entry in sorted(by_column.items())
    ]


def action_summaries(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Compute per-action reach and full-unlock contribution."""

    case_requirements = {row["case_id"]: set(row["unlock_columns"]) for row in rows}
    case_cluster = {row["case_id"]: row["cluster"] for row in rows}
    case_bucket = {row["case_id"]: row["bucket"] for row in rows}
    summaries = []
    for action in SHOP_ACTIONS:
        action_columns = set(action.columns)
        reached = sorted(case_id for case_id, columns in case_requirements.items() if columns & action_columns)
        fully_unlocked = sorted(case_id for case_id, columns in case_requirements.items() if columns <= action_columns)
        clusters = sorted({case_cluster[case_id] for case_id in reached})
        summaries.append(
            {
                "action_id": action.action_id,
                "name": action.name,
                "tier": action.tier,
                "cost": action.cost,
                "columns": list(action.columns),
                "clusters_reached": clusters,
                "case_count_reached": len(reached),
                "cases_reached": reached,
                "full_unlock_case_count": len(fully_unlocked),
                "full_unlock_cases": fully_unlocked,
                "buckets_reached": sorted({case_bucket[case_id] for case_id in reached}),
                "reach_per_cost": round(len(reached) / action.cost, 2),
                "notes": action.notes,
                "research_basis": action.research_basis,
            }
        )
    return summaries


def greedy_order(summaries: list[dict[str, Any]], total_cases: set[str]) -> list[dict[str, Any]]:
    """Rank actions by marginal reached cases per cost, with cumulative coverage."""

    remaining = {item["action_id"]: dict(item) for item in summaries}
    covered: set[str] = set()
    ordered: list[dict[str, Any]] = []
    while covered != total_cases and remaining:
        best_id = max(
            remaining,
            key=lambda action_id: (
                len(set(remaining[action_id]["cases_reached"]) - covered) / remaining[action_id]["cost"],
                len(set(remaining[action_id]["cases_reached"]) - covered),
                -remaining[action_id]["cost"],
                remaining[action_id]["action_id"],
            ),
        )
        item = remaining.pop(best_id)
        marginal = sorted(set(item["cases_reached"]) - covered)
        if not marginal:
            continue
        covered.update(marginal)
        ranked = dict(item)
        ranked["marginal_case_count"] = len(marginal)
        ranked["marginal_cases"] = marginal
        ranked["marginal_per_cost"] = round(len(marginal) / item["cost"], 2)
        ranked["cumulative_case_count"] = len(covered)
        ranked["cumulative_cases"] = sorted(covered)
        ordered.append(ranked)
    return ordered


def cluster_order(rows: list[dict[str, Any]], spec: dict[str, Any]) -> list[dict[str, Any]]:
    """Return corrected cluster ordering from the spec counts plus CASE-039 overlay."""

    overlay_counts = defaultdict(int)
    for row in rows:
        overlay_counts[row["cluster"]] += 1
    spec_counts = spec["cluster_counts"]
    records = []
    for cluster in CORRECTED_CLUSTER_ORDER:
        records.append(
            {
                "cluster": cluster,
                "spec_count": spec_counts.get(cluster, 0),
                "effective_count_with_case_039": overlay_counts[cluster],
                "note": "includes CASE-039 overlay" if cluster == "C3" else "",
            }
        )
    return records


def uncovered_cases(rows: list[dict[str, Any]], summaries: list[dict[str, Any]]) -> list[str]:
    """Return cases not attributed to any shop action."""

    attributed = set()
    for summary in summaries:
        attributed.update(summary["cases_reached"])
    return sorted({row["case_id"] for row in rows} - attributed)


def render_md(payload: dict[str, Any]) -> str:
    """Render the markdown report."""

    lines = [
        "# V3_MIN_SIGNAL_SET_2026-07-01",
        "",
        "**Task:** `T-V3-P4-2`  **Mode:** DISCLOSE only  **Writes engine code:** no",
        "",
        "## Headline",
        "",
        "The cheapest first move is **A1_TRIMS — enable live fuel trims at idle and 2500 rpm**. It reaches 50 residual cases across C2/C4/C5/C9 for one Tier-a OBD action, but it is a shared start, not a standalone unlock. The first full signal pack should still be **T-V3-P4-C2**: C2 has 22 canonical cases, uses that same trim action plus Mode $06 catalyst data, and is cheaper than the C3 control-plausibility bundle. `CASE-039` is folded into C3 as a +1 overlay, so the operating set reconciles to 104 cases.",
        "",
        "## Corrected cluster yield order",
        "",
        "This supersedes `V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md`'s stale `ordered_clusters` for owner sequencing.",
        "",
        "| Rank | Cluster | Spec count | Effective count with CASE-039 | Note |",
        "| ---: | --- | ---: | ---: | --- |",
    ]
    for rank, item in enumerate(payload["corrected_cluster_order"], start=1):
        lines.append(
            f"| {rank} | {item['cluster']} | {item['spec_count']} | {item['effective_count_with_case_039']} | {item['note']} |"
        )

    lines.extend(
        [
            "",
            "## Minimum added-signal set — greedy shop-action order",
            "",
            "Cost scale: Tier-a = 1, Tier-b = 2, Tier-c = 3, Tier-d = 5. `Marginal cases` counts cases newly reached by at least one column from the action. `Full unlock cases` counts cases whose complete current column contract is contained inside that one action. Shared columns lower acquisition cost; they do **not** independently unlock a case until the cluster's decisive producer signal is present.",
            "",
            "| Rank | Action | Tier | Cost | Marginal cases | Marginal / cost | Cumulative cases | Clusters reached | Full unlock cases |",
            "| ---: | --- | --- | ---: | ---: | ---: | ---: | --- | ---: |",
        ]
    )
    for rank, item in enumerate(payload["greedy_order"], start=1):
        lines.append(
            f"| {rank} | {item['action_id']}: {item['name']} | {item['tier']} | {item['cost']} | "
            f"{item['marginal_case_count']} | {item['marginal_per_cost']} | {item['cumulative_case_count']} | "
            f"{', '.join(item['clusters_reached'])} | {item['full_unlock_case_count']} |"
        )

    lines.extend(["", "## Shop-action details", ""])
    for item in payload["actions"]:
        lines.extend(
            [
                f"### {item['action_id']} — {item['name']}",
                "",
                f"- **Tier/cost:** {item['tier']} / {item['cost']}",
                f"- **Columns:** `{', '.join(item['columns'])}`",
                f"- **Clusters reached:** {', '.join(item['clusters_reached']) or 'none'}",
                f"- **Cases reached:** {item['case_count_reached']} ({', '.join(item['cases_reached'])})",
                f"- **Full unlock cases:** {item['full_unlock_case_count']} ({', '.join(item['full_unlock_cases']) or 'none'})",
                f"- **Research basis:** {item['research_basis']}",
                f"- **Caveat:** {item['notes']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Column → served index",
            "",
            "| Column | Clusters | Case count | Shop actions |",
            "| --- | --- | ---: | --- |",
        ]
    )
    for item in payload["column_index"]:
        lines.append(
            f"| `{item['column']}` | {', '.join(item['clusters'])} | {item['case_count']} | {', '.join(item['actions'])} |"
        )

    lines.extend(
        [
            "",
            "## Recommended first pack",
            "",
            "**Author `T-V3-P4-C2` first after owner data lands.** C2 remains the best first commit because its 22-case canonical yield is tied for the largest cluster, it consumes the cheapest shared start (`A1_TRIMS`) plus Tier-a Mode $06 catalyst evidence (`A2_MODE06_EMISSIONS`), and the same acquisition also starts C4/C5/C9. C3 becomes 22 effective cases after `CASE-039`, but its decisive bundle (`A5_CONTROL_PLAUSIBILITY`) may escalate to DMM/breakout or bidirectional tooling, so it is second for acquisition cost even though it is near-tied by yield.",
            "",
            "## Reconciliation and honest gaps",
            "",
            f"- P4-1 residual rows: {payload['source_case_count']}.",
            "- `CASE-039` overlay: +1 C3 ECU/control signal row from `V3_P4_CLASSIFIER_FIXABLE_RECHECK_2026-07-01.md`.",
            f"- Operating rows attributed to at least one shop action: {payload['attributed_case_count']} / {payload['operating_case_count']}.",
            f"- Unattributed cases: {', '.join(payload['uncovered_cases']) or '(none)'}.",
            "- Expensive-to-unlock cases are any row whose first decisive evidence needs Tier-c action (`A5_CONTROL_PLAUSIBILITY`, `A7_CRANKING_BUNDLE`, `A8_COMPRESSION_LEAKDOWN`, `A9_O2_SCOPE_FALLBACK`, `A10_VVT_CAM`, `A11_FUEL_PRESSURE_LOAD`, or `A12_BIDIRECTIONAL_RESPONSE`). They stay abstained until the owner supplies real measurements.",
            "- Shared-column caveat: fuel trims, MAF, Mode $06, and two-point gas lower acquisition cost across clusters, but a case is not unlocked unless its named producer can emit the cluster's decisive state; partial columns are only a cost-efficient start.",
            "- No engine, scorer, oracle, CSV, registry, lab, graph, or `Vault/` file was modified.",
            "",
        ]
    )
    return "\n".join(lines)


def build() -> dict[str, Any]:
    """Build and write the JSON and markdown reports."""

    spec = load_spec()
    rows = case_rows(spec)
    total_cases = {row["case_id"] for row in rows}
    columns = build_column_index(rows)
    actions = action_summaries(rows)
    not_attributed = uncovered_cases(rows, actions)
    payload = {
        "task": "T-V3-P4-2",
        "mode": "DISCLOSE_ONLY_NO_ENGINE_CHANGE",
        "source_spec": str(SPEC_JSON.relative_to(ROOT)),
        "source_case_count": len(spec["case_unlocks"]),
        "operating_case_count": len(rows),
        "case_039_overlay": {
            "cluster": "C3",
            "columns": list(CASE_039_COLUMNS),
            "source": "V3_P4_CLASSIFIER_FIXABLE_RECHECK_2026-07-01.md",
        },
        "corrected_cluster_order": cluster_order(rows, spec),
        "column_index": columns,
        "actions": actions,
        "greedy_order": greedy_order(actions, total_cases),
        "uncovered_cases": not_attributed,
        "attributed_case_count": len(total_cases) - len(not_attributed),
        "shared_column_caveat": "A shared column lowers acquisition cost but does not independently unlock a case; the cluster's decisive producer signal must be present.",
        "recommended_first_pack": "T-V3-P4-C2",
        "recommended_first_acquisition": "A1_TRIMS plus A2_MODE06_EMISSIONS for the C2 producer path",
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUT_MD.write_text(render_md(payload), encoding="utf-8")
    return payload


def main() -> None:
    """Entry point for the read-only report builder."""

    payload = build()
    print(f"Wrote {OUT_MD.relative_to(ROOT)}")
    print(f"Wrote {OUT_JSON.relative_to(ROOT)}")
    print(f"Operating cases attributed: {payload['attributed_case_count']}/{payload['operating_case_count']}")
    print("Corrected order: " + ", ".join(item["cluster"] for item in payload["corrected_cluster_order"]))
    print(f"Recommended first pack: {payload['recommended_first_pack']}")


if __name__ == "__main__":
    main()
