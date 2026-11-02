"""Control (ii) replacement for router.execute_triage_loop (the first planted mutant, ceiling -> 5.0, was
killed only by crashes). Usage: python audit/scratch/P4/planted_extra.py <workdir> -> planted_extra.json
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from p4_config import SCRATCH  # noqa: E402
from p4_lib import make_copy, run_suite  # noqa: E402
from run_matrix import planted_mutant, run_one  # noqa: E402

TEST = "tests/unit/test_tag_discriminator.py::test_misfire_history_lifts_misfire_family"


def main() -> None:
    root = make_copy(Path(sys.argv[1]) / "wx")
    base = run_suite(root, "comlab", 600)
    bf = {"comlab": {f["nodeid"] for f in base["state"]["failures"]}}
    out = {"baseline_summary": base["summary"].split(" in ")[0], "baseline_guard": base["state"]["guard_ok"]}
    for kind, orig, repl in [("PLANTED", "score_val + self._discriminator_weight", "score_val - 0.5"),
                             ("CEILING-5.0", "_SCORE_CEILING", "5.0")]:
        m = planted_mutant("router.execute_triage_loop", 1135 if kind != "PLANTED" else 1134, orig, repl,
                           "PLANTED")
        r = run_one(root, m, bf)
        out[kind] = {"named_test": TEST if kind == "PLANTED" else None, "outcome": r["outcome"],
                     "named_test_killed": TEST in r["killing_tests"], "killing_tests": r["killing_tests"],
                     "crash_tests": r["crash_tests"], "guard_ok": r["guard_ok"]}
    (SCRATCH / "planted_extra.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
