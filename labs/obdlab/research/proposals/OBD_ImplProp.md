To diagnose the internal ECU hardware failures using live OBD PID measurements at both low idle ($700\text{–}800\text{ RPM}$) and stress idle ($3500\text{–}4500\text{ RPM}$), the `obdlab` software module must be systematically configured and compiled `[1]`.

By structuring the module's static configurations, core diagnostic pipelines, semantic checkers, and compilation/deployment routines, you can isolate internal solid-state control module failures from standard mechanical or sensor faults `[1]`.

---

## 1. Static Configuration Setup (`config/`)

The module relies on two static configuration files that must be custom-tailored to handle the extreme electrical drift caused by ECU internal hardware failures without triggering premature pipeline crashes `[1]`.

### A. Physical Sensor Bounds Configuration (`config/physical_sensor_bounds.json`)

The ingestion validator (`PIDIngestionValidator`) reads this file at startup `[1]`. It must be configured with broad sensor thresholds `[1]`. If these bounds are set too tight, a floated sensor reading (like a $-40\text{ }^\circ\text{C}$ coolant temperature caused by a blown ground trace) would fail validation at ingestion, preventing the diagnostic engine from analyzing the data pattern ``.

Configure the bounds as follows:

* **`engine_rpm`**: Range of $0$ to $8000\text{ RPM}$ to accommodate both low idle ($700\text{–}800\text{ RPM}$) and high stress idle ($3500\text{–}4500\text{ RPM}$) `[1]`.
* **`coolant_temp_c`**: Range of $-40\text{ }^\circ\text{C}$ to $130\text{ }^\circ\text{C}$ `[1]`. This is critical to capture the floating reference ground trace failure, which pulls the temperature down to $-40\text{ }^\circ\text{C}$ ``.
* **`throttle_pos_pct`**: Range of $0\%$ to $100\%$ `[1]`.
* **`map_kpa`**: Range of $10\text{ kPa}$ to $120\text{ kPa}$ `[1]`.
* **`maf_gps`**: Range of $0\text{ g/s}$ to $300\text{ g/s}$ `[1]`.
* **`shrtft1`, `longft1`, `shrtft2`, `longft2**`: Range of $-100\%$ to $+100\%$ (clamped at the absolute software logic limit of $[-127, 127]$ inside the checker) `[1]`.

### B. State Translation Rules (`config/obd_translation_rules.yaml`)

This file defines the operating conditions analyzed by the state-bucketing machine `[1]`.

* **`STABILIZED_IDLE`**: Defined using a `BETWEEN` operator for engine speeds of $650\text{–}850\text{ RPM}$ `[1]`.
* **`STRESS_IDLE`**: Defined using a `BETWEEN` operator for engine speeds of $3500\text{–}4500\text{ RPM}$ `[1]`.
* **`COLD_OPEN_LOOP_INVALID`**: A fallback state triggered if coolant temperature is below $75\text{ }^\circ\text{C}$ `[1]`.

---

## 2. Configuring the Core Processing Pipeline

Once data passes ingestion, the core logical modules must be configured to identify the diagnostic signatures of the five target failures `[1]`.

### A. Volumetric Efficiency (VE) Engine Gating (`core/ve_engine.py`)

The `VEEngine` calculates the engine’s volumetric efficiency `[1]`. Under normal operating conditions, a naturally aspirated engine exhibits a VE of $75\text{–}90\%$ ``. Internal ECU failures cause severe sensor discrepancies that distort the physical VE calculation, which is resolved via:

$$\text{VE} = \frac{\text{maf} \times R_{\text{GAS}} \times \text{IAT}_K}{\text{map\_kpa} \times \left(\frac{\text{rpm}}{60}\right) \times \left(\frac{\text{displacement}}{2}\right) \times \text{MM\_AIR}} \times 100$$



Configure the VE classifier (`_classify_validity`) to flag these specific faults `[1]`:

1. **`FAULT_VE_IDLE_COLLAPSE` (Flags Blown Grounds & Collapsed 5V Regulator)**:
* *Trigger*: Calculated VE drops below $50\%$ while idling, accompanied by a MAP reading $> 45\text{ kPa}$ `[1]`.
* *ECU Failure Match*: If the internal $5\text{ V}$ regulator collapses, MAP and MAF signals flatline near $0\text{ V}$, lowering the numerator `[2, 3, 1]`. If the sensor ground trace blows, the TPS floats to $100\%$ and MAP floats to atmospheric pressure, inflating the denominator while the engine is physically at idle, causing a massive math collapse ``.


2. **`FAULT_VE_SENSOR_SKEW` (Flags Capacitor Leakage)**:
* *Trigger*: Calculated VE $> 90\%$ under naturally aspirated idle conditions `[1]`.
* *ECU Failure Match*: Board-level electrolyte leakage superimposes an AC ripple on sensor reference lines, causing MAP and MAF inputs to spike and fluctuate, pushing the calculated VE to unrealistic levels for an idling engine `[1]`.



### B. O2 Sensor Normalization & Trim Aggregation (`core/o2_normalizer.py` & `trim_vector_aggregator.py`)

To isolate bank-specific driver failures, configure the `TrimVectorAggregator` to execute asymmetric bank audits `[1]`.

