# REVIEW T-GASA-4 — ACCEPT, score 96 (Windows Cowork, 2026-11-13)

Inline difficulty-1 row (roster 2026-11-13). `fix/T-GASA-4` on `fix/T-GASA-3` `11d1648`: commits `b22b38d` (fix) and
`f806d5e` (review corrections). F-C2-6 (HIGH). Ruling: GASWIKI-04 §4.10's lean-branch gate "HC > 1000" is inherited
from the retired WRONG_VALVE_TIMING rule (the §4.10 code note) and excludes both GASWIKI-06B lean cam vectors. The
HC > 1000 idle-only path is unchanged. Below it, the rule opens at each branch's 06B idle floor (ADVANCED 250,
RETARDED_MAF 300; ontology `hc_atlas_floor`, `hc_atlas_floor_maf`) only when a 2500 RPM reading is present and
matches the branch's 2500 vector. An idle-only lean reading at HC 250-1000 is not pre-empted. The outer O2 > 2.0 gate
is unchanged (ADVANCED idle O2 1.2-2.0 stays unreachable on this path; recorded, not in this finding).

Facts: probe f3 passes (f5b red: T-GASA-3 residual). gaslab `238 passed, 2 skipped, 4 deselected` (base 230 + 8);
comlab `570`, wired `186`, ui `75` (= handoff-2115 baselines); v7 corpus per-case `0 of 314` changed. Mutations:
confirmation dropped → 2 failed; ADVANCED floor 251 → 1 failed; gate back to HC > 1000 only → 3 failed; MAF floor
dropped → 1 failed. ruff clean.

## Second review
APPROVE WITH CORRECTIONS (ds-flash, `C:/4DApp/recheck/codex/T-GASA-4_review.md`).
- M1 (MAF fires at HC 250-299, below its 06B floor 300) — upheld, re-derived: idle R(299, 0.48, 10.98, 2.64, 10) with
  the MAF 2500 vector returned CAM_TIMING_RETARDED_MAF. Fixed with a MAF floor; pinned 299/300.
- L1 (ontology description stale) — upheld, updated. L2 (no non-confirming 2500 pin at low HC) — upheld, pinned
  (NOx 100). L3 (comment overclaims "every 06B vector") — upheld, reworded. L4 (five blank lines) — upheld, fixed.
- L5 (comlab/wired/ui only absolute counts) — not upheld: they equal the measured handoff-2115 baselines.

## Score
96: the MAF floor was missed until the review.
