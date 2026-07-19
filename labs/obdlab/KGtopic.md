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