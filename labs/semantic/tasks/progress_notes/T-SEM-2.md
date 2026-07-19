# T-SEM-2 — progress note

## Plan
We will scaffold the `comlab/config/proposals/` registry by creating its `README.md` (defining the entry schema, graduation rules, dual ISO/SAE citation convention, and worked add-a-fault example) and materializing the `EP-DTC-02` 8-family taxonomy backbone in `taxonomy_backbone.md` and `taxonomy_backbone.yaml` with standard citations. We will also implement a config loader `_load_taxonomy_backbone` in `FaultAtlasRouter` to prove that the router can consume this backbone. All existing `comlab` pytest tests must pass, confirming no routing behavior changes.

## VERIFICATION GATE
- **Scaffold files present:** Verified that `comlab/config/proposals/README.md`, `taxonomy_backbone.md`, `taxonomy_backbone.yaml`, and `proposals.yaml` exist.
- **Router loader verification:** Verified that `fault_atlas_router.py` imports and runs successfully, loading the 8 taxonomy families at router initialization.
- **Ruff check:** Verified that `ruff check comlab/` passes without any issues.
- **Pytest execution:** Confirmed that `pytest -x -q` executes successfully with 332 passing tests (matching baseline).

## CODE REVIEW
- **comlab/config/proposals/README.md:** Defines the proposals registry layout, graduation rules (`proposed` → `pinned` → `graduated`), dual ISO/SAE citation format, and contains an end-to-end worked example for `EP-OBD-17`.
- **comlab/config/proposals/taxonomy_backbone.md / .yaml:** Specifies the 8 powertrain P-code families (P00XX through P09XX) matching the EP-DTC-02 specification, with ISO 15031-6 / SAE J2012 citations and descriptions of what attaches to each.
- **comlab/comlab/core/fault_atlas_router.py:** Added `_DEFAULT_TAXONOMY_PATH` constant, called `self._load_taxonomy_backbone()` in `__init__`, and implemented the `_load_taxonomy_backbone()` method to read the YAML backbone gracefully.
