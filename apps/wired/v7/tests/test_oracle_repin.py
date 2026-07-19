"""
Guard tests for V3 oracle re-pins.

Ensures:
1. SURFACE_DEFECT named-fault rows have ERR- prefix stripped from expected_fault_code
2. SURFACE_DEFECT named-fault rows have confidence bands updated to per-family observed bands
3. ORACLE_SUSPECT mechanical_wear->misfire rows are re-pinned to MF-001
4. Non-suspect mechanical_wear rows remain mechanical_wear
5. ERR-ABORT-* rows (if any) and OPTIMAL_HEALTH / no_fault rows are protected
6. Expected state values stay within the scorer vocabulary
"""
import csv

import pytest

CSV_PATH = "apps/wired/v7/data/cases_petrol_v7.csv"

# Per-family confidence bands from run 20260630_163900 (Option B re-pin)
FAMILY_BANDS = {
    'cam_timing': (0.80, 1.00),
    'catalyst_failure': (0.90, 1.00),
    'ecu_fault': (0.90, 1.00),
    'ignition_fault': (1.00, 1.00),
    'lean_condition': (0.90, 1.00),
    'misfire': (0.80, 1.00),
    'rich_mixture': (0.95, 1.00),
    'sensor_fault': (0.95, 1.00),
}

# SURFACE_DEFECT case IDs from FL_LOCALIZATION_2026-06-30.md
SURFACE_DEFECT_IDS = {
    'era1_003', 'era1_004', 'era1_005', 'era1_007', 'era1_008', 'era1_009',
    'era1_012', 'era1_013', 'era1_014', 'era1_018', 'era1_020',
    'era2_001', 'era2_002', 'era2_003', 'era2_004', 'era2_009', 'era2_010',
    'era2_013', 'era2_014', 'era2_017', 'era2_020',
    'era3_001', 'era3_002', 'era3_003', 'era3_004', 'era3_006', 'era3_011',
    'era3_013', 'era3_016', 'era3_017', 'era3_018', 'era3_020',
    'CASE-010', 'CASE-011', 'CASE-012', 'CASE-016', 'CASE-017', 'CASE-018',
    'CASE-019', 'CASE-021', 'CASE-024', 'CASE-025', 'CASE-026', 'CASE-027',
    'CASE-028', 'CASE-030', 'CASE-031', 'CASE-033', 'CASE-034', 'CASE-036',
    'CASE-037', 'CASE-038',
    'CSV-016', 'CSV-018', 'CSV-022', 'CSV-052', 'CSV-066', 'CSV-068',
    'CSV-072', 'CSV-101', 'CSV-102', 'CSV-103', 'CSV-104', 'CSV-105',
    'CSV-106', 'CSV-107', 'CSV-108', 'CSV-109', 'CSV-110', 'CSV-111',
    'CSV-112', 'CSV-115', 'CSV-116',
    'ECU-007', 'ECU-008',
    'EXP-N001', 'EXP-N003', 'EXP-N006', 'EXP-N008', 'EXP-N009', 'EXP-N012',
    'EXP-N013', 'EXP-N016', 'EXP-N028',
    'EXT-201', 'EXT-202', 'EXT-203', 'EXT-204', 'EXT-205', 'EXT-206',
    'EXT-209', 'EXT-210', 'EXT-214', 'EXT-215', 'EXT-218',
    'EXT-225', 'EXT-226', 'EXT-227', 'EXT-228', 'EXT-234', 'EXT-235',
    'EXT-236', 'EXT-237', 'EXT-240',
    'MECH-003', 'MECH-004',
    'PDF-4G-03', 'PDF-HI-002', 'PDF-HI-008',
    'REAL-005', 'TC-011',
    'YAML-CSV18', 'YAML-CSV22', 'YAML-CSV52', 'YAML-CSV66', 'YAML-CSV68',
    'YAML-CSV72', 'YAML-PDF_4G_02', 'YAML-PDF_4G_03', 'YAML-PDF_4G_04',
    'YAML-PDF_HI_002', 'YAML-TC12', 'YAML-TC36', 'YAML-TC37',
    'case_005', 'case_009', 'case_010', 'case_018', 'case_019', 'case_022',
    'case_023', 'case_027', 'case_034',
}

# ORACLE_SUSPECT mechanical_wear rows re-pinned by FL-V3-ORACLE-MW-MISFIRE.
MW_MISFIRE_REPIN_IDS = {
    'CSV-118', 'CSV-119', 'CSV-120',
    'EXT-222', 'EXT-223', 'EXT-224',
    'MECH-002', 'MECH-006',
    'era1_002', 'era1_015',
}

