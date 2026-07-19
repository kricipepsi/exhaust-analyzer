# Boundary Generator Report

**Date:** 2026-06-07  
**Total cases:** 1020  
**PASS:** 427 | **FAIL:** 593  

**427/1020** boundary points match geometric oracle (41.9%).  
**593 mismatch(es)**.

**Overlap caveat:** mismatches may be caused by overlapping fault boxes (to be analyzed in T-TH-2). A FAIL with oracle=inside means the classifier returned a different signature for a point geometrically inside this box — which may be correct if the point also falls inside another box.

## Results

| # | case_id | Box | Dim | Position | Oracle | Actual | Match |
|---|---|---|---|---|---|---|---|
| 1 | TH-BND-NORMAL_OPERATION-gas_hc-min-eps | NORMAL_OPERATION | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 2 | TH-BND-NORMAL_OPERATION-gas_hc-min | NORMAL_OPERATION | gas_hc | min | inside | TIMING_RETARDED | FAIL |
| 3 | TH-BND-NORMAL_OPERATION-gas_hc-min+eps | NORMAL_OPERATION | gas_hc | min+eps | inside | TIMING_RETARDED | FAIL |
| 4 | TH-BND-NORMAL_OPERATION-gas_hc-max-eps | NORMAL_OPERATION | gas_hc | max-eps | inside | TIMING_RETARDED | FAIL |
| 5 | TH-BND-NORMAL_OPERATION-gas_hc-max | NORMAL_OPERATION | gas_hc | max | inside | TIMING_RETARDED | FAIL |
| 6 | TH-BND-NORMAL_OPERATION-gas_hc-max+eps | NORMAL_OPERATION | gas_hc | max+eps | outside | WORN_VALVE_SEALS | PASS |
| 7 | TH-BND-NORMAL_OPERATION-gas_co-min-eps | NORMAL_OPERATION | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 8 | TH-BND-NORMAL_OPERATION-gas_co-min | NORMAL_OPERATION | gas_co | min | inside | TIMING_RETARDED | FAIL |
| 9 | TH-BND-NORMAL_OPERATION-gas_co-min+eps | NORMAL_OPERATION | gas_co | min+eps | inside | TIMING_RETARDED | FAIL |
| 10 | TH-BND-NORMAL_OPERATION-gas_co-max-eps | NORMAL_OPERATION | gas_co | max-eps | inside | TIMING_RETARDED | FAIL |
| 11 | TH-BND-NORMAL_OPERATION-gas_co-max | NORMAL_OPERATION | gas_co | max | inside | TIMING_RETARDED | FAIL |
| 12 | TH-BND-NORMAL_OPERATION-gas_co-max+eps | NORMAL_OPERATION | gas_co | max+eps | outside | O2_SENSOR_BIASED_LOW | PASS |
| 13 | TH-BND-NORMAL_OPERATION-gas_co2-min-eps | NORMAL_OPERATION | gas_co2 | min-eps | outside | SAMPLE_INVALID | PASS |
| 14 | TH-BND-NORMAL_OPERATION-gas_co2-min | NORMAL_OPERATION | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 15 | TH-BND-NORMAL_OPERATION-gas_co2-min+eps | NORMAL_OPERATION | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 16 | TH-BND-NORMAL_OPERATION-gas_co2-max-eps | NORMAL_OPERATION | gas_co2 | max-eps | inside | TIMING_RETARDED | FAIL |
| 17 | TH-BND-NORMAL_OPERATION-gas_co2-max | NORMAL_OPERATION | gas_co2 | max | inside | TIMING_RETARDED | FAIL |
| 18 | TH-BND-NORMAL_OPERATION-gas_co2-max+eps | NORMAL_OPERATION | gas_co2 | max+eps | outside | NORMAL_OPERATION | FAIL |
| 19 | TH-BND-NORMAL_OPERATION-gas_o2-min-eps | NORMAL_OPERATION | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 20 | TH-BND-NORMAL_OPERATION-gas_o2-min | NORMAL_OPERATION | gas_o2 | min | inside | TIMING_RETARDED | FAIL |
| 21 | TH-BND-NORMAL_OPERATION-gas_o2-min+eps | NORMAL_OPERATION | gas_o2 | min+eps | inside | TIMING_RETARDED | FAIL |
| 22 | TH-BND-NORMAL_OPERATION-gas_o2-max-eps | NORMAL_OPERATION | gas_o2 | max-eps | inside | TIMING_RETARDED | FAIL |
| 23 | TH-BND-NORMAL_OPERATION-gas_o2-max | NORMAL_OPERATION | gas_o2 | max | inside | TIMING_RETARDED | FAIL |
| 24 | TH-BND-NORMAL_OPERATION-gas_o2-max+eps | NORMAL_OPERATION | gas_o2 | max+eps | outside | VVT_FAILURE | PASS |
| 25 | TH-BND-NORMAL_OPERATION-gas_nox-min-eps | NORMAL_OPERATION | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 26 | TH-BND-NORMAL_OPERATION-gas_nox-min | NORMAL_OPERATION | gas_nox | min | inside | TIMING_RETARDED | FAIL |
| 27 | TH-BND-NORMAL_OPERATION-gas_nox-min+eps | NORMAL_OPERATION | gas_nox | min+eps | inside | TIMING_RETARDED | FAIL |
| 28 | TH-BND-NORMAL_OPERATION-gas_nox-max-eps | NORMAL_OPERATION | gas_nox | max-eps | inside | WORN_PISTON_RINGS | FAIL |
| 29 | TH-BND-NORMAL_OPERATION-gas_nox-max | NORMAL_OPERATION | gas_nox | max | inside | WORN_PISTON_RINGS | FAIL |
| 30 | TH-BND-NORMAL_OPERATION-gas_nox-max+eps | NORMAL_OPERATION | gas_nox | max+eps | outside | VVT_FAILURE | PASS |
| 31 | TH-BND-RICH_MIXTURE-gas_hc-min-eps | RICH_MIXTURE | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 32 | TH-BND-RICH_MIXTURE-gas_hc-min | RICH_MIXTURE | gas_hc | min | inside | VVT_FAILURE | FAIL |
| 33 | TH-BND-RICH_MIXTURE-gas_hc-min+eps | RICH_MIXTURE | gas_hc | min+eps | inside | VVT_FAILURE | FAIL |
| 34 | TH-BND-RICH_MIXTURE-gas_hc-max-eps | RICH_MIXTURE | gas_hc | max-eps | inside | INCOMPLETE_OXIDATION | FAIL |
| 35 | TH-BND-RICH_MIXTURE-gas_hc-max | RICH_MIXTURE | gas_hc | max | inside | POA_SIGNATURE | FAIL |
| 36 | TH-BND-RICH_MIXTURE-gas_hc-max+eps | RICH_MIXTURE | gas_hc | max+eps | outside | POA_SIGNATURE | PASS |
| 37 | TH-BND-RICH_MIXTURE-gas_co-min-eps | RICH_MIXTURE | gas_co | min-eps | outside | SAMPLE_INVALID | PASS |
| 38 | TH-BND-RICH_MIXTURE-gas_co-min | RICH_MIXTURE | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 39 | TH-BND-RICH_MIXTURE-gas_co-min+eps | RICH_MIXTURE | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 40 | TH-BND-RICH_MIXTURE-gas_co-max-eps | RICH_MIXTURE | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 41 | TH-BND-RICH_MIXTURE-gas_co-max | RICH_MIXTURE | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 42 | TH-BND-RICH_MIXTURE-gas_co-max+eps | RICH_MIXTURE | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 43 | TH-BND-RICH_MIXTURE-gas_co2-min-eps | RICH_MIXTURE | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 44 | TH-BND-RICH_MIXTURE-gas_co2-min | RICH_MIXTURE | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 45 | TH-BND-RICH_MIXTURE-gas_co2-min+eps | RICH_MIXTURE | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 46 | TH-BND-RICH_MIXTURE-gas_co2-max-eps | RICH_MIXTURE | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 47 | TH-BND-RICH_MIXTURE-gas_co2-max | RICH_MIXTURE | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 48 | TH-BND-RICH_MIXTURE-gas_co2-max+eps | RICH_MIXTURE | gas_co2 | max+eps | outside | SAMPLE_INVALID | PASS |
| 49 | TH-BND-RICH_MIXTURE-gas_o2-min-eps | RICH_MIXTURE | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 50 | TH-BND-RICH_MIXTURE-gas_o2-min | RICH_MIXTURE | gas_o2 | min | inside | INCOMPLETE_OXIDATION | FAIL |
| 51 | TH-BND-RICH_MIXTURE-gas_o2-min+eps | RICH_MIXTURE | gas_o2 | min+eps | inside | INCOMPLETE_OXIDATION | FAIL |
| 52 | TH-BND-RICH_MIXTURE-gas_o2-max-eps | RICH_MIXTURE | gas_o2 | max-eps | inside | INCOMPLETE_OXIDATION | FAIL |
| 53 | TH-BND-RICH_MIXTURE-gas_o2-max | RICH_MIXTURE | gas_o2 | max | inside | INCOMPLETE_OXIDATION | FAIL |
| 54 | TH-BND-RICH_MIXTURE-gas_o2-max+eps | RICH_MIXTURE | gas_o2 | max+eps | outside | INCOMPLETE_OXIDATION | PASS |
| 55 | TH-BND-RICH_MIXTURE-gas_nox-min-eps | RICH_MIXTURE | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 56 | TH-BND-RICH_MIXTURE-gas_nox-min | RICH_MIXTURE | gas_nox | min | inside | RICH_MIXTURE | PASS |
| 57 | TH-BND-RICH_MIXTURE-gas_nox-min+eps | RICH_MIXTURE | gas_nox | min+eps | inside | RICH_MIXTURE | PASS |
| 58 | TH-BND-RICH_MIXTURE-gas_nox-max-eps | RICH_MIXTURE | gas_nox | max-eps | inside | INCOMPLETE_OXIDATION | FAIL |
| 59 | TH-BND-RICH_MIXTURE-gas_nox-max | RICH_MIXTURE | gas_nox | max | inside | CATALYST_OVERWHELMED | FAIL |
| 60 | TH-BND-RICH_MIXTURE-gas_nox-max+eps | RICH_MIXTURE | gas_nox | max+eps | outside | CATALYST_OVERWHELMED | PASS |
| 61 | TH-BND-LEAN_MIXTURE-gas_hc-min-eps | LEAN_MIXTURE | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 62 | TH-BND-LEAN_MIXTURE-gas_hc-min | LEAN_MIXTURE | gas_hc | min | inside | SAMPLE_INVALID | FAIL |
| 63 | TH-BND-LEAN_MIXTURE-gas_hc-min+eps | LEAN_MIXTURE | gas_hc | min+eps | inside | SAMPLE_INVALID | FAIL |
| 64 | TH-BND-LEAN_MIXTURE-gas_hc-max-eps | LEAN_MIXTURE | gas_hc | max-eps | inside | SAMPLE_INVALID | FAIL |
| 65 | TH-BND-LEAN_MIXTURE-gas_hc-max | LEAN_MIXTURE | gas_hc | max | inside | SAMPLE_INVALID | FAIL |
| 66 | TH-BND-LEAN_MIXTURE-gas_hc-max+eps | LEAN_MIXTURE | gas_hc | max+eps | outside | SAMPLE_INVALID | PASS |
| 67 | TH-BND-LEAN_MIXTURE-gas_co-min-eps | LEAN_MIXTURE | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 68 | TH-BND-LEAN_MIXTURE-gas_co-min | LEAN_MIXTURE | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 69 | TH-BND-LEAN_MIXTURE-gas_co-min+eps | LEAN_MIXTURE | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 70 | TH-BND-LEAN_MIXTURE-gas_co-max-eps | LEAN_MIXTURE | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 71 | TH-BND-LEAN_MIXTURE-gas_co-max | LEAN_MIXTURE | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 72 | TH-BND-LEAN_MIXTURE-gas_co-max+eps | LEAN_MIXTURE | gas_co | max+eps | outside | SAMPLE_INVALID | PASS |
| 73 | TH-BND-LEAN_MIXTURE-gas_co2-min-eps | LEAN_MIXTURE | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 74 | TH-BND-LEAN_MIXTURE-gas_co2-min | LEAN_MIXTURE | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 75 | TH-BND-LEAN_MIXTURE-gas_co2-min+eps | LEAN_MIXTURE | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 76 | TH-BND-LEAN_MIXTURE-gas_co2-max-eps | LEAN_MIXTURE | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 77 | TH-BND-LEAN_MIXTURE-gas_co2-max | LEAN_MIXTURE | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 78 | TH-BND-LEAN_MIXTURE-gas_co2-max+eps | LEAN_MIXTURE | gas_co2 | max+eps | outside | SAMPLE_INVALID | PASS |
| 79 | TH-BND-LEAN_MIXTURE-gas_o2-min-eps | LEAN_MIXTURE | gas_o2 | min-eps | outside | SAMPLE_INVALID | PASS |
| 80 | TH-BND-LEAN_MIXTURE-gas_o2-min | LEAN_MIXTURE | gas_o2 | min | inside | SAMPLE_INVALID | FAIL |
| 81 | TH-BND-LEAN_MIXTURE-gas_o2-min+eps | LEAN_MIXTURE | gas_o2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 82 | TH-BND-LEAN_MIXTURE-gas_o2-max-eps | LEAN_MIXTURE | gas_o2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 83 | TH-BND-LEAN_MIXTURE-gas_o2-max | LEAN_MIXTURE | gas_o2 | max | inside | SAMPLE_INVALID | FAIL |
| 84 | TH-BND-LEAN_MIXTURE-gas_o2-max+eps | LEAN_MIXTURE | gas_o2 | max+eps | outside | ERROR:ValueError | PASS |
| 85 | TH-BND-LEAN_MIXTURE-gas_nox-min-eps | LEAN_MIXTURE | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 86 | TH-BND-LEAN_MIXTURE-gas_nox-min | LEAN_MIXTURE | gas_nox | min | inside | SAMPLE_INVALID | FAIL |
| 87 | TH-BND-LEAN_MIXTURE-gas_nox-min+eps | LEAN_MIXTURE | gas_nox | min+eps | inside | SAMPLE_INVALID | FAIL |
| 88 | TH-BND-LEAN_MIXTURE-gas_nox-max-eps | LEAN_MIXTURE | gas_nox | max-eps | inside | SAMPLE_INVALID | FAIL |
| 89 | TH-BND-LEAN_MIXTURE-gas_nox-max | LEAN_MIXTURE | gas_nox | max | inside | SAMPLE_INVALID | FAIL |
| 90 | TH-BND-LEAN_MIXTURE-gas_nox-max+eps | LEAN_MIXTURE | gas_nox | max+eps | outside | SAMPLE_INVALID | PASS |
| 91 | TH-BND-IGNITION_MISFIRE-gas_hc-min-eps | IGNITION_MISFIRE | gas_hc | min-eps | outside | SAMPLE_INVALID | PASS |
| 92 | TH-BND-IGNITION_MISFIRE-gas_hc-min | IGNITION_MISFIRE | gas_hc | min | inside | SAMPLE_INVALID | FAIL |
| 93 | TH-BND-IGNITION_MISFIRE-gas_hc-min+eps | IGNITION_MISFIRE | gas_hc | min+eps | inside | SAMPLE_INVALID | FAIL |
| 94 | TH-BND-IGNITION_MISFIRE-gas_hc-max-eps | IGNITION_MISFIRE | gas_hc | max-eps | inside | SAMPLE_INVALID | FAIL |
| 95 | TH-BND-IGNITION_MISFIRE-gas_hc-max | IGNITION_MISFIRE | gas_hc | max | inside | SAMPLE_INVALID | FAIL |
| 96 | TH-BND-IGNITION_MISFIRE-gas_hc-max+eps | IGNITION_MISFIRE | gas_hc | max+eps | outside | ERROR:ValueError | PASS |
| 97 | TH-BND-IGNITION_MISFIRE-gas_co-min-eps | IGNITION_MISFIRE | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 98 | TH-BND-IGNITION_MISFIRE-gas_co-min | IGNITION_MISFIRE | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 99 | TH-BND-IGNITION_MISFIRE-gas_co-min+eps | IGNITION_MISFIRE | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 100 | TH-BND-IGNITION_MISFIRE-gas_co-max-eps | IGNITION_MISFIRE | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 101 | TH-BND-IGNITION_MISFIRE-gas_co-max | IGNITION_MISFIRE | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 102 | TH-BND-IGNITION_MISFIRE-gas_co-max+eps | IGNITION_MISFIRE | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 103 | TH-BND-IGNITION_MISFIRE-gas_co2-min-eps | IGNITION_MISFIRE | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 104 | TH-BND-IGNITION_MISFIRE-gas_co2-min | IGNITION_MISFIRE | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 105 | TH-BND-IGNITION_MISFIRE-gas_co2-min+eps | IGNITION_MISFIRE | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 106 | TH-BND-IGNITION_MISFIRE-gas_co2-max-eps | IGNITION_MISFIRE | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 107 | TH-BND-IGNITION_MISFIRE-gas_co2-max | IGNITION_MISFIRE | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 108 | TH-BND-IGNITION_MISFIRE-gas_co2-max+eps | IGNITION_MISFIRE | gas_co2 | max+eps | outside | SAMPLE_INVALID | PASS |
| 109 | TH-BND-IGNITION_MISFIRE-gas_o2-min-eps | IGNITION_MISFIRE | gas_o2 | min-eps | outside | SAMPLE_INVALID | PASS |
| 110 | TH-BND-IGNITION_MISFIRE-gas_o2-min | IGNITION_MISFIRE | gas_o2 | min | inside | SAMPLE_INVALID | FAIL |
| 111 | TH-BND-IGNITION_MISFIRE-gas_o2-min+eps | IGNITION_MISFIRE | gas_o2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 112 | TH-BND-IGNITION_MISFIRE-gas_o2-max-eps | IGNITION_MISFIRE | gas_o2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 113 | TH-BND-IGNITION_MISFIRE-gas_o2-max | IGNITION_MISFIRE | gas_o2 | max | inside | SAMPLE_INVALID | FAIL |
| 114 | TH-BND-IGNITION_MISFIRE-gas_o2-max+eps | IGNITION_MISFIRE | gas_o2 | max+eps | outside | ERROR:ValueError | PASS |
| 115 | TH-BND-IGNITION_MISFIRE-gas_nox-min-eps | IGNITION_MISFIRE | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 116 | TH-BND-IGNITION_MISFIRE-gas_nox-min | IGNITION_MISFIRE | gas_nox | min | inside | SAMPLE_INVALID | FAIL |
| 117 | TH-BND-IGNITION_MISFIRE-gas_nox-min+eps | IGNITION_MISFIRE | gas_nox | min+eps | inside | SAMPLE_INVALID | FAIL |
| 118 | TH-BND-IGNITION_MISFIRE-gas_nox-max-eps | IGNITION_MISFIRE | gas_nox | max-eps | inside | SAMPLE_INVALID | FAIL |
| 119 | TH-BND-IGNITION_MISFIRE-gas_nox-max | IGNITION_MISFIRE | gas_nox | max | inside | SAMPLE_INVALID | FAIL |
| 120 | TH-BND-IGNITION_MISFIRE-gas_nox-max+eps | IGNITION_MISFIRE | gas_nox | max+eps | outside | SAMPLE_INVALID | PASS |
| 121 | TH-BND-LEAN_MISFIRE-gas_hc-min-eps | LEAN_MISFIRE | gas_hc | min-eps | outside | SAMPLE_INVALID | PASS |
| 122 | TH-BND-LEAN_MISFIRE-gas_hc-min | LEAN_MISFIRE | gas_hc | min | inside | SAMPLE_INVALID | FAIL |
| 123 | TH-BND-LEAN_MISFIRE-gas_hc-min+eps | LEAN_MISFIRE | gas_hc | min+eps | inside | SAMPLE_INVALID | FAIL |
| 124 | TH-BND-LEAN_MISFIRE-gas_hc-max-eps | LEAN_MISFIRE | gas_hc | max-eps | inside | SAMPLE_INVALID | FAIL |
| 125 | TH-BND-LEAN_MISFIRE-gas_hc-max | LEAN_MISFIRE | gas_hc | max | inside | SAMPLE_INVALID | FAIL |
| 126 | TH-BND-LEAN_MISFIRE-gas_hc-max+eps | LEAN_MISFIRE | gas_hc | max+eps | outside | SAMPLE_INVALID | PASS |
| 127 | TH-BND-LEAN_MISFIRE-gas_co-min-eps | LEAN_MISFIRE | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 128 | TH-BND-LEAN_MISFIRE-gas_co-min | LEAN_MISFIRE | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 129 | TH-BND-LEAN_MISFIRE-gas_co-min+eps | LEAN_MISFIRE | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 130 | TH-BND-LEAN_MISFIRE-gas_co-max-eps | LEAN_MISFIRE | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 131 | TH-BND-LEAN_MISFIRE-gas_co-max | LEAN_MISFIRE | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 132 | TH-BND-LEAN_MISFIRE-gas_co-max+eps | LEAN_MISFIRE | gas_co | max+eps | outside | SAMPLE_INVALID | PASS |
| 133 | TH-BND-LEAN_MISFIRE-gas_co2-min-eps | LEAN_MISFIRE | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 134 | TH-BND-LEAN_MISFIRE-gas_co2-min | LEAN_MISFIRE | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 135 | TH-BND-LEAN_MISFIRE-gas_co2-min+eps | LEAN_MISFIRE | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 136 | TH-BND-LEAN_MISFIRE-gas_co2-max-eps | LEAN_MISFIRE | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 137 | TH-BND-LEAN_MISFIRE-gas_co2-max | LEAN_MISFIRE | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 138 | TH-BND-LEAN_MISFIRE-gas_co2-max+eps | LEAN_MISFIRE | gas_co2 | max+eps | outside | SAMPLE_INVALID | PASS |
| 139 | TH-BND-LEAN_MISFIRE-gas_o2-min-eps | LEAN_MISFIRE | gas_o2 | min-eps | outside | SAMPLE_INVALID | PASS |
| 140 | TH-BND-LEAN_MISFIRE-gas_o2-min | LEAN_MISFIRE | gas_o2 | min | inside | SAMPLE_INVALID | FAIL |
| 141 | TH-BND-LEAN_MISFIRE-gas_o2-min+eps | LEAN_MISFIRE | gas_o2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 142 | TH-BND-LEAN_MISFIRE-gas_o2-max-eps | LEAN_MISFIRE | gas_o2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 143 | TH-BND-LEAN_MISFIRE-gas_o2-max | LEAN_MISFIRE | gas_o2 | max | inside | SAMPLE_INVALID | FAIL |
| 144 | TH-BND-LEAN_MISFIRE-gas_o2-max+eps | LEAN_MISFIRE | gas_o2 | max+eps | outside | ERROR:ValueError | PASS |
| 145 | TH-BND-LEAN_MISFIRE-gas_nox-min-eps | LEAN_MISFIRE | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 146 | TH-BND-LEAN_MISFIRE-gas_nox-min | LEAN_MISFIRE | gas_nox | min | inside | SAMPLE_INVALID | FAIL |
| 147 | TH-BND-LEAN_MISFIRE-gas_nox-min+eps | LEAN_MISFIRE | gas_nox | min+eps | inside | SAMPLE_INVALID | FAIL |
| 148 | TH-BND-LEAN_MISFIRE-gas_nox-max-eps | LEAN_MISFIRE | gas_nox | max-eps | inside | SAMPLE_INVALID | FAIL |
| 149 | TH-BND-LEAN_MISFIRE-gas_nox-max | LEAN_MISFIRE | gas_nox | max | inside | SAMPLE_INVALID | FAIL |
| 150 | TH-BND-LEAN_MISFIRE-gas_nox-max+eps | LEAN_MISFIRE | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 151 | TH-BND-RICH_MISFIRE-gas_hc-min-eps | RICH_MISFIRE | gas_hc | min-eps | outside | SAMPLE_INVALID | PASS |
| 152 | TH-BND-RICH_MISFIRE-gas_hc-min | RICH_MISFIRE | gas_hc | min | inside | SAMPLE_INVALID | FAIL |
| 153 | TH-BND-RICH_MISFIRE-gas_hc-min+eps | RICH_MISFIRE | gas_hc | min+eps | inside | SAMPLE_INVALID | FAIL |
| 154 | TH-BND-RICH_MISFIRE-gas_hc-max-eps | RICH_MISFIRE | gas_hc | max-eps | inside | SAMPLE_INVALID | FAIL |
| 155 | TH-BND-RICH_MISFIRE-gas_hc-max | RICH_MISFIRE | gas_hc | max | inside | SAMPLE_INVALID | FAIL |
| 156 | TH-BND-RICH_MISFIRE-gas_hc-max+eps | RICH_MISFIRE | gas_hc | max+eps | outside | ERROR:ValueError | PASS |
| 157 | TH-BND-RICH_MISFIRE-gas_co-min-eps | RICH_MISFIRE | gas_co | min-eps | outside | SAMPLE_INVALID | PASS |
| 158 | TH-BND-RICH_MISFIRE-gas_co-min | RICH_MISFIRE | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 159 | TH-BND-RICH_MISFIRE-gas_co-min+eps | RICH_MISFIRE | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 160 | TH-BND-RICH_MISFIRE-gas_co-max-eps | RICH_MISFIRE | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 161 | TH-BND-RICH_MISFIRE-gas_co-max | RICH_MISFIRE | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 162 | TH-BND-RICH_MISFIRE-gas_co-max+eps | RICH_MISFIRE | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 163 | TH-BND-RICH_MISFIRE-gas_co2-min-eps | RICH_MISFIRE | gas_co2 | min-eps | outside | SAMPLE_INVALID | PASS |
| 164 | TH-BND-RICH_MISFIRE-gas_co2-min | RICH_MISFIRE | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 165 | TH-BND-RICH_MISFIRE-gas_co2-min+eps | RICH_MISFIRE | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 166 | TH-BND-RICH_MISFIRE-gas_co2-max-eps | RICH_MISFIRE | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 167 | TH-BND-RICH_MISFIRE-gas_co2-max | RICH_MISFIRE | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 168 | TH-BND-RICH_MISFIRE-gas_co2-max+eps | RICH_MISFIRE | gas_co2 | max+eps | outside | SAMPLE_INVALID | PASS |
| 169 | TH-BND-RICH_MISFIRE-gas_o2-min-eps | RICH_MISFIRE | gas_o2 | min-eps | outside | SAMPLE_INVALID | PASS |
| 170 | TH-BND-RICH_MISFIRE-gas_o2-min | RICH_MISFIRE | gas_o2 | min | inside | SAMPLE_INVALID | FAIL |
| 171 | TH-BND-RICH_MISFIRE-gas_o2-min+eps | RICH_MISFIRE | gas_o2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 172 | TH-BND-RICH_MISFIRE-gas_o2-max-eps | RICH_MISFIRE | gas_o2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 173 | TH-BND-RICH_MISFIRE-gas_o2-max | RICH_MISFIRE | gas_o2 | max | inside | SAMPLE_INVALID | FAIL |
| 174 | TH-BND-RICH_MISFIRE-gas_o2-max+eps | RICH_MISFIRE | gas_o2 | max+eps | outside | ERROR:ValueError | PASS |
| 175 | TH-BND-RICH_MISFIRE-gas_nox-min-eps | RICH_MISFIRE | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 176 | TH-BND-RICH_MISFIRE-gas_nox-min | RICH_MISFIRE | gas_nox | min | inside | SAMPLE_INVALID | FAIL |
| 177 | TH-BND-RICH_MISFIRE-gas_nox-min+eps | RICH_MISFIRE | gas_nox | min+eps | inside | SAMPLE_INVALID | FAIL |
| 178 | TH-BND-RICH_MISFIRE-gas_nox-max-eps | RICH_MISFIRE | gas_nox | max-eps | inside | SAMPLE_INVALID | FAIL |
| 179 | TH-BND-RICH_MISFIRE-gas_nox-max | RICH_MISFIRE | gas_nox | max | inside | SAMPLE_INVALID | FAIL |
| 180 | TH-BND-RICH_MISFIRE-gas_nox-max+eps | RICH_MISFIRE | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 181 | TH-BND-EXHAUST_AIR_LEAK-gas_hc-min-eps | EXHAUST_AIR_LEAK | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 182 | TH-BND-EXHAUST_AIR_LEAK-gas_hc-min | EXHAUST_AIR_LEAK | gas_hc | min | inside | SAMPLE_INVALID | FAIL |
| 183 | TH-BND-EXHAUST_AIR_LEAK-gas_hc-min+eps | EXHAUST_AIR_LEAK | gas_hc | min+eps | inside | SAMPLE_INVALID | FAIL |
| 184 | TH-BND-EXHAUST_AIR_LEAK-gas_hc-max-eps | EXHAUST_AIR_LEAK | gas_hc | max-eps | inside | SAMPLE_INVALID | FAIL |
| 185 | TH-BND-EXHAUST_AIR_LEAK-gas_hc-max | EXHAUST_AIR_LEAK | gas_hc | max | inside | SAMPLE_INVALID | FAIL |
| 186 | TH-BND-EXHAUST_AIR_LEAK-gas_hc-max+eps | EXHAUST_AIR_LEAK | gas_hc | max+eps | outside | ERROR:ValueError | PASS |
| 187 | TH-BND-EXHAUST_AIR_LEAK-gas_co-min-eps | EXHAUST_AIR_LEAK | gas_co | min-eps | outside | SAMPLE_INVALID | PASS |
| 188 | TH-BND-EXHAUST_AIR_LEAK-gas_co-min | EXHAUST_AIR_LEAK | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 189 | TH-BND-EXHAUST_AIR_LEAK-gas_co-min+eps | EXHAUST_AIR_LEAK | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 190 | TH-BND-EXHAUST_AIR_LEAK-gas_co-max-eps | EXHAUST_AIR_LEAK | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 191 | TH-BND-EXHAUST_AIR_LEAK-gas_co-max | EXHAUST_AIR_LEAK | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 192 | TH-BND-EXHAUST_AIR_LEAK-gas_co-max+eps | EXHAUST_AIR_LEAK | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 193 | TH-BND-EXHAUST_AIR_LEAK-gas_co2-min-eps | EXHAUST_AIR_LEAK | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 194 | TH-BND-EXHAUST_AIR_LEAK-gas_co2-min | EXHAUST_AIR_LEAK | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 195 | TH-BND-EXHAUST_AIR_LEAK-gas_co2-min+eps | EXHAUST_AIR_LEAK | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 196 | TH-BND-EXHAUST_AIR_LEAK-gas_co2-max-eps | EXHAUST_AIR_LEAK | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 197 | TH-BND-EXHAUST_AIR_LEAK-gas_co2-max | EXHAUST_AIR_LEAK | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 198 | TH-BND-EXHAUST_AIR_LEAK-gas_co2-max+eps | EXHAUST_AIR_LEAK | gas_co2 | max+eps | outside | SAMPLE_INVALID | PASS |
| 199 | TH-BND-EXHAUST_AIR_LEAK-gas_o2-min-eps | EXHAUST_AIR_LEAK | gas_o2 | min-eps | outside | NORMAL_OPERATION | PASS |
| 200 | TH-BND-EXHAUST_AIR_LEAK-gas_o2-min | EXHAUST_AIR_LEAK | gas_o2 | min | inside | NORMAL_OPERATION | FAIL |
| 201 | TH-BND-EXHAUST_AIR_LEAK-gas_o2-min+eps | EXHAUST_AIR_LEAK | gas_o2 | min+eps | inside | RICH_MISFIRE | FAIL |
| 202 | TH-BND-EXHAUST_AIR_LEAK-gas_o2-max-eps | EXHAUST_AIR_LEAK | gas_o2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 203 | TH-BND-EXHAUST_AIR_LEAK-gas_o2-max | EXHAUST_AIR_LEAK | gas_o2 | max | inside | SAMPLE_INVALID | FAIL |
| 204 | TH-BND-EXHAUST_AIR_LEAK-gas_o2-max+eps | EXHAUST_AIR_LEAK | gas_o2 | max+eps | outside | ERROR:ValueError | PASS |
| 205 | TH-BND-EXHAUST_AIR_LEAK-gas_nox-min-eps | EXHAUST_AIR_LEAK | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 206 | TH-BND-EXHAUST_AIR_LEAK-gas_nox-min | EXHAUST_AIR_LEAK | gas_nox | min | inside | SAMPLE_INVALID | FAIL |
| 207 | TH-BND-EXHAUST_AIR_LEAK-gas_nox-min+eps | EXHAUST_AIR_LEAK | gas_nox | min+eps | inside | SAMPLE_INVALID | FAIL |
| 208 | TH-BND-EXHAUST_AIR_LEAK-gas_nox-max-eps | EXHAUST_AIR_LEAK | gas_nox | max-eps | inside | SAMPLE_INVALID | FAIL |
| 209 | TH-BND-EXHAUST_AIR_LEAK-gas_nox-max | EXHAUST_AIR_LEAK | gas_nox | max | inside | SAMPLE_INVALID | FAIL |
| 210 | TH-BND-EXHAUST_AIR_LEAK-gas_nox-max+eps | EXHAUST_AIR_LEAK | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 211 | TH-BND-HIGH_COMBUSTION_TEMP-gas_hc-min-eps | HIGH_COMBUSTION_TEMP | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 212 | TH-BND-HIGH_COMBUSTION_TEMP-gas_hc-min | HIGH_COMBUSTION_TEMP | gas_hc | min | inside | HIGH_COMBUSTION_TEMP | PASS |
| 213 | TH-BND-HIGH_COMBUSTION_TEMP-gas_hc-min+eps | HIGH_COMBUSTION_TEMP | gas_hc | min+eps | inside | HIGH_COMBUSTION_TEMP | PASS |
| 214 | TH-BND-HIGH_COMBUSTION_TEMP-gas_hc-max-eps | HIGH_COMBUSTION_TEMP | gas_hc | max-eps | inside | HIGH_COMBUSTION_TEMP | PASS |
| 215 | TH-BND-HIGH_COMBUSTION_TEMP-gas_hc-max | HIGH_COMBUSTION_TEMP | gas_hc | max | inside | HIGH_COMBUSTION_TEMP | PASS |
| 216 | TH-BND-HIGH_COMBUSTION_TEMP-gas_hc-max+eps | HIGH_COMBUSTION_TEMP | gas_hc | max+eps | outside | VVT_FAILURE | PASS |
| 217 | TH-BND-HIGH_COMBUSTION_TEMP-gas_co-min-eps | HIGH_COMBUSTION_TEMP | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 218 | TH-BND-HIGH_COMBUSTION_TEMP-gas_co-min | HIGH_COMBUSTION_TEMP | gas_co | min | inside | TIMING_OVER_ADVANCED | FAIL |
| 219 | TH-BND-HIGH_COMBUSTION_TEMP-gas_co-min+eps | HIGH_COMBUSTION_TEMP | gas_co | min+eps | inside | TIMING_OVER_ADVANCED | FAIL |
| 220 | TH-BND-HIGH_COMBUSTION_TEMP-gas_co-max-eps | HIGH_COMBUSTION_TEMP | gas_co | max-eps | inside | HIGH_COMBUSTION_TEMP | PASS |
| 221 | TH-BND-HIGH_COMBUSTION_TEMP-gas_co-max | HIGH_COMBUSTION_TEMP | gas_co | max | inside | HIGH_COMBUSTION_TEMP | PASS |
| 222 | TH-BND-HIGH_COMBUSTION_TEMP-gas_co-max+eps | HIGH_COMBUSTION_TEMP | gas_co | max+eps | outside | VVT_FAILURE | PASS |
| 223 | TH-BND-HIGH_COMBUSTION_TEMP-gas_co2-min-eps | HIGH_COMBUSTION_TEMP | gas_co2 | min-eps | outside | SAMPLE_INVALID | PASS |
| 224 | TH-BND-HIGH_COMBUSTION_TEMP-gas_co2-min | HIGH_COMBUSTION_TEMP | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 225 | TH-BND-HIGH_COMBUSTION_TEMP-gas_co2-min+eps | HIGH_COMBUSTION_TEMP | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 226 | TH-BND-HIGH_COMBUSTION_TEMP-gas_co2-max-eps | HIGH_COMBUSTION_TEMP | gas_co2 | max-eps | inside | HIGH_COMBUSTION_TEMP | PASS |
| 227 | TH-BND-HIGH_COMBUSTION_TEMP-gas_co2-max | HIGH_COMBUSTION_TEMP | gas_co2 | max | inside | HIGH_COMBUSTION_TEMP | PASS |
| 228 | TH-BND-HIGH_COMBUSTION_TEMP-gas_co2-max+eps | HIGH_COMBUSTION_TEMP | gas_co2 | max+eps | outside | NORMAL_OPERATION | PASS |
| 229 | TH-BND-HIGH_COMBUSTION_TEMP-gas_o2-min-eps | HIGH_COMBUSTION_TEMP | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 230 | TH-BND-HIGH_COMBUSTION_TEMP-gas_o2-min | HIGH_COMBUSTION_TEMP | gas_o2 | min | inside | HIGH_COMBUSTION_TEMP | PASS |
| 231 | TH-BND-HIGH_COMBUSTION_TEMP-gas_o2-min+eps | HIGH_COMBUSTION_TEMP | gas_o2 | min+eps | inside | HIGH_COMBUSTION_TEMP | PASS |
| 232 | TH-BND-HIGH_COMBUSTION_TEMP-gas_o2-max-eps | HIGH_COMBUSTION_TEMP | gas_o2 | max-eps | inside | HIGH_COMBUSTION_TEMP | PASS |
| 233 | TH-BND-HIGH_COMBUSTION_TEMP-gas_o2-max | HIGH_COMBUSTION_TEMP | gas_o2 | max | inside | HIGH_COMBUSTION_TEMP | PASS |
| 234 | TH-BND-HIGH_COMBUSTION_TEMP-gas_o2-max+eps | HIGH_COMBUSTION_TEMP | gas_o2 | max+eps | outside | VVT_FAILURE | PASS |
| 235 | TH-BND-HIGH_COMBUSTION_TEMP-gas_nox-min-eps | HIGH_COMBUSTION_TEMP | gas_nox | min-eps | outside | VVT_FAILURE | PASS |
| 236 | TH-BND-HIGH_COMBUSTION_TEMP-gas_nox-min | HIGH_COMBUSTION_TEMP | gas_nox | min | inside | HIGH_COMBUSTION_TEMP | PASS |
| 237 | TH-BND-HIGH_COMBUSTION_TEMP-gas_nox-min+eps | HIGH_COMBUSTION_TEMP | gas_nox | min+eps | inside | HIGH_COMBUSTION_TEMP | PASS |
| 238 | TH-BND-HIGH_COMBUSTION_TEMP-gas_nox-max-eps | HIGH_COMBUSTION_TEMP | gas_nox | max-eps | inside | HIGH_COMBUSTION_TEMP | PASS |
| 239 | TH-BND-HIGH_COMBUSTION_TEMP-gas_nox-max | HIGH_COMBUSTION_TEMP | gas_nox | max | inside | HIGH_COMBUSTION_TEMP | PASS |
| 240 | TH-BND-HIGH_COMBUSTION_TEMP-gas_nox-max+eps | HIGH_COMBUSTION_TEMP | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 241 | TH-BND-CATALYST_NOT_LIGHTING_-gas_hc-min-eps | CATALYST_NOT_LIGHTING_OFF | gas_hc | min-eps | outside | VVT_FAILURE | PASS |
| 242 | TH-BND-CATALYST_NOT_LIGHTING_-gas_hc-min | CATALYST_NOT_LIGHTING_OFF | gas_hc | min | inside | VVT_FAILURE | FAIL |
| 243 | TH-BND-CATALYST_NOT_LIGHTING_-gas_hc-min+eps | CATALYST_NOT_LIGHTING_OFF | gas_hc | min+eps | inside | VVT_FAILURE | FAIL |
| 244 | TH-BND-CATALYST_NOT_LIGHTING_-gas_hc-max-eps | CATALYST_NOT_LIGHTING_OFF | gas_hc | max-eps | inside | VVT_FAILURE | FAIL |
| 245 | TH-BND-CATALYST_NOT_LIGHTING_-gas_hc-max | CATALYST_NOT_LIGHTING_OFF | gas_hc | max | inside | VVT_FAILURE | FAIL |
| 246 | TH-BND-CATALYST_NOT_LIGHTING_-gas_hc-max+eps | CATALYST_NOT_LIGHTING_OFF | gas_hc | max+eps | outside | VVT_FAILURE | PASS |
| 247 | TH-BND-CATALYST_NOT_LIGHTING_-gas_co-min-eps | CATALYST_NOT_LIGHTING_OFF | gas_co | min-eps | outside | HIGH_COMBUSTION_TEMP | PASS |
| 248 | TH-BND-CATALYST_NOT_LIGHTING_-gas_co-min | CATALYST_NOT_LIGHTING_OFF | gas_co | min | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 249 | TH-BND-CATALYST_NOT_LIGHTING_-gas_co-min+eps | CATALYST_NOT_LIGHTING_OFF | gas_co | min+eps | inside | VVT_FAILURE | FAIL |
| 250 | TH-BND-CATALYST_NOT_LIGHTING_-gas_co-max-eps | CATALYST_NOT_LIGHTING_OFF | gas_co | max-eps | inside | VVT_FAILURE | FAIL |
| 251 | TH-BND-CATALYST_NOT_LIGHTING_-gas_co-max | CATALYST_NOT_LIGHTING_OFF | gas_co | max | inside | VVT_FAILURE | FAIL |
| 252 | TH-BND-CATALYST_NOT_LIGHTING_-gas_co-max+eps | CATALYST_NOT_LIGHTING_OFF | gas_co | max+eps | outside | VVT_FAILURE | PASS |
| 253 | TH-BND-CATALYST_NOT_LIGHTING_-gas_co2-min-eps | CATALYST_NOT_LIGHTING_OFF | gas_co2 | min-eps | outside | VVT_FAILURE | PASS |
| 254 | TH-BND-CATALYST_NOT_LIGHTING_-gas_co2-min | CATALYST_NOT_LIGHTING_OFF | gas_co2 | min | inside | VVT_FAILURE | FAIL |
| 255 | TH-BND-CATALYST_NOT_LIGHTING_-gas_co2-min+eps | CATALYST_NOT_LIGHTING_OFF | gas_co2 | min+eps | inside | VVT_FAILURE | FAIL |
| 256 | TH-BND-CATALYST_NOT_LIGHTING_-gas_co2-max-eps | CATALYST_NOT_LIGHTING_OFF | gas_co2 | max-eps | inside | VVT_FAILURE | FAIL |
| 257 | TH-BND-CATALYST_NOT_LIGHTING_-gas_co2-max | CATALYST_NOT_LIGHTING_OFF | gas_co2 | max | inside | VVT_FAILURE | FAIL |
| 258 | TH-BND-CATALYST_NOT_LIGHTING_-gas_co2-max+eps | CATALYST_NOT_LIGHTING_OFF | gas_co2 | max+eps | outside | VVT_FAILURE | PASS |
| 259 | TH-BND-CATALYST_NOT_LIGHTING_-gas_o2-min-eps | CATALYST_NOT_LIGHTING_OFF | gas_o2 | min-eps | outside | VVT_FAILURE | PASS |
| 260 | TH-BND-CATALYST_NOT_LIGHTING_-gas_o2-min | CATALYST_NOT_LIGHTING_OFF | gas_o2 | min | inside | VVT_FAILURE | FAIL |
| 261 | TH-BND-CATALYST_NOT_LIGHTING_-gas_o2-min+eps | CATALYST_NOT_LIGHTING_OFF | gas_o2 | min+eps | inside | VVT_FAILURE | FAIL |
| 262 | TH-BND-CATALYST_NOT_LIGHTING_-gas_o2-max-eps | CATALYST_NOT_LIGHTING_OFF | gas_o2 | max-eps | inside | VVT_FAILURE | FAIL |
| 263 | TH-BND-CATALYST_NOT_LIGHTING_-gas_o2-max | CATALYST_NOT_LIGHTING_OFF | gas_o2 | max | inside | VVT_FAILURE | FAIL |
| 264 | TH-BND-CATALYST_NOT_LIGHTING_-gas_o2-max+eps | CATALYST_NOT_LIGHTING_OFF | gas_o2 | max+eps | outside | VVT_FAILURE | PASS |
| 265 | TH-BND-CATALYST_NOT_LIGHTING_-gas_nox-min-eps | CATALYST_NOT_LIGHTING_OFF | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 266 | TH-BND-CATALYST_NOT_LIGHTING_-gas_nox-min | CATALYST_NOT_LIGHTING_OFF | gas_nox | min | inside | VVT_FAILURE | FAIL |
| 267 | TH-BND-CATALYST_NOT_LIGHTING_-gas_nox-min+eps | CATALYST_NOT_LIGHTING_OFF | gas_nox | min+eps | inside | VVT_FAILURE | FAIL |
| 268 | TH-BND-CATALYST_NOT_LIGHTING_-gas_nox-max-eps | CATALYST_NOT_LIGHTING_OFF | gas_nox | max-eps | inside | VVT_FAILURE | FAIL |
| 269 | TH-BND-CATALYST_NOT_LIGHTING_-gas_nox-max | CATALYST_NOT_LIGHTING_OFF | gas_nox | max | inside | VVT_FAILURE | FAIL |
| 270 | TH-BND-CATALYST_NOT_LIGHTING_-gas_nox-max+eps | CATALYST_NOT_LIGHTING_OFF | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 271 | TH-BND-CATALYST_OVERWHELMED-gas_hc-min-eps | CATALYST_OVERWHELMED | gas_hc | min-eps | outside | VVT_FAILURE | PASS |
| 272 | TH-BND-CATALYST_OVERWHELMED-gas_hc-min | CATALYST_OVERWHELMED | gas_hc | min | inside | CATALYST_OVERWHELMED | PASS |
| 273 | TH-BND-CATALYST_OVERWHELMED-gas_hc-min+eps | CATALYST_OVERWHELMED | gas_hc | min+eps | inside | CATALYST_OVERWHELMED | PASS |
| 274 | TH-BND-CATALYST_OVERWHELMED-gas_hc-max-eps | CATALYST_OVERWHELMED | gas_hc | max-eps | inside | NORMAL_OPERATION | FAIL |
| 275 | TH-BND-CATALYST_OVERWHELMED-gas_hc-max | CATALYST_OVERWHELMED | gas_hc | max | inside | NORMAL_OPERATION | FAIL |
| 276 | TH-BND-CATALYST_OVERWHELMED-gas_hc-max+eps | CATALYST_OVERWHELMED | gas_hc | max+eps | outside | ERROR:ValueError | PASS |
| 277 | TH-BND-CATALYST_OVERWHELMED-gas_co-min-eps | CATALYST_OVERWHELMED | gas_co | min-eps | outside | SAMPLE_INVALID | PASS |
| 278 | TH-BND-CATALYST_OVERWHELMED-gas_co-min | CATALYST_OVERWHELMED | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 279 | TH-BND-CATALYST_OVERWHELMED-gas_co-min+eps | CATALYST_OVERWHELMED | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 280 | TH-BND-CATALYST_OVERWHELMED-gas_co-max-eps | CATALYST_OVERWHELMED | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 281 | TH-BND-CATALYST_OVERWHELMED-gas_co-max | CATALYST_OVERWHELMED | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 282 | TH-BND-CATALYST_OVERWHELMED-gas_co-max+eps | CATALYST_OVERWHELMED | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 283 | TH-BND-CATALYST_OVERWHELMED-gas_co2-min-eps | CATALYST_OVERWHELMED | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 284 | TH-BND-CATALYST_OVERWHELMED-gas_co2-min | CATALYST_OVERWHELMED | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 285 | TH-BND-CATALYST_OVERWHELMED-gas_co2-min+eps | CATALYST_OVERWHELMED | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 286 | TH-BND-CATALYST_OVERWHELMED-gas_co2-max-eps | CATALYST_OVERWHELMED | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 287 | TH-BND-CATALYST_OVERWHELMED-gas_co2-max | CATALYST_OVERWHELMED | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 288 | TH-BND-CATALYST_OVERWHELMED-gas_co2-max+eps | CATALYST_OVERWHELMED | gas_co2 | max+eps | outside | SAMPLE_INVALID | PASS |
| 289 | TH-BND-CATALYST_OVERWHELMED-gas_o2-min-eps | CATALYST_OVERWHELMED | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 290 | TH-BND-CATALYST_OVERWHELMED-gas_o2-min | CATALYST_OVERWHELMED | gas_o2 | min | inside | NORMAL_OPERATION | FAIL |
| 291 | TH-BND-CATALYST_OVERWHELMED-gas_o2-min+eps | CATALYST_OVERWHELMED | gas_o2 | min+eps | inside | NORMAL_OPERATION | FAIL |
| 292 | TH-BND-CATALYST_OVERWHELMED-gas_o2-max-eps | CATALYST_OVERWHELMED | gas_o2 | max-eps | inside | NORMAL_OPERATION | FAIL |
| 293 | TH-BND-CATALYST_OVERWHELMED-gas_o2-max | CATALYST_OVERWHELMED | gas_o2 | max | inside | NORMAL_OPERATION | FAIL |
| 294 | TH-BND-CATALYST_OVERWHELMED-gas_o2-max+eps | CATALYST_OVERWHELMED | gas_o2 | max+eps | outside | RICH_MISFIRE | PASS |
| 295 | TH-BND-CATALYST_OVERWHELMED-gas_nox-min-eps | CATALYST_OVERWHELMED | gas_nox | min-eps | outside | NORMAL_OPERATION | PASS |
| 296 | TH-BND-CATALYST_OVERWHELMED-gas_nox-min | CATALYST_OVERWHELMED | gas_nox | min | inside | NORMAL_OPERATION | FAIL |
| 297 | TH-BND-CATALYST_OVERWHELMED-gas_nox-min+eps | CATALYST_OVERWHELMED | gas_nox | min+eps | inside | NORMAL_OPERATION | FAIL |
| 298 | TH-BND-CATALYST_OVERWHELMED-gas_nox-max-eps | CATALYST_OVERWHELMED | gas_nox | max-eps | inside | NORMAL_OPERATION | FAIL |
| 299 | TH-BND-CATALYST_OVERWHELMED-gas_nox-max | CATALYST_OVERWHELMED | gas_nox | max | inside | NORMAL_OPERATION | FAIL |
| 300 | TH-BND-CATALYST_OVERWHELMED-gas_nox-max+eps | CATALYST_OVERWHELMED | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 301 | TH-BND-SAMPLE_INVALID-gas_hc-min-eps | SAMPLE_INVALID | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 302 | TH-BND-SAMPLE_INVALID-gas_hc-min | SAMPLE_INVALID | gas_hc | min | inside | SAMPLE_INVALID | PASS |
| 303 | TH-BND-SAMPLE_INVALID-gas_hc-min+eps | SAMPLE_INVALID | gas_hc | min+eps | inside | SAMPLE_INVALID | PASS |
| 304 | TH-BND-SAMPLE_INVALID-gas_hc-max-eps | SAMPLE_INVALID | gas_hc | max-eps | inside | SAMPLE_INVALID | PASS |
| 305 | TH-BND-SAMPLE_INVALID-gas_hc-max | SAMPLE_INVALID | gas_hc | max | inside | SAMPLE_INVALID | PASS |
| 306 | TH-BND-SAMPLE_INVALID-gas_hc-max+eps | SAMPLE_INVALID | gas_hc | max+eps | outside | ERROR:ValueError | PASS |
| 307 | TH-BND-SAMPLE_INVALID-gas_co-min-eps | SAMPLE_INVALID | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 308 | TH-BND-SAMPLE_INVALID-gas_co-min | SAMPLE_INVALID | gas_co | min | inside | SAMPLE_INVALID | PASS |
| 309 | TH-BND-SAMPLE_INVALID-gas_co-min+eps | SAMPLE_INVALID | gas_co | min+eps | inside | SAMPLE_INVALID | PASS |
| 310 | TH-BND-SAMPLE_INVALID-gas_co-max-eps | SAMPLE_INVALID | gas_co | max-eps | inside | SAMPLE_INVALID | PASS |
| 311 | TH-BND-SAMPLE_INVALID-gas_co-max | SAMPLE_INVALID | gas_co | max | inside | SAMPLE_INVALID | PASS |
| 312 | TH-BND-SAMPLE_INVALID-gas_co-max+eps | SAMPLE_INVALID | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 313 | TH-BND-SAMPLE_INVALID-gas_co2-min-eps | SAMPLE_INVALID | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 314 | TH-BND-SAMPLE_INVALID-gas_co2-min | SAMPLE_INVALID | gas_co2 | min | inside | SAMPLE_INVALID | PASS |
| 315 | TH-BND-SAMPLE_INVALID-gas_co2-min+eps | SAMPLE_INVALID | gas_co2 | min+eps | inside | SAMPLE_INVALID | PASS |
| 316 | TH-BND-SAMPLE_INVALID-gas_co2-max-eps | SAMPLE_INVALID | gas_co2 | max-eps | inside | SAMPLE_INVALID | PASS |
| 317 | TH-BND-SAMPLE_INVALID-gas_co2-max | SAMPLE_INVALID | gas_co2 | max | inside | SAMPLE_INVALID | PASS |
| 318 | TH-BND-SAMPLE_INVALID-gas_co2-max+eps | SAMPLE_INVALID | gas_co2 | max+eps | outside | ERROR:ValueError | PASS |
| 319 | TH-BND-SAMPLE_INVALID-gas_o2-min-eps | SAMPLE_INVALID | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 320 | TH-BND-SAMPLE_INVALID-gas_o2-min | SAMPLE_INVALID | gas_o2 | min | inside | SAMPLE_INVALID | PASS |
| 321 | TH-BND-SAMPLE_INVALID-gas_o2-min+eps | SAMPLE_INVALID | gas_o2 | min+eps | inside | SAMPLE_INVALID | PASS |
| 322 | TH-BND-SAMPLE_INVALID-gas_o2-max-eps | SAMPLE_INVALID | gas_o2 | max-eps | inside | SAMPLE_INVALID | PASS |
| 323 | TH-BND-SAMPLE_INVALID-gas_o2-max | SAMPLE_INVALID | gas_o2 | max | inside | SAMPLE_INVALID | PASS |
| 324 | TH-BND-SAMPLE_INVALID-gas_o2-max+eps | SAMPLE_INVALID | gas_o2 | max+eps | outside | ERROR:ValueError | PASS |
| 325 | TH-BND-SAMPLE_INVALID-gas_nox-min-eps | SAMPLE_INVALID | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 326 | TH-BND-SAMPLE_INVALID-gas_nox-min | SAMPLE_INVALID | gas_nox | min | inside | SAMPLE_INVALID | PASS |
| 327 | TH-BND-SAMPLE_INVALID-gas_nox-min+eps | SAMPLE_INVALID | gas_nox | min+eps | inside | SAMPLE_INVALID | PASS |
| 328 | TH-BND-SAMPLE_INVALID-gas_nox-max-eps | SAMPLE_INVALID | gas_nox | max-eps | inside | SAMPLE_INVALID | PASS |
| 329 | TH-BND-SAMPLE_INVALID-gas_nox-max | SAMPLE_INVALID | gas_nox | max | inside | SAMPLE_INVALID | PASS |
| 330 | TH-BND-SAMPLE_INVALID-gas_nox-max+eps | SAMPLE_INVALID | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 331 | TH-BND-TIMING_OVER_ADVANCED-gas_hc-min-eps | TIMING_OVER_ADVANCED | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 332 | TH-BND-TIMING_OVER_ADVANCED-gas_hc-min | TIMING_OVER_ADVANCED | gas_hc | min | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 333 | TH-BND-TIMING_OVER_ADVANCED-gas_hc-min+eps | TIMING_OVER_ADVANCED | gas_hc | min+eps | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 334 | TH-BND-TIMING_OVER_ADVANCED-gas_hc-max-eps | TIMING_OVER_ADVANCED | gas_hc | max-eps | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 335 | TH-BND-TIMING_OVER_ADVANCED-gas_hc-max | TIMING_OVER_ADVANCED | gas_hc | max | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 336 | TH-BND-TIMING_OVER_ADVANCED-gas_hc-max+eps | TIMING_OVER_ADVANCED | gas_hc | max+eps | outside | VVT_FAILURE | PASS |
| 337 | TH-BND-TIMING_OVER_ADVANCED-gas_co-min-eps | TIMING_OVER_ADVANCED | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 338 | TH-BND-TIMING_OVER_ADVANCED-gas_co-min | TIMING_OVER_ADVANCED | gas_co | min | inside | TIMING_OVER_ADVANCED | PASS |
| 339 | TH-BND-TIMING_OVER_ADVANCED-gas_co-min+eps | TIMING_OVER_ADVANCED | gas_co | min+eps | inside | TIMING_OVER_ADVANCED | PASS |
| 340 | TH-BND-TIMING_OVER_ADVANCED-gas_co-max-eps | TIMING_OVER_ADVANCED | gas_co | max-eps | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 341 | TH-BND-TIMING_OVER_ADVANCED-gas_co-max | TIMING_OVER_ADVANCED | gas_co | max | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 342 | TH-BND-TIMING_OVER_ADVANCED-gas_co-max+eps | TIMING_OVER_ADVANCED | gas_co | max+eps | outside | VVT_FAILURE | PASS |
| 343 | TH-BND-TIMING_OVER_ADVANCED-gas_co2-min-eps | TIMING_OVER_ADVANCED | gas_co2 | min-eps | outside | SAMPLE_INVALID | PASS |
| 344 | TH-BND-TIMING_OVER_ADVANCED-gas_co2-min | TIMING_OVER_ADVANCED | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 345 | TH-BND-TIMING_OVER_ADVANCED-gas_co2-min+eps | TIMING_OVER_ADVANCED | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 346 | TH-BND-TIMING_OVER_ADVANCED-gas_co2-max-eps | TIMING_OVER_ADVANCED | gas_co2 | max-eps | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 347 | TH-BND-TIMING_OVER_ADVANCED-gas_co2-max | TIMING_OVER_ADVANCED | gas_co2 | max | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 348 | TH-BND-TIMING_OVER_ADVANCED-gas_co2-max+eps | TIMING_OVER_ADVANCED | gas_co2 | max+eps | outside | NORMAL_OPERATION | PASS |
| 349 | TH-BND-TIMING_OVER_ADVANCED-gas_o2-min-eps | TIMING_OVER_ADVANCED | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 350 | TH-BND-TIMING_OVER_ADVANCED-gas_o2-min | TIMING_OVER_ADVANCED | gas_o2 | min | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 351 | TH-BND-TIMING_OVER_ADVANCED-gas_o2-min+eps | TIMING_OVER_ADVANCED | gas_o2 | min+eps | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 352 | TH-BND-TIMING_OVER_ADVANCED-gas_o2-max-eps | TIMING_OVER_ADVANCED | gas_o2 | max-eps | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 353 | TH-BND-TIMING_OVER_ADVANCED-gas_o2-max | TIMING_OVER_ADVANCED | gas_o2 | max | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 354 | TH-BND-TIMING_OVER_ADVANCED-gas_o2-max+eps | TIMING_OVER_ADVANCED | gas_o2 | max+eps | outside | VVT_FAILURE | PASS |
| 355 | TH-BND-TIMING_OVER_ADVANCED-gas_nox-min-eps | TIMING_OVER_ADVANCED | gas_nox | min-eps | outside | VVT_FAILURE | PASS |
| 356 | TH-BND-TIMING_OVER_ADVANCED-gas_nox-min | TIMING_OVER_ADVANCED | gas_nox | min | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 357 | TH-BND-TIMING_OVER_ADVANCED-gas_nox-min+eps | TIMING_OVER_ADVANCED | gas_nox | min+eps | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 358 | TH-BND-TIMING_OVER_ADVANCED-gas_nox-max-eps | TIMING_OVER_ADVANCED | gas_nox | max-eps | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 359 | TH-BND-TIMING_OVER_ADVANCED-gas_nox-max | TIMING_OVER_ADVANCED | gas_nox | max | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 360 | TH-BND-TIMING_OVER_ADVANCED-gas_nox-max+eps | TIMING_OVER_ADVANCED | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 361 | TH-BND-TIMING_RETARDED-gas_hc-min-eps | TIMING_RETARDED | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 362 | TH-BND-TIMING_RETARDED-gas_hc-min | TIMING_RETARDED | gas_hc | min | inside | TIMING_RETARDED | PASS |
| 363 | TH-BND-TIMING_RETARDED-gas_hc-min+eps | TIMING_RETARDED | gas_hc | min+eps | inside | TIMING_RETARDED | PASS |
| 364 | TH-BND-TIMING_RETARDED-gas_hc-max-eps | TIMING_RETARDED | gas_hc | max-eps | inside | TIMING_RETARDED | PASS |
| 365 | TH-BND-TIMING_RETARDED-gas_hc-max | TIMING_RETARDED | gas_hc | max | inside | TIMING_RETARDED | PASS |
| 366 | TH-BND-TIMING_RETARDED-gas_hc-max+eps | TIMING_RETARDED | gas_hc | max+eps | outside | WORN_VALVE_SEALS | PASS |
| 367 | TH-BND-TIMING_RETARDED-gas_co-min-eps | TIMING_RETARDED | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 368 | TH-BND-TIMING_RETARDED-gas_co-min | TIMING_RETARDED | gas_co | min | inside | TIMING_RETARDED | PASS |
| 369 | TH-BND-TIMING_RETARDED-gas_co-min+eps | TIMING_RETARDED | gas_co | min+eps | inside | TIMING_RETARDED | PASS |
| 370 | TH-BND-TIMING_RETARDED-gas_co-max-eps | TIMING_RETARDED | gas_co | max-eps | inside | TIMING_RETARDED | PASS |
| 371 | TH-BND-TIMING_RETARDED-gas_co-max | TIMING_RETARDED | gas_co | max | inside | TIMING_RETARDED | PASS |
| 372 | TH-BND-TIMING_RETARDED-gas_co-max+eps | TIMING_RETARDED | gas_co | max+eps | outside | O2_SENSOR_BIASED_LOW | PASS |
| 373 | TH-BND-TIMING_RETARDED-gas_co2-min-eps | TIMING_RETARDED | gas_co2 | min-eps | outside | SAMPLE_INVALID | PASS |
| 374 | TH-BND-TIMING_RETARDED-gas_co2-min | TIMING_RETARDED | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 375 | TH-BND-TIMING_RETARDED-gas_co2-min+eps | TIMING_RETARDED | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 376 | TH-BND-TIMING_RETARDED-gas_co2-max-eps | TIMING_RETARDED | gas_co2 | max-eps | inside | TIMING_RETARDED | PASS |
| 377 | TH-BND-TIMING_RETARDED-gas_co2-max | TIMING_RETARDED | gas_co2 | max | inside | TIMING_RETARDED | PASS |
| 378 | TH-BND-TIMING_RETARDED-gas_co2-max+eps | TIMING_RETARDED | gas_co2 | max+eps | outside | NORMAL_OPERATION | PASS |
| 379 | TH-BND-TIMING_RETARDED-gas_o2-min-eps | TIMING_RETARDED | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 380 | TH-BND-TIMING_RETARDED-gas_o2-min | TIMING_RETARDED | gas_o2 | min | inside | TIMING_RETARDED | PASS |
| 381 | TH-BND-TIMING_RETARDED-gas_o2-min+eps | TIMING_RETARDED | gas_o2 | min+eps | inside | TIMING_RETARDED | PASS |
| 382 | TH-BND-TIMING_RETARDED-gas_o2-max-eps | TIMING_RETARDED | gas_o2 | max-eps | inside | TIMING_RETARDED | PASS |
| 383 | TH-BND-TIMING_RETARDED-gas_o2-max | TIMING_RETARDED | gas_o2 | max | inside | TIMING_RETARDED | PASS |
| 384 | TH-BND-TIMING_RETARDED-gas_o2-max+eps | TIMING_RETARDED | gas_o2 | max+eps | outside | VVT_FAILURE | PASS |
| 385 | TH-BND-TIMING_RETARDED-gas_nox-min-eps | TIMING_RETARDED | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 386 | TH-BND-TIMING_RETARDED-gas_nox-min | TIMING_RETARDED | gas_nox | min | inside | TIMING_RETARDED | PASS |
| 387 | TH-BND-TIMING_RETARDED-gas_nox-min+eps | TIMING_RETARDED | gas_nox | min+eps | inside | TIMING_RETARDED | PASS |
| 388 | TH-BND-TIMING_RETARDED-gas_nox-max-eps | TIMING_RETARDED | gas_nox | max-eps | inside | TIMING_RETARDED | PASS |
| 389 | TH-BND-TIMING_RETARDED-gas_nox-max | TIMING_RETARDED | gas_nox | max | inside | TIMING_RETARDED | PASS |
| 390 | TH-BND-TIMING_RETARDED-gas_nox-max+eps | TIMING_RETARDED | gas_nox | max+eps | outside | WORN_PISTON_RINGS | PASS |
| 391 | TH-BND-O2_SENSOR_BIASED_LOW-gas_hc-min-eps | O2_SENSOR_BIASED_LOW | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 392 | TH-BND-O2_SENSOR_BIASED_LOW-gas_hc-min | O2_SENSOR_BIASED_LOW | gas_hc | min | inside | VVT_FAILURE | FAIL |
| 393 | TH-BND-O2_SENSOR_BIASED_LOW-gas_hc-min+eps | O2_SENSOR_BIASED_LOW | gas_hc | min+eps | inside | VVT_FAILURE | FAIL |
| 394 | TH-BND-O2_SENSOR_BIASED_LOW-gas_hc-max-eps | O2_SENSOR_BIASED_LOW | gas_hc | max-eps | inside | VVT_FAILURE | FAIL |
| 395 | TH-BND-O2_SENSOR_BIASED_LOW-gas_hc-max | O2_SENSOR_BIASED_LOW | gas_hc | max | inside | VVT_FAILURE | FAIL |
| 396 | TH-BND-O2_SENSOR_BIASED_LOW-gas_hc-max+eps | O2_SENSOR_BIASED_LOW | gas_hc | max+eps | outside | VVT_FAILURE | PASS |
| 397 | TH-BND-O2_SENSOR_BIASED_LOW-gas_co-min-eps | O2_SENSOR_BIASED_LOW | gas_co | min-eps | outside | VVT_FAILURE | PASS |
| 398 | TH-BND-O2_SENSOR_BIASED_LOW-gas_co-min | O2_SENSOR_BIASED_LOW | gas_co | min | inside | VVT_FAILURE | FAIL |
| 399 | TH-BND-O2_SENSOR_BIASED_LOW-gas_co-min+eps | O2_SENSOR_BIASED_LOW | gas_co | min+eps | inside | VVT_FAILURE | FAIL |
| 400 | TH-BND-O2_SENSOR_BIASED_LOW-gas_co-max-eps | O2_SENSOR_BIASED_LOW | gas_co | max-eps | inside | VVT_FAILURE | FAIL |
| 401 | TH-BND-O2_SENSOR_BIASED_LOW-gas_co-max | O2_SENSOR_BIASED_LOW | gas_co | max | inside | VVT_FAILURE | FAIL |
| 402 | TH-BND-O2_SENSOR_BIASED_LOW-gas_co-max+eps | O2_SENSOR_BIASED_LOW | gas_co | max+eps | outside | VVT_FAILURE | PASS |
| 403 | TH-BND-O2_SENSOR_BIASED_LOW-gas_co2-min-eps | O2_SENSOR_BIASED_LOW | gas_co2 | min-eps | outside | VVT_FAILURE | PASS |
| 404 | TH-BND-O2_SENSOR_BIASED_LOW-gas_co2-min | O2_SENSOR_BIASED_LOW | gas_co2 | min | inside | VVT_FAILURE | FAIL |
| 405 | TH-BND-O2_SENSOR_BIASED_LOW-gas_co2-min+eps | O2_SENSOR_BIASED_LOW | gas_co2 | min+eps | inside | VVT_FAILURE | FAIL |
| 406 | TH-BND-O2_SENSOR_BIASED_LOW-gas_co2-max-eps | O2_SENSOR_BIASED_LOW | gas_co2 | max-eps | inside | VVT_FAILURE | FAIL |
| 407 | TH-BND-O2_SENSOR_BIASED_LOW-gas_co2-max | O2_SENSOR_BIASED_LOW | gas_co2 | max | inside | VVT_FAILURE | FAIL |
| 408 | TH-BND-O2_SENSOR_BIASED_LOW-gas_co2-max+eps | O2_SENSOR_BIASED_LOW | gas_co2 | max+eps | outside | NORMAL_OPERATION | PASS |
| 409 | TH-BND-O2_SENSOR_BIASED_LOW-gas_o2-min-eps | O2_SENSOR_BIASED_LOW | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 410 | TH-BND-O2_SENSOR_BIASED_LOW-gas_o2-min | O2_SENSOR_BIASED_LOW | gas_o2 | min | inside | VVT_FAILURE | FAIL |
| 411 | TH-BND-O2_SENSOR_BIASED_LOW-gas_o2-min+eps | O2_SENSOR_BIASED_LOW | gas_o2 | min+eps | inside | VVT_FAILURE | FAIL |
| 412 | TH-BND-O2_SENSOR_BIASED_LOW-gas_o2-max-eps | O2_SENSOR_BIASED_LOW | gas_o2 | max-eps | inside | VVT_FAILURE | FAIL |
| 413 | TH-BND-O2_SENSOR_BIASED_LOW-gas_o2-max | O2_SENSOR_BIASED_LOW | gas_o2 | max | inside | VVT_FAILURE | FAIL |
| 414 | TH-BND-O2_SENSOR_BIASED_LOW-gas_o2-max+eps | O2_SENSOR_BIASED_LOW | gas_o2 | max+eps | outside | VVT_FAILURE | PASS |
| 415 | TH-BND-O2_SENSOR_BIASED_LOW-gas_nox-min-eps | O2_SENSOR_BIASED_LOW | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 416 | TH-BND-O2_SENSOR_BIASED_LOW-gas_nox-min | O2_SENSOR_BIASED_LOW | gas_nox | min | inside | O2_SENSOR_BIASED_LOW | PASS |
| 417 | TH-BND-O2_SENSOR_BIASED_LOW-gas_nox-min+eps | O2_SENSOR_BIASED_LOW | gas_nox | min+eps | inside | O2_SENSOR_BIASED_LOW | PASS |
| 418 | TH-BND-O2_SENSOR_BIASED_LOW-gas_nox-max-eps | O2_SENSOR_BIASED_LOW | gas_nox | max-eps | inside | VVT_FAILURE | FAIL |
| 419 | TH-BND-O2_SENSOR_BIASED_LOW-gas_nox-max | O2_SENSOR_BIASED_LOW | gas_nox | max | inside | VVT_FAILURE | FAIL |
| 420 | TH-BND-O2_SENSOR_BIASED_LOW-gas_nox-max+eps | O2_SENSOR_BIASED_LOW | gas_nox | max+eps | outside | VVT_FAILURE | PASS |
| 421 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_hc-min-eps | O2_SENSOR_BIASED_HIGH | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 422 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_hc-min | O2_SENSOR_BIASED_HIGH | gas_hc | min | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 423 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_hc-min+eps | O2_SENSOR_BIASED_HIGH | gas_hc | min+eps | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 424 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_hc-max-eps | O2_SENSOR_BIASED_HIGH | gas_hc | max-eps | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 425 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_hc-max | O2_SENSOR_BIASED_HIGH | gas_hc | max | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 426 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_hc-max+eps | O2_SENSOR_BIASED_HIGH | gas_hc | max+eps | outside | VVT_FAILURE | PASS |
| 427 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_co-min-eps | O2_SENSOR_BIASED_HIGH | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 428 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_co-min | O2_SENSOR_BIASED_HIGH | gas_co | min | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 429 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_co-min+eps | O2_SENSOR_BIASED_HIGH | gas_co | min+eps | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 430 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_co-max-eps | O2_SENSOR_BIASED_HIGH | gas_co | max-eps | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 431 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_co-max | O2_SENSOR_BIASED_HIGH | gas_co | max | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 432 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_co-max+eps | O2_SENSOR_BIASED_HIGH | gas_co | max+eps | outside | VVT_FAILURE | PASS |
| 433 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_co2-min-eps | O2_SENSOR_BIASED_HIGH | gas_co2 | min-eps | outside | VVT_FAILURE | PASS |
| 434 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_co2-min | O2_SENSOR_BIASED_HIGH | gas_co2 | min | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 435 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_co2-min+eps | O2_SENSOR_BIASED_HIGH | gas_co2 | min+eps | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 436 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_co2-max-eps | O2_SENSOR_BIASED_HIGH | gas_co2 | max-eps | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 437 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_co2-max | O2_SENSOR_BIASED_HIGH | gas_co2 | max | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 438 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_co2-max+eps | O2_SENSOR_BIASED_HIGH | gas_co2 | max+eps | outside | NORMAL_OPERATION | PASS |
| 439 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_o2-min-eps | O2_SENSOR_BIASED_HIGH | gas_o2 | min-eps | outside | VVT_FAILURE | PASS |
| 440 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_o2-min | O2_SENSOR_BIASED_HIGH | gas_o2 | min | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 441 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_o2-min+eps | O2_SENSOR_BIASED_HIGH | gas_o2 | min+eps | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 442 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_o2-max-eps | O2_SENSOR_BIASED_HIGH | gas_o2 | max-eps | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 443 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_o2-max | O2_SENSOR_BIASED_HIGH | gas_o2 | max | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 444 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_o2-max+eps | O2_SENSOR_BIASED_HIGH | gas_o2 | max+eps | outside | VVT_FAILURE | PASS |
| 445 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_nox-min-eps | O2_SENSOR_BIASED_HIGH | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 446 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_nox-min | O2_SENSOR_BIASED_HIGH | gas_nox | min | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 447 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_nox-min+eps | O2_SENSOR_BIASED_HIGH | gas_nox | min+eps | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 448 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_nox-max-eps | O2_SENSOR_BIASED_HIGH | gas_nox | max-eps | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 449 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_nox-max | O2_SENSOR_BIASED_HIGH | gas_nox | max | inside | O2_SENSOR_BIASED_HIGH | PASS |
| 450 | TH-BND-O2_SENSOR_BIASED_HIGH-gas_nox-max+eps | O2_SENSOR_BIASED_HIGH | gas_nox | max+eps | outside | VVT_FAILURE | PASS |
| 451 | TH-BND-WORN_ENGINE-gas_hc-min-eps | WORN_ENGINE | gas_hc | min-eps | outside | O2_SENSOR_BIASED_LOW | PASS |
| 452 | TH-BND-WORN_ENGINE-gas_hc-min | WORN_ENGINE | gas_hc | min | inside | O2_SENSOR_BIASED_LOW | FAIL |
| 453 | TH-BND-WORN_ENGINE-gas_hc-min+eps | WORN_ENGINE | gas_hc | min+eps | inside | O2_SENSOR_BIASED_LOW | FAIL |
| 454 | TH-BND-WORN_ENGINE-gas_hc-max-eps | WORN_ENGINE | gas_hc | max-eps | inside | VVT_FAILURE | FAIL |
| 455 | TH-BND-WORN_ENGINE-gas_hc-max | WORN_ENGINE | gas_hc | max | inside | VVT_FAILURE | FAIL |
| 456 | TH-BND-WORN_ENGINE-gas_hc-max+eps | WORN_ENGINE | gas_hc | max+eps | outside | VVT_FAILURE | PASS |
| 457 | TH-BND-WORN_ENGINE-gas_co-min-eps | WORN_ENGINE | gas_co | min-eps | outside | WORN_VALVE_SEALS | PASS |
| 458 | TH-BND-WORN_ENGINE-gas_co-min | WORN_ENGINE | gas_co | min | inside | WORN_VALVE_SEALS | FAIL |
| 459 | TH-BND-WORN_ENGINE-gas_co-min+eps | WORN_ENGINE | gas_co | min+eps | inside | WORN_VALVE_SEALS | FAIL |
| 460 | TH-BND-WORN_ENGINE-gas_co-max-eps | WORN_ENGINE | gas_co | max-eps | inside | VVT_FAILURE | FAIL |
| 461 | TH-BND-WORN_ENGINE-gas_co-max | WORN_ENGINE | gas_co | max | inside | VVT_FAILURE | FAIL |
| 462 | TH-BND-WORN_ENGINE-gas_co-max+eps | WORN_ENGINE | gas_co | max+eps | outside | VVT_FAILURE | PASS |
| 463 | TH-BND-WORN_ENGINE-gas_co2-min-eps | WORN_ENGINE | gas_co2 | min-eps | outside | SAMPLE_INVALID | PASS |
| 464 | TH-BND-WORN_ENGINE-gas_co2-min | WORN_ENGINE | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 465 | TH-BND-WORN_ENGINE-gas_co2-min+eps | WORN_ENGINE | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 466 | TH-BND-WORN_ENGINE-gas_co2-max-eps | WORN_ENGINE | gas_co2 | max-eps | inside | VVT_FAILURE | FAIL |
| 467 | TH-BND-WORN_ENGINE-gas_co2-max | WORN_ENGINE | gas_co2 | max | inside | VVT_FAILURE | FAIL |
| 468 | TH-BND-WORN_ENGINE-gas_co2-max+eps | WORN_ENGINE | gas_co2 | max+eps | outside | NORMAL_OPERATION | PASS |
| 469 | TH-BND-WORN_ENGINE-gas_o2-min-eps | WORN_ENGINE | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 470 | TH-BND-WORN_ENGINE-gas_o2-min | WORN_ENGINE | gas_o2 | min | inside | VVT_FAILURE | FAIL |
| 471 | TH-BND-WORN_ENGINE-gas_o2-min+eps | WORN_ENGINE | gas_o2 | min+eps | inside | VVT_FAILURE | FAIL |
| 472 | TH-BND-WORN_ENGINE-gas_o2-max-eps | WORN_ENGINE | gas_o2 | max-eps | inside | WORN_ENGINE | PASS |
| 473 | TH-BND-WORN_ENGINE-gas_o2-max | WORN_ENGINE | gas_o2 | max | inside | WORN_ENGINE | PASS |
| 474 | TH-BND-WORN_ENGINE-gas_o2-max+eps | WORN_ENGINE | gas_o2 | max+eps | outside | VVT_FAILURE | PASS |
| 475 | TH-BND-WORN_ENGINE-gas_nox-min-eps | WORN_ENGINE | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 476 | TH-BND-WORN_ENGINE-gas_nox-min | WORN_ENGINE | gas_nox | min | inside | VVT_FAILURE | FAIL |
| 477 | TH-BND-WORN_ENGINE-gas_nox-min+eps | WORN_ENGINE | gas_nox | min+eps | inside | VVT_FAILURE | FAIL |
| 478 | TH-BND-WORN_ENGINE-gas_nox-max-eps | WORN_ENGINE | gas_nox | max-eps | inside | VVT_FAILURE | FAIL |
| 479 | TH-BND-WORN_ENGINE-gas_nox-max | WORN_ENGINE | gas_nox | max | inside | VVT_FAILURE | FAIL |
| 480 | TH-BND-WORN_ENGINE-gas_nox-max+eps | WORN_ENGINE | gas_nox | max+eps | outside | VVT_FAILURE | PASS |
| 481 | TH-BND-FLAT_CAMSHAFT-gas_hc-min-eps | FLAT_CAMSHAFT | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 482 | TH-BND-FLAT_CAMSHAFT-gas_hc-min | FLAT_CAMSHAFT | gas_hc | min | inside | TIMING_RETARDED | FAIL |
| 483 | TH-BND-FLAT_CAMSHAFT-gas_hc-min+eps | FLAT_CAMSHAFT | gas_hc | min+eps | inside | TIMING_RETARDED | FAIL |
| 484 | TH-BND-FLAT_CAMSHAFT-gas_hc-max-eps | FLAT_CAMSHAFT | gas_hc | max-eps | inside | TIMING_RETARDED | FAIL |
| 485 | TH-BND-FLAT_CAMSHAFT-gas_hc-max | FLAT_CAMSHAFT | gas_hc | max | inside | TIMING_RETARDED | FAIL |
| 486 | TH-BND-FLAT_CAMSHAFT-gas_hc-max+eps | FLAT_CAMSHAFT | gas_hc | max+eps | outside | WORN_VALVE_SEALS | PASS |
| 487 | TH-BND-FLAT_CAMSHAFT-gas_co-min-eps | FLAT_CAMSHAFT | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 488 | TH-BND-FLAT_CAMSHAFT-gas_co-min | FLAT_CAMSHAFT | gas_co | min | inside | TIMING_RETARDED | FAIL |
| 489 | TH-BND-FLAT_CAMSHAFT-gas_co-min+eps | FLAT_CAMSHAFT | gas_co | min+eps | inside | TIMING_RETARDED | FAIL |
| 490 | TH-BND-FLAT_CAMSHAFT-gas_co-max-eps | FLAT_CAMSHAFT | gas_co | max-eps | inside | TIMING_RETARDED | FAIL |
| 491 | TH-BND-FLAT_CAMSHAFT-gas_co-max | FLAT_CAMSHAFT | gas_co | max | inside | TIMING_RETARDED | FAIL |
| 492 | TH-BND-FLAT_CAMSHAFT-gas_co-max+eps | FLAT_CAMSHAFT | gas_co | max+eps | outside | O2_SENSOR_BIASED_LOW | PASS |
| 493 | TH-BND-FLAT_CAMSHAFT-gas_co2-min-eps | FLAT_CAMSHAFT | gas_co2 | min-eps | outside | SAMPLE_INVALID | PASS |
| 494 | TH-BND-FLAT_CAMSHAFT-gas_co2-min | FLAT_CAMSHAFT | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 495 | TH-BND-FLAT_CAMSHAFT-gas_co2-min+eps | FLAT_CAMSHAFT | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 496 | TH-BND-FLAT_CAMSHAFT-gas_co2-max-eps | FLAT_CAMSHAFT | gas_co2 | max-eps | inside | TIMING_RETARDED | FAIL |
| 497 | TH-BND-FLAT_CAMSHAFT-gas_co2-max | FLAT_CAMSHAFT | gas_co2 | max | inside | TIMING_RETARDED | FAIL |
| 498 | TH-BND-FLAT_CAMSHAFT-gas_co2-max+eps | FLAT_CAMSHAFT | gas_co2 | max+eps | outside | NORMAL_OPERATION | PASS |
| 499 | TH-BND-FLAT_CAMSHAFT-gas_o2-min-eps | FLAT_CAMSHAFT | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 500 | TH-BND-FLAT_CAMSHAFT-gas_o2-min | FLAT_CAMSHAFT | gas_o2 | min | inside | TIMING_RETARDED | FAIL |
| 501 | TH-BND-FLAT_CAMSHAFT-gas_o2-min+eps | FLAT_CAMSHAFT | gas_o2 | min+eps | inside | TIMING_RETARDED | FAIL |
| 502 | TH-BND-FLAT_CAMSHAFT-gas_o2-max-eps | FLAT_CAMSHAFT | gas_o2 | max-eps | inside | TIMING_RETARDED | FAIL |
| 503 | TH-BND-FLAT_CAMSHAFT-gas_o2-max | FLAT_CAMSHAFT | gas_o2 | max | inside | TIMING_RETARDED | FAIL |
| 504 | TH-BND-FLAT_CAMSHAFT-gas_o2-max+eps | FLAT_CAMSHAFT | gas_o2 | max+eps | outside | VVT_FAILURE | PASS |
| 505 | TH-BND-FLAT_CAMSHAFT-gas_nox-min-eps | FLAT_CAMSHAFT | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 506 | TH-BND-FLAT_CAMSHAFT-gas_nox-min | FLAT_CAMSHAFT | gas_nox | min | inside | TIMING_RETARDED | FAIL |
| 507 | TH-BND-FLAT_CAMSHAFT-gas_nox-min+eps | FLAT_CAMSHAFT | gas_nox | min+eps | inside | TIMING_RETARDED | FAIL |
| 508 | TH-BND-FLAT_CAMSHAFT-gas_nox-max-eps | FLAT_CAMSHAFT | gas_nox | max-eps | inside | WORN_PISTON_RINGS | FAIL |
| 509 | TH-BND-FLAT_CAMSHAFT-gas_nox-max | FLAT_CAMSHAFT | gas_nox | max | inside | WORN_PISTON_RINGS | FAIL |
| 510 | TH-BND-FLAT_CAMSHAFT-gas_nox-max+eps | FLAT_CAMSHAFT | gas_nox | max+eps | outside | VVT_FAILURE | PASS |
| 511 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_hc-min-eps | GDI_INTAKE_VALVE_CARBON | gas_hc | min-eps | outside | SAMPLE_INVALID | PASS |
| 512 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_hc-min | GDI_INTAKE_VALVE_CARBON | gas_hc | min | inside | SAMPLE_INVALID | FAIL |
| 513 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_hc-min+eps | GDI_INTAKE_VALVE_CARBON | gas_hc | min+eps | inside | SAMPLE_INVALID | FAIL |
| 514 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_hc-max-eps | GDI_INTAKE_VALVE_CARBON | gas_hc | max-eps | inside | SAMPLE_INVALID | FAIL |
| 515 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_hc-max | GDI_INTAKE_VALVE_CARBON | gas_hc | max | inside | SAMPLE_INVALID | FAIL |
| 516 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_hc-max+eps | GDI_INTAKE_VALVE_CARBON | gas_hc | max+eps | outside | ERROR:ValueError | PASS |
| 517 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co-min-eps | GDI_INTAKE_VALVE_CARBON | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 518 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co-min | GDI_INTAKE_VALVE_CARBON | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 519 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co-min+eps | GDI_INTAKE_VALVE_CARBON | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 520 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co-max-eps | GDI_INTAKE_VALVE_CARBON | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 521 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co-max | GDI_INTAKE_VALVE_CARBON | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 522 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co-max+eps | GDI_INTAKE_VALVE_CARBON | gas_co | max+eps | outside | SAMPLE_INVALID | PASS |
| 523 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co2-min-eps | GDI_INTAKE_VALVE_CARBON | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 524 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co2-min | GDI_INTAKE_VALVE_CARBON | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 525 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co2-min+eps | GDI_INTAKE_VALVE_CARBON | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 526 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co2-max-eps | GDI_INTAKE_VALVE_CARBON | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 527 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co2-max | GDI_INTAKE_VALVE_CARBON | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 528 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co2-max+eps | GDI_INTAKE_VALVE_CARBON | gas_co2 | max+eps | outside | SAMPLE_INVALID | PASS |
| 529 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_o2-min-eps | GDI_INTAKE_VALVE_CARBON | gas_o2 | min-eps | outside | SAMPLE_INVALID | PASS |
| 530 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_o2-min | GDI_INTAKE_VALVE_CARBON | gas_o2 | min | inside | SAMPLE_INVALID | FAIL |
| 531 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_o2-min+eps | GDI_INTAKE_VALVE_CARBON | gas_o2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 532 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_o2-max-eps | GDI_INTAKE_VALVE_CARBON | gas_o2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 533 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_o2-max | GDI_INTAKE_VALVE_CARBON | gas_o2 | max | inside | SAMPLE_INVALID | FAIL |
| 534 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_o2-max+eps | GDI_INTAKE_VALVE_CARBON | gas_o2 | max+eps | outside | ERROR:ValueError | PASS |
| 535 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_nox-min-eps | GDI_INTAKE_VALVE_CARBON | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 536 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_nox-min | GDI_INTAKE_VALVE_CARBON | gas_nox | min | inside | SAMPLE_INVALID | FAIL |
| 537 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_nox-min+eps | GDI_INTAKE_VALVE_CARBON | gas_nox | min+eps | inside | SAMPLE_INVALID | FAIL |
| 538 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_nox-max-eps | GDI_INTAKE_VALVE_CARBON | gas_nox | max-eps | inside | SAMPLE_INVALID | FAIL |
| 539 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_nox-max | GDI_INTAKE_VALVE_CARBON | gas_nox | max | inside | SAMPLE_INVALID | FAIL |
| 540 | TH-BND-GDI_INTAKE_VALVE_CARBO-gas_nox-max+eps | GDI_INTAKE_VALVE_CARBON | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 541 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_hc-min-eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_hc | min-eps | outside | CATALYST_OVERWHELMED | PASS |
| 542 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_hc-min | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_hc | min | inside | CATALYST_OVERWHELMED | FAIL |
| 543 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_hc-min+eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_hc | min+eps | inside | CATALYST_OVERWHELMED | FAIL |
| 544 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_hc-max-eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_hc | max-eps | inside | NORMAL_OPERATION | FAIL |
| 545 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_hc-max | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_hc | max | inside | NORMAL_OPERATION | FAIL |
| 546 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_hc-max+eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_hc | max+eps | outside | ERROR:ValueError | PASS |
| 547 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_co-min-eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_co | min-eps | outside | SAMPLE_INVALID | PASS |
| 548 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_co-min | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 549 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_co-min+eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 550 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_co-max-eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 551 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_co-max | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 552 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_co-max+eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 553 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_co2-min-eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 554 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_co2-min | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 555 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_co2-min+eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 556 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_co2-max-eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 557 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_co2-max | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 558 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_co2-max+eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_co2 | max+eps | outside | SAMPLE_INVALID | PASS |
| 559 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_o2-min-eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 560 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_o2-min | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_o2 | min | inside | NORMAL_OPERATION | FAIL |
| 561 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_o2-min+eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_o2 | min+eps | inside | NORMAL_OPERATION | FAIL |
| 562 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_o2-max-eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_o2 | max-eps | inside | NORMAL_OPERATION | FAIL |
| 563 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_o2-max | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_o2 | max | inside | NORMAL_OPERATION | FAIL |
| 564 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_o2-max+eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_o2 | max+eps | outside | NORMAL_OPERATION | PASS |
| 565 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_nox-min-eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 566 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_nox-min | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_nox | min | inside | NORMAL_OPERATION | FAIL |
| 567 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_nox-min+eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_nox | min+eps | inside | NORMAL_OPERATION | FAIL |
| 568 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_nox-max-eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_nox | max-eps | inside | NORMAL_OPERATION | FAIL |
| 569 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_nox-max | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_nox | max | inside | NORMAL_OPERATION | FAIL |
| 570 | TH-BND-VACUUM_REGULATOR_DIAPH-gas_nox-max+eps | VACUUM_REGULATOR_DIAPHRAGM_RUPTURE | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 571 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_hc-min-eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_hc | min-eps | outside | CATALYST_OVERWHELMED | PASS |
| 572 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_hc-min | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_hc | min | inside | CATALYST_OVERWHELMED | FAIL |
| 573 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_hc-min+eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_hc | min+eps | inside | CATALYST_OVERWHELMED | FAIL |
| 574 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_hc-max-eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_hc | max-eps | inside | NORMAL_OPERATION | FAIL |
| 575 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_hc-max | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_hc | max | inside | NORMAL_OPERATION | FAIL |
| 576 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_hc-max+eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_hc | max+eps | outside | ERROR:ValueError | PASS |
| 577 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co-min-eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_co | min-eps | outside | SAMPLE_INVALID | PASS |
| 578 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co-min | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 579 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co-min+eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 580 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co-max-eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 581 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co-max | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 582 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co-max+eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 583 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co2-min-eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 584 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co2-min | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 585 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co2-min+eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 586 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co2-max-eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 587 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co2-max | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 588 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co2-max+eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_co2 | max+eps | outside | SAMPLE_INVALID | PASS |
| 589 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_o2-min-eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 590 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_o2-min | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_o2 | min | inside | NORMAL_OPERATION | FAIL |
| 591 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_o2-min+eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_o2 | min+eps | inside | NORMAL_OPERATION | FAIL |
| 592 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_o2-max-eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_o2 | max-eps | inside | NORMAL_OPERATION | FAIL |
| 593 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_o2-max | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_o2 | max | inside | NORMAL_OPERATION | FAIL |
| 594 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_o2-max+eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_o2 | max+eps | outside | NORMAL_OPERATION | PASS |
| 595 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_nox-min-eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 596 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_nox-min | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_nox | min | inside | NORMAL_OPERATION | FAIL |
| 597 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_nox-min+eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_nox | min+eps | inside | NORMAL_OPERATION | FAIL |
| 598 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_nox-max-eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_nox | max-eps | inside | NORMAL_OPERATION | FAIL |
| 599 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_nox-max | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_nox | max | inside | NORMAL_OPERATION | FAIL |
| 600 | TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_nox-max+eps | GDI_HPFP_INTERNAL_SEAL_LEAK | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 601 | TH-BND-WORN_VALVE_SEALS-gas_hc-min-eps | WORN_VALVE_SEALS | gas_hc | min-eps | outside | SAMPLE_INVALID | PASS |
| 602 | TH-BND-WORN_VALVE_SEALS-gas_hc-min | WORN_VALVE_SEALS | gas_hc | min | inside | SAMPLE_INVALID | FAIL |
| 603 | TH-BND-WORN_VALVE_SEALS-gas_hc-min+eps | WORN_VALVE_SEALS | gas_hc | min+eps | inside | SAMPLE_INVALID | FAIL |
| 604 | TH-BND-WORN_VALVE_SEALS-gas_hc-max-eps | WORN_VALVE_SEALS | gas_hc | max-eps | inside | SAMPLE_INVALID | FAIL |
| 605 | TH-BND-WORN_VALVE_SEALS-gas_hc-max | WORN_VALVE_SEALS | gas_hc | max | inside | SAMPLE_INVALID | FAIL |
| 606 | TH-BND-WORN_VALVE_SEALS-gas_hc-max+eps | WORN_VALVE_SEALS | gas_hc | max+eps | outside | SAMPLE_INVALID | PASS |
| 607 | TH-BND-WORN_VALVE_SEALS-gas_co-min-eps | WORN_VALVE_SEALS | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 608 | TH-BND-WORN_VALVE_SEALS-gas_co-min | WORN_VALVE_SEALS | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 609 | TH-BND-WORN_VALVE_SEALS-gas_co-min+eps | WORN_VALVE_SEALS | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 610 | TH-BND-WORN_VALVE_SEALS-gas_co-max-eps | WORN_VALVE_SEALS | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 611 | TH-BND-WORN_VALVE_SEALS-gas_co-max | WORN_VALVE_SEALS | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 612 | TH-BND-WORN_VALVE_SEALS-gas_co-max+eps | WORN_VALVE_SEALS | gas_co | max+eps | outside | SAMPLE_INVALID | PASS |
| 613 | TH-BND-WORN_VALVE_SEALS-gas_co2-min-eps | WORN_VALVE_SEALS | gas_co2 | min-eps | outside | SAMPLE_INVALID | PASS |
| 614 | TH-BND-WORN_VALVE_SEALS-gas_co2-min | WORN_VALVE_SEALS | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 615 | TH-BND-WORN_VALVE_SEALS-gas_co2-min+eps | WORN_VALVE_SEALS | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 616 | TH-BND-WORN_VALVE_SEALS-gas_co2-max-eps | WORN_VALVE_SEALS | gas_co2 | max-eps | inside | VVT_FAILURE | FAIL |
| 617 | TH-BND-WORN_VALVE_SEALS-gas_co2-max | WORN_VALVE_SEALS | gas_co2 | max | inside | VVT_FAILURE | FAIL |
| 618 | TH-BND-WORN_VALVE_SEALS-gas_co2-max+eps | WORN_VALVE_SEALS | gas_co2 | max+eps | outside | VVT_FAILURE | PASS |
| 619 | TH-BND-WORN_VALVE_SEALS-gas_o2-min-eps | WORN_VALVE_SEALS | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 620 | TH-BND-WORN_VALVE_SEALS-gas_o2-min | WORN_VALVE_SEALS | gas_o2 | min | inside | SAMPLE_INVALID | FAIL |
| 621 | TH-BND-WORN_VALVE_SEALS-gas_o2-min+eps | WORN_VALVE_SEALS | gas_o2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 622 | TH-BND-WORN_VALVE_SEALS-gas_o2-max-eps | WORN_VALVE_SEALS | gas_o2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 623 | TH-BND-WORN_VALVE_SEALS-gas_o2-max | WORN_VALVE_SEALS | gas_o2 | max | inside | SAMPLE_INVALID | FAIL |
| 624 | TH-BND-WORN_VALVE_SEALS-gas_o2-max+eps | WORN_VALVE_SEALS | gas_o2 | max+eps | outside | SAMPLE_INVALID | PASS |
| 625 | TH-BND-WORN_VALVE_SEALS-gas_nox-min-eps | WORN_VALVE_SEALS | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 626 | TH-BND-WORN_VALVE_SEALS-gas_nox-min | WORN_VALVE_SEALS | gas_nox | min | inside | SAMPLE_INVALID | FAIL |
| 627 | TH-BND-WORN_VALVE_SEALS-gas_nox-min+eps | WORN_VALVE_SEALS | gas_nox | min+eps | inside | SAMPLE_INVALID | FAIL |
| 628 | TH-BND-WORN_VALVE_SEALS-gas_nox-max-eps | WORN_VALVE_SEALS | gas_nox | max-eps | inside | SAMPLE_INVALID | FAIL |
| 629 | TH-BND-WORN_VALVE_SEALS-gas_nox-max | WORN_VALVE_SEALS | gas_nox | max | inside | SAMPLE_INVALID | FAIL |
| 630 | TH-BND-WORN_VALVE_SEALS-gas_nox-max+eps | WORN_VALVE_SEALS | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 631 | TH-BND-WORN_PISTON_RINGS-gas_hc-min-eps | WORN_PISTON_RINGS | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 632 | TH-BND-WORN_PISTON_RINGS-gas_hc-min | WORN_PISTON_RINGS | gas_hc | min | inside | TIMING_RETARDED | FAIL |
| 633 | TH-BND-WORN_PISTON_RINGS-gas_hc-min+eps | WORN_PISTON_RINGS | gas_hc | min+eps | inside | TIMING_RETARDED | FAIL |
| 634 | TH-BND-WORN_PISTON_RINGS-gas_hc-max-eps | WORN_PISTON_RINGS | gas_hc | max-eps | inside | TIMING_RETARDED | FAIL |
| 635 | TH-BND-WORN_PISTON_RINGS-gas_hc-max | WORN_PISTON_RINGS | gas_hc | max | inside | TIMING_RETARDED | FAIL |
| 636 | TH-BND-WORN_PISTON_RINGS-gas_hc-max+eps | WORN_PISTON_RINGS | gas_hc | max+eps | outside | WORN_ENGINE | PASS |
| 637 | TH-BND-WORN_PISTON_RINGS-gas_co-min-eps | WORN_PISTON_RINGS | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 638 | TH-BND-WORN_PISTON_RINGS-gas_co-min | WORN_PISTON_RINGS | gas_co | min | inside | TIMING_RETARDED | FAIL |
| 639 | TH-BND-WORN_PISTON_RINGS-gas_co-min+eps | WORN_PISTON_RINGS | gas_co | min+eps | inside | TIMING_RETARDED | FAIL |
| 640 | TH-BND-WORN_PISTON_RINGS-gas_co-max-eps | WORN_PISTON_RINGS | gas_co | max-eps | inside | TIMING_RETARDED | FAIL |
| 641 | TH-BND-WORN_PISTON_RINGS-gas_co-max | WORN_PISTON_RINGS | gas_co | max | inside | TIMING_RETARDED | FAIL |
| 642 | TH-BND-WORN_PISTON_RINGS-gas_co-max+eps | WORN_PISTON_RINGS | gas_co | max+eps | outside | O2_SENSOR_BIASED_LOW | PASS |
| 643 | TH-BND-WORN_PISTON_RINGS-gas_co2-min-eps | WORN_PISTON_RINGS | gas_co2 | min-eps | outside | TIMING_RETARDED | PASS |
| 644 | TH-BND-WORN_PISTON_RINGS-gas_co2-min | WORN_PISTON_RINGS | gas_co2 | min | inside | TIMING_RETARDED | FAIL |
| 645 | TH-BND-WORN_PISTON_RINGS-gas_co2-min+eps | WORN_PISTON_RINGS | gas_co2 | min+eps | inside | TIMING_RETARDED | FAIL |
| 646 | TH-BND-WORN_PISTON_RINGS-gas_co2-max-eps | WORN_PISTON_RINGS | gas_co2 | max-eps | inside | TIMING_RETARDED | FAIL |
| 647 | TH-BND-WORN_PISTON_RINGS-gas_co2-max | WORN_PISTON_RINGS | gas_co2 | max | inside | TIMING_RETARDED | FAIL |
| 648 | TH-BND-WORN_PISTON_RINGS-gas_co2-max+eps | WORN_PISTON_RINGS | gas_co2 | max+eps | outside | NORMAL_OPERATION | PASS |
| 649 | TH-BND-WORN_PISTON_RINGS-gas_o2-min-eps | WORN_PISTON_RINGS | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 650 | TH-BND-WORN_PISTON_RINGS-gas_o2-min | WORN_PISTON_RINGS | gas_o2 | min | inside | TIMING_RETARDED | FAIL |
| 651 | TH-BND-WORN_PISTON_RINGS-gas_o2-min+eps | WORN_PISTON_RINGS | gas_o2 | min+eps | inside | TIMING_RETARDED | FAIL |
| 652 | TH-BND-WORN_PISTON_RINGS-gas_o2-max-eps | WORN_PISTON_RINGS | gas_o2 | max-eps | inside | TIMING_RETARDED | FAIL |
| 653 | TH-BND-WORN_PISTON_RINGS-gas_o2-max | WORN_PISTON_RINGS | gas_o2 | max | inside | TIMING_RETARDED | FAIL |
| 654 | TH-BND-WORN_PISTON_RINGS-gas_o2-max+eps | WORN_PISTON_RINGS | gas_o2 | max+eps | outside | VVT_FAILURE | PASS |
| 655 | TH-BND-WORN_PISTON_RINGS-gas_nox-min-eps | WORN_PISTON_RINGS | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 656 | TH-BND-WORN_PISTON_RINGS-gas_nox-min | WORN_PISTON_RINGS | gas_nox | min | inside | TIMING_RETARDED | FAIL |
| 657 | TH-BND-WORN_PISTON_RINGS-gas_nox-min+eps | WORN_PISTON_RINGS | gas_nox | min+eps | inside | TIMING_RETARDED | FAIL |
| 658 | TH-BND-WORN_PISTON_RINGS-gas_nox-max-eps | WORN_PISTON_RINGS | gas_nox | max-eps | inside | WORN_PISTON_RINGS | PASS |
| 659 | TH-BND-WORN_PISTON_RINGS-gas_nox-max | WORN_PISTON_RINGS | gas_nox | max | inside | WORN_PISTON_RINGS | PASS |
| 660 | TH-BND-WORN_PISTON_RINGS-gas_nox-max+eps | WORN_PISTON_RINGS | gas_nox | max+eps | outside | VVT_FAILURE | PASS |
| 661 | TH-BND-POA_SIGNATURE-gas_hc-min-eps | POA_SIGNATURE | gas_hc | min-eps | outside | SAMPLE_INVALID | PASS |
| 662 | TH-BND-POA_SIGNATURE-gas_hc-min | POA_SIGNATURE | gas_hc | min | inside | SAMPLE_INVALID | FAIL |
| 663 | TH-BND-POA_SIGNATURE-gas_hc-min+eps | POA_SIGNATURE | gas_hc | min+eps | inside | SAMPLE_INVALID | FAIL |
| 664 | TH-BND-POA_SIGNATURE-gas_hc-max-eps | POA_SIGNATURE | gas_hc | max-eps | inside | SAMPLE_INVALID | FAIL |
| 665 | TH-BND-POA_SIGNATURE-gas_hc-max | POA_SIGNATURE | gas_hc | max | inside | SAMPLE_INVALID | FAIL |
| 666 | TH-BND-POA_SIGNATURE-gas_hc-max+eps | POA_SIGNATURE | gas_hc | max+eps | outside | ERROR:ValueError | PASS |
| 667 | TH-BND-POA_SIGNATURE-gas_co-min-eps | POA_SIGNATURE | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 668 | TH-BND-POA_SIGNATURE-gas_co-min | POA_SIGNATURE | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 669 | TH-BND-POA_SIGNATURE-gas_co-min+eps | POA_SIGNATURE | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 670 | TH-BND-POA_SIGNATURE-gas_co-max-eps | POA_SIGNATURE | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 671 | TH-BND-POA_SIGNATURE-gas_co-max | POA_SIGNATURE | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 672 | TH-BND-POA_SIGNATURE-gas_co-max+eps | POA_SIGNATURE | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 673 | TH-BND-POA_SIGNATURE-gas_co2-min-eps | POA_SIGNATURE | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 674 | TH-BND-POA_SIGNATURE-gas_co2-min | POA_SIGNATURE | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 675 | TH-BND-POA_SIGNATURE-gas_co2-min+eps | POA_SIGNATURE | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 676 | TH-BND-POA_SIGNATURE-gas_co2-max-eps | POA_SIGNATURE | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 677 | TH-BND-POA_SIGNATURE-gas_co2-max | POA_SIGNATURE | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 678 | TH-BND-POA_SIGNATURE-gas_co2-max+eps | POA_SIGNATURE | gas_co2 | max+eps | outside | SAMPLE_INVALID | PASS |
| 679 | TH-BND-POA_SIGNATURE-gas_o2-min-eps | POA_SIGNATURE | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 680 | TH-BND-POA_SIGNATURE-gas_o2-min | POA_SIGNATURE | gas_o2 | min | inside | NORMAL_OPERATION | FAIL |
| 681 | TH-BND-POA_SIGNATURE-gas_o2-min+eps | POA_SIGNATURE | gas_o2 | min+eps | inside | NORMAL_OPERATION | FAIL |
| 682 | TH-BND-POA_SIGNATURE-gas_o2-max-eps | POA_SIGNATURE | gas_o2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 683 | TH-BND-POA_SIGNATURE-gas_o2-max | POA_SIGNATURE | gas_o2 | max | inside | SAMPLE_INVALID | FAIL |
| 684 | TH-BND-POA_SIGNATURE-gas_o2-max+eps | POA_SIGNATURE | gas_o2 | max+eps | outside | ERROR:ValueError | PASS |
| 685 | TH-BND-POA_SIGNATURE-gas_nox-min-eps | POA_SIGNATURE | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 686 | TH-BND-POA_SIGNATURE-gas_nox-min | POA_SIGNATURE | gas_nox | min | inside | SAMPLE_INVALID | FAIL |
| 687 | TH-BND-POA_SIGNATURE-gas_nox-min+eps | POA_SIGNATURE | gas_nox | min+eps | inside | SAMPLE_INVALID | FAIL |
| 688 | TH-BND-POA_SIGNATURE-gas_nox-max-eps | POA_SIGNATURE | gas_nox | max-eps | inside | SAMPLE_INVALID | FAIL |
| 689 | TH-BND-POA_SIGNATURE-gas_nox-max | POA_SIGNATURE | gas_nox | max | inside | SAMPLE_INVALID | FAIL |
| 690 | TH-BND-POA_SIGNATURE-gas_nox-max+eps | POA_SIGNATURE | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 691 | TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-min-eps | CAM_TIMING_RETARDED_MAP | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 692 | TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-min | CAM_TIMING_RETARDED_MAP | gas_hc | min | inside | SAMPLE_INVALID | FAIL |
| 693 | TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-min+eps | CAM_TIMING_RETARDED_MAP | gas_hc | min+eps | inside | SAMPLE_INVALID | FAIL |
| 694 | TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-max-eps | CAM_TIMING_RETARDED_MAP | gas_hc | max-eps | inside | SAMPLE_INVALID | FAIL |
| 695 | TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-max | CAM_TIMING_RETARDED_MAP | gas_hc | max | inside | SAMPLE_INVALID | FAIL |
| 696 | TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-max+eps | CAM_TIMING_RETARDED_MAP | gas_hc | max+eps | outside | ERROR:ValueError | PASS |
| 697 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co-min-eps | CAM_TIMING_RETARDED_MAP | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 698 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co-min | CAM_TIMING_RETARDED_MAP | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 699 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co-min+eps | CAM_TIMING_RETARDED_MAP | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 700 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co-max-eps | CAM_TIMING_RETARDED_MAP | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 701 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co-max | CAM_TIMING_RETARDED_MAP | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 702 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co-max+eps | CAM_TIMING_RETARDED_MAP | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 703 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-min-eps | CAM_TIMING_RETARDED_MAP | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 704 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-min | CAM_TIMING_RETARDED_MAP | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 705 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-min+eps | CAM_TIMING_RETARDED_MAP | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 706 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-max-eps | CAM_TIMING_RETARDED_MAP | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 707 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-max | CAM_TIMING_RETARDED_MAP | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 708 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-max+eps | CAM_TIMING_RETARDED_MAP | gas_co2 | max+eps | outside | ERROR:ValueError | PASS |
| 709 | TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-min-eps | CAM_TIMING_RETARDED_MAP | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 710 | TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-min | CAM_TIMING_RETARDED_MAP | gas_o2 | min | inside | SAMPLE_INVALID | FAIL |
| 711 | TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-min+eps | CAM_TIMING_RETARDED_MAP | gas_o2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 712 | TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-max-eps | CAM_TIMING_RETARDED_MAP | gas_o2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 713 | TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-max | CAM_TIMING_RETARDED_MAP | gas_o2 | max | inside | SAMPLE_INVALID | FAIL |
| 714 | TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-max+eps | CAM_TIMING_RETARDED_MAP | gas_o2 | max+eps | outside | ERROR:ValueError | PASS |
| 715 | TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-min-eps | CAM_TIMING_RETARDED_MAP | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 716 | TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-min | CAM_TIMING_RETARDED_MAP | gas_nox | min | inside | SAMPLE_INVALID | FAIL |
| 717 | TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-min+eps | CAM_TIMING_RETARDED_MAP | gas_nox | min+eps | inside | SAMPLE_INVALID | FAIL |
| 718 | TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-max-eps | CAM_TIMING_RETARDED_MAP | gas_nox | max-eps | inside | SAMPLE_INVALID | FAIL |
| 719 | TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-max | CAM_TIMING_RETARDED_MAP | gas_nox | max | inside | SAMPLE_INVALID | FAIL |
| 720 | TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-max+eps | CAM_TIMING_RETARDED_MAP | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 721 | TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-min-eps | CAM_TIMING_RETARDED_MAF | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 722 | TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-min | CAM_TIMING_RETARDED_MAF | gas_hc | min | inside | SAMPLE_INVALID | FAIL |
| 723 | TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-min+eps | CAM_TIMING_RETARDED_MAF | gas_hc | min+eps | inside | SAMPLE_INVALID | FAIL |
| 724 | TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-max-eps | CAM_TIMING_RETARDED_MAF | gas_hc | max-eps | inside | SAMPLE_INVALID | FAIL |
| 725 | TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-max | CAM_TIMING_RETARDED_MAF | gas_hc | max | inside | SAMPLE_INVALID | FAIL |
| 726 | TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-max+eps | CAM_TIMING_RETARDED_MAF | gas_hc | max+eps | outside | ERROR:ValueError | PASS |
| 727 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co-min-eps | CAM_TIMING_RETARDED_MAF | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 728 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co-min | CAM_TIMING_RETARDED_MAF | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 729 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co-min+eps | CAM_TIMING_RETARDED_MAF | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 730 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co-max-eps | CAM_TIMING_RETARDED_MAF | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 731 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co-max | CAM_TIMING_RETARDED_MAF | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 732 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co-max+eps | CAM_TIMING_RETARDED_MAF | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 733 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-min-eps | CAM_TIMING_RETARDED_MAF | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 734 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-min | CAM_TIMING_RETARDED_MAF | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 735 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-min+eps | CAM_TIMING_RETARDED_MAF | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 736 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-max-eps | CAM_TIMING_RETARDED_MAF | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 737 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-max | CAM_TIMING_RETARDED_MAF | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 738 | TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-max+eps | CAM_TIMING_RETARDED_MAF | gas_co2 | max+eps | outside | ERROR:ValueError | PASS |
| 739 | TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-min-eps | CAM_TIMING_RETARDED_MAF | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 740 | TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-min | CAM_TIMING_RETARDED_MAF | gas_o2 | min | inside | SAMPLE_INVALID | FAIL |
| 741 | TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-min+eps | CAM_TIMING_RETARDED_MAF | gas_o2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 742 | TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-max-eps | CAM_TIMING_RETARDED_MAF | gas_o2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 743 | TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-max | CAM_TIMING_RETARDED_MAF | gas_o2 | max | inside | SAMPLE_INVALID | FAIL |
| 744 | TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-max+eps | CAM_TIMING_RETARDED_MAF | gas_o2 | max+eps | outside | ERROR:ValueError | PASS |
| 745 | TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-min-eps | CAM_TIMING_RETARDED_MAF | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 746 | TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-min | CAM_TIMING_RETARDED_MAF | gas_nox | min | inside | SAMPLE_INVALID | FAIL |
| 747 | TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-min+eps | CAM_TIMING_RETARDED_MAF | gas_nox | min+eps | inside | SAMPLE_INVALID | FAIL |
| 748 | TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-max-eps | CAM_TIMING_RETARDED_MAF | gas_nox | max-eps | inside | SAMPLE_INVALID | FAIL |
| 749 | TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-max | CAM_TIMING_RETARDED_MAF | gas_nox | max | inside | SAMPLE_INVALID | FAIL |
| 750 | TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-max+eps | CAM_TIMING_RETARDED_MAF | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 751 | TH-BND-CAM_TIMING_ADVANCED-gas_hc-min-eps | CAM_TIMING_ADVANCED | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 752 | TH-BND-CAM_TIMING_ADVANCED-gas_hc-min | CAM_TIMING_ADVANCED | gas_hc | min | inside | SAMPLE_INVALID | FAIL |
| 753 | TH-BND-CAM_TIMING_ADVANCED-gas_hc-min+eps | CAM_TIMING_ADVANCED | gas_hc | min+eps | inside | SAMPLE_INVALID | FAIL |
| 754 | TH-BND-CAM_TIMING_ADVANCED-gas_hc-max-eps | CAM_TIMING_ADVANCED | gas_hc | max-eps | inside | SAMPLE_INVALID | FAIL |
| 755 | TH-BND-CAM_TIMING_ADVANCED-gas_hc-max | CAM_TIMING_ADVANCED | gas_hc | max | inside | SAMPLE_INVALID | FAIL |
| 756 | TH-BND-CAM_TIMING_ADVANCED-gas_hc-max+eps | CAM_TIMING_ADVANCED | gas_hc | max+eps | outside | ERROR:ValueError | PASS |
| 757 | TH-BND-CAM_TIMING_ADVANCED-gas_co-min-eps | CAM_TIMING_ADVANCED | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 758 | TH-BND-CAM_TIMING_ADVANCED-gas_co-min | CAM_TIMING_ADVANCED | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 759 | TH-BND-CAM_TIMING_ADVANCED-gas_co-min+eps | CAM_TIMING_ADVANCED | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 760 | TH-BND-CAM_TIMING_ADVANCED-gas_co-max-eps | CAM_TIMING_ADVANCED | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 761 | TH-BND-CAM_TIMING_ADVANCED-gas_co-max | CAM_TIMING_ADVANCED | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 762 | TH-BND-CAM_TIMING_ADVANCED-gas_co-max+eps | CAM_TIMING_ADVANCED | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 763 | TH-BND-CAM_TIMING_ADVANCED-gas_co2-min-eps | CAM_TIMING_ADVANCED | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 764 | TH-BND-CAM_TIMING_ADVANCED-gas_co2-min | CAM_TIMING_ADVANCED | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 765 | TH-BND-CAM_TIMING_ADVANCED-gas_co2-min+eps | CAM_TIMING_ADVANCED | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 766 | TH-BND-CAM_TIMING_ADVANCED-gas_co2-max-eps | CAM_TIMING_ADVANCED | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 767 | TH-BND-CAM_TIMING_ADVANCED-gas_co2-max | CAM_TIMING_ADVANCED | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 768 | TH-BND-CAM_TIMING_ADVANCED-gas_co2-max+eps | CAM_TIMING_ADVANCED | gas_co2 | max+eps | outside | ERROR:ValueError | PASS |
| 769 | TH-BND-CAM_TIMING_ADVANCED-gas_o2-min-eps | CAM_TIMING_ADVANCED | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 770 | TH-BND-CAM_TIMING_ADVANCED-gas_o2-min | CAM_TIMING_ADVANCED | gas_o2 | min | inside | SAMPLE_INVALID | FAIL |
| 771 | TH-BND-CAM_TIMING_ADVANCED-gas_o2-min+eps | CAM_TIMING_ADVANCED | gas_o2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 772 | TH-BND-CAM_TIMING_ADVANCED-gas_o2-max-eps | CAM_TIMING_ADVANCED | gas_o2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 773 | TH-BND-CAM_TIMING_ADVANCED-gas_o2-max | CAM_TIMING_ADVANCED | gas_o2 | max | inside | SAMPLE_INVALID | FAIL |
| 774 | TH-BND-CAM_TIMING_ADVANCED-gas_o2-max+eps | CAM_TIMING_ADVANCED | gas_o2 | max+eps | outside | ERROR:ValueError | PASS |
| 775 | TH-BND-CAM_TIMING_ADVANCED-gas_nox-min-eps | CAM_TIMING_ADVANCED | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 776 | TH-BND-CAM_TIMING_ADVANCED-gas_nox-min | CAM_TIMING_ADVANCED | gas_nox | min | inside | SAMPLE_INVALID | FAIL |
| 777 | TH-BND-CAM_TIMING_ADVANCED-gas_nox-min+eps | CAM_TIMING_ADVANCED | gas_nox | min+eps | inside | SAMPLE_INVALID | FAIL |
| 778 | TH-BND-CAM_TIMING_ADVANCED-gas_nox-max-eps | CAM_TIMING_ADVANCED | gas_nox | max-eps | inside | SAMPLE_INVALID | FAIL |
| 779 | TH-BND-CAM_TIMING_ADVANCED-gas_nox-max | CAM_TIMING_ADVANCED | gas_nox | max | inside | SAMPLE_INVALID | FAIL |
| 780 | TH-BND-CAM_TIMING_ADVANCED-gas_nox-max+eps | CAM_TIMING_ADVANCED | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 781 | TH-BND-EGR_STUCK_CLOSED-gas_hc-min-eps | EGR_STUCK_CLOSED | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 782 | TH-BND-EGR_STUCK_CLOSED-gas_hc-min | EGR_STUCK_CLOSED | gas_hc | min | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 783 | TH-BND-EGR_STUCK_CLOSED-gas_hc-min+eps | EGR_STUCK_CLOSED | gas_hc | min+eps | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 784 | TH-BND-EGR_STUCK_CLOSED-gas_hc-max-eps | EGR_STUCK_CLOSED | gas_hc | max-eps | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 785 | TH-BND-EGR_STUCK_CLOSED-gas_hc-max | EGR_STUCK_CLOSED | gas_hc | max | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 786 | TH-BND-EGR_STUCK_CLOSED-gas_hc-max+eps | EGR_STUCK_CLOSED | gas_hc | max+eps | outside | VVT_FAILURE | PASS |
| 787 | TH-BND-EGR_STUCK_CLOSED-gas_co-min-eps | EGR_STUCK_CLOSED | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 788 | TH-BND-EGR_STUCK_CLOSED-gas_co-min | EGR_STUCK_CLOSED | gas_co | min | inside | TIMING_OVER_ADVANCED | FAIL |
| 789 | TH-BND-EGR_STUCK_CLOSED-gas_co-min+eps | EGR_STUCK_CLOSED | gas_co | min+eps | inside | TIMING_OVER_ADVANCED | FAIL |
| 790 | TH-BND-EGR_STUCK_CLOSED-gas_co-max-eps | EGR_STUCK_CLOSED | gas_co | max-eps | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 791 | TH-BND-EGR_STUCK_CLOSED-gas_co-max | EGR_STUCK_CLOSED | gas_co | max | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 792 | TH-BND-EGR_STUCK_CLOSED-gas_co-max+eps | EGR_STUCK_CLOSED | gas_co | max+eps | outside | VVT_FAILURE | PASS |
| 793 | TH-BND-EGR_STUCK_CLOSED-gas_co2-min-eps | EGR_STUCK_CLOSED | gas_co2 | min-eps | outside | SAMPLE_INVALID | PASS |
| 794 | TH-BND-EGR_STUCK_CLOSED-gas_co2-min | EGR_STUCK_CLOSED | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 795 | TH-BND-EGR_STUCK_CLOSED-gas_co2-min+eps | EGR_STUCK_CLOSED | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 796 | TH-BND-EGR_STUCK_CLOSED-gas_co2-max-eps | EGR_STUCK_CLOSED | gas_co2 | max-eps | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 797 | TH-BND-EGR_STUCK_CLOSED-gas_co2-max | EGR_STUCK_CLOSED | gas_co2 | max | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 798 | TH-BND-EGR_STUCK_CLOSED-gas_co2-max+eps | EGR_STUCK_CLOSED | gas_co2 | max+eps | outside | NORMAL_OPERATION | PASS |
| 799 | TH-BND-EGR_STUCK_CLOSED-gas_o2-min-eps | EGR_STUCK_CLOSED | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 800 | TH-BND-EGR_STUCK_CLOSED-gas_o2-min | EGR_STUCK_CLOSED | gas_o2 | min | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 801 | TH-BND-EGR_STUCK_CLOSED-gas_o2-min+eps | EGR_STUCK_CLOSED | gas_o2 | min+eps | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 802 | TH-BND-EGR_STUCK_CLOSED-gas_o2-max-eps | EGR_STUCK_CLOSED | gas_o2 | max-eps | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 803 | TH-BND-EGR_STUCK_CLOSED-gas_o2-max | EGR_STUCK_CLOSED | gas_o2 | max | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 804 | TH-BND-EGR_STUCK_CLOSED-gas_o2-max+eps | EGR_STUCK_CLOSED | gas_o2 | max+eps | outside | VVT_FAILURE | PASS |
| 805 | TH-BND-EGR_STUCK_CLOSED-gas_nox-min-eps | EGR_STUCK_CLOSED | gas_nox | min-eps | outside | VVT_FAILURE | PASS |
| 806 | TH-BND-EGR_STUCK_CLOSED-gas_nox-min | EGR_STUCK_CLOSED | gas_nox | min | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 807 | TH-BND-EGR_STUCK_CLOSED-gas_nox-min+eps | EGR_STUCK_CLOSED | gas_nox | min+eps | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 808 | TH-BND-EGR_STUCK_CLOSED-gas_nox-max-eps | EGR_STUCK_CLOSED | gas_nox | max-eps | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 809 | TH-BND-EGR_STUCK_CLOSED-gas_nox-max | EGR_STUCK_CLOSED | gas_nox | max | inside | HIGH_COMBUSTION_TEMP | FAIL |
| 810 | TH-BND-EGR_STUCK_CLOSED-gas_nox-max+eps | EGR_STUCK_CLOSED | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 811 | TH-BND-EGR_STUCK_OPEN-gas_hc-min-eps | EGR_STUCK_OPEN | gas_hc | min-eps | outside | VVT_FAILURE | PASS |
| 812 | TH-BND-EGR_STUCK_OPEN-gas_hc-min | EGR_STUCK_OPEN | gas_hc | min | inside | VVT_FAILURE | FAIL |
| 813 | TH-BND-EGR_STUCK_OPEN-gas_hc-min+eps | EGR_STUCK_OPEN | gas_hc | min+eps | inside | VVT_FAILURE | FAIL |
| 814 | TH-BND-EGR_STUCK_OPEN-gas_hc-max-eps | EGR_STUCK_OPEN | gas_hc | max-eps | inside | NORMAL_OPERATION | FAIL |
| 815 | TH-BND-EGR_STUCK_OPEN-gas_hc-max | EGR_STUCK_OPEN | gas_hc | max | inside | NORMAL_OPERATION | FAIL |
| 816 | TH-BND-EGR_STUCK_OPEN-gas_hc-max+eps | EGR_STUCK_OPEN | gas_hc | max+eps | outside | ERROR:ValueError | PASS |
| 817 | TH-BND-EGR_STUCK_OPEN-gas_co-min-eps | EGR_STUCK_OPEN | gas_co | min-eps | outside | SAMPLE_INVALID | PASS |
| 818 | TH-BND-EGR_STUCK_OPEN-gas_co-min | EGR_STUCK_OPEN | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 819 | TH-BND-EGR_STUCK_OPEN-gas_co-min+eps | EGR_STUCK_OPEN | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 820 | TH-BND-EGR_STUCK_OPEN-gas_co-max-eps | EGR_STUCK_OPEN | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 821 | TH-BND-EGR_STUCK_OPEN-gas_co-max | EGR_STUCK_OPEN | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 822 | TH-BND-EGR_STUCK_OPEN-gas_co-max+eps | EGR_STUCK_OPEN | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 823 | TH-BND-EGR_STUCK_OPEN-gas_co2-min-eps | EGR_STUCK_OPEN | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 824 | TH-BND-EGR_STUCK_OPEN-gas_co2-min | EGR_STUCK_OPEN | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 825 | TH-BND-EGR_STUCK_OPEN-gas_co2-min+eps | EGR_STUCK_OPEN | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 826 | TH-BND-EGR_STUCK_OPEN-gas_co2-max-eps | EGR_STUCK_OPEN | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 827 | TH-BND-EGR_STUCK_OPEN-gas_co2-max | EGR_STUCK_OPEN | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 828 | TH-BND-EGR_STUCK_OPEN-gas_co2-max+eps | EGR_STUCK_OPEN | gas_co2 | max+eps | outside | SAMPLE_INVALID | PASS |
| 829 | TH-BND-EGR_STUCK_OPEN-gas_o2-min-eps | EGR_STUCK_OPEN | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 830 | TH-BND-EGR_STUCK_OPEN-gas_o2-min | EGR_STUCK_OPEN | gas_o2 | min | inside | NORMAL_OPERATION | FAIL |
| 831 | TH-BND-EGR_STUCK_OPEN-gas_o2-min+eps | EGR_STUCK_OPEN | gas_o2 | min+eps | inside | NORMAL_OPERATION | FAIL |
| 832 | TH-BND-EGR_STUCK_OPEN-gas_o2-max-eps | EGR_STUCK_OPEN | gas_o2 | max-eps | inside | NORMAL_OPERATION | FAIL |
| 833 | TH-BND-EGR_STUCK_OPEN-gas_o2-max | EGR_STUCK_OPEN | gas_o2 | max | inside | NORMAL_OPERATION | FAIL |
| 834 | TH-BND-EGR_STUCK_OPEN-gas_o2-max+eps | EGR_STUCK_OPEN | gas_o2 | max+eps | outside | RICH_MISFIRE | PASS |
| 835 | TH-BND-EGR_STUCK_OPEN-gas_nox-min-eps | EGR_STUCK_OPEN | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 836 | TH-BND-EGR_STUCK_OPEN-gas_nox-min | EGR_STUCK_OPEN | gas_nox | min | inside | NORMAL_OPERATION | FAIL |
| 837 | TH-BND-EGR_STUCK_OPEN-gas_nox-min+eps | EGR_STUCK_OPEN | gas_nox | min+eps | inside | NORMAL_OPERATION | FAIL |
| 838 | TH-BND-EGR_STUCK_OPEN-gas_nox-max-eps | EGR_STUCK_OPEN | gas_nox | max-eps | inside | NORMAL_OPERATION | FAIL |
| 839 | TH-BND-EGR_STUCK_OPEN-gas_nox-max | EGR_STUCK_OPEN | gas_nox | max | inside | NORMAL_OPERATION | FAIL |
| 840 | TH-BND-EGR_STUCK_OPEN-gas_nox-max+eps | EGR_STUCK_OPEN | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 841 | TH-BND-VVT_FAILURE-gas_hc-min-eps | VVT_FAILURE | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 842 | TH-BND-VVT_FAILURE-gas_hc-min | VVT_FAILURE | gas_hc | min | inside | SAMPLE_INVALID | FAIL |
| 843 | TH-BND-VVT_FAILURE-gas_hc-min+eps | VVT_FAILURE | gas_hc | min+eps | inside | SAMPLE_INVALID | FAIL |
| 844 | TH-BND-VVT_FAILURE-gas_hc-max-eps | VVT_FAILURE | gas_hc | max-eps | inside | SAMPLE_INVALID | FAIL |
| 845 | TH-BND-VVT_FAILURE-gas_hc-max | VVT_FAILURE | gas_hc | max | inside | SAMPLE_INVALID | FAIL |
| 846 | TH-BND-VVT_FAILURE-gas_hc-max+eps | VVT_FAILURE | gas_hc | max+eps | outside | SAMPLE_INVALID | PASS |
| 847 | TH-BND-VVT_FAILURE-gas_co-min-eps | VVT_FAILURE | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 848 | TH-BND-VVT_FAILURE-gas_co-min | VVT_FAILURE | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 849 | TH-BND-VVT_FAILURE-gas_co-min+eps | VVT_FAILURE | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 850 | TH-BND-VVT_FAILURE-gas_co-max-eps | VVT_FAILURE | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 851 | TH-BND-VVT_FAILURE-gas_co-max | VVT_FAILURE | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 852 | TH-BND-VVT_FAILURE-gas_co-max+eps | VVT_FAILURE | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 853 | TH-BND-VVT_FAILURE-gas_co2-min-eps | VVT_FAILURE | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 854 | TH-BND-VVT_FAILURE-gas_co2-min | VVT_FAILURE | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 855 | TH-BND-VVT_FAILURE-gas_co2-min+eps | VVT_FAILURE | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 856 | TH-BND-VVT_FAILURE-gas_co2-max-eps | VVT_FAILURE | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 857 | TH-BND-VVT_FAILURE-gas_co2-max | VVT_FAILURE | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 858 | TH-BND-VVT_FAILURE-gas_co2-max+eps | VVT_FAILURE | gas_co2 | max+eps | outside | ERROR:ValueError | PASS |
| 859 | TH-BND-VVT_FAILURE-gas_o2-min-eps | VVT_FAILURE | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 860 | TH-BND-VVT_FAILURE-gas_o2-min | VVT_FAILURE | gas_o2 | min | inside | SAMPLE_INVALID | FAIL |
| 861 | TH-BND-VVT_FAILURE-gas_o2-min+eps | VVT_FAILURE | gas_o2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 862 | TH-BND-VVT_FAILURE-gas_o2-max-eps | VVT_FAILURE | gas_o2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 863 | TH-BND-VVT_FAILURE-gas_o2-max | VVT_FAILURE | gas_o2 | max | inside | SAMPLE_INVALID | FAIL |
| 864 | TH-BND-VVT_FAILURE-gas_o2-max+eps | VVT_FAILURE | gas_o2 | max+eps | outside | ERROR:ValueError | PASS |
| 865 | TH-BND-VVT_FAILURE-gas_nox-min-eps | VVT_FAILURE | gas_nox | min-eps | outside | SAMPLE_INVALID | PASS |
| 866 | TH-BND-VVT_FAILURE-gas_nox-min | VVT_FAILURE | gas_nox | min | inside | SAMPLE_INVALID | FAIL |
| 867 | TH-BND-VVT_FAILURE-gas_nox-min+eps | VVT_FAILURE | gas_nox | min+eps | inside | SAMPLE_INVALID | FAIL |
| 868 | TH-BND-VVT_FAILURE-gas_nox-max-eps | VVT_FAILURE | gas_nox | max-eps | inside | SAMPLE_INVALID | FAIL |
| 869 | TH-BND-VVT_FAILURE-gas_nox-max | VVT_FAILURE | gas_nox | max | inside | SAMPLE_INVALID | FAIL |
| 870 | TH-BND-VVT_FAILURE-gas_nox-max+eps | VVT_FAILURE | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 871 | TH-BND-EVAP_CANISTER_SATURATE-gas_hc-min-eps | EVAP_CANISTER_SATURATED | gas_hc | min-eps | outside | SAMPLE_INVALID | PASS |
| 872 | TH-BND-EVAP_CANISTER_SATURATE-gas_hc-min | EVAP_CANISTER_SATURATED | gas_hc | min | inside | SAMPLE_INVALID | FAIL |
| 873 | TH-BND-EVAP_CANISTER_SATURATE-gas_hc-min+eps | EVAP_CANISTER_SATURATED | gas_hc | min+eps | inside | SAMPLE_INVALID | FAIL |
| 874 | TH-BND-EVAP_CANISTER_SATURATE-gas_hc-max-eps | EVAP_CANISTER_SATURATED | gas_hc | max-eps | inside | SAMPLE_INVALID | FAIL |
| 875 | TH-BND-EVAP_CANISTER_SATURATE-gas_hc-max | EVAP_CANISTER_SATURATED | gas_hc | max | inside | SAMPLE_INVALID | FAIL |
| 876 | TH-BND-EVAP_CANISTER_SATURATE-gas_hc-max+eps | EVAP_CANISTER_SATURATED | gas_hc | max+eps | outside | SAMPLE_INVALID | PASS |
| 877 | TH-BND-EVAP_CANISTER_SATURATE-gas_co-min-eps | EVAP_CANISTER_SATURATED | gas_co | min-eps | outside | SAMPLE_INVALID | PASS |
| 878 | TH-BND-EVAP_CANISTER_SATURATE-gas_co-min | EVAP_CANISTER_SATURATED | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 879 | TH-BND-EVAP_CANISTER_SATURATE-gas_co-min+eps | EVAP_CANISTER_SATURATED | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 880 | TH-BND-EVAP_CANISTER_SATURATE-gas_co-max-eps | EVAP_CANISTER_SATURATED | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 881 | TH-BND-EVAP_CANISTER_SATURATE-gas_co-max | EVAP_CANISTER_SATURATED | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 882 | TH-BND-EVAP_CANISTER_SATURATE-gas_co-max+eps | EVAP_CANISTER_SATURATED | gas_co | max+eps | outside | SAMPLE_INVALID | PASS |
| 883 | TH-BND-EVAP_CANISTER_SATURATE-gas_co2-min-eps | EVAP_CANISTER_SATURATED | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 884 | TH-BND-EVAP_CANISTER_SATURATE-gas_co2-min | EVAP_CANISTER_SATURATED | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 885 | TH-BND-EVAP_CANISTER_SATURATE-gas_co2-min+eps | EVAP_CANISTER_SATURATED | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 886 | TH-BND-EVAP_CANISTER_SATURATE-gas_co2-max-eps | EVAP_CANISTER_SATURATED | gas_co2 | max-eps | inside | EVAP_CANISTER_SATURATED | PASS |
| 887 | TH-BND-EVAP_CANISTER_SATURATE-gas_co2-max | EVAP_CANISTER_SATURATED | gas_co2 | max | inside | EVAP_CANISTER_SATURATED | PASS |
| 888 | TH-BND-EVAP_CANISTER_SATURATE-gas_co2-max+eps | EVAP_CANISTER_SATURATED | gas_co2 | max+eps | outside | VVT_FAILURE | PASS |
| 889 | TH-BND-EVAP_CANISTER_SATURATE-gas_o2-min-eps | EVAP_CANISTER_SATURATED | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 890 | TH-BND-EVAP_CANISTER_SATURATE-gas_o2-min | EVAP_CANISTER_SATURATED | gas_o2 | min | inside | SAMPLE_INVALID | FAIL |
| 891 | TH-BND-EVAP_CANISTER_SATURATE-gas_o2-min+eps | EVAP_CANISTER_SATURATED | gas_o2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 892 | TH-BND-EVAP_CANISTER_SATURATE-gas_o2-max-eps | EVAP_CANISTER_SATURATED | gas_o2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 893 | TH-BND-EVAP_CANISTER_SATURATE-gas_o2-max | EVAP_CANISTER_SATURATED | gas_o2 | max | inside | SAMPLE_INVALID | FAIL |
| 894 | TH-BND-EVAP_CANISTER_SATURATE-gas_o2-max+eps | EVAP_CANISTER_SATURATED | gas_o2 | max+eps | outside | SAMPLE_INVALID | PASS |
| 895 | TH-BND-EVAP_CANISTER_SATURATE-gas_nox-min-eps | EVAP_CANISTER_SATURATED | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 896 | TH-BND-EVAP_CANISTER_SATURATE-gas_nox-min | EVAP_CANISTER_SATURATED | gas_nox | min | inside | SAMPLE_INVALID | FAIL |
| 897 | TH-BND-EVAP_CANISTER_SATURATE-gas_nox-min+eps | EVAP_CANISTER_SATURATED | gas_nox | min+eps | inside | SAMPLE_INVALID | FAIL |
| 898 | TH-BND-EVAP_CANISTER_SATURATE-gas_nox-max-eps | EVAP_CANISTER_SATURATED | gas_nox | max-eps | inside | SAMPLE_INVALID | FAIL |
| 899 | TH-BND-EVAP_CANISTER_SATURATE-gas_nox-max | EVAP_CANISTER_SATURATED | gas_nox | max | inside | SAMPLE_INVALID | FAIL |
| 900 | TH-BND-EVAP_CANISTER_SATURATE-gas_nox-max+eps | EVAP_CANISTER_SATURATED | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 901 | TH-BND-EGR_DILUTION_MISFIRE-gas_hc-min-eps | EGR_DILUTION_MISFIRE | gas_hc | min-eps | outside | SAMPLE_INVALID | PASS |
| 902 | TH-BND-EGR_DILUTION_MISFIRE-gas_hc-min | EGR_DILUTION_MISFIRE | gas_hc | min | inside | SAMPLE_INVALID | FAIL |
| 903 | TH-BND-EGR_DILUTION_MISFIRE-gas_hc-min+eps | EGR_DILUTION_MISFIRE | gas_hc | min+eps | inside | SAMPLE_INVALID | FAIL |
| 904 | TH-BND-EGR_DILUTION_MISFIRE-gas_hc-max-eps | EGR_DILUTION_MISFIRE | gas_hc | max-eps | inside | SAMPLE_INVALID | FAIL |
| 905 | TH-BND-EGR_DILUTION_MISFIRE-gas_hc-max | EGR_DILUTION_MISFIRE | gas_hc | max | inside | SAMPLE_INVALID | FAIL |
| 906 | TH-BND-EGR_DILUTION_MISFIRE-gas_hc-max+eps | EGR_DILUTION_MISFIRE | gas_hc | max+eps | outside | ERROR:ValueError | PASS |
| 907 | TH-BND-EGR_DILUTION_MISFIRE-gas_co-min-eps | EGR_DILUTION_MISFIRE | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 908 | TH-BND-EGR_DILUTION_MISFIRE-gas_co-min | EGR_DILUTION_MISFIRE | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 909 | TH-BND-EGR_DILUTION_MISFIRE-gas_co-min+eps | EGR_DILUTION_MISFIRE | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 910 | TH-BND-EGR_DILUTION_MISFIRE-gas_co-max-eps | EGR_DILUTION_MISFIRE | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 911 | TH-BND-EGR_DILUTION_MISFIRE-gas_co-max | EGR_DILUTION_MISFIRE | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 912 | TH-BND-EGR_DILUTION_MISFIRE-gas_co-max+eps | EGR_DILUTION_MISFIRE | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 913 | TH-BND-EGR_DILUTION_MISFIRE-gas_co2-min-eps | EGR_DILUTION_MISFIRE | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 914 | TH-BND-EGR_DILUTION_MISFIRE-gas_co2-min | EGR_DILUTION_MISFIRE | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 915 | TH-BND-EGR_DILUTION_MISFIRE-gas_co2-min+eps | EGR_DILUTION_MISFIRE | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 916 | TH-BND-EGR_DILUTION_MISFIRE-gas_co2-max-eps | EGR_DILUTION_MISFIRE | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 917 | TH-BND-EGR_DILUTION_MISFIRE-gas_co2-max | EGR_DILUTION_MISFIRE | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 918 | TH-BND-EGR_DILUTION_MISFIRE-gas_co2-max+eps | EGR_DILUTION_MISFIRE | gas_co2 | max+eps | outside | SAMPLE_INVALID | PASS |
| 919 | TH-BND-EGR_DILUTION_MISFIRE-gas_o2-min-eps | EGR_DILUTION_MISFIRE | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 920 | TH-BND-EGR_DILUTION_MISFIRE-gas_o2-min | EGR_DILUTION_MISFIRE | gas_o2 | min | inside | NORMAL_OPERATION | FAIL |
| 921 | TH-BND-EGR_DILUTION_MISFIRE-gas_o2-min+eps | EGR_DILUTION_MISFIRE | gas_o2 | min+eps | inside | NORMAL_OPERATION | FAIL |
| 922 | TH-BND-EGR_DILUTION_MISFIRE-gas_o2-max-eps | EGR_DILUTION_MISFIRE | gas_o2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 923 | TH-BND-EGR_DILUTION_MISFIRE-gas_o2-max | EGR_DILUTION_MISFIRE | gas_o2 | max | inside | SAMPLE_INVALID | FAIL |
| 924 | TH-BND-EGR_DILUTION_MISFIRE-gas_o2-max+eps | EGR_DILUTION_MISFIRE | gas_o2 | max+eps | outside | ERROR:ValueError | PASS |
| 925 | TH-BND-EGR_DILUTION_MISFIRE-gas_nox-min-eps | EGR_DILUTION_MISFIRE | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 926 | TH-BND-EGR_DILUTION_MISFIRE-gas_nox-min | EGR_DILUTION_MISFIRE | gas_nox | min | inside | SAMPLE_INVALID | FAIL |
| 927 | TH-BND-EGR_DILUTION_MISFIRE-gas_nox-min+eps | EGR_DILUTION_MISFIRE | gas_nox | min+eps | inside | SAMPLE_INVALID | FAIL |
| 928 | TH-BND-EGR_DILUTION_MISFIRE-gas_nox-max-eps | EGR_DILUTION_MISFIRE | gas_nox | max-eps | inside | SAMPLE_INVALID | FAIL |
| 929 | TH-BND-EGR_DILUTION_MISFIRE-gas_nox-max | EGR_DILUTION_MISFIRE | gas_nox | max | inside | SAMPLE_INVALID | FAIL |
| 930 | TH-BND-EGR_DILUTION_MISFIRE-gas_nox-max+eps | EGR_DILUTION_MISFIRE | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 931 | TH-BND-INCOMPLETE_OXIDATION-gas_hc-min-eps | INCOMPLETE_OXIDATION | gas_hc | min-eps | outside | SAMPLE_INVALID | PASS |
| 932 | TH-BND-INCOMPLETE_OXIDATION-gas_hc-min | INCOMPLETE_OXIDATION | gas_hc | min | inside | SAMPLE_INVALID | FAIL |
| 933 | TH-BND-INCOMPLETE_OXIDATION-gas_hc-min+eps | INCOMPLETE_OXIDATION | gas_hc | min+eps | inside | SAMPLE_INVALID | FAIL |
| 934 | TH-BND-INCOMPLETE_OXIDATION-gas_hc-max-eps | INCOMPLETE_OXIDATION | gas_hc | max-eps | inside | SAMPLE_INVALID | FAIL |
| 935 | TH-BND-INCOMPLETE_OXIDATION-gas_hc-max | INCOMPLETE_OXIDATION | gas_hc | max | inside | SAMPLE_INVALID | FAIL |
| 936 | TH-BND-INCOMPLETE_OXIDATION-gas_hc-max+eps | INCOMPLETE_OXIDATION | gas_hc | max+eps | outside | ERROR:ValueError | PASS |
| 937 | TH-BND-INCOMPLETE_OXIDATION-gas_co-min-eps | INCOMPLETE_OXIDATION | gas_co | min-eps | outside | RICH_MISFIRE | PASS |
| 938 | TH-BND-INCOMPLETE_OXIDATION-gas_co-min | INCOMPLETE_OXIDATION | gas_co | min | inside | RICH_MISFIRE | FAIL |
| 939 | TH-BND-INCOMPLETE_OXIDATION-gas_co-min+eps | INCOMPLETE_OXIDATION | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 940 | TH-BND-INCOMPLETE_OXIDATION-gas_co-max-eps | INCOMPLETE_OXIDATION | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 941 | TH-BND-INCOMPLETE_OXIDATION-gas_co-max | INCOMPLETE_OXIDATION | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 942 | TH-BND-INCOMPLETE_OXIDATION-gas_co-max+eps | INCOMPLETE_OXIDATION | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 943 | TH-BND-INCOMPLETE_OXIDATION-gas_co2-min-eps | INCOMPLETE_OXIDATION | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 944 | TH-BND-INCOMPLETE_OXIDATION-gas_co2-min | INCOMPLETE_OXIDATION | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 945 | TH-BND-INCOMPLETE_OXIDATION-gas_co2-min+eps | INCOMPLETE_OXIDATION | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 946 | TH-BND-INCOMPLETE_OXIDATION-gas_co2-max-eps | INCOMPLETE_OXIDATION | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 947 | TH-BND-INCOMPLETE_OXIDATION-gas_co2-max | INCOMPLETE_OXIDATION | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 948 | TH-BND-INCOMPLETE_OXIDATION-gas_co2-max+eps | INCOMPLETE_OXIDATION | gas_co2 | max+eps | outside | SAMPLE_INVALID | PASS |
| 949 | TH-BND-INCOMPLETE_OXIDATION-gas_o2-min-eps | INCOMPLETE_OXIDATION | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 950 | TH-BND-INCOMPLETE_OXIDATION-gas_o2-min | INCOMPLETE_OXIDATION | gas_o2 | min | inside | NORMAL_OPERATION | FAIL |
| 951 | TH-BND-INCOMPLETE_OXIDATION-gas_o2-min+eps | INCOMPLETE_OXIDATION | gas_o2 | min+eps | inside | NORMAL_OPERATION | FAIL |
| 952 | TH-BND-INCOMPLETE_OXIDATION-gas_o2-max-eps | INCOMPLETE_OXIDATION | gas_o2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 953 | TH-BND-INCOMPLETE_OXIDATION-gas_o2-max | INCOMPLETE_OXIDATION | gas_o2 | max | inside | SAMPLE_INVALID | FAIL |
| 954 | TH-BND-INCOMPLETE_OXIDATION-gas_o2-max+eps | INCOMPLETE_OXIDATION | gas_o2 | max+eps | outside | ERROR:ValueError | PASS |
| 955 | TH-BND-INCOMPLETE_OXIDATION-gas_nox-min-eps | INCOMPLETE_OXIDATION | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 956 | TH-BND-INCOMPLETE_OXIDATION-gas_nox-min | INCOMPLETE_OXIDATION | gas_nox | min | inside | SAMPLE_INVALID | FAIL |
| 957 | TH-BND-INCOMPLETE_OXIDATION-gas_nox-min+eps | INCOMPLETE_OXIDATION | gas_nox | min+eps | inside | SAMPLE_INVALID | FAIL |
| 958 | TH-BND-INCOMPLETE_OXIDATION-gas_nox-max-eps | INCOMPLETE_OXIDATION | gas_nox | max-eps | inside | SAMPLE_INVALID | FAIL |
| 959 | TH-BND-INCOMPLETE_OXIDATION-gas_nox-max | INCOMPLETE_OXIDATION | gas_nox | max | inside | SAMPLE_INVALID | FAIL |
| 960 | TH-BND-INCOMPLETE_OXIDATION-gas_nox-max+eps | INCOMPLETE_OXIDATION | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 961 | TH-BND-INCOMPLETE_COMBUSTION-gas_hc-min-eps | INCOMPLETE_COMBUSTION | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 962 | TH-BND-INCOMPLETE_COMBUSTION-gas_hc-min | INCOMPLETE_COMBUSTION | gas_hc | min | inside | SAMPLE_INVALID | FAIL |
| 963 | TH-BND-INCOMPLETE_COMBUSTION-gas_hc-min+eps | INCOMPLETE_COMBUSTION | gas_hc | min+eps | inside | SAMPLE_INVALID | FAIL |
| 964 | TH-BND-INCOMPLETE_COMBUSTION-gas_hc-max-eps | INCOMPLETE_COMBUSTION | gas_hc | max-eps | inside | SAMPLE_INVALID | FAIL |
| 965 | TH-BND-INCOMPLETE_COMBUSTION-gas_hc-max | INCOMPLETE_COMBUSTION | gas_hc | max | inside | SAMPLE_INVALID | FAIL |
| 966 | TH-BND-INCOMPLETE_COMBUSTION-gas_hc-max+eps | INCOMPLETE_COMBUSTION | gas_hc | max+eps | outside | ERROR:ValueError | PASS |
| 967 | TH-BND-INCOMPLETE_COMBUSTION-gas_co-min-eps | INCOMPLETE_COMBUSTION | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 968 | TH-BND-INCOMPLETE_COMBUSTION-gas_co-min | INCOMPLETE_COMBUSTION | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 969 | TH-BND-INCOMPLETE_COMBUSTION-gas_co-min+eps | INCOMPLETE_COMBUSTION | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 970 | TH-BND-INCOMPLETE_COMBUSTION-gas_co-max-eps | INCOMPLETE_COMBUSTION | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 971 | TH-BND-INCOMPLETE_COMBUSTION-gas_co-max | INCOMPLETE_COMBUSTION | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 972 | TH-BND-INCOMPLETE_COMBUSTION-gas_co-max+eps | INCOMPLETE_COMBUSTION | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 973 | TH-BND-INCOMPLETE_COMBUSTION-gas_co2-min-eps | INCOMPLETE_COMBUSTION | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 974 | TH-BND-INCOMPLETE_COMBUSTION-gas_co2-min | INCOMPLETE_COMBUSTION | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 975 | TH-BND-INCOMPLETE_COMBUSTION-gas_co2-min+eps | INCOMPLETE_COMBUSTION | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 976 | TH-BND-INCOMPLETE_COMBUSTION-gas_co2-max-eps | INCOMPLETE_COMBUSTION | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 977 | TH-BND-INCOMPLETE_COMBUSTION-gas_co2-max | INCOMPLETE_COMBUSTION | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 978 | TH-BND-INCOMPLETE_COMBUSTION-gas_co2-max+eps | INCOMPLETE_COMBUSTION | gas_co2 | max+eps | outside | ERROR:ValueError | PASS |
| 979 | TH-BND-INCOMPLETE_COMBUSTION-gas_o2-min-eps | INCOMPLETE_COMBUSTION | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 980 | TH-BND-INCOMPLETE_COMBUSTION-gas_o2-min | INCOMPLETE_COMBUSTION | gas_o2 | min | inside | SAMPLE_INVALID | FAIL |
| 981 | TH-BND-INCOMPLETE_COMBUSTION-gas_o2-min+eps | INCOMPLETE_COMBUSTION | gas_o2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 982 | TH-BND-INCOMPLETE_COMBUSTION-gas_o2-max-eps | INCOMPLETE_COMBUSTION | gas_o2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 983 | TH-BND-INCOMPLETE_COMBUSTION-gas_o2-max | INCOMPLETE_COMBUSTION | gas_o2 | max | inside | SAMPLE_INVALID | FAIL |
| 984 | TH-BND-INCOMPLETE_COMBUSTION-gas_o2-max+eps | INCOMPLETE_COMBUSTION | gas_o2 | max+eps | outside | ERROR:ValueError | PASS |
| 985 | TH-BND-INCOMPLETE_COMBUSTION-gas_nox-min-eps | INCOMPLETE_COMBUSTION | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 986 | TH-BND-INCOMPLETE_COMBUSTION-gas_nox-min | INCOMPLETE_COMBUSTION | gas_nox | min | inside | SAMPLE_INVALID | FAIL |
| 987 | TH-BND-INCOMPLETE_COMBUSTION-gas_nox-min+eps | INCOMPLETE_COMBUSTION | gas_nox | min+eps | inside | SAMPLE_INVALID | FAIL |
| 988 | TH-BND-INCOMPLETE_COMBUSTION-gas_nox-max-eps | INCOMPLETE_COMBUSTION | gas_nox | max-eps | inside | SAMPLE_INVALID | FAIL |
| 989 | TH-BND-INCOMPLETE_COMBUSTION-gas_nox-max | INCOMPLETE_COMBUSTION | gas_nox | max | inside | SAMPLE_INVALID | FAIL |
| 990 | TH-BND-INCOMPLETE_COMBUSTION-gas_nox-max+eps | INCOMPLETE_COMBUSTION | gas_nox | max+eps | outside | ERROR:ValueError | PASS |
| 991 | TH-BND-COOLANT_LEAK_INTERNAL-gas_hc-min-eps | COOLANT_LEAK_INTERNAL | gas_hc | min-eps | outside | ERROR:ValueError | PASS |
| 992 | TH-BND-COOLANT_LEAK_INTERNAL-gas_hc-min | COOLANT_LEAK_INTERNAL | gas_hc | min | inside | SAMPLE_INVALID | FAIL |
| 993 | TH-BND-COOLANT_LEAK_INTERNAL-gas_hc-min+eps | COOLANT_LEAK_INTERNAL | gas_hc | min+eps | inside | SAMPLE_INVALID | FAIL |
| 994 | TH-BND-COOLANT_LEAK_INTERNAL-gas_hc-max-eps | COOLANT_LEAK_INTERNAL | gas_hc | max-eps | inside | SAMPLE_INVALID | FAIL |
| 995 | TH-BND-COOLANT_LEAK_INTERNAL-gas_hc-max | COOLANT_LEAK_INTERNAL | gas_hc | max | inside | SAMPLE_INVALID | FAIL |
| 996 | TH-BND-COOLANT_LEAK_INTERNAL-gas_hc-max+eps | COOLANT_LEAK_INTERNAL | gas_hc | max+eps | outside | ERROR:ValueError | PASS |
| 997 | TH-BND-COOLANT_LEAK_INTERNAL-gas_co-min-eps | COOLANT_LEAK_INTERNAL | gas_co | min-eps | outside | ERROR:ValueError | PASS |
| 998 | TH-BND-COOLANT_LEAK_INTERNAL-gas_co-min | COOLANT_LEAK_INTERNAL | gas_co | min | inside | SAMPLE_INVALID | FAIL |
| 999 | TH-BND-COOLANT_LEAK_INTERNAL-gas_co-min+eps | COOLANT_LEAK_INTERNAL | gas_co | min+eps | inside | SAMPLE_INVALID | FAIL |
| 1000 | TH-BND-COOLANT_LEAK_INTERNAL-gas_co-max-eps | COOLANT_LEAK_INTERNAL | gas_co | max-eps | inside | SAMPLE_INVALID | FAIL |
| 1001 | TH-BND-COOLANT_LEAK_INTERNAL-gas_co-max | COOLANT_LEAK_INTERNAL | gas_co | max | inside | SAMPLE_INVALID | FAIL |
| 1002 | TH-BND-COOLANT_LEAK_INTERNAL-gas_co-max+eps | COOLANT_LEAK_INTERNAL | gas_co | max+eps | outside | ERROR:ValueError | PASS |
| 1003 | TH-BND-COOLANT_LEAK_INTERNAL-gas_co2-min-eps | COOLANT_LEAK_INTERNAL | gas_co2 | min-eps | outside | ERROR:ValueError | PASS |
| 1004 | TH-BND-COOLANT_LEAK_INTERNAL-gas_co2-min | COOLANT_LEAK_INTERNAL | gas_co2 | min | inside | SAMPLE_INVALID | FAIL |
| 1005 | TH-BND-COOLANT_LEAK_INTERNAL-gas_co2-min+eps | COOLANT_LEAK_INTERNAL | gas_co2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 1006 | TH-BND-COOLANT_LEAK_INTERNAL-gas_co2-max-eps | COOLANT_LEAK_INTERNAL | gas_co2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 1007 | TH-BND-COOLANT_LEAK_INTERNAL-gas_co2-max | COOLANT_LEAK_INTERNAL | gas_co2 | max | inside | SAMPLE_INVALID | FAIL |
| 1008 | TH-BND-COOLANT_LEAK_INTERNAL-gas_co2-max+eps | COOLANT_LEAK_INTERNAL | gas_co2 | max+eps | outside | ERROR:ValueError | PASS |
| 1009 | TH-BND-COOLANT_LEAK_INTERNAL-gas_o2-min-eps | COOLANT_LEAK_INTERNAL | gas_o2 | min-eps | outside | ERROR:ValueError | PASS |
| 1010 | TH-BND-COOLANT_LEAK_INTERNAL-gas_o2-min | COOLANT_LEAK_INTERNAL | gas_o2 | min | inside | SAMPLE_INVALID | FAIL |
| 1011 | TH-BND-COOLANT_LEAK_INTERNAL-gas_o2-min+eps | COOLANT_LEAK_INTERNAL | gas_o2 | min+eps | inside | SAMPLE_INVALID | FAIL |
| 1012 | TH-BND-COOLANT_LEAK_INTERNAL-gas_o2-max-eps | COOLANT_LEAK_INTERNAL | gas_o2 | max-eps | inside | SAMPLE_INVALID | FAIL |
| 1013 | TH-BND-COOLANT_LEAK_INTERNAL-gas_o2-max | COOLANT_LEAK_INTERNAL | gas_o2 | max | inside | SAMPLE_INVALID | FAIL |
| 1014 | TH-BND-COOLANT_LEAK_INTERNAL-gas_o2-max+eps | COOLANT_LEAK_INTERNAL | gas_o2 | max+eps | outside | ERROR:ValueError | PASS |
| 1015 | TH-BND-COOLANT_LEAK_INTERNAL-gas_nox-min-eps | COOLANT_LEAK_INTERNAL | gas_nox | min-eps | outside | ERROR:ValueError | PASS |
| 1016 | TH-BND-COOLANT_LEAK_INTERNAL-gas_nox-min | COOLANT_LEAK_INTERNAL | gas_nox | min | inside | SAMPLE_INVALID | FAIL |
| 1017 | TH-BND-COOLANT_LEAK_INTERNAL-gas_nox-min+eps | COOLANT_LEAK_INTERNAL | gas_nox | min+eps | inside | SAMPLE_INVALID | FAIL |
| 1018 | TH-BND-COOLANT_LEAK_INTERNAL-gas_nox-max-eps | COOLANT_LEAK_INTERNAL | gas_nox | max-eps | inside | SAMPLE_INVALID | FAIL |
| 1019 | TH-BND-COOLANT_LEAK_INTERNAL-gas_nox-max | COOLANT_LEAK_INTERNAL | gas_nox | max | inside | SAMPLE_INVALID | FAIL |
| 1020 | TH-BND-COOLANT_LEAK_INTERNAL-gas_nox-max+eps | COOLANT_LEAK_INTERNAL | gas_nox | max+eps | outside | ERROR:ValueError | PASS |

