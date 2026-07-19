# T-SYMGRAPH-WIKI-AUTHOR — Build the canonical SymptomLab wiki corpus from DNA research

**Status:** pending · **Pack:** symptomlab_graph · **Mode:** LITE / architect-author lane (no lab inner-loop/gate)
**Blocked by:** — (needs the research source files in place; see Context. If the owner is still
running the supplemental web research from `WIKI_COVERAGE_RESEARCH_PROMPT.md`, wait for those files.)

> **Lane:** this is **author-lane** work (domain-prose authoring), not coder-lane. No `ruff`/
> `pyright`/`pytest` — the "inner loop" here is the wiki-prep verify pass, which runs in the
> *next* task (T-SYMGRAPH-WIKIPREP). This task only writes `.md`; it does **not** touch
> `symptomlab/` code, and it does **not** run graphify.

### Goal ###

Replace SymptomLab's single reference-only index (`labs/symptomlab/wiki/00_index.md`,
`kg_ingestion: none`) with a **real, chunked, citation-backed wiki corpus** authored from
`labs/dnalab/research/DNAresearch.md` (+ supporting research). The corpus is the Pass-3
extraction source for the `v2_wiki` graph tier. Proof of done: a set of headed `.md` notes
under `labs/symptomlab/wiki/` whose **live** notes carry `kg_ingestion: extract` front-matter
and cite real symptomlab code paths, whose **proposal** content is registered separately under
`labs/comlab/comlab/config/proposals/`, and a rewritten `00_index.md` that routes to them.

### Success criteria ###

This is author-lane, so success is *spec-completeness of the prose*, not green tests:

- `labs/symptomlab/wiki/` contains **≥ 5 chunked notes** (one per major subject, see
  Deliverables), each with valid front-matter and at least one `# source:` citation resolving
  to a real URL or repo path.
- **Live/proposal split is clean and verifiable:** a `grep` for any prior-probability band,
  chemistry-footprint %, or trust-ceiling number returns **zero hits inside the live wiki
  notes** — all such content lives only in the proposals registry note. (This is the
  signal/noise gate, mechanically checkable.)
- The 18-pair catalog and 3 environmental axes in the live notes match
  `labs/symptomlab/symptomlab/data/allowed_combinations.yaml` and `models.py` **exactly**
  (same tier_1/tier_2 ids, same `StrEnum` axis values incl. `load_state`) — no drift.
- `00_index.md` is rewritten: `kg_ingestion: none` → routing index; the false
  "no empirical numeric literals" justification is removed.
