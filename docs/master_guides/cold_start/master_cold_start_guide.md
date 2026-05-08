# Master Cold-Start / Open-Loop Guide — 4D Petrol Diagnostic Engine

**Purpose.** Define open-loop vs. closed-loop fuel control, cold-start enrichment physics, ECT-based transition thresholds, cold-start gas signatures, and the rules the 4D engine must use to **suppress false-rich fault flags** during warm-up. Without this gate, a healthy engine in the first two minutes after cold start looks identical to a serious rich-running fault.

**Scope.** Petrol (1990–2020). Hybrid restart logic out of scope. Cold-start emission strategies (heated cat, ignition retard at start) covered to the extent they shape gas signatures.

---

## 1. Open-loop vs. closed-loop

| Mode | Description | When active |
|---|---|---|
| **Open loop** | ECU uses pre-calibrated fuel maps; **ignores** O₂ sensor feedback | Cold start, WOT (power enrichment), DFCO (deceleration fuel cut), O₂ sensor faulted, first ~10–60 s after start, ECT below threshold |
| **Closed loop** | ECU adjusts fuel based on upstream O₂ feedback; STFT/LTFT update | Part-throttle cruise, warm idle (modern systems), ECT above threshold AND O₂ sensor at operating temperature |

In **open loop**, fuel-trim values (STFT/LTFT) are either frozen at last-known or invalid. The 4D engine must **never** interpret fuel trim during open loop — see `master_fuel_trim_guide.md §6, §9`.

The ECU reports its mode via the `fuel_sys_status` PID. Common values:

- `OL` — Open loop (always; e.g. cold start, WOT).
- `CL` — Closed loop using O₂ sensor.
- `OL-Drive` — Open loop due to driving conditions (WOT, DFCO).
- `OL-Fault` — Open loop due to system fault (O₂ sensor failure).

The 4D engine should consume `ff_fuel_status` from freeze frame; if it equals `OL` for a fuel-trim or catalyst DTC, the DTC was set under invalid conditions — flag `dtc_set_in_open_loop` and demote.

---

## 2. Cold-start enrichment physics

Cold engines need extra fuel because liquid petrol vaporises poorly off cold cylinder walls and intake-port surfaces. Most of the fuel briefly condenses on the cold port floor and only a fraction reaches the chamber as vapour. The ECU compensates with a calibrated cold-start enrichment table:

- **ECT at start-up:** colder ⇒ more enrichment.
- **Engine Run Time (ERT):** enrichment decays as the engine warms.
- **Intake Air Temperature (IAT):** secondary modifier (cold air is denser).

Typical commanded λ during cold start ranges from 0.85 at very low ambient to 0.95 just below closed-loop entry, decaying to 1.00 as ECT crosses ~40–60 °C.

Beyond enrichment, the ECU also retards ignition at start-up (delaying combustion) so that exhaust gases are still hot when they reach the catalyst — accelerating cat light-off. This adds another transient gas-signature distortion.

---

## 3. Closed-loop transition thresholds

| Parameter | Typical value | Notes |
|---|---|---|
| **Closed-loop enable ECT** | 20–40 °C (68–104 °F) | Minimum coolant temperature |
| **O₂ sensor readiness** | ~350 °C sensor element temp | Heater brings sensor up; ~20 s post cold start |
| **Time-to-CL after start** | 10–60 s | Combined ECT + O₂ readiness |
| **P0125 trigger** | ECT fails to reach ~70 °C within ~50 s after warm start, or ~5 minutes after cold | Insufficient ECT for closed loop |
| **Hot-restart enrichment** | ECT > 80 °C plus engine off for short period | Brief enrichment to prevent vapour lock |

The 4D engine should treat the period from start-up to closed-loop entry as a **gate window**: any rich-side gas signature inside this window is presumed normal and must be re-confirmed with a measurement after the engine reaches ECT ≥ 70 °C. This is the core cold-start gate.

---

## 4. Cold-start gas signatures — what is normal

During open-loop warm-up (ECT < ~40 °C, ERT < ~60 s post cold start), these gas readings are **normal** and must not trigger rich-running fault candidates:

| Gas | Cold-start normal | Reason |
|---|---|---|
| HC | Up to 400–600 ppm briefly | Enrichment + poor vaporisation + cat not yet lit |
| CO | Up to 1.5–3.0 % | Enrichment → partial burn of excess fuel |
| CO₂ | 8–12 % | Combustion incomplete; cat not converting |
| O₂ | < 1 % | Enrichment consumes most available oxygen |
| λ | 0.85–0.95 | Commanded enrichment |

This signature is **identical** to a genuine rich-running fault. The discriminator is **time** and **ECT**:

- **If ECT < 40 °C:** Suppress `rich_mixture`, `Mechanical_Rich_Leaking_Injector`, `high_fuel_pressure`, and similar candidates unless DTCs (which were set during normal warm-up of past drives) explicitly contradict.
- **If ECT ≥ 70 °C and λ < 0.97 still:** The engine has finished warm-up; the rich is real. Pursue rich-mixture candidates.
- **If ECT 40–70 °C:** Transition zone. Prefer to defer; if forced, demote rich-side candidates by ≥ 50 %.

