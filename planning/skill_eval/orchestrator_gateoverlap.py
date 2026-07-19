#!/usr/bin/env python3.14
"""Trial orchestrator for the T-SE-5 gate-overlap cohort (arm C only).

Builds the arm-C matrix and batches captures. Matrix: full 5-task corpus × 3
conditions (C_no_skill, C_verification-loop, C_code-review-excellence) × K=3 seeds
= 45 single-shot, gate-OFF trials. No arm B (a gated run of a gate-clone skill is a
structural null — CONTRACT §1). Arm A is reused from T-SE-3, not re-run here.

Usage:
    python orchestrator_gateoverlap.py prepare   # create all arm-C trial dirs
    python orchestrator_gateoverlap.py capture    # capture metrics (oracle + single-shot)
    python orchestrator_gateoverlap.py status     # show matrix progress
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from runner import capture_metrics, prepare_trial

PACK_HOME = Path(__file__).resolve().parent
RESULTS_DIR = PACK_HOME / "results"
# Isolated trials dir: the gate-overlap cohort uses its own __none__C__ /
# __<skill>__C__ trial IDs; keep them off T-SE-3's trials/ and T-SE-4's
# trials_testcraft/ for reproducibility.
TRIALS_DIR = PACK_HOME / "trials_gateoverlap"

COHORT = "gateoverlap"
CORPUS_TASKS = [
    "task_01_string_tools",
    "task_02_csv_stats",
    "task_03_trap_api",
    "task_04_refactor",
    "task_05_bug_fix",
]
# All three conditions run gate-OFF (arm C). skill_id "none" is the no-skill
# control for the no-gate condition (C_no_skill).
CONDITIONS = ["none", "verification-loop", "code-review-excellence"]
SEEDS = [42, 43, 44]
MODEL = "opus-4.7@t=0.0"


def _build_matrix() -> list[dict]:
    """Build the arm-C trial matrix: 5 tasks × 3 conditions × 3 seeds = 45."""
    matrix: list[dict] = []
    for task_id in CORPUS_TASKS:
        for skill_id in CONDITIONS:
            for seed in SEEDS:
                matrix.append(
                    {
                        "task_id": task_id,
                        "skill_id": skill_id,
                        "arm": "C",
                        "seed": seed,
                        "model": MODEL,
                    }
                )
    return matrix


def _matrix_trial_ids() -> set[str]:
    return {
        f"{c['task_id']}__{c['skill_id']}__{c['arm']}__{c['seed']}"
        for c in _build_matrix()
    }


def prepare_all() -> list[Path]:
    """Prepare all arm-C trial working directories (gate OFF)."""
    matrix = _build_matrix()
    work_dirs: list[Path] = []
    existing: set[str] = set()
    if TRIALS_DIR.exists():
        existing = {d.name for d in TRIALS_DIR.iterdir() if d.is_dir()}

    for cell in matrix:
        trial_id = f"{cell['task_id']}__{cell['skill_id']}__{cell['arm']}__{cell['seed']}"
        if trial_id in existing:
            work_dirs.append(TRIALS_DIR / trial_id)
            continue
        work_dir = prepare_trial(
            task_id=cell["task_id"],
            arm=cell["arm"],
            skill_id=cell["skill_id"],
            seed=cell["seed"],
            model=cell["model"],
            no_gate=True,  # arm C — single-shot, gate OFF
            trials_dir=TRIALS_DIR,
        )
        work_dirs.append(work_dir)
        print(f"  prepared: {work_dir.name}")
    return work_dirs


def capture_all(jsonl_path: str | None = None) -> list[dict]:
    """Run capture_metrics on every arm-C trial. Returns record dicts."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    if jsonl_path is None:
        jsonl_path = str(RESULTS_DIR / f"cohort_{COHORT}.jsonl")

    wanted = _matrix_trial_ids()
    records: list[dict] = []
    for trial_dir in sorted(TRIALS_DIR.iterdir()):
        if not trial_dir.is_dir() or trial_dir.name not in wanted:
            continue
        if not (trial_dir / "trial_meta.json").exists():
            continue
        rec = capture_metrics(trial_dir)
        records.append(rec.to_dict())
        print(
            f"  captured: {trial_dir.name}  "
            f"oracle_failures={rec.extra.get('oracle_failures')} "
            f"single_shot_pytest_failures={rec.extra.get('single_shot_pytest_failures')} "
            f"iters={rec.iterations_to_green}"
        )

    with open(jsonl_path, "w", encoding="utf-8") as handle:
        for rec in records:
            handle.write(json.dumps(rec) + "\n")

    print(f"\n{len(records)} records written to {jsonl_path}")
    return records


def show_status() -> None:
    """Show which arm-C trial dirs exist and whether they have code."""
    wanted = _matrix_trial_ids()
    if not TRIALS_DIR.exists():
        print("No trials_gateoverlap/ directory yet. Run 'prepare' first.")
        return
    dirs = sorted(d for d in TRIALS_DIR.iterdir() if d.is_dir() and d.name in wanted)
    has_code = sum(1 for d in dirs if any(d.glob("*.py")))
    print(f"Gate-overlap matrix: {len(wanted)} expected, {len(dirs)} present, {has_code} with code")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: orchestrator_gateoverlap.py [prepare|capture|status]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "prepare":
        total = len(_build_matrix())
        print(
            f"Preparing gate-overlap matrix: {len(CORPUS_TASKS)} tasks × "
            f"{len(CONDITIONS)} conditions × {len(SEEDS)} seeds = {total} arm-C trials\n"
        )
        prepare_all()
        print("\nDone preparing. Next: python deploy_gateoverlap.py, then capture.")
    elif cmd == "capture":
        print("Capturing arm-C metrics (oracle + single-shot pytest)...\n")
        capture_all()
    elif cmd == "status":
        show_status()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
