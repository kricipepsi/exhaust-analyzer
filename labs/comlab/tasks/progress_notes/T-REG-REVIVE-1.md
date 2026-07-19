# T-REG-REVIVE-1 progress note

Status: done
Date: 2026-06-21

## Scope Confirm

Clean the canonical `labs/comlab/registry` package only: purge generated caches,
remove the empty non-production `ignition_fault.json` stub while preserving the
live enum/KG family, lock the production manifest to the rules directory, and
move process documentation out of the import root. Retain the standalone
pyright config and corpus tooling because they have named analysis and deferred
`REG-V2-AUTHOR-ignition_fault` consumers. No DELTA-2, KG, corpus rebuild,
emitter, archived-registry, or graph changes.

## Changed Files

- `registry/rules/ignition_fault.json` — removed empty rule stub; real rule
  authoring remains deferred to `REG-V2-AUTHOR-ignition_fault`.
- `registry/tests/test_integration_shim.py` — added manifest-versus-directory
  equality gate.
- `registry/docs/` — relocated nine Markdown documents plus
  `registry_tasks/` and `_registry_skills/` from the import root.
- `registry/tools/build_corpus.py` and `registry/tests/test_build_corpus.py` —
  replaced legacy absolute paths with current workspace-relative paths and
  normalized BOM-aware master CSV reads.
- `registry/tests/test_oil_no_kg_on_live_path.py` — corrected COMLab-local
  proposal/KG paths.
- `registry/tests/test_charging_system_rules.py` and `registry/schema_v2.py` —
  reconciled the stale routing-tag count comment/assertion to the actual
  19-member mirror.
- `registry/tests/test_oil_live_verdicts.py` and
  `registry/tests/test_shim_high_idle_pids.py` — removed stale imports.
- `pyproject.toml` — registered the existing `integration` pytest marker.
- `comlab/core/fault_atlas_router.py` — made existing optional DTC payload
  handling explicit so the required package-wide pyright gate is clean.
- `tasks/PROGRESS.md` — closed this task and unblocked DELTA-2.

## Verification Gate

- Interpreter: native `.venv-comlab`, Python 3.14.6; registry imports from
  `C:\Workspace\labs\comlab\registry\__init__.py`.
- Canonical-path check: no `ARCHIVE` entry appears on `sys.path`.
- `python -m ruff check .` — all checks passed.
- `python -m pyright --pythonpath .venv-comlab\Scripts\python.exe comlab\ registry\`
  — 0 errors, 0 warnings.
- `python -m pytest tests\ -q` — 378 passed, 6 skipped, 0 failed.
- `python -m pytest registry\tests\ -q` — 470 passed, 0 failed.
- `test_production_manifest_matches_rules_directory` — passed; 15 manifest
  files exactly match the 15 JSON files on disk.
- Bytecode check after tests — only `cpython-314` remains.
- Import-root check — no Markdown files remain directly under `registry/`.
- `registry/rules/ignition_fault.json` is absent; `IGNITION_FAULT` enum/KG
  remain unchanged.

## Code Review

- The production registry and glob-mode tests now load the same rule set.
- Removing the empty ignition stub cannot remove production behavior because
  it was absent from `_EXPECTED_RULE_FILES` and contained no rules.
- Registry documentation remains preserved under `registry/docs/`; nothing
  was deleted except generated caches and the explicitly scoped empty stub.
- `pyrightconfig.json` is retained for standalone registry analysis.
- Corpus data and builder are retained for the deferred ignition-rule task;
  only path portability and BOM handling changed, and all 470 registry tests
  validate the retained tooling.
- Nullable-DTC router edits preserve behavior for populated requests and
  fail safely for schema-valid absent DTC payloads.
- No DELTA-2 wiring, delta-engine change, KG rebuild, corpus rebuild,
  cross-lab import, or graph operation was performed.

## Next

`T-COMV2-DELTA-2` is unblocked. Stop.
