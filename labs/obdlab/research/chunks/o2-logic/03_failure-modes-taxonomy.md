---
chunk: o2-logic/03_failure-modes-taxonomy
topic: o2-logic
sources:
  - master_o2_sensor_guide.md §2 (narrowband failure patterns)
  - master_o2_sensor_guide.md §3 (wideband failure modes)
  - master_o2_sensor_guide.md §5 (heater)
  - O2logic.md §Scenario-1 (bias/lazy threshold checks)
consumer: O2FailureMode {NO_FAULT, STUCK_LEAN, STUCK_RICH, SLUGGISH, DEAD, WRONG_CENTERLINE, HEATER_FAULT} — OBDLab o2_normalizer.py emits o2_failure_mode; COMLab vocabulary.py mirror is read by the perception-contradiction detector and fault_atlas_router
consumer_status: active
reconciliation: source-doc terms (LAZY / BIASED_RICH / BIASED_LEAN / NO_ACTIVITY) map to the shipped narrowband enum — see mapping below and README §reconciliation. BIASED_OFFSET is a v2 addition (new two-stage WIDEBAND_OFFSET expression + consumer), specced in O2-FU-1.
---

# O₂ sensor failure-mode taxonomy

The shipped failure-mode enum is **narrowband** (`O2FailureMode`, OBDLab_KG_Wiki
§6.7, mirrored in COMLab `vocabulary.py`). OBDLab's `o2_normalizer.py` classifies
the upstream signal into exactly one of these and emits it as `o2_failure_mode`:

| Enum value | Trigger (upstream NB) | Cause | Resulting fuel trim |
|---|---|---|---|
| `NO_FAULT` | Healthy switching, cross-counts ≥ 8 / 10 s @ 2500 RPM | — | normal |
| `STUCK_LEAN` | Voltage pinned **< 0.20 V** | Exhaust leak pre-sensor, poisoning, signal short-to-ground | Positive (ECU adds fuel chasing false-lean) |
| `STUCK_RICH` | Voltage pinned **> 0.85 V** | Silicone contamination, short-to-voltage, end-of-life | Negative (ECU subtracts fuel) |
| `SLUGGISH` | Cross-counts < 8 / 10 s @ 2500 RPM; freq < 0.5 Hz; rise/fall **> 100 ms**; propane-response delay > 100 ms | Age, contamination, carbon, weak heater | Trims trail; may pass a static voltage check yet still be slow |
| `DEAD` | No switching activity; flat-lined at ~0.45 V bias only | Open heater circuit, broken signal wire, cracked sensor | None (ECU drops to open loop, sets P0134-family) |
| `WRONG_CENTERLINE` | Switches off-centre (e.g. 0.3–0.6 V instead of 0.1–0.9 V) | End-of-life, partial poisoning — stoich centre drifted from ~0.45 V | Trims slightly off-centre; cross-counts may still pass |
| `HEATER_FAULT` | Heater resistance outside **4–14 Ω** (open or shorted) | Heater fuse/open/short | Delays/blocks closed-loop entry |

## Source-vocabulary reconciliation (do not ship the source terms)

`O2logic.md` and SWEEP_MANIFEST §11 use a different vocabulary. The shipped
mapping is:

- `LAZY_SWITCHING` → **`SLUGGISH`**
- `BIASED_RICH` → **`STUCK_RICH`** (source threshold V_min > 0.55 V; shipped pin > 0.85 V)
- `BIASED_LEAN` → **`STUCK_LEAN`** (source threshold V_max < 0.35 V; shipped pin < 0.20 V)
- `NO_ACTIVITY` → **`DEAD`**
- `BIASED_OFFSET` → **accepted v2 addition (two-stage) — spec in O2-FU-1.**
  A wideband sensor reading a *constant* λ offset while the engine is
  physically stoichiometric is a distinct, routable fault that v1's
  narrowband-only taxonomy cannot express. v2 adds it as a two-stage
  expression so each lab only asserts what it can see:
  - OBDLab emits `o2_failure_mode = WIDEBAND_OFFSET_CANDIDATE` — all it can
    assert from its own signal: persistent `|normalized_obd_lambda − 1.0| > 0.05`
    on a `WIDEBAND_LINEAR` sensor.
  - COMLab's fusion confirms against GASLab `λ_chem ≈ 1.0` and routes to a
    `SENSOR_FAULT` wideband-calibration node (more specific than a generic
    `perception_contradiction`).
  Both halves — new field **and** its named consumer/code path — ship
  together, satisfying the signal/noise rule. Until O2-FU-1's task file lands
  and the coder implements it, chunk 05 documents the interim λ-delta path.

> Threshold note: the shipped pins (`< 0.20 V` / `> 0.85 V`) are wider than the
> source-doc draft pins (`< 0.35 V` / `> 0.55 V`). The shipped values in
> COMLab `vocabulary.py` are canonical; the wiki chunk follows the code, not the
> draft. Source thresholds preserved above only as provenance.

## Wideband-specific failure modes (no narrowband-enum equivalent)

`master_o2_sensor_guide.md §3` lists heater-out-of-spec (→ `HEATER_FAULT`),
calibration-resistor failure, and reference-voltage drift. The latter two
produce a *constant-offset* λ error and are detected by the λ-delta path
(`05`), not by a distinct `O2FailureMode` value. Heater faults set the
P0030/P0036/P0050/P0056 family (see `07_o2-dtc-families`).

Citation: thresholds per OBDLab_KG_Wiki.md §6.7 (`O2FailureMode` docstrings,
labs/obdlab/obdlab/schemas/vocabulary.py); narrowband patterns
master_o2_sensor_guide.md §2; cross-count ≥ 8 / 10 s @ 2500 RPM and
rise/fall > 100 ms per §2.


## Core Entities

- O2FailureMode.NO_FAULT, O2FailureMode.STUCK_LEAN, O2FailureMode.STUCK_RICH, O2FailureMode.SLUGGISH, O2FailureMode.DEAD, O2FailureMode.WRONG_CENTERLINE, O2FailureMode.HEATER_FAULT
- WIDEBAND_OFFSET_CANDIDATE, o2_failure_mode
- o2_normalizer.py (producer) -> COMLab detector + fault_atlas_router (consumer, active)

## Graph relations (explicit)

**o2_normalizer.py** EMITS **o2_failure_mode**
upstream voltage below 0.20V CLASSIFIES **STUCK_LEAN**
upstream voltage above 0.85V CLASSIFIES **STUCK_RICH**
cross-counts below 8 per 10s CLASSIFIES **SLUGGISH**
no switching CLASSIFIES **DEAD**
heater resistance outside 4-14ohm CLASSIFIES **HEATER_FAULT**
**LAZY_SWITCHING** MAPS_TO **SLUGGISH**
**BIASED_RICH** MAPS_TO **STUCK_RICH**
**BIASED_LEAN** MAPS_TO **STUCK_LEAN**
**NO_ACTIVITY** MAPS_TO **DEAD**
**BIASED_OFFSET** PROMOTED_TO **WIDEBAND_OFFSET_CANDIDATE** (O2-FU-1)

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
