# Audit Part 1 (the ceiling, diagnosed) — research synthesis

**Author:** architect (4DLab) · **Date:** 2026-06-19
**Source:** `docs/reference/audit_2026-06-03/4DLAB_CAPABILITY_AUDIT_AND_RESEARCH_QUESTIONS.md` → **Part 1** (§1.1 leak buckets, §1.2 the four culprits, §1.3 one-sentence diagnosis).
**Purpose:** Part 1 states *problems*, not research questions. This doc applies the same dual treatment used for the Part 3 question packs: each problem is classified **web-researchable** (→ a project-agnostic research prompt) or **internal** (→ answered here from codebase/archive, web only if in doubt), grounded in the actual repo, and routed so nothing is left without a destination.

**Provenance note (surfaced, not hidden):** the original diagnostic docs Part 1 was built from (`DIAG_SUMMARY.md`, `TRIM_RESEARCH`, `ARCH_DECISION_PATH_FORWARD`, `REG_FAILURE_TRIAGE`) are **no longer in the live tree** — they were archived during the lab rework. `CORPUS_AUDIT.md` and `CHEMISTRY_COVERAGE.md` survive under `ARCHIVE/registry/`. Where a Part 1 claim can only be traced to the audit's own summary, it is cited as such; where it can be re-grounded in live code or surviving archive docs, it is.

---

## Anti-redundancy map — Part 1 problems are mostly already in flight

Part 1's culprits decompose into the per-lab Part 3 questions that the project has already researched (GASLab/OBDLab/DTCLab/DNALab) and the COMLab questions just answered. Only **one genuinely new external gap** falls out — corpus/label-noise (Culprit 3) — which gets a new prompt.

| Part 1 problem | Bucket | Destination |
|---|---|---|
| §1.1 PRUNED / never-surfaced (coverage) | internal | answered below (REG-2 result) + per-lab coverage research |
| §1.1 OUTRANKED (discrimination) | mixed | COMLab prompt **A** (ranker/fusion) + internal COMLab **Q6, Q9** |
| §1.1 data-gap STOP (measurement) | internal | answered below; OBDLab **Q1/Q4** (done) + GASLab **Q6** |
| §1.2 Culprit 1 — ranking is DTC-starved; need a DTC-independent primary discriminator | mixed | DTCLab **Q1** (done) + COMLab prompt **A** + internal COMLab **Q6** |
| §1.2 Culprit 2 — perception-vs-truth not measurable | internal | OBDLab **Q1/Q4** (done) + GASLab **Q6**; conceded data-gap (below) |
| §1.2 Culprit 3 — synthetic/hand-filled corpus may lack signal for 85 % | **web (new)** | **`WEB_RESEARCH_PROMPT_C_corpus_quality_and_label_noise.md`** + internal grounding below |
| §1.2 Culprit 4 — families chemically/electronically indistinguishable | internal | COMLab **Q6, Q10** (done) + per-lab tie-break research |
| §1.3 one-sentence diagnosis ("data, not code, is the constraint") | mixed | tested by COMLab **Q2** (Bayes ceiling) + prompt **C** |

The only file added for Part 1 is **prompt C**. Everything else is routed to research that already exists or was authored in this session — no duplicate prompts.

---

## §1.1 — Where capability leaks (the three buckets)

**Internal status, grounded:**

- **PRUNED / never-surfaced (~44, coverage).** This is *solved enough to be measured*: `T-FX-REG-2` added 24 coverage rules and rescued **37/44** PRUNED cases — yet top-1 accuracy did **not** move (`AUDIT §2 Wave E`). Coverage is therefore **not** the binding constraint; the rescued rule simply moves into the OUTRANKED bucket (`T-FX-REG-4`: "bottleneck shifted PRUNED→OUTRANKED"). See COMLab **Q9** for the precision/recall reading of the prune gate.
- **OUTRANKED (~82–90, discrimination).** The whole game. The correct rule survives pruning but loses the additive score to a higher-`base_weight` generic rule. The intended tie-breaker (DTC routing tag, `comlab/comlab/config/tag_discriminator.yaml`, weight `0.10`) is **present but starved** — 64/90 of these cases carry no DTC. Routed to COMLab prompt **A** (does the additive paradigm have an inherent ceiling; what fusion replaces it) and internal **Q6** (the minimal tie-break evidence and whether it is available).
- **data-gap STOP (~27 `ecu_fault`, measurement).** No code change recovers these — the discriminating signal is absent from the corpus (see Culprit 2). Internal status: **concede unless a new sensor channel is added.**

---

## §1.2 Culprit 1 — the ranking problem is the whole game, and it is data-starved

**Internal evidence (grounded):** the primary rank discriminator is the DTC routing tag (`tag_discriminator.yaml`, `discriminator_weight: 0.10`, applied only when the tag is present). `T-FX-REG-3` promoted routing tags into the rank weight and measured **0 false-positive delta**; `T-FX-WIRE-1` honest composite run held at **51.2 %** (`AUDIT §2 Wave E`). The structural point — *not every fault matures a DTC* (single-trip monitors, sub-threshold faults, mechanical/vacuum/exhaust conditions with no monitor, pre-/thin-OBD vehicles) — means a DTC-keyed primary discriminator is betting on a signal **missing for a structural majority** of cases.

