# Semantic Contract — the 4DLab boundary protocol

**Purpose:** the binding agreement that lets DNALab, GASLab, OBDLab, DTCLab and COMLab evolve in parallel (across separate cowork accounts and codebases) without semantic drift. Every cross-lab data exchange is JSON; every field in that JSON is governed by this contract.

**Scope:** the 4DLab v2 ecosystem in the flat `labs/` layout under `C:\Workspace\` (each lab carries its own package · tests · tasks · wiki · graph).

**Anchored to:**
- `labs/comlab/docs/Vocabulary/OBD_VOCABULARY.md` (canonical OBD identifiers)
- `labs/comlab/docs/Vocabulary/DTC_VOCABULARY.md` (canonical DTC identifiers)
- `labs/comlab/wiki/00_index.md … 14_sources_appendices.md` (the COMLab v2 reasoning grammar — the fusion-spine boundary surface this contract serves)
- `labs/gaslab/wiki/` (GASWIKI), `labs/obdlab/wiki/OBDLab_KG_Wiki.md`, `labs/dtclab/wiki/` (DTCWIKI) — emitter wikis
- `labs/dnalab/` / VINLab — `VehicleDNA` combined-payload JSON contract

**Version:** 1.3 (2026-06-20). Aligns the boundary to the COMLab v2 wiki (`COMWIKI-00…14`) and the reworked emitter labs (GASLab S1 / OBDLab S2 / DTCLab S3). Supersedes v1.0 (2026-05-17). See §10 for change protocol; v2 boundary deltas are summarised in §13.

---

## 1. Architecture in one diagram

```
  ┌───────────┐   ┌───────────────┐
  │  VINLab   │   │  SymptomLab   │
  │   VinDNA  │   │  SymptomDNA   │  ← upstream producers
  └─────┬─────┘   └───────┬───────┘
        │                 │
        ▼                 ▼
       ┌────────────────────┐
       │      DNALab        │  ← ONLY lab that imports other labs
       │   build_vehicle_   │     (intentional umbrella exception)
       │   dna() composes:  │
       │   VehicleDNA       │
       │   (Part A + B +    │
       │   session meta)    │
       └─────────┬──────────┘
                 │
                 │ JSON only
                 ▼
        ┌──────────────────────────────────────┐
        │              COMLab                  │
        │                                      │
        │  ingests:                            │
        │  - VehicleDNA (from DNALab)          │
        │  - GasLabPayload (from GASLab)       │ ← all JSON
        │  - OBDLivePayload (from OBDLab)      │
        │  - DTCLabPayload (from DTCLab)       │
        │                                      │
        │  produces:                           │
        │  - OrchestratorFinalUIOutput JSON    │
        └──────────────────┬───────────────────┘
                           │
                           ▼
                          UI
