"""
MOT Emissions Knowledge Database
Stores MOT inspection standards, emission limits, test procedures, and vehicle classification rules.
Enables make/year-based lookup for accurate MOT test determination.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Any


class MOTDatabase:
    """Manages the MOT emissions knowledge base."""

    def __init__(self, db_path: str = "mot_emissions.db"):
        self.db_path = Path(db_path)
        self.conn: Optional[sqlite3.Connection] = None

    def initialize(self):
        """Create all tables and populate with reference data."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_tables()
        self._seed_reference_data()

    def close(self):
        if self.conn:
            self.conn.close()

    def _create_tables(self):
        """Define database schema."""
        cur = self.conn.cursor()

        # Vehicle Makes
        cur.execute("""
        CREATE TABLE IF NOT EXISTS vehicle_makes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            common_name TEXT
        )
        """)

        # Vehicle Types Classification
        cur.execute("""
        CREATE TABLE IF NOT EXISTS vehicle_types (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,  -- 'petrol_car', 'diesel_car', 'petrol_lgv', 'diesel_lgv', 'motorcycle'
            name TEXT NOT NULL,
            description TEXT
        )
        """)

        # Vehicle Classification Rules (determine type from V5C, weight, seats)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS classification_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_name TEXT UNIQUE NOT NULL,
            condition_sql TEXT NOT NULL,  -- Python expression as string for evaluation
            vehicle_type_id INTEGER NOT NULL,
            FOREIGN KEY (vehicle_type_id) REFERENCES vehicle_types(id)
        )
        """)

        # Emission Standards (general limits by date and vehicle type)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS emission_standards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_type_id INTEGER NOT NULL,
            date_from DATE NOT NULL,  -- first use on or after this date
            date_to DATE,             -- first use before this date (NULL = ongoing)
            test_type TEXT NOT NULL,  -- 'non_catalyst', 'basic', 'extended', 'diesel_smoke'
            co_limit_percent REAL,    -- CO limit % vol at idle/fast idle
            hc_limit_ppm INTEGER,     -- HC limit ppm
            lambda_min REAL,          -- Min lambda (air/fuel ratio)
            lambda_max REAL,          -- Max lambda
            fast_idle_rpm_min INTEGER,
            fast_idle_rpm_max INTEGER,
            normal_idle_rpm_min INTEGER,
            normal_idle_rpm_max INTEGER,
            oil_temp_min_c INTEGER,
            notes TEXT,
            FOREIGN KEY (vehicle_type_id) REFERENCES vehicle_types(id)
        )
        """)

        # Specific Model Limits (from the Annex - detailed per make/model/engine)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS specific_model_limits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            make_id INTEGER NOT NULL,
            model_name TEXT NOT NULL,
            engine_code TEXT,
            engine_cc INTEGER,
            fuel_type TEXT NOT NULL,  -- 'petrol', 'diesel', 'gas'
            date_from DATE,           -- model year start
            date_to DATE,             -- model year end
            test_type TEXT NOT NULL,  -- 'extended' catalyst test
            co_limit_percent REAL,
            hc_limit_ppm INTEGER,
            lambda_min REAL,
            lambda_max REAL,
            fast_idle_rpm_min INTEGER,
            fast_idle_rpm_max INTEGER,
            normal_idle_rpm_min INTEGER,
            normal_idle_rpm_max INTEGER,
            oil_temp_min_c INTEGER,
            FOREIGN KEY (make_id) REFERENCES vehicle_makes(id),
            UNIQUE(make_id, model_name, engine_code, date_from)
        )
        """)

        # Diesel Smoke Standards (by date and turbocharged status)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS diesel_smoke_standards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_from DATE NOT NULL,
            date_to DATE,
            vehicle_weight_category TEXT NOT NULL,  -- 'passenger_car', 'lgv', 'hgv'
            turbocharged BOOLEAN NOT NULL,         -- 0=naturally aspirated, 1=turbocharged
            opacity_limit_m1 REAL NOT NULL,        -- smoke absorption coefficient (m⁻¹)
            notes TEXT
        )
        """)

        # Test Procedure Flowcharts (decision logic)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS test_flowcharts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_type TEXT NOT NULL,  -- 'petrol', 'diesel'
            first_use_date DATE,
            has_catalyst BOOLEAN,
            is_passenger_car BOOLEAN,
            is_in_annex BOOLEAN,
            result_test_type TEXT NOT NULL,
            description TEXT
        )
        """)

        # Exceptions and Special Cases
        cur.execute("""
        CREATE TABLE IF NOT EXISTS special_cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_name TEXT UNIQUE NOT NULL,
            condition_description TEXT NOT NULL,
            test_procedure TEXT NOT NULL,
            notes TEXT
        )
        """)

        # MIL (Engine Management Light) Requirements
        cur.execute("""
        CREATE TABLE IF NOT EXISTS mil_requirements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fuel_type TEXT NOT NULL,
            first_use_date DATE NOT NULL,
            min_passenger_seats INTEGER,  -- NULL = any
            includes_hybrids BOOLEAN DEFAULT 0,
            must_check_mil BOOLEAN DEFAULT 1,
            notes TEXT
        )
        """)

        # Visual Smoke Test (pre-1979 diesel, pre-1975 petrol)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS visual_smoke_criteria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_type TEXT NOT NULL,  -- 'petrol', 'diesel'
            first_use_before DATE NOT NULL,
            test_description TEXT NOT NULL,
            fail_condition TEXT NOT NULL
        )
        """)

        self.conn.commit()

    def _seed_reference_data(self):
        """Populate tables with initial MOT manual data."""
        cur = self.conn.cursor()

        # Vehicle Types
        vehicle_types = [
            ('petrol_car', 'Petrol Passenger Car', 'Petrol-engined passenger car as defined in C&U Regulations'),
            ('diesel_car', 'Diesel Passenger Car', 'Diesel-engined passenger car'),
            ('petrol_lgv', 'Petrol Light Goods Vehicle', 'Petrol LGV up to 3500kg DGW'),
            ('diesel_lgv', 'Diesel Light Goods Vehicle', 'Diesel LGV up to 3500kg DGW'),
            ('petrol_passenger_many_seats', 'Petrol Large Passenger Vehicle', 'Petrol vehicle with >8 passenger seats'),
            ('diesel_passenger_many_seats', 'Diesel Large Passenger Vehicle', 'Diesel vehicle with >8 passenger seats'),
            ('motorcycle', 'Motorcycle', 'Two-wheeled vehicle'),
            ('kit_car', 'Kit Car/Amateur Built', 'Self-built vehicle requiring SVA/IVA'),
        ]
        for code, name, desc in vehicle_types:
            cur.execute("INSERT OR IGNORE INTO vehicle_types (code, name, description) VALUES (?, ?, ?)",
                       (code, name, desc))

        # MIL Requirements
        mil_requirements = [
            # Petrol cars with 4+ wheels, up to 8 passenger seats + driver, first used on/after 1 July 2003
            ('petrol', '2003-07-01', 8, False, True, 'Check MIL illuminates on ignition and goes off after engine start'),
            # Petrol with >8 passenger seats, first used on/after 1 July 2008
            ('petrol', '2008-07-01', None, False, True, 'Check MIL for larger passenger vehicles'),
            # Gas and bi-fuel including hybrids, first used on/after 1 July 2008
            ('gas', '2008-07-01', None, True, True, 'Check MIL for gas/bi-fuel vehicles'),
            # Diesel including hybrids, first used on/after 1 July 2008
            ('diesel', '2008-07-01', None, True, True, 'Check MIL for diesel vehicles'),
        ]
        for fuel_type, date, seats, hybrid, must_check, notes in mil_requirements:
            cur.execute("""
                INSERT OR IGNORE INTO mil_requirements
                (fuel_type, first_use_date, min_passenger_seats, includes_hybrids, must_check_mil, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (fuel_type, date, seats, hybrid, must_check, notes))

        # Visual Smoke Criteria
        visual_smoke = [
            ('petrol', '1975-08-01', 'Visual check for dense blue or black smoke at idle and during acceleration',
             'Fail if dense blue or clearly visible black smoke emitted continuously for 5 seconds at idle'),
            ('diesel', '1980-01-01', 'Visual assessment at idle and during free acceleration',
             'Fail if dense blue or black smoke for 5+ seconds at idle, or excessive smoke during acceleration obscuring vision'),
        ]
        for vehicle_type, date_before, desc, fail_cond in visual_smoke:
            cur.execute("""
                INSERT OR IGNORE INTO visual_smoke_criteria
                (vehicle_type, first_use_before, test_description, fail_condition)
                VALUES (?, ?, ?, ?)
            """, (vehicle_type, date_before, desc, fail_cond))

        # Diesel Smoke Standards (Table 3)
        diesel_standards = [
            # Pre-1980: visual only (no numeric limit)
            ('1980-01-01', None, 'passenger_car', False, None, 'Visual test only'),
            # 1979-2008: non-turbo 2.5 m⁻¹, turbo 3.0 m⁻¹
            ('1979-08-01', '2008-07-01', 'passenger_car', False, 2.5, 'Non-turbocharged engines'),
            ('1979-08-01', '2008-07-01', 'passenger_car', True, 3.0, 'Turbocharged engines'),
            # 2008-2014: all 1.5 m⁻¹
            ('2008-07-01', '2014-01-01', 'passenger_car', False, 1.5, 'All engines'),
            ('2008-07-01', '2014-01-01', 'passenger_car', True, 1.5, 'All engines'),
            # 2014 onwards: all 0.7 m⁻¹
            ('2014-01-01', None, 'passenger_car', False, 0.7, 'All engines'),
            ('2014-01-01', None, 'passenger_car', True, 0.7, 'All engines'),
        ]
        for date_from, date_to, weight_cat, turbo, limit, notes in diesel_standards:
            cur.execute("""
                INSERT OR IGNORE INTO diesel_smoke_standards
                (date_from, date_to, vehicle_weight_category, turbocharged, opacity_limit_m1, notes)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (date_from, date_to, weight_cat, turbo, limit, notes))

        # General Petrol Emission Standards (Table 1 & 2)
        # These are simplified defaults; specific model limits override
        petrol_standards = [
            # Pre-1975: visual only
            ('1975-08-01', None, 'petrol_car', 'visual', None, None, None, None, None, None, None, None, None, 'Visual test'),
            # 1975-1986: non-catalyst idle standards
            ('1975-08-01', '1986-08-01', 'petrol_car', 'non_catalyst', 4.5, 1200, None, None, None, None, None, None, None, 'Idle test only'),
            # 1986-1992: non-catalyst idle standards (slightly tighter)
            ('1986-08-01', '1992-08-01', 'petrol_car', 'non_catalyst', 3.5, 1200, None, None, None, None, None, None, None, 'Idle test only'),
            # 1992-1995 (not in Annex): non-catalyst but may need extended if catalyst present
            ('1992-08-01', '1995-09-01', 'petrol_car', 'non_catalyst', 3.5, 1200, None, None, None, None, None, None, None, 'Use if not listed in Annex'),
            # 1995-2002 (not in Annex): basic catalyst test (BET)
            ('1995-09-01', '2002-09-01', 'petrol_car', 'basic', 0.2, 200, 0.97, 1.03, 2500, 3000, 450, 1500, 80, 'BET: fast idle CO/HC/λ, idle CO'),
            # 2002 onwards (not in Annex): basic catalyst test (same)
            ('2002-09-01', None, 'petrol_car', 'basic', 0.2, 200, 0.97, 1.03, 2500, 3000, 450, 1500, 80, 'BET for vehicles not in Annex but first used after 2002'),
        ]
        for entry in petrol_standards:
            date_from, date_to, vtype, test_type, co, hc, lam_min, lam_max, fast_min, fast_max, idle_min, idle_max, oil_temp, notes = entry
            cur.execute("""
                INSERT OR IGNORE INTO emission_standards
                (vehicle_type_id, date_from, date_to, test_type, co_limit_percent, hc_limit_ppm,
                 lambda_min, lambda_max, fast_idle_rpm_min, fast_idle_rpm_max,
                 normal_idle_rpm_min, normal_idle_rpm_max, oil_temp_min_c, notes)
                VALUES (
                    (SELECT id FROM vehicle_types WHERE code = ?),
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            """, (vtype, date_from, date_to, test_type, co, hc, lam_min, lam_max, fast_min, fast_max, idle_min, idle_max, oil_temp, 'Default from Table 1/2'))

        # Special Cases
        special_cases = [
            ('kit_cars', 'Kit car or amateur-built vehicle first used on/after 1 Aug 1998',
             'Test to limits in V5C registration document. If no limits shown, test to limits of engine at time of SVA/IVA.',
             'Kit cars require SVA/IVA approval; use engine date for standards if V5C silent'),
            ('personal_imports', 'Personal import with manufacturer letter proving engine cannot meet catalyst standards',
             'Test to next lower emission standard (non-catalyst)',
             'Letter from manufacturer required; otherwise must meet catalyst limits'),
            ('engine_swap_old', 'Vehicle first used before 1 Sep 2002 fitted with older engine',
             'Test to standards applicable to engine age (not vehicle age)',
             'Presenter must prove engine age via documentation'),
            ('engine_swap_new', 'Vehicle first used on/after 1 Sep 2002 fitted with different engine',
             'Test to standards for vehicle age (not engine age)',
             'Regardless of engine, follow vehicle first use date'),
            ('dual_exhaust', 'Vehicle with dual exhaust system',
             'Average emissions from both tailpipes (add readings, divide by 2)',
             'Even if balance pipe present, treat as dual exhaust'),
            ('lpg_hc_correction', 'Vehicle running on LPG',
             'Divide HC reading by Propane/Hexane Equivalency Factor (PEF) from analyser',
             'HC reading on LPG is propane; must convert to hexane equivalent'),
            ('modified_engine', 'Engine modified in any way',
             'Must still meet exhaust emission requirements according to vehicle age',
             'Modifications do not exempt from standards'),
        ]
        for name, cond, proc, notes in special_cases:
            cur.execute("""
                INSERT OR IGNORE INTO special_cases (case_name, condition_description, test_procedure, notes)
                VALUES (?, ?, ?, ?)
            """, (name, cond, proc, notes))

        self.conn.commit()

    def add_make(self, name: str, common_name: Optional[str] = None) -> int:
        """Add a vehicle make and return its ID."""
        cur = self.conn.cursor()
        cur.execute("INSERT OR IGNORE INTO vehicle_makes (name, common_name) VALUES (?, ?)",
                    (name, common_name or name))
        cur.execute("SELECT id FROM vehicle_makes WHERE name = ?", (name,))
        row = cur.fetchone()
        return row['id'] if row else None

    def add_model_limit(self, make_id: int, model: str, engine_code: Optional[str], engine_cc: Optional[int],
                       fuel_type: str, date_from: str, date_to: Optional[str], test_type: str, limits: Dict[str, Any]):
        """Insert a specific model limit from the Annex."""
        cur = self.conn.cursor()
        cur.execute("""
            INSERT OR REPLACE INTO specific_model_limits
            (make_id, model_name, engine_code, engine_cc, fuel_type, date_from, date_to,
             test_type, co_limit_percent, hc_limit_ppm, lambda_min, lambda_max,
             fast_idle_rpm_min, fast_idle_rpm_max, normal_idle_rpm_min, normal_idle_rpm_max,
             oil_temp_min_c)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            make_id, model, engine_code, engine_cc, fuel_type, date_from, date_to, test_type,
            limits.get('co'), limits.get('hc'), limits.get('lambda_min'), limits.get('lambda_max'),
            limits.get('fast_rpm_min'), limits.get('fast_rpm_max'),
            limits.get('idle_rpm_min'), limits.get('idle_rpm_max'),
            limits.get('oil_temp')
        ))

    def get_test_type_for_vehicle(self, first_use_date: str, fuel_type: str, vehicle_type_code: str,
                                  has_catalyst: bool, is_in_annex: bool) -> Dict[str, Any]:
        """
        Determine which MOT emissions test applies to a given vehicle.
        Implements the flowchart logic from MOT manual section 8.2.1.
        """
        # Convert date string to date object for comparison
        fud = datetime.strptime(first_use_date, '%Y-%m-%d').date()

        cur = self.conn.cursor()

        # Get vehicle type ID
        cur.execute("SELECT id FROM vehicle_types WHERE code = ?", (vehicle_type_code,))
        vt_row = cur.fetchone()
        if not vt_row:
            return {'error': f'Unknown vehicle type: {vehicle_type_code}'}
        vt_id = vt_row['id']

        # Special pre-1975 petrol: visual only
        if fuel_type == 'petrol' and fud < datetime(1975, 8, 1).date():
            return {
                'test_type': 'visual',
                'description': 'Visual smoke check only (vehicle first used before 1 Aug 1975)'
            }

        # Diesel pre-1980: visual
        if fuel_type == 'diesel' and fud < datetime(1980, 1, 1).date():
            return {
                'test_type': 'visual_diesel',
                'description': 'Visual smoke check at idle and during acceleration (diesel pre-1980)'
            }

        # From here: metered test required
        # Check for catalyst/advanced emission control
        # Logic from manual: Use flowcharts 1-3 to decide

        # If petrol first used on/after 1 Aug 1992 AND listed in Annex → extended catalyst test
        # If petrol first used on/after 1 Aug 1995 but NOT in Annex → still basic test (non-catalyst limits)
        # If petrol first used between 1975-1992 → non-catalyst test

        if fuel_type == 'petrol':
            # Passenger car (pre-1992)
            if fud < datetime(1992, 8, 1).date():
                # Non-catalyst test (Table 1/2)
                cur.execute("""
                    SELECT * FROM emission_standards
                    WHERE vehicle_type_id = ? AND date_from <= ? AND (date_to IS NULL OR ? < date_to)
                      AND test_type = 'non_catalyst'
                    ORDER BY date_from DESC LIMIT 1
                """, (vt_id, first_use_date, first_use_date))
                row = cur.fetchone()
                if row:
                    return dict(row)

            # 1992-1995 transition period
            elif fud < datetime(1995, 9, 1).date():
                if is_in_annex:
                    # Extended catalyst test using Annex limits
                    return {'test_type': 'extended_catalyst', 'uses_annex': True}
                else:
                    # Non-catalyst (these vehicles not required to meet catalyst standards)
                    cur.execute("""
                        SELECT * FROM emission_standards
                        WHERE vehicle_type_id = ? AND date_from <= ? AND (date_to IS NULL OR ? < date_to)
                          AND test_type = 'non_catalyst'
                        ORDER BY date_from DESC LIMIT 1
                    """, (vt_id, first_use_date, first_use_date))
                    row = cur.fetchone()
                    if row:
                        return dict(row)

            # 1995 onwards
            else:
                if is_in_annex or has_catalyst:
                    # Extended catalyst test
                    return {'test_type': 'extended_catalyst', 'uses_annex': is_in_annex}
                else:
                    # Basic emissions test (BET)
                    cur.execute("""
                        SELECT * FROM emission_standards
                        WHERE vehicle_type_id = ? AND date_from <= ? AND (date_to IS NULL OR ? < date_to)
                          AND test_type = 'basic'
                        ORDER BY date_from DESC LIMIT 1
                    """, (vt_id, first_use_date, first_use_date))
                    row = cur.fetchone()
                    if row:
                        return dict(row)

        elif fuel_type == 'diesel':
            # Diesel: all post-1980 get metered smoke test
            # Determine limit based on date and turbocharged status
            # Note: turbo status may need to be detected from vehicle or determined by presence of turbo (VIN inspection)
            cur.execute("""
                SELECT * FROM diesel_smoke_standards
                WHERE date_from <= ? AND (date_to IS NULL OR ? < date_to)
                  AND vehicle_weight_category = ?
                ORDER BY date_from DESC LIMIT 1
            """, (first_use_date, first_use_date, 'passenger_car'))
            row = cur.fetchone()
            if row:
                result = dict(row)
                result['test_type'] = 'diesel_smoke'
                return result

        return {'error': 'No matching emission standard found'}

    def query_vehicle_standards(self, make: str, model: str, engine_code: Optional[str],
                                first_use_date: str) -> Dict[str, Any]:
        """
        Complete lookup for a specific vehicle.
        Returns: test type, limits, procedure, and references.
        """
        cur = self.conn.cursor()

        # Normalize inputs
        make_lower = make.strip().lower()
        model_lower = model.strip().lower()

        # Look up make
        cur.execute("SELECT id FROM vehicle_makes WHERE LOWER(name) = ? OR LOWER(common_name) = ?",
                    (make_lower, make_lower))
        make_row = cur.fetchone()
        if not make_row:
            return {'error': f'Make not found: {make}'}
        make_id = make_row['id']

        # Look up specific model limit
        # Try exact match on model and optionally engine_code
        cur.execute("""
            SELECT * FROM specific_model_limits
            WHERE make_id = ? AND LOWER(model_name) = ? AND fuel_type IN ('petrol', 'diesel')
              AND date_from <= ? AND (date_to IS NULL OR ? <= date_to)
            ORDER BY date_from DESC
            LIMIT 1
        """, (make_id, model_lower, first_use_date, first_use_date))
        model_row = cur.fetchone()

        if model_row:
            model_data = dict(model_row)
            # This is an Annex-listed vehicle → extended catalyst test with specific limits
            return {
                'source': 'specific_model_limits',
                'vehicle': model_data,
                'test_type': 'extended_catalyst',
                'requires_annex_lookup': True,
                'limits': {
                    'co_limit_percent': model_data['co_limit_percent'],
                    'hc_limit_ppm': model_data['hc_limit_ppm'],
                    'lambda_min': model_data['lambda_min'],
                    'lambda_max': model_data['lambda_max'],
                    'fast_idle_rpm_min': model_data['fast_idle_rpm_min'],
                    'fast_idle_rpm_max': model_data['fast_idle_rpm_max'],
                    'normal_idle_rpm_min': model_data['normal_idle_rpm_min'],
                    'normal_idle_rpm_max': model_data['normal_idle_rpm_max'],
                    'oil_temp_min_c': model_data['oil_temp_min_c']
                }
            }

        # No specific model in Annex → use general standards based on date, fuel, type
        # Determine vehicle type
        # For this demo, assume passenger car if weight <=2500kg and seats <=5
        # In real app, you'd have V5C data or user input
        vehicle_type_code = 'petrol_car'  # placeholder; would derive from fuel_type + classification

        # Need fuel_type and first_use_date
        # Since we don't have it from the query yet, we'd get it from make/model metadata
        # For now, let's assume petrol if not diesel

        # In a full implementation, we'd first determine fuel_type and vehicle_type_code
        # from a separate metadata table or user input. For this prototype we'll need that info.

        return {'error': 'Model not in Annex; need general classification (fuel type, DGW, seats) to determine test'}


def build_database(db_path: str = "mot_emissions.db"):
    """
    Build the MOT emissions database.
    This function populates the database with seed data.
    In a real implementation, we would parse the full Annex tables
    from the PDF to populate specific_model_limits.
    """
    db = MOTDatabase(db_path)
    db.initialize()
    print(f"[OK] Created MOT database: {db_path}")

    # Demonstrate a query
    print("\n--- Demo Query ---")
    result = db.get_test_type_for_vehicle('2010-05-15', 'petrol', 'petrol_car', True, True)
    if 'error' not in result:
        print("Test determination result:")
        for k, v in result.items():
            print(f"  {k}: {v}")
    else:
        print(f"Error: {result['error']}")

    db.close()


if __name__ == "__main__":
    build_database()
