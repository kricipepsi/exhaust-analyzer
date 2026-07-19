# Design note — splitting internal **oil** leak from internal **coolant** leak

**Date:** 2026-06-22 · **Status:** proposal (architect → coder) · **Family:** mechanical_wear / gas chemistry
**Engine:** Citroën 5FR (EP6CDT 1.6 THP, turbo + GDI) reference case, but the split is engine-agnostic.

---

## 1. Problem

Today the gas pipeline has **one** internal-leak chemical state, `COOLANT_LEAK_INTERNAL`
(`gas_lab_ontology.yaml` §7.32), and the head-gasket rule `MW-003` gates on it. That state's
signature is a **coolant-quench** fingerprint (lean, O₂ up, NOx crushed). An **internal oil leak**
— oil entering a cylinder through a head-gasket oil-gallery breach — burns as fuel and produces the
*opposite* chemistry, so it has **no home**: it neither matches the coolant state nor is cleanly
told apart from the other oil-in-chamber faults.

A *chemical state* here is just the named category the gas stage assigns (a value in the
`ChemicalSignature` enum — the fixed list of allowed categories). We need a second internal-leak
category and a rule that consumes it.

> **Scope:** this note is about the **oil-burning** internal leak. Coolant intrusion stays as-is.

---

## 2. The core split — oil vs coolant in the chamber

They contaminate the same place but move the gas in opposite directions, because **coolant quenches
the flame and oil feeds it.**

| Channel | `COOLANT_LEAK_INTERNAL` (quench) | `OIL_LEAK_INTERNAL` (combustible) | Why opposite |
|---|---|---|---|
| **λ** | **LEAN** (1.0–2.5) | **stoich / slightly rich** (≈0.92–1.02) | water leaves O₂ behind; oil is extra fuel |
| **O₂** | **HIGH** (H₂O dissociation) | **normal / low** | unconsumed vs. consumed by rich burn |
| **NOx** | **CRUSHED** (cool flame) | **near-normal** | only a *cooled* flame kills NOx |
| **HC** | elevated (glycol flash) | **elevated** (heavy-HC oil) | both raise HC — *not* a discriminator |
| **CO** | **low** (0–0.5) | **raised** (incomplete oil burn) | fuelling-neutral vs. rich |
| **CO₂** | depressed (water dilution) | mildly depressed | weak discriminator |
| **ECT** | **HOT, coolant dropping** | **normal, coolant stable** | only the coolant path loses coolant |
| **Smoke** | WHITE steam, sweet | BLUE, oily | physical confirmation |

**Decisive separators:** the **O₂ / λ / NOx triad** plus **ECT**. Lean + O₂-up + NOx-crushed + hot =
coolant; rich/CO-up + O₂-normal + NOx-normal + normal-temp = oil. HC is high in *both*, so it must
**not** be used to tell them apart.

---

## 3. The harder overlap — oil-internal vs rings / valve seals

Once `OIL_LEAK_INTERNAL` exists, its chemistry looks like the **other oil-in-chamber faults**
(`WORN_PISTON_RINGS`, `WORN_VALVE_SEALS`) — all three burn oil in the cylinder. Gas chemistry gives
you *"oil is burning,"* not *"via the head gasket."* Two non-gas channels finish the job:

| Discriminator | Head-gasket oil breach | Rings / valve seals | Source channel |
|---|---|---|---|
| **Cylinder localization** | **one cylinder** (the breach) | broad / load- or vacuum-driven | OBD `per_cylinder_misfire_counts`, `ltft_cell_vector` (already in payload) |
| **Oil/coolant cross-mix** | **possible** (gasket is the wall between the galleries → milky oil, oil in coolant) | never | **manual check** — flag for confirmation |
| **RPM behaviour** | roughly steady | rings rise with load; seals clear at high idle | gas L1→L2 delta (already used) |

Localization is the channel that says *head gasket* rather than *rings*. Cross-contamination is the
clincher but is a manual observation, not a live reading.

---

## 4. Gate logic (plain-English)

```
internal leak suspected (fluid entering a cylinder):

  if  O2 HIGH  and  λ LEAN  and  NOx CRUSHED  and  ECT HOT (coolant dropping):
        → COOLANT_LEAK_INTERNAL                 (unchanged)

  elif HC HIGH and O2 normal/low and NOx normal and ECT normal (coolant stable):
        → OIL_LEAK_INTERNAL                     (NEW)
             then localize:
               one cylinder + (oil/coolant cross-mix)  → head-gasket oil breach
               broad / load- or idle-driven            → defer to rings / valve-seal rules
```

