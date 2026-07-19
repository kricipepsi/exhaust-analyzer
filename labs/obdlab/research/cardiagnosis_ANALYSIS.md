---
title: "cardiagnosis.md — Architect Viability Analysis"
author: "4DLab architect"
date: "2026-06-08"
source_doc: "labs/obdlab/research/cardiagnosis_prepped.md (OCR of Radovan Marić, *Car Diagnostics — Step by Step*, Zagreb 2013, ISBN 978-953-95888-4-5)"
role: "architect (spec/analysis only — no implementation code, no ledger rows authored here)"
status: "analysis complete — dispositions are RECOMMENDATIONS, not registered tasks"
domain: "obdlab/research"
---

# cardiagnosis.md — Architect Viability Analysis

## What this is (and is not)

This is the **architect analysis** requested for `cardiagnosis.md`: chunk the
book, study each chunk, and judge which diagnostic techniques are **viable to
implement in the 4DLab petrol workflow**, within what 4DLab can actually
diagnose. Per the workspace HARD RULE, the architect deliverable is the
spec/analysis — **no implementation code and no `*_tasks/` rows are written in
this session.** Every disposition below is a *recommendation* for a later
authoring session, and every proposed field names its consumer + code path so
it is signal/noise-clean before anyone authors it.

The prepped source and its change log are companions to this file:
`cardiagnosis_prepped.md` and `cardiagnosis_PREP_REPORT.md`.

### Readability gate (passed on the prepped file)

- `![][` image placeholders: **0**
- Read truncation: handled by deliberate chunking (book is 6.7k lines / 44k words)
- Formula content: present as inline prose (λ, 14.7:1, voltages) — no lost equations
- Residual OCR glitches after prep: 0 vertical-tab bytes, 0 CR, depth ≤ `###`

## Method

The book had no heading structure, CRLF endings, and an OCR glitch where every
vertical-tab byte (`0x0B`) had replaced a capital **N** (MARI**N**, **N**ational,
ISB**N**, DIAG**N**OSTICS). Prep (md-prep skill) fixed encoding, stripped 139
page-number noise lines, injected the book's own chapter/section headings at
their body anchors, and produced `cardiagnosis_prepped.md`. Chunks follow the
book's chapters; the chunk index lives in the PREP_REPORT. I then read every
**in-scope** chunk in full and confirmed the out-of-scope chapters from their
chapter purpose.

## The scope frame I judged against

Three facts about 4DLab decide everything below.

1. **4DLab performs inference on *ingested* data — it does not talk to the car.**
   The user supplies gas-analyzer readings, DTCs, freeze-frame, and live-PID
   values. So the book's large "how to connect / flash / scan / repair" content
   is **out of scope as technique**, no matter how detailed — there is no live
   comms, no bench multimeter, no soldering iron in the pipeline.

2. **Petrol-only, idle-centric pipeline (L1–L5).** L1 idle gas → L2 high-idle
   gas → L3 DTCs → L4 freeze frame → L5 live PIDs. Truth-vs-perception: **gas
   chemistry (Brettschneider λ) is ground truth; the ECU is perception.**

3. **Lab division of labour (from `KGtopic.md`, the lab READMEs, and the OBDLab
   ledger).** GASLab = truth (`λ_chem`, `chemical_state`, e.g. `COMBUSTION_FAIL`).
   OBDLab = **perception-channel emitter only** (`o2_failure_mode`, trim deltas,
   `lambda_perception_delta`, VE) — it emits typed channels, never verdicts.
   DTCLab = DTC-state weighting + P-code→family causal sub-graphs + freeze-frame
   params. COMLab (Stage 4) = the fusion spine + **fault-atlas routing** that
   cross-references the deltas and outputs the verdict. DNALab/VINLab = the
   `VehicleDNA` that prunes the graph (narrowband vs wideband, MAF vs
   speed-density, bank count, OBD era).

The signal/noise rule and the "progress-forward" rule together mean: a book
technique is **viable** only if I can name an existing-or-paired consumer (a
COMLab analytics path or fault-atlas node) and the code path that reads it.

## Headline finding

**The book is overwhelmingly a *corroboration and sourcing* asset, not a
greenfield of new techniques.** Its entire OBD-relevant core — O2/wideband
behaviour, fuel-trim/Closed-Loop logic, MAP/TPS cross-checks, misfire→lean
cascades, pending-vs-confirmed DTC states — maps onto OBDLab/DTCLab tasks that
are **already specced** (`T-OBDV2-2…8`, `ECU-PERCEPT-1`, `BANK-ASYM-1`, the
unallocated `T-OBDV2-9/10`). For those, the right move is **cite the book as a
research source against the existing task**, not re-propose. The book yields a
small number of **genuinely net-new candidates** — all of them COMLab
**fault-atlas fusion patterns over fields we already emit**, which is the
cheapest, most signal/noise-clean kind of addition.