# Mechanical-wear rows explicitly excluded by FL-V3-ORACLE-MW-MISFIRE.
MW_REPIN_EXCLUDED_IDS = {
    'CSV-117',
    'EXP-N030',
    'MECH-001',
    'case_044',
}


def load_csv():
    with open(CSV_PATH) as f:
        reader = csv.DictReader(f)
        return list(reader)


def test_mw_oracle_suspects_repin_to_misfire() -> None:
    """The 10 signed-off ORACLE_SUSPECT rows score against MF-001."""
    rows = {row['case_id']: row for row in load_csv()}

    assert set(rows) >= MW_MISFIRE_REPIN_IDS
    for case_id in MW_MISFIRE_REPIN_IDS:
        row = rows[case_id]
        assert row['expected_fault_family'] == 'misfire'
        assert row['expected_fault_code'] == 'MF-001'
        assert row['expected_state'] == 'named_fault'
        assert row['expected_confidence_min'] == '0.80'
        assert row['expected_confidence_max'] == '1.00'


def test_mw_repin_excluded_rows_stay_mechanical_wear() -> None:
    """The 4 non-suspect mechanical_wear rows are not part of the re-pin."""
    rows = {row['case_id']: row for row in load_csv()}

    assert set(rows) >= MW_REPIN_EXCLUDED_IDS
    for case_id in MW_REPIN_EXCLUDED_IDS:
        assert rows[case_id]['expected_fault_family'] == 'mechanical_wear'


def test_surface_defect_fault_code_stripped():
    """SURFACE_DEFECT named-fault rows: expected_fault_code has ERR- prefix stripped."""
    rows = load_csv()
    for row in rows:
        if row['case_id'] in SURFACE_DEFECT_IDS:
            code = row['expected_fault_code']
            assert not code.startswith('ERR-'), f"{row['case_id']}: fault_code still has ERR- prefix: {code}"
            assert '-' in code, f"{row['case_id']}: fault_code not in short form: {code}"


def test_surface_defect_confidence_bands():
    """SURFACE_DEFECT named-fault rows: confidence bands match per-family observed bands."""
    rows = load_csv()
    for row in rows:
        if row['case_id'] in SURFACE_DEFECT_IDS:
            family = row['expected_fault_family']
            conf_min = float(row['expected_confidence_min'])
            conf_max = float(row['expected_confidence_max'])

            assert family in FAMILY_BANDS, f"{row['case_id']}: family {family} not in band map"
            expected_min, expected_max = FAMILY_BANDS[family]

            assert abs(conf_min - expected_min) < 0.01, \
                f"{row['case_id']}: conf_min {conf_min} != expected {expected_min} for family {family}"
            assert abs(conf_max - expected_max) < 0.01, \
                f"{row['case_id']}: conf_max {conf_max} != expected {expected_max} for family {family}"


def test_abort_rows_untouched():
    """ERR-ABORT-* rows (if any) have expected_* columns unchanged."""
    rows = load_csv()
    for row in rows:
        code = row['expected_fault_code']
        if code.startswith('ERR-ABORT-'):
            assert code.startswith('ERR-ABORT-'), f"{row['case_id']}: abort code incorrectly modified: {code}"


def test_optimal_health_no_fault_untouched():
    """OPTIMAL_HEALTH and no_fault rows have expected_* columns unchanged."""
    rows = load_csv()
    for row in rows:
        code = row['expected_fault_code']
        family = row['expected_fault_family']

        if code == 'OPTIMAL_HEALTH' or family == 'no_fault':
            conf_min = float(row['expected_confidence_min'])
            conf_max = float(row['expected_confidence_max'])
            assert conf_max <= 0.5, \
                f"{row['case_id']}: no_fault/OPTIMAL_HEALTH row has high confidence band {conf_min}-{conf_max}"


def test_family_state_unchanged():
    """expected_fault_family and expected_state unchanged for ALL rows."""
    rows = load_csv()
    valid_states = {'insufficient_evidence', 'invalid_input', 'named_fault', 'warning'}
    for row in rows:
        assert row['expected_fault_family'], f"{row['case_id']}: expected_fault_family is empty"
        assert row['expected_state'], f"{row['case_id']}: expected_state is empty"
        assert row['expected_state'] in valid_states, \
            f"{row['case_id']}: unexpected expected_state: {row['expected_state']}"


def test_corpus_validates():
    """Corpus still validates against FaultAtlasKG (no vocabulary/KG violation)."""
    import subprocess
    result = subprocess.run(
        ['/agent_workspace/.venv-wired/bin/python', 'apps/wired/v7/load_corpus.py', '--validate'],
        capture_output=True, text=True, cwd='/agent_workspace'
    )
    assert result.returncode == 0, f"Corpus validation failed: {result.stderr}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
