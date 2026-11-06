# T-AUD-15 — authoring sidecar (Windows Cowork, 2026-11-06)

Input: `audit/drift/2026-11-05_DRIFT_REPORT_dtclab.md` (44 bullets), `reviews/REVIEW_T-AUD-11d.md`. Rehearsal:
`C:/4DApp/recheck/T-AUD-15/` (`apply_fix.py`, `rehearsal.patch`, `census.sh`); AST check `C:/4DApp/recheck/T-AUD-4t/ast_same.py`.

### Verified context ###
1. **Code facts re-measured on `fix/T-AUD-14`:** `len(DTCRoutingTag)` 17 (venv import); `routing_tag_map.yaml` 30
   `- patterns`, 3 `dna_gate:` (`egr_equipped`, `has_catalyst` ×2); `DtcEmissionsView` 2 bool fields
   (`schemas/dna_view.py:80-81`); 7 `ff_*` bools (`schemas/freeze_frame.py:77-95`); `Mode06MonitorState` 4 members
   incl. `MONITOR_ABORTED`; `evaluate_monitor(..., *, monitor_incomplete, euro_emission_category)`
   (`mode06_evaluator.py:77-83`); `P060[1-6]` routed to `ECU_INTERNAL_HISTORY` (`yaml:151`). Observed.
2. **41 of the 44 doc quotes still present;** the 3 projector quotes (HLD:48, VOCAB:506, ADR:37) were fixed by
   T-AUD-4u (`grep -cF` = 0). Observed.
3. **Three more HLD sites** found by the census: 57 (`18-tag`), 69 (scorer via the Wired adapter), 199 (three named
   gates). Observed.
4. **The composition aborts an incomplete freeze frame** (`composition.py` `FREEZE_FRAME_INCOMPLETE`); the extractor
   raises `FreezeFrameIncompleteError`. The 180 rpm rule is in `DTC_VOCABULARY.md §12.3` (line 369). Observed.
5. **Rehearsal** (restored): census base `stale 31`, after `stale 0`; `aborted` 2/1/1; `spark` 1 → 6; dtclab 590
   passed; `ast same` for the extractor; ruff clean; 8 files, 57 insertions / 44 deletions. Observed.

### Rulings and the tradeoff that lost ###
- **R1 scorer documented unused.** Lost: wiring it in (new verdict input, would need its own design and corpus check).
- **R2 B/C/U documented as passing.** Lost: a stricter gate (changes DTCLab output).
- **R3 raise documented.** Lost: mark-and-degrade (a partial freeze frame would need new degraded scoring).
- **R4 NOSTART shipped (DTC side).** Lost: nothing; the "proposed" text was stale. GPF scenario kept with a
  not-implemented marker. Lost: a cleaner BDD (deleting a design scenario loses the design).
- Docs row (one comment, AST-equal): no second-model review. Plan NONE, difficulty 1.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `stale 0`; `aborted` 2/1/1; `spark 6`; `ast same` |
| step 2 | SIMULATED | `590 passed` |
| step 3 | SIMULATED | ruff `All checks passed!`; status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-15: DTCLab docs match the shipped package (44 bullets of 11d; scorer, B/C/U, FF rulings: document).

### Cold read ###
own pass 2026-11-06: P1-P3 measured · `apply_fix.py` exits on any literal count other than 1 · counts from venv import
and grep (sidecar fact 1) · traceability: criteria 1-3 → steps 1-3 · patched: census output `aborted DLD=…` (check 14
read `file:N` as a citation); HLD:69 wording kept out of the census pattern · no finding.
cold read 2026-11-06 FOCUSED reader; trigger 1c grep hit (criterion 3 "only"); 0 findings, 0 patched — 3 calls.

### Correction history ###
(none)
