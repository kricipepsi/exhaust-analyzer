# Master Fuel System Guide — 4D Petrol Diagnostic Engine

**Purpose.** Define fuel delivery components (low-pressure pump, regulator, port injectors, GDI HPFP and direct injectors, EVAP purge), pressure specifications, injector pulse-width interpretation, return-vs-returnless system behaviour, and how fuel-delivery faults manifest in gas readings, fuel trims, and DTCs.

**Scope.** Petrol port-injection (1990–present) and gasoline direct injection (GDI, ~2005–present). Diesel high-pressure systems out of scope. CNG/LPG bi-fuel out of scope.

---

## 1. Fuel pressure fundamentals

Most port-injected petrol engines regulate fuel pressure to maintain a constant **pressure differential across the injector**, not constant absolute pressure. The differential matters because injector flow scales with √(rail pressure − manifold pressure).

| Architecture | Idle pressure | Cruise pressure | Regulator location |
|---|---|---|---|
| **Return-style with vacuum-referenced FPR** | ~2.5 bar (~36 psi) | ~3.0 bar (~43 psi) | On fuel rail; vacuum line to intake manifold |
| **Returnless system** | ~3.5–4.0 bar constant | ~3.5–4.0 bar | In-tank; ECU adjusts pump duty cycle |
| **GDI low-pressure (lift pump)** | 4–6 bar (~60–90 psi) | 4–6 bar | In-tank; constant supply to HPFP |
| **GDI high-pressure (rail)** | 30–50 bar at idle | 100–200 bar under load | On rail; ECU controls via Volume Control Valve (VCV) |

**Maximum healthy deviation:** ±0.2 bar (±3 psi) from manufacturer spec. Greater deviation indicates regulator, pump, or filter fault.

**Vacuum-line test (vacuum-referenced FPR):** Disconnect and plug the vacuum line to the FPR. Pressure should rise by ~0.5 bar (7 psi). If it does not rise, the FPR diaphragm is torn or the vacuum reference is blocked.

---

## 2. Injector pulse-width interpretation

Injector pulse width (PW) is the ECU's most fundamental fuel-control output. The 4D engine compares observed pulse width against expected for the operating point.

| Condition | PW (port injection, 3 bar base) | Duty cycle |
|---|---|---|
| Idle, warm | 1.5–3.0 ms | 1–3 % |
| Cruise, 2500 RPM | 2.5–5.0 ms | 5–15 % |
| Acceleration (transient) | up to 20 ms briefly | — |
| WOT, max power | 8–15 ms | 50–80 % |
| Minimum reliable opening | ~0.5 ms | Below this, injector opening is non-linear |

**Diagnostic logic:**

- **PW too high for condition:** ECU compensating for lean (vacuum leak, low fuel pressure, dirty MAF reading low).
- **PW too low for condition:** ECU compensating for rich (high fuel pressure, leaking injector, contaminated MAF reading high, stuck-open EVAP purge).
- **PW normal but gases abnormal:** Look at mechanical (compression) or ignition. Fuel control is working; the problem is elsewhere.

GDI direct-injectors run different PW ranges (0.3–2 ms typical) because they inject at much higher pressure with smaller pulse times.

### Injector electrical and balance specifications

| Parameter | Specification | Notes |
|-----------|--------------|-------|
| **High-impedance (high-Z) injector coil resistance** | **11–18 Ω** | Most port-injection petrol injectors (1990s–present). Resistance outside this range = coil failure or wiring fault. |
| **Low-impedance (peak-and-hold) injectors** | 1–3 Ω | Older systems (pre-1990s Bosch); require a peak-and-hold driver. Do not confuse with high-Z. |
| **Injector balance test tolerance** | **≤ 10 % variation between cylinders** | Pressure-drop test: each injector fired for a fixed pulse count; rail-pressure drop should be equal across all cylinders. A cylinder > 10 % below the mean = clogged injector. > 10 % above the mean = leaking injector. |

**Critical note:** An injector can pass a resistance test and still be clogged. Resistance checks winding integrity only; a partially blocked spray pattern will not affect DC resistance. Always follow resistance check with a rail pressure-drop or flow test when the fault pattern suggests cylinder-specific lean misfire.

---

