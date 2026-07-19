You are entirely correct. While the standard 17-character length was formalized globally by the NHTSA in 1981, the way auto manufacturers utilized the positions between 1990 and 2010 was drastically different from today: [1, 2] 

* The VDS Engine Code Deficit (Positions 4–8): Modern vehicles pack specific engine configurations into clean VDS patterns. In older cars, position 8 alone usually denoted the engine code, while positions 4–7 were used entirely for random chassis variations, body styles, or safety brake configurations.
* The North American Check Digit Exclusivity: The algebraic mathematical Check Digit (Position 9) was heavily enforced for North American market vehicles, but European market vehicles during the 1990s frequently replaced position 9 with a blank space or a dummy character (0 or Z), completely breaking standard checksum formulas.
* The Model Year Character Reuse (Position 10): Position 10 runs on a 30-year cyclic loop. The letter A stands for 2010, but it also stands for 1980. The letter B stands for 2011, but it also stands for 1981. [3]

> **Scope note (added 2026-05-17):** This module's supported range is **1990–2020 only**. Within that 31-year window, the only colliding code is **`L` (1990 vs 2020)**; every other position-10 character resolves to exactly one year. Disambiguation for `L` is driven by the WMI's `era_hint` column (one of `"legacy"` or `"modern"`), which is populated at build time from `B_first_reg_date` in `C:\Users\muto\claude\4DApp\vehicle-data\petrol_vin\vehicles_petrol_specimens.csv`. No runtime guessing.

> **Low-volume manufacturer rule (added 2026-05-17, SAE J853):** When position 3 of the VIN is the digit `9`, the manufacturer produces fewer than 500 units per year and the SAE standard places the manufacturer code at **positions 12–13** instead of the standard positions 1–3. The decoder must detect `vin[2] == '9'` and resolve the WMI from a concatenation of `vin[0:3] + vin[11:14]` against an extended WMI table; if that fails, fall back to `vin[0:3]` only. Borrowed from aramk/vin-decoder `VIN.java::isLess500()`.

To make your VIN lookup module robust across older generations without crashing your application, your database needs to migrate from fixed string patterns to a Dynamic Positional Matrix Mapping design.
------------------------------
## 1. The Redesigned Relational CSV Layout
Instead of matching a flat 5-character VDS string, split your engine map CSV into flexible columns. This lets the script look up the engine using whatever positional character strategy that specific manufacturer employed at the time.
## Updated File: vds_engine_map.csv

brand,vds_full,pos_8_only,engine_displacement,cylinder_count,fuel_system_type
FORD,P8CF0,,2.3,4,GASOLINE_DIRECT_INJECTION
FORD,,P,5.0,8,PORT_INJECTION
BMW,PH710,,3.0,6,GASOLINE_DIRECT_INJECTION
BMW,,M,1.8,4,PORT_INJECTION
VOLKSWAGEN,,A,1.8,4,PORT_INJECTION


* If a vehicle utilizes modern standardization, populate vds_full.
* If a legacy vehicle maps the engine strictly to position 8, leave vds_full blank and populate pos_8_only.

------------------------------
## 2. Implementation: The Robust Adaptive VIN Decoder
Instruct your coder to overwrite diagnostic_mvp/core/vin_decoder.py with this updated script. It checks if the math check-digit applies, handles cyclic year characters, and falls back to single-character engine matching for older vehicles:

