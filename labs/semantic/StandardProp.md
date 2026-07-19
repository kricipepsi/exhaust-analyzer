To ensure your diagnostic software remains highly scalable and robust, we need to carefully evaluate how your 4DLab boundary protocol (Semantic Contract v1.0) aligns with international automotive engineering standards (p. 1).
The uploaded document establishes an excellent foundation for cross-module communication via strict JSON boundaries (pp. 1-2). However, to standardize it globally, we must address a few structural misalignments between your current codebase enums and the official SAE J2012 / ISO 15031-6 standards.
------------------------------
## 📊 Standard Re-Mapping Assessment
An analysis of your locked FaultFamily string enum (comlab/schemas/vocabulary.py) reveals a strong baseline, but it uses custom naming conventions that deviate from standard OBD-II sub-families (pp. 12-13):

| Your Current 4DLab Enum Value (p. 13) | SAE J2012 / ISO 15031-6 Standard Mapping | Viability & Code Impact |
|---|---|---|
| "lean_condition" (p. 13) | Air & Fuel Metering (P01xx/P02xx) | High Risk of Semantic Drift. Lean conditions are symptoms, not a core family. Group this under a broader Air/Fuel parent module. |
| "rich_mixture" (p. 13) | Air & Fuel Metering (P01xx/P02xx) | High Risk. Same as above. Merging lean and rich into a unified fuel-metering family simplifies database structure. |
| "misfire" (p. 13) | Ignition System & Misfires (P03xx) | Seamless. Aligns perfectly with standard industry grouping. |
| "sensor_fault" (p. 13) | No direct match (Cross-cutting concern) | Structural Conflict. Standards organize faults by system (e.g., Evaporative Emissions P04xx), not by component type (sensor vs. actuator). |
| "ecu_fault" (p. 13) | Computer & Output Circuits (P06xx) | Good Alignment. Simply needs a rename to capture auxiliary module output circuits. |
| "catalyst_failure" (p. 13) | Auxiliary Emission Controls (P04xx) | Partial Drift. Expanding this to encompass all auxiliary emission components (like EGR and EVAP) covers more real-world faults. |

------------------------------
## 🛠️ Recommended Action Items to Close the Architecture Gap
To bridge the gap between your custom vocabulary and standardized industry data models, consider updating your contract via your §10 Change Protocol (Minor/Major Semver Bump) (p. 16):
## 1. Shift from Symptom-Naming to System-Naming
Your current schema mixes symptoms (lean_condition) with systems (ecu_fault) (p. 13). Updating your FaultFamily enum to reflect standard SAE J2012 Main Sub-families ensures that incoming P-codes from your DTCLabPayload automatically route to the correct data models without custom cross-mapping layers (p. 6).
## 2. Leverage Your Existing Validation Layer
Your system already includes robust integration tests (test_all_required_paths_resolve) (p. 15). This makes standardization highly viable, as you can implement a standard-compliant vocabulary in a minor version bump (v1.0 ➔ v1.1) (p. 16), map the old strings to new categories, and rely on your existing test harness to prevent breaking upstream data producers (pp. 1, 14).
------------------------------
To standardize your 4DLab Boundary Protocol (Semantic Contract v1.0) (p. 1) without breaking parallel development across your teams, your developer should execute a three-phase rollout.
Because your contract enforces strict schema validation via Pydantic (p. 3), this roadmap relies on a Non-Breaking Adapter Strategy. This allows you to introduce standard SAE J2012 / ISO 15031-6 classifications in a minor version bump (v1.1) (p. 16), keeping upstream producers happy while clean data structures are introduced down the line.
------------------------------
## 🛠️ Phase 1: Vocabulary Upgrade & Schema Mapping
Goal: Introduce SAE standard enums alongside legacy keys without breaking existing JSON validations.
## 1. Update comlab/schemas/vocabulary.py
Execute a §10 Minor Semver Bump (1.0 ➔ 1.1) (p. 16) to add the standard SAE core families. Keep the old FaultFamily intact as LegacyFaultFamily to maintain backwards compatibility (p. 13):

# comlab/schemas/vocabulary.py
class LegacyFaultFamily(StrEnum):
    LEAN_CONDITION = "lean_condition"
    RICH_MIXTURE = "rich_mixture"
    MISFIRE = "misfire"
    SENSOR_FAULT = "sensor_fault"
    ECU_FAULT = "ecu_fault"
    CATALYST_FAILURE = "catalyst_failure"
