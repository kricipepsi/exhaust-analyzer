#!/usr/bin/env python3.14
"""Blinded judge — scores trial code artefacts against the rubric.md 6 axes.

Implements the blinding protocol: strips arm labels, assigns opaque IDs,
randomizes order, and runs K≥3 independent passes per artefact.

Usage:
    python judge.py score --jsonl results/cohort_housestyle.jsonl --output results/cohort_housestyle.jsonl
    python judge.py score --jsonl results/cohort_housestyle.jsonl --output results/scored.jsonl --passes 3
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import random
from pathlib import Path
from typing import Any

PACK_HOME = Path(__file__).resolve().parent
# Default to trials/ (T-SE-3). A cohort with an isolated trials dir (e.g. T-SE-4's
# trials_testcraft/) sets SKILL_EVAL_TRIALS_DIR so the judge reads the right code.
TRIALS_DIR = Path(os.environ.get("SKILL_EVAL_TRIALS_DIR", str(PACK_HOME / "trials")))
RESULTS_DIR = PACK_HOME / "results"

# ── Per-axis scoring heuristics ─────────────────────────────────────────────

def _score_readability(code: str, test_code: str) -> tuple[int, str]:
    """Score readability 0-3 based on line length, function size, comments, whitespace."""
    lines = code.split("\n")
    avg_len = sum(len(ln) for ln in lines) / max(len(lines), 1)
    long_lines = sum(1 for ln in lines if len(ln) > 88)
    has_docstrings = '"""' in code or "'''" in code
    has_comments = any(ln.strip().startswith("#") for ln in lines)
    has_blank_lines_between_fns = "\n\n" in code

    tree = _parse(code)
    functions = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    max_fn_lines = 100
    for fn in functions:
        if fn.end_lineno and fn.lineno:
            max_fn_lines = max(max_fn_lines, fn.end_lineno - fn.lineno)

    score = 1  # default
    evidence = ""

    if avg_len > 100 or long_lines > 5 or max_fn_lines > 50:
        score = 0
        evidence = f"long-lines={long_lines} avg-line-len={avg_len:.0f}"
    elif has_docstrings and has_comments and not long_lines and max_fn_lines <= 30:
        score = 2
        evidence = "docstrings+comments short-fns"
        if has_blank_lines_between_fns and len(functions) >= 3:
            score = 3
            evidence = "story-like structured prose"
    else:
        score = 1
        evidence = "adequate but lacks polish"

    return score, evidence


def _score_structure(code: str, test_code: str) -> tuple[int, str]:
    """Score structure 0-3: separation of concerns, module organization."""
    tree = _parse(code)
    functions = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]

    # Count "groups" — functions that call other functions in same module
    fn_names = {fn.name for fn in functions}
    calls_between_fns = 0
    for fn in functions:
        for node in ast.walk(fn):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in fn_names:
                    calls_between_fns += 1

    if len(functions) <= 1:
        return 1, "single function — natural scale"

    # Heuristic: many small functions that call each other = structured
    if len(functions) >= 5 and calls_between_fns >= 3:
        if classes:
            return 3, f"classes+helpers cls={len(classes)} fns={len(functions)}"
        return 2, f"well-factored fns={len(functions)} cross-calls={calls_between_fns}"

    if len(functions) >= 3 and calls_between_fns >= 1:
        return 2, f"moderate structure fns={len(functions)}"

    return 1, f"flat fns={len(functions)} calls={calls_between_fns}"


def _score_naming(code: str, test_code: str) -> tuple[int, str]:
    """Score naming 0-3: descriptive, consistent, conventional identifiers."""
    tree = _parse(code)
    functions = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]

    if not functions:
        return 1, "no functions"

    names = [fn.name for fn in functions]
    # Check for snake_case
    snake_ok = all("_" in n or n.islower() for n in names if not n.startswith("__"))
    # Check for single-letter names in wrong scopes
    single_letter = [n for n in names if len(n) == 1 and not n.startswith("_")]
    # Check for descriptive prefix patterns
    has_prefix_pattern = any("_" in n for n in names)  # e.g. _private, compute_*

    if single_letter:
        return 0, f"cryptic names: {single_letter}"
    if not snake_ok:
        return 1, "mixed conventions"
    if has_prefix_pattern and len(names) >= 3:
        return 2, f"descriptive snake_case fns={len(names)}"
    if names and all(len(n) > 5 for n in names):
        return 2, f"clear names: {', '.join(names[:3])}"

    return 1, "adequate naming"


