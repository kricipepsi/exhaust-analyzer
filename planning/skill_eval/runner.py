#!/usr/bin/env python3.14
"""Skill-Eval Trial Runner.

Prepares trial working directories, captures gate-invisible metrics after the
coder produces code, and writes TrialRecord JSON-lines rows per metrics_schema.md.

Usage:
    python runner.py prepare --task corpus/task_01_string_tools --arm A --seed 42
    python runner.py capture --working-dir trials/T-SE-2-T1__none__A__42
    python runner.py smoke --task corpus/task_01_string_tools

Arm semantics (CONTRACT §2):
    A — baseline: no skill under test, gate ON
    B — skill: skill under test loaded, gate ON
    C — no-gate ablation: skill under test, gate OFF (single-shot, no iterate-to-green)
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# TrialRecord — canonical form from metrics_schema.md §5
# ---------------------------------------------------------------------------


@dataclass(slots=True)
class TrialRecord:
    # Identity
    trial_id: str
    task_id: str
    skill_id: str
    arm: str  # "A" | "B" | "C"
    seed: int
    model: str
    timestamp_utc: str

    # First-pass counts
    first_ruff_errors: int = 0
    first_pyright_errors: int = 0
    first_pytest_failures: int = 0
    first_pytest_errors: int = 0

    # Convergence cost
    iterations_to_green: int = 0
    total_tokens: int = 0
    total_time_s: float = 0.0

    # Hallucinated-API
    hallucinated_imports: int = 0
    hallucinated_functions: int = 0
    hallucinated_params: int = 0

    # Rubric (blinded, filled later by judge)
    rubric_readability: float = 0.0
    rubric_structure: float = 0.0
    rubric_naming: float = 0.0
    rubric_cohesion: float = 0.0
    rubric_error_handling: float = 0.0
    rubric_test_meaningfulness: float = 0.0
    rubric_total: float = 0.0
    rubric_sd_total: float = 0.0
    rubric_max_axis_sd: float = 0.0
    rubric_passes: int = 0

    # Objective proxies
    cyclomatic_complexity_avg: float = 0.0
    cyclomatic_complexity_max: int = 0
    mutation_score: float | None = None
    type_coverage_pct: float = 0.0
    docstring_coverage_pct: float = 0.0
    diff_churn_lines: int = 0
    diff_files_touched: int = 0

    # Extensibility
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for fld in self.__slots__:  # type: ignore[attr-defined]
            result[fld] = getattr(self, fld)
        return result


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PACK_HOME = Path(__file__).resolve().parent
CORPUS_DIR = PACK_HOME / "corpus"
TRIALS_DIR = PACK_HOME / "trials"

# ---------------------------------------------------------------------------
# Python file discovery
# ---------------------------------------------------------------------------


def _py_files(work_dir: Path) -> list[Path]:
    """Return all .py files in work_dir, excluding __pycache__ and oracle dirs."""
    return sorted(
        p
        for p in work_dir.rglob("*.py")
        if "__pycache__" not in p.parts and "oracle" not in p.parts
    )


# ---------------------------------------------------------------------------
# First-pass gate counts (§2.1)
# ---------------------------------------------------------------------------


def _run_ruff(work_dir: Path) -> int:
    """Run ruff check, return error count (first run, no fix)."""
    py_files = _py_files(work_dir)
    if not py_files:
        return 0
    try:
        result = subprocess.run(
            [sys.executable, "-m", "ruff", "check", "--output-format=concise", "."],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=str(work_dir),
        )
        if result.returncode == 0:
            return 0
        lines = [line for line in result.stdout.split("\n") if line.strip()]
        return len(lines)
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return -1


def _run_pyright(work_dir: Path) -> int:
    """Run pyright, return diagnostic count."""
    py_files = _py_files(work_dir)
    if not py_files:
        return 0
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pyright", "--outputjson", "."],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(work_dir),
        )
        if result.returncode == 0:
            return 0
        try:
            data = json.loads(result.stdout)
            return data.get("summary", {}).get("numberOfErrors", len(data.get("generalDiagnostics", [])))
        except json.JSONDecodeError:
            return len([line for line in result.stdout.split("\n") if line.strip()])
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return -1


def _run_pytest(work_dir: Path) -> tuple[int, int]:
    """Run pytest -x, return (failures, errors)."""
    py_files = _py_files(work_dir)
    test_files = [p for p in py_files if p.name.startswith("test_")]
    if not test_files:
        return 0, 0
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-x", "-q", "--tb=short", "."],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(work_dir),
        )
        output = result.stdout + result.stderr
        failures = 0
        errors = 0
        m = re.search(r"(\d+) failed", output)
        if m:
            failures = int(m.group(1))
        m = re.search(r"(\d+) errors", output)
        if m:
            errors = int(m.group(1))
        return failures, errors
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return -1, -1


def _run_pytest_measure_only(work_dir: Path) -> tuple[int, int]:
    """Run the coder's own visible suite **once**, no ``-x``, no fix loop.

    This is the single-shot (arm-C) measurement of the coder's visible tests:
    every test runs (no short-circuit), the total failure/error counts are read
    once and never repaired. Returns ``(failures, errors)``; ``(0, 0)`` when the
    trial ships no test file, ``(-1, -1)`` on timeout/missing pytest.

    Distinct from :func:`_run_pytest` (which uses ``-x`` to count the *first*
    failure for the gated first-pass metric): arm C wants the full single-shot
    failure tally, so the short-circuit is intentionally dropped.
    """
    py_files = _py_files(work_dir)
    test_files = [p for p in py_files if p.name.startswith("test_")]
    if not test_files:
        return 0, 0
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "--tb=no", "."],
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(work_dir),
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return -1, -1
    output = result.stdout + result.stderr
    failures = 0
    errors = 0
    m = re.search(r"(\d+) failed", output)
    if m:
        failures = int(m.group(1))
    m = re.search(r"(\d+) error", output)
    if m:
        errors = int(m.group(1))
    return failures, errors


# ---------------------------------------------------------------------------
# Hallucinated-API detection (§2.3)
# ---------------------------------------------------------------------------


def _detect_hallucinated_imports(work_dir: Path) -> int:
    """Count import statements that fail importlib.util.find_spec.

    Local modules (files in the same directory) are NOT counted as hallucinated.
    """
    hallu_count = 0
    for py_file in _py_files(work_dir):
        try:
            source = py_file.read_text()
        except Exception:
            continue
        tree = ast.parse(source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top_level = alias.name.split(".")[0]
                    if _is_real_import(top_level, py_file, work_dir):
                        continue
                    hallu_count += 1
            elif isinstance(node, ast.ImportFrom):
                if node.module is None:
                    continue
                if node.level > 0:  # Relative imports
                    continue
                top_level = node.module.split(".")[0]
                if _is_real_import(top_level, py_file, work_dir):
                    continue
                hallu_count += 1
    return hallu_count


def _is_real_import(top_level: str, py_file: Path, work_dir: Path) -> bool:
    """Check if a top-level import name resolves to a real module or local file."""
    if importlib.util.find_spec(top_level) is not None:
        return True
    # Check for local module in same directory
    local = py_file.parent / f"{top_level}.py"
    if local.exists():
        return True
    return False


def _detect_hallucinated_functions(work_dir: Path) -> int:
    """Count calls to functions not found in the imported module.

    This is a best-effort static analysis. For each `from X import Y`, verify Y
    exists in X. For each `import X` + `X.Y()`, verify Y exists in X.
    Local modules are checked via AST parsing instead of import.
    """
    hallu_count = 0
    for py_file in _py_files(work_dir):
        try:
            source = py_file.read_text()
        except Exception:
            continue
        tree = ast.parse(source)

        # Build a map: imported_name → (module_name, attr_name)
        imported_names: dict[str, tuple[str, str]] = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                # Bare imports (import X): skip — we only check from-imports
                # because `import X` alone doesn't claim specific attributes.
                pass
            elif isinstance(node, ast.ImportFrom):
                if node.module is None or node.level > 0:
                    continue
                for alias in node.names:
                    if alias.name == "*":
                        continue
                    imported_names[alias.asname or alias.name] = (
                        node.module,
                        alias.name,
                    )

        # Check each imported name resolves
        for name, (module_name, attr_name) in imported_names.items():
            local_path = py_file.parent / f"{module_name}.py"
            try:
                mod = importlib.import_module(module_name)
                if not hasattr(mod, attr_name):
                    hallu_count += 1
            except (ImportError, ModuleNotFoundError):
                if local_path.exists():
                    # Check local module's AST for the attribute
                    if not _local_module_has_attr(local_path, attr_name):
                        hallu_count += 1
                # else: already caught by hallucinated_imports
            except Exception:
                pass  # Can't verify, skip

    return hallu_count


def _local_module_has_attr(file_path: Path, attr_name: str) -> bool:
    """Check if a local Python file defines a given top-level name."""
    try:
        tree = ast.parse(file_path.read_text())
    except Exception:
        return True  # Can't verify, be conservative
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.name == attr_name:
                return True
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == attr_name:
                    return True
    return False


def _detect_hallucinated_params(work_dir: Path) -> int:
    """Count keyword arguments to real functions that don't exist in their signature.

    Best-effort: for each function call with keyword arguments, verify params exist.
    """
    hallu_count = 0
    for py_file in _py_files(work_dir):
        try:
            source = py_file.read_text()
        except Exception:
            continue
        tree = ast.parse(source)

        # Collect function definitions in the same file
        local_fns: dict[str, set[str]] = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                params = set()
                for arg in node.args.args:
                    params.add(arg.arg)
                local_fns[node.name] = params

        # Check each call
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                # Get function name
                fn_name = None
                if isinstance(node.func, ast.Name):
                    fn_name = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    fn_name = node.func.attr

                if fn_name is None:
                    continue

                # Check keyword arguments
                for kw in node.keywords:
                    if kw.arg is None:
                        continue  # **kwargs expansion, skip
                    # Check against local functions
                    if fn_name in local_fns:
                        if kw.arg not in local_fns[fn_name]:
                            hallu_count += 1

    return hallu_count


# ---------------------------------------------------------------------------
# Objective proxies (§4)
# ---------------------------------------------------------------------------


def _cyclomatic_complexity(work_dir: Path) -> tuple[float, int]:
    """Compute avg and max cyclomatic complexity using radon."""
    py_files = _py_files(work_dir)
    if not py_files:
        return 0.0, 0
    try:
        from radon.complexity import cc_visit  # pyright: ignore[reportMissingImports]  # untyped 3rd-party
        all_complexities: list[int] = []
        for py_file in py_files:
            try:
                for block in cc_visit(py_file.read_text()):
                    all_complexities.append(block.complexity)
            except Exception:
                pass
        if not all_complexities:
            return 0.0, 0
        return round(sum(all_complexities) / len(all_complexities), 2), max(all_complexities)
    except ImportError:
        return 0.0, 0


def _type_coverage(work_dir: Path) -> float:
    """Compute percentage of functions/methods with complete type annotations."""
    total = 0
    annotated = 0
    for py_file in _py_files(work_dir):
        try:
            tree = ast.parse(py_file.read_text())
        except Exception:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                total += 1
                # Check if all args have annotations and return is annotated
                args_ok = all(
                    arg.annotation is not None
                    for arg in node.args.args
                    if arg.arg != "self"
                )
                ret_ok = node.returns is not None
                if args_ok and ret_ok:
                    annotated += 1
    return round(annotated / total * 100, 1) if total > 0 else 100.0


def _docstring_coverage(work_dir: Path) -> float:
    """Compute percentage of public functions/classes with docstrings."""
    total = 0
    has_doc = 0
    for py_file in _py_files(work_dir):
        try:
            tree = ast.parse(py_file.read_text())
        except Exception:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                # Skip private/dunder names
                if node.name.startswith("_") and not node.name.startswith("__"):
                    continue
                total += 1
                if (
                    ast.get_docstring(node) is not None
                    and len(ast.get_docstring(node) or "") >= 5
                ):
                    has_doc += 1
    return round(has_doc / total * 100, 1) if total > 0 else 100.0


def _diff_churn(work_dir: Path) -> tuple[int, int]:
    """Count lines and files touched. Uses starter_code comparison for refactor tasks.

    Returns (lines_changed, files_touched).
    """
    py_files = _py_files(work_dir)
    total_lines = 0
    for py_file in py_files:
        try:
            total_lines += len(py_file.read_text().split("\n"))
        except Exception:
            pass
    return total_lines, len(py_files)


# ---------------------------------------------------------------------------
# Mutation score (§4 `mutation_score`; FU-SE-5)
# ---------------------------------------------------------------------------
#
# A self-contained AST mutation engine. For each production module we enumerate
# small semantic mutations (mutants); for each mutant we materialise a copy of
# the trial directory with the *production* file mutated and the coder's test
# suite untouched, then run pytest. A mutant is "killed" when the suite, which
# passed on the original, now fails on the mutant. `mutation_score` is the kill
# ratio — the fraction of injected defects the coder's tests catch. This is the
# direct, objective test-craft metric (CONTRACT §3.6 / metrics_schema §4): an
# unkilled mutant in uncovered code already counts against the score, so line
# coverage is subsumed and is not captured as a separate field (T-SE-4 spec).
#
# We do not depend on mutmut/mutpy: both shell out per mutant against a tox/venv
# layout this corpus does not use, and add an uninstalled dependency. The metric
# computed here is identical (killed / total) and runs deterministically.

# Comparison-operator swaps (each op -> a distinct op that changes meaning).
_CMPOP_MUTATIONS: dict[type[ast.cmpop], type[ast.cmpop]] = {
    ast.Lt: ast.LtE,
    ast.LtE: ast.Lt,
    ast.Gt: ast.GtE,
    ast.GtE: ast.Gt,
    ast.Eq: ast.NotEq,
    ast.NotEq: ast.Eq,
    ast.Is: ast.IsNot,
    ast.IsNot: ast.Is,
    ast.In: ast.NotIn,
    ast.NotIn: ast.In,
}

# Binary arithmetic-operator swaps.
_BINOP_MUTATIONS: dict[type[ast.operator], type[ast.operator]] = {
    ast.Add: ast.Sub,
    ast.Sub: ast.Add,
    ast.Mult: ast.FloorDiv,
    ast.Div: ast.Mult,
    ast.FloorDiv: ast.Mult,
    ast.Mod: ast.Mult,
}

# Boolean-operator swaps.
_BOOLOP_MUTATIONS: dict[type[ast.boolop], type[ast.boolop]] = {
    ast.And: ast.Or,
    ast.Or: ast.And,
}


class _MutantApplier(ast.NodeTransformer):
    """Apply exactly one mutation, identified by a zero-based ordinal counter.

    The transformer walks the tree counting mutation *sites*; it rewrites only
    the site whose ordinal equals ``target``. ``applied`` records whether the
    target site was reached (False means ``target`` was out of range).
    """

    def __init__(self, target: int) -> None:
        self._target = target
        self._counter = 0
        self.applied = False

    def _hit(self) -> bool:
        """Return True iff the current site is the targeted one; advance counter."""
        is_target = self._counter == self._target
        self._counter += 1
        return is_target

    def visit_Compare(self, node: ast.Compare) -> ast.AST:
        self.generic_visit(node)
        new_ops: list[ast.cmpop] = []
        for op in node.ops:
            replacement = _CMPOP_MUTATIONS.get(type(op))
            if replacement is not None and self._hit():
                new_ops.append(replacement())
                self.applied = True
            else:
                new_ops.append(op)
        node.ops = new_ops
        return node

    def visit_BinOp(self, node: ast.BinOp) -> ast.AST:
        self.generic_visit(node)
        replacement = _BINOP_MUTATIONS.get(type(node.op))
        if replacement is not None and self._hit():
            node.op = replacement()
            self.applied = True
        return node

    def visit_BoolOp(self, node: ast.BoolOp) -> ast.AST:
        self.generic_visit(node)
        replacement = _BOOLOP_MUTATIONS.get(type(node.op))
        if replacement is not None and self._hit():
            node.op = replacement()
            self.applied = True
        return node

    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        # Mutate numeric and boolean literals (skip docstrings / arbitrary str).
        if isinstance(node.value, bool):
            if self._hit():
                node = ast.copy_location(ast.Constant(value=not node.value), node)
                self.applied = True
        elif isinstance(node.value, int) and not isinstance(node.value, bool):
            if self._hit():
                node = ast.copy_location(ast.Constant(value=node.value + 1), node)
                self.applied = True
        return node


def _count_mutation_sites(source: str) -> int:
    """Count how many mutation sites a module source exposes."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return 0
    counter = _MutantApplier(target=-1)  # -1 is never hit; just tallies sites
    counter.visit(tree)
    return counter._counter