## Chunk index and scope verdict

| Chunk | Section | In/Out | Why |
|---|---|---|---|
| C0 | Front matter / TOC | ref | — |
| C1 | Electronic Engine Management (sensor roster; lambda=truth, ECU=perception) | **IN** | Conceptual spine; corroborates truth-vs-perception |
| C2 | Diagnosing without devices (blink codes, Autodata) | mostly OUT | Workshop procedure; one reusable *principle* (below) |
| C3 | SRS / ABS / service-interval reset | **OUT** | Non-engine safety/maintenance subsystems |
| C4 | OBD I — K/L lines, KL interface install | **OUT** | Live-comms setup; 4DLab ingests, no comms |
| C5 | OBD II — software/interface/scanners; Pending codes; Freeze Frame mention | partial | Tooling OUT; **Pending-codes** + freeze-frame concept IN |
| C6 | Most common causes of trouble codes (per-sensor) | **IN — core** | The diagnostic-inference heart |
| C7 | EVAP | partial | P-code triage + monitor-readiness precondition IN; plumbing OUT |
| C8 | ECU Flashing & Mapping | **OUT** | Modification, not diagnosis |
| C9 | Immobilizer / anti-theft | **OUT** | Security |
| C10 | Radio decoding / parking sensors | **OUT** | Infotainment / non-engine |
| C11 | ECM/PCM repair; transistor/resistor/capacitor testing | **OUT** | Board-level hardware repair |
| C12 | Cruise / Start-Stop / Regen braking / HHO | **OUT** | Non-fault features / fringe |

## Technique inventory and dispositions

Disposition key: **CORROBORATES** = existing task, cite the book, do not
re-propose · **PROPOSAL-CANDIDATE** = net-new, consumer nameable, author later
as a proposal (field + consumer ship together) · **DEFER** = no consumer
nameable within idle/perception scope · **OUT** = not a 4DLab technique.

### A. Corroborates existing specs (cite the book, no new proposal)

| # | Book technique (chunk) | 4DLab mapping | Existing task | Named consumer / code path |
|---|---|---|---|---|
| A1 | Wideband/AF sensor: stoich **14.7:1 = λ1**, current ± around λ1, **inverted voltage convention** vs narrowband, supply 2.6/3.3/5 V, op-temp ~400→~800 °C, heater = top failure (C6) | OBDLab wideband perception + `lambda_perception_delta` | `T-OBDV2-4`, `ECU-PERCEPT-1`, FU-ECU-2 | COMLab `T-COMV2-O2OFFSET-1`, `T-COMV2-ECU-FUSE-1` |
| A2 | Narrowband O2 **0.1–0.9 V**, switch ~**0.45 V** (low=lean/high=rich), slow/no oscillation = lazy probe, fault disables Closed Loop → ↑fuel (C1,C6) | OBDLab `o2_failure_mode` (e.g. `LAZY_SWITCHING`) | OBDLab emitter (T-OBDV2-1b) | COMLab fusion (`o2_failure_mode` reader) |
| A3 | Downstream (post-cat) probe = catalyst monitor on old platforms, rear-trim feedback on new (C1) | OBDLab downstream-O2 masking | `T-OBDV2-3` (closed) | **live** `comlab perception_contradiction.detect` |
| A4 | **Pending vs confirmed/permanent** DTC; pending clears after ~40 warm cycles, else MIL on; repeated-pending ⇒ mechanical (C5) | DTCLab DTC-state weighting | DTCLab role (Stage 3) | COMLab fault-atlas (DTC-state weight) |
| A5 | **MAP↔TPS proportionality** cross-check during throttle; MAP rises as vacuum drops; single-sensor fallback (C6) | OBDLab VE-as-evidence (`DUAL_MAF_MAP_CROSSCHECK`) + `throttle_pos_pct` | `T-OBDV2-2`, `T-OBDV2-7` | COMLab `T-COMV2-VE-GATE-1`; ve_engine |
| A6 | **Misfire** random (P0300) vs cylinder (P030x); misfire pumps raw HC+O2 → looks lean (C6) | GASLab `COMBUSTION_FAIL` (HC+O2 truth) + DTCLab P030x causal graph | EP-OBD-IN-07 misfire (unallocated `T-OBDV2-9/10`); GASLab; DTCLab | COMLab misfire fusion |
| A7 | Closed-Loop only at op-temp; CTS-cold/O2-fault force **open-loop enrichment** (C1,C6) | OBDLab `FuelSystemStatus` (CL/OL/OL_DRIVE/OL_FAULT) | `T-OBDV2-6` | **live** `analytics_preconditions` + `semantic_consistency_checker`; COMLab `T-COMV2-FUELSYS-GATE-1` |
| A8 | IAT/TPS as fuel-calc inputs; control-module voltage matters (C1) | OBDLab `intake_air_temp_c`, `throttle_pos_pct`, `control_module_voltage_v` | `T-OBDV2-7`, `T-OBDV2-8` | ve_engine; COMLab `T-COMV2-ECU-HW-1`, `T-COMV2-VPWR-GATE-1` |

