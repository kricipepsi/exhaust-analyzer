# 4DLab UI — Field-Placement Map (for Claude Design)

**Purpose.** Use the existing `UI/exhaust-analyzer-main/app.py` Streamlit screen as
the **graphics guide only** (light theme, white inputs, `st.expander` dropdowns,
two-column field grids, native widgets, square-checkbox selects, `?` help icons).
The **fields inside** each panel are redefined here for 4DLab — app.py's specific
fields are *not* binding. This document specifies which input fields go where,
what makes each appear, the column layout, and the `?` guide text per expander.

**Hard rule.** Every field that **ships** must have a named consumer in COMLab
analytics or fault-atlas routing (signal/noise principle). All fields in this
revision have named consumers; see §14 for resolved items.

**Source provenance.** Types/ranges taken from `labs/gaslab/gaslab/contracts.py`
(`GasReading`), `labs/obdlab/obdlab/schemas/payload.py` + `core/pid_ingestion_validator.py`,
`labs/dtclab/dtclab/schemas/{payload,freeze_frame,mode06_result,vocabulary}.py`,
DNA contract `labs/vinlab/vinlab/models.py` (`VinDNA`) + `labs/symptomlab/symptomlab/models.py`,
and COMLab consumers in `labs/comlab/comlab/` (`core/fault_atlas_router.py`,
`core/lab_pipeline_aggregator.py`, `core/symptom_router.py`, `schemas/ingestion.py`).
(Per-lab `*_adapter` wiring lives in the app layer — `apps/wired/wired/composition.py` —
not in `comlab/`.)

---

## 0. Scope & layout summary

In scope: the **left sidebar** (module selector + Vehicle DNA + context) and the
**central 7 expanders**, both in the app.py expander style.

Central expanders, fixed order, with column density:

| # | Expander | Columns / row | Field count |
|---|---|---|---|
| 1 | GASLab (Low Idle) | **3 per row** (2 rows) | 6 (fixed, DNA-independent) |
| 2 | GASLab (High Idle) | **3 per row** (2 rows) | 6 (fixed, DNA-independent) |
| 3 | OBDLab (Low Idle) | **4 per row** | up to 11 (DNA-gated) |
| 4 | OBDLab (High Idle) | **4 per row** | up to 11 (DNA-gated) |
| 5 | DTCLab (DTC) | single-column stack | 2 checkboxes + 3 code fields |
| 6 | DTCLab (FF) | **4 per row** | 12 mandatory + 7 extended |
| 7 | DTCLab ($06) | **3 per row**, repeating | 3 per monitor row |

Out of scope: results/output rendering, the engine, any CSS/graphics change.

---

## 1. Global components (reuse app.py graphics)

### 1.1 Unified square checkbox — every confirmation/selection

Per the user: **every confirmation is a click in one small square checkbox**, one
size, one style, everywhere. It replaces radios, toggles and OK buttons. Reuse
the existing `_check_radio()` helper (`app.py` lines 228–265) for single-select
groups (one box checked, others auto-uncheck), and a plain `st.checkbox` for
independent yes/no confirmations.

### 1.2 Module selector — 4 checkboxes in the LEFT column (not on expanders)

A single sidebar block titled **"Modules in this diagnosis"** holds **4 square
checkboxes** — the user ticks which modules they will use:

1. ☐ GASLab  2. ☐ OBDLab  3. ☐ DTCLab  4. ☐ DNA / VIN

Rules:
- A central expander is **active only if its module box is ticked**. Unticked →
  that lab's expander is hidden (or rendered greyed/disabled). This is the channel
  switch: ticked = the channel is sent to the engine.
- The 7 central expanders map to the first three module boxes: GASLab box → GASLab
  (Low) + GASLab (High); OBDLab box → OBDLab (Low) + (High); DTCLab box → DTCLab
  (DTC) + (FF) + ($06).
- **DNA / VIN box drives field visibility, not a central expander.** When ticked,
  the sidebar VIN Lookup is shown. If the decode succeeds (confidence == HIGH),
  the decoded `VinDNA` gates central fields. If decode fails (PARTIAL or NONE) or
  DNA/VIN box is unticked, the UI drops straight to **"no-DNA basic mode"**
  (see §1.6) — basic input fields only, no manual overrides.

### 1.3 Sub-confirmation nesting ("sub-folder" indentation)

