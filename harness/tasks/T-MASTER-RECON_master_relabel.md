# T-MASTER-RECON — Reconcile the master CSV label vocabulary + column integrity

**Status:** `authored · coder-runnable` — **owner decisions RATIFIED 2026-06-09 (§Decisions)** ·
**Pack:** `4DLabV2/harness/` · **Mode:** STRICT (data/wiring stage) · **Date:** 2026-06-09
**Blocked by:** — (keystone) · **Upstream of:** `T-TH-10/11/12`, `T-TST-6`, `T-TST-7`.
**Load skills (session start):** read `HARNESS_START_HERE.md`; sandbox Python 3.14; mandatory pair
(`4DLabV2/_skills/codingskills/pythonskill/python` + `ecc-subset/verification-loop`).

## Why this exists (H-10, coder-caught 2026-06-05)

`cases_petrol_master_v6.csv` cannot be projected into per-lab fixtures as-is. The `expected_top_fault`
column **matches 0/277 `ChemicalSignature` values** and is not one vocabulary: it mixes family-level
(`rich_mixture`), scenario-level (`Exhaust_Air_Leak_Pre_Cat`, `ECU_Logic_Inversion_*`), 61 perception-gap
rows, and **malformed cells** (`single`×25, blank×14 = column misalignment from unescaped commas). A mapping
table cannot repair misaligned columns. This task reconciles the vocabulary **and** fixes integrity, upstream
of every master-derived fixture.

## Decisions — RATIFIED by owner 2026-06-09 (do not re-litigate)

1. **Canonical `expected_top_fault` vocabulary → option (a): per-lab enums under the EP-DTC-02 backbone.**
   Do **not** invent a new unified flat taxonomy and do **not** rebuild `labs/semantic` (T-SEM-1..4 closed).
   Reuse the ratified two-axis model:
   - Pin **`expected_top_fault_family`** (already a master column) to the **12-value `FaultFamily` enum** in
     `labs/semantic/vocabul/SEMANTIC_CONTRACT.md` §8 — this is the canonical, **lab-projectable** label every
     lab can map to.
   - Keep **`expected_top_fault`** as the granular `FaultNode` ID (COMLab registry vocabulary) where the source
     narrative supports it; otherwise set it to the family value.
   - **Source of truth:** `labs/semantic/vocabul/SEMANTIC_CONTRACT.md` §8 (FaultFamily) + `comlab/config/proposals/
     taxonomy_backbone.md` (EP-DTC-02 eight-family ISO 15031-6 / SAE J2012 backbone).
   - **Future additions:** never edit a live enum — a new fault value enters via `comlab/config/proposals/`
     (named producer + consumer + growth-safe gate). The recon may **not** introduce a label absent from
     FaultFamily/FaultNode without a proposal entry.
2. **Perception-gap rows (61) → distinct fusion-only class.** Keep the existing `expected_perception_gap=True`
   flag; these rows are **COMLab/wired-only**, never lab-decidable. Add a **`lab_decidability`** column naming
   which labs can decide each row so `T-TST-6/7` filter deterministically (decidable rows only; perception-gap
   rows reserved for the wired integration gate). Emit-S2 / consume-S4 pattern (cf. OBDLab FU-OBD-ORPHAN-1).
3. **Malformed rows + missing OBD ground-truth → quarantine + characterization.**
   - Move the misaligned rows (`single`×25, blank×14) to **`master_quarantine.csv`** with a per-row reason
     (do not silently repair; do not delete from the canonical lineage).
   - The master carries **no OBD expected-output columns** (`expected_obd_lambda`, `expected_ve_pct`,
     `expected_ve_validity`, `expected_trim_analytics_gate`, `expected_maf_status`, `expected_map_status`,
     `expected_o2_failure_mode`) and **does not** add them. OBD expected-outputs in `obdlab_cases.csv` (T-TST-6)
     are therefore **`gt_method=characterization`** (regression net, not correctness) per T-TST-8 §6 — not
     sourced ground truth this pass.

(Folds the H-3..H-6 drift adjudications — see `HARNESS_PROGRESS.md`.)

## Master → OBD column-name reconciliation (absorbed from the T-TST-6 readiness gap, 2026-06-09)

