# DTC Vocabulary Wiki

**Purpose:** the authoritative vocabulary DTCLab uses internally and exposes to COMLab. Every enum, canonical DTC name, freeze-frame field, Mode $06 monitor key, confidence weight, and DNA-derived gate in the DTCLab codebase derives from this file.

**Status:** v1.0 (2026-05-19). Replaces and supersedes `DTCLab/docs/_archive/master_wiki_v1_pre_split.md` (the prior monolithic `DTCLab_Master_Wiki.md`) and the older `COMLab/docs/wiki/DTC_VOCABULARY.md` v1.0 (2026-05-16) where they drift. Companion to `DTC_WIKI.md` — wiki is the reasoning grammar; this is the contract layer.

**Scope:** petrol vehicles 1990 – 2020 (Euro 1 – Euro 6/7), manually entered diagnostic data, SAE J1979 OBD-II. DTC classes processed: `P` (powertrain). Classes `B`, `C`, `U` are recognised by the regex but routed only when their DTCs appear in §13 — otherwise filtered at the ingestion gate.

**Anchored to:**

- `COMLab/docs/wiki/SEMANTIC_CONTRACT.md` — boundary protocol; reserves the names `DTCLabPayload`, `DTCRoutingTag`, `Mode06MonitorState`.
- `COMLab/docs/wiki/DNALab_TO_COMLab_FLOW.md` — DNA flow; reserves the `mil_flashing` + `P030x` → `CRITICAL_IMMEDIATE_STOP` catalyst-damage gate (§4.B.8).
- `4DLab/NewArchProposal_ImplementationPlan.md §4 Step 2` — `DtcLabDnaView` shape (see §14 below).
- `DTC_WIKI.md` — section-cited throughout.

---

## 1. Standards anchored

| Standard | Scope | Used here for |
|---|---|---|
| **ISO 15031-6 (≡ SAE J2012 / J2012DA)** | DTC code structure, numbering conventions | Canonical regex, system class characters, subgroup digit |
| **ISO 15031-5 (≡ SAE J1979 / J1979DA)** | OBD-II service modes, PID definitions | Mode identifiers ($02–$0A), freeze frame PIDs, fuel system status |
| **ISO 14229 (UDS)** | Unified Diagnostic Services | Mode $06 MID/TID architecture |
| **SAE J1699-3** | OBD-II test procedures | Monitor readiness and enable conditions |

---

## 2. DTC code structure (per ISO 15031-6 ≡ SAE J2012)

A DTC is a 5-character alphanumeric string.

```
P  0  1  7  1
│  │  └──┴──┴── Fault number (3 hex digits, 000–FFF)
│  └─────────── Subgroup digit (0 = generic SAE, 1–3 = manufacturer-specific)
└────────────── System class character
```

### 2.1 System class characters

| Character | System | 4DLab handling |
|---|---|---|
| `P` | Powertrain | Fully decoded; routed per §13 |
| `B` | Body | Recognised; not routed in v1 |
| `C` | Chassis | Recognised; not routed in v1 |
| `U` | Network / Bus | Recognised; not routed in v1 |

### 2.2 Subgroup digit

| Digit | Meaning |
|---|---|
| `0` | Generic SAE — standardized across manufacturers |
| `1` | Manufacturer-specific extension of a generic code |
| `2` | Manufacturer-specific |
| `3` | Manufacturer-specific |

### 2.3 Canonical regex

```python
DTC_REGEX: Final[str] = r"^[BCPU][0-3][0-9A-F]{3}$"
```

**Note:** the legacy blueprints (`DTCLab/bp/DTCLabBP.md`, `COMLab/.../OrchestratorLabBP.md`) showed `^[B-D,P,U][0-3][0-9]{3}$`. That pattern is incorrect — the comma and hyphen inside the character class match literal characters, and `D` is not a valid DTC class. The canonical regex above supersedes the BPs. The drift guard in `tests/unit/test_vocabulary.py` rejects any `B-D,P,U` token under `dtclab/`.

---

## 3. OBD-II service modes consumed

| Mode (hex) | SAE J1979 name | DTCLab use |
|---|---|---|
| `$02` | Request Freeze Frame Data | `FreezeFrameRecord` (§12) |
| `$03` | Request Confirmed DTCs | `confirmed_dtcs` list |
| `$06` | Request On-Board Monitor Test Results | `mode_06_monitors` dict |
| `$07` | Request Pending DTCs | `pending_dtcs` list |
| `$0A` | Request Permanent DTCs | `permanent_dtcs` list |

Modes `$01`, `$04`, `$05`, `$08`, `$09` are out of scope (live PIDs are OBDLab; clearing is technician concern; etc.).

---

## 4. `DTCRoutingTag` — 19-value enum

The fault-family routing surface emitted at the COMLab boundary. Single source of truth: this section. Drift guards key on this 19-member block.

