---
node_type: "wiki"
lab: "comlab"
module: "comlab"
subsystem: "fault-atlas-kg"
implements:
  - "labs/comlab/comlab/core/fault_atlas_kg.py"
  - "labs/comlab/comlab/config/kg/rich_mixture.json"
consumers:
  - "comlab: labs/comlab/comlab/core/fault_atlas_kg.py 12-family JSON loading"
  - "comlab: labs/comlab/comlab/core/fault_atlas_router.py family routing"
  - "comlab: labs/comlab/comlab/analytics/delta_engine.py collision-set -> delta motivation"
drift_guards:
  - "labs/comlab/tests/unit/test_fault_atlas_kg.py"
  - "labs/comlab/tests/unit/test_kg_schema.py"
  - "labs/comlab/tests/unit/test_kg_population.py"
tags: [comlab, finished, wiki]
source: "labs/comlab/wiki/06_fault_atlas_families.md"
---

# Fault Atlas — families, discriminators & the colliding-pair set

The taxonomy table (`COMWIKI-05`) is the per-node fingerprint. This chunk is the **family-level
reasoning**: what unifies a family, which signal separates its members, and where families
*collide* — the structural source of the top-1 ceiling.

## Family diagnostic context {#CONCEPT_FAMILIES}

**rich_mixture (7)** {#CONCEPT_FAM_RICH} — λ<0.97 / negative trim. Within-family discriminator:
*source of extra fuel*. Injector/FPR/HPFP add metered or rail fuel (RICH_MIXTURE, strong negative
trim); CTS-bias tricks the ECU into commanded enrichment (RICH with cold-bias signature); worn
seals/rings burn oil (POA_SIGNATURE, HC dominated). KG: `rich_mixture.json`.

**lean_condition (7)** {#CONCEPT_FAM_LEAN} — λ>1.03 / positive trim. Discriminator: *where the
extra air enters or fuel is lost*. Post-MAF vacuum leak vs MAF under-report vs fuel-pressure
starvation vs EGR dilution vs pre-O₂ exhaust leak (false lean). This is the **densest collision
family** — many members share `LEAN_MIXTURE` and a positive trim. KG: `lean_condition.json`.

**misfire (7)** {#CONCEPT_FAM_MISFIRE} — combustion dropout. Discriminator: *ignition vs fuelling
vs mechanical*, and *localised vs global* (the `per_cylinder_misfire_counts` localiser,
`T-COMV2-MISFIRE-LOC-1`). Spark (COP arc, gap erosion, primary winding) vs fuel (dead injector)
vs compression (low-compression mechanical). KG: `misfire.json`.

**sensor_fault (6)** {#CONCEPT_FAM_SENSOR} — the *perception ≠ truth* family. The gas reads true
while the ECU's sensor lies (lazy/fixed O₂, MAF under-read, MAP drift, CTS stuck cold, downstream
O₂ contaminated → apparent cat failure). Discriminator: the **perception-vs-truth divergence**
(`COMWIKI-03` O₂ polymorph + `perception_contradiction.py`). KG: `sensor_fault.json`.

**ecu_fault (2)** {#CONCEPT_FAM_ECU} — adaptation saturated / closed-loop disabled. The
**irreducible-floor family**: the audit's provable ~9.6 % floor is 27 `ecu_fault` STOP cases
where the signal is absent on the four single-point channels — separable only via gas↔OBD
divergence at fusion, never gas-only (`COMWIKI-08`, `COMWIKI-12`). KG: `ecu_fault.json`.

**catalyst_failure** {#CONCEPT_FAM_CATALYST} — efficiency below threshold → meltdown / flow
restriction / breakthrough / poisoning / below light-off. Discriminator: the **dual-idle catalyst
test** (idle vs 2500 RPM) separating weak/lazy from dead/poisoned (GASWIKI-07). **Δ-uninformative
for routing** — on the abstain set (`COMWIKI-11`). KG: `catalyst_failure.json`.

**exhaust_leak** {#CONCEPT_FAM_EXHAUST_LEAK} — pre-O₂ air ingress reads as false lean
(`EXHAUST_AIR_LEAK`: O₂≈20 %, λ>1.30, CO₂ normal). Discriminator vs true lean: CO₂ stays normal
and the dilution signature. KG: `exhaust_leak.json`.

**ignition_fault** {#CONCEPT_FAM_IGNITION} — coil-driver / switch voltage-drop / CKP dropout.
Bridges to `misfire` chemically; separated by the electrical signature and DTC. KG:
`ignition_fault.json`.

**mechanical_wear** {#CONCEPT_FAM_MECH_WEAR} — head gasket, rings, valve seals, bore scoring,
multi-cylinder low compression. **No distinct single-snapshot chemistry** (0/11 separable in the
audit) — POA_SIGNATURE overlaps rich_mixture; the delta and freeze-frame are the only added
levers. **On the Δ abstain set** for routing. KG: `mechanical_wear.json`.

**cam_timing** {#CONCEPT_FAM_CAM_TIMING} — chain stretch / VVT phaser stuck advanced/retarded /
sludge lag / solenoid fault. The v2.1 timing split (`CAM_TIMING_RETARDED_MAP` /
`CAM_TIMING_RETARDED_MAF` / `CAM_TIMING_ADVANCED`) addresses the **`TIMING_RETARDED` → ~7-family
slice** (~25 % of the corpus) — the largest concentrated discrimination gap; local ceiling
≈ 1/7 ≈ 14 % absent new signal (`COMWIKI-12`). KG: `cam_timing.json`. [v2: GASWIKI-06B]

**non_starter** {#CONCEPT_FAM_NONSTART} — no-spark / no-fuel / lean or rich no-start / CKP no-RPM.
Gas + OBD largely suppressed (`engine_state` routing, `COMWIKI-07`); decided from DTC Mode `$06`
+ freeze-frame cut-state (`T-COMV2-NOSTART-1`). KG: `non_starter.json`. [v2: REWORK_PLAN §8.3]

**no_fault** {#CONCEPT_FAM_NOFAULT} — `OPTIMAL_HEALTH` sentinel; the verdict when no row scores
above zero. KG: `no_fault.json`.

## The colliding-pair set {#RULE_COLLISION_SET}

The taxonomy is **not mutually exclusive** — at least four pairs collide on a single snapshot, so
a forced top-1 must mislabel a fraction no matter the tuning (`AUDIT Q10`). These are the cases
the OUTRANKED bucket (~82–90 cases, the whole game) loses on, and the reason the rework makes the
**ranked differential** the primary output (`COMWIKI-10`) and adds the **two-point delta** as the
separating signal (`COMWIKI-11`).

| Collision | Shared snapshot | What separates them | Lever |
|---|---|---|---|
| vacuum leak vs MAF under-read vs exhaust leak | LEAN_MIXTURE + positive trim | sign of ΔTrim across RPM; CO₂ on leak; speed-density null | delta + arch gate |
| worn rings vs worn valve seals | POA_SIGNATURE | Δ oil-burn behaviour across RPM step | delta |
| `TIMING_RETARDED` → ~7 families | one timing state, ~25 % of corpus | RPM-differential matrix + air-metering split | delta + cam_timing split |
| sensor_fault vs real mixture fault | same apparent λ | perception-vs-truth divergence (gas↔OBD) | contradiction-as-feature |
| ecu_fault vs real lean/rich | LEAN/RICH at trim limit | gas↔OBD divergence magnitude | ECU-FUSE consumer |

**Implication for the engine:** within a colliding family, route to the **differential** (top-k
with calibrated per-candidate confidence), not a hard top-1 verdict; flag low-support families as
anecdotal (`COMWIKI-10`, `COMWIKI-12`). A within-noise delta is **not** diagnostic and abstains
(`COMWIKI-11`).

## Graph relations (explicit)

**12 families** DEFINED_IN **comlab/config/kg/*.json** (frozen) + **COMWIKI-05 taxonomy**
**RULE_COLLISION_SET** BOUNDS **top-1 accuracy** AND MOTIVATES **CONCEPT_DIFFERENTIAL (COMWIKI-10)**
**colliding pairs** SEPARATED_BY **TEST_TWO_POINT (COMWIKI-11)** WHERE Δ is informative
**catalyst_failure, mechanical_wear, sensor_fault, ecu_fault, non_starter** ON **Δ abstain set (COMWIKI-11)**
**cam_timing split** ADDRESSES **TIMING_RETARDED slice** (~25 % corpus)

## Core Entities

- **CONCEPT_FAM_RICH** — Rich mixture diagnostic family. Consumer: `comlab/core/fault_atlas_kg.py (rich_mixture.json)`.
- **CONCEPT_FAM_LEAN** — Lean condition diagnostic family. Consumer: `comlab/core/fault_atlas_kg.py (lean_condition.json)`.
- **CONCEPT_FAM_MISFIRE** — Combustion dropout diagnostic family. Consumer: `comlab/core/fault_atlas_kg.py (misfire.json)`.
- **CONCEPT_FAM_SENSOR** — Perception vs truth sensor fault diagnostic family. Consumer: `comlab/core/fault_atlas_kg.py (sensor_fault.json)`.
- **CONCEPT_FAM_ECU** — Adaptation saturated / closed-loop disabled diagnostic family. Consumer: `comlab/core/fault_atlas_kg.py (ecu_fault.json)`.
- **CONCEPT_FAM_CATALYST** — Catalyst failure diagnostic family. Consumer: `comlab/core/fault_atlas_kg.py (catalyst_failure.json)`.
- **CONCEPT_FAM_EXHAUST_LEAK** — Pre-O₂ air ingress diagnostic family. Consumer: `comlab/core/fault_atlas_kg.py (exhaust_leak.json)`.
- **CONCEPT_FAM_IGNITION** — Electrical coil/CKP fault diagnostic family. Consumer: `comlab/core/fault_atlas_kg.py (ignition_fault.json)`.
- **CONCEPT_FAM_MECH_WEAR** — Mechanical wear / low compression diagnostic family. Consumer: `comlab/core/fault_atlas_kg.py (mechanical_wear.json)`.
- **CONCEPT_FAM_CAM_TIMING** — Timing chain stretch / phaser diagnostic family. Consumer: `comlab/core/fault_atlas_kg.py (cam_timing.json)`.
- **CONCEPT_FAM_NONSTART** — No-spark / no-fuel non-starter diagnostic family. Consumer: `comlab/core/fault_atlas_kg.py (non_starter.json)`.
- **CONCEPT_FAM_NOFAULT** — Optimal health sentinel diagnostic family. Consumer: `comlab/core/fault_atlas_kg.py (no_fault.json)`.
- **RULE_COLLISION_SET** — Colliding fault pairs sharing the same single-point signatures. Consumer: `comlab/core/fault_atlas_router.py and comlab/analytics/delta_engine.py (motivates delta / differential)`.
