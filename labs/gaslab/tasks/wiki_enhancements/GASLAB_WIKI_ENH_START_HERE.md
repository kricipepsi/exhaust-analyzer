# GASLab Wiki-Enhancement Pack — START HERE

**Author:** architect (4DLab) · **Date:** 2026-06-10
**Driver:** owner request — mine `labs/obdlab/research/` (proposals, the Denton
`AdvAutomotiveFaultDiagnosis_VIABLE_prepped.md`, and `formula-wiki/`) for
gas-chemistry improvements **viable for the GASLab wiki**, then spec them for a coder.
**Target wiki (canonical):** `labs/gaslab/wiki/` (v2, 34-value contract).
**Viability bar (owner):** an improvement ships only if it adds **more diagnostic
capability than noise** to the engine.
**Consumer rule (owner override, this pack only):** *do not block on naming a live
consumer.* If an improvement is viable, author it; consumer wiring is "adjusted up
the chain" later. Candidate consumers are still noted where obvious, so the later
wiring is cheap — but a missing consumer is **not** a reason to defer here. This
overrides the standing signal/noise "named-consumer-or-it-doesn't-ship" gate **for
the authoring of these wiki rows only**, by explicit owner instruction.

> Plain-language note for the owner: "consumer" = the later piece of code that
> actually reads the new value. Normally we refuse to add a value with no reader.
> You've waived that for this pass, so this pack adds the *knowledge* (wiki) now
> and leaves the reader for a follow-up.

---

## What this pack is

A small, deliberately tight set of **wiki-enhancement tasks**. Each task adds a
specific, sourced piece of gas-chemistry reasoning that is **missing from the
current v2 wiki** and clears the signal-over-noise bar. The full inventory of
everything considered — including what was **rejected and why** — is in
`TRIAGE_research_to_gaslab_wiki.md`. Read the triage first; it is the evidence
behind this ledger.

The headline finding mirrors the OBDLab passes: the GASLab v2 wiki is already
**mature**. Brettschneider + reliability model, the inter-gas grammar, the oil-burn
sub-modes, the dual-idle catalyst test, the catalyst poisoning agents, the
RPM-separation matrix and the probe-occlusion test are all already in. The research
yields only **two** genuinely net-new, gas-only, signal-positive additions.

---

## Ledger

| ID | Task file | Adds | Scope | Status | Blocked by |
|---|---|---|---|---|---|
| GW-ENH-1 | `GW-ENH-1_combustion_integrity_metrics.md` | Two quantified gas-derived metrics: `chemical_efficiency = CO₂/(CO₂+CO)` and the `oxygen_usage` (O₂ vs CO) misfire-vs-rich discriminator | wiki chunks (GASWIKI-02, -04, -11) + **`GAS_VOCABULARY.md` §10.9/§15/§21, v2.2 bump** + optional code stub | done | — |
| GW-ENH-2 | `GW-ENH-2_healthy_catalyst_masking_limitation.md` | A documented **healthy-catalyst masking** limitation ("filter of truth") — a healthy cat hides a rich/lean engine; what tailpipe gas can and cannot see | wiki chunks (GASWIKI-07, -02, -10, -11) + **`GAS_VOCABULARY.md` §9 caveat (no contract change)** — concept + cross-lab resolution | done | — |
| GW-ENH-3 | `GW-ENH-3_vocab_path_and_citation_cleanup.md` | **Housekeeping (run first).** Repoint `test_validators.py` to `docs/GAS_VOCABULARY.md` (the suite is currently red — old `docs/wiki/` path is empty); sweep 85 stale `wikiNEW` comment citations to `GASWIKI-<chunk>` form | **code** (`tests/unit/test_validators.py`, `gaslab/resolution.py`, `gaslab/rule_engine.py`) — STRICT inner loop | done | — |

> **`GAS_VOCABULARY.md` is in scope for both tasks.** It lives in
> `labs/gaslab/docs/GAS_VOCABULARY.md` — a **separate vault** from the wiki chunks in
> `labs/gaslab/wiki/` (moved out of `wiki/` on 2026-06-10). Its §18.3 rule requires
> every vocabulary change to land in **both** the GAS wiki chunks (`wiki/00`–`11`) and
> `docs/GAS_VOCABULARY.md` in the same commit. (The single-file `GAS_WIKI.md` mirror was
> retired to ARCHIVE on 2026-06-10, so there is no third copy to sync.) GW-ENH-1 adds
> a derived-metric threshold block (minor v2.2 bump, no enum/payload change); GW-ENH-2
> is concept-only (a one-line §9 caveat + a §21 row, no contract change). Neither
> touches the 34-value `ChemicalSignature` surface.

**Status values:** `pending` · `in_progress` · `done` · `deferred` · `void`
**Ordering:** **run GW-ENH-3 first** — it is code housekeeping that un-breaks the test
suite (the `docs/wiki/` vocab path is empty after the 2026-06-10 vault reorg, so
`test_validators.py` currently fails). GW-ENH-1 and GW-ENH-2 are independent of each
other and of GW-ENH-3, but a green suite makes their (optional) code stubs verifiable.
One task per session per the workspace rule.

> **Note on task types.** GW-ENH-1/-2 are **wiki-content** tasks (docs gate; optional
> code stub). GW-ENH-3 is a **code** task (full STRICT `ruff`/`pyright`/`pytest` inner
> loop) — it changes test/code path strings and comments, no diagnostic logic.

---

## How a coder runs a task here

1. Read this file, then `TRIAGE_research_to_gaslab_wiki.md`, then the task file.
2. These are **wiki (spec) edits**, not behaviour changes to shipped code. The
   inner loop (`ruff`/`pyright`/`pytest`) does **not** apply to a docs-only edit —
   the gate is the **document readability + source-fidelity** check named in each
   task's *Verification* block. If a task also opts into the optional code stub,
   the standard STRICT inner loop applies to that part only.
3. **Do NOT run graphify.** Same rule as the main pack: the KG is off the runtime
   path; re-extraction is a separate, owner-instructed `T-GV2-KG` job only.
4. Keep scope **petrol 1990–2010, warm idle, tailpipe 5-gas only.** Anything that
   needs pre-cat O₂ switching, backpressure, IR temp, cranking or cold-start data
   is **not** GASLab — it routes to OBDLab/COMLab (the triage says which).
5. Fill the task's *Verification* block, flip the row to `done`, STOP.

## Source map (where each addition comes from)

- `labs/obdlab/research/proposals/extracted/EP-GAS-03_combustion-integrity-metrics.md`
- `labs/obdlab/research/proposals/extracted/EP-CAT-02_cat-masking-detection.md`
- `labs/obdlab/research/proposals/extracted/EP-CAT-05_pre-cat-inference-engine.md`
- `labs/obdlab/research/formula-wiki/01_gas-chemistry-lambda.md` (cards F-GAS-04, F-GAS-05)
- `labs/obdlab/research/proposals/wikiResearch.md` §4 (5-gas integration gap)
- Denton `AdvAutomotiveFaultDiagnosis_VIABLE_prepped.md` (cat thermal-threat figure only)
