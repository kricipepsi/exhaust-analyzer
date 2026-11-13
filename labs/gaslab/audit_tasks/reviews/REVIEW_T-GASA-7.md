# REVIEW T-GASA-7 — ACCEPT, score 98 (Windows Cowork, 2026-11-13)

Inline difficulty-1 row (roster 2026-11-13). `fix/T-GASA-7` on `fix/T-GASA-6` `303c4e7`: commits `0b77fa7` (fix) and
`f264888` (review pin). F-C2-9 (MEDIUM). Ruling: the collision `tier_max` is the active DNA-scaled tier (GAS_VOCABULARY
§10.2). The vocab names two points: Euro 4 + cat 0.45 (`normal_with_cat.max`) and Euro 1 no-cat 1.5 (`mild_rich.max`).
The tier is chosen by `has_catalyst` only, which covers both points and adds no number (ontology
`co_tier_max_no_cat: 1.5`). The vocab §10.2 "not DNA-scaled (T-AUD-16)" note is replaced. Not changed: the
GASWIKI-02 §2.8 Euro 4 CO ceiling 0.2 against vocab 0.45 (a wiki inconsistency the finding notes).

Facts: probe f9 passes. gaslab `251 passed, 2 skipped, 4 deselected` (base 246 + 5); comlab `570`, wired `186`, ui
`75` (= baselines); v7 corpus per-case `0 of 314` changed. Mutations: tier always 0.45 → 2 failed; no-cat tier 1.49
→ 1 failed. ruff clean.

## Second review
APPROVE WITH CORRECTIONS (ds-flash, `C:/4DApp/recheck/codex/T-GASA-7_review.md`).
- L1 (the with-cat pin used Euro 1, not the cited Euro 4) — upheld: Euro 4 + cat case added (`f264888`).
- L2 (probe not traceable) — not upheld: "probe f9" is `audit/scratch/C2/test_c2_probes.py::test_f9_collision_tier_max_scales_with_dna`, run and passing.
- L3 (validity discarded) — not upheld: the pin is about whether the collision rule fires; validity is T-GASA-2's pin.

## Score
98: the Euro 4 pin was missed until the review.