### B. Net-new proposal candidates (consumer nameable — author later, not now)

These are the only items I'd carry forward as **new** content. All three are
COMLab **fault-atlas patterns over fields 4DLab already emits/ingests**, so they
add a *consumer* (a routing node) far more than they add schema — the cleanest
signal/noise profile available.

1. **Vacuum-leak multi-code fault-atlas pattern (strongest candidate).**
   The book states it explicitly (C6, O2 section): O2-low/lean **+** MAP code
   **+** occasional misfire, **present only at idle**, points to an intake
   **vacuum leak** — *not* any of the named sensors. This is a textbook
   fault-atlas fusion: it reads existing channels (`o2_failure_mode`,
   `map_status`, a misfire indicator) gated by an idle context, and routes to a
   single root cause instead of three sensor verdicts.
   *Consumer to pair:* a new COMLab fault-atlas node (e.g. `EP-FA-VACLEAK-1`) in
   `fault_atlas_router`. *Schema cost:* none new if `map_status`/`o2_failure_mode`/
   misfire count already exist (they are pre-frozen contract surface per
   FU-OBD-ORPHAN-1). *Disposition:* **PROPOSAL-CANDIDATE** — field-free, consumer-only.

2. **CTS/ECT cold-enrichment root-cause pattern (+ possible `coolant_temp_c` input).**
   The book's CTS example (C6) is a clean root-cause cascade: CTS reads
   constant-cold → ECU over-fuels → **high CO** (GASLab truth) + lambda fouling →
   *multiple* DTCs whose root is one sensor; insufficient coolant / stuck-open
   thermostat mimic it. The viable 4DLab form is a COMLab check that cross-refs
   **GASLab high-CO truth** against a **cold-coolant-while-runtime-long**
   perception, and **suppresses lambda-fault routing** when the pattern fits.
   *Gap:* `coolant_temp_c` (PID 0x05) is **not** an OBDLab input today
   (`T-OBDV2-7` adds IAT, not ECT). So this needs either (a) the input field
   **plus** the COMLab cold-enrichment gate that reads it, shipped together as a
   proposal, or (b) DEFER if the gate can't be justified. *Disposition:*
   **PROPOSAL-CANDIDATE, consumer-paired** — viable only with the COMLab gate named.
   *Note:* the book's 7–13 kΩ(cold)→0.7–1 kΩ(hot) resistance curve is a **bench**
   value; 4DLab ingests a temperature PID, not resistance, so the consumer reasons
   on temp-vs-runtime, not Ω.
   *Measurement condition (owner-pinned 2026-06-08):* 4DLab takes all readings at
   **operating temperature (≥ 75 °C)**. So the only CTS fault it can see is the
   **stuck-cold-while-warm** case — at ≥ 75 °C the CTS still reports cold → ECU
   over-fuels → GASLab reads high CO. This is a *faulty-sensor-at-operating-temp*
   detection, **not** a cold-start reading: 4DLab never captures cold start or the
   cold↔hot resistance sweep, so those stay out of scope. The ≥ 75 °C reading is
   itself the discriminator, which *strengthens* B2 (no cold-start data needed).

3. **EVAP monitor-readiness precondition (fuel level 15–85 %).**
   The book (C7) states the ECU runs the EVAP monitor **only when the tank is
   15–85 % full**. That is a genuine *monitor-readiness* precondition: an EVAP
   P-code's confidence should be gated by whether the monitor could even run.
   *Consumer to pair:* OBDLab `analytics_preconditions` / monitor-readiness gate
   (same consumer family as `T-OBDV2-6`). *Disposition:* **PROPOSAL-CANDIDATE
   (small)** — likely a precondition flag, not a verdict field.
   *Related, DTCLab-owned:* EVAP P-code triage (P0440 gross→cap; P0442 pinhole→smoke;
   P0443/P0449→purge/vent) is a DTCLab P044x family mapping — author when DTCLab opens.

### C. Defer (no nameable consumer in idle/perception scope)

- **Turbocharger overboost/underboost (P0234/P0299) wastegate reasoning (C6).**
  Petrol turbos exist in v1, but the diagnosis needs **boost/load** signals that
  the idle-centric L1/L2 pipeline does not capture. No idle-time channel ⇒ no
  consumer. **DEFER** unless a boost-PID channel is ever added. (P023x/P029x can
  still live in the DTCLab family map as codes; only the *boost inference* defers.)
