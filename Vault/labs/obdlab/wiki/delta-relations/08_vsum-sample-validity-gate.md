---
chunk: delta-relations/08_vsum-sample-validity-gate
topic: delta-relations
sources:
  - various/Vol7.md — "validation sum (vsum)" + dilution-failure rule
consumer: GASLab ingestion validity gate — reject/flag a 5-gas frame before it enters any Δ or λ computation; prevents diluted samples from poisoning the transition matrix (delta-relations/07) and λ_chem.
consumer_status: PROPOSAL (gate not yet in gaslab; names producer GASLab + reader COMLab delta engine)
provenance: sources/various/Vol7.md — vsum/dilution thresholds READABLE as prose; the vsum display equation itself is stripped (see formula-wiki pending list)
dedup: new — no existing chunk carries 5-gas sample-validity
---

# 5-gas sample-validity gate (vsum + dilution)

Before any Δgas or Brettschneider-λ is trusted, the raw 5-gas sample must pass a
validity check. A diluted sample (probe leak, cracked tailpipe, ambient ingress)
produces false-lean λ and corrupts every downstream delta.

## Validity rules (Vol7, readable as prose)

```
vsum = HC + CO + CO2 + O2 + NOx   (key exhaust constituents, % volume basis)

VALID sample:     14.0% <= vsum <= 18.0%
vsum < 14.0%  ->  severe dilution (probe/tailpipe leak drawing ambient air)
vsum > 18.0%  ->  near-ambient / exhaust leak bypassing the cat (~20.9% O2 ref)
dilution fail:    CO + CO2 <= 6.0%   (too much ambient air for a reliable profile)
```

> ⚠ The vsum **display equation** in Vol7 was image-stripped in export; the
> threshold values above survive in prose. The exact constituent weighting is
> logged in the formula wiki's "pending readable export" list — not reconstructed here.

## Logic / why it matters

At **curb idle**, low exhaust velocity allows pulse reversion (ambient air drawn back
into the tailpipe), skewing O₂ up and λ lean. At **2500 RPM** the high-velocity
unidirectional stream builds a positive-pressure barrier that displaces ambient air →
a pure engine-out sample. So a frame failing vsum at idle but passing at 2500 RPM is
itself a signature (exhaust-path/sampling integrity), not an engine fault.

## Consumer / code path

GASLab marks each per-state frame `gas_sample_valid` + `vsum`; the COMLab delta engine
(delta-relations/07 consumer, FU-2) must skip Δ computation on an invalid frame. Field
+ consumer ship together.


## Core Entities

- VSUM, GAS_SAMPLE_VALID, DILUTION_FAIL
- GASLab (producer/gate), COMLab delta engine (reader, PENDING FU-2)

## Graph relations (explicit)

**GASLab** EMITS **GAS_SAMPLE_VALID** and **VSUM** per frame
**VSUM** below 14.0% INDICATES **DILUTION_FAIL**
**DILUTION_FAIL** INVALIDATES **DELTA_GAS** frame
**COMLab delta engine** SKIPS_ON **GAS_SAMPLE_VALID** false

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
