# 11 — v2 proposals register (signal/noise)

Every token this wiki introduces as **new** must name an existing or co-shipped
consumer (the COMLab/fault-atlas code path that reads it) and is listed here.
Nothing in this register is live yet: each ships only when its task spec is
authored, the consumer code path lands, **and** it is registered in the COMLab
proposals registry (`comlab/config/proposals/`) — never silently in the live
KG/registry. "Future use" is not a consumer.

Source provenance for all rows: `obdlab/research/AdvAutomotiveFaultDiagnosis_ANALYSIS.md`
(architect viability pass on Tom Denton, *Advanced Automotive Fault Diagnosis*,
2nd ed., Elsevier 2006), reconciled against `DtcDoc.md` / `DtcDoc2.md`.

---

## 11.1 Proposals (consumer nameable — author as task specs later)

| # | Proposed token / content | Chunk | Named consumer + code path | Disposition |
|---|---|---|---|---|
| P-DTC-1 | `misfire_severity_class` enum (`TYPE_A`/`TYPE_B`/`NONE`) + `catalyst_damage_imminent` escalation | `06`, `10` | COMLab misfire-severity fusion: fault-atlas escalates Type A (1 Hz flashing-MIL) misfire to `CRITICAL_IMMEDIATE_STOP` (catalyst protection) above a Type B steady code. Pairs with OBDLab misfire promotion `EP-OBD-IN-07` / `T-OBDV2-9/10`; GASLab `COMBUSTION_FAIL` is the truth side. | **PROPOSAL** |
| P-DTC-2 | `monitor_status` map (per-monitor `READY`/`NOT_READY`) + `readiness_reset_suspected` bool | `01` | COMLab confidence-weighting: fault-atlas demotes monitor-derived evidence where `monitor_status == NOT_READY`; raises a session caveat on `readiness_reset_suspected`. OBDLab `analytics_preconditions` family (`T-OBDV2-6`). Absorbs cardiagnosis EVAP-readiness B3. | **PROPOSAL** |
| P-DTC-3 | `fmem_suspected` bool (FMEM/limp-home perception-trust) | `10` | OBDLab perception-trust / `analytics_preconditions` → COMLab demotes PID-derived evidence whose source sensor is `fmem_suspected`. | **PROPOSAL (weak)** — viable only if FMEM state is detectable from available PIDs/DTCs; else DEFER |

---

## 11.2 Authoritative pins (refine an existing consumer — no new field)

These tighten numbers already consumed by a live code path; they ship as wiki
citations, not new contract fields.

| # | Pin | Chunk | Existing consumer it refines |
|---|---|---|---|
| Pin-1 | DTC-state cycle counts: PENDING immediate → CONFIRMED on **3rd consecutive driving cycle** → MIL heals after **3 clean cycles** → erase after **≥ 40 warm-up cycles** | `01` | `DTC_VOCABULARY.md §16` — confidence weights per `DTCState` |
| Pin-2 | Warm-up cycle = coolant **+22°C from start AND ≥ 70°C** | `01`, `02` | ECT validity gate (`02`); ≥ 75°C 4DLab read-floor sits above it |
| Pin-3 | Mandated freeze-frame parameter set (Denton §5.4.4) | `02` | `DTC_VOCABULARY.md §12.1` — 12 mandatory FF PIDs |
| Pin-4 | Monitor fault threshold = **1.5 × emission limit** (catalyst/misfire/O₂) | `04` | Mode `$06` marginal-result reading (`Mode06MonitorState`) |
| Pin-5 | EVAP leak-detection size: **1 mm (0.040″) 1996–1999**, **0.5 mm (0.020″) post-2000** | `07` | EVAP DTC reference (P0442/P0455/P0456) |

---

## 11.3 Corroborations (cite the source; no proposal)

Denton and the era docs corroborate work that already ships. No new token.

- Adaptive fuel-trim model (STFT instantaneous, LTFT learned/KAM/battery-robust;
  AFR constant 14.64) → OBDLab trim channels `BANK-ASYM-1`, COMLab fusion. (`03`)
- Catalyst pre/post-O₂ correlation → existing downstream-O₂ masking `T-OBDV2-3`;
  4DLab-viable form is the idle post-cat chemistry cross-check. (`07`)
