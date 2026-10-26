"""Step 3: controls (i)(ii)(iii) + clean control, then every mutant in mutants.json, in isolated copies.

Usage (repo root, venv active): python audit/scratch/P4/run_matrix.py <workdir> <out.json> [workers] [targets]
[targets] = optional comma list of target ids (re-run subset for the determinism check).
matrix JSON is deterministic (sorted, no timings); timings go to <out.json>.log.
"""

from __future__ import annotations

import json
import queue
import sys
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p4_config import REPO, SCRATCH, TARGETS  # noqa: E402
from p4_lib import apply_span, classify, make_copy, run_suite  # noqa: E402

# Expected unmutated summaries: audit/reports/baseline_20261017.txt (ui is not in the baseline file; its
# value is the suite with labs/comlab on sys.path, which removes the F-C1-5 masking: 6 passed 2 failed -> 8).
BASELINE = {"comlab": "522 passed, 4 skipped, 2 errors", "gaslab": "208 passed, 2 skipped, 4 deselected",
            "vinlab": "203 passed, 8 skipped", "ui": "8 passed"}
TIMEOUT = {"comlab": 120, "gaslab": 120, "vinlab": 60, "ui": 60}

# Control (ii): (target, line, original text on that line, replacement, test that must kill it by assertion)
PLANTED = [
    ("router.route", 2151, "winner_score < ABSTAIN_FLOOR", "winner_score >= ABSTAIN_FLOOR",
     "tests/unit/test_abstain_emit.py::test_v2_abstain_floor"),
    ("router.execute_triage_loop", 1135, "_SCORE_CEILING", "5.0",
     "tests/unit/test_tag_discriminator.py::test_discriminator_respects_score_cap"),
    ("shim._score_rule", 919, "_score_rule_raw(rule, obs)", "None",
     "tests/unit/test_abstain_emit.py::test_v2_abstain_floor"),
    ("gas.apply_differentiators", 306, "actual != expected", "actual == expected",
     "tests/unit/test_resolution.py::test_differentiator_resolves_hct_vs_egr"),
    ("gas._definitive_match", 256, "_is_low_triangle_exhaust_air_leak(reading, ontology)", "False",
     "tests/unit/test_rule_engine.py::test_exhaust_air_leak_low_triangle_sum_routes_before_gate"),
    ("ui.build_diagnose_payload", None, 'dtc["active_mil"] = True', 'dtc["active_mil"] = False',
     "tests/test_ui.py::test_widget_to_payload_roundtrip"),
    ("vin._resolve_year", 843, 'era_hint == "legacy"', 'era_hint != "legacy"',
     "tests/unit/test_decoder.py::TestLYearDisambiguation::test_l_year_legacy_wmi"),
    ("vin._resolve_wmi", 803, 'vin[2] == "9"', 'vin[2] != "9"',
     "tests/unit/test_decoder.py::TestLowVolumeManufacturer::test_low_volume_extended_wmi"),
]


def planted_mutant(tid: str, line: int | None, orig: str, repl: str, kind: str) -> dict:
    f = TARGETS[tid][0]
    lines = (REPO / f).read_bytes().splitlines(keepends=True)
    if line is None:
        line = next(i + 1 for i, ln in enumerate(lines) if orig.encode() in ln)
    col = lines[line - 1].index(orig.encode())
    return {"id": f"{kind}:{tid}", "target": tid, "file": f, "suite": TARGETS[tid][2], "op": kind,
            "line": line, "start": [line, col], "end": [line, col + len(orig.encode())],
            "original": orig, "replacement": repl if kind == "PLANTED" else _null(orig)}


def _null(orig: str) -> str:
    """Semantically null rewrite: parenthesise the expression (the RHS for an assignment)."""
    if " = " in orig:
        lhs, rhs = orig.split(" = ", 1)
        return f"{lhs} = ({rhs})"
    return f"({orig})"


def run_one(root: Path, m: dict, baseline_fail: dict[str, set[str]]) -> dict:
    path = root / m["file"]
    orig = path.read_bytes()
    try:
        path.write_bytes(apply_span(orig, tuple(m["start"]), tuple(m["end"]), m["replacement"]))
        t0 = time.time()
        res = run_suite(root, m["suite"], TIMEOUT[m["suite"]])
        dt = time.time() - t0
    finally:
        path.write_bytes(orig)
    outcome, kills, crashes = classify(res, baseline_fail[m["suite"]])
    return {"id": m["id"], "outcome": outcome, "killing_tests": kills[:5], "n_killing": len(kills),
            "crash_tests": crashes[:5], "n_crash": len(crashes), "summary": res["summary"].split(" in ")[0],
            "guard_ok": res["state"].get("guard_ok"), "modules": res["state"].get("modules", {}),
            "_dt": round(dt, 2)}


