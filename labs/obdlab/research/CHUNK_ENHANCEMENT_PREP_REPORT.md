# OBDLab wiki — graphify pre-ingestion enhancement pass

**Date:** 2026-06-08 · **Author:** architect · **Scope:** `research/chunks/` (63 `.md`, 8 topic dirs)
**Driver:** `research/IngestGraph.md` — the three low-risk recommendations from the prior session's
graphify-readiness review. **Downstream task:** `tasks/T-KG-OBD-1_graphify_ingest_enhanced_wiki.md`.

## What was applied (all 63 chunks)

Per `IngestGraph.md`, graphify pass-3 tags an edge **EXTRACTED** (confidence 1.0) only when the
relation is stated **directly in text**; otherwise it is **INFERRED** (0.55–0.95) or **AMBIGUOUS**.
The goal was therefore to make implied links explicit, not to restructure content. Three enhancements,
appended as two clearly-marked trailer sections at the **end** of every chunk — **no sourced prose,
numeric literal, table, citation, or frontmatter was altered** (the trailers are pure appends):

1. **Explicit relations (#1, highest leverage).** A `## Graph relations (explicit)` block of
   `**SUBJECT** PREDICATE **OBJECT**` lines for relations that previously lived only in
   table-adjacency or prose — e.g. `**P0131** INDICATES **STUCK_LEAN**`,
   `**VACUUM_LEAK** PRODUCES_NEGATIVE **DELTA_TRIM**`,
   `**control_module_voltage_v** CONSUMED_BY **COMLab electrical-health pre-check**`.
   **314 relation lines** total across the corpus.
2. **Byte-identical entity labels (#2).** Canonical forms applied consistently in every trailer:
   DTC codes as-is (`P0171`…); failure modes `ALLCAPS_UNDERSCORE`
   (`STUCK_LEAN`, `STUCK_RICH`, `BIASED_OFFSET`, `WIDEBAND_OFFSET_CANDIDATE`, `HEATER_FAULT`,
   `SENSOR_FAULT`, `SLUGGISH`, `DEAD`, `WRONG_CENTERLINE`); trims `STFT` / `LTFT` / `TOTAL_TRIM` /
   `DELTA_TRIM`; dotted enum values exactly as the shipped enums spell them
   (`TrimAnalyticsGate.O2_FAULT_ACTIVE`, `DownstreamTrimRole.CATALYST_MONITOR_ONLY`,
   `FuelSystemStatus.CLOSED_LOOP`). Fault tokens unified corpus-wide
   (`MAF_UNDERREPORT`, `EXHAUST_BACKPRESSURE`, `EGR_STUCK_OPEN`, `EVAP_PURGE_STUCK_OPEN`,
   `LEAKING_INJECTOR`, `ECU_CAPACITOR_LEAK`, `INJECTOR_DRIVER_OPEN|SHORT`, `COIL_DRIVER_SHORT`,
   `SENSOR_GROUND_TRACE_OPEN`, `VREF_RAIL_COLLAPSE`, consumer `ECU_HARDWARE_CHECKER`).
3. **Core Entities roster (#3, opt-in — owner chose to include).** A `## Core Entities` checklist per
   chunk listing its canonical entities + named consumer, giving the extractor an explicit roster so
   nothing important is skipped.

## Honesty / signal-noise guards observed

- **No invented edges.** Only relations stated in the chunk were made explicit (graphify honesty
  rule). Where the source carried a known **doc bug**, the trailer states the **non-edge**:
  `**SUPPRESS_POST_CAT_TRIM** IS_NOT a **TrimAnalyticsGate** value (doc bug O2-FU-2)` — it is *not*
  asserted as a gate edge (the ledger O2-FU-2 confirms it is not a real enum member).
- **Proposal vs active preserved.** Forward-progress entities (`WIDEBAND_OFFSET_CANDIDATE`,
  `ltft_cell_vector`, `prerequisite_dtc_gate`, the five ECU-hardware nodes, era/make priors, L5
  scorers, etc.) are labelled as proposals with their named consumers, matching each chunk's existing
  `consumer_status`. No live/proposal status was changed.

## Verification (this pass)

- **63/63** chunks carry **exactly one** `## Core Entities` and **exactly one**
  `## Graph relations (explicit)` block (no missing, no duplicate appends).
- **314** total `**bold** … **bold**` relation lines; **zero** chunks with an empty relations block.
- Trailers were appended in `a` (append) mode only — original bytes unchanged by construction.
- Canonical-token spot-check: enum values appear with identical spelling/casing across files
  (`DownstreamTrimRole.CATALYST_MONITOR_ONLY`, `TrimAnalyticsGate.O2_FAULT_ACTIVE`, `STUCK_LEAN`,
  `WIDEBAND_OFFSET_CANDIDATE`, `DELTA_TRIM`, `ECU_HARDWARE_CHECKER`).

## Per-dir coverage

| Dir | Chunks | Notes |
|---|---|---|
| `delta-relations/` | 9 | ΔTrim/Δgas profiles; PENDING consumer (FU-2) preserved. |
| `ecu-diagnosis/` | 10 | 5 proposed ECU-hardware fault nodes → `ECU_HARDWARE_CHECKER`. |
| `fuel-trim/` | 18 | DTC→fault `INDICATES` edges; 10 forward-progress proposals tagged. |
| `o2-logic/` | 9 | canonical `O2FailureMode` / `DownstreamTrimRole` / `TrimAnalyticsGate` enums; O2-FU-2 non-edge. |
| `pids-protocol/` | 9 | all-PROPOSAL input fields gated by named consumers. |
| `taxonomy/` | 3 | Euro-era / make-era priors. |
| `truth-perception/` | 5 | L1–L5; L3 = live `perception_contradiction`. |

## Next step

The corpus is ready for graphify pass-3. Run **T-KG-OBD-1** to build the brand-new wiki KG into
`graph/v2_wiki/` (input = `research/chunks/`; the old whole-lab `graph/v2_current/` stays untouched).
