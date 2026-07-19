---
node_type: "wiki"
lab: "dtclab"
module: "dtclab"
subsystem: "gas-perception-link"
implements:
  - "labs/dtclab/dtclab/schemas/vocabulary.py"
consumers:
  - "comlab: labs/comlab/comlab/core/perception_contradiction.py POA_HISTORY / perception gap evaluation"
drift_guards:
  - "labs/dtclab/tests/unit/test_vocabulary.py"
tags: [dtclab, finished, wiki]
source: "labs/dtclab/wiki/09_gas_reverse_lookup.md"
---
# 09 — Gas-signature reverse-lookup & perception gaps

**Reverse-lookup reference only.** DTCLab is blind to gas chemistry per the
data-isolation invariant (`00_INDEX.md §0`). The tokens in this chunk
(`POA_HISTORY`, `chemical_state`, `lambda_chem`, perception flags) are **injected
by COMLab** (`fault_atlas_router.py`) from GASLab output — DTCLab does not import,
compute, or transmit them. This chunk is recorded here so the DTCLab task pack
stays aware of what its routing tags feed into. Sources: `cases/casesDTC.md`,
`cases/Gas Lab DTC Code Matching (1).md`, `master_perception_guide.md`.

---

## 9.1 Lean signatures

| Gas signature | Lambda | Probable DTCs | Routing tags |
|---|---|---|---|
| CO low (< 0.3%), O₂ high (> 1.5%), HC normal | > 1.03 | P0171, P0174 | `LEAN_HISTORY` |
| CO low, O₂ high, HC elevated | > 1.05 | P0171 + P0300 | `LEAN_HISTORY`, `MISFIRE_HISTORY` |
| CO normal, O₂ moderate, MAF under-reading | > 1.02 | P0100 – P0104 | `LEAN_HISTORY` |

## 9.2 Rich signatures

| Gas signature | Lambda | Probable DTCs | Routing tags |
|---|---|---|---|
| CO high (> 1.5%), HC elevated, O₂ ≈ 0 | < 0.95 | P0172, P0175 | `RICH_HISTORY` |
| CO very high (> 3%), CO₂ dropping | < 0.90 | P0172 + injector fault | `RICH_HISTORY`, `INJECTOR_HISTORY` |
| CO high, STFT pegged negative | < 0.92 | P0172 + EVAP purge stuck open | `RICH_HISTORY`, `EVAP_HISTORY` |

## 9.3 Misfire signatures

| Gas signature | Lambda | Probable DTCs | Routing tags |
|---|---|---|---|
| HC very high (> 500 ppm), CO elevated, O₂ elevated | ≈ 1.00 | P0300 – P0312 | `MISFIRE_HISTORY` |
| O₂ rise ≈ 21%/N cylinders | variable | P0301 – P030x | `MISFIRE_HISTORY` |
| HC high, CO low, λ ≈ 1.00 | ≈ 1.00 | **No direct DTC; POA signature** | `POA_HISTORY` |

**Misfire O₂ math:** one dead cylinder on an N-cylinder engine → O₂ rise ≈ 21% ÷
N. Example: one dead cylinder on a 4-cyl engine → O₂ ≈ 5.25%.

**POA discriminator:** high HC, low CO, near-stoichiometric λ is the oil-aerosol
burning signature (POA = primary organic aerosol; oil HC reads with a reduced
NDIR response factor). The engine combusts oil but the catalyst handles the CO.
No direct DTC until plugs foul (→ P0300) or catalyst is poisoned (→ P0420); oil
level may set P250C. `POA_HISTORY` is emitted by COMLab (not DTCLab) only when
GASLab reports `chemical_state == "POA_SIGNATURE"` (T-FX-3).

## 9.4 Catalyst and EGR signatures

| Gas signature | Lambda | Probable DTCs | Routing tags |
|---|---|---|---|
| CO₂ low (< 13%), CO + HC elevated post-cat | variable | P0420, P0430 | `CATALYST_HISTORY` |
| Post-cat O₂ switching at pre-cat frequency | ≈ 1.00 | P0420 (OSC exhausted) | `CATALYST_HISTORY` |
| CO₂ low, O₂ high at idle only — normalises at 2500 RPM | variable | P0401 | `EGR_HISTORY` |

## 9.5 Stoichiometric reference (healthy engine)