- **CKP electrical bench test (inductive 200–400 Ω, AC 0.2–2 V cranking; Hall 5 V) (C6).**
  4DLab never measures sensor resistance/AC. The *useful* CKP fact — CKP failure ⇒
  engine won't run — already lands in the **Mode-06 no-start** proposal
  (`T-OBDV2-5`). **DEFER** the bench test; the no-start linkage is already covered.
- **EGR carbon-cleaning / partial-open (C6).** Mostly physical maintenance. The
  one inference nugget (EGR-partial-open → companion MAP + misfire codes) overlaps
  candidate B1's vacuum/idle-rough family; low marginal value. **DEFER/note.**

### D. Out of scope (chapters, with rationale)

SRS & ABS diagnostics (non-engine safety), service-interval reset (maintenance),
OBD I KL-line + OBD II interface install + ELM327 + handheld scanners (live comms;
4DLab ingests data), ECU flashing & mapping (modification), immobilizer / anti-theft
(security), radio decoding (infotainment), parking sensors (non-engine), ECM/PCM
hardware repair + transistor/resistor/capacitor testing (board-level repair),
cruise / Start-Stop / regenerative braking (non-fault features), HHO (fringe).
All are **OUT** because they are either workshop/bench/comms procedures 4DLab
never performs, or non-petrol-engine subsystems outside L1–L5.

### E. One reusable principle (not a feature)

C2/C6 hammer a philosophy already baked into 4DLab and worth keeping explicit in
the wikis: **a DTC only names a *sector*, never the part to replace; one DTC is
frequently the *consequence* of another.** This is exactly the DTCLab causal
sub-graph + COMLab fusion thesis (`KGtopic.md`). No new work — it validates the
existing architecture and is good citation ammunition for the DTCLab wiki.

## Citeable thresholds harvested (for later numeric-literal citations)

If any of these ever reach `gaslab/` or `obdlab/` code, the numeric-literal rule
requires a **wiki** citation, not a citation to this book. Treat the book as
*corroboration*; pin the shipping value from `OBDLab_KG_Wiki.md` and reconcile:

- Narrowband O2 swing **0.1–0.9 V**, stoich switch **~0.45 V** (low=lean / high=rich).
- Wideband stoich **14.7:1 (λ = 1)**; current zero at λ1; **inverted** V convention; supply **2.6 / 3.3 / 5 V**; op-temp **~400 → ~800 °C**.
- CTS resistance **7–13 kΩ cold → 0.7–1 kΩ at op-temp** (bench Ω; 4DLab uses temp PID).
- CKP inductive **200–400 Ω**, **0.2–2 V AC** cranking (bench only — defer).
- Pending DTC auto-clear after **~40 warm cycles**.
- EVAP monitor window **fuel level 15–85 %**; codes **P0440 / P0442 / P0443 / P0449**.
- Turbo codes **P0234 (overboost) / P0299 (underboost)** (defer the inference).

## Unplanned follow-ups (not in this diff)

| FU | Finding | Disposition |
|---|---|---|
| FU-CD-1 | `coolant_temp_c` (PID 0x05) is not an OBDLab input; candidate B2 needs it | Pair with COMLab cold-enrichment gate, or defer — author later |
| FU-CD-2 | Book thresholds (§ harvested) are research-grade; need wiki reconciliation before any reach code | Pin from `OBDLab_KG_Wiki.md` at authoring time |
| FU-CD-3 | OCR two-column flatten leaves occasional clause-order artifacts in prose (numeric values intact) | Cosmetic; logged in PREP_REPORT, not fixed |

## Recommended next actions (for a future authoring session — NOT done here)

1. **Author candidate B1** (vacuum-leak fault-atlas pattern) as a COMLab proposal
   when COMLab/Stage-4 opens — it's consumer-only over existing fields, the
   cheapest win. Cite C6.
2. **Decide B2** (CTS cold-enrichment): either author input `coolant_temp_c` +
   COMLab gate together as a proposal, or defer with reason. Do **not** add the
   input alone (orphan = signal/noise breach).
3. **Fold B3** (EVAP 15–85 % monitor-readiness) into the EVAP/precondition work
   when DTCLab/Stage-3 reaches P044x.
4. **Attach this book as a citation source** to `T-OBDV2-4`, `ECU-PERCEPT-1`,
   `T-OBDV2-2/6/7`, and the unallocated misfire promotion — corroboration, not
   new scope.

> Per the one-task-per-session rule, this analysis is the single deliverable.
> No `*_tasks/` rows were created or flipped; the candidates above are
> recommendations for separate authoring sessions.