**Classification & destination:** the empirical *"how often is a DTC present"* half is **DTCLab Q1** (already researched — DTC-presence reality on the 1990–2010 fleet). The *"what primary discriminator works when no code exists"* half is an **architecture** question fully inside **prompt A** (Q1 learned/statistical rankers that don't depend on one channel; Q3(b) preventing a weak/absent channel from swamping the result). **No new prompt needed** — Culprit 1 = DTCLab Q1 ∪ prompt A ∪ COMLab Q6.

## §1.2 Culprit 2 — perception-vs-truth is not measurable from the available data

**Internal evidence (grounded):** the 27 `ecu_fault` STOP cases need `lambda_perception_delta` + trim divergence, but OBDLab emits `NO_FAULT` across them (`AUDIT §1.2`). OBDLab's own research confirms the *defining* separation (ECU λ vs Brettschneider λ) **cannot be made from OBD-II alone** — it resolves only at the gas↔OBD fusion layer, which is why the architecture splits it (`obdlab/research/AUDIT_ANSWERS_OBDLab.md Q1`). The forced-override experiment was **net-negative** (App 4 `resolve_conflicts` = −5), so the design correctly pivoted to **"prior, not override"** (`AUDIT §1.2 Culprit 2`). The engine encodes that pivot today: `comlab/comlab/core/perception_contradiction.py` emits a contradiction flag rather than overriding.

**Classification & destination:** **internal — already researched and conceded.** The measurement gap is real and is answered by OBDLab **Q1/Q4** + GASLab **Q6** (how often tailpipe chemistry diverges from ECU λ). The *method* for using contradiction **as a feature without destructive override** is the one open architecture thread → **prompt A Q2**. No new prompt.

## §1.2 Culprit 3 — the corpus is synthetic, partly hand-filled, and may not carry enough signal *(NEW web gap → prompt C)*

**Internal evidence (grounded in surviving archive + live research):**

- **Synthetic + hand-curated.** The ground-truth corpus is `cases_petrol_master_v6.csv`, **281 cases curated to 252** (`ARCHIVE/registry/CORPUS_AUDIT.md`): **40 noise cases dropped** (analyser faults, sentinels, contrived multi-faults, hybrid/altitude edges) and **11 placeholder cases added** by gap analysis. Curation was **human-judgement dispositions** (46 proposals, 43 accepted, 3 overruled) — i.e. partly hand-filled.
- **Severe class imbalance.** Per-family counts range from `lean_condition` 53 and `misfire` 44 down to `ignition_fault` **3** and `non_starter` **4** (`CORPUS_AUDIT §2`). Single-digit families cannot support a tight accuracy estimate.
- **Ambiguous sentinels / fabricated values.** OBDLab research **confirmed ±127 is a sentinel, not a reading** (`obdlab/research/AUDIT_ANSWERS_OBDLab.md Q3`); the audit additionally records fabricated/uncertain trim values, blank `ect` masking, and a `DUAL_BANK` vs `dual` literal bug that dropped every bank-2 trim (`AUDIT §1.2 Culprit 3`).
- **Low separability slice.** The most common chemistry state (`TIMING_RETARDED`, ~25 % of cases) historically had **zero** matching rules and maps to **7 families** (`AUDIT §1.2 Culprit 3`; chemistry coverage in `ARCHIVE/registry/CHEMISTRY_COVERAGE.md`) — direct evidence of low class-conditional separability.

**Classification & destination:** the *internal facts above are settled*; what the repo **cannot** answer is the **external method/feasibility** question — *can a corpus of this size/quality support an 85 % target at all, how do you measure label-noise rate and separability, and how do you validate a partly-synthetic corpus?* That is a genuine new web gap, not covered by prompts A/B or any Part 3 question → **`WEB_RESEARCH_PROMPT_C_corpus_quality_and_label_noise.md`**. It pairs with COMLab **Q2** (the internal Bayes-ceiling estimate this corpus implies).

## §1.2 Culprit 4 — many families are indistinguishable with the evidence collected

**Internal evidence (grounded):** `mechanical_wear`, `exhaust_leak`, `ignition_fault`, `non_starter`, and several `ecu_fault` cases share chemistry/DTC signatures with louder families (misfire, lean) and lose every tie; weight-tuning to fix one provably regresses neighbours (`FT-8`, "scoring tightening is a smell"). This is a **taxonomy + evidence-sufficiency** problem.

**Classification & destination:** **internal — answered this session.** COMLab **Q10** shows the taxonomy is collectively exhaustive but **not mutually exclusive** (≥4 colliding family pairs), and **Q6** enumerates the minimal tie-break evidence per collision and whether it is available. The per-channel signature research (which gas/PID/DTC separates each pair) is the GASLab/OBDLab/DTCLab Part 3 packs. No new prompt.

---

## §1.3 — The one-sentence diagnosis is itself a testable hypothesis

Part 1 concludes: *"the tie-breakers are missing from the data, not the code — the next gains are a research/data problem."* That is the central claim to **test, not assume**. It is adjudicated by two things authored/identified here: COMLab **Q2** (the internal Bayes-optimal ceiling this corpus implies — currently estimated *below* 85 % with the four channels) and **prompt C** (the external evidence on whether a corpus of this size/quality can support a high target). If both confirm the corpus is the binding constraint, the productive path is **better/real data**, not more rules.

---

## Coverage check

Every Part 1 problem has a destination: §1.1 buckets and Culprits 2 & 4 are **internal/answered** (here + OBDLab research + COMLab Q6/Q9/Q10); Culprit 1 and the OUTRANKED bucket route to **prompt A** (+ DTCLab Q1, COMLab Q6); Culprit 3 and the §1.3 hypothesis route to the **new prompt C** (+ COMLab Q2). The only new artefact is `WEB_RESEARCH_PROMPT_C_corpus_quality_and_label_noise.md`; no Part 1 problem is dropped or duplicated.
