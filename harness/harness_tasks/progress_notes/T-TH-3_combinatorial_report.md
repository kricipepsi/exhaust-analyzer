# Combinatorial Generator Report

**Date:** 2026-06-07  
**Coverage:** pairwise (t=2) corners — C(5,2) dim-pairs x 4 corners per box  
**Total cases:** 1360  
**PASS:** 174 | **FAIL:** 1186  

**174/1360** pairwise corners match geometric oracle (12.8%).  
**1186 mismatch(es)**.

**Overlap caveat:** mismatches may be caused by overlapping fault boxes (analyzed in T-TH-2). A FAIL with oracle=inside means the classifier returned a different signature for a corner geometrically inside this box — which may be correct if the corner also falls inside another box.

## Results

| # | case_id | Box | Dim pair | Corner | Oracle | Actual | Match |
|---|---|---|---|---|---|---|---|
| 1 | TH-CMB-NORMAL_OPERATION-gas_hc-gas_co-mnmn | NORMAL_OPERATION | (gas_hc, gas_co) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 2 | TH-CMB-NORMAL_OPERATION-gas_hc-gas_co-mnmx | NORMAL_OPERATION | (gas_hc, gas_co) | (mn, mx) | inside | TIMING_RETARDED | FAIL |
| 3 | TH-CMB-NORMAL_OPERATION-gas_hc-gas_co-mxmn | NORMAL_OPERATION | (gas_hc, gas_co) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 4 | TH-CMB-NORMAL_OPERATION-gas_hc-gas_co-mxmx | NORMAL_OPERATION | (gas_hc, gas_co) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 5 | TH-CMB-NORMAL_OPERATION-gas_hc-gas_co2-mnmn | NORMAL_OPERATION | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 6 | TH-CMB-NORMAL_OPERATION-gas_hc-gas_co2-mnmx | NORMAL_OPERATION | (gas_hc, gas_co2) | (mn, mx) | inside | TIMING_RETARDED | FAIL |
| 7 | TH-CMB-NORMAL_OPERATION-gas_hc-gas_co2-mxmn | NORMAL_OPERATION | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 8 | TH-CMB-NORMAL_OPERATION-gas_hc-gas_co2-mxmx | NORMAL_OPERATION | (gas_hc, gas_co2) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 9 | TH-CMB-NORMAL_OPERATION-gas_hc-gas_o2-mnmn | NORMAL_OPERATION | (gas_hc, gas_o2) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 10 | TH-CMB-NORMAL_OPERATION-gas_hc-gas_o2-mnmx | NORMAL_OPERATION | (gas_hc, gas_o2) | (mn, mx) | inside | TIMING_RETARDED | FAIL |
| 11 | TH-CMB-NORMAL_OPERATION-gas_hc-gas_o2-mxmn | NORMAL_OPERATION | (gas_hc, gas_o2) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 12 | TH-CMB-NORMAL_OPERATION-gas_hc-gas_o2-mxmx | NORMAL_OPERATION | (gas_hc, gas_o2) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 13 | TH-CMB-NORMAL_OPERATION-gas_hc-gas_nox-mnmn | NORMAL_OPERATION | (gas_hc, gas_nox) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 14 | TH-CMB-NORMAL_OPERATION-gas_hc-gas_nox-mnmx | NORMAL_OPERATION | (gas_hc, gas_nox) | (mn, mx) | inside | WORN_PISTON_RINGS | FAIL |
| 15 | TH-CMB-NORMAL_OPERATION-gas_hc-gas_nox-mxmn | NORMAL_OPERATION | (gas_hc, gas_nox) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 16 | TH-CMB-NORMAL_OPERATION-gas_hc-gas_nox-mxmx | NORMAL_OPERATION | (gas_hc, gas_nox) | (mx, mx) | inside | WORN_PISTON_RINGS | FAIL |
| 17 | TH-CMB-NORMAL_OPERATION-gas_co-gas_co2-mnmn | NORMAL_OPERATION | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 18 | TH-CMB-NORMAL_OPERATION-gas_co-gas_co2-mnmx | NORMAL_OPERATION | (gas_co, gas_co2) | (mn, mx) | inside | TIMING_RETARDED | FAIL |
| 19 | TH-CMB-NORMAL_OPERATION-gas_co-gas_co2-mxmn | NORMAL_OPERATION | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 20 | TH-CMB-NORMAL_OPERATION-gas_co-gas_co2-mxmx | NORMAL_OPERATION | (gas_co, gas_co2) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 21 | TH-CMB-NORMAL_OPERATION-gas_co-gas_o2-mnmn | NORMAL_OPERATION | (gas_co, gas_o2) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 22 | TH-CMB-NORMAL_OPERATION-gas_co-gas_o2-mnmx | NORMAL_OPERATION | (gas_co, gas_o2) | (mn, mx) | inside | TIMING_RETARDED | FAIL |
| 23 | TH-CMB-NORMAL_OPERATION-gas_co-gas_o2-mxmn | NORMAL_OPERATION | (gas_co, gas_o2) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 24 | TH-CMB-NORMAL_OPERATION-gas_co-gas_o2-mxmx | NORMAL_OPERATION | (gas_co, gas_o2) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 25 | TH-CMB-NORMAL_OPERATION-gas_co-gas_nox-mnmn | NORMAL_OPERATION | (gas_co, gas_nox) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 26 | TH-CMB-NORMAL_OPERATION-gas_co-gas_nox-mnmx | NORMAL_OPERATION | (gas_co, gas_nox) | (mn, mx) | inside | WORN_PISTON_RINGS | FAIL |
| 27 | TH-CMB-NORMAL_OPERATION-gas_co-gas_nox-mxmn | NORMAL_OPERATION | (gas_co, gas_nox) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 28 | TH-CMB-NORMAL_OPERATION-gas_co-gas_nox-mxmx | NORMAL_OPERATION | (gas_co, gas_nox) | (mx, mx) | inside | WORN_PISTON_RINGS | FAIL |
| 29 | TH-CMB-NORMAL_OPERATION-gas_co2-gas_o2-mnmn | NORMAL_OPERATION | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 30 | TH-CMB-NORMAL_OPERATION-gas_co2-gas_o2-mnmx | NORMAL_OPERATION | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 31 | TH-CMB-NORMAL_OPERATION-gas_co2-gas_o2-mxmn | NORMAL_OPERATION | (gas_co2, gas_o2) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 32 | TH-CMB-NORMAL_OPERATION-gas_co2-gas_o2-mxmx | NORMAL_OPERATION | (gas_co2, gas_o2) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 33 | TH-CMB-NORMAL_OPERATION-gas_co2-gas_nox-mnmn | NORMAL_OPERATION | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 34 | TH-CMB-NORMAL_OPERATION-gas_co2-gas_nox-mnmx | NORMAL_OPERATION | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 35 | TH-CMB-NORMAL_OPERATION-gas_co2-gas_nox-mxmn | NORMAL_OPERATION | (gas_co2, gas_nox) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 36 | TH-CMB-NORMAL_OPERATION-gas_co2-gas_nox-mxmx | NORMAL_OPERATION | (gas_co2, gas_nox) | (mx, mx) | inside | WORN_PISTON_RINGS | FAIL |
| 37 | TH-CMB-NORMAL_OPERATION-gas_o2-gas_nox-mnmn | NORMAL_OPERATION | (gas_o2, gas_nox) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 38 | TH-CMB-NORMAL_OPERATION-gas_o2-gas_nox-mnmx | NORMAL_OPERATION | (gas_o2, gas_nox) | (mn, mx) | inside | WORN_PISTON_RINGS | FAIL |
| 39 | TH-CMB-NORMAL_OPERATION-gas_o2-gas_nox-mxmn | NORMAL_OPERATION | (gas_o2, gas_nox) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 40 | TH-CMB-NORMAL_OPERATION-gas_o2-gas_nox-mxmx | NORMAL_OPERATION | (gas_o2, gas_nox) | (mx, mx) | inside | WORN_PISTON_RINGS | FAIL |
| 41 | TH-CMB-RICH_MIXTURE-gas_hc-gas_co-mnmn | RICH_MIXTURE | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 42 | TH-CMB-RICH_MIXTURE-gas_hc-gas_co-mnmx | RICH_MIXTURE | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 43 | TH-CMB-RICH_MIXTURE-gas_hc-gas_co-mxmn | RICH_MIXTURE | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 44 | TH-CMB-RICH_MIXTURE-gas_hc-gas_co-mxmx | RICH_MIXTURE | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 45 | TH-CMB-RICH_MIXTURE-gas_hc-gas_co2-mnmn | RICH_MIXTURE | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 46 | TH-CMB-RICH_MIXTURE-gas_hc-gas_co2-mnmx | RICH_MIXTURE | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 47 | TH-CMB-RICH_MIXTURE-gas_hc-gas_co2-mxmn | RICH_MIXTURE | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 48 | TH-CMB-RICH_MIXTURE-gas_hc-gas_co2-mxmx | RICH_MIXTURE | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 49 | TH-CMB-RICH_MIXTURE-gas_hc-gas_o2-mnmn | RICH_MIXTURE | (gas_hc, gas_o2) | (mn, mn) | inside | VVT_FAILURE | FAIL |
| 50 | TH-CMB-RICH_MIXTURE-gas_hc-gas_o2-mnmx | RICH_MIXTURE | (gas_hc, gas_o2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 51 | TH-CMB-RICH_MIXTURE-gas_hc-gas_o2-mxmn | RICH_MIXTURE | (gas_hc, gas_o2) | (mx, mn) | inside | POA_SIGNATURE | FAIL |
| 52 | TH-CMB-RICH_MIXTURE-gas_hc-gas_o2-mxmx | RICH_MIXTURE | (gas_hc, gas_o2) | (mx, mx) | inside | POA_SIGNATURE | FAIL |
| 53 | TH-CMB-RICH_MIXTURE-gas_hc-gas_nox-mnmn | RICH_MIXTURE | (gas_hc, gas_nox) | (mn, mn) | inside | RICH_MIXTURE | PASS |
| 54 | TH-CMB-RICH_MIXTURE-gas_hc-gas_nox-mnmx | RICH_MIXTURE | (gas_hc, gas_nox) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 55 | TH-CMB-RICH_MIXTURE-gas_hc-gas_nox-mxmn | RICH_MIXTURE | (gas_hc, gas_nox) | (mx, mn) | inside | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | FAIL |
| 56 | TH-CMB-RICH_MIXTURE-gas_hc-gas_nox-mxmx | RICH_MIXTURE | (gas_hc, gas_nox) | (mx, mx) | inside | CATALYST_OVERWHELMED | FAIL |
| 57 | TH-CMB-RICH_MIXTURE-gas_co-gas_co2-mnmn | RICH_MIXTURE | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 58 | TH-CMB-RICH_MIXTURE-gas_co-gas_co2-mnmx | RICH_MIXTURE | (gas_co, gas_co2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 59 | TH-CMB-RICH_MIXTURE-gas_co-gas_co2-mxmn | RICH_MIXTURE | (gas_co, gas_co2) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 60 | TH-CMB-RICH_MIXTURE-gas_co-gas_co2-mxmx | RICH_MIXTURE | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 61 | TH-CMB-RICH_MIXTURE-gas_co-gas_o2-mnmn | RICH_MIXTURE | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 62 | TH-CMB-RICH_MIXTURE-gas_co-gas_o2-mnmx | RICH_MIXTURE | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 63 | TH-CMB-RICH_MIXTURE-gas_co-gas_o2-mxmn | RICH_MIXTURE | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 64 | TH-CMB-RICH_MIXTURE-gas_co-gas_o2-mxmx | RICH_MIXTURE | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 65 | TH-CMB-RICH_MIXTURE-gas_co-gas_nox-mnmn | RICH_MIXTURE | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 66 | TH-CMB-RICH_MIXTURE-gas_co-gas_nox-mnmx | RICH_MIXTURE | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 67 | TH-CMB-RICH_MIXTURE-gas_co-gas_nox-mxmn | RICH_MIXTURE | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 68 | TH-CMB-RICH_MIXTURE-gas_co-gas_nox-mxmx | RICH_MIXTURE | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 69 | TH-CMB-RICH_MIXTURE-gas_co2-gas_o2-mnmn | RICH_MIXTURE | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 70 | TH-CMB-RICH_MIXTURE-gas_co2-gas_o2-mnmx | RICH_MIXTURE | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 71 | TH-CMB-RICH_MIXTURE-gas_co2-gas_o2-mxmn | RICH_MIXTURE | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 72 | TH-CMB-RICH_MIXTURE-gas_co2-gas_o2-mxmx | RICH_MIXTURE | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 73 | TH-CMB-RICH_MIXTURE-gas_co2-gas_nox-mnmn | RICH_MIXTURE | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 74 | TH-CMB-RICH_MIXTURE-gas_co2-gas_nox-mnmx | RICH_MIXTURE | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 75 | TH-CMB-RICH_MIXTURE-gas_co2-gas_nox-mxmn | RICH_MIXTURE | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 76 | TH-CMB-RICH_MIXTURE-gas_co2-gas_nox-mxmx | RICH_MIXTURE | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 77 | TH-CMB-RICH_MIXTURE-gas_o2-gas_nox-mnmn | RICH_MIXTURE | (gas_o2, gas_nox) | (mn, mn) | inside | RICH_MIXTURE | PASS |
| 78 | TH-CMB-RICH_MIXTURE-gas_o2-gas_nox-mnmx | RICH_MIXTURE | (gas_o2, gas_nox) | (mn, mx) | inside | CATALYST_OVERWHELMED | FAIL |
| 79 | TH-CMB-RICH_MIXTURE-gas_o2-gas_nox-mxmn | RICH_MIXTURE | (gas_o2, gas_nox) | (mx, mn) | inside | RICH_MIXTURE | PASS |
| 80 | TH-CMB-RICH_MIXTURE-gas_o2-gas_nox-mxmx | RICH_MIXTURE | (gas_o2, gas_nox) | (mx, mx) | inside | CATALYST_OVERWHELMED | FAIL |
| 81 | TH-CMB-LEAN_MIXTURE-gas_hc-gas_co-mnmn | LEAN_MIXTURE | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 82 | TH-CMB-LEAN_MIXTURE-gas_hc-gas_co-mnmx | LEAN_MIXTURE | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 83 | TH-CMB-LEAN_MIXTURE-gas_hc-gas_co-mxmn | LEAN_MIXTURE | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 84 | TH-CMB-LEAN_MIXTURE-gas_hc-gas_co-mxmx | LEAN_MIXTURE | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 85 | TH-CMB-LEAN_MIXTURE-gas_hc-gas_co2-mnmn | LEAN_MIXTURE | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 86 | TH-CMB-LEAN_MIXTURE-gas_hc-gas_co2-mnmx | LEAN_MIXTURE | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 87 | TH-CMB-LEAN_MIXTURE-gas_hc-gas_co2-mxmn | LEAN_MIXTURE | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 88 | TH-CMB-LEAN_MIXTURE-gas_hc-gas_co2-mxmx | LEAN_MIXTURE | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 89 | TH-CMB-LEAN_MIXTURE-gas_hc-gas_o2-mnmn | LEAN_MIXTURE | (gas_hc, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 90 | TH-CMB-LEAN_MIXTURE-gas_hc-gas_o2-mnmx | LEAN_MIXTURE | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 91 | TH-CMB-LEAN_MIXTURE-gas_hc-gas_o2-mxmn | LEAN_MIXTURE | (gas_hc, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 92 | TH-CMB-LEAN_MIXTURE-gas_hc-gas_o2-mxmx | LEAN_MIXTURE | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 93 | TH-CMB-LEAN_MIXTURE-gas_hc-gas_nox-mnmn | LEAN_MIXTURE | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 94 | TH-CMB-LEAN_MIXTURE-gas_hc-gas_nox-mnmx | LEAN_MIXTURE | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 95 | TH-CMB-LEAN_MIXTURE-gas_hc-gas_nox-mxmn | LEAN_MIXTURE | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 96 | TH-CMB-LEAN_MIXTURE-gas_hc-gas_nox-mxmx | LEAN_MIXTURE | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 97 | TH-CMB-LEAN_MIXTURE-gas_co-gas_co2-mnmn | LEAN_MIXTURE | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 98 | TH-CMB-LEAN_MIXTURE-gas_co-gas_co2-mnmx | LEAN_MIXTURE | (gas_co, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 99 | TH-CMB-LEAN_MIXTURE-gas_co-gas_co2-mxmn | LEAN_MIXTURE | (gas_co, gas_co2) | (mx, mn) | inside | EXHAUST_AIR_LEAK | FAIL |
| 100 | TH-CMB-LEAN_MIXTURE-gas_co-gas_co2-mxmx | LEAN_MIXTURE | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 101 | TH-CMB-LEAN_MIXTURE-gas_co-gas_o2-mnmn | LEAN_MIXTURE | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 102 | TH-CMB-LEAN_MIXTURE-gas_co-gas_o2-mnmx | LEAN_MIXTURE | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 103 | TH-CMB-LEAN_MIXTURE-gas_co-gas_o2-mxmn | LEAN_MIXTURE | (gas_co, gas_o2) | (mx, mn) | inside | EXHAUST_AIR_LEAK | FAIL |
| 104 | TH-CMB-LEAN_MIXTURE-gas_co-gas_o2-mxmx | LEAN_MIXTURE | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 105 | TH-CMB-LEAN_MIXTURE-gas_co-gas_nox-mnmn | LEAN_MIXTURE | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 106 | TH-CMB-LEAN_MIXTURE-gas_co-gas_nox-mnmx | LEAN_MIXTURE | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 107 | TH-CMB-LEAN_MIXTURE-gas_co-gas_nox-mxmn | LEAN_MIXTURE | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 108 | TH-CMB-LEAN_MIXTURE-gas_co-gas_nox-mxmx | LEAN_MIXTURE | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 109 | TH-CMB-LEAN_MIXTURE-gas_co2-gas_o2-mnmn | LEAN_MIXTURE | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 110 | TH-CMB-LEAN_MIXTURE-gas_co2-gas_o2-mnmx | LEAN_MIXTURE | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 111 | TH-CMB-LEAN_MIXTURE-gas_co2-gas_o2-mxmn | LEAN_MIXTURE | (gas_co2, gas_o2) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 112 | TH-CMB-LEAN_MIXTURE-gas_co2-gas_o2-mxmx | LEAN_MIXTURE | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 113 | TH-CMB-LEAN_MIXTURE-gas_co2-gas_nox-mnmn | LEAN_MIXTURE | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 114 | TH-CMB-LEAN_MIXTURE-gas_co2-gas_nox-mnmx | LEAN_MIXTURE | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 115 | TH-CMB-LEAN_MIXTURE-gas_co2-gas_nox-mxmn | LEAN_MIXTURE | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 116 | TH-CMB-LEAN_MIXTURE-gas_co2-gas_nox-mxmx | LEAN_MIXTURE | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 117 | TH-CMB-LEAN_MIXTURE-gas_o2-gas_nox-mnmn | LEAN_MIXTURE | (gas_o2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 118 | TH-CMB-LEAN_MIXTURE-gas_o2-gas_nox-mnmx | LEAN_MIXTURE | (gas_o2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 119 | TH-CMB-LEAN_MIXTURE-gas_o2-gas_nox-mxmn | LEAN_MIXTURE | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 120 | TH-CMB-LEAN_MIXTURE-gas_o2-gas_nox-mxmx | LEAN_MIXTURE | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 121 | TH-CMB-IGNITION_MISFIRE-gas_hc-gas_co-mnmn | IGNITION_MISFIRE | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 122 | TH-CMB-IGNITION_MISFIRE-gas_hc-gas_co-mnmx | IGNITION_MISFIRE | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 123 | TH-CMB-IGNITION_MISFIRE-gas_hc-gas_co-mxmn | IGNITION_MISFIRE | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 124 | TH-CMB-IGNITION_MISFIRE-gas_hc-gas_co-mxmx | IGNITION_MISFIRE | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 125 | TH-CMB-IGNITION_MISFIRE-gas_hc-gas_co2-mnmn | IGNITION_MISFIRE | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 126 | TH-CMB-IGNITION_MISFIRE-gas_hc-gas_co2-mnmx | IGNITION_MISFIRE | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 127 | TH-CMB-IGNITION_MISFIRE-gas_hc-gas_co2-mxmn | IGNITION_MISFIRE | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 128 | TH-CMB-IGNITION_MISFIRE-gas_hc-gas_co2-mxmx | IGNITION_MISFIRE | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 129 | TH-CMB-IGNITION_MISFIRE-gas_hc-gas_o2-mnmn | IGNITION_MISFIRE | (gas_hc, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 130 | TH-CMB-IGNITION_MISFIRE-gas_hc-gas_o2-mnmx | IGNITION_MISFIRE | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 131 | TH-CMB-IGNITION_MISFIRE-gas_hc-gas_o2-mxmn | IGNITION_MISFIRE | (gas_hc, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 132 | TH-CMB-IGNITION_MISFIRE-gas_hc-gas_o2-mxmx | IGNITION_MISFIRE | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 133 | TH-CMB-IGNITION_MISFIRE-gas_hc-gas_nox-mnmn | IGNITION_MISFIRE | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 134 | TH-CMB-IGNITION_MISFIRE-gas_hc-gas_nox-mnmx | IGNITION_MISFIRE | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 135 | TH-CMB-IGNITION_MISFIRE-gas_hc-gas_nox-mxmn | IGNITION_MISFIRE | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 136 | TH-CMB-IGNITION_MISFIRE-gas_hc-gas_nox-mxmx | IGNITION_MISFIRE | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 137 | TH-CMB-IGNITION_MISFIRE-gas_co-gas_co2-mnmn | IGNITION_MISFIRE | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 138 | TH-CMB-IGNITION_MISFIRE-gas_co-gas_co2-mnmx | IGNITION_MISFIRE | (gas_co, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 139 | TH-CMB-IGNITION_MISFIRE-gas_co-gas_co2-mxmn | IGNITION_MISFIRE | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 140 | TH-CMB-IGNITION_MISFIRE-gas_co-gas_co2-mxmx | IGNITION_MISFIRE | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 141 | TH-CMB-IGNITION_MISFIRE-gas_co-gas_o2-mnmn | IGNITION_MISFIRE | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 142 | TH-CMB-IGNITION_MISFIRE-gas_co-gas_o2-mnmx | IGNITION_MISFIRE | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 143 | TH-CMB-IGNITION_MISFIRE-gas_co-gas_o2-mxmn | IGNITION_MISFIRE | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 144 | TH-CMB-IGNITION_MISFIRE-gas_co-gas_o2-mxmx | IGNITION_MISFIRE | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 145 | TH-CMB-IGNITION_MISFIRE-gas_co-gas_nox-mnmn | IGNITION_MISFIRE | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 146 | TH-CMB-IGNITION_MISFIRE-gas_co-gas_nox-mnmx | IGNITION_MISFIRE | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 147 | TH-CMB-IGNITION_MISFIRE-gas_co-gas_nox-mxmn | IGNITION_MISFIRE | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 148 | TH-CMB-IGNITION_MISFIRE-gas_co-gas_nox-mxmx | IGNITION_MISFIRE | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 149 | TH-CMB-IGNITION_MISFIRE-gas_co2-gas_o2-mnmn | IGNITION_MISFIRE | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 150 | TH-CMB-IGNITION_MISFIRE-gas_co2-gas_o2-mnmx | IGNITION_MISFIRE | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 151 | TH-CMB-IGNITION_MISFIRE-gas_co2-gas_o2-mxmn | IGNITION_MISFIRE | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 152 | TH-CMB-IGNITION_MISFIRE-gas_co2-gas_o2-mxmx | IGNITION_MISFIRE | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 153 | TH-CMB-IGNITION_MISFIRE-gas_co2-gas_nox-mnmn | IGNITION_MISFIRE | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 154 | TH-CMB-IGNITION_MISFIRE-gas_co2-gas_nox-mnmx | IGNITION_MISFIRE | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 155 | TH-CMB-IGNITION_MISFIRE-gas_co2-gas_nox-mxmn | IGNITION_MISFIRE | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 156 | TH-CMB-IGNITION_MISFIRE-gas_co2-gas_nox-mxmx | IGNITION_MISFIRE | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 157 | TH-CMB-IGNITION_MISFIRE-gas_o2-gas_nox-mnmn | IGNITION_MISFIRE | (gas_o2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 158 | TH-CMB-IGNITION_MISFIRE-gas_o2-gas_nox-mnmx | IGNITION_MISFIRE | (gas_o2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 159 | TH-CMB-IGNITION_MISFIRE-gas_o2-gas_nox-mxmn | IGNITION_MISFIRE | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 160 | TH-CMB-IGNITION_MISFIRE-gas_o2-gas_nox-mxmx | IGNITION_MISFIRE | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 161 | TH-CMB-LEAN_MISFIRE-gas_hc-gas_co-mnmn | LEAN_MISFIRE | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 162 | TH-CMB-LEAN_MISFIRE-gas_hc-gas_co-mnmx | LEAN_MISFIRE | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 163 | TH-CMB-LEAN_MISFIRE-gas_hc-gas_co-mxmn | LEAN_MISFIRE | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 164 | TH-CMB-LEAN_MISFIRE-gas_hc-gas_co-mxmx | LEAN_MISFIRE | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 165 | TH-CMB-LEAN_MISFIRE-gas_hc-gas_co2-mnmn | LEAN_MISFIRE | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 166 | TH-CMB-LEAN_MISFIRE-gas_hc-gas_co2-mnmx | LEAN_MISFIRE | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 167 | TH-CMB-LEAN_MISFIRE-gas_hc-gas_co2-mxmn | LEAN_MISFIRE | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 168 | TH-CMB-LEAN_MISFIRE-gas_hc-gas_co2-mxmx | LEAN_MISFIRE | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 169 | TH-CMB-LEAN_MISFIRE-gas_hc-gas_o2-mnmn | LEAN_MISFIRE | (gas_hc, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 170 | TH-CMB-LEAN_MISFIRE-gas_hc-gas_o2-mnmx | LEAN_MISFIRE | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 171 | TH-CMB-LEAN_MISFIRE-gas_hc-gas_o2-mxmn | LEAN_MISFIRE | (gas_hc, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 172 | TH-CMB-LEAN_MISFIRE-gas_hc-gas_o2-mxmx | LEAN_MISFIRE | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 173 | TH-CMB-LEAN_MISFIRE-gas_hc-gas_nox-mnmn | LEAN_MISFIRE | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 174 | TH-CMB-LEAN_MISFIRE-gas_hc-gas_nox-mnmx | LEAN_MISFIRE | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 175 | TH-CMB-LEAN_MISFIRE-gas_hc-gas_nox-mxmn | LEAN_MISFIRE | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 176 | TH-CMB-LEAN_MISFIRE-gas_hc-gas_nox-mxmx | LEAN_MISFIRE | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 177 | TH-CMB-LEAN_MISFIRE-gas_co-gas_co2-mnmn | LEAN_MISFIRE | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 178 | TH-CMB-LEAN_MISFIRE-gas_co-gas_co2-mnmx | LEAN_MISFIRE | (gas_co, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 179 | TH-CMB-LEAN_MISFIRE-gas_co-gas_co2-mxmn | LEAN_MISFIRE | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 180 | TH-CMB-LEAN_MISFIRE-gas_co-gas_co2-mxmx | LEAN_MISFIRE | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 181 | TH-CMB-LEAN_MISFIRE-gas_co-gas_o2-mnmn | LEAN_MISFIRE | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 182 | TH-CMB-LEAN_MISFIRE-gas_co-gas_o2-mnmx | LEAN_MISFIRE | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 183 | TH-CMB-LEAN_MISFIRE-gas_co-gas_o2-mxmn | LEAN_MISFIRE | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 184 | TH-CMB-LEAN_MISFIRE-gas_co-gas_o2-mxmx | LEAN_MISFIRE | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 185 | TH-CMB-LEAN_MISFIRE-gas_co-gas_nox-mnmn | LEAN_MISFIRE | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 186 | TH-CMB-LEAN_MISFIRE-gas_co-gas_nox-mnmx | LEAN_MISFIRE | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 187 | TH-CMB-LEAN_MISFIRE-gas_co-gas_nox-mxmn | LEAN_MISFIRE | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 188 | TH-CMB-LEAN_MISFIRE-gas_co-gas_nox-mxmx | LEAN_MISFIRE | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 189 | TH-CMB-LEAN_MISFIRE-gas_co2-gas_o2-mnmn | LEAN_MISFIRE | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 190 | TH-CMB-LEAN_MISFIRE-gas_co2-gas_o2-mnmx | LEAN_MISFIRE | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 191 | TH-CMB-LEAN_MISFIRE-gas_co2-gas_o2-mxmn | LEAN_MISFIRE | (gas_co2, gas_o2) | (mx, mn) | inside | LEAN_MISFIRE | PASS |
| 192 | TH-CMB-LEAN_MISFIRE-gas_co2-gas_o2-mxmx | LEAN_MISFIRE | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 193 | TH-CMB-LEAN_MISFIRE-gas_co2-gas_nox-mnmn | LEAN_MISFIRE | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 194 | TH-CMB-LEAN_MISFIRE-gas_co2-gas_nox-mnmx | LEAN_MISFIRE | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 195 | TH-CMB-LEAN_MISFIRE-gas_co2-gas_nox-mxmn | LEAN_MISFIRE | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 196 | TH-CMB-LEAN_MISFIRE-gas_co2-gas_nox-mxmx | LEAN_MISFIRE | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 197 | TH-CMB-LEAN_MISFIRE-gas_o2-gas_nox-mnmn | LEAN_MISFIRE | (gas_o2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 198 | TH-CMB-LEAN_MISFIRE-gas_o2-gas_nox-mnmx | LEAN_MISFIRE | (gas_o2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 199 | TH-CMB-LEAN_MISFIRE-gas_o2-gas_nox-mxmn | LEAN_MISFIRE | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 200 | TH-CMB-LEAN_MISFIRE-gas_o2-gas_nox-mxmx | LEAN_MISFIRE | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 201 | TH-CMB-RICH_MISFIRE-gas_hc-gas_co-mnmn | RICH_MISFIRE | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 202 | TH-CMB-RICH_MISFIRE-gas_hc-gas_co-mnmx | RICH_MISFIRE | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 203 | TH-CMB-RICH_MISFIRE-gas_hc-gas_co-mxmn | RICH_MISFIRE | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 204 | TH-CMB-RICH_MISFIRE-gas_hc-gas_co-mxmx | RICH_MISFIRE | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 205 | TH-CMB-RICH_MISFIRE-gas_hc-gas_co2-mnmn | RICH_MISFIRE | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 206 | TH-CMB-RICH_MISFIRE-gas_hc-gas_co2-mnmx | RICH_MISFIRE | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 207 | TH-CMB-RICH_MISFIRE-gas_hc-gas_co2-mxmn | RICH_MISFIRE | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 208 | TH-CMB-RICH_MISFIRE-gas_hc-gas_co2-mxmx | RICH_MISFIRE | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 209 | TH-CMB-RICH_MISFIRE-gas_hc-gas_o2-mnmn | RICH_MISFIRE | (gas_hc, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 210 | TH-CMB-RICH_MISFIRE-gas_hc-gas_o2-mnmx | RICH_MISFIRE | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 211 | TH-CMB-RICH_MISFIRE-gas_hc-gas_o2-mxmn | RICH_MISFIRE | (gas_hc, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 212 | TH-CMB-RICH_MISFIRE-gas_hc-gas_o2-mxmx | RICH_MISFIRE | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 213 | TH-CMB-RICH_MISFIRE-gas_hc-gas_nox-mnmn | RICH_MISFIRE | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 214 | TH-CMB-RICH_MISFIRE-gas_hc-gas_nox-mnmx | RICH_MISFIRE | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 215 | TH-CMB-RICH_MISFIRE-gas_hc-gas_nox-mxmn | RICH_MISFIRE | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 216 | TH-CMB-RICH_MISFIRE-gas_hc-gas_nox-mxmx | RICH_MISFIRE | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 217 | TH-CMB-RICH_MISFIRE-gas_co-gas_co2-mnmn | RICH_MISFIRE | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 218 | TH-CMB-RICH_MISFIRE-gas_co-gas_co2-mnmx | RICH_MISFIRE | (gas_co, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 219 | TH-CMB-RICH_MISFIRE-gas_co-gas_co2-mxmn | RICH_MISFIRE | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 220 | TH-CMB-RICH_MISFIRE-gas_co-gas_co2-mxmx | RICH_MISFIRE | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 221 | TH-CMB-RICH_MISFIRE-gas_co-gas_o2-mnmn | RICH_MISFIRE | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 222 | TH-CMB-RICH_MISFIRE-gas_co-gas_o2-mnmx | RICH_MISFIRE | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 223 | TH-CMB-RICH_MISFIRE-gas_co-gas_o2-mxmn | RICH_MISFIRE | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 224 | TH-CMB-RICH_MISFIRE-gas_co-gas_o2-mxmx | RICH_MISFIRE | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 225 | TH-CMB-RICH_MISFIRE-gas_co-gas_nox-mnmn | RICH_MISFIRE | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 226 | TH-CMB-RICH_MISFIRE-gas_co-gas_nox-mnmx | RICH_MISFIRE | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 227 | TH-CMB-RICH_MISFIRE-gas_co-gas_nox-mxmn | RICH_MISFIRE | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 228 | TH-CMB-RICH_MISFIRE-gas_co-gas_nox-mxmx | RICH_MISFIRE | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 229 | TH-CMB-RICH_MISFIRE-gas_co2-gas_o2-mnmn | RICH_MISFIRE | (gas_co2, gas_o2) | (mn, mn) | inside | NORMAL_OPERATION | FAIL |
| 230 | TH-CMB-RICH_MISFIRE-gas_co2-gas_o2-mnmx | RICH_MISFIRE | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 231 | TH-CMB-RICH_MISFIRE-gas_co2-gas_o2-mxmn | RICH_MISFIRE | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 232 | TH-CMB-RICH_MISFIRE-gas_co2-gas_o2-mxmx | RICH_MISFIRE | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 233 | TH-CMB-RICH_MISFIRE-gas_co2-gas_nox-mnmn | RICH_MISFIRE | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 234 | TH-CMB-RICH_MISFIRE-gas_co2-gas_nox-mnmx | RICH_MISFIRE | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 235 | TH-CMB-RICH_MISFIRE-gas_co2-gas_nox-mxmn | RICH_MISFIRE | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 236 | TH-CMB-RICH_MISFIRE-gas_co2-gas_nox-mxmx | RICH_MISFIRE | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 237 | TH-CMB-RICH_MISFIRE-gas_o2-gas_nox-mnmn | RICH_MISFIRE | (gas_o2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 238 | TH-CMB-RICH_MISFIRE-gas_o2-gas_nox-mnmx | RICH_MISFIRE | (gas_o2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 239 | TH-CMB-RICH_MISFIRE-gas_o2-gas_nox-mxmn | RICH_MISFIRE | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 240 | TH-CMB-RICH_MISFIRE-gas_o2-gas_nox-mxmx | RICH_MISFIRE | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 241 | TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_co-mnmn | EXHAUST_AIR_LEAK | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 242 | TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_co-mnmx | EXHAUST_AIR_LEAK | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 243 | TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_co-mxmn | EXHAUST_AIR_LEAK | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 244 | TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_co-mxmx | EXHAUST_AIR_LEAK | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 245 | TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_co2-mnmn | EXHAUST_AIR_LEAK | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 246 | TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_co2-mnmx | EXHAUST_AIR_LEAK | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 247 | TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_co2-mxmn | EXHAUST_AIR_LEAK | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 248 | TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_co2-mxmx | EXHAUST_AIR_LEAK | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 249 | TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_o2-mnmn | EXHAUST_AIR_LEAK | (gas_hc, gas_o2) | (mn, mn) | inside | VVT_FAILURE | FAIL |
| 250 | TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_o2-mnmx | EXHAUST_AIR_LEAK | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 251 | TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_o2-mxmn | EXHAUST_AIR_LEAK | (gas_hc, gas_o2) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 252 | TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_o2-mxmx | EXHAUST_AIR_LEAK | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 253 | TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_nox-mnmn | EXHAUST_AIR_LEAK | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 254 | TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_nox-mnmx | EXHAUST_AIR_LEAK | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 255 | TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_nox-mxmn | EXHAUST_AIR_LEAK | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 256 | TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_nox-mxmx | EXHAUST_AIR_LEAK | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 257 | TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_co2-mnmn | EXHAUST_AIR_LEAK | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 258 | TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_co2-mnmx | EXHAUST_AIR_LEAK | (gas_co, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 259 | TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_co2-mxmn | EXHAUST_AIR_LEAK | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 260 | TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_co2-mxmx | EXHAUST_AIR_LEAK | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 261 | TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_o2-mnmn | EXHAUST_AIR_LEAK | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 262 | TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_o2-mnmx | EXHAUST_AIR_LEAK | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 263 | TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_o2-mxmn | EXHAUST_AIR_LEAK | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 264 | TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_o2-mxmx | EXHAUST_AIR_LEAK | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 265 | TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_nox-mnmn | EXHAUST_AIR_LEAK | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 266 | TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_nox-mnmx | EXHAUST_AIR_LEAK | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 267 | TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_nox-mxmn | EXHAUST_AIR_LEAK | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 268 | TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_nox-mxmx | EXHAUST_AIR_LEAK | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 269 | TH-CMB-EXHAUST_AIR_LEAK-gas_co2-gas_o2-mnmn | EXHAUST_AIR_LEAK | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 270 | TH-CMB-EXHAUST_AIR_LEAK-gas_co2-gas_o2-mnmx | EXHAUST_AIR_LEAK | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 271 | TH-CMB-EXHAUST_AIR_LEAK-gas_co2-gas_o2-mxmn | EXHAUST_AIR_LEAK | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 272 | TH-CMB-EXHAUST_AIR_LEAK-gas_co2-gas_o2-mxmx | EXHAUST_AIR_LEAK | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 273 | TH-CMB-EXHAUST_AIR_LEAK-gas_co2-gas_nox-mnmn | EXHAUST_AIR_LEAK | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 274 | TH-CMB-EXHAUST_AIR_LEAK-gas_co2-gas_nox-mnmx | EXHAUST_AIR_LEAK | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 275 | TH-CMB-EXHAUST_AIR_LEAK-gas_co2-gas_nox-mxmn | EXHAUST_AIR_LEAK | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 276 | TH-CMB-EXHAUST_AIR_LEAK-gas_co2-gas_nox-mxmx | EXHAUST_AIR_LEAK | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 277 | TH-CMB-EXHAUST_AIR_LEAK-gas_o2-gas_nox-mnmn | EXHAUST_AIR_LEAK | (gas_o2, gas_nox) | (mn, mn) | inside | NORMAL_OPERATION | FAIL |
| 278 | TH-CMB-EXHAUST_AIR_LEAK-gas_o2-gas_nox-mnmx | EXHAUST_AIR_LEAK | (gas_o2, gas_nox) | (mn, mx) | inside | NORMAL_OPERATION | FAIL |
| 279 | TH-CMB-EXHAUST_AIR_LEAK-gas_o2-gas_nox-mxmn | EXHAUST_AIR_LEAK | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 280 | TH-CMB-EXHAUST_AIR_LEAK-gas_o2-gas_nox-mxmx | EXHAUST_AIR_LEAK | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 281 | TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_co-mnmn | HIGH_COMBUSTION_TEMP | (gas_hc, gas_co) | (mn, mn) | inside | TIMING_OVER_ADVANCED | FAIL |
| 282 | TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_co-mnmx | HIGH_COMBUSTION_TEMP | (gas_hc, gas_co) | (mn, mx) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 283 | TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_co-mxmn | HIGH_COMBUSTION_TEMP | (gas_hc, gas_co) | (mx, mn) | inside | TIMING_OVER_ADVANCED | FAIL |
| 284 | TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_co-mxmx | HIGH_COMBUSTION_TEMP | (gas_hc, gas_co) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 285 | TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_co2-mnmn | HIGH_COMBUSTION_TEMP | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 286 | TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_co2-mnmx | HIGH_COMBUSTION_TEMP | (gas_hc, gas_co2) | (mn, mx) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 287 | TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_co2-mxmn | HIGH_COMBUSTION_TEMP | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 288 | TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_co2-mxmx | HIGH_COMBUSTION_TEMP | (gas_hc, gas_co2) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 289 | TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_o2-mnmn | HIGH_COMBUSTION_TEMP | (gas_hc, gas_o2) | (mn, mn) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 290 | TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_o2-mnmx | HIGH_COMBUSTION_TEMP | (gas_hc, gas_o2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 291 | TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_o2-mxmn | HIGH_COMBUSTION_TEMP | (gas_hc, gas_o2) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 292 | TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_o2-mxmx | HIGH_COMBUSTION_TEMP | (gas_hc, gas_o2) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 293 | TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_nox-mnmn | HIGH_COMBUSTION_TEMP | (gas_hc, gas_nox) | (mn, mn) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 294 | TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_nox-mnmx | HIGH_COMBUSTION_TEMP | (gas_hc, gas_nox) | (mn, mx) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 295 | TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_nox-mxmn | HIGH_COMBUSTION_TEMP | (gas_hc, gas_nox) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 296 | TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_nox-mxmx | HIGH_COMBUSTION_TEMP | (gas_hc, gas_nox) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 297 | TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_co2-mnmn | HIGH_COMBUSTION_TEMP | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 298 | TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_co2-mnmx | HIGH_COMBUSTION_TEMP | (gas_co, gas_co2) | (mn, mx) | inside | TIMING_OVER_ADVANCED | FAIL |
| 299 | TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_co2-mxmn | HIGH_COMBUSTION_TEMP | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 300 | TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_co2-mxmx | HIGH_COMBUSTION_TEMP | (gas_co, gas_co2) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 301 | TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_o2-mnmn | HIGH_COMBUSTION_TEMP | (gas_co, gas_o2) | (mn, mn) | inside | TIMING_OVER_ADVANCED | FAIL |
| 302 | TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_o2-mnmx | HIGH_COMBUSTION_TEMP | (gas_co, gas_o2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 303 | TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_o2-mxmn | HIGH_COMBUSTION_TEMP | (gas_co, gas_o2) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 304 | TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_o2-mxmx | HIGH_COMBUSTION_TEMP | (gas_co, gas_o2) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 305 | TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_nox-mnmn | HIGH_COMBUSTION_TEMP | (gas_co, gas_nox) | (mn, mn) | inside | TIMING_OVER_ADVANCED | FAIL |
| 306 | TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_nox-mnmx | HIGH_COMBUSTION_TEMP | (gas_co, gas_nox) | (mn, mx) | inside | TIMING_OVER_ADVANCED | FAIL |
| 307 | TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_nox-mxmn | HIGH_COMBUSTION_TEMP | (gas_co, gas_nox) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 308 | TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_nox-mxmx | HIGH_COMBUSTION_TEMP | (gas_co, gas_nox) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 309 | TH-CMB-HIGH_COMBUSTION_TE-gas_co2-gas_o2-mnmn | HIGH_COMBUSTION_TEMP | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 310 | TH-CMB-HIGH_COMBUSTION_TE-gas_co2-gas_o2-mnmx | HIGH_COMBUSTION_TEMP | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 311 | TH-CMB-HIGH_COMBUSTION_TE-gas_co2-gas_o2-mxmn | HIGH_COMBUSTION_TEMP | (gas_co2, gas_o2) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 312 | TH-CMB-HIGH_COMBUSTION_TE-gas_co2-gas_o2-mxmx | HIGH_COMBUSTION_TEMP | (gas_co2, gas_o2) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 313 | TH-CMB-HIGH_COMBUSTION_TE-gas_co2-gas_nox-mnmn | HIGH_COMBUSTION_TEMP | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 314 | TH-CMB-HIGH_COMBUSTION_TE-gas_co2-gas_nox-mnmx | HIGH_COMBUSTION_TEMP | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 315 | TH-CMB-HIGH_COMBUSTION_TE-gas_co2-gas_nox-mxmn | HIGH_COMBUSTION_TEMP | (gas_co2, gas_nox) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 316 | TH-CMB-HIGH_COMBUSTION_TE-gas_co2-gas_nox-mxmx | HIGH_COMBUSTION_TEMP | (gas_co2, gas_nox) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 317 | TH-CMB-HIGH_COMBUSTION_TE-gas_o2-gas_nox-mnmn | HIGH_COMBUSTION_TEMP | (gas_o2, gas_nox) | (mn, mn) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 318 | TH-CMB-HIGH_COMBUSTION_TE-gas_o2-gas_nox-mnmx | HIGH_COMBUSTION_TEMP | (gas_o2, gas_nox) | (mn, mx) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 319 | TH-CMB-HIGH_COMBUSTION_TE-gas_o2-gas_nox-mxmn | HIGH_COMBUSTION_TEMP | (gas_o2, gas_nox) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | PASS |
| 320 | TH-CMB-HIGH_COMBUSTION_TE-gas_o2-gas_nox-mxmx | HIGH_COMBUSTION_TEMP | (gas_o2, gas_nox) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 321 | TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_co-mnmn | CATALYST_NOT_LIGHTING_OFF | (gas_hc, gas_co) | (mn, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 322 | TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_co-mnmx | CATALYST_NOT_LIGHTING_OFF | (gas_hc, gas_co) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 323 | TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_co-mxmn | CATALYST_NOT_LIGHTING_OFF | (gas_hc, gas_co) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 324 | TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_co-mxmx | CATALYST_NOT_LIGHTING_OFF | (gas_hc, gas_co) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 325 | TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_co2-mnmn | CATALYST_NOT_LIGHTING_OFF | (gas_hc, gas_co2) | (mn, mn) | inside | VVT_FAILURE | FAIL |
| 326 | TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_co2-mnmx | CATALYST_NOT_LIGHTING_OFF | (gas_hc, gas_co2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 327 | TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_co2-mxmn | CATALYST_NOT_LIGHTING_OFF | (gas_hc, gas_co2) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 328 | TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_co2-mxmx | CATALYST_NOT_LIGHTING_OFF | (gas_hc, gas_co2) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 329 | TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_o2-mnmn | CATALYST_NOT_LIGHTING_OFF | (gas_hc, gas_o2) | (mn, mn) | inside | VVT_FAILURE | FAIL |
| 330 | TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_o2-mnmx | CATALYST_NOT_LIGHTING_OFF | (gas_hc, gas_o2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 331 | TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_o2-mxmn | CATALYST_NOT_LIGHTING_OFF | (gas_hc, gas_o2) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 332 | TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_o2-mxmx | CATALYST_NOT_LIGHTING_OFF | (gas_hc, gas_o2) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 333 | TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_nox-mnmn | CATALYST_NOT_LIGHTING_OFF | (gas_hc, gas_nox) | (mn, mn) | inside | CATALYST_NOT_LIGHTING_OFF | PASS |
| 334 | TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_nox-mnmx | CATALYST_NOT_LIGHTING_OFF | (gas_hc, gas_nox) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 335 | TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_nox-mxmn | CATALYST_NOT_LIGHTING_OFF | (gas_hc, gas_nox) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 336 | TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_nox-mxmx | CATALYST_NOT_LIGHTING_OFF | (gas_hc, gas_nox) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 337 | TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_co2-mnmn | CATALYST_NOT_LIGHTING_OFF | (gas_co, gas_co2) | (mn, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 338 | TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_co2-mnmx | CATALYST_NOT_LIGHTING_OFF | (gas_co, gas_co2) | (mn, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 339 | TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_co2-mxmn | CATALYST_NOT_LIGHTING_OFF | (gas_co, gas_co2) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 340 | TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_co2-mxmx | CATALYST_NOT_LIGHTING_OFF | (gas_co, gas_co2) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 341 | TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_o2-mnmn | CATALYST_NOT_LIGHTING_OFF | (gas_co, gas_o2) | (mn, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 342 | TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_o2-mnmx | CATALYST_NOT_LIGHTING_OFF | (gas_co, gas_o2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 343 | TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_o2-mxmn | CATALYST_NOT_LIGHTING_OFF | (gas_co, gas_o2) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 344 | TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_o2-mxmx | CATALYST_NOT_LIGHTING_OFF | (gas_co, gas_o2) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 345 | TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_nox-mnmn | CATALYST_NOT_LIGHTING_OFF | (gas_co, gas_nox) | (mn, mn) | inside | CATALYST_NOT_LIGHTING_OFF | PASS |
| 346 | TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_nox-mnmx | CATALYST_NOT_LIGHTING_OFF | (gas_co, gas_nox) | (mn, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 347 | TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_nox-mxmn | CATALYST_NOT_LIGHTING_OFF | (gas_co, gas_nox) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 348 | TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_nox-mxmx | CATALYST_NOT_LIGHTING_OFF | (gas_co, gas_nox) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 349 | TH-CMB-CATALYST_NOT_LIGHT-gas_co2-gas_o2-mnmn | CATALYST_NOT_LIGHTING_OFF | (gas_co2, gas_o2) | (mn, mn) | inside | VVT_FAILURE | FAIL |
| 350 | TH-CMB-CATALYST_NOT_LIGHT-gas_co2-gas_o2-mnmx | CATALYST_NOT_LIGHTING_OFF | (gas_co2, gas_o2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 351 | TH-CMB-CATALYST_NOT_LIGHT-gas_co2-gas_o2-mxmn | CATALYST_NOT_LIGHTING_OFF | (gas_co2, gas_o2) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 352 | TH-CMB-CATALYST_NOT_LIGHT-gas_co2-gas_o2-mxmx | CATALYST_NOT_LIGHTING_OFF | (gas_co2, gas_o2) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 353 | TH-CMB-CATALYST_NOT_LIGHT-gas_co2-gas_nox-mnmn | CATALYST_NOT_LIGHTING_OFF | (gas_co2, gas_nox) | (mn, mn) | inside | VVT_FAILURE | FAIL |
| 354 | TH-CMB-CATALYST_NOT_LIGHT-gas_co2-gas_nox-mnmx | CATALYST_NOT_LIGHTING_OFF | (gas_co2, gas_nox) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 355 | TH-CMB-CATALYST_NOT_LIGHT-gas_co2-gas_nox-mxmn | CATALYST_NOT_LIGHTING_OFF | (gas_co2, gas_nox) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 356 | TH-CMB-CATALYST_NOT_LIGHT-gas_co2-gas_nox-mxmx | CATALYST_NOT_LIGHTING_OFF | (gas_co2, gas_nox) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 357 | TH-CMB-CATALYST_NOT_LIGHT-gas_o2-gas_nox-mnmn | CATALYST_NOT_LIGHTING_OFF | (gas_o2, gas_nox) | (mn, mn) | inside | O2_SENSOR_BIASED_LOW | FAIL |
| 358 | TH-CMB-CATALYST_NOT_LIGHT-gas_o2-gas_nox-mnmx | CATALYST_NOT_LIGHTING_OFF | (gas_o2, gas_nox) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 359 | TH-CMB-CATALYST_NOT_LIGHT-gas_o2-gas_nox-mxmn | CATALYST_NOT_LIGHTING_OFF | (gas_o2, gas_nox) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 360 | TH-CMB-CATALYST_NOT_LIGHT-gas_o2-gas_nox-mxmx | CATALYST_NOT_LIGHTING_OFF | (gas_o2, gas_nox) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 361 | TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_co-mnmn | CATALYST_OVERWHELMED | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 362 | TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_co-mnmx | CATALYST_OVERWHELMED | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 363 | TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_co-mxmn | CATALYST_OVERWHELMED | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 364 | TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_co-mxmx | CATALYST_OVERWHELMED | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 365 | TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_co2-mnmn | CATALYST_OVERWHELMED | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 366 | TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_co2-mnmx | CATALYST_OVERWHELMED | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 367 | TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_co2-mxmn | CATALYST_OVERWHELMED | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 368 | TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_co2-mxmx | CATALYST_OVERWHELMED | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 369 | TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_o2-mnmn | CATALYST_OVERWHELMED | (gas_hc, gas_o2) | (mn, mn) | inside | CATALYST_OVERWHELMED | PASS |
| 370 | TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_o2-mnmx | CATALYST_OVERWHELMED | (gas_hc, gas_o2) | (mn, mx) | inside | CATALYST_OVERWHELMED | PASS |
| 371 | TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_o2-mxmn | CATALYST_OVERWHELMED | (gas_hc, gas_o2) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 372 | TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_o2-mxmx | CATALYST_OVERWHELMED | (gas_hc, gas_o2) | (mx, mx) | inside | NORMAL_OPERATION | FAIL |
| 373 | TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_nox-mnmn | CATALYST_OVERWHELMED | (gas_hc, gas_nox) | (mn, mn) | inside | CATALYST_OVERWHELMED | PASS |
| 374 | TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_nox-mnmx | CATALYST_OVERWHELMED | (gas_hc, gas_nox) | (mn, mx) | inside | CATALYST_OVERWHELMED | PASS |
| 375 | TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_nox-mxmn | CATALYST_OVERWHELMED | (gas_hc, gas_nox) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 376 | TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_nox-mxmx | CATALYST_OVERWHELMED | (gas_hc, gas_nox) | (mx, mx) | inside | NORMAL_OPERATION | FAIL |
| 377 | TH-CMB-CATALYST_OVERWHELM-gas_co-gas_co2-mnmn | CATALYST_OVERWHELMED | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 378 | TH-CMB-CATALYST_OVERWHELM-gas_co-gas_co2-mnmx | CATALYST_OVERWHELMED | (gas_co, gas_co2) | (mn, mx) | inside | NORMAL_OPERATION | FAIL |
| 379 | TH-CMB-CATALYST_OVERWHELM-gas_co-gas_co2-mxmn | CATALYST_OVERWHELMED | (gas_co, gas_co2) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 380 | TH-CMB-CATALYST_OVERWHELM-gas_co-gas_co2-mxmx | CATALYST_OVERWHELMED | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 381 | TH-CMB-CATALYST_OVERWHELM-gas_co-gas_o2-mnmn | CATALYST_OVERWHELMED | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 382 | TH-CMB-CATALYST_OVERWHELM-gas_co-gas_o2-mnmx | CATALYST_OVERWHELMED | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 383 | TH-CMB-CATALYST_OVERWHELM-gas_co-gas_o2-mxmn | CATALYST_OVERWHELMED | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 384 | TH-CMB-CATALYST_OVERWHELM-gas_co-gas_o2-mxmx | CATALYST_OVERWHELMED | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 385 | TH-CMB-CATALYST_OVERWHELM-gas_co-gas_nox-mnmn | CATALYST_OVERWHELMED | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 386 | TH-CMB-CATALYST_OVERWHELM-gas_co-gas_nox-mnmx | CATALYST_OVERWHELMED | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 387 | TH-CMB-CATALYST_OVERWHELM-gas_co-gas_nox-mxmn | CATALYST_OVERWHELMED | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 388 | TH-CMB-CATALYST_OVERWHELM-gas_co-gas_nox-mxmx | CATALYST_OVERWHELMED | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 389 | TH-CMB-CATALYST_OVERWHELM-gas_co2-gas_o2-mnmn | CATALYST_OVERWHELMED | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 390 | TH-CMB-CATALYST_OVERWHELM-gas_co2-gas_o2-mnmx | CATALYST_OVERWHELMED | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 391 | TH-CMB-CATALYST_OVERWHELM-gas_co2-gas_o2-mxmn | CATALYST_OVERWHELMED | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 392 | TH-CMB-CATALYST_OVERWHELM-gas_co2-gas_o2-mxmx | CATALYST_OVERWHELMED | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 393 | TH-CMB-CATALYST_OVERWHELM-gas_co2-gas_nox-mnmn | CATALYST_OVERWHELMED | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 394 | TH-CMB-CATALYST_OVERWHELM-gas_co2-gas_nox-mnmx | CATALYST_OVERWHELMED | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 395 | TH-CMB-CATALYST_OVERWHELM-gas_co2-gas_nox-mxmn | CATALYST_OVERWHELMED | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 396 | TH-CMB-CATALYST_OVERWHELM-gas_co2-gas_nox-mxmx | CATALYST_OVERWHELMED | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 397 | TH-CMB-CATALYST_OVERWHELM-gas_o2-gas_nox-mnmn | CATALYST_OVERWHELMED | (gas_o2, gas_nox) | (mn, mn) | inside | NORMAL_OPERATION | FAIL |
| 398 | TH-CMB-CATALYST_OVERWHELM-gas_o2-gas_nox-mnmx | CATALYST_OVERWHELMED | (gas_o2, gas_nox) | (mn, mx) | inside | NORMAL_OPERATION | FAIL |
| 399 | TH-CMB-CATALYST_OVERWHELM-gas_o2-gas_nox-mxmn | CATALYST_OVERWHELMED | (gas_o2, gas_nox) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 400 | TH-CMB-CATALYST_OVERWHELM-gas_o2-gas_nox-mxmx | CATALYST_OVERWHELMED | (gas_o2, gas_nox) | (mx, mx) | inside | NORMAL_OPERATION | FAIL |
| 401 | TH-CMB-SAMPLE_INVALID-gas_hc-gas_co-mnmn | SAMPLE_INVALID | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | PASS |
| 402 | TH-CMB-SAMPLE_INVALID-gas_hc-gas_co-mnmx | SAMPLE_INVALID | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | PASS |
| 403 | TH-CMB-SAMPLE_INVALID-gas_hc-gas_co-mxmn | SAMPLE_INVALID | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | PASS |
| 404 | TH-CMB-SAMPLE_INVALID-gas_hc-gas_co-mxmx | SAMPLE_INVALID | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | PASS |
| 405 | TH-CMB-SAMPLE_INVALID-gas_hc-gas_co2-mnmn | SAMPLE_INVALID | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | PASS |
| 406 | TH-CMB-SAMPLE_INVALID-gas_hc-gas_co2-mnmx | SAMPLE_INVALID | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | PASS |
| 407 | TH-CMB-SAMPLE_INVALID-gas_hc-gas_co2-mxmn | SAMPLE_INVALID | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | PASS |
| 408 | TH-CMB-SAMPLE_INVALID-gas_hc-gas_co2-mxmx | SAMPLE_INVALID | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | PASS |
| 409 | TH-CMB-SAMPLE_INVALID-gas_hc-gas_o2-mnmn | SAMPLE_INVALID | (gas_hc, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | PASS |
| 410 | TH-CMB-SAMPLE_INVALID-gas_hc-gas_o2-mnmx | SAMPLE_INVALID | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | PASS |
| 411 | TH-CMB-SAMPLE_INVALID-gas_hc-gas_o2-mxmn | SAMPLE_INVALID | (gas_hc, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | PASS |
| 412 | TH-CMB-SAMPLE_INVALID-gas_hc-gas_o2-mxmx | SAMPLE_INVALID | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | PASS |
| 413 | TH-CMB-SAMPLE_INVALID-gas_hc-gas_nox-mnmn | SAMPLE_INVALID | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | PASS |
| 414 | TH-CMB-SAMPLE_INVALID-gas_hc-gas_nox-mnmx | SAMPLE_INVALID | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | PASS |
| 415 | TH-CMB-SAMPLE_INVALID-gas_hc-gas_nox-mxmn | SAMPLE_INVALID | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | PASS |
| 416 | TH-CMB-SAMPLE_INVALID-gas_hc-gas_nox-mxmx | SAMPLE_INVALID | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | PASS |
| 417 | TH-CMB-SAMPLE_INVALID-gas_co-gas_co2-mnmn | SAMPLE_INVALID | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | PASS |
| 418 | TH-CMB-SAMPLE_INVALID-gas_co-gas_co2-mnmx | SAMPLE_INVALID | (gas_co, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | PASS |
| 419 | TH-CMB-SAMPLE_INVALID-gas_co-gas_co2-mxmn | SAMPLE_INVALID | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | PASS |
| 420 | TH-CMB-SAMPLE_INVALID-gas_co-gas_co2-mxmx | SAMPLE_INVALID | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | PASS |
| 421 | TH-CMB-SAMPLE_INVALID-gas_co-gas_o2-mnmn | SAMPLE_INVALID | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | PASS |
| 422 | TH-CMB-SAMPLE_INVALID-gas_co-gas_o2-mnmx | SAMPLE_INVALID | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | PASS |
| 423 | TH-CMB-SAMPLE_INVALID-gas_co-gas_o2-mxmn | SAMPLE_INVALID | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | PASS |
| 424 | TH-CMB-SAMPLE_INVALID-gas_co-gas_o2-mxmx | SAMPLE_INVALID | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | PASS |
| 425 | TH-CMB-SAMPLE_INVALID-gas_co-gas_nox-mnmn | SAMPLE_INVALID | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | PASS |
| 426 | TH-CMB-SAMPLE_INVALID-gas_co-gas_nox-mnmx | SAMPLE_INVALID | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | PASS |
| 427 | TH-CMB-SAMPLE_INVALID-gas_co-gas_nox-mxmn | SAMPLE_INVALID | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | PASS |
| 428 | TH-CMB-SAMPLE_INVALID-gas_co-gas_nox-mxmx | SAMPLE_INVALID | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | PASS |
| 429 | TH-CMB-SAMPLE_INVALID-gas_co2-gas_o2-mnmn | SAMPLE_INVALID | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | PASS |
| 430 | TH-CMB-SAMPLE_INVALID-gas_co2-gas_o2-mnmx | SAMPLE_INVALID | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | PASS |
| 431 | TH-CMB-SAMPLE_INVALID-gas_co2-gas_o2-mxmn | SAMPLE_INVALID | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | PASS |
| 432 | TH-CMB-SAMPLE_INVALID-gas_co2-gas_o2-mxmx | SAMPLE_INVALID | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | PASS |
| 433 | TH-CMB-SAMPLE_INVALID-gas_co2-gas_nox-mnmn | SAMPLE_INVALID | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | PASS |
| 434 | TH-CMB-SAMPLE_INVALID-gas_co2-gas_nox-mnmx | SAMPLE_INVALID | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | PASS |
| 435 | TH-CMB-SAMPLE_INVALID-gas_co2-gas_nox-mxmn | SAMPLE_INVALID | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | PASS |
| 436 | TH-CMB-SAMPLE_INVALID-gas_co2-gas_nox-mxmx | SAMPLE_INVALID | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | PASS |
| 437 | TH-CMB-SAMPLE_INVALID-gas_o2-gas_nox-mnmn | SAMPLE_INVALID | (gas_o2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | PASS |
| 438 | TH-CMB-SAMPLE_INVALID-gas_o2-gas_nox-mnmx | SAMPLE_INVALID | (gas_o2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | PASS |
| 439 | TH-CMB-SAMPLE_INVALID-gas_o2-gas_nox-mxmn | SAMPLE_INVALID | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | PASS |
| 440 | TH-CMB-SAMPLE_INVALID-gas_o2-gas_nox-mxmx | SAMPLE_INVALID | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | PASS |
| 441 | TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_co-mnmn | TIMING_OVER_ADVANCED | (gas_hc, gas_co) | (mn, mn) | inside | TIMING_OVER_ADVANCED | PASS |
| 442 | TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_co-mnmx | TIMING_OVER_ADVANCED | (gas_hc, gas_co) | (mn, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 443 | TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_co-mxmn | TIMING_OVER_ADVANCED | (gas_hc, gas_co) | (mx, mn) | inside | TIMING_OVER_ADVANCED | PASS |
| 444 | TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_co-mxmx | TIMING_OVER_ADVANCED | (gas_hc, gas_co) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 445 | TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_co2-mnmn | TIMING_OVER_ADVANCED | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 446 | TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_co2-mnmx | TIMING_OVER_ADVANCED | (gas_hc, gas_co2) | (mn, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 447 | TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_co2-mxmn | TIMING_OVER_ADVANCED | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 448 | TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_co2-mxmx | TIMING_OVER_ADVANCED | (gas_hc, gas_co2) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 449 | TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_o2-mnmn | TIMING_OVER_ADVANCED | (gas_hc, gas_o2) | (mn, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 450 | TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_o2-mnmx | TIMING_OVER_ADVANCED | (gas_hc, gas_o2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 451 | TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_o2-mxmn | TIMING_OVER_ADVANCED | (gas_hc, gas_o2) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 452 | TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_o2-mxmx | TIMING_OVER_ADVANCED | (gas_hc, gas_o2) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 453 | TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_nox-mnmn | TIMING_OVER_ADVANCED | (gas_hc, gas_nox) | (mn, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 454 | TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_nox-mnmx | TIMING_OVER_ADVANCED | (gas_hc, gas_nox) | (mn, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 455 | TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_nox-mxmn | TIMING_OVER_ADVANCED | (gas_hc, gas_nox) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 456 | TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_nox-mxmx | TIMING_OVER_ADVANCED | (gas_hc, gas_nox) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 457 | TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_co2-mnmn | TIMING_OVER_ADVANCED | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 458 | TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_co2-mnmx | TIMING_OVER_ADVANCED | (gas_co, gas_co2) | (mn, mx) | inside | TIMING_OVER_ADVANCED | PASS |
| 459 | TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_co2-mxmn | TIMING_OVER_ADVANCED | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 460 | TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_co2-mxmx | TIMING_OVER_ADVANCED | (gas_co, gas_co2) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 461 | TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_o2-mnmn | TIMING_OVER_ADVANCED | (gas_co, gas_o2) | (mn, mn) | inside | TIMING_OVER_ADVANCED | PASS |
| 462 | TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_o2-mnmx | TIMING_OVER_ADVANCED | (gas_co, gas_o2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 463 | TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_o2-mxmn | TIMING_OVER_ADVANCED | (gas_co, gas_o2) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 464 | TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_o2-mxmx | TIMING_OVER_ADVANCED | (gas_co, gas_o2) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 465 | TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_nox-mnmn | TIMING_OVER_ADVANCED | (gas_co, gas_nox) | (mn, mn) | inside | TIMING_OVER_ADVANCED | PASS |
| 466 | TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_nox-mnmx | TIMING_OVER_ADVANCED | (gas_co, gas_nox) | (mn, mx) | inside | TIMING_OVER_ADVANCED | PASS |
| 467 | TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_nox-mxmn | TIMING_OVER_ADVANCED | (gas_co, gas_nox) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 468 | TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_nox-mxmx | TIMING_OVER_ADVANCED | (gas_co, gas_nox) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 469 | TH-CMB-TIMING_OVER_ADVANC-gas_co2-gas_o2-mnmn | TIMING_OVER_ADVANCED | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 470 | TH-CMB-TIMING_OVER_ADVANC-gas_co2-gas_o2-mnmx | TIMING_OVER_ADVANCED | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 471 | TH-CMB-TIMING_OVER_ADVANC-gas_co2-gas_o2-mxmn | TIMING_OVER_ADVANCED | (gas_co2, gas_o2) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 472 | TH-CMB-TIMING_OVER_ADVANC-gas_co2-gas_o2-mxmx | TIMING_OVER_ADVANCED | (gas_co2, gas_o2) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 473 | TH-CMB-TIMING_OVER_ADVANC-gas_co2-gas_nox-mnmn | TIMING_OVER_ADVANCED | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 474 | TH-CMB-TIMING_OVER_ADVANC-gas_co2-gas_nox-mnmx | TIMING_OVER_ADVANCED | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 475 | TH-CMB-TIMING_OVER_ADVANC-gas_co2-gas_nox-mxmn | TIMING_OVER_ADVANCED | (gas_co2, gas_nox) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 476 | TH-CMB-TIMING_OVER_ADVANC-gas_co2-gas_nox-mxmx | TIMING_OVER_ADVANCED | (gas_co2, gas_nox) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 477 | TH-CMB-TIMING_OVER_ADVANC-gas_o2-gas_nox-mnmn | TIMING_OVER_ADVANCED | (gas_o2, gas_nox) | (mn, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 478 | TH-CMB-TIMING_OVER_ADVANC-gas_o2-gas_nox-mnmx | TIMING_OVER_ADVANCED | (gas_o2, gas_nox) | (mn, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 479 | TH-CMB-TIMING_OVER_ADVANC-gas_o2-gas_nox-mxmn | TIMING_OVER_ADVANCED | (gas_o2, gas_nox) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 480 | TH-CMB-TIMING_OVER_ADVANC-gas_o2-gas_nox-mxmx | TIMING_OVER_ADVANCED | (gas_o2, gas_nox) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 481 | TH-CMB-TIMING_RETARDED-gas_hc-gas_co-mnmn | TIMING_RETARDED | (gas_hc, gas_co) | (mn, mn) | inside | TIMING_RETARDED | PASS |
| 482 | TH-CMB-TIMING_RETARDED-gas_hc-gas_co-mnmx | TIMING_RETARDED | (gas_hc, gas_co) | (mn, mx) | inside | TIMING_RETARDED | PASS |
| 483 | TH-CMB-TIMING_RETARDED-gas_hc-gas_co-mxmn | TIMING_RETARDED | (gas_hc, gas_co) | (mx, mn) | inside | TIMING_RETARDED | PASS |
| 484 | TH-CMB-TIMING_RETARDED-gas_hc-gas_co-mxmx | TIMING_RETARDED | (gas_hc, gas_co) | (mx, mx) | inside | TIMING_RETARDED | PASS |
| 485 | TH-CMB-TIMING_RETARDED-gas_hc-gas_co2-mnmn | TIMING_RETARDED | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 486 | TH-CMB-TIMING_RETARDED-gas_hc-gas_co2-mnmx | TIMING_RETARDED | (gas_hc, gas_co2) | (mn, mx) | inside | TIMING_RETARDED | PASS |
| 487 | TH-CMB-TIMING_RETARDED-gas_hc-gas_co2-mxmn | TIMING_RETARDED | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 488 | TH-CMB-TIMING_RETARDED-gas_hc-gas_co2-mxmx | TIMING_RETARDED | (gas_hc, gas_co2) | (mx, mx) | inside | TIMING_RETARDED | PASS |
| 489 | TH-CMB-TIMING_RETARDED-gas_hc-gas_o2-mnmn | TIMING_RETARDED | (gas_hc, gas_o2) | (mn, mn) | inside | TIMING_RETARDED | PASS |
| 490 | TH-CMB-TIMING_RETARDED-gas_hc-gas_o2-mnmx | TIMING_RETARDED | (gas_hc, gas_o2) | (mn, mx) | inside | TIMING_RETARDED | PASS |
| 491 | TH-CMB-TIMING_RETARDED-gas_hc-gas_o2-mxmn | TIMING_RETARDED | (gas_hc, gas_o2) | (mx, mn) | inside | TIMING_RETARDED | PASS |
| 492 | TH-CMB-TIMING_RETARDED-gas_hc-gas_o2-mxmx | TIMING_RETARDED | (gas_hc, gas_o2) | (mx, mx) | inside | TIMING_RETARDED | PASS |
| 493 | TH-CMB-TIMING_RETARDED-gas_hc-gas_nox-mnmn | TIMING_RETARDED | (gas_hc, gas_nox) | (mn, mn) | inside | TIMING_RETARDED | PASS |
| 494 | TH-CMB-TIMING_RETARDED-gas_hc-gas_nox-mnmx | TIMING_RETARDED | (gas_hc, gas_nox) | (mn, mx) | inside | TIMING_RETARDED | PASS |
| 495 | TH-CMB-TIMING_RETARDED-gas_hc-gas_nox-mxmn | TIMING_RETARDED | (gas_hc, gas_nox) | (mx, mn) | inside | TIMING_RETARDED | PASS |
| 496 | TH-CMB-TIMING_RETARDED-gas_hc-gas_nox-mxmx | TIMING_RETARDED | (gas_hc, gas_nox) | (mx, mx) | inside | TIMING_RETARDED | PASS |
| 497 | TH-CMB-TIMING_RETARDED-gas_co-gas_co2-mnmn | TIMING_RETARDED | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 498 | TH-CMB-TIMING_RETARDED-gas_co-gas_co2-mnmx | TIMING_RETARDED | (gas_co, gas_co2) | (mn, mx) | inside | TIMING_RETARDED | PASS |
| 499 | TH-CMB-TIMING_RETARDED-gas_co-gas_co2-mxmn | TIMING_RETARDED | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 500 | TH-CMB-TIMING_RETARDED-gas_co-gas_co2-mxmx | TIMING_RETARDED | (gas_co, gas_co2) | (mx, mx) | inside | TIMING_RETARDED | PASS |
| 501 | TH-CMB-TIMING_RETARDED-gas_co-gas_o2-mnmn | TIMING_RETARDED | (gas_co, gas_o2) | (mn, mn) | inside | TIMING_RETARDED | PASS |
| 502 | TH-CMB-TIMING_RETARDED-gas_co-gas_o2-mnmx | TIMING_RETARDED | (gas_co, gas_o2) | (mn, mx) | inside | TIMING_RETARDED | PASS |
| 503 | TH-CMB-TIMING_RETARDED-gas_co-gas_o2-mxmn | TIMING_RETARDED | (gas_co, gas_o2) | (mx, mn) | inside | TIMING_RETARDED | PASS |
| 504 | TH-CMB-TIMING_RETARDED-gas_co-gas_o2-mxmx | TIMING_RETARDED | (gas_co, gas_o2) | (mx, mx) | inside | TIMING_RETARDED | PASS |
| 505 | TH-CMB-TIMING_RETARDED-gas_co-gas_nox-mnmn | TIMING_RETARDED | (gas_co, gas_nox) | (mn, mn) | inside | TIMING_RETARDED | PASS |
| 506 | TH-CMB-TIMING_RETARDED-gas_co-gas_nox-mnmx | TIMING_RETARDED | (gas_co, gas_nox) | (mn, mx) | inside | TIMING_RETARDED | PASS |
| 507 | TH-CMB-TIMING_RETARDED-gas_co-gas_nox-mxmn | TIMING_RETARDED | (gas_co, gas_nox) | (mx, mn) | inside | TIMING_RETARDED | PASS |
| 508 | TH-CMB-TIMING_RETARDED-gas_co-gas_nox-mxmx | TIMING_RETARDED | (gas_co, gas_nox) | (mx, mx) | inside | TIMING_RETARDED | PASS |
| 509 | TH-CMB-TIMING_RETARDED-gas_co2-gas_o2-mnmn | TIMING_RETARDED | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 510 | TH-CMB-TIMING_RETARDED-gas_co2-gas_o2-mnmx | TIMING_RETARDED | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 511 | TH-CMB-TIMING_RETARDED-gas_co2-gas_o2-mxmn | TIMING_RETARDED | (gas_co2, gas_o2) | (mx, mn) | inside | TIMING_RETARDED | PASS |
| 512 | TH-CMB-TIMING_RETARDED-gas_co2-gas_o2-mxmx | TIMING_RETARDED | (gas_co2, gas_o2) | (mx, mx) | inside | TIMING_RETARDED | PASS |
| 513 | TH-CMB-TIMING_RETARDED-gas_co2-gas_nox-mnmn | TIMING_RETARDED | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 514 | TH-CMB-TIMING_RETARDED-gas_co2-gas_nox-mnmx | TIMING_RETARDED | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 515 | TH-CMB-TIMING_RETARDED-gas_co2-gas_nox-mxmn | TIMING_RETARDED | (gas_co2, gas_nox) | (mx, mn) | inside | TIMING_RETARDED | PASS |
| 516 | TH-CMB-TIMING_RETARDED-gas_co2-gas_nox-mxmx | TIMING_RETARDED | (gas_co2, gas_nox) | (mx, mx) | inside | TIMING_RETARDED | PASS |
| 517 | TH-CMB-TIMING_RETARDED-gas_o2-gas_nox-mnmn | TIMING_RETARDED | (gas_o2, gas_nox) | (mn, mn) | inside | TIMING_RETARDED | PASS |
| 518 | TH-CMB-TIMING_RETARDED-gas_o2-gas_nox-mnmx | TIMING_RETARDED | (gas_o2, gas_nox) | (mn, mx) | inside | TIMING_RETARDED | PASS |
| 519 | TH-CMB-TIMING_RETARDED-gas_o2-gas_nox-mxmn | TIMING_RETARDED | (gas_o2, gas_nox) | (mx, mn) | inside | TIMING_RETARDED | PASS |
| 520 | TH-CMB-TIMING_RETARDED-gas_o2-gas_nox-mxmx | TIMING_RETARDED | (gas_o2, gas_nox) | (mx, mx) | inside | TIMING_RETARDED | PASS |
| 521 | TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_co-mnmn | O2_SENSOR_BIASED_LOW | (gas_hc, gas_co) | (mn, mn) | inside | VVT_FAILURE | FAIL |
| 522 | TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_co-mnmx | O2_SENSOR_BIASED_LOW | (gas_hc, gas_co) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 523 | TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_co-mxmn | O2_SENSOR_BIASED_LOW | (gas_hc, gas_co) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 524 | TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_co-mxmx | O2_SENSOR_BIASED_LOW | (gas_hc, gas_co) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 525 | TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_co2-mnmn | O2_SENSOR_BIASED_LOW | (gas_hc, gas_co2) | (mn, mn) | inside | VVT_FAILURE | FAIL |
| 526 | TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_co2-mnmx | O2_SENSOR_BIASED_LOW | (gas_hc, gas_co2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 527 | TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_co2-mxmn | O2_SENSOR_BIASED_LOW | (gas_hc, gas_co2) | (mx, mn) | inside | EVAP_CANISTER_SATURATED | FAIL |
| 528 | TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_co2-mxmx | O2_SENSOR_BIASED_LOW | (gas_hc, gas_co2) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 529 | TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_o2-mnmn | O2_SENSOR_BIASED_LOW | (gas_hc, gas_o2) | (mn, mn) | inside | VVT_FAILURE | FAIL |
| 530 | TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_o2-mnmx | O2_SENSOR_BIASED_LOW | (gas_hc, gas_o2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 531 | TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_o2-mxmn | O2_SENSOR_BIASED_LOW | (gas_hc, gas_o2) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 532 | TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_o2-mxmx | O2_SENSOR_BIASED_LOW | (gas_hc, gas_o2) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 533 | TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_nox-mnmn | O2_SENSOR_BIASED_LOW | (gas_hc, gas_nox) | (mn, mn) | inside | O2_SENSOR_BIASED_LOW | PASS |
| 534 | TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_nox-mnmx | O2_SENSOR_BIASED_LOW | (gas_hc, gas_nox) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 535 | TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_nox-mxmn | O2_SENSOR_BIASED_LOW | (gas_hc, gas_nox) | (mx, mn) | inside | O2_SENSOR_BIASED_LOW | PASS |
| 536 | TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_nox-mxmx | O2_SENSOR_BIASED_LOW | (gas_hc, gas_nox) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 537 | TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_co2-mnmn | O2_SENSOR_BIASED_LOW | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 538 | TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_co2-mnmx | O2_SENSOR_BIASED_LOW | (gas_co, gas_co2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 539 | TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_co2-mxmn | O2_SENSOR_BIASED_LOW | (gas_co, gas_co2) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 540 | TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_co2-mxmx | O2_SENSOR_BIASED_LOW | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 541 | TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_o2-mnmn | O2_SENSOR_BIASED_LOW | (gas_co, gas_o2) | (mn, mn) | inside | VVT_FAILURE | FAIL |
| 542 | TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_o2-mnmx | O2_SENSOR_BIASED_LOW | (gas_co, gas_o2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 543 | TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_o2-mxmn | O2_SENSOR_BIASED_LOW | (gas_co, gas_o2) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 544 | TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_o2-mxmx | O2_SENSOR_BIASED_LOW | (gas_co, gas_o2) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 545 | TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_nox-mnmn | O2_SENSOR_BIASED_LOW | (gas_co, gas_nox) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 546 | TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_nox-mnmx | O2_SENSOR_BIASED_LOW | (gas_co, gas_nox) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 547 | TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_nox-mxmn | O2_SENSOR_BIASED_LOW | (gas_co, gas_nox) | (mx, mn) | inside | O2_SENSOR_BIASED_LOW | PASS |
| 548 | TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_nox-mxmx | O2_SENSOR_BIASED_LOW | (gas_co, gas_nox) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 549 | TH-CMB-O2_SENSOR_BIASED_L-gas_co2-gas_o2-mnmn | O2_SENSOR_BIASED_LOW | (gas_co2, gas_o2) | (mn, mn) | inside | VVT_FAILURE | FAIL |
| 550 | TH-CMB-O2_SENSOR_BIASED_L-gas_co2-gas_o2-mnmx | O2_SENSOR_BIASED_LOW | (gas_co2, gas_o2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 551 | TH-CMB-O2_SENSOR_BIASED_L-gas_co2-gas_o2-mxmn | O2_SENSOR_BIASED_LOW | (gas_co2, gas_o2) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 552 | TH-CMB-O2_SENSOR_BIASED_L-gas_co2-gas_o2-mxmx | O2_SENSOR_BIASED_LOW | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 553 | TH-CMB-O2_SENSOR_BIASED_L-gas_co2-gas_nox-mnmn | O2_SENSOR_BIASED_LOW | (gas_co2, gas_nox) | (mn, mn) | inside | O2_SENSOR_BIASED_LOW | PASS |
| 554 | TH-CMB-O2_SENSOR_BIASED_L-gas_co2-gas_nox-mnmx | O2_SENSOR_BIASED_LOW | (gas_co2, gas_nox) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 555 | TH-CMB-O2_SENSOR_BIASED_L-gas_co2-gas_nox-mxmn | O2_SENSOR_BIASED_LOW | (gas_co2, gas_nox) | (mx, mn) | inside | O2_SENSOR_BIASED_LOW | PASS |
| 556 | TH-CMB-O2_SENSOR_BIASED_L-gas_co2-gas_nox-mxmx | O2_SENSOR_BIASED_LOW | (gas_co2, gas_nox) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 557 | TH-CMB-O2_SENSOR_BIASED_L-gas_o2-gas_nox-mnmn | O2_SENSOR_BIASED_LOW | (gas_o2, gas_nox) | (mn, mn) | inside | O2_SENSOR_BIASED_LOW | PASS |
| 558 | TH-CMB-O2_SENSOR_BIASED_L-gas_o2-gas_nox-mnmx | O2_SENSOR_BIASED_LOW | (gas_o2, gas_nox) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 559 | TH-CMB-O2_SENSOR_BIASED_L-gas_o2-gas_nox-mxmn | O2_SENSOR_BIASED_LOW | (gas_o2, gas_nox) | (mx, mn) | inside | O2_SENSOR_BIASED_LOW | PASS |
| 560 | TH-CMB-O2_SENSOR_BIASED_L-gas_o2-gas_nox-mxmx | O2_SENSOR_BIASED_LOW | (gas_o2, gas_nox) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 561 | TH-CMB-O2_SENSOR_BIASED_H-gas_hc-gas_co-mnmn | O2_SENSOR_BIASED_HIGH | (gas_hc, gas_co) | (mn, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 562 | TH-CMB-O2_SENSOR_BIASED_H-gas_hc-gas_co-mnmx | O2_SENSOR_BIASED_HIGH | (gas_hc, gas_co) | (mn, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 563 | TH-CMB-O2_SENSOR_BIASED_H-gas_hc-gas_co-mxmn | O2_SENSOR_BIASED_HIGH | (gas_hc, gas_co) | (mx, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 564 | TH-CMB-O2_SENSOR_BIASED_H-gas_hc-gas_co-mxmx | O2_SENSOR_BIASED_HIGH | (gas_hc, gas_co) | (mx, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 565 | TH-CMB-O2_SENSOR_BIASED_H-gas_hc-gas_co2-mnmn | O2_SENSOR_BIASED_HIGH | (gas_hc, gas_co2) | (mn, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 566 | TH-CMB-O2_SENSOR_BIASED_H-gas_hc-gas_co2-mnmx | O2_SENSOR_BIASED_HIGH | (gas_hc, gas_co2) | (mn, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 567 | TH-CMB-O2_SENSOR_BIASED_H-gas_hc-gas_co2-mxmn | O2_SENSOR_BIASED_HIGH | (gas_hc, gas_co2) | (mx, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 568 | TH-CMB-O2_SENSOR_BIASED_H-gas_hc-gas_co2-mxmx | O2_SENSOR_BIASED_HIGH | (gas_hc, gas_co2) | (mx, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 569 | TH-CMB-O2_SENSOR_BIASED_H-gas_hc-gas_o2-mnmn | O2_SENSOR_BIASED_HIGH | (gas_hc, gas_o2) | (mn, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 570 | TH-CMB-O2_SENSOR_BIASED_H-gas_hc-gas_o2-mnmx | O2_SENSOR_BIASED_HIGH | (gas_hc, gas_o2) | (mn, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 571 | TH-CMB-O2_SENSOR_BIASED_H-gas_hc-gas_o2-mxmn | O2_SENSOR_BIASED_HIGH | (gas_hc, gas_o2) | (mx, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 572 | TH-CMB-O2_SENSOR_BIASED_H-gas_hc-gas_o2-mxmx | O2_SENSOR_BIASED_HIGH | (gas_hc, gas_o2) | (mx, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 573 | TH-CMB-O2_SENSOR_BIASED_H-gas_hc-gas_nox-mnmn | O2_SENSOR_BIASED_HIGH | (gas_hc, gas_nox) | (mn, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 574 | TH-CMB-O2_SENSOR_BIASED_H-gas_hc-gas_nox-mnmx | O2_SENSOR_BIASED_HIGH | (gas_hc, gas_nox) | (mn, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 575 | TH-CMB-O2_SENSOR_BIASED_H-gas_hc-gas_nox-mxmn | O2_SENSOR_BIASED_HIGH | (gas_hc, gas_nox) | (mx, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 576 | TH-CMB-O2_SENSOR_BIASED_H-gas_hc-gas_nox-mxmx | O2_SENSOR_BIASED_HIGH | (gas_hc, gas_nox) | (mx, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 577 | TH-CMB-O2_SENSOR_BIASED_H-gas_co-gas_co2-mnmn | O2_SENSOR_BIASED_HIGH | (gas_co, gas_co2) | (mn, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 578 | TH-CMB-O2_SENSOR_BIASED_H-gas_co-gas_co2-mnmx | O2_SENSOR_BIASED_HIGH | (gas_co, gas_co2) | (mn, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 579 | TH-CMB-O2_SENSOR_BIASED_H-gas_co-gas_co2-mxmn | O2_SENSOR_BIASED_HIGH | (gas_co, gas_co2) | (mx, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 580 | TH-CMB-O2_SENSOR_BIASED_H-gas_co-gas_co2-mxmx | O2_SENSOR_BIASED_HIGH | (gas_co, gas_co2) | (mx, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 581 | TH-CMB-O2_SENSOR_BIASED_H-gas_co-gas_o2-mnmn | O2_SENSOR_BIASED_HIGH | (gas_co, gas_o2) | (mn, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 582 | TH-CMB-O2_SENSOR_BIASED_H-gas_co-gas_o2-mnmx | O2_SENSOR_BIASED_HIGH | (gas_co, gas_o2) | (mn, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 583 | TH-CMB-O2_SENSOR_BIASED_H-gas_co-gas_o2-mxmn | O2_SENSOR_BIASED_HIGH | (gas_co, gas_o2) | (mx, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 584 | TH-CMB-O2_SENSOR_BIASED_H-gas_co-gas_o2-mxmx | O2_SENSOR_BIASED_HIGH | (gas_co, gas_o2) | (mx, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 585 | TH-CMB-O2_SENSOR_BIASED_H-gas_co-gas_nox-mnmn | O2_SENSOR_BIASED_HIGH | (gas_co, gas_nox) | (mn, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 586 | TH-CMB-O2_SENSOR_BIASED_H-gas_co-gas_nox-mnmx | O2_SENSOR_BIASED_HIGH | (gas_co, gas_nox) | (mn, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 587 | TH-CMB-O2_SENSOR_BIASED_H-gas_co-gas_nox-mxmn | O2_SENSOR_BIASED_HIGH | (gas_co, gas_nox) | (mx, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 588 | TH-CMB-O2_SENSOR_BIASED_H-gas_co-gas_nox-mxmx | O2_SENSOR_BIASED_HIGH | (gas_co, gas_nox) | (mx, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 589 | TH-CMB-O2_SENSOR_BIASED_H-gas_co2-gas_o2-mnmn | O2_SENSOR_BIASED_HIGH | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 590 | TH-CMB-O2_SENSOR_BIASED_H-gas_co2-gas_o2-mnmx | O2_SENSOR_BIASED_HIGH | (gas_co2, gas_o2) | (mn, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 591 | TH-CMB-O2_SENSOR_BIASED_H-gas_co2-gas_o2-mxmn | O2_SENSOR_BIASED_HIGH | (gas_co2, gas_o2) | (mx, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 592 | TH-CMB-O2_SENSOR_BIASED_H-gas_co2-gas_o2-mxmx | O2_SENSOR_BIASED_HIGH | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 593 | TH-CMB-O2_SENSOR_BIASED_H-gas_co2-gas_nox-mnmn | O2_SENSOR_BIASED_HIGH | (gas_co2, gas_nox) | (mn, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 594 | TH-CMB-O2_SENSOR_BIASED_H-gas_co2-gas_nox-mnmx | O2_SENSOR_BIASED_HIGH | (gas_co2, gas_nox) | (mn, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 595 | TH-CMB-O2_SENSOR_BIASED_H-gas_co2-gas_nox-mxmn | O2_SENSOR_BIASED_HIGH | (gas_co2, gas_nox) | (mx, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 596 | TH-CMB-O2_SENSOR_BIASED_H-gas_co2-gas_nox-mxmx | O2_SENSOR_BIASED_HIGH | (gas_co2, gas_nox) | (mx, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 597 | TH-CMB-O2_SENSOR_BIASED_H-gas_o2-gas_nox-mnmn | O2_SENSOR_BIASED_HIGH | (gas_o2, gas_nox) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 598 | TH-CMB-O2_SENSOR_BIASED_H-gas_o2-gas_nox-mnmx | O2_SENSOR_BIASED_HIGH | (gas_o2, gas_nox) | (mn, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 599 | TH-CMB-O2_SENSOR_BIASED_H-gas_o2-gas_nox-mxmn | O2_SENSOR_BIASED_HIGH | (gas_o2, gas_nox) | (mx, mn) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 600 | TH-CMB-O2_SENSOR_BIASED_H-gas_o2-gas_nox-mxmx | O2_SENSOR_BIASED_HIGH | (gas_o2, gas_nox) | (mx, mx) | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 601 | TH-CMB-WORN_ENGINE-gas_hc-gas_co-mnmn | WORN_ENGINE | (gas_hc, gas_co) | (mn, mn) | inside | NORMAL_OPERATION | FAIL |
| 602 | TH-CMB-WORN_ENGINE-gas_hc-gas_co-mnmx | WORN_ENGINE | (gas_hc, gas_co) | (mn, mx) | inside | O2_SENSOR_BIASED_LOW | FAIL |
| 603 | TH-CMB-WORN_ENGINE-gas_hc-gas_co-mxmn | WORN_ENGINE | (gas_hc, gas_co) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 604 | TH-CMB-WORN_ENGINE-gas_hc-gas_co-mxmx | WORN_ENGINE | (gas_hc, gas_co) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 605 | TH-CMB-WORN_ENGINE-gas_hc-gas_co2-mnmn | WORN_ENGINE | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 606 | TH-CMB-WORN_ENGINE-gas_hc-gas_co2-mnmx | WORN_ENGINE | (gas_hc, gas_co2) | (mn, mx) | inside | O2_SENSOR_BIASED_LOW | FAIL |
| 607 | TH-CMB-WORN_ENGINE-gas_hc-gas_co2-mxmn | WORN_ENGINE | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 608 | TH-CMB-WORN_ENGINE-gas_hc-gas_co2-mxmx | WORN_ENGINE | (gas_hc, gas_co2) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 609 | TH-CMB-WORN_ENGINE-gas_hc-gas_o2-mnmn | WORN_ENGINE | (gas_hc, gas_o2) | (mn, mn) | inside | O2_SENSOR_BIASED_LOW | FAIL |
| 610 | TH-CMB-WORN_ENGINE-gas_hc-gas_o2-mnmx | WORN_ENGINE | (gas_hc, gas_o2) | (mn, mx) | inside | O2_SENSOR_BIASED_LOW | FAIL |
| 611 | TH-CMB-WORN_ENGINE-gas_hc-gas_o2-mxmn | WORN_ENGINE | (gas_hc, gas_o2) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 612 | TH-CMB-WORN_ENGINE-gas_hc-gas_o2-mxmx | WORN_ENGINE | (gas_hc, gas_o2) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 613 | TH-CMB-WORN_ENGINE-gas_hc-gas_nox-mnmn | WORN_ENGINE | (gas_hc, gas_nox) | (mn, mn) | inside | O2_SENSOR_BIASED_LOW | FAIL |
| 614 | TH-CMB-WORN_ENGINE-gas_hc-gas_nox-mnmx | WORN_ENGINE | (gas_hc, gas_nox) | (mn, mx) | inside | O2_SENSOR_BIASED_LOW | FAIL |
| 615 | TH-CMB-WORN_ENGINE-gas_hc-gas_nox-mxmn | WORN_ENGINE | (gas_hc, gas_nox) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 616 | TH-CMB-WORN_ENGINE-gas_hc-gas_nox-mxmx | WORN_ENGINE | (gas_hc, gas_nox) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 617 | TH-CMB-WORN_ENGINE-gas_co-gas_co2-mnmn | WORN_ENGINE | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 618 | TH-CMB-WORN_ENGINE-gas_co-gas_co2-mnmx | WORN_ENGINE | (gas_co, gas_co2) | (mn, mx) | inside | WORN_ENGINE | PASS |
| 619 | TH-CMB-WORN_ENGINE-gas_co-gas_co2-mxmn | WORN_ENGINE | (gas_co, gas_co2) | (mx, mn) | inside | RICH_MIXTURE | FAIL |
| 620 | TH-CMB-WORN_ENGINE-gas_co-gas_co2-mxmx | WORN_ENGINE | (gas_co, gas_co2) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 621 | TH-CMB-WORN_ENGINE-gas_co-gas_o2-mnmn | WORN_ENGINE | (gas_co, gas_o2) | (mn, mn) | inside | VVT_FAILURE | FAIL |
| 622 | TH-CMB-WORN_ENGINE-gas_co-gas_o2-mnmx | WORN_ENGINE | (gas_co, gas_o2) | (mn, mx) | inside | WORN_VALVE_SEALS | FAIL |
| 623 | TH-CMB-WORN_ENGINE-gas_co-gas_o2-mxmn | WORN_ENGINE | (gas_co, gas_o2) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 624 | TH-CMB-WORN_ENGINE-gas_co-gas_o2-mxmx | WORN_ENGINE | (gas_co, gas_o2) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 625 | TH-CMB-WORN_ENGINE-gas_co-gas_nox-mnmn | WORN_ENGINE | (gas_co, gas_nox) | (mn, mn) | inside | WORN_VALVE_SEALS | FAIL |
| 626 | TH-CMB-WORN_ENGINE-gas_co-gas_nox-mnmx | WORN_ENGINE | (gas_co, gas_nox) | (mn, mx) | inside | WORN_VALVE_SEALS | FAIL |
| 627 | TH-CMB-WORN_ENGINE-gas_co-gas_nox-mxmn | WORN_ENGINE | (gas_co, gas_nox) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 628 | TH-CMB-WORN_ENGINE-gas_co-gas_nox-mxmx | WORN_ENGINE | (gas_co, gas_nox) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 629 | TH-CMB-WORN_ENGINE-gas_co2-gas_o2-mnmn | WORN_ENGINE | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 630 | TH-CMB-WORN_ENGINE-gas_co2-gas_o2-mnmx | WORN_ENGINE | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 631 | TH-CMB-WORN_ENGINE-gas_co2-gas_o2-mxmn | WORN_ENGINE | (gas_co2, gas_o2) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 632 | TH-CMB-WORN_ENGINE-gas_co2-gas_o2-mxmx | WORN_ENGINE | (gas_co2, gas_o2) | (mx, mx) | inside | WORN_ENGINE | PASS |
| 633 | TH-CMB-WORN_ENGINE-gas_co2-gas_nox-mnmn | WORN_ENGINE | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 634 | TH-CMB-WORN_ENGINE-gas_co2-gas_nox-mnmx | WORN_ENGINE | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 635 | TH-CMB-WORN_ENGINE-gas_co2-gas_nox-mxmn | WORN_ENGINE | (gas_co2, gas_nox) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 636 | TH-CMB-WORN_ENGINE-gas_co2-gas_nox-mxmx | WORN_ENGINE | (gas_co2, gas_nox) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 637 | TH-CMB-WORN_ENGINE-gas_o2-gas_nox-mnmn | WORN_ENGINE | (gas_o2, gas_nox) | (mn, mn) | inside | VVT_FAILURE | FAIL |
| 638 | TH-CMB-WORN_ENGINE-gas_o2-gas_nox-mnmx | WORN_ENGINE | (gas_o2, gas_nox) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 639 | TH-CMB-WORN_ENGINE-gas_o2-gas_nox-mxmn | WORN_ENGINE | (gas_o2, gas_nox) | (mx, mn) | inside | WORN_ENGINE | PASS |
| 640 | TH-CMB-WORN_ENGINE-gas_o2-gas_nox-mxmx | WORN_ENGINE | (gas_o2, gas_nox) | (mx, mx) | inside | WORN_ENGINE | PASS |
| 641 | TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_co-mnmn | FLAT_CAMSHAFT | (gas_hc, gas_co) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 642 | TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_co-mnmx | FLAT_CAMSHAFT | (gas_hc, gas_co) | (mn, mx) | inside | TIMING_RETARDED | FAIL |
| 643 | TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_co-mxmn | FLAT_CAMSHAFT | (gas_hc, gas_co) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 644 | TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_co-mxmx | FLAT_CAMSHAFT | (gas_hc, gas_co) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 645 | TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_co2-mnmn | FLAT_CAMSHAFT | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 646 | TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_co2-mnmx | FLAT_CAMSHAFT | (gas_hc, gas_co2) | (mn, mx) | inside | TIMING_RETARDED | FAIL |
| 647 | TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_co2-mxmn | FLAT_CAMSHAFT | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 648 | TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_co2-mxmx | FLAT_CAMSHAFT | (gas_hc, gas_co2) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 649 | TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_o2-mnmn | FLAT_CAMSHAFT | (gas_hc, gas_o2) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 650 | TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_o2-mnmx | FLAT_CAMSHAFT | (gas_hc, gas_o2) | (mn, mx) | inside | TIMING_RETARDED | FAIL |
| 651 | TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_o2-mxmn | FLAT_CAMSHAFT | (gas_hc, gas_o2) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 652 | TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_o2-mxmx | FLAT_CAMSHAFT | (gas_hc, gas_o2) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 653 | TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_nox-mnmn | FLAT_CAMSHAFT | (gas_hc, gas_nox) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 654 | TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_nox-mnmx | FLAT_CAMSHAFT | (gas_hc, gas_nox) | (mn, mx) | inside | WORN_PISTON_RINGS | FAIL |
| 655 | TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_nox-mxmn | FLAT_CAMSHAFT | (gas_hc, gas_nox) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 656 | TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_nox-mxmx | FLAT_CAMSHAFT | (gas_hc, gas_nox) | (mx, mx) | inside | WORN_PISTON_RINGS | FAIL |
| 657 | TH-CMB-FLAT_CAMSHAFT-gas_co-gas_co2-mnmn | FLAT_CAMSHAFT | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 658 | TH-CMB-FLAT_CAMSHAFT-gas_co-gas_co2-mnmx | FLAT_CAMSHAFT | (gas_co, gas_co2) | (mn, mx) | inside | TIMING_RETARDED | FAIL |
| 659 | TH-CMB-FLAT_CAMSHAFT-gas_co-gas_co2-mxmn | FLAT_CAMSHAFT | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 660 | TH-CMB-FLAT_CAMSHAFT-gas_co-gas_co2-mxmx | FLAT_CAMSHAFT | (gas_co, gas_co2) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 661 | TH-CMB-FLAT_CAMSHAFT-gas_co-gas_o2-mnmn | FLAT_CAMSHAFT | (gas_co, gas_o2) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 662 | TH-CMB-FLAT_CAMSHAFT-gas_co-gas_o2-mnmx | FLAT_CAMSHAFT | (gas_co, gas_o2) | (mn, mx) | inside | TIMING_RETARDED | FAIL |
| 663 | TH-CMB-FLAT_CAMSHAFT-gas_co-gas_o2-mxmn | FLAT_CAMSHAFT | (gas_co, gas_o2) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 664 | TH-CMB-FLAT_CAMSHAFT-gas_co-gas_o2-mxmx | FLAT_CAMSHAFT | (gas_co, gas_o2) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 665 | TH-CMB-FLAT_CAMSHAFT-gas_co-gas_nox-mnmn | FLAT_CAMSHAFT | (gas_co, gas_nox) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 666 | TH-CMB-FLAT_CAMSHAFT-gas_co-gas_nox-mnmx | FLAT_CAMSHAFT | (gas_co, gas_nox) | (mn, mx) | inside | WORN_PISTON_RINGS | FAIL |
| 667 | TH-CMB-FLAT_CAMSHAFT-gas_co-gas_nox-mxmn | FLAT_CAMSHAFT | (gas_co, gas_nox) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 668 | TH-CMB-FLAT_CAMSHAFT-gas_co-gas_nox-mxmx | FLAT_CAMSHAFT | (gas_co, gas_nox) | (mx, mx) | inside | WORN_PISTON_RINGS | FAIL |
| 669 | TH-CMB-FLAT_CAMSHAFT-gas_co2-gas_o2-mnmn | FLAT_CAMSHAFT | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 670 | TH-CMB-FLAT_CAMSHAFT-gas_co2-gas_o2-mnmx | FLAT_CAMSHAFT | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 671 | TH-CMB-FLAT_CAMSHAFT-gas_co2-gas_o2-mxmn | FLAT_CAMSHAFT | (gas_co2, gas_o2) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 672 | TH-CMB-FLAT_CAMSHAFT-gas_co2-gas_o2-mxmx | FLAT_CAMSHAFT | (gas_co2, gas_o2) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 673 | TH-CMB-FLAT_CAMSHAFT-gas_co2-gas_nox-mnmn | FLAT_CAMSHAFT | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 674 | TH-CMB-FLAT_CAMSHAFT-gas_co2-gas_nox-mnmx | FLAT_CAMSHAFT | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 675 | TH-CMB-FLAT_CAMSHAFT-gas_co2-gas_nox-mxmn | FLAT_CAMSHAFT | (gas_co2, gas_nox) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 676 | TH-CMB-FLAT_CAMSHAFT-gas_co2-gas_nox-mxmx | FLAT_CAMSHAFT | (gas_co2, gas_nox) | (mx, mx) | inside | WORN_PISTON_RINGS | FAIL |
| 677 | TH-CMB-FLAT_CAMSHAFT-gas_o2-gas_nox-mnmn | FLAT_CAMSHAFT | (gas_o2, gas_nox) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 678 | TH-CMB-FLAT_CAMSHAFT-gas_o2-gas_nox-mnmx | FLAT_CAMSHAFT | (gas_o2, gas_nox) | (mn, mx) | inside | WORN_PISTON_RINGS | FAIL |
| 679 | TH-CMB-FLAT_CAMSHAFT-gas_o2-gas_nox-mxmn | FLAT_CAMSHAFT | (gas_o2, gas_nox) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 680 | TH-CMB-FLAT_CAMSHAFT-gas_o2-gas_nox-mxmx | FLAT_CAMSHAFT | (gas_o2, gas_nox) | (mx, mx) | inside | WORN_PISTON_RINGS | FAIL |
| 681 | TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_co-mnmn | GDI_INTAKE_VALVE_CARBON | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 682 | TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_co-mnmx | GDI_INTAKE_VALVE_CARBON | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 683 | TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_co-mxmn | GDI_INTAKE_VALVE_CARBON | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 684 | TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_co-mxmx | GDI_INTAKE_VALVE_CARBON | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 685 | TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_co2-mnmn | GDI_INTAKE_VALVE_CARBON | (gas_hc, gas_co2) | (mn, mn) | inside | EXHAUST_AIR_LEAK | FAIL |
| 686 | TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_co2-mnmx | GDI_INTAKE_VALVE_CARBON | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 687 | TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_co2-mxmn | GDI_INTAKE_VALVE_CARBON | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 688 | TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_co2-mxmx | GDI_INTAKE_VALVE_CARBON | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 689 | TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_o2-mnmn | GDI_INTAKE_VALVE_CARBON | (gas_hc, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 690 | TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_o2-mnmx | GDI_INTAKE_VALVE_CARBON | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 691 | TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_o2-mxmn | GDI_INTAKE_VALVE_CARBON | (gas_hc, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 692 | TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_o2-mxmx | GDI_INTAKE_VALVE_CARBON | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 693 | TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_nox-mnmn | GDI_INTAKE_VALVE_CARBON | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 694 | TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_nox-mnmx | GDI_INTAKE_VALVE_CARBON | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 695 | TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_nox-mxmn | GDI_INTAKE_VALVE_CARBON | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 696 | TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_nox-mxmx | GDI_INTAKE_VALVE_CARBON | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 697 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_co2-mnmn | GDI_INTAKE_VALVE_CARBON | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 698 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_co2-mnmx | GDI_INTAKE_VALVE_CARBON | (gas_co, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 699 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_co2-mxmn | GDI_INTAKE_VALVE_CARBON | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 700 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_co2-mxmx | GDI_INTAKE_VALVE_CARBON | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 701 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_o2-mnmn | GDI_INTAKE_VALVE_CARBON | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 702 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_o2-mnmx | GDI_INTAKE_VALVE_CARBON | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 703 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_o2-mxmn | GDI_INTAKE_VALVE_CARBON | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 704 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_o2-mxmx | GDI_INTAKE_VALVE_CARBON | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 705 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_nox-mnmn | GDI_INTAKE_VALVE_CARBON | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 706 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_nox-mnmx | GDI_INTAKE_VALVE_CARBON | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 707 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_nox-mxmn | GDI_INTAKE_VALVE_CARBON | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 708 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_nox-mxmx | GDI_INTAKE_VALVE_CARBON | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 709 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co2-gas_o2-mnmn | GDI_INTAKE_VALVE_CARBON | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 710 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co2-gas_o2-mnmx | GDI_INTAKE_VALVE_CARBON | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 711 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co2-gas_o2-mxmn | GDI_INTAKE_VALVE_CARBON | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 712 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co2-gas_o2-mxmx | GDI_INTAKE_VALVE_CARBON | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 713 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co2-gas_nox-mnmn | GDI_INTAKE_VALVE_CARBON | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 714 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co2-gas_nox-mnmx | GDI_INTAKE_VALVE_CARBON | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 715 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co2-gas_nox-mxmn | GDI_INTAKE_VALVE_CARBON | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 716 | TH-CMB-GDI_INTAKE_VALVE_C-gas_co2-gas_nox-mxmx | GDI_INTAKE_VALVE_CARBON | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 717 | TH-CMB-GDI_INTAKE_VALVE_C-gas_o2-gas_nox-mnmn | GDI_INTAKE_VALVE_CARBON | (gas_o2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 718 | TH-CMB-GDI_INTAKE_VALVE_C-gas_o2-gas_nox-mnmx | GDI_INTAKE_VALVE_CARBON | (gas_o2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 719 | TH-CMB-GDI_INTAKE_VALVE_C-gas_o2-gas_nox-mxmn | GDI_INTAKE_VALVE_CARBON | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 720 | TH-CMB-GDI_INTAKE_VALVE_C-gas_o2-gas_nox-mxmx | GDI_INTAKE_VALVE_CARBON | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 721 | TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_co-mnmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 722 | TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_co-mnmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 723 | TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_co-mxmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 724 | TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_co-mxmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 725 | TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_co2-mnmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 726 | TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_co2-mnmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 727 | TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_co2-mxmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 728 | TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_co2-mxmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 729 | TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_o2-mnmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_hc, gas_o2) | (mn, mn) | inside | CATALYST_OVERWHELMED | FAIL |
| 730 | TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_o2-mnmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_hc, gas_o2) | (mn, mx) | inside | CATALYST_OVERWHELMED | FAIL |
| 731 | TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_o2-mxmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_hc, gas_o2) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 732 | TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_o2-mxmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_hc, gas_o2) | (mx, mx) | inside | NORMAL_OPERATION | FAIL |
| 733 | TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_nox-mnmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_hc, gas_nox) | (mn, mn) | inside | RICH_MIXTURE | FAIL |
| 734 | TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_nox-mnmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_hc, gas_nox) | (mn, mx) | inside | CATALYST_OVERWHELMED | FAIL |
| 735 | TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_nox-mxmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_hc, gas_nox) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 736 | TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_nox-mxmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_hc, gas_nox) | (mx, mx) | inside | NORMAL_OPERATION | FAIL |
| 737 | TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_co2-mnmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 738 | TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_co2-mnmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co, gas_co2) | (mn, mx) | inside | NORMAL_OPERATION | FAIL |
| 739 | TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_co2-mxmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co, gas_co2) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 740 | TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_co2-mxmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 741 | TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_o2-mnmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 742 | TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_o2-mnmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 743 | TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_o2-mxmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 744 | TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_o2-mxmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 745 | TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_nox-mnmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 746 | TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_nox-mnmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 747 | TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_nox-mxmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 748 | TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_nox-mxmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 749 | TH-CMB-VACUUM_REGULATOR_D-gas_co2-gas_o2-mnmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 750 | TH-CMB-VACUUM_REGULATOR_D-gas_co2-gas_o2-mnmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 751 | TH-CMB-VACUUM_REGULATOR_D-gas_co2-gas_o2-mxmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 752 | TH-CMB-VACUUM_REGULATOR_D-gas_co2-gas_o2-mxmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 753 | TH-CMB-VACUUM_REGULATOR_D-gas_co2-gas_nox-mnmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 754 | TH-CMB-VACUUM_REGULATOR_D-gas_co2-gas_nox-mnmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 755 | TH-CMB-VACUUM_REGULATOR_D-gas_co2-gas_nox-mxmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 756 | TH-CMB-VACUUM_REGULATOR_D-gas_co2-gas_nox-mxmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 757 | TH-CMB-VACUUM_REGULATOR_D-gas_o2-gas_nox-mnmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_o2, gas_nox) | (mn, mn) | inside | NORMAL_OPERATION | FAIL |
| 758 | TH-CMB-VACUUM_REGULATOR_D-gas_o2-gas_nox-mnmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_o2, gas_nox) | (mn, mx) | inside | NORMAL_OPERATION | FAIL |
| 759 | TH-CMB-VACUUM_REGULATOR_D-gas_o2-gas_nox-mxmn | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_o2, gas_nox) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 760 | TH-CMB-VACUUM_REGULATOR_D-gas_o2-gas_nox-mxmx | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | (gas_o2, gas_nox) | (mx, mx) | inside | NORMAL_OPERATION | FAIL |
| 761 | TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_co-mnmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 762 | TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_co-mnmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 763 | TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_co-mxmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 764 | TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_co-mxmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 765 | TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_co2-mnmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 766 | TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_co2-mnmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 767 | TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_co2-mxmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 768 | TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_co2-mxmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 769 | TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_o2-mnmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_hc, gas_o2) | (mn, mn) | inside | CATALYST_OVERWHELMED | FAIL |
| 770 | TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_o2-mnmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_hc, gas_o2) | (mn, mx) | inside | CATALYST_OVERWHELMED | FAIL |
| 771 | TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_o2-mxmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_hc, gas_o2) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 772 | TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_o2-mxmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_hc, gas_o2) | (mx, mx) | inside | NORMAL_OPERATION | FAIL |
| 773 | TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_nox-mnmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_hc, gas_nox) | (mn, mn) | inside | RICH_MIXTURE | FAIL |
| 774 | TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_nox-mnmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_hc, gas_nox) | (mn, mx) | inside | CATALYST_OVERWHELMED | FAIL |
| 775 | TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_nox-mxmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_hc, gas_nox) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 776 | TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_nox-mxmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_hc, gas_nox) | (mx, mx) | inside | NORMAL_OPERATION | FAIL |
| 777 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_co2-mnmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 778 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_co2-mnmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co, gas_co2) | (mn, mx) | inside | NORMAL_OPERATION | FAIL |
| 779 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_co2-mxmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co, gas_co2) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 780 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_co2-mxmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 781 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_o2-mnmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 782 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_o2-mnmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 783 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_o2-mxmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 784 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_o2-mxmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 785 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_nox-mnmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 786 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_nox-mnmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 787 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_nox-mxmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 788 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_nox-mxmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 789 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co2-gas_o2-mnmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 790 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co2-gas_o2-mnmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 791 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co2-gas_o2-mxmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 792 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co2-gas_o2-mxmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 793 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co2-gas_nox-mnmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 794 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co2-gas_nox-mnmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 795 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co2-gas_nox-mxmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 796 | TH-CMB-GDI_HPFP_INTERNAL_-gas_co2-gas_nox-mxmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 797 | TH-CMB-GDI_HPFP_INTERNAL_-gas_o2-gas_nox-mnmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_o2, gas_nox) | (mn, mn) | inside | NORMAL_OPERATION | FAIL |
| 798 | TH-CMB-GDI_HPFP_INTERNAL_-gas_o2-gas_nox-mnmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_o2, gas_nox) | (mn, mx) | inside | NORMAL_OPERATION | FAIL |
| 799 | TH-CMB-GDI_HPFP_INTERNAL_-gas_o2-gas_nox-mxmn | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_o2, gas_nox) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 800 | TH-CMB-GDI_HPFP_INTERNAL_-gas_o2-gas_nox-mxmx | GDI_HPFP_INTERNAL_SEAL_LEAK | (gas_o2, gas_nox) | (mx, mx) | inside | NORMAL_OPERATION | FAIL |
| 801 | TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_co-mnmn | WORN_VALVE_SEALS | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 802 | TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_co-mnmx | WORN_VALVE_SEALS | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 803 | TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_co-mxmn | WORN_VALVE_SEALS | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 804 | TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_co-mxmx | WORN_VALVE_SEALS | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 805 | TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_co2-mnmn | WORN_VALVE_SEALS | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 806 | TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_co2-mnmx | WORN_VALVE_SEALS | (gas_hc, gas_co2) | (mn, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 807 | TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_co2-mxmn | WORN_VALVE_SEALS | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 808 | TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_co2-mxmx | WORN_VALVE_SEALS | (gas_hc, gas_co2) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 809 | TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_o2-mnmn | WORN_VALVE_SEALS | (gas_hc, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 810 | TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_o2-mnmx | WORN_VALVE_SEALS | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 811 | TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_o2-mxmn | WORN_VALVE_SEALS | (gas_hc, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 812 | TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_o2-mxmx | WORN_VALVE_SEALS | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 813 | TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_nox-mnmn | WORN_VALVE_SEALS | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 814 | TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_nox-mnmx | WORN_VALVE_SEALS | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 815 | TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_nox-mxmn | WORN_VALVE_SEALS | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 816 | TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_nox-mxmx | WORN_VALVE_SEALS | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 817 | TH-CMB-WORN_VALVE_SEALS-gas_co-gas_co2-mnmn | WORN_VALVE_SEALS | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 818 | TH-CMB-WORN_VALVE_SEALS-gas_co-gas_co2-mnmx | WORN_VALVE_SEALS | (gas_co, gas_co2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 819 | TH-CMB-WORN_VALVE_SEALS-gas_co-gas_co2-mxmn | WORN_VALVE_SEALS | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 820 | TH-CMB-WORN_VALVE_SEALS-gas_co-gas_co2-mxmx | WORN_VALVE_SEALS | (gas_co, gas_co2) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 821 | TH-CMB-WORN_VALVE_SEALS-gas_co-gas_o2-mnmn | WORN_VALVE_SEALS | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 822 | TH-CMB-WORN_VALVE_SEALS-gas_co-gas_o2-mnmx | WORN_VALVE_SEALS | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 823 | TH-CMB-WORN_VALVE_SEALS-gas_co-gas_o2-mxmn | WORN_VALVE_SEALS | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 824 | TH-CMB-WORN_VALVE_SEALS-gas_co-gas_o2-mxmx | WORN_VALVE_SEALS | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 825 | TH-CMB-WORN_VALVE_SEALS-gas_co-gas_nox-mnmn | WORN_VALVE_SEALS | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 826 | TH-CMB-WORN_VALVE_SEALS-gas_co-gas_nox-mnmx | WORN_VALVE_SEALS | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 827 | TH-CMB-WORN_VALVE_SEALS-gas_co-gas_nox-mxmn | WORN_VALVE_SEALS | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 828 | TH-CMB-WORN_VALVE_SEALS-gas_co-gas_nox-mxmx | WORN_VALVE_SEALS | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 829 | TH-CMB-WORN_VALVE_SEALS-gas_co2-gas_o2-mnmn | WORN_VALVE_SEALS | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 830 | TH-CMB-WORN_VALVE_SEALS-gas_co2-gas_o2-mnmx | WORN_VALVE_SEALS | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 831 | TH-CMB-WORN_VALVE_SEALS-gas_co2-gas_o2-mxmn | WORN_VALVE_SEALS | (gas_co2, gas_o2) | (mx, mn) | inside | VVT_FAILURE | FAIL |
| 832 | TH-CMB-WORN_VALVE_SEALS-gas_co2-gas_o2-mxmx | WORN_VALVE_SEALS | (gas_co2, gas_o2) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 833 | TH-CMB-WORN_VALVE_SEALS-gas_co2-gas_nox-mnmn | WORN_VALVE_SEALS | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 834 | TH-CMB-WORN_VALVE_SEALS-gas_co2-gas_nox-mnmx | WORN_VALVE_SEALS | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 835 | TH-CMB-WORN_VALVE_SEALS-gas_co2-gas_nox-mxmn | WORN_VALVE_SEALS | (gas_co2, gas_nox) | (mx, mn) | inside | WORN_VALVE_SEALS | PASS |
| 836 | TH-CMB-WORN_VALVE_SEALS-gas_co2-gas_nox-mxmx | WORN_VALVE_SEALS | (gas_co2, gas_nox) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 837 | TH-CMB-WORN_VALVE_SEALS-gas_o2-gas_nox-mnmn | WORN_VALVE_SEALS | (gas_o2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 838 | TH-CMB-WORN_VALVE_SEALS-gas_o2-gas_nox-mnmx | WORN_VALVE_SEALS | (gas_o2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 839 | TH-CMB-WORN_VALVE_SEALS-gas_o2-gas_nox-mxmn | WORN_VALVE_SEALS | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 840 | TH-CMB-WORN_VALVE_SEALS-gas_o2-gas_nox-mxmx | WORN_VALVE_SEALS | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 841 | TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_co-mnmn | WORN_PISTON_RINGS | (gas_hc, gas_co) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 842 | TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_co-mnmx | WORN_PISTON_RINGS | (gas_hc, gas_co) | (mn, mx) | inside | TIMING_RETARDED | FAIL |
| 843 | TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_co-mxmn | WORN_PISTON_RINGS | (gas_hc, gas_co) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 844 | TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_co-mxmx | WORN_PISTON_RINGS | (gas_hc, gas_co) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 845 | TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_co2-mnmn | WORN_PISTON_RINGS | (gas_hc, gas_co2) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 846 | TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_co2-mnmx | WORN_PISTON_RINGS | (gas_hc, gas_co2) | (mn, mx) | inside | TIMING_RETARDED | FAIL |
| 847 | TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_co2-mxmn | WORN_PISTON_RINGS | (gas_hc, gas_co2) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 848 | TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_co2-mxmx | WORN_PISTON_RINGS | (gas_hc, gas_co2) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 849 | TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_o2-mnmn | WORN_PISTON_RINGS | (gas_hc, gas_o2) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 850 | TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_o2-mnmx | WORN_PISTON_RINGS | (gas_hc, gas_o2) | (mn, mx) | inside | TIMING_RETARDED | FAIL |
| 851 | TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_o2-mxmn | WORN_PISTON_RINGS | (gas_hc, gas_o2) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 852 | TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_o2-mxmx | WORN_PISTON_RINGS | (gas_hc, gas_o2) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 853 | TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_nox-mnmn | WORN_PISTON_RINGS | (gas_hc, gas_nox) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 854 | TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_nox-mnmx | WORN_PISTON_RINGS | (gas_hc, gas_nox) | (mn, mx) | inside | WORN_PISTON_RINGS | PASS |
| 855 | TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_nox-mxmn | WORN_PISTON_RINGS | (gas_hc, gas_nox) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 856 | TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_nox-mxmx | WORN_PISTON_RINGS | (gas_hc, gas_nox) | (mx, mx) | inside | WORN_PISTON_RINGS | PASS |
| 857 | TH-CMB-WORN_PISTON_RINGS-gas_co-gas_co2-mnmn | WORN_PISTON_RINGS | (gas_co, gas_co2) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 858 | TH-CMB-WORN_PISTON_RINGS-gas_co-gas_co2-mnmx | WORN_PISTON_RINGS | (gas_co, gas_co2) | (mn, mx) | inside | TIMING_RETARDED | FAIL |
| 859 | TH-CMB-WORN_PISTON_RINGS-gas_co-gas_co2-mxmn | WORN_PISTON_RINGS | (gas_co, gas_co2) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 860 | TH-CMB-WORN_PISTON_RINGS-gas_co-gas_co2-mxmx | WORN_PISTON_RINGS | (gas_co, gas_co2) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 861 | TH-CMB-WORN_PISTON_RINGS-gas_co-gas_o2-mnmn | WORN_PISTON_RINGS | (gas_co, gas_o2) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 862 | TH-CMB-WORN_PISTON_RINGS-gas_co-gas_o2-mnmx | WORN_PISTON_RINGS | (gas_co, gas_o2) | (mn, mx) | inside | TIMING_RETARDED | FAIL |
| 863 | TH-CMB-WORN_PISTON_RINGS-gas_co-gas_o2-mxmn | WORN_PISTON_RINGS | (gas_co, gas_o2) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 864 | TH-CMB-WORN_PISTON_RINGS-gas_co-gas_o2-mxmx | WORN_PISTON_RINGS | (gas_co, gas_o2) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 865 | TH-CMB-WORN_PISTON_RINGS-gas_co-gas_nox-mnmn | WORN_PISTON_RINGS | (gas_co, gas_nox) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 866 | TH-CMB-WORN_PISTON_RINGS-gas_co-gas_nox-mnmx | WORN_PISTON_RINGS | (gas_co, gas_nox) | (mn, mx) | inside | WORN_PISTON_RINGS | PASS |
| 867 | TH-CMB-WORN_PISTON_RINGS-gas_co-gas_nox-mxmn | WORN_PISTON_RINGS | (gas_co, gas_nox) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 868 | TH-CMB-WORN_PISTON_RINGS-gas_co-gas_nox-mxmx | WORN_PISTON_RINGS | (gas_co, gas_nox) | (mx, mx) | inside | WORN_PISTON_RINGS | PASS |
| 869 | TH-CMB-WORN_PISTON_RINGS-gas_co2-gas_o2-mnmn | WORN_PISTON_RINGS | (gas_co2, gas_o2) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 870 | TH-CMB-WORN_PISTON_RINGS-gas_co2-gas_o2-mnmx | WORN_PISTON_RINGS | (gas_co2, gas_o2) | (mn, mx) | inside | TIMING_RETARDED | FAIL |
| 871 | TH-CMB-WORN_PISTON_RINGS-gas_co2-gas_o2-mxmn | WORN_PISTON_RINGS | (gas_co2, gas_o2) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 872 | TH-CMB-WORN_PISTON_RINGS-gas_co2-gas_o2-mxmx | WORN_PISTON_RINGS | (gas_co2, gas_o2) | (mx, mx) | inside | TIMING_RETARDED | FAIL |
| 873 | TH-CMB-WORN_PISTON_RINGS-gas_co2-gas_nox-mnmn | WORN_PISTON_RINGS | (gas_co2, gas_nox) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 874 | TH-CMB-WORN_PISTON_RINGS-gas_co2-gas_nox-mnmx | WORN_PISTON_RINGS | (gas_co2, gas_nox) | (mn, mx) | inside | WORN_PISTON_RINGS | PASS |
| 875 | TH-CMB-WORN_PISTON_RINGS-gas_co2-gas_nox-mxmn | WORN_PISTON_RINGS | (gas_co2, gas_nox) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 876 | TH-CMB-WORN_PISTON_RINGS-gas_co2-gas_nox-mxmx | WORN_PISTON_RINGS | (gas_co2, gas_nox) | (mx, mx) | inside | WORN_PISTON_RINGS | PASS |
| 877 | TH-CMB-WORN_PISTON_RINGS-gas_o2-gas_nox-mnmn | WORN_PISTON_RINGS | (gas_o2, gas_nox) | (mn, mn) | inside | TIMING_RETARDED | FAIL |
| 878 | TH-CMB-WORN_PISTON_RINGS-gas_o2-gas_nox-mnmx | WORN_PISTON_RINGS | (gas_o2, gas_nox) | (mn, mx) | inside | WORN_PISTON_RINGS | PASS |
| 879 | TH-CMB-WORN_PISTON_RINGS-gas_o2-gas_nox-mxmn | WORN_PISTON_RINGS | (gas_o2, gas_nox) | (mx, mn) | inside | TIMING_RETARDED | FAIL |
| 880 | TH-CMB-WORN_PISTON_RINGS-gas_o2-gas_nox-mxmx | WORN_PISTON_RINGS | (gas_o2, gas_nox) | (mx, mx) | inside | WORN_PISTON_RINGS | PASS |
| 881 | TH-CMB-POA_SIGNATURE-gas_hc-gas_co-mnmn | POA_SIGNATURE | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 882 | TH-CMB-POA_SIGNATURE-gas_hc-gas_co-mnmx | POA_SIGNATURE | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 883 | TH-CMB-POA_SIGNATURE-gas_hc-gas_co-mxmn | POA_SIGNATURE | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 884 | TH-CMB-POA_SIGNATURE-gas_hc-gas_co-mxmx | POA_SIGNATURE | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 885 | TH-CMB-POA_SIGNATURE-gas_hc-gas_co2-mnmn | POA_SIGNATURE | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 886 | TH-CMB-POA_SIGNATURE-gas_hc-gas_co2-mnmx | POA_SIGNATURE | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 887 | TH-CMB-POA_SIGNATURE-gas_hc-gas_co2-mxmn | POA_SIGNATURE | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 888 | TH-CMB-POA_SIGNATURE-gas_hc-gas_co2-mxmx | POA_SIGNATURE | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 889 | TH-CMB-POA_SIGNATURE-gas_hc-gas_o2-mnmn | POA_SIGNATURE | (gas_hc, gas_o2) | (mn, mn) | inside | CATALYST_OVERWHELMED | FAIL |
| 890 | TH-CMB-POA_SIGNATURE-gas_hc-gas_o2-mnmx | POA_SIGNATURE | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 891 | TH-CMB-POA_SIGNATURE-gas_hc-gas_o2-mxmn | POA_SIGNATURE | (gas_hc, gas_o2) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 892 | TH-CMB-POA_SIGNATURE-gas_hc-gas_o2-mxmx | POA_SIGNATURE | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 893 | TH-CMB-POA_SIGNATURE-gas_hc-gas_nox-mnmn | POA_SIGNATURE | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 894 | TH-CMB-POA_SIGNATURE-gas_hc-gas_nox-mnmx | POA_SIGNATURE | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 895 | TH-CMB-POA_SIGNATURE-gas_hc-gas_nox-mxmn | POA_SIGNATURE | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 896 | TH-CMB-POA_SIGNATURE-gas_hc-gas_nox-mxmx | POA_SIGNATURE | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 897 | TH-CMB-POA_SIGNATURE-gas_co-gas_co2-mnmn | POA_SIGNATURE | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 898 | TH-CMB-POA_SIGNATURE-gas_co-gas_co2-mnmx | POA_SIGNATURE | (gas_co, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 899 | TH-CMB-POA_SIGNATURE-gas_co-gas_co2-mxmn | POA_SIGNATURE | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 900 | TH-CMB-POA_SIGNATURE-gas_co-gas_co2-mxmx | POA_SIGNATURE | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 901 | TH-CMB-POA_SIGNATURE-gas_co-gas_o2-mnmn | POA_SIGNATURE | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 902 | TH-CMB-POA_SIGNATURE-gas_co-gas_o2-mnmx | POA_SIGNATURE | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 903 | TH-CMB-POA_SIGNATURE-gas_co-gas_o2-mxmn | POA_SIGNATURE | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 904 | TH-CMB-POA_SIGNATURE-gas_co-gas_o2-mxmx | POA_SIGNATURE | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 905 | TH-CMB-POA_SIGNATURE-gas_co-gas_nox-mnmn | POA_SIGNATURE | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 906 | TH-CMB-POA_SIGNATURE-gas_co-gas_nox-mnmx | POA_SIGNATURE | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 907 | TH-CMB-POA_SIGNATURE-gas_co-gas_nox-mxmn | POA_SIGNATURE | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 908 | TH-CMB-POA_SIGNATURE-gas_co-gas_nox-mxmx | POA_SIGNATURE | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 909 | TH-CMB-POA_SIGNATURE-gas_co2-gas_o2-mnmn | POA_SIGNATURE | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 910 | TH-CMB-POA_SIGNATURE-gas_co2-gas_o2-mnmx | POA_SIGNATURE | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 911 | TH-CMB-POA_SIGNATURE-gas_co2-gas_o2-mxmn | POA_SIGNATURE | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 912 | TH-CMB-POA_SIGNATURE-gas_co2-gas_o2-mxmx | POA_SIGNATURE | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 913 | TH-CMB-POA_SIGNATURE-gas_co2-gas_nox-mnmn | POA_SIGNATURE | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 914 | TH-CMB-POA_SIGNATURE-gas_co2-gas_nox-mnmx | POA_SIGNATURE | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 915 | TH-CMB-POA_SIGNATURE-gas_co2-gas_nox-mxmn | POA_SIGNATURE | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 916 | TH-CMB-POA_SIGNATURE-gas_co2-gas_nox-mxmx | POA_SIGNATURE | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 917 | TH-CMB-POA_SIGNATURE-gas_o2-gas_nox-mnmn | POA_SIGNATURE | (gas_o2, gas_nox) | (mn, mn) | inside | NORMAL_OPERATION | FAIL |
| 918 | TH-CMB-POA_SIGNATURE-gas_o2-gas_nox-mnmx | POA_SIGNATURE | (gas_o2, gas_nox) | (mn, mx) | inside | NORMAL_OPERATION | FAIL |
| 919 | TH-CMB-POA_SIGNATURE-gas_o2-gas_nox-mxmn | POA_SIGNATURE | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 920 | TH-CMB-POA_SIGNATURE-gas_o2-gas_nox-mxmx | POA_SIGNATURE | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 921 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co-mnmn | CAM_TIMING_RETARDED_MAP | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 922 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co-mnmx | CAM_TIMING_RETARDED_MAP | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 923 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co-mxmn | CAM_TIMING_RETARDED_MAP | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 924 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co-mxmx | CAM_TIMING_RETARDED_MAP | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 925 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co2-mnmn | CAM_TIMING_RETARDED_MAP | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 926 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co2-mnmx | CAM_TIMING_RETARDED_MAP | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 927 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co2-mxmn | CAM_TIMING_RETARDED_MAP | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 928 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co2-mxmx | CAM_TIMING_RETARDED_MAP | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 929 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_o2-mnmn | CAM_TIMING_RETARDED_MAP | (gas_hc, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 930 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_o2-mnmx | CAM_TIMING_RETARDED_MAP | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 931 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_o2-mxmn | CAM_TIMING_RETARDED_MAP | (gas_hc, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 932 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_o2-mxmx | CAM_TIMING_RETARDED_MAP | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 933 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_nox-mnmn | CAM_TIMING_RETARDED_MAP | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 934 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_nox-mnmx | CAM_TIMING_RETARDED_MAP | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 935 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_nox-mxmn | CAM_TIMING_RETARDED_MAP | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 936 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_nox-mxmx | CAM_TIMING_RETARDED_MAP | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 937 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_co2-mnmn | CAM_TIMING_RETARDED_MAP | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 938 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_co2-mnmx | CAM_TIMING_RETARDED_MAP | (gas_co, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 939 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_co2-mxmn | CAM_TIMING_RETARDED_MAP | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 940 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_co2-mxmx | CAM_TIMING_RETARDED_MAP | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 941 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_o2-mnmn | CAM_TIMING_RETARDED_MAP | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 942 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_o2-mnmx | CAM_TIMING_RETARDED_MAP | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 943 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_o2-mxmn | CAM_TIMING_RETARDED_MAP | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 944 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_o2-mxmx | CAM_TIMING_RETARDED_MAP | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 945 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_nox-mnmn | CAM_TIMING_RETARDED_MAP | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 946 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_nox-mnmx | CAM_TIMING_RETARDED_MAP | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 947 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_nox-mxmn | CAM_TIMING_RETARDED_MAP | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 948 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_nox-mxmx | CAM_TIMING_RETARDED_MAP | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 949 | TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_o2-mnmn | CAM_TIMING_RETARDED_MAP | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 950 | TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_o2-mnmx | CAM_TIMING_RETARDED_MAP | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 951 | TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_o2-mxmn | CAM_TIMING_RETARDED_MAP | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 952 | TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_o2-mxmx | CAM_TIMING_RETARDED_MAP | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 953 | TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_nox-mnmn | CAM_TIMING_RETARDED_MAP | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 954 | TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_nox-mnmx | CAM_TIMING_RETARDED_MAP | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 955 | TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_nox-mxmn | CAM_TIMING_RETARDED_MAP | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 956 | TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_nox-mxmx | CAM_TIMING_RETARDED_MAP | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 957 | TH-CMB-CAM_TIMING_RETARDE-gas_o2-gas_nox-mnmn | CAM_TIMING_RETARDED_MAP | (gas_o2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 958 | TH-CMB-CAM_TIMING_RETARDE-gas_o2-gas_nox-mnmx | CAM_TIMING_RETARDED_MAP | (gas_o2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 959 | TH-CMB-CAM_TIMING_RETARDE-gas_o2-gas_nox-mxmn | CAM_TIMING_RETARDED_MAP | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 960 | TH-CMB-CAM_TIMING_RETARDE-gas_o2-gas_nox-mxmx | CAM_TIMING_RETARDED_MAP | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 961 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co-mnmn | CAM_TIMING_RETARDED_MAF | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 962 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co-mnmx | CAM_TIMING_RETARDED_MAF | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 963 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co-mxmn | CAM_TIMING_RETARDED_MAF | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 964 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co-mxmx | CAM_TIMING_RETARDED_MAF | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 965 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co2-mnmn | CAM_TIMING_RETARDED_MAF | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 966 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co2-mnmx | CAM_TIMING_RETARDED_MAF | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 967 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co2-mxmn | CAM_TIMING_RETARDED_MAF | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 968 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co2-mxmx | CAM_TIMING_RETARDED_MAF | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 969 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_o2-mnmn | CAM_TIMING_RETARDED_MAF | (gas_hc, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 970 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_o2-mnmx | CAM_TIMING_RETARDED_MAF | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 971 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_o2-mxmn | CAM_TIMING_RETARDED_MAF | (gas_hc, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 972 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_o2-mxmx | CAM_TIMING_RETARDED_MAF | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 973 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_nox-mnmn | CAM_TIMING_RETARDED_MAF | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 974 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_nox-mnmx | CAM_TIMING_RETARDED_MAF | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 975 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_nox-mxmn | CAM_TIMING_RETARDED_MAF | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 976 | TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_nox-mxmx | CAM_TIMING_RETARDED_MAF | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 977 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_co2-mnmn | CAM_TIMING_RETARDED_MAF | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 978 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_co2-mnmx | CAM_TIMING_RETARDED_MAF | (gas_co, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 979 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_co2-mxmn | CAM_TIMING_RETARDED_MAF | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 980 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_co2-mxmx | CAM_TIMING_RETARDED_MAF | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 981 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_o2-mnmn | CAM_TIMING_RETARDED_MAF | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 982 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_o2-mnmx | CAM_TIMING_RETARDED_MAF | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 983 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_o2-mxmn | CAM_TIMING_RETARDED_MAF | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 984 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_o2-mxmx | CAM_TIMING_RETARDED_MAF | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 985 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_nox-mnmn | CAM_TIMING_RETARDED_MAF | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 986 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_nox-mnmx | CAM_TIMING_RETARDED_MAF | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 987 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_nox-mxmn | CAM_TIMING_RETARDED_MAF | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 988 | TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_nox-mxmx | CAM_TIMING_RETARDED_MAF | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 989 | TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_o2-mnmn | CAM_TIMING_RETARDED_MAF | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 990 | TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_o2-mnmx | CAM_TIMING_RETARDED_MAF | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 991 | TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_o2-mxmn | CAM_TIMING_RETARDED_MAF | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 992 | TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_o2-mxmx | CAM_TIMING_RETARDED_MAF | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 993 | TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_nox-mnmn | CAM_TIMING_RETARDED_MAF | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 994 | TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_nox-mnmx | CAM_TIMING_RETARDED_MAF | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 995 | TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_nox-mxmn | CAM_TIMING_RETARDED_MAF | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 996 | TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_nox-mxmx | CAM_TIMING_RETARDED_MAF | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 997 | TH-CMB-CAM_TIMING_RETARDE-gas_o2-gas_nox-mnmn | CAM_TIMING_RETARDED_MAF | (gas_o2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 998 | TH-CMB-CAM_TIMING_RETARDE-gas_o2-gas_nox-mnmx | CAM_TIMING_RETARDED_MAF | (gas_o2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 999 | TH-CMB-CAM_TIMING_RETARDE-gas_o2-gas_nox-mxmn | CAM_TIMING_RETARDED_MAF | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1000 | TH-CMB-CAM_TIMING_RETARDE-gas_o2-gas_nox-mxmx | CAM_TIMING_RETARDED_MAF | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1001 | TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_co-mnmn | CAM_TIMING_ADVANCED | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1002 | TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_co-mnmx | CAM_TIMING_ADVANCED | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1003 | TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_co-mxmn | CAM_TIMING_ADVANCED | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1004 | TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_co-mxmx | CAM_TIMING_ADVANCED | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1005 | TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_co2-mnmn | CAM_TIMING_ADVANCED | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1006 | TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_co2-mnmx | CAM_TIMING_ADVANCED | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1007 | TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_co2-mxmn | CAM_TIMING_ADVANCED | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1008 | TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_co2-mxmx | CAM_TIMING_ADVANCED | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1009 | TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_o2-mnmn | CAM_TIMING_ADVANCED | (gas_hc, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1010 | TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_o2-mnmx | CAM_TIMING_ADVANCED | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1011 | TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_o2-mxmn | CAM_TIMING_ADVANCED | (gas_hc, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1012 | TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_o2-mxmx | CAM_TIMING_ADVANCED | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1013 | TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_nox-mnmn | CAM_TIMING_ADVANCED | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1014 | TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_nox-mnmx | CAM_TIMING_ADVANCED | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1015 | TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_nox-mxmn | CAM_TIMING_ADVANCED | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1016 | TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_nox-mxmx | CAM_TIMING_ADVANCED | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1017 | TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_co2-mnmn | CAM_TIMING_ADVANCED | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1018 | TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_co2-mnmx | CAM_TIMING_ADVANCED | (gas_co, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1019 | TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_co2-mxmn | CAM_TIMING_ADVANCED | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1020 | TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_co2-mxmx | CAM_TIMING_ADVANCED | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1021 | TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_o2-mnmn | CAM_TIMING_ADVANCED | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1022 | TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_o2-mnmx | CAM_TIMING_ADVANCED | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1023 | TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_o2-mxmn | CAM_TIMING_ADVANCED | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1024 | TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_o2-mxmx | CAM_TIMING_ADVANCED | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1025 | TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_nox-mnmn | CAM_TIMING_ADVANCED | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1026 | TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_nox-mnmx | CAM_TIMING_ADVANCED | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1027 | TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_nox-mxmn | CAM_TIMING_ADVANCED | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1028 | TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_nox-mxmx | CAM_TIMING_ADVANCED | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1029 | TH-CMB-CAM_TIMING_ADVANCE-gas_co2-gas_o2-mnmn | CAM_TIMING_ADVANCED | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1030 | TH-CMB-CAM_TIMING_ADVANCE-gas_co2-gas_o2-mnmx | CAM_TIMING_ADVANCED | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1031 | TH-CMB-CAM_TIMING_ADVANCE-gas_co2-gas_o2-mxmn | CAM_TIMING_ADVANCED | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1032 | TH-CMB-CAM_TIMING_ADVANCE-gas_co2-gas_o2-mxmx | CAM_TIMING_ADVANCED | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1033 | TH-CMB-CAM_TIMING_ADVANCE-gas_co2-gas_nox-mnmn | CAM_TIMING_ADVANCED | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1034 | TH-CMB-CAM_TIMING_ADVANCE-gas_co2-gas_nox-mnmx | CAM_TIMING_ADVANCED | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1035 | TH-CMB-CAM_TIMING_ADVANCE-gas_co2-gas_nox-mxmn | CAM_TIMING_ADVANCED | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1036 | TH-CMB-CAM_TIMING_ADVANCE-gas_co2-gas_nox-mxmx | CAM_TIMING_ADVANCED | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1037 | TH-CMB-CAM_TIMING_ADVANCE-gas_o2-gas_nox-mnmn | CAM_TIMING_ADVANCED | (gas_o2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1038 | TH-CMB-CAM_TIMING_ADVANCE-gas_o2-gas_nox-mnmx | CAM_TIMING_ADVANCED | (gas_o2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1039 | TH-CMB-CAM_TIMING_ADVANCE-gas_o2-gas_nox-mxmn | CAM_TIMING_ADVANCED | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1040 | TH-CMB-CAM_TIMING_ADVANCE-gas_o2-gas_nox-mxmx | CAM_TIMING_ADVANCED | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1041 | TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_co-mnmn | EGR_STUCK_CLOSED | (gas_hc, gas_co) | (mn, mn) | inside | TIMING_OVER_ADVANCED | FAIL |
| 1042 | TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_co-mnmx | EGR_STUCK_CLOSED | (gas_hc, gas_co) | (mn, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1043 | TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_co-mxmn | EGR_STUCK_CLOSED | (gas_hc, gas_co) | (mx, mn) | inside | TIMING_OVER_ADVANCED | FAIL |
| 1044 | TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_co-mxmx | EGR_STUCK_CLOSED | (gas_hc, gas_co) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1045 | TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_co2-mnmn | EGR_STUCK_CLOSED | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1046 | TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_co2-mnmx | EGR_STUCK_CLOSED | (gas_hc, gas_co2) | (mn, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1047 | TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_co2-mxmn | EGR_STUCK_CLOSED | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1048 | TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_co2-mxmx | EGR_STUCK_CLOSED | (gas_hc, gas_co2) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1049 | TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_o2-mnmn | EGR_STUCK_CLOSED | (gas_hc, gas_o2) | (mn, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1050 | TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_o2-mnmx | EGR_STUCK_CLOSED | (gas_hc, gas_o2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 1051 | TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_o2-mxmn | EGR_STUCK_CLOSED | (gas_hc, gas_o2) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1052 | TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_o2-mxmx | EGR_STUCK_CLOSED | (gas_hc, gas_o2) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1053 | TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_nox-mnmn | EGR_STUCK_CLOSED | (gas_hc, gas_nox) | (mn, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1054 | TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_nox-mnmx | EGR_STUCK_CLOSED | (gas_hc, gas_nox) | (mn, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1055 | TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_nox-mxmn | EGR_STUCK_CLOSED | (gas_hc, gas_nox) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1056 | TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_nox-mxmx | EGR_STUCK_CLOSED | (gas_hc, gas_nox) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1057 | TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_co2-mnmn | EGR_STUCK_CLOSED | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1058 | TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_co2-mnmx | EGR_STUCK_CLOSED | (gas_co, gas_co2) | (mn, mx) | inside | TIMING_OVER_ADVANCED | FAIL |
| 1059 | TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_co2-mxmn | EGR_STUCK_CLOSED | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1060 | TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_co2-mxmx | EGR_STUCK_CLOSED | (gas_co, gas_co2) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1061 | TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_o2-mnmn | EGR_STUCK_CLOSED | (gas_co, gas_o2) | (mn, mn) | inside | TIMING_OVER_ADVANCED | FAIL |
| 1062 | TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_o2-mnmx | EGR_STUCK_CLOSED | (gas_co, gas_o2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 1063 | TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_o2-mxmn | EGR_STUCK_CLOSED | (gas_co, gas_o2) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1064 | TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_o2-mxmx | EGR_STUCK_CLOSED | (gas_co, gas_o2) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1065 | TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_nox-mnmn | EGR_STUCK_CLOSED | (gas_co, gas_nox) | (mn, mn) | inside | TIMING_OVER_ADVANCED | FAIL |
| 1066 | TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_nox-mnmx | EGR_STUCK_CLOSED | (gas_co, gas_nox) | (mn, mx) | inside | TIMING_OVER_ADVANCED | FAIL |
| 1067 | TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_nox-mxmn | EGR_STUCK_CLOSED | (gas_co, gas_nox) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1068 | TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_nox-mxmx | EGR_STUCK_CLOSED | (gas_co, gas_nox) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1069 | TH-CMB-EGR_STUCK_CLOSED-gas_co2-gas_o2-mnmn | EGR_STUCK_CLOSED | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1070 | TH-CMB-EGR_STUCK_CLOSED-gas_co2-gas_o2-mnmx | EGR_STUCK_CLOSED | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1071 | TH-CMB-EGR_STUCK_CLOSED-gas_co2-gas_o2-mxmn | EGR_STUCK_CLOSED | (gas_co2, gas_o2) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1072 | TH-CMB-EGR_STUCK_CLOSED-gas_co2-gas_o2-mxmx | EGR_STUCK_CLOSED | (gas_co2, gas_o2) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1073 | TH-CMB-EGR_STUCK_CLOSED-gas_co2-gas_nox-mnmn | EGR_STUCK_CLOSED | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1074 | TH-CMB-EGR_STUCK_CLOSED-gas_co2-gas_nox-mnmx | EGR_STUCK_CLOSED | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1075 | TH-CMB-EGR_STUCK_CLOSED-gas_co2-gas_nox-mxmn | EGR_STUCK_CLOSED | (gas_co2, gas_nox) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1076 | TH-CMB-EGR_STUCK_CLOSED-gas_co2-gas_nox-mxmx | EGR_STUCK_CLOSED | (gas_co2, gas_nox) | (mx, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1077 | TH-CMB-EGR_STUCK_CLOSED-gas_o2-gas_nox-mnmn | EGR_STUCK_CLOSED | (gas_o2, gas_nox) | (mn, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1078 | TH-CMB-EGR_STUCK_CLOSED-gas_o2-gas_nox-mnmx | EGR_STUCK_CLOSED | (gas_o2, gas_nox) | (mn, mx) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1079 | TH-CMB-EGR_STUCK_CLOSED-gas_o2-gas_nox-mxmn | EGR_STUCK_CLOSED | (gas_o2, gas_nox) | (mx, mn) | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 1080 | TH-CMB-EGR_STUCK_CLOSED-gas_o2-gas_nox-mxmx | EGR_STUCK_CLOSED | (gas_o2, gas_nox) | (mx, mx) | inside | VVT_FAILURE | FAIL |
| 1081 | TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_co-mnmn | EGR_STUCK_OPEN | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1082 | TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_co-mnmx | EGR_STUCK_OPEN | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1083 | TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_co-mxmn | EGR_STUCK_OPEN | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1084 | TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_co-mxmx | EGR_STUCK_OPEN | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1085 | TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_co2-mnmn | EGR_STUCK_OPEN | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1086 | TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_co2-mnmx | EGR_STUCK_OPEN | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1087 | TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_co2-mxmn | EGR_STUCK_OPEN | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1088 | TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_co2-mxmx | EGR_STUCK_OPEN | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1089 | TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_o2-mnmn | EGR_STUCK_OPEN | (gas_hc, gas_o2) | (mn, mn) | inside | VVT_FAILURE | FAIL |
| 1090 | TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_o2-mnmx | EGR_STUCK_OPEN | (gas_hc, gas_o2) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 1091 | TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_o2-mxmn | EGR_STUCK_OPEN | (gas_hc, gas_o2) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 1092 | TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_o2-mxmx | EGR_STUCK_OPEN | (gas_hc, gas_o2) | (mx, mx) | inside | NORMAL_OPERATION | FAIL |
| 1093 | TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_nox-mnmn | EGR_STUCK_OPEN | (gas_hc, gas_nox) | (mn, mn) | inside | RICH_MIXTURE | FAIL |
| 1094 | TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_nox-mnmx | EGR_STUCK_OPEN | (gas_hc, gas_nox) | (mn, mx) | inside | VVT_FAILURE | FAIL |
| 1095 | TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_nox-mxmn | EGR_STUCK_OPEN | (gas_hc, gas_nox) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 1096 | TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_nox-mxmx | EGR_STUCK_OPEN | (gas_hc, gas_nox) | (mx, mx) | inside | NORMAL_OPERATION | FAIL |
| 1097 | TH-CMB-EGR_STUCK_OPEN-gas_co-gas_co2-mnmn | EGR_STUCK_OPEN | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1098 | TH-CMB-EGR_STUCK_OPEN-gas_co-gas_co2-mnmx | EGR_STUCK_OPEN | (gas_co, gas_co2) | (mn, mx) | inside | NORMAL_OPERATION | FAIL |
| 1099 | TH-CMB-EGR_STUCK_OPEN-gas_co-gas_co2-mxmn | EGR_STUCK_OPEN | (gas_co, gas_co2) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 1100 | TH-CMB-EGR_STUCK_OPEN-gas_co-gas_co2-mxmx | EGR_STUCK_OPEN | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1101 | TH-CMB-EGR_STUCK_OPEN-gas_co-gas_o2-mnmn | EGR_STUCK_OPEN | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1102 | TH-CMB-EGR_STUCK_OPEN-gas_co-gas_o2-mnmx | EGR_STUCK_OPEN | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1103 | TH-CMB-EGR_STUCK_OPEN-gas_co-gas_o2-mxmn | EGR_STUCK_OPEN | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1104 | TH-CMB-EGR_STUCK_OPEN-gas_co-gas_o2-mxmx | EGR_STUCK_OPEN | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1105 | TH-CMB-EGR_STUCK_OPEN-gas_co-gas_nox-mnmn | EGR_STUCK_OPEN | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1106 | TH-CMB-EGR_STUCK_OPEN-gas_co-gas_nox-mnmx | EGR_STUCK_OPEN | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1107 | TH-CMB-EGR_STUCK_OPEN-gas_co-gas_nox-mxmn | EGR_STUCK_OPEN | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1108 | TH-CMB-EGR_STUCK_OPEN-gas_co-gas_nox-mxmx | EGR_STUCK_OPEN | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1109 | TH-CMB-EGR_STUCK_OPEN-gas_co2-gas_o2-mnmn | EGR_STUCK_OPEN | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1110 | TH-CMB-EGR_STUCK_OPEN-gas_co2-gas_o2-mnmx | EGR_STUCK_OPEN | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1111 | TH-CMB-EGR_STUCK_OPEN-gas_co2-gas_o2-mxmn | EGR_STUCK_OPEN | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1112 | TH-CMB-EGR_STUCK_OPEN-gas_co2-gas_o2-mxmx | EGR_STUCK_OPEN | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1113 | TH-CMB-EGR_STUCK_OPEN-gas_co2-gas_nox-mnmn | EGR_STUCK_OPEN | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1114 | TH-CMB-EGR_STUCK_OPEN-gas_co2-gas_nox-mnmx | EGR_STUCK_OPEN | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1115 | TH-CMB-EGR_STUCK_OPEN-gas_co2-gas_nox-mxmn | EGR_STUCK_OPEN | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1116 | TH-CMB-EGR_STUCK_OPEN-gas_co2-gas_nox-mxmx | EGR_STUCK_OPEN | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1117 | TH-CMB-EGR_STUCK_OPEN-gas_o2-gas_nox-mnmn | EGR_STUCK_OPEN | (gas_o2, gas_nox) | (mn, mn) | inside | NORMAL_OPERATION | FAIL |
| 1118 | TH-CMB-EGR_STUCK_OPEN-gas_o2-gas_nox-mnmx | EGR_STUCK_OPEN | (gas_o2, gas_nox) | (mn, mx) | inside | NORMAL_OPERATION | FAIL |
| 1119 | TH-CMB-EGR_STUCK_OPEN-gas_o2-gas_nox-mxmn | EGR_STUCK_OPEN | (gas_o2, gas_nox) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 1120 | TH-CMB-EGR_STUCK_OPEN-gas_o2-gas_nox-mxmx | EGR_STUCK_OPEN | (gas_o2, gas_nox) | (mx, mx) | inside | NORMAL_OPERATION | FAIL |
| 1121 | TH-CMB-VVT_FAILURE-gas_hc-gas_co-mnmn | VVT_FAILURE | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1122 | TH-CMB-VVT_FAILURE-gas_hc-gas_co-mnmx | VVT_FAILURE | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1123 | TH-CMB-VVT_FAILURE-gas_hc-gas_co-mxmn | VVT_FAILURE | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1124 | TH-CMB-VVT_FAILURE-gas_hc-gas_co-mxmx | VVT_FAILURE | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1125 | TH-CMB-VVT_FAILURE-gas_hc-gas_co2-mnmn | VVT_FAILURE | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1126 | TH-CMB-VVT_FAILURE-gas_hc-gas_co2-mnmx | VVT_FAILURE | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1127 | TH-CMB-VVT_FAILURE-gas_hc-gas_co2-mxmn | VVT_FAILURE | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1128 | TH-CMB-VVT_FAILURE-gas_hc-gas_co2-mxmx | VVT_FAILURE | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1129 | TH-CMB-VVT_FAILURE-gas_hc-gas_o2-mnmn | VVT_FAILURE | (gas_hc, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1130 | TH-CMB-VVT_FAILURE-gas_hc-gas_o2-mnmx | VVT_FAILURE | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1131 | TH-CMB-VVT_FAILURE-gas_hc-gas_o2-mxmn | VVT_FAILURE | (gas_hc, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1132 | TH-CMB-VVT_FAILURE-gas_hc-gas_o2-mxmx | VVT_FAILURE | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1133 | TH-CMB-VVT_FAILURE-gas_hc-gas_nox-mnmn | VVT_FAILURE | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1134 | TH-CMB-VVT_FAILURE-gas_hc-gas_nox-mnmx | VVT_FAILURE | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1135 | TH-CMB-VVT_FAILURE-gas_hc-gas_nox-mxmn | VVT_FAILURE | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1136 | TH-CMB-VVT_FAILURE-gas_hc-gas_nox-mxmx | VVT_FAILURE | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1137 | TH-CMB-VVT_FAILURE-gas_co-gas_co2-mnmn | VVT_FAILURE | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1138 | TH-CMB-VVT_FAILURE-gas_co-gas_co2-mnmx | VVT_FAILURE | (gas_co, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1139 | TH-CMB-VVT_FAILURE-gas_co-gas_co2-mxmn | VVT_FAILURE | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1140 | TH-CMB-VVT_FAILURE-gas_co-gas_co2-mxmx | VVT_FAILURE | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1141 | TH-CMB-VVT_FAILURE-gas_co-gas_o2-mnmn | VVT_FAILURE | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1142 | TH-CMB-VVT_FAILURE-gas_co-gas_o2-mnmx | VVT_FAILURE | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1143 | TH-CMB-VVT_FAILURE-gas_co-gas_o2-mxmn | VVT_FAILURE | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1144 | TH-CMB-VVT_FAILURE-gas_co-gas_o2-mxmx | VVT_FAILURE | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1145 | TH-CMB-VVT_FAILURE-gas_co-gas_nox-mnmn | VVT_FAILURE | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1146 | TH-CMB-VVT_FAILURE-gas_co-gas_nox-mnmx | VVT_FAILURE | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1147 | TH-CMB-VVT_FAILURE-gas_co-gas_nox-mxmn | VVT_FAILURE | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1148 | TH-CMB-VVT_FAILURE-gas_co-gas_nox-mxmx | VVT_FAILURE | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1149 | TH-CMB-VVT_FAILURE-gas_co2-gas_o2-mnmn | VVT_FAILURE | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1150 | TH-CMB-VVT_FAILURE-gas_co2-gas_o2-mnmx | VVT_FAILURE | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1151 | TH-CMB-VVT_FAILURE-gas_co2-gas_o2-mxmn | VVT_FAILURE | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1152 | TH-CMB-VVT_FAILURE-gas_co2-gas_o2-mxmx | VVT_FAILURE | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1153 | TH-CMB-VVT_FAILURE-gas_co2-gas_nox-mnmn | VVT_FAILURE | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1154 | TH-CMB-VVT_FAILURE-gas_co2-gas_nox-mnmx | VVT_FAILURE | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1155 | TH-CMB-VVT_FAILURE-gas_co2-gas_nox-mxmn | VVT_FAILURE | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1156 | TH-CMB-VVT_FAILURE-gas_co2-gas_nox-mxmx | VVT_FAILURE | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1157 | TH-CMB-VVT_FAILURE-gas_o2-gas_nox-mnmn | VVT_FAILURE | (gas_o2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1158 | TH-CMB-VVT_FAILURE-gas_o2-gas_nox-mnmx | VVT_FAILURE | (gas_o2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1159 | TH-CMB-VVT_FAILURE-gas_o2-gas_nox-mxmn | VVT_FAILURE | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1160 | TH-CMB-VVT_FAILURE-gas_o2-gas_nox-mxmx | VVT_FAILURE | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1161 | TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_co-mnmn | EVAP_CANISTER_SATURATED | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1162 | TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_co-mnmx | EVAP_CANISTER_SATURATED | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1163 | TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_co-mxmn | EVAP_CANISTER_SATURATED | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1164 | TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_co-mxmx | EVAP_CANISTER_SATURATED | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1165 | TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_co2-mnmn | EVAP_CANISTER_SATURATED | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1166 | TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_co2-mnmx | EVAP_CANISTER_SATURATED | (gas_hc, gas_co2) | (mn, mx) | inside | EVAP_CANISTER_SATURATED | PASS |
| 1167 | TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_co2-mxmn | EVAP_CANISTER_SATURATED | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1168 | TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_co2-mxmx | EVAP_CANISTER_SATURATED | (gas_hc, gas_co2) | (mx, mx) | inside | EVAP_CANISTER_SATURATED | PASS |
| 1169 | TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_o2-mnmn | EVAP_CANISTER_SATURATED | (gas_hc, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1170 | TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_o2-mnmx | EVAP_CANISTER_SATURATED | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1171 | TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_o2-mxmn | EVAP_CANISTER_SATURATED | (gas_hc, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1172 | TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_o2-mxmx | EVAP_CANISTER_SATURATED | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1173 | TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_nox-mnmn | EVAP_CANISTER_SATURATED | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1174 | TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_nox-mnmx | EVAP_CANISTER_SATURATED | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1175 | TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_nox-mxmn | EVAP_CANISTER_SATURATED | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1176 | TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_nox-mxmx | EVAP_CANISTER_SATURATED | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1177 | TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_co2-mnmn | EVAP_CANISTER_SATURATED | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1178 | TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_co2-mnmx | EVAP_CANISTER_SATURATED | (gas_co, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1179 | TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_co2-mxmn | EVAP_CANISTER_SATURATED | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1180 | TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_co2-mxmx | EVAP_CANISTER_SATURATED | (gas_co, gas_co2) | (mx, mx) | inside | EVAP_CANISTER_SATURATED | PASS |
| 1181 | TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_o2-mnmn | EVAP_CANISTER_SATURATED | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1182 | TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_o2-mnmx | EVAP_CANISTER_SATURATED | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1183 | TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_o2-mxmn | EVAP_CANISTER_SATURATED | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1184 | TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_o2-mxmx | EVAP_CANISTER_SATURATED | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1185 | TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_nox-mnmn | EVAP_CANISTER_SATURATED | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1186 | TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_nox-mnmx | EVAP_CANISTER_SATURATED | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1187 | TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_nox-mxmn | EVAP_CANISTER_SATURATED | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1188 | TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_nox-mxmx | EVAP_CANISTER_SATURATED | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1189 | TH-CMB-EVAP_CANISTER_SATU-gas_co2-gas_o2-mnmn | EVAP_CANISTER_SATURATED | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1190 | TH-CMB-EVAP_CANISTER_SATU-gas_co2-gas_o2-mnmx | EVAP_CANISTER_SATURATED | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1191 | TH-CMB-EVAP_CANISTER_SATU-gas_co2-gas_o2-mxmn | EVAP_CANISTER_SATURATED | (gas_co2, gas_o2) | (mx, mn) | inside | EVAP_CANISTER_SATURATED | PASS |
| 1192 | TH-CMB-EVAP_CANISTER_SATU-gas_co2-gas_o2-mxmx | EVAP_CANISTER_SATURATED | (gas_co2, gas_o2) | (mx, mx) | inside | EVAP_CANISTER_SATURATED | PASS |
| 1193 | TH-CMB-EVAP_CANISTER_SATU-gas_co2-gas_nox-mnmn | EVAP_CANISTER_SATURATED | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1194 | TH-CMB-EVAP_CANISTER_SATU-gas_co2-gas_nox-mnmx | EVAP_CANISTER_SATURATED | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1195 | TH-CMB-EVAP_CANISTER_SATU-gas_co2-gas_nox-mxmn | EVAP_CANISTER_SATURATED | (gas_co2, gas_nox) | (mx, mn) | inside | RICH_MIXTURE | FAIL |
| 1196 | TH-CMB-EVAP_CANISTER_SATU-gas_co2-gas_nox-mxmx | EVAP_CANISTER_SATURATED | (gas_co2, gas_nox) | (mx, mx) | inside | EVAP_CANISTER_SATURATED | PASS |
| 1197 | TH-CMB-EVAP_CANISTER_SATU-gas_o2-gas_nox-mnmn | EVAP_CANISTER_SATURATED | (gas_o2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1198 | TH-CMB-EVAP_CANISTER_SATU-gas_o2-gas_nox-mnmx | EVAP_CANISTER_SATURATED | (gas_o2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1199 | TH-CMB-EVAP_CANISTER_SATU-gas_o2-gas_nox-mxmn | EVAP_CANISTER_SATURATED | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1200 | TH-CMB-EVAP_CANISTER_SATU-gas_o2-gas_nox-mxmx | EVAP_CANISTER_SATURATED | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1201 | TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_co-mnmn | EGR_DILUTION_MISFIRE | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1202 | TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_co-mnmx | EGR_DILUTION_MISFIRE | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1203 | TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_co-mxmn | EGR_DILUTION_MISFIRE | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1204 | TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_co-mxmx | EGR_DILUTION_MISFIRE | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1205 | TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_co2-mnmn | EGR_DILUTION_MISFIRE | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1206 | TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_co2-mnmx | EGR_DILUTION_MISFIRE | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1207 | TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_co2-mxmn | EGR_DILUTION_MISFIRE | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1208 | TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_co2-mxmx | EGR_DILUTION_MISFIRE | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1209 | TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_o2-mnmn | EGR_DILUTION_MISFIRE | (gas_hc, gas_o2) | (mn, mn) | inside | CATALYST_OVERWHELMED | FAIL |
| 1210 | TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_o2-mnmx | EGR_DILUTION_MISFIRE | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1211 | TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_o2-mxmn | EGR_DILUTION_MISFIRE | (gas_hc, gas_o2) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 1212 | TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_o2-mxmx | EGR_DILUTION_MISFIRE | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1213 | TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_nox-mnmn | EGR_DILUTION_MISFIRE | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1214 | TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_nox-mnmx | EGR_DILUTION_MISFIRE | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1215 | TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_nox-mxmn | EGR_DILUTION_MISFIRE | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1216 | TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_nox-mxmx | EGR_DILUTION_MISFIRE | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1217 | TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_co2-mnmn | EGR_DILUTION_MISFIRE | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1218 | TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_co2-mnmx | EGR_DILUTION_MISFIRE | (gas_co, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1219 | TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_co2-mxmn | EGR_DILUTION_MISFIRE | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1220 | TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_co2-mxmx | EGR_DILUTION_MISFIRE | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1221 | TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_o2-mnmn | EGR_DILUTION_MISFIRE | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1222 | TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_o2-mnmx | EGR_DILUTION_MISFIRE | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1223 | TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_o2-mxmn | EGR_DILUTION_MISFIRE | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1224 | TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_o2-mxmx | EGR_DILUTION_MISFIRE | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1225 | TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_nox-mnmn | EGR_DILUTION_MISFIRE | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1226 | TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_nox-mnmx | EGR_DILUTION_MISFIRE | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1227 | TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_nox-mxmn | EGR_DILUTION_MISFIRE | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1228 | TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_nox-mxmx | EGR_DILUTION_MISFIRE | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1229 | TH-CMB-EGR_DILUTION_MISFI-gas_co2-gas_o2-mnmn | EGR_DILUTION_MISFIRE | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1230 | TH-CMB-EGR_DILUTION_MISFI-gas_co2-gas_o2-mnmx | EGR_DILUTION_MISFIRE | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1231 | TH-CMB-EGR_DILUTION_MISFI-gas_co2-gas_o2-mxmn | EGR_DILUTION_MISFIRE | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1232 | TH-CMB-EGR_DILUTION_MISFI-gas_co2-gas_o2-mxmx | EGR_DILUTION_MISFIRE | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1233 | TH-CMB-EGR_DILUTION_MISFI-gas_co2-gas_nox-mnmn | EGR_DILUTION_MISFIRE | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1234 | TH-CMB-EGR_DILUTION_MISFI-gas_co2-gas_nox-mnmx | EGR_DILUTION_MISFIRE | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1235 | TH-CMB-EGR_DILUTION_MISFI-gas_co2-gas_nox-mxmn | EGR_DILUTION_MISFIRE | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1236 | TH-CMB-EGR_DILUTION_MISFI-gas_co2-gas_nox-mxmx | EGR_DILUTION_MISFIRE | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1237 | TH-CMB-EGR_DILUTION_MISFI-gas_o2-gas_nox-mnmn | EGR_DILUTION_MISFIRE | (gas_o2, gas_nox) | (mn, mn) | inside | NORMAL_OPERATION | FAIL |
| 1238 | TH-CMB-EGR_DILUTION_MISFI-gas_o2-gas_nox-mnmx | EGR_DILUTION_MISFIRE | (gas_o2, gas_nox) | (mn, mx) | inside | NORMAL_OPERATION | FAIL |
| 1239 | TH-CMB-EGR_DILUTION_MISFI-gas_o2-gas_nox-mxmn | EGR_DILUTION_MISFIRE | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1240 | TH-CMB-EGR_DILUTION_MISFI-gas_o2-gas_nox-mxmx | EGR_DILUTION_MISFIRE | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1241 | TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_co-mnmn | INCOMPLETE_OXIDATION | (gas_hc, gas_co) | (mn, mn) | inside | RICH_MISFIRE | FAIL |
| 1242 | TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_co-mnmx | INCOMPLETE_OXIDATION | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1243 | TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_co-mxmn | INCOMPLETE_OXIDATION | (gas_hc, gas_co) | (mx, mn) | inside | RICH_MISFIRE | FAIL |
| 1244 | TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_co-mxmx | INCOMPLETE_OXIDATION | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1245 | TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_co2-mnmn | INCOMPLETE_OXIDATION | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1246 | TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_co2-mnmx | INCOMPLETE_OXIDATION | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1247 | TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_co2-mxmn | INCOMPLETE_OXIDATION | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1248 | TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_co2-mxmx | INCOMPLETE_OXIDATION | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1249 | TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_o2-mnmn | INCOMPLETE_OXIDATION | (gas_hc, gas_o2) | (mn, mn) | inside | CATALYST_OVERWHELMED | FAIL |
| 1250 | TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_o2-mnmx | INCOMPLETE_OXIDATION | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1251 | TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_o2-mxmn | INCOMPLETE_OXIDATION | (gas_hc, gas_o2) | (mx, mn) | inside | NORMAL_OPERATION | FAIL |
| 1252 | TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_o2-mxmx | INCOMPLETE_OXIDATION | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1253 | TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_nox-mnmn | INCOMPLETE_OXIDATION | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1254 | TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_nox-mnmx | INCOMPLETE_OXIDATION | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1255 | TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_nox-mxmn | INCOMPLETE_OXIDATION | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1256 | TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_nox-mxmx | INCOMPLETE_OXIDATION | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1257 | TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_co2-mnmn | INCOMPLETE_OXIDATION | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1258 | TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_co2-mnmx | INCOMPLETE_OXIDATION | (gas_co, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1259 | TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_co2-mxmn | INCOMPLETE_OXIDATION | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1260 | TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_co2-mxmx | INCOMPLETE_OXIDATION | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1261 | TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_o2-mnmn | INCOMPLETE_OXIDATION | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1262 | TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_o2-mnmx | INCOMPLETE_OXIDATION | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1263 | TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_o2-mxmn | INCOMPLETE_OXIDATION | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1264 | TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_o2-mxmx | INCOMPLETE_OXIDATION | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1265 | TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_nox-mnmn | INCOMPLETE_OXIDATION | (gas_co, gas_nox) | (mn, mn) | inside | IGNITION_MISFIRE | FAIL |
| 1266 | TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_nox-mnmx | INCOMPLETE_OXIDATION | (gas_co, gas_nox) | (mn, mx) | inside | RICH_MISFIRE | FAIL |
| 1267 | TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_nox-mxmn | INCOMPLETE_OXIDATION | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1268 | TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_nox-mxmx | INCOMPLETE_OXIDATION | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1269 | TH-CMB-INCOMPLETE_OXIDATI-gas_co2-gas_o2-mnmn | INCOMPLETE_OXIDATION | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1270 | TH-CMB-INCOMPLETE_OXIDATI-gas_co2-gas_o2-mnmx | INCOMPLETE_OXIDATION | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1271 | TH-CMB-INCOMPLETE_OXIDATI-gas_co2-gas_o2-mxmn | INCOMPLETE_OXIDATION | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1272 | TH-CMB-INCOMPLETE_OXIDATI-gas_co2-gas_o2-mxmx | INCOMPLETE_OXIDATION | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1273 | TH-CMB-INCOMPLETE_OXIDATI-gas_co2-gas_nox-mnmn | INCOMPLETE_OXIDATION | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1274 | TH-CMB-INCOMPLETE_OXIDATI-gas_co2-gas_nox-mnmx | INCOMPLETE_OXIDATION | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1275 | TH-CMB-INCOMPLETE_OXIDATI-gas_co2-gas_nox-mxmn | INCOMPLETE_OXIDATION | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1276 | TH-CMB-INCOMPLETE_OXIDATI-gas_co2-gas_nox-mxmx | INCOMPLETE_OXIDATION | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1277 | TH-CMB-INCOMPLETE_OXIDATI-gas_o2-gas_nox-mnmn | INCOMPLETE_OXIDATION | (gas_o2, gas_nox) | (mn, mn) | inside | NORMAL_OPERATION | FAIL |
| 1278 | TH-CMB-INCOMPLETE_OXIDATI-gas_o2-gas_nox-mnmx | INCOMPLETE_OXIDATION | (gas_o2, gas_nox) | (mn, mx) | inside | NORMAL_OPERATION | FAIL |
| 1279 | TH-CMB-INCOMPLETE_OXIDATI-gas_o2-gas_nox-mxmn | INCOMPLETE_OXIDATION | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1280 | TH-CMB-INCOMPLETE_OXIDATI-gas_o2-gas_nox-mxmx | INCOMPLETE_OXIDATION | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1281 | TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_co-mnmn | INCOMPLETE_COMBUSTION | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1282 | TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_co-mnmx | INCOMPLETE_COMBUSTION | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1283 | TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_co-mxmn | INCOMPLETE_COMBUSTION | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1284 | TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_co-mxmx | INCOMPLETE_COMBUSTION | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1285 | TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_co2-mnmn | INCOMPLETE_COMBUSTION | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1286 | TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_co2-mnmx | INCOMPLETE_COMBUSTION | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1287 | TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_co2-mxmn | INCOMPLETE_COMBUSTION | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1288 | TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_co2-mxmx | INCOMPLETE_COMBUSTION | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1289 | TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_o2-mnmn | INCOMPLETE_COMBUSTION | (gas_hc, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1290 | TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_o2-mnmx | INCOMPLETE_COMBUSTION | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1291 | TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_o2-mxmn | INCOMPLETE_COMBUSTION | (gas_hc, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1292 | TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_o2-mxmx | INCOMPLETE_COMBUSTION | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1293 | TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_nox-mnmn | INCOMPLETE_COMBUSTION | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1294 | TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_nox-mnmx | INCOMPLETE_COMBUSTION | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1295 | TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_nox-mxmn | INCOMPLETE_COMBUSTION | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1296 | TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_nox-mxmx | INCOMPLETE_COMBUSTION | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1297 | TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_co2-mnmn | INCOMPLETE_COMBUSTION | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1298 | TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_co2-mnmx | INCOMPLETE_COMBUSTION | (gas_co, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1299 | TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_co2-mxmn | INCOMPLETE_COMBUSTION | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1300 | TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_co2-mxmx | INCOMPLETE_COMBUSTION | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1301 | TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_o2-mnmn | INCOMPLETE_COMBUSTION | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1302 | TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_o2-mnmx | INCOMPLETE_COMBUSTION | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1303 | TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_o2-mxmn | INCOMPLETE_COMBUSTION | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1304 | TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_o2-mxmx | INCOMPLETE_COMBUSTION | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1305 | TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_nox-mnmn | INCOMPLETE_COMBUSTION | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1306 | TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_nox-mnmx | INCOMPLETE_COMBUSTION | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1307 | TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_nox-mxmn | INCOMPLETE_COMBUSTION | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1308 | TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_nox-mxmx | INCOMPLETE_COMBUSTION | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1309 | TH-CMB-INCOMPLETE_COMBUST-gas_co2-gas_o2-mnmn | INCOMPLETE_COMBUSTION | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1310 | TH-CMB-INCOMPLETE_COMBUST-gas_co2-gas_o2-mnmx | INCOMPLETE_COMBUSTION | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1311 | TH-CMB-INCOMPLETE_COMBUST-gas_co2-gas_o2-mxmn | INCOMPLETE_COMBUSTION | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1312 | TH-CMB-INCOMPLETE_COMBUST-gas_co2-gas_o2-mxmx | INCOMPLETE_COMBUSTION | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1313 | TH-CMB-INCOMPLETE_COMBUST-gas_co2-gas_nox-mnmn | INCOMPLETE_COMBUSTION | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1314 | TH-CMB-INCOMPLETE_COMBUST-gas_co2-gas_nox-mnmx | INCOMPLETE_COMBUSTION | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1315 | TH-CMB-INCOMPLETE_COMBUST-gas_co2-gas_nox-mxmn | INCOMPLETE_COMBUSTION | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1316 | TH-CMB-INCOMPLETE_COMBUST-gas_co2-gas_nox-mxmx | INCOMPLETE_COMBUSTION | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1317 | TH-CMB-INCOMPLETE_COMBUST-gas_o2-gas_nox-mnmn | INCOMPLETE_COMBUSTION | (gas_o2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1318 | TH-CMB-INCOMPLETE_COMBUST-gas_o2-gas_nox-mnmx | INCOMPLETE_COMBUSTION | (gas_o2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1319 | TH-CMB-INCOMPLETE_COMBUST-gas_o2-gas_nox-mxmn | INCOMPLETE_COMBUSTION | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1320 | TH-CMB-INCOMPLETE_COMBUST-gas_o2-gas_nox-mxmx | INCOMPLETE_COMBUSTION | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1321 | TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_co-mnmn | COOLANT_LEAK_INTERNAL | (gas_hc, gas_co) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1322 | TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_co-mnmx | COOLANT_LEAK_INTERNAL | (gas_hc, gas_co) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1323 | TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_co-mxmn | COOLANT_LEAK_INTERNAL | (gas_hc, gas_co) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1324 | TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_co-mxmx | COOLANT_LEAK_INTERNAL | (gas_hc, gas_co) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1325 | TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_co2-mnmn | COOLANT_LEAK_INTERNAL | (gas_hc, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1326 | TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_co2-mnmx | COOLANT_LEAK_INTERNAL | (gas_hc, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1327 | TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_co2-mxmn | COOLANT_LEAK_INTERNAL | (gas_hc, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1328 | TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_co2-mxmx | COOLANT_LEAK_INTERNAL | (gas_hc, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1329 | TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_o2-mnmn | COOLANT_LEAK_INTERNAL | (gas_hc, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1330 | TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_o2-mnmx | COOLANT_LEAK_INTERNAL | (gas_hc, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1331 | TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_o2-mxmn | COOLANT_LEAK_INTERNAL | (gas_hc, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1332 | TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_o2-mxmx | COOLANT_LEAK_INTERNAL | (gas_hc, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1333 | TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_nox-mnmn | COOLANT_LEAK_INTERNAL | (gas_hc, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1334 | TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_nox-mnmx | COOLANT_LEAK_INTERNAL | (gas_hc, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1335 | TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_nox-mxmn | COOLANT_LEAK_INTERNAL | (gas_hc, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1336 | TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_nox-mxmx | COOLANT_LEAK_INTERNAL | (gas_hc, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1337 | TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_co2-mnmn | COOLANT_LEAK_INTERNAL | (gas_co, gas_co2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1338 | TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_co2-mnmx | COOLANT_LEAK_INTERNAL | (gas_co, gas_co2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1339 | TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_co2-mxmn | COOLANT_LEAK_INTERNAL | (gas_co, gas_co2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1340 | TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_co2-mxmx | COOLANT_LEAK_INTERNAL | (gas_co, gas_co2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1341 | TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_o2-mnmn | COOLANT_LEAK_INTERNAL | (gas_co, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1342 | TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_o2-mnmx | COOLANT_LEAK_INTERNAL | (gas_co, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1343 | TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_o2-mxmn | COOLANT_LEAK_INTERNAL | (gas_co, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1344 | TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_o2-mxmx | COOLANT_LEAK_INTERNAL | (gas_co, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1345 | TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_nox-mnmn | COOLANT_LEAK_INTERNAL | (gas_co, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1346 | TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_nox-mnmx | COOLANT_LEAK_INTERNAL | (gas_co, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1347 | TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_nox-mxmn | COOLANT_LEAK_INTERNAL | (gas_co, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1348 | TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_nox-mxmx | COOLANT_LEAK_INTERNAL | (gas_co, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1349 | TH-CMB-COOLANT_LEAK_INTER-gas_co2-gas_o2-mnmn | COOLANT_LEAK_INTERNAL | (gas_co2, gas_o2) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1350 | TH-CMB-COOLANT_LEAK_INTER-gas_co2-gas_o2-mnmx | COOLANT_LEAK_INTERNAL | (gas_co2, gas_o2) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1351 | TH-CMB-COOLANT_LEAK_INTER-gas_co2-gas_o2-mxmn | COOLANT_LEAK_INTERNAL | (gas_co2, gas_o2) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1352 | TH-CMB-COOLANT_LEAK_INTER-gas_co2-gas_o2-mxmx | COOLANT_LEAK_INTERNAL | (gas_co2, gas_o2) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1353 | TH-CMB-COOLANT_LEAK_INTER-gas_co2-gas_nox-mnmn | COOLANT_LEAK_INTERNAL | (gas_co2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1354 | TH-CMB-COOLANT_LEAK_INTER-gas_co2-gas_nox-mnmx | COOLANT_LEAK_INTERNAL | (gas_co2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1355 | TH-CMB-COOLANT_LEAK_INTER-gas_co2-gas_nox-mxmn | COOLANT_LEAK_INTERNAL | (gas_co2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1356 | TH-CMB-COOLANT_LEAK_INTER-gas_co2-gas_nox-mxmx | COOLANT_LEAK_INTERNAL | (gas_co2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |
| 1357 | TH-CMB-COOLANT_LEAK_INTER-gas_o2-gas_nox-mnmn | COOLANT_LEAK_INTERNAL | (gas_o2, gas_nox) | (mn, mn) | inside | SAMPLE_INVALID | FAIL |
| 1358 | TH-CMB-COOLANT_LEAK_INTER-gas_o2-gas_nox-mnmx | COOLANT_LEAK_INTERNAL | (gas_o2, gas_nox) | (mn, mx) | inside | SAMPLE_INVALID | FAIL |
| 1359 | TH-CMB-COOLANT_LEAK_INTER-gas_o2-gas_nox-mxmn | COOLANT_LEAK_INTERNAL | (gas_o2, gas_nox) | (mx, mn) | inside | SAMPLE_INVALID | FAIL |
| 1360 | TH-CMB-COOLANT_LEAK_INTER-gas_o2-gas_nox-mxmx | COOLANT_LEAK_INTERNAL | (gas_o2, gas_nox) | (mx, mx) | inside | SAMPLE_INVALID | FAIL |

## Failures

- **TH-CMB-NORMAL_OPERATION-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-NORMAL_OPERATION-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-NORMAL_OPERATION-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=WORN_PISTON_RINGS
- **TH-CMB-NORMAL_OPERATION-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=WORN_PISTON_RINGS
- **TH-CMB-NORMAL_OPERATION-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-NORMAL_OPERATION-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-NORMAL_OPERATION-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=WORN_PISTON_RINGS
- **TH-CMB-NORMAL_OPERATION-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=WORN_PISTON_RINGS
- **TH-CMB-NORMAL_OPERATION-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-NORMAL_OPERATION-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-NORMAL_OPERATION-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-NORMAL_OPERATION-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-NORMAL_OPERATION-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=WORN_PISTON_RINGS
- **TH-CMB-NORMAL_OPERATION-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=WORN_PISTON_RINGS
- **TH-CMB-NORMAL_OPERATION-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-NORMAL_OPERATION-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=WORN_PISTON_RINGS
- **TH-CMB-RICH_MIXTURE-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-RICH_MIXTURE-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-RICH_MIXTURE-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=POA_SIGNATURE
- **TH-CMB-RICH_MIXTURE-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=POA_SIGNATURE
- **TH-CMB-RICH_MIXTURE-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-RICH_MIXTURE-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=VACUUM_REGULATOR_DIAPHRAGM_RUPTURE
- **TH-CMB-RICH_MIXTURE-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=CATALYST_OVERWHELMED
- **TH-CMB-RICH_MIXTURE-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-RICH_MIXTURE-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-RICH_MIXTURE-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MIXTURE-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=CATALYST_OVERWHELMED
- **TH-CMB-RICH_MIXTURE-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=CATALYST_OVERWHELMED
- **TH-CMB-LEAN_MIXTURE-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=EXHAUST_AIR_LEAK
- **TH-CMB-LEAN_MIXTURE-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=EXHAUST_AIR_LEAK
- **TH-CMB-LEAN_MIXTURE-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-LEAN_MIXTURE-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MIXTURE-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-IGNITION_MISFIRE-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-LEAN_MISFIRE-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-RICH_MISFIRE-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-RICH_MISFIRE-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-EXHAUST_AIR_LEAK-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-EXHAUST_AIR_LEAK-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EXHAUST_AIR_LEAK-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=TIMING_OVER_ADVANCED
- **TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=TIMING_OVER_ADVANCED
- **TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-HIGH_COMBUSTION_TE-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=TIMING_OVER_ADVANCED
- **TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=TIMING_OVER_ADVANCED
- **TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=TIMING_OVER_ADVANCED
- **TH-CMB-HIGH_COMBUSTION_TE-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=TIMING_OVER_ADVANCED
- **TH-CMB-HIGH_COMBUSTION_TE-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-HIGH_COMBUSTION_TE-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-HIGH_COMBUSTION_TE-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-HIGH_COMBUSTION_TE-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-HIGH_COMBUSTION_TE-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=O2_SENSOR_BIASED_LOW
- **TH-CMB-CATALYST_NOT_LIGHT-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_NOT_LIGHT-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-CATALYST_OVERWHELM-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-CATALYST_OVERWHELM-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-CATALYST_OVERWHELM-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-CATALYST_OVERWHELM-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CATALYST_OVERWHELM-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-CATALYST_OVERWHELM-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-CATALYST_OVERWHELM-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-CATALYST_OVERWHELM-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-TIMING_OVER_ADVANC-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-TIMING_OVER_ADVANC-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-TIMING_OVER_ADVANC-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-TIMING_OVER_ADVANC-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-TIMING_OVER_ADVANC-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-TIMING_RETARDED-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-TIMING_RETARDED-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-TIMING_RETARDED-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-TIMING_RETARDED-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-TIMING_RETARDED-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-TIMING_RETARDED-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-TIMING_RETARDED-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-TIMING_RETARDED-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=EVAP_CANISTER_SATURATED
- **TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-O2_SENSOR_BIASED_L-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_L-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-O2_SENSOR_BIASED_H-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-O2_SENSOR_BIASED_H-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-O2_SENSOR_BIASED_H-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_ENGINE-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-WORN_ENGINE-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=O2_SENSOR_BIASED_LOW
- **TH-CMB-WORN_ENGINE-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_ENGINE-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_ENGINE-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_ENGINE-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=O2_SENSOR_BIASED_LOW
- **TH-CMB-WORN_ENGINE-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_ENGINE-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_ENGINE-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=O2_SENSOR_BIASED_LOW
- **TH-CMB-WORN_ENGINE-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=O2_SENSOR_BIASED_LOW
- **TH-CMB-WORN_ENGINE-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_ENGINE-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_ENGINE-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=O2_SENSOR_BIASED_LOW
- **TH-CMB-WORN_ENGINE-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=O2_SENSOR_BIASED_LOW
- **TH-CMB-WORN_ENGINE-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_ENGINE-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_ENGINE-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_ENGINE-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=RICH_MIXTURE
- **TH-CMB-WORN_ENGINE-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_ENGINE-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_ENGINE-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=WORN_VALVE_SEALS
- **TH-CMB-WORN_ENGINE-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_ENGINE-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_ENGINE-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=WORN_VALVE_SEALS
- **TH-CMB-WORN_ENGINE-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=WORN_VALVE_SEALS
- **TH-CMB-WORN_ENGINE-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_ENGINE-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_ENGINE-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_ENGINE-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_ENGINE-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_ENGINE-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_ENGINE-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_ENGINE-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_ENGINE-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_ENGINE-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_ENGINE-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=WORN_PISTON_RINGS
- **TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=WORN_PISTON_RINGS
- **TH-CMB-FLAT_CAMSHAFT-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-FLAT_CAMSHAFT-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-FLAT_CAMSHAFT-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=WORN_PISTON_RINGS
- **TH-CMB-FLAT_CAMSHAFT-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=WORN_PISTON_RINGS
- **TH-CMB-FLAT_CAMSHAFT-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-FLAT_CAMSHAFT-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-FLAT_CAMSHAFT-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-FLAT_CAMSHAFT-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-FLAT_CAMSHAFT-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=WORN_PISTON_RINGS
- **TH-CMB-FLAT_CAMSHAFT-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=WORN_PISTON_RINGS
- **TH-CMB-FLAT_CAMSHAFT-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-FLAT_CAMSHAFT-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=WORN_PISTON_RINGS
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=EXHAUST_AIR_LEAK
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_INTAKE_VALVE_C-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=CATALYST_OVERWHELMED
- **TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=CATALYST_OVERWHELMED
- **TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=RICH_MIXTURE
- **TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=CATALYST_OVERWHELMED
- **TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-VACUUM_REGULATOR_D-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VACUUM_REGULATOR_D-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-VACUUM_REGULATOR_D-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-VACUUM_REGULATOR_D-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-VACUUM_REGULATOR_D-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=CATALYST_OVERWHELMED
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=CATALYST_OVERWHELMED
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=RICH_MIXTURE
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=CATALYST_OVERWHELMED
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-GDI_HPFP_INTERNAL_-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_VALVE_SEALS-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_VALVE_SEALS-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_VALVE_SEALS-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_VALVE_SEALS-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-WORN_VALVE_SEALS-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_VALVE_SEALS-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-WORN_PISTON_RINGS-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=TIMING_RETARDED
- **TH-CMB-POA_SIGNATURE-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=CATALYST_OVERWHELMED
- **TH-CMB-POA_SIGNATURE-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-POA_SIGNATURE-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-POA_SIGNATURE-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-POA_SIGNATURE-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-POA_SIGNATURE-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_RETARDE-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-CAM_TIMING_ADVANCE-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=TIMING_OVER_ADVANCED
- **TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=TIMING_OVER_ADVANCED
- **TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=TIMING_OVER_ADVANCED
- **TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=TIMING_OVER_ADVANCED
- **TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=TIMING_OVER_ADVANCED
- **TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=TIMING_OVER_ADVANCED
- **TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_CLOSED-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_CLOSED-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_CLOSED-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_CLOSED-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-CMB-EGR_STUCK_CLOSED-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=RICH_MIXTURE
- **TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=VVT_FAILURE
- **TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-EGR_STUCK_OPEN-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-EGR_STUCK_OPEN-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-EGR_STUCK_OPEN-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-EGR_STUCK_OPEN-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_STUCK_OPEN-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-EGR_STUCK_OPEN-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-EGR_STUCK_OPEN-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-EGR_STUCK_OPEN-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-VVT_FAILURE-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-VVT_FAILURE-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=RICH_MIXTURE
- **TH-CMB-EVAP_CANISTER_SATU-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EVAP_CANISTER_SATU-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=CATALYST_OVERWHELMED
- **TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-EGR_DILUTION_MISFI-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-EGR_DILUTION_MISFI-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-EGR_DILUTION_MISFI-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=RICH_MISFIRE
- **TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=RICH_MISFIRE
- **TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=CATALYST_OVERWHELMED
- **TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=IGNITION_MISFIRE
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=RICH_MISFIRE
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-INCOMPLETE_OXIDATI-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=NORMAL_OPERATION
- **TH-CMB-INCOMPLETE_OXIDATI-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_OXIDATI-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-INCOMPLETE_COMBUST-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_co-mnmn:** (gas_hc, gas_co) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_co-mnmx:** (gas_hc, gas_co) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_co-mxmn:** (gas_hc, gas_co) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_co-mxmx:** (gas_hc, gas_co) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_co2-mnmn:** (gas_hc, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_co2-mnmx:** (gas_hc, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_co2-mxmn:** (gas_hc, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_co2-mxmx:** (gas_hc, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_o2-mnmn:** (gas_hc, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_o2-mnmx:** (gas_hc, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_o2-mxmn:** (gas_hc, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_o2-mxmx:** (gas_hc, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_nox-mnmn:** (gas_hc, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_nox-mnmx:** (gas_hc, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_nox-mxmn:** (gas_hc, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_hc-gas_nox-mxmx:** (gas_hc, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_co2-mnmn:** (gas_co, gas_co2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_co2-mnmx:** (gas_co, gas_co2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_co2-mxmn:** (gas_co, gas_co2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_co2-mxmx:** (gas_co, gas_co2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_o2-mnmn:** (gas_co, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_o2-mnmx:** (gas_co, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_o2-mxmn:** (gas_co, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_o2-mxmx:** (gas_co, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_nox-mnmn:** (gas_co, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_nox-mnmx:** (gas_co, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_nox-mxmn:** (gas_co, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co-gas_nox-mxmx:** (gas_co, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co2-gas_o2-mnmn:** (gas_co2, gas_o2) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co2-gas_o2-mnmx:** (gas_co2, gas_o2) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co2-gas_o2-mxmn:** (gas_co2, gas_o2) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co2-gas_o2-mxmx:** (gas_co2, gas_o2) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co2-gas_nox-mnmn:** (gas_co2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co2-gas_nox-mnmx:** (gas_co2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co2-gas_nox-mxmn:** (gas_co2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_co2-gas_nox-mxmx:** (gas_co2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_o2-gas_nox-mnmn:** (gas_o2, gas_nox) corner (mn, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_o2-gas_nox-mnmx:** (gas_o2, gas_nox) corner (mn, mx), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_o2-gas_nox-mxmn:** (gas_o2, gas_nox) corner (mx, mn), oracle=inside, actual=SAMPLE_INVALID
- **TH-CMB-COOLANT_LEAK_INTER-gas_o2-gas_nox-mxmx:** (gas_o2, gas_nox) corner (mx, mx), oracle=inside, actual=SAMPLE_INVALID