| Gas | Idle | Post-cat (healthy) |
|---|---|---|
| CO | < 0.5% | < 0.1% |
| HC | < 35 ppm | < 35 ppm |
| O₂ | 0.0 – 0.5% | < 0.5% |
| CO₂ | 14.5 – 16% | 14.5 – 16% (slight rise) |
| NOₓ | < 100 ppm | < 100 ppm |
| λ | 0.995 – 1.005 | 0.995 – 1.005 |

---

## 9.6 Perception-gap rules

A **perception gap** is a disagreement between the ECU's internal mixture model
(O₂ feedback + fuel trims) and the exhaust chemistry measured by the gas analyser
(ground truth). These gaps expose sensor faults, exhaust intrusions, or ECU logic
inversions.

**Ownership note:** DTCLab supplies the freeze-frame STFT/LTFT and the routing
tags; GASLab supplies `lambda_chem` and `chemical_state`; the gap classification
is COMLab's. Recorded here so the DTCLab task pack stays aware of what its outputs
feed into.

### 9.6.1 Vocabulary

| Term | Definition |
|---|---|
| `perception_lean_seen_rich` | ECU lean (LTFT+, lean DTC) AND gas λ < 0.905 |
| `perception_rich_seen_lean` | ECU rich (LTFT−, rich DTC) AND gas λ > 1.095 |
| `expected_perception_gap` | Cases-corpus flag that this contradiction is expected |
| `perception_contradiction` | Generic flag for `|obd_lambda − gas_lambda| ≥ 0.08` |

The 0.905 / 1.095 boundaries are the lambda equivalents of ±10% deviation. Inside
the window, drift and analyser tolerance can explain the delta. Outside, it
cannot.

### 9.6.2 Four gap mechanisms

| Mechanism | How it creates the gap | DTC pattern |
|---|---|---|
| Exhaust air leak | Atmospheric O₂ enters pre-cat; sensor reads lean; ECU adds fuel; trims positive — but exhaust is actually rich | P0171 with rich exhaust |
| O₂ contamination (silicone, phosphorus) | Sensor biased low; always reads lean; ECU adds fuel; exhaust richens | P0171 with worsening rich chemistry |
| MAF under-reporting | ECU enriches less than needed; trims positive but lean exhaust | P0171 with anomalous MAF |
| Misfire O₂ misinterpretation | Unburned O₂ from misfire reaches sensor; reads lean; trims+; combustion failure not lean | P0171 + P030x; HC very high |

**"False lean" worked illustration** (`DtcDoc2.md` EXP-N004): a pre-O₂ exhaust
manifold crack draws ambient air in during pressure pulses → sensor reads lean →
trims drive positive → engine physically rich (high CO) while the ECU still logs
P0171. The discriminator vs true lean: in true lean CO stays near zero; in
false-lean-from-leak CO is elevated by the PCM's reactive enrichment.

## Graph relations (explicit)

**chemical_state** == "POA_SIGNATURE" INJECTS **DTCRoutingTag.POA_HISTORY**
**DTCRoutingTag.POA_HISTORY** MAPS_TO **None** family
**DTCRoutingTag.POA_HISTORY** GATED_BY **None** (chemistry-driven)
**perception_lean_seen_rich** DEFINED_AS **ECU lean** AND **lambda_chem < 0.905**
**perception_rich_seen_lean** DEFINED_AS **ECU rich** AND **lambda_chem > 1.095**
**perception_contradiction** DEFINED_AS **|obd_lambda − gas_lambda| >= 0.08**
**expected_perception_gap** CARRIED_AS **context only**
**Exhaust air leak** PRODUCES **perception_lean_seen_rich**
**O₂ contamination** PRODUCES **perception_lean_seen_rich**
**MAF under-reporting** PRODUCES **perception_lean_seen_rich**
**Misfire O₂ misinterpretation** PRODUCES **perception_lean_seen_rich**

## Core Entities

- **DTCRoutingTag.POA_HISTORY** — Routing tag injected when primary organic aerosol (oil-burning) signature is detected. Consumer: `dtclab/schemas/vocabulary.py`, COMLab.
- **perception_lean_seen_rich** — Gap classification flag indicating ECU reports lean while chemistry is rich. Consumer: COMLab perception-gap evaluator.
- **perception_rich_seen_lean** — Gap classification flag indicating ECU reports rich while chemistry is lean. Consumer: COMLab perception-gap evaluator.

