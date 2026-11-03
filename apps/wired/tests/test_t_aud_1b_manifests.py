"""T-AUD-1b: deploy manifests use unique dist names, declare lab imports and pin the closure."""

from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LABS = ("comlab", "dnalab", "dtclab", "gaslab", "obdlab", "symptomlab", "vinlab")
MANIFESTS = [ROOT / "labs" / lab / "pyproject.toml" for lab in LABS] + [
    ROOT / "apps" / "wired" / "pyproject.toml"
]
BARE = set(LABS) | {"wired"}


def _project(path: Path) -> dict:
    return tomllib.loads(path.read_text(encoding="utf-8"))["project"]


def _dep_name(spec: str) -> str:
    return re.split(r"[\s<>=!~;\[]", spec.strip(), maxsplit=1)[0].lower()


def _requirement_lines() -> list[str]:
    text = (ROOT / "requirements.txt").read_text(encoding="utf-8")
    return [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]


def _constraint_lines() -> list[str]:
    text = (ROOT / "constraints.txt").read_text(encoding="utf-8")
    return [ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith("#")]


def test_local_dists_are_prefixed():
    assert len(MANIFESTS) == 8
    for path in MANIFESTS:
        assert _project(path)["name"].startswith("fourdapp-"), path


def test_no_bare_lab_dependency():
    for path in MANIFESTS:
        for spec in _project(path).get("dependencies", []):
            assert _dep_name(spec) not in BARE, (path, spec)


def test_every_local_dependency_has_an_editable_line():
    editable = {
        ROOT / ln.split(None, 1)[1].strip() for ln in _requirement_lines() if ln.startswith("-e ")
    }
    installed = {_project(p / "pyproject.toml")["name"] for p in editable}
    for path in MANIFESTS:
        for spec in _project(path).get("dependencies", []):
            name = _dep_name(spec)
            if name.startswith("fourdapp-"):
                assert name in installed, (path, spec)


def test_dnalab_declares_its_lab_imports():
    deps = {_dep_name(s) for s in _project(ROOT / "labs" / "dnalab" / "pyproject.toml").get("dependencies", [])}
    assert {"fourdapp-symptomlab", "fourdapp-vinlab"} <= deps


def test_requirements_use_pinned_constraints():
    assert "-c constraints.txt" in _requirement_lines()
    lines = _constraint_lines()
    assert len(lines) >= 48
    for ln in lines:
        assert re.match(r"^[A-Za-z0-9._-]+==[^=\s]+$", ln), ln
    assert "streamlit==1.59.0" in lines
    assert "six==1.17.0" in lines
