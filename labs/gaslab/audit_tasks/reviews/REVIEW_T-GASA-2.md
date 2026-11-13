# REVIEW T-GASA-2 — ACCEPT, score 99 (Windows Cowork, 2026-11-13)

Inline difficulty-1 row (roster 2026-11-13). `fix/T-GASA-2` on `fix/T-GASA-1` `794cddb`: commit `f00d7d9` (F-C2-2,
HIGH). Ruling: the collision rule (GASWIKI §8.5) names the chemistry and returns the triangle gate's `validity`, not a
hard-coded EXTERNAL_O2_SUSPECT; two tests that pinned EXTERNAL_O2_SUSPECT on a 16.0 % sum (inside VALID [14, 16]) are
re-stated. Since T-COMA-17 COMLab warns and continues on EXTERNAL_O2_SUSPECT, so the finding's abort no longer occurs;
the label was still wrong. Also carries the T-GASA-1 docstring nit.

Facts: new test `3 passed` (base `2 failed, 1 passed`); F-C2-2 and F-C2-1 probes pass; gaslab `226 passed, 2 skipped,
4 deselected`; comlab `570`, wired `186`, ui `75`; corpus verdicts `0` changed; ruff clean.

## Second review
APPROVE (`C:/4DApp/recheck/codex/T-GASA-2_review.md`). Lows: probe NOx 80 vs the finding's 30 and no 14/18 boundary
cases (nits, recorded); RICH_MISFIRE at λ 1.074 (residual for F-C2-6 / F-C2-9, out of scope by ruling); the docstring
edit (the planned T-GASA-1 nit, not scope noise).

## Score
99: the boundary-coverage nit.