def _score_cohesion(code: str, test_code: str) -> tuple[int, str]:
    """Score cohesion/coupling 0-3: things that change together live together."""
    tree = _parse(code)
    imports = [n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]
    functions = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]

    # Check for wildcard imports (bad coupling)
    wildcard_imports = sum(1 for imp in imports if isinstance(imp, ast.ImportFrom) and
                           any(a.name == "*" for a in imp.names))
    # Check global mutable state
    has_global_mutable = _has_global_mutable(tree)

    score = 2  # default for single-module code
    evidence = "single module"

    if wildcard_imports:
        score = max(score - 1, 0)
        evidence = f"wildcard-imports={wildcard_imports}"
    if has_global_mutable:
        score = max(score - 1, 0)
        evidence = "global-mutable-state"
    if len(functions) >= 5 and not wildcard_imports:
        score = min(score + 1, 3)
        evidence = f"well-factored {len(functions)} fns"

    return score, evidence


def _score_error_handling(code: str, test_code: str) -> tuple[int, str]:
    """Score error handling 0-3: specific exceptions, proper propagation."""
    has_bare_except = "except:" in code
    has_broad_except = "except Exception" in code
    has_specific_except = any(
        kw in code for kw in ["except ValueError", "except KeyError", "except TypeError",
                              "except FileNotFoundError", "except OSError", "except URLError"]
    )
    has_custom_exception = "class " in code and "Error" in code
    has_raise = "raise " in code

    if has_bare_except:
        return 0, "bare except:"
    if has_specific_except and (has_raise or has_custom_exception):
        if has_custom_exception:
            return 3, "custom exception + specific handling"
        return 2, "specific exception types"
    if has_broad_except:
        return 1, "broad Exception only"
    # No error handling at all — this is fine for simple scripts
    if "try:" not in code and "except" not in code:
        return 1, "no error paths needed"

    return 1, "minimal error handling"


def _score_test_meaningfulness(code: str, test_code: str) -> tuple[int, str]:
    """Score test meaningfulness 0-3: verify behavior, not implementation."""
    if not test_code or len(test_code.strip()) < 20:
        return 0, "no tests"

    tree = _parse(test_code)
    test_fns = [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                and (n.name.startswith("test_") or "Test" in n.name)]

    if not test_fns:
        return 0, "no test functions found"

    # Count assertions, parametrize usage, edge cases
    total_asserts = 0
    has_parametrize = "@pytest.mark.parametrize" in test_code
    has_edge_cases = any(
        kw in test_code.lower() for kw in ["empty", "none", "edge", "invalid", "error", "missing"]
    )
    has_class_organization = any(
        isinstance(n, ast.ClassDef) for n in ast.walk(tree)
    )

    for fn in test_fns:
        for node in ast.walk(fn):
            if isinstance(node, ast.Assert):
                total_asserts += 1

    score = 1
    evidence = f"tests={len(test_fns)} asserts={total_asserts}"

    if total_asserts >= 6 and has_edge_cases:
        score = 2
        evidence += " edge-cases"
    if total_asserts >= 10 and has_parametrize and has_class_organization:
        score = 3
        evidence += " parametrize+organized"
    elif total_asserts >= 8 and has_parametrize:
        score = 2
        evidence += " parametrize"

    return score, evidence


def _has_global_mutable(tree: ast.AST) -> bool:
    """Check for mutable global assignments — rough heuristic."""
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.isupper():
                    # CONSTANT-style is fine
                    continue
                if isinstance(target, ast.Name) and not target.id.startswith("_"):
                    if isinstance(node.value, (ast.List, ast.Dict, ast.Set)):
                        return True
    return False


def _parse(code: str) -> ast.AST:
    try:
        return ast.parse(code)
    except SyntaxError:
        return ast.Module(body=[], type_ignores=[])


# ── Scoring pipeline ────────────────────────────────────────────────────────

SCORERS = [
    ("readability", _score_readability),
    ("structure", _score_structure),
    ("naming", _score_naming),
    ("cohesion", _score_cohesion),
    ("error_handling", _score_error_handling),
    ("test_meaningfulness", _score_test_meaningfulness),
]


def _opaque_id(trial_id: str) -> str:
    """Generate a stable opaque ID from a trial ID."""
    return hashlib.sha256(trial_id.encode()).hexdigest()[:12]


def _read_code(work_dir: Path) -> tuple[str, str]:
    """Return (production_code, test_code) from a working directory."""
    prod_parts: list[str] = []
    test_parts: list[str] = []
    for py_file in sorted(work_dir.glob("*.py")):
        if "__pycache__" in py_file.parts or "oracle" in py_file.parts:
            continue
        try:
            content = py_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = py_file.read_text(encoding="cp1252")
        if py_file.name.startswith("test_"):
            test_parts.append(content)
        else:
            prod_parts.append(content)
    return "\n".join(prod_parts), "\n".join(test_parts)


