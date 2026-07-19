---
chunk: fuel-trim/13_ltft-load-cell-matrix
topic: fuel-trim
sources:
  - Fuel Trim Diagnostics.txt §"GMH Long Term Fuel Trim Cell Descriptive"
  - FuelTrimFamilies.md §"Evolution of Fuel Trim Architecture" (LTFT cell adaptation)
consumer: PROPOSAL — consumer = a COMLab load-cell-resolved trim analyzer (register in comlab/config/proposals/). v2 today reads scalar trims + rpm_state_bucket + calculated_engine_load_pct, but does NOT resolve LTFT per MAF×RPM cell. Load-cell resolution is a forward-progress diagnostic dimension: it localises a fault to the operating region where trim deviates. Field (per-cell LTFT) + its consumer ship together as a proposal.
consumer_status: PROPOSAL
provenance: sources/fuel-trim/Fuel Trim Diagnostics.txt + FuelTrimFamilies.md
related: [[01_stft-ltft-fundamentals]], [[04_trim-pattern-decision-tree]], [[14_dtc-enable-criteria-and-blocking-codes]]
---

# LTFT load-cell matrix (MAF × RPM) — proposal

## The diagnostic idea

The PCM does not learn one LTFT — it learns a **matrix of LTFT cells indexed by
MAF (load) and RPM**. STFT operates in whichever cell the engine currently
occupies; LTFT for that cell absorbs the persistent correction. *Which cells*
deviate localises the fault:

- Deviation in **idle/low-load cells only** → idle-specific cause (vacuum leak,
  IAC leak, PCV).
- Deviation in **part-throttle cells only** → "concentrate on components that
  affect the part-throttle operating range" (e.g. mid-range fuel delivery, EGR).
- Deviation **across all cells** → global cause (MAF, fuel pressure, O₂ bias).

GMH example cells (VT V8 at idle): auto trans shows **cell 0** (canister purge
active) or **cell 17** (purge inactive); manual shows **cell 16** or **cell 33**.
The cell index itself encodes operating context (e.g. whether purge is flowing).

## Why this is a proposal, not active

Today's `OBDLivePayload` carries scalar `shrtft1/longft1` (+b2),
`calculated_engine_load_pct`, and `rpm_state_bucket` — enough to know the *current*
load bucket but **not** to compare LTFT *across* cells. No live code reads a
per-cell LTFT vector. The forward-progress proposal:

- **New field:** `ltft_cell_vector` (per-cell LTFT, indexed by load×RPM) on the
  OBDLab boundary — emitted only on platforms that expose the cell PIDs.
- **New consumer:** a COMLab load-cell trim analyzer that flags *which* region
  deviates and routes accordingly (idle-only vs part-throttle-only vs global),
  feeding fault_atlas family selection.
- **Ships together** (field + consumer) as a proposal per the v2 rule; register in
  `comlab/config/proposals/`. Until then, scalar idle-vs-RPM (chunk 04) is the
  active approximation.

Citation: Fuel Trim Diagnostics.txt LTFT cell descriptive (MAF×RPM matrix, idle
cells 0/17 auto, 16/33 manual, part-throttle-only localisation rule);
FuelTrimFamilies.md LTFT cell-adaptation paragraph.


## Core Entities

- ltft_cell_vector, LTFT
- COMLab load-cell trim analyzer (PROPOSAL consumer)

## Graph relations (explicit)

**LTFT** LEARNED_PER **MAF-x-RPM cell**
idle-cell-only deviation INDICATES idle-specific cause
part-throttle-cell deviation INDICATES mid-range cause
all-cell deviation INDICATES global cause (MAF / fuel pressure / O2 bias)
**ltft_cell_vector** EMITTED_BY OBDLab and CONSUMED_BY **COMLab load-cell trim analyzer**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
