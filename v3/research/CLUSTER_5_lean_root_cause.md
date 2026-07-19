# Research Brief — Cluster 5: Lean-condition root cause (vacuum leak vs fuel delivery vs MAF under-read)

**Provided with:** the *4DLab System Context* document — read it first. This brief assumes it.

### Role ###
You are an automotive fuel-and-air-metering diagnostics expert. Write for an engineer specifying
a diagnostic acquisition protocol. Do not explain basic terms.

**Search note:** "4DLab" is this system's internal name, not a public entity — never web-search it or any "4D lab"; research only the automotive question below.

### The cluster (the confusable set) ###
Within a confirmed **lean** verdict (λ>1.03 / positive trim), separate **where the lean is**:
- **vacuum / intake air leak** (unmetered air);
- **fuel delivery shortfall** (pump, filter, pressure, injectors);
- **MAF under-read** (sensor reports less air than is entering).

4DLab states lean is a "where the lean is" family that **does not separate on a single idle
snapshot**; the proposed discriminator is the **fuel-trim pattern across operating points**.

### Candidate signals to evaluate (critically — keep, replace, or reject each) ###
- **STFT/LTFT across idle vs ~2500 RPM vs load** — the classic split: vacuum leak lean at idle and
  normalizes under load; fuel delivery worsens with load/demand; MAF a characteristic
  low/high-RPM trim signature. Quantify each pattern and its threshold.
- **Architecture pre-gate** (speed-density vs MAF vs forced induction) before applying any trim-
  delta profile — required per the context caveats.
- **Propane / controlled enrichment** response to confirm an unmetered-air leak.
- **Fuel pressure and volume under load**; injector balance test.
- **MAF actual vs calculated airflow** (from MAP/RPM/VE) plausibility.

### Research questions (answer each) ###
1. **Discriminating measurement** — the single measurement, or smallest combination, that most
   reliably separates this cluster. Rank candidates by discriminating power × practicality.
2. **Physical rationale** — the combustion / sensor / measurement mechanism that makes it separate.
3. **Acquisition protocol** — exact procedure and equipment: test maneuver, RPM/load points,
   engine/warm-up state, sampling, number of points, and any architecture pre-gate required.
4. **Expected signature** — the quantitative separator: direction, approximate magnitude, and a
   usable threshold or decision band, with numeric ranges where the literature supports them.
   State uncertainty and the conditions under which it fails.
5. **Feasibility tier** — classify the equipment as (a) generic OBD-II live data / Mode $06,
   (b) the existing 5-gas analyzer used differently (e.g. transient or two-point capture, second
   probe), (c) added shop equipment (pressure transducer, scope, leak/compression tester), or
   (d) lab-only / impractical. Flag anything not obtainable in a normal workshop.
6. **Evidence** — cite authoritative sources and note each source's reliability.

### Required output format ###
1. A ranked answer to question 1 (best discriminator first), each candidate marked
   **kept / replaced / rejected** with the reason.
2. A signature table: candidate × maneuver/point × expected direction & magnitude × threshold ×
   feasibility tier × primary citation.
3. A one-paragraph **bottom line**: the single recommended measurement to add, its feasibility
   tier, and the expected post-add separability — or a plain statement that **no practical
   measurement separates this cluster**, in which case the families should be handled by honest
   abstention.
4. **Open questions / data gaps** where the literature is thin and real-vehicle data collection
   would be needed (with a minimal collection plan).

### Source & evidence standards ###
Prefer SAE standards (J1979 / OBD modes, relevant emissions-test papers), ISO OBD standards,
EPA / CARB I/M and OBD guidance, OEM and professional service literature, and peer-reviewed
combustion/emissions research. For every quantitative threshold, cite the source and mark it
**standardized / manufacturer-typical / empirical-anecdotal**. Distinguish measurement science
from shop folklore; verify claims rather than assuming them.

### Constraints ###
Petrol (spark-ignition) engines only. Focus on **practically-acquirable** signals against the
equipment baseline in the context document; treat lab-only methods as out of scope except to
note them. Be specific and quantitative — name the PID, Mode, maneuver, RPM point, and number,
never "use a scan tool." It is acceptable and useful to conclude that a cluster has **no**
practical discriminator. No preamble; begin with the ranked answer to question 1.
