"""Tests for harness.descriptor — ModuleDescriptor and GASLab descriptor builder."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
# GASLab package at 4DLabV2/labs/gaslab/
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "labs" / "gaslab"))

from harness.descriptor import (
    FaultBox,
    FieldRange,
    ModuleDescriptor,
    build_gaslab_descriptor,
)
try:
    from tests.fixtures.descriptor import _BOX_DEFS
except ImportError:
    try:
        from gaslab.tests.fixtures.descriptor import _BOX_DEFS
    except ImportError:
        _BOX_DEFS = []


try:
    from gaslab.contracts import ChemicalSignature
    _HAS_GASLAB = True
except ImportError:
    _HAS_GASLAB = False
    ChemicalSignature = None  # type: ignore[assignment]


# --- FieldRange / FaultBox / ModuleDescriptor unit tests ---


def test_field_range_creation():
    fr = FieldRange("gas_hc", "int", 0, 20000)
    assert fr.name == "gas_hc"
    assert fr.type_ == "int"
    assert fr.min_ == 0
    assert fr.max_ == 20000
    assert fr.enum_values is None


def test_field_range_with_enum():
    fr = FieldRange("ctx_engine_state", "str", enum_values=["STABILIZED_IDLE", "REGULATORY_HIGH_IDLE"])
    assert fr.enum_values == ["STABILIZED_IDLE", "REGULATORY_HIGH_IDLE"]


def test_fault_box_creation():
    fb = FaultBox(
        signature="RICH_MIXTURE",
        dimensions={"gas_hc": (0, 500), "gas_co": (1.5, 15), "gas_co2": (0, 14), "gas_o2": (0, 0.5), "gas_nox": (0, 500)},
        source="GAS_WIKI §7.2",
    )
    assert fb.signature == "RICH_MIXTURE"
    assert fb.dimensions["gas_co"] == (1.5, 15)


def test_module_descriptor_creation():
    md = ModuleDescriptor(
        name="test",
        fields=[FieldRange("x", "float", 0, 1)],
        boxes={"test_sig": FaultBox("test_sig", {"x": (0, 1)}, "src")},
        build_args=lambda row: (float(row["x"]),),
        entry_point=lambda x: x,
        extract_expected=lambda row: {"val": row.get("expected_val", "")},
        diff=lambda actual, expected: [],
    )
    assert md.name == "test"
    assert md.get_field("x") is not None
    assert md.get_field("nonexistent") is None
    assert len(md.boxes) == 1


# --- Box table structural tests (no gaslab import needed) ---


def test_all_box_dims_have_five_gas_fields():
    """Every box must define all 5 gas dimensions with min <= max."""
    gas_fields = {"gas_hc", "gas_co", "gas_co2", "gas_o2", "gas_nox"}
    for bd in _BOX_DEFS:
        dims = bd["dims"]
        assert set(dims.keys()) == gas_fields, f"{bd['sig']}: expected 5 gas fields, got {set(dims.keys())}"
        for field, (lo, hi) in dims.items():
            assert lo <= hi, f"{bd['sig']}.{field}: min={lo} > max={hi}"


def test_box_table_no_duplicate_signatures():
    sigs = [bd["sig"] for bd in _BOX_DEFS]
    assert len(sigs) == len(set(sigs)), f"Duplicate signatures: {[s for s in sigs if sigs.count(s) > 1]}"


def test_box_table_covers_all_enum_members():
    """If gaslab is importable, verify every ChemicalSignature has a box."""
    if not _HAS_GASLAB or ChemicalSignature is None:
        pytest.skip("gaslab not importable in this environment")
    enum_sigs = {e.value for e in ChemicalSignature}
    box_sigs = {bd["sig"] for bd in _BOX_DEFS}
    missing = enum_sigs - box_sigs
    extra = box_sigs - enum_sigs
    assert not missing, f"ChemicalSignature members missing from box table: {missing}"
    assert not extra, f"Box table entries not in ChemicalSignature: {extra}"


# --- GASLab descriptor tests (require gaslab) ---


@pytest.mark.skipif(not _HAS_GASLAB, reason="gaslab not importable in this environment")
def test_gaslab_descriptor_loads():
    """The GASLab ModuleDescriptor loads, exposes one box per ChemicalSignature,
    and every box dimension has a (min, max) with min <= max."""
    desc = build_gaslab_descriptor()
    assert desc.name == "GASLab"
    assert len(desc.fields) == 23  # gas(5) + ctx(4) + dna(14) = 23

    # One box per ChemicalSignature member
    assert ChemicalSignature is not None
    enum_sigs = {e.value for e in ChemicalSignature}
    assert set(desc.boxes.keys()) == enum_sigs, (
        f"Mismatch: boxes={set(desc.boxes.keys()) - enum_sigs}, "
        f"enum={enum_sigs - set(desc.boxes.keys())}"
    )

    # Every box has all 5 gas dimensions with min <= max
    gas_fields = {"gas_hc", "gas_co", "gas_co2", "gas_o2", "gas_nox"}
    for sig, box in desc.boxes.items():
        assert set(box.dimensions.keys()) == gas_fields, f"{sig}: expected 5 gas fields"
        for field, (lo, hi) in box.dimensions.items():
            assert lo <= hi, f"{sig}.{field}: min={lo} > max={hi}"
        assert box.source, f"{sig}: missing source citation"

    # Entry point and callables are wired
    assert desc.entry_point is not None
    assert desc.build_args is not None
    assert desc.extract_expected is not None
    assert desc.diff is not None


@pytest.mark.skipif(not _HAS_GASLAB, reason="gaslab not importable in this environment")
def test_gaslab_descriptor_build_args_smoke():
    """build_args constructs valid GasReading + GasLabContext from a row dict."""
    desc = build_gaslab_descriptor()
    row = {
        "gas_hc": "15", "gas_co": "0.2", "gas_co2": "15.0", "gas_o2": "0.2", "gas_nox": "30",
        "ctx_engine_state": "STABILIZED_IDLE",
        "ctx_secondary_air_injection_active": "False",
        "ctx_lambda_measured": "",
        "dna_engine_displacement_liters": "1.6",
        "dna_cylinder_count": "4",
        "dna_number_of_banks": "1",
        "dna_euro_emission_category": "EURO_4",
        "dna_fuel_delivery_type": "NON_GDI",
        "dna_induction_type": "NATURALLY_ASPIRATED",
        "dna_upstream_o2_type": "NARROWBAND_0_TO_1V",
        "dna_secondary_air_equipped": "False",
        "dna_has_catalyst": "True",
        "dna_egr_equipped": "False",
        "dna_target_lambda_v112": "",
        "dna_co_low_idle": "",
        "dna_co_high_idle": "",
        "dna_confidence": "NONE",
    }
    args = desc.build_args(row)
    assert len(args) == 2  # (reading, context)
    reading, context = args
    assert reading.hc == 15
    assert reading.co == 0.2
    assert context.engine_state.value == "STABILIZED_IDLE"
    assert context.dna.has_catalyst is True