* **Asymmetric Bank Gating**:
* *Bank 1 Total Trim* = $\text{STFT B1} + \text{LTFT B1}$ `[1]`
* *Bank 2 Total Trim* = $\text{STFT B2} + \text{LTFT B2}$ `[1]`
* If a dual-bank configuration is declared in the engine’s DNA (`number_of_banks == 2`), but the total trim difference between banks $|\text{Total B1} - \text{Total B2}| \ge 20\%$, the pipeline isolates a bank-specific hardware fault `[1, 4]`.
* *Injector Driver Failed Open (Bank 1)*: Bank 1 total trim spikes to $+50\%$ (maximum limit), while Bank 2 total trim remains normal ($0\text{–}3\%$) `[1]`.
* *Injector Driver Shorted (Bank 1)*: Bank 1 total trim pegs at $-50\%$, while Bank 2 total trim remains normal `[1]`.



### C. Semantic Consistency Gating (`core/semantic_consistency_checker.py`)

The `SemanticConsistencyChecker` ensures the data obeys physical and thermodynamic principles `[1]`. This is the primary module for detecting a **Vaporized/Blown Internal Sensor Ground Trace** ``.

Configure the following diagnostic gates:

* **Physics Gate 2 (Blown Ground Trace Detection)**:
* *Logic*: If the engine is physically warm (coolant temperature $\ge 80\text{ }^\circ\text{C}$ as verified by a manual check or infrared thermometer) but the ingested OBD `fuel_status` is locked in `Open_Loop_Cold` and the `coolant_temp_c` PID reads $-40\text{ }^\circ\text{C}$ (or equivalent floating minimum), raise a `SemanticConsistencyError` ``.
* *Diagnostic Action*: This specific exception is mapped as the definitive signature of a vaporized internal sensor ground trace, separating it from a simple failed thermostat or bad sensor element ``.


* **Physics Gate 4 (Trim Saturation Control)**:
* *Logic*: If computed total trim corrections exceed the physical storage parameters of $[-127, 127]$, throw a `ValueError` `[1]`.



### D. Analytics Preconditions Evaluation (`core/analytics_preconditions.py`)

The module evaluates preconditions sequentially `[1]`. For diagnosing ECU failures, you must capture the **failure reasons** returned by this module:

1. If the ground trace is blown, the floating ECT voltage reads $-40\text{ }^\circ\text{C}$, causing the gate to stop at **Gate 1** and return `ENGINE_COLD` ``.
2. If the capacitor leakage forces the ECU to default to an open-loop fault mode, the gate stops at **Gate 2** and returns `OPEN_LOOP` `[1]`.
3. These returned failure reasons serve as diagnostic markers for board-level failures `[1]`.

---

To expand your diagnostic framework and build a robust, production-grade diagnostic bridge, you must integrate these ten traditional external engine fault families into the diagnostic pipeline.

By analyzing how these physical faults manifest in On-Board Diagnostics (OBD) Parameter IDs (PIDs) at both low idle (700-800 RPM) and high-stress idle (3500-4500 RPM), we can establish how they differ fundamentally from internal Engine Control Unit (ECU) hardware failures.

---

## 1. The Core Paradigm: Semantic Coherence vs. Digital Divergence

To programmatically classify these faults, the diagnostics engine must evaluate the **Semantic Coherence** of the incoming data.

* **Traditional External Faults (Semantically Coherent):** Standard physical faults (such as vacuum leaks, mechanical wear, or catalyst degradation) represent real thermodynamic or chemical shifts. The engine's sensors accurately measure these changes and report them to the ECU. The resulting OBD-II PIDs follow the laws of physics. For example, a physical vacuum leak introduces unmetered air. The upstream O2 sensor detects the resulting excess oxygen and drops in voltage. The ECU calculates a positive fuel trim to inject more fuel and restore stoichiometry. Both the OBD datastream and the physical tailpipe emissions reflect this corrective action.
* **ECU Internal Hardware Failures (Semantically Incoherent / Digital Lies):** Internal solid-state failures corrupt the measurement or calculation medium itself. The microprocessor receives incorrect inputs due to a physical board-level failure (such as an analog-to-digital converter multiplexer failure  or a vaporized sensor ground trace ). This breaks the closed-loop control loop. The OBD PIDs report a false state (e.g., a cold-start state of -40 degrees Celsius or a wide-open throttle condition ), while a physical five-gas analyzer reveals a completely contradictory tailpipe signature (such as a heavily rich mixture).



---

## 2. Characterization of the Ten Traditional External Fault Families

### A. Lean Conditions (Vacuum Leaks vs. Fuel Delivery Restrictions)

* **Vacuum Leaks (Intake Manifold Gasket, Torn Inlet Boot, Cracked PCV Elbow):**
* *Low Idle (700-800 RPM):* Manifold vacuum is high. Unmetered air entering through the leak represents a large percentage of the total intake air charge. The upstream O2 sensor pegs low. The ECU applies highly positive fuel trims (STFT + LTFT > +20%) to compensate.
* *Stress Idle (3500-4500 RPM):* The throttle plate opens significantly. The massive volume of metered air rushing through the throttle body makes the unmetered leak rate negligible. Fuel trims return to normal limits (+5% to -5%).


* **Fuel Delivery Restrictions (Weak Fuel Pump, Clogged Filter, Restricted Injector):**
* *Low Idle (700-800 RPM):* Fuel volume demand is minimal. Even a weak pump can maintain the target rail pressure. Fuel trims remain normal.
* *Stress Idle (3500-4500 RPM):* High engine speed demands significant fuel volume. The restricted fuel system cannot maintain flow. The engine runs lean under load. Upstream O2 sensors drop low. Fuel trims spike to positive maximums (+25%) and stay there, failing to recover.



### B. Rich Mixtures (Stuck Open EVAP Purge, Leaking Pressure Regulator, Dripping Injector)

