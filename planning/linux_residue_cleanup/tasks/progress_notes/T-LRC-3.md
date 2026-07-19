## Plan

- Picked task T-LRC-3: Replace hardcoded Windows absolute paths in the five VINLab tools with environment-variable-derived paths (`VEHICLE_DATA_ROOT` and `DBS_ROOT`) following the owner decision (Env-var only, no default paths).
- Files to touch:
  - `labs/vinlab/tools/build_vds_map.py` (modify)
  - `labs/vinlab/tools/build_wmi_map.py` (modify)
  - `labs/vinlab/tools/extract_opsi_engine_codes.py` (modify)
  - `labs/vinlab/tools/tecdoc_ktype_bridge.py` (modify)
  - `labs/vinlab/tools/build_vref_db.py` (modify)
- Verification steps to run:
  - Grep for `C:\` under `labs/vinlab/tools/` to verify it returns zero matches.
  - Compile the five modified tools with `py_compile` to ensure no syntax errors.
  - Run `ruff check` and `pyright` on the modified files to check linting and types.
  - Smoke-test the environment variable resolution on import of `build_vds_map`.

VERIFICATION GATE — T-LRC-3
===========================
Phase 1 Syntax/import:  PASS — All 5 modified tools compiled without error; importing build_vds_map with VEHICLE_DATA_ROOT set succeeds.
Phase 2 Type check:     PASS — `pyright` run from `labs/vinlab` with the venv pythonpath returns OK for all 5 modified files.
Phase 3 Lint:           PASS — `ruff check` on all 5 modified tools is OK.
Phase 4 pytest:         PASS — `pytest` on `labs/vinlab` ran successfully (194 passed, 8 skipped).
Phase 5 Wiki/orphan:    PASS — N/A; path configuration updates only, no diagnostic logic or wikis affected.
Phase 6 Diff review:    PASS — Edits are strictly limited to path variables and error checking in the 5 named tools, plus progress notes and residue ledger updates. No graphify/KG rebuild run.

Checklist items applied:
  1. Pathlib — Path concatenation uses `/` operators on Path objects.
  2. No mutable defaults — Checked; none.
  3. No bare except — Checked; none.
  4. Sorted imports — Ruff clean.

Status: DONE — flipping residue cleanup ledger row to done.

CODE REVIEW — T-LRC-3
=====================
1. Design rules:        PASS — no cross-lab imports, no logic changed.
2. Scope compliance:    PASS — only the 5 specified tool files, this progress note, and the ledger file were modified.
3. Contracts:           PASS — path settings are now environment-derived and throw clean RuntimeErrors if the required variables are missing.
4. Docstrings:          PASS — unchanged, public surfaces documented.
5. Wiki provenance:     PASS — N/A.
6. Immediate Checklist: PASS — all syntax, pyright, ruff, pytest, and env-var checks passed.
7. Test coverage:       PASS — full vinlab test suite passed.
8. Structural craft:    PASS — standard environment variable checks correctly implement the owner's choice of "Env-var only (no default paths)".

Verdict: CLEAN
Blockers: none

