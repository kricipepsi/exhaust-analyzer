# REVIEW T-GASA-11 — ACCEPT, score 100 (Windows Cowork, 2026-11-13)

Inline difficulty-1 docs row (roster 2026-11-13; a docs row has no second review). `fix/T-GASA-11` on `fix/T-GASA-10`
`064bc91`: commit `ef0125a`. F-C2-14 (MEDIUM, doc-drift). Ruling: GAS_VOCABULARY §6 and GASWIKI-02 §2.3 now state the
implemented λ (`brettschneider.lambda_chem`): λ₄ = ([CO₂] + [CO]/2 + [O₂]) / ([CO₂] + [CO] + HC·0.0025), plus the
5-gas NOx term. The formula printed before is kept only as a note: it has no `(1 + Hcv/4 …)` normalisation and gives
λ ≈ 1.45 at stoichiometry, so it is not a definition. Changing the code to the full Brettschneider equation (`Hcv`,
normalised denominator) moves every verdict and is deferred as T-GASA-F14. Probe `test_f14` asserts the old printed
formula and stays red by this ruling.

Facts: the stated formula reproduces the code on R(20, 0.2, 15.0, 0.2, 50): `1.003441` both ways. gaslab `271
passed, 2 skipped, 4 deselected`; comlab `570`, wired `186`, ui `75` (unchanged; no code changed).

## Score
100.
