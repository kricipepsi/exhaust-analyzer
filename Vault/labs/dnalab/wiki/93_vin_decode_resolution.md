---
chunk_id: DNAWIKI-93
title: "VIN-decode resolution for 1990–2010 petrol cars"
lab: dnalab
doc: DNA_WIKI
role: research-evidence
status: authoritative
date: 2026-06-12
kg_ingestion: none
consumer: "VINLab decode-confidence field ; COMLab identity-channel trust ; deferred full/basic tier"
raw_inputs: "../answersDNA.md §5"
related_chunks: [DNAWIKI-90, DNAWIKI-94]
---

# VIN-decode resolution for 1990–2010 petrol cars

**Disposition: research-evidence.** Numbers `routes-to:` VINLab / COMLab consumers and the
deferred tier decision. This is the headline empirical input for whether the output dataset
can be split into `full` | `basic`. (DNA10 Q2, and partly Q4/Q8.)

## Finding — VIN resolution is sharply **region-dependent**

```
# source: ISO 3779 / 4030 + NHTSA 49 CFR 565 (standards); Grokipedia Porsche VIN (industry, 2024)
# finding: VDS (positions 4–8) is engine-precise in North America but frequently a "ZZZ" placeholder in Europe/RoW
routes-to: VINLab decode-confidence field   (confidence must be region-aware, not uniform)
routes-to: COMLab identity-channel trust    (identity prior weaker for RoW VINs)
routes-to: deferred full/basic tier         (this is the empirical basis for the split)
```

| VIN positions | Section | North America (NHTSA) | Europe / Rest-of-World |
|---|---|---|---|
| 1–3 | WMI | country + manufacturer + division — **100% reliable** | same — **100% reliable** |
| 4–8 | VDS | model, body, restraint, **exact engine code** — highly detailed | **often `ZZZ` placeholder** — blind to engine/fuel/induction/emissions |
| 9 | check digit | modulo-11 check digit (catches transcription errors) | generic filler — no check-digit security |
| 10 | model year | cyclic year code — reliable | reliable |
| 11 | plant | plant code | plant code |
| 12–17 | serial | sequential serial | sequential serial |

## The regional loophole (the crux)

Detailed VDS encoding was **not legally mandated outside North America** in the 1990–2010
era, so European makers (e.g. VW/Audi/Porsche) routinely filled VDS positions 4–6 with
`ZZZ`. For such a VIN the number is **completely blind** to engine displacement, fuel
delivery, induction, and emissions spec without a **proprietary OEM build-database** lookup.

```
# consequence for VINLab: a uniform confidence=PARTIAL today is hiding two very different cases:
#   NA VIN     → engine code decodable        (→ candidate "full")
#   RoW ZZZ VIN→ engine spec NOT in the VIN    (→ candidate "basic" unless OEM lookup available)
routes-to: deferred full/basic tier (../research/DEFERRED_full_basic_dataset_decision.md)
```

This is exactly why the owner's future **two-tier (`full` | `basic`)** model is well-founded:
the `full`/`basic` boundary maps cleanly onto *"is the engine spec actually recoverable from
this VIN?"* — not onto an arbitrary fill threshold.

## What a VIN can never resolve (even when VDS is full)

```
# source: answersDNA.md §5 (VECI-label dependence)
# finding: even a fully-populated VDS cannot give exact heated-O2 count, EGR revision, or catalyst monolith weight
routes-to: VINLab CoC fields (these sub-attributes need CoC / VECI lookup — see page 94)
routes-to: COMLab identity-channel trust (do not assume fine emissions config from VIN alone)
```

Fine-grain emissions equipment requires the under-hood VECI label or a CoC lookup, never the
VIN. This bounds how much hardware COMLab may infer from identity alone.

## Q8 corollary — `model` can stay empty

The decodable, diagnosis-relevant identity is **engine code + displacement + induction**
(when present). Finer identity (`model`, trim variant) adds little once those are known,
which supports leaving `model` empty rather than forcing a lookup.

```
routes-to: COMLab identity scope (no consumer needs `model`; leave it empty — signal/noise)
```

## Gap

No public database lists exactly **which European models dropped the `ZZZ` placeholder before
2010**, so the `full`/`basic` rule cannot be derived from a clean per-model table — it must
key off *observed VDS content per VIN* plus WMI region. Logged as a question; it is a primary
unknown the deferred tier decision must resolve.



## Graph relations (explicit)

**VIN VDS positions 4–8** ARE **engine-precise in North America** (PROPOSAL — VINLab decode-confidence field; deferred full/basic tier)
**VIN VDS positions 4–8** ARE **frequently ZZZ placeholder in Europe/RoW** (PROPOSAL — VINLab region-aware confidence)
**NA vs RoW VIN resolution gap** DRIVES **full|basic two-tier output model** (PROPOSAL — deferred decision)
**RoW ZZZ VIN** IS **blind to engine displacement/fuel/induction/emissions** (PROPOSAL — COMLab identity-channel trust discount)
**full/basic boundary** MAPS_ONTO **"is engine spec recoverable from VIN?"** (PROPOSAL — not an arbitrary fill threshold)
**even full VDS** CANNOT resolve **heated-O2 count, EGR revision, catalyst monolith weight** (PROPOSAL — needs CoC/VECI lookup)
**fine emissions config** REQUIRES **under-hood VECI label or CoC lookup** (PROPOSAL — bounds COMLab hardware-from-identity inference)
**model field** CAN stay empty (PROPOSAL — no consumer needs it; signal/noise)
**no public ZZZ-dropoff table per model** IS_A **genuine gap** (QUESTION — full/basic rule must key off observed VDS + WMI region)

## Core Entities

- `VINLab decode-confidence field` — region-aware confidence (NA high, RoW low); STATUS: PROPOSAL
- `COMLab identity-channel trust` — discount for RoW VINs + aftermarket mods; STATUS: PROPOSAL
- `full|basic two-tier output` — deferred dataset-split decision; STATUS: PROPOSAL
- `ZZZ placeholder` — European VDS positions 4–6 blind spot; consumer: VINLab
- `VECI label / CoC lookup` — fine emissions config source; consumer: VINLab CoC fields (PROPOSAL)
