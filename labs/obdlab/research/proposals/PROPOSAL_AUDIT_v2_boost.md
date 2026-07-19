# OBDLab proposal audit — v2-boost triage

**Author:** architect (4DLab) · **Date:** 2026-06-08 · **Scope:** OBDLab proposals only
(`EP-OBD-10…19` + `EP-OBD-IN-01…10`, 20 files in `extracted/`). Cross-lab proposals
(COM/ECU/FA/GAS/CAT/DTC/DNA/ARCH) are **out of scope** this pass.

**Question answered:** which proposals genuinely advance v2 over v1 (new diagnostic
capability with a nameable consumer), which are *already realised* in v2 code/tasks, and
which need owner research before they can be specced.

**Method:** each proposal cross-checked against the live OBDLab surface
(`obdlab/obdlab/{schemas,core}`), the COMLab consumer surface, and the in-flight
`T-OBDV2-2…5` pack. "Absorbed" = the producing code or its registered consumer already
exists; "boost" judged on diagnostic lift × consumer-nameability × input-model feasibility.

---

## Verdict table

| ID | Proposal | v2 lift | Disposition | Consumer status |
|---|---|---|---|---|
| EP-OBD-10 | VE engine math + validity classifier | — | **Absorbed** | `ve_engine.py` live; reader `T-COMV2-VE-GATE-1` registered (T-OBDV2-2) |
| EP-OBD-11 | Speed-density W_theo / sensor-error-delta MAF crosscheck | High | **Promote — research-gated** | threshold unquantified (RQ-C); reader = `fault_atlas` MAF-contam |
| EP-OBD-12 | LTFT adaptive cell-matrix (RPM×Load cells) | High | **Promote** | reader = COMLab `EP-COM-09` cell-vector analyzer (pairs) |
| EP-OBD-13 | Asymmetric bank-trim audit | — | **Absorbed** | `per_bank_trim_delta` + `T-COMV2-BANK-FUSE-1` (note ≥20 % hard-fault tier below) |
| EP-OBD-14 | Semantic-consistency physics gates | — | **Absorbed (OBD half)** | `semantic_consistency_checker.py` gates 1–4 + thermal/closed-loop live; gas-dependent ADC/cat gates are COMLab |
| EP-OBD-15 | Broad physical-sensor-bounds config | — | **Absorbed** | `pid_ingestion_validator.py` config-driven; ±127 rails live |
| EP-OBD-16 | State-translation RPM bands | — | **Absorbed except band conflict** | buckets live; **STRESS_IDLE band unresolved (RQ-A)** |
| EP-OBD-17 | WIDEBAND_OFFSET two-stage O₂ mode | — | **Absorbed (authored)** | `T-OBDV2-4` + `T-COMV2-O2OFFSET-1` |
| EP-OBD-18 | MAF/MAP/TPS rationality + inferred-BARO (P0068) | High | **Promote — research-gated** | P0068 route named in `T-COMV2-VE-GATE-1`; needs BARO + formula (RQ-B) |
| EP-OBD-19 | MAP cranking mechanical test | Med | **Defer — input-model scope** | needs cranking-capture (RQ-E) |
| EP-OBD-IN-01 | Calculated Load PID (0x04) | Low | **Mostly absorbed** | field live; reader folds into load-cell categoriser |
| EP-OBD-IN-02 | Absolute Load PID (0x43) | Med | **Promote (low priority)** | VE cross-ref reader; field gap |
| EP-OBD-IN-03 | Fuel System Status (0x03) | Med | **Promote (partial)** | internal `OPEN_LOOP` gate already reads `fuel_sys_status`; promote the **COMLab-facing raw field + Δ-signature** |
| EP-OBD-IN-04 | Control Module Voltage (0x42) | Med | **Promote** | electrical pre-check in `perception_contradiction`; pairs `EP-FA-05` |
| EP-OBD-IN-05 | Throttle Position (0x11/0x45) | High | **Promote** | field gap; readers = idle-leak validator + ECU checker (ECU-PERCEPT deferred TPS here) |
| EP-OBD-IN-06 | Barometric Pressure (0x33) | Med | **Promote-with-18** | enabler for EP-OBD-18/11 |
| EP-OBD-IN-07 | Per-cylinder misfire counts (Mode 06) | High | **Promote — research-gated** | availability + OBD-vs-DTC ownership (RQ-D) |
| EP-OBD-IN-08 | Intake Air Temp (IAT) | High | **Promote (top pick)** | **VE engine already consumes `intake_air_temp_c`**; only the field + ECU-checker reader missing |
| EP-OBD-IN-09 | GDI rail-pressure PIDs | Med | **Defer — scope** | GDI-fleet ruling needed (RQ-E/F) |
| EP-OBD-IN-10 | Secondary-ignition waveform | Med | **Defer — no live stream** | manual-entry; consumer unspecced (RQ-E) |

