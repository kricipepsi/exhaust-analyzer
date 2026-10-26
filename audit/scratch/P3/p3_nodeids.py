"""pytest plugin (P3 audit): record every test's node ID and final outcome to $P3_NODEIDS_OUT (JSON)."""
import json
import os

_RES: dict[str, str] = {}


def pytest_runtest_logreport(report):
    nid = report.nodeid
    if report.when == "call":
        _RES[nid] = "passed" if report.passed else ("skipped" if report.skipped else "failed")
    elif report.when == "setup" and not report.passed:
        _RES[nid] = "skipped" if report.skipped else "error"
    elif report.when == "teardown" and report.failed:
        _RES[nid] = "error"


def pytest_sessionfinish(session):
    out = os.environ.get("P3_NODEIDS_OUT")
    if out:
        with open(out, "w") as f:
            json.dump({"rootdir": str(session.config.rootpath), "results": dict(sorted(_RES.items()))}, f, indent=0, sort_keys=True)
