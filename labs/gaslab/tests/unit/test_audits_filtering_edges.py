"""T-GASA-10 (F-C2-13): the collision audit counts only filtering edges as a resolution path."""

from __future__ import annotations

from gaslab.audits import _has_resolution, find_uncovered_overlaps
from gaslab.ontology_loader import load_ontology


def test_note_only_and_physical_check_edges_do_not_resolve() -> None:
    """resolution.apply_differentiators: physical_check edges are informational; a note-only edge filters nothing."""
    assert not _has_resolution({"differentiator_edges": [{"type": "physical_check", "key": "X"}]})
    assert not _has_resolution({"differentiator_edges": [{"type": "rpm_differential", "note": "clears at RPM"}]})
    assert not _has_resolution({"differentiator_edges": [{"type": "rpm_differential", "appears_in_states": []}]})
    assert not _has_resolution({"differentiator_edges": [{"type": "rpm_differential", "route_when_matched": False}]})


def test_filtering_edges_and_dna_gate_resolve() -> None:
    assert _has_resolution({"dna_gate": {"field": "emissions.egr_equipped"}})
    assert _has_resolution({"differentiator_edges": [{"type": "dna", "field": "f", "equals": True}]})
    assert _has_resolution({"differentiator_edges": [{"type": "rpm_differential", "appears_in_states": ["S"]}]})
    assert _has_resolution({"differentiator_edges": [{"type": "rpm_differential", "route_when_matched": True}]})


def test_egr_dilution_overlaps_are_reported() -> None:
    """The F-C2-13 probe pairs are no longer hidden by EGR_DILUTION_MISFIRE's note-only edge."""
    uncovered = {frozenset(p) for p in find_uncovered_overlaps(load_ontology())}
    assert frozenset({"EGR_DILUTION_MISFIRE", "RICH_MISFIRE"}) in uncovered
    assert frozenset({"EGR_DILUTION_MISFIRE", "INCOMPLETE_COMBUSTION"}) in uncovered
