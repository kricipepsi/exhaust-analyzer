---
node_type: "wiki"
lab: "obdlab"
module: "obd_live_lab"
subsystem: "o2-lambda-perception"
implements:
  - "labs/obdlab/code/core/o2_normalizer.py"
consumers:
  - "comlab: labs/comlab/comlab/core/perception_contradiction.py — O2/lambda bias-vs-truth comparison"
  - "comlab: labs/comlab/comlab/analytics/power_loss_analytics.py — mixture scoring"
drift_guards:
  - "labs/obdlab/tests/unit/test_o2_normalizer.py"
tags: [obdlab, finished, wiki]
source: "labs/obdlab/research/chunks/o2-logic/README.md"
---
# chunks/o2-logic/ — index & dedup ledger


**Date:** 2026-06-07 · **Step:** Phase 2 (chunking), folder 2 of 6 per
SWEEP_MANIFEST §4.5 order. **Mode:** classify+dedup into concept chunks; each
chunk carries a named signal/noise consumer in its frontmatter. **Catalyst
deferred this session by owner** (see §deferred); the O₂-delta section of
`O2logic.md` deferred to the delta-relations pass (SWEEP_MANIFEST §7).

## Chunk set

| Chunk | Concept | Primary consumer | Status |
|---|---|---|---|
| `01_sensor-types-and-physics` | NB zirconia vs WB UEGO physics, ranges, switching, heater | composition.py sensor-type map → o2_normalizer | active |
| `02_upstream-vs-downstream-roles` | pre-cat fuel-control vs post-cat monitor; `DownstreamTrimRole` | composition.py / COMLab perception-contradiction detector | active |
| `03_failure-modes-taxonomy` | `O2FailureMode` enum + source-vocab reconciliation | OBDLab o2_normalizer → COMLab detector + fault_atlas_router | active |
| `04_normalized-lambda-translation` | NB step-wise λ, WB Φ→λ / K_scale → `normalized_obd_lambda` | o2_normalizer.py (producer) → COMLab lab_pipeline_aggregator + family_map | active |
| `05_bias-vs-real-truth-perception` | λ_obd vs λ_chem decision table; `perception_contradiction` | COMLab perception-contradiction detector / truth-vs-perception override (PRD §5) | active |
| `06_downstream-trim-suppression` | `CATALYST_MONITOR_ONLY` → suppress P2096/P2099 | composition.py downstream_trim_role → COMLab fault_atlas_router | active |
| `07_o2-dtc-families` | P013x/P015x/heater/P2A0x catalogue; misfire-lean caveat | `TrimAnalyticsGate.O2_FAULT_ACTIVE` gate + fault_atlas_router routing | active |

No chunk is an orphan: every consumer named above is a live code path
(verified — see §anti-orphan). Two source-doc fields are handled differently,
and the difference is deliberate (this is a v2 rework, so a new expression that
improves diagnosis is *added with its consumer*, not deferred for being absent
from v1):

- `BIASED_OFFSET` — **accepted v2 addition.** Promoted to a new two-stage
  expression (`WIDEBAND_OFFSET`) with a named consumer; spec is O2-FU-1. Not
  withheld.
- `SUPPRESS_POST_CAT_TRIM` — **declined, but for redundancy, not for being
  new.** The capability already has a working path via `downstream_trim_role`;
  a second gate value would be duplicate signal. Reconciled (O2-FU-2), not added.

## Source disposition (all 6 o2-logic sources)

| Source | Disposition | Where |
|---|---|---|
| `master_o2_sensor_guide.md` | **Spine — fully chunked** | §1→01, §2→01/03, §3→01/03/04, §4→02/06, §5→01/03/07, §6→05, §7→07, §8→05 |
| `O2logic.md` | **Partially chunked** — ontology/translation/suppression folded; delta section deferred | Scenario-1→03/04, Scenario-2→04/05, Scenario-3 step3→06. §"O₂ deltas in COMLab" + 6-row matrix → **delta-relations pass** (§7, PENDING/FU-2) |
| `O2NBvsWB.md` | **Partially folded** — downstream secondary-loop + sensor configs | →02, →06. WB+WB OSC/mass-balance model → **catalyst** (deferred) |
| `O2sensorLogic.md` | **Dropped (dup)** — confirmed strict subset of O2NBvsWB.md (same opening, shorter, ends at WB+NB section) | — |
| `Oxygen Sensor Codes - A Complete Guide ...md` | **Folded by dedup (REF)** — lean/rich causes overlap spine §6/§7 | superseded by 05, 07; unique misfire→false-lean caveat preserved in 07 |
| `master_catalyst_guide.md` | **Deferred (owner call)** — catalyst/TWC, not pure O₂ | not chunked this session — see §deferred |

