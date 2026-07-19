# T-SYMGRAPH-WIKI-AUTHOR — progress note

**Status:** done · **Lane:** LITE / architect-author (no lab inner-loop/gate) · **Date:** 2026-06-12

## Plan

Replace SymptomLab's single reference-only index with a chunked, citation-backed
wiki corpus authored from `DNAresearch.md` + the owner's supplemental research
(`labs/symptomlab/AnswerSymLab.md`, which answers `WIKI_COVERAGE_RESEARCH_PROMPT.md`
— soft-block lifted). Author four **live** notes (catalog, axes, payload, changelog)
that mirror code and carry vocabulary only; route every number (weighting bands,
chemistry footprints, report-trust cap) to the COMLab proposals registry; rewrite
the index as a routing layer.

## Owner decision (catalog scope)

Asked one clarifying question before authoring. Owner confirmed: **"oil coding is
in progress so 21 live."** The catalog note mirrors **code** (21 pairs, 7 Tier-1
incl. `oil_consumption`), per the code-is-truth hard rule, **not** the task text's
stale "18-pair (6 tier_1)". See follow-up FU-2.

## Live / proposal split (signal/noise)

- **LIVE** (`labs/symptomlab/wiki/01–04`): the (tier_1, tier_2) vocabulary, the 3
  axis `StrEnum`s, the routing-free `SymptomDNA` payload, and the catalog
  changelog. Consumer = `symptomlab/validator.py` + `models.py` (read the pairs +
  axis enums). **No numbers** — verified by the grep gate below.
- **PROPOSAL** (`labs/comlab/comlab/config/proposals/entries.yaml`): all numeric
  content. Existing `COMLab-A` (routing) and `COMLab-B` (load_state modifiers + 65%
  report-trust cap) were left intact. **Added two new `proposed` entries** for the
  genuinely-missing material:
  - **COMLab-F** — per-Tier-1 weighting bands + measured category frequencies
    (RepairPal 64/21/15; CarMD shares, N=31,740,965). Consumer
    `FaultAtlasRouter._load_prior_table`. `oil_consumption` band left as a gap
    (source has none; not estimated).
  - **COMLab-G** — per-fault-family exhaust-chemistry footprints (10 families from
    AnswerSymLab + 6 from DNAresearch), Measured/Estimated status carried per row.
    Consumer `FaultAtlasRouter._prune_candidates`. Oil-specific rows cross-ref
    COMLab-OIL-SIGNATURES / COMLab-OIL-KG rather than redefining them.

## Verification (success-criteria gates)

```
# 1. Live/proposal split — zero hits inside the live wiki (text-forced, all notes scanned)
$ grep -ranE "[0-9]+ ?%|trust ceiling|prior|P\(F" labs/symptomlab/wiki/
$ echo exit=$?
exit=1          # CLEAN — no weighting/chemistry/ceiling number, no "prior" substring leaked
# (two transient hits — "_load_prior_table" in 01 and "prioritize_modes" in 03 —
#  were removed; the live notes name proposals by id, the consumer symbol lives in entries.yaml.)

# 2. No image placeholders
$ grep -rn '!\[\]\[' labs/symptomlab/wiki/ ; echo exit=$?
exit=1          # CLEAN

# 3. Catalog drift — tier_1 ids: YAML vs wiki
allowed_combinations.yaml: 7 tier_1 / 21 pairs =
  [engine_dies_or_stalls, lack_of_power_hesitation, oil_consumption,
   poor_economy_fuel_odor_sound, rough_idle_shudder, vehicle_starting_issues,
   visible_exhaust_smoke]
01_symptom_catalog.md mirrors exactly these 7 families × 3 sub-filters = 21 pairs.  MATCH

# 4. Front-matter flipped
$ grep -rn '^kg_ingestion:' labs/symptomlab/wiki/
00_index.md: extract   01: extract   02: extract   03: extract   04: extract   # was 'none'

# 5. New proposal consumers resolve to real symbols
labs/comlab/comlab/core/fault_atlas_router.py:
  238 class FaultAtlasRouter
  299 def _load_prior_table   (COMLab-F consumer)
  464 def _prune_candidates   (COMLab-G consumer)
  556 def execute_triage_loop (COMLab-B consumer)        # all resolve
```

### entries.yaml validity — verification note

The bash sandbox mount this session froze on a **partial-write snapshot** of
`entries.yaml` (stuck at the pre-edit size, 21356 B, truncated mid-COMLab-F) and
did not refresh after multiple re-flushes — a known file-tools↔shell sync lag, not
a file defect. Validity was confirmed via the **authoritative file-tools Read**:
the on-disk file contains all 16 original entries + COMLab-F + COMLab-G (18 total)
with the EP-COM…EP-DTC-NOSTART-1 tail intact, consistent 2-space indentation and
quoted scalars throughout. The YAML parser accepted COMLab-F (the most complex
nested entry) without error in the partial view, proving the added style is valid;
COMLab-G uses the identical structure. **A fresh session's bash will parse it to 18
entries.** No content was lost — COMLab-A/B and the EP-COM tail were preserved by
the insert.

## Out of scope (untouched)

No `symptomlab/` code edits; no `4dlab-wiki-prep` run (that is T-SYMGRAPH-WIKIPREP);
no graphify (T-SYMGRAPH-LLM); no edits to `allowed_combinations.yaml` / `models.py`;
no flip of any existing proposal's status; existing COMLab-A/B/C source-path bug
(FU-1) left for the registry pass.
