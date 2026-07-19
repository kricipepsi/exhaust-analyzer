"""Tests for ``gas_lab_ontology.yaml`` and ``ontology_loader.py``.

Covers the seven success criteria from ``T-P2-2_yaml_ontology.md``.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from gaslab.contracts import ChemicalSignature
from gaslab.ontology_loader import OntologyLoadError, load_ontology


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ONTOLOGY_PATH = Path(__file__).resolve().parent.parent.parent / "gaslab" / "data" / "gas_lab_ontology.yaml"


def _load_raw() -> dict:
    """Load the YAML directly (bypasses loader validation) for low-level checks."""
    with ONTOLOGY_PATH.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


# ---------------------------------------------------------------------------
# 1. YAML parses
# ---------------------------------------------------------------------------

def test_yaml_parses() -> None:
    """``yaml.safe_load`` succeeds on the ontology file."""
    ontology = load_ontology(ONTOLOGY_PATH)
    assert isinstance(ontology, dict)
    assert "faults" in ontology


# ---------------------------------------------------------------------------
# 2. 30 fault entries
# ---------------------------------------------------------------------------

def test_34_fault_entries() -> None:
    """Ontology contains exactly 34 fault entries matching ``ChemicalSignature``."""
    ontology = _load_raw()
    fault_keys = list(ontology["faults"].keys())
    expected = {e.value for e in ChemicalSignature}
    assert len(fault_keys) == 34, f"expected 34 faults, got {len(fault_keys)}"
    assert set(fault_keys) == expected, (
        f"fault keys must match ChemicalSignature values exactly.\n"
        f"Missing: {expected - set(fault_keys)}\n"
        f"Extra:   {set(fault_keys) - expected}"
    )


# ---------------------------------------------------------------------------
# 3. Every fault has a citation
# ---------------------------------------------------------------------------

def test_every_fault_has_citation() -> None:
    """Every fault entry has a non-empty ``citation`` starting with ``GAS_WIKI §7.`` or ``GAS_WIKI §8.``."""
    ontology = _load_raw()
    for name, entry in ontology["faults"].items():
        citation = entry.get("citation", "")
        assert isinstance(citation, str) and citation, (
            f"{name}: missing or empty citation"
        )
        assert citation.startswith(("GAS_WIKI §7.", "GAS_WIKI §8.")), (
            f"{name}: citation {citation!r} does not start with 'GAS_WIKI §7.' or 'GAS_WIKI §8.'"
        )


# ---------------------------------------------------------------------------
# 4. Validity gates match wiki
# ---------------------------------------------------------------------------

def test_validity_gates_match_wiki() -> None:
    """Triangle valid range == [14.0, 16.0]; dilution floor == 6.0."""
    ontology = _load_raw()
    gates = ontology["validity_gates"]

    triangle = gates["exhaust_gas_triangle"]
    assert triangle["sum_valid_min"] == 14.0  # wiki: GAS_WIKI §6.1
    assert triangle["sum_valid_max"] == 16.0  # wiki: GAS_WIKI §6.1

    dilution = gates["dilution_screen"]
    assert dilution["co_plus_co2_floor"] == 6.0  # wiki: GAS_WIKI §6.2


# ---------------------------------------------------------------------------
# 5. Collision rule present
# ---------------------------------------------------------------------------

def test_collision_rule_present() -> None:
    """The CO+O₂ collision rule per ``GAS_WIKI §8.5`` is encoded."""
    ontology = _load_raw()
    grammar = ontology["reasoning_grammar"]
    assert "collision_rule" in grammar, "missing collision_rule in reasoning_grammar"
    cr = grammar["collision_rule"]
    assert cr["citation"] == "GAS_WIKI §8.5"
    assert "co_tier_max" in cr
    assert "o2_threshold" in cr


# ---------------------------------------------------------------------------
# 6. Masking rule present
# ---------------------------------------------------------------------------

def test_masking_rule_present() -> None:
    """The low-NOₓ + high-HC + high-O₂ override per ``GAS_WIKI §8.4`` is encoded."""
    ontology = _load_raw()
    grammar = ontology["reasoning_grammar"]
    assert "masking_rule" in grammar, "missing masking_rule in reasoning_grammar"
    mr = grammar["masking_rule"]
    assert mr["citation"] == "GAS_WIKI §8.4"
    assert "hc_threshold" in mr
    assert "o2_threshold" in mr
    assert "nox_threshold" in mr


# ---------------------------------------------------------------------------
# 7. DNA-gated faults
# ---------------------------------------------------------------------------

# The six values in GAS_VOCABULARY §3.1 that list an explicit DNA gate.
# (Task T-P2-2 says "7" but the canonical wiki §3.1 lists 6 — IGNITION_MISFIRE
# notes "cylinder_count" as a DNA dependency but does NOT list it as a gate.)
DNA_GATED_VALUES: set[str] = {
    "CATALYST_NOT_LIGHTING_OFF",
    "CATALYST_OVERWHELMED",
    "GDI_INTAKE_VALVE_CARBON",
    "GDI_HPFP_INTERNAL_SEAL_LEAK",
    "EGR_STUCK_CLOSED",
    "EGR_STUCK_OPEN",
}


def test_dna_gated_faults() -> None:
    """Every DNA-gated ``ChemicalSignature`` from ``GAS_VOCABULARY §3.1``
    declares a ``dna_gate`` field in the ontology."""
    ontology = _load_raw()
    faults = ontology["faults"]

    for name in DNA_GATED_VALUES:
        entry = faults.get(name)
        assert entry is not None, f"{name}: not found in ontology faults"
        dna_gate = entry.get("dna_gate")
        assert dna_gate is not None, (
            f"{name}: expected dna_gate field per GAS_VOCABULARY §3.1, got {dna_gate!r}"
        )
        assert "field" in dna_gate, f"{name}: dna_gate missing 'field' key"
        assert "value" in dna_gate, f"{name}: dna_gate missing 'value' key"

    # No non-gated value should have a dna_gate (negative check — sample)
    assert "dna_gate" not in faults.get("NORMAL_OPERATION", {})
    assert "dna_gate" not in faults.get("RICH_MIXTURE", {})


# ---------------------------------------------------------------------------
# Loader error paths
# ---------------------------------------------------------------------------

def test_loader_raises_on_missing_file(tmp_path: Path) -> None:
    """``load_ontology`` raises ``OntologyLoadError`` for a missing file."""
    bad = tmp_path / "nonexistent.yaml"
    with pytest.raises(OntologyLoadError, match="cannot read file"):
        load_ontology(bad)


def test_loader_raises_on_bad_yaml(tmp_path: Path) -> None:
    """``load_ontology`` raises ``OntologyLoadError`` for unparseable YAML."""
    bad = tmp_path / "bad.yaml"
    bad.write_text(": broken :: yaml :", encoding="utf-8")
    with pytest.raises(OntologyLoadError, match="YAML parse failed"):
        load_ontology(bad)


def test_loader_raises_on_missing_keys(tmp_path: Path) -> None:
    """``load_ontology`` raises ``OntologyLoadError`` when required keys are absent."""
    bad = tmp_path / "minimal.yaml"
    bad.write_text("version: '1.0'\nscope: test\n", encoding="utf-8")
    with pytest.raises(OntologyLoadError, match="missing required top-level key"):
        load_ontology(bad)


def test_loader_default_path_works() -> None:
    """``load_ontology()`` with no argument resolves the default path."""
    ontology = load_ontology()
    assert isinstance(ontology, dict)
    assert "faults" in ontology
    assert len(ontology["faults"]) == 34
