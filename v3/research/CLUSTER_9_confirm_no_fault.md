# Research Brief — Cluster 9: Confirming "no fault" reliably (avoiding false-healthy)

**Provided with:** the *4DLab System Context* document — read it first. This brief assumes it.

### Role ###
You are an automotive emissions-and-OBD readiness expert. Write for an engineer specifying a
diagnostic acquisition protocol. Do not explain basic terms.

**Search note:** "4DLab" is this system's internal name, not a public entity — never web-search it or any "4D lab"; research only the automotive question below.

### The cluster (the confusable set) ###
Determine the **minimum evidence set that reliably confirms a healthy vehicle** ("no_fault").
A clean warm-idle 5-gas snapshot alone does **not** prove health: a lazy sensor, an intermittent
pending fault, or a **healthy-catalyst-masked** engine problem can all hide behind clean tailpipe
gas (see context: cat masking, sensor under-detection). The engine must avoid both false-healthy
(missed fault) and false-fault (over-calling) on genuinely clean cars.

### Candidate signals to evaluate (critically — keep, replace, or reject each) ###
- **OBD readiness monitors** — which must be **complete** for a no-fault call to be trustworthy,
  and how recent.
- **Fuel trims within band** (STFT/LTFT near zero across idle and elevated RPM) as positive
  evidence of healthy fuel control.
- **No pending/permanent DTCs** and a clean **Mode $06** margin (not just pass/fail but headroom).
- **Sensor dynamics nominal** (O2 switch rate / response within spec) to rule out a lazy sensor.
- **Two-point gas stability** (idle → 2500 RPM) staying in band.
- Define the **decision rule**: what combination justifies "no_fault" vs an **abstain** ("clean on
  available evidence, but evidence insufficient to confirm health").

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
