"""Manual verification for T-P2-3 — VL categories 6 and 8b."""
import sys

sys.path.insert(0, ".")

from engine.v2.input_model import (
    DiagnosticInput,
    GasRecord,
    OBDRecord,
    VehicleContext,
)

ctx = VehicleContext(
    brand="VW", model="Golf", engine_code="EA113_1.8T",
    displacement_cc=1781, my=2002,
)

# --- Test 1: Category 6 trigger (negative trims + low fuel pressure) ---
di1 = DiagnosticInput(
    vehicle_context=ctx, dtcs=["P0301"], analyser_type="5-gas",
    gas_idle=GasRecord(co_pct=0.5, hc_ppm=200, co2_pct=14.5, o2_pct=0.5, nox_ppm=200),
    obd=OBDRecord(stft_b1=-18.0, ltft_b1=-20.0, fuel_pressure_kpa=160.0, rpm=800, ect_c=85.0),
)

from engine.v2.validation import validate

vi1 = validate(di1, soft_mode=True)
w6 = [w for w in vi1.warnings if w.category == 6]
print(f"Test 1 (neg trim + low FP): {len(w6)} cat-6 warnings (expect 1)")
for w in w6:
    print(f"  -> {w.message}")
print(f"  obd in valid_channels: {'obd' in vi1.valid_channels} (expect True)")
if "obd" in vi1.invalid_channels:
    print(f"  REJECTION reason: {vi1.invalid_channels['obd']}")

# --- Test 2: Category 6 trigger (positive trims + rich O2) ---
di2 = DiagnosticInput(
    vehicle_context=ctx, dtcs=["P0172"], analyser_type="5-gas",
    gas_idle=GasRecord(co_pct=0.5, hc_ppm=200, co2_pct=14.5, o2_pct=0.5, nox_ppm=200),
    obd=OBDRecord(stft_b1=18.0, ltft_b1=5.0, o2_voltage_b1=0.85, rpm=800, ect_c=85.0),
)
vi2 = validate(di2, soft_mode=True)
w6b = [w for w in vi2.warnings if w.category == 6 and "O2" in w.message]
print(f"Test 2 (pos trim + rich O2): {len(w6b)} cat-6 O2 warnings (expect 1)")
for w in w6b:
    print(f"  -> {w.message}")
print(f"  obd in valid_channels: {'obd' in vi2.valid_channels} (expect True)")

# --- Test 3: Category 8b trigger (VVT angle present) ---
di3 = DiagnosticInput(
    vehicle_context=ctx, dtcs=["P0301"], analyser_type="5-gas",
    gas_idle=GasRecord(co_pct=0.5, hc_ppm=200, co2_pct=14.5, o2_pct=0.5, nox_ppm=200),
    obd=OBDRecord(vvt_angle=35.0, rpm=800, ect_c=85.0),
)
vi3 = validate(di3, soft_mode=True)
w8 = [w for w in vi3.warnings if w.category == 8]
print(f"Test 3 (VVT angle present): {len(w8)} cat-8 warnings (expect 1)")
for w in w8:
    print(f"  -> {w.message}")

# --- Test 4: soft_mode=False suppresses categories 6/8b ---
vi4 = validate(di1, soft_mode=False)
print(f"Test 4 (soft_mode=False): {len(vi4.warnings)} warnings (expect 0)")

# --- Test 5: Clean data, no warnings ---
di5 = DiagnosticInput(
    vehicle_context=ctx, dtcs=["P0301"], analyser_type="5-gas",
    gas_idle=GasRecord(co_pct=0.5, hc_ppm=200, co2_pct=14.5, o2_pct=0.5, nox_ppm=200),
    obd=OBDRecord(stft_b1=-5.0, ltft_b1=-3.0, fuel_pressure_kpa=350.0, rpm=800, ect_c=85.0),
)
vi5 = validate(di5, soft_mode=True)
print(f"Test 5 (clean data): {len(vi5.warnings)} warnings (expect 0)")

# --- Test 6: No OBD — no crash ---
di6 = DiagnosticInput(
    vehicle_context=ctx, dtcs=[], analyser_type="4-gas",
    gas_idle=GasRecord(co_pct=0.5, hc_ppm=200, co2_pct=14.5, o2_pct=0.5),
)
vi6 = validate(di6, soft_mode=True)
print(f"Test 6 (no OBD): {len(vi6.warnings)} warnings (expect 0), nox_suppressed={vi6.nox_suppressed} (expect True)")

# --- Test 7: Categories 6/8b never reject channels ---
print(f"Test 7a (cat-6 no reject): obd valid={'obd' in vi1.valid_channels}, obd ok={'obd' not in vi1.invalid_channels}")
print(f"Test 7b (cat-8b no reject): obd valid={'obd' in vi3.valid_channels}, obd ok={'obd' not in vi3.invalid_channels}")

print("\nDone.")
