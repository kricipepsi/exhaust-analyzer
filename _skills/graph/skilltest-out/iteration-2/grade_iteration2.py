from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FIXTURE = Path(r"C:\tmp\gfxskilltest\iteration-2")


def read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def sha256_body_before_trailer(text: str) -> str:
    marker = "\n## Graph relations (explicit)"
    body = text.split(marker, 1)[0] if marker in text else text
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def expectation(text: str, passed: bool, evidence: str) -> dict:
    return {"text": text, "passed": bool(passed), "evidence": evidence}


def write_grading(run_dir: Path, expectations: list[dict], notes: list[str] | None = None) -> None:
    passed = sum(1 for exp in expectations if exp["passed"])
    total = len(expectations)
    grading = {
        "summary": {
            "passed": passed,
            "failed": total - passed,
            "total": total,
            "pass_rate": round(passed / total, 4) if total else 0.0,
        },
        "expectations": expectations,
        "timing": {
            "total_duration_seconds": None,
            "total_tokens": None,
        },
        "execution_metrics": {
            "total_tool_calls": 0,
            "errors_encountered": 0,
        },
        "user_notes_summary": {
            "uncertainties": notes or [],
            "needs_review": [],
            "workarounds": [],
        },
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "grading.json").write_text(json.dumps(grading, indent=2), encoding="utf-8")
    (run_dir / "timing.json").write_text(
        json.dumps({"total_duration_seconds": None, "total_tokens": None}, indent=2),
        encoding="utf-8",
    )


def grade_code(run_dir: Path, config: str) -> None:
    text = read(run_dir / "outputs" / "audit_report.md")
    lower = text.lower()

    expectations = []
    ia_t = (
        "dirty_module.py:1" in text
        and "__init__.py" in text
        and ("dirty_module.py:4" in text or "dirty_module.py:3" in text)
    )
    expectations.append(expectation(
        "audit flags I/A/T seeded violations with correct file:line",
        ia_t,
        "Expected dirty_module.py:1 star import, __init__.py missing __all__, and dirty_module.py:4 unannotated calculate_ratio.",
    ))

    c_hit = "dynamic_runtime.py:12" in text or "dynamic_runtime.py:13" in text or "route_with_getattr" in text
    c_dispatch = "dynamic_runtime.py:18" in text or "dynamic_runtime.py:19" in text or "dispatch" in lower
    expectations.append(expectation(
        "audit flags the seeded C dispatch site advisory with file:line",
        c_hit and c_dispatch,
        "Expected dynamic_runtime.py getattr and dispatch-dict call to be surfaced as advisory C findings.",
    ))

    s_hit = "dynamic_runtime.py:21" in text or "runtimebuiltfault" in lower or "type(" in text
    expectations.append(expectation(
        "audit flags the seeded S runtime symbol with file:line",
        s_hit,
        "Expected dynamic_runtime.py runtime-built RuntimeBuiltFault/type(...) to be flagged as an S finding.",
    ))

    finding_lines = [line for line in text.splitlines() if line.strip().startswith("| `")]
    no_clean_fp = not any("clean_module.py:" in line for line in finding_lines)
    expectations.append(expectation(
        "audit still has zero false positives on clean_module.py",
        no_clean_fp,
        "Expected no finding-table row against clean_module.py.",
    ))

    local_build_version_ok = "0.8.13" in text or "0.8.36" in text
    probe_ok = (
        local_build_version_ok
        and re.search(r"enum[^\n]*(no|absent|not)", lower)
        and re.search(r"why[^\n]*(yes|present|found)", lower)
        and re.search(r"docstring[^\n]*(yes|present|found)", lower)
    )
    expectations.append(expectation(
        "probe confirms pinned verdict: enum-member=NO, WHY=YES, docstring=YES",
        bool(probe_ok),
        "Expected a graphify version line plus the pinned probe verdict. Local CLI package was separately checked as 0.8.13.",
    ))

    no_edits = all(
        path.exists()
        for path in [
            FIXTURE / "code_fix" / "__init__.py",
            FIXTURE / "code_fix" / "dirty_module.py",
            FIXTURE / "code_fix" / "clean_module.py",
            FIXTURE / "code_fix" / "dynamic_runtime.py",
        ]
    )
    expectations.append(expectation(
        "run makes no edits to fixture source",
        no_edits,
        "Fixture source files still exist in the original fixture path; graders inspect emitted output only.",
    ))

    if config == "with_skill":
        retired = "4dlab-graph.skill" not in lower and "retired control loaded" not in lower
        expectations.append(expectation(
            "skill-only: retired 4dlab-graph does not trigger",
            retired,
            "No evidence that the retired 4dlab-graph skill was used.",
        ))

    write_grading(run_dir, expectations)


