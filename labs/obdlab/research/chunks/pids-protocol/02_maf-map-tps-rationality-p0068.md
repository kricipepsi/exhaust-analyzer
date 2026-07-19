---
chunk: pids-protocol/02_maf-map-tps-rationality-p0068
topic: pids-protocol
sources:
  - various/Vol2.md — Master Document 4 (MAF/MAP Airflow Rationality); inferred-BARO
consumer: OBDLab rationality gate → COMLab fault_atlas (sensor-conflict / P0068). Cross-checks MAF vs MAP vs TPS so a single drifted air sensor cannot corrupt the whole fuel strategy.
consumer_status: PROPOSAL (rationality gate + inferred-BARO check not yet in v2)
provenance: sources/various/Vol2.md — concepts/prose READABLE; several numeric specs in the MD4 table stripped (flagged in formula wiki)
dedup: new; complements EP-OBD-11 theoretical-airflow cross-check (proposals/extracted)
---

# MAF/MAP/TPS rationality + inferred BARO (P0068)

Modern PCMs cross-check the three load sensors so one liar is caught by the other two.

## Rules (Vol2 MD4, readable)

- **P0068 trigger:** MAF reports high airflow but MAP shows high vacuum (low load) →
  MAF/MAP/TPS disagreement.
- **Volumetric-flow rule of thumb:** idle airflow ≈ engine displacement in litres
  (a 3.0 L engine pulls ≈ 3.0 g/s at idle).
- **Inferred BARO:** MAF-equipped vehicles without a BARO sensor compute it from
  MAF+MAP at hard WOT. If calculated BARO deviates from local actual (verified via a
  known-good MAP at KOEO or airport data) the MAF is out of calibration and is
  corrupting fuel control — a sensor that sets **no DTC** but skews λ (the L3
  blindness class, truth-perception/03 N-009/N-019).
- **WOT airflow:** MAF must reach peak rated g/s at WOT; failing to peak = under-report.

## Consumer / code path
OBDLab emits a `rationality` verdict (sensor agreement) + `inferred_baro_delta`;
COMLab fault_atlas reads them to demote a "lean fuelling" route in favour of "MAF
calibration drift" when the cross-check fails. Pairs with EP-OBD-11.


## Core Entities

- P0068, rationality, inferred_baro_delta, MAF, MAP, TPS
- OBDLab rationality gate -> COMLab fault_atlas (PROPOSAL, EP-OBD-11)

## Graph relations (explicit)

**MAF** high with **MAP** high-vacuum TRIGGERS **P0068**
**inferred_baro_delta** INDICATES **MAF_UNDERREPORT** calibration drift with no DTC
**rationality** EMITTED_BY OBDLab and CONSUMED_BY **fault_atlas**
**MAF-MAP-TPS rationality** PAIRS_WITH **EP-OBD-11**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
