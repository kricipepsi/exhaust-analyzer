Your architectural assessment is **100% correct**. In a strict parallel execution model where the input data is sliced and routed to individual labs simultaneously, the individual labs (GASLab, OBDLab, and DTCLab) operate as isolated black boxes. They have no awareness of each other's concurrent discoveries.

For instance:

* **GASLab** translates exhaust gas chemistry into a raw stoichiometric index ($\text{lambda}_{\text{chem}}$ or $\lambda_{\text{chem}}$) without knowing if DTCLab has flagged a cylinder misfire DTC.


* **OBDLab** translates fuel trim percentages and sensor voltages without knowing if GASLab has flagged high carbon monoxide (CO) emissions.


* **DTCLab** sanitizes diagnostic codes without knowing whether OBDLab’s PID stream reports a fully warmed-up engine.



If the individual labs were responsible for outputting the final diagnostics on their own, **they would be unable to cross-reference data**, leading to frequent false positives, missed contradictions, and inaccurate diagnoses.

Here is an analysis of how this limitation is resolved, how the 20 real-world cases depend on cross-referencing, and the ideal data flow to handle this within the application.

---

### How the Architecture Resolves This: Downstream Centralized Fusion

The system solves the cross-referencing problem by utilizing a **Downstream Centralized Data Fusion Model**. Instead of forcing the labs to communicate with one another—which would violate the isolation contract and create chaotic cyclic dependencies—the individual labs are stripped of diagnostic decision-making power.

They are designed purely as **stateless translators** that output structured intermediate "perceptions" :

1. **GASLab** translates raw chemical PPM/percentage values into localized stoichiometry ($\lambda_{\text{chem}}$).


2. **OBDLab** translates raw PIDs into standardized sensor statuses, volumetric efficiency percentages, and fuel trim deltas.


3. **DTCLab** sanitizes the raw DTC fault codes and freeze frame profiles.



The actual **cross-referencing, correlation, and contradiction analysis** is deferred entirely to **COMLab** (the "Central Brain") during its sequential decision pipeline :

$$\text{Stage A Gates} \rightarrow \text{Perception Contradiction} \rightarrow \text{Fault Atlas Routing} \rightarrow \text{Family Verdict} \rightarrow \text{Output Assembly}$$

---

### Concrete Case Examples: Why Cross-Referencing is Mandatory

Without COMLab cross-referencing the translated payloads downstream, several of our studied cases would result in diagnostic failure:

#### 1. Case 12: Cylinder 1 Ignition Coil Primary Failure (P0351 / P0301)

* **The isolated lab view:**
* **OBDLab** detects that the upstream oxygen sensor voltage is low and STFT is at $+14\%$. Without context, this points to a lean fuel-delivery issue.


* **DTCLab** sanitizes and outputs active DTCs P0351 and P0301.




* **The COMLab cross-reference:** COMLab receives both payloads. Its `fault_atlas_router` cross-references the active ignition circuit fault with the lean trim behavior. It applies logic: *If an ignition misfire is present, the oxygen sensor reading is a "false lean" caused by unburned oxygen exiting the cylinder, not a fuel-delivery deficit*. COMLab suppresses the lean fuel-routing logic and targets the ignition coil primary circuit.



#### 2. Case 16: Stuck-Open Canister Purge Valve (P0446 / P1450)

* **The isolated lab view:**
* **DTCLab** sanitizes P0446 (generically defined as a rear vent control circuit fault).


* **OBDLab** detects highly negative fuel trims (STFT/LTFT at $-25\%$).


* **GASLab** translates gas readings into an extremely rich chemical state.




* **The COMLab cross-reference:** COMLab pulls the vehicle's configuration from the DNALab payload (e.g., 2014 Ford Focus 2.0L GDI). It cross-references the P0446 code with the rich running condition (negative fuel trims and rich gas readings). Knowing the vehicle's topology, COMLab correctly overrides the generic "vent valve" definition and pinpoints the root cause as a stuck-open engine-bay canister purge valve.



---

### The Ideal Diagnostic Data Flow

To ensure complete cross-referencing while strictly maintaining the isolation of individual labs, the application should execute the following optimized, four-phase sequential pipeline:

```
                  ┌──────────────────────────────┐
                  │       User Raw Inputs        │
                  │  (Gas, OBD PIDs, DTCs, VIN)  │
                  └──────────────┬───────────────┘
                                 │
                                 ▼
                            (Phase 1: Identity & Topology)
                                 │
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
                               (Phase 2: Translation)
 (Gas -> Chem State)    (PIDs -> Trim/Sensors)  (DTCs -> Sanitized Faults)
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                                 ▼
                     [ Orchestrator Inbound ]  (Phase 3: Payload Assembly)
                                 │
                                 ▼
                           [ COMLab ]  (Phase 4: Reasoning & Cross-Reference)
                                 │
                                 ▼
                    

```

