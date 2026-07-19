The Engine Load PID is one of the most powerful but frequently misunderstood data parameters available in the OBD-II standard. Properly utilizing it within the `obdlab` knowledge graph and `comlab` reasoning pipeline is essential for verifying airflow sensor health, calculating engine pumping efficiency, and isolating complex driveability faults.

Below is the technical blueprint on how to mathematically utilize **Calculated Load** versus **Absolute Load**, followed by the additional live OBD PIDs you must add to establish a highly robust diagnostic application.

---

### Part 1: How to Properly Utilize the "Load" PIDs

In OBD-II diagnostics, there are two distinct types of load PIDs defined by the SAE J1979 standard:

#### 1. Calculated Engine Load Value (PID `0x04`)

Calculated Load represents the current percentage of maximum available engine torque being produced. The PCM calculates it using the following standardized formula:

$$\text{Calculated Load} = \left( \frac{\text{Current Airflow}}{\text{Peak Airflow @ Sea Level}} \right) \times \left( \frac{\text{Barometric Pressure @ Sea Level}}{\text{Barometric Pressure}_{\text{ambient}}} \right) \times 100\%$$

* **Key Diagnostic Rule:** Because it is mathematically corrected for altitude (via the barometric pressure term), Calculated Load **must reach approximately $100\%$ at Wide Open Throttle (WOT)** under normal conditions, regardless of elevation, for both naturally aspirated and forced-induction engines.
* **How `obdlab` Uses It:**
* **The WOT Sensor Sanity Check:** During a transient stress sweep (acceleration), if the user drives the throttle to $100\%$ but Calculated Load struggles to climb past $70\text{--}80\%$, the engine is experiencing either a physical airflow restriction (clogged intake/exhaust) or the MAF sensor is severely degraded and under-reporting the air mass.
* **Engine Idle Parasitic Drag:** At standard warm idle with no accessories on (A/C off, steering wheel straight), Calculated Load should hover between $15\%$ and $25\%$. If Calculated Load is abnormally high at idle ($>35\%$), it indicates heavy internal mechanical resistance, a failing alternator, or a tight engine block.



#### 2. Absolute Load Value (PID `0x43`)

Absolute Load represents the normalized percentage of air mass entering the cylinders per intake stroke. It is calculated by dividing the physical air mass per stroke by the theoretical maximum air mass the cylinder can hold at stoichiometric conditions:

$$\text{Absolute Load} = \left( \frac{\text{Air Mass per Intake Stroke}}{\text{Theoretical Air Mass @ 100\% Throttle \& Standard Temperature & Pressure}} \right) \times 100\%$$

* **Key Diagnostic Rule:** Unlike Calculated Load, **Absolute Load is not corrected for altitude**. It directly scales with local ambient air density, dropping by approximately $3\%$ per $1000\text{ feet}$ of elevation. This makes Absolute Load a direct reflection of the engine's true **Volumetric Efficiency (VE)**.
* **How `obdlab` Uses It:**
* **Volumetric Efficiency Verification:** Under WOT at sea level, a naturally aspirated engine should display an Absolute Load of approximately $80\text{--}90\%$ (matching its peak volumetric efficiency). For supercharged or turbocharged engines, Absolute Load will easily exceed $100\%$ under boost because air is being actively forced into the cylinders.
* **Isolating MAF under-reporting:** If the calculated VE from your math model shows $95\%$ but the Absolute Load reported on the OBD data stream is only $70\%$, it confirms that the MAF sensor is electrically intact (no P0102 code) but is severely dirty and under-reporting the air weight.



#### 3. Long Term Fuel Trim Cell Mapping

The PCM organizes its Long Term Fuel Trim adaptive memory into a physical cell-matrix. It uses **Engine Speed (RPM)** and **Calculated Load (or MAF g/s)** as the coordinates to locate the correct memory cell.

* Your `obdlab` knowledge graph should map PIDs to these cells (e.g., *Idle Cell*, *Cruise Cell*, *Power Enrichment/WOT Cell*).