The O₂/λ/NOx + ECT branch is **automatic** (all channels the engine already has). The head-gasket-vs-rings
step needs the per-cylinder OBD data plus a confirmation prompt for cross-contamination.

---

## 5. Engine change checklist

A new state ships **with** its consumer (signal/noise rule — no orphan categories).

1. **Add the enum value** `OIL_LEAK_INTERNAL` to `ChemicalSignature` (`GAS_VOCABULARY §3`).
2. **Add a signature atlas entry** in `gas_lab_ontology.yaml` (alongside §7.32) with the oil-burn
   bounds from §2. Numbers below are **PROPOSED** and must be pinned to a wiki section before merge
   (suggest a new `GAS_WIKI §8.8 OilLeakSig`, mirroring the existing `CoolantLeakSig.md`):

   ```yaml
   OIL_LEAK_INTERNAL:
     citation: "GAS_WIKI §8.8"          # PROPOSED — author OilLeakSig first
     operating_state: "STABILIZED_IDLE"
     requires_block_test: false         # block test is the COOLANT path; oil uses ECT + localization
     signature:
       hc:     { min: 300,  max: 20000 } # wiki: §8.8 — heavy-HC oil; shared-high with coolant (not a discriminator)
       co:     { min: 0.5,  max: 5.0 }   # wiki: §8.8 — raised by incomplete oil burn  ← vs coolant ≤0.5
       co2:    { min: 0.0,  max: 14.0 }  # wiki: §8.8 — mildly depressed
       o2:     { min: 0.0,  max: 1.5 }   # wiki: §8.8 — normal/low  ← vs coolant high/variable
       nox:    { min: 0,    max: 400 }   # wiki: §8.8 — NOT crushed  ← key vs coolant
       lambda: { min: 0.90, max: 1.03 }  # wiki: §8.8 — stoich/rich  ← vs coolant lean ≥1.0
     differentiator_edges: []            # populate vs WORN_PISTON_RINGS / WORN_VALVE_SEALS
   ```

3. **Add the consumer rule** in `mechanical_wear.json` (new `MW-0xx`, "head-gasket internal oil
   breach"): `chemistry_evidence` GATING on `OIL_LEAK_INTERNAL`; `obd_evidence` SUGGESTIVE on
   `ect_c < 95` (normal temp — the inverse of MW-003) **and** a per-cylinder localization signal.
4. **Add a differentiator** vs `WORN_PISTON_RINGS` / `WORN_VALVE_SEALS` using per-cylinder
   localization + the L1→L2 HC behaviour, so the three oil-burners don't collide.
5. **Surface the cross-contamination check** as a confirmation prompt in the verdict (manual), not a
   gate — the engine separates oil from coolant automatically, then asks the technician to confirm
   the head-gasket origin.
6. **Do not touch** `COOLANT_LEAK_INTERNAL` / `MW-003`. The coolant case keeps its block-test gate
   and lean/quench bounds.

---

## 6. Honest scoping

- **Automatic today:** oil-vs-coolant separation runs on gas (O₂/λ/NOx) + `ect_c`, both already in
  the pipeline. This is the high-value, low-risk half.
- **Needs the per-cylinder channel:** head-gasket-oil vs rings/valve-seals relies on
  `per_cylinder_misfire_counts` / `ltft_cell_vector` — present in the OBD payload but read by a
  COMLab consumer that isn't wired yet.
- **Manual:** coolant-level trend and oil/coolant cross-mix are technician observations. The engine
  should prompt, not assume.

Net: ship the **O₂/λ/NOx + ECT split** first (it cleanly separates oil from coolant and is fully
automatic); add the per-cylinder head-gasket localization as a follow-up once its consumer lands.

---

## Source files

- `labs/gaslab/gaslab/data/gas_lab_ontology.yaml` — §7.32 `COOLANT_LEAK_INTERNAL`, `coolant_intrusion_rule` (priority 87)
- `labs/gaslab/docs/GAS_VOCABULARY.md` §3 — `ChemicalSignature` enum
- `labs/comlab/registry/rules/mechanical_wear.json` — `MW-003` (coolant, GATING + `ect_c > 95`)
- OBD payload fields — `per_cylinder_misfire_counts`, `ltft_cell_vector` (`HLD_OBDLab.md` §7)
- `planning/OIL_CASE_SIGNATURES_5FR.md` — 5-case gas/OBD reference numbers
