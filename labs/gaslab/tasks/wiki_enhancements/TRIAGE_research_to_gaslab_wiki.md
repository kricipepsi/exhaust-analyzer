# Triage — research → GASLab wiki (what's viable, what's not)

**Author:** architect (4DLab) · **Date:** 2026-06-10
**Inputs read in full:** GASLab v2 wiki chunks 00–11 + `CHANGE_v2.1`; the OBDLab
research tree — `proposals/` (`wikiResearch.md`, `AddObdFields.md`, `DataFlow.md`,
`OBD_ImplProp.md`, `PROPOSAL_AUDIT_v2_boost.md`), `proposals/extracted/` (70 EP-*
proposals incl. the EP-GAS-* and EP-CAT-* sets), `formula-wiki/` (22 cards + 12
pending), the two viability analyses (`AdvAutomotiveFaultDiagnosis_ANALYSIS.md`,
`cardiagnosis_ANALYSIS.md`), `MAFLinearity.md`, `CHUNK_ENHANCEMENT_PREP_REPORT.md`,
and the Denton viable extract.
**Question:** which of this material is a real, gas-only improvement to the **GASLab
wiki** — adding more diagnostic capability than noise — and which is already covered,
out of GASLab's scope, or net noise?

> Owner override in force: viability is judged on diagnostic-capability-vs-noise.
> A missing live consumer is **not** a rejection reason here (it is "adjusted up
> the chain"). Items below are rejected only for **redundancy, scope, or noise** —
> never merely for lacking a wired reader.

---

## Headline

The GASLab v2 wiki is **mature**. Most gas-relevant research is already in it.
After a full sweep, only **two** net-new, gas-only, signal-positive additions
remain → `GW-ENH-1`, `GW-ENH-2`. Everything else is **already covered**, **out of
GASLab scope** (OBDLab/COMLab/DTCLab), or **net noise**.

---

## A. VIABLE — author now (→ this pack)

### GW-ENH-1 · Combustion-integrity quantified metrics
**Source:** `EP-GAS-03`; formula-wiki `F-GAS-04` (`chemical_efficiency = CO₂/(CO₂+CO)`)
and `F-GAS-05` (`oxygen_usage`, O₂ vs CO); Vol1 "Combustion Integrity Truth";
`chunks/truth-perception/04`; `wikiResearch.md` §4.
**Gap confirmed:** `grep` of the whole wiki finds **no** `chemical_efficiency`,
no `CO₂/(CO₂+CO)`, and no `oxygen_usage` metric. The wiki discusses Combustion
Efficiency only **narratively** ("~95 % engine-out → >99 % tailpipe", glossary
"CE"), and discriminates misfire-vs-rich only **qualitatively** (the seesaw
`RULE_SEESAW`, the HC/O₂/CO truth table `RULE_HC_O2_CO_TRUTH_TABLE`).
**Why it's signal, not noise:** both metrics are computed from the **existing five
gases** — zero new input, zero new sample. They convert two judgments the wiki
already relies on into **numeric, citable discriminators**:
`chemical_efficiency` < ~0.95 ⇒ a fundamental combustion failure independent of
the fuelling ratio; the O₂-vs-CO relation cleanly splits "both reactants present =
misfire" from "CO high, O₂≈0 = pure rich". This is exactly the kind of
cheapest-possible addition (derive-from-what-we-have) the workspace prefers.
**Disposition: VIABLE.** See `GW-ENH-1`.

### GW-ENH-2 · Healthy-catalyst masking limitation ("filter of truth")
**Source:** `EP-CAT-02` (Catalyst_Masking_Rich/_Lean), `EP-CAT-05` (pre-cat
inference), Vol1 "Systemic Masking" / case N-008 (cat-masked oil burn).
**Gap confirmed:** GASWIKI-07 covers detecting a **failed/weak/poisoned** cat in
depth (dual-idle test, poisoning agents, false-P0420 trap). It does **not** cover
the inverse: a **healthy** cat scrubbing the tailpipe evidence of an engine that is
actually running rich (or lean), so the tailpipe reads clean while the engine is
sick. The current wiki even states "a working catalyst raises CE to >99 %" without
flagging that this same scrubbing **hides** a feed-gas fault until the cat itself
is overwhelmed.
**Why it's signal, not noise:** this is a real diagnostic-safety limitation — the
guide calls cat-masked rich the single most common misdiagnosis to defend against
(user drives away with a damaged engine "saved" by the cat). The honest gas-only
content is a **CONCEPT + limitation note**: what tailpipe gas can see (often
nothing — that's the point) and therefore why the resolution must come from
**pre-cat O₂ + LTFT sign (OBDLab/COMLab)** or pre-cat inference from cat ΔT. It
adds a guardrail and a clean hand-off, not a false gas-only verdict.
**Disposition: VIABLE** (as a documented concept + limitation; resolution is
cross-lab). See `GW-ENH-2`.

---

## B. ALREADY IN THE WIKI — cite the research, add nothing

| Research item | Already covered by |
|---|---|
| `EP-GAS-01` 5-gas schema + Brettschneider λ | GASWIKI-02 §2.3–2.4 (incl. reliability model), GASWIKI-03 |
| `EP-GAS-02` misfire chemistry resolver (high HC + high O₂) | `RULE_MASKING` (§4.8) + truth table (§4.6) + cheat-sheet (§3.6) |
| `EP-GAS-04` two-speed gas transition matrix (Δgas idle→2500) | `TEST_RPM_SEPARATION_MATRIX` (§8.9) + dual-idle (§7.6) |
| `EP-CAT-03` false-P0420 cluster (demote cat when feed-gas clean) | `CONCEPT_POSTCAT_O2_DIAGNOSTIC` §7.3 "false-P0420 trap" |
| Brettschneider per-fault reliability / uncertainty band | `CONCEPT_BRETTSCHNEIDER_RELIABILITY` §2.4 |
| Catalyst poisoning agents (Si, P/Zn, S, Pb) | `CONCEPT_CATALYST_POISONING_AGENTS` §7.7 |
| Oil-burn five modes + RPM-delta sub-cuts | GASWIKI-06A + §8.9 oil-burn sub-cut |
| ECU-vs-tailpipe divergence magnitudes | `CONCEPT_DIVERGENCE_MAGNITUDE` §4.12 |
| Ethanol / altitude shifts, "don't relax the triangle" | `CONCEPT_FUEL_ALTITUDE` §2.9, `GATE_TRIANGLE` §4.1 |

For these, the move is the same as the OBDLab passes: **attach the research file as a
citation** against the existing chunk; do not re-author.

---

## C. OUT of GASLab scope (route elsewhere — not a wiki gap)

- **`EP-GAS-05` 5-gas `vsum` gate** (`HC+CO+CO₂+O₂+NOₓ`, 14–18 %). **Rejected as
  redundant + dimensionally awkward.** GASLab already gates samples with the
  **Exhaust-Gas-Triangle** (`CO+CO₂+O₂`, 14–16 %, `GATE_TRIANGLE`) plus the
  dilution screen (`CO+CO₂ > 6 %`). `vsum` adds HC and NOₓ (ppm) to %-vol gases,
  which is dimensionally muddy, for no separation the triangle doesn't already
  give. More noise than signal → **do not add.**
- **`EP-CAT-01` OSC damping ratio / `TI_cat`** — post-cat **O₂-sensor switching**;
  the wiki itself (§7.3) says GASLab does **not** consume switching ("OBDLab's
  job"). OBDLab/COMLab. Formula lives at `F-O2-03`.
- **`EP-CAT-04` catalyst field-test inputs** (backpressure, IR Δtemp, Mode-06) —
  **non-gas physical inputs**; outside GASLab's tailpipe-5-gas emit boundary →
  COMLab catalyst routing. Formula at `F-O2-04`.
- **`wikiResearch.md` delta/divergence engine** (digital vs physical λ deltas,
  cross-delta Δδ, EPROM/ADC/capacitor fingerprints) — **COMLab**; already carded
  at `F-DLT-01..04`.
- **All OBDLab EP-OBD-* / EP-OBD-IN-* / `MAFLinearity.md` / VE / trim / BARO** —
  OBDLab, covered by `PROPOSAL_AUDIT_v2_boost.md`. Not GASLab.

## D. Denton (`AdvAutomotiveFaultDiagnosis_VIABLE_prepped.md`) — gas relevance

Per `AdvAutomotiveFaultDiagnosis_ANALYSIS.md`, Denton is an **OBD/DTC structural**
asset (monitor taxonomy, DTC-state machine, freeze-frame set, readiness flags) —
DTCLab/COMLab territory, not gas chemistry. The gas-adjacent facts:
- **Misfire severity Type A/B, ~45 % at idle, 1 Hz MIL** — an **OBD-monitor**
  concept; GASLab detects misfire *chemically*, it does not measure misfire %.
  → DTCLab/COMLab.
- **Catalyst light-off ~260 °C, secondary-air cold-start** — **cold-start**;
  GASLab reads warm (≥75 °C). Out of scope.
- **Catalyst thermal-damage threshold ~1000 °C** — the only figure worth carrying,
  and only as a **one-line citation** inside `GW-ENH-2` (why masked rich is
  dangerous), not a standalone task.

## E. cardiagnosis — gas relevance

Corroboration asset (per `cardiagnosis_ANALYSIS.md`). The one gas-truth-adjacent
item, **CTS-stuck-cold → ECU over-fuels → high CO at operating temp**, is a
**perception/root-cause** attribution (COMLab gate over GASLab's `RICH_MIXTURE`
truth) — GASLab alone just sees rich. Not a GASLab wiki gap. Already logged as
cardiagnosis candidate B2 for a COMLab session.