```

**Rule of thumb (the only one):**
> Every lab boundary is JSON. The only allowed Python imports across labs are DNALab importing VINLab + SymptomLab. Everything else talks via the schemas defined in this contract.

---

## 2. Naming agreement (2026-05-17, strict)

Three names are reserved and unambiguous. Any document or code drifting from these names is wrong.

| Concept | Reserved name | Owner module |
|---|---|---|
| Part A — physical vehicle profile decoded from the VIN | **`VinDNA`** | VINLab |
| Part B — user-reported symptom triage | **`SymptomDNA`** | SymptomLab |
| Combined Part A + Part B + session metadata | **`VehicleDNA`** | DNALab |
| Orchestrator inbound payload (VehicleDNA + 3 lab outputs) | **`OrchestratorInboundRequest`** | COMLab |
| Final UI output | **`OrchestratorFinalUIOutput`** | COMLab |

Avoid synonyms in code, docs, and test names: do not write `vehicle_dna_part_a`, `physical_dna`, `dna_payload`, etc. Use the reserved name.

---

## 3. The single source of truth per concern

When in doubt about a field name or enum value, this table tells you which document is authoritative.

| Concern | Authority | Why that one |
|---|---|---|
| OBD PID names, units, ranges | `OBD_VOCABULARY.md` §2 | SAE J1979 anchored |
| O₂ sensor types, air metering strategies | `OBD_VOCABULARY.md` §4 | OBDLab BP §4 "Global VIN Guards" |
| RPM measurement bands (idle / regulatory / stress) | `OBD_VOCABULARY.md` §3 | OBDLab BP + user spec 2026-05-16 |
| Fault families | `OBD_VOCABULARY.md` §6 | cases CSV `expected_top_fault_family` |
| DTC regex, severity, P-code ranges | `DTC_VOCABULARY.md` §2 + §9 | SAE J2012 anchored |
| DTC routing tags | `DTC_VOCABULARY.md` §11 | aggregated from cases material |
| Mode 06 MID/TID dictionary | `DTC_VOCABULARY.md` §19 + §7 | OBDadd1.md + DTCLabBP §3.2 |
| Chemical signatures emitted by GASLab | `GAS_VOCABULARY.md` §21 / `OBD_VOCABULARY.md` §17 (**34-value** enum, v2.1) | v2.1 cam-timing split retired `WRONG_VALVE_TIMING` for three `CAM_TIMING_*` states |
| VehicleDNA JSON shape (combined payload) | `VINLab/VehicleDNA.md` §"Combined" | upstream owner (VINLab) |
| Ingestion + response Pydantic models | `comlab/comlab/schemas/{ingestion,response}.py` | implementation |
| Horizons (LEGACY/ADAPTIVE/MODERN) | `OBD_VOCABULARY.md` §7 | OBDLab BP §"Era-to-EURO" |
| Severity / confidence ratings (values) | `OBD_VOCABULARY.md` §8 + §10 | OrchestratorLabBP |
| Confidence-tier **semantics** (calibrated posterior/LR bands) | COMLab v2 wiki `COMWIKI-09` | v2 calibration rework — values locked, meaning redefined |
| Conflict-aware late fusion · differential output | COMLab v2 wiki `COMWIKI-08` / `COMWIKI-10` | v2 rework — replaces additive tie-break |
| Two-point delta operating points · noise floors · cross-reference | COMLab v2 wiki `COMWIKI-11` | v2 rework — second-frame signal |
| Provenance flags · achievable ceiling · eval gates | COMLab v2 wiki `COMWIKI-02` / `COMWIKI-12` | v2 corpus discipline |

If two documents disagree, the table above wins. If `VehicleDNA.md` says `induction_type: TURBOCHARGED` and `OBD_VOCABULARY.md` says `air_metering_strategy: DUAL_MAF_MAP_CROSSCHECK`, **both are correct** — they describe different fields. See §6 for the reconciliation table.

---

## 4. The four boundary schemas

These are the JSON shapes that cross lab boundaries. Each shape is owned by one module and consumed by exactly one downstream module.

### 4.1 `VinDNA` (VINLab → DNALab)

Produced by VINLab's `decode()`. Matches Part A of `VehicleDNA.md`:

```jsonc
{
  "vin": "1FA6P8CF0HXXXXXXX",
  "make": "Ford",
  "model_year": 2017,
  "engine_displacement_liters": 2.3,
  "cylinder_count": 4,
  "number_of_banks": 1,
  "induction_type": "TURBOCHARGED",          // see §6.1
  "fuel_delivery_type": "GDI",
  "air_metering_architecture": {
    "has_maf_sensor": true,
    "has_map_sensor": true,
    "primary_load_calculation": "HYBRID_MAF_MAP"  // see §6.2
  },
  "emissions": {
    "upstream_o2_type": "WIDEBAND_AFR",      // see §6.3
    "downstream_o2_present": true,
    "egr_equipped": false,
    "secondary_air_equipped": false
  },
  "euro_emission_category": "EURO_6",        // NEW — see §6.4
  "stress_idle_rpm_target": 4500,            // NEW — see §6.5
  "confidence": "HIGH"                       // HIGH | PARTIAL | NONE
}
```

**Notes:**
- `vin` is the 17-char VIN that produced this profile. Required.
- `confidence` reflects how many fields were inferred vs defaulted.
- Three fields marked NEW are extensions added by this contract and must be added to `VehicleDNA.md` (tracked in §11 open actions).

### 4.2 `SymptomDNA` (SymptomLab → DNALab)

Produced by SymptomLab's `resolve()`. Matches Part B of `VehicleDNA.md`:

```jsonc
{
  "tier_1_primary_symptom": "visible_exhaust_smoke",
  "tier_2_subfield_filter": "black_smoke",
  "environmental_conditions": {
    "occurs_during": "always",       // always | cold_only | hot_only | intermittent
    "engine_state": "running"        // running | cranking | will_not_start
  },
  "free_text_notes": null            // optional, technician shorthand
}
```

The Tier 1 and Tier 2 strings come from `VehicleDNA.md` §"Complete Universal Triage & Diagnostic Mapping Diagram" — that mapping diagram is the enum source.

### 4.3 `VehicleDNA` (DNALab → COMLab)

DNALab's `build_vehicle_dna()` produces this. It is the **only** umbrella composition allowed in 4DLab.

```jsonc
{
  "session_id": "DNA_TX_8849201",
  "timestamp": "2026-05-17T09:10:00Z",
  "schema_version": "1.3",            // contract version (this document)
  "vin_dna": { /* §4.1 VinDNA */ },
  "symptom_dna": { /* §4.2 SymptomDNA */ }
}
```

The keys `vin_dna` and `symptom_dna` are snake_case lowercase. `VehicleDNA.md` shows headings like `"PART A: VEHICLE PHYSICAL DNA (From VIN Module)"` — those are document headings, not JSON keys. The JSON keys are `vin_dna` and `symptom_dna` per the strict naming agreement.

### 4.4 `GasLabPayload`, `OBDLivePayload`, `DTCLabPayload`

Defined in `COMLab/comlab/schemas/ingestion.py` (Pydantic). Each owned by its respective producer lab.

```jsonc
// GasLabPayload — owned by GASLab
{
  "chemical_state": "RICH_MIXTURE",       // value from §3 ChemicalSignature enum (34-value, v2.1)
  "gas_co": 4.5,                           // vol %
  "gas_hc": 650,                           // ppm
  "gas_co2": 9.5,                          // vol %    (added v1.1, 2026-05-19)
  "gas_o2": 0.1,                           // vol %
  "gas_nox": 15,                           // ppm      (added v1.1, 2026-05-19)
  "lambda_chem": 0.82,
  "lambda_measured": 0.85,                 // float | None — directly-measured analyser λ for no-OBD fallback (T-FX-7)
  "sample_validity": "VALID",              // VALID | BORDERLINE | INVALID | EXTERNAL_O2_SUSPECT
  "reading_high": null,                    // GasReading | None — OPTIONAL 2500-RPM frame (T-GV2-4); enables Δgas (COMWIKI-11)
  "high_idle_hc": null,                    // float | None — per-gas high-idle frame values (high_idle_{hc,co,co2,o2,nox,lambda})
  "high_idle_co": null, "high_idle_co2": null, "high_idle_o2": null, "high_idle_nox": null, "high_idle_lambda": null
}

