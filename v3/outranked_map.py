#!/usr/bin/env python3
"""Build T-V3-D1 OUTRANKED rank-depth and deciding-term report."""

from __future__ import annotations

import csv
import datetime as dt
import json
from collections import Counter
from pathlib import Path
from typing import Any

WORKSPACE = Path(__file__).resolve().parents[1]
TRACES_RAW_JSON = WORKSPACE / "apps/wired/trace/runs/V7_TRACE_20260630/traces-raw.json"
V7_CSV = WORKSPACE / "apps/wired/v7/data/cases_petrol_v7.csv"
V2_RESULTS_JSON = WORKSPACE / "apps/wired/v7/runs/20260630_190651/results.json"
FL_LOCALIZATION = WORKSPACE / "apps/wired/fl_tasks/reports/FL_LOCALIZATION_2026-06-30.md"
REPORT_OUT = WORKSPACE / "v3/reports/V3_OUTRANKED_MAP_2026-06-30.md"
JSON_OUT = WORKSPACE / "v3/reports/V3_OUTRANKED_MAP_2026-06-30.json"
EXPECTED_OUTRANKED = 107
EXPECTED_FREE = 38


def load_registry_rules() -> dict[str, dict[str, Any]]:
    """Return rule_id-keyed family and scoring metadata from the v2 registry."""
    rules: dict[str, dict[str, Any]] = {}
    for fp in sorted((WORKSPACE / "labs/comlab/registry/rules").glob("*.json")):
        data = json.loads(fp.read_text(encoding="utf-8"))
        file_family = data.get("fault_family", "?")
        for rule in data.get("rules", []):
            rule_id = str(rule.get("rule_id", ""))
            if not rule_id:
                continue
            rules[rule_id] = {
                "family": str(rule.get("fault_family") or file_family),
                "base_weight": rule.get("base_weight"),
                "competition_group": rule.get("competition_group", ""),
                "source_file": str(fp.relative_to(WORKSPACE)),
            }
    return rules


def parse_localization_table() -> dict[str, dict[str, str]]:
    """Parse the FL localization per-case table."""
    rows: dict[str, dict[str, str]] = {}
    in_table = False
    for line in FL_LOCALIZATION.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("| case_id | expected | predicted"):
            in_table = True
            continue
        if in_table and stripped.startswith("| --- |"):
            continue
        if in_table and stripped.startswith("|"):
            parts = [part.strip() for part in stripped.strip("|").split("|")]
            if len(parts) >= 6 and parts[0] and parts[0] != "case_id":
                rows[parts[0]] = {
                    "expected": parts[1],
                    "predicted": parts[2],
                    "stage": parts[3],
                    "mode": parts[4],
                    "evidence_ref": parts[5],
                }
            continue
        if in_table and stripped == "" and len(rows) > 100:
            break
    return rows


def load_accuracy_rows() -> list[dict[str, str]]:
    """Return accuracy-case CSV rows from the frozen v7 corpus."""
    rows: list[dict[str, str]] = []
    with V7_CSV.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["tag"] != "invalid" and row["accuracy_excluded"].lower() != "true":
                rows.append(row)
    return rows


def fields_by_key(log: dict[str, Any]) -> dict[str, Any]:
    """Convert one Jaeger log field list into a plain dict."""
    return {field["key"]: field.get("value") for field in log.get("fields", [])}


def tags_by_key(span: dict[str, Any]) -> dict[str, Any]:
    """Convert one Jaeger span tag list into a plain dict."""
    return {tag["key"]: tag.get("value") for tag in span.get("tags", [])}


def case_id_for_trace(trace: dict[str, Any]) -> str:
    """Return the suite case_id tag from a trace, or an empty string."""
    for span in trace.get("spans", []):
        case_id = tags_by_key(span).get("case_id")
        if case_id:
            return str(case_id)
    return ""


