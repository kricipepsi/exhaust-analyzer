---
chunk_id: DNAWIKI-94
title: "Per-engine reference data & aftermarket-mod corruption"
lab: dnalab
doc: DNA_WIKI
role: research-evidence
status: authoritative
date: 2026-06-12
kg_ingestion: none
consumer: "VINLab CoC / rated_rpm fields ; COMLab identity-trust cap"
raw_inputs: "../answersDNA.md §6, §7"
related_chunks: [DNAWIKI-90, DNAWIKI-93]
---

# Per-engine reference data & aftermarket-mod corruption

**Disposition: research-evidence.** Numbers `routes-to:` VINLab CoC fields and the COMLab
identity-trust cap. (DNA10 Q3, Q7.)

## Part A — per-engine reference-data availability (Q3)

```
# source: EPA certification archives (dataset, 2026)
# finding: public CoC / certified test-result archives span model years 1979–2013
routes-to: VINLab CoC / rated_rpm fields (a real public source backs the CoC fill, not just CSV medians)
```

The EPA CoC archives are a **real, free, in-scope** source for the 1990–2010 fleet —
engine-family / test-group names, federal + California emissions standards, evaporative
compliance. This is the canonical backing for VINLab's CoC fields (today ~62–65% filled from
CSV medians per DNA10 Q3).

**But** the government data is compliance-shaped, not workshop-shaped:

| Attribute | EPA public CoC | Commercial (ALLDATA / Identifix) |
|---|---|---|
| emissions standards / test groups | fully detailed | partial |
| target idle RPM | generic certification limits only | specific OEM nominal ranges |
| wiring / pin-outs | absent | fully integrated |
| symptom→repair case history | absent | fully documented |
| access | **free, public domain** | **paid licence** |

```
# finding: no FREE public source maps engine-code → physical repair params (target fuel pressure,
#          compression, sensor sweeps) — those need a paid commercial licence
routes-to: COMLab data-sourcing note (CoC gives emissions/idle envelope; repair params are out of reach for free)
```

**Read for VINLab/COMLab:** the EPA archive can legitimately raise CoC fill and ground
`rated_rpm` / emissions class, but it will **not** supply technician repair parameters — so
COMLab must not assume those are derivable from identity for free.

## Part B — aftermarket mods corrupt VIN assumptions (Q7)

A VIN describes the **factory** car. The 1990–2010 enthusiast fleet is heavily modified, and
none of it shows in the VIN — this is a direct cap on identity-channel trust.

```
# source: Dataintelo tuning-market analysis (industry, 2025)
# finding: petrol = 41.2% of a $9.8B remap market; Europe = 32.7% ($3.2B) — mods are prevalent
routes-to: COMLab identity-trust cap (factory-spec-from-VIN is an assumption, not a fact)
```

```
# source: EPA tampering surveys (government, 1984/1986/1989 — early-fleet baseline, in/near scope)
# finding: overall gasoline tampering 19–22%; up to 1/3 show possible/definite tampering
routes-to: COMLab identity-trust cap (discount hardware-from-VIN by a tampering allowance)
```

Component-level tampering rates (gasoline cars):

| Component tampered | rate | effect | # source: |
|---|---|---|---|
| catalytic converter removal | 5–11% (lower where I/M active) | +475% HC / +425% CO | EPA survey |
| air-pump deactivation | 8–11% | +200% HC / +800% CO | EPA survey |
| EGR tampering | 7–14% | +175% NOx | EPA survey |
| O2 sensor disconnect/tamper | ~1% (rises with age) | +450% HC / +1200% CO | EPA survey |

```
# source: SciencePG ECU-tuning study (peer-reviewed, 2026)
# finding: remaps add up to 25% power (turbo) / 15% (NA); post-2000 flashed via OBD-II, pre-2000 chip-swap
routes-to: COMLab identity-trust cap (remapped ECM behaviour ≠ factory map the VIN implies)
```

### The diagnostic trap (carry this for COMLab)

```
# finding: a de-cat + remap can make a tuned ECM SKIP the catalyst monitor — upstream & downstream O2
#          mimic each other, P0420/P0421 never set, yet no functional catalyst is present
routes-to: COMLab identity-trust cap + truth-vs-perception logic
          (gas chemistry is ground truth; a "clean" ECU on modified hardware is perception)
```

This is the strongest argument for the project's **truth-vs-perception** stance: when
hardware may be silently modified, the ECU's "no codes" is *perception* and the gas chemistry
is *ground truth*. COMLab should treat VIN-derived hardware as a **discountable assumption**,
not fact.

## Gap

No post-2020 remote-sensing survey isolates ECU-remap rates **specifically for 1990–2010
petrol passenger cars** in today's fleet (modern surveys target diesel pickups). So the
tampering allowance must be an estimate band, not a precise rate. Logged as a question.



## Graph relations (explicit)

**EPA CoC archives (MY 1979–2013)** PROVIDE **free, public CoC / test-result data** (PROPOSAL — VINLab CoC/rated_rpm fill; not live)
**EPA CoC data** IS **compliance-shaped, not workshop-shaped** (PROPOSAL — gives emissions/idle envelope, not repair params)
**commercial repair params (fuel pressure, compression, sensor sweeps)** ARE **paid-licence only** (PROPOSAL — COMLab data-sourcing constraint)
**petrol remap market** IS **41.2% of $9.8B** (PROPOSAL — COMLab identity-trust cap; factory-spec-from-VIN is an assumption)
**gasoline tampering rate** IS **19–22% overall** (EPA surveys 1984–1989) (PROPOSAL — COMLab identity-trust cap discount)
**catalyst removal rate** IS **5–11%** (PROPOSAL — +475% HC / +425% CO emission impact)
**EGR tampering rate** IS **7–14%** (PROPOSAL — +175% NOx emission impact)
**remap power gains** ARE **up to 25% turbo / 15% NA** (PROPOSAL — remapped ECM behaviour ≠ factory map)
**de-cat + remap** CAN **skip catalyst monitor** (PROPOSAL — upstream & downstream O2 mimic each other, P0420/P0421 never set)
**gas chemistry** IS **ground truth** (PROPOSAL — ECU "no codes" on modified hardware is perception)
**VIN-derived hardware** IS **a discountable assumption, not fact** (PROPOSAL — COMLab identity-trust cap)
**no post-2020 remap survey for 1990–2010 petrol** IS_A **genuine gap** (QUESTION — tampering allowance is estimate band, not precise rate)

## Core Entities

- `VINLab CoC / rated_rpm fields` — per-engine reference data; STATUS: PROPOSAL (EPA archives backing)
- `COMLab identity-trust cap` — discount for aftermarket mods + tampering; STATUS: PROPOSAL
- `EPA certification archives` — free public CoC source MY 1979–2013
- `EPA tampering surveys (1984–1989)` — gasoline tampering baseline evidence
- `truth-vs-perception` — architecture principle: gas chemistry is ground truth, ECU is perception
- `aftermarket mods` — remap + de-cat + tampering; corrupt VIN assumptions