// OBDLivePayload — owned by OBDLab. Core v1 payload (11-field, T-FX-1) + v2 fusion-evidence fields (see §13).
{
  "engine_warmed": true,
  "total_trim_correction_delta": -35.0,    // STFT+LTFT aggregated; range −254..+254 %
  "normalized_obd_lambda": 0.85,           // float | None — Optional for no-OBD fallback (T-FX-7)
  "ve_pct": 72.5,                          // volumetric efficiency %
  "ve_validity": "VALID",                  // VEValidity enum
  "rpm_state_bucket": "STRESS_IDLE",       // EngineStateBucket enum — the two-point key (STABILIZED/REGULATORY_HIGH/STRESS/COLD_OPEN_LOOP_INVALID)
  "trim_analytics_gate": "VALID",          // TrimAnalyticsGate enum
  "o2_failure_mode": "NO_FAULT",           // O2FailureMode enum — authority OBD_VOCABULARY; v1 contract listed 4 values, OBDLab v2 emitter set differs → reconcile per §11 action 13
  "maf_status": "REAL_SENSOR_FEED",        // NodeMAFStatus enum
  "map_status": "REAL_SENSOR_FEED",        // NodeMAPStatus enum
  "freeze_frame_pids": { /* see DTC_VOCABULARY §12 */ }
  // ── v2 fusion-evidence fields (each has a named COMLab consumer — §13 / COMWIKI-13) ──
  // total_trim_correction_delta_b2, lambda_perception_delta, per_bank_trim_delta,
  // fuel_system_status, per_cylinder_misfire_counts, w_theo, sensor_error_delta,
  // ltft_cell_vector, intake_air_temp_c, throttle_pos_pct, coolant_temp_c, control_module_voltage_v
}