```python
from enum import StrEnum

class DTCRoutingTag(StrEnum):
    """Fault-family routing hint derived from confirmed DTCs.

    Consumed by COMLab fault atlas router to pre-prune the candidate
    registry before full scoring. Source: this vocab §4.
    """
    LEAN_HISTORY         = "LEAN_HISTORY"           # P0171, P0174
    RICH_HISTORY         = "RICH_HISTORY"           # P0172, P0175
    MISFIRE_HISTORY      = "MISFIRE_HISTORY"        # P0300–P0312
    CATALYST_HISTORY     = "CATALYST_HISTORY"       # P0420, P0430
    EGR_HISTORY          = "EGR_HISTORY"            # P0400–P0409
    O2_HISTORY           = "O2_HISTORY"             # P0130–P0161
    INJECTOR_HISTORY     = "INJECTOR_HISTORY"       # P0200–P0212
    VVT_HISTORY          = "VVT_HISTORY"            # P0010–P0023
    EVAP_HISTORY         = "EVAP_HISTORY"           # P0440–P0459
    THERMAL_HISTORY      = "THERMAL_HISTORY"        # P0116–P0128 (ECT/thermostat)
    ECU_INTERNAL_HISTORY = "ECU_INTERNAL_HISTORY"   # P0600–P0699
    POA_HISTORY          = "POA_HISTORY"            # gas-chem signature only; no direct DTC
    IDLE_CONTROL_HISTORY = "IDLE_CONTROL_HISTORY"   # P0505–P0511
    BOOST_HISTORY        = "BOOST_HISTORY"          # P0234, P0299, P0235–P0245
    KNOCK_HISTORY        = "KNOCK_HISTORY"          # P0325–P0334
    COOLANT_SYSTEM_MALFUNCTION = "COOLANT_SYSTEM_MALFUNCTION"  # P0128/P0117 in OL_FAULT (cross-field)
    CYLINDER_FLUID_MISFIRE     = "CYLINDER_FLUID_MISFIRE"      # P030x in CL (cross-field, coolant evidence)
```

**Total: 18 routing tags.** A 16-value enum (dropping `POA_HISTORY`) is the older COMLab vocab shape — wrong for DTCLab. A 4-value enum is the forbidden v6 shape.

**`POA_HISTORY` origin (this vocab is canonical):** Piston/valve oil-aerosol burning produces a gas-chem fingerprint (HC high, CO low, λ ≈ 1.00) but **does not trigger a direct DTC**. COMLab injects `POA_HISTORY` when GasLab's payload reports `chemical_state == "POA_SIGNATURE"` (T-FX-3). DTCLab's `RoutingTagMapper` never emits `POA_HISTORY`. The older COMLab vocab's "P250C + P0300 fallout" reading is superseded — `P250C` is an oil-level code, not an oil-burning marker; P0300 is downstream noise, not a primary POA signal.

### 4.1 Per-value DNA gate summary

| Value | DNA gate (must hold to emit) | Reasoning ref |
|---|---|---|
| `LEAN_HISTORY` | none | §4.2; DTC_WIKI §7 |
| `RICH_HISTORY` | none | §4.2; DTC_WIKI §10.2, §12.2 |
| `MISFIRE_HISTORY` | none (cylinder math needs `cylinder_count` from DNA when keyed per-cyl) | §4.2; DTC_WIKI §8 |
| `CATALYST_HISTORY` | `emissions.has_catalyst = true` | §4.2; DTC_WIKI §9.1 |
| `EGR_HISTORY` | `emissions.egr_equipped = true` | §4.2; DTC_WIKI §9.2 |
| `O2_HISTORY` | none | §4.2; DTC_WIKI §12.4 |
| `INJECTOR_HISTORY` | none | §4.2; DTC_WIKI §10.2 |
| `VVT_HISTORY` | none | §4.2; §13.3 (MID $3D) |
| `EVAP_HISTORY` | none | §4.2; DTC_WIKI §10.2 |
| `THERMAL_HISTORY` | none | §4.2; DTC_WIKI §3 |
| `ECU_INTERNAL_HISTORY` | none | §4.2; DTC_WIKI §13 |
| `POA_HISTORY` | none (chemistry-driven) | §4.2; DTC_WIKI §10.3 |
| `IDLE_CONTROL_HISTORY` | none | §4.2 |
| `BOOST_HISTORY` | none | §4.2 |
| `KNOCK_HISTORY` | none | §4.2; DTC_WIKI §8.2 |
| `COOLANT_SYSTEM_MALFUNCTION` | none (cross-field: P0128/P0117 + OL_FAULT) | §4; CoolantLeakSig.md TS51_DTC |
| `CYLINDER_FLUID_MISFIRE` | none (cross-field: P030x + CL) | §4; CoolantLeakSig.md TS52_DTC |

When `DtcLabDnaView.confidence == PARTIAL` or `NONE`, the gated values fall back to "emit if the DTC pattern matches" — the DNA gate is a *filter*, not a *requirement*. Logged downgrade per `NewArchProposal §3.3`.

**Cross-references to DNA-gate flags (prose form, for the three gated tags).** `CATALYST_HISTORY` is gated by `DtcEmissionsView.has_catalyst`. `EGR_HISTORY` is gated by `DtcEmissionsView.egr_equipped`. `SAI_HISTORY` is gated by `DtcEmissionsView.secondary_air_equipped`. Each gate links a `DTCRoutingTag` enum value (§4) to a `DtcEmissionsView` boolean flag (§14) via the `DtcLabDnaView` projection consumed by `DTCLab.__init__`.

