"""T-V3-4B Tunable reweight validation tests."""

from __future__ import annotations

import csv
import sys
from pathlib import Path
WORKSPACE_ROOT = Path("/agent_workspace")
for relative in (
    "apps/wired",
    "labs/comlab",
    "labs/dnalab",
    "labs/dtclab",
    "labs/gaslab",
    "labs/obdlab",
    "labs/symptomlab",
    "labs/vinlab",
):
    path = str(WORKSPACE_ROOT / relative)
    if path not in sys.path:
        sys.path.insert(0, path)

from v7.load_corpus import row_to_raw_inputs  # type: ignore # noqa: E402
from wired.composition import diagnose  # type: ignore # noqa: E402
from fl_tasks.score_v3_yardstick import load_rule_family_map, sibling_family  # type: ignore # noqa: E402


def test_tunable_reweight_recovered_cases() -> None:
    """Assert that each of the 8 recovered cases now has its expected family in top-3."""
    csv_path = WORKSPACE_ROOT / "apps/wired/v7/data/cases_petrol_v7.csv"
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    rule_map = load_rule_family_map()

    # The 8 recovered cases
    recovered_case_ids = {
        "CSV-095": "exhaust_leak",
        "era1_016": "exhaust_leak",
        "era3_019": "exhaust_leak",
        "EXP-N027": "rich_mixture",
        "EXP-N010": "rich_mixture",
        "era3_007": "lean_condition",
        "YAML-PDF_4G_01": "catalyst_failure",
        "EXP-N014": "misfire",
    }

    found_cases = 0
    for row in rows:
        case_id = row["case_id"]
        if case_id in recovered_case_ids:
            found_cases += 1
            raw_inputs = row_to_raw_inputs(row)
            verdict = diagnose(raw_inputs)
            verdict_dict = verdict.model_dump()
            dv = verdict_dict.get("diagnostic_verdict", {})
            winner_family = dv.get("fault_family", "")
            
            # Build top-3 families
            siblings = dv.get("differential_siblings", [])
            sibling_families = []
            for sib in siblings[:2]:  # top-2 siblings
                fam = sibling_family(sib, rule_map)
                if fam != "unspecified":
                    sibling_families.append(fam)
            
            top3_families = {winner_family} | set(sibling_families)
            expected_family = recovered_case_ids[case_id]
            
            assert expected_family in top3_families, (
                f"Case {case_id} failed: expected {expected_family} to be in top-3 {top3_families}"
            )

    assert found_cases == len(recovered_case_ids), f"Expected to find {len(recovered_case_ids)} cases, found {found_cases}"


def test_tunable_reweight_neighbour_cases() -> None:
    """Assert that a named neighbour from each touched rule's passes_cases still passes."""
    csv_path = WORKSPACE_ROOT / "apps/wired/v7/data/cases_petrol_v7.csv"
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    rule_map = load_rule_family_map()

    # Named neighbours that are expected to pass the top-3 family metric
    neighbours = {
        "CSV-018": "rich_mixture",       # neighbour for RM-001 rich_mixture
        "CSV-101": "misfire",            # neighbour for MF-001 misfire
        "EXP-N008": "catalyst_failure",  # neighbour for CF-002 catalyst_failure
        "case_010": "catalyst_failure",  # neighbour for CF-001 catalyst_failure
        "CSV-095": "exhaust_leak",       # neighbour/pass case for EL-001 exhaust_leak
    }

    found_cases = 0
    for row in rows:
        case_id = row["case_id"]
        if case_id in neighbours:
            found_cases += 1
            raw_inputs = row_to_raw_inputs(row)
            verdict = diagnose(raw_inputs)
            verdict_dict = verdict.model_dump()
            dv = verdict_dict.get("diagnostic_verdict", {})
            winner_family = dv.get("fault_family", "")
            
            # Build top-3 families
            siblings = dv.get("differential_siblings", [])
            sibling_families = []
            for sib in siblings[:2]:  # top-2 siblings
                fam = sibling_family(sib, rule_map)
                if fam != "unspecified":
                    sibling_families.append(fam)
            
            top3_families = {winner_family} | set(sibling_families)
            expected_family = neighbours[case_id]
            
            assert expected_family in top3_families, (
                f"Neighbour case {case_id} failed: expected {expected_family} to be in top-3 {top3_families}"
            )

    assert found_cases == len(neighbours), f"Expected to find {len(neighbours)} neighbours, found {found_cases}"
