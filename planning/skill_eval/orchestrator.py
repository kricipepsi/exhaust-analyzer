#!/usr/bin/env python3.14
"""Trial orchestrator — prepares the full matrix and batches captures.

Usage:
    python orchestrator.py prepare  # create all trial working dirs
    python orchestrator.py capture  # run capture_metrics on all trials
    python orchestrator.py status   # show trial matrix progress
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from runner import TRIALS_DIR, capture_metrics, prepare_trial

PACK_HOME = Path(__file__).resolve().parent
RESULTS_DIR = PACK_HOME / "results"

# ── Trial matrix ────────────────────────────────────────────────────────────
COHORT = "housestyle"
CORPUS_TASKS = [
    "task_01_string_tools",
    "task_02_csv_stats",
    "task_03_trap_api",
    "task_04_refactor",
    "task_05_bug_fix",
]
SKILLS = ["python", "uncle-bob-craft", "improve-codebase-architecture"]
ARMS = ["A", "B"]
K_TRIALS = 3
SEEDS = [42, 43, 44]
MODEL = "opus-4.7@t=0.0"

MATRIX: list[dict] = []


def _build_matrix() -> list[dict]:
    """Build the full trial matrix.

    Arm A (baseline, no skill) is shared across all skills in the cohort.
    Arm B is per-skill. Total: 5 tasks × (1 baseline + 3 skills) × 3 seeds = 60 trials.
    """
    global MATRIX
    if MATRIX:
        return MATRIX
    for task_id in CORPUS_TASKS:
        # Arm A — baseline, shared across all skills
        for seed in SEEDS:
            MATRIX.append({
                "task_id": task_id,
                "skill_id": "none",
                "arm": "A",
                "seed": seed,
                "model": MODEL,
            })
        # Arm B — one set per skill
        for skill_id in SKILLS:
            for seed in SEEDS:
                MATRIX.append({
                    "task_id": task_id,
                    "skill_id": skill_id,
                    "arm": "B",
                    "seed": seed,
                    "model": MODEL,
                })
    return MATRIX


def prepare_all() -> list[Path]:
    """Prepare all trial working directories. Returns list of work_dir paths."""
    matrix = _build_matrix()
    work_dirs: list[Path] = []
    existing = set()
    if TRIALS_DIR.exists():
        existing = {d.name for d in TRIALS_DIR.iterdir() if d.is_dir()}

    for cell in matrix:
        trial_id = f"{cell['task_id']}__{cell['skill_id']}__{cell['arm']}__{cell['seed']}"
        if trial_id in existing:
            work_dirs.append(TRIALS_DIR / trial_id)
            continue
        wd = prepare_trial(
            task_id=cell["task_id"],
            arm=cell["arm"],
            skill_id=cell["skill_id"],
            seed=cell["seed"],
            model=cell["model"],
        )
        work_dirs.append(wd)
        print(f"  prepared: {wd.name}")

    return work_dirs


def capture_all(jsonl_path: str | None = None) -> list[dict]:
    """Run capture_metrics on every trial directory. Returns list of record dicts."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if jsonl_path is None:
        jsonl_path = str(RESULTS_DIR / f"cohort_{COHORT}.jsonl")

    records: list[dict] = []
    for d in sorted(TRIALS_DIR.iterdir()):
        if not d.is_dir():
            continue
        meta_path = d / "trial_meta.json"
        if not meta_path.exists():
            continue
        rec = capture_metrics(d)
        rec_dict = rec.to_dict()
        records.append(rec_dict)
        gate = "gate-ON" if (d / "GATE_ON").exists() else "gate-OFF"
        print(f"  captured: {d.name}  ruff={rec.first_ruff_errors} pyright={rec.first_pyright_errors} pytest={rec.first_pytest_failures}/{rec.first_pytest_errors}  {gate}")

    with open(jsonl_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")

    print(f"\n{len(records)} records written to {jsonl_path}")
    return records


def show_status() -> None:
    """Show which trial dirs exist and whether they have code."""
    if not TRIALS_DIR.exists():
        print("No trials/ directory yet. Run 'prepare' first.")
        return

    dirs = sorted(d for d in TRIALS_DIR.iterdir() if d.is_dir())
    if not dirs:
        print("No trial directories found.")
        return

    has_code = 0
    has_capture = 0
    total = len(dirs)

    for d in dirs:
        py_files = list(d.glob("*.py"))
        if py_files:
            has_code += 1
        meta = d / "trial_meta.json"
        if meta.exists():
            has_capture += 1

    print(f"Trial matrix: {total} dirs, {has_code} with code")
    total_expected = len(CORPUS_TASKS) * (1 + len(SKILLS)) * K_TRIALS
    print(f"  Tasks: {len(CORPUS_TASKS)} × (1 baseline + {len(SKILLS)} skills) × K: {K_TRIALS}")
    print(f"  = {total_expected} total trials\n")

    # Group by task+skill+arm
    groups: dict[str, list[str]] = {}
    for d in dirs:
        meta = d / "trial_meta.json"
        if not meta.exists():
            continue
        m = json.loads(meta.read_text())
        key = f"{m['task_id']}|{m['skill_id']}|{m['arm']}"
        groups.setdefault(key, []).append(d.name)

    for key in sorted(groups):
        task, skill, arm = key.split("|")
        dirs_list = groups[key]
        with_code = sum(1 for dn in dirs_list if list((TRIALS_DIR / dn).glob("*.py")))
        print(f"  {task:25s} skill={skill:30s} arm={arm}  seeds={len(dirs_list)}  with_code={with_code}/{len(dirs_list)}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: orchestrator.py [prepare|capture|status]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "prepare":
        total = len(CORPUS_TASKS) * (1 + len(SKILLS)) * K_TRIALS
        print(f"Preparing trial matrix: {len(CORPUS_TASKS)} tasks × (1 baseline + {len(SKILLS)} skills) × {K_TRIALS} seeds")
        print(f"  = {total} total trials\n")
        prepare_all()
        print("\nDone preparing. Next: write code in each trial dir.")
    elif cmd == "capture":
        print("Capturing metrics from all trial directories...\n")
        capture_all()
    elif cmd == "status":
        show_status()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
