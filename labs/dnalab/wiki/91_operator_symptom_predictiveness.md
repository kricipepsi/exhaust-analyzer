---
chunk_id: DNAWIKI-91
title: "Operator-symptom predictiveness & the false-report rate"
lab: dnalab
doc: DNA_WIKI
role: research-evidence
status: authoritative
date: 2026-06-12
kg_ingestion: none
consumer: "COMLab-B report-trust cap ; COMLab-F symptom-prior weighting"
raw_inputs: "../answersDNA.md §1, §2, §8"
related_chunks: [DNAWIKI-90, DNAWIKI-92]
---

# Operator-symptom predictiveness & the false-report rate

**Disposition: research-evidence.** Every number here `routes-to:` a COMLab consumer. The
real home of these figures is the COMLab proposals registry; this page is the evidence
trail. (DNA10 Q1, Q9, Q10.)

## Finding 1 — raw reported symptoms are weak predictors

```
# source: Deep-SBM / Cognitran Ltd evaluation (peer-reviewed, 2020)
# finding: hand-crafted expert RMI rule-bases peak at ≈ 50% symptom→fault accuracy
routes-to: COMLab-F symptom-prior weighting   (cap the prior's strength at the evidence)
routes-to: COMLab-B report-trust cap          (a ~50% baseline is a prior, never an override)
```

A direct symptom→fault rule-base — exactly the "first-guess" flow a cheap channel would use
— tops out around **50%** accuracy. This is the honest ceiling for *unassisted* symptom
prediction and is the central reason the architecture insists the symptom prior **stays a
prior**.

Accuracy rises sharply only when the symptom is **fused with structured signals**, which is
COMLab's job, not DNALab's:

| Method | Inputs | Accuracy | # source: |
|---|---|---|---|
| Traditional OEM RMI (symptom→fault rules) | manual symptom mapping | **≤ 50%** | Deep-SBM eval, 2020 |
| KG-LLM framework | cleaned diagnostic dialogue | **77.3%** (+46.1% vs baseline LLM) | KG-LLM / German OEM, 2024 |
| G-OBD assistant | OBD-II codes + live PIDs + history | **89.3%** vs certified mechanics (450 DTCs) | G-OBD, 2024 |
| Deep-SBM | 2,093 structured features → ~3,000 fault classes | "significant improvement over RMI" | Deep-SBM, 2020 |

```
routes-to: COMLab fusion design — evidence that the symptom channel must be COMBINED with
           OBD/gas signals to be trustworthy; it does not license a standalone symptom verdict.
```

**Read for COMLab:** the gap between ~50% (symptom alone) and ~89% (symptom + OBD/live data)
quantifies *how much* the symptom prior should be discounted before fusion.

## Finding 2 — the false / misleading report rate is large (NTF)

```
# source: Symestic / MES diagnostics (industry, 2026)
# finding: No-Trouble-Found / RTOK / CND rates run 30–70% of warranty returns;
#          €50–€500 cost per false claim
routes-to: COMLab-B report-trust cap   (upper bound on how far a raw report is trusted)
```

In **up to 70%** of triage cases the customer's self-reported symptom **cannot be
duplicated** on re-inspection. That is the single hardest cap on the channel: a large share
of reports are noise before any mapping even happens.

A major driver is **linguistic degradation** of complaints:

```
# source: text-mining diagnostic study (peer-reviewed, 2015)
# finding: customer descriptions are ill-structured; the word "engine" had >20 spellings;
#          one fault described as "engine knocks" / "hood squeak" / "engine misses idle" / "engine lopes"
routes-to: COMLab-A (tier_1,tier_2) routing   (why SymptomLab's CLOSED tier vocabulary exists)
routes-to: SymptomLab catalog mapping         (standardised pairs replace free text — see page 92)
```

This is the evidence base for SymptomLab using a **closed two-tier catalog** rather than
free text: the catalog is the noise-reduction step that makes the prior usable at all.

## Finding 3 — labeled symptom→fault data is real but gated (Q10)

```
# source: software-market reviews + diagnostic evaluations (industry/peer-reviewed, 2024)
# finding: no FREE open multi-brand raw-complaint→fix dataset exists; structured ones do —
#          Identifix, ALLDATA, Cognitran (2,093 inputs / 3,000 faults), German-OEM dialogue set
routes-to: COMLab validation plan   (which dataset could validate the prior — NOT a shippable literal)
```

No open dataset pairs raw driver text with confirmed fixes; the usable ones are
**commercial/proprietary**. This bounds how the prior can be *validated* (it likely cannot be
trained on open data), and is logged as a validation constraint, not a number that ships.

## Net for the trust cap

The channel is cheap and independent but **noisy on two axes at once** — ~50% best-case
mapping accuracy *and* 30–70% unverifiable reports. Both push the same way: COMLab should set
a deliberately **conservative report-trust cap** and treat the symptom output as a prior to
be confirmed by gas/OBD evidence. All specific cap/weight values are authored in the COMLab
proposals registry (COMLab-B/F), never here.



## Graph relations (explicit)

**symptom→fault expert RMI accuracy** PEAKS_AT **~50%** (PROPOSAL — COMLab-F symptom-prior weighting; COMLab-F not live)
**NTF/RTOK false-report rate** IS **30–70% of warranty returns** (PROPOSAL — COMLab-B report-trust cap; COMLab-B not live)
**unassisted symptom prediction** IS_A **prior, never an override** (PROPOSAL — architecture constraint for COMLab fusion)
**symptom + OBD/gas fusion accuracy** REACHES **~89%** (G-OBD baseline) (PROPOSAL — COMLab fusion design evidence)
**symptom-alone vs fused gap** IS **~50% → ~89%** (PROPOSAL — quantifies how much to discount symptom prior)
**linguistic degradation of complaints** DRIVES **SymptomLab CLOSED tier vocabulary** (PROPOSAL — catalog design evidence)
**customer text→fix dataset** IS **commercial/proprietary only** (PROPOSAL — validation constraint, not shippable)
**report-trust cap** MUST_BE **conservative** (PROPOSAL — both mapping noise AND NTF noise push same way)
**all specific cap/weight values** AUTHORED_IN **COMLab proposals registry** (PROPOSAL — never in dnalab/)

## Core Entities

- `COMLab-B report-trust cap` — upper bound on raw symptom report trust; STATUS: PROPOSAL
- `COMLab-F symptom-prior weighting` — prior strength bands; STATUS: PROPOSAL
- `~50% symptom→fault accuracy` — Deep-SBM / Cognitran (2020); consumer: COMLab-F
- `30–70% NTF rate` — Symestic / MES (2026); consumer: COMLab-B
- `~89% fused accuracy` — G-OBD (2024); consumer: COMLab fusion design
- `SymptomLab CLOSED tier catalog` — noise-reduction step; consumer: COMLab-A (PROPOSAL)