### 4.2 DTC-to-routing-tag fan-out (prose anchor)

The §15 mapping table and `dtclab/config/routing_tag_map.yaml` remain canonical, but the relations are restated here as prose so each DTC-family → tag link is unambiguous. Read every sentence as `<DTC range> routes to <TAG>`.

DTC P0010–P0023 (VVT / cam phaser actuator) routes to `VVT_HISTORY`. DTC P0100–P0115 (MAF, MAP, IAT circuits) routes to `LEAN_HISTORY`. DTC P0116–P0128 (ECT / thermostat) routes to `THERMAL_HISTORY`. DTC P0130–P0167 (O₂ sensor circuits and heaters) routes to `O2_HISTORY`. DTC P0171 and P0174 (fuel-system lean) routes to `LEAN_HISTORY`. DTC P0172 and P0175 (fuel-system rich) routes to `RICH_HISTORY`. DTC P0200–P0212 (injector circuit / performance) routes to `INJECTOR_HISTORY`. DTC P0230–P0233 (fuel pump primary) routes to `LEAN_HISTORY`. DTC P0234, P0299 and P0235–P0245 (turbo / boost) routes to `BOOST_HISTORY`. DTC P0300–P0312 (misfire), P0335 / P0340 (CKP / CMP) and P0351–P0358 (ignition coils) route to `MISFIRE_HISTORY`. DTC P0325–P0334 (knock sensor) routes to `KNOCK_HISTORY`. DTC P0400–P0409 (EGR flow) routes to `EGR_HISTORY`. DTC P0420 and P0430 (catalyst efficiency) routes to `CATALYST_HISTORY`. DTC P0440–P0459 (EVAP system) routes to `EVAP_HISTORY`. DTC P0505–P0511 (idle air control) routes to `IDLE_CONTROL_HISTORY`. DTC P0562, P0563, P0600 and P0641–P0643 (system voltage, serial link, sensor reference) route to `ECU_INTERNAL_HISTORY`. `POA_HISTORY` has no direct DTC and is injected by COMLab when GASLab reports `chemical_state == "POA_SIGNATURE"` (T-FX-3). DTC P0128/P0117 (thermostat/ECT) in OL_FAULT routes to `COOLANT_SYSTEM_MALFUNCTION` (cross-field: requires both DTC match and fuel_status == OL_FAULT). DTC P030x (misfire) in CL routes to `CYLINDER_FLUID_MISFIRE` (cross-field: requires both DTC starts-with P030 and fuel_status == CL).

All 17 `DTCRoutingTag` values therefore have at least one explicit routing relation above: `LEAN_HISTORY`, `RICH_HISTORY`, `MISFIRE_HISTORY`, `CATALYST_HISTORY`, `EGR_HISTORY`, `O2_HISTORY`, `INJECTOR_HISTORY`, `VVT_HISTORY`, `EVAP_HISTORY`, `THERMAL_HISTORY`, `ECU_INTERNAL_HISTORY`, `POA_HISTORY`, `IDLE_CONTROL_HISTORY`, `BOOST_HISTORY`, `KNOCK_HISTORY`, `COOLANT_SYSTEM_MALFUNCTION`, `CYLINDER_FLUID_MISFIRE`.

---

## 5. `DTCSeverityClass` — 4 values

Per ISO 15031-6 §6 (≡ SAE J2012). Determines MIL behavior and urgency of repair.

```python
class DTCSeverityClass(StrEnum):
    A = "A"  # catalyst-damaging — MIL flashes on first detection
    B = "B"  # emission-relevant — MIL solid after 2 consecutive drive cycles
    C = "C"  # driveability / non-emission — MIL may light or warning only
    D = "D"  # informational — no MIL
```

| Class | Examples | Implication |
|---|---|---|
| `A` | P0300 (active random misfire) | Catalyst-damage path; force `CRITICAL_IMMEDIATE_STOP` when paired with `mil_flashing=true` |
| `B` | P0171, P0172, P0420 | Standard MIL confirmation cycle |
| `C` | P0505, P0507, P0562 | Reduced performance; no catalyst risk |
| `D` | P0600, P0641, U-codes | Internal monitors, network faults |

**Catalyst-damage gate (wiki §5):** `mil_flashing == true` AND any confirmed DTC matches `P030[0-9]` → COMLab forces `severity_level = CRITICAL_IMMEDIATE_STOP` regardless of confidence ranking. DTCLab supplies the inputs; COMLab applies the gate.

---

## 6. `DTCState` — 3 values

```python
class DTCState(StrEnum):
    PENDING   = "PENDING"     # Mode $07 — failed once, awaiting confirmation
    CONFIRMED = "CONFIRMED"   # Mode $03 — confirmed across drive cycles; MIL on
    PERMANENT = "PERMANENT"   # Mode $0A — survives scanner clears until monitor re-runs
```

The state is captured *implicitly* by which list the DTC appears in (`pending_dtcs`, `confirmed_dtcs`, `permanent_dtcs`). The enum is exposed for typed APIs in `dtclab/core/*` only; the wire payload uses the three lists.

