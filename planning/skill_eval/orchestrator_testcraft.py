#!/usr/bin/env python3.14
"""Trial orchestrator for the T-SE-4 test-craft cohort.

Builds the test-craft trial matrix and batches captures. The matrix is the
test-writing subset only ({task_01, task_02, task_03}), arms A vs B, two skills,
K=3 seeds → 3 × (1 baseline + 2 skills) × 3 = 27 trials.

Usage:
    python orchestrator_testcraft.py prepare  # create all trial working dirs
    python orchestrator_testcraft.py capture   # capture metrics (incl. mutation)
    python orchestrator_testcraft.py status    # show trial matrix progress
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from runner import capture_metrics, prepare_trial

PACK_HOME = Path(__file__).resolve().parent
RESULTS_DIR = PACK_HOME / "results"
# Isolated trials dir: T-SE-4 reuses the shared arm-A `__none__A__` trial IDs,
# so it must not overwrite T-SE-3's trials/ artefacts (reproducibility).
TRIALS_DIR = PACK_HOME / "trials_testcraft"

COHORT = "testcraft"
CORPUS_TASKS = [
    "task_01_string_tools",
    "task_02_csv_stats",
    "task_03_trap_api",
]
SKILLS = ["python-testing", "ai-regression-testing"]
SEEDS = [42, 43, 44]
MODEL = "opus-4.7@t=0.0"


def _build_matrix() -> list[dict]:
    """Build the full test-craft trial matrix.

    Arm A (baseline, no skill) is shared across both skills in the cohort.
    Arm B is per-skill.
    """
    matrix: list[dict] = []
    for task_id in CORPUS_TASKS:
        for seed in SEEDS:
            matrix.append(
                {"task_id": task_id, "skill_id": "none", "arm": "A", "seed": seed, "model": MODEL}
            )
        for skill_id in SKILLS:
            for seed in SEEDS:
                matrix.append(
                    {"task_id": task_id, "skill_id": skill_id, "arm": "B", "seed": seed, "model": MODEL}
                )
    return matrix


def prepare_all() -> list[Path]:
    """Prepare all test-craft trial working directories."""
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
            trials_dir=TRIALS_DIR,
        )
        work_dirs.append(work_dir)
        print(f"  prepared: {work_dir.name}")
    return work_dirs


def _matrix_trial_ids() -> set[str]:
    return {
        f"{cell['task_id']}__{cell['skill_id']}__{cell['arm']}__{cell['seed']}"
        for cell in _build_matrix()
    }


def capture_all(jsonl_path: str | None = None) -> list[dict]:
    """Run capture_metrics on every test-craft trial. Returns record dicts."""
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
            f"ruff={rec.first_ruff_errors} pyright={rec.first_pyright_errors} "
            f"pytest={rec.first_pytest_failures}/{rec.first_pytest_errors} "
            f"mutation={rec.mutation_score}"
        )

    with open(jsonl_path, "w", encoding="utf-8") as handle:
        for rec in records:
            handle.write(json.dumps(rec) + "\n")

    print(f"\n{len(records)} records written to {jsonl_path}")
    return records


def show_status() -> None:
    """Show which test-craft trial dirs exist and whether they have code."""
    wanted = _matrix_trial_ids()
    if not TRIALS_DIR.exists():
        print("No trials/ directory yet. Run 'prepare' first.")
        return
    dirs = sorted(d for d in TRIALS_DIR.iterdir() if d.is_dir() and d.name in wanted)
    has_code = sum(1 for d in dirs if any(d.glob("*.py")))
    print(f"Test-craft matrix: {len(wanted)} expected, {len(dirs)} present, {has_code} with code")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: orchestrator_testcraft.py [prepare|capture|status]")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "prepare":
        total = len(_build_matrix())
        print(f"Preparing test-craft matrix: {len(CORPUS_TASKS)} tasks × "
              f"(1 baseline + {len(SKILLS)} skills) × {len(SEEDS)} seeds = {total} trials\n")
        prepare_all()
        print("\nDone preparing. Next: deploy code, then capture.")
    elif cmd == "capture":
        print("Capturing metrics (incl. mutation score) from test-craft trials...\n")
        capture_all()
    elif cmd == "status":
        show_status()
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
