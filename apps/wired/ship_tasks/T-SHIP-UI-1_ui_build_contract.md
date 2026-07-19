# T-SHIP-UI-1 — UI build contract (READ-ONLY disclose)
**Pack:** ship · **Blocked by:** — · **Lane:** coder (read-only on code)
**Write scope:** ONE report `apps/wired/ship_tasks/reports/SHIP_UI_CONTRACT_2026-07-07.md`
(+ progress note). No app code in this task.

## Why (audit B-1 — the publish surface)
Owner ruling 2026-07-07: publishing = an end-user UI with the **same graphics look as the
old UI**, **populated with all fields**. No runnable UI exists today. Before building,
disclose the exact contract — the old app predates the v3 output change (ranked top-3 +
abstain) and the C2..C9 input columns, so a blind rebuild would ship a stale surface.

## Inputs (all exist; read, do not edit)
- Old look: `ARCHIVE/4DLabWired/app.py` (archived Streamlit app — layout, widget order,
  conditional-grid behaviour) + `apps/ui/_sample_app_reference.py` +
  `apps/ui/UI design/` (`4DLab Petrol UI.html`, `app.jsx`, `styles.css`).
- Field contract: `apps/ui/4DLab_UI_FieldMap.md` (reconciled by T-UI-SYNC-1, but BEFORE
  the C2..C9 packs — expect drift).
- Live input schema: `apps/wired/wired/composition.py` + `apps/wired/v7/load_corpus.py`
  column set (incl. the C2..C9 columns landed 2026-07-05/06).
- Live output: `OrchestratorFinalUIOutput` + ranked differential siblings + abstain flag
  (`labs/comlab/comlab/schemas/response.py`; v3 T-V3-3/3B/3C semantics).

## Deliverable — the contract, 4 sections
1. **Field inventory diff.** Every FieldMap field vs the live `diagnose()` input surface:
   `UNCHANGED / RENAMED / REMOVED / NEW-since-map` (the C2..C9 columns land here — mark
   each with its producer state + whether a lay user can plausibly supply it, or it
   belongs behind an "advanced / workshop data" toggle).
2. **Look extraction.** From the old app + `UI design/`: page structure, section order,
   conditional-grid rules (DNA-driven show/hide), styling cues to preserve.
3. **Verdict rendering.** How the UI shows the v3 output honestly: ranked top-3 with
   per-family confidence, the ABSTAIN verdict as a first-class outcome (78/294 abstain by
   design — never render as an error), and the `synthetic=true`-calibration caveat wording.
4. **Open forks for the owner** (each with a recommendation): advanced-fields toggle
   default; single-file Streamlit vs the `UI design/` React look; where the app lives
   (`apps/ui/` proposed, importing `wired.diagnose()` only — composition boundary per
   DECISIONS D-V2-9).

## Success criteria
- Every FieldMap row + every live schema field appears exactly once in the diff (no
  orphans either direction); each NEW field names its producer state and consumer.
- Contract is implementable without further code reading (T-SHIP-UI-2 is authored from it
  after owner sign-off).