* *Low Idle (700-800 RPM):* Extra fuel vapor drawn from a stuck-open EVAP purge valve or a leaking fuel pressure regulator diaphragm is drawn directly into the high-vacuum intake manifold. This fuel represents a significant percentage of the total idle fuel requirement. The ECU commands highly negative trims (STFT + LTFT < -20%) to lean out the mixture.
* *Stress Idle (3500-4500 RPM):* As the throttle opens and engine speed increases, the constant leak volume is diluted by the massive increase in metered fuel and air. The fuel trims return toward normal.

### C. Misfires (Mechanical vs. External Ignition vs. Fuel-Related)

* *Low Idle (700-800 RPM):* A dead cylinder (due to a bad spark plug or a clogged injector) fails to burn its air-fuel charge. It pumps unburned fuel and atmospheric oxygen directly into the exhaust manifold. The upstream O2 sensor detects this oxygen and pegs low. The ECU increases fuel trims on that bank, causing the remaining healthy cylinders to run rich. Manifold vacuum is unstable, causing MAP to fluctuate slightly.


* *Stress Idle (3500-4500 RPM):* Under high engine speed, the raw hydrocarbon and oxygen molecules pass into the catalytic converter. An intense exothermic reaction occurs. If the misfire is ignition-related, the misfire count PID rises on that specific cylinder. If it is a mechanical valve-sealing issue, the misfire persists or worsens under load.



### D. Sensor Faults (Contaminated MAF, Sluggish O2 Sensors)

* **Contaminated MAF Sensor:**
* *Low Idle (700-800 RPM):* Dirt or oil on the hot-wire element insulates it. It under-reports airflow. The ECU commands less fuel than required. The engine runs lean, and trims are moderately positive (+10% to +15%).
* *Stress Idle (3500-4500 RPM):* The under-reporting gets progressively worse as the volume of air increases. On a snap-throttle or steady high-RPM run, the MAF voltage fails to reach its expected peak (>4.0V). The J1979 Calculated Load (LOAD_PCT) remains abnormally low (<70% at wide-open throttle). Fuel trims remain highly positive.


* **Sluggish/Degraded Upstream O2 Sensor:**
* The sensor's switching frequency between 0.1V and 0.9V drops from several times per second to once every few seconds. It is slow to respond to induced rich or lean conditions. Fuel trims fluctuate in slow, high-amplitude waves rather than tight, rapid adjustments.



### E. Catalyst Failures (P0420/P0430 Efficiency Below Threshold)

* *Low Idle (700-800 RPM):* The upstream O2 sensor switches rapidly between 0.1V and 0.9V. Because the catalyst has lost its oxygen storage capacity, the downstream O2 sensor mimics this switching pattern directly, oscillating in-phase with the upstream sensor rather than remaining stable at 0.45-0.65V.
* *Stress Idle (3500-4500 RPM):* High exhaust gas velocity further highlights the catalyst's inability to store oxygen. The downstream sensor mirrors the upstream oscillations. Fuel trims and Calculated Load remain completely unaffected.

### F. Exhaust Leaks Upstream of O2 Sensors

* *Low Idle (700-800 RPM):* The low velocity of the exhaust pulses creates a venturi effect at the leak point. It draws outside air (oxygen) into the exhaust stream before it reaches the O2 sensor. The O2 sensor reports a false lean condition (<0.1V). The ECU commands positive fuel trims (+15% to +20%).
* *Stress Idle (3500-4500 RPM):* The high volume and pressure of the exhaust gases force exhaust out of the leak, stopping outside air from entering. The O2 sensor begins reading the actual combustion mixture, and the fuel trims quickly return to normal.

### G. Ignition Faults (Worn Plugs, Cracked Boots, Weak Coil Insulation)

* *Low Idle (700-800 RPM):* Cylinder pressure is low, making it easy for the spark plug to fire. The engine may run smoothly with normal trims.


* *Stress Idle (3500-4500 RPM):* Rapidly rising cylinder pressures under load place a high electrical demand on the secondary ignition circuit. The spark energy jumps through cracked boots or weak coil insulation to the engine block instead of firing the plug. This causes immediate, load-dependent misfires, positive trims, and a spike in raw hydrocarbons (HC).



### H. Mechanical Wear (Low Compression, Worn Valves, Rings)

* *Low Idle (700-800 RPM):* Poor cylinder sealing reduces intake vacuum. Manifold Absolute Pressure (MAP) is elevated (40-50 kPa vs. 25-30 kPa normal). Calculated Load is elevated at idle. Manifold vacuum is unstable, and the vacuum needle fluctuates.
* *Stress Idle (3500-4500 RPM):* Dynamic engine momentum partially compensates for the sealing loss, but volumetric efficiency (VE) and maximum power are limited. The Calculated Load fails to scale smoothly with engine speed and throttle angle.

### I. Camshaft Timing Retarded and Advanced

* **Retarded Cam Timing (Slipped Belt/Chain, Slipped Cam Phaser):**
* *Low Idle (700-800 RPM):* Late intake valve closing reduces idle compression and manifold vacuum. MAP is elevated (45-55 kPa). The engine runs rough. Calculated Load is elevated.
* *Stress Idle (3500-4500 RPM):* As RPM increases, late valve closing helps cylinder filling. Volumetric efficiency improves, and the engine's performance partially recovers at higher speeds.


* **Advanced Cam Timing:**
* *Low Idle (700-800 RPM):* Early valve closing maintains high idle vacuum (MAP is normal or low, 22-26 kPa).
* *Stress Idle (3500-4500 RPM):* Early valve closing restricts breathing at high RPM, dropping volumetric efficiency and engine power significantly. Calculated Load drops at higher engine speeds.



