"""Reconstruction CONFIG for the petrol-engine-timings (1990-2010) source doc.
Archetype B (wall-of-text + box-drawing). Table blobs are sliced by anchor from
the prepped baseline so they match byte-for-byte (no hand-copy drift)."""
from pathlib import Path

SRC = Path(
    "/sessions/zealous-happy-johnson/mnt/4DLab/docs/GASLab/q1&7/"
    "Advanced Engineering Analysis of Petrol Engine Timings (1990–2010)_prepped.md"
).read_text(encoding="utf-8")


def _blob(start: str, end: str) -> str:
    i = SRC.index(start)
    j = SRC.index(end, i)
    return SRC[i:j]


GAS_BLOB = _blob("Timing StateOperating ModeHC (ppm)", "Over-Advanced Ignition Timing Dynamics")
FF_BLOB = _blob("ParameterObserved ValueNormal BaselineDiagnostic ImplicationTriggered DTC",
                "This freeze frame profile shows")
PID_BLOB = _blob("OBD ParameterNormal Baseline (Low Idle)",
                 "Comparative System Diagnostics: Retarded Cam Timing")

GAS_MD = """

<!-- TABLE: timing_5gas_signatures -->
| Timing State | Operating Mode | HC (ppm) | CO (%) | CO2 (%) | O2 (%) | NOx (ppm) | Lambda |
|---|---|---|---|---|---|---|---|
| Normal Stoichiometric Baseline | Low Idle (750 RPM) | < 50 | < 0.10 | 14.0 - 15.5 | < 0.50 | 0 - 15 | 0.99 - 1.01 |
| Normal Stoichiometric Baseline | High Idle (2500 RPM) | < 30 | < 0.10 | 14.5 - 16.0 | < 0.30 | 50 - 150 | 0.99 - 1.01 |
| Over-Advanced Ignition Timing | Low Idle (750 RPM) | 120 - 250 | 0.10 - 0.30 | 11.5 - 13.0 | 0.80 - 1.50 | 20 - 60 | 1.01 - 1.04 |
| Over-Advanced Ignition Timing | High Idle (2500 RPM) | 150 - 400 | 0.15 - 0.40 | 10.5 - 12.5 | 1.00 - 2.00 | 1200 - 3000+ | 1.02 - 1.06 |
| Retarded Ignition Timing | Low Idle (750 RPM) | 300 - 800 | 0.05 - 0.15 | 8.5 - 11.0 | 1.50 - 3.50 | 0 - 5 | 1.05 - 1.15 |
| Retarded Ignition Timing | High Idle (2500 RPM) | 250 - 600 | 0.05 - 0.15 | 9.0 - 11.5 | 1.20 - 3.00 | 10 - 50 | 1.04 - 1.12 |
| Retarded Cam Timing (Speed Density) | Low Idle (750 RPM) | 400 - 1200 | 3.50 - 7.00 | 8.0 - 10.5 | < 0.50 | 0 - 10 | 0.75 - 0.88 |
| Retarded Cam Timing (Speed Density) | High Idle (2500 RPM) | 200 - 600 | 1.50 - 4.50 | 11.0 - 13.0 | < 0.50 | 100 - 400 | 0.85 - 0.95 |
| Retarded Cam Timing (MAF System) | Low Idle (750 RPM) | 300 - 900 | 0.10 - 0.50 | 9.0 - 11.5 | 2.00 - 4.50 | 0 - 15 | 1.08 - 1.18 |
| Retarded Cam Timing (MAF System) | High Idle (2500 RPM) | 150 - 400 | 0.10 - 0.30 | 11.5 - 13.5 | 1.00 - 2.50 | 150 - 500 | 1.03 - 1.09 |
| Advanced Cam Timing (Both Systems) | Low Idle (750 RPM) | 250 - 600 | 0.20 - 0.80 | 10.0 - 12.5 | 1.20 - 2.50 | 10 - 40 | 1.03 - 1.08 |
| Advanced Cam Timing (Both Systems) | High Idle (2500 RPM) | 100 - 300 | 0.15 - 0.50 | 12.0 - 14.0 | 0.80 - 1.80 | 300 - 900 | 1.01 - 1.05 |

"""

FF_MD = """

<!-- TABLE: freeze_frame_p0016 -->
Triggered DTC: P0016 (Crankshaft-Camshaft Correlation fault on Bank 1).

| Parameter | Observed Value | Normal Baseline | Diagnostic Implication |
|---|---|---|---|
| Engine Speed (RPM) | 720 RPM | 700 - 800 RPM | Standard low idle condition |
| Calculated Load (%) | 42.5% | 15% - 25% | Elevated load calculation due to low manifold vacuum |
| Manifold Absolute Pressure | 54.0 kPa | 30 - 35 kPa | Abnormally high manifold pressure (low vacuum) |
| Mass Air Flow | 2.1 g/s | 3.5 - 4.5 g/s | Reduced physical air intake due to pumping loss |
| Short-Term Fuel Trim (STFT) | -14.2% | +/- 3% | Active subtraction of fuel due to rich bias |
| Long-Term Fuel Trim (LTFT) | -18.5% | +/- 5% | Learned subtraction of fuel in memory |
| Total Fuel Trim | -32.7% | +/- 5% | Extreme rich correction under Speed Density logic |
| Engine Coolant Temp (ECT) | 194F (90C) | 185F - 210F | Fully warmed operating temperature |
| Fuel System Status | Closed Loop | Closed Loop | Active closed-loop feedback control |

"""

