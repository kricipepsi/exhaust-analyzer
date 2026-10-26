"""P5 case runner — executes INSIDE the Render-simulated venv, one case per process.

usage: <render>/.venv/bin/python cases.py <render_root> <case> <mode>
  case: blank | unticked | minimal | minimal_vin | taint | control_pos | control_clean
  mode: faithful   sys.path as `streamlit run app.py` builds it (script dir = repo root first)
        comlab     faithful + labs/comlab (the F-C1-5 work-around the audit prompt names)

Drives the root app.py shim (which runpy's apps/ui/app.py) with streamlit.testing AppTest, i.e. the
same build_diagnose_payload() -> wired.composition.diagnose() calls the deployed page makes.
A sys.addaudithook records runtime capability events (subprocess, socket, file write, sqlite) and
attributes each to the innermost first-party frame (a file under <render_root>, not under .venv).
Prints one JSON object on stdout.
"""

from __future__ import annotations

import json
import os
import sys
import traceback

ROOT = os.path.realpath(sys.argv[1])
CASE, MODE = sys.argv[2], sys.argv[3]
VENV = os.path.join(ROOT, ".venv")

# --- streamlit bootstrap._fix_sys_path: the main script's directory goes first -------------------
sys.path.insert(0, ROOT)
if MODE == "comlab":
    sys.path.insert(0, os.path.join(ROOT, "labs", "comlab"))

EVENTS: set[tuple[str, str, str]] = set()
WATCH = {"subprocess.Popen", "os.system", "os.exec", "os.posix_spawn", "os.spawn", "os.fork",
         "socket.connect", "socket.bind", "socket.getaddrinfo", "socket.sendto",
         "urllib.Request", "http.client.connect", "sqlite3.connect", "os.remove", "os.rename",
         "os.mkdir", "os.chmod", "shutil.rmtree", "shutil.copyfile", "shutil.move", "webbrowser.open",
         "open"}
_ON = False


def _site() -> str:
    f = sys._getframe(2)
    third = None
    while f is not None:
        if f.f_code.co_filename.startswith("<"):  # <frozen ...>, <string>: never first-party
            f = f.f_back
            continue
        fn = os.path.realpath(f.f_code.co_filename)
        if fn.startswith(CTRL):
            return f"controls/{os.path.basename(fn)}:{f.f_lineno}"
        if fn.startswith(ROOT) and not fn.startswith(VENV) and not fn.endswith("/cases.py"):
            return f"{os.path.relpath(fn, ROOT)}:{f.f_lineno}"
        if third is None and "site-packages" in fn:
            third = fn.split("site-packages/")[1].split("/")[0]
        f = f.f_back
    return f"third-party:{third or 'stdlib'}"


def _norm(a) -> str:
    s = str(a)
    s = s.replace(ROOT, "<render>")
    if s.startswith("/tmp") or "/tmp/" in s:
        s = "<tmp>"
    return s[:120]


def hook(event, args):
    if args and "__pycache__" in str(args[0]):
        return
    if not _ON or event not in WATCH and not event.startswith(("os.exec", "os.spawn")):
        return
    if event == "open":
        path, mode = args[0], args[1] if len(args) > 1 else "r"
        if not isinstance(mode, str) or not any(c in mode for c in "wax+"):
            return
        detail = f"{_norm(path)} mode={mode}"
    elif event == "sqlite3.connect":
        detail = _norm(args[0])
    elif event.startswith("socket"):
        detail = _norm(args[1] if len(args) > 1 else args)
    else:
        detail = _norm(args[0] if args else "")
    EVENTS.add((event, _site(), detail))


sys.dont_write_bytecode = True
CTRL = os.path.join(os.path.dirname(os.path.realpath(__file__)), "controls")
sys.addaudithook(hook)

MARK = "<b id=p5taint>P5TAINT</b>"


def app_test(path: str):
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(path, default_timeout=180)
    at.run()
    return at


def lab(at, kind, label):
    return [e for e in getattr(at, kind) if e.label == label][0]


def out_of(at) -> dict:
    res = at.session_state["diagnose_result"] if "diagnose_result" in at.session_state else None
    html = [str(m.value) for m in at.markdown if getattr(m, "allow_html", False)]
    verdict = None
    if res is not None:
        v = res.diagnostic_verdict
        verdict = (f"{v.fault_code} {v.fault_family} conf={v.confidence_score:.2f} "
                   f"abstained={v.abstained} mode={res.execution_meta.degradation_mode}")
    return {
        "exception": [str(e.value)[:300] for e in at.exception],
        "st_error": [str(e.value)[:300] for e in at.error],
        "verdict": verdict,
        "taint_in_unsafe_html": sum(MARK in h for h in html),
        "unsafe_html_elements": len(html),
    }


def click(at):
    lab(at, "button", "🔬 Run Diagnostic Seam").click()
    at.run()


def fill(at, **kv):
    for k, v in kv.items():
        at.number_input(key=k).set_value(v)
    at.run()


def symptom(at):
    lab(at, "selectbox", "Primary symptom (Tier 1)").set_value("⬇️ Lack of Power / Hesitation")
    at.run()
    lab(at, "selectbox", "Subfield filter (Tier 2)").set_value("Flat / sluggish always")
    at.run()


GOOD_GAS = {"gas_hc": 80, "gas_co": 0.3, "gas_co2": 14.8, "gas_o2": 0.3, "gas_nox": 50}

result: dict = {"case": CASE, "mode": MODE}
try:
    _ON = True
    if CASE in ("control_pos", "control_clean"):
        # planted: control_pos does a subprocess, a file write and renders a text_input unescaped
        at = app_test(os.path.join(CTRL, f"st_{CASE}.py"))
        at.text_input(key="t").set_value(MARK)
        at.run()
        lab(at, "button", "go").click()
        at.run()
        result.update(out_of(at))
    else:
        at = app_test(os.path.join(ROOT, "app.py"))
        if CASE == "blank":
            click(at)  # first load, nothing typed, all four module boxes at their default (ticked)
        elif CASE == "unticked":
            for name in ("GASLab", "OBDLab", "DTCLab", "DNA / VIN"):
                lab(at, "checkbox", name).uncheck()
                at.run()
            click(at)
        elif CASE in ("minimal", "minimal_vin", "taint"):
            lab(at, "checkbox", "OBDLab").uncheck()
            at.run()
            lab(at, "checkbox", "DTCLab").uncheck()
            at.run()
            if CASE in ("minimal_vin", "taint"):
                at.text_input(key="vin_input").set_value("WME01MC01XH072806")
                at.run()
            symptom(at)
            fill(at, **GOOD_GAS)
            if CASE == "taint":
                # every free-text widget the page offers that survives the DTCLab untick
                tainted = [t for t in list(at.text_input) + list(at.text_area) if t.key != "vin_input"]
                for t in tainted:
                    t.set_value(MARK)
                result["tainted_widgets"] = sorted(str(t.label) for t in tainted)
                at.run()
            click(at)
        result.update(out_of(at))
except Exception as e:  # noqa: BLE001 — the probe reports, it does not judge
    result["probe_error"] = f"{type(e).__name__}: {e}"[:300]
    result["probe_tb"] = traceback.format_exc().splitlines()[-3:]
_ON = False

fp = sorted({m.split(".")[0] for m in sys.modules})
result["loaded_top_modules"] = fp
result["registry_loaded"] = "registry" in sys.modules
result["capability_events"] = sorted([list(e) for e in EVENTS])
sys.stdout.write("\nP5JSON " + json.dumps(result, sort_keys=True) + "\n")
