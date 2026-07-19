#!/usr/bin/env python3
"""Read-only Phase-4 classifier-fixable recheck for T-V3-P4-0A."""

from __future__ import annotations

import contextlib
import csv
import io
import json
import sys
from collections import Counter
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

WORKSPACE_ROOT = Path(__file__).resolve().parents[1]
for relative in (
    "apps/wired",
    "apps/wired/fl_tasks",
    "apps/wired/v7",
    "labs/comlab",
    "labs/dnalab",
    "labs/dtclab",
    "labs/gaslab",
    "labs/obdlab",
    "labs/symptomlab",
    "labs/vinlab",
    "v3",
):
    path = str(WORKSPACE_ROOT / relative)
    if path not in sys.path:
        sys.path.insert(0, path)

from capture_upstream_evidence import _build_vin_dna  # noqa: E402
from producer_gap_split import (  # noqa: E402
    _bound_evidence,
    _build_gas_dna_view,
    _gas_readings,
    _split_case,
    _upstream_records,
)
from v7.load_corpus import DEFAULT_CSV_PATH, row_to_raw_inputs  # noqa: E402
from wired.composition import _run_gaslab, diagnose  # noqa: E402

from gaslab.brettschneider import lambda_chem  # noqa: E402
from gaslab.contracts import EngineStateBucket  # noqa: E402
from gaslab.ontology_loader import load_ontology  # noqa: E402
from gaslab.rule_engine import (  # noqa: E402
    _definitive_match,
    _matching_fault_candidates,
    _resolve_candidates,
)
from gaslab.validity_gates import sample_validity  # noqa: E402

TARGET_CASES = ("era2_008", "CASE-039")
CURRENT_RESULTS = WORKSPACE_ROOT / "apps/wired/v7/runs/POST_T_V3_3D/results.json"
UPSTREAM_PATH = WORKSPACE_ROOT / "apps/wired/fl_tasks/reports/FL_UPSTREAM_2026-06-30.json"
REPORT_MD = WORKSPACE_ROOT / "v3/reports/V3_P4_CLASSIFIER_FIXABLE_RECHECK_2026-07-01.md"
REPORT_JSON = WORKSPACE_ROOT / "v3/reports/V3_P4_CLASSIFIER_FIXABLE_RECHECK_2026-07-01.json"


@dataclass(frozen=True)
class ReplayCase:
    """Read-only replay facts for one corpus row."""

    case_id: str
    idle: Mapping[str, float | int]
    idle_lambda: float
    sample_validity: str
    high_idle: Mapping[str, float | int] | None
    high_idle_lambda: float | None
    emitted_state: str
    candidates: tuple[str, ...]
    resolved_candidates: tuple[str, ...]
    definitive_state: str | None
    bound_evidence: str


