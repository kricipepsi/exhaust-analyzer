# REVIEW T-GASA-18 — ACCEPT, score 97 (Windows Cowork, 2026-11-14)

Inline difficulty-1 row (roster 2026-11-13). `fix/T-GASA-18` on `fix/T-GASA-17` `66acf33`: commits `8b7b4f3` (fix) and
`4287ab1` (correction 1). T-GASA-F45: the CO normal-with-cat maximum 0.45 % becomes 0.3 %, the UK in-service legal
idle limit for cat cars first used from 1/9/2002 (T-GASA-17 verdicts W0185 and W1303 CONTRADICTED; source S001, MOT
inspection manual 8.2.1). Changed: ontology NORMAL co max and collision `co_tier_max`, the TIMING_OVER_ADVANCED
"others near normal" guard, the rule_engine default, vocab 10.2, wiki 03/05/07/11.

Facts: gaslab `279 passed, 2 skipped, 4 deselected`; comlab `570`, wired `186`, ui `75` (re-run after correction 1).
v7 corpus: family accuracy 221 of 314 before and after, 0 family verdicts change; 5 GASLab states move to
RICH_MISFIRE, all labelled misfire. Mutations: 3 killed by the new pin test; a mutant that ignores `co_low_idle` fails
the corrected CoC test.

Finding outside the row (already registered as T-GASA-FEURO): classify always replaces the ontology NORMAL co max with
the Euro table idle ceiling (`_euro_thresholds`), so the 0.3 value is the stated baseline, not the operative ceiling.

## Second review
APPROVE WITH CORRECTIONS (ds-flash, `C:/4DApp/recheck/codex/T-GASA-18_review.md`).
- M1 (CoC CO test lost its discriminating power) — upheld: CO 0.15 with `co_low_idle` 0.12 and a no-CoC control.
- L1 (0.3 fallback unreachable) — not upheld: a defensive default equal to the ontology value, the house pattern.
- L2 (test name implies 0.3 is operative) — upheld: renamed to the stated baseline, docstring names FEURO.
- L3 (0.3-0.5 gap undocumented) — upheld: vocab note, 0.5 % for cat cars first used 1/8/1995-31/8/2002 (S009).
- L4 (before/after labels not shown) — not upheld: the 5 states were already in the misfire family.

Correction review: APPROVE (ds-flash, `C:/4DApp/recheck/codex/T-GASA-18_c1_review.md`).

## Score
97: one Medium test-strength defect needed a correction.