### J. Ignition Timing Retarded and Advanced

* **Retarded Ignition Timing:**
* *Low Idle (700-800 RPM):* Late combustion reduces idle efficiency. The throttle plate must open wider to maintain idle speed. Manifold vacuum drops (MAP is elevated to 35-42 kPa). Exhaust gas temperatures rise significantly.
* *Stress Idle (3500-4500 RPM):* Power output is low. Calculated Load is elevated for a given throttle angle. Fuel trims remain normal if no misfires occur.


* **Advanced Ignition Timing:**
* *Low Idle (700-800 RPM):* Early spark increases cylinder pressure before Top Dead Center (TDC). Idle vacuum is high (MAP is low). The engine may exhibit a sharp, metallic pinging sound (detonation).
* *Stress Idle (3500-4500 RPM):* Severe detonation occurs under load. The knock sensor (if equipped) registers high activity, prompting the ECU to retard timing.



---

## 3. High-Density Comparative Diagnostic Matrix

The following table uses single-space formatting to map these external faults against your primary OBD PIDs.

| Fault Family | Operating State | LOAD_PCT (%) | STFT B1 (%) | LTFT B1 (%) | MAP (kPa) / MAF (g/s) | Upstream O2 | Downstream O2 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **1. Vacuum Leak** | Low Idle | 15-20 | +15 to +25 | +15 to +20 | Elevated MAP / Low MAF | Pegged Lean (<0.15V) | Pegged Lean (<0.15V) |
|  | Stress Idle | 10-12 | -3 to +3 | 0 to +5 | Normal scaling | Switching (0.1-0.9V) | Stable (0.45-0.65V) |
| **2. Restricted Fuel** | Low Idle | 18-22 | 0 to +5 | 0 to +5 | Normal | Switching (0.1-0.9V) | Stable (0.45-0.65V) |
|  | Stress Idle | 8-10 | +20 to +25 | +20 to +25 | Under-reports under load | Pegged Lean (<0.1V) | Pegged Lean (<0.1V) |
| **3. Stuck-Open Purge** | Low Idle | 25-30 | -15 to -25 | -15 to -20 | Normal to High MAP | Pegged Rich (>0.85V) | Pegged Rich (>0.8V) |
|  | Stress Idle | 12-15 | -5 to +2 | 0 to -5 | Normal scaling | Switching (0.1-0.9V) | Stable (0.45-0.65V) |
| **4. Contaminated MAF** | Low Idle | 8-12 | +8 to +15 | +10 to +15 | Artificially Low MAF | Lean Bias (<0.3V) | Lean Bias (<0.2V) |
|  | Stress Idle | <65 (WOT) | +20 to +25 | +20 to +25 | Low peak MAF at high RPM | Pegged Lean (<0.15V) | Pegged Lean (<0.15V) |
| **5. Catalyst Failure** | Low Idle | 18-22 | -5 to +5 | -5 to +5 | Normal | Switching (0.1-0.9V) | Switching (0.1-0.9V) |
|  | Stress Idle | 10-12 | -3 to +3 | -3 to +3 | Normal scaling | Switching (0.1-0.9V) | Switching (0.1-0.9V) |
| **6. Exhaust Leak** | Low Idle | 18-22 | +12 to +20 | +10 to +15 | Normal | False Lean (<0.2V) | Pegged Lean (<0.15V) |
|  | Stress Idle | 10-12 | -3 to +3 | 0 to +5 | Normal scaling | Switching (0.1-0.9V) | Stable (0.45-0.65V) |
| **7. Ignition Fault** 

 | Low Idle | 18-22 | 0 to +5 | 0 to +5 | Normal | Switching (0.1-0.9V) | Stable (0.45-0.65V) |
|  | Stress Idle | 12-15 | +10 to +20 | +5 to +15 | Normal scaling | Erratic Lean Drops | Fluctuating (0.2-0.7V) |
| **8. Mechanical Wear** | Low Idle | 25-35 | -5 to +5 | -5 to +5 | Elevated MAP (40-50 kPa) | Switching (Slow) | Stable (0.45-0.65V) |
|  | Stress Idle | 15-20 | -5 to +5 | -5 to +5 | Lower Volumetric Flow | Switching (Slow) | Stable (0.45-0.65V) |
| **9. Retarded Cam** | Low Idle | 28-35 | -3 to +3 | -5 to +5 | Elevated MAP (45-55 kPa) | Switching | Stable (0.45-0.65V) |
|  | Stress Idle | 12-15 | -3 to +3 | -5 to +5 | High-RPM VE matches spec | Switching | Stable (0.45-0.65V) |
| **10. Retarded Spark** | Low Idle | 24-30 | -3 to +3 | -3 to +3 | Elevated MAP (35-42 kPa) | Switching | Stable (0.45-0.65V) |
|  | Stress Idle | 15-18 | -3 to +3 | -3 to +3 | Normal scaling | Switching | Stable (0.45-0.65V) |

---

## 4. Software Architecture Integration: Updating the `obdlab` Module

To incorporate these traditional fault families alongside the solid-state ECU hardware failures, you must add specific logical gates to the core classes of the `obdlab` diagnostic pipeline.

### A. Updating the Volumetric Efficiency (VE) Engine (`core/ve_engine.py`)

Add specific classification states inside the `_classify_validity` function to separate mechanical wear, timing issues, and MAF contamination from internal ECU failures:

