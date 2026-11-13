# REVIEW T-GASA-3 — ACCEPT, score 97 (Windows Cowork, 2026-11-13)

Inline difficulty-1 row (roster 2026-11-13). `fix/T-GASA-3` on `fix/T-GASA-2` `6427c7f`: commits `cc03534` (fix) and
`228aadf` (review pins). F-C2-5 (HIGH), first half. Ruling: the valve-seal route's idle band is 75-500, not 300-500.
GASWIKI-06A §FAULT_WORN_VALVE_SEALS physics says the v1 (HC 75-250) and v2 (HC 300-500) rows are one fault at two
severities, and §6A.1 routing precedence sends a sharp HC drop at 2500 RPM to WORN_VALVE_SEALS first. A bound-matched
WORN_VALVE_SEALS now survives a confirming 2500 RPM reading (before: VVT_FAILURE).

Rejected alternative (measured): widening the ontology box to HC 500 / CO 1.2 / λ 0.90 makes probe f5b pass, but the
pin `test_worn_valve_seals_idle_hc_drops_at_2500` (idle HC 150, no 2500 reading) then returns WORN_ENGINE. The v2 band
also needs F-C2-14: the code's λ is 0.914 for the wiki's λ 0.96 vector. **Residual: F-C2-5 second half (probe f5b, v2
idle 300-500 never bound-matches) stays open** with F-C2-14.

Facts: probe f5 passes, f5b red (residual). gaslab `230 passed, 2 skipped, 4 deselected` (base 226 + 4). comlab `570`,
wired `186`, ui `75`. v7 corpus per-case verdicts `0 of 314` changed (`recheck/gasa/f5_base.json` vs
`f5_routeA.json`; family accuracy 221). Mutations: band 300 → 4 failed; band 150 → 1 failed; union 75-250|300-500 →
1 failed. ruff clean.

## Second review
APPROVE WITH CORRECTIONS (ds-flash, `C:/4DApp/recheck/codex/T-GASA-3_review.md`).
- M1 (hull 250-300 is in neither source) — upheld as untested, not as wrong: a seeded scan found 81 of 39 890 valid
  idle readings at HC 251-299 that now route to WORN_VALVE_SEALS. Their idle-only verdict is WORN_ENGINE, which the wiki
  defines as HC that does not clean up; a drop to 20 ppm is the valve-seal pattern by §6A.1 precedence. Kept the band;
  pinned HC 258 (`228aadf`).
- L1 (only HC 150 pinned) — upheld: pins at 101 (the lowest idle HC that reaches the route, seeded scan; 75-100 never
  holds a wear survivor) and 250 (v1 top edge).
- L2 (aggregate corpus evidence only) — not upheld: the per-case diff was measured, 0 of 314 changed.
- L3 (residual f5b / F-C2-14) — recorded above.

## Score
97: the band's 250-300 behaviour was not tested until the review.