---

## The v2-boost shortlist (what to actually pick)

**Tier 1 — promote now, cheap and high-lift (no research blocker).** These have a named,
feasible consumer and clear diagnostic gain:

1. **EP-OBD-IN-08 (IAT)** — *top pick.* The VE/airflow math in `ve_engine.py` already reads
   `intake_air_temp_c`; today it arrives as an untyped raw input. Formalising it as a payload
   field + adding the ECU ground-trace consumer (IAT/ECT/TPS = −40 °C/−40 °C/100 % digital-lie
   signature) closes a real gap at near-zero cost. Pairs with EP-OBD-IN-05.
2. **EP-OBD-IN-05 (TPS)** — the ECU-PERCEPT task explicitly *deferred* TPS to "the ECU checker
   that names it." Two named readers (idle-air-leak P0505 validator + ECU ground-trace tell).
   Promote together with IN-08 as the **ECU-hardware checker input pair**.
3. **EP-OBD-IN-03 (FUELSYS raw field)** — the *internal* open-loop gate is already live
   (`analytics_preconditions` → `TrimAnalyticsGate.OPEN_LOOP`). The boost is exposing the **raw
   `fuel_system_status`** to COMLab + the CL→OL_Fault-across-RPM Δ-signature. Small, solid.
4. **EP-OBD-IN-04 (VPWR)** — electrical-health pre-check that stops the engine blaming air/fuel
   sensors when the rail is out of band. Defensive, modest, consumer-clear.
