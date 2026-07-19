# T-SHIP-3 — VIN blank-brand join recovery (~11.6% of petrol traffic)
**Pack:** ship · **Blocked by:** — · **Lane:** coder
**Write scope:** `labs/vinlab/vinlab/data/wmi.csv`, `labs/vinlab/vinlab/data/vds_engine_map.csv`
(brand-cell repairs only), any small normalizer in `labs/vinlab/vinlab/`, tests, report.

## Why (audit B-4)
`planning/AUDIT_2026-07-06_vin_engine_number.md` §6: blank-brand WMI rows kill the brand
join for **11.6% of petrol traffic** (top: TMB, VSS, TSM, UU1, TMA, NLH); Škoda is dead on
both sides (`wmi.csv` blank AND map brand mojibake `�KODA`); +1.1% of traffic WMIs are
absent from `wmi.csv` entirely. ENG-1/ENG-2 fixed the engine map + vref join, not this.

## Signal/noise consumer (named, live)
`RobustVINDecoder` brand join → VehicleDNA brand/model fields → dnalab
`build_vehicle_dna` → wired composition. No new field ships; this repairs data an
existing code path already reads.

## Steps
1. Backfill blank `brand` cells in `wmi.csv` from majority vote over the in-repo
   `docs/Nio_vozila_1/2.csv` (train) — same method the ENG-1 rebuild used. Repair
   mojibake brand cells in `vds_engine_map.csv` (fold to the `wmi.csv` spelling).
   Add absent high-traffic WMIs (>0.05% traffic) from the same vote.
2. Held-out eval on `docs/Nio_vozila_3.csv` (all petrol rows): report blank-brand share
   before/after, and decode spot-checks for `TMB…` (Škoda) and `UU1…` (Dacia) VINs.
3. Unit tests: one recovered-brand decode per repaired top-6 WMI; mojibake-free
   assertion over both CSVs (`no '�' in any brand cell`).
4. Report `labs/vinlab/VIN_BRAND_RECOVERY_2026-07-07.md`; both gates; flip the row.

## Success criteria
- Blank-brand share on file-3 petrol traffic: 11.6% → **< 2%**; no existing decode regresses
  (`pytest labs/vinlab/tests` green, incl. the ENG-2 suite 197 passed baseline).
- Every backfilled brand is majority-vote evidence, never guessed; ambiguous WMIs
  (no majority ≥ 0.70) stay blank and are listed in the report.