```python
def _classify_validity(self, ve_pct, state_bucket, map_kpa, total_trim, tps_pct):
    # 1. Capture ECU Collapsed 5V Rail / Reference Ground Open
    if ve_pct < 50 and state_bucket == "STABILIZED_IDLE" and map_kpa > 45 and tps_pct > 90:
        return "FAULT_ECU_GROUND_TRACE_BLOWN" # Blown ground trace pulls TPS to 100% false WOT
        
    # 2. Capture Traditional Mechanical Wear or Retarded Cam Timing
    if ve_pct < 55 and state_bucket == "STABILIZED_IDLE" and map_kpa > 40 and tps_pct < 10:
        return "FAULT_MECHANICAL_WEAR_OR_CAM_SKEW" # Low idle vacuum with closed throttle
        
    # 3. Capture Traditional MAF Contamination (Under-reporting)
    if ve_pct < 65 and state_bucket in and total_trim > 15:
        return "FAULT_MAF_CONTAMINATION"
        
    # 4. Capture Traditional Vacuum Leaks
    if ve_pct > 90 and state_bucket == "STABILIZED_IDLE" and total_trim > 15:
        return "FAULT_VACUUM_LEAK"
        
    return "VALID"

```

### B. Updating Semantic Consistency Checking (`core/semantic_consistency_checker.py`)

Add logical gates to systematically separate internal ECU failures from sensor and exhaust issues:

```python
def check_fault_separation(self, payload):
    # Gate A: Separating ECU Blown Ground from a simple bad Coolant Temp Sensor (ECT)
    # ECU ground trace failure locks ECT to -40C AND floats TPS to 100% WOT simultaneously
    if payload.coolant_temp_c == -40 and payload.throttle_pos_pct == 100:
         payload.diagnostic_verdict = "ECU_INTERNAL_GROUND_TRACE_BLOWN"
         return payload

    # Gate B: Separating ECU ADC Input Failure from a simple Bad O2 Sensor
    # If O2 sensor voltage back-probed at the harness is switching (0.1V - 0.9V) but 
    # the OBD stream reports a flatline <0.15V, triggering maximum trims:
    if payload.upstream_o2_voltage_obd < 0.15 and payload.total_trim_b1 > 20:
         # Check physical tailpipe lambda (passed via DNA/5-gas channel input)
         if payload.physical_lambda_5_gas < 0.90:
              payload.diagnostic_verdict = "ECU_ADC_MULTIPLEXER_INPUT_FAILURE"
              return payload
         else:
              payload.diagnostic_verdict = "TRADITIONAL_EXTERNAL_LEAN_CONDITION"
              return payload

    # Gate C: Separating a Catalyst Failure from ECU Capacitor Leakage AC Ripple
    # In a pure catalyst failure, fuel trims and calculated loads are completely stable.
    # If the downstream sensor mimics upstream, but trims are balanced:
    if payload.downstream_o2_oscillating and abs(payload.total_trim_b1) < 5:
         payload.diagnostic_verdict = "TRADITIONAL_CATALYST_FAILURE"
         return payload
         
    return payload

```

### C. Updating Analytics Preconditions (`core/analytics_preconditions.py`)

To prevent the diagnostic bridge from halting when encountering a cold-start state that is actually an ECU ground fault, modify the sequential gates:

1. **Gate 1 (ECT Evaluation):** If `coolant_temp_c == -40`, evaluate `throttle_pos_pct`. If the TPS is locked at 100%, bypass the standard cold-start block (`ENGINE_COLD`). Flag the state as `ECU_HARDWARE_FAULT_BYPASS` and pass the execution to the semantic checker to generate the internal ground fault verdict.
2. **Gate 2 (Fuel Status Evaluation):** If the vehicle is in open loop due to a detected fault (`OL_FAULT`) , do not halt the analysis if `ve_engine_status` returns `FAULT_VE_SENSOR_SKEW` or `FAULT_VE_IDLE_COLLAPSE`. These states confirm that the open-loop condition is a direct consequence of board-level hardware damage.

Configuring the diagnostic tool as a static, manual-entry application simplifies the software architecture. It eliminates the need for thread-safe queues, asynchronous data loggers, and real-time noise filters ``.

Instead of processing a continuous stream of data points, a static manual-entry app leverages **side-by-side comparative analysis** `. By requiring the technician to enter exactly two telemetry snapshots—one at Low Idle ($700\text{--}800\text{ RPM}$) and one at Stress Idle ($3500\text{--}4500\text{ RPM}$)—the diagnostic engine can immediately evaluate deterministic rules, calculate absolute deltas, and cross-reference OBD parameters with physical five-gas exhaust values to isolate the root cause `.

---

## 1. Static Manual-Entry Data Schemas

The application’s data layer is represented by three lightweight, immutable Python data classes. These hold the OBD-II Parameter IDs (PIDs) and optional physical 5-gas data for both engine speeds ``.

```python
from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass(frozen=True)
class OBDTelemetricSnapshot:
    engine_rpm: float
    calculated_load: float  # LOAD_PCT (%)
    coolant_temp_c: float   # ECT (Celsius)
    shrtft1: float          # STFT Bank 1 (%)
    longft1: float          # LTFT Bank 1 (%)
    shrtft2: Optional[float] = 0.0  # STFT Bank 2 (%)
    longft2: Optional[float] = 0.0  # LTFT Bank 2 (%)
    map_kpa: Optional[float] = None
    maf_gps: Optional[float] = None
    tps_pct: Optional[float] = None
    upstream_o2_voltage: Optional[float] = None  # Narrowband (0-1V)
    upstream_o2_lambda: Optional[float] = None   # Wideband Lambda (0.7 - 1.3)
    downstream_o2_voltage: Optional[float] = None
    fuel_system_status: Optional[int] = 2       # 2 = Closed Loop, 8 = OL Fault

@dataclass(frozen=True)
class FiveGasSnapshot:
    co2_pct: float     # CO2 (%)
    o2_pct: float      # O2 (%)
    co_pct: float      # CO (%)
    hc_ppm: float      # Hydrocarbons (ppm)
    nox_ppm: float     # Nitrogen Oxides (ppm)
    physical_lambda: float  # Calculated Brettschneider Lambda

```

