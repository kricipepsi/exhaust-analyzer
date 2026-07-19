# OBDLab Drift Inventory — 2026-05-25

**Audit:** T-DOC-6 — derived docs vs `OBDLab_KG_Wiki.md` vs `OBDLab/code/obdlab/` live code
**Method:** Pass 1 (derived-doc-driven) + Pass 2 (vocab-walk)
**Date:** 2026-05-25

## Summary

| Classification | Row count |
|---|---|
| ALIGNED (not in table) | ~122 claims across PRD (11), HLD (24), DLD (40), LLD (47) |
| WIKI-STALE | 13 |
| DOC-STALE | 2 |
| CODE-DRIFT | 0 |
| 3-WAY | 0 |
| **Total non-aligned** | **15** |

Pass 1 (derived-doc-driven): 12 rows | Pass 2 (vocab-walk): 3 rows

## Inventory

| # | claim_source | claim_text | wiki_says | code_says | classification | proposed_owner |
|---|---|---|---|---|---|---|
| 1 | LLD_OBDLab.md §2:33-36 | `shrtft1/longft1/shrtft2/longft2` bounds `min: -100.0, max: 99.22` | `OBDLab_KG_Wiki.md §3.1:110-113` — `−100.0 / +99.22` | `physical_sensor_bounds.json:30-33` — `min: -127.0, max: 127.0`; `payload.py:48-59` — `Field(ge=-127, le=127)` | WIKI-STALE | T-DOC-N (wiki update §3.1 + §4) |
| 2 | PRD_OBDLab.md §6:59 | `ve_state_isValid` (bool field in OBDLivePayload) | `OBDLab_KG_Wiki.md §5:191` — internal field `ve_state_isValid`; `§9:369` — `ve_state_isValid = false` | `payload.py:74` — `ve_validity: VEValidity` (StrEnum, not bool) | WIKI-STALE | T-DOC-N (wiki update §5, §9, §10) |
| 3 | PRD_OBDLab.md §7:78 | OBDLivePayload "17 fields" | `OBDLab_KG_Wiki.md §5:168-185` — schema shows 14 fields (also stale, missing T-OBD-WIRE-1 additions) | `payload.py` — 21 fields (15 original + `total_trim_correction_delta_b2` + 6 analytics from T-OBD-WIRE-1) | DOC-STALE | T-DOC-N (wiki + PRD/HLD/DLD field count update) |
| 4 | HLD_OBDLab.md §4:110-112 | VE formula: `[MAF × R(8.314) × IAT_K] / [MAP × (RPM/60) × (Disp_L/2) × MM_AIR(28.97)]` (R in numerator, MM in denominator) | `OBDLab_KG_Wiki.md §10.1:389-392` — `[MAF × 28.97 × (IAT+273.15)] / [MAP × (RPM/60) × (Disp/2) × 8.314]` (MM in numerator, R in denominator — **transposed**); `§10.4:447` — same transposition in YAML block | `ve_engine.py:202-204` — `numerator = maf * R_GAS * iat_k`, `denominator = ... * MM_AIR` (matches HLD/LLD) | WIKI-STALE | T-DOC-N (wiki §10.1 + §10.4 YAML correction) |
| 5 | DLD_OBDLab.md §2:43 | `O2NormalizationMode` enum has 4 members including `O2_CHANNEL_FAULT` | `OBDLab_KG_Wiki.md §6.3:225-230` — lists only 3 members (`NARROWBAND_VOLTAGE_TO_LAMBDA`, `WIDEBAND_PASSTHROUGH`, `WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA`); `O2_CHANNEL_FAULT` not in enum declaration | `vocabulary.py:41` — `O2_CHANNEL_FAULT = "O2_CHANNEL_FAULT"` (4th member) | WIKI-STALE | T-DOC-N (wiki §6.3 add O2_CHANNEL_FAULT) |
| 6 | DLD_OBDLab.md §2:48 | `O2FailureMode` enum has 6 members (STUCK_LEAN through HEATER_FAULT) | `OBDLab_KG_Wiki.md §6.7:274-282` — lists 6 members, no `NO_FAULT` | `vocabulary.py:95` — `NO_FAULT = "NO_FAULT"` (7th member, healthy baseline) | WIKI-STALE | T-DOC-N (wiki §6.7 add NO_FAULT) |
| 7 | LLD_OBDLab.md §7:126 | `ve_pct > 90.0` triggers `FAULT_VE_SENSOR_SKEW` | `OBDLab_KG_Wiki.md §6.4:242` — `VE > 85% at idle on NA engine`; `§10.3:430` — `> 85% on NA engine → FAULT_VE_SENSOR_SKEW` | `ve_engine.py:49` — `_CUTOFF_VE_SKEW = 90.0`; `ve_engine.py:263` — `ve_pct > _CUTOFF_VE_SKEW` | WIKI-STALE | T-DOC-N (wiki §6.4 + §10.3: 85% → 90%) |
| 8 | DLD_OBDLab.md §7:189 | `FAULT_MAF_CONTAMINATION` triggers on `STRESS_IDLE` only | `OBDLab_KG_Wiki.md §6.4:241` — `VE < 65% at STRESS_IDLE + positive TFT`; `§10.3:430` — `STRESS_IDLE: < 65% AND TFT > +15%` | `ve_engine.py:250-253` — checks both `STRESS_IDLE` **and** `REGULATORY_HIGH_IDLE` | WIKI-STALE | T-DOC-N (wiki §6.4 + §10.3: add REGULATORY_HIGH_IDLE) |
| 9 | DLD_OBDLab.md §7:178-183 | `TARGET_VE` table has 4 entries (STABILIZED_IDLE + STRESS_IDLE only, no REGULATORY_HIGH_IDLE) | `OBDLab_KG_Wiki.md` — does not list TARGET_VE constants explicitly; §10.3 table mentions only STABILIZED_IDLE and STRESS_IDLE | `ve_engine.py:33-42` — 6 entries including `REGULATORY_HIGH_IDLE` for both MAP_ONLY (0.80) and MAF_ONLY (0.82) | WIKI-STALE | T-DOC-N (DLD §7 + wiki §10.3: add REGULATORY_HIGH_IDLE rows) |
| 10 | LLD_OBDLab.md §8:143-144 | `RICH_V_MIN = 0.51` — rich lambda at 0.51–0.90 V | `OBDLab_KG_Wiki.md §11.1:465-469` — 5-zone mapping: `0.51–0.59 V → STOICH_RICH_SIDE (λ=1.00)`, `0.60–0.90 V → RICH_STATE (λ≈0.95)` | `o2_normalizer.py:23` — `_ZONE_STOICH_BOUNDARY = 0.50`; rich zone starts at `>0.50` (i.e. 0.51+) → λ=0.95 | WIKI-STALE | T-DOC-N (wiki §11.1: collapse 5-zone to 3-zone to match code) |
| 11 | PRD_OBDLab.md §8:93 | `O2_CHANNEL_FAULT` is "a code-only sentinel, exempt from wiki drift guard" | `OBDLab_KG_Wiki.md §6.3` — still does not list `O2_CHANNEL_FAULT` (only 3 modes) | `vocabulary.py:41` — `O2_CHANNEL_FAULT` is a formal 4th enum member in `O2NormalizationMode` | DOC-STALE | T-DOC-N (PRD §8: remove sentinel exemption; O2_CHANNEL_FAULT is a proper enum value) |
| 12 | vocab-walk: OBDLab_KG_Wiki.md §8.1:326 vs §8.2:349 | STRESS_IDLE load range `40–60%` (§8.1 table) vs `[10.0, 60.0]` (§8.2 YAML) | `OBDLab_KG_Wiki.md §8.1:326` — `STRESS_IDLE ... Load: 40–60%`; `§8.2:349` — `value: [10.0, 60.0]` | `obd_translation_rules.yaml:39` — `value: [10.0, 60.0]` (matches wiki §8.2) | WIKI-STALE | T-DOC-N (wiki §8.1: correct STRESS_IDLE load to 10–60%) |
| 13 | vocab-walk: OBDLab_KG_Wiki.md domain-ref:621-628 vs §9:375 | O2 DTC families: `P0130–P0137` B1S1, `P0138–P0145` B1S2, `P0150–P0167` B2S1/B2S2 (34 codes) | `OBDLab_KG_Wiki.md §9:375` — `No active P0130–P0161` (32 codes) | `analytics_preconditions.py:18-26` — `O2_FAULT_DTCS` frozenset with P0130–P0161 (32 codes, matches wiki §9) | WIKI-STALE | T-DOC-N (wiki domain ref DTC table: reconcile with §9/code P0130–P0161 range) |
| 14 | vocab-walk: OBDLab_KG_Wiki.md §12.1:529 vs §3.1:110-113 | Trim sentinel `±127%` register saturation (§12.1) vs bounds `−100.0 / +99.22` (§3.1) | `OBDLab_KG_Wiki.md §12.1:529` — `±127%: register saturation`; `§3.1:110-113` — `−100.0 / +99.22` | `physical_sensor_bounds.json:30` — `min: -127.0, max: 127.0`; `semantic_consistency_checker.py:18-19` — `_TRIM_MIN = -127.0, _TRIM_MAX = 127.0` | WIKI-STALE | T-DOC-N (wiki §3.1 + §4: update trim bounds to ±127 to match code and wiki §12.1) |
| 15 | vocab-walk: OBDLab_KG_Wiki.md §5:168-185 | Wiki §5 JSON schema missing 6 T-OBD-WIRE-1 analytics fields (`ve_pct`, `ve_validity`, `trim_analytics_gate`, `maf_status`, `map_status`, `o2_failure_mode`) | `OBDLab_KG_Wiki.md §5:168-185` — JSON block shows 14 fields; `§10:396` — references old `ve_state_isValid` | `payload.py:70-88` — includes all 6 analytics fields from T-OBD-WIRE-1 | WIKI-STALE | T-DOC-N (wiki §5: add 6 analytics fields; rename ve_state_isValid → ve_validity) |

### Sanity check rows

Rows 1 and 2 are the pre-known drifts that must classify as `WIKI-STALE`:

- **Row 1** (trim bounds `-100/+99.22` → `-127/+127`): `WIKI-STALE` — confirmed.
- **Row 2** (`ve_state_isValid` → `ve_validity`): `WIKI-STALE` — confirmed.

### Drift classification guide

| Label | Meaning |
|---|---|
| `WIKI-STALE` | Wiki and derived docs agree; code disagrees. Root cause: code change never propagated to wiki. |
| `DOC-STALE` | Derived doc(s) disagree with both wiki and code. Root cause: doc update missed. |
| `CODE-DRIFT` | Code disagrees with both wiki and derived docs. Root cause: unplanned code change (rare — flag for architect). |
| `3-WAY` | All three sources disagree with each other. |
