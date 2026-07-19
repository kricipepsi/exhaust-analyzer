# T-COM-PATHS-1 — progress note

**Task:** Register COMLab's source paths in `build_lab_vault.py` (`LAB_SRC_PATHS`).
**Lane:** GRAPH-TOOLING / vault-tooling (no lab inner-loop/gate). **Run:** 2026-06-28.

## Plan (confirmed)

Two minimal edits to `_skills/graph/4dlab-vault/scripts/build_lab_vault.py`, mirroring the
`dtclab`/`dnalab` precedent — no new mechanism, read-only on all graphs, no graphify:

1. Add a `comlab` entry to `LAB_SRC_PATHS` (wiki at `wiki/`, two AST tiers
   `("v2_code", "v2_tests")`; prose Pass-3 waived per owner 2026-06-26, liftable per
   T-COM-GRAPH-LLM).
2. Add `"comlab"` to the provenance "waived" branch (~line 364) so PROVENANCE.md records
   the `v2_wiki/v2_docs waived` note.

## Defect reproduced (before edit)

`--dry-run --lab comlab` fell through to the OBDLab default and aborted:

```
Lab 'comlab' is not eligible — missing:
  /agent_workspace/labs/comlab/research/chunks
  /agent_workspace/labs/comlab/graph/v2_wiki/graph.json
  /agent_workspace/labs/comlab/graph/v2_docs/graph.json
```

(Note the missing list did NOT include `v2_code`/`v2_tests` graphs — those exist from
T-COM-GRAPH-AST, confirming the only defect was the path fallthrough.)

## Exact change (minimal — two regions)

- `LAB_SRC_PATHS["comlab"]` dict entry (after `dnalab`, ~line 81):
  `wiki_subpath: "wiki"`, `wiki_source_template: "labs/{lab}/wiki/{note}"`,
  `required_graph_tiers: ("v2_code", "v2_tests")` + the waiver comment.
- Provenance branch (~line 364): `("gaslab", "dtclab", "vinlab", "dnalab")` →
  `(... "dnalab", "comlab")`.

No `graph_source` mechanism change was needed (the script keys off the tier dirs, same as
`dtclab`). No third edit required — diff is exactly the two lines specified.

## VERIFICATION GATE — PASS

- **ruff** `build_lab_vault.py`: **All checks passed!** (house style clean).
- **Regression guard (criterion 1):** captured `_before` for obdlab + dtclab, re-ran after
  edit → `diff` empty for both. **OK obdlab unchanged · OK dtclab unchanged** (byte-identical).
- **COMLab resolution (criterion 2):** `--dry-run --lab comlab` no longer aborts on
  `research/chunks` / `v2_wiki` / `v2_docs`. The eligibility check (code/tests/wiki/docs +
  `v2_code`/`v2_tests` graphs) now PASSES; the script advances to the *next* real gate,
  `No vault-map for 'comlab'` — which is T-COM-VAULT's job (out of scope here). grep for
  `research/chunks|v2_wiki|v2_docs|not eligible` in output → **NONE**.
- **Provenance + source string (criteria 3):** verified by importing the module and
  exercising the resolved config:
  - `wiki_source_template.format(...)` → `labs/comlab/wiki/00_index.md` ✓ (criterion 3).
  - `required_graph_tiers` → `("v2_code", "v2_tests")` ✓.
  - provenance `graph_note` → `v2_code, v2_tests; v2_wiki/v2_docs waived by owner direction` ✓.
- **No graphify; no re-extraction; no lab code/test edit (criterion 4):** frozen
  `graph/v1_baseline/` and the `v2_*` dirs untouched; only the vault-tooling script edited.

## CODE REVIEW — PASS

- Minimal diff: exactly the two regions the task specified (one `LAB_SRC_PATHS` entry + one
  branch tuple). Mirrors the existing `dtclab`/`dnalab` rows verbatim in shape — no new
  mechanism, no enlarged scope.
- Comment records the owner waiver date and the T-COM-GRAPH-LLM lift condition, consistent
  with the sibling entries.
- Other labs' entries unchanged; regression guard proves no behavioural drift.

**Result:** both gates clean → ledger row T-COM-PATHS-1 → `done`.
T-COM-VAULT is now unblocked (its other blocker, T-COM-GRAPH-AST, is already `done`).
