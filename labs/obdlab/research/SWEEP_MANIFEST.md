# OBDLab Research — Sweep & Sort Manifest

**Date:** 2026-06-07
**Step:** Phase 1 of the new-wiki build — *classify + sort only*. No chunking
or extraction performed this session (that is the next step, run one folder at a
time per the agreed workflow).
**Target topics (per request):** fuel trims, ECU diagnosis, O₂ logic — the areas
the old wiki under-covered.

---

## 1. Folder layout created under `research/`

```
research/
  SWEEP_MANIFEST.md            <- this file (the sweep deliverable)
  sources/                     <- raw source docs, sorted by topic (INPUT for chunking)
    fuel-trim/
    o2-logic/
    ecu-diagnosis/
    pids-protocol/
    taxonomy/
    _reference/                <- the OLD wiki baseline (what we are replacing; not chunked)
  proposals/                   <- descriptive proposals: new input fields + open-question solutions
  chunks/                      <- OUTPUT (empty now; populated per-folder in later sessions)
    fuel-trim/ o2-logic/ ecu-diagnosis/ pids-protocol/ taxonomy/
    delta-relations/           <- low-idle vs stress-idle delta data + formulas (see §7)
```

**Sorting criteria (decided this session):** primary axis = **topic** (matches
the three target areas + two support buckets), because the next step processes
one topic folder at a time and chunks will be filed `chunks/<topic>/<concept>`.
Document *type* (source vs proposal vs reference) is the second axis, kept
physically separate so proposals are never mistaken for ground-truth wiki source.

---

## 2. Classification table — `sources/`

Legend — **Type:** GUIDE = already wiki-quality 4D-engine doc · REPORT = long
research report · EXTRACT = PDF→md text extraction · REF = third-party reference.

### `sources/fuel-trim/`

| File | ~words | Type | Viable data for wiki/KG | Cross-topic |
|---|---|---|---|---|
| `master_fuel_trim_guide.md` | 1,540 | GUIDE | **Spine doc.** STFT/LTFT definitions, sign convention table, healthy ranges, idle-vs-cruise, trim-rail/sentinel values, vacuum-leak vs fuel-delivery vs MAF vs EVAP decision tree | o2-logic, taxonomy |
| `Research10.md` | 2,010 | REPORT | STFT/LTFT magnitudes & signs **per fault family** at warm idle (1990–2010); healthy ±5% baseline | taxonomy |
| `Fuel Trim Diagnostics Across Fault Families/` (HTML+169 img) | ~large | REPORT | 8-step diagnostic protocol, PCM compensation logic, sensor metrology, trim behaviour by fault family | taxonomy, o2-logic |
| `Fuel Trim Diagnostics Wiki Preparation/` (HTML+61 img) | ~large | REPORT | Low-idle vs stress-idle **trim delta** logic, closed-loop stoichiometry, OBD PID analysis — closest to "wiki-ready" | pids-protocol |
| `Short Term Long Term Fuel Trim Explained.md` | 8,737 | EXTRACT | Deep STFT/LTFT mechanics, examples; largest single source | — |
| `Ross-Tech_ VAG-COM_ Fuel Trim Info.md` | 2,493 | REF | VAG-specific trim blocks, partial-throttle vs idle cells | — |
| `fuel-trim-analysis.md` | 1,154 | REF | Ross-Tech wiki version — **likely overlaps** Ross-Tech md above | — |
| `Fuel trim can be a valuable diagnostic tool - Eastern Manufacturing.md` | 1,469 | REF | Practitioner framing of trim trends | — |
| `Fuel Trim Diagnostics.txt` | 4,557 | REF | STFT/LTFT interaction, trend plotting methodology | — |
| `fuel-trim.md` | 999 | REF | General fuel-trim primer (was tagged "general-diagnostics") | — |
| `What are fuel trims all about.md` | 169 | REF | Stub (169 words). Probably drop at chunk time | — |

### `sources/o2-logic/`

