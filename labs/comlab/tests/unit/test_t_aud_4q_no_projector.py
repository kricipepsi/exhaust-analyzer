"""T-AUD-4q (F-D2-10/11): COMLab has no DNA projector; the composition builds each lab's view.

Tags: NEW fails on the base fix/T-AUD-4q spec commit.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

DOCS = Path(__file__).resolve().parents[2] / "docs"


def test_projector_modules_are_gone() -> None:
    """NEW: comlab.projection and comlab.schemas.lab_dna_views no longer exist."""
    assert importlib.util.find_spec("comlab.projection") is None
    assert importlib.util.find_spec("comlab.schemas.lab_dna_views") is None


def test_comlab_docs_name_no_projector_call() -> None:
    """NEW: no COMLab design doc still routes a lab view through COMLab.project()."""
    for rel in ("COMLab_HLD.md", "COMLab_LLD.md", "Vocabulary/DTC_VOCABULARY.md"):
        text = (DOCS / rel).read_text(encoding="utf-8")
        for stale in ("COMLab.project(", "project_all(", "def project("):
            assert stale not in text, (rel, stale)
        assert "_build_" in text, rel
