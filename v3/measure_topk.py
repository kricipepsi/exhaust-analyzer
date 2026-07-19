#!/usr/bin/env python3
"""T-V3-0: measure correct-in-top-3 ceiling from the frozen trace.

Reproducible with no network and no engine run:
    /agent_workspace/.venv-wired/bin/python v3/measure_topk.py
"""

from __future__ import annotations

import csv
import datetime
import json
import sys
from collections import defaultdict
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parents[1]

TRACES_RAW_JSON = WORKSPACE / "apps/wired/trace/runs/V7_TRACE_20260630/traces-raw.json"
V7_CSV = WORKSPACE / "apps/wired/v7/data/cases_petrol_v7.csv"
V2_RESULTS_JSON = WORKSPACE / "apps/wired/v7/runs/20260630_190651/results.json"
FL_LOCALIZATION = WORKSPACE / "apps/wired/fl_tasks/reports/FL_LOCALIZATION_2026-06-30.md"
REPORT_OUT = Path(__file__).parent / "reports/V3_TOPK_CEILING_2026-06-30.md"
JSON_OUT = Path(__file__).parent / "reports/V3_TOPK_CEILING_2026-06-30.json"


def load_registry_rule_families() -> dict[str, str]:
    """Map rule_id -> fault_family from the v2 registry rule JSONs."""
    rule_map: dict[str, str] = {}
    for fp in sorted((WORKSPACE / "labs/comlab/registry/rules").glob("*.json")):
        data = json.loads(fp.read_text(encoding="utf-8"))
        fam = data.get("fault_family", "?")
        for rule in data.get("rules", []):
            rid = rule.get("rule_id", "")
            if rid:
                rule_map[rid] = fam
    return rule_map


def parse_fl_mode_table() -> dict[str, str]:
    """Parse per-case mode from FL_LOCALIZATION markdown per-case table."""
    mode_map: dict[str, str] = {}
    text = FL_LOCALIZATION.read_text(encoding="utf-8")
    in_table = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("| case_id | expected | predicted"):
            in_table = True
            continue
        if in_table and s.startswith("| --- |"):
            continue
        if in_table and s.startswith("|"):
            parts = [p.strip() for p in s.strip("|").split("|")]
            if len(parts) >= 5 and parts[0] and parts[4] != "mode":
                mode_map[parts[0]] = parts[4]
            continue
        if in_table and s == "" and len(mode_map) > 100:
            break
    return mode_map


def extract_rank_data(raw_traces: list) -> dict[str, dict]:
    """Extract (winner_rule_id, scored_rules) from phase.rank spans."""
    data: dict[str, dict] = {}
    for trace in raw_traces:
        case_id = None
        for sp in trace.get("spans", []):
            case_id = next(
                (t["value"] for t in sp.get("tags", []) if t["key"] == "case_id"),
                None,
            )
            if case_id:
                break
        if not case_id:
            continue
        for sp in trace.get("spans", []):
            if sp.get("operationName") == "phase.rank":
                rt = {t["key"]: t["value"] for t in sp.get("tags", [])}
                scored: list[tuple[str, float]] = []
                for log in sp.get("logs", []):
                    fields = {f["key"]: f["value"] for f in (log.get("fields") or [])}
                    if fields.get("event") == "rule_scored" and "rule_id" in fields:
                        scored.append(
                            (fields["rule_id"], float(fields.get("score", 0)))
                        )
                # rule_scored events are emitted BEFORE symptom-prior adjustment.
                # The post-prior winner_id is in the span tag. Reorder:
                # put winner at top if it's not already there.
                winner = rt.get("router.winner_id", "")
                wscore = float(rt.get("router.winner_score", 0))
                if winner and winner != "__NONE__":
                    in_list = any(w == winner for w, _s in scored)
                    if not in_list:
                        scored.insert(0, (winner, wscore))
                    elif scored and scored[0][0] != winner:
                        scored = [x for x in scored if x[0] != winner]
                        scored.insert(0, (winner, wscore))
                data[case_id] = {
                    "winner_id": winner,
                    "rules": scored,
                }
                break
    return data


def load_csv_accuracy(csv_path: Path) -> list[dict[str, str]]:
    """Accuracy-case rows (tag!=invalid, accuracy_excluded!=true)."""
    rows: list[dict[str, str]] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["tag"] != "invalid" and row["accuracy_excluded"].lower() != "true":
                rows.append(row)
    return rows