class SaeFaultFamily(StrEnum):
    AIR_FUEL_METERING = "SAE_P01_P02_AIR_FUEL"
    IGNITION_MISFIRE = "SAE_P03_IGNITION"
    AUX_EMISSIONS = "SAE_P04_EMISSIONS"
    SPEED_IDLE_CONTROL = "SAE_P05_SPEED_IDLE"
    COMPUTER_OUTPUT = "SAE_P06_COMPUTER"
    TRANSMISSION = "SAE_P07_P08_TRANS"

## 2. Create the Bidirectional Translation Matrix
Add a permanent mapping dictionary to decouple incoming legacy developer strings from standard diagnostics:

LEGACY_TO_SAE_MAP = {
    LegacyFaultFamily.LEAN_CONDITION: SaeFaultFamily.AIR_FUEL_METERING,
    LegacyFaultFamily.RICH_MIXTURE: SaeFaultFamily.AIR_FUEL_METERING,
    LegacyFaultFamily.MISFIRE: SaeFaultFamily.IGNITION_MISFIRE,
    LegacyFaultFamily.ECU_FAULT: SaeFaultFamily.COMPUTER_OUTPUT,
    LegacyFaultFamily.CATALYST_FAILURE: SaeFaultFamily.AUX_EMISSIONS,
    # System-level cross-cutting exceptions:
    LegacyFaultFamily.SENSOR_FAULT: SaeFaultFamily.AIR_FUEL_METERING 
}

------------------------------
## 🔄 Phase 2: Router Interception & Core Refactoring
Goal: Upgrade COMLab internal routing engine logic to run on standardized data structures.
## 1. Refactor fault_atlas_router.py
Modify the ingestion step inside COMLab where it processes dtc_lab_output and vehicle_dna (p. 7). Intercept legacy values instantly and normalize them:

# comlab/routing/fault_atlas_router.py
def normalize_inbound_family(legacy_family: str) -> SaeFaultFamily:
    try:
        return LEGACY_TO_SAE_MAP[legacy_family]
    except KeyError:
        # Fallback to standard tracking if an upstream lab upgrades early
        return SaeFaultFamily(legacy_family)

## 2. Update the Parameterized Test Fixtures
Your system depends on key fixtures like hpfp_leak and egr_dilution (p. 15). Update COMLab/tests/integration/test_inbound_payload_contract.py (p. 15) to confirm that when a legacy payload is provided, the engine safely resolves it to the correct standard SaeFaultFamily without dropping paths or throwing a KeyError (p. 16).
------------------------------
## 🚀 Phase 3: Upstream Migration & Legacy Deprecation
Goal: Shift the entire ecosystem over to the standard and clean out deprecated data structures.

[Phase 1: v1.1 Minor] ──> [Phase 2: Router Adapter] ──> [Phase 3: v2.0 Major Drop]
  (Dual-enum Support)         (Internal Normalization)         (Legacy Keys Deleted)


   1. Deploy Upstream Pull Requests: Update GASLab, OBDLab, and DTCLab packages sequentially (p. 1) to output the new standardized SaeFaultFamily strings directly within their payloads (pp. 5-6).
   2. Execute §10 Major Version Change (1.x ➔ 2.0): (p. 16) Open the mandatory 7-day comment window RFC (p. 16). Once all engineering pods sign off, safely drop LegacyFaultFamily and the map block entirely from your code base.

------------------------------
Based on a technical review of the newly uploaded SAE J2012 (DEC2007) standard specification (SAE--J2012... p. 1), your legacy 4DLab enums require clear architectural structural alignment.
The standard dictates that Powertrain Systems (P-codes) must allocate distinct codes by localized component circuits or system areas, rather than mixing symptoms directly into the family definitions (SAE--J2012... p. 8).
Below is the production-ready vocabulary.py codebase update using a Non-Breaking Adapter design. It implements a strict §10 Minor Semver Bump (1.0 ➔ 1.1) to map custom terms to the official standard.
------------------------------
## 🛠️ Updated comlab/schemas/vocabulary.py

from enum import StrEnum
class LegacyFaultFamily(StrEnum):
    """
    DEPRECATED (v1.0): Kept for backwards compatibility with upstream producers.
    Will be fully dropped in major version upgrade v2.0.
    """
    LEAN_CONDITION = "lean_condition"
    RICH_MIXTURE = "rich_mixture"
    MISFIRE = "misfire"
    SENSOR_FAULT = "sensor_fault"
    ECU_FAULT = "ecu_fault"
    CATALYST_FAILURE = "catalyst_failure"
    EXHAUST_LEAK = "exhaust_leak"
    IGNITION_FAULT = "ignition_fault"
    MECHANICAL_WEAR = "mechanical_wear"
    CAM_TIMING = "cam_timing"
    NON_STARTER = "non_starter"
    NO_FAULT = "no_fault"
