# REVIEW T-GASA-6 — ACCEPT, score 100 (Windows Cowork, 2026-11-13)

Inline difficulty-1 row (roster 2026-11-13). `fix/T-GASA-6` on `fix/T-GASA-5` `7d8ab6b`: commit `956fed6`. F-C2-8
(MEDIUM). Ruling: both CoC overrides in `_coc_adjust_normal_bounds` (`target_lambda_v112`, `co_low_idle`) apply only
when `dna.confidence == "HIGH"` (GAS_VOCABULARY §11, GASWIKI-02 §2.8), the gate that `resolution._rich_co_ceiling`
already uses. The probe's no-CoC verdict (TIMING_RETARDED) is F-C2-4 and stays out of scope.

Facts: probe f7 (F-C2-8) passes. gaslab `246 passed, 2 skipped, 4 deselected` (base 242 + 4); comlab `570`, wired
`186`, ui `75` (= baselines); v7 corpus per-case `0 of 314` changed. Mutations: λ gate removed → 2 failed; CO gate
removed → 3 failed. ruff clean.

## Second review
APPROVE, no findings (ds-flash, `C:/4DApp/recheck/codex/T-GASA-6_review.md`).

## Score
100.
