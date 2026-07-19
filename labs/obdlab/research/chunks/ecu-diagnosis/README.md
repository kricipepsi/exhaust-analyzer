---
node_type: "wiki"
lab: "obdlab"
module: "obd_live_lab"
subsystem: "ecu-hardware"
implements:
  - "labs/obdlab/obdlab/core/semantic_consistency_checker.py"
consumers:
  - "comlab: labs/comlab/comlab/core/ecu_hardware_checker.py — ECU driver/rail fault checks"
drift_guards:
  - "labs/obdlab/tests/unit/test_semantic_consistency_checker.py"
tags: [obdlab, finished, wiki]
source: "labs/obdlab/research/chunks/ecu-diagnosis/README.md"
---
# chunks/ecu-diagnosis/ — index & disposition ledger


**Date:** 2026-06-07 · **Step:** Phase 2 (chunking), folder 3 of 6 per
SWEEP_MANIFEST §4.5 order (`fuel-trim` ✅ → `o2-logic` ✅ → **`ecu-diagnosis`** →
`pids-protocol` → `taxonomy` → `delta-relations` staged). **Mode:** classify into
concept chunks; each chunk carries a named signal/noise consumer.

## Headline (read before using these chunks)

This folder delivers **five forward-progress fault PROPOSALS + one active method
chunk** — per the v2-rework rule (root `CLAUDE.md` → "Progress the app forward";
SWEEP_MANIFEST §4.4). The document describes a fault class v1 **cannot detect**:
internal ECU hardware failures. That is precisely what v2 exists to fix, so these
ship as **proposals**, not deferrals: each has a **nameable consumer** — the
COMLab/OBDLab ECU-hardware-fault checker (`proposals/OBD_ImplProp.md`, specced in
**ECU-FU-1**) — and is registered in `comlab/config/proposals/` with its consumer
+ code path named. "Not in v1" is not a reason to defer.

These are not greenfield: they **refine existing `ecu_fault.json` nodes** —
ERR-EF-006 (5V-ref/ground → lean bias) ↔ modes 4 & 5, ERR-EF-007 (injector-driver
/MAP → rich bias) ↔ mode 2B, ERR-ECU-001 (processor/5V-ref) ↔ mode 1. The
proposals cross-ref and sharpen these, they do not duplicate them.

The **ACTIVE** hook is chunk 01's *method* — truth-vs-perception
(`perception_contradiction.detect()`, λ_obd vs λ_chem). Note its Lambda Truth
guard (`lambda_chem < 0.90 or > 1.10`) deliberately *suppresses* on these modes
(λ 0.72–1.55), which is why a dedicated checker — not a tweak to the bias
detector — is the right consumer to propose.

Two consumers the proposals require are themselves **companion proposals** (not
blockers, per the v2 rule — field + consumer ship together): a B1-vs-B2 divergence
reader of `total_trim_correction_delta_b2` (emitted-but-unread today — ECU-FU-2),
and new TPS/IAT input fields for mode 4 (ECU-FU-3).

## Chunk set

| Chunk | Concept | Consumer | Status |
|---|---|---|---|
| `01_method-load-pct-and-idle-bands` | OBD-vs-5gas method, J1979 LOAD_PCT formula, 700–800/3500–4500 bands | perception_contradiction.py (method) + RpmStateBucket + calculated_engine_load_pct field | **MIXED** (method/bands/field active; WOT formula pending) |
| `02_capacitor-leakage-trace-corrosion` | Mode 1 — AC ripple, ±15 % symmetric STFT, OL_FAULT freeze | proposed ECU checker | PROPOSAL |
| `03_injector-driver-open-and-short` | Mode 2 — single-bank ±25 % railed trim (open +25 / short −25) | proposed ECU checker (Mode B overlaps `detect_compensated_rich`, ≠ consumer) | PROPOSAL |
| `04_coil-driver-transistor-failure` | Mode 3 — deceptive λ≈1.01 + HC 2200, single-cyl misfire | proposed ECU checker (symptom→`IGNITION_MISFIRE`/`CATALYST_OVERWHELMED`) | PROPOSAL |
| `05_sensor-ground-trace-open` | Mode 4 — −40 °C ECT + 100 % TPS + 100 % LOAD, all-bank | proposed ECU checker **+ TPS/IAT field gap** | PROPOSAL |
| `06_5v-regulator-rail-collapse` | Mode 5 — global lean, +25 % both banks, NOx spike | proposed ECU checker (symptom→`LEAN_MIXTURE`/`HIGH_COMBUSTION_TEMP`) | PROPOSAL |
| `07_comparative-signature-tables` | Tables 1–3 + analytical conclusions (symmetry, deceptive λ) | proposed ECU checker discriminator matrix | PROPOSAL |
| `09_control-module-voltage` | VPWR (PID 0x42) rail health; <12.0/>15.0 V + ΔVPWR signatures | COMLab perception_contradiction electrical pre-check (T-COMV2-VPWR-GATE-1) + EP-FA-05 | PROPOSAL |

## Source disposition (3 sources — all one document)

| Source | Disposition | Where |
|---|---|---|
| `EcuSignatures.md` | **Spine — fully chunked** | intro→01, mode 1→02, mode 2→03, mode 3→04, mode 4→05, mode 5→06, Tables 1–3 + Conclusions→07 |
| `ECU Hardware Fault OBD PID Signatures/` (HTML+imgs) | **Not chunked — duplicate render** of EcuSignatures.md (owner-confirmed same content, different format) | — |
| `ECU Hardware Fault OBD PID Signatures.pdf` | **Not chunked — duplicate render** (source PDF the HTML/md came from) | — |

## Anti-orphan verification (2026-06-07)

