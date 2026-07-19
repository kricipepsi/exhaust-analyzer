# GW-ENH-1 — Combustion-integrity quantified metrics (chemical_efficiency + oxygen_usage)

**Type:** wiki enhancement (spec) · optional code stub
**Scope:** petrol 1990–2010, warm idle, tailpipe 5-gas only
**Sources:** `EP-GAS-03_combustion-integrity-metrics.md`; formula-wiki `F-GAS-04`,
`F-GAS-05` (`01_gas-chemistry-lambda.md`); Vol1 "Combustion Integrity Truth";
`chunks/truth-perception/04`; `wikiResearch.md` §4.

---

## Goal

Add two **quantified, gas-derived metrics** to the GASLab wiki that today exist only
as narrative judgments. Both are computed from the **existing five gases** — no new
input, no new sample, no new enum value.

1. **Chemical / combustion efficiency** — a combustion-failure score:

   ```
   chemical_efficiency = CO₂ / (CO₂ + CO)        (both in vol %)
   healthy → near 1.0  (≥ ~0.95);  low → fundamental combustion failure
   ```

   It answers the **Quality** axis (→ `CONCEPT_TWO_TRUTHS`, §2.6) numerically: a low
   value means carbon is not being fully oxidised — pumping loss, misfire, bad
   timing — **regardless of the fuelling ratio / λ**.

2. **Oxygen-usage discriminator** — a misfire-vs-rich separator on the O₂↔CO pair:

   ```
   high O₂ + high HC/CO   → MISFIRE   (both reactants escape unburned)
   high CO + O₂ ≈ 0        → pure RICH over-fuelling
   ```

   This is the **quantified form** of the qualitative seesaw (`RULE_SEESAW`, §4.5)
   and truth table (`RULE_HC_O2_CO_TRUTH_TABLE`, §4.6): it states *why* "rich AND
   lean at once" resolves to misfire (combustion never happened) rather than a
   mixture error.

> Plain-language note: "metric" here just means a number the engine derives from the
> gases it already has — like a fuel-economy score computed from a receipt you
> already hold, not a new measurement.

---

## What to add (exact placements)

### 1. `wiki/02_combustion_foundations.md` (GASWIKI-02) — new section

Add a section **§2.10 Combustion-integrity metrics** with anchor
`{#CONCEPT_COMBUSTION_INTEGRITY}`, after §2.9. Content:

- The `chemical_efficiency = CO₂/(CO₂+CO)` formula card (ASCII block), with the
  healthy band **≥ ~0.95** and the reading rule: low CE = combustion failure
  independent of λ. Worked anchors (from the §11.2.1 idle reference, keep
  consistent): healthy idle CO₂ ≈ 14.7 %, CO ≈ 0.6 % → CE ≈ 0.96; severe rich
  CO ≈ 5 %, CO₂ ≈ 10 % → CE ≈ 0.67.
- The `oxygen_usage` discriminator (O₂ vs CO), stated as the qualitative rule above
  — **do not invent a numeric ratio threshold**; F-GAS-05 is explicitly qualitative
  (Vol1 prose). Frame it as the quantified basis of `RULE_SEESAW` / the truth table.
- Cross-refs: `→ CONCEPT_TWO_TRUTHS` (§2.6), `→ RULE_SEESAW` (§4.5),
  `→ RULE_HC_O2_CO_TRUTH_TABLE` (§4.6), `→ RULE_MASKING` (§4.8).
- Provenance tag inline: `[v2.3: EP-GAS-03 / F-GAS-04, F-GAS-05]`.
- Update the chunk front-matter `entities_defined` to include
  `CONCEPT_COMBUSTION_INTEGRITY`, and `summary` to mention the two metrics.

### 2. `wiki/04_inter_gas_grammar_validity_gates.md` (GASWIKI-04) — wire in

In §4.5 (`RULE_SEESAW`) and §4.6 (truth table), add a one-line cross-ref that the
**quantified** form of these discriminators is `→ CONCEPT_COMBUSTION_INTEGRITY`
(§2.10). Do **not** duplicate the formula; just link, to keep one-concept-per-section.