`PROJECTION_CONTRACT.md` lists OBDLab input columns that **do not match the real master header**, and several
do not exist. The recon's `MASTER_RECON_REPORT.md` MUST publish the canonical input-column inventory so
`T-TST-6` projects deterministically (no coder guessing). Observed drift to resolve:

| PROJECTION_CONTRACT name | Actual master column | Disposition |
|---|---|---|
| `engine_rpm` | `rpm` | map to real name |
| `coolant_temp_c` | `ect` | map to real name |
| `mass_airflow_gps` | `maf` | map to real name |
| `manifold_vacuum_kpa` | `map` | map to real name (note: MAP pressure, not vacuum — confirm unit) |
| `shrtft1`/`longft1`/`shrtft2`/`longft2` | `stft_b1`/`ltft_b1`/`stft_b2`/`ltft_b2` | map to real names |
| `calculated_engine_load_pct` | (absent) | not in master → omit from OBD projection or mark unavailable |
| `has_maf`/`has_map`/`number_of_banks` (DNA) | (absent) | derive from `bank_config`/VIN columns, else default per OBDLab schema; pin in report |

Correcting `PROJECTION_CONTRACT.md` itself is a **follow-up** (logged below), not this diff — the recon publishes
the authoritative inventory; the contract is reconciled to it when `T-TST-6` is implemented.

## Deliverables

1. Reconciled `cases_petrol_master_v6.csv` — `expected_top_fault_family` ∈ the 12-value `FaultFamily` enum
   (Decision 1); `expected_top_fault` = granular `FaultNode` or the family value; column integrity fixed
   (no `single`/blank misalignment — those rows quarantined, not repaired); existing `expected_perception_gap`
   retained; **new `lab_decidability` column** naming the labs that can decide each row (Decision 2). Backup the
   pre-recon file by path.
2. `master_quarantine.csv` — the `single`×25 + blank×14 misaligned rows, each with a per-row reason (Decision 3).
3. `MASTER_RECON_REPORT.md` — row-count before/after, the FaultFamily relabel map, integrity fixes, quarantine
   list, which rows are GASLab-/OBD-/DTC-decidable vs fusion-only, **and the canonical OBD input-column inventory**
   (the master→OBD name map in §"Master → OBD column-name reconciliation") so `T-TST-6` projects without guessing.

## Success criteria

- 0 malformed/misaligned rows in the reconciled master; every misaligned row is in `master_quarantine.csv` with a reason.
- Every `expected_top_fault_family` cell ∈ the 12-value `FaultFamily` enum; no label introduced that is absent
  from FaultFamily/FaultNode without a `comlab/config/proposals/` entry.
- Each row classified lab-decidable (`lab_decidability`) vs perception-gap (`expected_perception_gap`), so
  `T-TST-6/7` and `T-TH-10` can filter deterministically.
- `MASTER_RECON_REPORT.md` publishes the master→OBD input-column inventory; no OBD expected-output column is
  added to the master (OBD expecteds are characterization downstream in T-TST-6).
- Master stays the canonical wired-integration corpus (do not delete rows; relabel/classify/quarantine only).

## Signal/noise consumer

The reconciled labels + decidability column are consumed by `T-TST-6` (obdlab CSV), `T-TST-7` (dtclab CSV),
and `T-TH-10/12` (gaslab fixture + wired gate). No new column ships without one of those consumers.

## Out of scope

Building any per-lab CSV (that is `T-TST-6/7`). Editing lab code or schemas. Re-running graphify.
Correcting `PROJECTION_CONTRACT.md` to the real column names (follow-up below — the report publishes the
authoritative inventory; the contract is reconciled to it when `T-TST-6` is implemented).

## Unplanned follow-ups (logged, not in this diff)

| ID | Finding | Disposition |
|---|---|---|
| FU-RECON-1 | `PROJECTION_CONTRACT.md` OBDLab input names (`engine_rpm`, `mass_airflow_gps`, `shrtft1`, `has_maf`/`has_map`, `calculated_engine_load_pct`) don't match the real master header (`rpm`, `maf`, `stft_b1`, no has_maf/has_map/load%). | Reconcile `PROJECTION_CONTRACT.md` to the report's inventory at `T-TST-6` implementation. |

## VERIFICATION GATE / CODE REVIEW
(coder fills in `progress_notes/T-MASTER-RECON.md`, opening with `## Plan`.)