PID_MD = """

<!-- TABLE: pid_transient_stress_idle -->
| OBD Parameter | Normal (Low Idle) | Normal Stress Idle (3800 RPM) | Jumped Tooth (Low Idle / Speed Density) | Jumped Tooth (Stress Idle / Speed Density) | Jumped Tooth (Low Idle / MAF) | Jumped Tooth (Stress Idle / MAF) |
|---|---|---|---|---|---|---|
| Engine Speed (RPM) | 700 - 800 | 3500 - 4000 | 650 - 750 | 3500 - 4000 | 750 - 850 (Rough) | 3500 - 4000 |
| MAP (kPa / in-Hg) | 30 - 35 / 20.6 | 22 - 28 / 22.4 | 50 - 65 / 14.7 | 35 - 45 / 19.2 | 45 - 55 / 16.2 | 30 - 38 / 20.0 |
| MAF (g/s) | 2.0 - 4.5 | 12.0 - 18.0 | 3.5 - 5.5 | 16.0 - 24.0 | 1.5 - 3.0 | 8.0 - 12.0 |
| O2 Sensor (NB / WB) | 0.1 - 0.9 V / lambda ~ 1.0 | 0.1 - 0.9 V / lambda ~ 1.0 | Stuck Rich > 0.85 V / lambda ~ 0.82 | Stuck Rich > 0.80 V / lambda ~ 0.88 | Lean Bias < 0.20 V / lambda ~ 1.12 | Lean Bias < 0.35 V / lambda ~ 1.06 |
| STFT (%) | Oscillating +/- 3% | Oscillating +/- 2% | -15% to -25% | -10% to -15% | +10% to +20% | +5% to +12% |
| LTFT (%) | -5% to +5% | -5% to +5% | -12% to -20% | -8% to -12% | +12% to +22% | +8% to +15% |
| Total Fuel Trim (%) | -5% to +5% | -5% to +5% | -27% to -45% | -18% to -27% | +22% to +42% | +13% to +27% |

"""

FLOWCHART_MD = """

```mermaid
graph TD
  A[Timing fault suspected] --> B{DTC family present?}
  B -->|Crank-Cam correlation P0016-P0019| C[Probe CKP and CMP sensors]
  B -->|Misfires or fuel-trim faults| D[Monitor MAP, MAF, Total Fuel Trim]
  C --> C1{MAP at idle?}
  C1 -->|Normal MAP 30-35 kPa| C2[Check VVT actuators; verify oil pressure; monitor phaser response]
  C1 -->|High MAP 50-65 kPa| C3[Replace stretched chain/belt; check Mode 06 MIDs]
  D --> D1[Compare low idle vs 2500 RPM]
  D1 -->|Speed Density: rich, high CO| D2[Target mechanical timing / pumping loss]
  D1 -->|MAF: lean, high O2| D2
  D2 --> E[Install transducer in isolated cylinder; analyse EVO, IVO, IVC phasing]
  E -->|Delayed IVO = vacuum pull ATDC; delayed EVO = exhaust-stroke pressure rise| F[Reset timing chain/belt alignment; replace failed tensioners/guides]
```

"""

CONFIG = {
    "headings": [
        (1, "Advanced Engineering Analysis of Petrol Engine Timings (1990–2010): Thermodynamic Signatures, Diagnostic Protocols, and OBD-II PID Dynamics"),
        (2, "Thermodynamic and Mechanical Foundations of Petrol Engine Timings"),
        (3, "The Evolution of Ignition Timing and the Spark Curve"),
        (3, "Mechanical Synchronization and Camshaft Desynchronization"),
        (3, "Hydraulic Variable Valve Timing"),
        (3, "Mathematical Diagnostics of Cylinder Pressure"),
        (2, "Exhaust Gas and Lambda Signatures (Low Idle vs. High Idle)"),
        (3, "Over-Advanced Ignition Timing Dynamics"),
        (3, "Retarded Ignition Timing Dynamics"),
        (3, "Retarded Cam/Valve Timing Dynamics"),
        (3, "Advanced Cam/Valve Timing Dynamics"),
        (2, "On-Board Diagnostics: DTC, Freeze Frame, and Mode $06 Protocols"),
        (3, "Diagnostic Trouble Code (DTC) Generation"),
        (3, "Freeze Frame Architecture"),
        (3, "OBD-II Mode $06 Systems Evolution"),
        (3, "Pre-CAN (1996–2002) vs. CAN (2003–2010) Implementations"),
        (3, "Predictive Diagnostics via Mode $06 Misfire and VVT Testing"),
        (2, "OBD PID Dynamics under Transient and Stress Idle Conditions"),
        (3, "Comparative System Diagnostics: Retarded Cam Timing"),
        (2, "In-Cylinder Pressure Diagnostics"),
        (3, "Exhaust Valve Opening (EVO)"),
        (3, "Intake Valve Opening (IVO) and Intake Valve Closing (IVC)"),
        (2, "Advanced Engineering Diagnostics and Conclusions"),
        (3, "Diagnostic Flowchart: Isolating Timing Failures"),
        (3, "Analytical Diagnostic Protocols"),
    ],
    "table_replacements": [
        (GAS_BLOB, GAS_MD),
        (FF_BLOB, FF_MD),
        (PID_BLOB, PID_MD),
    ],
    "box_drawing_replacements": [
        ("│", "Replace Failed Tensioners/Guides", FLOWCHART_MD),
    ],
    "sec2_anchor": "To isolate true engine timing issues",
    "promote_headings_regex": None,
}
