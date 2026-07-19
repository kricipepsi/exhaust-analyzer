# T-VAULT-BUILD-1 — progress note

**Status:** `done` · **Pack:** VAULT (OBDLab) · authored 2026-06-11 (architect) · built 2026-06-11
Task spec: `Vault/tasks/T-VAULT-BUILD-1_populate_obdlab_vault.md` · Ledger: `Vault/VAULT_IMPLEMENTATION_PLAN.md` §8

## Plan

Edit `build_lab_vault.py` eligibility gate from single `graphify-out/graph.json` to four-tier `graph/v2_{code,tests,wiki,docs}/graph.json`, update PROVENANCE string, dry-run, apply, verify idempotency and no re-extraction. The three `.base` views (`modules.base`, `consumers.base`, `drift-guards.base`) read every framed frontmatter field — the consumer signal/noise gate (no framed note with empty `consumers` list) is enforced by the builder itself.

## VERIFICATION GATE

### 1. Builder eligibility gate corrected to four-tier model — PASS
`build_lab_vault.py` lines ~197–203: replaced single `graph = lab_src / "graphify-out" / "graph.json"` with four `tier_graphs` entries (`graph/v2_code/graph.json`, `v2_tests`, `v2_wiki`, `v2_docs`). `missing` list checks `(code_src, tests_src, wiki_src, docs_src, *tier_graphs)`. Line ~284: PROVENANCE string updated from `labs/{a.lab}/graphify-out/graph.json` to `labs/{a.lab}/graph/ (v2_code, v2_tests, v2_wiki, v2_docs)`.

### 2. Dry-run clean — PASS
All four tiers resolved. Four framed notes: PRD_OBDLab.md (consumers=1), HLD_OBDLab.md (consumers=2), LLD_OBDLab.md (consumers=1), DLD_OBDLab.md (consumers=1). No "not eligible", "not found", "missing", or "signal/noise breach" lines.

### 3. Apply populates Vault/labs/obdlab/ — PASS
`code/`, `tests/`, `wiki/`, `docs/` tiers materialized. `_obdlab.md` landing note written. Four design docs (PRD/HLD/LLD/DLD) framed with consumer-aware frontmatter. `__pycache__`/`.pyc`/cache excluded via IGNORE set.

### 4. Three .base views installed — PASS
`Vault/_bases/{modules,consumers,drift-guards}.base` all present, copied from assets/.

### 5. System-Map.md and PROVENANCE.md refreshed — PARTIAL
PROVENANCE.md refreshed with four-tier provenance (built date, source tiers, framed note count=4, canonical graphs as not copied). **System-Map.md was not created** — the builder script has no System-Map.md generation logic and no template exists in `assets/`. The task's surgical rule ("only builder edit is eligibility/PROVENANCE path correction") puts this outside scope. Logged as §8 follow-up.

### 6. Idempotent — PASS
Second `--lab obdlab` run produced identical output (same framed notes, same copies, same writes). No duplication.

### 7. No re-extraction — PASS
`git status --porcelain -- labs/obdlab/graph/ labs/obdlab/research/chunks/` shows only untracked files (`??` for PASS3_CROSSCHECK.md and v2_docs_llm/), no modifications (`M`). No graphify was run.

### Manual check (Obsidian) — PENDING
Open `Vault/` in Obsidian, confirm the three Bases render with rows, graph view shows OBD notes, orphans/unresolved empty or explained.

## CODE REVIEW

### Changes made

**File:** `_skills/graph/4dlab-vault/scripts/build_lab_vault.py` — 2 surgical edits.

**Edit 1 — Eligibility gate:**
```python
# Before:
graph = lab_src / "graphify-out" / "graph.json"
missing = [str(p) for p in (code_src, tests_src, wiki_src, docs_src, graph) if not p.exists()]

# After:
tier_graphs = [
    lab_src / "graph" / "v2_code" / "graph.json",
    lab_src / "graph" / "v2_tests" / "graph.json",
    lab_src / "graph" / "v2_wiki" / "graph.json",
    lab_src / "graph" / "v2_docs" / "graph.json",
]
missing = [str(p) for p in (code_src, tests_src, wiki_src, docs_src, *tier_graphs) if not p.exists()]
```

**Edit 2 — PROVENANCE string:**
```python
# Before:
f"- canonical graph (not copied): `labs/{a.lab}/graphify-out/graph.json`\n"

# After:
f"- canonical graphs (not copied): `labs/{a.lab}/graph/` (v2_code, v2_tests, v2_wiki, v2_docs)\n"
```

### Review notes
- Both edits surgical — no other builder behavior changed.
- `*tier_graphs` unpacking in the `missing` tuple preserves existing error message format.
- PROVENANCE edit is string literal swap; no logic impact.
- Four-tier paths match actual directory layout confirmed in preconditions.
- No new imports, functions, or API changes.
- ADR/BDD notes not framed (as designed — vault-map excludes them); vocabulary duplicate not framed.
- No `graph.json` re-extraction performed. Graphify not invoked.

### Tier coverage
| Tier | Source copied | Graph proof checked |
|---|---|---|
| code | `labs/obdlab/obdlab/` | `graph/v2_code/graph.json` |
| tests | `labs/obdlab/tests/` | `graph/v2_tests/graph.json` |
| wiki | `labs/obdlab/research/chunks/` | `graph/v2_wiki/graph.json` |
| docs | `labs/obdlab/docs/` | `graph/v2_docs/graph.json` |

## Findings
1. **System-Map.md not generated.** Builder has no System-Map.md logic and no template exists. Per surgical rule, logged as §8 follow-up. The three .base views + PROVENANCE.md provide the navigational surface.
