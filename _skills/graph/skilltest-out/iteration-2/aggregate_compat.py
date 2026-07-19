from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
AGGREGATOR = Path(
    r"C:\Users\muto\.claude\plugins\marketplaces\claude-plugins-official\plugins\skill-creator\skills\skill-creator\scripts\aggregate_benchmark.py"
)


def set_nulls_to_zero() -> list[Path]:
    touched: list[Path] = []
    for path in ROOT.glob("eval-*/*/run-*/grading.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        timing = data.setdefault("timing", {})
        changed = False
        for key in ["total_duration_seconds", "total_tokens"]:
            if timing.get(key) is None:
                timing[key] = 0
                changed = True
        if changed:
            path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            touched.append(path)
    for path in ROOT.glob("eval-*/*/run-*/timing.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        changed = False
        for key in ["total_duration_seconds", "total_tokens"]:
            if data.get(key) is None:
                data[key] = 0
                changed = True
        if changed:
            path.write_text(json.dumps(data, indent=2), encoding="utf-8")
            touched.append(path)
    return touched


def restore_zero_to_null(paths: list[Path]) -> None:
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        if path.name == "grading.json":
            timing = data.setdefault("timing", {})
            timing["total_duration_seconds"] = None
            timing["total_tokens"] = None
        else:
            data["total_duration_seconds"] = None
            data["total_tokens"] = None
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def null_benchmark_timings() -> None:
    path = ROOT / "benchmark.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data.setdefault("metadata", {})["executor_model"] = "codex"
    data["metadata"]["runs_per_configuration"] = 2
    for run in data.get("runs", []):
        result = run.setdefault("result", {})
        result["time_seconds"] = None
        result["tokens"] = None
    for config in ["with_skill", "without_skill"]:
        summary = data.setdefault("run_summary", {}).setdefault(config, {})
        summary["time_seconds"] = {"mean": None, "stddev": None, "min": None, "max": None}
        summary["tokens"] = {"mean": None, "stddev": None, "min": None, "max": None}
    data.setdefault("run_summary", {}).setdefault("delta", {})["time_seconds"] = None
    data["run_summary"]["delta"]["tokens"] = None
    notes = data.setdefault("notes", [])
    notes.append("Timing/token values were unavailable from Codex subagent notifications and are recorded as null, not stand-in zero.")
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main() -> None:
    touched = set_nulls_to_zero()
    try:
        subprocess.run(
            [
                sys.executable,
                str(AGGREGATOR),
                str(ROOT),
                "--skill-name",
                "4dlab-graphify-skills",
                "--skill-path",
                "4DLabV2/_skills/graph/",
            ],
            check=True,
            cwd=ROOT,
        )
    finally:
        restore_zero_to_null(touched)
    null_benchmark_timings()


if __name__ == "__main__":
    main()