- Rationality testing (sensor vs rpm/throttle-mapped value) → OBDLab
  `DUAL_MAF_MAP_CROSSCHECK` / VE gate `T-OBDV2-2`. (cross-lab)
- O₂ failure modes (stuck lean/rich, lazy = reduced amplitude+frequency; zirconia
  0.6–0.8 V rich) → OBDLab `o2_failure_mode`. (cross-lab)

---

## 11.4 Deferred / out (no consumer nameable, or out of scope)

| Item | Reason |
|---|---|
| Post-2010 / Euro 6+ tech: GPF differential-pressure **P2452**, Low-Speed Pre-Ignition **P0324/LSPI**, and any hex-tailed Euro-6d code (e.g. **P244A**) | Outside the **1990–2010 (Euro 1–5)** scope. Removed from chunk `08`. Resolves DTC10 Q7: GPF / hex-tailed codes are dead weight inherited from a wider-scope era — drop them (and the `T-FX-13` regex need not match them). |
| Secondary air injection (**SAI**, P0411) | System dropped from 4DLab. Cold-start light-off (~260°C) is unreadable at the ≥ 75°C read-floor anyway; not inferred and no longer passed through as an SAI signal. (was `07`) |
| Oscilloscope waveforms (ignition primary/secondary, alternator ripple, relative-compression, CAN-H/L) | 4DLab ingests values, not traces. Expected behaviours are reference only. |
| Bench electrical tests (coil/plug resistance, gap, DLC pinout) | No resistance probe / live socket. |
| EOBD g/km emission-limit tables (Euro III/IV) | Drive-cycle mass limits, not idle ppm — GASLab/OBDLab scope, not DTCLab. |
| Brettschneider / lambda math, two-speed-idle gas profiles | GASLab-owned (data-isolation invariant `00_INDEX.md §0`). |
| Transmission shift-strategy / gear-ratio inference (P07xx–P09xx) | Outside L1–L5 idle scope. Code passed through, not inferred. (`00_INDEX.md §0`) |
| Boost-pressure verdicts (P0234/P0299) | Load-dependent, largely outside idle window. Code + Mode `$06` MID `$71` passed through; COMLab decides. (`08`) |

---

## 11.5 Next authoring actions (separate sessions — one task each)

1. Author **P-DTC-1** (misfire Type A/B severity) alongside the OBDLab misfire
   promotion; GASLab `COMBUSTION_FAIL` as truth side.
2. Author **P-DTC-2** (readiness/monitor-status trust gate) as an OBDLab
   precondition proposal absorbing cardiagnosis B3 (EVAP).
3. Evaluate **P-DTC-3** (FMEM trust flag) — confirm FMEM detectability from
   available PIDs/DTCs before promoting from weak to active.
4. Attach Denton as a citation source on the OBDLab trim / rationality /
   catalyst tasks per §11.3.

> One-task-per-session: this wiki is the architect deliverable. No `*_tasks/`
> rows are created or flipped here. Each proposal above becomes its own task
> spec with success criteria and the named consumer code path before any code
> ships.

## Graph relations (explicit)

**P-DTC-1** PROPOSES **misfire_severity_class** AND **catalyst_damage_imminent**
**P-DTC-2** PROPOSES **monitor_status** AND **readiness_reset_suspected**
**P-DTC-3** PROPOSES **fmem_suspected**
**P2452** DEFERRED_AS **out of scope (post-2010)**
**P0411** DEFERRED_AS **out of scope (SAI)**
**Pin-1** REFINES **DTCState confidence weights**
**Pin-2** REFINES **coolant_temp_c warm-up gate**
**Pin-3** REFINES **FreezeFrameRecord mandatory PIDs**
**Pin-4** REFINES **Mode06MonitorState thresholds**
**Pin-5** REFINES **EVAP leak-size thresholds**

## Core Entities

- **P-DTC-1** — Proposed misfire severity classification task. Status: PROPOSAL. Consumer: COMLab misfire-severity.
- **P-DTC-2** — Proposed monitor readiness trust gating task. Status: PROPOSAL. Consumer: COMLab confidence-weighting.
- **P-DTC-3** — Proposed FMEM/limp-home perception-trust task. Status: PROPOSAL (weak). Consumer: OBDLab/COMLab.

