---
chunk: o2-logic/08_wideband-pumping-current-logic
topic: o2-logic
sources:
  - various/Vol2.md — Master Document 2 (Lambda and Wideband Sensor Protocols)
consumer: OBDLab o2_normalizer — wideband (UEGO) current→λ translation; the sign of the pumping current Ip distinguishes rich/lean and sensor drift from real mixture error. Feeds normalized_obd_lambda → COMLab.
consumer_status: active (extends o2_normalizer wideband path, o2-logic/04) + PROPOSAL for Ip-sign drift flag
provenance: sources/various/Vol2.md MD2 — dual-cell concept + Ip sign READABLE; some mA/voltage spec cells stripped
dedup: top-up to o2-logic/01 (NB/WB physics) and /04 (λ translation); adds the pumping-current mechanism explicitly
---

# Wideband pumping-current logic (UEGO)

A wideband/A-F sensor is a dual-cell device: a Nernst sensing cell held at a constant
reference by varying the current to a pumping cell. That **pumping current (Ip)** — not
a voltage — is the diagnostic parameter.

```
Ip sign convention:
  Ip > 0 (positive)  -> LEAN  (O2 pumped OUT of the sensing chamber)
  Ip = 0             -> stoichiometric (λ = 1.000, no transfer)
  Ip < 0 (negative)  -> RICH  (O2 pumped IN to balance excess fuel)
```

## Logic / why it matters
Narrowband can only say richer/leaner-than-stoich (binary switch); wideband quantifies
λ across ≈0.7–1.3 via Ip. A drifted reference-current circuit (Vol1 N-015, N-028)
keeps the loop internally consistent but externally wrong — the ECU sees λ=1.00 while
the engine runs lean. That is the WIDEBAND_OFFSET case: detectable only by cross-checking
Ip-derived λ against λ_chem.

## Consumer / code path
OBDLab `o2_normalizer.py` maps Ip→`normalized_obd_lambda` on WIDEBAND_LINEAR sensors;
a persistent |λ−1.0|>0.05 with healthy Ip slope raises the WIDEBAND_OFFSET candidate
(o2-logic reconciliation, O2-FU-1 / EP-OBD-17). COMLab confirms vs λ_chem.


## Core Entities

- Ip, WIDEBAND_LINEAR, normalized_obd_lambda, WIDEBAND_OFFSET_CANDIDATE
- o2_normalizer.py wideband path -> COMLab (consumer, active; Ip-drift flag PROPOSAL O2-FU-1)

## Graph relations (explicit)

**Ip** positive INDICATES lean
**Ip** negative INDICATES rich
**Ip** zero INDICATES stoich (lambda 1.000)
**o2_normalizer.py** MAPS **Ip** to **normalized_obd_lambda** on **WIDEBAND_LINEAR**
persistent abs(lambda minus 1.0) above 0.05 with healthy Ip slope RAISES **WIDEBAND_OFFSET_CANDIDATE**

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
