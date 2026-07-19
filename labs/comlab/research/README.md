# COMLab research — audit answers & external-research prompts

Index of the research artefacts produced for the COMLab leg of the
2026-06-03 capability audit (`docs/reference/audit_2026-06-03/4DLAB_CAPABILITY_AUDIT_AND_RESEARCH_QUESTIONS.md`).
Same pattern as `labs/obdlab/research/` and `labs/dnalab/research/`: questions the
codebase **cannot** answer become self-contained, project-agnostic web-research
prompts; questions the repo **can** answer are answered inline with file citations.

| File | What it is | Covers |
|---|---|---|
| `AUDIT_ANSWERS_COMLab.md` | Internal answers (codebase/docs-grounded) + routing table | Part 3 COMLab **Q2, Q6, Q9, Q10** answered; **Q1,Q3,Q4,Q5,Q7,Q8** routed to prompts A/B |
| `AUDIT_PART1_CEILING_RESEARCH.md` | Part 1 ("the ceiling, diagnosed") synthesis — grounds & routes each of the 4 culprits + 3 leak buckets | Part 1 §1.1–§1.3 |
| `WEB_RESEARCH_PROMPT_A_scoring_and_fusion.md` | Web prompt — scoring paradigm + evidence fusion | Q1, Q3, Q4 |
| `WEB_RESEARCH_PROMPT_B_calibration_and_differential.md` | Web prompt — confidence calibration, differential output, symptom-prior magnitude | Q5, Q7, Q8 |
| `WEB_RESEARCH_PROMPT_C_corpus_quality_and_label_noise.md` | Web prompt — synthetic-corpus signal sufficiency & label-noise impact | Part 1 Culprit 3 + §1.3 hypothesis |
| `OPEN_LEVERS_COMLab.md` | Analyst notes beyond the audit packs — measure-now / fix-now / new questions | levers not in Part 1/3 (score-gap dist, registry consolidation, base-weight inversion, fusion-mode split, gate leak) |
| `PROPOSAL_DeltaLab_cross_lab_delta_module.md` | Radical-rework candidate — cross-lab delta module as the primary discriminator | Culprits 1 & 4; builds on obdlab `delta-relations` research (FU-2) |
| `WEB_RESEARCH_PROMPT_D_delta_test_fixtures.md` | Web prompt — ground-truth fixtures for a two-point (delta) test suite | canonical operating points, full-taxonomy two-point signatures, tolerances, validity gating, paired datasets |

**How to use the web prompts (A/B/C/D):** each block between the `###` delimiters is
self-contained and contains **no project paths, lab names, or file references** —
hand it to a research agent verbatim. They are independent and can be run in
parallel.

**Status:** all 10 Part 3 COMLab questions and all of Part 1 are accounted for;
no question is dropped or duplicated. The four web prompts are the open external
gaps; everything else is answered internally. Cross-references the already-closed
OBDLab gate (`labs/obdlab/research/AUDIT_ANSWERS_OBDLab.md`) and the DNALab symptom
prompt (`labs/dnalab/research/WEB_RESEARCH_PROMPT_symptom_prior_and_vin_decode.md`).
