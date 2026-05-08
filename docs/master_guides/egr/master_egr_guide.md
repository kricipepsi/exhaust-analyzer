# Master EGR Guide — 4D Petrol Diagnostic Engine

**Purpose.** A single, self-contained reference for Exhaust Gas Recirculation (EGR) on petrol engines — the physics of NOx reduction, how the valve strategy maps to the operating envelope, the canonical gas-analyser signatures for every EGR fault state, the physical justification for every threshold the 4D engine uses in the `stuck_egr_open`, `stuck_egr_open_confirmed`, `egr_dilution_pattern`, and `dual_egr_recovery_pattern` KG nodes, and the DTC-to-cause mapping for the P0400–P0408 family. Rows in the CSV that cite EGR as the expected fault cite the rules below.

---

## 1. What EGR does — the three physical effects

EGR reduces NOx formation by recirculating a metered portion of inert exhaust gas into the intake charge. The physical mechanism is threefold:

**Dilution effect (dominant):** Exhaust gas — primarily CO₂, H₂O, and N₂ — displaces atmospheric oxygen in the intake charge. Less oxygen per unit volume reduces peak flame temperature, which is the primary driver of NOx formation. A stuck-open EGR valve at idle reduces volumetric efficiency from nominal to 60–70 % or lower, crowding out oxygen with inert nitrogen.

**Thermal effect:** Triatomic molecules (CO₂, H₂O) have high specific heat capacity. The diluted charge absorbs more energy for the same temperature rise, suppressing peak combustion temperature by approximately 150 °C. This is the physical basis for EGR preventing the ~1370 °C threshold where atmospheric nitrogen becomes reactive and forms NOx (N₂ + O₂ → 2 NO above this temperature).

**Chemical effect (minor):** CO₂ and H₂O can participate marginally in combustion chemistry, contributing a smaller additional NOx reduction. EGR rates of 5–15 % at cruise and up to ~90 % at warm idle reduce NOx effectively; beyond ~25 % EGR, HC and CO emissions begin to deteriorate sharply. Fuel economy peaks at 8–15 % EGR rate at cruise load.

---

## 2. EGR operating strategy — when it opens and closes

EGR is never active across the full operating envelope. The strategy is precisely the opposite of what many technicians assume:

| Operating condition | EGR valve state | Physical reason |
|---------------------|-----------------|-----------------|
| **Cold start / cranking** | Closed | Engine needs maximum combustibility; cold ECT inhibits EGR. Cold ECT gate typically: ECT < 40 °C → EGR disabled. |
| **Warm idle** | **Up to ~90 % open** | Low cylinder charge density — a large fraction of inert gas can be tolerated without misfire. This is where NOx would otherwise spike due to low exhaust scavenging. |
| **Part-throttle cruise** | Modulated open (5–20 %) | Maintains target NOx reduction while balancing driveability. |
| **WOT / high load** | Closed | Engine needs maximum oxygen for power; EGR would displace charge and reduce output. |
| **Decel (closed throttle)** | Closed | No combustion occurring; EGR irrelevant. |
| **High-RPM snap-throttle** | Closed or transitioning | Manifold vacuum drops; EGR valve may not physically open far enough. |

**The single most important rule for the 4D engine:** A stuck-open EGR valve produces its worst symptoms **at warm idle, not under load.** This is the direct opposite of a vacuum leak from a disconnected hose, which becomes less significant at higher RPM. A stuck-open EGR is an internal vacuum leak through the EGR passage admitting *inert exhaust gas* (not fresh air) into the intake.

---

## 3. EGR valve types in petrol engines (1990–2020)

