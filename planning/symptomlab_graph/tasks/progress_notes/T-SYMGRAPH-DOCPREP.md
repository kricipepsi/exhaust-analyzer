## Plan

**Task:** T-SYMGRAPH-DOCPREP — `4dlab-doc-prep` on the six v2 SymptomLab design docs.
**Files to touch:** `labs/symptomlab/graph/v2_docs/ingest_ready/` (six doc subtrees, CREATE), this progress note.
**Verification:** `ls` 6 subtrees + vocab-exclusion check, `grep` CONSUMES/VERIFIES edges and resolve each against `labs/symptomlab/symptomlab/` and `labs/symptomlab/tests/`, `4dlab-doc-prep verify` coverage report.
**Guard at risk:** Currency confirm found 18→21 pair drift across all six docs (code ships 21, docs say 18). Logged as unplanned follow-up — does not block prep (stale count, not a pruned/renamed symbol).
**Approach:** Python explode script via `.venv-wired` for header-splitting (deterministic), then manual tables/anchor/relations passes.

### Currency confirm result

- **18→21 pair invariant mismatch:** `validator.py:36` enforces `len == 21` (7 tier_1 × 3 tier_2 with `oil_consumption`); all six docs describe an 18-pair invariant (6 × 3). The docs are stale — `oil_consumption` (7th tier_1) landed after docs were last refreshed. Stale count, not a renamed/pruned symbol → logged as FU-4, does not block prep.
- **Enum members match AST ground truth:** OccursDuring (4), EngineState (3), LoadState (4) — all correct in docs.
- **SymptomDNA 4-field structure matches** — correct in all docs.
- **`from_json` behavior matches** — correct in HLD §9, DLD §3, LLD §5, ADR-0006, BDD §Feature: JSON boundary.
- **`models.py` docstring still says "18 allowed combinations"** — also stale (see FU-4).
- **All other claims (no routing, no cross-lab imports, open vocabulary via YAML, resolve() signature) match AST ground truth.**

---

### Verification

**4dlab-doc-prep verify — CLEAN (5/5)**

1. **Six doc subtrees present:** ADR(8), BDD(7), DLD(8), HLD(9), LLD(7), PRD(8) = 47 chunks total ✓
2. **Vocab excluded:** `SYMPTOM_VOCABULARY` not in ingest_ready ✓
3. **Anchors:** 47/47 chunks start with `> **Context:**` header (module + parent document + contract) ✓
4. **Relations:** 47/47 chunks have exactly one `## Graph relations (explicit)` block; 188 relation lines total; 35 CONSUMES/VERIFIES/CONSUMED_BY edges ✓
5. **No graph.json:** T-SYMGRAPH-LLM (not this task) writes graph.json; confirmed absent ✓

**Orphan check — ALL EDGES RESOLVE**

35 unique CONSUMES/VERIFIES/CONSUMED_BY edges extracted. Code-path targets verified:
- `symptomlab.resolve` → `symptomlab/__init__.py` resolve()
- `SymptomValidator` → `symptomlab/validator.py` SymptomValidator class
- `SymptomDNA` / `SymptomDNA.tier_1_primary_symptom` / `SymptomDNA.tier_2_subfield_filter` / `SymptomDNA.tier_1/tier_2` → `symptomlab/models.py` SymptomDNA dataclass
- `EnvironmentalConditions.load_state` → `symptomlab/models.py` EnvironmentalConditions dataclass
- `data/allowed_combinations.yaml` → `symptomlab/data/allowed_combinations.yaml` (exists on disk)
- `OccursDuring, EngineState, LoadState` → `symptomlab/models.py` enums
- Test targets (`from_json boundary`, `catalog drift guard`, `import isolation`, etc.) → all five test modules in `tests/unit/` verified present
- COMLab targets (`fault_atlas_router`, `context-modifier prior`) → proposal COMLab-A/COMLab-B (named consumers per PROGRESS, signal/noise satisfied)
- `DNALab build_vehicle_dna` → in-family caller (DNALab→symptomlab flow)

**Currency confirm finding (FU-4):** 18→21 pair invariant drift — `validator.py:36` enforces `len == 21` (`oil_consumption` 7th tier_1 landed); all six docs still describe 18 pairs. Logged as unplanned follow-up.
