# T-GAS-PATHS-1 — progress note

**Status:** `done` · **Pack:** VAULT (GASLab) · completed 2026-06-11
Task spec: `Vault/tasks/T-GAS-PATHS-1_parametrize_build_source_paths.md` · Pack ledger: `Vault/tasks/GAS_VAULT_TASKS_START_HERE.md`

## Plan

**Approach (1): Per-lab path config table** (`LAB_SRC_PATHS` dict in `build_lab_vault.py`).
Keyed by lab slug; unknown labs fall back to OBDLab defaults.

**Graph-source decision:** The four-tier `graph/v2_{code,tests,wiki,docs}/graph.json` structure
was already in the code (lines 211-216) and works for both labs. No graph-source parametrization
needed — the eligibility check already requires all four tiers. The task file's line 197 citation
(`graphify-out/graph.json`) was stale; the code had already been updated to four-tier before this task.

### Changes made (3 locations in `build_lab_vault.py`)

| Line | Old (hardcoded OBD) | New (per-lab) |
|---|---|---|
| ~207-209 | `wiki_src = lab_src / "research" / "chunks"` | `paths = LAB_SRC_PATHS.get(...)` + `wiki_src = lab_src / paths["wiki_subpath"]` |
| ~256 | `f"labs/{a.lab}/research/chunks/{note}"` | `paths["wiki_source_template"].format(lab=a.lab, note=note)` |
| ~294 | `wiki=research/chunks` (literal) | `wiki={paths['wiki_subpath']}` |

### LAB_SRC_PATHS table

```python
LAB_SRC_PATHS = {
    "obdlab": {
        "wiki_subpath":          "research/chunks",
        "wiki_source_template":  "labs/{lab}/research/chunks/{note}",
    },
    "gaslab": {
        "wiki_subpath":          "wiki",
        "wiki_source_template":  "labs/{lab}/wiki/{note}",
    },
}
```

## VERIFICATION GATE

### 1. OBDLab regression — structural proof of byte-identity

The OBDLab entry in `LAB_SRC_PATHS` uses the exact same path strings as the old hardcoded values:
- `wiki_subpath` = `"research/chunks"` (same as old literal)
- `wiki_source_template` = `"labs/{lab}/research/chunks/{note}"` which formats to `labs/obdlab/research/chunks/{note}` (same as old f-string)

OBDLab dry-run output (2026-06-11): resolves `research/chunks` → copies to `wiki/`, frames 4 docs
(PRD, HLD, LLD, DLD), installs 3 bases, writes PROVENANCE. Identical to pre-edit behavior.

### 2. GASLab wiki resolution — PASS

GASLab dry-run output (2026-06-11): eligibility check reports only the four missing graph tiers
(`v2_code`, `v2_tests`, `v2_wiki`, `v2_docs`). `labs/gaslab/wiki/` is **not** reported as missing —
confirmed the per-lab path resolves correctly. The graph tiers are legitimately absent (T-GAS-GRAPH-AST
and T-GAS-GRAPH-LLM have not run), so this is the correct eligibility gate, not a path bug.

### 3. Source provenance string — PASS (by template inspection)

GASLab's `wiki_source_template` = `"labs/{lab}/wiki/{note}"`. When T-GAS-VAULT frames a GAS wiki note
(e.g. `labs/gaslab/wiki/00_index.md`), the injected `source:` frontmatter will read
`labs/gaslab/wiki/00_index.md`. Confirmed by template inspection — full end-to-end test requires
T-GAS-VAULT (vault-map.gaslab.yaml not yet authored).

## CODE REVIEW

- **Minimal diff**: 3 hunks, +17 lines (config table + lookup), −3 lines (old hardcoded strings).
- **OBDLab untouched**: The `obdlab` entry reproduces the old hardcoded values exactly.
- **Fallback safe**: Unknown lab slugs default to OBDLab paths via `LAB_SRC_PATHS.get(a.lab, LAB_SRC_PATHS["obdlab"])`.
- **No graphify, no re-extraction, no lab code/tests touched.**
- **Python syntax**: py_compile pass (clean).