---

## 2. Deterministic Delta Calculations

With static entry, we can compute direct differences (deltas) between the two operating points. Let $\Delta$ represent the absolute or directional shift from Low Idle to Stress Idle ``:

* **Total Trim Bank 1 ($TFT_{B1}$):**

$$TFT_{B1} = \text{shrtft1} + \text{longft1}$$


* **Total Trim Bank 2 ($TFT_{B2}$):**

$$TFT_{B2} = \text{shrtft2} + \text{longft2}$$


* **Trim Delta ($\Delta TFT_{B1}$):**

$$\Delta TFT_{B1} = TFT_{B1,\text{Low}} - TFT_{B1,\text{Stress}}$$


* **Load Delta ($\Delta LOAD$):**

$$\Delta LOAD = LOAD_{\text{Stress}} - LOAD_{\text{Low}}$$





* **Physical Exhaust Delta ($\Delta\lambda_{\text{Exhaust}}$):**

$$\Delta\lambda_{\text{Exhaust}} = \lambda_{\text{Exhaust},\text{Stress}} - \lambda_{\text{Exhaust},\text{Low}}$$






---

## 3. The Forensic Diagnostic Engine

The static classifier below runs sequentially. It evaluates the "lies vs. truth" structural divergence (comparing OBD data to physical 5-gas values) to isolate the 10 ECU hardware failures and 10 traditional external engine faults ``.