def _make_mutant_source(source: str, ordinal: int) -> str | None:
    """Return the source with the *ordinal*-th mutation applied, or None.

    None means the ordinal was out of range or the mutated tree did not
    round-trip through ``ast.unparse`` (defensive — should not happen).
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return None
    applier = _MutantApplier(target=ordinal)
    mutated = applier.visit(tree)
    if not applier.applied:
        return None
    ast.fix_missing_locations(mutated)
    try:
        return ast.unparse(mutated)
    except Exception:
        return None


def _pytest_passes(work_dir: Path) -> bool:
    """Return True iff the coder's pytest suite passes cleanly in *work_dir*."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", "."],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(work_dir),
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False
    return result.returncode == 0


def _mutation_score(work_dir: Path) -> float | None:
    """Compute the mutation kill ratio of the coder's suite over production code.

    Returns ``None`` when the trial has no test suite (the metric is undefined),
    or when the suite does not pass on the unmutated code (a mutation score is
    only meaningful against a green baseline — a red suite cannot "kill" anything
    attributably). Otherwise returns killed / total in [0.0, 1.0].
    """
    py_files = _py_files(work_dir)
    test_files = [p for p in py_files if p.name.startswith("test_")]
    prod_files = [p for p in py_files if not p.name.startswith("test_")]
    if not test_files or not prod_files:
        return None

    # Baseline must be green, else kills are not attributable to the mutant.
    if not _pytest_passes(work_dir):
        return None

    rel_prod = [p.relative_to(work_dir) for p in prod_files]
    sources = {p: (work_dir / p).read_text(encoding="utf-8") for p in rel_prod}

    total = 0
    killed = 0
    with tempfile.TemporaryDirectory(prefix="mutscore_") as tmp:
        sandbox = Path(tmp) / "trial"
        for rel_prod_file in rel_prod:
            source = sources[rel_prod_file]
            site_count = _count_mutation_sites(source)
            for ordinal in range(site_count):
                mutant_source = _make_mutant_source(source, ordinal)
                if mutant_source is None:
                    continue
                total += 1
                # Fresh copy of the trial; mutate one production file.
                if sandbox.exists():
                    shutil.rmtree(sandbox)
                shutil.copytree(
                    work_dir,
                    sandbox,
                    ignore=shutil.ignore_patterns("__pycache__", "oracle"),
                )
                (sandbox / rel_prod_file).write_text(mutant_source, encoding="utf-8")
                if not _pytest_passes(sandbox):
                    killed += 1  # suite failed on the mutant -> mutant killed

    if total == 0:
        return None
    return round(killed / total, 4)