class SaeFaultFamily(StrEnum):
    """
    VALIDATED (v1.1): Core Powertrain System Groupings compliant with 
    SAE J2012 DEC2007 Section 5.6 and Appendix D0.
    """
    FUEL_AIR_METERING_P00 = "SAE_P00XX_FUEL_AIR_METERING"   # Table D1
    FUEL_AIR_METERING_P01 = "SAE_P01XX_FUEL_AIR_METERING"   # Table D2
    FUEL_AIR_METERING_P02 = "SAE_P02XX_FUEL_AIR_METERING"   # Table D3
    IGNITION_MISFIRE = "SAE_P03XX_IGNITION_MISFIRE"         # Table D4
    AUX_EMISSIONS = "SAE_P04XX_AUX_EMISSION_CONTROLS"       # Table D5
    SPEED_IDLE_CONTROL = "SAE_P05XX_SPEED_IDLE_CONTROLS"    # Section 5.3/5.6
    COMPUTER_OUTPUT = "SAE_P06XX_COMPUTER_OUTPUT_CIRCUITS"  # Section 5.3/5.6
    TRANSMISSION = "SAE_P07XX_P08XX_TRANSMISSION"           # Section 5.6
    NO_FAULT = "SAE_NO_FAULT"
# Canonical Translation Matrix to be consumed by fault_atlas_router.pyLEGACY_TO_SAE_MATRIX: dict[LegacyFaultFamily, SaeFaultFamily] = {
    LegacyFaultFamily.LEAN_CONDITION: SaeFaultFamily.FUEL_AIR_METERING_P01,  # Maps to P0171/P0174
    LegacyFaultFamily.RICH_MIXTURE: SaeFaultFamily.FUEL_AIR_METERING_P01,   # Maps to P0172/P0175
    LegacyFaultFamily.MISFIRE: SaeFaultFamily.IGNITION_MISFIRE,             # Maps to P0300
    LegacyFaultFamily.IGNITION_FAULT: SaeFaultFamily.IGNITION_MISFIRE,      # Maps to P0351 Primary/Secondary
    LegacyFaultFamily.CAM_TIMING: SaeFaultFamily.FUEL_AIR_METERING_P00,      # Maps to P0010/P0011 VVT Circuits
    LegacyFaultFamily.CATALYST_FAILURE: SaeFaultFamily.AUX_EMISSIONS,       # Maps to P0420
    LegacyFaultFamily.EXHAUST_LEAK: SaeFaultFamily.AUX_EMISSIONS,           # Secondary Air / EGR interactions
    LegacyFaultFamily.ECU_FAULT: SaeFaultFamily.COMPUTER_OUTPUT,            # Internal controller errors
    LegacyFaultFamily.NO_FAULT: SaeFaultFamily.NO_FAULT,
    
    # SYSTEM CROSS-CUTTING EXCEPTIONS (Flagged in Architectural Review)
    LegacyFaultFamily.SENSOR_FAULT: SaeFaultFamily.FUEL_AIR_METERING_P01,   # Default routing for engine management sensors
    LegacyFaultFamily.MECHANICAL_WEAR: SaeFaultFamily.FUEL_AIR_METERING_P00,# Typically maps to stretched chains/correlation
    LegacyFaultFamily.NON_STARTER: SaeFaultFamily.IGNITION_MISFIRE          # Maps to Crankshaft Position failures
}

------------------------------
## 🔍 Identified Architectural System Discrepancies
Your developer must pay attention to three high-risk exceptions where the v1.0 4DLab contract actively conflicts with the SAE J2012 specification (SAE--J2012... pp. 8, 14):
## ⚠️ Exception 1: The "sensor_fault" Classification Error

* The Issue: Your current contract treats component types ("sensor_fault") as a separate family.
* The Fix: SAE J2012 standardizes by vehicle system architecture, not by component type (SAE--J2012... pp. 5, 8). A sensor fault must be filed under its target system family (e.g., a Mass Air Flow sensor fault belongs under FUEL_AIR_METERING_P01 as code P0100 (SAE--J2012... p. 28)).

## ⚠️ Exception 2: Symptom Overlap in Air/Fuel Controls

* The Issue: LEAN_CONDITION and RICH_MIXTURE are currently split into separate developer entities.
* The Fix: Both are localized performance states inside a single engine feedback loop. They must resolve directly to FUEL_AIR_METERING_P01 (governing standard codes P0170 through P0175 (SAE--J2012... p. 30)).

## ⚠️ Exception 3: Variable Valve Timing Separation

