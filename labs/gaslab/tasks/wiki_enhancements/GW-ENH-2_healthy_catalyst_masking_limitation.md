# GW-ENH-2 — Healthy-catalyst masking limitation ("filter of truth")

**Type:** wiki enhancement (concept + limitation)
**Scope:** petrol 1990–2010, warm idle, tailpipe 5-gas only
**Sources:** `EP-CAT-02_cat-masking-detection.md`, `EP-CAT-05_pre-cat-inference-engine.md`,
Vol1 "Systemic Masking" / case N-008 (cat-masked oil burn); Denton thermal-damage
figure (~1000 °C) for the urgency note only.

---

## Goal

Document the **inverse** of everything GASWIKI-07 currently covers. Today §7 is rich
on detecting a **failed / weak / poisoned** catalyst (dual-idle test, poisoning
agents, false-P0420 trap). It is silent on the case where the catalyst is **healthy
and is hiding a sick engine** — a healthy three-way cat scrubs the tailpipe evidence
of an engine running **rich** (or lean), so the tailpipe reads clean while the engine
is actually faulting. The guide calls cat-masked rich the single most common
misdiagnosis to defend against: the technician sees clean gas, clears the car, and
the customer drives away with a damaging condition the cat is only temporarily
covering — until the cat itself is overwhelmed or destroyed (thermal damage begins
around ~1000 °C).

The honest, gas-only deliverable is a **CONCEPT + limitation note**, not a new
emittable verdict: state plainly **what tailpipe gas can and cannot see here**, and
hand the resolution to the channels that *can* see it (pre-cat O₂ + LTFT sign,
OBDLab/COMLab; or pre-cat inference from cat ΔT).

> Plain-language note: the catalyst is a chemical scrubber on the tailpipe. When it's
> working, it can clean up a genuinely bad exhaust well enough that the sniffer at the
> pipe looks fine. So "clean tailpipe" is not the same as "healthy engine" — this
> section makes that boundary explicit so the engine never over-claims health.

---

## What to add (exact placements)

### 1. `wiki/07_catalyst_postcat_logic.md` (GASWIKI-07) — new section

Add **§7.8 Healthy-catalyst masking (the "filter of truth" limit)** with anchor
`{#CONCEPT_HEALTHY_CAT_MASKING}`, after §7.7. Content:

- **The mechanism.** A high-OSC, lit-off cat oxidises CO + HC and buffers O₂ swings,
  so a feed-gas fault (leaking injector, high fuel pressure, GDI HPFP leak, oil burn)
  can present at the **tailpipe** with near-normal HC/CO/O₂ and a λ sitting inside the
  cat window (0.97–1.03). The cat is doing its job; that is exactly why the tailpipe
  hides the engine.
- **What tailpipe gas CAN contribute (honest scope).** Usually little on its own — and
  that is the teaching point. Two weak gas tells worth stating, both **suggestive, not
  definitive**: (a) over a long enough rich feed, the cat eventually saturates and
  tailpipe CO/HC begin to climb — by then masking is failing, not absent; (b) the
  dual-idle / RPM behaviour (→ `TEST_DUAL_IDLE_CATALYST` §7.6, → `TEST_RPM_SEPARATION_MATRIX`
  GASWIKI-08) can still expose a *cat* fault, but a **healthy** cat masking a rich
  engine shows no such gas delta — which is the trap.
- **What tailpipe gas CANNOT do.** Confirm or exonerate the engine behind a healthy
  cat from tailpipe 5-gas alone. State this as a hard limitation.
- **Resolution (cross-lab hand-off).** Name the channels that break it, without
  claiming them for GASLab:
  - **pre-cat (upstream) O₂ stuck rich (> ~0.7 V) + negative LTFT at idle and cruise,
    while tailpipe λ is in-window** ⇒ masked rich engine (EP-CAT-02). Pre-cat O₂ and
    LTFT are **OBDLab perception channels → COMLab fusion**, not GASLab inputs.
  - **pre-cat inference from cat inlet/outlet ΔT** (EP-CAT-05) — model the feed-gas
    chemistry from the heat the cat releases; a COMLab L5 step.