When a checked box reveals sub-confirmations or dependent fields, render those
**indented to the right** beneath the parent — a sub-folder look. Parent stays
flush-left; children indent one step (a second level indents again).

Streamlit pattern (no CSS change — use a narrow left spacer column):

```python
parent = st.checkbox("Add extended freeze-frame PIDs")
if parent:
    pad, body = st.columns([0.06, 0.94])   # 6% left offset = the indent
    with body:
        st.number_input("Commanded EGR (%)", ...)
```

Every "shown when …" rule below means: conditionally rendered **and** indented one
level under the control that gates it.

### 1.4 Per-expander `?` help circle

At the **right end of every expander title**, a small circle with a question mark;
on hover it shows the data-input requirements for that expander (where to read,
engine state, units). The `?` text is given per expander below. Individual fields
keep the inline `help=` tooltip already used in app.py.

### 1.5 DNA-driven rendering pattern

As in `StreamliteUI.md`: read the decoded `VinDNA` once, then plain `if` statements
draw or skip each field; skipped fields collapse the gap. Master switches in §2.

### 1.6 No-DNA basic mode (DNA/VIN box unticked)

Without DNA we cannot know banks/sensors/O₂ type, so render only the safe,
DNA-independent minimum:

- **GASLab:** all 6 fields (DNA-independent anyway — unchanged).
- **OBDLab:** Bank-1 only — Engine RPM, ECT, Calc load, STFT B1, LTFT B1, and a
  generic **Upstream O₂ (V)** (narrowband default). Hide Bank-2 trims, MAF, MAP,
  downstream O₂.
- **DTCLab (DTC):** unchanged (codes + MIL are DNA-independent).
- **DTCLab (FF):** 12 mandatory PIDs only; hide all extended/DNA-gated PIDs.
- **DTCLab ($06):** unchanged (monitor rows are DNA-independent).

---

## 2. The DNA contract — visibility switches (when DNA/VIN is ticked)

The sidebar **VIN Lookup** produces a `VinDNA`. These fields are the *only*
switches that show/hide central fields:

| DNA field (`VinDNA`) | Values | Drives |
|---|---|---|
| `number_of_banks` | 1 / 2 | Bank-2 trims (OBDLab STFT2/LTFT2; FF STFT2/LTFT2) |
| `air_metering_architecture.has_maf_sensor` | bool | OBDLab MAF field |
| `air_metering_architecture.has_map_sensor` | bool | OBDLab MAP field |
| `emissions.upstream_o2_type` | NARROWBAND / WIDEBAND_AFR / WIDEBAND_LAMBDA / WIDEBAND_NB_SIM / NONE | Upstream-O₂ field label, unit & range. **Overridable** via Hardware Overrides (§4.2b) for aftermarket WB installations. |
| `emissions.downstream_o2_present` | bool | OBDLab downstream O₂; FF `o2_voltage_b1s1` |
| `emissions.egr_equipped` | bool | FF commanded-EGR field |
| `emissions.has_catalyst` | bool | **Overridable** via Hardware Overrides (§4.2b) — de-cat checkbox sets to `False`. |
| `cylinder_count` | int | misfire-cylinder cap (sidebar symptom) |
| `induction_type` | NA / TURBO / SUPER | high-idle boost note in `?` text |
| `euro_emission_category` / `resolved_horizon` | enum | era warnings in `?` text |
| `confidence` | HIGH / PARTIAL / NONE | HIGH = DNA committed; PARTIAL or NONE = basic mode (§1.6), no manual overrides |

Routing-only flags (no input field): `has_catalyst`, `fuel_delivery_type`. CoC targets
(`co_low_idle`, `co_high_idle`, `target_lambda_v112`, `stress_idle_rpm_target`)
are **not inputs** — they feed the `?` guide / reference captions.

---

## 3. Reading the field tables

Each row: **Label** · **Widget** · **Range / unit** · **Visibility** (blank = always)
· **Consumer** (payload field → COMLab code path).

---

## 4. LEFT SIDEBAR

### 4.0 Block: `🧩 Modules in this diagnosis` (top of sidebar)

Four square checkboxes per §1.2: GASLab · OBDLab · DTCLab · DNA/VIN. Drives which
central expanders are active and whether DNA gating or basic mode applies.

`?` guide: *"Tick the data you'll enter today. Each ticked module opens its panel
in the centre and sends that channel to the engine. Tick DNA/VIN to decode the
car and auto-hide fields that don't apply; leave it off for a basic, show-all
diagnosis."*

