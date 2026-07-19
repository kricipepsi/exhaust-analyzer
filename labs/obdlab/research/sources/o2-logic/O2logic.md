To properly implement the oxygen ($O_2$) sensor logic within the `obdlab` local knowledge graph, the system must utilize the vehicle configuration provided by `DNALab` (`ObdLabDnaView`) to dynamically alter its internal evaluation pathways.

When `DNALab` identifies the vehicle's specific emissions profile and sensor topology, `composition.py` maps the O2 sensor type to either `WIDEBAND_LINEAR` or `NARROWBAND_0_TO_1V`. `obdlab` then loads this structural configuration into its local knowledge graph to select the appropriate translation rules and calculation algorithms.

Here is how the ontology is structured and how the next steps are executed for each of the three petrol-only (1990–2010) scenarios.

---

### 1. Structural Ontological Modeling of the O2 Sensor Nodes

The local knowledge graph inside `obdlab` represents the physical exhaust layout using semantically typed nodes and directed relationships. Instead of hardcoding conditional loops, the sensor signals are evaluated by traversing this ontological structure:

```
              
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
                 
     (Upstream Loop)          (Downstream Loop)
             │                         │
          
             │                         │
      

```

The primary RDF triple relationships asserted in the graph based on the `ObdLabDnaView` are:

* `(O2_Sensor_1, rdf:type, obd:UpstreamFeedbackSensor)`
* `(O2_Sensor_1, obd:hasMeasurementType, obd:WIDEBAND_LINEAR)` (or `obd:NARROWBAND_0_TO_1V`)
* `(O2_Sensor_2, rdf:type, obd:DownstreamMonitoringSensor)`
* `(O2_Sensor_2, obd:hasTrimRole, obd:MONITOR_ONLY)` (or `obd:ACTIVE_REAR_TRIM`)

---

### Scenario 1: Just Narrowband (NB) Upstream

This configuration is typical for pre-1996 OBD-I vehicles or early, cost-sensitive OBD-II models (1996–2000) with a single-sensor feedback loop.

```
  ───> [Cross-Count Evaluator] ───> ───> OBDLivePayload

```

#### Graph Routing & Translation Steps:

1. **Initialize Narrowband Path:** The graph activates the `NarrowbandSignalEvaluator` sub-graph and connects the incoming voltage parameter `O2S11_V` (0.1 V to 0.9 V).


2. **Dynamic Switching Evaluation:** Because a healthy narrowband sensor must cycle rapidly across the stoichiometric threshold of 0.45 V under closed-loop control, `obdlab` runs a sliding-window cross-count algorithm:
* Let $C_{\text{cross}}$ be the number of times the voltage signal crosses the 0.45 V threshold within a 1-second interval.
* If the engine is warm (coolant temperature $>80^{\circ}\text{C}$ / 176°F) and the system is in closed-loop, the switching frequency must satisfy:

$$C_{\text{cross}} \ge f_{\text{min}} \quad (\text{where } f_{\text{min}} = 0.5\text{ Hz})$$




3. **Threshold and Bias Checks:**
* **Lazy Sensor:** If $C_{\text{cross}} < 0.5\text{ Hz}$, the local graph asserts the triple: `(O2_Sensor_1, obd:hasFailureMode, obd:LAZY_SWITCHING)`.
* **Biased Rich:** If the signal voltage remains consistently high ($V_{\text{min}} > 0.55\text{ V}$), the graph asserts: `(O2_Sensor_1, obd:hasFailureMode, obd:BIASED_RICH)`.
* **Biased Lean:** If the signal voltage remains consistently low ($V_{\text{max}} < 0.35\text{ V}$), the graph asserts: `(O2_Sensor_1, obd:hasFailureMode, obd:BIASED_LEAN)`.
* **Open Circuit / Dead Sensor:** If the voltage flatlines at exactly 0.45 V with no activity, the graph flags an unheated or failed sensor state (`NO_ACTIVITY`).


4. **Normalized Lambda Calculation:** Since narrowband sensors behave like binary switches rather than linear meters, `obdlab` calculates a normalized, step-wise lambda ($\lambda_{\text{obd}}$) for COMLab:
* If $V_{\text{upstream}} > 0.45\text{ V} \implies \lambda_{\text{obd}} \approx 0.97$ (Rich).
* If $V_{\text{upstream}} < 0.45\text{ V} \implies \lambda_{\text{obd}} \approx 1.03$ (Lean).