| File | ~words | Type | Viable data | Cross-topic |
|---|---|---|---|---|
| `master_o2_sensor_guide.md` | 1,812 | GUIDE | **Spine doc.** Narrowband (zirconia) vs wideband (UEGO) physics, voltage/current ranges, switching, upstream vs downstream | fuel-trim, catalyst |
| `master_catalyst_guide.md` | 1,669 | GUIDE | TWC chemistry, light-off, **oxygen storage capacity (OSC)**, OBD catalyst efficiency monitor, failure modes. *NB: catalyst content — candidate to split into its own `catalyst` topic at chunk time* | o2-logic (downstream) |
| `O2logic.md` | 2,025 | REPORT | O₂ sensor **ontology in obdlab KG**: node typing, WIDEBAND_LINEAR vs NARROWBAND_SWITCHING mapping via composition.py, 3 petrol scenarios | ecu-diagnosis, DNALab |
| `O2NBvsWB.md` | 992 | REPORT | Downstream NB vs WB logic, catalyst-monitor signal use | catalyst |
| `O2sensorLogic.md` | 720 | REPORT | **Near-duplicate of `O2NBvsWB.md`** (same opening, shorter). Dedup at chunk time | catalyst |
| `Oxygen Sensor Codes - A Complete Guide ...md` | 1,557 | REF | O₂ DTC catalogue & diagnosis steps | taxonomy |

### `sources/ecu-diagnosis/`

| File | ~words | Type | Viable data | Cross-topic |
|---|---|---|---|---|
| `EcuSignatures.md` | 4,031 | EXTRACT | **Text version** of the ECU-hardware report: internal solid-state failure signatures, forensic OBD-PID + exhaust analysis. Use as the readable spine | pids-protocol |
| `ECU Hardware Fault OBD PID Signatures/` (HTML+200 img) | ~large | REPORT | Same content as above **with figures**; richer but image-heavy | — |
| `ECU Hardware Fault OBD PID Signatures.pdf` | — | REPORT | Source PDF the HTML/md were rendered from | — |

### `sources/pids-protocol/`

| File | ~words | Type | Viable data | Cross-topic |
|---|---|---|---|---|
| `PIDresearch.md` | 5,728 | REPORT | Legacy OBD-II protocol layers, J1962 pinout, PID module testing methodology, Mode/PID reference | all |

### `sources/taxonomy/`

| File | ~words | Type | Viable data | Cross-topic |
|---|---|---|---|---|
| `faultatlas.md` | 711 | REPORT | **8 SAE J2012 / ISO 15031-6 P-code fault families** with subfaults + common DTCs. Backbone for fault-atlas routing | all |
| `faultlist.md` | 386 | REPORT | Same taxonomy as a tree/DTC list (P01xx/P02xx ...). Pairs with faultatlas | all |

### `sources/_reference/` (not chunked)

| File | ~words | Type | Note |
|---|---|---|---|
| `OBDLab_KG_Wiki.md` | 9,254 | REF | **The existing wiki v5.0** — the one being replaced. Kept as baseline/gap reference. Duplicate of `obdlab/wiki/OBDLab_KG_Wiki.md`. Do **not** treat as new source data |

---

## 3. `proposals/` — descriptive proposals (per request, kept separate)

| File | ~words | What it proposes |
|---|---|---|
| `AddObdFields.md` | 2,160 | New input PIDs: Calculated Load (`0x04`) vs Absolute Load (`0x43`) usage, LTFT cell-matrix mapping (RPM × Load), plus the additional live PIDs to add. **Each proposed field needs a named COMLab/fault-atlas consumer before it can ship** (signal/noise rule) |
| `OBD_ImplProp.md` | 5,407 | Module implementation proposal: `config/physical_sensor_bounds.json` ranges, `obd_translation_rules.yaml`, pipeline/checker layout for ECU-hardware-fault detection at low + stress idle |
| `DataFlow.md` | 2,826 | Cross-lab parallel-execution model: typed-JSON boundaries, why labs stay isolated, how COMLab fuses (open-question resolution doc) |
| `wikiResearch.md` | 2,135 | Gap analysis of the OLD wiki: identifies missing math engine (§7–12), VE math, O₂ translation — i.e. *why* the new wiki is needed. Use as the requirements checklist |

---

## 4. Flags for the chunking step (do NOT skip)