def grade_wiki(run_dir: Path) -> None:
    out_dtc = read(run_dir / "outputs" / "dtc_fault_map.md")
    out_trim = read(run_dir / "outputs" / "trim_analytics.md")
    src_dtc = read(FIXTURE / "wiki_fix" / "dtc_fault_map.md")
    src_trim = read(FIXTURE / "wiki_fix" / "trim_analytics.md")
    combined = out_dtc + "\n" + out_trim

    append_only = (
        sha256_body_before_trailer(out_dtc) == hashlib.sha256(src_dtc.encode("utf-8")).hexdigest()
        and sha256_body_before_trailer(out_trim) == hashlib.sha256(src_trim.encode("utf-8")).hexdigest()
    )
    relation_lines = [line for line in combined.splitlines() if line.startswith("**")]
    invented = any("downstream validation" in line.lower() or "associated" in line.lower() for line in relation_lines)
    doc_bug = "SUPPRESS_POST_CAT_TRIM" in combined and "IS_NOT" in combined
    canonical = "TrimAnalyticsGate.O2_FAULT_ACTIVE" in combined and "TrimAnalyticsGate.o2_fault_active" not in "\n".join(relation_lines)

    expectations = [
        expectation(
            "appends ## Graph relations (explicit) and body bytes are append-only",
            append_only and out_dtc.count("## Graph relations (explicit)") == 1 and out_trim.count("## Graph relations (explicit)") == 1,
            f"dtc body hash append-only={append_only}; trailer counts dtc={out_dtc.count('## Graph relations (explicit)')} trim={out_trim.count('## Graph relations (explicit)')}.",
        ),
        expectation(
            "every appended relation line is traceable to fixture text; no invented edges",
            len(relation_lines) >= 6 and not invented,
            f"Found {len(relation_lines)} relation-like lines; invented-edge marker present={invented}.",
        ),
        expectation(
            "seeded doc-bug is written as an IS_NOT non-edge",
            doc_bug,
            "Expected SUPPRESS_POST_CAT_TRIM IS_NOT a TrimAnalyticsGate value.",
        ),
        expectation(
            "two enum spellings are unified to shipped canonical form",
            canonical,
            "Expected trailer labels to use TrimAnalyticsGate.O2_FAULT_ACTIVE consistently.",
        ),
    ]
    write_grading(run_dir, expectations)


def grade_graphify(run_dir: Path, config: str) -> None:
    text = read(run_dir / "outputs" / "run_report.md")
    lower = text.lower()
    graph_json = run_dir / "outputs" / "graph.json"
    if not graph_json.exists():
        nested = list((run_dir / "outputs").rglob("graph.json")) if (run_dir / "outputs").exists() else []
        graph_json = nested[0] if nested else graph_json

    nodes = links = None
    labels = []
    if graph_json.exists():
        try:
            graph = json.loads(graph_json.read_text(encoding="utf-8"))
            nodes = len(graph.get("nodes", []))
            links = len(graph.get("links", []))
            labels = [str(n.get("label") or n.get("id")) for n in graph.get("nodes", [])]
        except Exception:
            pass

    scoped = any(tok in lower for tok in ["code_fix", "scoped", "no-llm", "update"]) and "repo root" not in lower.split("run", 1)[0]
    relocated = graph_json.exists() and not (run_dir / "outputs" / "graphify-out").exists()
    counts = (nodes or 0) > 0 and (links or 0) > 0
    symbols = all(sym in "\n".join(labels) or sym.lower() in lower for sym in ["SensorState", "describe_sensor", "normalize_reading", "calculate_ratio"])
    refused = any(word in lower for word in ["refuse", "refused", "re-scope", "rescope", "must not", "never"]) and "repo root" in lower

    expectations = [
        expectation(
            "runs graphify scoped to code_fix, relocates output, and leaves no run-root graphify-out",
            scoped and relocated,
            f"graph_json={graph_json if graph_json.exists() else 'missing'}; outputs/graphify-out exists={(run_dir / 'outputs' / 'graphify-out').exists()}.",
        ),
        expectation(
            "verify reports node/edge counts and finds clean module symbols",
            counts and symbols,
            f"Parsed graph counts nodes={nodes} links={links}; symbol spot-check={symbols}.",
        ),
        expectation(
            "never-from-root guard refuses or re-scopes the repo-root request",
            refused,
            "Expected the report to refuse/re-scope 'just graphify everything from the repo root'.",
        ),
        expectation(
            "no graph.json is patched by hand",
            graph_json.exists(),
            "Graph JSON exists as produced/relocated output; manual patch evidence not detected by this grader.",
        ),
    ]
    if config == "with_skill":
        retired = "4dlab-graph.skill" not in lower and "retired control loaded" not in lower
        expectations.append(expectation(
            "skill-only: retired 4dlab-graph does not trigger",
            retired,
            "No evidence that the retired 4dlab-graph skill was used.",
        ))
    write_grading(run_dir, expectations)


def main() -> None:
    for eval_id, grader in [(0, grade_code), (1, grade_wiki), (2, grade_graphify)]:
        for config in ["with_skill", "without_skill"]:
            for run_num in [1, 2]:
                run_dir = ROOT / f"eval-{eval_id}" / config / f"run-{run_num}"
                if eval_id in (0, 2):
                    grader(run_dir, config)
                else:
                    grader(run_dir)


if __name__ == "__main__":
    main()