---

### Scenario 2: Just Wideband (WB) Upstream

This setup utilizes a high-precision, linear Air-Fuel Ratio (A/F) sensor as the sole source of fuel feedback control.

```
  ───> ───> ───> OBDLivePayload

```

#### Graph Routing & Translation Steps:

1. **Prune Switching Rules:** The local graph dynamically **deactivates** the `NarrowbandSignalEvaluator`, `CrossCountEvaluator`, and `VoltageSwitchingLimits` nodes. Running these algorithms on a wideband sensor would trigger a false "lazy sensor" or "stuck" fault because wideband signals remain highly stable and linear under normal operation.
2. **Linear Scale Mapping:** Read the equivalence ratio ($\Phi$) from PID `0x34` (or `0x24` for raw voltage/current output). The sensor measures pump current ($I_{\text{pump}}$) to maintain the internal reference sensing cell (VS) at 450 mV:

$$I_{\text{pump}} \propto \left( \lambda - 1.0 \right)$$



Where positive current ($I_{\text{pump}} > 0\text{ mA}$) represents a lean mixture and negative current ($I_{\text{pump}} < 0\text{ mA}$) represents a rich mixture.
3. **Normalized Lambda Calculation:** Convert the reported equivalence ratio directly to lambda:

$$\lambda_{\text{obd}} = \frac{1}{\Phi}$$



If the vehicle reports a raw linear voltage output ($V_{\text{linear}}$) on a 0–5 V scale (such as Toyota's 3.3 V stoichiometric baseline or Honda's 2.5 V baseline), `obdlab` maps this voltage through the manufacturer's scaling constant ($K_{\text{scale}}$) stored in the ontology database :



$$\lambda_{\text{obd}} = \text{Offset}_{\text{base}} + K_{\text{scale}} \cdot V_{\text{linear}}$$


4. **Setpoint Offset Delta Tracking:**
At a steady cruise with fuel trims stabilized, calculate the offset from target stoichiometry:

$$\Delta\lambda_{\text{offset}} = \left| \lambda_{\text{obd}} - 1.0 \right|$$