## Vocabulary reconciliation (source-doc term → shipped enum)

The source docs (`O2logic.md`, repeated in SWEEP_MANIFEST §11) use a vocabulary
that does **not** match the live enums. Chunks ship the live enum; source terms
are recorded only as provenance.

| Source-doc term | Shipped value | Notes |
|---|---|---|
| `LAZY_SWITCHING` | `O2FailureMode.SLUGGISH` | rise/fall > 100 ms |
| `BIASED_RICH` | `O2FailureMode.STUCK_RICH` | shipped pin > 0.85 V (source draft > 0.55 V) |
| `BIASED_LEAN` | `O2FailureMode.STUCK_LEAN` | shipped pin < 0.20 V (source draft < 0.35 V) |
| `NO_ACTIVITY` | `O2FailureMode.DEAD` | — |
| `MONITOR_ONLY` | `DownstreamTrimRole.CATALYST_MONITOR_ONLY` | — |
| `ACTIVE_REAR_TRIM` | `DownstreamTrimRole.SECONDARY_FUEL_TRIM` | — |
| `BIASED_OFFSET` | **`WIDEBAND_OFFSET` (new v2, two-stage)** | OBDLab `WIDEBAND_OFFSET_CANDIDATE` + COMLab confirm vs λ_chem → `SENSOR_FAULT` calib node. Added with consumer, not deferred. Spec: O2-FU-1 |
| `trim_analytics_gate = SUPPRESS_POST_CAT_TRIM` | **— (no enum member)** | suppression carried by `downstream_trim_role`, not the gate. O2-FU-2 |

Shipped enums (canonical, labs/obdlab/obdlab/schemas/vocabulary.py, mirrored in
COMLab vocabulary.py):

- `O2FailureMode` = {NO_FAULT, STUCK_LEAN, STUCK_RICH, SLUGGISH, DEAD, WRONG_CENTERLINE, HEATER_FAULT}
- `DownstreamTrimRole` = {NONE, CATALYST_MONITOR_ONLY, SECONDARY_FUEL_TRIM}
- `TrimAnalyticsGate` = {VALID, ENGINE_COLD, OPEN_LOOP, O2_FAULT_ACTIVE, CKP_CMP_FAULT_ACTIVE, CODES_RECENTLY_CLEARED, WOT_ACTIVE, DFCO_ACTIVE, SEMANTIC_ERROR}

## Anti-orphan verification (2026-06-07)

Each named consumer confirmed present in a live (non-test) code path:

- `composition.py` — `apps/wired/wired/composition.py` constructs
  `DownstreamTrimRole`, `O2FailureMode`, `TrimAnalyticsGate`, and forwards
  `normalized_obd_lambda`.
- `o2_normalizer.py` — `labs/obdlab/obdlab/core/o2_normalizer.py` produces
  `normalized_obd_lambda` (0.7–1.3), `o2_failure_mode`.
- `lab_pipeline_aggregator.py` — `labs/comlab/comlab/core/` reads
  `request.obd_live_data.normalized_obd_lambda`.
- `fault_atlas_router.py` — `labs/comlab/comlab/core/fault_atlas_router.py`.
- Enums — `labs/obdlab/obdlab/schemas/vocabulary.py` and
  `labs/comlab/comlab/schemas/vocabulary.py` (mirror, JSON-only boundary).

## Deferred (not this folder)

