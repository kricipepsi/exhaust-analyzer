# T-SHIP-UI-2 — build the publish UI (COMMIT)
**Pack:** ship · **Blocked by:** T-SHIP-UI-1 (**done** — contract on disk) · **Lane:** coder
**Spec of record:** `apps/wired/ship_tasks/reports/SHIP_UI_CONTRACT_2026-07-07.md` — build
EXACTLY that contract; this file only adds mechanics.
**Write scope:** `apps/ui/app.py` (+ optional `apps/ui/ui_payload.py` helper + tests under
`apps/ui/tests/`), progress note, ledger row. Nothing in `labs/`, `wired/`, corpus, registry.

## Mechanics
1. Read the contract §1-§5 + `apps/ui/4DLab_UI_FieldMap.md` (placement) +
   `apps/ui/_sample_app_reference.py` (graphics helpers, `_check_radio()`).
2. Build sidebar + 7 mapped expanders + the NEW 8th "Advanced / workshop signals" expander
   (36 columns, 6 producer-state groups, collapsed) per contract §1.
3. Payload assembly: mirror `apps/wired/v7/load_corpus.py` typing; untouched widget ⇒ key
   absent (no default-fill — producers must abstain on absence).
4. Verdict panel per contract §3 (top-3, ABSTAIN first-class, calibration footer).
5. Entry: `.venv-wired/bin/python -m streamlit run apps/ui/app.py` (add streamlit to
   `.venv-wired` if absent — record version in the note; no other env changes).
6. Fix in passing: FieldMap provenance note `apps/wiredV2/...` → `apps/wired/wired/composition.py`.

## Success criteria (from the contract, binding)
- Every FieldMap field + all 36 advanced columns present and wired.
- Widget→payload unit test: untouched fields absent; typed fields round-trip.
- e2e: MW-002 fixture values entered via the UI path return `fault_code=MW-002`; one
  abstain case renders the contract §3.2 pattern (never an error state).
- ruff + pyright clean; `apps/ui/tests` green; both gate blocks filled.
- FORBIDDEN: default-filling advanced fields; importing lab modules; touching the engine;
  score chasing.