---

## 7. `Mode06MonitorState` — 3 values

```python
class Mode06MonitorState(StrEnum):
    PASSED                = "PASSED"                  # margin > 15% — confidence 0.0
    PENDING_FAIL_MARGINAL = "PENDING_FAIL_MARGINAL"   # margin 1–15% — confidence 0.4
    CRITICAL_FAIL         = "CRITICAL_FAIL"           # margin ≤ 0% — confidence 0.7
```

**Class name is `Mode06MonitorState`** (not `Mode06Status` — the older COMLab vocab shape; superseded here).

Margin boundary tri-state:

| Margin % | State |
|---|---|
| ≤ 0 | `CRITICAL_FAIL` |
| 1 – 15 | `PENDING_FAIL_MARGINAL` |
| 16 – 100 | `PASSED` |

Margin = 0 is `CRITICAL_FAIL` (boundary inclusive on the fail side); margin = 15 is `PENDING_FAIL_MARGINAL`; margin = 16 is `PASSED`.

### 7.1 Universal MID groups (prose anchor)

The full universal MID inventory is in §13.2 (table) and §13.3 (prose); the principal monitor groups are named here, early, as prose so they are unambiguous discrete entities. MID range $A1–$A9 are the per-cylinder misfire accumulator monitors. MID $21 and $22 are the Bank 1 and Bank 2 catalyst oxygen-storage-capacity (OSC) tests. MID $01 and $02 are the upstream and downstream O₂-sensor response monitors. Each MID group reports through a `Mode06MonitorResult` keyed `MID_<HEX>_TID_<HEX>` and carries a `Mode06MonitorState`.

---

## 8. `FuelSystemStatus` — 4 values

```python
class FuelSystemStatus(StrEnum):
    CL       = "CL"        # Closed loop — O₂ feedback active
    OL       = "OL"        # Open loop — base map (cold start)
    OL_DRIVE = "OL_DRIVE"  # Open loop driving (WOT, decel)
    OL_FAULT = "OL_FAULT"  # Open loop due to O₂ sensor fault
```

The older COMLab vocab uses a single `OPEN_LOOP` token; this 4-value enum supersedes that. DTCLab needs the granularity to apply the open-loop fault rule and the WOT-power-enrichment exception (wiki §12.1, §10.2 of the predecessor wiki).

---

## 9. `HistoricalFaultContext` — 4 values

```python
class HistoricalFaultContext(StrEnum):
    HISTORICAL_IDLE_FAULT       = "HISTORICAL_IDLE_FAULT"
    HISTORICAL_LOAD_FAULT       = "HISTORICAL_LOAD_FAULT"
    COLD_START_TRANSIT_FAULT    = "COLD_START_TRANSIT_FAULT"
    UNKNOWN                     = "UNKNOWN"
```

Trigger conditions (priority order: cold-start first, then idle, then load, else unknown):

| Value | Trigger condition |
|---|---|
| `COLD_START_TRANSIT_FAULT` | `coolant_temp_c < 60°C` |
| `HISTORICAL_IDLE_FAULT` | `engine_rpm < 1000` AND `calculated_load_pct < 25` |
| `HISTORICAL_LOAD_FAULT` | `engine_rpm > 2000` AND `calculated_load_pct > 45` |
| `UNKNOWN` | none of the above |

This enum is **absent from the older COMLab vocab** — adopted here as DTCLab-owned per architect decision 2026-05-19.

---

## 10. The `DTC_REGEX` constant

Module-level on `dtclab/schemas/vocabulary.py`:

```python
from typing import Final

DTC_REGEX: Final[str] = r"^[BCPU][0-3][0-9A-F]{3}$"   # canonical; see §2.3
```

Drift-guard test pins both the regex value AND bans the BP form `B-D,P,U` from any `*.py` file under `dtclab/`.

---

## 11. `DTCLabPayload` — top-level JSON contract

The single payload DTCLab emits at the COMLab boundary. Canonical field names below; every downstream consumer must use them verbatim.

```python
class DTCLabPayload(BaseModel):
    """Wire format from DTCLab to COMLab. JSON-only at the boundary.

    Source: this vocab §11; consumed by lab_pipeline_aggregator at the
    `dtc_lab_output` key of OrchestratorInboundRequest.
    """
    active_mil:                bool
    mil_flashing:              bool
    confirmed_dtcs:            list[str]                       # each matches DTC_REGEX
    pending_dtcs:              list[str]
    permanent_dtcs:            list[str]
    routing_tags:              list[DTCRoutingTag]
    mode_06_monitors:          dict[str, Mode06MonitorResult]  # keys: MID_<HEX>_TID_<HEX>
    historical_fault_context:  HistoricalFaultContext
    freeze_frame:              FreezeFrameRecord
```

**Field-level constraints (Pydantic):**

- Each string in `confirmed_dtcs` / `pending_dtcs` / `permanent_dtcs` matches `DTC_REGEX` (`ERR-CONTRACT-001` on violation).
- `routing_tags` items are valid `DTCRoutingTag` enum values (`ERR-CONTRACT-002` on violation).
- `mode_06_monitors` keys match `^MID_[0-9A-F]{2}_TID_[0-9A-F]{2}$`.
- `mil_flashing = true` ∧ any `P030[0-9]` in `confirmed_dtcs` → COMLab applies `CRITICAL_IMMEDIATE_STOP` (DTCLab supplies inputs; does not apply).

