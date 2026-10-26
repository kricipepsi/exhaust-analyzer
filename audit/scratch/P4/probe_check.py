"""Run a probe test against the original and against one mutant applied to an isolated copy.

Usage: python audit/scratch/P4/probe_check.py <workdir> <mutant id> <probe nodeid relative to repo root>
Prints ORIGINAL / MUTANT outcomes; the copy's module __file__ is asserted by p4_guard as in the matrix.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p4_config import REPO, SCRATCH, SUITES, TARGETS  # noqa: E402
from p4_lib import apply_span, make_copy, suite_env  # noqa: E402


def run(root: Path, suite: str, probe: str) -> str:
    out = Path(os.environ.get("TMPDIR", "/tmp")) / "p4_probe_guard.json"
    env = suite_env(root, suite, out)
    p = subprocess.run([sys.executable, "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider",
                        "-p", "p4_guard", str(REPO / probe)], cwd=root / SUITES[suite], env=env,
                       capture_output=True, text=True)
    st = json.loads(out.read_text())
    last = [ln for ln in p.stdout.splitlines() if ln.strip()][-1]
    return f"{last} | guard_ok={st.get('guard_ok')} failures={[f['types'] for f in st['failures']]}"


def main() -> None:
    work, mid, probe = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    m = next(x for x in json.loads((SCRATCH / "mutants.json").read_text())["mutants"] if x["id"] == mid)
    suite = TARGETS[m["target"]][2]
    root = make_copy(work / "probe")
    print("ORIGINAL", run(root, suite, probe))
    path = root / m["file"]
    orig = path.read_bytes()
    path.write_bytes(apply_span(orig, tuple(m["start"]), tuple(m["end"]), m["replacement"]))
    try:
        print("MUTANT  ", mid, repr(m["original"][:50]), "->", repr(m["replacement"][:50]))
        print("MUTANT  ", run(root, suite, probe))
    finally:
        path.write_bytes(orig)
    assert path.read_bytes() == (REPO / m["file"]).read_bytes()


if __name__ == "__main__":
    main()