### 3. `wiki/11_sources_appendices.md` (GASWIKI-11) — glossary + sources

- Extend the glossary entry **CE** to name the explicit formula
  `CO₂/(CO₂+CO)` and point to `→ CONCEPT_COMBUSTION_INTEGRITY`.
- Add a glossary entry **Oxygen-usage** (O₂-vs-CO misfire/rich discriminator).
- Add a v2 research-dossier source row: `EP-GAS-03 / formula-wiki F-GAS-04, F-GAS-05`
  → integrated into GASWIKI-02 §2.10.

### 4. `docs/GAS_VOCABULARY.md` — formal vocabulary (REQUIRED, per §18.3)

> Path note: the vocabulary lives in `labs/gaslab/docs/GAS_VOCABULARY.md` — a
> **separate vault** from the wiki chunks in `labs/gaslab/wiki/` (moved out of `wiki/`
> on 2026-06-10). Edit the copy in `docs/`.

`GAS_VOCABULARY.md` is the enum/threshold companion and its own §18.3 rule mandates
that any vocabulary change land in **both** `GAS_WIKI.md` and `GAS_VOCABULARY.md` in
the same commit. This addition is a **backwards-compatible** derived-metric addition
(§18.1 → minor version bump), **not** an enum or payload change. Add:

- A new **§10.9 `chemical_efficiency` (dimensionless)** threshold block, in the same
  YAML style as §10.6 `volumetric_sum` / §10.7 `lambda_chem` / §10.8 `fuel_trim`:
  `healthy: { min: 0.95 }`, `combustion_deficit: { max: 0.95 }` (band from F-GAS-04 /
  Vol1 prose; cite GASWIKI-02 §2.10). State it is a **derived** metric (computed from
  `gas_co2` + `gas_co`), not an analyser channel.
- In the **same §10.9** (or a short §10.10), the `oxygen_usage` O₂-vs-CO discriminator,
  stated **qualitatively** (no invented numeric threshold) — it shares the §10.2/§10.4
  CO/O₂ bands; "no new numbers" note like §10.8.
- Two rows in the **§15 internal-vs-emitted summary table**: `chemical_efficiency` and
  `oxygen_usage` → *used internally: yes; in `GasLabPayload`: no (derivable)*, Source
  §10.9 — exactly as `volumetric_sum` is handled.
- A **§21 change-log** row and a **version bump v2.1 → v2.2** (header + §21).
- **Do not** touch §3 (`ChemicalSignature` stays 34) or §12 (`GasLabPayload`) — these
  are internal derived metrics. They enter §12 only if the optional consumer stub
  (below) is wired, which is a separate, owner-gated contract step.

### 5. ~~`wiki/GAS_WIKI.md` mirror~~ — RETIRED (no longer applicable)

The single-file `GAS_WIKI.md` mirror was archived on 2026-06-10. The chunks
(`00`–`11`) are the sole canonical form, so there is **no mirror step**: edit the
chunk(s) above and `GAS_VOCABULARY.md` only. Do not recreate the single file.

### 6. (Optional, owner's call) candidate consumer note — not required to ship

Per the pack's consumer override, you may **stop at the wiki**. If the owner wants
the reader wired in the same change, the natural, already-named candidate consumers
(from EP-GAS-03) are the COMLab **misfire-vs-fuelling gate** (`EP-COM-07`) and the
**fault_atlas misfire family** — i.e. `chemical_efficiency` and the O₂-usage call
become two more corroborating channels behind the existing misfire route. If wired,
the metric functions belong in GASLab's resolver alongside `lambda_chem`, every
numeric literal carries the §2.10 wiki cite, and the STRICT inner loop applies.

---

## Success criteria

- §2.10 exists in `02_combustion_foundations.md` with anchor
  `{#CONCEPT_COMBUSTION_INTEGRITY}`, both metrics, the CE healthy band ≥ ~0.95, and
  the worked anchors above.
