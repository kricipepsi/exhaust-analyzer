# Post-Cat Fuel-Trim (B1S2) — PROGRESS ledger

Effort: re-implement downstream secondary fuel-trim modelling (Option C).
Reference oracle: `planning/sim/oil_burn_5fr_sim.py` (5/5 green).
Depends on: `T-VIN-FIX-3` (decoder).

| ID | Title | Lab | Depends | Status | Verification |
|---|---|---|---|---|---|
| PCT-1 | O2_MODEL_STRATEGY wiki | wiki | — | pending | |
| PCT-2 | OBDLab wiki: B1S2 PIDs + bias | wiki | PCT-1 | pending | |
| PCT-3 | VINLab/registry wiki: dual sensor + role | wiki | PCT-1 | pending | |
| PCT-4 | Identity: dual o2 type + role; seed 5FR | vinlab/dnalab | PCT-3 | pending | |
| PCT-5 | OBDLab schema+ingestion: B1S2 PIDs | obdlab | PCT-2,4 | pending | |
| PCT-6 | OBDLab core: post_cat_trim_bias | obdlab | PCT-5 | pending | |
| PCT-7 | COMLab mirror + perception | comlab | PCT-6 | pending | |
| PCT-8 | Registry post-cat evidence (MW-001/002/008/009) | registry | PCT-7 | pending | |
| PCT-9 | wiredV2 composition + fixtures | wiredV2 | PCT-8 | pending | |
| PCT-10 | E2E + corpus + sim parity | all | PCT-9 | pending | |

Notes:
- PCT-8 supersedes follow-ups U-WV2-1 (rings) and U-WV2-2 (PCV) from T-WV2-2.
- PCT-4 corrects the wrong single `o2_type='NB'` on 5FR → upstream WIDEBAND + downstream NARROWBAND.
