# UI build contract — T-SHIP-UI-1 (input to T-SHIP-UI-2)
**Date:** 2026-07-07 · **Author:** Cowork architect · **Owner ruling:** same graphics look
as the old UI, populated with ALL fields.

## 1. Field inventory diff (FieldMap vs live `diagnose()` surface)
**Baseline map:** `apps/ui/4DLab_UI_FieldMap.md` (T-UI-SYNC-1-reconciled) remains the
placement contract for the sidebar (module picker, Vehicle DNA, SymptomLab context) and the
7 central expanders (GAS low/high ×6, OBD low/high ×11 DNA-gated, DTC stack, FF 12+7, $06
monitors ×3/row). Those panels map 1:1 onto the live payload builders
(`apps/wired/wired/composition.py`, `apps/wired/v7/load_corpus.py:106-300`) — spot-checked
current: `lambda_measured`, `has_catalyst`, `fuel_sys_status` all live.
One stale reference: the map's provenance note cites `apps/wiredV2/wiredv2/composition.py` —
the live composer is `apps/wired/wired/composition.py` (fix in passing at UI-2).

**NEW since the map — the 36 C2..C9 columns (corpus header cols 75-110,
`cases_petrol_v7.csv`; per-column consumer comments at `load_corpus.py:228-276`).**
All 36 are real `diagnose()` inputs with named registry-shim consumer states and MUST appear
in the UI (owner: "all fields"). None are lay-user data — every one is a workshop
measurement — so they form a NEW 8th central expander **"Advanced / workshop signals"**,
collapsed by default, sub-grouped:

| Group (producer state) | Columns | Widget hints |
|---|---|---|
| Rich/catalyst — C2 (`CatalystConversionState`) | mode06_catalyst_margin_pct, catalyst_index_ratio, stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct, pre_post_cat_hc_delta_ppm, pre_post_cat_co_delta_pct, decel_co_pct | number inputs, % / ppm units |
| ECU electrical — C3 (`ControlPlausibilityState`) | koeo_map_baro_delta_kpa, module_voltage_loaded_v, dlc_signal_ground_drop_v, bidirectional_fuel_response_ok_bool | 3 numbers + 1 checkbox |
| Sensor dynamics — C6 (`SensorDynamicsState`) | mode06_o2_response_margin_pct, maf_actual_calc_delta_pct_idle/_2500, maf_gps_idle/_2500, calc_airflow_gps_idle/_2500 | numbers |
| Lean root-cause — C5 (`LeanRootCauseState`) | stft_load_pct, ltft_load_pct, calc_load_wot_pct, fuel_rail_pressure_load_kpa, wideband_lambda_wot | numbers |
| Leak/dilution — C4 (`C4SignalState`) | co2_idle_pct, tailpipe_o2_elevation_pct, downstream_o2_v, propane_trim_shift_pct | numbers |
| Health confirm — C9 (`HealthConfirmationState`) | readiness_supported_complete_bool, stored/pending/permanent_dtc_count, mode06_min_margin_pct, warmup_cycles_since_clear, miles_since_clear | 1 checkbox + 5 ints + 1 number |

Empty = omitted (loader semantics: blank cell → field absent → producer abstains). The UI
must never default-fill these — an untouched field stays out of the payload.

## 2. Look extraction (owner: same as old UI)
Graphics guide = the FieldMap's own §1 rules, sourced from the archived app:
`ARCHIVE/4DLabWired/app.py` (read-only reference) + `apps/ui/_sample_app_reference.py`
(1195-line copy, incl. `_check_radio()` at ~lines 228-265). Preserve: light theme, white
inputs, `st.expander` panels, 2/3/4-per-row `st.columns` grids, unified square checkbox
(replaces radios/toggles/OK), `?` help icons per expander. `apps/ui/UI design/`
(React/HTML) is a divergent later concept — NOT the target (fork F-2 below).

## 3. Verdict rendering (new — the map scoped outputs out; v3 changed them)
Render `OrchestratorFinalUIOutput` (`labs/comlab/comlab/schemas/response.py`):
1. **Ranked top-3 differential** — winner + `differential_siblings` (first 2 distinct
   families), each with family, fault name, confidence.
2. **ABSTAIN as a first-class outcome** (78/294 abstain by design): when
   `diagnostic_verdict.abstained`, show "No single confident verdict — top candidates:"
   with the ranked list and `abstain_reason` (floor/margin). Never style as an error.
3. **Calibration caveat** (canon Provisional-synthetic #3), static footer: "Rankings are
   calibrated on research-grounded synthetic signal data until real measurements accumulate."
4. Confidence display: band label + score; do not invent precision (scores saturate — see
   F-V7-CONF-SAT memo).

## 4. Build parameters (decided per audit/DECISIONS; forks below)
- Home: `apps/ui/app.py`, importing **only** `wired.diagnose()` (+ mirrors of its output
  types) — composition boundary per D-V2-9; no lab imports.
- Single-file Streamlit; run via `.venv-wired`.
- Payload assembly mirrors `load_corpus.py` typing exactly (floats/ints/bools/JSON lists).

## 5. Owner forks (recommendation first — UI-2 proceeds on these unless overruled)
- **F-1 advanced expander default:** collapsed (recommended) vs always open.
- **F-2 look source:** archived Streamlit app.py look (recommended; matches "same as old
  UI") vs the `UI design/` React mock.
- **F-3 DNA source:** VIN decode via vinlab in-UI (recommended — brand join fixed in
  T-SHIP-3) vs manual DNA entry only.

## Success criteria for T-SHIP-UI-2 (carry into its spec)
Every FieldMap field + all 36 advanced columns present and wired; untouched fields absent
from payload (assert in a widget→payload unit test); MW-002 fixture entered via UI returns
fault_code MW-002; an abstain case renders the §3.2 pattern; ruff/pyright clean.

## Amendment 2026-07-08 — per-field help tooltips (owner requirement)
Every payload-feeding input widget must carry a Streamlit `help=` hover tooltip with two
lines: (1) one lay-readable sentence on the field's function, (2) `Range: min–max unit`
(or `Options: …`). Tooltip and widget `min_value`/`max_value` come from one shared
`FIELD_HELP` table so they cannot drift. The per-expander `?` guides from FieldMap §1
remain; this ADDS the per-field layer. Implementing task: `T-SHIP-UI-3` (pending).
