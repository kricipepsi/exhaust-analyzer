"""Build the v3 Phase-4 signal acquisition specification.

Read-only assembler for T-V3-P4-1. It joins the residual reports to the
cluster-level research contracts and emits the markdown + JSON owner data ask.
It intentionally does not import or mutate the engine, registry, corpus, or labs.
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "v3" / "reports"
OUT_MD = REPORTS / "V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md"
OUT_JSON = REPORTS / "V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json"

PRODUCER_REPORT = REPORTS / "V3_PRODUCER_GAP_SPLIT_2026-06-30.md"
DATA_REPORT = REPORTS / "V3_DATA_GAP_SPLIT_2026-06-30.md"
OUTRANKED_REPORT = REPORTS / "V3_OUTRANKED_MAP_2026-06-30.md"
TUNABLE_REPORT = REPORTS / "V3_TUNABLE_REWEIGHT_MAP_2026-07-01.md"

ORDERED_CLUSTERS = ["C2", "C9", "C5", "C8", "C1", "C3", "C6", "C7"]
C4_SHARED_CONTRACT = "C4 is not a new-column ask; its residuals consume the shared C5 trim/load columns and C6 O2/MAF dynamics columns."


@dataclass(frozen=True)
class Contract:
    title: str
    measurement: str
    feasibility: str
    columns: tuple[str, ...]
    units: str
    range_or_enum: str
    maneuver: str
    producer_state: str
    producer_threshold: str
    consumer_rule: str
    separates: str
    abstain_fallback: str
    research_source: str


CONTRACTS: dict[str, Contract] = {
    "C2": Contract(
        title="C2 — rich mixture vs catalyst failure",
        measurement="Mode $06 catalyst monitor + fuel trims; optional pre/post-cat or upstream/downstream O2/5-gas conversion check",
        feasibility="Tier (a) OBD Mode $01/$06 first; Tier (b) existing 5-gas used as dual-point/dual-probe corroboration",
        columns=(
            "mode06_catalyst_margin_pct",
            "catalyst_index_ratio",
            "stft_idle_pct",
            "ltft_idle_pct",
            "stft_2500_pct",
            "ltft_2500_pct",
            "pre_post_cat_hc_delta_ppm",
            "pre_post_cat_co_delta_pct",
        ),
        units="%, ratio, %, %, %, %, ppm, %",
        range_or_enum="margin >= 10% pass-band; index_ratio <= 0.20 pass / high ratio fail; total trim near 0 for catalyst, <= -10% for true rich; nullable if tool unsupported",
        maneuver="Warm closed-loop; hold 2500±100 rpm for 120 s; collect idle trims; read Mode $06 catalyst monitor; if available compare pre/post catalyst gas or upstream/downstream O2 during lean/rich perturbation.",
        producer_state="OBDLab CatalystMonitorState plus GASLab CatalystConversionState",
        producer_threshold="Rich producer emits TRUE_RICH when negative trims are sustained; catalyst producer emits LOW_OSC_OR_HIGH_INDEX when Mode $06 margin/index fails without rich trims.",
        consumer_rule="labs/comlab/registry/rules/rich_mixture.json RM-001/RM-003/RM-004 and catalyst_failure.json CF-001/CF-002/CF-006/CF-007",
        separates="rich_mixture from catalyst_failure, and C2 catalyst-vs-lean/rich runner-ups",
        abstain_fallback="If Mode $06 catalyst data and fuel trims are absent, leave the case abstained; a single downstream tailpipe snapshot is not a discriminator.",
        research_source="cluster2.md §Evaluation/Protocol/Quantitative Signatures",
    ),
    "C9": Contract(
        title="C9 — confirm no fault reliably",
        measurement="OBD health-confirmation bundle: readiness complete, no stored/pending/permanent DTCs, Mode $06 margins, trim stability, two-point gas stability",
        feasibility="Tier (a) OBD Mode $01/$03/$07/$06 plus Mode $0A/Service $09 when supported; Tier (b) two-point 5-gas corroboration",
        columns=(
            "readiness_supported_complete_bool",
            "stored_dtc_count",
            "pending_dtc_count",
            "permanent_dtc_count",
            "mode06_min_margin_pct",
            "warmup_cycles_since_clear",
            "miles_since_clear",
            "stft_idle_pct",
            "ltft_idle_pct",
            "stft_2500_pct",
            "ltft_2500_pct",
            "gas_delta_hc_ppm",
            "gas_delta_co_pct",
            "gas_delta_co2_pct",
            "gas_delta_o2_pct",
        ),
        units="bool, count, count, count, %, cycles, miles, %, %, %, %, ppm, %, %, %",
        range_or_enum="all readiness complete; DTC counts 0; Mode $06 margin >= 10%; warmups>=15 and miles>=200 when available; trims near zero; gas stable",
        maneuver="Warm closed-loop; read OBD status before any clear; capture stable idle and 2500 rpm no-load trim/gas windows.",
        producer_state="OBDLab NoFaultEvidenceState",
        producer_threshold="Emit HEALTH_CONFIRMED only when OBD bundle is complete and non-marginal; otherwise emit HEALTH_UNPROVEN_ABSTAIN.",
        consumer_rule="labs/comlab/registry/rules/no_fault.json NF-001/NF-002",
        separates="no_fault from catalyst-masked, sensor-under-detected, ECU/control, and intermittent pending faults",
        abstain_fallback="If any OBD health evidence is unsupported, incomplete, marginal, contradictory, or freshly reset, leave the case abstained.",
        research_source="cluster9.1.md §Bottom Line/Decision Rule and cluster9.2.md §Recommended decision rule",
    ),
    "C5": Contract(
        title="C5 — lean-condition root cause",
        measurement="STFT/LTFT across idle, 2500 rpm, and load/WOT; calculated load/MAF and fuel pressure under load",
        feasibility="Tier (a) OBD live PIDs where supported; Tier (c) fuel-pressure gauge/transducer where rail pressure PID absent",
        columns=(
            "stft_idle_pct",
            "ltft_idle_pct",
            "stft_2500_pct",
            "ltft_2500_pct",
            "stft_load_pct",
            "ltft_load_pct",
            "calc_load_wot_pct",
            "maf_gps_idle",
            "maf_gps_2500",
            "fuel_rail_pressure_load_kpa",
            "wideband_lambda_wot",
        ),
        units="%, %, %, %, %, %, %, g/s, g/s, kPa, lambda",
        range_or_enum="vacuum leak: trim positive at idle then recovers at 2500; fuel delivery: lean worsens under load with pressure drop >35 kPa; MAF under-read: peak load <80% with positive trims",
        maneuver="Warm closed-loop; 60 s idle; 30 s 2500±100 rpm no-load; safe WOT/load sweep where available; sample >=10 Hz.",
        producer_state="OBDLab LeanRootCauseState",
        producer_threshold="Emit VACUUM_LEAK_TRIM_PATTERN, FUEL_DELIVERY_SHORTFALL, or MAF_UNDERREAD based on multi-point trim/load/pressure signature.",
        consumer_rule="labs/comlab/registry/rules/lean_condition.json LC-001/LC-002/LC-003 plus exhaust_leak.json EL-001 when C4 consumes the shared trim columns",
        separates="lean_condition sub-causes and shared C4 exhaust-leak/true-lean collisions",
        abstain_fallback="If only one warm-idle trim/gas point is available, leave the case abstained.",
        research_source="cluster5.md §Multi-Point Diagnostic Acquisition Protocol/Signal Evaluation",
    ),
    "C8": Contract(
        title="C8 — non-starter root cause",
        measurement="Cranking evidence bundle: RPM, relative compression, cranking vacuum, fuel pressure, injector pulse, spark, immobilizer/security status",
        feasibility="Tier (a) OBD RPM/DTC/freeze-frame where supported; Tier (c) vacuum gauge, fuel-pressure gauge, spark tester, noid light/scope, current clamp",
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
        units="rpm, inHg, kPa, kPa, ms, bool, bool, %",
        range_or_enum="rpm=0 -> CKP path; vacuum <3 inHg or relative compression <85% -> compression; low pressure -> fuel; pulse 0 -> ECU/immobilizer; no spark -> ignition",
        maneuver="No-start crank test; 10-15 s maximum crank with 2 min cooldown; collect OBD while cranking plus shop measurements.",
        producer_state="OBDLab NonStarterCrankState",
        producer_threshold="Emit the no-start substate indicated by the first positive cranking discriminator.",
        consumer_rule="labs/comlab/registry/rules/non_starter.json NS-001/NS-002/NS-003/NS-004",
        separates="non_starter root causes from invalid ambient-air exhaust samples and misfire-like no-starts",
        abstain_fallback="If cranking data are absent, keep no-start rows abstained; warm-idle gas cannot exist for these cases.",
        research_source="cluster8.md §Diagnostic Acquisition Protocol/Signature Table",
    ),
    "C1": Contract(
        title="C1 — mechanical wear vs misfire vs coolant intrusion",
        measurement="Mode $06 per-cylinder misfire/freeze-frame + cooling headspace HC/block test + compression/leak-down or relative compression + two-point HC/O2 behavior",
        feasibility="Tier (a) OBD Mode $06/freeze-frame; Tier (b) existing 5-gas for coolant headspace/two-point tailpipe; Tier (c) compression/leak-down/current clamp",
        columns=(
            "mode06_misfire_counts_json",
            "misfire_cold_start_seconds",
            "cooling_headspace_hc_ppm",
            "relative_compression_min_pct",
            "leakdown_pct",
            "two_point_hc_delta_ppm",
            "tailpipe_o2_2500_pct",
        ),
        units="json, s, ppm, %, %, ppm, %",
        range_or_enum="coolant breach: headspace HC >50 ppm; mechanical loss: compression <90 psi or relative <85%; ignition misfire: elevated O2 around 5% with normal compression; valve-seal plume uses sustained two-point HC, not snap folklore",
        maneuver="Cold-start OBD misfire capture; warm coolant headspace sniff; cranking compression/leak-down; idle then 2500 rpm 5-gas hold.",
        producer_state="OBDLab MisfireLocalizerState plus GASLab MechanicalWearEvidenceState",
        producer_threshold="Emit COOLANT_INTRUSION, COMPRESSION_LOSS, OIL_BURNING_PATTERN, or IGNITION_MISFIRE_CORROBORATED from the combined evidence.",
        consumer_rule="labs/comlab/registry/rules/mechanical_wear.json MW-001/MW-002/MW-003/MW-007/MW-008/MW-009 and misfire.json MF-001/MF-005",
        separates="mechanical_wear from ignition/misfire and coolant-intrusion lookalikes",
        abstain_fallback="If OBD misfire/cooling/compression evidence is not supplied, keep the case abstained rather than using HC alone.",
        research_source="cluster1.md §Comparative Framework/Critical Signal Evaluation",
    ),
    "C3": Contract(
        title="C3 — ECU/control-system fault",
        measurement="KOEO MAP-vs-BARO plausibility, module supply/ground voltage under load, gas-vs-OBD lambda divergence, bidirectional response",
        feasibility="Tier (a) OBD live data for MAP/BARO/trims/voltage; Tier (b) 5-gas for physical lambda; Tier (c) DMM/breakout/bidirectional scan tool",
        columns=(
            "koeo_map_baro_delta_kpa",
            "module_voltage_loaded_v",
            "dlc_signal_ground_drop_v",
            "gas_obd_lambda_delta",
            "lambda_perception_delta",
            "bidirectional_fuel_response_ok_bool",
        ),
        units="kPa, V, V, lambda, lambda, bool",
        range_or_enum="MAP-BARO delta >=5 kPa, ground drop >0.20 V, ground joint >0.10 V, lambda divergence >=0.05, trims railed ±25%, active response absent/reversed",
        maneuver="KOEO pressure/voltage gate; high electrical load ground test; warm closed-loop 5-gas+OBD capture; optional +25%/-12.5% fuel command response.",
        producer_state="OBDLab ControlPlausibilityState",
        producer_threshold="Emit CONTROL_REFERENCE_FAULT when electrical/reference or gas-vs-OBD divergence gates pass.",
        consumer_rule="labs/comlab/registry/rules/ecu_fault.json EF-001/EF-002/EF-003 and sensor_fault.json SF-001/SF-002 when dispersion presents as sensor bias",
        separates="ecu_fault/control dispersion from true lean/rich/sensor/catalyst chemistry",
        abstain_fallback="If no KOEO plausibility or voltage/divergence data are supplied, keep control-dispersion cases abstained.",
        research_source="cluster3.md §Acquisition Protocols/Quantitative Diagnostic Signature Mapping",
    ),
    "C6": Contract(
        title="C6 — sensor fault under-detection",
        measurement="Mode $06 O2-sensor dynamics with rich↔lean response fallback; MAF actual-vs-calculated airflow plausibility",
        feasibility="Tier (a) OBD Mode $06/live PIDs when decisive; Tier (c) scope for millisecond response or missing scan-tool dynamics",
        columns=(
            "mode06_o2_response_margin_pct",
            "o2_rich_to_lean_ms",
            "o2_lean_to_rich_ms",
            "maf_actual_calc_delta_pct_idle",
            "maf_actual_calc_delta_pct_2500",
            "maf_gps_idle",
            "maf_gps_2500",
            "calc_airflow_gps_idle",
            "calc_airflow_gps_2500",
        ),
        units="%, ms, ms, %, %, g/s, g/s, g/s, g/s",
        range_or_enum="use vehicle Mode $06 limits; O2 slower than OEM limit is fault; MAF sustained >10-15% low vs modeled airflow at both points is provisional fault",
        maneuver="Warm closed-loop; read Mode $06; if absent/equivocal, hold ~2500 rpm then decel fuel cut and controlled return; capture MAF/MAP/IAT/BARO/RPM at idle and 2500.",
        producer_state="OBDLab SensorDynamicsState",
        producer_threshold="Emit O2_LAZY_OR_BIASED, MAF_UNDERREAD, or SENSOR_HEALTH_UNPROVEN_ABSTAIN.",
        consumer_rule="labs/comlab/registry/rules/sensor_fault.json SF-005/SF-008/SF-001/SF-002 and no_fault.json NF-001/NF-002 for healthy-vs-under-detected split",
        separates="sensor_fault from no_fault, misfire, lean, and catalyst lookalikes",
        abstain_fallback="If only static O2/MAF values are supplied, keep the case abstained.",
        research_source="cluster6.md §Question One/Three/Four Answers",
    ),
    "C7": Contract(
        title="C7 — cam timing / VVT fault",
        measurement="VVT command-vs-actual angle, cam-to-crank correlation, VE/MAF-at-RPM signature",
        feasibility="Tier (a) OBD live data/DTC/freeze-frame when supported; Tier (c) scope/OEM tool for cam correlation if generic PIDs unavailable",
        columns=(
            "vvt_command_deg",
            "vvt_actual_deg",
            "vvt_tracking_error_deg",
            "cam_crank_correlation_deg",
            "ve_idle_pct",
            "ve_2500_load_pct",
            "maf_gps_2500_load",
        ),
        units="deg, deg, deg, deg, %, %, g/s",
        range_or_enum="tracking error beyond OEM tolerance; cam-crank correlation fault/P0016-class; depressed VE/MAF at 2500 load compared with expected displacement/RPM model",
        maneuver="Warm engine; baseline idle; WOT or loaded sweep; 2500±50 rpm at 50-70% calculated load for 30 s; sample >=10 Hz.",
        producer_state="OBDLab CamVvtEvidenceState plus GASLab CamTimingState",
        producer_threshold="Emit VVT_TRACKING_FAULT, STATIC_CAM_CORRELATION_FAULT, or VE_DEPRESSED_CAM_TIMING_PATTERN.",
        consumer_rule="labs/comlab/registry/rules/cam_timing.json CT-001/CT-002/CT-004/CT-005/CT-007/CT-008",
        separates="cam_timing/VVT from misfire, sensor, and chemically non-normal exhaust",
        abstain_fallback="If cam/VVT or VE evidence is unavailable, keep cam-timing residuals abstained.",
        research_source="cluster7.md §Evaluation/Acquisition Protocol",
    ),
}

CLUSTER_LABELS = {
    "Cluster 1": "C1",
    "Cluster 2": "C2",
    "Cluster 3": "C3",
    "Cluster 4": "C4",
    "Cluster 5": "C5",
    "Cluster 6": "C6",
    "Cluster 7": "C7",
    "Cluster 8": "C8",
    "Cluster 9": "C9",
}


def parse_tables(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    headers: list[str] | None = None
    for raw in path.read_text().splitlines():
        if not raw.startswith("|"):
            continue
        cells = [cell.strip() for cell in raw.strip().strip("|").split("|")]
        if not cells:
            continue
        if all(set(cell) <= {"-", ":", " "} for cell in cells):
            continue
        first = cells[0].lower()
        if first in {"case_id", "case id"}:
            headers = cells
            continue
        if headers and len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    return rows


def cluster_from_text(text: str) -> str:
    for label, cluster in CLUSTER_LABELS.items():
        if label in text:
            return cluster
    raise ValueError(f"No cluster label in {text!r}")


def unique_by_case(rows: list[dict[str, str]], case_key: str) -> list[dict[str, str]]:
    out: dict[str, dict[str, str]] = {}
    for row in rows:
        case_id = row.get(case_key, "")
        if case_id and case_id not in out:
            out[case_id] = row
    return list(out.values())


def hard_cluster(expected: str, winner: str) -> str:
    pair = {expected, winner}
    if expected == "no_fault":
        return "C9"
    if expected == "non_starter":
        return "C8"
    if "cam_timing" in pair:
        return "C7"
    if expected == "ecu_fault":
        return "C3"
    if expected in {"mechanical_wear", "ignition_fault", "misfire"}:
        return "C1"
    if "catalyst_failure" in pair or "rich_mixture" in pair:
        return "C2"
    if expected == "sensor_fault":
        return "C6"
    if expected == "lean_condition":
        return "C5"
    if expected == "exhaust_leak":
        return "C4"
    return "UNMAPPED"


def tunable_cluster_map() -> dict[str, str]:
    rows = parse_tables(TUNABLE_REPORT)
    mapping: dict[str, str] = {}
    for row in rows:
        case_id = row.get("Case ID", "")
        discriminator = row.get("Research Cluster", "")
        if case_id and discriminator.startswith("Cluster"):
            mapping[case_id] = cluster_from_text(discriminator)
    return mapping


def collect_cases() -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []

    producer_rows = [
        row
        for row in unique_by_case(parse_tables(PRODUCER_REPORT), "case_id")
        if row.get("verdict") == "SIGNAL_REQUIRED"
    ]
    for row in producer_rows:
        cluster = cluster_from_text(row["research cluster"])
        cases.append(
            {
                "case_id": row["case_id"],
                "bucket": "PRODUCER_GAP_SIGNAL_REQUIRED",
                "cluster": cluster,
                "expected_family": row["expected_family"],
                "predicted_family": None,
                "unlock_columns": list(CONTRACTS[cluster].columns),
                "unlock_verdict": "unlockable",
                "abstain_if_absent": True,
                "source_report": PRODUCER_REPORT.name,
                "source_detail": row["missing quantity"],
            }
        )

    data_rows = [
        row
        for row in unique_by_case(parse_tables(DATA_REPORT), "case_id")
        if row.get("verdict") == "ACQUISITION_GAP"
    ]
    for row in data_rows:
        cluster = cluster_from_text(row["action"])
        cases.append(
            {
                "case_id": row["case_id"],
                "bucket": "DATA_GAP_ACQUISITION_GAP",
                "cluster": cluster,
                "expected_family": row["expected_family"],
                "predicted_family": row["predicted_family"],
                "unlock_columns": list(CONTRACTS[cluster].columns),
                "unlock_verdict": "unlockable",
                "abstain_if_absent": True,
                "source_report": DATA_REPORT.name,
                "source_detail": row["missing input"],
            }
        )

    hard_rows = [
        row
        for row in unique_by_case(parse_tables(OUTRANKED_REPORT), "case_id")
        if row.get("bucket") == "HARD"
    ]
    for row in hard_rows:
        cluster = hard_cluster(row["expected_family"], row["winner_family"])
        columns = (
            [*CONTRACTS["C5"].columns, *CONTRACTS["C6"].columns]
            if cluster == "C4"
            else list(CONTRACTS[cluster].columns)
            if cluster in CONTRACTS
            else []
        )
        cases.append(
            {
                "case_id": row["case_id"],
                "bucket": "OUTRANKED_HARD",
                "cluster": cluster,
                "expected_family": row["expected_family"],
                "predicted_family": row["winner_family"],
                "unlock_columns": columns,
                "unlock_verdict": "unlockable_shared_contract" if cluster == "C4" else "unlockable" if columns else "honest_gap",
                "abstain_if_absent": True,
                "source_report": OUTRANKED_REPORT.name,
                "source_detail": f"expected_rank={row['rank']}; expected_rule={row['expected_rule']}; winner_rule={row['winner_rule']}",
            }
        )

    citation_clusters = tunable_cluster_map()
    tunable_rows = [
        row
        for row in unique_by_case(parse_tables(TUNABLE_REPORT), "Case ID")
        if row.get("Verdict") in {"**SIGNAL-GATED**", "**RISKY**", "**HARD**"}
    ]
    for row in tunable_rows:
        cluster = citation_clusters[row["Case ID"]]
        columns = list(CONTRACTS[cluster].columns) if cluster in CONTRACTS else []
        cases.append(
            {
                "case_id": row["Case ID"],
                "bucket": "TUNABLE_HELD",
                "cluster": cluster,
                "expected_family": row["Expected Family (Rule)"].split()[0],
                "predicted_family": row["Winner Family (Rule)"].split()[0],
                "unlock_columns": columns,
                "unlock_verdict": "unlockable" if columns else "unlockable_shared_contract",
                "abstain_if_absent": True,
                "source_report": TUNABLE_REPORT.name,
                "source_detail": f"{row['Verdict']}; {row['Regressions / Absent PIDs']}",
            }
        )

    return sorted(cases, key=lambda row: (row["cluster"], row["bucket"], row["case_id"]))


def bucket_counts(cases: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for row in cases:
        counts[row["bucket"]] += 1
    return dict(sorted(counts.items()))


def cluster_cases(cases: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in cases:
        grouped[row["cluster"]].append(row)
    return dict(sorted(grouped.items()))


def validate(cases: list[dict[str, Any]]) -> None:
    counts = bucket_counts(cases)
    expected = {
        "PRODUCER_GAP_SIGNAL_REQUIRED": 23,
        "DATA_GAP_ACQUISITION_GAP": 19,
        "OUTRANKED_HARD": 49,
        "TUNABLE_HELD": 12,
    }
    if counts != expected:
        raise SystemExit(f"Residual mismatch: {counts!r} != {expected!r}")
    missing = [row for row in cases if row["cluster"] not in {*ORDERED_CLUSTERS, "C4"}]
    if missing:
        raise SystemExit(f"Unmapped cases: {missing!r}")


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(cell).replace("\n", "<br>") for cell in row) + " |")
    return "\n".join(out)


def build_markdown(cases: list[dict[str, Any]]) -> str:
    grouped = cluster_cases(cases)
    cumulative = 0
    headline_rows: list[list[Any]] = []
    for cluster in ORDERED_CLUSTERS:
        contract = CONTRACTS[cluster]
        count = len(grouped.get(cluster, []))
        cumulative += count
        headline_rows.append(
            [
                cluster,
                contract.measurement,
                contract.feasibility,
                ", ".join(contract.columns),
                contract.producer_state,
                contract.consumer_rule,
                count,
                cumulative,
            ]
        )

    c4_count = len(grouped.get("C4", []))
    bucket_summary = bucket_counts(cases)
    text: list[str] = [
        "# V3_SIGNAL_ACQUISITION_SPEC_2026-07-01",
        "",
        "**Task:** `T-V3-P4-1`  **Mode:** DISCLOSE only  **Writes engine code:** no",
        "",
        "This is the owner data-acquisition contract for Phase 4. It names the corpus columns, producer state, consumer rule, cases unlocked, and abstain fallback for each signal pack. It does not add corpus columns, synthesize values, modify rules, or change the yardstick.",
        "",
        "## Tier 1 — headline acquisition matrix",
        "",
        markdown_table(
            [
                "Cluster",
                "Measurement",
                "Feasibility",
                "New corpus column(s)",
                "Producer state",
                "Consumer rule",
                "Residual cases mapped",
                "Running cumulative",
            ],
            headline_rows,
        ),
        "",
        f"**C4 note:** {C4_SHARED_CONTRACT} C4 residual cases mapped in Tier 3: **{c4_count}**.",
        "",
        "**Reconciliation:** residual rows mapped = "
        f"{len(cases)} = PRODUCER_GAP·SIGNAL_REQUIRED {bucket_summary['PRODUCER_GAP_SIGNAL_REQUIRED']} + "
        f"DATA_GAP·ACQUISITION_GAP {bucket_summary['DATA_GAP_ACQUISITION_GAP']} + "
        f"OUTRANKED·HARD {bucket_summary['OUTRANKED_HARD']} + "
        f"TUNABLE_HELD {bucket_summary['TUNABLE_HELD']}. "
        "No engine/scorer/oracle/CSV/registry/lab file is modified; cases without supplied signal stay abstained.",
        "",
        "## Tier 2 — per-cluster contracts",
        "",
    ]

    for cluster in ORDERED_CLUSTERS:
        contract = CONTRACTS[cluster]
        rows = grouped.get(cluster, [])
        case_ids = ", ".join(row["case_id"] for row in rows) or "—"
        bucket_text = ", ".join(f"{name}={sum(1 for row in rows if row['bucket'] == name)}" for name in sorted({row["bucket"] for row in rows})) or "none"
        text.extend(
            [
                f"### {contract.title}",
                "",
                f"1. **Discriminating measurement:** {contract.measurement}",
                f"2. **Corpus column contract:** `{', '.join(contract.columns)}`. Units: {contract.units}. Allowed range/enum: {contract.range_or_enum}. Acquisition maneuver: {contract.maneuver}",
                f"3. **Producer state:** {contract.producer_state}. Bound/threshold: {contract.producer_threshold}",
                f"4. **Consumer rule:** {contract.consumer_rule}. Separates: {contract.separates}.",
                f"5. **Cases unlocked:** {len(rows)} mapped residual rows ({bucket_text}): {case_ids}.",
                f"6. **Abstain fallback:** {contract.abstain_fallback}",
                f"**Research source:** `{contract.research_source}`.",
                "",
            ]
        )

    if c4_count:
        c4_rows = grouped["C4"]
        text.extend(
            [
                "### C4 — shared residual note (not a separate new-column ask)",
                "",
                C4_SHARED_CONTRACT,
                "",
                "C4 cases: " + ", ".join(row["case_id"] for row in c4_rows) + ".",
                "Producer/consumer path: C5 `LeanRootCauseState` for true-lean vs load/trim behavior plus C6 `SensorDynamicsState` for biased/lazy O2 behavior; consumers are `EL-001/EL-003`, `LC-001/LC-002`, and `SF-001/SF-002/SF-008` in the existing registry rule families.",
                "Abstain fallback: absent shared trim/load/O2 dynamics, these stay abstained; no independent C4 corpus column is requested here.",
                "",
            ]
        )

    leftovers = [row for row in cases if row["unlock_verdict"] == "honest_gap"]
    text.extend(
        [
            "## Tier 3 — JSON per-case unlock table",
            "",
            f"Machine-readable table: `{OUT_JSON.relative_to(ROOT)}`.",
            "",
            "## Honest gaps and abstain policy",
            "",
        ]
    )
    if leftovers:
        text.append("Residual cases not unlockable by any listed signal: " + ", ".join(row["case_id"] for row in leftovers) + ".")
    else:
        text.append("No residual row is left unmapped. All mapped rows remain `abstain-if-absent` until the owner supplies the named real measurement; no synthetic value may be filled.")
    text.append("")
    return "\n".join(text)


def build_json(cases: list[dict[str, Any]]) -> dict[str, Any]:
    grouped = cluster_cases(cases)
    return {
        "task": "T-V3-P4-1",
        "generated": "2026-07-01",
        "mode": "DISCLOSE_ONLY_NO_ENGINE_CHANGE",
        "ordered_clusters": ORDERED_CLUSTERS,
        "bucket_reconciliation": bucket_counts(cases),
        "cluster_counts": {cluster: len(grouped.get(cluster, [])) for cluster in [*ORDERED_CLUSTERS, "C4"]},
        "contracts": {
            cluster: {
                "title": contract.title,
                "measurement": contract.measurement,
                "feasibility": contract.feasibility,
                "columns": list(contract.columns),
                "units": contract.units,
                "range_or_enum": contract.range_or_enum,
                "maneuver": contract.maneuver,
                "producer_state": contract.producer_state,
                "producer_threshold": contract.producer_threshold,
                "consumer_rule": contract.consumer_rule,
                "separates": contract.separates,
                "abstain_fallback": contract.abstain_fallback,
                "research_source": contract.research_source,
            }
            for cluster, contract in CONTRACTS.items()
        },
        "shared_c4_contract": C4_SHARED_CONTRACT,
        "case_unlocks": cases,
    }


def main() -> None:
    cases = collect_cases()
    validate(cases)
    OUT_JSON.write_text(json.dumps(build_json(cases), indent=2, sort_keys=True) + "\n")
    OUT_MD.write_text(build_markdown(cases))
    print(f"Wrote {OUT_MD}")
    print(f"Wrote {OUT_JSON}")
    print(json.dumps({"bucket_reconciliation": bucket_counts(cases), "total": len(cases)}, sort_keys=True))


if __name__ == "__main__":
    main()
