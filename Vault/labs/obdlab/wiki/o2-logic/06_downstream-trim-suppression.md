---
chunk: o2-logic/06_downstream-trim-suppression
topic: o2-logic
sources:
  - O2logic.md §Scenario-3 step 3 (rear-trim fault suppression)
  - master_o2_sensor_guide.md §4 (post-cat sensor does not drive fuel control)
consumer: composition.py writes downstream_trim_role + trim_analytics_gate to OBDLivePayload; COMLab fault_atlas_router suppresses post-cat trim verdicts (P2096/P2099) when downstream_trim_role = CATALYST_MONITOR_ONLY
consumer_status: active
reconciliation: source asserts `trim_analytics_gate = SUPPRESS_POST_CAT_TRIM` — that value does NOT exist in TrimAnalyticsGate. Suppression is carried by downstream_trim_role, not the gate. See README §reconciliation / O2-FU-2.
related: [[02_upstream-vs-downstream-roles]]
---

# Downstream trim suppression

On a platform whose rear sensor is monitor-only, COMLab must **not** raise
post-cat fuel-trim faults (P2096 "post-cat fuel trim system too lean" / P2099
"too rich") — there is no rear trim loop to be out of range. This keeps any
P0171/P0172 trim verdict isolated to the upstream control loop.

## How the suppression is actually expressed

The carrier is `DownstreamTrimRole` (see `02_upstream-vs-downstream-roles`),
written to the `OBDLivePayload` by `composition.py`:

- `CATALYST_MONITOR_ONLY` → COMLab `fault_atlas_router` **bypasses** all
  post-cat trim calculations; P2096/P2099 are not eligible to fire.
- `SECONDARY_FUEL_TRIM` → post-cat trim analytics run normally; P2096/P2099 are
  eligible.
- `NONE` → no rear sensor / role unassigned; nothing to suppress.

DNALab/VINLab supplies the role from the vehicle's emissions profile; OBDLab
mirrors it on the typed JSON boundary (no cross-lab import).

## Reconciliation — `SUPPRESS_POST_CAT_TRIM` is not a gate value

`O2logic.md §Scenario-3` instructs writing
`trim_analytics_gate = SUPPRESS_POST_CAT_TRIM`. **No such value exists** in the
shipped `TrimAnalyticsGate` enum, whose members are: `VALID`, `ENGINE_COLD`,
`OPEN_LOOP`, `O2_FAULT_ACTIVE`, `CKP_CMP_FAULT_ACTIVE`,
`CODES_RECENTLY_CLEARED`, `WOT_ACTIVE`, `DFCO_ACTIVE`, `SEMANTIC_ERROR`
(OBDLab_KG_Wiki §6.5). The gate governs whether *all* trim analytics run for a
sample (cold / open-loop / active O₂ fault / etc.); it is **not** the mechanism
for routing-out post-cat trim. That routing is the `downstream_trim_role`
field above. The source's gate value is therefore a draft artefact, not a
shippable enum — flagged O2-FU-2 (reconcile SWEEP_MANIFEST §11, which repeats
the `SUPPRESS_POST_CAT_TRIM` claim).

> Distinct but adjacent: when an *upstream* O₂ DTC (P0130–P0161) is active, the
> gate value `O2_FAULT_ACTIVE` suppresses **trim verdicts in general** — see
> `07_o2-dtc-families`. That is a real gate value; `SUPPRESS_POST_CAT_TRIM` is
> not.

Citation: post-cat-doesn't-drive-trim rule master_o2_sensor_guide.md §4;
role-based suppression O2logic.md §Scenario-3 step 3; enum members
labs/obdlab/obdlab/schemas/vocabulary.py (`TrimAnalyticsGate`,
`DownstreamTrimRole`).


## Core Entities

- DownstreamTrimRole.CATALYST_MONITOR_ONLY, DownstreamTrimRole.SECONDARY_FUEL_TRIM, DownstreamTrimRole.NONE
- P2096, P2099, TrimAnalyticsGate.O2_FAULT_ACTIVE
- composition.py downstream_trim_role -> COMLab fault_atlas_router (consumer, active)

## Graph relations (explicit)

**DownstreamTrimRole.CATALYST_MONITOR_ONLY** SUPPRESSES **P2096** and **P2099**
**DownstreamTrimRole.SECONDARY_FUEL_TRIM** ENABLES **P2096** and **P2099** eligibility
post-cat suppression CARRIED_BY **DownstreamTrimRole**, not by the gate
**SUPPRESS_POST_CAT_TRIM** IS_NOT a **TrimAnalyticsGate** value (doc bug O2-FU-2)
**TrimAnalyticsGate.O2_FAULT_ACTIVE** SUPPRESSES trim verdicts when P0130-P0161 active

_Note: relations and Core Entities added 2026-06-08 for graphify pass-3 (T-KG-OBD-1); upgrades implied links from INFERRED to EXTRACTED. No sourced prose, numerics, or citations altered._
