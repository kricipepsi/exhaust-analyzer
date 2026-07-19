# Research Prompt — Discriminating Measurements for Confusable Engine-Fault Families

*Copy everything below the line into your research tool (deep-research LLM or hand to a domain researcher). It is fully self-contained.*

---

### Role ###
You are an automotive emissions-and-diagnostics measurement expert (combustion, exhaust-gas analysis, OBD-II/SAE J1979, in-shop test protocols). You write for an engineer building a diagnostic engine; assume deep familiarity with 5-gas analysis, fuel trims, lambda, DTCs, freeze frame, and Mode $06. Do not explain basic terms.

### Background / system under study ###
A rule-based engine classifies a petrol vehicle's fault into one fault family from a **single warm-idle measurement set**:

- **5-gas exhaust snapshot at warm idle:** HC (ppm), CO (%), CO2 (%), O2 (%), NOx (ppm) — one steady reading, single sample point, single RPM.
- **OBD-II data, often sparse:** stored DTCs (frequently few or none), and in many cases **no** live fuel trims, **no** freeze frame, and **no** Mode $06 monitor results.

This modality has a proven ceiling: several fault families are **physically indistinguishable** from one warm-idle snapshot because they produce overlapping steady-state gas signatures. Adding rules cannot fix a separation that is absent from the measurement. The goal of this research is to identify **which additional, practically-acquirable measurements would discriminate the specific confusable families below**, so the right discriminating signal can be added to the data-acquisition protocol — not the code.

### Objective ###
For each confusable cluster in the next section, determine the **minimum additional measurement(s)** that reliably separate the listed families, and characterize each so it can be specified as an acquisition requirement. Critically evaluate the candidate signals I list (do not merely confirm them) and surface better or cheaper alternatives where they exist.

### The confusable clusters (the actual failure points) ###

Each cluster lists the families the engine confuses, why a warm-idle 5-gas snapshot fails to separate them, and candidate discriminating signals to evaluate.

**Cluster 1 — Mechanical compression loss vs ignition misfire vs internal coolant intrusion.**
Worn piston rings, worn valve seals, low compression, and internal coolant/head-gasket leaks all raise idle HC and can mimic an ignition misfire (and a misfire DTC such as P0300 is often present for all of them). Separate: mechanical/compression cause vs ignition cause vs oil/coolant intrusion.
Candidate signals: relative compression via starter-current or crank-speed analysis; cylinder leak-down/compression test; **snap-throttle transient HC plume** (valve seals reportedly emit a transient HC spike vs a steady misfire); oil-derived vs fuel-derived HC speciation; coolant-combustion markers in exhaust; per-cylinder Mode $06 misfire counts; in-cylinder pressure.

**Cluster 2 — Rich mixture vs catalyst failure.**
A degraded catalyst and a genuinely rich fuel mixture both shift tailpipe gases and are routinely confused. Separate: fuel-control richness vs catalyst inefficiency.
Candidate signals: **pre-catalyst vs post-catalyst** 5-gas (or upstream vs downstream lambda/O2); catalyst oxygen-storage / light-off test (forced lean-rich perturbation, observe downstream O2 lag); STFT/LTFT (true richness shows in negative trims, catalyst inefficiency does not); Mode $06 catalyst monitor.

**Cluster 3 — ECU / control-module fault (symptom dispersion).**
Control-module faults scatter across lean, rich, sensor, and catalyst classifications because the gas snapshot shows the downstream symptom, not the control-system root cause. Separate: control-system fault from the true gas-chemistry faults it imitates.
Candidate signals: live PID plausibility cross-checks; STFT/LTFT adaptation behavior; control-module supply/ground voltages; freeze-frame correlation; Mode $06; bidirectional actuator response tests.

