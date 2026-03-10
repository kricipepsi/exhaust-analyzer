# MOT Database & Query System — Implementation Summary

## Overview

Created a comprehensive Python/SQLite database containing the UK MOT Inspection Manual emissions standards (19th edition, 2017). This enables the 5-gas analyzer app to provide accurate MOT test determination based on vehicle make, model, year, fuel type, and equipment.

## Files Created

### Core Database

- **`knowledge/mot_database.py`** (25.8 KB)
  - `MOTDatabase` class with full schema and seed data
  - Tables: vehicle_makes, vehicle_types, emission_standards, specific_model_limits, diesel_smoke_standards, test_flowcharts, special_cases, mil_requirements, visual_smoke_criteria
  - Pre-populated with general standards (Table 1, 2, 3) and special case rules
  - Ready to receive full Annex data (see "Next Steps")

- **`knowledge/mot_emissions.db`** (SQLite, 143 KB)
  - Actual database file created by running `mot_database.py`
  - Contains: vehicle types, emission standards by date, diesel smoke limits, MIL rules, special cases

### Query API

- **`knowledge/mot_query_api.py`** (18.7 KB)
  - `MOTQueryAPI` class for programmatic lookups
  - `query_vehicle_info()` single-function API for Flask integration
  - Implements flowchart logic from MOT manual sections 8.2.1 and flowcharts 1-3
  - Returns: test_type, procedure, limits, special notes

- **`knowledge/mot_query_api.py` demo output:*
```
Query 1: 2010 petrol car with catalyst
Test type: extended_catalyst
Description: Petrol vehicle with catalyst (or listed in Annex): Extended catalyst test required.

Query 2: 2015 diesel car
Test type: diesel_smoke
Smoke limit: 0.7 m-1
Procedure: 1. Warm engine to operating temperature...
```

## Data Sources

### From Web Page (gov.uk)
- MOT Inspection Manual section 8.2.1 Spark ignition engine emissions
- Flowcharts 1-3 decision trees
- Defect categories and references
- MIL (engine management light) requirements
- Test procedures: non-catalyst, BET, extended catalyst
- Diesel opacity test procedures
- Special rules: kit cars, personal imports, engine swaps, dual exhaust

### From PDF Text (`19th edition - in-service-exhaust-emission-standards-for-road-vehicles-19th-edition.txt`)
- **Table 1**: Petrol car limits by first use date
- **Table 2**: Other petrol vehicles (large passenger, LGV)
- **Table 3**: Diesel smoke limits by date and turbocharger
- Annex start: Specific model entries (ABARTH, AC, ALFA ROMEO...) with detailed per-engine limits
  - Columns: Manufacturer, Model, Engine code, CO, HC, lambda, RPM ranges, oil temp

## Database Schema Highlights

```sql
-- Emission standards (general fallback)
SELECT * FROM emission_standards
WHERE vehicle_type_id = ? AND date_from <= ? AND test_type = 'basic'

-- Specific model limits (Annex) override general standards
SELECT * FROM specific_model_limits
WHERE make_id = ? AND model_name = ? AND date_from <= ? ORDER BY date_from DESC

-- Diesel smoke by date
SELECT opacity_limit_m1 FROM diesel_smoke_standards
WHERE date_from <= ? AND turbocharged = ? ORDER BY date_from DESC
```

## How to Integrate into Flask App (5-Gas Analyzer)

### 1. Add route to Flask backend

```python
from flask import Blueprint, request, jsonify
from knowledge.mot_query_api import query_vehicle_info, MOTQueryAPI

mot_bp = Blueprint('mot', __name__)

@mot_bp.route('/mot/query', methods=['POST'])
def mot_query():
    data = request.json
    result = query_vehicle_info(
        make=data['make'],
        model=data['model'],
        first_use_date=data['first_use_date'],  # 'YYYY-MM-DD'
        fuel_type=data['fuel_type'],           # 'petrol', 'diesel', 'gas'
        engine_code=data.get('engine_code'),
        has_catalyst=data.get('has_catalyst', False),
        dgw_kg=data.get('dgw_kg'),
        seat_count=data.get('seat_count')
    )
    return jsonify(result)
```

### 2. Frontend Query Window

Add a new tab/section to the Tauri frontend (or web UI):

**Inputs:**
- Vehicle make (text, with autocomplete from vehicle_makes table)
- Model (text)
- Engine code (optional)
- First use date (date picker)
- Fuel type (dropdown: petrol/diesel/gas/hybrid/electric)
- Has catalytic converter? (checkbox, if unknown leave unchecked)
- DGW (optional, number)
- Seats (optional, number)

**Outputs:**
- **Required MOT Test**: e.g., "Extended catalyst test", "Basic Emissions Test (BET)", "Diesel smoke meter test"
- **What it involves**: Paragraph description
- **Step-by-step procedure**: Multi-line
- **Emission limits**: Table (CO%, HCppm, λ range, RPM range, oil temp)
- **Special notes**: Warnings about kit cars, imports, etc.
- **MOT Manual reference**: Section 8.2.1, Flowchart 2 etc.

### 3. Populate Specific Model Annex Data (Optional but Recommended)

Currently the `specific_model_limits` table is empty. To fill it:

Parse the full `19th edition - in-service-exhaust-emission-standards-for-road-vehicles-19th-edition.txt` file and extract all the tabulated model entries (ABARTH, AC, ALFA ROMEO, etc.). The format is:

```
[Manufacturer]
[Model line]
[Engine specs]
[Limit row: CO% HCppm MinRPM MaxRPM MinLambda MaxLambda MinRPM Idle MinRPM MaxRPM MinOilTemp]
```

A parser would extract: make, model_name, engine_code, engine_cc, fuel_type, dates, and the 10 limit fields.

**Future task**: Write `parse_annex.py` to import all specific model limits.

## Testing

```bash
cd knowledge
python mot_database.py   # Creates mot_emissions.db
python mot_query_api.py  # Runs demo queries
```

## Next Steps

1. **Parse Annex**: Write script to extract all make/model/engine rows from the PDF text and populate `specific_model_limits`
2. **Expose API**: Add `/mot/query` endpoint to Flask app
3. **Frontend**: Build query UI panel with React/Vue/HTML
4. **Autocomplete**: Query `vehicle_makes` table to suggest makes
5. **Cache**: Consider caching query results for performance
6. **Error handling**: Gracefully handle unknown makes/models by falling back to general standards
7. **Unit tests**: Add test suite for edge cases

## Query Examples

```python
# Petrol car 2012, likely has catalyst
query_vehicle_info(
    make="Ford",
    model="Focus",
    first_use_date="2012-03-10",
    fuel_type="petrol",
    has_catalyst=True
)
# Returns: extended_catalyst with BET fallback limits

# Diesel car 2016
query_vehicle_info(
    make="Audi",
    model="A4",
    first_use_date="2016-06-01",
    fuel_type="diesel",
    dgw_kg=1800
)
# Returns: diesel_smoke with limit 0.7 m-1
```

## Files Location

All files in: `C:\Users\asus\.openclaw\workspace\exhaust-analyzer\knowledge\`

---
**Status**: Database schema complete, seeded with general standards. Query API functional. Ready for Flask integration and Annex data import.