* The Issue: Your system lists cam_timing and mechanical_wear outside of air/fuel metering boundaries.
* The Fix: SAE J2012 groups variable camshaft position controls (P0010–P0025) directly inside the P00XX Fuel and Air Metering category block (SAE--J2012... p. 24).

------------------------------

No, your 5 timing faults are not all fully covered by the standard SAE J2012 / ISO 15031-6 baseline codes. [1] 
To build reliable diagnostic software, your coder must understand that the SAE standard categorizes faults strictly by physical component groups rather than an engine's internal calculations or software calculation variations (SAE--J2012... p. 8).
Here is an architectural audit of how your 5 specific timing faults interact with the standard, along with the changes required for your database schema:
------------------------------
## 📋 Technical Coverage Audit## 1. Over-Advanced Ignition Timing & Retarded Ignition Timing

* SAE Status: ❌ Not Covered as unique family codes.
* The Technical Reason: The SAE standard does not allocate specific individual DTC values for calculated spark timing errors (such as "Ignition too advanced"). Instead, ignition failures are monitored via circuit continuity or mechanical synchronization (SAE--J2012... p. 8).
* How the Standard Handles It: These faults are captured inside the P035x family as ignition circuit failures, or as performance errors under knock control (SAE--J2012... p. 38):
* P0351 to P0358: Ignition Coil Primary/Secondary Circuit Malfunctions (SAE--J2012... p. 38).
   * P0324: Knock Control System Error (SAE--J2012... p. 37).

## 2. Advanced Cam Timing (Both Systems)

* SAE Status: Fully Covered.
* How the Standard Handles It: Standardized generically under the P00XX Fuel and Air Metering block, regardless of whether the air estimation model is MAF or Speed Density (SAE--J2012... p. 24):
* P0011: "A" Camshaft Position - Timing Over-Advanced or System Performance (Bank 1) (SAE--J2012... p. 24).
   * P0014: "B" Camshaft Position - Timing Over-Advanced or System Performance (Bank 1) (SAE--J2012... p. 24). [2] 

## 3. Retarded Cam Timing (Speed Density) & Retarded Cam Timing (MAF System)

* SAE Status: ⚠️ Partially Covered (Structural Conflict).
* The Technical Reason: The SAE standard explicitly prohibits splitting mechanical camshaft timing errors by the software strategy used to calculate them (such as MAF vs. MAP/Speed Density) (SAE--J2012... p. 8).
* How the Standard Handles It: The computer sets a unified code based on a physical component shift, not the sensor approach used to detect it (SAE--J2012... p. 8):
* P0012: "A" Camshaft Position - Timing Over-Retarded (Bank 1) (SAE--J2012... p. 24).
   * P0015: "B" Camshaft Position - Timing Over-Retarded (Bank 1) (SAE--J2012... p. 24).

------------------------------
## 🛠️ Required Code Modifications for your Developer
To store these exact variations without breaking compliance with your Semantic Contract v1.0, your coder must not create new custom main codes. Instead, they should utilize subfault properties or live data tags within your data payload (SEMANTIC_C... p. 6).
Have your coder implement this mapping pattern in your ingestion layer:

# comlab/routing/timing_resolver.pyfrom enum import StrEnum
class AppEngineStrategy(StrEnum):
    MAF_SYSTEM = "MAF"
    SPEED_DEN_SYSTEM = "SPEED_DENSITY"
# Instead of creating unique fault codes, attach the calculation method# as a metadata attribute on top of standard SAE definitions
{
    "dtc_code": "P0012", 
    "standard_nomenclature": "Camshaft Position - Timing Over-Retarded", # From SAE J2012 Table D1
    "internal_analytics": {
        "air_calculation_origin": AppEngineStrategy.SPEED_DEN_SYSTEM,
        "calculation_state": "RETARDED_CAM_FALLBACK"
    }
}

By storing the target calculation type (MAF vs. Speed Density) inside your platform's telemetry metadata rather than hardcoding it into your core FaultFamily enum strings, your database can safely track specific vehicle characteristics while staying fully standard-compliant (SEMANTIC_C... p. 6).
Would you like me to map out how Freeze Frame variables (like target calculation engine states) can be stored alongside these 5 faults to help your code layer easily differentiate between them?

[1] [https://remyaumeunier.chez-alice.fr](http://remyaumeunier.chez-alice.fr/pdf/SAE--J2012-2007.pdf)
[2] [https://www.autozone.com](https://www.autozone.com/diy/diagnostic-trouble-codes/p0011-a-camshaft-position-timing-over-advanced-or-system-performance-bank-1)