**Cluster 4 — Exhaust leak vs lean condition vs biased O2 sensor.**
An exhaust leak upstream of the O2 sensor draws in air and reads false-lean, mimicking a true lean condition or a biased sensor. Separate: physical air ingress vs true lean fueling vs sensor bias.
Candidate signals: O2 waveform vs load (a leak's false-lean is load/pulsation dependent); upstream vs downstream probe; exhaust smoke/pressure test; fuel-trim mapped against RPM/load; wideband lambda vs narrowband cross-check.

**Cluster 5 — Lean-condition root cause (vacuum leak vs fuel delivery vs MAF).**
Lean cases that lack discriminating trim/DTC evidence at idle. Separate the lean sub-causes.
Candidate signals: **STFT/LTFT across idle vs ~2500 rpm vs load** (vacuum leak: lean at idle, normalizes under load; fuel delivery: lean worsens with load; MAF: characteristic trim split); propane/fuel-enrichment response; fuel pressure and volume under load.

**Cluster 6 — Sensor fault under-detection (lazy/biased sensor read as "healthy").**
A lazy or biased O2 (or MAF) sensor yields a normal-looking steady reading, so the fault is missed and reported as no-fault. Separate: a degraded sensor from a genuinely healthy one.
Candidate signals: O2 switch rate / cross-counts; forced rich-lean response time (slew rate); MAF actual vs calculated airflow; sensor heater-circuit behavior; Mode $06 oxygen-sensor monitors.

**Cluster 7 — Cam timing / VVT fault.**
Retarded cam timing or VVT failure cannot be expressed in a steady warm-idle gas reading. Separate it from the misfire/sensor families it gets routed to.
Candidate signals: cam-to-crank correlation (P0016-class); VVT solenoid command-vs-response; volumetric-efficiency / MAF-at-RPM signature; P0011/P0014 patterns; idle manifold vacuum stability.

**Cluster 8 — Non-starter.**
A non-starting engine never reaches warm idle, so no idle gas exists. Separate the no-start root causes (compression / fuel / spark / immobilizer).
Candidate signals: cranking RPM and relative compression during crank; fuel pressure/volume at crank; spark presence; injector pulse confirmation; fuel-spark-cut-at-crank freeze-frame; immobilizer/security status; Mode $06.

**Cluster 9 (negative case) — Confirming "no fault" reliably.**
A clean idle 5-gas snapshot alone does not prove a healthy vehicle (a lazy sensor or pending intermittent fault can hide). Determine the **minimum evidence set** that reliably confirms no-fault: e.g., readiness/OBD monitors complete, fuel trims within band, no pending codes, sensor dynamics nominal.

### Research questions (answer each, per cluster) ###
1. **Discriminating measurement:** What single measurement (or smallest combination) most reliably separates the families in this cluster? Rank candidates by discriminating power × practicality.
2. **Physical rationale:** Why does it separate them — the combustion/measurement mechanism.
3. **Acquisition protocol:** Exact procedure and equipment to capture it (test maneuver, RPM/load points, sampling, warm-up state, number of points).
4. **Expected signature:** The quantitative separator — direction, approximate magnitude, and a usable threshold or decision band, with numeric ranges where the literature supports them. State uncertainty.
5. **Feasibility tier:** Classify the equipment needed as (a) generic OBD-II scan tool live data / Mode $06, (b) existing 5-gas analyzer used differently (e.g., transient capture or a second probe), (c) added shop equipment (pressure transducer, scope, leak tester), or (d) lab-only/impractical. Flag anything not obtainable in a normal workshop.
6. **Evidence:** Cite authoritative sources (see standards below) and note each source's reliability.

### Required output format ###
1. **Per-cluster sections** (one per cluster 1-9), each answering the six research questions, with the candidate signals evaluated explicitly (kept / replaced / rejected, and why).
2. **Master discrimination matrix** — table: rows = clusters; columns = recommended measurement, feasibility tier, expected separator/threshold, primary citation.
3. **Minimum added-signal set** — the shortest list of new acquisitions that unblocks the most clusters for the least new equipment (e.g., "enable live STFT/LTFT + a standardized snap-throttle transient capture" unlocks clusters X, Y, Z). Rank by clusters-unblocked-per-cost.
4. **Open questions / data gaps** — where the literature is thin and real-vehicle data collection would be required, with a suggested minimal data-collection plan.

### Source & evidence standards ###
- Prefer: SAE standards (e.g., J1979 / OBD modes, relevant emissions test SAE papers), ISO OBD standards, EPA/CARB I/M and OBD guidance, OEM/professional service literature, and peer-reviewed combustion/emissions research.
- For every quantitative threshold, cite the source and note whether it is standardized, manufacturer-typical, or empirical/anecdotal.
- Distinguish established measurement science from shop folklore; flag claims that lack solid backing (e.g., verify the "valve-seal transient HC plume" claim against real evidence rather than assuming it).

### Constraints ###
- Focus on **petrol** engines and **practically acquirable** signals; treat lab-only methods as out of scope except to note them.
- Be specific and quantitative; avoid generic advice ("use a scan tool"). Name the PID, mode, maneuver, and number.
- It is acceptable to conclude that a given cluster has **no** practical discriminating measurement — if so, say so plainly and explain why, so those families can be handled by honest abstention rather than a false signal.
- No preamble or pleasantries; begin with the first cluster.