- **Routing rule (cross-lab, stated for the consumer).** When tailpipe chemistry is
  clean **but** pre-cat O₂/LTFT indicate rich, COMLab should assert a *masked-rich*
  candidate (e.g. `Catalyst_Masking_Rich`) rather than returning
  `insufficient_evidence` / clean. GASLab's own emission stays the truthful tailpipe
  state; it does **not** fabricate an engine verdict it cannot chemically support.
- **Urgency note.** One line: masked rich can drive cat substrate toward thermal
  damage (~1000 °C, Denton §5) — flag, don't clear. Cite Denton for the figure only.
- Provenance tag inline: `[v2.3: EP-CAT-02, EP-CAT-05; Vol1 N-008]`.
- Update chunk front-matter `entities_defined` (+ `CONCEPT_HEALTHY_CAT_MASKING`) and
  `summary`.

### 2. `wiki/02_combustion_foundations.md` (GASWIKI-02) — one-line cross-ref

In §2.5 (`CONCEPT_CATALYST_WINDOW`), where the wiki says a working cat raises CE to
> 99 %, add a single sentence: this scrubbing also **masks** a feed-gas fault →
`CONCEPT_HEALTHY_CAT_MASKING` (§7.8). Do not duplicate the section.

### 3. `wiki/10_limited_scope_confidence.md` (GASWIKI-10) — limitation note

In §10.4 / §10.5, add a one-line note that a clean tailpipe **downstream of a healthy
cat** is a known confidence limitation (cannot exonerate the engine on gas alone) →
`CONCEPT_HEALTHY_CAT_MASKING`. This keeps the confidence model honest about the trap.

### 4. `docs/GAS_VOCABULARY.md` — light touch only (NO contract change)

> Path note: vocabulary lives in `labs/gaslab/docs/GAS_VOCABULARY.md` (separate vault
> from the `wiki/` chunks; moved out of `wiki/` on 2026-06-10).

This task adds **no** enum, threshold, or field, so the contract surface is
untouched. Per the §18.3 no-drift rule, still make two small, non-contract edits:

- In **§9 `CatalystStatus`**, add a one-line caveat: `LIT_AND_WORKING` describes the
  **catalyst**, not the engine — a healthy cat can mask a rich/lean engine
  (→ GASWIKI-07 §7.8 `CONCEPT_HEALTHY_CAT_MASKING`). Do **not** add a new
  `CatalystStatus` member (a masking cat *is* `LIT_AND_WORKING`).
- Add a **§21 change-log** row noting the concept addition (concept-only, no version
  bump required since no vocabulary member/threshold changed — but the row keeps the
  two docs in sync per §18.3).
- **Confirm** `ChemicalSignature` (§3) is untouched; `Catalyst_Masking_Rich` is a
  **COMLab** candidate named in the wiki prose, **not** a GASLab enum value.

### 5. Glossary + source (GASWIKI-11)

- Add a glossary entry **Healthy-catalyst masking / "filter of truth"** pointing to
  `→ CONCEPT_HEALTHY_CAT_MASKING`, and a source row for EP-CAT-02 / EP-CAT-05.

> Note: there is **no** single-file `GAS_WIKI.md` mirror step — that file was retired
> to ARCHIVE on 2026-06-10. The chunks (`00`–`11`) are the sole canonical form.

---

## Success criteria

- §7.8 `CONCEPT_HEALTHY_CAT_MASKING` exists with: the mechanism; an **honest** "what
  gas can / cannot see" split; the cross-lab resolution naming **pre-cat O₂ + LTFT
  sign** and **pre-cat ΔT inference**; the COMLab routing rule; the thermal-urgency
  line.
- The section makes clear GASLab does **not** emit an engine verdict here on tailpipe
  gas alone — no new `ChemicalSignature` value is added; the 34-value surface is
  unchanged. (`Catalyst_Masking_Rich` is named as a **COMLab** candidate, not a
  GASLab state.)