# ---------------------------------------------------------------------------
# Oracle (hidden test) execution
# ---------------------------------------------------------------------------

def _run_oracle(task_dir: Path, work_dir: Path) -> dict[str, Any] | None:
    """Run the hidden oracle tests for a task against the coder's work_dir.

    Returns the oracle's run_all() dict, or None if no oracle exists.
    """
    oracle_test = task_dir / "oracle" / f"test_{task_dir.name.split('_', 1)[1]}.py"
    if not oracle_test.exists():
        # Try generic oracle pattern
        oracle_files = list((task_dir / "oracle").glob("test_*.py"))
        if oracle_files:
            oracle_test = oracle_files[0]
        else:
            return None

    # Load and run the oracle
    spec = importlib.util.spec_from_file_location(
        f"oracle_{task_dir.name}", str(oracle_test)
    )
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    try:
        spec.loader.exec_module(mod)
        if hasattr(mod, "run_all"):
            return mod.run_all(work_dir)
    except Exception as exc:
        return {"error": str(exc), "pass": False}
    return None


# ---------------------------------------------------------------------------
# Prepare / Capture / Smoke
# ---------------------------------------------------------------------------


def prepare_trial(
    task_id: str,
    arm: str,
    skill_id: str = "none",
    seed: int = 0,
    model: str = "opus-4.7@t=0.0",
    no_gate: bool = False,
    trials_dir: Path | None = None,
) -> Path:
    """Create a working directory for a trial with metadata.

    *trials_dir* defaults to the module-level ``TRIALS_DIR``; cohorts that must
    not collide with another cohort's trial IDs (e.g. T-SE-4 reuses the shared
    arm-A ``__none__A__`` IDs) pass their own directory to stay isolated.

    Returns the path to the working directory.
    """
    task_dir = CORPUS_DIR / task_id
    if not task_dir.is_dir():
        raise FileNotFoundError(f"Task directory not found: {task_dir}")

    base_dir = trials_dir if trials_dir is not None else TRIALS_DIR
    trial_id = _make_trial_id(task_id, skill_id, arm, seed)
    work_dir = base_dir / trial_id
    work_dir.mkdir(parents=True, exist_ok=True)

    # Copy task files (but NOT the oracle) to work_dir
    for item in task_dir.iterdir():
        if item.name == "oracle":
            continue
        dest = work_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True)
        else:
            shutil.copy2(item, dest)

    # For refactor tasks, copy starter_code as the target filename
    starter = work_dir / "starter_code.py"
    if starter.exists():
        # Determine target filename from prompt
        prompt = work_dir / "prompt.md"
        if prompt.exists():
            prompt_text = prompt.read_text()
            m = re.search(r"Write.*?`(\w+\.py)`", prompt_text)
            if m:
                target = work_dir / m.group(1)
                if not target.exists():
                    starter.rename(target)
                else:
                    starter.unlink()  # target already exists, remove starter duplicate

    # Write trial metadata
    meta = {
        "trial_id": trial_id,
        "task_id": task_id,
        "skill_id": skill_id,
        "arm": arm,
        "seed": seed,
        "model": model,
        "no_gate": no_gate,
        "prepared_utc": datetime.now(timezone.utc).isoformat(),
    }
    (work_dir / "trial_meta.json").write_text(json.dumps(meta, indent=2))
    (work_dir / ("GATE_OFF" if no_gate else "GATE_ON")).touch()

    return work_dir