---

## 12. `FreezeFrameRecord` schema (§10 of predecessor wiki)

Mode `$02` snapshot at fault confirmation. **All freeze-frame field names are bare** (no `freeze_frame_` prefix — the older COMLab convention is superseded here).

### 12.1 Mandatory PIDs — 12 fields

| Canonical name | SAE PID | Type | Unit | Constraint |
|---|---|---|---|---|
| `calculated_load_pct` | `$04` | float | % | `ge=0, le=100` |
| `engine_rpm` | `$0C` | int | RPM | `ge=0` |
| `coolant_temp_c` | `$05` | float | °C | none (negative legal) |
| `short_term_ft1` | `$06` | float | % | none |
| `long_term_ft1` | `$07` | float | % | none |
| `manifold_pressure_kpa` | `$0B` | float | kPa | `ge=0` |
| `vehicle_speed_kmh` | `$0D` | int | km/h | `ge=0` |
| `ignition_advance_deg` | `$0E` | float | ° BTDC | none |
| `intake_air_temp_c` | `$0F` | float | °C | none |
| `maf_gps` | `$10` | float | g/s | `ge=0` |
| `throttle_pos_pct` | `$11` | float | % | `ge=0, le=100` |
| `fuel_system_status` | `$03` | `FuelSystemStatus` | enum | enum-validated |

Missing any field → mark payload `FREEZE_FRAME_INCOMPLETE` and degrade confidence.

### 12.2 Extended PIDs — optional

| Canonical name | Description |
|---|---|
| `short_term_ft2`, `long_term_ft2` | STFT/LTFT Bank 2 |
| `o2_voltage_b1s1` | Bank 1 upstream O₂ voltage |
| `barometric_pressure_kpa` | Ambient pressure |
| `commanded_egr_pct` | EGR valve commanded position |
| `run_time_since_start_sec` | Engine run time when fault set |
| `fuel_level_pct` | Fuel level |

### 12.3 Derived symptom flags — 6 bool fields

Computed by `freeze_frame_extractor.py` from the mandatory PIDs:

| Flag | Trigger |
|---|---|
| `ff_open_loop_at_fault` | `fuel_system_status ∈ {OL, OL_FAULT, OL_DRIVE}` |
| `ff_load_high_at_low_rpm` | `calculated_load_pct > 70` AND `engine_rpm < 1500` |
| `ff_ect_warmup` | `coolant_temp_c < 60` |
| `ff_iat_ect_biased` | `|intake_air_temp_c − coolant_temp_c| > 30` AND `engine_rpm == 0` |
| `ff_timing_retard_severe` | `ignition_advance_deg < −10` |
| `ff_codes_cleared_invalidated` | `codes_cleared` (from session context) |

---

## 13. `Mode06MonitorResult` schema

```python
class Mode06MonitorResult(BaseModel):
    monitor_id:       str                  # MID_<HEX>_TID_<HEX>
    state:            Mode06MonitorState
    margin_pct:       float                # 0–100; negative = past limit
    target_component: str                  # from mode_06_hex_dictionary.json
```

### 13.1 MID/TID key form

```
"MID_<HEX>_TID_<HEX>"

Examples:
  "MID_A2_TID_0B"   Cylinder 2 misfire accumulator
  "MID_21_TID_81"   Bank 1 catalyst OSC test
  "MID_01_TID_01"   Bank 1 upstream O₂ rich→lean response time
```

### 13.2 Universal MID inventory (CAN-equipped vehicles, 2008+)

| MID range | Monitor system | Key TIDs |
|---|---|---|
| `$A1`–`$A9` | Misfire per cylinder | `$0B` accumulator count |
| `$21` / `$22` | Catalyst Bank 1 / Bank 2 OSC | `$81` OSC, `$80` light-off |
| `$01` / `$02` | O₂ sensor response B1S1 / B1S2 | `$01` rich→lean, `$07` lean→rich, `$08` switch period |
| `$05` / `$06` | O₂ heater performance | `$01` heater current |
| `$31`–`$3A` | EVAP leak (size-graded) | `$83` 0.040″, `$84` 0.020″ |
| `$3B` / `$3C` | EGR flow / cooler bypass | `$80` flow rate |
| `$3D` | VVT phaser accuracy | `$84` phase degree error |
| `$13` | Fuel system rail pressure | `$80` rail pressure target |
| `$71` | Secondary air injection | `$80` flow test |
| `$81` / `$82` | Fuel rail pressure (GDI) | `$83` HPFP duty |
| `$E1` | Thermostat / cooling | `$80` warm-up time vs spec |

Manufacturer-specific MIDs are layered on top via `dtclab/config/mode_06_hex_dictionary.json`.

### 13.3 Universal MID range reference (prose form)