| Type | Era | Control | Position feedback | Key failure modes |
|------|-----|---------|-------------------|-------------------|
| **Ported vacuum EGR** | 1973–1980s | Venturi vacuum signal, modulated by thermal vacuum switch | None | Carbon clogging; diaphragm rupture; thermal switch failure |
| **Positive backpressure EGR** | 1973–present | Exhaust backpressure modulates vacuum signal | None | Backpressure valve stuck; diaphragm leak; carbon blockage |
| **PWM electronic EGR** | Early 1980s–2000s | ECU pulses solenoid; no feedback | None typically | Solenoid coil open/short; pintle carbon-stuck open |
| **Digital electronic EGR** | Late 1980s–1990s | 3 solenoid valves; ECU opens in binary steps | None | Any one solenoid stuck; carbon on seat |
| **Linear electronic EGR** | Early 1990s–present | ECU drives stepper motor or PWM solenoid with position feedback | Hall-effect or potentiometer sensor | Motor failure; position sensor drift; carbon on pintle/seat |
| **VVT internal EGR** | Late 1990s–present | Exhaust-valve closing timing retains residual gas internally | Cam position sensor | VVT solenoid failure, sludge; phaser lock — covered by `master_mechanical_guide.md §9` |

On VVT-equipped engines without an external EGR valve, EGR DTCs will not exist; misfire-like symptoms attributed to "EGR stuck open" are actually VVT-strategy failures — route to `master_mechanical_guide.md §9`.

---

## 4. Gas signatures — the four canonical EGR fault states

#### 4.1 Normal EGR operation (warm idle, valve partially open)

| HC | CO | CO₂ | O₂ | λ | NOx |
|----|-----|------|-----|-----|------|
| Slightly elevated (50–150 ppm) | Normal | Slightly reduced (12–14 %) | Slightly elevated (1–2 %) | ≈1.00 | Low — dilution cooling suppresses NOx |

The inert exhaust gas displaces oxygen, so O₂ rises slightly and CO₂ falls slightly. HC may rise mildly because the diluted charge burns slightly slower. **This is normal — do not flag as a fault.**

#### 4.2 EGR stuck open at idle (worst case)

| HC | CO | CO₂ | O₂ | λ | NOx |
|----|-----|------|-----|-----|------|
| **300–1500+ ppm** | Normal to low | **8–12 %** | **3–8 %** | ≈1.00 (balanced) | **Very low — inert gas quenches peak temp** |

**Physical mechanism:** Excessive inert exhaust gas displaces intake oxygen beyond the lean combustion limit. HC spikes because raw fuel passes through unburned. O₂ reads high because the diluted charge leaves unreacted oxygen. λ stays near 1.00 because the fuel and air remain in approximate balance — both enter, both partially exit. CO stays low because the mixture is not rich, it is *diluted* to the point of lean misfire while lambda balance is preserved.

**Critical splitter — vacuum leak vs EGR stuck open:**

| Signal | Vacuum leak (fresh air) | EGR stuck open (inert gas) |
|--------|------------------------|---------------------------|
| Tailpipe O₂ | Elevated (3–8 %) | Elevated (3–8 %) |
| Fuel trim | Sharply positive at idle, normalises at cruise | **Near normal on MAF systems** (inert gas not metered by MAF, no O₂ sensor lean shift) |
| Tailpipe CO₂ | Depressed (leak dilutes with 0 % CO₂ air) | More severely depressed (exhaust gas is ~14 % CO₂ but mixes to lower the "total" reading) |
| NOx | Often elevated if lean misfire heats the chamber | **Suppressed** — inert gas quench prevents NOx formation |
| 2500 RPM test | Improves dramatically (leak effect shrinks at higher MAP) | **Also improves** — EGR closes at WOT/high load; this is the dual-speed pattern |

**The trap for MAF-based systems:** Excessive EGR has little or no effect on fuel trim because the inert gas does not change the O₂ concentration in a way the narrowband O₂ sensor interprets as "lean." A stuck-open EGR can cause severe misfire with fuel trims appearing *normal* — the engine must explicitly guard against this.