#### Phase 1: Identity & Topology Resolution (DNALab)

* **Input:** Raw VIN and basic user triage data.


* **Process:** Resolves the VIN to build a master `VehicleDNA` payload. This establishes the vehicle configuration: engine displacement, aspiration, fuel system type (GDI vs. Port), catalytic converter topology, oxygen sensor configuration, and emissions tier (e.g., Euro 4 vs. Euro 6).


* **Output:** This master DNA is projected into slim, targeted views (e.g., `ObdLabDnaView`) to serve as context for the downstream translation labs.



#### Phase 2: Parallel Perceptual Translation (GASLab, OBDLab, DTCLab)

Using the vehicle configuration as a baseline context, the translation labs process their respective raw inputs in parallel :

* **GASLab:** Evaluates raw gas percentages (`co`, `co2`, `o2`, `hc`, `nox`) against the resolved emissions standard to output a verified stoichiometric chemical lambda ($\lambda_{\text{chem}}$).


* **OBDLab:** Consumes raw PIDs (such as coolant temperature, RPM, and MAF/MAP) to derive engine thermal states, volumetric efficiency (`ve_pct`), and total fuel trim corrections.


* **DTCLab:** Filters raw fault codes, cross-references freeze-frame variables, and verifies sensor parameters.



#### Phase 3: Typed Payload Assembly (`OrchestratorInboundRequest`)

The composition layer aggregates the outputs from all three translation labs into a single, comprehensive `OrchestratorInboundRequest`. **This is the step that packages all raw, isolated perceptions together for cross-referencing**.

#### Phase 4: Centralized Reasoning and Decision Making (COMLab)

COMLab processes the inbound request through its reasoning stages, resolving the isolated variables :

* **Perception Contradiction:** Compares OBDLab's reported sensor-calculated lambda against GASLab's measured chemical tailpipe lambda. A discrepancy (e.g., OBD reports stoichiometric lambda $\lambda = 1.0$ while the tailpipe shows a lean $\lambda = 1.15$) immediately exposes a cracked exhaust manifold, false sensor readings, or a biased oxygen sensor.


* **Fault Atlas Routing:** Weighs evidence across all inputs. If OBDLab reports fuel trims are pinned rich but DTCLab shows no codes, and GASLab shows an elevated chemical lambda, it routes the fault specifically to a failing mechanical component (e.g., a leaking intake manifold gasket) rather than an electrical sensor circuit.


* **Family Verdict:** Combines the findings to issue a precise root-cause diagnostic verdict and generate target validation test recommendations.



### Why This is Better Than Allowing Labs to Talk to Each Other

Allowing individual labs to directly import or query other labs during execution would introduce tight code coupling and cyclic dependencies, making the system incredibly fragile and difficult to test.

Keeping the labs as **stateless translators** and utilizing **COMLab as a centralized, downstream broker** ensures clean, modular code while fully enabling the complex cross-referencing required to solve advanced automotive diagnostic cases.

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


The reason **DTCLab**, **OBDLab**, and **GASLab** require an internal knowledge graph or ontology—despite ultimately outputting clean, standardized payloads—lies in the difference between **syntactic data** (raw numbers and strings) and **semantic information** (what those numbers and strings actually *mean* in a physical system).

To output simple, structured data like `o2_failure_mode = BIASED_RICH` or `chemical_state = COMBUSTION_FAIL`, these labs cannot rely on simple flat tables or basic `if/else` statements. They must internally traverse a network of relationships, rules, and causal dependencies.

Here is a detailed breakdown of why these individual labs must use a knowledge graph and ontology to produce their basic outputs.

---

### 1. Translating Raw Metrics into Semantic Concepts (Ontological Alignment)

A raw measurement is completely meaningless without its structural context. For example, if the user inputs a raw voltage of $0.1\text{ V}$ for an oxygen sensor, that is just a float.

To translate this float into a semantic state, OBDLab must consult its internal ontology:

* **What is the sensor's physical configuration?** Is it a Narrowband sensor (switching $0.1\text{ V}$ to $0.9\text{ V}$) or a Wideband Air/Fuel ratio sensor ($3.0\text{ V}$ to $3.3\text{ V}$ equivalent)?
* **What is its spatial location?** Is it Bank 1 Sensor 1 (upstream feedback control) or Bank 1 Sensor 2 (downstream catalyst monitor)?
* **What are the downstream dependencies?** On newer platforms, a downstream sensor is actively used for rear fuel trim feedback. On older platforms, it is strictly a passive catalyst efficiency checker.