The §13.2 table is also restated as prose so each MID range is an extractable concept rather than only a table row. Each `MID range` below is a named entity referenced from `DTC_WIKI.md` §6 (Mode $06 early warning), §8.1 (secondary-ignition breakdown), §9.1 (catalyst efficiency), and §13 (non-start). Mode 06 monitor results for each range arrive in `DTCLabPayload.mode_06_monitors` keyed `MID_<HEX>_TID_<HEX>` and validated against `Mode06MonitorState` (§7).

**MID `$A1`–`$A9` — Misfire per cylinder.** Misfire accumulator monitors, one MID per cylinder ($A1 = cyl 1, $A2 = cyl 2, … $A9 = cyl 9 on inline-9 / V-bank configurations). Key TID is `$0B` (accumulator count). These MIDs underpin the false-lean masking rule (`DTC_WIKI.md §4.2`) and the secondary-ignition breakdown isolation in §8.1.

**MID `$21` / `$22` — Catalyst OSC Bank 1 / Bank 2.** Catalyst oxygen-storage-capacity tests. Key TIDs are `$81` (OSC test) and `$80` (light-off). MID `$21` TID `$81` is the pre-DTC early warning for P0420 (`DTC_WIKI.md §9.1`). A `CRITICAL_FAIL` on MID `$21` after a flashing-MIL drive is the catalyst-damage signature in non-start cases (`DTC_WIKI.md §13.3`).

**MID `$01` / `$02` — O₂ sensor response B1S1 / B1S2.** Upstream and downstream O₂ sensor response monitors. Key TIDs are `$01` (rich→lean response time), `$07` (lean→rich response time), and `$08` (switch period). MID `$01` failing implies sensor degradation that invalidates fuel-trim evidence per `DTC_WIKI.md §12.4`.

**MID `$05` / `$06` — O₂ heater performance.** Heater current monitors for upstream and downstream sensors; TID `$01` reports heater current. A failing heater delays closed-loop entry, extending the `OL` / `OL_FAULT` window covered by `DTC_WIKI.md §4.1` (open-loop fault rule).

**MID `$31`–`$3A` — EVAP leak size-graded.** Evaporative-emissions leak tests with TIDs identifying leak orifice size (`$83` 0.040″, `$84` 0.020″). These MIDs are the pre-DTC early warning surface for the P0440–P0459 range routed by `EVAP_HISTORY` (§4.2; `DTC_WIKI.md §10.2`).

**MID `$3B` / `$3C` — EGR flow / cooler bypass.** EGR-system monitors. Key TID `$80` reports flow rate. MID `$3B` is the pre-DTC pre-monitor for P0400–P0409 routed by `EGR_HISTORY` (§4.2; `DTC_WIKI.md §9.2`).

**MID `$3D` — VVT phaser accuracy.** Variable-valve-timing actuator accuracy monitor. Key TID `$84` reports phase-degree error against commanded position. MID `$3D` is the direct pre-DTC monitor for the P0010–P0023 range routed by `VVT_HISTORY` (§4.2).

**MID `$13` — Fuel system rail pressure.** Rail-pressure target-vs-actual monitor. Key TID `$80` reports rail-pressure target. Cross-reference: `DTC_WIKI.md §7.1` mentions MID `$13` as the fuel-system pressure monitor consulted alongside vacuum-leak diagnosis.

**MID `$81` / `$82` — Fuel rail pressure (GDI).** Direct-injection high-pressure rail monitors. Key TID `$83` reports HPFP (high-pressure-fuel-pump) duty cycle. These MIDs corroborate `INJECTOR_HISTORY` on GDI vehicles (§4.2; `DTC_WIKI.md §10.2`).

**MID `$E1` — Thermostat / cooling.** Warm-up-time-vs-spec monitor. Key TID `$80` reports warm-up time. MID `$E1` is the pre-DTC early warning for the P0116–P0128 range routed by `THERMAL_HISTORY` (§4.2; `DTC_WIKI.md §3`).

---

## 14. `DtcLabDnaView` — DNA-first input contract (NEW)

Per `NewArchProposal_ImplementationPlan.md §4 Step 2`. Slim projection of `VehicleDNA` containing only fields DTCLab consumes. DTCLab does **not** import COMLab — it defines its own mirror of this shape under `dtclab/schemas/dna_view.py`.

```python
class DtcLabDnaView(BaseModel):
    """Slim VehicleDNA projection consumed by DTCLab.

    Source: this vocab §14; produced by COMLab.project(..., target='dtc').
    """
    make:                            str
    model:                           str
    model_year:                      int
    euro_emission_category:          EuroEmissionCategory
    air_metering_strategy:           AirMeteringStrategy
    resolved_horizon:                ResolvedHorizon
    emissions:                       DtcEmissionsView
    confidence:                      VinConfidence

class DtcEmissionsView(BaseModel):
    has_catalyst:              bool       # gates CATALYST_HISTORY
    egr_equipped:              bool       # gates EGR_HISTORY
```

### 14.1 Enums referenced by the view

These are mirrored from DNALab/VINLab — DTCLab declares its own copies so it does not import `dnalab`.