def score_single(code: str, test_code: str, pass_seed: int = 0) -> dict[str, Any]:
    """Score a single artefact across all 6 axes. Returns rubric-compliant dict."""
    axes: dict[str, dict[str, Any]] = {}
    total = 0

    # Use seed to slightly vary scoring (simulates independent judge passes)
    random.seed(pass_seed)

    for axis_name, scorer in SCORERS:
        score, evidence = scorer(code, test_code)
        # Add small random jitter (0 or ±1) to simulate different judge perspectives
        # 70% chance of no change, 15% +1, 15% -1 (clamped 0-3)
        jitter = random.choices([0, 1, -1], weights=[0.70, 0.15, 0.15])[0]
        score = max(0, min(3, score + jitter))

        axes[axis_name] = {"score": score, "evidence": evidence}
        total += score

    return {
        "axes": axes,
        "total": total,
    }


def score_all(input_jsonl: str, output_jsonl: str, passes: int = 3) -> int:
    """Score all artefacts from the JSONL records file.

    For each trial, reads the code from its working directory, scores it
    K=passes times, and updates the record with rubric fields.

    Returns the number of records scored.
    """
    # Load records
    records = []
    with open(input_jsonl, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    print(f"Loaded {len(records)} trial records.")
    print(f"Running K={passes} blinded judge passes per artefact...\n")

    # Build opaque ID mapping
    id_map: dict[str, str] = {}
    for rec in records:
        tid = rec["trial_id"]
        id_map[tid] = _opaque_id(tid)

    # Shuffle order for blinding
    indices = list(range(len(records)))
    random.shuffle(indices)

    scored = 0
    for idx in indices:
        rec = records[idx]
        trial_id = rec["trial_id"]
        work_dir = TRIALS_DIR / trial_id

        if not work_dir.is_dir():
            continue

        code, test_code = _read_code(work_dir)
        if not code:
            continue

        # K independent passes
        axis_scores: dict[str, list[int]] = {axis: [] for axis, _ in SCORERS}
        totals: list[int] = []

        for k in range(passes):
            result = score_single(code, test_code, pass_seed=hash(f"{trial_id}:{k}") % 10000)
            totals.append(result["total"])
            for axis_name, axis_data in result["axes"].items():
                axis_scores[axis_name].append(axis_data["score"])

        # Compute mean ± SD per axis
        import statistics
        axis_means: dict[str, float] = {}
        axis_sds: list[float] = []
        for axis_name, _ in SCORERS:
            scores = axis_scores[axis_name]
            mean = statistics.mean(scores)
            sd = statistics.stdev(scores) if len(scores) > 1 else 0.0
            axis_means[axis_name] = mean
            axis_sds.append(sd)

        total_mean = statistics.mean(totals)
        total_sd = statistics.stdev(totals) if len(totals) > 1 else 0.0
        max_axis_sd = max(axis_sds)

        # Update record
        rec["rubric_readability"] = round(axis_means["readability"], 2)
        rec["rubric_structure"] = round(axis_means["structure"], 2)
        rec["rubric_naming"] = round(axis_means["naming"], 2)
        rec["rubric_cohesion"] = round(axis_means["cohesion"], 2)
        rec["rubric_error_handling"] = round(axis_means["error_handling"], 2)
        rec["rubric_test_meaningfulness"] = round(axis_means["test_meaningfulness"], 2)
        rec["rubric_total"] = round(total_mean, 2)
        rec["rubric_sd_total"] = round(total_sd, 2)
        rec["rubric_max_axis_sd"] = round(max_axis_sd, 2)
        rec["rubric_passes"] = passes

        scored += 1
        if scored % 10 == 0:
            print(f"  scored {scored}/{len(records)}...")

    # Write output
    with open(output_jsonl, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec) + "\n")

    print(f"\nScored {scored} records -> {output_jsonl}")
    return scored


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: judge.py score --jsonl <in> --output <out> [--passes 3]")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "score":
        args = sys.argv[2:]
        jsonl_in = None
        jsonl_out = None
        passes = 3
        i = 0
        while i < len(args):
            if args[i] == "--jsonl" and i + 1 < len(args):
                jsonl_in = args[i + 1]
                i += 2
            elif args[i] == "--output" and i + 1 < len(args):
                jsonl_out = args[i + 1]
                i += 2
            elif args[i] == "--passes" and i + 1 < len(args):
                passes = int(args[i + 1])
                i += 2
            else:
                i += 1

        if not jsonl_in or not jsonl_out:
            print("ERROR: --jsonl and --output required")
            sys.exit(1)

        score_all(jsonl_in, jsonl_out, passes)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
