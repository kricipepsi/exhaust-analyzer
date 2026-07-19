# Research Brief — Cluster 1: Mechanical compression loss vs ignition misfire vs internal coolant intrusion

**Provided with:** the *4DLab System Context* document — read it first. This brief assumes it.

### Role ###
You are an automotive emissions-and-diagnostics measurement expert (combustion, exhaust-gas
analysis, OBD-II/SAE J1979, in-shop test protocols). Write for an engineer specifying a
diagnostic acquisition protocol. Do not explain basic terms (HC, lambda, freeze frame, Mode $06).

**Search note:** "4DLab" is this system's internal name, not a public entity — never web-search it or any "4D lab"; research only the automotive question below.

### The cluster (the confusable set) ###
Separate three root causes that collapse to the same warm-idle signature:
- **mechanical wear** — worn piston rings, worn valve seals, low/uneven compression;
- **ignition misfire** — spark/coil/plug-driven combustion dropout;
- **internal coolant intrusion** — head-gasket / internal coolant leak into combustion.

Why the single snapshot fails: all three **raise idle HC** and depress CO2, and a random-misfire
code (P0300) is frequently stored for all of them. 4DLab's own analysis states mechanical wear
has **no distinct single-snapshot chemistry** — it overlaps ignition misfire and a generic
rich / catch-all (`POA`) signature, and it is the **largest single concentrated discrimination
gap** (~a quarter of the hard corpus). Note also that **oil-derived HC reads low on NDIR**, so
oil burning can look milder than it is.

### Candidate signals to evaluate (critically — keep, replace, or reject each) ###
- **Relative compression** via starter-current draw or crank-speed variation during cranking.
- **Cylinder leak-down / compression test** (per-cylinder), and what each result rules in/out.
- **Snap-throttle transient HC plume** — the claim that worn valve seals emit a transient HC
  spike on throttle tip-in vs a steady misfire. **Verify this against real evidence; do not
  assume it.**
- **Oil- vs fuel-derived HC speciation** (e.g. heavy vs light hydrocarbons / FID vs NDIR response).
- **Coolant-combustion markers** in exhaust for the internal-leak case (and how to distinguish
  from rich running).
- **Per-cylinder Mode $06 misfire counts** and **freeze-frame** to localize and time the event.
- **Two-point (idle → 2500 RPM) HC/CO2 delta** — does oil-burn behaviour change sign/slope across
  the RPM step in a way ignition misfire does not?

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