* If fuel trims are highly positive strictly in low-load cells ($<20\%$ load) but normalize in high-load cells ($>50\%$ load), the logic automatically isolates the fault to a vacuum leak downstream of the throttle body.

---

### Part 2: Additional Essential Live PIDs for Robust Diagnostics

To transition your system from basic code reading to a highly robust "expert-system" diagnostic tool, `obdlab` must accept and cross-reference the following additional live PIDs:

#### 1. Fuel System Status (PID `0x03` - `FUELSYS`)

This PID returns the status of the fuel feedback loop (e.g., `OL` for Open Loop, `CL` for Closed Loop, `OL_Drive` for deceleration/enrichment, or `OL_Fault` for loop failures).

* **Why it's essential:** Fuel trim values (STFT/LTFT) are **meaningless** in Open Loop because the PCM is ignoring sensor feedback and running off default lookup tables.
* **Causal Logic:** If the engine coolant temperature (ECT) is high ($>80^{\circ}\text{C}$) but `FUELSYS` remains locked in `OL`, and fuel trims flatline at $0\%$, COMLab can immediately pinpoint an active system fault preventing closed-loop transition (such as an unheated/dead oxygen sensor).

#### 2. Control Module Voltage (PID `0x42` - `VPWR`)

Measures the supply voltage at the PCM input pins.

* **Why it's essential:** Computerized engine sensors rely on a clean, stable DC power supply. High AC ripple voltage or a system voltage dropping below $12.0\text{ V}$ or spiking above $15.0\text{ V}$ will cause sensors to drift, shift stoichiometric references, and trigger false PCM processor codes (such as the false P0606 code on Toyotas).


* **Causal Logic:** If the trim delta is unstable and `VPWR` reads $<11.5\text{ V}$, the system flags a primary electrical ground or charging system failure before blaming any air/fuel sensors.



#### 3. Absolute / Relative Throttle Position (PIDs `0x11` / `0x45` - `TP` / `TP_R`)

These PIDs monitor the physical angle of the throttle plate relative to the learned closed-idle stop.

* **Why it's essential:** Essential for diagnosing air leaks and idle control system malfunctions (P0505).
* **Causal Logic:** On an engine with a surging idle (Case 19), if the `TP_R` reads $0\%$ (completely closed) but engine RPM is high ($1500\text{ RPM}$) and Calculated Load is high, it proves that a massive volume of unmetered air is bypassing the throttle blade (intake manifold crack, blown IAC gasket, or stuck-open EVAP purge valve).

#### 4. Barometric Pressure (PID `0x33` - `BARO`)

This represents atmospheric pressure, measured directly by a dedicated sensor or calculated by the MAP sensor at Key On Engine Off (KOEO).

* **Why it's essential:** Standard ambient pressure at sea level is $101.3\text{ kPa}$ ($29.92\ \text{in Hg}$). As altitude increases, pressure drops.
* **Causal Logic:** The diagnostic engine must scale its maximum theoretical airflow equations dynamically based on the local BARO. A faulty MAP sensor that under-reports ambient BARO will force the PCM into an incorrect, lean-biased altitude compensation map.

#### 5. Misfire Cylinder Monitors (Cylinder-Specific Counts)

Standard OBD-II Mode $06$ or enhanced data streams monitor misfire counts per cylinder over $200$ and $1000$ engine revolutions.

* **Why it's essential:** Raw fuel trims are highly sensitive to misfires. A misfiring cylinder cannot consume oxygen, pumping fresh $O_2$ directly past the exhaust sensor and creating a false lean indication.


* **Causal Logic:** If positive fuel trims ($>15\%$) are accompanied by a single-cylinder misfire count (e.g., Cylinder 1 misfires escalating), the system isolates the issue to a localized cylinder fault (ignition coil, bad plug, or leaking injector). If misfires are randomly spread across all cylinders alongside high positive trims, the system routes the fault to global fuel starvation (weak fuel pump).



---

### Diagnostic Workflow Mapping in `composition.py`

To incorporate these metrics into the existing `composition.py` data flow:

```python
# wired/composition.py (Mechanical mapping extension)

# raw_inputs mapped from the 7 Streamlit UI sidebar expanders:
raw_obd_pids = raw_inputs["obd_pids"]

# Inside Phase 2: OBDLab Translation:
obd_payload = SensorSignalTranslator.translate(raw_obd_pids, dna_view)

# Mapped variables forwarded to COMLab via OrchestratorInboundRequest:
# calculated_load_pct       -> consumer: fault_atlas_router (load cell categorizer)
# absolute_load_pct         -> consumer: fault_atlas_router (VE calculation cross-reference)
# fuel_system_status        -> consumer: Stage A gate (abort diagnostics if in OPEN loop)
# control_module_voltage    -> consumer: perception_contradiction (grounds & alternator health) [2]
# absolute_throttle_pct     -> consumer: fault_atlas_router (idle air leak validator)
# barometric_pressure_kpa   -> consumer: fault_atlas_router (ambient pressure calibration)

```

Integrating these highly correlated airflow, electrical, and control PIDs into your state frames prevents your diagnostic engine from being fooled by sensor cross-talk and ensures dealer-level diagnostics.

Evaluating the engine between low idle (~750 RPM) and stationary stress idle (~2500 RPM) in neutral provides an effective diagnostic approach, even without transient "sweep-snap" throttle tests.

By comparing steady-state data points across these two distinct operating ranges, your system can calculate transition deltas ($\Delta$) to assess sensor calibration health, electrical charging system integrity, parasitic mechanical drag, and combustion anomalies.

---

### Part 1: Deducing Parasitic Drag and Sensor Health from Static Deltas

#### 1. Deducting Parasitic Drag from Calculated Load Delta

Because there is no external load on the flywheel when the transmission is in neutral, any torque produced at both low and high idle is consumed strictly by internal engine friction, pumping losses, and accessory drag.

The Calculated Load delta ($\Delta\text{Load}_{\text{calc}}$) is defined as:

$$\Delta\text{Load}_{\text{calc}}=\text{Load}_{\text{calc\_2500}}-\text{Load}_{\text{calc\_750}}$$

* **Normal Behavior:** At a warm idle, Calculated Load hovers between 15% and 25%. When elevated to 2500 RPM in neutral, a healthy engine only requires a minor torque increase to overcome additional friction, keeping Calculated Load low (typically 20% to 30%).
* **High Parasitic Drag:** If the delta spikes significantly high ($\Delta\text{Load}_{\text{calc}}>15\%$), it reveals a major parasitic load. Because the engine is not moving the vehicle, this drag is isolated to:
* An alternator under maximum electrical load (e.g., failed battery or shorted alternator field winding drawing excessive current).
* Mechanical binding of an engine accessory (e.g., a binding air conditioning compressor or water pump).
* Extreme exhaust backpressure (e.g., a clogged catalytic converter choking the engine, forcing it to pump harder to expel exhaust).



#### 2. Mass Air Flow (MAF) / Manifold Absolute Pressure (MAP) Sensor Sanity Checking

A damaged or contaminated MAF or MAP sensor often has a non-linear calibration curve. A sensor may report accurate airflow at low velocities (750 RPM) but over- or under-report airflow as air velocity and density increase at 2500 RPM.

To verify sensor calibration without a snap-throttle test, OBDLab can calculate the theoretical airflow ($W_{\text{theo}}$) based on the ideal gas law and engine speed-density parameters:

$$W_{\text{theo}}=\frac{\eta_{V}\times V_{\text{disp}}\times P_{\text{manifold}}\times\text{RPM}}{120\times R\times T_{\text{intake}}}$$

Using this baseline, COMLab evaluates the sensor calibration error delta ($\Delta\text{Sensor}_{\text{error}}$):

$$\Delta\text{Sensor}_{\text{error}}=\left|\text{Sensor}_{\text{reported\_2500}}-W_{\text{theo\_2500}}\right|-\left|\text{Sensor}_{\text{reported\_750}}-W_{\text{theo\_750}}\right|$$

