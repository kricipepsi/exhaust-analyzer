# 4DLabV2 — Decision Log

Ratified architectural/business decisions for the v2 workspace. Append-only; supersede with a new dated row.

## Ratified 2026-06-05 (owner)

| ID | Decision | Resolution |
|---|---|---|
| **Q-A → D1** | v1 lifecycle + code disentanglement | **v1 is sunset.** Fork-and-freeze is **permanent**: each v1 lab is copied into `4DLabV2/labs/<lab>` and the v1 lab is moved to `ARCHIVE/` **as soon as its v2 lab is built and green** (per-lab archival, not all at once). |
| **Q-B** | T-GV2-14 bank-asymmetry disposition | **VOID from GASLab; re-home to OBDLabV2.** See proposal below. |
| **Q-C** | Where v2 labs live | **Born inside `4DLabV2/labs/`.** Folders for **all** labs created now (gaslab, obdlab, dtclab, comlab, dnalab) + `4dlabwired_v2/` at root — not just gaslab. |
| **Q-D → D5** | FX cross-lab pack | **Kept OUT** of the v2 brain. `FX_START_HERE.md` / `FX_PROGRESS.md` stay at the `4DLab` root, out of scope for this migration. |
| D2 | Consumer repoint timing | **Unchanged — Stage-4 (COMLab).** `4DLabWired`/`registry`/`COMLab` repoint to the forked code during the Stage-4 reconciliation (FU-1/FU-4/T-GV2-2), not during the move. |
| D3 | Canonical wiki `docs/GASLab/wikiNEW/` | **Unchanged — link in place.** Never copy the single source of truth into `4DLabV2`. |
| D4 | Legacy `v2/` (+ `v6/`) | **Ratified — archive** to `ARCHIVE/legacy_v2/` (kills the `v2/` vs `4DLabV2` collision). |

## Proposal — T-GV2-14 (bank-asymmetry) disposition

**Recommendation: VOID it from GASLab scope** (same pattern as the voided T-GV2-11 SAI), and **re-home
the question to OBDLabV2 (Stage 2)**, because:

1. **Signal/noise fails in GASLab.** `number_of_banks` is wiki-flagged *"future"*, read in **0** GASLab
   paths, and **no** bank-asymmetry `ChemicalSignature` exists. "Future use" is not a consumer → it
   does not ship in GASLab.
2. **Physics makes it un-emittable from gas.** A single tailpipe sample is **both banks mixed** — there
   is no per-bank signal in bulk exhaust chemistry. Bank asymmetry is only observable from a channel
   that sees the banks separately.
3. **OBDLab is the natural home.** Per-bank **STFT/LTFT bank1 vs bank2** trim is exactly that channel;
   the consumer is **COMLab fusion** (bank-asymmetry verdict = GASLab+OBD→COMLab, not a GASLab emit) —
   the same fusion pattern the ECU-fault study (`STUDY_ecu_fault_gas_signatures_merge.md`) established.

**Actions when applied (next atomic ledger step, architect):**
- Flip `T-GV2-14` row → `void` in the (migrated) `stage1_gaslab/PROGRESS.md`, with this rationale.
- **Drop `number_of_banks`** from the GASLab DNA-view slice (no GASLab consumer).
- Register a placeholder follow-up in the **OBDLabV2** ledger when Stage 2 starts: *"bank-asymmetry via
  per-bank trim; consumer = COMLab fusion."*

> **Applied 2026-06-05 (Phase-0):** GASLabV2 ledger updated — `T-GV2-14` → `void`, `T-GV2-15` → `done`
> (207 GAS green). `number_of_banks` drop from the GASLab DNA-view slice is carried by the OBDLabV2
> re-home + the Stage-4 consumer reconciliation. Freeze gate now MET.

## Ratified 2026-06-06 (owner, Phase-3 authoring session)

