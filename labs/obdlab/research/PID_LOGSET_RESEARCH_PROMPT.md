# Research Prompt — Build a Test PID Log Set for OBDLab

> Paste everything below the line into your research assistant. It is self-contained:
> it carries OBDLab's exact input contract, so the output will load straight into the
> module's `translate()` entry point and exercise real code paths — not return
> `NO_FAULT` / `UNKNOWN` like the current PID-less corpus does.

---

## Role and goal

You are an automotive diagnostics data researcher. Your job is to produce a **test
PID log set** for a petrol-only OBD-II live-data analytics module (OBDLab). The set
must contain realistic, sourced OBD-II Parameter ID (PID) readings for known engine
conditions, structured so each case drives the module to a **discriminating output**
(a specific lambda, trim, VE, or fault classification) — not a default "no fault".

Scope is **petrol, naturally-aspirated and turbo, model years 1990–2010** only. No
diesel. No GDI/forced-induction families that fall outside this window unless they
genuinely existed in scope.

## Why this matters (context, do not skip)

The module was quarantined because the available test corpus carried no live PID
data, so it returned `o2_mode=NO_FAULT` on >95% of cases, `ve_pct=0.0`,
`ve_validity=UNKNOWN`. To un-quarantine it, we must prove it produces non-trivial,
discriminating output on PID-bearing fixtures. Every case you author must therefore
be designed to make a specific signal *move*.

## The input contract — match these field names and units exactly

### Part A — raw PID dict (`raw_user_inputs`)

The module validates and unit-converts these. Provide values in the canonical unit
where possible; if you cite a source in another unit, you may instead supply the
alternate-unit key (the module converts):

| Canonical field | Unit | Valid range | Alt-unit keys accepted |
|---|---|---|---|
| `engine_rpm` | RPM | 0–8000 | — |
| `coolant_temp_c` | °C | -40–140 | `coolant_temp_f` (°F, ignored if _c present) |
| `intake_air_temp_c` | °C | -40–80 | `intake_air_temp_f` (°F) |
| `calculated_engine_load_pct` | % | 0–100 | — |
| `mass_airflow_gps` | g/s | 0–655.35 | `mass_airflow_lbmin` (lb/min) |
| `manifold_vacuum_kpa` | kPa | 0–255 | `manifold_vacuum_psi` (psi), `manifold_vacuum_inhg` (inHg) |
| `shrtft1` | % | -127–127 | — |
| `longft1` | % | -127–127 | — |
| `shrtft2` | % | -127–127 | only on 2-bank engines |
| `longft2` | % | -127–127 | only on 2-bank engines |
| `o2_voltage_b1s1` | V | 0.0–1.0 | for narrowband / NB-sim sensors |
| `pid_wideband_equivalence_ratio` | λ | ~0.7–1.3 | for wideband-linear sensors |

Also include where the scenario needs it: `fuel_status` (`Closed_Loop` /
`Open_Loop_Cold` / etc.), `vehicle_speed_kmh`, `throttle_position_pct`,
active DTC list, `drive_cycles_since_clear`, DFCO active flag.

### Part B — vehicle DNA view (`ObdLabDnaView`)

Each case must name the engine so these are derivable from real spec:

| Field | Values |
|---|---|
| `engine_displacement_liters` | float (required for VE math) |
| `cylinder_count` | int |
| `rated_rpm` | int (redline / rated) |
| `stress_idle_rpm_target` | int |
| `air_metering_strategy` | `DUAL_MAF_MAP_CROSSCHECK` / `MAP_ONLY_SPEED_DENSITY` / `MAF_ONLY` |
| `upstream_o2_type` | `NARROWBAND_0_TO_1V` / `WIDEBAND_LINEAR` / `WIDEBAND_NB_SIM` |
| `induction_type` | `NATURALLY_ASPIRATED` / `TURBOCHARGED` |
| `emissions.egr_equipped` | bool |
| `number_of_banks` | 1 or 2 |

## Coverage matrix — what the log set must span

Author **at least one case per cell** below, and tag each with the OBDLab output it
is designed to trigger so the result is verifiable:

1. **VE routing branches** (all three): a MAF-only engine, a MAP-only speed-density
   engine, and a dual MAF+MAP engine.
2. **O2 sensor types** (all three): narrowband 0–1V, wideband linear, wideband NB-sim.
3. **Lambda outcomes**: a lean case (O2 ≈ 0.10–0.40 V → λ 1.05), stoich
   (0.41–0.50 V → λ 1.00), rich (0.51–0.90 V → λ 0.95), and an out-of-range O2 that
   should clamp and flag `O2_CHANNEL_FAULT`.
4. **Fuel-trim outcomes**: a healthy near-zero trim case, a large positive total trim
   (lean correction, e.g. vacuum leak / failing MAF), a large negative trim (rich).
5. **VE-validity faults**: idle-collapse (`ve_pct<50` at stabilized idle, MAP>45),
   MAF contamination (`ve_pct<65` at stress idle, total trim >15%), and VE sensor skew
   (`ve_pct>90` at idle on an NA engine).
6. **RPM/thermal states**: stabilized warm idle, regulatory high idle, stress idle,
   and a cold open-loop case (ECT<75) that should freeze analytics.
7. **Trim-analytics gates**: at minimum cases that trip `ENGINE_COLD`, `OPEN_LOOP`,
   `O2_FAULT_ACTIVE` (active DTC in P0130–P0161), `CKP_CMP_FAULT_ACTIVE`
   (P0335/P0340), and one clean `VALID`.
8. **Boundary / rejection cases** (must be rejected as typed errors, not crash):
   `mass_airflow` or O2 voltage out of range, `coolant_temp_c=999`,
   `manifold_vacuum_kpa=999`, a malformed/garbage DTC, a 1-bank engine that wrongly
   carries `shrtft2`/`longft2` (bank-2 null-contract violation), and an `engine_rpm`
   that breaches `rated_rpm × 1.05` on a HIGH-confidence DNA.

## Fault families to represent (within 1990–2010 petrol scope)

Spread the realistic-fault cases across these so OBDLab data discriminates between
them: `lean_condition` (vacuum leak, failing MAF), `rich_condition` (leaking
injector, stuck-rich O2), `catalyst_failure` signatures, `misfire`/ignition,
`sensor_fault` (O2 dead/sluggish/stuck), `mechanical_wear` (low VE), and a clean
`no_fault` baseline. For each, base the PID values on documented symptom signatures
for that fault on real port-injection petrol engines of the era.

## Output format

Return a JSON array. Each element:

```json
{
  "case_id": "pid_lean_vacuum_leak_01",
  "description": "1998 2.0L I4 NA, port injection — intake vacuum leak",
  "fault_family": "lean_condition",
  "vehicle": "make/model/year/engine_code",
  "dna_view": { ...the Part B fields... },
  "raw_pids": { ...the Part A fields... },
  "expected_obd_signature": {
    "normalized_obd_lambda": 1.05,
    "total_trim_correction_delta": ">+15",
    "ve_validity": "VALID|FAULT_*",
    "trim_analytics_gate": "VALID",
    "o2_channel_fault": false,
    "rpm_state_bucket": "STABILIZED_IDLE"
  },
  "sources": ["citation 1", "citation 2"]
}
```

For the rejection cases (matrix item 8), replace `expected_obd_signature` with
`expected_rejection` naming the error type (`PIDValidationError` /
`SemanticConsistencyError`) and the reason.

## Sourcing rules

- Cite every non-obvious numeric value: SAE J1979 / ISO 15031 PID definitions,
  service manuals, manufacturer spec, or reputable diagnostic references.
- Prefer real engine specs for displacement, cylinder count, rated RPM, and metering
  strategy. Do not invent a sensor configuration a given engine never had.
- Flag any value you had to estimate as `"estimated": true` with your reasoning.
- If you cannot source a realistic value for a cell, say so rather than fabricate.

## Deliverable

One JSON array covering the full matrix (target ~25–40 cases), plus a short table
mapping each `case_id` to the single OBDLab signal it is designed to move, so the
set can be used as the wiring-gate proof that OBDLab produces discriminating output.
