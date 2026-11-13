# REVIEW T-GASA-10 — ACCEPT, score 98 (Windows Cowork, 2026-11-13)

Inline difficulty-1 row (roster 2026-11-13). `fix/T-GASA-10` on `fix/T-GASA-9` `975ec74`: commits `3d6b47e` (fix) and
`6975153` (review fold-ins). F-C2-13 (MEDIUM, test-gap). Ruling: `audits._has_resolution` counts a `dna_gate` or a
filtering edge only (`dna`; `rpm_differential` with a truthy `appears_in_states` or `route_when_matched`, the keys
`resolution.py` consumes). `physical_check` and note-only edges never filter. The two pairs this surfaces
(EGR_DILUTION_MISFIRE with RICH_MISFIRE and with INCOMPLETE_COMBUSTION) are genuinely unresolved in v1: the fault's
gate is `requires_dtc`, which v1 does not consume (GASWIKI-06B). They are listed in `test_validators`
`KNOWN_UNRESOLVED_V1` with that reason; ledger row T-GASA-F13 (deferred) carries the work. Adding a DNA gate the wiki
does not state was rejected. `audits.py` is test-time only (`resolution.py` imports just `_is_catch_all`).

Facts: probe f13 passes. gaslab `271 passed, 2 skipped, 4 deselected` (base 268 + 3); comlab `570`, wired `186`, ui
`75`; v7 corpus per-case `0 of 314` changed. Mutations: old any-edge rule → 2 failed; `rpm_differential` always
filtering → 2 failed; key presence instead of truthiness → 1 failed. ruff clean.

## Second review
APPROVE (ds-flash, `C:/4DApp/recheck/codex/T-GASA-10_review.md`), four Lows.
- L1 (ordered tuples) — upheld, folded in (frozenset). L2 (falsy keys untested) — upheld, folded in (pins + mutation).
- L3 (the 0.99 / 0.985 ratios not pinned) — recorded nit; `test_validators` fails on them without the set.
- L4 (ledger row missing) — upheld: T-GASA-F13 written with this acceptance.

## Score
98: the Lows.
