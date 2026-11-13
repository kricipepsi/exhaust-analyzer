# REVIEW T-GASA-5 — ACCEPT, score 98 (Windows Cowork, 2026-11-13)

Inline difficulty-1 row (roster 2026-11-13). `fix/T-GASA-5` on `fix/T-GASA-4` `f94a76e`: commit `aef9671`. F-C2-7
(HIGH). Ruling: the rule_engine rich-branch CAM_TIMING_RETARDED_MAP fallback adopts the two partial-normalisation
conditions that `resolution.py` already uses (λ rises idle→2500; CO falls idle→2500), per GASWIKI-04 §4.10 and
GASWIKI-06B. The fallback's other bounds are unchanged.

Facts: probe f6 (F-C2-7) passes. gaslab `242 passed, 2 skipped, 4 deselected` (base 238 + 4); comlab `570`, wired
`186`, ui `75` (= baselines); v7 corpus per-case `0 of 314` changed. Mutations: λ-rise removed → 1 failed; CO-fall
removed → 1 failed. ruff clean.

## Second review
APPROVE (ds-flash, `C:/4DApp/recheck/codex/T-GASA-5_review.md`). Three Lows, recorded as nits: the flat pin does not
test strict equality (each condition is killed by its own pin); the λ-falling pin needs Euro 2, because the Euro 3/4
2500 HC ceiling of 200 leaves no such pair (an 800k-reading seeded scan); the idle pin uses the finding's CO2 11.0,
above the 06B idle range 8.0-10.5.

## Score
98: the coverage nits.