`master_gas_guide.md §3 rule 10` already encodes this gate at the gas-module level. This guide elaborates on the rule.

---

## 5. Hot-start / WOT / DFCO — other open-loop windows

### 5.1 Hot restart

After a hot soak (engine off, ECT high), restart can briefly engage open-loop enrichment to prevent vapour lock in fuel rails. Duration: a few seconds. Gas signature: brief mild rich at idle, λ recovers within ~10 s.

### 5.2 WOT (power enrichment)

At wide-open throttle, the ECU commands ~λ 0.85–0.90 for maximum power and component protection (preventing exhaust-gas-temperature runaway). This is open loop. Gas signature: rich. The engine should suppress rich candidates whenever `fuel_sys_status = OL-Drive` is reported in freeze frame and the freeze-frame load is high.

### 5.3 DFCO (Deceleration Fuel Cut-Off)

On closed-throttle deceleration above a threshold RPM, the ECU shuts injectors off entirely. The engine pumps air with no fuel. Gas signature:

- HC ≈ 0
- CO ≈ 0
- CO₂ ≈ 0 (no combustion)
- O₂ ≈ 20.9 % (ambient)
- λ → ∞

This is **identical** to the no-combustion / non-starter fingerprint (`master_gas_guide.md §3 rule 8`, `master_non_starter_guide.md §2`). The discriminator: DFCO occurs while the engine is running (RPM > 1000) on decel; non-combustion occurs during cranking (RPM 150–300) or with engine off.

The 4D engine should check `vehicle_speed > 0` and `rpm > 1000` to confirm DFCO when this gas pattern appears mid-drive.

---

## 6. ECT sensor bias — when the gating rule itself is poisoned

A faulty ECT sensor poisons the cold-start gate because the gate's input is wrong. Two failure modes:

| Failure | ECU sees | Real engine state | Result | DTC |
|---|---|---|---|---|
| **ECT stuck cold (high resistance, open-trending)** | Always cold | Engine actually warm | ECU runs permanent enrichment → rich λ, high CO, fuel consumption worse | May set P0117 (low input) or P0125 |
| **ECT stuck hot (low resistance)** | Always hot | Engine actually cold at start | ECU runs no enrichment → hard starting in cold weather, lean λ at start, may stall | May set P0118 (high input) |
| **ECT sluggish** | Slow to update | Gradually warming | Cold-start gate releases too late or too early | Often sets nothing; subtle misdiagnosis |

The 4D engine must surface `ECT_Sensor_Bias` when:

- Reported ECT and gases disagree (e.g. ECT 90 °C but λ 0.90, suggesting permanent cold-enrichment).
- Reported ECT and time-since-start disagree (e.g. ECT 25 °C reported but the user has been driving for 30 minutes).
- Coolant-temperature DTC active (P0115–P0118, P0125, P0128).

When `ECT_Sensor_Bias` is active, the cold-start gate uses **time-since-start** rather than reported ECT.

---

## 7. The cold-start gate — exact rule the engine implements

```
if ECT < 40 °C OR (ECT_Sensor_Bias AND ERT < 90 s):
    SUPPRESS [rich_mixture, leaking_injector, high_fuel_pressure,
              EVAP_purge_stuck_open]
    NOTE: cold-start enrichment legitimately produces this signature

elif 40 ≤ ECT < 70 °C:
    DEMOTE rich-side candidates by 50 %
    PROMOTE [cold_start_enrichment_normal] as alternate explanation

elif ECT ≥ 70 °C:
    APPLY all candidate weights normally
```

This rule alone eliminates the largest class of cold-start false positives in the v4 audit. The 4D engine implements it in `engine/validators.py` (`is_warmed_up()` style check) and the `cold_start_enrichment` symptom node.

---

## 8. Cross-domain interactions

| Other guide | Cross-rule |
|---|---|
| `master_fuel_trim_guide.md` | §6, §9 — never interpret trims during open loop |
| `master_catalyst_guide.md` | §3 — catalyst monitor enable requires ECT ≥ 70 °C; cold-start P0420 is suspect |
| `master_o2_sensor_guide.md` | §5 — sensor heater brings O₂ to operating temp; cold-start gate relaxes once O₂ is ready |
| `master_gas_guide.md` | §3 rule 10 — cold-start enrichment legitimately raises HC + CO and drops λ |
| `master_obd_guide.md` | §6 — pending DTCs during warm-up are common and often clear by themselves |

---

## 9. Citations

- SAE J1979 — Mode $01 PIDs `$03` (`fuel_sys_status`), `$05` (ECT), `$0F` (IAT), `$1F` (run-time since engine start).
- `cases/library/automotive/mix/Seeing The Whole Picture  The Importance of Loop Status - iATN.pdf` — closed-loop / open-loop validation.
- `cases/library/automotive/mix/extracted/Interpreting OBDII Data.md` — practical fuel-status interpretation.
- `cases/library/automotive/mix/obdii-data-interpretation.md` — extracted summary.
- Cross-ref: `master_gas_guide.md §3 rule 10` (cold-start enrichment legitimately rich), `master_fuel_trim_guide.md §9` (preconditions for valid trim), `master_obd_guide.md §3, §7` (DTC types and freeze-frame validity).