def capture_metrics(work_dir: Path, task_id: str | None = None) -> TrialRecord:
    """Run all metric captures against the code in work_dir.

    Returns a TrialRecord. Does NOT apply rubric scores (those are done by the blinded judge later).
    """
    meta_path = work_dir / "trial_meta.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"No trial_meta.json in {work_dir} — run prepare first")

    meta = json.loads(meta_path.read_text())
    no_gate = meta.get("no_gate", False)
    resolved_task_id: str = task_id or meta["task_id"]

    rec = TrialRecord(
        trial_id=meta["trial_id"],
        task_id=resolved_task_id,
        skill_id=meta["skill_id"],
        arm=meta["arm"],
        seed=meta["seed"],
        model=meta["model"],
        timestamp_utc=meta["prepared_utc"],
    )

    # First-pass gate counts (skip if no_gate / arm C)
    if not no_gate:
        rec.first_ruff_errors = _run_ruff(work_dir)
        rec.first_pyright_errors = _run_pyright(work_dir)
        failures, errors = _run_pytest(work_dir)
        rec.first_pytest_failures = failures
        rec.first_pytest_errors = errors
    else:
        # Arm C (gate OFF, single-shot): the single-shot result *is* the
        # measurement (T-SE-5 / FU-SE-4). Record, into the existing `extra`
        # dict (no new schema field):
        #   - oracle_failures: escaped defects vs the hidden oracle — the
        #     quality the gate would have caught. Lower is better.
        #   - single_shot_pytest_failures: the coder's own visible suite,
        #     measured once and never repaired.
        oracle = _run_oracle(CORPUS_DIR / resolved_task_id, work_dir)
        if oracle is not None:
            rec.extra["oracle_failures"] = oracle.get("failed")
            rec.extra["oracle_total_checks"] = oracle.get("total_checks")
            rec.extra["oracle_passed"] = oracle.get("passed")
        else:
            rec.extra["oracle_failures"] = None
        ss_failures, ss_errors = _run_pytest_measure_only(work_dir)
        rec.extra["single_shot_pytest_failures"] = ss_failures
        rec.extra["single_shot_pytest_errors"] = ss_errors

    # Hallucinated API
    rec.hallucinated_imports = _detect_hallucinated_imports(work_dir)
    rec.hallucinated_functions = _detect_hallucinated_functions(work_dir)
    rec.hallucinated_params = _detect_hallucinated_params(work_dir)

    # Objective proxies
    rec.cyclomatic_complexity_avg, rec.cyclomatic_complexity_max = _cyclomatic_complexity(work_dir)
    rec.type_coverage_pct = _type_coverage(work_dir)
    rec.docstring_coverage_pct = _docstring_coverage(work_dir)
    rec.diff_churn_lines, rec.diff_files_touched = _diff_churn(work_dir)

    # Mutation score — primary metric for the test-craft cohort (T-SE-4 / FU-SE-5).
    # Populated only for trials that ship a test suite over a green baseline;
    # tasks with no suite return None (unchanged default).
    rec.mutation_score = _mutation_score(work_dir)

    return rec