- **Catalyst** — `master_catalyst_guide.md`, the OSC / TI_cat efficiency model
  (`O2logic.md` Scenario-3 step 2: `TI_cat = σ(V_down)/σ(V_up)`, DEGRADED_P0420
  assertion), and the WB+WB mass-balance OSC model (`O2NBvsWB.md §3). Owner
  deferred a `chunks/catalyst/` split this session; not chunked. SWEEP_MANIFEST
  §4.3 split decision remains open.
- **Delta-relations** — `O2logic.md` low-idle (750 RPM) vs stress-idle (2500
  RPM) O₂ deltas Δf_O2, ΔV_O2, ΔTI_cat + the 6-row O₂×trim×VE matrix. These are
  **accepted v2 additions**; their consumer is the COMLab delta-calculation
  script being specced in **FU-2** (consumer-spec-in-flight, not parked).
  Extract to `chunks/delta-relations/` once FU-2's task file pins the formulas
  and the fault-atlas/analytics path that reads them. ⚠ idle-band inconsistency
  (O2-FU-3): this source uses 2500 RPM for stress idle; existing delta chunks
  use 3500–4500 RPM (FuelTrimW.md). Reconcile bands before adding O₂ deltas —
  do not silently mix them.

## Unplanned follow-ups (from this pass)

| ID | Item | Why deferred |
|---|---|---|
| O2-FU-1 | **Decided 2026-06-07 (two-stage) — write the task spec.** Add a v2 wideband-offset expression: OBDLab `O2FailureMode.WIDEBAND_OFFSET_CANDIDATE` (emit when sensor=`WIDEBAND_LINEAR` AND persistent `\|normalized_obd_lambda − 1.0\| > 0.05`), produced in `o2_normalizer.py`; COMLab fusion confirms against GASLab `λ_chem ≈ 1.0` and routes to a new `SENSOR_FAULT` wideband-calibration node in `fault_atlas_router`. Task spec must pin: threshold + persistence window, the candidate→confirm JSON field on the OBDLab boundary, and the fault-atlas node id. Field + consumer ship together. | Next session's one-task; architect writes the task file, coder implements + runs gates. Decision (placement) already made — no longer open. |
| O2-FU-2 | `O2logic.md` / SWEEP_MANIFEST §11 assert `trim_analytics_gate = SUPPRESS_POST_CAT_TRIM`, which is not a `TrimAnalyticsGate` value. Post-cat suppression is carried by `downstream_trim_role = CATALYST_MONITOR_ONLY`. Correct §11 of the manifest so the next consumer isn't built against a non-existent gate value. | Doc-truth fix to the manifest; out of chunk scope. |
| O2-FU-3 | Stress-idle band inconsistency for O₂ deltas (2500 RPM here vs 3500–4500 RPM in FuelTrimW.md delta chunks). Pick canonical band(s) before O₂ deltas enter `chunks/delta-relations/`. | Tied to FU-2 (COMLab delta script) per SWEEP_MANIFEST §7. |

---

## Volume-sweep addition (2026-06-07 — sources/various/Vol2.md)

| Chunk | Concept | Consumer | Status |
|---|---|---|---|
| `08_wideband-pumping-current-logic` | UEGO dual-cell pumping-current Ip sign → λ; drift = WIDEBAND_OFFSET | o2_normalizer wideband path → COMLab | active + PROPOSAL (Ip-drift flag, O2-FU-1) |

Source: Vol2 Master Document 2. Concept readable; some mA/voltage spec cells stripped.


## Core Entities

- o2-logic (7 active chunks + 1 volume-sweep)
- O2FailureMode, DownstreamTrimRole, TrimAnalyticsGate, normalized_obd_lambda, perception_contradiction
- o2_normalizer.py + COMLab perception-contradiction detector + fault_atlas_router

## Graph relations (explicit)

**o2-logic** PRODUCES **normalized_obd_lambda** and **o2_failure_mode**
**o2-logic** FEEDS **COMLab perception-contradiction detector**
**BIASED_OFFSET** PROMOTED_TO **WIDEBAND_OFFSET_CANDIDATE** (O2-FU-1)
**SUPPRESS_POST_CAT_TRIM** DECLINED (redundant with DownstreamTrimRole, O2-FU-2)

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
