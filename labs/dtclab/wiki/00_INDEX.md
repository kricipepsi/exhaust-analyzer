# DTC Wiki — Index & Reading Map (v2, chunked)

**Purpose:** the diagnostic *reasoning grammar* (the rule-set DTCLab applies to
read, weight, and route OBD-II evidence) for OBD-II Mode `$03/$07/$0A` (DTCs),
Mode `$02` (freeze frame), and Mode `$06` (on-board monitors). Where
`docs/DTC_VOCABULARY.md` defines the contract surface (the enums, field names,
and schema that cross the COMLab boundary), this wiki defines how those tokens
are read, weighted, and routed against the cases corpus.

**Status:** v2.0 (2026-06-11). Chunked successor to the single-document
`docs/_archive/DTC_WIKI_v1_single.md` (v1.0, 2026-05-19). All v1 content is
carried forward across the chunks below; v2 adds knowledge extracted from the
Denton OBD viability analysis and the era/case reference docs (see `11_*` and
the Sources section here).

**Scope:** petrol vehicles 1990–2010 (Euro 1 – Euro 5), manually entered data,
SAE J1979 OBD-II. No live CAN/OBD streaming. No diesel, LPG, CNG, E85, hybrid
drive logic. No post-2010 / Euro 6+ tech (GPF, LSPI, secondary-air-injection
inference). Turbo/GDI petrol *is* in scope (chunk `08` — both predate 2010);
transmission codes are boundary-only (pass-through, not inferred — see §0 below).

---

## 0. Module purpose & data-isolation invariant

DTCLab is the **digital diagnostic fault compiler** (the module that turns
electronic status arrays into one validated evidence packet) of 4DLab. It
ingests electronic status arrays only:

- Mode `$03` (confirmed DTCs)
- Mode `$07` (pending DTCs)
- Mode `$0A` (permanent DTCs)
- Mode `$02` (freeze-frame PIDs)
- Mode `$06` (on-board monitor test results)

…and emits one validated `DTCLabPayload` (see `DTC_VOCABULARY.md §11`) to COMLab.

**Data-isolation invariant.** DTCLab is blind to:

- Exhaust gas concentrations (CO, HC, CO₂, O₂, NOx) — owned by GASLab.
- Lambda values, chemistry math, Brettschneider — owned by GASLab.
- Live OBD PIDs — owned by OBDLab.
- Mechanical degradation / power-loss math — owned by COMLab fault registry.
- Fault node IDs (`Mechanical_Lean_Vacuum_Leak`, etc.) — owned by COMLab.

If a task ever tempts the coder to compute a lambda, a CO threshold, or a
mechanical-fault verdict, the task is wrong-module. Surface and stop. The gas
signatures in chunk `09` are **reverse-lookup reference only**; the tokens there
are injected by COMLab, never computed by DTCLab.

**Three-mode coupling invariant.** Mode `$03`, `$02`, `$06` are collected and
emitted **together** inside one `DTCLabPayload`. No per-mode independent modules;
no per-mode independent emission. The fusion sanitizer is the single output
surface.

**Transmission boundary.** P07xx/P08xx/P09xx codes are integrated into the PCM
but sit outside the L1–L5 idle-centric inference scope. DTCLab passes a
transmission DTC through as a code token (so COMLab can see it) but performs no
shift-strategy or gear-ratio inference. (Source: DtcDoc.md "Cluster 6/7".)

---

## 1. Chunk map

Read in order for a full pass; jump directly when you need one rule.

| Chunk | Title | Covers (v1 §) | v2 additions |
|---|---|---|---|
| `01_dtc_state_lifecycle.md` | DTC state lifecycle & monitor readiness | §1 | DTC-state authoritative pin (3/3/40 cycles); readiness/monitor-status trust gate **[PROPOSAL]**; one-trip/two-trip maturation + corpus skew |
| `02_freeze_frame_validity.md` | Freeze-frame validity gates & interpretation | §2, §3, §4 | Mandated freeze-frame parameter-set pin |
| `03_fuel_trim_grammar.md` | Fuel-trim formulas, patterns, healing | §5, §12 | — |
| `04_mode06_monitors.md` | Mode `$06` as pre-DTC early warning | §6 | MID/TID early-warning reference |
| `05_fuel_air_metering.md` | Fuel & air metering DTCs | §7 | Extended inventory (cam-timing, MAF, MAP, IAT, ECT-rationality) |
| `06_ignition_misfire.md` | Ignition & misfire DTCs | §8 | Misfire Type A/B severity model **[PROPOSAL]**; knock |
| `07_catalyst_egr_evap.md` | Catalyst, EGR & EVAP DTCs | §9 | Pre/post-O₂ idle cross-check; EVAP variants |
| `08_forced_induction_gdi.md` | Forced-induction & GDI DTCs | — (new) | Turbo P0234/P0299; GDI HPFP P0087/P0090/P0191 |
| `09_gas_reverse_lookup.md` | Gas-signature reverse-lookup & perception gaps | §10, §11 | — (COMLab-injected reference) |
| `10_nonstart_diagnostics.md` | Non-start vocabulary & era cases | §13, §14 | Era non-start cases with FF+Mode `$06` values; FMEM trust flag **[PROPOSAL]** |
| `11_proposals_register.md` | v2 proposals — consumer + code path | — | Consolidated signal/noise register |
| `12_ranking_discriminator.md` | Ranking discriminator: prevalence, fan-out & priority | — (new) | DTC-prevalence at intake; generic-code fan-out matrix; P1xxx usability; primary-code priority hierarchy + tie-breaks |