## Failures

- **TH-BND-NORMAL_OPERATION-gas_hc-min:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-NORMAL_OPERATION-gas_hc-min+eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-NORMAL_OPERATION-gas_hc-max-eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-NORMAL_OPERATION-gas_hc-max:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-NORMAL_OPERATION-gas_co-min:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-NORMAL_OPERATION-gas_co-min+eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-NORMAL_OPERATION-gas_co-max-eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-NORMAL_OPERATION-gas_co-max:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-NORMAL_OPERATION-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-NORMAL_OPERATION-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-NORMAL_OPERATION-gas_co2-max-eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-NORMAL_OPERATION-gas_co2-max:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-NORMAL_OPERATION-gas_co2-max+eps:** oracle=outside, actual=NORMAL_OPERATION
- **TH-BND-NORMAL_OPERATION-gas_o2-min:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-NORMAL_OPERATION-gas_o2-min+eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-NORMAL_OPERATION-gas_o2-max-eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-NORMAL_OPERATION-gas_o2-max:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-NORMAL_OPERATION-gas_nox-min:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-NORMAL_OPERATION-gas_nox-min+eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-NORMAL_OPERATION-gas_nox-max-eps:** oracle=inside, actual=WORN_PISTON_RINGS
- **TH-BND-NORMAL_OPERATION-gas_nox-max:** oracle=inside, actual=WORN_PISTON_RINGS
- **TH-BND-RICH_MIXTURE-gas_hc-min:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-RICH_MIXTURE-gas_hc-min+eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-RICH_MIXTURE-gas_hc-max-eps:** oracle=inside, actual=INCOMPLETE_OXIDATION
- **TH-BND-RICH_MIXTURE-gas_hc-max:** oracle=inside, actual=POA_SIGNATURE
- **TH-BND-RICH_MIXTURE-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MIXTURE-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MIXTURE-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MIXTURE-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MIXTURE-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MIXTURE-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MIXTURE-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MIXTURE-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MIXTURE-gas_o2-min:** oracle=inside, actual=INCOMPLETE_OXIDATION
- **TH-BND-RICH_MIXTURE-gas_o2-min+eps:** oracle=inside, actual=INCOMPLETE_OXIDATION
- **TH-BND-RICH_MIXTURE-gas_o2-max-eps:** oracle=inside, actual=INCOMPLETE_OXIDATION
- **TH-BND-RICH_MIXTURE-gas_o2-max:** oracle=inside, actual=INCOMPLETE_OXIDATION
- **TH-BND-RICH_MIXTURE-gas_nox-max-eps:** oracle=inside, actual=INCOMPLETE_OXIDATION
- **TH-BND-RICH_MIXTURE-gas_nox-max:** oracle=inside, actual=CATALYST_OVERWHELMED
- **TH-BND-LEAN_MIXTURE-gas_hc-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_hc-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_hc-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_hc-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_o2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_o2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_o2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_o2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_nox-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_nox-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_nox-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MIXTURE-gas_nox-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_hc-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_hc-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_hc-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_hc-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_o2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_o2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_o2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_o2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_nox-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_nox-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_nox-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-IGNITION_MISFIRE-gas_nox-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_hc-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_hc-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_hc-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_hc-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_o2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_o2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_o2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_o2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_nox-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_nox-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_nox-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-LEAN_MISFIRE-gas_nox-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_hc-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_hc-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_hc-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_hc-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_o2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_o2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_o2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_o2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_nox-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_nox-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_nox-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-RICH_MISFIRE-gas_nox-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_hc-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_hc-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_hc-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_hc-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_o2-min:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-EXHAUST_AIR_LEAK-gas_o2-min+eps:** oracle=inside, actual=RICH_MISFIRE
- **TH-BND-EXHAUST_AIR_LEAK-gas_o2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_o2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_nox-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_nox-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_nox-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EXHAUST_AIR_LEAK-gas_nox-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-HIGH_COMBUSTION_TEMP-gas_co-min:** oracle=inside, actual=TIMING_OVER_ADVANCED
- **TH-BND-HIGH_COMBUSTION_TEMP-gas_co-min+eps:** oracle=inside, actual=TIMING_OVER_ADVANCED
- **TH-BND-HIGH_COMBUSTION_TEMP-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-HIGH_COMBUSTION_TEMP-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_hc-min:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_hc-min+eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_hc-max-eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_hc-max:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_co-min:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_co-min+eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_co-max-eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_co-max:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_co2-min:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_co2-min+eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_co2-max-eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_co2-max:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_o2-min:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_o2-min+eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_o2-max-eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_o2-max:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_nox-min:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_nox-min+eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_nox-max-eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_NOT_LIGHTING_-gas_nox-max:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-CATALYST_OVERWHELMED-gas_hc-max-eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-CATALYST_OVERWHELMED-gas_hc-max:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-CATALYST_OVERWHELMED-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CATALYST_OVERWHELMED-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CATALYST_OVERWHELMED-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CATALYST_OVERWHELMED-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CATALYST_OVERWHELMED-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CATALYST_OVERWHELMED-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CATALYST_OVERWHELMED-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CATALYST_OVERWHELMED-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CATALYST_OVERWHELMED-gas_o2-min:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-CATALYST_OVERWHELMED-gas_o2-min+eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-CATALYST_OVERWHELMED-gas_o2-max-eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-CATALYST_OVERWHELMED-gas_o2-max:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-CATALYST_OVERWHELMED-gas_nox-min:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-CATALYST_OVERWHELMED-gas_nox-min+eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-CATALYST_OVERWHELMED-gas_nox-max-eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-CATALYST_OVERWHELMED-gas_nox-max:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-TIMING_OVER_ADVANCED-gas_hc-min:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-TIMING_OVER_ADVANCED-gas_hc-min+eps:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-TIMING_OVER_ADVANCED-gas_hc-max-eps:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-TIMING_OVER_ADVANCED-gas_hc-max:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-TIMING_OVER_ADVANCED-gas_co-max-eps:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-TIMING_OVER_ADVANCED-gas_co-max:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-TIMING_OVER_ADVANCED-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-TIMING_OVER_ADVANCED-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-TIMING_OVER_ADVANCED-gas_co2-max-eps:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-TIMING_OVER_ADVANCED-gas_co2-max:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-TIMING_OVER_ADVANCED-gas_o2-min:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-TIMING_OVER_ADVANCED-gas_o2-min+eps:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-TIMING_OVER_ADVANCED-gas_o2-max-eps:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-TIMING_OVER_ADVANCED-gas_o2-max:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-TIMING_OVER_ADVANCED-gas_nox-min:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-TIMING_OVER_ADVANCED-gas_nox-min+eps:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-TIMING_OVER_ADVANCED-gas_nox-max-eps:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-TIMING_OVER_ADVANCED-gas_nox-max:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-TIMING_RETARDED-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-TIMING_RETARDED-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_hc-min:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_hc-min+eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_hc-max-eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_hc-max:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_co-min:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_co-min+eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_co-max-eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_co-max:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_co2-min:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_co2-min+eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_co2-max-eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_co2-max:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_o2-min:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_o2-min+eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_o2-max-eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_o2-max:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_nox-max-eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-O2_SENSOR_BIASED_LOW-gas_nox-max:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-WORN_ENGINE-gas_hc-min:** oracle=inside, actual=O2_SENSOR_BIASED_LOW
- **TH-BND-WORN_ENGINE-gas_hc-min+eps:** oracle=inside, actual=O2_SENSOR_BIASED_LOW
- **TH-BND-WORN_ENGINE-gas_hc-max-eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-WORN_ENGINE-gas_hc-max:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-WORN_ENGINE-gas_co-min:** oracle=inside, actual=WORN_VALVE_SEALS
- **TH-BND-WORN_ENGINE-gas_co-min+eps:** oracle=inside, actual=WORN_VALVE_SEALS
- **TH-BND-WORN_ENGINE-gas_co-max-eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-WORN_ENGINE-gas_co-max:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-WORN_ENGINE-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_ENGINE-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_ENGINE-gas_co2-max-eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-WORN_ENGINE-gas_co2-max:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-WORN_ENGINE-gas_o2-min:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-WORN_ENGINE-gas_o2-min+eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-WORN_ENGINE-gas_nox-min:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-WORN_ENGINE-gas_nox-min+eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-WORN_ENGINE-gas_nox-max-eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-WORN_ENGINE-gas_nox-max:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-FLAT_CAMSHAFT-gas_hc-min:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-FLAT_CAMSHAFT-gas_hc-min+eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-FLAT_CAMSHAFT-gas_hc-max-eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-FLAT_CAMSHAFT-gas_hc-max:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-FLAT_CAMSHAFT-gas_co-min:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-FLAT_CAMSHAFT-gas_co-min+eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-FLAT_CAMSHAFT-gas_co-max-eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-FLAT_CAMSHAFT-gas_co-max:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-FLAT_CAMSHAFT-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-FLAT_CAMSHAFT-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-FLAT_CAMSHAFT-gas_co2-max-eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-FLAT_CAMSHAFT-gas_co2-max:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-FLAT_CAMSHAFT-gas_o2-min:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-FLAT_CAMSHAFT-gas_o2-min+eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-FLAT_CAMSHAFT-gas_o2-max-eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-FLAT_CAMSHAFT-gas_o2-max:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-FLAT_CAMSHAFT-gas_nox-min:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-FLAT_CAMSHAFT-gas_nox-min+eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-FLAT_CAMSHAFT-gas_nox-max-eps:** oracle=inside, actual=WORN_PISTON_RINGS
- **TH-BND-FLAT_CAMSHAFT-gas_nox-max:** oracle=inside, actual=WORN_PISTON_RINGS
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_hc-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_hc-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_hc-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_hc-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_o2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_o2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_o2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_o2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_nox-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_nox-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_nox-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_INTAKE_VALVE_CARBO-gas_nox-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_hc-min:** oracle=inside, actual=CATALYST_OVERWHELMED
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_hc-min+eps:** oracle=inside, actual=CATALYST_OVERWHELMED
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_hc-max-eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_hc-max:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_o2-min:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_o2-min+eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_o2-max-eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_o2-max:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_nox-min:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_nox-min+eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_nox-max-eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-VACUUM_REGULATOR_DIAPH-gas_nox-max:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_hc-min:** oracle=inside, actual=CATALYST_OVERWHELMED
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_hc-min+eps:** oracle=inside, actual=CATALYST_OVERWHELMED
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_hc-max-eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_hc-max:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_o2-min:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_o2-min+eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_o2-max-eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_o2-max:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_nox-min:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_nox-min+eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_nox-max-eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-GDI_HPFP_INTERNAL_SEAL-gas_nox-max:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-WORN_VALVE_SEALS-gas_hc-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_VALVE_SEALS-gas_hc-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_VALVE_SEALS-gas_hc-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_VALVE_SEALS-gas_hc-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_VALVE_SEALS-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_VALVE_SEALS-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_VALVE_SEALS-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_VALVE_SEALS-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_VALVE_SEALS-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_VALVE_SEALS-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_VALVE_SEALS-gas_co2-max-eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-WORN_VALVE_SEALS-gas_co2-max:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-WORN_VALVE_SEALS-gas_o2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_VALVE_SEALS-gas_o2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_VALVE_SEALS-gas_o2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_VALVE_SEALS-gas_o2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_VALVE_SEALS-gas_nox-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_VALVE_SEALS-gas_nox-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_VALVE_SEALS-gas_nox-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_VALVE_SEALS-gas_nox-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-WORN_PISTON_RINGS-gas_hc-min:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-WORN_PISTON_RINGS-gas_hc-min+eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-WORN_PISTON_RINGS-gas_hc-max-eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-WORN_PISTON_RINGS-gas_hc-max:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-WORN_PISTON_RINGS-gas_co-min:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-WORN_PISTON_RINGS-gas_co-min+eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-WORN_PISTON_RINGS-gas_co-max-eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-WORN_PISTON_RINGS-gas_co-max:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-WORN_PISTON_RINGS-gas_co2-min:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-WORN_PISTON_RINGS-gas_co2-min+eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-WORN_PISTON_RINGS-gas_co2-max-eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-WORN_PISTON_RINGS-gas_co2-max:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-WORN_PISTON_RINGS-gas_o2-min:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-WORN_PISTON_RINGS-gas_o2-min+eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-WORN_PISTON_RINGS-gas_o2-max-eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-WORN_PISTON_RINGS-gas_o2-max:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-WORN_PISTON_RINGS-gas_nox-min:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-WORN_PISTON_RINGS-gas_nox-min+eps:** oracle=inside, actual=TIMING_RETARDED
- **TH-BND-POA_SIGNATURE-gas_hc-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-POA_SIGNATURE-gas_hc-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-POA_SIGNATURE-gas_hc-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-POA_SIGNATURE-gas_hc-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-POA_SIGNATURE-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-POA_SIGNATURE-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-POA_SIGNATURE-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-POA_SIGNATURE-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-POA_SIGNATURE-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-POA_SIGNATURE-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-POA_SIGNATURE-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-POA_SIGNATURE-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-POA_SIGNATURE-gas_o2-min:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-POA_SIGNATURE-gas_o2-min+eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-POA_SIGNATURE-gas_o2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-POA_SIGNATURE-gas_o2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-POA_SIGNATURE-gas_nox-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-POA_SIGNATURE-gas_nox-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-POA_SIGNATURE-gas_nox-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-POA_SIGNATURE-gas_nox-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_hc-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_o2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_RETARDED_MA-gas_nox-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_hc-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_hc-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_hc-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_hc-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_o2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_o2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_o2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_o2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_nox-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_nox-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_nox-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-CAM_TIMING_ADVANCED-gas_nox-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_STUCK_CLOSED-gas_hc-min:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-EGR_STUCK_CLOSED-gas_hc-min+eps:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-EGR_STUCK_CLOSED-gas_hc-max-eps:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-EGR_STUCK_CLOSED-gas_hc-max:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-EGR_STUCK_CLOSED-gas_co-min:** oracle=inside, actual=TIMING_OVER_ADVANCED
- **TH-BND-EGR_STUCK_CLOSED-gas_co-min+eps:** oracle=inside, actual=TIMING_OVER_ADVANCED
- **TH-BND-EGR_STUCK_CLOSED-gas_co-max-eps:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-EGR_STUCK_CLOSED-gas_co-max:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-EGR_STUCK_CLOSED-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_STUCK_CLOSED-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_STUCK_CLOSED-gas_co2-max-eps:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-EGR_STUCK_CLOSED-gas_co2-max:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-EGR_STUCK_CLOSED-gas_o2-min:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-EGR_STUCK_CLOSED-gas_o2-min+eps:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-EGR_STUCK_CLOSED-gas_o2-max-eps:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-EGR_STUCK_CLOSED-gas_o2-max:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-EGR_STUCK_CLOSED-gas_nox-min:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-EGR_STUCK_CLOSED-gas_nox-min+eps:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-EGR_STUCK_CLOSED-gas_nox-max-eps:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-EGR_STUCK_CLOSED-gas_nox-max:** oracle=inside, actual=HIGH_COMBUSTION_TEMP
- **TH-BND-EGR_STUCK_OPEN-gas_hc-min:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-EGR_STUCK_OPEN-gas_hc-min+eps:** oracle=inside, actual=VVT_FAILURE
- **TH-BND-EGR_STUCK_OPEN-gas_hc-max-eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-EGR_STUCK_OPEN-gas_hc-max:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-EGR_STUCK_OPEN-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_STUCK_OPEN-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_STUCK_OPEN-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_STUCK_OPEN-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_STUCK_OPEN-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_STUCK_OPEN-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_STUCK_OPEN-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_STUCK_OPEN-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_STUCK_OPEN-gas_o2-min:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-EGR_STUCK_OPEN-gas_o2-min+eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-EGR_STUCK_OPEN-gas_o2-max-eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-EGR_STUCK_OPEN-gas_o2-max:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-EGR_STUCK_OPEN-gas_nox-min:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-EGR_STUCK_OPEN-gas_nox-min+eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-EGR_STUCK_OPEN-gas_nox-max-eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-EGR_STUCK_OPEN-gas_nox-max:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-VVT_FAILURE-gas_hc-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_hc-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_hc-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_hc-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_o2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_o2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_o2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_o2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_nox-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_nox-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_nox-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-VVT_FAILURE-gas_nox-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_hc-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_hc-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_hc-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_hc-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_o2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_o2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_o2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_o2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_nox-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_nox-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_nox-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EVAP_CANISTER_SATURATE-gas_nox-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_hc-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_hc-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_hc-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_hc-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_o2-min:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-EGR_DILUTION_MISFIRE-gas_o2-min+eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-EGR_DILUTION_MISFIRE-gas_o2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_o2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_nox-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_nox-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_nox-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-EGR_DILUTION_MISFIRE-gas_nox-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_OXIDATION-gas_hc-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_OXIDATION-gas_hc-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_OXIDATION-gas_hc-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_OXIDATION-gas_hc-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_OXIDATION-gas_co-min:** oracle=inside, actual=RICH_MISFIRE
- **TH-BND-INCOMPLETE_OXIDATION-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_OXIDATION-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_OXIDATION-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_OXIDATION-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_OXIDATION-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_OXIDATION-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_OXIDATION-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_OXIDATION-gas_o2-min:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-INCOMPLETE_OXIDATION-gas_o2-min+eps:** oracle=inside, actual=NORMAL_OPERATION
- **TH-BND-INCOMPLETE_OXIDATION-gas_o2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_OXIDATION-gas_o2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_OXIDATION-gas_nox-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_OXIDATION-gas_nox-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_OXIDATION-gas_nox-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_OXIDATION-gas_nox-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_hc-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_hc-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_hc-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_hc-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_o2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_o2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_o2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_o2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_nox-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_nox-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_nox-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-INCOMPLETE_COMBUSTION-gas_nox-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_hc-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_hc-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_hc-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_hc-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_co-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_co-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_co-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_co-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_co2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_co2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_co2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_co2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_o2-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_o2-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_o2-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_o2-max:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_nox-min:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_nox-min+eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_nox-max-eps:** oracle=inside, actual=SAMPLE_INVALID
- **TH-BND-COOLANT_LEAK_INTERNAL-gas_nox-max:** oracle=inside, actual=SAMPLE_INVALID