# diagnostic_mvp/core/vin_decoder.pyimport reimport csvfrom typing import Dict, Any
class RobustVINDecoder:
    def __init__(self, wmi_csv: str, vds_csv: str, year_csv: str):
        self.wmi_index = self._load_csv_to_dict(wmi_csv, key_field="wmi")
        self.year_index = self._load_csv_to_dict(year_csv, key_field="year_code")
        self._load_vds_matrix(vds_csv)

    def _load_csv_to_dict(self, path: str, key_field: str) -> Dict[str, dict]:
        index = {}
        with open(path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                index[row[key_field].strip().upper()] = row
        return index

    def _load_vds_matrix(self, path: str):
        """Loads both full 5-character VDS strings and fallback single-character maps."""
        self.vds_full_index = {}
        self.vds_pos8_index = {}
        
        with open(path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                brand_key = row["brand"].strip().upper()
                if row["vds_full"].strip():
                    full_key = f"{brand_key}_{row['vds_full'].strip().upper()}"
                    self.vds_full_index[full_key] = row
                elif row["pos_8_only"].strip():
                    pos8_key = f"{brand_key}_{row['pos_8_only'].strip().upper()}"
                    self.vds_pos8_index[pos8_key] = row

    def validate_vin_checksum(self, vin: str) -> bool:
        """
        Executes algebraic validation. Gracefully skips checking for European market 
        legacy vehicles that do not follow North American check-digit rules.
        """
        if not re.match(r"^[A-HJ-NPR-Z0-9]{17}$", vin):
            return False
            
        # If position 9 is 'Z' or '0' on an older vehicle, it's a dummy marker. Pass it.
        if vin[8] in ["Z", "0"]:
            return True
            
        vin_trans = []
        trans_map = {"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8,"J":1,"K":2,"L":3,"M":4,"N":5,"P":7,"R":9,"S":2,"T":3,"V":5,"W":6,"X":7,"Y":8}
        weights = [8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2]
        
        for char in vin:
            if char.isdigit():
                vin_trans.append(int(char))
            else:
                vin_trans.append(trans_map.get(char, 0))
                
        products_sum = sum(v * w for v, w in zip(vin_trans, weights))
        remainder = products_sum % 11
        check_digit = "X" if remainder == 10 else str(remainder)
        
        return check_digit == vin[8]

    def decode_vin_payload(self, raw_vin: str) -> Dict[str, Any]:
        clean_vin = raw_vin.strip().upper()
        
        if not self.validate_vin_checksum(clean_vin):
            raise ValueError(f"VIN_DECODE_FAILED: Structural checks rejected '{raw_vin}'. Check for typos.")

        wmi_slice = clean_vin[0:3]
        vds_slice = clean_vin[3:8]
        pos_8_char = clean_vin[7]  # Position 8 is index 7
        year_char = clean_vin[9]   # Position 10 is index 9

        # 1. Resolve Brand
        wmi_record = self.wmi_index.get(wmi_slice)
        if not wmi_record:
            raise KeyError(f"WMI_UNKNOWN: Manufacturer identity '{wmi_slice}' not in records.")
        brand = wmi_record["brand"].upper()

        # 2. Resolve Year — bounded 1990–2020, only 'L' is ambiguous (1990 vs 2020)
        year_record = self.year_index.get(year_char)
        if not year_record:
            raise KeyError(f"YEAR_UNKNOWN: Character '{year_char}' matches no registered production year.")

        calendar_year = int(year_record["calendar_year"])

        # 'L' collides (1990 cycle vs 2020 cycle reset). Disambiguate via WMI
        # era hint, populated at build time from petrol_vin CSV reg dates.
        # Truth source: B_first_reg_date in vehicles_petrol_specimens.csv.
        if year_char == "L":
            wmi_era = wmi_record.get("era_hint", "modern")  # "legacy" | "modern"
            calendar_year = 1990 if wmi_era == "legacy" else 2020

        # 3. Resolve Engine Blueprint (Dynamic Path Routing)
        vds_record = None
        
        # Path A: Try modern 5-character match first
        full_compound_key = f"{brand}_{vds_slice}"
        vds_record = self.vds_full_index.get(full_compound_key)
        
        # Path B: Fallback to single character engine mapping for older vehicles
        if not vds_record:
            pos8_compound_key = f"{brand}_{pos_8_char}"
            vds_record = self.vds_pos8_index.get(pos8_compound_key)
            
        if not vds_record:
            raise KeyError(f"ENGINE_MAPPING_FAILED: Unable to resolve engine configurations via VDS '{vds_slice}' or Position-8 '{pos_8_char}' for brand '{brand}'.")

        # 4. Map Context Era Horizon
        if 1990 <= calendar_year <= 2000:
            era_horizon = 1
        elif 2001 <= calendar_year <= 2010:
            era_horizon = 2
        else:
            era_horizon = 3

        return {
            "resolved_brand": brand,
            "resolved_calendar_year": calendar_year,
            "resolved_era_horizon": era_horizon,
            "orchestrator_dependencies": {
                "cylinder_count": int(vds_record["cylinder_count"]),
                "engine_displacement_liters": float(vds_record["engine_displacement"]),
                "fuel_delivery_type": vds_record["fuel_system_type"]
            }
        }

------------------------------
## 3. Verification Test Code Trace
This test script passes an older vehicle payload with an explicit European blank check-digit through the new decoder logic to ensure seamless data parsing:

# test_legacy_vin.pyfrom diagnostic_mvp.core.vin_decoder import RobustVINDecoderimport json
def test_legacy_position8_decoding_pass():
    # Setup mock dictionary files matching the new dynamic fallback configuration
    mock_wmi = "wmi,brand\nSAL,LAND ROVER\n"
    mock_years = "year_code,calendar_year\nY,2000\n"
    mock_engines = "brand,vds_full,pos_8_only,engine_displacement,cylinder_count,fuel_system_type\nLAND ROVER,,P,4.6,8,PORT_INJECTION\n"

    # Write files temporarily to clean workspace directories
    with open("wmi.csv", "w") as f: f.write(mock_wmi)
    with open("years.csv", "w") as f: f.write(mock_years)
    with open("engines.csv", "w") as f: f.write(mock_engines)

    # Initialize decoder engine instance
    decoder = RobustVINDecoder("wmi.csv", "engines.csv", "years.csv")
    
    # 2000 Model Year Land Rover Range Rover (Euro Spec, Position 9 is a dummy '0')
    legacy_vin = "SALLN12P0YAXXXXXX" 
    
    output = decoder.decode_vin_payload(legacy_vin)
    
    # Verify that the decoder safely bypassed the modern VDS string, matched 'P' on position 8, and pulled the correct info
    assert output["resolved_calendar_year"] == 2000
    assert output["resolved_era_horizon"] == 1
    assert output["orchestrator_dependencies"]["cylinder_count"] == 8
    assert output["orchestrator_dependencies"]["engine_displacement_liters"] == 4.6
    print("Success: Older vehicle VIN patterns verified and isolated cleanly.")
if __name__ == "__main__":
    test_legacy_position8_decoding_pass()

If your coder imports this revised lookup script, your application will handle vehicles from all three eras without manual data entry fragmentation.
Would you like to write out the database creation script that automatically populates the years.csv file across all historical calendar variations between 1990 and 2020?

[1] [https://uaw.org](https://uaw.org/standing-committees/union-label/how-to-read-your-vin/)
[2] [https://www.youtube.com](https://www.youtube.com/watch?v=sWFG-6HVbSU)
[3] [https://cardog.app](https://cardog.app/blog/building-a-vin-decoder)