If the offset is persistent ($\Delta\lambda_{\text{offset}} > 0.05$) while the engine is physically running stoichiometrically (confirmed downstream by GASLab's measured exhaust chemistry $\lambda_{\text{chem}} \approx 1.0$), `obdlab` asserts the failure mode :
`(O2_Sensor_1, obd:hasFailureMode, obd:BIASED_OFFSET)`



---

### Scenario 3: Wideband Upstream and Narrowband Downstream (No Active Trim Regulation)

This hybrid configuration is standard on vehicles from 2001–2005 (such as the Toyota Celica/Corolla 1ZZ-FE). The upstream wideband sensor handles active fueling adjustments, while the downstream narrowband sensor acts strictly as a passive catalytic converter monitor with no authority to adjust fuel trims.

```
  ───> ───>

```

#### Graph Routing & Translation Steps:

1. **Parallel Execution Branching:** The graph splits the incoming data into two independent evaluation loops:
* **Upstream:** Sent to the `WidebandLinearEvaluation` path (same as Scenario 2) to calculate `normalized_obd_lambda`.
* **Downstream:** Sent to the `DownstreamPassiveEvaluation` path to monitor the downstream voltage `O2S12_V` (0.1 V to 0.9 V).


2. **Passive Catalyst Evaluation Logic:**
* A healthy catalytic converter stores oxygen, dampening any exhaust fluctuations. The downstream narrowband sensor should produce a smooth, stable, non-switching line (typically hovering between 0.5 V and 0.7 V).


* If the catalytic converter degrades, its oxygen storage capacity drops, and the downstream sensor begins to cycle and mimic the upstream exhaust pattern.


* `obdlab` calculates a signal transfer index ($TI_{\text{cat}}$) by comparing the standard deviation ($\sigma$) of the downstream voltage against the upstream wideband's converted lambda signal over a 10-second window under steady cruise conditions :



$$TI_{\text{cat}} = \frac{\sigma(V_{\text{downstream}})}{\sigma(V_{\text{upstream}})}$$


* If $TI_{\text{cat}} > 0.75$, the graph asserts the failure mode:
`(Catalytic_Converter_1, obd:hasEfficiencyStatus, obd:DEGRADED_P0420)`.


3. **Rear Trim Fault Suppression (Crucial Step):**
* On newer post-2005 vehicles, the downstream sensor actively adjusts long-term fueling trends (rear fuel trim feedback) to compensate for upstream sensor wear, logging codes P2096 or P2099 if the adjustments reach their limits.
* In this scenario, however, `DNALab` flags that the platform lacks downstream active trim capability.
* `obdlab` must write `downstream_trim_role = MONITOR_ONLY` and `trim_analytics_gate = SUPPRESS_POST_CAT_TRIM` to the `OBDLivePayload`.
* This instruction commands the downstream COMLab `fault_atlas_router` to **bypass** and suppress all post-catalyst fuel trim calculations (P2096/P2099). This ensures any fuel trim codes (like P0171 or P0172) are isolated strictly to the upstream sensor's control loop.





---

### Summary of O2 Sensor Graph Translation and Outputs

| Vehicle O2 Configuration | Input Signals | local Graph Traversal Path | OBDLivePayload Output Values | COMLab Downstream Action |
| --- | --- | --- | --- | --- |
| **Scenario 1:** Upstream Narrowband Only | `O2S11_V` | `NarrowbandSignalEvaluator` $\rightarrow$ `CrossCountEvaluator` | `normalized_obd_lambda` (oscillating steps), `o2_failure_mode` (LAZY / BIASED) | Evaluate switching speed; verify if lean trim code P0171 is caused by a slow sensor.

 |
| **Scenario 2:** Upstream Wideband Only | `EQ_RAT11`, `O2S11_V` (linear) | `WidebandLinearEvaluation` (Prune switching rules) | `normalized_obd_lambda` (continuous $\lambda$), `o2_failure_mode` (BIASED_OFFSET) | Cross-reference $\lambda_{\text{obd}}$ with GASLab's chemical tailpipe $\lambda_{\text{chem}}$ to identify sensor drift. |
| **Scenario 3:** Upstream Wideband + Downstream Narrowband (No Rear Trim) | `EQ_RAT11` (S1) + `O2S12_V` (S2) | `WidebandLinearEvaluation` (S1) + `DownstreamPassiveEvaluation` (S2) | `downstream_trim_role = MONITOR_ONLY`, `trim_analytics_gate = SUPPRESS_POST_CAT_TRIM` | Run catalyst efficiency check (P0420); suppress all post-cat trim low/high limit codes (P2096/P2099). |


Comparing oxygen ($O_2$) sensor behavior between low idle ($\approx 750\text{ RPM}$) and stress idle ($\approx 2500\text{ RPM}$) is essential for accurate diagnostics.

At low idle, the exhaust gas velocity and temperature are low, which can cause an aged or partially contaminated sensor to cool down, resulting in sluggish switching or flatlining. At stress idle, the increased exhaust flow and thermal energy ($>600^{\circ}\text{C}$) will often "wake up" a lazy sensor element.

By calculating the transition deltas of the $O_2$ signals across both speeds and cross-referencing them with fuel trims and airflow metrics (MAP/MAF), your system can isolate faults with high precision.

---

### 1. Calculating $O_2$ Sensor Deltas in COMLab

Your system can calculate three distinct $O_2$ transition deltas within the centralized reasoning module:

#### A. Upstream Switching Frequency Delta ($\Delta f_{\text{O2}}$)

Measures the change in the sensor's switching rate as exhaust temperature rises:


$$\Delta f_{\text{O2}}=f_{\text{switching\_2500}}-f_{\text{switching\_750}}$$

* **Interpretation:** A significant positive delta ($\Delta f_{\text{O2}}\ge 1.0\text{ Hz}$) where the sensor fails to switch at idle but cycles normally at $2500\text{ RPM}$ indicates an **aged or contaminated sensor element** (or a failing internal heater circuit).

#### B. Upstream Voltage Bias Delta ($\Delta V_{\text{O2}}$)

Measures the shift in the average signal voltage between low and high speeds:


$$\Delta V_{\text{O2}}=V_{\text{avg\_2500}}-V_{\text{avg\_750}}$$

* **Interpretation:** A sensor that switches normally at idle but flatlines low under load ($\Delta V_{\text{O2}}\ll 0$) indicates **physical fuel starvation** or an **under-reporting MAF sensor**.

#### C. Downstream Signal Transfer Index Delta ($\Delta TI_{\text{cat}}$)

Evaluates catalytic converter oxygen storage capacity under load :


$$\Delta TI_{\text{cat}}=TI_{\text{cat\_2500}}-TI_{\text{cat\_750}}$$

* **Interpretation:** If the downstream sensor is stable at idle but begins to cycle and mirror the upstream sensor at stress idle ($\Delta TI_{\text{cat}}\gg 0$), it indicates a **degraded catalytic converter** that has lost its oxygen storage capability.

---

### 2. Multi-Module Cross-Referencing Matrix

The table below demonstrates how the centralized reasoning engine cross-references $O_2$ deltas with fuel trims (STFT/LTFT) and calculated Volumetric Efficiency (VE, derived from MAP or MAF) across both speeds to isolate the root cause.

| Fault Scenario | Low Idle (750 RPM) | Stress Idle (2500 RPM) | Cross-Referenced Delta Trends | Root Cause Isolation Logic | Citation |
| --- | --- | --- | --- | --- | --- |
| **Intake Vacuum Leak** | Trims $>+20\%$, upstream O2 flatlines lean ($<0.2\text{ V}$) | Trims recover ($<\pm 5\%$), upstream O2 switches cleanly ($0.1\text{--}0.9\text{ V}$) | $\Delta\text{Trim}\ll 0$, $\Delta f_{\text{O2}}>1.0\text{ Hz}$, VE is valid at both speeds | Unmetered air entering downstream of the throttle body is chemically diluted by the high volume of metered air under load. |  |
| **Upstream Exhaust Leak** | Trims $>+20\%$, upstream O2 flatlines lean ($<0.2\text{ V}$) | Trims recover ($<\pm 5\%$), upstream O2 switches cleanly ($0.1\text{--}0.9\text{ V}$) | $\Delta\text{Trim}\ll 0$, $\Delta f_{\text{O2}}>1.0\text{ Hz}$, VE is valid, but **idle IAC/throttle angles are normal** | Unlike an intake leak, no unmetered air enters the cylinders. At $2500\text{ RPM}$, exhaust backpressure prevents fresh air from being drawn past the crack into the exhaust stream. |  |
| **Fuel Delivery Starvation** | Trims are normal ($\approx 0\%$), upstream O2 switches cleanly | Trims climb ($>+25\%$), upstream O2 flatlines lean ($<0.1\text{ V}$) | $\Delta\text{Trim}\gg 0$, $\Delta V_{\text{O2}}\ll 0$, VE calculation is **fully valid** | The engine receives the commanded air mass (valid MAF/MAP), but the weak fuel pump or restricted filter cannot deliver the required fuel volume under load. |  |
| **Under-reporting MAF Sensor** | Trims are normal ($\approx 0\%$), upstream O2 switches cleanly | Trims climb ($>+25\%$), upstream O2 flatlines lean ($<0.1\text{ V}$) | $\Delta\text{Trim}\gg 0$, $\Delta V_{\text{O2}}\ll 0$, VE calculation **drops significantly under load** | The MAF sensor's calibration curve is degraded; it fails to report the actual air mass entering the cylinders under high-flow conditions. |  |
| **Lazy/Contaminated Upstream O2** | Trims are erratic, upstream O2 switching is sluggish ($<0.3\text{ Hz}$) | Trims stabilize, upstream O2 switches normally ($\ge 1.5\text{ Hz}$) | $\Delta\text{Trim}\approx 0$, $\Delta f_{\text{O2}}\gg 0$, VE is valid at both speeds | The sensor element is physically contaminated. High exhaust temperatures under load temporarily clean and activate the sensing ceramic. |  |
| **Degraded Catalytic Converter** | Upstream O2 switches cleanly, downstream O2 is stable ($\approx 0.6\text{ V}$) | Upstream O2 switches cleanly, downstream O2 switches rapidly | $\Delta\text{Trim}\approx 0$, $\Delta TI_{\text{cat}}\gg 0$, VE and trims are stable | The catalyst can store oxygen at low exhaust velocities (idle), but fails under the higher flow rates of stress idle, mirroring upstream behavior. |  |

### Summary of System Integration

This cross-referencing logic resolves complex, overlapping symptoms without any direct communication between your parsing labs. Your UI collects the datasets at both low idle and stress idle; the specialized parsing labs (OBDLab, GASLab, DTCLab) translate the raw inputs into static semantic statuses; and COMLab's analytics module processes the transition deltas to deliver a single, highly accurate diagnostic verdict.