- Cross-refs added in §2.5 and §10; glossary + source row in GASWIKI-11. (No
  single-file `GAS_WIKI.md` mirror — retired 2026-06-10.)
- `GAS_VOCABULARY.md` §9 caveat + §21 row added; `ChemicalSignature` and
  `CatalystStatus` member lists **unchanged** (no-drift per §18.3).

## Files to touch

- `labs/gaslab/wiki/07_catalyst_postcat_logic.md` (MODIFY — new §7.8)
- `labs/gaslab/wiki/02_combustion_foundations.md` (MODIFY — §2.5 cross-ref)
- `labs/gaslab/wiki/10_limited_scope_confidence.md` (MODIFY — limitation note)
- `labs/gaslab/wiki/11_sources_appendices.md` (MODIFY — glossary + source)
- `labs/gaslab/docs/GAS_VOCABULARY.md` (MODIFY — §9 caveat + §21 row; no contract change)
- ~~`GAS_WIKI.md`~~ — retired 2026-06-10; no mirror edit.

## Verification (docs gate)

- **Readability gate:** `grep '!\[\]\['` = 0 on edited files; full Read; content is
  text, no image-locked figures.
- **Scope honesty:** the section does **not** claim a gas-only verdict; the resolution
  is attributed to OBDLab/COMLab; pre-cat O₂ and LTFT are described as **not** GASLab
  inputs. Confirm `has_catalyst` gating language is consistent with §10.2 scope
  shrinkage (this concept is only meaningful when a cat is present/known).
- **Source fidelity:** masking signature (pre-cat O₂ > ~0.7 V, negative LTFT,
  tailpipe λ 0.97–1.03) matches EP-CAT-02; the ~1000 °C figure is attributed to
  Denton; N-008 cited for the masked-oil-burn precedent.
- **Anchor:** new anchor unique and all `→ CONCEPT_HEALTHY_CAT_MASKING` references
  resolve. (No single-file mirror to check — `GAS_WIKI.md` retired 2026-06-10.)
- **Contract guard:** no new enum member; "34-value" phrasing untouched.

**Verification result (2026-06-10): PASS**

- Readability gate: `rg '!\[\]\['` over the edited files returned 0; the new section is plain Markdown text with no image-locked content.
- Scope honesty: GASWIKI-07 §7.8 states tailpipe 5-gas alone cannot confirm or exonerate the engine behind a healthy cat; pre-cat O₂, LTFT, and cat ΔT are explicitly OBDLab/COMLab evidence, not GASLab inputs. The section is tied to known catalyst presence via the GASWIKI-10 §10.2 `has_catalyst` scope note.
- Source fidelity: the masked-rich signature names pre-cat O₂ > ~0.7 V, negative LTFT at idle/cruise, and tailpipe λ 0.97–1.03 per EP-CAT-02; the ΔT hand-off follows EP-CAT-05; the ~1000 °C urgency figure is attributed to Denton §5; Vol1 N-008 is cited for the cat-masked oil-burn precedent.
- Anchor resolution: `{#CONCEPT_HEALTHY_CAT_MASKING}` appears once; all new `→ CONCEPT_HEALTHY_CAT_MASKING` references point to GASWIKI-07 §7.8.
- Contract guard: no `ChemicalSignature` or `CatalystStatus` enum member was added; `Catalyst_Masking_Rich` is named only as a COMLab candidate in prose, and the "34-value" contract phrasing remains unchanged.

## Deliverables

1. GASWIKI-07 §7.8 `CONCEPT_HEALTHY_CAT_MASKING` (mechanism + can/cannot-see +
   cross-lab resolution + COMLab routing rule + urgency line + provenance).
2. GASWIKI-02 §2.5 and GASWIKI-10 cross-reference notes.
3. GASWIKI-11 glossary + source row.
4. `GAS_VOCABULARY.md` §9 caveat + §21 change-log row (no contract change).