1. **Readability gate (CLAUDE.md) before any report becomes chunk input.** The
   three HTML reports + the ECU PDF are Google-Docs/PDF exports — verify formulas
   are present as **text**, not images, before extracting. The `.md` extractions
   (`EcuSignatures.md`, the `master_*` guides, `Research10.md`) are the known-safe
   text spines; prefer them, pull figures from the HTML only where they add data.
   - **RESOLVED 2026-06-07 — "Fuel Trim Diagnostics Wiki Preparation" HTML:** gate
     **FAILED** (formulas + numeric literals were images in the export). Readable
     replacement provided by owner: **`sources/fuel-trim/FuelTrimW.md`** (formulas
     as LaTeX; Gemini share https://gemini.google.com/share/23ff406a7345). Use
     `FuelTrimW.md` as the source of record for this report — **not** the HTML.
   - **STILL OPEN — "Fuel Trim Diagnostics Across Fault Families" HTML (169 imgs):**
     no readable `.md` yet; gate not cleared. Owner to provide `.md` (FT-FU-B).
2. **Dedup pairs:** `O2sensorLogic.md` ⊂ `O2NBvsWB.md`; `fuel-trim-analysis.md`
   vs `Ross-Tech_ VAG-COM_ Fuel Trim Info.md` (both Ross-Tech). Merge, don't
   double-ingest.
3. **`master_catalyst_guide.md`** is catalyst/TWC, currently filed under
   `o2-logic`. Decide at chunk time whether catalyst becomes its own `chunks/catalyst/`.
4. **Signal/noise rule applies at chunk time — but v2 progresses forward.** A
   field/threshold earns a KG node/chunk only with a **named** consumer in COMLab
   analytics or fault-atlas routing. **New for the v2-rework (root `CLAUDE.md` →
   "Progress the app forward"):** that consumer may be one *added in the same
   change*. So **all new faults/fields that improve the engine are marked as
   PROPOSALS, not deferred** — registered in a **separate proposals registry**
   (`comlab/config/proposals/`, never silently in the live KG), with their
   consumer + code path named and a task spec to land them. `consumer: PENDING`
   is reserved for the narrow case where **no consumer can be named at all**. The
   `proposals/` research docs remain candidates, but "not in v1" is **not** a
   reason to defer — default to proposal.
5. **Suggested chunking order** (richest spine first): `fuel-trim` →
   `o2-logic` → `ecu-diagnosis` → `pids-protocol` → `taxonomy` →
   `delta-relations` (last, because its chunks are extracted *across* the
   fuel-trim / ecu / pids feeders — see §7).

---

## 5. Known issue (needs your hand)

An **empty folder shell** `research/Fuel Trim Diagnostics Across Fault Families`
remains at the research root. Its full content (HTML + 169 images) was copied
intact to `sources/fuel-trim/` and the originals deleted, but the now-empty
directory itself is held by a host-level lock and could not be removed from the
sandbox. **Action:** close any app/Explorer window viewing that folder, then
delete the empty folder manually. It contains no files.

---

## 7. Delta-relations topic (added 2026-06-07)

**What it is.** The relationship between PID measurements taken at **low idle
(~700–800 RPM)** and **stress idle (~3500–4500 RPM)** — the *delta* and its
derived ratios/formulas. This is a cross-cutting topic: its data lives inside
several source docs rather than one, so it gets its own **`chunks/delta-relations/`**
home (per request) and is extracted last, after its feeders are chunked.

**Source feeders** (do not move these out of their topic folders — extract delta
excerpts into `chunks/delta-relations/`):

| Feeder | Lives in | Delta content it carries |
|---|---|---|
| `Fuel Trim Diagnostics Wiki Preparation/` → use `FuelTrimW.md` | `sources/fuel-trim/` | Primary feeder — explicit low-idle vs stress-idle trim-delta logic + formulas. **EXTRACTED 2026-06-07** → `chunks/delta-relations/` (6 chunks). |
| `O2logic.md` (added 2026-06-07) | `sources/o2-logic/` | **Delta feeder.** O₂-signal deltas at low (750 RPM) vs stress (2500 RPM): switching-frequency Δf_O2, voltage-bias ΔV_O2, downstream Signal-Transfer-Index ΔTI_cat, + a 6-row cross-ref matrix (O₂ delta × trim × VE). Extract its delta section to `chunks/delta-relations/` when o2-logic is chunked; its ontology/translation content stays in `chunks/o2-logic/`. |
| `EcuSignatures.md` + `ECU Hardware Fault OBD PID Signatures/` | `sources/ecu-diagnosis/` | ECU-fault signatures defined *as deltas* between the two idle states |
| `OBD_ImplProp.md` | `proposals/` | Names the two idle bands and the bounds needed to capture both |
| `AddObdFields.md` | `proposals/` | Load-PID / LTFT-cell behaviour across the RPM span |

> **⚠ Idle-band inconsistency to reconcile before more delta chunks.** "Stress idle"
> is defined differently across sources: `FuelTrimW.md` = **3500–4500 RPM** (used by
> the 6 existing delta chunks); `O2logic.md` = **2500 RPM**; fuel-trim chunk 04 =
> **2500–3000 RPM**. The COMLab delta-script spec (FU-2) must pick one canonical band
> pair (or define per-signal bands) — do not silently mix them when adding O₂ deltas.

**Consumer status (signal/noise).** The named consumer for delta fields is the
**proposed COMLab delta-calculation script** (`AddObdFields.md` / `OBD_ImplProp.md`).
That script does **not exist yet** — so per the signal/noise rule the delta
fields **do not ship** until the script is specced and a live code path reads
them. Treat `chunks/delta-relations/` as a **staging area**: extract and preserve
the data + formulas, but mark every delta field `consumer: PENDING (COMLab delta
script)` until FU-2 below closes.

**Formula handling.** The delta math is extensive and currently embedded in the
HTML report (`Fuel Trim Diagnostics Wiki Preparation`). Before chunking, run the
readability gate (§4.1): formulas must be captured as **text/LaTeX**, not images.
Keep each formula with its variable definitions and the idle-band it applies to.

---

## 8. Unplanned follow-ups (out of this session's scope)

| ID | Task | Why deferred |
|---|---|---|
| FU-1 | **Viability / signal-noise study** of the new input PIDs proposed in `AddObdFields.md` (Calculated vs Absolute Load, extra live PIDs, LTFT cell matrix). Decide per-field whether it earns a place in the workflow — i.e. real diagnostic value > added noise — and name a concrete consumer + code path for each. Fields that fail the test are dropped, not parked. | Separate analysis task; one-task-per-session. Architect deliverable = a task-file spec, not adoption. |
| FU-2 | **Spec the COMLab delta-calculation script** (the proposed consumer for delta-relations). Define inputs (low/stress idle PIDs), the delta formulas, and the fault-atlas/analytics path that reads the result. This is what unblocks `chunks/delta-relations/` fields from `PENDING`. | Depends on FU-1 outcome for which fields are real; implementation is the coder's, spec is the architect's next task. |
| O2-FU-1 | **Write the `WIDEBAND_OFFSET` task spec (placement DECIDED 2026-06-07: two-stage).** Add OBDLab `O2FailureMode.WIDEBAND_OFFSET_CANDIDATE` (emit when sensor=`WIDEBAND_LINEAR` AND persistent `\|normalized_obd_lambda − 1.0\| > 0.05`) in `o2_normalizer.py`; COMLab fusion confirms vs GASLab `λ_chem ≈ 1.0` → new `SENSOR_FAULT` wideband-calibration node in `fault_atlas_router`. Spec must pin threshold + persistence window, the candidate→confirm JSON boundary field, and the fault-atlas node id. Accepted v2 addition — field + consumer ship together. | A v2 improvement, not deferral. Architect writes the task file next session; coder implements + runs gates. From the o2-logic pass. |
| O2-FU-2 | **Fix SWEEP_MANIFEST §11 + any consumer built on it.** `trim_analytics_gate = SUPPRESS_POST_CAT_TRIM` is not a real `TrimAnalyticsGate` value; post-cat suppression is carried by `downstream_trim_role = CATALYST_MONITOR_ONLY`. Declined as redundant (not added). §11 marker already placed; confirm no downstream code/spec references the phantom value. | Doc-truth fix; redundancy, not new value. From the o2-logic pass. |
| O2-FU-3 | **Reconcile the stress-idle RPM band before O₂ deltas enter `chunks/delta-relations/`.** `O2logic.md` uses 2500 RPM; existing delta chunks use 3500–4500 RPM (`FuelTrimW.md`); fuel-trim chunk 04 uses 2500–3000. Pick canonical band(s) (or per-signal bands) in the FU-2 delta-script spec. | Tied to FU-2. Do not mix bands silently. From the o2-logic pass. |
| ECU-FU-1 | **Spec the COMLab/OBDLab ECU-hardware-fault checker** — the named consumer that unblocks `chunks/ecu-diagnosis/` 02–07. Define ≥5 new fault-atlas node ids (capacitor-leak, injector-driver, coil-driver, reference-ground-open, vref-collapse), the discriminator logic drawn from chunk 07's Tables 1–3, and the JSON-boundary inputs it reads. Until it exists and reads them in a live path, all five ECU-mode chunks stay PENDING. Source: `proposals/OBD_ImplProp.md`. | Architect task-file next session; coder implements. From the ecu-diagnosis pass. |
| ECU-FU-2 | **Decide the bank-divergence consumer.** `total_trim_correction_delta_b2` is emitted by OBDLab but read nowhere in COMLab non-test code; the symmetric-vs-asymmetric bank discriminator (the strongest internal-vs-external ECU tell, chunk 07 §2) has no live reader. Specify whether the ECU checker (ECU-FU-1) consumes it or a shared B1/B2-divergence helper is added. **Add the consumer, not a field** (field already exists; emitted-but-unread is an orphan). | Tied to ECU-FU-1. From the ecu-diagnosis pass. |
| ECU-FU-3 | **Input-field gap for Mode 4 (vaporized sensor ground trace).** Signature needs TPS = 100 % and IAT = −40 °C; neither is an `OBDLivePayload` field (only ECT/`coolant_temp_c`), and `calculated_engine_load_pct = 100 %` at idle reads as implausible. Per signal/noise, TPS/IAT earn payload fields **only** if ECU-FU-1 names them as consumers — else dropped, not parked. | Depends on ECU-FU-1. Do not add input PIDs speculatively. From the ecu-diagnosis pass. |
| ECU-FU-4 | **LOAD_PCT WOT-formula evaluator (chunk 01).** The J1979 closed-form (m_actual / m_max_WOT·BARO·√(298/(AAT+273))) has no live evaluator and references `AAT` (no field); the field is ingested as a PID instead. Only needed if a consumer computes load rather than reading the PID. | Low priority — field already ingested directly. From the ecu-diagnosis pass. |

---

## 9. Accounting

28 content documents sorted (24 `.md`/`.txt` + 1 `.pdf` + 3 `.html` reports);
report image sets moved with their reports (~430 images). Nothing deleted except
the duplicate originals of the one copied report. See §5 for the single leftover.

---

## 10. Phase 2 chunking — progress log

| Date | Folder | Result |
|---|---|---|
| 2026-06-07 | `fuel-trim` | **DONE (pass 1: 8 fundamentals chunks).** Spine `master_fuel_trim_guide.md` fully chunked; `Research10.md §1–2` folded. Delta content + HTML reports deferred. Every chunk names an existing consumer; RPM-delta discriminator `PENDING` (FU-2). |
| 2026-06-07 | `fuel-trim` | **DONE (pass 2: expanded 8 → 15 chunks; owner flagged pass-1 coverage insufficient).** Added the missing **diagnostic evidence base**: the previously-deferred "Across Fault Families" report is now readable (`FuelTrimFamilies.md`, gate passed) and `Fuel Trim Diagnostics.txt` is now properly chunked (was only dedup-folded). New chunks 09–15: 20-case fault-family discriminator matrix (idle/2500RPM), P01xx/P02xx + P03xx + P04xx/05xx/06xx case detail, LTFT load-cell matrix, DTC enable-criteria/prerequisite-codes envelope, PCM memory/freeze-frame. 14 of 20 cases map to existing fault nodes (active); **10 forward-progress PROPOSALS** identified and marked (6 new faults: maf_circuit_ground_open_failsafe, thermostat_stuck_open_closedloop_delay, injector_thermal_intermittent, fuel_water_contamination, alternator_ac_ripple_sensor_corruption, egr_insufficient_flow; + 4 concept proposals: misfire_vs_fuelling gate, ltft_cell_vector analyzer, prerequisite_dtc_gate, fuel_delivery_restriction split) — to land via **FT-FU-B**, register in `comlab/config/proposals/`. New follow-ups FT-FU-B, FT-FU-C. See `chunks/fuel-trim/README.md`. |
| 2026-06-07 | `delta-relations` | **STAGED (out of order, owner-directed).** 6 delta chunks + index in `chunks/delta-relations/` from `FuelTrimW.md` (gate-passed): ΔTrim method + 4 profiles (vacuum leak / fuel starvation / MAF under-report / exhaust backpressure) + architecture modifiers (speed-density paradox, turbo boost-leak inversion). **All `consumer: PENDING`** until FU-2 (COMLab delta script). Non-delta unique content in the feeder logged unhomed in `chunks/delta-relations/README.md` (new follow-up DR-FU-1). Normally extracted last per §7; pulled forward because the readable source arrived now. |
| 2026-06-07 | `o2-logic` | **DONE (pure-O₂; catalyst deferred by owner).** 7 concept chunks + index in `chunks/o2-logic/` from 4 pure-O₂ sources (`master_o2_sensor_guide.md` spine fully chunked; `O2logic.md` ontology/translation/suppression folded; `O2NBvsWB.md` downstream loop folded; `Oxygen Sensor Codes` REF dedup-folded). `O2sensorLogic.md` dropped (subset of O2NBvsWB). Every chunk names a live consumer (composition.py / o2_normalizer.py / lab_pipeline_aggregator / fault_atlas_router; O2FailureMode/DownstreamTrimRole/TrimAnalyticsGate enums) — anti-orphan verified. **Source-vocab reconciled to live enums** (LAZY→SLUGGISH, BIASED_*→STUCK_*, NO_ACTIVITY→DEAD, MONITOR_ONLY→CATALYST_MONITOR_ONLY). **Two source fields handled per v2-rework principle (add new value + its consumer; decline only true redundancy):** `BIASED_OFFSET` → **accepted v2 addition**, promoted to a two-stage `WIDEBAND_OFFSET` expression (OBDLab candidate + COMLab confirm → SENSOR_FAULT calib node), spec decided in O2-FU-1. `trim_analytics_gate=SUPPRESS_POST_CAT_TRIM` → **declined as redundant** (capability already exists via `downstream_trim_role`), reconciled in O2-FU-2 + §11 fix. O₂-delta section + catalyst/OSC content deferred (delta-relations / catalyst passes). See `chunks/o2-logic/README.md`. Note: `Research10.md §3–§7` (O₂/VE/λ) still routes here — not yet folded (lives in fuel-trim folder; pull at a later o2 top-up or its own pass). |
| 2026-06-07 | `ecu-diagnosis` | **DONE (5 fault PROPOSALS + 1 active method chunk).** 7 concept chunks + index in `chunks/ecu-diagnosis/` from `EcuSignatures.md` (spine fully chunked; HTML + PDF are duplicate renders — owner-confirmed — not re-ingested). The five internal-ECU-hardware failure modes are **forward-progress proposals** (per §4.4 / root `CLAUDE.md`): they improve the engine and have a **nameable consumer** — the ECU-hardware-fault checker (`proposals/OBD_ImplProp.md`), specced in **ECU-FU-1** — so they ship as `consumer_status: PROPOSAL`, registered in `comlab/config/proposals/`, **not** deferred. They also refine existing `ecu_fault.json` nodes (ERR-EF-006 lean-bias ↔ modes 4/5, ERR-EF-007 rich-bias ↔ mode 2B, ERR-ECU-001 ↔ mode 1) — proposals cross-ref these, not duplicate them. Chunk 01's **method** (truth-vs-perception → `perception_contradiction.detect()`), **idle bands** (`RpmStateBucket`), **LOAD_PCT field** (`calculated_engine_load_pct`) are ACTIVE. New consumers the proposals require (also proposals, not blockers): a B1-vs-B2 divergence reader of `total_trim_correction_delta_b2` (emitted-but-unread today — ECU-FU-2) and TPS/IAT input fields for mode 4 (ECU-FU-3). Follow-ups **ECU-FU-1..4** (§8). See `chunks/ecu-diagnosis/README.md`. |
| — | `pids-protocol` | pending (OBD-I↔OBD-II conversion formula from FuelTrimW.md routes here — DR-FU-1) |
| — | `taxonomy` | pending |

---

## 11. o2-logic prep notes (CONSUMED 2026-06-07 — o2-logic chunked; see §10)

> **RECONCILED 2026-06-07.** The consumer map below names two values that do
> **not** exist in the shipped enums: `MONITOR_ONLY` is actually
> `DownstreamTrimRole.CATALYST_MONITOR_ONLY`, and `trim_analytics_gate =
> SUPPRESS_POST_CAT_TRIM` is **not** a `TrimAnalyticsGate` value at all
> (post-cat suppression is carried by `downstream_trim_role`). Use the live
> enums in `chunks/o2-logic/README.md §reconciliation`, not the draft terms
> below. Follow-ups in §8: O2-FU-1 (`BIASED_OFFSET` → accepted v2 `WIDEBAND_OFFSET`
> addition, placement decided, task spec pending), O2-FU-2 (this fix).


Two sources were **read** but **not chunked** this session (chunks/o2-logic/ is empty
— no partial state). Notes captured so the fresh session can name consumers and dedup
without re-deriving them.

**Sources in `sources/o2-logic/`** (6): `master_o2_sensor_guide.md` (spine — NB/WB
physics, voltage/current, upstream-vs-downstream, bias-vs-real rule §6, DTC families),
`master_catalyst_guide.md` (catalyst/TWC — **see §4.3 split decision**), `O2logic.md`
(KG ontology + translation + **delta content → §7**), `O2NBvsWB.md`, `O2sensorLogic.md`
(**dup ⊂ O2NBvsWB**, §4.2), `Oxygen Sensor Codes ….md` (DTC catalogue).

**Consumer map (signal/noise — name these per chunk).** From `O2logic.md`:
- `composition.py` maps sensor type → `WIDEBAND_LINEAR` or `NARROWBAND_0_TO_1V`,
  driven by **DNALab `ObdLabDnaView`** (sensor topology). Cross-lab input dependency.
- OBDLivePayload emit fields with named downstream readers in **COMLab `fault_atlas_router`**:
  `normalized_obd_lambda`, `o2_failure_mode` (LAZY / BIASED_RICH / BIASED_LEAN /
  BIASED_OFFSET / NO_ACTIVITY), `downstream_trim_role = MONITOR_ONLY`,
  `trim_analytics_gate = SUPPRESS_POST_CAT_TRIM` (suppresses P2096/P2099 post-cat trim).
- Truth-vs-perception consumer: `obd_lambda` vs GASLab `lambda_chem` (bias-vs-real rule,
  spine §6 / §8) — same COMLab fusion that fuel-trim chunk 07 feeds.

**Routing reminders.** `Research10.md §3–§7` (commanded-λ PIDs 0x13/0x1D/0x24-2B/
0x34-3B + mutual exclusivity, VE cross-check, pre-2001 trust, Bosch ME7 downstream
trim, lazy/biased/dead metrics P0131/P0132/P0133/P0134 + cross-counts) routes to
o2-logic — except the **λ-PID availability/encoding** part, which is pids-protocol.
`master_catalyst_guide.md` → resolve §4.3 (own `chunks/catalyst/`?) before chunking.

---

## 12. sources/various/ volume sweep (2026-06-07)

Seven volume docs (`Vol1–4,6–8.md`, no Vol5) swept and chunked. **Readability gate:**
prose/case-tables readable across all; **display equations + inline math symbols were
image-stripped in Vol1/2/3/6 and the two Vol7 display formulas (Brettschneider, vsum)**.
Per the gate, stripped formulas are **flagged as "pending readable export," not
reconstructed**; the formula wiki (`formula-wiki/`) carries the readable formulas and a
pending list. New chunk files written:

| Pack | New chunks | From |
|---|---|---|
| `truth-perception/` (NEW pack) | 01 L1–L5 framing · 02 Δλ vector + L5 scoring · 03 30-case liar library · 04 combustion-integrity/oxygen-usage | Vol1 |
| `pids-protocol/` (was empty) | 01 Mode06/FreezeFrame no-start · 02 MAF/MAP/TPS rationality+P0068 · 03 secondary-ignition waveform · 04 GDI high-pressure fuel | Vol4, Vol2 MD4/5/6 |
| `delta-relations/` | 07 two-speed gas transition matrix (25 GAS-* cases) · 08 vsum sample-validity gate | Vol7 |
| `taxonomy/` (was empty) | 01 Euro emission eras · 02 era/make fault-case priors | Vol6, Vol4, Vol8 |
| `o2-logic/` | 08 wideband pumping-current Ip logic | Vol2 MD2 |
| `ecu-diagnosis/` | 08 T15 startup + 70 % load enrichment gates | Vol2 MD12/13 |
| `fuel-trim/` | 16 three-speed trim test | Vol2 MD3, Vol3 |

Every new chunk names a signal/noise consumer; novel content marked PROPOSAL (consumer
named, not yet wired). Band conflict (Vol7 2500 vs FuelTrimW 3500–4500) reaffirmed for
FU-2/O2-FU-3.

---

## 13. Formula wiki (2026-06-07 — `formula-wiki/`)

Built a formula reference over the **readable** parts of the whole `sources/` tree +
`sources/various/`. **22 formula cards** in 5 domain files + an index + a pending list.
Each card: formula (code/ASCII block) · ASCII plot where it aids intuition · logic ·
connected diagnostic case · owning lab · source.

| File | Domain | Cards |
|---|---|---|
| `01_gas-chemistry-lambda.md` | Brettschneider λ, stoich, vsum validity, chemical efficiency, oxygen-usage | F-GAS-01..05 |
| `02_fuel-trim.md` | total trim, bank divergence, ΔTrim, OBD-I↔II conversion | F-FT-01..04 |
| `03_airflow-ve-load.md` | VE, theoretical airflow, sensor-error Δ, calc/abs load, MAF rules | F-AIR-01..05 |
| `04_o2-lambda-translation.md` | wideband Ip→λ, Δλ vector, catalyst OSC ratio, cat field tests | F-O2-01..04 |
| `05_delta-divergence.md` | δ, cross-delta Δδ, state deltas, two-speed gas deltas | F-DLT-01..04 |
| `PENDING_STRIPPED_FORMULAS.md` | 12 referenced-but-stripped formulas | — |

**No-fabrication rule held.** Where a Vol export stripped a display equation but the same
formula survives readable elsewhere (e.g. full Brettschneider/VE in `wikiResearch.md` /
`OBD_ImplProp.md`), the card carries it and cites that source. Where it survives nowhere
readable (vsum weighting, wideband mA scale, ignition KV/ms, T15/70 % limits, EGR % cells,
later Euro g/km cells, inferred-BARO threshold — 12 items), it is listed PENDING a readable
re-export, **not reconstructed**.

## 14. Proposal extraction from the volume sweep (2026-06-07 — `proposals/extracted/`)

The Vol docs contained many proposals; the new ones (deduped against the 53 already in
`extracted/` from the earlier proposal sweep) were chunked one-per-file and added.
**+17 → 70 total** (`INDEX.md` regenerated; new rows tagged 🆕).

| New proposals | IDs | From |
|---|---|---|
| OBDLab (4) | EP-OBD-18 rationality+inferred-BARO · EP-OBD-19 MAP cranking test · EP-OBD-IN-09 GDI rail-pressure PIDs · EP-OBD-IN-10 secondary-ignition features | Vol2 MD4/9/5/6, Vol4 |
| COMLab (6) | EP-COM-10 L5 prognostic scoring · 11 TCG root-source · 12 load-correction delta · 13 startup/70%-load gates · 14 no-DTC PID profiling · 15 30-case test corpus | Vol1, Vol2 MD12/13, Vol3 |
| GASLab (3) | EP-GAS-03 combustion-integrity metrics · 04 two-speed gas matrix capability · 05 5-gas sample-validity gate | Vol1, Vol7 |
| Cat/DTC/DNA/EVAP (4) | EP-CAT-05 pre-cat inference engine · EP-DTC-04 Mode06/FF no-start+immobilizer · EP-DNA-03 Euro-era tier gate+priors · EP-FA-08 EVAP purge-flow/leak-detect | Vol1, Vol4, Vol6/8, Vol2 MD8 |

Each names a consumer + code path and cross-links to its chunk (§12). Two
(EP-COM-13, EP-GAS-05) depend on stripped thresholds — each says so in-file and points to
`formula-wiki/PENDING_STRIPPED_FORMULAS.md` rather than guessing a bound.

### md-prep assessment (why stripped formulas were NOT auto-recovered)

The owner offered `_skills/doc/md-prep` to fix unreadable docs. Ran its detector
(`diagnose_wall.py`) on all 7 Vols → **exit 0 (clean) for every file**: they are **not**
the wall-of-text / box-drawing archetype md-prep's reconstruction scripts repair. Their
unreadability is **content dropped to blank in the original Google-Docs export**, and
md-prep by design does not change technical content or invent missing data — it restructures
what is present. So it cannot resurrect the stripped equations. **Correct fix = a readable
re-export** (plain-text/LaTeX math, as was done for `FuelTrimW.md`); the 12 affected
formulas remain in the §13 pending list until then.

---

## 15. Session summary (2026-06-07)

| Deliverable | Location | Count |
|---|---|---|
| New chunk files (6 packs, 2 new) | `chunks/{truth-perception,pids-protocol,delta-relations,taxonomy,o2-logic,ecu-diagnosis,fuel-trim}/` | 16 + 3 READMEs |
| Formula wiki | `formula-wiki/` | 22 cards + 12 pending |
| New proposals | `proposals/extracted/` | +17 → 70 total |

**Verification:** every chunk/proposal names a signal/noise consumer; all wiki-links
resolve; no ARCHIVE/v2/v6 sourcing; no fabricated formula or threshold. **Open carry-forward:**
(a) stress-idle band conflict 2500 vs 3500–4500 RPM (FU-2/O2-FU-3); (b) 12 stripped formulas
+ 2 proposal thresholds pending a readable Vol2/Vol7 re-export.
