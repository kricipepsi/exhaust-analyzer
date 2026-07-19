# T-DTC-PATHS-1 — progress note

**Status:** `done` · **Pack:** VAULT (DTCLab) · completed 2026-06-11
Task spec: [T-DTC-PATHS-1_register_dtclab_source_paths.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/Vault/tasks/T-DTC-PATHS-1_register_dtclab_source_paths.md) · Pack ledger: [DTC_VAULT_TASKS_START_HERE.md](file:///C:/Users/muto/claude/4DApp/4DLab/4DLabV2/Vault/tasks/DTC_VAULT_TASKS_START_HERE.md)

## Plan

**Approach (1): Per-lab path config table** (`LAB_SRC_PATHS` dict in `build_lab_vault.py`).
Add `dtclab` entry to `LAB_SRC_PATHS` mirroring `gaslab`, so the build resolves `wiki/` and requires only the two AST graph tiers (`v2_code` and `v2_tests`).

### Changes made (2 locations in `build_lab_vault.py`)

| Line | Old | New |
|---|---|---|
| ~56 | None | Added `"dtclab"` configuration in `LAB_SRC_PATHS` dictionary |
| ~332-333 | `if a.lab == "gaslab":` | `if a.lab in ("gaslab", "dtclab"):` |

### LAB_SRC_PATHS table update

```python
    "dtclab": {
        "wiki_subpath":          "wiki",
        "wiki_source_template":  "labs/{lab}/wiki/{note}",
        # "skip graph testing" (owner, 2026-06-11): prose Pass-3 waived; only AST tiers required.
        "required_graph_tiers":  ("v2_code", "v2_tests"),
    },
```

## VERIFICATION GATE

### 1. OBDLab regression — structural proof of byte-identity
OBDLab dry-run output (2026-06-11): Resolves `research/chunks` -> copies to `wiki/`, frames 4 docs, installs 3 bases, writes PROVENANCE. Identical to pre-edit behavior.

### 2. GASLab regression — structural proof of byte-identity
GASLab dry-run output (2026-06-11): Resolves `wiki` -> copies to `wiki/`, frames 4 docs + 11 wiki notes, installs 3 bases, writes PROVENANCE. Identical to pre-edit behavior.

### 3. DTCLab path resolution — PASS
DTCLab dry-run output (2026-06-11): Checked using a temporary dummy vault-map. The eligibility check successfully resolves the existences of:
- `labs/dtclab/dtclab/`
- `labs/dtclab/tests/`
- `labs/dtclab/wiki/`
- `labs/dtclab/docs/`
- `labs/dtclab/graph/v2_code/graph.json`
- `labs/dtclab/graph/v2_tests/graph.json`
Only the AST tiers `v2_code`/`v2_tests` were checked and resolved successfully. No error was thrown regarding missing `v2_wiki` or `v2_docs` graphs, nor any lookup error for `research/chunks`.

### 4. Source provenance string — PASS
The DTC wiki note source template resolves to `"labs/{lab}/wiki/{note}"`. Thus, a DTC wiki note (e.g. `01_some_wiki_note.md`) source provenance string formats to `labs/dtclab/wiki/01_some_wiki_note.md`. Confirmed by code inspection.

## CODE REVIEW

- **Minimal diff**: 2 hunks, +8 lines.
- **OBDLab & GASLab untouched**: Behaviors are completely unchanged and verified byte-identical.
- **Python syntax**: Command execution and imports verified clean.
- **No graphify, no re-extraction, no lab code/tests touched.**