By running these inputs through an internal ontology, OBDLab translates a raw, chaotic voltage into a precise, typed concept (e.g., `o2_failure_mode = LAZY_SWITCHING` or `trim_analytics_gate = SUPPRESS_LEARNED`). **The ontology defines the rules of interpretation, and the graph resolves the spatial/physical relationships of that specific engine layout.**

---

### 2. Resolving Causal Hierarchies and "Companion" Codes (DTCLab)

If DTCLab acted as a flat, stateless list parser, it would pass a raw, unorganized array of codes (e.g., `["P0351", "P0301", "P0171", "P0420"]`) to COMLab. This flat list forces the central brain to figure out how they relate.

Instead, DTCLab uses an internal **Diagnostic Trouble Code Ontology** to build a directed, causal sub-graph:

$$\text{P0351 (Ignition Coil Circuit Fault)} \xrightarrow{\text{causes}} \text{P0301 (Cylinder 1 Misfire)} \xrightarrow{\text{causes}} \text{P0171 (System Too Lean due to excess O}_2\text{)}$$

Using this internal hierarchy:

* DTCLab instantly recognizes that **P0351** is an *electrical circuit fault* (high-priority, primary cause).


* It identifies **P0301** as a *combustion performance failure* (direct physical consequence).


* It identifies **P0171** as a *feedback logic response* (a secondary, systemic symptom).



Because DTCLab has this relational knowledge, it can group, prioritize, and sanitize these codes. It outputs a clean payload to COMLab that explicitly flags **P0351** as the root trigger, preventing COMLab from chasing a false lean fuel delivery problem.

---

### 3. Dynamic Graph Pruning Based on Vehicle DNA

Modern vehicle platforms are highly heterogeneous. Hardcoding different parsing logic for every single engine configuration makes software incredibly fragile and difficult to maintain.

Using a knowledge graph allows the individual labs to dynamically "prune" or alter their evaluation pathways at runtime based on the resolved `VehicleDNA`:

* **For a Speed-Density engine:** OBDLab's load-calculation subgraph activates the relationships connecting `MAP` + `IAT` $\rightarrow$ `Air Density` $\rightarrow$ `Target Injection Pulse Width`.


* **For a Mass Air Flow engine:** OBDLab's load-calculation subgraph bypasses the manifold pressure equations and maps `MAF frequency/voltage` directly to metered air mass.



Rather than writing thousands of lines of conditional code, the lab simply loads the vehicle's structural template into its local graph, runs a standard graph-lookup (`$graphLookup` or similar traversal), and executes the relevant calculation paths. The output remains basic data, but the mechanism to derive it is highly dynamic and flexible.

---

### 4. Distinguishing Chemical Causality vs. Sensor Faults (GASLab)

GASLab's job is to convert raw tailpipe gas percentages (`co`, `co2`, `o2`, `hc`, `nox`) into a stoichiometric index ($\lambda_{\text{chem}}$) and a chemical state. Doing this accurately requires an internal understanding of combustion chemistry.

For instance, if the analyzer reads high Hydrocarbons (HC) and high Oxygen ($O_2$) simultaneously, a naive calculator might conclude the engine is running both rich (high HC) and lean (high $O_2$).

GASLab's internal chemical ontology resolves this apparent contradiction using causal logic :

* *Rule:* Unburned fuel (HC) and unused oxygen ($O_2$) exiting the tailpipe together is the distinct chemical signature of a **misfire** (combustion failure), not a fueling ratio error.


* *Causal Path:* No spark/compression $\implies$ Air-fuel mixture does not ignite $\implies$ Both raw fuel (HC) and fresh air ($O_2$) are pumped directly into the exhaust.



GASLab uses this internal chemical relationship graph to resolve the raw, conflicting PPM values. It outputs a clean, synthesized state (`chemical_state = COMBUSTION_FAIL`), saving COMLab from receiving contradictory, raw chemical conflicts.

---

### Summary: The Division of Labor

The architectural separation of concerns relies on this exact design:

```
 ──> [Lab Ontologies & Local Graphs] ──> ──>
   (Voltages,          (Translates raw metrics             (Standardized, typed           (Cross-references deltas,
   PPMs, DTCs)          into physical meaning)               conceptual data)              resolves root-cause verdict)

```

The parsing labs (GAS, OBD, DTC) use **local knowledge graphs** to translate raw, messy metrics into standardized, high-level "perceptions". **COMLab** then uses a **system-level causality graph** to cross-reference these perceptions, analyze their transitions (deltas) between low and high idle, and output the final diagnostic verdict. This keeps your code modular, highly scalable, and capable of diagnosing complex driveability failures with absolute precision.