"""KG/Registry consistency — 4-audit validation suite.

Audit 1 — Node coverage: all 30 fault IDs present, counts per family correct.
Audit 2 — Sibling resolution: zero dangling ``differential_siblings`` references.
Audit 3 — Enum validity: every ``fault_family`` and ``editor_severity_hint``
         is a valid enum value.
Audit 4 — Field constraint drift guard: ``mechanical_failure_mode`` ≤ 280 chars,
         ``ui_remediation_steps`` 1–8 items, ``differential_siblings`` 0–5 items,
         ``impacted_subsystems`` 1–8 items.

Source: COMLab_LLD.md §9.4.
"""

from __future__ import annotations

import pytest

from comlab.core.fault_atlas_kg import FaultAtlasKG


# ---------------------------------------------------------------------------
# Expected family counts (LLD §9.4 — 30 fault nodes total)
# ---------------------------------------------------------------------------
EXPECTED_FAMILY_COUNTS = {
    "rich_mixture": 13,
    "lean_condition": 10,
    "misfire": 10,
    "sensor_fault": 8,
    "ecu_fault": 9,
    "catalyst_failure": 9,
    "exhaust_leak": 8,
    "ignition_fault": 7,
    "mechanical_wear": 13,
    "cam_timing": 8,
    "non_starter": 6,
    "no_fault": 1,
    "invalid_input": 6,
}
EXPECTED_TOTAL = 108

VALID_FAULT_FAMILIES = frozenset(EXPECTED_FAMILY_COUNTS)
VALID_SEVERITY_HINTS = frozenset({"INFORMATIONAL", "WATCH", "REPAIR", "URGENT"})


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def kg() -> FaultAtlasKG:
    """Load the full KG once per test session."""
    return FaultAtlasKG()


@pytest.fixture(scope="session")
def all_nodes(kg: FaultAtlasKG) -> dict:
    """Access internal node index for audit traversal."""
    return kg._nodes


# ===================================================================
# Audit 1 — Node coverage
# ===================================================================
class TestNodeCoverage:
    """All 30 fault IDs load correctly with expected per-family counts."""

    def test_node_count_per_family(self, kg: FaultAtlasKG, all_nodes: dict) -> None:
        """Audit 1a: node count per family matches expected (LLD §9.4)."""
        counts: dict[str, int] = {family: 0 for family in EXPECTED_FAMILY_COUNTS}
        for node in all_nodes.values():
            family = node.fault_family
            assert family in counts, (
                f"Unknown fault_family {family!r} — not in expected families"
            )
            counts[family] += 1

        for family, expected in EXPECTED_FAMILY_COUNTS.items():
            assert counts[family] == expected, (
                f"Family {family}: expected {expected} nodes, got {counts[family]}"
            )

    def test_all_fault_ids_present(self, kg: FaultAtlasKG) -> None:
        """Audit 1b: total node count == 30 (LLD §9.4)."""
        assert kg.node_count == EXPECTED_TOTAL, (
            f"Expected {EXPECTED_TOTAL} fault nodes, got {kg.node_count}"
        )


# ===================================================================
# Audit 2 — Sibling resolution
# ===================================================================
class TestSiblingResolution:
    """Every ``differential_siblings`` entry resolves to another loaded node."""

    def test_no_dangling_differential_siblings(
        self, kg: FaultAtlasKG, all_nodes: dict
    ) -> None:
        """Audit 2: every sibling ref must resolve in the KG."""
        dangling: list[tuple[str, str]] = []
        for fault_id, node in all_nodes.items():
            for sibling_id in node.differential_siblings:
                if sibling_id not in all_nodes:
                    dangling.append((fault_id, sibling_id))

        assert not dangling, (
            f"Dangling differential_siblings found: "
            f"{'; '.join(f'{src} -> {tgt}' for src, tgt in dangling)}"
        )


# ===================================================================
# Audit 3 — Enum validity
# ===================================================================
class TestEnumValidity:
    """Every ``fault_family`` and ``editor_severity_hint`` is a valid value."""

    def test_all_enum_values_valid(self, all_nodes: dict) -> None:
        """Audit 3: fault_family and editor_severity_hint must be valid."""
        bad_family: list[tuple[str, str]] = []
        bad_severity: list[tuple[str, str]] = []

        for fault_id, node in all_nodes.items():
            if node.fault_family not in VALID_FAULT_FAMILIES:
                bad_family.append((fault_id, node.fault_family))
            hint = node.editor_severity_hint
            if hint is not None and hint not in VALID_SEVERITY_HINTS:
                bad_severity.append((fault_id, hint))

        failures: list[str] = []
        if bad_family:
            failures.append(
                f"Invalid fault_family values: "
                f"{'; '.join(f'{fid}={val}' for fid, val in bad_family)}"
            )
        if bad_severity:
            failures.append(
                f"Invalid editor_severity_hint values: "
                f"{'; '.join(f'{fid}={val}' for fid, val in bad_severity)}"
            )
        assert not failures, "\n".join(failures)