// DTCLabPayload — owned by DTCLab
{
  "active_mil": true,
  "mil_flashing": false,                   // distinguishes Type A flashing-MIL hazard
  "confirmed_dtcs": ["P0172"],
  "pending_dtcs": [],
  "permanent_dtcs": [],
  "routing_tags": ["RICH_HISTORY"],        // values from DTC_VOCABULARY §11 enum
  "mode_06_monitors": [
    {
      "mid": "A2",
      "tid": "0B",
      "component": "Misfire_Cylinder_2_Data",
      "status": "PENDING_FAIL_MARGINAL",   // PASSED | PENDING_FAIL_MARGINAL | CRITICAL_FAIL
      "margin_pct": 8.5
    }
  ],
  "historical_fault_context": "HISTORICAL_LOAD_FAULT",
  "freeze_frame": { /* FreezeFrameRecord — PIDs at fault moment (RPM, ECT, load, trims); see DTC_VOCABULARY §12.
                       v2: conditional evidence channel — present only when a DTC is stored; fused at the verdict
                       stage, NEVER as a delta input (single async snapshot). Consumer: T-COMV2-NOSTART-1 +
                       fusion intermittent-fault branch (COMWIKI-02 / COMWIKI-08). */ }
}
```

### 4.5 `OrchestratorInboundRequest` (the assembled COMLab input)

Whoever calls COMLab assembles this. In production the UI does it; in tests the regression harness does it.

```jsonc
{
  "vehicle_dna": { /* §4.3 VehicleDNA */ },
  "gas_lab_output": { /* §4.4 GasLabPayload */ },
  "obd_live_data": { /* §4.4 OBDLivePayload */ },
  "dtc_lab_output": { /* §4.4 DTCLabPayload */ },
  "symptom_dna": { /* plain dict — consumed by symptom_router.route_symptom().
                      Keys: tier_1_primary_symptom, tier_2_subfield_filter,
                      environmental_conditions (with engine_state, occurs_during),
                      free_text_notes. Not forwarded to any upstream lab. */ }
}
```

The top-level keys are snake_case. The `vehicle_dna` slice **replaces** the older `metadata` block from `OrchestratorLabBP.md` (which had `session_id`, `vin_dna_string`, `resolved_horizon`, `cylinder_count`). All of those fields are now inside `vehicle_dna` — COMLab reads `vehicle_dna.session_id`, `vehicle_dna.vin_dna.vin`, `vehicle_dna.vin_dna.cylinder_count`, and derives `resolved_horizon` from `vehicle_dna.vin_dna.euro_emission_category`.

---

## 5. Where COMLab reads each piece

This is the lookup table for COMLab's code — `lab_pipeline_aggregator.py` and `fault_atlas_router.py`.

| What COMLab needs | Path in `OrchestratorInboundRequest` |
|---|---|
| session id | `vehicle_dna.session_id` |
| VIN string | `vehicle_dna.vin_dna.vin` |
| cylinder count | `vehicle_dna.vin_dna.cylinder_count` |
| number of banks | `vehicle_dna.vin_dna.number_of_banks` |
| displacement (L) | `vehicle_dna.vin_dna.engine_displacement_liters` |
| Horizon | derived from `vehicle_dna.vin_dna.euro_emission_category` per §3 mapping |
| air metering strategy | derived from `vehicle_dna.vin_dna.air_metering_architecture.{has_maf_sensor,has_map_sensor}` per §6.2 |
| O₂ sensor type (canonical) | translated from `vehicle_dna.vin_dna.emissions.upstream_o2_type` per §6.3 |
| stress idle RPM target | `vehicle_dna.vin_dna.stress_idle_rpm_target` |
| presence of EGR | `vehicle_dna.vin_dna.emissions.egr_equipped` |

| primary symptom (Tier 1) | `vehicle_dna.symptom_dna.tier_1_primary_symptom` |
| symptom subfield (Tier 2) | `vehicle_dna.symptom_dna.tier_2_subfield_filter` |
| gas chemistry state | `gas_lab_output.chemical_state` |
| chemistry numbers | `gas_lab_output.{gas_co,gas_hc,gas_co2,gas_o2,gas_nox,lambda_chem}` |
| live trim delta | `obd_live_data.total_trim_correction_delta` |
| VE and trim analytics | `obd_live_data.{ve_pct,ve_validity,trim_analytics_gate,o2_failure_mode}` |
| sensor provenance | `obd_live_data.{maf_status,map_status}` |
| RPM state bucket | `obd_live_data.rpm_state_bucket` |
| DTCs (confirmed) | `dtc_lab_output.confirmed_dtcs` |
| DTC routing tags | `dtc_lab_output.routing_tags` |
| MIL flashing flag | `dtc_lab_output.mil_flashing` (triggers `catalyst_damage_imminent`) |
| Mode 06 monitor results | `dtc_lab_output.mode_06_monitors` |
| Freeze-frame context | `obd_live_data.freeze_frame_pids` |

Anything COMLab needs that isn't in this table is a contract gap — file a §10 change request rather than reaching into internal lab state.

### 5.1 Internal routing — LabRoutingDirective

**LabRoutingDirective** — produced by `symptom_router.route_symptom()`.
4 bool flags: `suppress_gaslab`, `suppress_obd_live_pids`,
`suppress_mode06_ui`, `cold_start_mode`. Consumed by
`LabPipelineAggregator.run_fallback_tree()` and `fault_atlas_router`.
Source: `data_flow_report.md §5.3`.

### 5.2 POA routing

**POA routing:** `fault_atlas_router` injects `DTCRoutingTag.POA_HISTORY`
when `gas_lab_output.chemical_state == "POA_SIGNATURE"`. This was
previously a cross-lab dependency (GASLab → DTCLab via `chemical_state`
param); removed in T-FX-3. DTCLab's `RoutingTagMapper.map()` takes no
external inputs.

---

## 6. Reconciliation of known drift between `VehicleDNA.md` and the wikis

`VehicleDNA.md` was drafted before the OBD/DTC vocabulary wikis crystallized. Some fields use different names for the same concept. The contract reconciles them as follows.

### 6.1 `induction_type` (VehicleDNA) ≠ "air metering strategy"

`vin_dna.induction_type` is a **mechanical** classifier (NATURALLY_ASPIRATED / TURBOCHARGED / SUPERCHARGED) describing how the engine breathes. It is **not** the same thing as the OBDLab BP's `air_metering_strategy`, which describes which sensors the ECU uses to measure that breath.

Keep `induction_type` as a separate field. Add `air_metering_strategy` as a derived value (see §6.2). Both belong in `VinDNA`.

### 6.2 `primary_load_calculation` (VehicleDNA) ↔ `air_metering_strategy` (OBDLab BP)

These are the same concept under two different names. Canonical mapping:

| `air_metering_architecture` booleans | VehicleDNA `primary_load_calculation` | OBDLab BP `air_metering_strategy` |
|---|---|---|
| `has_maf_sensor: true, has_map_sensor: true` | `HYBRID_MAF_MAP` | `DUAL_MAF_MAP_CROSSCHECK` |
| `has_maf_sensor: false, has_map_sensor: true` | `MAP_ONLY` | `MAP_ONLY_SPEED_DENSITY` |
| `has_maf_sensor: true, has_map_sensor: false` | `MAF_ONLY` | `MAF_ONLY` |

**Resolution:** `VinDNA` ships **both** fields. `primary_load_calculation` is the developer-friendly form; `air_metering_strategy` is the OBDLab-canonical form. They must agree (a contract test enforces this — §9.3). COMLab reads `air_metering_strategy`.

### 6.3 `upstream_o2_type` (VehicleDNA) ↔ `upstream_o2_sensor_type` (OBDLab BP)

Names differ slightly; values must align. Canonical mapping:

| VehicleDNA `upstream_o2_type` | OBDLab BP `upstream_o2_sensor_type` | Notes |
|---|---|---|
| `NARROWBAND` | `NARROWBAND_0_TO_1V` | classic 0.1-0.9V switching |
| `WIDEBAND_AFR` | `WIDEBAND_LINEAR` | linear AFR or lambda ratio |
| `WIDEBAND_LAMBDA` | `WIDEBAND_LINEAR` | alternate manufacturer encoding |
| `WIDEBAND_NB_SIM` | `WIDEBAND_NB_SIM` | aftermarket WB controller in NB simulation mode — 0–1 V swing, ECU sees NB signal |
| `NONE` | (n/a — vehicle lacks pre-cat O₂) | pre-OBD-II only |

**Resolution:** `VinDNA` keeps `upstream_o2_type` with the four values above. COMLab applies the mapping to drive its polymorphic O₂ normalization.

### 6.4 `euro_emission_category` — must be added to `VinDNA`

`VehicleDNA.md` Part A as currently drafted omits `euro_emission_category`. The contract requires it (COMLab uses it to derive Horizon for fault registry pruning). Acceptable values from `OBD_VOCABULARY.md` §4.1:

```
EURO_1 | EURO_2 | EURO_3 | EURO_4 | EURO_5 | EURO_6 | EURO_7
```

DNALab can compute Horizon from this:

```
EURO_1, EURO_2          -> HORIZON_LEGACY
EURO_3, EURO_4          -> HORIZON_ADAPTIVE
EURO_5, EURO_6, EURO_7  -> HORIZON_MODERN
```

### 6.5 `stress_idle_rpm_target` — must be added to `VinDNA`

Per `OBD_VOCABULARY.md` §3.2 and the user spec 2026-05-16: VINLab emits the per-vehicle stress-idle RPM target so OBDLab knows what high-RPM band to ask the technician to hold. Range 2800-5000. Examples:

```
Euro 1 NA 1.0L         -> 3000
Euro 3 NA 1.6L         -> 3500
Euro 4 NA 2.0L         -> 4000
Euro 5 turbo 1.4L      -> 4000
Euro 6 GDI 2.0L        -> 4500
```

### 6.6 `session_id` — moved from "metadata" to `vehicle_dna`

`OrchestratorLabBP.md` showed `session_id` inside a top-level `metadata` block. The contract relocates it: `session_id` lives inside `vehicle_dna`, generated by DNALab when it assembles the combined payload.

### 6.7 Volumetric Efficiency Gating (DEP-6)

A Volumetric Efficiency (VE) fault verdict (emitted in `obd_live_data.ve_validity` as `FAULT_VE_IDLE_COLLAPSE`, `FAULT_MAF_CONTAMINATION`, or `FAULT_VE_SENSOR_SKEW`) counts as independent sensor-diagnosis evidence *only* when the engine is equipped with both air sensors (`vehicle_dna.vin_dna.air_metering_strategy == DUAL_MAF_MAP_CROSSCHECK`).

Under single-sensor configurations (`MAP_ONLY_SPEED_DENSITY` or `MAF_ONLY`), the VE calculation is circular and cannot independently confirm a fault. For these configurations, the COMLab consumer (`T-COMV2-VE-GATE-1`) must suppress any VE-based verdicts and route instead to the single-sensor **P0068 rationality cross-check (MAF/MAP/TPS) + IAC/idle-MAP** fallback.

---

## 7. Who owns which field — change-ownership table

If you need to modify a field's semantics, this table says which lab is the authoritative editor. Other labs may *consume* but not *redefine* these.

| Field | Owner lab | Consumers |
|---|---|---|
| `vehicle_dna.vin_dna.*` | VINLab | DNALab, COMLab |
| `vehicle_dna.symptom_dna.*` | SymptomLab | DNALab, COMLab |
| `vehicle_dna.session_id` | DNALab | COMLab |
| `vehicle_dna.timestamp` | DNALab | COMLab |
| `vehicle_dna.schema_version` | this contract | all |
| `gas_lab_output.*` | GASLab | COMLab |
| `obd_live_data.*` | OBDLab | COMLab |
| `dtc_lab_output.*` | DTCLab | COMLab |
| `OrchestratorFinalUIOutput.*` | COMLab | UI |
| Fault registry rows | COMLab (config edit) | COMLab router |
| Mode 06 hex dictionary | DTCLab | DTCLab + COMLab |
| Era sensitivity masks | COMLab (config) | OBDLab via threshold injection |

---

## 8. The enum vocabulary — locked

Every enum below is locked at this contract version. Producers must emit ONLY these strings. Consumers must accept ALL of these strings.

```python
# from comlab/schemas/vocabulary.py — Phase 0b deliverable