- No image placeholders (`![][`) and no flattened tables in any authored note (the source
  blob's tables are restored to real Markdown tables).

### Context ###

**Why this task exists — the previous agent mislabeled the wiki.** The current
`labs/symptomlab/wiki/00_index.md` declares `kg_ingestion: none` and justifies it by claiming
SymptomLab "carries no empirical numeric literals." That premise is false:
`labs/dnalab/research/DNAresearch.md` (32 KB) contains heuristic prior bands (rough idle →
vacuum leak 64% / spark 21% / coil 15%), exhaust-chemistry footprints per fault family (lean
O₂ bias → +249% HC, +150% CO; EGR-stuck → +169% HC), the 35%-CND / 65% trust-ceiling figure,
and the `load_state` axis derivation. That is exactly the measured, citation-backed prose a
canonical wiki owns and that feeds graphify Pass-3. SymptomLab is the "Part B DNA producer"
(`docs/PRD_SymptomLab.md` scope line); this research is its domain.

**Source files (READ-NARROW — these are the spec inputs):**

- `labs/dnalab/research/DNAresearch.md` — the primary source. **Caveat: it is a flattened
  run-on blob** (headers concatenated into sentences, tables collapsed into prose, LaTeX
  inline). Do **not** copy it verbatim — re-chunk it into headed notes and restore the tables.
- `labs/dnalab/research/RESEARCH_PROMPT_symptom_channel_and_prior.md` — the brief that
  produced it (scope/intent reference).
- `labs/dnalab/research/Q8_model_variance.md` — supporting note.
- `planning/symptomlab_graph/WIKI_COVERAGE_RESEARCH_PROMPT.md` — coverage gaps the owner may
  fill with extra web research before this task runs; ingest any new `*.md` the owner drops in
  `labs/dnalab/research/`.

**Ground-truth anchors the live notes must match (read these, narrow):**

- `labs/symptomlab/symptomlab/data/allowed_combinations.yaml` — the 18-pair catalog
  (6 tier_1 × 3 tier_2) + axis enums. The live catalog note is a *prose mirror* of this file.
- `labs/symptomlab/symptomlab/models.py` — `SymptomDNA`, `OccursDuring`, `EngineState`,
  `LoadState` StrEnums. The live axes note mirrors these.
- `labs/symptomlab/wiki/00_index.md` — the note being rewritten (51 lines, whole-read OK).

**Load skills:** none required to author prose. (Do **not** load `4dlab-wiki-prep` here — that
is T-SYMGRAPH-WIKIPREP's job; mixing them is the "cross the streams" anti-pattern.)

### Consumer (signal/noise) ###

This task adds schema surface (wiki notes that assert facts), so the consumer split is the
core deliverable, not an afterthought:

- **LIVE notes — Consumer:** SymptomLab's validator. **Code path:**
  `labs/symptomlab/symptomlab/validator.py` (validates the 18-pair catalog +
  `allowed_combinations.yaml`) and `models.py` (the `LoadState`/`OccursDuring`/`EngineState`
  StrEnums + `SymptomDNA` payload). The live notes describe content this code already reads —
  catalog pairs, axis values, the `len == 18` structural invariant. Real and existing today.
- **PROPOSAL content — Consumer:** COMLab fault-atlas routing
  (`comlab/comlab/core/fault_atlas_router.py:FaultAtlasRouter`). **The registry already exists
  and already covers most of this content — do NOT create a new file and do NOT duplicate.**
  The structured registry is `labs/comlab/comlab/config/proposals/entries.yaml` (schema +
  lifecycle in that dir's `README.md`: fields `id`/`family`/`consumer`/`iso_sae_citation`/
  `status`/`owning_ledger`; lifecycle `proposed → pinned → graduated`). Two relevant entries
  are **already registered as `proposed`**:
  - **`COMLab-A`** — the revised tier_1/tier_2 → fault_family routing mappings
    (consumer `FaultAtlasRouter`).
  - **`COMLab-B`** — the `load_state` context-modifier promotions/demotions **and** the 65%
    trust-ceiling (consumer `FaultAtlasRouter.execute_triage_loop`).
  So the task's proposal work is **reconcile + extend, not create**: verify the wiki's
  proposal-track content agrees with COMLab-A/B, and add **only the genuinely missing**
  material — the **per-tier heuristic prior bands** and the **exhaust-chemistry footprint
  table** — as new schema-conformant entries (e.g. `COMLab-F`/`COMLab-G`) in `entries.yaml`,
  each naming a real `FaultAtlasRouter` code path + `iso_sae_citation`, status `proposed`.
  **Never** merge any of this into the live wiki notes or `allowed_combinations.yaml`.
- **Mechanical gate:** the success-criteria `grep` (no prior/chemistry/ceiling number inside
  `labs/symptomlab/wiki/`) is the enforcement. A number found in a live note = signal/noise
  breach = task not done.

### Deliverables ###

1. `labs/symptomlab/wiki/01_symptom_catalog.md` (CREATE) — the revised 18-pair catalog
   (tier_1 × tier_2) + fault-family mapping + one-line rationale + source links; prose mirror
   of `allowed_combinations.yaml`. **LIVE.**
2. `labs/symptomlab/wiki/02_environmental_axes.md` (CREATE) — the 3 axes (`occurs_during`,
   `engine_state`, `load_state`) with values and the physical derivation of `load_state` from
   `DNAresearch.md`; mirrors `models.py` StrEnums. **LIVE.**
3. `labs/symptomlab/wiki/03_symptom_dna_payload.md` (CREATE) — the 4-field routing-free
   `SymptomDNA` Part-B payload contract. **LIVE.**
4. `labs/symptomlab/wiki/04_catalog_changelog.md` (CREATE) — the legacy→revised changelog
   (KEEP/REWORD/DROP/ADD) with reasons + sources; provenance for why the catalog is shaped as
   it is. **LIVE** (it describes the live catalog's lineage; carries no prior/chemistry numbers).
5. `labs/comlab/comlab/config/proposals/entries.yaml` (MODIFY — extend, do not recreate) —
   add new schema-conformant entries for the **per-tier prior bands** and the **chemistry
   footprint table** (the parts COMLab-A/B don't already cover), each with a real
   `FaultAtlasRouter` consumer path + `iso_sae_citation`, status `proposed`. Reconcile (don't
   duplicate) against existing `COMLab-A` (catalog routing) and `COMLab-B` (load_state +
   trust-ceiling). **NOT a live wiki note.**
6. `labs/symptomlab/wiki/00_index.md` (REWRITE) — routing index over notes 01–04; flip
   `kg_ingestion: none` → `extract`; remove the false "no numeric literals" justification; add
   a pointer to the proposals note for the parked prior/chemistry track.
7. `planning/symptomlab_graph/tasks/progress_notes/T-SYMGRAPH-WIKI-AUTHOR.md` (CREATE) —
   `## Plan` + the live/proposal split decisions + the success-criteria grep output.

### Files to touch ###

- `labs/symptomlab/wiki/00_index.md` (REWRITE)
- `labs/symptomlab/wiki/01_symptom_catalog.md` … `04_catalog_changelog.md` (CREATE ×4)
- `labs/comlab/comlab/config/proposals/entries.yaml` (MODIFY — extend COMLab-A/B; add prior-band + chemistry entries)
- progress note (CREATE)

### Out of scope ###

No `symptomlab/` code edits — the catalog/axes are *mirrored from* code, never the reverse; if
the prose and code disagree, the code is truth and the mismatch is logged as an Unplanned
follow-up, not patched here. No `4dlab-wiki-prep` run (that is T-SYMGRAPH-WIKIPREP). No
graphify (that is T-SYMGRAPH-LLM). No edits to `allowed_combinations.yaml` or `models.py`. Do
**not** promote any proposal content into the live wiki or the live registry/KG. Do **not**
invent priors/chemistry numbers not present in the research source — if a fault family lacks a
chemistry footprint, leave the gap and note it for the research prompt rather than estimating.
Do **not** recreate the proposals registry or duplicate `COMLab-A`/`COMLab-B` — extend
`entries.yaml` only with the missing prior-band/chemistry entries. Do not flip any existing
proposal's `status` (proposed→pinned is the consumer-implementation task's job, not this one).

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab\4DLabV2

# 1. Live/proposal split — MUST return zero hits inside the live wiki
grep -rnE "[0-9]+ ?%|trust ceiling|prior|P\(F" labs/symptomlab/wiki/ ; echo "exit=$? (1 = clean: no numbers leaked into live wiki)"

# 2. No image placeholders / readability gate
grep -rn '!\[\]\[' labs/symptomlab/wiki/ ; echo "exit=$? (1 = clean)"

# 3. Catalog drift check — tier ids in the prose must match the YAML
grep -oE "tier_(1|2)|[a-z_]+_(smoke|smell|idle|crank|stall)" labs/symptomlab/symptomlab/data/allowed_combinations.yaml | sort -u > /tmp/yaml_ids.txt
echo "compare /tmp/yaml_ids.txt against the ids in 01_symptom_catalog.md by eye"

# 4. Front-matter flipped
grep -n "kg_ingestion" labs/symptomlab/wiki/00_index.md   # must read 'extract', not 'none'

# 5. Proposal entries: existing COMLab-A/B intact + new prior/chemistry entries added, all naming a real consumer
grep -nE "id: \"COMLab-[A-Z]\"|consumer:|status:" labs/comlab/comlab/config/proposals/entries.yaml | head -40
#   confirm each new entry's consumer symbol resolves:
grep -rn "class FaultAtlasRouter\|def execute_triage_loop" labs/comlab/comlab/core/fault_atlas_router.py
```

Criterion 1 returning exit 1 (no matches) is the signal/noise proof. Criterion 5 must show
COMLab-A and COMLab-B unchanged plus the new prior/chemistry entries, every `consumer:`
resolving to a real symbol. Paste all five outputs into the progress note.

### Progress hook ###

PROGRESS `T-SYMGRAPH-WIKI-AUTHOR`: Status=done, Files=5 wiki notes + 1 proposal + index,
Verification="live/proposal grep clean; catalog matches YAML; kg_ingestion=extract".