# ===================================================================
# Audit 4 — Field constraint compliance (drift guard)
# ===================================================================
class TestFieldConstraints:
    """Every node respects the schema constraints — wiki drift guard."""

    def test_field_constraints_all_nodes(self, all_nodes: dict) -> None:
        """Audit 4: field-level constraint checks on all 30 nodes.

        mechanical_failure_mode ≤ 280 chars          (LLD §3.4)
        ui_remediation_steps 1–8 items              (LLD §3.4)
        differential_siblings 0–5 items             (LLD §3.3 Q1)
        impacted_subsystems 1–8 items               (LLD §3.4)
        """
        violations: list[str] = []

        for fault_id, node in all_nodes.items():
            mfm_len = len(node.mechanical_failure_mode)
            if mfm_len > 280:
                violations.append(
                    f"{fault_id}: mechanical_failure_mode {mfm_len} chars (max 280)"
                )

            steps = node.ui_remediation_steps
            if not (1 <= len(steps) <= 8):
                violations.append(
                    f"{fault_id}: ui_remediation_steps {len(steps)} items (need 1–8)"
                )

            siblings = node.differential_siblings
            if len(siblings) > 5:
                violations.append(
                    f"{fault_id}: differential_siblings {len(siblings)} items (max 5)"
                )

            subsystems = node.impacted_subsystems
            if not (1 <= len(subsystems) <= 8):
                violations.append(
                    f"{fault_id}: impacted_subsystems {len(subsystems)} items (need 1–8)"
                )

        assert not violations, (
            f"{len(violations)} field constraint violation(s):\n"
            + "\n".join(violations)
        )


# ===================================================================
# Audit 5 — ChemicalSignature validity guard (T-P6-9c)
# ===================================================================

# Parked dead values: option (a) decisions — GASLab enum extension needed.
# Each entry maps a dead gas_lab_state string to the GASLab follow-up
# task ID that will mint the corresponding ChemicalSignature value.
# When a follow-up is completed, re-point the matching registry rules
# to the new enum value and remove the entry from this allowlist.
_PARKED_GAS_LAB_ALLOWLIST: dict[str, str] = {}


class TestChemicalSignatureGuard:
    """Every registry ``gas_lab_state`` is a valid ChemicalSignature or parked."""

    def test_all_registry_gas_lab_states_are_valid_chemical_signatures(
        self,
    ) -> None:
        """Audit 5: registry gas_lab_state ∈ ChemicalSignature or parked.

        Any value NOT in the enum and NOT in the parked allowlist is a
        vocabulary drift — it has no matching GASLab emission and no
        follow-up plan.
        """
        import json
        from pathlib import Path

        from comlab.schemas.vocabulary import ChemicalSignature

        reg_path = (
            Path(__file__).resolve().parent.parent.parent
            / "comlab" / "config" / "global_fault_registry.json"
        )
        registry = json.loads(reg_path.read_text(encoding="utf-8"))["registry"]

        valid = {m.value for m in ChemicalSignature}

        unregistered: list[tuple[str, str]] = []
        parked_no_followup: list[tuple[str, str]] = []

        for rule in registry:
            gsl: str = rule["cross_domain_matrix"]["gas_lab_state"]
            fid: str = rule["fault_id"]

            if gsl in valid:
                continue

            if gsl in _PARKED_GAS_LAB_ALLOWLIST:
                fu_id = _PARKED_GAS_LAB_ALLOWLIST[gsl]
                if not fu_id:
                    parked_no_followup.append((fid, gsl))
                continue

            unregistered.append((fid, gsl))

        failures: list[str] = []
        if unregistered:
            failures.append(
                "Unregistered gas_lab_state values (not in ChemicalSignature"
                " and not parked): "
                + "; ".join(f"{fid}={val!r}" for fid, val in unregistered)
            )
        if parked_no_followup:
            failures.append(
                "Parked gas_lab_state values with missing/empty follow-up ID: "
                + "; ".join(f"{fid}={val!r}" for fid, val in parked_no_followup)
            )

        assert not failures, "\n".join(failures)