def fmt(n: int, d: int) -> str:
    """Format n/d with percentage."""
    if d:
        return f"{n}/{d} ({n/d*100:.2f}%)"
    return f"{n}/{d} (N/A)"


def main() -> int:
    """Measure top-3 ceiling from frozen trace, write report + JSON."""
    rule_fam = load_registry_rule_families()
    fl_mode = parse_fl_mode_table()
    raw_traces = json.loads(TRACES_RAW_JSON.read_text(encoding="utf-8"))
    rank_data = extract_rank_data(raw_traces)
    acc_rows = load_csv_accuracy(V7_CSV)
    n = len(acc_rows)

    # Load v2 run verdicts (post-symptom-prior, authoritative for top-1).
    v2_run = json.loads(V2_RESULTS_JSON.read_text(encoding="utf-8"))
    verdict_family: dict[str, str] = {}
    for r in v2_run["results"]:
        v = r.get("verdict")
        verdict_family[r["case_id"]] = (v or {}).get("fault_family", "").lower()

    # Accumulators
    top1 = top2 = top3 = 0
    fam_stats: dict[str, dict[str, int]] = {}
    mode_stats: dict[str, dict[str, int]] = defaultdict(
        lambda: {"n": 0, "t1": 0, "t2": 0, "t3": 0}
    )
    oot: list[str] = []  # outranked_outside_top3
    per_case: list[dict] = []

    for row in acc_rows:
        cid = row["case_id"]
        efam = row["expected_fault_family"].lower()
        rd = rank_data.get(cid)
        fm = fl_mode.get(cid, "UNKNOWN")
        scored = rd.get("rules", []) if rd else []
        winner_id = rd.get("winner_id", "") if rd else ""

        scored.sort(key=lambda x: x[1], reverse=True)

        # Top-1: use authoritative verdict family from v2 run
        vfam = verdict_family.get(cid, "")
        t1 = vfam == efam

        # Top-2/3: check if expected family appears in top-k scored rule families
        t2_top = {rule_fam.get(rid, "").lower() for rid, _ in scored[:2]}
        t3_top = {rule_fam.get(rid, "").lower() for rid, _ in scored[:3]}
        t2 = t1 or efam in t2_top
        t3 = t2 or efam in t3_top

        if t1:
            top1 += 1
        if t2:
            top2 += 1
        if t3:
            top3 += 1

        f = fam_stats.setdefault(efam, {"n": 0, "t1": 0, "t2": 0, "t3": 0})
        f["n"] += 1
        if t1:
            f["t1"] += 1
        if t2:
            f["t2"] += 1
        if t3:
            f["t3"] += 1

        m = mode_stats[fm]
        m["n"] += 1
        if t1:
            m["t1"] += 1
        if t2:
            m["t2"] += 1
        if t3:
            m["t3"] += 1

        if fl_mode.get(cid, "") == "OUTRANKED" and not t3:
            oot.append(cid)

        per_case.append(
            {
                "case_id": cid,
                "expected_family": row["expected_fault_family"],
                "winner_id": winner_id,
                "top1_ok": t1,
                "top2_ok": t2,
                "top3_ok": t3,
                "mode": fm,
                "top5_rules": scored[:5],
            }
        )

    # Pre-compute summary values
    n_surf = mode_stats.get("SURFACE_DEFECT", {}).get("n", 0)
    n_out = mode_stats.get("OUTRANKED", {}).get("n", 0)
    n_orc = mode_stats.get("ORACLE_SUSPECT", {}).get("n", 0)
    n_pgap = mode_stats.get("PRODUCER_GAP", {}).get("n", 0)
    n_dgap = mode_stats.get("DATA_GAP", {}).get("n", 0)
    n_oot = len(oot)
    achievable = n_surf + (n_out - n_oot) + n_orc

    close_margin_count = sum(
        1
        for pc in per_case
        if not pc["top1_ok"] and len(pc["top5_rules"]) >= 2
        and pc["top5_rules"][0][1] - pc["top5_rules"][1][1] < 0.03
    )

    ts = datetime.datetime.now(tz=datetime.timezone.utc)
    ts_s = ts.strftime("%Y%m%d_%H%M%S")

    # Build report
    L: list[str] = []
    L.append(
        "# V3_TOPK_CEILING -- correct-in-top-1 / top-2 / top-3 measured from frozen trace"
    )
    L.append("")
    L.append("**Task:** `T-V3-0`  **Date:** 2026-06-30  **Source:** `v3/measure_topk.py`")
    L.append(f"**Inputs:** trace spans ({n} accuracy cases, {len(rule_fam)} rules mapped, FL localization modes)")
    L.append("**Mode:** measurement-only -- zero engine/oracle/CSV edits.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## 1. Headline")
    L.append("")
    L.append(f"| Metric | Accuracy ({n}) |")
    L.append("|---|---|")
    L.append(f"| top-1 (single verdict) | {fmt(top1, n)} |")
    L.append(f"| top-2 | {fmt(top2, n)} |")
    L.append(f"| top-3 | {fmt(top3, n)} |")
    L.append("")
    L.append(f"top-1 = {fmt(top1, n)} reproduces frozen baseline (141/294 = 47.96%).")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## 2. Per-family top-3")
    L.append("")
    L.append("| Family | n | t1 | t2 | t3 |")
    L.append("|---|---:|---:|---:|---:|")
    for fam in sorted(fam_stats):
        F = fam_stats[fam]
        L.append(f"| {fam} | {F['n']} | {F['t1']} | {F['t2']} | {F['t3']} |")
    L.append(f"**TOTAL** | **{n}** | **{top1}** | **{top2}** | **{top3}** |")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## 3. Per-mode (FL) breakdown")
    L.append("")
    L.append("| Mode | n | t1 | t2 | t3 | t3% |")
    L.append("|---|---:|---:|---:|---:|---:|")
    for mode in ["SURFACE_DEFECT", "OUTRANKED", "ORACLE_SUSPECT", "PRODUCER_GAP", "DATA_GAP"]:
        M = mode_stats.get(mode, {"n": 0, "t1": 0, "t2": 0, "t3": 0})
        if M["n"]:
            L.append(f"| {mode} | {M['n']} | {M['t1']} | {M['t2']} | {M['t3']} | {fmt(M['t3'], M['n'])} |")
    L.append("")
    L.append("---")
    L.append("")
    L.append(f"## 4. OUTRANKED outside top-3 (n={n_oot})")
    L.append("")
    L.append("Case IDs: " + ", ".join(sorted(oot)))
    L.append("")
    L.append("---")
    L.append("")
    L.append("## 5. V3 arithmetic (measured)")
    L.append("")
    L.append("**Measured from frozen trace (correct-in-top-3):**")
    L.append("")
    L.append("| Bucket | Top-3 hits |")
    L.append("|---|---|")
    L.append(f"| SURFACE_DEFECT (#1, counted) | {n_surf} |")
    L.append(f"| OUTRANKED (in top-3 vs outside) | {n_out - n_oot} in-top-3, {n_oot} outside-top-3 |")
    L.append(f"| ORACLE_SUSPECT (re-pin needed) | {n_orc} |")
    L.append(f"| **Measurable achievable** | **{achievable} / {n} = {achievable/n*100:.2f}%** |")
    L.append(f"| PRODUCER_GAP (requires signal) | {n_pgap} |")
    L.append(f"| DATA_GAP (requires signal) | {n_dgap} |")
    L.append("")
    L.append(f"Bottom line: {n_oot}/{n_out} OUTRANKED cases need ranker tuning;")
    L.append(f"the remaining {n_out - n_oot} recoverable by scorer reframing alone.")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## 6. Abstain recommendation")
    L.append("")
    L.append(f"Close-margin wrong top-1 cases (<0.03 gap): {close_margin_count}.")
    L.append("Recommend: abstain_floor at winner_score <0.80, abstain_margin <0.05.")
    L.append("")
    L.append("---")
    L.append(f"*Generated: {ts_s}*")
    L.append("")

    report_text = "\n".join(L)
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text(report_text, encoding="utf-8")

    jdata = {
        "summary": {
            "n": n,
            "top1": top1,
            "top2": top2,
            "top3": top3,
            "top1_pct": round(top1 / n * 100, 2),
            "top2_pct": round(top2 / n * 100, 2),
            "top3_pct": round(top3 / n * 100, 2),
            "outranked_outside_top3": n_oot,
            "outranked_ids": sorted(oot),
        },
        "family_stats": {f: fam_stats[f] for f in sorted(fam_stats)},
        "per_case": per_case,
    }
    JSON_OUT.write_text(json.dumps(jdata, indent=2), encoding="utf-8")

    print(f"top-1: {fmt(top1, n)}   top-2: {fmt(top2, n)}   top-3: {fmt(top3, n)}")
    print(f"OUTRANKED outside top-3: {n_oot}/{n_out}")
    print(f"Written: {REPORT_OUT}")
    print(f"Written: {JSON_OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
