"""
MOT Query API for 5-Gas Analyzer
Provides lookup interface to determine MOT test requirements based on vehicle details.
"""

from datetime import datetime, date
from typing import Optional, Dict, Any, List
import sqlite3
from pathlib import Path
import os

class MOTQueryAPI:
    """
    Query interface for MOT emissions standards database.
    Allows the 5-gas analyzer app to determine test procedures based on:
    - Vehicle make
    - Model
    - Engine code (optional)
    - First use date (registration date)
    - Fuel type
    - DGW (design gross weight) and seating (for vehicle classification)
    """

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            # Default to mot_emissions.db in the same directory as this module
            script_dir = Path(__file__).parent.resolve()
            self.db_path = script_dir / "mot_emissions.db"
        else:
            self.db_path = Path(db_path)
        self.conn: Optional[sqlite3.Connection] = None

    def connect(self):
        """Open database connection."""
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found: {self.db_path}")
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        if self.conn:
            self.conn.close()

    def determine_test_type(self,
                           first_use_date: str,
                           fuel_type: str,
                           is_passenger_car: bool,
                           has_catalyst: bool = False,
                           is_in_annex: bool = False) -> Dict[str, Any]:
        """
        Core flowchart logic: determine which MOT emissions test applies.
        This replicates the decision logic from MOT manual section 8.2.1 and flowcharts 1-3.

        Args:
            first_use_date: 'YYYY-MM-DD' format
            fuel_type: 'petrol', 'diesel', 'gas', 'hybrid', 'electric'
            is_passenger_car: True if passenger car (≤5 seats + driver, ≤2500kg DGW)
            has_catalyst: True if vehicle equipped with catalytic converter (advanced emission control)
            is_in_annex: True if specific make/model/engine combination listed in the Annex

        Returns:
            Dict with test_type, requirements, limits, and description
        """
        cur = self.conn.cursor()
        fud = datetime.strptime(first_use_date, '%Y-%m-%d').date()

        # Electric vehicles: no exhaust emissions test
        if fuel_type == 'electric':
            return {
                'test_type': 'none',
                'description': 'Electric vehicles are exempt from exhaust emissions testing.'
            }

        # Visual checks for very old vehicles
        if fuel_type == 'petrol' and fud < date(1975, 8, 1):
            return {
                'test_type': 'visual_petrol',
                'description': 'Petrol vehicle first used before 1 Aug 1975: visual smoke check only. Assess for dense blue/black smoke at idle and during acceleration.',
                'pass_criteria': 'No dense blue or clearly visible black smoke for 5+ seconds at idle, and not obscuring vision during acceleration.'
            }

        if fuel_type == 'diesel' and fud < date(1980, 1, 1):
            return {
                'test_type': 'visual_diesel',
                'description': 'Diesel vehicle first used before 1 Jan 1980: visual smoke check. Assess at idle and during free acceleration.',
                'pass_criteria': 'No dense smoke for 5+ seconds at idle; smoke during acceleration must not obscure other road users.'
            }

        # For modern vehicles: metered test

        # Determine vehicle type code for standards lookup
        if fuel_type in ('petrol', 'gas'):
            vt_code = 'petrol_car' if is_passenger_car else 'petrol_lgv'
        elif fuel_type == 'diesel':
            vt_code = 'diesel_car' if is_passenger_car else 'diesel_lgv'
        else:
            vt_code = 'petrol_car'  # fallback

        # --- PETROL LOGIC (from flowcharts 1-3) ---

        if fuel_type == 'petrol':
            # Pre-1992: non-catalyst test (Table 1/2)
            if fud < date(1992, 8, 1):
                return self._get_standard_limit(cur, vt_code, first_use_date, 'non_catalyst',
                    "Non-catalyst test (pre-1992 petrol). Measure CO and HC at idle. Required for vehicles not equipped with catalytic converter or first used before catalyst standards.")

            # 1992-1995 transition period
            if fud < date(1995, 9, 1):
                if is_in_annex:
                    # Listed in Annex → extended catalyst test with specific limits
                    return {
                        'test_type': 'extended_catalyst',
                        'uses_annex': True,
                        'description': 'Vehicle first used 1992-1995 and listed in Annex: Extended catalyst test required.',
                        'procedure': 'Perform fast-idle test (CO, HC, λ) and idle CO test. Use limits from specific model entry in Annex.'
                    }
                else:
                    # Not in Annex → non-catalyst (these transitional vehicles not required to meet catalyst standards)
                    return self._get_standard_limit(cur, vt_code, first_use_date, 'non_catalyst',
                        "Vehicle first used 1992-1995 not listed in Annex: Non-catalyst test applies.")

            # 1995 onwards
            if is_in_annex or has_catalyst:
                # Extended catalyst test with specific model limits from Annex
                return {
                    'test_type': 'extended_catalyst',
                    'uses_annex': is_in_annex,
                    'description': 'Petrol vehicle with catalyst (or listed in Annex): Extended catalyst test required.',
                    'procedure': '1. Check engine oil temperature >= specified minimum (usually 80°C). 2. Perform HC hang-up check (<20ppm). 3. Fast-idle test: hold at specified RPM (from Annex or 2500-3000) for 30s, measure CO, HC, lambda. 4. Normal idle test: measure CO. All limits must be met.',
                    'fast_idle_limits': {
                        'co': 'See Annex or <=0.2% if using default',
                        'hc': 'See Annex or <=200ppm if using default',
                        'lambda_min': 0.97,
                        'lambda_max': 1.03,
                        'duration_seconds': 30
                    },
                    'idle_limits': {
                        'co': '<=0.3%'
                    }
                }
            else:
                # Basic Emissions Test (BET) for non-catalyst vehicles post-1995
                return self._get_standard_limit(cur, vt_code, first_use_date, 'basic',
                    "Petrol vehicle without catalyst first used after 1995: Basic Emissions Test (BET).")

        # --- DIESEL LOGIC ---

        elif fuel_type == 'diesel':
            # All diesel cars/LGVs first used on/after 1 Aug 1979 need metered smoke test
            if fud < date(1980, 1, 1):
                return {
                    'test_type': 'visual_diesel',
                    'description': 'Pre-1980 diesel: visual smoke assessment only.'
                }

            # Determine turbocharged status (would need VIN or visual inspection)
            # For query interface, we may need to ask user or guess from model
            # Return both possibilities or ask for clarification

            return {
                'test_type': 'diesel_smoke',
                'description': 'Diesel smoke meter test required.',
                'procedure': '1. Warm engine to operating temperature (oil >=80°C or normal operating temp). 2. Purge inlet/exhaust: rev to ~2500rpm for 30s. 3. Perform free acceleration tests: accelerate quickly to maximum RPM, record smoke level. 4. Fast pass: if first reading <=1.5m-1, vehicle passes. 5. Otherwise average up to 6 accelerations. 6. Pass if any consecutive 3 readings <= limit.',
                'note': 'Turbocharged status affects limit. Check vehicle for turbo or use VIN to determine. Default assumptions may fail.',
                'limits_by_date': 'See diesel_smoke_standards table for exact limits by year.'
            }

        # Gas (LPG/CNG) generally follows petrol rules
        elif fuel_type in ('gas', 'lpg', 'cng'):
            # Similar to petrol but with HC PEF correction for LPG
            if fud < date(1992, 8, 1):
                return self._get_standard_limit(cur, vt_code, first_use_date, 'non_catalyst',
                    "Gas vehicle: Non-catalyst test with HC propane/hexane correction.")
            else:
                if is_in_annex or has_catalyst:
                    return {
                        'test_type': 'extended_catalyst',
                        'uses_annex': is_in_annex,
                        'description': 'Gas vehicle with catalyst: Extended catalyst test.',
                        'hc_note': 'HC reading on LPG is propane; must divide by Propane/Hexane Equivalency Factor (PEF) from analyser to get hexane equivalent.'
                    }
                else:
                    return self._get_standard_limit(cur, vt_code, first_use_date, 'basic',
                        "Gas vehicle without catalyst: BET.")

        return {'error': 'Could not determine test type'}

    def _get_standard_limit(self, cur: sqlite3.Cursor, vehicle_type_code: str,
                           first_use_date: str, test_type: str, description: str) -> Dict[str, Any]:
        """Fetch standard emission limits from the emission_standards table."""
        cur.execute("""
            SELECT * FROM emission_standards
            WHERE vehicle_type_id = (SELECT id FROM vehicle_types WHERE code = ?)
              AND date_from <= ?
              AND (date_to IS NULL OR ? < date_to)
              AND test_type = ?
            ORDER BY date_from DESC LIMIT 1
        """, (vehicle_type_code, first_use_date, first_use_date, test_type))
        row = cur.fetchone()
        if row:
            data = dict(row)
            data['description'] = description
            return data
        return {'error': f'No standard found for {vehicle_type_code}, {test_type}'}

    def lookup_specific_model(self, make: str, model: str, engine_code: Optional[str],
                             first_use_date: str) -> Optional[Dict[str, Any]]:
        """
        Check if vehicle make/model/engine combination is in the Annex
        with specific limits for extended catalyst test.
        """
        cur = self.conn.cursor()
        cur.execute("""
            SELECT sml.*, vm.name as make_name
            FROM specific_model_limits sml
            JOIN vehicle_makes vm ON sml.make_id = vm.id
            WHERE LOWER(vm.name) = LOWER(?) AND LOWER(sml.model_name) = LOWER(?)
              AND sml.date_from <= ? AND (sml.date_to IS NULL OR ? <= sml.date_to)
            ORDER BY sml.date_from DESC
            LIMIT 1
        """, (make, model, first_use_date, first_use_date))
        row = cur.fetchone()
        if row:
            result = dict(row)
            # Also fetch MIL requirement
            cur.execute("""
                SELECT * FROM mil_requirements
                WHERE fuel_type = ? AND first_use_date <= ?
                ORDER BY first_use_date DESC LIMIT 1
            """, (row['fuel_type'], first_use_date))
            mil_row = cur.fetchone()
            if mil_row:
                result['mil_required'] = mil_row['must_check_mil']
            return result
        return None

    def get_diesel_smoke_limit(self, first_use_date: str, is_turbocharged: bool) -> Dict[str, Any]:
        """Get diesel smoke opacity limit based on date and turbo status."""
        cur = self.conn.cursor()
        cur.execute("""
            SELECT * FROM diesel_smoke_standards
            WHERE date_from <= ? AND (date_to IS NULL OR ? < date_to)
              AND vehicle_weight_category = 'passenger_car'
            ORDER BY date_from DESC LIMIT 1
        """, (first_use_date, first_use_date))
        row = cur.fetchone()
        if row:
            return dict(row)
        return {'error': 'No diesel smoke limit found'}

    def get_special_case(self, case_name: str) -> Dict[str, Any]:
        """Retrieve special case rule by name."""
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM special_cases WHERE case_name = ?", (case_name,))
        row = cur.fetchone()
        return dict(row) if row else {'error': 'Special case not found'}

    def classify_vehicle_from_v5c(self, v5c_data: Dict[str, Any]) -> str:
        """
        Determine vehicle classification from V5C document details.
        This is a simplified implementation; full logic can be more complex.
        """
        # V5C fields: body type, fuel, maximum authorised mass (MAM), number of seats
        body_type = v5c_data.get('body_type', '').lower()
        fuel = v5c_data.get('fuel', '').lower()
        mam = v5c_data.get('max_gross_weight', 0)  # in kg
        seats = v5c_data.get('seats', 0)  # total including driver

        # Passenger car: ≤5 passenger seats + driver (≤6 total seats), DGW ≤2500kg, not a goods vehicle
        # Goods vehicle: constructed/adapted for carrying goods
        goods_keywords = ['pickup', 'van', 'goods', 'truck', 'flatbed', 'tipper']

        if any(kw in body_type for kw in goods_keywords):
            return 'goods_vehicle'

        if seats > 8:
            return 'large_passenger_vehicle'

        if mam <= 2500 and seats <= 6:
            return 'passenger_car'

        if mam <= 3500:
            return 'light_commercial_vehicle'

        return 'unclassified'

    def build_query_ui_model(self) -> Dict[str, Any]:
        """
        Return a schema for the frontend query window.
        Defines what inputs the user should provide and what outputs to display.
        """
        return {
            'inputs': {
                'make': {'type': 'text', 'label': 'Vehicle Make', 'required': True},
                'model': {'type': 'text', 'label': 'Vehicle Model', 'required': True},
                'engine_code': {'type': 'text', 'label': 'Engine Code (optional)', 'required': False},
                'first_use_date': {'type': 'date', 'label': 'First Use Date (registration)', 'required': True},
                'fuel_type': {'type': 'select', 'label': 'Fuel Type', 'options': ['petrol', 'diesel', 'gas', 'hybrid', 'electric'], 'required': True},
                'has_catalyst': {'type': 'boolean', 'label': 'Has catalytic converter?', 'required': False},
                'diesel_turbo': {'type': 'boolean', 'label': 'Turbocharged (diesel only)', 'required': False},
                'dgw_kg': {'type': 'number', 'label': 'Design Gross Weight (kg)', 'required': False},
                'seat_count': {'type': 'number', 'label': 'Total seats (incl. driver)', 'required': False},
            },
            'outputs': {
                'test_type': {'label': 'Required MOT Test', 'type': 'text'},
                'description': {'label': 'What this test involves', 'type': 'text'},
                'procedure': {'label': 'Step-by-step procedure', 'type': 'multiline'},
                'limits': {'label': 'Emission limits', 'type': 'table'},
                'special_notes': {'label': 'Important notes', 'type': 'text'},
                'references': {'label': 'MOT Manual references', 'type': 'text'}
            }
        }