### 4.1 Expander: `🔍 VIN Lookup` (shown when DNA/VIN ticked)

| Label | Widget | Range / unit | Visibility | Consumer |
|---|---|---|---|---|
| VIN (17 characters) | `st.text_input` | 17 chars | always | DNALab `vinlab.decode()` → `VinDNA` → COMLab `lab_pipeline_aggregator` |
| ✅ Use this decoded DNA | square checkbox | bool | when decode `confidence` ∈ {HIGH, PARTIAL} | commits `VinDNA` for the session |

Show the decode summary line (make · engine · displacement · induction · O₂ arch)
as app.py does. `?` guide: *"Enter the full 17-character VIN. A good decode
auto-fills the hardware profile and hides fields that don't apply. If it can't
decode, the UI switches to basic input mode — all DNA-dependent fields show in
their safe, narrowband-default form."*

### 4.2 No-DNA fallback (decode fails or DNA/VIN unticked)

No manual override input fields. When VIN decode returns PARTIAL or NONE confidence,
or the DNA/VIN module box is unticked, the UI drops straight to **basic mode** (§1.6)
with no prompts to fill in hardware details manually. The sidebar shows a brief
inline notice: *"VIN decode unavailable — using basic input mode."*

This keeps the signal/noise principle clean: without a confirmed `VinDNA`, we cannot
know which hardware-specific fields are meaningful, so the safe minimum is presented
rather than a guess.

### 4.2b Expander: `🛠️ Hardware Overrides` (shown when DNA/VIN active AND decode confidence == HIGH)

Two technician-settable overrides for aftermarket hardware that VIN decode cannot
detect. Both appear in a single expander, visible only when a HIGH-confidence VIN
decode is committed.

| Label | Widget | Options / Range | Default | Consumer |
|---|---|---|---|---|
| Upstream O₂ type override | `st.selectbox` | Auto (VIN-decoded) · Narrowband 0-1V (OEM) · Wideband NB-Sim (Aftermarket) | Auto (VIN-decoded) | OBDLab `O2SensorType` → `normalized_obd_lambda` + `perception_contradiction` upstream-type branch (WIDEBAND_NB_SIM resolved by T-FX-4) |
| De-catted vehicle | `st.checkbox` | bool | unchecked (catalyst present) | `VINLab/Emissions.has_catalyst` → `COMLab EmissionsConfiguration.has_catalyst` → `power_loss_analytics` catalyst index gate + `perception_contradiction` de-cat incoherence check (T-FX-11) |

**Override injection path:** both values travel via `raw_inputs["overrides"]` into
`composition.diagnose()`, which patches `emissions_dict` before building lab DNA
views. The O₂ override replaces `upstream_o2_type` in the emissions dict; the
de-cat checkbox sets `has_catalyst = False`.

**UI rendering:** when the O₂ override is not "Auto", the upstream-O₂ input field
in OBDLab (Low Idle) and OBDLab (High Idle) switches its label, unit and range to
match the selected sensor type, independent of the VIN-decoded value.

`?` guide: *"Override VIN-decoded values when aftermarket hardware is fitted.
Leave on 'Auto' to use the VIN-decoded value. Use Wideband NB-Sim when an
aftermarket wideband controller is wired to output a simulated narrowband signal
to the stock ECU. Check 'De-catted' if the catalytic converter has been physically
removed — this disables catalyst efficiency checks and enables de-cat detection
in the perception module."*

### 4.3 Context expanders (always shown) — square-checkbox selects

> ⚠ **Engine temperature prerequisite (mandatory, not a user input).** The
> diagnostic engine requires ECT ≥ 75 °C before trim / lambda / VE analytics are
> valid. This is enforced automatically by the thermal gate in
> `semantic_consistency_checker.py` (`_CUTOFF_ECT_COLD = 75`): if the entered
> `coolant_temp_c` is below 75 °C, `engine_warmed = false` is set and downstream
> analytics are frozen with flag `COLD_OPEN_LOOP_INVALID`. **Do not begin a
> diagnosis on a cold engine.** There is no user checkbox for this — it is a hard
> precondition, not a choice.

| Expander | Options | Consumer |
|---|---|---|
| ⛽ Fuel Blend | E0 · E5 · E10 | GASLab `brettschneider.py` stoich constants |
| 🛣️ Mileage | Unknown · Low · Mid · High | wear priors in `fault_atlas_router` |
| 🗒️ DTC Memory Status | Normal · Recently cleared (<50 mi) | DTCLab `freeze_frame.ff_codes_cleared_invalidated` |