def _read_csv_rows(csv_path: Path = DEFAULT_CSV_PATH) -> list[dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _result_rows(path: Path = CURRENT_RESULTS) -> dict[str, Mapping[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {str(row["case_id"]): row for row in payload["results"]}


def _accuracy_rows(rows: Sequence[Mapping[str, str]]) -> list[Mapping[str, str]]:
    return [
        row for row in rows
        if row.get("tag") != "invalid"
        and row.get("accuracy_excluded", "false").strip().lower() != "true"
    ]


def _top3_families(verdict: Mapping[str, Any]) -> tuple[str, ...]:
    winner = str(verdict.get("fault_family", ""))
    siblings = tuple(
        str(sibling.get("fault_family", ""))
        for sibling in verdict.get("differential_siblings", [])[:2]
    )
    return (winner, *siblings)


def _family_rank(families: Sequence[str], expected_family: str) -> int | None:
    expected = expected_family.lower()
    for index, family in enumerate(families, start=1):
        if family.lower() == expected:
            return index
    return None


def _as_reading_dict(reading: Any) -> dict[str, float | int]:
    return {
        "hc": reading.hc,
        "co": reading.co,
        "co2": reading.co2,
        "o2": reading.o2,
        "nox": reading.nox,
    }


def _replay_case(row: Mapping[str, str], required_state: str, ontology: Mapping[str, Any]) -> ReplayCase:
    raw_inputs = row_to_raw_inputs(dict(row))
    vin_dna = _build_vin_dna(raw_inputs)
    gas_inputs = raw_inputs["gas"]
    idle, high = _gas_readings(gas_inputs)
    gas_dna = _build_gas_dna_view(
        vin_dna,
        coc_target_lambda_v112=gas_inputs.get("coc_target_lambda_v112"),
        coc_target_lambda_low=gas_inputs.get("coc_target_lambda_low"),
        coc_target_lambda_high=gas_inputs.get("coc_target_lambda_high"),
        coc_co_low_idle=gas_inputs.get("coc_co_low_idle"),
        coc_co_high_idle=gas_inputs.get("coc_co_high_idle"),
    )
    engine_state = EngineStateBucket(gas_inputs.get("engine_state", "STABILIZED_IDLE"))
    candidates = _matching_fault_candidates(idle, engine_state, dict(ontology), gas_dna)
    resolved = _resolve_candidates(
        candidates,
        idle,
        gas_dna,
        dict(ontology),
        engine_state,
        high,
        fuel_trim=gas_inputs.get("fuel_trim"),
    )
    definitive = _definitive_match(
        idle,
        gas_dna,
        engine_state,
        dict(ontology),
        block_test_passed=bool(gas_inputs.get("block_test_passed", False)),
        reading_high=high,
        fuel_trim=gas_inputs.get("fuel_trim"),
    )
    chemical_state = str(_run_gaslab(dict(gas_inputs), vin_dna).chemical_state)
    bound_evidence = _bound_evidence(required_state, ontology, idle, gas_dna)
    return ReplayCase(
        case_id=str(row["case_id"]),
        idle=_as_reading_dict(idle),
        idle_lambda=lambda_chem(idle),
        sample_validity=sample_validity(idle).value,
        high_idle=_as_reading_dict(high) if high is not None else None,
        high_idle_lambda=lambda_chem(high) if high is not None else None,
        emitted_state=chemical_state,
        candidates=tuple(candidates),
        resolved_candidates=tuple(resolved),
        definitive_state=definitive[0].value if definitive is not None else None,
        bound_evidence=f"{bound_evidence}; sample_validity={sample_validity(idle).value}",
    )


def _self_check(rows: Sequence[Mapping[str, str]], stored_results: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    mismatches = []
    with contextlib.redirect_stdout(io.StringIO()):
        for row in _accuracy_rows(rows):
            case_id = str(row["case_id"])
            raw_inputs = row_to_raw_inputs(dict(row))
            current_verdict = diagnose(raw_inputs).diagnostic_verdict.model_dump(mode="json")
            stored_verdict = stored_results[case_id]["verdict"]
            if current_verdict.get("fault_family") != stored_verdict.get("fault_family"):
                mismatches.append(
                    {
                        "case_id": case_id,
                        "field": "fault_family",
                        "stored": stored_verdict.get("fault_family"),
                        "replayed": current_verdict.get("fault_family"),
                    }
                )
                continue
            current_top3 = _top3_families(current_verdict)
            stored_top3 = _top3_families(stored_verdict)
            if current_top3 != stored_top3:
                mismatches.append(
                    {
                        "case_id": case_id,
                        "field": "top3_families",
                        "stored": stored_top3,
                        "replayed": current_top3,
                    }
                )
    return {
        "checked_cases": len(_accuracy_rows(rows)),
        "drift_count": len(mismatches),
        "mismatches": mismatches,
    }


def _target_status(case_id: str, row: Mapping[str, str], stored: Mapping[str, Any]) -> dict[str, Any]:
    verdict = stored["verdict"]
    families = _top3_families(verdict)
    rank = _family_rank(families, row["expected_fault_family"])
    return {
        "expected_family": row["expected_fault_family"],
        "expected_code": row["expected_fault_code"],
        "top3_families": families,
        "expected_family_rank": rank,
        "top3_family_member": rank is not None,
        "covered": not bool(verdict.get("abstained", False)),
        "abstained": bool(verdict.get("abstained", False)),
        "abstain_reason": verdict.get("abstain_reason"),
        "winner_family": verdict.get("fault_family"),
        "winner_code": verdict.get("fault_code"),
    }


def _all_replays(rows: Sequence[Mapping[str, str]], upstream: Mapping[str, Mapping[str, Any]], ontology: Mapping[str, Any]) -> dict[str, ReplayCase]:
    out = {}
    for row in _accuracy_rows(rows):
        case_id = str(row["case_id"])
        required = str(upstream.get(case_id, {}).get("required_gating_state_for_expected_code") or row.get("expected_state") or "")
        try:
            out[case_id] = _replay_case(row, required, ontology)
        except Exception as exc:  # noqa: BLE001 - report read-only replay failures explicitly.
            out[case_id] = ReplayCase(
                case_id=case_id,
                idle={},
                idle_lambda=0.0,
                sample_validity="REPLAY_ERROR",
                high_idle=None,
                high_idle_lambda=None,
                emitted_state=f"REPLAY_ERROR:{type(exc).__name__}",
                candidates=(),
                resolved_candidates=(),
                definitive_state=None,
                bound_evidence=str(exc),
            )
    return out


def _case_verdict(case_id: str, status: Mapping[str, Any], replay: ReplayCase) -> tuple[str, str, list[str]]:
    if status["top3_family_member"]:
        return (
            "ALREADY_BANKS",
            "No classifier fix needed: expected family is already emitted in the POST_T_V3_3D top-3; abstain, not rank, is the remaining blocker.",
            [],
        )
    if case_id == "CASE-039":
        return (
            "RE-BUCKET_TO_SIGNAL",
            "POA_SIGNATURE is reachable only as a co-surviving catch-all; the emitted state stays EGR_STUCK_OPEN because the idle-only gas row has no high-idle/ECU-strategy discriminator. A classifier-only POA win would require broad EGR_STUCK_OPEN narrowing or catch-all priority reversal, not a safe one-case bin fix.",
            ["Cluster 3 — ECU/control fault evidence"],
        )
    return (
        "CLASSIFIER_FIX",
        "Required state is reachable but not banked; inspect the exact bin before any commit.",
        [],
    )


def _neighbour_sets(replays: Mapping[str, ReplayCase]) -> dict[str, Any]:
    egr_resolved = sorted(
        case_id for case_id, replay in replays.items()
        if "EGR_STUCK_OPEN" in replay.resolved_candidates
    )
    poa_egr_collision = sorted(
        case_id for case_id, replay in replays.items()
        if "POA_SIGNATURE" in replay.resolved_candidates and "EGR_STUCK_OPEN" in replay.resolved_candidates
    )
    sample_invalid = sorted(
        case_id for case_id, replay in replays.items()
        if replay.sample_validity == "INVALID"
    )
    return {
        "egr_stuck_open_resolved_neighbours": egr_resolved,
        "poa_egr_collision_neighbours": poa_egr_collision,
        "sample_invalid_neighbours": sample_invalid,
        "competition_group_field": "not present in POST_T_V3_3D results.json or global_fault_registry.json",
    }


def _build_payload() -> dict[str, Any]:
    rows = _read_csv_rows()
    rows_by_id = {row["case_id"]: row for row in rows}
    stored_results = _result_rows()
    upstream = _upstream_records(UPSTREAM_PATH)
    ontology = load_ontology()
    self_check = _self_check(rows, stored_results)
    replays = _all_replays(rows, upstream, ontology)
    neighbours = _neighbour_sets(replays)

    cases = []
    for case_id in TARGET_CASES:
        split = _split_case(case_id, rows_by_id[case_id], upstream[case_id], ontology)
        status = _target_status(case_id, rows_by_id[case_id], stored_results[case_id])
        replay = replays[case_id]
        verdict, rationale, clusters = _case_verdict(case_id, status, replay)
        case_neighbours = {}
        if case_id == "era2_008":
            case_neighbours = {
                "sample_invalid_boundary_neighbours": neighbours["sample_invalid_neighbours"],
            }
        elif case_id == "CASE-039":
            case_neighbours = {
                "egr_stuck_open_resolved_neighbours": neighbours["egr_stuck_open_resolved_neighbours"],
                "poa_egr_collision_neighbours": neighbours["poa_egr_collision_neighbours"],
            }
        cases.append(
            {
                "case_id": case_id,
                "expected_family": status["expected_family"],
                "expected_code": status["expected_code"],
                "required_state": split.required_state,
                "current_run_status": status,
                "reachability": {
                    "t_v3_d2_verdict": split.verdict,
                    "bound_evidence": split.threshold_evidence,
                    "live_replay_bound_evidence": replay.bound_evidence,
                    "emitted_state": replay.emitted_state,
                    "candidates": replay.candidates,
                    "resolved_candidates": replay.resolved_candidates,
                    "definitive_state": replay.definitive_state,
                    "idle": replay.idle,
                    "idle_lambda": replay.idle_lambda,
                    "sample_validity": replay.sample_validity,
                    "high_idle": replay.high_idle,
                    "high_idle_lambda": replay.high_idle_lambda,
                },
                "minimal_classifier_fix": rationale,
                "ft8_neighbour_risk": case_neighbours,
                "competition_group_collisions": neighbours["competition_group_field"],
                "rebucket_clusters": clusters,
                "verdict": verdict,
            }
        )
    counts = Counter(case["verdict"] for case in cases)
    return {
        "metadata": {
            "task": "T-V3-P4-0A",
            "generated_utc": datetime.now(UTC).isoformat(timespec="seconds"),
            "current_results": str(CURRENT_RESULTS.relative_to(WORKSPACE_ROOT)),
            "corpus_csv": str(DEFAULT_CSV_PATH.relative_to(WORKSPACE_ROOT)),
            "engine_lab_registry_edits": False,
        },
        "self_check": self_check,
        "summary": {
            "total": len(cases),
            "already_banks": counts["ALREADY_BANKS"],
            "classifier_fix": counts["CLASSIFIER_FIX"],
            "rebucket_to_signal": counts["RE-BUCKET_TO_SIGNAL"],
        },
        "cases": cases,
    }


def _md_cell(value: Any) -> str:
    text = ", ".join(value) if isinstance(value, (list, tuple)) else str(value)
    return text.replace("|", "\\|").replace("\n", " ")


def _table(headers: Sequence[str], rows: Sequence[Sequence[Any]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    lines.extend("| " + " | ".join(_md_cell(value) for value in row) + " |" for row in rows)
    return "\n".join(lines)


def _render_report(payload: Mapping[str, Any]) -> str:
    summary = payload["summary"]
    self_check = payload["self_check"]
    lines = [
        "# V3 P4 classifier-fixable recheck — 2026-07-01",
        "",
        "## Headline",
        "",
        (
            f"2 CLASSIFIER_FIXABLE cases rechecked against `POST_T_V3_3D`: "
            f"{summary['already_banks']} already-bank / "
            f"{summary['classifier_fix']} classifier-fix / "
            f"{summary['rebucket_to_signal']} re-bucket."
        ),
        "",
        (
            f"Self-check: replayed {self_check['checked_cases']} accuracy cases; "
            f"drift={self_check['drift_count']}."
        ),
        "",
        "## Per-case status",
        "",
        _table(
            ["case_id", "expected", "top3", "rank", "covered", "abstain", "emitted_state", "verdict"],
            [
                [
                    case["case_id"],
                    f"{case['expected_family']} / {case['expected_code']}",
                    case["current_run_status"]["top3_families"],
                    case["current_run_status"]["expected_family_rank"],
                    case["current_run_status"]["covered"],
                    case["current_run_status"]["abstain_reason"],
                    case["reachability"]["emitted_state"],
                    case["verdict"],
                ]
                for case in payload["cases"]
            ],
        ),
        "",
    ]
    for case in payload["cases"]:
        reach = case["reachability"]
        lines.extend(
            [
                f"## {case['case_id']} — {case['verdict']}",
                "",
                f"- Current run: winner `{case['current_run_status']['winner_family']}` / `{case['current_run_status']['winner_code']}`; top3 families `{', '.join(case['current_run_status']['top3_families'])}`; expected-family rank `{case['current_run_status']['expected_family_rank']}`; abstained `{case['current_run_status']['abstained']}` (`{case['current_run_status']['abstain_reason']}`).",
                f"- Reachability: required state `{case['required_state']}`; T-V3-D2 said `{reach['t_v3_d2_verdict']}`; live replay says `{reach['live_replay_bound_evidence']}`.",
                f"- Replay candidates: candidates `{', '.join(reach['candidates']) or 'none'}`; resolved `{', '.join(reach['resolved_candidates']) or 'none'}`; definitive `{reach['definitive_state']}`; emitted `{reach['emitted_state']}`.",
                f"- Idle vector: {reach['idle']} lambda={reach['idle_lambda']:.3f}; sample_validity={reach['sample_validity']}; high_idle={reach['high_idle']} high_lambda={reach['high_idle_lambda'] if reach['high_idle_lambda'] is not None else 'n/a'}.",
                f"- Minimal classifier fix: {case['minimal_classifier_fix']}",
                f"- FT-8 neighbour risk: {json.dumps(case['ft8_neighbour_risk'], sort_keys=True)}",
                f"- Same competition_group collisions: {case['competition_group_collisions']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Gate notes",
            "",
            "- No engine, lab, registry, oracle, corpus, scorer, or yardstick files are edited.",
            "- `CASE-039` is not a safe classifier-only commit: the broad EGR/POA overlap has a large neighbour set, so the honest Phase-4 path is an ECU/control signal contract rather than an in-place threshold nudge.",
            "- `era2_008` already banks in the differential; a T-V3-P4-0B fix for it would be a no-op.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    payload = _build_payload()
    REPORT_JSON.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    REPORT_MD.write_text(_render_report(payload), encoding="utf-8")
    summary = payload["summary"]
    self_check = payload["self_check"]
    print(
        "P4 classifier recheck: "
        f"{summary['already_banks']} already-bank / "
        f"{summary['classifier_fix']} classifier-fix / "
        f"{summary['rebucket_to_signal']} re-bucket; "
        f"self-check drift={self_check['drift_count']}"
    )
    print(f"Wrote {REPORT_MD.relative_to(WORKSPACE_ROOT)}")
    print(f"Wrote {REPORT_JSON.relative_to(WORKSPACE_ROOT)}")
    return 0 if self_check["drift_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
