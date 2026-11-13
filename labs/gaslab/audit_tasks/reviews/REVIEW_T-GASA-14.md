# REVIEW T-GASA-14 — ACCEPT, score 96 (Windows Cowork, 2026-11-13)

Inline difficulty-1 row (roster 2026-11-13). `fix/T-GASA-14` on `fix/T-GASA-13` `952005f`: commits `1ea548d` (fix) and
`25c4bbe` (review fold-ins). F-C2-3 (HIGH; missed in the first pass, caught by the pre-handoff probe run). Ruling: the
VR edge `equals: NON_GDI` (a value no producer emits) becomes `not_equals: GDI`, a new dna-edge key consumed in
`resolution.apply_differentiators`. VR is reachable for PORT_INJECTION and CARBURETOR (GASWIKI-06A "FPR universal").
On GDI cars the edge keeps the ontology's existing disambiguation: the identical tailpipe goes to GDI_HPFP (06A: HPFP
"tailpipe identical to FPR rupture"). This is a deliberate exception to "universal" and is stated so in the ontology
comment. GDI behaviour is unchanged from before. Removing the edge was rejected: VR and GDI_HPFP would tie at an equal
rank on GDI cars.

Facts: probe f2 (F-C2-3) `1 passed`. gaslab `275 passed, 2 skipped, 4 deselected` (base 271 + 4); comlab `570`, wired
`186`, ui `75` (= baselines). v7 corpus: 9 of 314 GASLab states move to VACUUM_REGULATOR_DIAPHRAGM_RUPTURE (CSV-100,
EXP-N002, EXP-N003, YAML-CSV100 from INCOMPLETE_OXIDATION; EXP-N030, EXT-216, EXT-227, PDF-HI-001, YAML-PDF_HI_001 from
POA_SIGNATURE). All 9 carry no fuel type, so the composition default PORT_INJECTION applies. 0 family verdicts change;
accuracy 221 → 221. The fold-ins changed 0 verdicts. Mutations: ontology back to `equals: NON_GDI` → 2 failed; None
guard removed → 1 failed. ruff clean.

## Second review
APPROVE WITH CORRECTIONS (ds-flash, `C:/4DApp/recheck/codex/T-GASA-14_review.md`).
- H1 (GDI still excluded against "FPR universal") — upheld in part: the behaviour is the pre-existing disambiguation
  and is kept; the wrong comment is replaced by a stated exception.
- M2 (the GDI arm accepts any non-VR result) — upheld: it asserts GDI_HPFP_INTERNAL_SEAL_LEAK / VALID.
- M3 (`not_equals` fails open on an unresolved field) — upheld as hardening: `fuel_delivery_type` is a required
  `GasLabDnaView` field, so only a mistyped path gives None; it now fails closed, with a pin.
- M4 (the 9 states not listed) — evidence added above.
- L5 (no edge-key validation) — recorded nit (no loader validates edge keys today).
- L6 (probe output not pasted) — not upheld: f2 ran and printed `1 passed`; the baselines equal handoff 2115.

## Score
96: H1's comment and M2's weak pin were review catches.