### 4.4 Expander: `🩺 Primary Symptom` (SymptomDNA — Part B)

| Label | Widget | Visibility | Consumer |
|---|---|---|---|
| Primary symptom (Tier 1) | `st.selectbox` (catalog) | always | `SymptomDNA.tier_1_primary_symptom` → `symptom_router` |
| Subfield filter (Tier 2) | `st.selectbox` (depends on Tier 1; 18 valid pairs) | after Tier 1 (indented) | `SymptomDNA.tier_2_subfield_filter` |
| Misfiring cylinder | `st.slider` 1…`cylinder_count` | rough-idle/misfire Tier 1 only | symptom subfield |
| Occurs during | square select: Always · Cold only · Hot only · Intermittent | always | `environmental_conditions.occurs_during` |
| Engine state | square select: Running · Cranking · Won't start | always | `environmental_conditions.engine_state` |
| Free-text notes | `st.text_area` | always | `SymptomDNA.free_text_notes` |

**Complete Tier-1 → Tier-2 tree (18 valid pairs)**
Source: `labs/symptomlab/symptomlab/data/allowed_combinations.yaml`

| # | Tier 1 (display label) | Tier 2 options (display label) |
|---|---|---|
| 1 | 🚫 Vehicle Won't Start | Fast crank / whining · No crank / silent · Normal crank / zero RPM |
| 2 | 🔧 Rough Idle / Shudder | Cold engine only · Hot engine only · Constant shudder |
| 3 | ⬇️ Lack of Power / Hesitation | Flat / sluggish always · Only at high RPM / highway · Sudden jerk / stumble |
| 4 | ⛽ Poor Economy / Fuel Odour | Just poor MPG · Strong fuel smell · Right after fill-up |
| 5 | 🛑 Engine Dies / Stalls | When coasting to stop · Intermittent / random · Only when hot |
| 6 | 💨 Visible Exhaust Smoke | Black smoke · Blue / oily smell · White / sweet smell |

YAML enum keys → display labels mapping (exact strings from schema):

| Tier 1 enum key | Tier 2 enum key | UI display |
|---|---|---|
| `vehicle_wont_start` | `fast_crank_whining` | Fast crank / whining |
| `vehicle_wont_start` | `no_crank_silent` | No crank / silent |
| `vehicle_wont_start` | `normal_crank_zero_rpm` | Normal crank / zero RPM |
| `rough_idle_shudder` | `cold_engine_only` | Cold engine only |
| `rough_idle_shudder` | `hot_engine_only` | Hot engine only |
| `rough_idle_shudder` | `constant_shudder` | Constant shudder |
| `lack_of_power_hesitation` | `flat_sluggish_always` | Flat / sluggish always |
| `lack_of_power_hesitation` | `only_high_rpm_highway` | Only at high RPM / highway |
| `lack_of_power_hesitation` | `sudden_jerk_stumble` | Sudden jerk / stumble |
| `poor_economy_fuel_odor` | `just_poor_mpg` | Just poor MPG |
| `poor_economy_fuel_odor` | `strong_fuel_smell` | Strong fuel smell |
| `poor_economy_fuel_odor` | `right_after_fillup` | Right after fill-up |
| `engine_dies_or_stalls` | `when_coasting_to_stop` | When coasting to stop |
| `engine_dies_or_stalls` | `intermittent_random` | Intermittent / random |
| `engine_dies_or_stalls` | `only_when_hot` | Only when hot |
| `visible_exhaust_smoke` | `black_smoke` | Black smoke |
| `visible_exhaust_smoke` | `blue_oily_smell` | Blue / oily smell |
| `visible_exhaust_smoke` | `white_sweet_smell` | White / sweet smell |

Misfiring-cylinder slider is shown only for Tier 1 = `rough_idle_shudder` (all three Tier 2) and is capped at `cylinder_count` from `VinDNA` (4 if no DNA).

`?` guide: *"Pick the main complaint, then the sub-filter. Only the 18 catalogued
pairs are offered. Cranking / Won't-start relax the gas-chemistry checks. Engine
state 'Cranking' or 'Won't start' suppresses trim and λ analytics."*

### 4.5 Status panels (computed, no input — carry over)

- **Probe Depth Check** — warns if `CO + CO₂ < 12%` from GASLab Low-Idle gases.
- **Validation** — physical-bounds check on the GASLab Low-Idle gases.