## 3. Fuel delivery diagnostic patterns in gas readings + trims

This is the cross-domain decision table that ties fuel-system faults to gas signatures and trim direction:

| Condition | CO | CO₂ | HC | O₂ | λ | Trim | Bank pattern |
|---|---|---|---|---|---|---|---|
| **Low fuel pressure / weak pump** | Low | Low | Normal–High | High | > 1.03 | Positive (lean) | Both banks worsen with RPM |
| **High fuel pressure / pinched return / failed FPR** | High | Low | Normal | Low | < 0.97 | Negative (rich) | Both banks |
| **Leaking injector (drip)** | High at idle | Low | High | Low | < 0.97 | Negative on **one bank** | Bank-specific |
| **Clogged injector (low flow)** | Low | Low | High (lean misfire) | High | > 1.03 | Positive on **one bank** | Bank-specific |
| **EVAP purge stuck open** | High at idle | Low | Moderate–High | Low | < 0.97 | Negative at idle, normalises at cruise | Both banks |
| **GDI HPFP failure** | High under load | Low | Normal–High | Low at load | < 0.97 under load | Negative under load | Both banks |
| **Port injector electrically failed (open)** | Cylinder-specific misfire pattern | Low | Very high | High | ≈ 1.00 | Cylinder-specific lean misfire P030x | One cylinder |

Cross-ref: `master_fuel_trim_guide.md §4` (decision tree), `master_gas_guide.md §3` (inter-gas rules).

---

## 4. EVAP system fault signatures

The EVAP system stores fuel vapour from the tank in a charcoal canister and purges it into the intake when conditions permit. A fault is a "hidden fuel source" the ECU does not meter through the injectors.

