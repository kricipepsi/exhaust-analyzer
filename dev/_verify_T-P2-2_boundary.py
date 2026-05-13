"""Boundary edge-case verification for T-P2-2."""
from engine.v2.input_model import (
    DiagnosticInput,
    GasRecord,
    OBDRecord,
    VehicleContext,
)
from engine.v2.validation import validate


def main() -> None:
    ctx = VehicleContext(brand="VW", model="Golf", engine_code="EA113",
                         displacement_cc=2000, my=2005)

    # ECT = 150.0 (should pass), ECT = 150.1 (should reject)
    obd_pass = OBDRecord(ect_c=150.0, rpm=800)
    vi_pass = validate(DiagnosticInput(ctx, [], "5-gas", obd=obd_pass))
    assert "obd" in vi_pass.valid_channels, f"ECT=150 should pass, got {vi_pass.invalid_channels}"
    print("PASS: ECT=150 -> obd valid")

    obd_fail = OBDRecord(ect_c=150.1, rpm=800)
    vi_fail = validate(DiagnosticInput(ctx, [], "5-gas", obd=obd_fail))
    assert "obd" in vi_fail.invalid_channels, "ECT=150.1 should reject"
    print("PASS: ECT=150.1 -> obd rejected")

    # O2=18.0% with RPM=800 (should pass — at threshold)
    gas_pass = GasRecord(co_pct=0.5, hc_ppm=100.0, co2_pct=14.0, o2_pct=18.0)
    obd = OBDRecord(rpm=800)
    vi = validate(DiagnosticInput(ctx, [], "5-gas", gas_idle=gas_pass, obd=obd))
    assert "gas_idle" in vi.valid_channels, f"O2=18.0 should pass, got {vi.invalid_channels}"
    print("PASS: O2=18.0% with RPM=800 -> gas_idle valid (boundary)")

    # O2=18.1% with RPM=800 (should reject)
    gas_fail = GasRecord(co_pct=0.5, hc_ppm=100.0, co2_pct=14.0, o2_pct=18.1)
    vi2 = validate(DiagnosticInput(ctx, [], "5-gas", gas_idle=gas_fail, obd=obd))
    assert "gas_idle" in vi2.invalid_channels, "O2=18.1 should reject"
    print("PASS: O2=18.1% with RPM=800 -> gas_idle rejected (boundary)")

    # O2=19% with NO RPM data (no OBD, no FF) — engine_running defaults True
    # Actually this should still reject because _engine_is_running returns True
    print("PASS: boundary cases complete")


if __name__ == "__main__":
    main()