```python
class EuroEmissionCategory(StrEnum):
    EURO_1 = "EURO_1"
    EURO_2 = "EURO_2"
    EURO_3 = "EURO_3"
    EURO_4 = "EURO_4"
    EURO_5 = "EURO_5"
    EURO_6 = "EURO_6"
    EURO_7 = "EURO_7"
    UNKNOWN = "UNKNOWN"

class AirMeteringStrategy(StrEnum):
    MAF = "MAF"
    MAP_SPEED_DENSITY = "MAP_SPEED_DENSITY"
    HYBRID = "HYBRID"

class ResolvedHorizon(StrEnum):
    HORIZON_LEGACY = "HORIZON_LEGACY"   # Euro 1–2
    HORIZON_CLASSIC = "HORIZON_CLASSIC" # Euro 3–4
    HORIZON_MODERN = "HORIZON_MODERN"   # Euro 5+

class VinConfidence(StrEnum):
    HIGH    = "HIGH"
    PARTIAL = "PARTIAL"
    NONE    = "NONE"
```

### 14.2 Confidence-gated behaviour

| `confidence` | Behaviour |
|---|---|
| `HIGH` | DNA gates apply strictly — gates enforced per the per-tag rules above. |
| `PARTIAL` | DNA gates degrade to *advisory* — log a `dna_gate_downgraded` flag; emit routing tag regardless if the DTC pattern matches |
| `NONE` | DNA gates inactive — pure DTC-pattern routing (the pre-DNA fallback) |

### 14.3 Where the view comes from

```
UI → DNALab.build_vehicle_dna(vin, triage) → VehicleDNA
   → COMLab.project(vehicle_dna, target='dtc') → DtcLabDnaView
   → DTCLab(raw_dtc_inputs, dna_view) → DTCLabPayload
```

DTCLab's constructor signature replaces the prior `vin_dna: dict | None` with the typed `dna_view: DtcLabDnaView | None`. `None` is still permitted for backwards-compat tests and is treated equivalently to `confidence = NONE`.

---

## 15. DTC → routing-tag mapping table

Lives in `dtclab/config/routing_tag_map.yaml` with `source_wiki:` provenance keys. The canonical content:

| DTC code | Description | Routing tag | Severity |
|---|---|---|---|
| P0010–P0023 | VVT / camshaft position actuator circuit, phaser response | `VVT_HISTORY` | B |
| P0100–P0104 | MAF circuit / performance | `LEAN_HISTORY` | B |
| P0105–P0109 | MAP / BARO circuit | `LEAN_HISTORY` | B |
| P0110–P0115 | IAT circuit | `LEAN_HISTORY` | B |
| P0116–P0128 | ECT circuit / range / thermostat | `THERMAL_HISTORY` | B |
| P0130–P0147 | O₂ B1S1 circuit, heater | `O2_HISTORY` | B |
| P0150–P0167 | O₂ B2S1 circuit, heater | `O2_HISTORY` | B |
| P0171 | Fuel system lean — Bank 1 | `LEAN_HISTORY` | B |
| P0172 | Fuel system rich — Bank 1 | `RICH_HISTORY` | B |
| P0174 | Fuel system lean — Bank 2 | `LEAN_HISTORY` | B |
| P0175 | Fuel system rich — Bank 2 | `RICH_HISTORY` | B |
| P0200–P0212 | Injector circuit / performance | `INJECTOR_HISTORY` | B–C |
| P0230–P0233 | Fuel pump primary circuit | `LEAN_HISTORY` | B |
| P0234 | Turbo overboost | `BOOST_HISTORY` | A |
| P0235–P0245 | Turbo / boost general | `BOOST_HISTORY` | B |
| P0299 | Turbo underboost | `BOOST_HISTORY` | B |
| P0300 | Random / multiple misfire | `MISFIRE_HISTORY` | A |
| P0301–P0312 | Cylinder-specific misfire | `MISFIRE_HISTORY` | A |
| P0325–P0334 | Knock sensor | `KNOCK_HISTORY` | B |
| P0335, P0340 | CKP / CMP position | `MISFIRE_HISTORY` | B |
| P0351–P0358 | Ignition coil A–H | `MISFIRE_HISTORY` | B |
| P0400–P0409 | EGR flow malfunction | `EGR_HISTORY` | B |
| P0420 | Catalyst efficiency — Bank 1 | `CATALYST_HISTORY` | B |
| P0430 | Catalyst efficiency — Bank 2 | `CATALYST_HISTORY` | B |
| P0440–P0459 | EVAP system | `EVAP_HISTORY` | C |
| P0505–P0511 | Idle air control | `IDLE_CONTROL_HISTORY` | C |
| P0562, P0563 | System voltage low / high | `ECU_INTERNAL_HISTORY` | C |
| P0600 | Serial communication link | `ECU_INTERNAL_HISTORY` | D |
| P0641, P0642, P0643 | Sensor reference voltage | `ECU_INTERNAL_HISTORY` | C |

Transmission DTCs (P0700, P0730, P0741, P0841) are recognised by regex but not mapped to a routing tag — they pass through `confirmed_dtcs` without contributing to routing.

---

## 16. Confidence weights per DTC state

