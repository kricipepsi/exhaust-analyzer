---
chunk: truth-perception/04_combustion-integrity-oxygen-usage
topic: truth-perception
sources:
  - various/Vol1.md — "Combustion Integrity Truth" enhancement (Chemical_Efficiency_Score, Oxygen_Usage_Factor)
consumer: GASLab chemical resolver → COMLab misfire-vs-rich discriminator (fault_atlas). Separates a misfire (raw O₂+raw fuel) from pure over-fuelling from the gas chemistry alone.
consumer_status: PROPOSAL (named consumer; pairs with GASLab misfire chemistry resolver, proposals/extracted EP-GAS-02)
provenance: sources/various/Vol1.md — formula intent READABLE in prose ("ratio of CO2 to CO+CO2"; "ratio of O2 to CO"); exact display forms stripped
dedup: new — quantifies what o2-logic/07 misfire-vs-lean caveat states qualitatively
---

# Combustion integrity + oxygen-usage factor

Two derived chemical ratios that discriminate combustion-failure from fuelling-error
without any OBD data.

```
Chemical_Efficiency_Score = CO2 / (CO2 + CO)      # fraction of carbon fully oxidised
   healthy  -> high (near 1.0; >~0.95)
   low      -> fundamental combustion failure (pumping loss, misfire, bad timing)

Oxygen_Usage_Factor = O2 / CO   (qualitative, per Vol1)
   high O2 WITH high CO/HC  -> MISFIRE  (both reactants pass unburned)
   high CO with near-zero O2 -> pure RICH over-fuelling
```

> Vol1 names these as proposed columns; the exact denominators are stated in prose,
> not as display equations. The CO2/(CO2+CO) form is the standard combustion-efficiency
> ratio and is given here as readable-prose-derived, flagged in the formula wiki.

## Logic
A naive reader sees "high HC + high O₂" as simultaneously rich and lean. The
oxygen-usage factor resolves it: both reactants unburned = combustion never happened
= misfire, **not** a mixture error. This is the chemical basis of the misfire-vs-fuelling
pre-route gate.

## Consumer / code path
GASLab emits `chemical_efficiency` + `oxygen_usage_factor`; COMLab fault_atlas misfire
family reads them to suppress the lean/rich fuelling route on a misfire. See EP-GAS-02,
EP-COM-07.


## Core Entities

- Chemical_Efficiency_Score, Oxygen_Usage_Factor, IGNITION_MISFIRE
- GASLab resolver -> COMLab fault_atlas misfire family (PROPOSAL, EP-GAS-02)

## Graph relations (explicit)

**Chemical_Efficiency_Score** EQUALS CO2 over (CO2 plus CO)
low **Chemical_Efficiency_Score** INDICATES combustion failure
high O2 with high CO/HC INDICATES **IGNITION_MISFIRE**
**Chemical_Efficiency_Score** and **Oxygen_Usage_Factor** EMITTED_BY GASLab and CONSUMED_BY **fault_atlas misfire family**
**combustion-integrity** QUANTIFIES the misfire-vs-fuelling gate

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