* **Interpretation:** If $\Delta\text{Sensor}_{\text{error}}\approx 0$, the sensor's reported flow scales linearly with physical engine demands. If $\Delta\text{Sensor}_{\text{error}}$ deviates significantly from zero, the sensor element has suffered a calibration drift (such as a dirty MAF hot-wire), causing incorrect fuel calculations under load.

---

### Part 2: Delta Logic Behind Additional PIDs

Transition deltas across the other major live PIDs provide highly specific diagnostic pathways:

#### 1. Fuel System Status (PID `0x03` - `FUELSYS`)

$$\Delta\text{FUELSYS}=\text{FUELSYS}_{2500}-\text{FUELSYS}_{750}$$

* **The Transient Closed-Loop Dropout:** If the engine runs in Closed Loop (CL) at idle but drops into an Open Loop fault state (OL_Fault) at 2500 RPM, it indicates an RPM- or heat-dependent electrical failure. This points directly to an $O_2$ sensor heater circuit dropping out, or a wiring harness shorting out due to engine vibration under higher speeds.

#### 2. Control Module Voltage (PID `0x42` - `VPWR`)

$$\Delta\text{VPWR}=\text{VPWR}_{2500}-\text{VPWR}_{750}$$

* **The Rectifier Diode Breakdowns:** System voltage should remain stable between 13.5V and 14.5V with the engine running.
* If $\Delta\text{VPWR}<-1.0\text{ V}$, the alternator is dropping voltage under load, pointing to alternator belt slippage or a failed regulator diode.
* If $\Delta\text{VPWR}>+2.5\text{ V}$ (causing system voltage to exceed 15.5V under revs), the alternator voltage regulator has failed, creating high AC ripple voltage that corrupts sensor reference signals and triggers false ECM processor faults.





#### 3. Throttle Position (PIDs `0x11` / `0x45` - `TP` / `TP_R`)

$$\Delta\text{TP\_R}=\text{TP\_R}_{2500}-\text{TP\_R}_{750}$$

* **Pumping & Obstruction Verification:** Holding 2500 RPM in neutral requires very little physical throttle opening ($\Delta\text{TP\_R}$ should only be roughly 3% to 8%).
* If $\Delta\text{TP\_R}>15\%$, the engine requires an excessively wide throttle plate angle to pull in air, indicating a severe intake manifold restriction, a clogged air filter, or heavy exhaust backpressure.
* If $\Delta\text{TP\_R}\approx 0\%$ but RPM remains elevated or surges, it confirms unmetered air is bypassing the throttle blade, indicating an idle air control valve malfunction or a stuck-open EVAP purge valve.



#### 4. Barometric Pressure (PID `0x33` - `BARO`)

$$\Delta\text{BARO}=\text{BARO}_{2500}-\text{BARO}_{750}$$

* **Intake Plenum Restriction Test:** Since local atmospheric pressure is constant during a stationary test, $\Delta\text{BARO}$ must equal $0\text{ kPa}$.
* If the calculated barometric pressure drops at higher RPMs ($\Delta\text{BARO}<0\text{ kPa}$), the engine is pulling a vacuum on the intake ductwork due to a collapsed intake hose, a restricted air box, or a heavily restricted air filter.





#### 5. Cylinder-Specific Misfire Counts

$$\Delta\text{Misfire}_{\text{cyl}}=\text{Misfire}_{\text{cyl\_2500}}-\text{Misfire}_{\text{cyl\_750}}$$

Evaluating how misfires respond to engine speed allows the system to isolate vacuum leaks, ignition faults, and fuel limitations:

* **$\Delta\text{Misfire}\ll 0$ (Misfires at idle, but clear up at 2500 RPM):** This is the classic signature of an intake manifold vacuum leak or a dirty fuel injector. The high intake vacuum at idle pulls in unmetered air, but this leak becomes mathematically insignificant as the throttle opens under higher speeds.


* **$\Delta\text{Misfire}\gg 0$ (Smooth idle, but misfires spike at 2500 RPM):** This isolates ignition system electrical breakdown (such as a cracked spark plug insulator or failing ignition coil primary/secondary winding) or fuel delivery volume starvation (a weak fuel pump or clogged fuel filter that cannot keep up with higher fuel demand).