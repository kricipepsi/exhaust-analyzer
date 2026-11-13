# REVIEW T-GASA-9 — ACCEPT, score 98 (Windows Cowork, 2026-11-13)

Inline difficulty-1 row (roster 2026-11-13). `fix/T-GASA-9` on `fix/T-GASA-8` `9636b26`: commits `8fdd9a1` (fix) and
`a884c69` (review fold-ins). F-C2-12 (MEDIUM). Ruling: GASWIKI-04 §4.8 is unconditional, and GASWIKI-05 gives
IGNITION_MISFIRE `dna_gate: none`, DEFINITIVE via RULE_MASKING, with the cylinder count as an estimate (≈). The
`inferred_cyl >= 1` gate is removed, which also removes the banker's-rounding edge. The former pin
`test_cylinder_count_read_in_masking_path` pinned that unstated gate and is restated over cylinder counts 1-16. The
DLD and LLD follow the code; the generated `graph/` artefacts are not edited.

Before this row, F-C2-11 was measured inline and deferred (ledger row T-GASA-F11, `9636b26`).

Facts: probe f12 passes. gaslab `268 passed, 2 skipped, 4 deselected` (base 253: -1 old pin, +16 parametrized);
comlab `570`, wired `186`, ui `75` (= baselines); v7 corpus per-case `0 of 314` changed. Mutation: gate restored → 2
failed. ruff clean.

## Second review
APPROVE (ds-flash, `C:/4DApp/recheck/codex/T-GASA-9_review.md`), two Lows, both folded in (`a884c69`): the pin now covers
cylinder counts 1-16 (the DLD range); the LLD change note records the removal.

## Score
98: the Lows.