class Horizon(StrEnum):
    LEGACY    = "HORIZON_LEGACY"
    ADAPTIVE  = "HORIZON_ADAPTIVE"
    MODERN    = "HORIZON_MODERN"

class EuroEmissionCategory(StrEnum):
    EURO_1 = "EURO_1"
    EURO_2 = "EURO_2"
    EURO_3 = "EURO_3"
    EURO_4 = "EURO_4"
    EURO_5 = "EURO_5"
    EURO_6 = "EURO_6"
    EURO_7 = "EURO_7"

class InductionType(StrEnum):
    NATURALLY_ASPIRATED = "NATURALLY_ASPIRATED"
    TURBOCHARGED        = "TURBOCHARGED"
    SUPERCHARGED        = "SUPERCHARGED"

class AirMeteringStrategy(StrEnum):
    DUAL_MAF_MAP_CROSSCHECK = "DUAL_MAF_MAP_CROSSCHECK"
    MAP_ONLY_SPEED_DENSITY  = "MAP_ONLY_SPEED_DENSITY"
    MAF_ONLY                = "MAF_ONLY"

class PrimaryLoadCalculation(StrEnum):
    HYBRID_MAF_MAP = "HYBRID_MAF_MAP"
    MAP_ONLY       = "MAP_ONLY"
    MAF_ONLY       = "MAF_ONLY"

class FuelDeliveryType(StrEnum):
    GDI            = "GDI"
    PORT_INJECTION = "PORT_INJECTION"
    CARBURETOR     = "CARBURETOR"

class UpstreamO2Type(StrEnum):
    NARROWBAND       = "NARROWBAND"
    WIDEBAND_AFR     = "WIDEBAND_AFR"
    WIDEBAND_LAMBDA  = "WIDEBAND_LAMBDA"
    WIDEBAND_NB_SIM  = "WIDEBAND_NB_SIM"  # aftermarket WB sensor outputting 0–1 V NB simulation signal to ECU
    NONE             = "NONE"

class RpmStateBucket(StrEnum):
    STABILIZED_IDLE         = "STABILIZED_IDLE"
    REGULATORY_HIGH_IDLE    = "REGULATORY_HIGH_IDLE"
    STRESS_IDLE             = "STRESS_IDLE"
    COLD_OPEN_LOOP_INVALID  = "COLD_OPEN_LOOP_INVALID"

class FaultFamily(StrEnum):
    LEAN_CONDITION    = "lean_condition"
    RICH_MIXTURE      = "rich_mixture"
    MISFIRE           = "misfire"
    SENSOR_FAULT      = "sensor_fault"
    ECU_FAULT         = "ecu_fault"
    CATALYST_FAILURE  = "catalyst_failure"
    EXHAUST_LEAK      = "exhaust_leak"
    IGNITION_FAULT    = "ignition_fault"
    MECHANICAL_WEAR   = "mechanical_wear"
    CAM_TIMING        = "cam_timing"
    NON_STARTER       = "non_starter"
    NO_FAULT          = "no_fault"

class SampleValidity(StrEnum):
    VALID               = "VALID"
    BORDERLINE          = "BORDERLINE"
    INVALID             = "INVALID"
    EXTERNAL_O2_SUSPECT = "EXTERNAL_O2_SUSPECT"