def smoke_run(task_id: str) -> list[TrialRecord]:
    """Run a smoke test: 1 task × arms A/B × K=2.

    Prepares 4 trials (2 arms × 2 seeds). The coder must write code in each
    working dir before calling capture.
    """
    records: list[TrialRecord] = []
    for arm in ("A", "B"):
        for k in range(2):
            seed = 42 + k
            skill = "none" if arm == "A" else "uncle-bob-craft"
            work_dir = prepare_trial(
                task_id=task_id,
                arm=arm,
                skill_id=skill,
                seed=seed,
            )
            print(f"Prepared: {work_dir}")
            print(f"  Arm={arm}, skill={skill}, seed={seed}")
            records.append(
                TrialRecord(
                    trial_id=_make_trial_id(task_id, skill, arm, seed),
                    task_id=task_id,
                    skill_id=skill,
                    arm=arm,
                    seed=seed,
                    model="opus-4.7@t=0.0",
                    timestamp_utc=datetime.now(timezone.utc).isoformat(),
                )
            )
    return records


def write_records(records: list[TrialRecord], output_path: Path) -> None:
    """Write TrialRecord list as JSON-lines."""
    with open(output_path, "a", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec.to_dict()) + "\n")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_trial_id(task_id: str, skill_id: str, arm: str, seed: int) -> str:
    return f"{task_id}__{skill_id}__{arm}__{seed}"


