Yes, incorporating a dedicated delta-calculation module inside **COMLab** (e.g., `comlab/analytics/idle_transition_evaluator.py`) is **highly recommended** and is structurally essential to resolving the majority of our studied cases with high accuracy.

Without analyzing the dynamic transitions (deltas) of the engine between low idle and high idle ($2500\text{ RPM}$), the central brain is forced to diagnose complex driveability issues using static, single-point snapshots. This static approach makes it incredibly difficult to distinguish between physically distinct faults that present identical static values.

To implement this without violating the system's strict **Isolation Contract**, the delta calculations must be handled as a centralized downstream reasoning step within COMLab.

---

### 1. The Diagnostic Value: Why Delta Cross-Referencing is Critical

By comparing the rate of change ($\Delta$) of **Tailpipe Gases (GASLab)** against **Sensor PIDs (OBDLab)** across two distinct load states, COMLab can isolate root causes with mathematical certainty.

```
  [User Inputs: Low Idle] ───┐
                             ├───> [ wired/composition.py ] ───>
  [User Inputs: High Idle] ──┘

```

#### A. Isolating Vacuum Leaks vs. Failing Fuel Pumps 



A vehicle presenting with highly positive fuel trims at low idle could have a vacuum leak (Case 1) or a failing fuel pump (Case 2).

* **The Vacuum Leak Delta:** As engine speed increases from low idle to high idle, the intake vacuum pulls in a negligible percentage of unmetered air relative to total metered air.


$$\Delta\text{Trim} < 0 \quad \left(\text{e.g., drops from } +40\% \text{ to } +5\%\right)$$


$$\Delta\lambda_{\text{chem}} \approx 0 \quad \left(\text{remains stabilized near } 1.0\right)$$


* **The Restricted Fuel Delivery Delta:** As engine speed increases, the fuel volume requirement scales up, but a restricted filter or weak pump cannot keep up.


$$\Delta\text{Trim} > 0 \quad \left(\text{e.g., climbs from } +5\% \text{ to } +50\%\right)$$


$$\Delta\lambda_{\text{chem}} > 0 \quad \left(\text{exhaust gas chemistry shifts sharply lean, } \lambda > 1.15\right)$$



#### B. Catching Carbon Monoxide ($\text{CO}$) vs. Sensor Biases 



If OBDLab reports a normal stoichiometric lambda ($\lambda_{\text{obd}} \approx 1.0$) but GASLab reports a falling chemical lambda ($\lambda_{\text{chem}} < 0.95$), calculating the delta between the two reveals an oxygen sensor that has drifted in its stoichiometric reference.

* $$\Delta\text{Lambda} = \lambda_{\text{chem}} - \lambda_{\text{obd}}$$


* If $\Delta\text{Lambda}$ spikes negative at high idle while $\text{CO}$ emissions climb, it proves the engine is physically running rich because the upstream sensor is lying to the PCM.



---

### 2. Architectural Blueprint under the Strict Isolation Contract

To keep **GASLab** and **OBDLab** completely independent and stateless, they must never calculate these deltas themselves. Instead, the application's sequential data pipeline should adapt to a **multi-frame payload structure**.

#### Phase 1: Streamlit UI (`app.py`) Input Collection

The UI is updated with dual tabs or expanders allowing the user to input:

1. **Low Idle Dataset:** (Gas PIDs, OBD trims, MAP/MAF, and O2 voltages at $\approx 750\text{ RPM}$).
2. **High Idle Dataset:** (Gas PIDs, OBD trims, MAP/MAF, and O2 voltages at $\approx 2500\text{ RPM}$).

#### Phase 2: Dual-Frame Orchestration in `wired/composition.py`

The entry point `diagnose()` executes DNALab, GASLab, OBDLab, and DTCLab **twice** (once for each engine state). It then compiles these translated perceptions into a dual-state `OrchestratorInboundRequest`:

```python
# wired/composition.py (Sole legal composition point)

class StateFrame(BaseModel):
    gas: GasLabPayload        # From GASLab
    obd: OBDLivePayload       # From OBDLab
    dtc: DTCLabPayload        # From DTCLab

class OrchestratorInboundRequest(BaseModel):
    vehicle_dna: VehicleDNA   # From DNALab
    low_idle: StateFrame      # Low RPM state data
    high_idle: StateFrame     # High RPM state data

```

#### Phase 3: Centralized Delta Processing in COMLab

Inside `comlab/`, a dedicated script (e.g., `comlab/analytics/delta_engine.py`) is invoked inside the `perception_contradiction` stage of the pipeline. This script runs strictly mathematical evaluations:

```python
# comlab/analytics/delta_engine.py

def calculate_state_deltas(request: OrchestratorInboundRequest) -> dict:
    # 1. Fuel Trim Delta [1]
    trim_low = request.low_idle.obd.total_trim_correction_delta
    trim_high = request.high_idle.obd.total_trim_correction_delta
    delta_trim = trim_high - trim_low  # consumer: fault_atlas_router

    # 2. Chemical Stoichiometry Delta
    lambda_low = request.low_idle.gas.lambda_chem
    lambda_high = request.high_idle.gas.lambda_chem
    delta_lambda_chem = lambda_high - lambda_low  # consumer: perception_contradiction

    # 3. Volumetric Efficiency / Airflow Delta
    maf_low = request.low_idle.obd.ve_pct if request.low_idle.obd.maf_status == "VALID" else 0.0
    maf_high = request.high_idle.obd.ve_pct if request.high_idle.obd.maf_status == "VALID" else 0.0
    delta_airflow_efficiency = maf_high - maf_low  # consumer: fault_atlas_router

    return {
        "delta_trim": delta_trim,
        "delta_lambda_chem": delta_lambda_chem,
        "delta_airflow_efficiency": delta_airflow_efficiency
    }

```

---

### 3. Impact on the Diagnostics Decision Tree

Once COMLab receives these calculated deltas, the `fault_atlas_router` stage can execute clear logical decisions:

| Delta Pattern | Diagnostic Interpretation | Target Verdict |
| --- | --- | --- |
| $\Delta\text{Trim} \ll 0$ AND $\Delta\text{Lambda}_{\text{chem}} \approx 0$ | Air leak bypassing the throttle body decreases in significance as engine throughput increases.

 | **Intake Vacuum Leak** (Case 1 / Case 19) 

 |
| $\Delta\text{Trim} \gg 0$ AND $\Delta\text{Lambda}_{\text{chem}} > 0$ (Lean) | Inability of fuel delivery system to supply the required volume under high-RPM demand.

 | **Fuel Pressure Drop / Restricted Filter** (Case 2) 

 |
| $\Delta\text{Trim} > 0$ AND $\Delta\text{Airflow}_{\text{efficiency}} < 0$ | MAF sensor under-reporting actual airflow as mass flow rates increase. | **Degraded / Dirty MAF Sensor** (Case 3) 

 |
| $\Delta\text{Lambda}_{\text{chem}} > 0$ (Lean) AND $\Delta\text{Trim} \approx 0$ | The PCM is blind to a physical lean condition occurring strictly at high idle.

 | **Biased / Lazy Upstream O2 Sensor** (Case 18) 

 |

By executing this delta logic in **COMLab**, you preserve the statelessness of your parsing labs, protect the isolation contract, and unlock the exact reasoning patterns required to solve complex real-world driveability failures.