def query_vehicle_info(make: str, model: str, first_use_date: str, fuel_type: str,
                      engine_code: Optional[str] = None, has_catalyst: bool = False,
                      dgw_kg: Optional[int] = None, seat_count: Optional[int] = None) -> Dict[str, Any]:
    """
    Single-function query for the Flask app backend.
    Returns complete MOT test determination result.
    """
    api = MOTQueryAPI()
    try:
        api.connect()

        # Determine vehicle classification
        # For now, simple: assume passenger car if DGW <=2500 and seats <=6, else LGV/goods
        is_passenger_car = True
        if dgw_kg is not None and dgw_kg > 2500:
            is_passenger_car = False
        if seat_count is not None and seat_count > 6:
            is_passenger_car = False

        # First, check if specific model is in Annex
        annex_entry = api.lookup_specific_model(make, model, engine_code, first_use_date)

        result = api.determine_test_type(
            first_use_date=first_use_date,
            fuel_type=fuel_type,
            is_passenger_car=is_passenger_car,
            has_catalyst=has_catalyst,
            is_in_annex=(annex_entry is not None)
        )

        # Enrich with specific model data if found
        if annex_entry:
            result['annex_entry'] = annex_entry
            result['test_type'] = 'extended_catalyst_with_specific_limits'
            result['limits'] = {
                'CO (fast idle)': f"{annex_entry['co_limit_percent']}% vol",
                'HC (fast idle)': f"{annex_entry['hc_limit_ppm']} ppm",
                'Lambda': f"{annex_entry['lambda_min']} - {annex_entry['lambda_max']}",
                'Fast idle RPM': f"{annex_entry['fast_idle_rpm_min']}-{annex_entry['fast_idle_rpm_max']}",
                'Normal idle RPM': f"{annex_entry['normal_idle_rpm_min']}-{annex_entry['normal_idle_rpm_max']}",
                'Min oil temp': f"{annex_entry['oil_temp_min_c']}°C"
            }

        # For diesel, also get smoke limit
        if fuel_type == 'diesel' and result.get('test_type') == 'diesel_smoke':
            smoke_limit = api.get_diesel_smoke_limit(first_use_date, False)  # TODO: get turbo from input
            if 'error' not in smoke_limit:
                result['smoke_limit'] = f"{smoke_limit['opacity_limit_m1']} m-1"
                result['smoke_limit_notes'] = smoke_limit['notes']

        return result

    finally:
        api.close()