class Mode06Status(StrEnum):
    PASSED                 = "PASSED"
    PENDING_FAIL_MARGINAL  = "PENDING_FAIL_MARGINAL"
    CRITICAL_FAIL          = "CRITICAL_FAIL"

class HistoricalFaultContext(StrEnum):
    HISTORICAL_IDLE_FAULT     = "HISTORICAL_IDLE_FAULT"
    HISTORICAL_LOAD_FAULT     = "HISTORICAL_LOAD_FAULT"
    COLD_START_TRANSIT_FAULT  = "COLD_START_TRANSIT_FAULT"
    UNKNOWN                   = "UNKNOWN"

class DegradationMode(StrEnum):
    FULL_FUSION       = "FULL_FUSION"
    GAS_DOMINANT      = "GAS_DOMINANT"
    FATAL_INCOMPLETE  = "FATAL_INCOMPLETE"
    SINGLE_POINT      = "SINGLE_POINT"      # v2 (COMLab-internal): no 2nd frame / no calibration data →
                                           # additive single-point path runs unchanged, byte-identical (COMWIKI-07/§13)

class SeverityLevel(StrEnum):
    CRITICAL_IMMEDIATE_STOP        = "CRITICAL_IMMEDIATE_STOP"
    WARNING_DEGRADED_PERFORMANCE   = "WARNING_DEGRADED_PERFORMANCE"
    OPTIMAL_HEALTH                 = "OPTIMAL_HEALTH"

class VinConfidence(StrEnum):
    HIGH     = "HIGH"
    PARTIAL  = "PARTIAL"
    NONE     = "NONE"

class ProcessingConfidenceRating(StrEnum):
    HIGH_ASSURANCE      = "HIGH_ASSURANCE"   # v2: values LOCKED, but semantics redefined as calibrated
    DEGRADED_ASSURANCE  = "DEGRADED_ASSURANCE"  # posterior / likelihood-ratio bands (not evidence-chain
    LOW_CERTAINTY       = "LOW_CERTAINTY"    # completeness). See COMWIKI-09. Until the Gate-Data eval
                                            # subset exists, the bands are expert-set priors, flagged as such.
```

**Three larger enums live in separate files** because they grow per-case:

- `ChemicalSignature` (**34 values**, v2.1) — in `GAS_VOCABULARY.md` §21 / `OBD_VOCABULARY.md` §17. Owned by GASLab. The v2.1 timing-taxonomy split retired `WRONG_VALVE_TIMING` for three `CAM_TIMING_*` states (`CAM_TIMING_RETARDED_MAP` / `CAM_TIMING_RETARDED_MAF` / `CAM_TIMING_ADVANCED`); COMLab's local mirror reconciliation to 34 is `T-GV2-2`/`FU-1` (DEP-1, deferred to S4).
- `DTCRoutingTag` (16 values today, growing) — in `DTC_VOCABULARY.md` §11. Owned by DTCLab.
- `FaultNode` (the granular fault IDs like `Mechanical_Lean_Vacuum_Leak`) — extracted from cases CSV. Owned by COMLab via its fault registry.

These three are still locked at contract level (no producer can emit a value not in the enum) but are expected to grow with normal release cadence. Adding a value is a minor-version bump (§10).

---

## 9. Contract conformance — what every lab must test

Every producer ships at least these tests in its own repo. COMLab also runs them as a consumer-side integration check.

### 9.1 Schema test

Each producer test serializes a known input, parses the JSON, and asserts every field of its contract section is present with the correct type.

```python
# example for VINLab
def test_vin_dna_contract_round_trip():
    dna = decode("1FA6P8CF0HXXXXXXX")
    payload = dna.to_json()
    assert set(payload.keys()) >= {
        "vin", "make", "model_year",
        "engine_displacement_liters", "cylinder_count", "number_of_banks",
        "induction_type", "fuel_delivery_type",
        "air_metering_architecture", "emissions",
        "euro_emission_category", "stress_idle_rpm_target", "confidence",
    }
```

### 9.2 Enum-value test

Each producer asserts that any field it emits with an enum-valued type contains only values from §8 (or the three extended enums in their respective wikis).

```python
def test_obd_payload_uses_canonical_enums():
    payload = obdlab.translate(user_inputs)
    assert payload["rpm_state_bucket"] in {
        "STABILIZED_IDLE", "REGULATORY_HIGH_IDLE", "STRESS_IDLE", "COLD_OPEN_LOOP_INVALID"
    }
```

### 9.3 Cross-field consistency test (VINLab)

Specifically for the §6.2 reconciliation:

```python
def test_air_metering_consistency():
    dna = decode(vin)
    arch = dna["air_metering_architecture"]
    strategy = dna["air_metering_strategy"]
    if arch["has_maf_sensor"] and arch["has_map_sensor"]:
        assert strategy == "DUAL_MAF_MAP_CROSSCHECK"
    elif not arch["has_maf_sensor"] and arch["has_map_sensor"]:
        assert strategy == "MAP_ONLY_SPEED_DENSITY"
    elif arch["has_maf_sensor"] and not arch["has_map_sensor"]:
        assert strategy == "MAF_ONLY"
```

### 9.4 COMLab consumer test

COMLab ships a parameterized test that feeds a fixture payload (one VehicleDNA + one each of Gas/OBD/DTC) and asserts every key in §5 resolves cleanly. This is the integration check that catches drift from any producer.

```python
# COMLab/tests/integration/test_inbound_payload_contract.py
@pytest.mark.parametrize("fixture", ["hpfp_leak", "egr_dilution", "coil_arc", "healthy"])
def test_all_required_paths_resolve(fixture):
    payload = load_fixture(fixture)
    request = OrchestratorInboundRequest(**payload)
    # walk every path from §5 and assert it resolves without KeyError