| ID | Decision | Resolution |
|---|---|---|
| **D-V2-9** | **Wired ↔ lab import boundary** (resolves migration **FU-B**) | **Type-mirror isolation.** `apps/wired` mirrors every lab *type* it needs locally (DNA views, payload/contract types, enums) and crosses boundaries via JSON (`model_dump`), importing **no lab type/schema module**. It **retains in-process imports of lab _entry points_ only** (`gaslab.process`/`GasLabContext`, `obdlab.SensorSignalTranslator`, `dtclab.DataFusionSanitizer`, `dnalab.build_vehicle_dna`, `comlab…LabPipelineAggregator`) — the sanctioned composition role (*"composition imports labs, never lab-to-lab"*). The proposal §6.3 phrase *"importing none of them"* is shorthand for this **type-level** decoupling, consistent with `CROSS_LAB_SEQUENCING §4.1` ("mirror the types it needs locally — no cross-lab import; contract changes flow registry → mirrors, reconciled at Stage 4") and root `CLAUDE.md`. A strict zero-import (JSON/subprocess **IPC**) re-architecture is **out of scope** unless the owner later requests it — no current need, large cost, serialization/latency hit. **Migration is unaffected:** `T-RM-3-WIRED` preserves v1 imports. The type-mirror cleanup is **Track-2, Stage-4** work (boundary contracts freeze with COMLab+registry; mirroring against a moving contract is wasted — same logic as D-V2-6). It extends the already-registered wired mapper reconciliation **FU-4** and is registered as **DEP-5** in `CROSS_LAB_DEPENDENCIES.md`. |
| **D-V2-10** | **`*Simple` lab variants** (confirms `CLASSIFICATION.md`; resolves migration **FU-A**) | **All `*Simple/` are dead experiments → ARCHIVE** (COMLabSimple, GASLabSimple, OBDLabSimple, DTCLabSimple — the top-3 line). Not migrated into `labs/`. The only live importer was `4DLabWired` (top-level `from comlabsimple …` in `composition.py`); `T-RM-3-WIRED` is **cut-on-copy** — it brings wired in without the simple subsystem. Unblocks `T-RM-5` to archive all four `*Simple/` (grep-gate each as a *target* first). |

## Still open (see `docs/Brain/QUESTIONS.md`)

None blocking the migration. Stage-2/3/4 architecture choices (OBD revive-vs-quarantine, COMLab
ranker family) are deferred to each stage's start, per the roadmap research gate.

## Ratified 2026-07-06 (owner, via Cowork architect session)
| ID | Decision | Resolution |
|---|---|---|
| **Q-C5-EGR** | dtclab wiki `03_fuel_trim_grammar.md` §3.3 ("High+ at idle, normalises at cruise → Stuck-open EGR") conflicts with cluster5.md + the C5 seed (EGR seeded normal/negative trims, stay-abstained). | **Surface conflict, HOLD ruling.** EGR rows stay abstained; C5B proceeds on +5 with the conflict recorded as an OPEN item (see `v3/v3_tasks/progress_notes/AUDIT_C5-SYNTH_C5A_2026-07-06.md` §OPEN CONFLICT). Neither wiki nor cluster5.md is edited until independently verified with real (authenticated) firecrawl research. |
| **Q-WIKI-FIRST** | Coder re-researched trim signatures already covered by the dtclab wiki. | **Canon amended** — `4DLab_CLAUDE.md` §Provisional-synthetic point 5 is now "Wiki-first, then web-corroborated"; wiki-vs-web conflicts STOP and surface. |
| **Q-GRAPH-LANES** | Nemo refused T-GR-2 (graphify = architect lane per guards); pack was queued across lanes. | **Architect runs all graph BUILD tasks** (T-GR-2..7, T-GR-9; precedent T-COM-GRAPH-AST). Coders get **read-only** graphify queries (`query/explain/path/affected/diagnose`) — guard `lane-guard-no-graphify` narrowed to build subcommands. New guard `lane-guard-no-guard-edit`: coders never edit `.omp/rules/**` (T-GR-1 self-exemption ruled out of bounds; its `Vault/tasks/` annotations stand — that path was never guard-scoped and is those tasks' only home). |