def get_reference_values(make: str, model: str, first_use_date: str, fuel_type: str,
                        engine_code: Optional[str] = None, has_catalyst: bool = False,
                        dgw_kg: Optional[int] = None, seat_count: Optional[int] = None) -> Dict[str, Any]:
    """
    Get reference gas concentrations for a healthy vehicle of this type.
    Returns a dict with keys matching the analyzer form fields.
    Values are derived from MOT emission standards where available.
    """
    # Get vehicle info from MOT database
    info = query_vehicle_info(make, model, first_use_date, fuel_type,
                             engine_code, has_catalyst, dgw_kg, seat_count)

    ref: Dict[str, Any] = {}
    test_type = info.get('test_type', 'unknown')

    # Default descriptions
    description = info.get('description', '')

    # Helper to extract numeric from string like "<=0.2%"
    def extract_num(val, default=None):
        if val is None:
            return default
        if isinstance(val, (int, float)):
            return float(val)
        if isinstance(val, str):
            import re
            m = re.search(r'[\d\.]+', val)
            if m:
                return float(m.group())
        return default

    # Initialize all fields to None
    ref['lambda_idle'] = None
    ref['lambda_high'] = None
    ref['co_idle'] = None
    ref['co_high'] = None
    ref['hc_idle'] = None
    ref['hc_high'] = None
    ref['co2_high'] = None
    ref['o2_high'] = None
    ref['nox_high'] = None

    # Petrol / Gas
    if fuel_type in ('petrol', 'gas', 'lpg', 'cng', 'hybrid'):
        # Typical values for a healthy, well-tuned vehicle
        # These will be overridden by MOT limits when available
        ref.update({
            'lambda_idle': 1.0,
            'lambda_high': 1.0,
            'co_idle': 0.3,       # % typical
            'co_high': 0.2,        # %
            'hc_idle': 100,        # ppm
            'hc_high': 200,        # ppm
            'co2_high': 14.0,      # %
            'o2_high': 0.8,        # %
            'nox_high': 100        # ppm
        })

        # Replace with MOT-based limits if we have them
        if test_type in ('basic', 'extended_catalyst', 'extended_catalyst_with_specific_limits'):
            # Fast idle values
            if test_type == 'extended_catalyst_with_specific_limits' and 'limits' in info:
                # info['limits'] is a dict with display strings; parse numbers
                # Example: {'CO (fast idle)': '0.3% vol', 'HC (fast idle)': '200 ppm', ...}
                co_str = info['limits'].get('CO (fast idle)', '')
                hc_str = info['limits'].get('HC (fast idle)', '')
                lam_range = info['limits'].get('Lambda', '')
                ref['co_high'] = extract_num(co_str, ref['co_high'])
                ref['hc_high'] = extract_num(hc_str, ref['hc_high'])
                if lam_range and '-' in lam_range:
                    try:
                        parts = lam_range.split('-')
                        lam_min = float(parts[0].strip())
                        lam_max = float(parts[1].strip())
                        ref['lambda_high'] = (lam_min + lam_max) / 2
                        ref['lambda_idle'] = ref['lambda_high']
                    except:
                        pass
            elif 'co_limit_percent' in info:
                ref['co_high'] = info.get('co_limit_percent', ref['co_high'])
                ref['hc_high'] = info.get('hc_limit_ppm', ref['hc_high'])
                if info.get('lambda_min') is not None and info.get('lambda_max') is not None:
                    ref['lambda_high'] = (info['lambda_min'] + info['lambda_max']) / 2
                    ref['lambda_idle'] = ref['lambda_high']

            # Idle CO: for basic test, typically 0.3% if not separately stored
            # If we had a separate field we'd use it; for now keep default 0.3
            # Could also set to same as co_high if no specific

    elif fuel_type == 'diesel':
        # Diesel: smoke is primary; provide typical gas values
        # Determine approximate smoke limit from date
        from datetime import datetime
        fud = datetime.strptime(first_use_date, '%Y-%m-%d').date()
        year = fud.year
        if year >= 2014:
            smoke_limit = 0.7
        elif year >= 2008:
            smoke_limit = 1.5
        else:
            # Pre-2008: depends on turbo
            smoke_limit = 3.0  # default for older turbo? We'll simplify
        ref.update({
            'smoke_limit': smoke_limit,
            'co_idle': 0.1,      # diesel CO low
            'co_high': 0.1,
            'hc_idle': 20,
            'hc_high': 20,
            'co2_high': 12.0,
            'o2_high': 2.0,      # diesel runs lean
            'nox_high': 300,     # diesel NOx higher
            'lambda_idle': 1.0,  # not typically used
            'lambda_high': 1.0
        })
        test_type = 'diesel_smoke'
        description = f"Diesel smoke test required. Opacity limit: {smoke_limit} m⁻¹"

    # Electric
    elif fuel_type == 'electric':
        test_type = 'none'
        description = "Electric vehicle - no exhaust emissions test."
        ref.update({
            'co_idle': 0, 'co_high': 0,
            'hc_idle': 0, 'hc_high': 0,
            'lambda_idle': None, 'lambda_high': None,
            'co2_high': 0, 'o2_high': 0, 'nox_high': 0
        })

    return {
        **ref,
        'mot_test_type': test_type,
        'description': description
    }


if __name__ == "__main__":
    # Example queries
    print("--- MOT Query API Demo ---\n")

    # Query 1: Petrol car 2010 with catalyst
    print("Query 1: 2010 petrol car with catalyst")
    res1 = query_vehicle_info(
        make="Ford",
        model="Focus",
        first_use_date="2010-05-15",
        fuel_type="petrol",
        has_catalyst=True,
        dgw_kg=1400,
        seat_count=5
    )
    print(f"Test type: {res1.get('test_type')}")
    print(f"Description: {res1.get('description')}\n")

    # Query 2: Diesel car 2015
    print("Query 2: 2015 diesel car")
    res2 = query_vehicle_info(
        make="Volkswagen",
        model="Golf",
        first_use_date="2015-03-22",
        fuel_type="diesel",
        dgw_kg=1500,
        seat_count=5
    )
    print(f"Test type: {res2.get('test_type')}")
    print(f"Smoke limit: {res2.get('smoke_limit', 'N/A')}")
    proc = res2.get('procedure', '')[:200] if res2.get('procedure') else 'N/A'
    print(f"Procedure: {proc}...\n")

    print("API demo complete. Database ready for Flask integration.")