---

## 5. CENTRAL 1 — `GASLab (Low Idle)` · 6 fields · 3 per row · fixed in all DNA

**RPM source: V10 Low Idle RPM (OPSI).** Readings taken at the stabilised low-idle
measurement point V10.

Title: `📊 GASLab (Low Idle)` + right-end `?`. **No DNA gating — all 6 always show.**
Two rows of three.

Row 1: CO · CO₂ · HC   Row 2: O₂ · NOx · Measured λ

| Label | Widget | Range / unit | Default | Consumer |
|---|---|---|---|---|
| CO (%) | `st.number_input` | 0.0–15.0, step 0.01 | 0.0 | `GasLabPayload.gas_co` → `gaslab_adapter` → `lab_pipeline_aggregator` → `fault_atlas_router` |
| CO₂ (%) | `st.number_input` | 0.0–22.0, step 0.1 | 0.0 | `GasLabPayload.gas_co2` |
| HC (ppm) | `st.number_input` | 0–20000, int | 0 | `GasLabPayload.gas_hc` |
| O₂ (%) | `st.number_input` | 0.0–22.0, step 0.01 | 0.0 | `GasLabPayload.gas_o2` |
| NOx (ppm) | `st.number_input` | 0–5000, int | 0 | `GasLabPayload.gas_nox` |
| **Measured λ (analyser)** | `st.number_input` | 0.500–2.000, step 0.001 | 1.000 | `GasLabPayload.lambda_measured` → `perception_contradiction.select_perception_lambda` (no-OBD fallback, T-FX-7) |

> ✅ **Measured λ — resolved (T-FX-7, 2026-05-22).** This field ships as the
> **no-OBD fallback** source for the perception-contradiction detector. When OBDLab
> is not active (module box unticked), `perception_contradiction.select_perception_lambda` selects
> `lambda_measured` in place of `normalized_obd_lambda` to pass to COMLab `perception_contradiction.detect()`.
> Consumer is `GasLabPayload.lambda_measured` → `wired/composition.py` (via `COMGasLabPayload`) →
> `perception_contradiction.select_perception_lambda`. See §14 #1.

`?` guide: *"Engine at V10 Low Idle RPM, fully warm (ECT ≥ 75 °C), stabilised
closed-loop idle. Probe ≥ 30 cm into the tailpipe (sidebar Probe-Depth check
confirms CO + CO₂ ≥ 12 %). All five gases are required — no 4-gas fallback. The
engine recomputes λ from the gases; enter the analyser's own Measured-λ reading if
OBDLab is not connected (it becomes the lambda perception source)."*

---

## 6. CENTRAL 2 — `GASLab (High Idle)` · 6 fields · 3 per row · fixed in all DNA

**RPM source: V11 High Idle RPM (OPSI).** Readings taken at the V11 high-idle
measurement point.

Identical 6-field 3×2 grid to §5 (same ranges, same `gaslab_adapter` high-idle
channel; Measured λ maps to `GasLabPayload.high_idle_lambda` → `R3b PID resolver`).

`?` guide: *"Hold at V11 High Idle RPM — the COC stress-idle target
(`stress_idle_rpm_target` from VIN, target λ ≈ `target_lambda_v112`). Engine fully
warm (ECT ≥ 75 °C). Same six fields as low idle. Turbo / supercharged: let boost
settle fully before reading."* (RPM / λ caption rendered from `VinDNA` when present.)

---

## 7. CENTRAL 3 — `OBDLab (Low Idle)` · 4 per row · DNA-gated

**RPM source: V10 Low Idle RPM (OPSI).** PIDs captured at the same stabilised V10
low-idle measurement point as GASLab Low Idle.

Raw OBD-II PIDs → `OBDLivePayload` (validated by `pid_ingestion_validator`,
O₂ normalised by `o2_normalizer`, trims by `trim_vector_aggregator`).

