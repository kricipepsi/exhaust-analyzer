# T-UI-VAULT-SUPPORT-1 — progress note

**Task:** `Vault/tasks/T-UI-VAULT-SUPPORT-1_*.md` · **Pack:** VAULT (UI) · **Lane:** vault-tooling (no lab inner-loop).

## Plan
1. Capture dry-run before-states for `obdlab` and `comlab` using Python 3.14 venv.
2. Add new `APP_SRC_PATHS` configuration entry mapping `ui` to `apps/ui` with designated docs notes and empty required graphs.
3. Add source resolution logic: if `a.lab` is registered in `APP_SRC_PATHS`, set `lab_src` to repo/src_root, skip code/tests/wiki/graphs.
4. Implement customized eligibility checks verifying only that listed `docs_notes` exist in `src_root`.
5. Update destination, copy, framing, and provenance paths so that app docs copy to `apps/` instead of `labs/` and generate correct metadata.
6. Verify no-regression on existing lab dry-runs and verify `ui` dry-run stops at the missing map gate.
7. Run `ruff check` on `build_lab_vault.py`.

## VERIFICATION GATE
- **OBD+COM Dry-Runs Byte-Identical:** Verified that before/after dry-run logs for `obdlab` and `comlab` are 100% byte-identical.
- **UI Dry-Run Resolves to Missing-Map Gate:** Executing `--lab ui --dry-run` resolved eligibility checks and copying checks, then exited cleanly at the missing map check: `No vault-map for 'ui': /agent_workspace/_skills/graph/4dlab-vault/assets/vault-map.ui.yaml`.
- **Ruff Clean:** `ruff check` passes cleanly on the edited script with zero errors.

## CODE REVIEW
- **Minimal, Additive Logic:** Edits to `build_lab_vault.py` introduce `APP_SRC_PATHS` and conditional logic (`is_app = a.lab in APP_SRC_PATHS`) to override paths and behaviors for doc-only applications.
- **Zero Lab Changes:** Regular lab resolution path is completely untouched inside the `else` blocks, ensuring no side effects on any existing labs.
- **Clean Framing & Provenance:** For apps, copies only specified docs notes to `Vault/apps/<lab>/docs/`, sets source metadata to `apps/ui/<note>`, and specifies `graphs required: none` in `PROVENANCE.md`.