- The O₂-usage rule is stated **qualitatively** (no fabricated numeric threshold).
- §4.5 and §4.6 link to §2.10; no formula duplicated.
- Glossary (CE updated + Oxygen-usage added) and a source row present in GASWIKI-11.
- **`GAS_VOCABULARY.md` updated** (§10.9 `chemical_efficiency` block + `oxygen_usage`
  note, §15 rows, §21 change-log, version bump v2.1 → v2.2) — required by its §18.3
  no-drift rule.
- Front-matter `entities_defined` / `summary` updated in GASWIKI-02.
- **No new `ChemicalSignature` value** and **no `GasLabPayload` change** (these are
  derived/internal metrics) — the 34-value contract surface is unchanged.

## Files to touch

- `labs/gaslab/wiki/02_combustion_foundations.md` (MODIFY — new §2.10)
- `labs/gaslab/wiki/04_inter_gas_grammar_validity_gates.md` (MODIFY — cross-refs)
- `labs/gaslab/wiki/11_sources_appendices.md` (MODIFY — glossary + source)
- `labs/gaslab/docs/GAS_VOCABULARY.md` (MODIFY — §10.9 + §15 + §21, version bump)
- ~~`GAS_WIKI.md`~~ — retired 2026-06-10; no mirror edit.

## Verification (docs gate — replaces inner loop for the wiki edit)

- **Readability gate (CLAUDE.md):** `grep '!\[\]\['` on every edited file = 0; full
  Read confirmed (no truncation); the §2.10 formula present as **text/ASCII**, not an
  image.
- **Source fidelity:** the CE formula is exactly `CO₂/(CO₂+CO)`; the O₂-usage rule
  matches F-GAS-05 / Vol1 prose; no numeric bound was invented beyond the
  prose-stated ≥ ~0.95.
- **Anchor resolution:** every new `→ CONCEPT_COMBUSTION_INTEGRITY` reference
  resolves; the new anchor is unique.
- **Contract guard:** `grep` confirms no new enum member added; "34-value" phrasing
  elsewhere in the wiki is untouched; `GasLabPayload` (§12) unchanged.
- **No-drift check (§18.3):** the metric definition appears in **both** the chunk set
  and `GAS_VOCABULARY.md`; the §21 change-log row and version bump are present in
  `GAS_VOCABULARY.md`. (No single-file mirror exists — `GAS_WIKI.md` retired
  2026-06-10.)
- If the optional code stub was taken: STRICT inner loop (`ruff` → `pyright` →
  `pytest -x -q`) green; the two metric functions are grep-confirmed read in a live
  path.

**Verification result (2026-06-10): PASS**

- Readability gate: `rg '!\[\]\['` over all four edited files returned 0; the §2.10 formula is plain text/ASCII-style Markdown, not an image.
- Source fidelity: `chemical_efficiency = CO₂/(CO₂+CO)` is present; `oxygen_usage` remains qualitative and reuses existing CO/O₂ bands without a new numeric ratio threshold.
- Anchor resolution: `{#CONCEPT_COMBUSTION_INTEGRITY}` appears once; all new `→ CONCEPT_COMBUSTION_INTEGRITY` references point to GASWIKI-02 §2.10.
- Contract guard: `git diff -U0` shows no added `ChemicalSignature` enum members and no `GasLabPayload` schema edits; the 34-value contract surface remains unchanged.
- No-drift check: the metric definition appears in GASWIKI-02 and `docs/GAS_VOCABULARY.md`; §15 rows and the §21 v2.2 change-log row are present.
- Optional code stub: not taken; this session was docs/vocabulary only.

## Deliverables

1. GASWIKI-02 §2.10 `CONCEPT_COMBUSTION_INTEGRITY` (both metrics + bands + worked
   anchors + cross-refs + provenance tag).
2. GASWIKI-04 cross-references from §4.5 / §4.6.
3. GASWIKI-11 glossary + source-row updates.
4. `GAS_VOCABULARY.md` §10.9 metric block + §15 rows + §21 change-log + v2.2 bump.