```python
class ForensicDiagnosticEngine:
    def __init__(self, displacement_liters: float):
        self.displacement = displacement_liters

    def diagnose(self, 
                 low_obd: OBDTelemetricSnapshot, 
                 low_gas: Optional,
                 stress_obd: OBDTelemetricSnapshot,
                 stress_gas: Optional) -> Dict[str, Any]:
        
        # 1. Standard Aggregations & Deltas
        tft1_low = low_obd.shrtft1 + low_obd.longft1
        tft1_stress = stress_obd.shrtft1 + stress_obd.longft1
        delta_tft1 = tft1_low - tft1_stress
        
        tft2_low = (low_obd.shrtft2 + low_obd.longft2) if low_obd.shrtft2 else 0.0
        tft2_stress = (stress_obd.shrtft2 + stress_obd.longft2) if stress_obd.shrtft2 else 0.0
        
        # Delta Load and Delta RPM
        delta_load = stress_obd.calculated_load - low_obd.calculated_load
        
        # -------------------------------------------------------------
        # FAULT 1: ECU BLOWN SENSOR GROUND TRACE
        # -------------------------------------------------------------
        # Both ECT and TPS are pinned at extreme out-of-range limits across both speeds
        if (low_obd.coolant_temp_c <= -39 and stress_obd.coolant_temp_c <= -39) and \
           (low_obd.tps_pct >= 99 and stress_obd.tps_pct >= 99):
            return {
                "verdict": "ECU_INTERNAL_GROUND_TRACE_BLOWN",
                "confidence": "HIGH",
                "details": "Vaporized PCB ground trace causing floating sensor references. "
                           "OBD reports false -40C ECT and false 100% WOT simultaneously. "
                           "Physical exhaust is flooded rich."
            }

        # -------------------------------------------------------------
        # FAULT 2: ECU DRIFTED / COLLAPSED 5V REGULATOR RAIL [3, 2]
        # -------------------------------------------------------------
        # TPS and MAP are severely depressed across both speeds; trims pinned high
        if low_obd.tps_pct == 0.0 and stress_obd.tps_pct <= 20.0 and \
           low_obd.calculated_load <= 8.0 and stress_obd.calculated_load <= 10.0 and \
           tft1_low >= 40.0 and tft1_stress >= 40.0:
            return {
                "verdict": "ECU_COLLAPSED_5V_REGULATOR_RAIL",
                "confidence": "HIGH",
                "details": "Internal 5V reference rail collapsed (e.g. to 4.1V). "
                           "All ratiometric sensors (TPS, MAP) are suppressed. "
                           "ECU commands maximum enrichment but engine runs physically lean."
            }

        # -------------------------------------------------------------
        # FAULT 3: ECU LOW-SIDE INJECTOR DRIVER STUCK-ACTIVE (SHORTED) [4, 2]
        # -------------------------------------------------------------
        # Max negative trims on affected bank, normal trims on opposite bank. Highly rich exhaust.
        if tft1_low <= -45.0 and tft1_stress <= -45.0 and abs(tft2_low) < 10.0:
            if low_gas and low_gas.co_pct >= 6.0 and low_gas.physical_lambda < 0.85:
                return {
                    "verdict": "ECU_INJECTOR_DRIVER_SHORTED_BANK1",
                    "confidence": "HIGH",
                    "details": "Bank 1 low-side driver MOSFET fused closed. "
                               "Injector is stuck wide-open (100% duty cycle). "
                               "Bank 1 fuel trims pinned at -25% but tailpipe is heavily rich."
                }

        # -------------------------------------------------------------
        # FAULT 4: ECU LOW-SIDE INJECTOR DRIVER FAILED OPEN [4, 2]
        # -------------------------------------------------------------
        # Max positive trims on affected bank, opposite bank normal. High unburned oxygen.
        if tft1_low >= 45.0 and tft1_stress >= 45.0 and abs(tft2_low) < 10.0:
            if low_gas and low_gas.o2_pct >= 4.0 and low_gas.co_pct >= 1.0:
                return {
                    "verdict": "ECU_INJECTOR_DRIVER_OPEN_BANK1",
                    "confidence": "HIGH",
                    "details": "Bank 1 injector driver failed open. "
                               "Affected cylinder is dead and acts as an air pump. "
                               "Trims pinned at +25% while physical lambda reads falsely lean."
                }

        # -------------------------------------------------------------
        # FAULT 5: ECU HIGH-POWER IGNITION COIL DRIVER SHORTED [5, 2]
        # -------------------------------------------------------------
        # Permanent single-cylinder ignition misfire. Massive raw HC and high O2, very low CO.
        if 15.0 <= tft1_low <= 40.0 and abs(tft2_low) < 10.0:
            if low_gas and low_gas.hc_ppm >= 1800 and low_gas.o2_pct >= 4.5 and low_gas.co_pct <= 0.3:
                return {
                    "verdict": "ECU_IGNITION_COIL_DRIVER_SHORTED_BANK1",
                    "confidence": "HIGH",
                    "details": "IGBT driver shorted closed, melting the coil primary. "
                               "Permanent lack of spark. Raw fuel and unburned air are pumped, "
                               "threatening to melt the catalyst (>900C) under stress idle."
                }

        # -------------------------------------------------------------
        # FAULT 6: ECU ANALOG-TO-DIGITAL CONVERTER (ADC) CHANNEL FAILURE [6, 2]
        # -------------------------------------------------------------
        # Upstream O2 reads flatline low (<0.15V) OBD, but physical exhaust is heavily rich (CO > 3%)
        if (low_obd.upstream_o2_voltage and low_obd.upstream_o2_voltage < 0.15) and \
           (tft1_low >= 40.0 and tft1_stress >= 40.0):
            if low_gas and low_gas.co_pct >= 3.5 and low_gas.physical_lambda < 0.90:
                return {
                    "verdict": "ECU_ADC_O2_INPUT_PORT_FAILURE",
                    "confidence": "HIGH",
                    "details": "ECU internal ADC port failed or shorted internally. "
                               "Microprocessor reads static 0.0V (lean) and forces enrichment "
                               "to max limits, despite the actual engine running rich."
                }

        # -------------------------------------------------------------
        # FAULT 7: ECU CAPACITOR LEAKAGE & BOARD CORROSION [7, 2]
        # -------------------------------------------------------------
        # Highly fluctuating trims at idle; defaults to open loop fault at stress RPM
        if low_obd.fuel_system_status == 2 and stress_obd.fuel_system_status == 8 and \
           low_obd.calculated_load >= 15.0 and stress_obd.calculated_load < 10.0:
            return {
                "verdict": "ECU_CAPACITOR_LEAKAGE_BOARD_CORROSION",
                "confidence": "HIGH",
                "details": "Leaked corrosive electrolyte creates high-impedance shorts on the PCB. "
                           "Alternator ripple corrupts ADCs at high RPM, forcing ECU to "
                           "drop communication or crash into open loop fault mode (OL_FAULT)."
            }

        # -------------------------------------------------------------
        # FAULT 8: TRADITIONAL VACUUM LEAK
        # -------------------------------------------------------------
        # Trim delta is positive and large (trims recover significantly at higher speed)
        if tft1_low >= 15.0 and delta_tft1 >= 15.0:
            return {
                "verdict": "TRADITIONAL_VACUUM_LEAK",
                "confidence": "HIGH",
                "details": "Unmetered air enters the intake at idle. "
                           "As throttle opens at stress idle, leak volume becomes negligible, "
                           "causing fuel trims to return to normal limits."
            }

        # -------------------------------------------------------------
        # FAULT 9: TRADITIONAL FUEL RESTRICTION (WEAK PUMP/CLOGGED FILTER)
        # -------------------------------------------------------------
        # Trims are normal at idle but spike to positive maximums at stress idle
        if abs(tft1_low) < 8.0 and tft1_stress >= 20.0:
            return {
                "verdict": "TRADITIONAL_FUEL_RESTRICTION",
                "confidence": "HIGH",
                "details": "Fuel pump cannot supply required volume under load/high RPM. "
                           "Fuel trims remain normal at low idle but spike to max limits "
                           "under stress idle."
            }

        # -------------------------------------------------------------
        # FAULT 10: CONTAMINATED MAF SENSOR
        # -------------------------------------------------------------
        # Trims are positive at idle and stay positive/get worse under load; low load at high RPM
        if tft1_low >= 8.0 and tft1_stress >= 15.0 and stress_obd.calculated_load < 70.0:
            return {
                "verdict": "TRADITIONAL_MAF_CONTAMINATION",
                "confidence": "HIGH",
                "details": "Insulated hot-wire under-reports air mass. "
                           "Calculated load remains artificially low under snap-throttle/high speed, "
                           "and fuel trims remain highly positive across both speeds."
            }

        # -------------------------------------------------------------
        # FAULT 11: UPSTREAM EXHAUST LEAK
        # -------------------------------------------------------------
        # Lean trims at idle that recover instantly at high speed (exhaust pressure stops leak intake)
        if tft1_low >= 12.0 and delta_tft1 >= 10.0 and \
           low_obd.upstream_o2_voltage and low_obd.upstream_o2_voltage < 0.2:
            return {
                "verdict": "TRADITIONAL_UPSTREAM_EXHAUST_LEAK",
                "confidence": "MEDIUM",
                "details": "Exhaust pulses create a venturi effect pulling outside air into "
                           "the exhaust manifold past the O2 sensor at idle. "
                           "High exhaust backpressure at stress idle blocks outside air intrusion."
            }

        # -------------------------------------------------------------
        # FAULT 12: CATALYST EFFICIENCY FAILURE
        # -------------------------------------------------------------
        # Downstream O2 sensor mimics the upstream sensor's rapid oscillations across both speeds
        if (low_obd.downstream_o2_voltage and low_obd.downstream_o2_voltage < 0.45) and \
           abs(tft1_low) < 8.0 and abs(tft1_stress) < 8.0:
            return {
                "verdict": "TRADITIONAL_CATALYTIC_CONVERTER_FAILURE",
                "confidence": "HIGH",
                "details": "Downstream oxygen sensor mimics upstream voltage switching. "
                           "The catalyst has lost its oxygen storage and conversion capacity."
            }

        # -------------------------------------------------------------
        # FAULT 13: STUCK-OPEN EVAP PURGE VALVE
        # -------------------------------------------------------------
        # Rich trims at idle (negative) that recover back to normal at high speed
        if tft1_low <= -15.0 and tft1_stress >= -5.0:
            return {
                "verdict": "TRADITIONAL_STUCK_OPEN_EVAP_PURGE",
                "confidence": "HIGH",
                "details": "Fuel vapors are drawn directly into the high vacuum manifold at idle. "
                           "At stress idle, the constant leak is diluted by metered air, "
                           "normalizing fuel trims."
            }

        # -------------------------------------------------------------
        # FAULT 14: MECHANICAL ENGINE WEAR / TIMING RETARDED
        # -------------------------------------------------------------
        # High MAP and elevated calculated load at low idle; fuel trims remain normal
        if low_obd.map_kpa and low_obd.map_kpa >= 40.0 and \
           low_obd.calculated_load >= 25.0 and abs(tft1_low) < 8.0:
            return {
                "verdict": "TRADITIONAL_ENGINE_MECHANICAL_WEAR_OR_RETARDED_TIMING",
                "confidence": "MEDIUM",
                "details": "Low engine intake vacuum at idle (high MAP). "
                           "May be caused by low cylinder compression, late valve timing, "
                           "or retarded ignition timing."
            }

        # Default fallback if no deterministic pattern is matched
        return {
            "verdict": "COHERENT_SYSTEM_LIMITS_MET_OR_UNCLASSIFIED_FAULT",
            "confidence": "LOW",
            "details": "Telemetry patterns do not match any known solid-state "
                       "ECU hardware failures or standard external faults."
        }

```

