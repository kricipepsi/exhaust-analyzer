"""P4 isolation layer: build copies of the tree, run a suite inside a copy, classify the result."""

from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

from p4_config import COPY_EXCLUDE, GUARD_MODULES, LAB_PATHS, REPO, SCRATCH, SUITES


def make_copy(dest: Path) -> Path:
    """Copy the repo (minus COPY_EXCLUDE, byte-code caches included in the exclusion) to a fresh dest."""
    shutil.rmtree(dest, ignore_errors=True)
    shutil.copytree(REPO, dest, symlinks=True, ignore=shutil.ignore_patterns(*COPY_EXCLUDE))
    return Path(os.path.realpath(dest))


def suite_env(copy_root: Path, suite: str, out_json: Path) -> dict[str, str]:
    env = dict(os.environ)
    env["PYTHONPATH"] = os.pathsep.join([str(SCRATCH)] + [str(copy_root / p) for p in LAB_PATHS])
    # A same-size mutant written in the same second as the restore would otherwise reuse stale .pyc.
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["P4_ROOT"] = str(copy_root)
    env["P4_MODULES"] = ",".join(GUARD_MODULES[suite])
    env["P4_OUT"] = str(out_json)
    env.pop("COVERAGE_PROCESS_START", None)
    return env


def run_suite(copy_root: Path, suite: str, timeout: float, cov_include: list[str] | None = None,
              cov_data: Path | None = None) -> dict:
    cwd = copy_root / SUITES[suite]
    shutil.rmtree(cwd / ".hypothesis", ignore_errors=True)
    fd, out = tempfile.mkstemp(suffix=".json", prefix="p4g_")
    os.close(fd)
    out_json = Path(out)
    out_json.write_text("{}")
    head = [sys.executable, "-m"]
    if cov_include:
        head += ["coverage", "run", f"--data-file={cov_data}", f"--include={','.join(cov_include)}", "-m"]
    cmd = head + ["pytest", "-q", "--no-header", "-p", "no:cacheprovider", "-p", "p4_guard",
                  "--continue-on-collection-errors", "--hypothesis-seed=0"]
    proc = subprocess.Popen(cmd, cwd=cwd, env=suite_env(copy_root, suite, out_json),
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True,
                            start_new_session=True)
    try:
        stdout, _ = proc.communicate(timeout=timeout)
        timed_out = False
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid, signal.SIGKILL)
        stdout, _ = proc.communicate()
        timed_out = True
    state = json.loads(out_json.read_text() or "{}")
    out_json.unlink()
    lines = [ln for ln in stdout.strip().splitlines() if ln.strip()]
    return {"timed_out": timed_out, "returncode": proc.returncode, "summary": lines[-1] if lines else "",
            "state": state}


def classify(res: dict, baseline_fail: set[str]) -> tuple[str, list[str], list[str]]:
    """-> (outcome, killing assertion nodeids, crash nodeids). Baseline failures are ignored."""
    if res["timed_out"]:
        return "TIMEOUT", [], []
    st = res["state"]
    if st.get("guard_ok") is not True:
        bad = sorted(m for m, f in st.get("modules", {}).items() if f.startswith("IMPORT-FAILED"))
        if bad:  # the mutant broke the module's import (e.g. SyntaxError): a crash, not an assertion
            return "KILLED-WRONG-REASON", [], [f"import {m}: {st['modules'][m]}" for m in bad]
        return "GUARD-FAIL", [], []
    new = [f for f in st.get("failures", []) if f["nodeid"] not in baseline_fail]
    asserts = sorted({f["nodeid"] for f in new if f["kind"] == "assertion"})
    crashes = sorted({f["nodeid"] + " [" + "/".join(f["types"]) + "]" for f in new if f["kind"] == "crash"})
    if asserts:
        return "KILLED", asserts, crashes
    if crashes:
        return "KILLED-WRONG-REASON", [], crashes
    if res["returncode"] not in (0, 1):
        return "KILLED-WRONG-REASON", [], [f"pytest returncode {res['returncode']}"]
    return "SURVIVED", [], []


def apply_span(src: bytes, start: tuple[int, int], end: tuple[int, int], repl: str) -> bytes:
    """Replace the (lineno, utf8-col) span [start, end) of src with repl."""
    lines = src.splitlines(keepends=True)
    offs = [0]
    for ln in lines:
        offs.append(offs[-1] + len(ln))
    a = offs[start[0] - 1] + start[1]
    b = offs[end[0] - 1] + end[1]
    return src[:a] + repl.encode() + src[b:]