**Vacuum gauge cross-check:** A stuck-open EGR valve also manifests as **steady manifold vacuum below 15 inHg at warm idle** (normal is 17–22 inHg). Inert exhaust gas displacing fresh intake charge reduces volumetric efficiency, pulling vacuum down. This vacuum reading provides an independent, non-DTC confirmation of stuck-open EGR. Cross-ref `master_mechanical_guide.md §3` (vacuum gauge interpretation) and `§3.2` (backpressure limits).

#### 4.3 EGR stuck closed (all load conditions)

| HC | CO | CO₂ | O₂ | λ | NOx |
|----|-----|------|-----|-----|------|
| Normal | Normal | Normal | Normal | ≈1.00 | **High at idle and under load (5-gas only)** |

On a 4-gas analyser, EGR stuck closed is **invisible to gas analysis** — the engine must rely on DTCs (P0401) or the user reporting spark knock at light throttle. On a 5-gas analyser, idle NOx > 150 ppm with otherwise normal gases points strongly to EGR stuck closed or insufficient flow. Cross-reference `master_nox_guide.md §3` for the NOx-temperature relationship.

#### 4.4 EGR insufficient flow (P0401)

Same gas signature as stuck closed — normal HC/CO/CO₂/O₂ with elevated NOx. The ECM detects insufficient flow when the expected MAP/MAF change on EGR command is absent. The gas analysis cannot distinguish "stuck closed" from "coked passage with zero flow."

---

## 5. Physical justification for the 4D engine thresholds

#### 5.1 HC_min = 300 ppm (DTC-assisted EGR stuck-open node)

**Physical basis:** At warm idle with a functioning three-way catalyst, a healthy petrol engine produces HC ≤ 50 ppm at the tailpipe. Mild combustion inefficiency raises this to 100–150 ppm. The 300 ppm threshold is set deliberately above the "normal but imperfect" band:

- Normal idle HC: ≤ 50 ppm (with cat), ≤ 250 ppm (no cat)
- Marginal combustion (ageing engine, ageing cat): 50–250 ppm
- **300+ ppm: measurably incomplete combustion** — consistent with charge dilution from stuck-open EGR, lean misfire, or ignition fault

At 300 ppm HC, roughly 1.5 % of fuel is passing through unburned. This is the minimal level where a dilution-related combustion deficit is distinguishable from normal variance. The engine gates this on warm engine (ECT ≥ 70 °C) because cold-start enrichment legitimately produces HC in the 200–600 ppm range per `master_cold_start_guide.md §4`.

#### 5.2 O2_min = 2.0 % (DTC-assisted EGR stuck-open node)

**Physical basis:**

- Below 2.0 % O₂ at warm idle: consistent with healthy combustion, mild lean condition, or vacuum leak the ECU is compensating for
- **Above 2.0 % O₂ at warm idle:** too much oxygen is exiting the cylinder — the charge is diluted (EGR), has a significant vacuum leak beyond trim compensation, or has a misfire