```

---

## 10. Change protocol — how the contract evolves

The contract is intentionally hard to change. Anyone can propose; only the COMLab owner can merge.

| Change type | Semver bump | Process |
|---|---|---|
| **Patch:** clarify wording, fix typo, add example | 1.0 → 1.0.1 | one-line PR; merge after one reviewer |
| **Minor:** add new optional field, add value to growing enum (ChemicalSignature, DTCRoutingTag, FaultNode), tighten a range without breaking existing producers | 1.0 → 1.1 | PR with updated test suite + 2 reviewers (COMLab owner + at least one producer lab) |
| **Major:** rename field, remove field, restrict a value previously allowed, change a JSON shape | 1.x → 2.0 | RFC document required, all producer labs must accept before merge, 7-day comment window |

The current version is `schema_version: "1.3"` (2026-06-20) — the v2 fusion-spine alignment (§13). v1.0 (2026-05-17) was the first stable contract; v1.1 added `gas_co2`/`gas_nox`; v1.2 relocated `session_id` and the DNA slice.

`schema_version` flows through `VehicleDNA` and into `OrchestratorInboundRequest` so COMLab can refuse a payload from an older producer that hasn't been upgraded.

---

## 11. Open actions (must close before declaring 4DLab v1.0)

| # | Action | Owner | Status |
|---|---|---|---|
| 1 | Add `euro_emission_category` to `VehicleDNA.md` Part A and the eventual `vinlab/models.py` `VinDNA` dataclass | VINLab + DNALab | open |
| 2 | Add `stress_idle_rpm_target` to `VehicleDNA.md` Part A and `vinlab/models.py` | VINLab | open |
| 3 | Add `air_metering_strategy` field to `VinDNA` (alongside the existing `primary_load_calculation`) | VINLab | open |
| 4 | Add `model_year` to Part A | VINLab | open |
| 5 | Build `COMLab/comlab/schemas/vocabulary.py` from §8 of this contract (Phase 0b) | COMLab | done (T-FX-1) |
| 6 | Add the §9.4 consumer test to COMLab's regression suite | COMLab | done (contract tests in tests/) |
| 7 | DNALab's `to_json_payload()` round-trip test must use this contract's key names (`vin_dna`, `symptom_dna`), not the `"PART A:"` heading style | DNALab | open |
| 8 | OBDLab payload's `rpm_state_bucket` field replaces the older `current_engine_state_bucket` from OBDLab BP §2 | OBDLab | done (T-FX-1) |
| 9 | DTCLab payload exposes `mil_flashing` boolean separately from `active_mil` for catalyst-damage-imminent detection | DTCLab | done (T-FX-2) |
| 10 | Bulk-rename remaining `COMLab` references → `COMLab` across all docs (cosmetic, do after v1.0 ships) | COMLab | deferred |
| 11 | Reconcile dual engine-warmed thresholds (70 °C trim-analytics gate vs 75 °C `COLD_OPEN_LOOP_INVALID` bucket) to one consistent gate | COMLab (`OPEN_LEVERS F3`) | open (Phase 0) |
| 12 | Consolidate the two registries (REG-V2 shim ↔ `global_fault_registry.json`) — known +4 cases → 52.7 % | COMLab (`OPEN_LEVERS F1`) | open (Phase 0) |
| 13 | Reconcile `O2FailureMode` membership: v1 contract listed 4 values; OBDLab v2 emitter set differs — pin the authoritative set in `OBD_VOCABULARY.md` and mirror it | OBDLab + COMLab | open |
| 14 | Add optional **provenance flags** companion (observed/derived/imputed/synthetic/manual-override/sentinel/out-of-range/saturated) to ingestion; consumer = eval harness + validity gates + calibrator | COMLab (`COMWIKI-02/12`) | open (proposal, ships with Gate-Data) |
| 15 | Land the conflict-aware late-fusion stage + calibration layer + ranked-differential output; the 13 `T-COMV2-*` consumers become evidence inputs (not additive bumps) | COMLab (`COMWIKI-08/09/10`) | open (Stage 4) |
| 16 | Confirm Gate-Capture (second operating-point frame populated) before the delta module goes live; `T-COMV2-DELTA-1` builds default-off | human/manager (`COMWIKI-11/12/14`) | open (product gate) |

When all items 1-9 close, this contract is "v1.x stable" for the v1 boundary. Items 11–16 track the v2 fusion-spine rework (§13); they are additive and default-off at the seams, so the v1 boundary stays valid while they land.

---

## 12. Oil-Consumption Expansion (Registry & Proposals)

To align human-facing documentation with the production implementation, the five oil-consumption failure modes are resolved on the live path purely by the Fault Registry via the integration shim, completely bypassing the COMLab knowledge graph (KG).

### 12.1 Shipped Live Registry Rules

| Case ID | Failure Mode | Live Registry Rule ID | Live Diagnostic Logic |
|---|---|---|---|
| **P_NEW_09** | Worn piston rings | `MW-001` | Gated on `WORN_PISTON_RINGS` chemical state; `hc >= 200.0` (definitive), `co2 < 13.0` (suggestive), `o2 >= 1.5` (suggestive) |
| **P_NEW_10** | Degraded valve stem seals | `MW-002` | Gated on `WORN_VALVE_SEALS` chemical state; `hc >= 200.0` (definitive), `co2 < 13.0` (suggestive) |
| **P_NEW_12** | Blown head gasket (oil breach) | `MW-003` | Gated on `COOLANT_LEAK_INTERNAL` chemical state; `ect_c > 95.0` (suggestive) |
| **P_NEW_11** | Faulty PCV (stuck open) | `MW-008` | Gated on `POA_SIGNATURE` chemical state; `hc >= 500.0` (definitive), `high_idle_hc < 250.0` (gating), `lambda_chem < 0.94` (suggestive rich shift at idle) |
| **P_NEW_13** | Worn turbo turbine seals | `MW-009` | Gated on `POA_SIGNATURE` chemical state; `hc >= 500.0` (definitive), `co < 0.15` (definitive low CO), `lambda_chem ∈ [0.99, 1.01]` (gating stoich λ), `high_idle_hc < 200.0` (gating) |

### 12.2 Proposed SymptomDNA Oil Vocabulary (Count: 3)

The following symptom-triage pairs are registered as proposal-only in the proposals registry:

* `oil_consumption` -> `blue_smoke_on_cold_start_clears` (future consumer: U-OIL-KG-1)
* `oil_consumption` -> `blue_smoke_under_acceleration` (future consumer: T-OIL-R5 / U-OIL-KG-1)
* `oil_consumption` -> `oil_loss_no_visible_smoke` (future consumer: T-OIL-R4 / U-OIL-KG-1)

### 12.3 Proposed ChemicalSignature Additions

The following proposed chemical states map to existing runtime signals until coordinated schema bumps graduate them:

* `PCV_STUCK_OPEN` (emits `POA_SIGNATURE` today)
* `TURBO_SEAL_OIL_LEAK` (emits `POA_SIGNATURE` today)
* `HEAD_GASKET_OIL_BREACH` (emits `COOLANT_LEAK_INTERNAL` today)

### 12.4 Proposed KG Fault Nodes & Families

* `P_NEW_09` (worn rings) -> `Engine Mechanical (Piston Rings)`
* `P_NEW_10` (valve seals) -> `Engine Mechanical (Valve Stem Seals)`
* `P_NEW_11` (PCV open) -> `Engine Mechanical (PCV/Crankcase)`
* `P_NEW_12` (head gasket breach) -> `Engine Mechanical (Head Gasket)`
* `P_NEW_13` (turbo seal leak) -> `Engine Mechanical (Turbo Oil Seal)`

---

## 13. v2 fusion-spine alignment (2026-06-20)

This section records what the COMLab v2 rework changes about the **boundary**, so the contract
stays the single source of truth. Full reasoning is in the COMLab v2 wiki (`labs/comlab/wiki/`,
`COMWIKI-00…14`); this is the contract-level summary. **Governing principle: the rework is
additive and default-off at the seams** — when no second frame and no calibration data exist, the
boundary and the verdict path are byte-identical to v1 (`DegradationMode.SINGLE_POINT`). None of
the below breaks an existing producer.

### 13.1 What does NOT change

- The four-channel boundary, JSON-only rule, naming agreement (§2), and ownership table (§7).
- Emitter labs still emit **channels, not verdicts** — the cross-lab fault verdict is COMLab
  fusion. The new fusion stage is the single verdict surface; analytics still only quantify
  severity (`COMWIKI-01`, `COMWIKI-07`).
- COMLab still **mirrors emitter types locally**; no cross-lab Python imports.

### 13.2 Boundary additions (all optional / additive)

| Addition | Channel | Field(s) | Named consumer | Status |
|---|---|---|---|---|
| Second operating-point frame | GAS | `reading_high`, `high_idle_{hc,co,co2,o2,nox,lambda}` | `T-COMV2-DELTA-1` (`analytics/delta_engine.py`) | optional; live-gated on Gate-Capture |
| Fusion-evidence fields | OBD | `total_trim_correction_delta_b2`, `lambda_perception_delta`, `per_bank_trim_delta`, `fuel_system_status`, `per_cylinder_misfire_counts`, `w_theo`, `sensor_error_delta`, `ltft_cell_vector`, `intake_air_temp_c`, `throttle_pos_pct`, `coolant_temp_c`, `control_module_voltage_v` | the 13 `T-COMV2-*` consumers (`COMWIKI-13`) | emitted at S2; consumers forward-registered, authored at S4 |
| Freeze frame | DTC | `freeze_frame` (`FreezeFrameRecord`) | `T-COMV2-NOSTART-1` + fusion intermittent-fault branch | conditional (DTC stored); verdict-stage only, never a delta input |
| Provenance flags | ingestion | per-field companion ∈ {observed, derived, imputed, synthetic, manual-override, sentinel, out-of-range, saturated} | eval harness + validity gates + calibrator | **[PROPOSAL]** — §11 action 14 |

### 13.3 Semantics changed (no value changes)

- **Confidence tiers** (`ProcessingConfidenceRating`) are redefined as **calibrated posterior /
  likelihood-ratio bands**, not evidence-chain completeness (`COMWIKI-09`). Values are locked;
  meaning changes. Until the Gate-Data eval subset exists, bands are expert-set priors, flagged.
- **`ChemicalSignature` is 34-value** (v2.1 cam-timing split) — §3 / §8.
- **`DegradationMode.SINGLE_POINT`** added (COMLab-internal) for the no-2nd-frame fallback.
- The Stage-B additive tie-break is **frozen as the fallback**; the live verdict comes from a
  **conflict-aware late-fusion → calibration → ranked-differential** stage (`COMWIKI-08/09/10`).
  The differential (top-3 with per-candidate calibrated confidence) becomes the primary output;
  a single lead verdict is retained for back-compat.

### 13.4 Targets & gates (the honest framing)

- The measured achievable ceiling on the current four single-point channels is **70–80 %, not
  85 %** (provable ~9.6 % irreducible floor). Set the product target from Gate-Data, not from 85 %
  (`COMWIKI-12`).
- Two human/manager gates dominate: **Gate-Capture** (can a second frame be populated? → whether
  the delta rework is real) and **Target** (accept a measured-ceiling + differential product, or
  fund real data collection). See `COMWIKI-14` §human gates and §11 actions 15–16.

*End of contract.*