---

## 2. Signal/noise discipline in this wiki

Every field, enum value, or flag this wiki introduces as **new** must name an
existing or co-shipped consumer (the COMLab analytics or fault-atlas code path
that reads it) and the code path. v2-new tokens are tagged **[PROPOSAL]** inline
and consolidated in `11_proposals_register.md`. Domain prose that cites a source
without adding a contract field is reference material and ships freely.

A token marked **[PROPOSAL]** is *not yet* in `docs/DTC_VOCABULARY.md` or the
live config; it ships only when its task spec is authored and the consumer code
path lands. The proposal must also be registered in the COMLab proposals
registry (`comlab/config/proposals/`), never silently in the live KG/registry.

---

## 3. Anchored to

- `docs/DTC_VOCABULARY.md` — every enum, regex, field name cited here lives there.
- `COMLab/docs/wiki/SEMANTIC_CONTRACT.md` — boundary protocol.
- `GASLab/docs/wiki/GAS_WIKI.md` — gas-chem cross-lookup (chunk `09`).
- `COMLab/docs/wiki/OBD_VOCABULARY.md` — OBD live-PID naming for cross-lab fields.

---

## 4. Sources

**Standards:**

- SAE J2012 / J2012DA (DTC structure)
- SAE J1979 / J1979DA (OBD-II modes + PIDs)
- ISO 15031-5 / 15031-6 (international DTC)
- ISO 14229 UDS (Mode `$06` architecture)
- SAE J1699-3 (monitor enable conditions)

**Industry / vendor:**

- Innova Diagnostic Reference — CLV bands, 70% threshold
- Autodtcs freeze-frame docs — 70% load definition
- Nissan OBD service docs — ECT ≥ 70°C gate
- Ford PCED — OBD-II freeze-frame reference
- AVI OnDemand — "Fuel Trim Diagnosis and O₂ Sensor Performance"

**v2 research inputs** (under `obdlab/research/`):

- `AdvAutomotiveFaultDiagnosis_ANALYSIS.md` — architect viability pass on Tom
  Denton, *Advanced Automotive Fault Diagnosis* (2nd ed., Elsevier 2006). Source
  of the DTC-state pin, readiness gate, freeze-frame parameter set, misfire
  Type A/B model, catalyst pre/post-O₂ idle form, and FMEM trust flag.
- `sources/various/DtcDoc.md` — 5-gas↔DTC cluster atlas, extended DTC inventory,
  idle-vs-stress PID profiles, 30 non-start era cases (FF + Mode `$06`).
- `sources/various/DtcDoc2.md` — era A/B/C architectural classification (era C /
  post-2010 / Euro 6+ is out of the 1990–2010 scope; eras A and B only).
- `sources/various/Vol1–Vol8.md` — corroborating truth-vs-perception, two-speed
  idle, era, and gas-analysis reference (largely GASLab/OBDLab-owned; cited for
  cross-lab context only).
- `DTCanswers.md` / `DTCansw2.md` — web-research synthesis (2026-06-11) on DTC
  prevalence, generic-code fan-out, P1xxx usability, one-trip/two-trip
  maturation, and primary-code priority. Source for chunk `12` and `01 §1.4`.
  (`DTCansw2.md` is the value-complete copy; `DTCanswers.md` dropped some inline
  thresholds in export.)

**Internal case corpus** (under `DTCLab/cases/`): `DTCcases1.md`, `DTCcase2.md`,
`DTCadd.md`, `DTClab.md`, `casesDTC.md`, `NonStartCases.md`,
`Gas Lab DTC Code Matching (1).md`, `FF+$06DS.md`, `FFFT$06.md`,
`master_freeze_frame_guide.md`, `master_perception_guide.md`,
`Advanced Diagnostic Correlation … Powertrain Control Systems_*.md`.

**4DLab anchors:** `docs/DTC_VOCABULARY.md`, `COMLab/docs/wiki/SEMANTIC_CONTRACT.md`,
`COMLab/docs/wiki/DNALab_TO_COMLab_FLOW.md`,
`4DLab/NewArchProposal_ImplementationPlan.md`.

## Graph relations (explicit)

**DTCWIKI-00-INDEX** DESCRIBES **DTCWIKI-01** through **DTCWIKI-12**
**DTC_WIKI v1.0** SUPERSEDED_BY **DTC_WIKI v2.0 chunk corpus**
**DTC_VOCABULARY.md** COMPANION_TO **DTC_WIKI v2.0**
**DTCLab** ROUTES_TO **COMLab**
**DTCLabPayload** CONSUMED_BY **COMLab.comlab.schemas.ingestion**

## Core Entities

- **DTCWIKI-00-INDEX** — Authoritative index & reading map for the DTCLab v2 wiki corpus (13 chunks). Consumer: `T-DTC-GRAPH-AST`.
- **DTC_VOCABULARY.md** — Companion vocabulary contract (v1.0), located at `labs/dtclab/docs/DTC_VOCABULARY.md`. Consumer: `dtclab/schemas/vocabulary.py`, `family_map.py`, and COMLab.
- **DTCLabPayload** — Canonical output payload emitted by DTCLab to COMLab. Consumer: `dtclab/schemas/payload.py`, COMLab ingestion.
- **DTCRoutingTag** — 18-value routing tag enum for pre-pruning candidates. Consumer: `dtclab/schemas/vocabulary.py`, `family_map.py`, `dtclab/core/routing_tag_mapper.py`.