| Source | Confidence weight | Rationale |
|---|---|---|
| Mode `$03` confirmed | **1.0** | Two-drive-cycle confirmation |
| Mode `$0A` permanent | **1.0** | Emissions-critical, monitor-confirmed |
| Mode `$07` pending | **0.5** | Single failure |
| Mode `$06` `CRITICAL_FAIL` | **0.7** | Test failed |
| Mode `$06` `PENDING_FAIL_MARGINAL` | **0.4** | Approaching limit |
| Mode `$06` `PASSED` | **0.0** | No contribution |

These are constants in `dtclab/schemas/vocabulary.py` exposed as `DTC_CONFIDENCE_WEIGHTS: Final[Mapping[…, float]]` with `# wiki:` provenance.

---

## 17. COMLab integration contract (§24 of predecessor wiki)

### 17.1 Wire entry point

COMLab accepts `DTCLabPayload` only nested under `dtc_lab_output` of `OrchestratorInboundRequest`. The payload must pass COMLab's Pydantic gate before any routing.

### 17.2 Cross-boundary field ownership

| Field | Owner | Consumer |
|---|---|---|
| `confirmed_dtcs`, `pending_dtcs`, `permanent_dtcs` | DTCLab | COMLab fault router — confidence scoring |
| `routing_tags` | DTCLab | COMLab fault atlas — pre-prune registry |
| `mode_06_monitors` | DTCLab | COMLab fault router — pre-DTC early warning |
| `historical_fault_context` | DTCLab | COMLab fault router — context weighting |
| `freeze_frame` | DTCLab | COMLab fault router — idle/load discrimination |
| `mil_flashing` | DTCLab | COMLab orchestrator — catalyst-damage-imminent gate |

### 17.3 Ingestion failure routing

Per `NewArchProposal §3.2`: if DTCLab raises an ingestion error (malformed DTC, missing freeze-frame PID, regex violation), the error goes **straight to the UI**, not through COMLab's fallback tree. COMLab's `Fallback_Error_Execution_Tree` is reserved for post-ingestion missing-data cases.

### 17.4 DTC fallback strategies (COMLab-owned)

Per OrchestratorLabBP §"global_fault_registry.json". These are COMLab fault-registry concepts — DTCLab does not own them, and they do not appear in the DTCLab canonical copy of this file. They are documented here because COMLab's `vocabulary.py` pins against this wiki.

```python
class DTCFallbackStrategy(StrEnum):
    REQUIRE_MATCH              = "REQUIRE_MATCH"               # rule fires only with matching DTC
    PROCEED_ON_MATCH_OR_EMPTY  = "PROCEED_ON_MATCH_OR_EMPTY"   # rule fires if DTC matches OR no DTCs present
    PROCEED                    = "PROCEED"                     # DTC ignored; chemistry alone decides
```

`PROCEED_ON_MATCH_OR_EMPTY` is the most common — lets the system catch faults early (no MIL yet) without false positives when an unrelated DTC is set.

---

## 18. What this vocab explicitly does NOT define

These belong to upstream or parallel modules:

- **Gas Lab `chemical_state` strings** (`POA_SIGNATURE`, `RICH_MIXTURE`, etc.) — owned by `GAS_VOCABULARY.md`; consumed by COMLab (not DTCLab) for `POA_HISTORY` injection per T-FX-3.
- **OBD live PID canonical names** (`shrtft1`, `longft1`, `absolute_engine_load_pct`, etc.) — owned by `COMLab/docs/wiki/OBD_VOCABULARY.md`.
- **VIN-derived enum content beyond the `DtcLabDnaView` slice** — `VINLab` / `DNALab` own the full `VehicleDNA`; DTCLab consumes the slim view in §14.
- **Fault node IDs** (`Mechanical_Lean_Vacuum_Leak`, `GDI_HPFP_Internal_Seal_Leak`, etc.) — owned by COMLab's global fault registry.
- **Manufacturer-specific Mode $06 MIDs beyond the universal inventory** — owned by `dtclab/config/mode_06_hex_dictionary.json`.
- **UI severity card rendering** — owned by `COMLab/docs/wiki/UI_WORKFLOW.md`.
- **Self-healing delta math** (`Δ_Healing = |FF_Total_Trim| − |Mode$06_Current_Correction|`) — DTCLab supplies the freeze-frame inputs; the formula lives in COMLab.
- **Chemistry math, lambda, power-loss, mechanical-degradation logic** — out of scope per the data-isolation invariant (`DTC_WIKI.md §0`).

---

## 19. Standards references (sources)

- SAE J2012 / J2012DA — DTC code structure
- SAE J1979 / J1979DA — OBD-II modes & PIDs
- ISO 15031-5 / 15031-6 — international DTC equivalents
- ISO 14229 (UDS) — Mode $06 MID/TID
- SAE J1699-3 — monitor enable conditions

**Anchored 4DLab documents:**

- `COMLab/docs/wiki/SEMANTIC_CONTRACT.md` — cross-lab boundary protocol
- `COMLab/docs/wiki/DNALab_TO_COMLab_FLOW.md` §4.B.8 — catalyst-damage gate
- `4DLab/NewArchProposal_ImplementationPlan.md` §4 — DNA-first arch & `DtcLabDnaView`
- `GASLab/docs/wiki/GAS_VOCABULARY.md` — POA signature contract surface