| Label | Widget | Range / unit | Visibility | Consumer |
|---|---|---|---|---|
| Engine RPM | number | 0–8000, int | always | `engine_rpm` → `obdlab_adapter` → `lab_pipeline_aggregator` |
| Coolant temp ECT (°C) | number | −40–140 | always | `coolant_temp_c` (derives `engine_warmed`) |
| Calc load (%) | number | 0–100 | always | `calculated_engine_load_pct` |
| STFT B1 (%) | number | −127–127 | always | `shrtft1` → `total_trim_correction_delta` |
| LTFT B1 (%) | number | −127–127 | always | `longft1` → `total_trim_correction_delta` |
| STFT B2 (%) | number | −127–127 | **`number_of_banks == 2`** (indented) | `shrtft2` → `total_trim_correction_delta_b2` |
| LTFT B2 (%) | number | −127–127 | **`number_of_banks == 2`** | `longft2` → `total_trim_correction_delta_b2` |
| MAF (g/s) | number | 0–655.35 | **`has_maf_sensor`** | `mass_airflow_gps` → VE engine |
| MAP / manifold vacuum (kPa) | number | 0–255 | **`has_map_sensor`** | `manifold_vacuum_kpa` → VE engine |
| Upstream O₂ — *label varies* | number | varies (below) | always (hidden if O₂ type NONE) | raw O₂ → `o2_normalizer` → `normalized_obd_lambda` (perception cross-check vs `lambda_chem`) |
| Downstream O₂ S12 (V) | number | 0.0–1.5 | **`downstream_o2_present`** | post-cat O₂ |

**Upstream-O₂ polymorphic field** (`emissions.upstream_o2_type`):

| Type | Label | Range / unit |
|---|---|---|
| NARROWBAND / WIDEBAND_NB_SIM | Upstream O₂ (V) | 0.0–1.0 V |
| WIDEBAND_LAMBDA | Upstream O₂ (λ) | 0.7–1.3 λ |
| WIDEBAND_AFR | Upstream O₂ (AFR) | ~10–20 :1 |
| NONE | *hidden* | — |

`?` guide: *"Capture at V10 Low Idle RPM — stabilised, closed-loop, ECT ≥ 75 °C.
Bank-2 boxes appear only on V-engines; MAF/MAP appear only for the sensors fitted;
the upstream-O₂ box auto-switches between V, λ and AFR to match the decoded sensor.
In basic mode (no DNA) only Bank-1 trims, RPM, ECT, load and a generic O₂ box show."*

---

## 8. CENTRAL 4 — `OBDLab (High Idle)` · 4 per row · DNA-gated

**RPM source: U2 RPM at stationary noise test (OPSI).** PIDs captured at the U2
measurement point (stationary noise test RPM), which is the high-idle reference
used for OBDLab trim and VE analytics.

Identical field set and visibility to §7, captured at the U2 measurement point
(same `obdlab_adapter` high-idle channel).

`?` guide: *"Capture at U2 RPM (stationary noise test point) — ECT ≥ 75 °C,
same DNA-gated field set as low idle. On turbocharged cars the VE-ceiling check
(Physics Gate 3) relaxes — read only after boost has fully settled."*

---

## 9. CENTRAL 5 — `DTCLab (DTC)` · single-column stack

Source: `DTCLabPayload` (DTC portion).

| Label | Widget | Notes | Consumer |
|---|---|---|---|
| ☐ MIL illuminated (solid) | square checkbox | bool | `active_mil` → `dtclab_adapter` → `lab_pipeline_aggregator` |
| ☐ MIL flashing (Class-A misfire) | square checkbox | bool | `mil_flashing` |
| Confirmed DTCs (Mode $03) | `st.text_area` | comma/space sep; each matches DTC regex (P0171) | `confirmed_dtcs` → `routing_tag_mapper` |
| Pending DTCs (Mode $07) | `st.text_area` | same format | `pending_dtcs` |
| Permanent DTCs (Mode $0A) | `st.text_area` | same format | `permanent_dtcs` |

`routing_tags` and `historical_fault_context` are **derived** by DTCLab — not
inputs. Some routing tags are DNA-gated (CATALYST/EGR/SAI) via `emissions.*`.

`?` guide: *"Enter codes exactly as the scanner reports them (P0171, P0420, P0300).
Tick the MIL boxes to match the dash lamp. Codes are grouped by scanner mode:
$03 confirmed, $07 pending, $0A permanent."*

---

## 10. CENTRAL 6 — `DTCLab (FF)` — Freeze Frame (Mode $02) · 4 per row

Source: `FreezeFrameRecord`. **12 mandatory PIDs** always shown (basic mode = these only):

