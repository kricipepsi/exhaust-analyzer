# 4D Petrol Diagnostic Engine

Bretschneider-based exhaust gas analysis with theoretical lambda calculation. Diagnose engine faults from 5-gas measurements (CO, CO₂, HC, O₂, NOx).

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the diagnostic pipeline (CLI)
python main.py

# Run validation tests
python quick_test.py

# Run full calibration with expanded knowledge base
python full_calibration.py

# Launch interactive dashboard
streamlit run ui/app.py
```

## Architecture

- `core/` - Diagnostic engine modules
  - `validator.py` - Input gatekeeper ranges
  - `bretschneider.py` - Theoretical lambda calculation
  - `catalyst.py` - Catalyst efficiency bar
  - `matrix.py` - Case matching from knowledge base
  - `reporter.py` - Final verdict assembly
- `data/` - Knowledge base JSON files
  - `master_knowledge_base.json` - Original 6 cases
  - `expanded_knowledge_base.json` - 52 total cases (petrol-focused)
- `ui/` - Streamlit dashboard
  - `app.py` - Main interactive diagnostic interface

## Features

✅ **Bretschneider Formula** - Ground-truth lambda independent of O2 sensor
✅ **Validation Gatekeeper** - Rejects implausible measurements
✅ **Probe Depth Check** - Warns when CO+CO₂ sum < 12%
✅ **Catalyst Efficiency** - Calculates conversion percentage with penalty logic
✅ **52 Diagnostic Cases** - Rich pattern library (fueling, ignition, timing, sensors, mechanical)
✅ **Penalty System** - Lambda delta and catalyst efficiency affect health score
✅ **Interactive Dashboard** - Real-time diagnosis with Holy Grail graph overlay

## Test Results

- Bretschneider Gold Standard: 8/10 (+/- 0.02)
- Catalyst Efficiency: Optimal/Failed classification correct
- Matrix Matching: All 52 cases evaluatable without errors
- End-to-End Pipeline: Healthy engine → 100/100 health

## Knowledge Base Expansion

Original cases: 6 (P_001...P_100)
Added 14 high-value manual cases (2026-03-22)
Total: 52 diagnostic patterns

Cases cover:
- Intake vacuum leaks
- Ignition failures (no spark, misfire)
- Fuel delivery (lean, rich, injector leaks)
- MAF sensor under-report
- EGR stuck open/closed
- Catalyst inefficiency
- Late ignition timing
- Exhaust dilution
- Engine oil burning
- Cold start enrichment faults
- O2 sensor lazy

## Workflow (4D System)

1. **Validate** - Gatekeeper checks (ranges, probe depth)
2. **Calculate** - Bretschneider lambda (theoretical)
3. **Compare** - Measured vs calculated (detect exhaust leaks)
4. **Diagnose** - Match case from knowledge base
5. **Report** - Health score, verdict, action items

## Fuel Support

Currently optimized for petrol (E5/E10). E85, diesel, LPG constants available but not all cases support them.

---

**Built by:** krici pepsi  
**Date:** 2026-03-22
