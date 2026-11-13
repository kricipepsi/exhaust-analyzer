# T-COMA-22 — authoring sidecar (Windows Cowork, 2026-11-13)

Input: `audit/reports/R1_D2_20261017.md` F-D2-14; `docs/COMLab_PRD.md` §0 and §6.3; `docs/COMLab_HLD.md` §0;
`docs/COMLab_DLD.md` §11.2 and the Stage A.5 telemetry row; wiki 07 RULE_LAB_SUPPRESSION; T-COMA-21's
`_map_degradation`. Rehearsal: `C:/4DApp/recheck/T-COMA-22/`.

### Verified context ###
1. **Still open on `7d008da`:** the PRD chip says "Diagnosis based on gas chemistry only" while a non-starter (gas
   suppressed) is GAS_DOMINANT; PRD §0 and HLD §0 rows still say GAS_DOMINANT is "only when ... `suppress_gaslab`"
   (stale since T-COMA-21); DLD §11.2 and Stage A.5 name only `suppress_gaslab`. Observed (P1 grep, 4 lines).
2. **No UI renders the chip:** `grep -n "gas chemistry only" apps/ui/*.py` is empty. Observed.
3. **Rehearsal** (restored; `git apply --check` of the saved diff passes): `applied 6 edits`; a second run exits 1
   (no double edit); comlab `540`, wired `186`, ui `73`; step 2 empty; `3 files changed, 11 insertions(+), 8
   deletions(-)`. Observed.

### Rulings and the tradeoff that lost ###
- **Keep GAS_DOMINANT for a non-starter; change the copy.** Lost: a new degradation literal for a non-running engine
  (a schema change for every consumer, for a chip no UI renders yet). wiki 07 names OBD suppression as GAS_DOMINANT.
- **Edit the §0 deviation rows and DLD, not the HLD §4 design body.** Lost: rewriting the design (the §0 table is the
  shipped-code statement).
- Plan NONE, difficulty 1. Docs row: no second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `540 passed, 4 skipped`; `186 passed`; `73 passed` |
| step 2 | SIMULATED | no output |
| step 3 | SIMULATED | `3 files changed, 11 insertions(+), 8 deletions(-)` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-COMA-22: GAS_DOMINANT chip copy true for both causes; PRD/HLD/DLD state T-COMA-21's rule (F-D2-14).

### Cold read ###
own pass 2026-11-13: P1-P2 measured (facts 1, 3) · `rehearse.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-3 · cold read: not triggered (d1, scripted) · no finding.

### Correction history ###
(none)