| Label | Widget | Range / unit | Consumer field |
|---|---|---|---|
| Calc load (%) | number | 0.0–100.0, step 0.1 | `calculated_load_pct` |
| Engine RPM | number | 0–16383, int | `engine_rpm` |
| Coolant temp ECT (°C) | number | −40–215, int | `coolant_temp_c` |
| STFT B1 (%) | number | −100.0–99.22, step 0.01 | `short_term_ft1` |
| LTFT B1 (%) | number | −100.0–99.22, step 0.01 | `long_term_ft1` |
| MAP (kPa) | number | 0–255, int | `manifold_pressure_kpa` |
| Vehicle speed (km/h) | number | 0–255, int | `vehicle_speed_kmh` |
| Ignition advance (°BTDC) | number | −64.0–63.5, step 0.5 (neg = ATDC) | `ignition_advance_deg` |
| Intake air temp IAT (°C) | number | −40–215, int | `intake_air_temp_c` |
| MAF (g/s) | number | 0.0–655.35, step 0.01 | `maf_gps` |
| Throttle (%) | number | 0.0–100.0, step 0.1 | `throttle_pos_pct` |
| Fuel-system status | square select: CL · OL · OL_DRIVE · OL_FAULT | enum | `fuel_system_status` |

**Extended PIDs (§12.2, optional)** — behind a square checkbox **"Add extended
freeze-frame PIDs"**, rendered indented (sub-folder):

| Label | Range / unit | Visibility | Consumer field |
|---|---|---|---|
| STFT B2 (%) | −100.0–99.22, step 0.01 | `number_of_banks == 2` | `short_term_ft2` |
| LTFT B2 (%) | −100.0–99.22, step 0.01 | `number_of_banks == 2` | `long_term_ft2` |
| Upstream O₂ B1S1 (V) | 0.000–1.275, step 0.001 | `downstream_o2_present` | `o2_voltage_b1s1` |
| Barometric pressure (kPa) | 0–255, int | always in group | `barometric_pressure_kpa` |
| Commanded EGR (%) | 0.0–100.0, step 0.1 | **`egr_equipped`** | `commanded_egr_pct` |
| Run time since start (s) | 0–65535, int | always in group | `run_time_since_start_sec` |
| Fuel level (%) | 0.0–100.0, step 0.1 | always in group | `fuel_level_pct` |

Derived flags (`ff_open_loop_at_fault`, `ff_load_high_at_low_rpm`, `ff_ect_warmup`,
`ff_iat_ect_biased`, `ff_timing_retard_severe`, `ff_codes_cleared_invalidated`) are
**computed** — never inputs.

`?` guide: *"This is the single snapshot the ECU stored when it set the code — not
a live reading. Enter the 12 mandatory PIDs from the freeze-frame screen. Extended
PIDs are optional; Bank-2 and EGR rows appear only if the car has them."*

---

## 11. CENTRAL 7 — `DTCLab ($06)` — Mode $06 monitors · 3 per row, repeating

Source: `Mode06MonitorResult` dict, keyed `MID_<HEX>_TID_<HEX>`. **Repeating-row**
pattern with an **"Add monitor"** square checkbox/button that appends an indented
row group.

Per-row fields:

| Label | Widget | Range / unit | Consumer field |
|---|---|---|---|
| Monitor ID | `st.text_input` | `MID_<HEX>_TID_<HEX>` e.g. `MID_A2_TID_0B` | `monitor_id` |
| Result state | square select: Passed · Pending/marginal · Critical fail | enum | `state` (`Mode06MonitorState`) |
| Margin (%) | number | 0–100; neg = past limit | `margin_pct` |

`target_component` is **looked up** from `mode_06_hex_dictionary.json`, shown
read-only beside the row — not an input. Whole expander → `mode_06_monitors` →
`mode06_evaluator` → `dtclab_adapter` → `lab_pipeline_aggregator`.

`?` guide: *"Mode $06 reports each on-board monitor's self-test. Read the MID/TID
and margin from the scanner. >15% passes; 1–15% marginal; ≤0% critical fail. Add
one row per monitor — the component name is filled in from the MID/TID."*

---

## 12. Consolidated visibility rules (builder quick reference)

