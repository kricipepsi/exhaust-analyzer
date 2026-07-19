# GPF Removal — Cross-Lab Ledger

> **Coder session start → read `GPF_REMOVAL_START_HERE.md` first** (it sets the
> CODER role, the sandbox-Python + inner-loop bootstrap, and the ledger-picks-the-
> task rule). This ledger is the source of truth for *which* task; START_HERE is
> *how* to run it.

> **Owner ruling (2026-06-11):** GPF / gasoline-particulate-filter content is
> **out of scope** (1990–2010, Euro 1–5). Remove it from **all code and
> documents**. This pack is the architect's spec for that removal. A separate
> coder session implements one task per session, ledger-picks-the-task.

**Date authored:** 2026-06-11 · **Author:** architect · **Pack home:** `planning/gpf_removal/`

## Why this pack exists (the conflict it resolves)

GPF was simultaneously **declared dead** in the DTCLab wiki yet **kept alive**
as a wired consumer across the spine:

- **DTCLab wiki** (`labs/dtclab/wiki/08_forced_induction_gdi.md`,
  `11_proposals_register.md §11.4`) already lists GPF (P2452, P244A, P2459) and
  LSPI (P0324) as **out of the 1990–2010 scope — "dead weight… drop them."**
- **The code never followed.** DTCLab still emits the `GPF_HISTORY` routing tag
  (a routing tag is the label DTCLab hands COMLab to say "this kind of fault was
  seen"); COMLab still consumes it; VINLab still decodes the
  `has_particulate_filter` flag that feeds it; and two recent tasks
  (`T-FX-DTCHEX-1`, `T-TST-9`) reinforced the P244A→`GPF_HISTORY` path.

So GPF is not an orphan you can delete in one spot — it is a **producer→consumer
chain** spanning five labs plus the wired app. This pack removes the whole chain
in dependency order.

## The chain being removed

```
VINLab decoder.py / models.py            ← SOURCE: decodes has_particulate_filter
        │                                   (has_gdi AND euro_norm) per OBD_VOCAB §13.5
        ▼
DNALab VehicleDNA  ──────────────────►  COMLab ingestion.py / projection.py / lab_dna_views.py
        │   (carries the bool flag)        ← READERS: copy has_particulate_filter into
        │                                     COMLab's own mirrored view
        │                                  wired composition.py / app.py
        │                                     ← READER: surfaces the flag in the UI layer
        ▼
DTCLab dna_view.has_particulate_filter
        │
        ▼  gpf_combined gate (routing_tag_mapper.py)
        │  = has_particulate_filter AND resolved_horizon == HORIZON_MODERN
        ▼
   emits GPF_HISTORY  ───────────────►  COMLab vocabulary.py (enum), tag_discriminator.yaml,
   (P244A, P2459)                          global_fault_registry.json ERR-CF-003
                                           ← CONSUMERS of the tag / P-codes
```

**Removal order rule:** strip the *tag consumers and emitters* first, then the
*field readers*, then the *field at its source* last. Deleting the VINLab field
before its readers are gone would break every downstream lab mid-flight. The
DAG below enforces that.

## Two caveats the coder must not get wrong

1. **The hex DTC regex STAYS.** `T-FX-DTCHEX-1` (done) widened COMLab's
   `DTC_REGEX` from `[0-9]{3}` to `[0-9A-F]{3}` so hex-tailed codes like `P244A`
   parse at all. That widening is justified by **wiki §2.3 for all hex codes**,
   not only GPF. **Do not narrow it back** — other valid hex-tailed codes depend
   on it. Only the GPF *routing* and *fixtures* go; the regex is untouched.
2. **`catalyst_flow_restriction` (registry `ERR-CF-003`) is a real fault — it
   stays.** It is a catalyst-flow fault that merely *also* lists `P244A`/`P2459`
   in `p_code_match` and mentions "GPF soot overload" in its UI string. Keep the
   fault and `P0420`; **strip only** the two GPF P-codes and the GPF wording. Do
   **not** delete the fault or change its `target_horizons`.

## Signal/noise compliance

This is a **removal**, so the signal/noise rule is satisfied by elimination:
once `GPF_HISTORY` and `has_particulate_filter` are gone, there is no field
without a consumer. The anti-orphan check still applies in reverse at each
step — after a task, `grep` must show **zero** live readers of the symbol it
removed (outside regenerated graph artefacts).

## Task DAG

```
T-GPF-RM-1 (DTCLab: stop emitting tag + drop own field read)
      │
      ▼
T-GPF-RM-2 (COMLab: drop GPF_HISTORY enum, discriminator, registry P-codes)
      │
      ▼
T-GPF-RM-3 (COMLab: stop reading has_particulate_filter — projection/ingestion/views)
      │
      ├──────────────► T-GPF-RM-4 (wired + semantic + obdlab vocab: drop field/refs)
      │                       │
      ▼                       ▼
T-GPF-RM-5 (VINLab + DNALab: remove has_particulate_filter at SOURCE;
            annotate T-FX-DTCHEX-1, amend T-TST-9 spec) — runs LAST
```

RM-5 is blocked by RM-1, RM-3, **and** RM-4 (all readers gone before the source
is cut) and closes only when the **whole repo is green** (VINLab strict gate).

## Ledger

| ID | Task file | Status | Blocked by | Scope (one line) |
|---|---|---|---|---|
| T-GPF-RM-1 | `tasks/T-GPF-RM-1_dtclab_strip_gpf.md` | done | — | DTCLab: remove `GPF_HISTORY` enum, `gpf_combined` gate, `has_particulate_filter` field, routing_tag_map + family_map entries, `case_06_gpf_p244a` fixture, BDD P244A scenario, GPF refs in the 6 design docs. |
| T-GPF-RM-2 | `tasks/T-GPF-RM-2_comlab_tag_routing_registry.md` | done | T-GPF-RM-1 | COMLab tag side: drop `GPF_HISTORY` from `vocabulary.py`, the `tag_discriminator.yaml` block, strip P244A/P2459 + GPF wording from `global_fault_registry.json` ERR-CF-003 and `kg/catalyst_failure.json`; update COMLab wiki DTC_VOCABULARY/OBD_VOCABULARY + COMLab_LLD; fix `test_error_codes`, `test_tag_discriminator`. |
| T-GPF-RM-3 | `tasks/T-GPF-RM-3_comlab_dna_field_readers.md` | done | T-GPF-RM-2 | COMLab field readers: remove `has_particulate_filter` from `lab_dna_views.py`, `ingestion.py`, `projection.py`; update `SEMANTIC_CONTRACT.md`, `COMLab_Horizon_Eras.md`; fix `test_projection`. |
| T-GPF-RM-4 | `tasks/T-GPF-RM-4_wired_semantic_obd.md` | done | T-GPF-RM-1 | Wired app (`composition.py`, `app.py`, `test_composition.py`), semantic vocab files, and obdlab `OBD_VOCABULARY.md §13.5` / wired field-map: drop the field and all GPF references. |
| T-GPF-RM-5 | `tasks/T-GPF-RM-5_vinlab_dnalab_source_and_reversals.md` | done | T-GPF-RM-1, T-GPF-RM-3, T-GPF-RM-4 | VINLab `decoder.py`/`models.py` + DNALab models/fixtures: remove `has_particulate_filter` at source. Annotate `T-FX-DTCHEX-1` (regex stays, GPF no longer its consumer); amend `T-TST-9` spec to drop GPF cases. Closes only on whole-repo green. |

## Out-of-scope / not touched

- **Graph artefacts** (`graph/*/graph.json`, `graphify-out/`) regenerate from
  code; they are **not** hand-edited. They self-clear on the next graphify run —
  do **not** re-run graphify as part of this pack.
- **`v1_baseline` graphs and `ARCHIVE/`/`v2/`/`v6/`** — legacy, never edited.
- **HORIZON_MODERN itself** — the horizon model stays; only the GPF content that
  rode on it is removed.

## Unplanned follow-ups (discovered, not in this pack's diff)

| Item | Where | Note |
|---|---|---|
| `has_gdi` decode logic in VINLab | `vinlab/decoder.py` | Feeds the GPF computation. GDI is **in scope** (era B) — keep it; only the `has_particulate_filter` derivation that consumes it goes. Flag if it becomes orphaned. |
| Euro-6+/LSPI (P0324) references | various wikis | Same out-of-scope class as GPF but a separate phenomenon; not in this pack. Track separately if found in code. |
| GPF residuals in Vault | `Vault/tasks/` (3 task specs), `Vault/_vocabulary/OBD_VOCABULARY.md` | Mention `gpf_combined`/`has_particulate_filter` as historical examples or mirrors. Out of scope for this pack; self-documenting Vault artefacts. |
| GPF in wired/docs + components.jsx | `apps/wired/docs/`, `apps/ui/UI design/components.jsx` | Documentation and UI design mockups with GPF references. Not in any task file list. |
| GPF in COMLab docs | `labs/comlab/docs/COMLab_PRD.md`, `labs/comlab/docs/COMLab_HLD.md` | Historical architecture docs with GPF mentions. Not in any task file list (COMLab wiki/docs that were cleaned were the ones explicitly named). |