def extract_rank_data(raw_traces: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Extract phase.rank winners and rule_scored events per case."""
    rank_data: dict[str, dict[str, Any]] = {}
    for trace in raw_traces:
        case_id = case_id_for_trace(trace)
        if not case_id:
            continue
        for span in trace.get("spans", []):
            if span.get("operationName") != "phase.rank":
                continue
            tags = tags_by_key(span)
            scored: list[dict[str, Any]] = []
            for position, log in enumerate(span.get("logs", []), start=1):
                fields = fields_by_key(log)
                if fields.get("event") != "rule_scored" or "rule_id" not in fields:
                    continue
                scored.append(
                    {
                        "rule_id": str(fields["rule_id"]),
                        "score": float(fields.get("score", 0.0)),
                        "trace_order": position,
                    }
                )
            winner_id = str(tags.get("router.winner_id", ""))
            winner_score = float(tags.get("router.winner_score", 0.0) or 0.0)
            if winner_id and winner_id != "__NONE__":
                winner = next((rule for rule in scored if rule["rule_id"] == winner_id), None)
                if winner is None:
                    scored.insert(
                        0,
                        {
                            "rule_id": winner_id,
                            "score": winner_score,
                            "trace_order": 0,
                        },
                    )
                else:
                    winner["score"] = max(float(winner["score"]), winner_score)
                    winner["trace_order"] = 0
            scored.sort(key=lambda rule: (-float(rule["score"]), int(rule["trace_order"])))
            rank_data[case_id] = {
                "winner_id": winner_id,
                "winner_score": winner_score,
                "candidates_in": tags.get("router.candidates_in"),
                "threshold_miss": tags.get("router.threshold_miss"),
                "scored": scored,
            }
            break
    return rank_data


def score_delta_text(rule: dict[str, Any], meta: dict[str, Any]) -> str:
    """Describe direct-vs-inferred scoring contribution for one rule."""
    score = float(rule["score"])
    base = meta.get("base_weight")
    if not isinstance(base, int | float):
        return "base_weight unavailable; score observed in trace.phase.rank"
    delta = score - float(base)
    if abs(delta) < 0.000001:
        return f"base_weight={base:.2f} observed as final score; no uplift observable"
    if delta > 0:
        return f"score {score:.2f} exceeds base_weight={base:.2f} by +{delta:.2f} [inferred uplift]"
    return f"score {score:.2f} below base_weight={base:.2f} by {delta:.2f} [inferred cap/demotion]"


def classify_bucket(rank: int, margin: float) -> str:
    """Classify recovery difficulty for one OUTRANKED case."""
    if rank <= 3:
        return "FREE"
    if rank <= 5 and margin <= 0.15:
        return "TUNABLE"
    return "HARD"


def deciding_term(
    winner: dict[str, Any],
    expected: dict[str, Any],
    rules: dict[str, dict[str, Any]],
) -> str:
    """Name the observed score gap and inferred scoring lever that decided rank order."""
    winner_meta = rules.get(winner["rule_id"], {})
    expected_meta = rules.get(expected["rule_id"], {})
    margin = float(winner["score"]) - float(expected["score"])
    winner_term = score_delta_text(winner, winner_meta)
    expected_term = score_delta_text(expected, expected_meta)
    return (
        f"winner_score - expected_score = {margin:.2f}; "
        f"winner {winner['rule_id']}: {winner_term}; "
        f"expected {expected['rule_id']}: {expected_term}"
    )


def build_rows() -> list[dict[str, Any]]:
    """Build all OUTRANKED per-case rows."""
    rules = load_registry_rules()
    localization = parse_localization_table()
    traces = json.loads(TRACES_RAW_JSON.read_text(encoding="utf-8"))
    rank_data = extract_rank_data(traces)
    result_rows = {
        row["case_id"]: row for row in json.loads(V2_RESULTS_JSON.read_text(encoding="utf-8"))["results"]
    }
    mapped_rows: list[dict[str, Any]] = []
    for corpus_row in load_accuracy_rows():
        case_id = corpus_row["case_id"]
        localized = localization.get(case_id, {})
        if localized.get("mode") != "OUTRANKED":
            continue
        expected_family = corpus_row["expected_fault_family"].lower()
        ranked = rank_data.get(case_id)
        if ranked is None:
            raise RuntimeError(f"missing rank trace for OUTRANKED case {case_id}")
        expected_rules = [
            (position, rule)
            for position, rule in enumerate(ranked["scored"], start=1)
            if rules.get(rule["rule_id"], {}).get("family", "").lower() == expected_family
        ]
        if not expected_rules:
            raise RuntimeError(f"no expected-family scored rule for OUTRANKED case {case_id}")
        expected_rank, expected_rule = expected_rules[0]
        winner_rule = next(
            rule for rule in ranked["scored"] if rule["rule_id"] == ranked["winner_id"]
        )
        winner_meta = rules.get(winner_rule["rule_id"], {})
        expected_meta = rules.get(expected_rule["rule_id"], {})
        margin = float(winner_rule["score"]) - float(expected_rule["score"])
        bucket = classify_bucket(expected_rank, margin)
        mapped_rows.append(
            {
                "case_id": case_id,
                "expected_family": corpus_row["expected_fault_family"],
                "predicted_family": localized.get("predicted")
                or (result_rows.get(case_id, {}).get("verdict") or {}).get("fault_family", ""),
                "best_expected_rule": expected_rule["rule_id"],
                "best_expected_score": round(float(expected_rule["score"]), 6),
                "expected_rank": expected_rank,
                "winner_rule": winner_rule["rule_id"],
                "winner_family": winner_meta.get("family", "?"),
                "winner_score": round(float(winner_rule["score"]), 6),
                "score_margin": round(margin, 6),
                "bucket": bucket,
                "deciding_terms": deciding_term(winner_rule, expected_rule, rules),
                "evidence_citation": (
                    "trace.phase.rank rule_scored winner="
                    f"{winner_rule['rule_id']} score={float(winner_rule['score']):.6g}; "
                    "expected_family best="
                    f"{expected_rule['rule_id']} score={float(expected_rule['score']):.6g}; "
                    f"router.winner_id={ranked['winner_id']}; "
                    f"router.candidates_in={ranked['candidates_in']}; "
                    f"router.threshold_miss={ranked['threshold_miss']}; "
                    f"localization evidence_ref={localized.get('evidence_ref', '')}; "
                    f"registry winner_file={winner_meta.get('source_file', '?')}; "
                    f"registry expected_file={expected_meta.get('source_file', '?')}"
                ),
            }
        )
    mapped_rows.sort(key=lambda row: row["case_id"])
    return mapped_rows


def pct(count: int, total: int) -> str:
    """Format a count and percentage."""
    return f"{count}/{total} ({count / total * 100:.2f}%)" if total else "0/0 (N/A)"


def table(headers: list[str], rows: list[list[Any]]) -> str:
    """Render a Markdown table."""
    output = ["| " + " | ".join(headers) + " |"]
    output.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        output.append("| " + " | ".join(str(item).replace("\n", " ") for item in row) + " |")
    return "\n".join(output)


def render_report(rows: list[dict[str, Any]]) -> str:
    """Render the Markdown report."""
    counts = Counter(row["bucket"] for row in rows)
    rank_counts = Counter(str(min(int(row["expected_rank"]), 10)) for row in rows)
    family_counts = Counter(row["expected_family"] for row in rows)
    bucket_rows = [[name, counts[name], pct(counts[name], len(rows))] for name in ("FREE", "TUNABLE", "HARD")]
    rank_rows = [[rank, rank_counts[rank]] for rank in sorted(rank_counts, key=int)]
    family_rows = [[family, count] for family, count in sorted(family_counts.items())]
    per_case_rows = [
        [
            row["case_id"],
            row["expected_family"],
            row["predicted_family"],
            row["best_expected_rule"],
            f"{row['best_expected_score']:.2f}",
            row["expected_rank"],
            row["winner_rule"],
            row["winner_family"],
            f"{row['winner_score']:.2f}",
            f"{row['score_margin']:.2f}",
            row["bucket"],
            row["deciding_terms"],
            row["evidence_citation"],
        ]
        for row in rows
    ]
    generated = dt.datetime.now(dt.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    return "\n\n".join(
        [
            "# V3_OUTRANKED_MAP_2026-06-30 — rank-depth and deciding-term map",
            (
                "**Task:** `T-V3-D1`  **Source:** `v3/outranked_map.py`  "
                f"**Generated:** {generated}"
            ),
            (
                "Read-only analysis from frozen trace `apps/wired/trace/runs/"
                "V7_TRACE_20260630/traces-raw.json`, run `apps/wired/v7/runs/"
                "20260630_190651/results.json`, localization `FL_LOCALIZATION_2026-06-30`, "
                "and registry rule JSON metadata. No engine, oracle, scorer, or CSV edits."
            ),
            "## Bucket summary",
            table(["Bucket", "Cases", "Share"], bucket_rows),
            (
                f"Cross-check: FREE={counts['FREE']} equals T-V3-0's OUTRANKED-in-top-3 "
                f"figure ({EXPECTED_FREE}); total OUTRANKED={len(rows)} ({EXPECTED_OUTRANKED} expected)."
            ),
            "## Expected-family rank-depth distribution",
            table(["Expected-family best rank (10 = 10+)", "Cases"], rank_rows),
            "## Expected family counts",
            table(["Expected family", "OUTRANKED cases"], family_rows),
            "## Per-case map",
            table(
                [
                    "case_id",
                    "expected_family",
                    "predicted_family",
                    "expected_rule",
                    "expected_score",
                    "rank",
                    "winner_rule",
                    "winner_family",
                    "winner_score",
                    "margin",
                    "bucket",
                    "deciding_terms",
                    "evidence_citation",
                ],
                per_case_rows,
            ),
            "## Bucket semantics",
            (
                "- FREE: expected family is already rank 1-3 in `phase.rank`; T-V3-3 scorer "
                "surfacing can recover it without rank math.\n"
                "- TUNABLE: expected family is rank 4-5 and within 0.15 score of the winner; "
                "the report names the observed score gap and inferred base/uplift term for T-V3-4.\n"
                "- HARD: expected family is deeper than rank 5 or more than 0.15 behind; needs "
                "non-trivial rank work or new evidence."
            ),
        ]
    ) + "\n"


def main() -> int:
    """Write the OUTRANKED report and JSON artefact."""
    rows = build_rows()
    counts = Counter(row["bucket"] for row in rows)
    if len(rows) != EXPECTED_OUTRANKED:
        raise RuntimeError(f"expected {EXPECTED_OUTRANKED} OUTRANKED rows, got {len(rows)}")
    if counts["FREE"] != EXPECTED_FREE:
        raise RuntimeError(f"expected FREE={EXPECTED_FREE}, got {counts['FREE']}")
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "task": "T-V3-D1",
        "source": "v3/outranked_map.py",
        "generated_utc": dt.datetime.now(dt.UTC).isoformat(),
        "inputs": {
            "trace": str(TRACES_RAW_JSON.relative_to(WORKSPACE)),
            "v2_results": str(V2_RESULTS_JSON.relative_to(WORKSPACE)),
            "csv": str(V7_CSV.relative_to(WORKSPACE)),
            "localization": str(FL_LOCALIZATION.relative_to(WORKSPACE)),
        },
        "bucket_counts": {name: counts[name] for name in ("FREE", "TUNABLE", "HARD")},
        "total_outranked": len(rows),
        "free_cross_check_expected": EXPECTED_FREE,
        "cases": rows,
    }
    JSON_OUT.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    REPORT_OUT.write_text(render_report(rows), encoding="utf-8")
    print(
        "Wrote "
        f"{REPORT_OUT.relative_to(WORKSPACE)} and {JSON_OUT.relative_to(WORKSPACE)}; "
        f"FREE={counts['FREE']} TUNABLE={counts['TUNABLE']} HARD={counts['HARD']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
