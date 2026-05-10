"""Smoke test for pipeline.py — end-to-end diagnose() call."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine.v2.input_model import (
    DiagnosticInput,
    GasRecord,
    OBDRecord,
    VehicleContext,
)
from engine.v2.pipeline import diagnose


def main() -> None:
    # Vacuum leak profile: lean at idle (lambda 1.08), trims positive,
    # DTC P0171 (System Too Lean Bank 1), warm closed-loop.
    vc = VehicleContext(
        brand="Toyota",
        model="Camry",
        engine_code="2AZ-FE",
        displacement_cc=2362,
        my=2005,
    )
    gas_idle = GasRecord(
        co_pct=0.05,
        hc_ppm=45,
        co2_pct=14.5,
        o2_pct=1.2,
        nox_ppm=120,
        lambda_analyser=1.080,
    )
    gas_high = GasRecord(
        co_pct=0.03,
        hc_ppm=35,
        co2_pct=14.8,
        o2_pct=0.8,
        nox_ppm=200,
        lambda_analyser=1.045,
    )
    obd = OBDRecord(
        stft_b1=18.0,
        ltft_b1=22.0,
        map_kpa=35.0,
        maf_gs=3.2,
        rpm=750,
        ect_c=92.0,
        iat_c=35.0,
        fuel_status="CL",
        o2_voltage_b1=0.15,
        o2_voltage_b2=0.20,
        obd_lambda=1.06,
        baro_kpa=101.0,
        load_pct=22.0,
        tps_pct=3.0,
    )

    di = DiagnosticInput(
        vehicle_context=vc,
        dtcs=["P0171"],
        analyser_type="5-gas",
        gas_idle=gas_idle,
        gas_high=gas_high,
        obd=obd,
    )
    result = diagnose(di)

    print("R9 keys present:", all(
        k in result
        for k in (
            "state", "primary", "alternatives", "perception_gap",
            "validation_warnings", "cascading_consequences",
            "confidence_ceiling", "next_steps",
        )
    ))
    print("state:", result["state"])
    print("primary:", result["primary"]["fault_id"] if result["primary"] else None)
    if result["primary"]:
        print("  raw_score:", round(result["primary"]["raw_score"], 4))
        print("  confidence:", round(result["primary"]["confidence"], 4))
    print("confidence_ceiling:", result["confidence_ceiling"])
    print("alternatives:", len(result["alternatives"]))
    print("validation_warnings:", len(result["validation_warnings"]))

    assert result["state"] in ("named_fault", "insufficient_evidence"), (
        f"Unexpected state: {result['state']}"
    )
    assert all(
        k in result
        for k in (
            "state", "primary", "alternatives", "perception_gap",
            "validation_warnings", "cascading_consequences",
            "confidence_ceiling", "next_steps",
        )
    ), "R9 keys incomplete"
    assert result["confidence_ceiling"] > 0, "confidence_ceiling must be > 0"

    print(f"\nSmoke test PASSED — state={result['state']}")


if __name__ == "__main__":
    main()
