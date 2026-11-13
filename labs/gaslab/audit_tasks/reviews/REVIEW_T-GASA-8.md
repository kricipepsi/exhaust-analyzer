# REVIEW T-GASA-8 — ACCEPT, score 98 (Windows Cowork, 2026-11-13)

Inline difficulty-1 row (roster 2026-11-13). `fix/T-GASA-8` on `fix/T-GASA-7` `bd746c7`: commits `4488d91` (fix) and
`a105ba7` (review fold-ins). F-C2-10 (MEDIUM). Ruling: wideband only, the O2_SENSOR_BIASED_LOW CO2 window follows from
the GASWIKI-04 §4.1 VALID triangle sum (ontology `validity_gates.exhaust_gas_triangle` 14-16) and the calibrated CO
(5-8) and ontology O2 (0-0.3) windows: CO2 5.7-11.0. Narrowband is unchanged. The pin
`test_o2_bias_calibrated_by_sensor_type` reading 2 (CO 6.5 + CO2 14.5, sum 21.1, triangle-INVALID) encoded the defect
and is restated to CO2 8.5 (sum 15.1).

Facts: probe f10 passes. gaslab `253 passed, 2 skipped, 4 deselected` (base 251 + 2); comlab `570`, wired `186`, ui
`75` (= baselines); v7 corpus per-case `0 of 314` changed (before and after the fold-ins). Mutations: CO2 window
removed → 3 failed; O2 term dropped from the min → 1 failed. ruff clean.

## Second review
APPROVE (ds-flash, `C:/4DApp/recheck/codex/T-GASA-8_review.md`), four Lows.
- L1 (the box still admits triangle-invalid corners) — recorded residual: a box cannot encode a sum; the triangle gate
  rejects such samples before matching.
- L2 (O2 min missing from the CO2 max) — upheld, folded in (`a105ba7`; no behaviour change at O2 min 0).
- L3 (duplicated 14/16) — upheld, folded in: the caller passes the ontology triangle gate.
- L4 (no non-mutation check) — upheld, folded in.

## Score
98: the Lows.