| DTC | Fault | Mechanism | Diagnostic signature |
|---|---|---|---|
| **P0442** | Small leak (≤ 0.5 mm equivalent) | Loose fuel cap, cracked vacuum hose at canister, cracked tank seam | Detected by tank-decay test; smoke machine test |
| **P0455** | Large leak (gross) | Fuel cap missing, large hose disconnected, cracked filler neck | Test fails immediately on enable |
| **P0456** | Very small leak (≤ 0.020"/0.5 mm) | Same causes as P0442 but tighter threshold | Some manufacturers use this code; same diagnosis |
| **P0446** | Vent valve circuit / seal | Vent valve stuck open or solenoid driver fault | Tank cannot reach vacuum during decay test |
| **P0441** | Purge flow incorrect | Purge valve stuck closed | When purge commanded, no fuel-trim shift |
| **P0440** | EVAP general fault | — | Generic; review pending codes |

**Stuck-open purge valve** acts as a continuous unmetered fuel source:
- At idle: fuel trims go sharply negative, CO rises, λ drops below 0.97.
- At cruise: effect diminishes because vapour is a smaller fraction of total fuel demand — trims approach normal.
- This signature mimics a leaking injector but affects **both** banks equally — the splitter from leaking injector (which affects one bank).

**Stuck-closed purge valve:** canister saturates, fuel smell at tank, but no immediate mixture effect. May set P0441 over time.

**EVAP system check procedure (in-app):** if P0442 or P0455 is present **with negative fuel trim at idle that normalises at cruise**, the purge valve is the prime suspect — not the rest of the fuel system.

---

## 5. Fuel pump volume test

Pressure alone is not enough — fuel volume must also be verified. Industry rule of thumb:

> ≥ 0.2 litres (7 fl oz) of fuel delivered in 10 seconds of continuous pump operation is sufficient for any petrol engine to start and run.

Below this, the pump is failing under load even if static pressure looks fine. This test catches the failure mode where the pump can build pressure at zero flow but cannot maintain pressure under demand — the most common pump end-of-life pattern.

---

## 6. GDI specifics — high-pressure fuel system

GDI's dual-stage architecture has unique failure modes the 4D engine must recognise.

### 6.1 Architecture

- **Lift pump (in-tank):** ~4–6 bar (~60–90 psi) supply to the HPFP. Variable-speed PCM-controlled.
- **High-Pressure Fuel Pump (HPFP):** Cam-driven, single-cylinder pump compressing fuel to 30–200 bar. Driven by a dedicated camshaft lobe.
- **Volume Control Valve (VCV):** Solenoid on the HPFP inlet that varies the effective stroke, controlling rail pressure.
- **High-pressure rail + direct injectors:** Inject directly into combustion chamber, much higher pressure than port injectors.

### 6.2 Critical PIDs

| PID | What it shows | Healthy range |
|---|---|---|
| **Fuel Rail Pressure Desired** | ECU's target | Varies with load: 30 bar idle, up to 200 bar WOT |
| **Fuel Rail Pressure Actual** | Sensor reading | Should track desired within 5 % |
| **VCV Duty Cycle** | Valve command | 20–35 % at idle; > 50 % suggests over-compensation for HPFP wear or lift-pump drop |
| **Lift Pump Duty Cycle** | Variable-speed pump command | 30–60 % typical |

### 6.3 Common GDI failure modes

| Failure | DTC | Symptom | Diagnostic |
|---|---|---|---|
| **HPFP cam-lobe wear** | P0087 (pressure too low) under load | Power loss; long crank; high-load stumble | Inspect camshaft lobe for HPFP — common wear pattern |
| **HPFP internal seal leak** | Pressure decay after shutoff; rich at idle (negative trim) | Hot soak hard-start; raw fuel in oil | Leak-down test at hot shutdown |
| **VCV stuck** | P0089 (regulator performance) | Pressure cannot follow desired | VCV duty cycle pegged 0 % or 100 % |
| **Lift pump drop** | P008A or P008B | HPFP starves under load | Lift-pump pressure < 4 bar |
| **GDI carbon on intake valves** | Misfire codes; lean trims; cold-start rough | Long-term GDI issue; no port injection to wash valves | Intake-valve cleaning required (walnut-blast) |
| **GDI injector tip fouling** | Per-cylinder lean | Lean misfire on one cylinder; fuel spray pattern degraded | Specialty cleaning or replacement |

### 6.4 GDI pre-ignition (LSPI)

Low-Speed Pre-Ignition is a GDI-specific knock event where the mixture ignites before the spark plug fires, in low-RPM high-load conditions. Symptom: violent knock, bent rod possible, extremely loud single-event noise. Causes: oil with wrong additive package; carbon hot spots; over-fuelling at idle. This is real, sudden, destructive — not cumulative wear.

---

## 7. Cross-checks

- **Negative trim at idle, normal at cruise + no P0442/P0455** → leaking injector (one bank) more likely than EVAP.
- **Negative trim at idle, normal at cruise + P0442 or P0455** → stuck-open EVAP purge.
- **Positive trim under load only** → fuel-volume issue (pump, filter, sock).
- **Random P0300 + negative trim both banks + no exhaust leak** → consider EVAP purge or systemic rich (pressure, FPR).
- **GDI hot-start hard-start** → HPFP internal seal leak.

---

## 8. Cross-references

| Topic | Other master guide |
|---|---|
| Fuel-trim direction | `master_fuel_trim_guide.md §4` |
| EVAP DTCs | `master_obd_guide.md §5.7` |
| Injector circuit DTCs | `master_obd_guide.md §2` (P0201–P0212) |
| Rich gas signatures | `master_gas_guide.md §8.4` (rich-mixture causes) |
| Lean gas signatures from low pressure | `master_gas_guide.md §8.3` |
| Ignition-misfire vs fuel-misfire | `master_ignition_guide.md §6` |

---

## 9. Citations

- Bosch Automotive Handbook — fuel-system specifications.
- SAE J1979 — Mode $01 PIDs `$0A` (fuel rail pressure), `$22` (fuel rail pressure absolute), `$23` (fuel rail pressure direct-inject).
- `cases/library/automotive/mix/fuel-trim.pdf` and `fuel-trim-analysis.md` — fuel-system / trim cross-impact.
- `cases/library/automotive/mix/fuel_supplydiag.PDF` — fuel-supply diagnosis flow.
- `cases/library/automotive/mix/extracted/Generic OBD II DTC CODES P0400 to P0499.md` — EVAP and EGR DTC ranges.
- Cross-ref: `master_gas_guide.md §8.4` (rich-mixture causes), `master_air_induction_guide.md §5` (vacuum-leak topology that can mimic EVAP-stuck-open).
