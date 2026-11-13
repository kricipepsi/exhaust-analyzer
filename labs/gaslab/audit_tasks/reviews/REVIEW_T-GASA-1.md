# REVIEW T-GASA-1 — ACCEPT, score 99 (Windows Cowork, 2026-11-13)

Inline difficulty-1 row (roster 2026-11-13). `fix/T-GASA-1` on `fix/T-COMA-30` `7034d64`: commit `faf407d` (F-C2-1,
HIGH). Ruling: keep the sub-14 % leak route (GASWIKI-05) and add the GASWIKI-04 §4.2 dilution screen (CO + CO2 > 6 %);
a diluted sample falls through to the below-14 % halt (SAMPLE_INVALID / INVALID). Lost: removing the route
(contradicts GASWIKI-05); a bare lower bound on the sum (no wiki source).

Facts: new test `4 passed` (base `3 failed, 1 passed`); F-C2-1 probe `1 passed`; gaslab `220 passed, 2 skipped,
4 deselected, 3 errors` (the 3 `test_ontology` FileNotFound errors are on the base too, and do not recur on a fresh
basetemp); comlab `570`, wired `186`, ui `75`; corpus verdicts `0` changed vs the T-COMA-28 tip (no corpus case reaches
the leak route); ruff clean.

## Second review
APPROVE (`C:/4DApp/recheck/codex/T-GASA-1_review.md`). One Low upheld as a nit (the helper's docstring does not cite
§4.2); folded into T-GASA-2, which edits the same file.

## Score
99: the nit.