5. **EP-OBD-12 (LTFT cell matrix)** — strongest *localisation* lift (vacuum-leak isolation by
   load cell that scalar total-trim can't do). Promote paired with its COMLab reader EP-COM-09.

**Tier 2 — promote, but research-gated (need an owner answer first):**

6. **EP-OBD-18 (rationality + inferred-BARO)** + **EP-OBD-IN-06 (BARO)** — catches the
   DTC-silent drifted MAF ("one liar caught by the other two"). Blocked on RQ-B (BARO-inference
   formula + drift threshold).
7. **EP-OBD-11 (W_theo crosscheck)** — non-linear MAF drift across two idle points. Blocked on
   RQ-C (the ΔSensor_error threshold is unquantified). Overlaps EP-OBD-18 — pick one primary.
8. **EP-OBD-IN-07 (per-cylinder misfire)** — high lift (misfire localiser + catalyst-meltdown
   guard) but blocked on RQ-D (fleet availability + OBDLab-vs-DTCLab ownership, overlaps the
   Mode-06 work in `T-OBDV2-5`).

**Defer (not a merit judgement — the input model can't feed a consumer yet):**

- **EP-OBD-19** (cranking mechanical test), **EP-OBD-IN-09** (GDI rail pressure),
  **EP-OBD-IN-10** (secondary-ignition waveform). All three depend on capture the product may
  not collect (RQ-E/F). Hold until the input-model scope is ruled.

**Already realised (no action — fold the residual consumer naming into existing tasks):**
EP-OBD-10, -13, -14, -15, -16, -17, -IN-01.

> **One discrepancy to log, not act on:** EP-OBD-13 cites a **≥20 %** B1–B2 hard-fault
> threshold; `T-COMV2-BANK-FUSE-1` carries the **±5 %** bank-*match* bound from audit Q2. These
> are not in conflict (±5 % = asymmetry flag; ≥20 % = confirmed bank-hardware fault) — they're
> two tiers of the same ladder. The Stage-4 bank consumer should carry **both**. Noted for that
> task; no change here.

---

## Research questions for the owner

Answering these unblocks Tier-2 promotion and the deferred set. Each is scoped to a single
decision; numeric bounds may be image-stripped in the Vol exports (see
`formula-wiki/PENDING_STRIPPED_FORMULAS.md`).

**RQ-A — STRESS_IDLE canonical RPM band (blocks EP-OBD-16 close + the whole Δ-idle method; also closes O2-FU-3).**
The sources disagree: `FuelTrimW.md` 3500–4500, `O2logic.md` 2500, fuel-trim chunk 04
2500–3000, shipped `RpmStateBucket.STRESS_IDLE` 3000–4500. Is the stress-idle band **one fixed
range**, **per-signal** (one for O₂ switching, another for trim/gas), or **VIN/era-derived**
(`stress_idle_rpm_target` already on the DNA view)? Give the canonical pair (or the per-signal
set) with a source.

**RQ-B — inferred-BARO + rationality thresholds (blocks EP-OBD-18 + EP-OBD-IN-06).**
What is the inferred-BARO-at-WOT formula (from MAF+MAP at hard WOT), and what **delta vs local
actual BARO** flags a MAF out of calibration? Separately, what MAF↔MAP↔TPS **disagreement
magnitude** trips the P0068-equivalent rationality verdict? (Source: Vol2 MD4 / pids-protocol/02
— confirm the numerics survived export.)

**RQ-C — MAF-linearity ΔSensor_error threshold (blocks EP-OBD-11).**
`ΔSensor_error = |Sensor_2500 − W_theo_2500| − |Sensor_750 − W_theo_750|`. What numeric
magnitude separates "linear/healthy" (≈0) from "calibration drift (dirty hot-wire)"? Needed to
make the crosscheck routable rather than advisory.

**RQ-D — per-cylinder misfire availability + ownership (blocks EP-OBD-IN-07).**
On the 1990–2010 petrol fleet, how widely are **per-cylinder Mode-06 misfire counts**
(200/1000-rev) actually retrievable (CAN-era 2008+ only, like the Mode-06 no-start branch in
`T-OBDV2-5`?), and should the counts be ingested in **OBDLab** or produced by **DTCLab**
(overlap with EP-DTC-04)? A one-line ownership ruling + an availability bound.

**RQ-E — product input-model scope (blocks EP-OBD-19, EP-OBD-IN-09, EP-OBD-IN-10).**
Does 4DApp's capture layer (wizard / L1–L5 input model) collect — or plan to — any of:
(a) **cranking-vacuum / relative-compression** data (clear-flood crank test),
(b) **GDI high-pressure fuel-rail** PIDs (FRP desired/actual, VCV duty),
(c) **manual-entry secondary-ignition** waveform features (firing kV, burn time, ripple count)?
Anything we can't capture can't ship a consumer regardless of merit — a yes/no per item decides
defer-vs-promote.

**RQ-F — GDI in v2 scope? (refines EP-OBD-IN-09.)**
PRD §5 says petrol-only; GDI is a petrol subtype. Is **direct injection in v2 scope**, or is v2
port-injection-only (GDI a v3 concern)? Decides whether the GDI fuel branch is worth a DNA flag
now.

---

## Suggested sequencing (after research lands)

1. **Promote the ECU-hardware-checker input pair now:** one proposal-registry entry + a single
   OBDLab task adding `intake_air_temp_c` + `throttle_pos_pct` payload fields (IN-08 + IN-05),
   consumer = the COMLab ECU checker (`EP-COM-04`). Highest lift / lowest cost; IAT is already
   half-wired.
2. Register **IN-03 / IN-04** (FUELSYS raw + VPWR) as a small "perception-context fields" entry.
3. On **RQ-A**, close EP-OBD-16 and the wideband-offset band in `T-OBDV2-4` in one pass.
4. On **RQ-B/RQ-C**, pick **one** of EP-OBD-18 / EP-OBD-11 as the primary MAF-drift detector
   (they overlap) and promote it with BARO (IN-06).
5. On **RQ-D**, route per-cylinder misfire to its owning lab.
6. **RQ-E/F** decide the deferred three.

All promotions follow the standing rule: a new field/mode ships **only** with its named
consumer, registered in `comlab/comlab/config/proposals/proposals.yaml` — never a field alone.

---

## Resolutions — owner research, 2026-06-08

The six research questions are answered. Updated dispositions below supersede the table above.

**RQ-A → RESOLVED (EP-OBD-16, O2-FU-3 closed).** Stress-idle is **two-state, not multi-band**:
*VIN decoded* → OBDLab uses the **exact** `stress_idle_rpm_target` from DNALab/VINLab (already
wired via the `APPROXIMATELY` bucketing operator + tolerance); *no VIN* (`dna_view=None` /
`stress_idle_rpm_target=None`) → the **default `STRESS_IDLE` band = 3000–4500 RPM (~4000 typical)**.
The other source numbers are **not** per-signal bands and **not** live alternatives — they are
superseded drafts: `OBDLab_KG_Wiki.md` explicitly retires **2500 RPM** ("STRESS_IDLE supersedes
the old 2500 RPM"), and 3000–4500 already subsumes the 3500–4500 source. **Action: doc-only** —
mark 2500 deprecated; confirm 3000–4500 as the no-VIN default. No code change (shipped behaviour
already matches). *Owner to confirm: retire 2500 rather than treat it as a live default.*

**RQ-B → SKIP (EP-OBD-18 inferred-BARO + EP-OBD-IN-06 deferred).** BARO needs a DNALab
"BARO-equipped" flag and adds noise for little gain → **dropped for now.** Consequence: EP-OBD-18
loses its inferred-BARO half; its remaining MAF/MAP/TPS **rationality** half overlaps EP-OBD-11
(MAF-drift detection), so **EP-OBD-11 becomes the single primary MAF-drift detector** and the
EP-OBD-18 rationality residual is folded into it / deprioritised. **EP-OBD-IN-06 (BARO) → defer.**

**RQ-C → RESOLVED (EP-OBD-11 unblocked).** From `research/MAFLinearity.md`, the `ΔSensor_error`
ladder: **Healthy `< 3–4 %`** (LTFT absorbs) · **Calibration drift / dirty `5–12 %`** (fuel-trim
split) · **Component fault `> 12–15 %`** (trips P0101 MAF range/performance). These pin the
routable thresholds; numeric literals cite `MAFLinearity.md`. **EP-OBD-11 → promote.**

**RQ-D → RESOLVED (OBDLab owns its own input fields).** Even though DTCLab already parses
Mode-06, OBDLab gets **its own input fields** for **per-cylinder misfire (EP-OBD-IN-07)** and
**fuel system status (EP-OBD-IN-03)** — because a DTC is not always set and **DTCLab may not be
in use at all**, so OBDLab cannot depend on it. Both **→ promote** as OBDLab-owned inputs.

**RQ-E → DEFER (too complex to implement now).** EP-OBD-19 (cranking mechanical test),
EP-OBD-IN-10 (secondary-ignition waveform), and EP-OBD-IN-09 (GDI rail-pressure PIDs) are all
**deferred** — the capture is too complex for this phase.

**RQ-F → GDI stays in v2 scope** (do not rule out the GDI fleet), **but** the GDI-specific
rail-pressure branch (EP-OBD-IN-09) remains **deferred** per RQ-E. GDI vehicles are supported by
the general engine; the GDI fuel-rail module waits.

### New owner requirement (must-have)

**Fuel-system-status input dropdown.** Add a **manual-entry dropdown for fuel system status
(Closed-Loop / Open-Loop)** in OBDLab, **mirroring the DTCLab input**. This is the concrete,
required form of EP-OBD-IN-03: the technician selects loop state directly. It feeds the existing
`TrimAnalyticsGate.OPEN_LOOP` path (today `fuel_sys_status` is consumed internally but has no
input surface) and exposes the raw status to COMLab. **Priority: must-have.**

### Net promotion set (post-research)

| Action | Proposals | Note |
|---|---|---|
| **Promote now (Tier 1)** | IN-08 (IAT), IN-05 (TPS), **IN-03 (FUELSYS dropdown — must)**, IN-04 (VPWR), EP-OBD-12 (LTFT cells) | IAT half-wired; FUELSYS dropdown is the new must-have |
| **Promote now (newly unblocked)** | EP-OBD-11 (MAF linearity, thresholds pinned), IN-07 (per-cyl misfire, OBD-owned) | EP-OBD-11 is the primary MAF-drift detector |
| **Doc-only close** | EP-OBD-16 (stress-idle: retire 2500, default 3000–4500) | closes O2-FU-3 |
| **Defer** | EP-OBD-18 inferred-BARO, IN-06 (BARO), EP-OBD-19, IN-09 (GDI rail), IN-10 (ignition wave) | per RQ-B/E |
| **Already absorbed** | EP-OBD-10, -13, -14, -15, -17, IN-01 | unchanged |
