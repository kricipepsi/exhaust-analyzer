from gaslab.contracts import ChemicalSignature
from gaslab.family_map import CANONICAL_FAMILIES, SIGNATURE_TO_FAMILY


def test_all_32_signatures_mapped() -> None:
    assert set(SIGNATURE_TO_FAMILY) == set(ChemicalSignature)


def test_every_value_is_canonical() -> None:
    assert set(SIGNATURE_TO_FAMILY.values()) <= CANONICAL_FAMILIES


def test_ambiguous_decisions_pinned() -> None:
    assert {
        ChemicalSignature.HIGH_COMBUSTION_TEMP: "lean_condition",
        ChemicalSignature.EGR_STUCK_CLOSED: "lean_condition",
        ChemicalSignature.EGR_STUCK_OPEN: "misfire",
        ChemicalSignature.VACUUM_REGULATOR_DIAPHRAGM_RUPTURE: "rich_mixture",
        ChemicalSignature.GDI_HPFP_INTERNAL_SEAL_LEAK: "rich_mixture",
        ChemicalSignature.EVAP_CANISTER_SATURATED: "rich_mixture",
        ChemicalSignature.INCOMPLETE_OXIDATION: "catalyst_failure",
        ChemicalSignature.INCOMPLETE_COMBUSTION: "misfire",
    }.items() <= SIGNATURE_TO_FAMILY.items()


def test_gaslab_unreachable_families_absent() -> None:
    assert "ecu_fault" not in SIGNATURE_TO_FAMILY.values()
    assert "non_starter" not in SIGNATURE_TO_FAMILY.values()