---

## 4. Operational Differentiators

The manual-entry model allows technicians to run diagnostics using exact parameters, completely bypassing dynamic lag errors ``.

| Telemetric Delta | ECU Blown Ground Trace `[2]` | Traditional Vacuum Leak `` | MAF Contamination `` |
| --- | --- | --- | --- |
| **Low Idle ECT** | Locked at $-40\text{ }^\circ\text{C}$ | Normal Warm ($>75\text{ }^\circ\text{C}$) | Normal Warm ($>75\text{ }^\circ\text{C}$) |
| **Low Idle TPS** | Locked at $100\%$ | Normal ($0\text{--}12\%$) | Normal ($0\text{--}12\%$) |
| **Low Idle Trims** | $0\%$ (Locked Open-Loop) | High Positive ($>+15\%$) | Moderately Positive ($>+8\%$) |
| **Stress Idle Trims** | $0\%$ (Locked Open-Loop) | Normalized Trims ($< \pm5\%$) | Highly Positive ($>+20\%$) |
| **Stress Idle Load** | Pinned $100\%$ | Normal ($10\text{--}12\%$) | Artificially Low ($<70\%$) |
| **Physical Exhaust** | Opaque Rich ($CO \approx 9.5\%$) | Stoichiometric ($\lambda \approx 1.000$) | Balanced or Lean ($\lambda \ge 1.050$) |

---

## 5. Interface Implementation (CLI Example)

A simple Python CLI script wraps this system, allowing immediate manual entry and diagnostic generation in the field without any complex compilation requirements ``.

```python
# app.py
if __name__ == "__main__":
    print("--- OBDLab Static Manual-Entry Diagnostic Tool ---")
    
    # Example input representing a Blown ECU Ground Trace
    low_obd = OBDTelemetricSnapshot(
        engine_rpm=750.0,
        calculated_load=85.0,  # Pinned high false reading
        coolant_temp_c=-40.0,  # Floated sensor minimum
        shrtft1=0.0,
        longft1=0.0,
        tps_pct=100.0,          # Pinned high false reading
        fuel_system_status=8   # Open Loop due to fault
    )
    
    stress_obd = OBDTelemetricSnapshot(
        engine_rpm=4000.0,
        calculated_load=100.0,
        coolant_temp_c=-40.0,
        shrtft1=0.0,
        longft1=0.0,
        tps_pct=100.0,
        fuel_system_status=8
    )
    
    engine = ForensicDiagnosticEngine(displacement_liters=2.0)
    result = engine.diagnose(low_obd, None, stress_obd, None)
    
    print(f"\nDIAGNOSTIC VERDICT: {result['verdict']}")
    print(f"CONFIDENCE: {result['confidence']}")
    print(f"FORENSIC ANALYSIS: {result['details']}")

```