def main() -> None:
    work, out = Path(sys.argv[1]), Path(sys.argv[2])
    nw = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    only = set(sys.argv[4].split(",")) if len(sys.argv) > 4 else set(TARGETS)
    suites = sorted({TARGETS[t][2] for t in only})
    roots = [make_copy(work / f"w{i}") for i in range(nw)]
    log = open(str(out) + ".log", "w")

    # Control (i) + (iii): unmutated copy, every worker copy, every suite.
    ctrl_i, baseline_fail = {}, {}
    for suite in suites:
        for r in roots:
            res = run_suite(r, suite, 600)
            summ = res["summary"].split(" in ")[0]
            ok = summ == BASELINE[suite] and res["state"].get("guard_ok") is True
            ctrl_i.setdefault(suite, {"expected": BASELINE[suite], "observed": [], "pass": True})
            ctrl_i[suite]["observed"].append(summ)
            ctrl_i[suite]["pass"] &= ok
            baseline_fail[suite] = {f["nodeid"] for f in res["state"].get("failures", [])}
            ctrl_i[suite]["baseline_failures"] = sorted(baseline_fail[suite])
            for mname, mf in res["state"].get("modules", {}).items():
                assert mf.startswith(str(r) + "/"), (suite, mname, mf)
            print(f"control(i) {suite} {r.name}: {summ} guard={res['state'].get('guard_ok')}", file=log,
                  flush=True)
        ctrl_i[suite]["observed"] = sorted(set(ctrl_i[suite]["observed"]))
    if not all(v["pass"] for v in ctrl_i.values()):
        print(json.dumps(ctrl_i, indent=1))
        sys.exit("control (i) failed")

    mutants = json.loads((SCRATCH / "mutants.json").read_text())
    planted = [p for p in PLANTED if p[0] in only]
    jobs = [planted_mutant(t, ln, o, r, "PLANTED") for t, ln, o, r, _ in planted]
    jobs += [planted_mutant(t, ln, o, r, "NULL") for t, ln, o, r, _ in planted]
    jobs += [m for m in mutants["mutants"] if m["target"] in only]

    q: queue.Queue = queue.Queue()
    for j in jobs:
        q.put(j)
    results: dict[str, dict] = {}
    lock = threading.Lock()

    def worker(root: Path) -> None:
        while True:
            try:
                m = q.get_nowait()
            except queue.Empty:
                return
            r = run_one(root, m, baseline_fail)
            # control (iii) on every run; a mutant that breaks the module's own import cannot be
            # path-checked and is classified KILLED-WRONG-REASON by classify()
            assert r["guard_ok"] is True or r["outcome"] == "KILLED-WRONG-REASON", (m["id"], r["modules"])
            with lock:
                results[m["id"]] = r
                print(f"{m['id']:40s} {r['outcome']:20s} {r['_dt']:6.1f}s {r['summary']}", file=log,
                      flush=True)

    ths = [threading.Thread(target=worker, args=(r,)) for r in roots]
    for t in ths:
        t.start()
    for t in ths:
        t.join()

    ctrl_ii, ctrl_clean = [], []
    for t, _ln, _o, _r, test in planted:
        p = results[f"PLANTED:{t}"]
        ctrl_ii.append({"target": t, "named_test": test, "outcome": p["outcome"],
                        "named_test_killed": test in p["killing_tests"] or
                        any(k == test for k in p["killing_tests"]),
                        "n_killing": p["n_killing"], "n_crash": p["n_crash"]})
        n = results[f"NULL:{t}"]
        ctrl_clean.append({"target": t, "outcome": n["outcome"], "pass": n["outcome"] == "SURVIVED"})

    matrix: dict = {"controls": {"i_unmutated_matches_baseline": ctrl_i, "ii_planted": ctrl_ii,
                                 "clean_null_mutants": ctrl_clean,
                                 "iii_import_guard": "asserted on every run (p4_guard + runner)"},
                    "meta": {t: v for t, v in mutants["meta"].items() if t in only}, "targets": {}}
    by_id = {m["id"]: m for m in mutants["mutants"] if m["target"] in only}
    for mid in sorted(by_id):
        m, r = by_id[mid], results[mid]
        tgt = matrix["targets"].setdefault(m["target"], {"counts": {}, "by_op": {}, "mutants": []})
        tgt["counts"][r["outcome"]] = tgt["counts"].get(r["outcome"], 0) + 1
        bo = tgt["by_op"].setdefault(m["op"], {})
        bo[r["outcome"]] = bo.get(r["outcome"], 0) + 1
        rec = {k: m[k] for k in ("id", "op", "line", "original", "replacement", "note")}
        rec.update({k: r[k] for k in ("outcome", "killing_tests", "n_killing", "crash_tests", "n_crash")})
        tgt["mutants"].append(rec)
    out.write_text(json.dumps(matrix, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"controls": matrix["controls"]["ii_planted"], "clean": ctrl_clean}, indent=1))
    for t, v in sorted(matrix["targets"].items()):
        print(t, v["counts"])


if __name__ == "__main__":
    main()