Live (non-test) paths confirmed present, and what each can/can't consume:

- `comlab/core/perception_contradiction.py` — `detect()` (λ_obd vs λ_chem,
  Lambda Truth guard 0.90/1.10) and `detect_compensated_rich()` (trim<−15 % +
  rich DTC). **Active for the method; suppresses on abnormal-chemistry ECU modes.**
- `obdlab/schemas/payload.py::OBDLivePayload` — fields **present**:
  `calculated_engine_load_pct`, `shrtft1/longft1`, `shrtft2/longft2` (nullable),
  `total_trim_correction_delta` + `_b2`, `manifold_vacuum_kpa`,
  `mass_airflow_gps`, `coolant_temp_c`, `normalized_obd_lambda`, `o2_failure_mode`,
  `trim_analytics_gate`. Fields **absent**: **TPS, IAT, AAT**.
- `obdlab/schemas/vocabulary.py::RpmStateBucket` — `STABILIZED_IDLE` (650–900),
  `STRESS_IDLE` (3000–4500) cover both doc bands.
- `comlab/core/fault_atlas_router.py` — discriminator table reads
  `calc_load_pct`, `shrtft1/longft1/shrtft2/longft2`, `map_kpa`, `coolant_temp_c`,
  `mass_airflow_gps` to route **between existing fault families**. **No
  ECU-hardware node**; no read of B1-vs-B2 divergence.
- `total_trim_correction_delta_b2` — emitted by OBDLab but **read nowhere in
  comlab non-test code** → the symmetric/asymmetric discriminator (chunk 07 §2)
  has no consumer.

Result: chunk 01's method/bands/field are non-orphan and ACTIVE; chunks 02–07 are
**PROPOSALS** — each names the same proposed consumer (ECU-FU-1 checker) and is to
be registered in `comlab/config/proposals/`. They are not orphans (consumer is
named) and not deferrals (consumer is specced, not absent). No chunk is mislabelled
active.

## Unplanned follow-ups (from this pass)

| ID | Item | Why deferred |
|---|---|---|
| ECU-FU-1 | **Spec the COMLab/OBDLab ECU-hardware-fault checker** (the named consumer for 02–07). Define: the new fault-atlas node ids (≥5: capacitor-leak, injector-driver, coil-driver, reference-ground-open, vref-collapse), the discriminator logic from Table 1/2/3, and the JSON-boundary inputs it reads. This is what unblocks every PENDING chunk here. | One-task-per-session; architect writes the task file, coder implements. Source = `proposals/OBD_ImplProp.md`. |
| ECU-FU-2 | **Decide the bank-divergence consumer.** `total_trim_correction_delta_b2` is emitted but unread; the symmetric-vs-asymmetric discriminator (the strongest internal-vs-external tell) needs a live reader. Specify whether the ECU checker (ECU-FU-1) consumes it or a small shared B1/B2-divergence helper is added. Field already exists — add the consumer, do not add a field. | Tied to ECU-FU-1. Signal/noise: a field emitted but unread is an orphan; this closes it. |
| ECU-FU-3 | **Input-field gap for Mode 4 (ground trace).** The signature needs TPS = 100 % and IAT = −40 °C; neither is an OBDLivePayload field (only ECT/`coolant_temp_c` exists), and `calculated_engine_load_pct = 100 %` at idle would be treated as implausible. Decide per signal/noise whether TPS/IAT earn payload fields — each only if ECU-FU-1 names it as a consumer. Fields that don't earn a consumer are dropped, not parked. | Depends on ECU-FU-1. Do not add input PIDs speculatively. |
| ECU-FU-4 | **LOAD_PCT WOT-formula evaluator (chunk 01).** The J1979 closed-form (m_actual / m_max_WOT·BARO·√…) has no live evaluator and references `AAT` (no field). Only needed if a consumer computes load rather than ingesting the PID. | Low priority; the field is already ingested directly. |

## Notes

- Numeric literals here are research data quoted from the source, not code — the
  gaslab/obdlab numeric-citation rule applies to `.py`, not to these `.md` chunks;
  each chunk cites its source section instead.
- `master_catalyst_guide.md` split (SWEEP_MANIFEST §4.3) and `Research10.md §3–§7`
  top-up (o2-logic) remain open from prior passes — untouched here.

---

## Volume-sweep addition (2026-06-07 — sources/various/Vol2.md)

| Chunk | Concept | Consumer | Status |
|---|---|---|---|
| `08_t15-startup-lambda-logic` | T15 key-on window + 70 % high-load enrichment gates | analytics_preconditions (TrimAnalyticsGate: STARTUP_T15_ACTIVE / HIGH_LOAD_ENRICH_ACTIVE) | PROPOSAL |

Source: Vol2 Master Documents 12 (T15/λ) + 13 (70 % load). Logic readable; numeric
rich/lean fault-limit + load cells image-stripped → formula-wiki pending list.


## Core Entities

- ecu-diagnosis (5 proposed fault nodes + 1 active method)
- ECU_CAPACITOR_LEAK, INJECTOR_DRIVER_OPEN, INJECTOR_DRIVER_SHORT, COIL_DRIVER_SHORT, SENSOR_GROUND_TRACE_OPEN, VREF_RAIL_COLLAPSE
- ECU_HARDWARE_CHECKER (proposed consumer, ECU-FU-1)

## Graph relations (explicit)

**ecu-diagnosis** PROPOSES **ECU_HARDWARE_CHECKER**
**ECU_HARDWARE_CHECKER** REFINES **ecu_fault.json** nodes ERR-ECU-001, ERR-EF-006, ERR-EF-007
**perception_contradiction.detect** IS_ACTIVE_METHOD for chunk 01

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