| Field(s) | Shown only when |
|---|---|
| Central expander active | its module box ticked in sidebar §4.0 |
| OBDLab/FF STFT B2, LTFT B2 | `number_of_banks == 2` |
| OBDLab MAF | `has_maf_sensor` |
| OBDLab MAP | `has_map_sensor` |
| OBDLab upstream-O₂ label/unit | branch on `upstream_o2_type` (hidden if NONE) |
| OBDLab downstream O₂, FF O₂ B1S1 | `downstream_o2_present` |
| FF commanded EGR | `egr_equipped` |
| sidebar misfire-cylinder cap | misfire symptom; cap = `cylinder_count` |
| DNA-gated fields at all | DNA/VIN module box ticked **and** decode confidence == HIGH; else **basic mode** (§1.6) |
| Hardware Overrides expander | DNA/VIN module box ticked **and** decode confidence == HIGH (§4.2b) |
| OBDLab upstream-O₂ label/unit | Override value takes precedence when set (§4.2b); else DNA-gated per `upstream_o2_type` |

GASLab's 6 fields are **never** DNA-gated.

---

## 13. Module-picker decision (resolved)

Per the user: **4 square checkboxes in the left column** (GASLab, OBDLab, DTCLab,
DNA/VIN) — *not* a checkbox on each central expander. Ticking a module activates
its central expander(s) and sends that channel to the engine. The DNA/VIN box is
special: ticked = decode the car and gate fields by hardware; unticked = no-DNA
basic mode (§1.6), showing only the most basic DNA-independent fields. This keeps
channel-presence explicit (vs app.py inferring it from non-zero fields) using the
same unified square-checkbox component everywhere.

---

## 14. Open items / unplanned follow-ups (off-scope for this map)

| # | Item | Status / why |
|---|---|---|
| 1 | **GASLab Measured-λ consumer — RESOLVED.** T-FX-6 (perception-contradiction detector) and T-FX-7 (no-OBD fallback measured λ) both shipped 2026-05-22. Consumer: `GasLabPayload.lambda_measured` → `perception_contradiction.select_perception_lambda` → `perception_contradiction.detect()`. Field ships as an active input (not display-only) when OBDLab is inactive. | ✅ **Done — T-FX-6 / T-FX-7** |
| 2 | **Tier-1 → Tier-2 symptom pair table — RESOLVED.** Full 18-pair tree documented in §4.4 with YAML keys and display labels. Source: `allowed_combinations.yaml`. | ✅ **Done — included in §4.4** |
| 3 | Mode $06 `mode_06_hex_dictionary.json` lookup for live `target_component` display | engine-side, not UI-map |

---

## 15. Verification notes

- Every **shipping** field traces to a real schema field (cited in §0). All fields
  have named consumers — GASLab lambda_measured resolved as T-FX-7 no-OBD fallback
  (§5 / §14 #1 ✅).
- Ranges/types match source schemas: `GasReading` (CO 0–15, CO₂/O₂ 0–22, HC
  0–20000, NOx 0–5000); `OBDLivePayload` (RPM 0–8000, ECT −40–140, trims
  −127–127, MAF 0–655.35, MAP 0–255); `FreezeFrameRecord` 12 mandatory + 7
  extended (all ranges fully specified — RPM 0–16383, ECT/IAT −40–215, MAP/BAP
  0–255 kPa, speed 0–255 km/h, ignition −64–63.5 °, trims −100–99.22 %,
  MAF 0–655.35 g/s, EGR/throttle/fuel 0–100 %, run-time 0–65535 s, O₂ 0–1.275 V);
  `Mode06MonitorResult` (MID/TID pattern, state enum, margin 0–100 / neg).
- DNA switches match `VinDNA` exactly; truth-vs-perception path confirmed in
  `comlab/schemas/ingestion.py:184` (OBD `normalized_obd_lambda` vs `lambda_chem`).
  Manual DNA overrides removed — failed / missing decode → basic mode (§1.6);
  DNA gates only when confidence == HIGH (§4.2).
- Engine temperature is a **hard precondition** (ECT ≥ 75 °C, enforced by thermal
  gate `_CUTOFF_ECT_COLD = 75` in `semantic_consistency_checker.py`) — not a user
  input. Engine Temperature checkbox removed from §4.3.
- RPM measurement sources: GASLab Low = V10 (OPSI), GASLab High = V11 (OPSI),
  OBDLab Low = V10 (OPSI), OBDLab High = U2 stationary noise test (OPSI).
- Module selector = 4 sidebar checkboxes; DNA-off behaviour defined in §1.6.
- Symptom tree: full 18-pair tier-1/tier-2 catalog included in §4.4 (source:
  `allowed_combinations.yaml`).
- Layout density: GASLab 3/row (6 fixed), OBDLab 4/row, FF 4/row, $06 3/row, DTC
  single-column. Graphics unchanged — every widget already exists in app.py.