def _validate_record(rec: TrialRecord) -> list[str]:
    """Validate a TrialRecord against metrics_schema.md. Returns list of issues."""
    issues: list[str] = []
    # Required identity fields must be non-empty
    if not rec.trial_id:
        issues.append("trial_id is empty")
    if not rec.task_id:
        issues.append("task_id is empty")
    if rec.arm not in ("A", "B", "C"):
        issues.append(f"arm is {rec.arm!r}, must be A/B/C")
    return issues


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(description="Skill-Eval Trial Runner")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # prepare
    prep = subparsers.add_parser("prepare", help="Prepare a trial working directory")
    prep.add_argument("--task", required=True, help="Task ID (directory name under corpus/)")
    prep.add_argument("--arm", required=True, choices=["A", "B", "C"])
    prep.add_argument("--skill", default="none", help="Skill under test (none for arm A)")
    prep.add_argument("--seed", type=int, default=0)
    prep.add_argument("--model", default="opus-4.7@t=0.0")
    prep.add_argument("--no-gate", action="store_true", help="Disable gate (arm C)")
    prep.add_argument("--output-dir", default=None, help="Override trials directory")

    # capture
    cap = subparsers.add_parser("capture", help="Capture metrics from a trial working directory")
    cap.add_argument("--working-dir", required=True, help="Path to trial working directory")
    cap.add_argument("--task-id", default=None, help="Task ID override")
    cap.add_argument("--output", default=None, help="JSON-lines output file (appends)")

    # smoke
    smo = subparsers.add_parser("smoke", help="Prepare smoke run directories")
    smo.add_argument("--task", required=True, help="Task ID for smoke run")

    # validate
    val = subparsers.add_parser("validate", help="Validate a JSON-lines file against schema")
    val.add_argument("--input", required=True, help="JSON-lines file to validate")

    args = parser.parse_args()

    if args.command == "prepare":
        work_dir = prepare_trial(
            task_id=args.task,
            arm=args.arm,
            skill_id=args.skill,
            seed=args.seed,
            model=args.model,
            no_gate=args.no_gate,
        )
        print(f"Trial prepared: {work_dir}")
        print(f"  Trial ID: {work_dir.name}")
        print(f"  Arm: {args.arm}, Skill: {args.skill}, Seed: {args.seed}")
        print(f"  Gate: {'OFF' if args.no_gate else 'ON'}")

    elif args.command == "capture":
        work_dir = Path(args.working_dir)
        if not work_dir.is_dir():
            print(f"ERROR: Working directory not found: {work_dir}")
            sys.exit(1)
        rec = capture_metrics(work_dir, args.task_id)
        issues = _validate_record(rec)
        if issues:
            print(f"WARNING: {len(issues)} validation issues:")
            for i in issues:
                print(f"  - {i}")

        # Print summary
        print(json.dumps(rec.to_dict(), indent=2))

        # Write if output specified
        if args.output:
            write_records([rec], Path(args.output))
            print(f"Record appended to {args.output}")

    elif args.command == "smoke":
        records = smoke_run(args.task)
        print(f"\nPrepared {len(records)} smoke trials.")
        print("Working directories:")
        for r in records:
            print(f"  {TRIALS_DIR / r.trial_id}")
        print("\nNext: write code in each working dir, then run 'capture' on each.")

    elif args.command == "validate":
        input_path = Path(args.input)
        if not input_path.exists():
            print(f"ERROR: File not found: {input_path}")
            sys.exit(1)
        issues_total = 0
        records_count = 0
        for line in input_path.read_text().strip().split("\n"):
            if not line.strip():
                continue
            try:
                data = json.loads(line)
                records_count += 1
                # Check required fields
                for field in TrialRecord.__slots__:  # type: ignore[attr-defined]
                    if field not in data:
                        print(f"Record {records_count}: missing field '{field}'")
                        issues_total += 1
            except json.JSONDecodeError as e:
                print(f"Record {records_count}: invalid JSON — {e}")
                issues_total += 1
        print(f"\nValidated {records_count} records, {issues_total} issues.")
        if issues_total == 0:
            print("All records valid against schema.")


if __name__ == "__main__":
    main()
