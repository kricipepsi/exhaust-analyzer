# Petrol Diagnostic Test Suite

This directory contains a 100-case test validator suite for the petrol diagnostic application.

## Files
- `petrol_100_test_suite.csv` – Test cases in CSV format

## Test Case Format
Each case includes:
- **ID**: Unique test case identifier (TC001–TC100)
- **Fuel**: Petrol variant (E0, E5, E10, E85)
- **CO_Pct, CO2_Pct, HC_PPM, O2_Pct, NOx_PPM**: 5-gas analyzer readings
- **Lambda_Gas**: Calculated or measured lambda
- **OBD_STFT, OBD_LTFT, OBD_Lambda**: Live OBD-II PID data
- **OBD_DTC**: Diagnostic Trouble Code (if applicable)
- **Expected_Result**: The case name that should be matched
- **Confidence_Score**: Target confidence (0-1)
- **ECU_Health**: Target health score (0-100)

## Categories Covered (14)
- Intake Vacuum Leak: 14 cases
- Healthy Engine: 14 cases
- lean_exhaust: 12 cases
- Ignition Timing Issues: 8 cases
- Fuel Delivery Problem (Lean): 7 cases
- Engine Misfire: 7 cases
- Cold Start Enrichment: 6 cases
- System Running Rich: 6 cases
- Catalytic Converter Efficiency Failure: 6 cases
- Excessively Advanced Timing: 5 cases
- Exhaust Leak: 5 cases
- O2 Sensor Sluggish or Failed: 4 cases
- MAF Sensor Under-Reading: 4 cases
- rich_exhaust: 2 cases

## Usage
Run the test validator (ensure engine is running):
```bash
cd petrol_diagnostic
python run_100cvs_tests.py
```
The script expects the CSV at the same name. It will output pass/fail counts and save detailed results to `test_100cvs_results.json`.

## Notes
- Cases are designed for petrol engines only.
- Ranges are based on real-world diagnostic patterns (AHAA, ASE, OEM references) and the project's `diagnostic_rules.yaml`.
- Some cases include DTCs to test confidence boosting.
- Healthy engine variations cover different ethanol blends.
