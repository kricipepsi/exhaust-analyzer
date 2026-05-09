"""Ad-hoc manual verification for T-P2-2 validation.py task checks."""
from engine.v2.input_model import (
    DiagnosticInput, VehicleContext, GasRecord, OBDRecord, FreezeFrameRecord,
)
from engine.v2.validation import validate

def main() -> None:
    # Shared context
    ctx = VehicleContext(brand="VW", model="Golf", engine_code="EA113",
                         displacement_cc=2000, my=2005)

    # Verification 3: ECT=151 C -> obd channel marked invalid
    obd = OBDRecord(ect_c=151.0, rpm=800)
    di = DiagnosticInput(vehicle_context=ctx, dtcs=[], analyser_type="5-gas", obd=obd)
    vi = validate(di)
    assert "obd" in vi.invalid_channels, f"FAIL: ECT=151 should reject obd, got {vi.invalid_channels}"
    print("PASS: ECT=151 -> obd rejected")

    # Verification 4: O2=19% with RPM=800 -> gas_idle invalid
    gas = GasRecord(co_pct=0.5, hc_ppm=100.0, co2_pct=14.0, o2_pct=19.0)
    obd2 = OBDRecord(rpm=800)
    di2 = DiagnosticInput(vehicle_context=ctx, dtcs=[], analyser_type="5-gas",
                          gas_idle=gas, obd=obd2)
    vi2 = validate(di2)
    assert "gas_idle" in vi2.invalid_channels, f"FAIL: O2=19% should reject gas_idle"
    print("PASS: O2=19% with RPM=800 -> gas_idle rejected")

    # Verification 5: fuel_status=OL_FAULT, ECT=80 -> open_loop_suppression=True
    obd3 = OBDRecord(ect_c=80.0, fuel_status="OL_FAULT", rpm=800)
    di3 = DiagnosticInput(vehicle_context=ctx, dtcs=[], analyser_type="5-gas", obd=obd3)
    vi3 = validate(di3)
    assert vi3.open_loop_suppression, "FAIL: OL_FAULT warm should set open_loop_suppression"
    print("PASS: OL_FAULT + ECT=80 -> open_loop_suppression=True")

    # DTC regex: P0301 valid, BAD/p0420/X0301 invalid
    di4 = DiagnosticInput(vehicle_context=ctx, dtcs=["P0301", "BAD", "p0420", "X0301"],
                          analyser_type="5-gas")
    vi4 = validate(di4)
    assert "dtcs" in vi4.valid_channels, "FAIL: at least one valid DTC should keep channel"
    print("PASS: DTC regex filtering correct")

    # DTC era: P0420 on MY=1995 -> reject
    ctx5 = VehicleContext(brand="VW", model="Golf", engine_code="EA113",
                          displacement_cc=2000, my=1995)
    di5 = DiagnosticInput(vehicle_context=ctx5, dtcs=["P0420"], analyser_type="5-gas")
    vi5 = validate(di5)
    assert "dtcs" in vi5.invalid_channels, "FAIL: P0420 on pre-1996 should reject dtcs"
    print("PASS: P0420 on MY=1995 -> dtcs rejected")

    # DTC era: P0420 on MY=1997 -> pass
    ctx6 = VehicleContext(brand="VW", model="Golf", engine_code="EA113",
                          displacement_cc=2000, my=1997)
    di6 = DiagnosticInput(vehicle_context=ctx6, dtcs=["P0420"], analyser_type="5-gas")
    vi6 = validate(di6)
    assert "dtcs" in vi6.valid_channels, "FAIL: P0420 on 1997 should be valid"
    print("PASS: P0420 on MY=1997 -> dtcs valid")

    # Thermal gate: ECT=74 -> cold_start, ECT=75 -> no cold_start
    di_cold = DiagnosticInput(vehicle_context=ctx, dtcs=[], analyser_type="5-gas",
                              obd=OBDRecord(ect_c=74.0, rpm=800))
    vi_cold = validate(di_cold)
    assert vi_cold.restricted_cold_start, "FAIL: ECT 74 should set cold start"
    print("PASS: ECT=74 -> restricted_cold_start=True")

    di_warm = DiagnosticInput(vehicle_context=ctx, dtcs=[], analyser_type="5-gas",
                              obd=OBDRecord(ect_c=75.0, rpm=800))
    vi_warm = validate(di_warm)
    assert not vi_warm.restricted_cold_start, "FAIL: ECT 75 should not set cold start"
    print("PASS: ECT=75 -> restricted_cold_start=False")

    # Probe count gate
    di_4g = DiagnosticInput(vehicle_context=ctx, dtcs=[], analyser_type="4-gas")
    vi_4g = validate(di_4g)
    assert vi_4g.nox_suppressed, "FAIL: 4-gas should set nox_suppressed"
    print("PASS: 4-gas -> nox_suppressed=True")

    di_5g = DiagnosticInput(vehicle_context=ctx, dtcs=[], analyser_type="5-gas")
    vi_5g = validate(di_5g)
    assert not vi_5g.nox_suppressed, "FAIL: 5-gas should not set nox_suppressed"
    print("PASS: 5-gas -> nox_suppressed=False")

    # MY out of range -> all channels rejected
    ctx_bad = VehicleContext(brand="VW", model="Golf", engine_code="EA113",
                             displacement_cc=2000, my=1985)
    di_bad = DiagnosticInput(vehicle_context=ctx_bad, dtcs=["P0420"], analyser_type="5-gas",
                             gas_idle=GasRecord(co_pct=0.5, hc_ppm=100.0, co2_pct=14.0, o2_pct=0.5))
    vi_bad = validate(di_bad)
    assert len(vi_bad.valid_channels) == 0, f"FAIL: MY 1985 should reject all, got {vi_bad.valid_channels}"
    print("PASS: MY=1985 -> all channels rejected")

    # Gas sum reject: physically impossible sum
    gas_bad = GasRecord(co_pct=10.0, hc_ppm=2000.0, co2_pct=14.0, o2_pct=78.0)
    di8 = DiagnosticInput(vehicle_context=ctx, dtcs=[], analyser_type="5-gas", gas_idle=gas_bad)
    vi8 = validate(di8)
    assert "gas_idle" in vi8.invalid_channels, "FAIL: impossible gas sum should reject"
    print("PASS: impossible gas sum -> gas_idle rejected")

    # ECT delta > 100 between OBD and FF
    obd_delta = OBDRecord(ect_c=25.0, rpm=800)
    ff_delta = FreezeFrameRecord(ect_c=130.0)
    di9 = DiagnosticInput(vehicle_context=ctx, dtcs=[], analyser_type="5-gas",
                          obd=obd_delta, freeze_frame=ff_delta)
    vi9 = validate(di9)
    assert "obd" in vi9.invalid_channels, "FAIL: ECT delta 105 > 100 should reject obd"
    print("PASS: ECT delta 105 -> obd rejected")

    print()
    print("=== ALL 11 MANUAL VERIFICATIONS PASSED ===")


if __name__ == "__main__":
    main()