The 2.0 % value is intentionally placed above the healthy-no-cat boundary of 1.5 % but below the classic lean-misfire threshold of ~4 %. At 2.0–3.0 % O₂ with normal λ and no positive fuel trim (because the narrowband O₂ sensor doesn't see the inert gas as lean), the stuck-open EGR hypothesis gains probability.

#### 5.3 CO2_max = 13.0 % (DTC-assisted node)

**Physical basis:** At warm idle with healthy combustion, CO₂ is 13–15.5 % (lower without catalyst). EGR dilution by inert gas depresses CO₂ because the exhaust-gas fraction of the intake charge lowers the CO₂ partial pressure. Below 13 % CO₂ at warm idle with normal lambda, a dilution source is active. Above 13 % CO₂, the dilution effect is too mild to be definitively EGR-related (normal combustion).

#### 5.4 Why these thresholds MUST co-occur with a supporting DTC

HC 300+ ppm + O₂ 2.0+ % + λ ≈ 1.00 without a DTC is diagnostically ambiguous — it could equally be an ignition misfire per `master_ignition_guide.md §6`. The distinguishing factor without a DTC is **fuel trim behaviour**: ignition misfire produces positive fuel trim (O₂ sensor sees unburned oxygen), while EGR stuck-open on a MAF system produces little or no trim change. Without an EGR-specific DTC (P0401, P0402, P0404), the engine should surface `insufficient_evidence` rather than default to `egr_fault`.

#### 5.5 Dual-speed EGR pattern — why the 2500 RPM test resolves it

The `dual_egr_recovery_pattern` fires when idle shows HC↑/O₂↑/CO₂↓ but 2500 RPM shows improvement. Physical basis: at 2500 RPM the ECU ramps load above the EGR open window — even a stuck-open valve sees reduced manifold vacuum, reducing flow. The O₂ sensor now sees cleaner combustion and the trims return toward zero. This is the reliable differentiator from a true vacuum leak (which may still show some improvement at 2500 but typically not the dramatic recovery seen with EGR).

#### 5.6 Threshold provenance summary — every EGR threshold cited

This table maps every numeric threshold the 4D engine uses for EGR nodes to its physical justification section in this guide and to the underlying master-guide source chain:

| Threshold | Value | 4D engine node(s) | Physical justification | Source guide § |
|-----------|-------|-------------------|----------------------|----------------|
| `HC_min_stuck_open` | 300 ppm | `stuck_egr_open`, `stuck_egr_open_confirmed` | Combustion deficit at ~1.5% unburned fuel; §5.1 | `master_egr_guide.md §5.1` |
| `O2_min_stuck_open` | 2.0 % | `stuck_egr_open`, `stuck_egr_open_confirmed` | Above healthy-no-cat boundary, below lean-misfire threshold; §5.2 | `master_egr_guide.md §5.2` |
| `CO2_max_stuck_open` | 13.0 % | `stuck_egr_open`, `stuck_egr_open_confirmed` | CO₂ partial pressure depressed by inert dilution; §5.3 | `master_egr_guide.md §5.3` |
| `lambda_balance_window` | 0.97–1.03 | All EGR stuck-open nodes | λ stays near stoichiometric during inert dilution; §4.2 | `master_egr_guide.md §4.2` |
| `NOx_max_idle_normal_egr` | 150 ppm | `egr_insufficient_flow` | Idle NOx with otherwise normal gases = EGR absent; §4.3 | `master_nox_guide.md §2`, `master_egr_guide.md §4.3` |
| `ect_warm_gate` | 70 °C | All EGR nodes | Cold enrichment produces HC 200–600 ppm; §5.1 | `master_cold_start_guide.md §4` |
| `ect_cold_disable` | 40 °C | EGR valve operation | ECT below 40 °C: EGR disabled for combustibility; §2 table | `master_egr_guide.md §2` |
| `vacuum_egr_stuck_open` | < 15 inHg | `stuck_egr_open_confirmed` | Steady warm-idle vacuum below 15 inHg with EGR DTC; §4.2 | `master_mechanical_guide.md §3` |

**Citation format rule:** In `thresholds.yaml`, each row references the "Source guide §" column above as `# source_guide: docs/master_guides/egr/master_egr_guide.md §5.1` (or equivalent). This satisfies R10 provenance lint.

#### 5.7 Era-specific EGR threshold nuance

EGR architectures and sensitivity change across the four era buckets defined by R6. The thresholds above remain correct across all eras, but the *diagnostic weight* of each signal shifts:

| Era | EGR architecture | Dominant signal | Caveat |
|-----|-----------------|-----------------|--------|
| **1990–1995** | Ported vacuum / positive backpressure only | DTCs may be absent (pre-OBD-II); gas sigs carry nearly full weight | EGR position sensor absent — valve failure inferred from gas alone |
| **1996–2005** | PWM electronic + first linear types | P040x DTCs present; gas sigs used as confirmation layer | ECU P0401 monitor tests MAP change on EGR command — MAF-based only after ~1999 |
| **2006–2015** | Linear electronic position-feedback | DTC (full P040x family) + position sensor PID + gas sigs in triple-confirmation | Position sensor drift (P0405/P0406) may fire without gas disturbance |
| **2016–2020** | VVT internal EGR dominant; external EGR valve rare on GDI | May lack external EGR valve entirely; VVT phaser data replaces traditional EGR signals | Route to `master_mechanical_guide.md §9` for internal EGR; P040x DTCs expected absent on GDI |

**1990–1995 pre-OBD-II special case:** Vehicles without EGR position feedback and without DTCs require the 4D engine to place greater weight on the gas signature (HC > 300 ppm + O₂ > 2.0 % + λ ≈ 1.00) because no ECM-confirmed DTC exists. The `stuck_egr_open` node may fire on gas alone in this era. For all other eras, the `stuck_egr_open_confirmed` node requires co-occurring DTC evidence per §5.4.

---

## 6. EGR DTC reference for petrol engines

| DTC | Definition | Diagnostic trigger | Gas signature correlate |
|-----|-----------|-------------------|------------------------|
| **P0400** | EGR Flow Malfunction | Generic flow fault | Variable |
| **P0401** | EGR Flow Insufficient | MAP/MAF change on EGR command below threshold | Normal gases; elevated NOx; may knock at light throttle |
| **P0402** | EGR Flow Excessive | MAP/MAF or DPFE reading above threshold | HC high, O₂ high at idle; rough idle; possible P0300 |
| **P0403** | EGR Circuit Malfunction | Solenoid or motor circuit open/short | EGR valve inoperative |
| **P0404** | EGR Circuit Range/Performance | Position feedback disagrees with commanded position | Variable |
| **P0405/P0406** | EGR Position Sensor Low/High | Sensor voltage out of calibrated range | — |
| **P0407/P0408** | EGR Sensor B Circuit Low/High | Second position sensor out of range | — |

---

## 7. Diagnostic decision tree

1. **Is there a relevant EGR DTC (P0401–P0408)?** → Proceed to gas analysis with EGR as the confirmed hypothesis.
2. **At warm idle: O₂ > 2.0 % AND HC > 300 ppm AND λ ≈ 1.00 AND fuel trims near normal?** → Strong evidence for stuck-open EGR (on MAF system) or ignition misfire. Disambiguate: apply vacuum to EGR valve at idle — if RPM drops severely or engine stalls, the EGR passage is clear and the valve was held closed; the problem is elsewhere. If RPM improves on vacuum application, the valve was stuck open.
3. **At warm idle: O₂ normal AND HC normal AND NOx elevated (5-gas only)?** → EGR stuck closed or insufficient flow. Check P0401.
4. **2500 RPM test improves HC and O₂ dramatically from the idle readings?** → `dual_egr_recovery_pattern` fires; strong confirmation of EGR stuck-open vs vacuum leak which would not improve as dramatically.
5. **VVT-equipped engine with no external EGR valve?** → EGR is performed internally by valve-timing strategy. EGR DTCs will not exist. Misfire-like symptoms are VVT-related — route to `master_mechanical_guide.md §9`.

#### 7a. Era-specific diagnostic flow for EGR

The diagnostic decision tree above assumes a vehicle with an external EGR valve and OBD-II DTCs. For pre-OBD-II and VVT-only vehicles, use these era-adapted flows:

**1990–1995 (pre-OBD-II):**
1. **Warm idle gas analysis is the primary tool.** No P040x DTCs exist.
2. **HC > 300 ppm + O₂ > 2.0 % + λ ≈ 1.00 at warm idle** → stuck-open EGR is the leading hypothesis. Apply vacuum to EGR valve at idle:
   - RPM drops or stalls → EGR passage clear, valve was closed; problem is elsewhere
   - RPM improves or unchanged → EGR valve was stuck open or already partially open
3. **Vacuum gauge reading:** Steady vacuum < 15 inHg reinforces stuck-open EGR.
4. **2500 RPM test is critical:** HC and O₂ that improve dramatically at 2500 RPM confirm `dual_egr_recovery_pattern`.
5. **No DTC to distinguish EGR from ignition misfire** → the vacuum test and 2500 RPM recovery are the splitters.

**1996–2005 (OBD-II, early electronic EGR):**
1. **P0401/P0402 present** → confirm with gas analysis; thresholds same as §7.
2. **No DTC but gas sig present** → the ECM monitor may not have completed (drive-cycle dependent). Run drive cycle; recheck.
3. **P0404 + position sensor erratic** → pintle carbon-stuck; clean valve, recheck.
4. **PWM type without position feedback** → no P0404/P0405/P0406 possible.

**2006–2015 (CAN-bus, position-feedback EGR):**
1. **P040x present + position PID available** → compare commanded vs actual EGR position via scan tool. Disagreement > 10 % confirms mechanical fault.
2. **P0405/P0406 (position sensor low/high)** → sensor circuit fault; gas sig may be normal because the valve itself operates correctly.
3. **Stuck-open with normal position PID** → valve physically stuck but position sensor reads commanded position; detectable only by gas analysis.

**2016–2020 (VVT internal EGR era):**
1. **No external EGR valve on most GDI applications** → P040x DTCs will not exist.
2. **HC + O₂ → run VVT phaser diagnostics** (`master_mechanical_guide.md §9`).
3. **If external EGR valve is fitted** (rare on GDI, more common on PFI turbo) → apply the 2006–2015 flow above.

#### 7b. Common EGR diagnostic pitfalls

**Pitfall 1 — Confusing EGR stuck-open with vacuum leak.** Both produce HC↑/O₂↑ at idle. The technician's first instinct is often to hunt for a vacuum leak (hoses, intake gasket), because vacuum leaks are far more common than stuck-open EGR valves. The splitters are:

- **Fuel trim behaviour:** MAF-based vacuum leak → STFT sharply positive, normalising at cruise. EGR stuck-open on MAF system → STFT near normal because inert gas is not metered by MAF and doesn't shift the O₂ sensor lean signal. On a MAP-based system, both can look similar.
- **NOx (5-gas):** Vacuum leak → NOx may rise (lean misfire heats chamber). EGR stuck-open → NOx suppressed (inert gas quench).
- **2500 RPM:** Vacuum leak shows moderate improvement. EGR stuck-open shows dramatic improvement.
- **Vacuum gauge:** Vacuum leak: reading may be low but fluctuates. EGR stuck-open: steady low reading with minimal fluctuation.

**Pitfall 2 — Condemning the EGR valve when the passage is coked.** P0401 (insufficient flow) with commanded EGR position at 100 % and zero measured flow change → the valve is trying but the passage is blocked. Remove valve, clean passage, reinstall the same valve — replacing the valve without cleaning the passage produces a comeback.

**Pitfall 3 — Assuming P0400 with normal gases means the EGR is fine.** P0400 can fire for electrical faults (open/short in solenoid) without any gas disturbance. A P0403 (circuit fault) with normal gases is an electrical problem, not a flow problem.

**Pitfall 4 — Ignoring the cold-start inhibition.** If the engine is tested cold (ECT < 40 °C), EGR is disabled. Gas analysis under cold conditions will not reveal an EGR fault, and the EGR valve is closed — vacuum application at cold idle proves nothing. Always warm the engine to ECT ≥ 70 °C before EGR diagnostics.

**Pitfall 5 — Missing the VVT internal EGR transition.** On a 2016+ engine with VVT internal EGR and no external valve, running traditional EGR diagnostics (vacuum application, position sensor check) is impossible. The technician may falsely conclude "EGR is fine" because they tested for the wrong architecture. Always verify EGR valve type visually before beginning the diagnostic flow.

**Pitfall 6 — Cleaning the EGR valve without resetting adaptions.** After cleaning a carbon-stuck EGR valve, the ECU's learned position adaptions may still reflect the pre-cleaning state. The valve may be physically free but the ECU sees out-of-range position feedback when the motor moves to a freshly freed position. Always clear adaptions (usually via scan tool EGR relearn function) after cleaning an electronic EGR valve.

**Pitfall 7 — Cascade misdiagnosis with P0300 + P0402.** A stuck-open EGR causes lean-misfire at idle, generating P0300. The technician sees P0300 and replaces spark plugs/coils. The EGR fault stays, the misfire returns within weeks, and P0300 fires again. In all P0300 diagnosistics, specifically ask: does this engine have EGR, and is it stuck open at idle? Check P0402 before replacing any ignition component.

---

## 8. Inter-guide rules

- EGR stuck-open at idle produces the same HC↑/O₂↑ signature as lean misfire. The splitter is NOx: EGR suppresses NOx (inert-gas quench); lean misfire at threshold burns hotter and may elevate NOx slightly. If 5-gas NOx > 150 ppm alongside HC↑/O₂↑, suspect lean misfire over EGR. Cross-ref `master_nox_guide.md §2`.
- A P0401 (insufficient flow) combined with P0420 (catalyst degradation) may be related: without EGR dilution, NOx rises and the cat faces higher NOx load, degrading efficiency faster. When both DTCs are present, resolve EGR first.
- EGR stuck-open causes a real lean-misfire condition. The upstream O₂ sensor sees this as lean and generates positive fuel trim. This confirms a true lean condition — but the cause is charge dilution, not an air leak. The fuel-trim guide's "positive trim at idle normalising at cruise" rule can be overridden by EGR if the EGR flow is post-MAP/pre-throttle body on that platform. Cross-ref `master_fuel_trim_guide.md §4`.
- **Bank-specific EGR on V-engines:** Some V-configuration engines apply EGR to only one intake bank (usually bank 1). When EGR is stuck open and bank-specific, the gas analyser sees a partial signature — O₂ may be elevated but not as severely as with dual-bank EGR dilution. Bank-1 fuel trim may run sharply positive while bank 2 trims are normal. The inter-bank trim delta > 8 % at warm idle with EGR DTC present signals bank-specific EGR fault. Cross-ref `master_fuel_trim_guide.md §5`.
- **EGR + P0420 catalyst interaction:** A stuck-open EGR valve at idle increases HC emission and reduces NOx, but the elevated HC load taxes the catalyst, progressively degrading its efficiency. If P0420 appears alongside EGR DTCs, correct the EGR fault first and re-test catalyst efficiency — the cat may recover. If P0420 persists after EGR repair, the catalyst is genuinely degraded. Route to `master_catalyst_guide.md §4`.
- **EGR + P0300 random misfire:** A stuck-open EGR at idle causes lean-misfire that the ECU counts. With enough idle-misfire events across multiple cylinders, a P0300 (random misfire) can set. The 4D engine should always check for EGR DTCs when diagnosing P0300 at warm idle with otherwise normal ignition and fuel delivery. Fixing the EGR fault resolves the misfire; condemning the ignition system wastes diagnostic time.
- **EGR temperature sensor (where fitted):** Some linear EGR systems include an EGR temperature sensor. Normal EGR flow produces a 40–80 °C temperature rise at the EGR outlet above ambient intake temperature. Zero temperature rise when the valve is commanded open confirms zero flow (P0401). Persistently elevated EGR outlet temperature with valve commanded closed suggests the valve is stuck partially open. The temperature sensor provides an independent layer of EGR flow verification before resorting to gas analysis.
- **Exhaust backpressure and EGR flow:** A partially restricted exhaust (clogged catalytic converter) reduces the pressure differential that drives EGR. Reduced EGR flow from exhaust restriction is not an EGR fault — fix the exhaust restriction first. EGR flow tests can produce misleadingly low flow readings when the exhaust is restricted. Cross-ref `master_catalyst_guide.md §3` and `master_exhaust_guide.md §2`.

---

## 9. Cross-references

- `master_gas_guide.md §3 rule 6` — NOx high + lean λ + low CO ⇒ lean combustion or stuck-open EGR
- `master_nox_guide.md §2` — NOx formation temperature, EGR-NOx interaction
- `master_obd_guide.md §5.8` — EGR DTC monitor enable conditions
- `master_fuel_trim_guide.md §4` — trim pattern decision tree for stuck-open EGR vs vacuum leak
- `master_mechanical_guide.md §9` — VVT internal EGR variant
- `master_cold_start_guide.md §3` — ECT gate that inhibits EGR on cold start
- `master_mechanical_guide.md §3` — vacuum-gauge protocol; EGR stuck-open produces steady vacuum < 15 inHg

---

## 10. EGR testing and verification procedures

These procedures confirm or exclude EGR faults when the diagnostic decision tree (§7) returns ambiguous results.

#### 10.1 Manual vacuum test (ported vacuum and positive backpressure valves)

1. **Warm engine to ECT ≥ 70 °C.** EGR is disabled cold; testing cold proves nothing.
2. **At warm curb idle, apply vacuum directly to the EGR valve diaphragm with a hand pump.**
3. **Observe RPM:**
   - **RPM drops 100+ RPM or engine stalls** → EGR passage is clear; the valve was closed and the engine cannot tolerate the sudden inert-gas charge. Passage is not coked; valve was not stuck open.
   - **RPM unchanged** → EGR passage is fully coked, or valve diaphragm is ruptured. Apply vacuum while watching the valve stem — if stem moves but RPM does not change, the passage is coked. If stem does not move, the diaphragm is ruptured or the valve is mechanically seized.
   - **RPM improves or stabilises** → Valve was already stuck partially open; adding vacuum opens it further or keeps it in the open position. This is a positive stuck-open indication.

#### 10.2 Scan-tool position test (linear electronic EGR with feedback)

1. **Warm engine to ECT ≥ 70 °C.**
2. **Connect scan tool; monitor EGR commanded position and EGR actual position PIDs.**
3. **Command EGR valve from 0 % → 100 % in 20 % increments.**
4. **Verify:** Actual position tracks within ±10 % of commanded at each step. Actual position < commanded by > 10 % → pintle or seat carbon-stuck. Actual position erratic (jumping 0 % ↔ 100 %) → position sensor fault or loose connector.

#### 10.3 EGR temperature sensor flow confirmation (where fitted)

1. **Monitor EGR outlet temperature PID.**
2. **With EGR commanded closed → open:** Temperature rise should be 40–80 °C within 10 seconds.
3. **Interpretation:**
   - Temperature rises within spec → EGR flow confirmed; gas sig behaviour is not from zero-flow EGR.
   - No temperature rise → zero EGR flow despite commanded open position. P0401 flow insufficient is confirmed.
   - Temperature rises with EGR commanded closed → valve is stuck partially open.

#### 10.4 2500 RPM EGR recovery test

1. **Record HC, O₂, CO₂, and λ at warm curb idle.**
2. **Hold engine at 2500 RPM under no load for 60 seconds.**
3. **Record the same gases at steady 2500 RPM.**
4. **Interpretation:**
   - HC and O₂ drop substantially (> 30 % reduction) and CO₂ recovers → `dual_egr_recovery_pattern` fires. Strong positive for EGR stuck-open.
   - HC and O₂ unchanged or change ≤ 15 % → problem is not EGR-related.
   - HC and O₂ worsen at 2500 RPM → unlikely to be EGR; suspect ignition or fuel delivery fault.

---

## 11. Citations

- Delphi Product & Service Solutions: EGR valve technical documentation and operating strategy (2018)
- SAE J1979 — EGR monitor enable conditions (Mode $06)
- Walker Exhaust: 5-gas diagnostic chart — EGR fault gas patterns
- MOTOR Information Systems: "5-Gas Analysis" (May 1998) — EGR dilution gas signatures
- AutoZone Diagnostic Reference: P0401–P0408 family definitions
- OBD-II PIDs — Wikipedia, accessed 2026-05-03
