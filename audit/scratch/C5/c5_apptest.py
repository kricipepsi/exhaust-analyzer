"""C5 helper: drive the real apps/ui/app.py headless with streamlit.testing.AppTest.

sys.path as the Render shim sets it (apps/ui first) plus labs/comlab (F-C4-1 work-around, only
needed once a run gets past GASLab; noted per probe).
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
logging.disable(logging.WARNING)


def new_app(with_registry: bool = True):
    for p in (["labs/comlab"] if with_registry else []) + ["apps/ui"]:
        if str(ROOT / p) not in sys.path:
            sys.path.insert(0, str(ROOT / p))
    from streamlit.testing.v1 import AppTest

    at = AppTest.from_file(str(ROOT / "apps/ui/app.py"), default_timeout=120)
    at.run()
    assert not at.exception, at.exception
    return at


def by_label(elements, label: str):
    hits = [e for e in elements if e.label == label]
    assert hits, f"no widget labelled {label!r}: {[e.label for e in elements]}"
    return hits[0]


def set_num(at, key: str, value):
    at.number_input(key=key).set_value(value)


def click_run(at):
    by_label(at.button, "🔬 Run Diagnostic Seam").click()
    at.run()
    assert not at.exception, at.exception
    return at


def errors(at) -> list[str]:
    return [e.value for e in at.error]


def pick_symptom(at, t1: str, t2: str):
    by_label(at.selectbox, "Primary symptom (Tier 1)").set_value(t1)
    at.run()
    by_label(at.selectbox, "Subfield filter (Tier 2)").set_value(t2)
    at.run()


def markdown_text(at) -> str:
    return "\n".join(str(m.value) for m in at.markdown) + "\n" + "\n".join(
        str(c.value) for c in at.caption
    )
