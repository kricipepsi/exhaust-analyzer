# T-AUD-10e — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/reports/R1_C5_20261017.md` F-C5-7; `labs/comlab/docs/COMLab_PRD.md` §5.5, §5.8;
`labs/comlab/comlab/schemas/ingestion.py` (`UserInputEchoAudit`, `UserInputEchoFieldGroup`). Rehearsal:
`C:/4DApp/recheck/T-AUD-10e/`.

### Verified context ###
1. **COMLab carries the echo verbatim:** `lab_pipeline_aggregator.py::_echo_pass_through` returns
   `request.user_input_echo_audit` or the empty sentinel; `abort_incomplete(..., echo=None)` the same. Observed.
2. **`wired` sends none:** `grep -c user_input_echo_audit apps/wired/wired/composition.py apps/ui/app.py` → `0`, `0`
   on `2fa1af3`. The two `abort_incomplete` calls in `_diagnose` pass no echo. Observed.
3. **A DTC input with no freeze frame aborts** ("Freeze frame is incomplete"); the full-run test uses gas + OBD, and
   the DTC group is pinned on the abort path. Observed (probe in this session).
4. **Rehearsal** (restored): ui `65 → 68`; wired `106 → 110`; comlab `508 passed, 4 skipped` (equal); ruff clean;
   `3 files changed, 65 insertions(+), 2 deletions(-)`; base: wired test `4 failed`, ui test `3 failed`. Mutants:
   request echo `None` → wired `2 failed, 2 passed`; out-of-range abort without echo → `1 failed, 3 passed`;
   `expanded=True` → ui `1 failed, 2 passed`; `None` shown as `None` → ui `1 failed, 2 passed`. Audit probe:
   `fields never referenced in app.py: ['is_fault_detected']`. Observed.

### Rulings and the tradeoff that lost ###
- **Echo built in `wired`, from `raw_inputs`, before any lab runs.** Lost: building it in the UI (the PRD and LLD §3.3
  make COMLab's output the carrier; the UI already has `raw_payload`, but the abort page and any non-UI caller would
  get no echo).
- **Overrides go into the vehicle group as `override_<key>`.** Lost: a fifth group (the schema's `screen_id` has
  four values).
- **`is_fault_detected` out of scope** (F-C1-3, owner T-AUD-2: `True` when the no-fault rule wins). Lost: closing the
  F-C5-7 probe fully now.
- **Plan NONE, difficulty 2**, although the handoff listed the plan as REQUIRED (new construction). The whole edit is
  rehearsed and scripted, and no design choice is left to the implementer. Lost: one plan review round trip.
- Code row: second-model review at acceptance.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `68 passed`; `110 passed` |
| step 2 | SIMULATED | `4 passed`; `3 passed`; base `4 failed` / `3 failed` |
| step 3 | SIMULATED | ruff `All checks passed!`; `3 files changed, 65 insertions(+), 2 deletions(-)` |
| step 4 | SIMULATED | `fields never referenced in app.py: ['is_fault_detected']`; `rendered: {'horizon': True, 'gas skipped disclosure': True}` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-10e: wired echoes the typed inputs (all results and aborts); the pane shows them collapsed (F-C5-7, PRD 5.5).

### Cold read ###
own pass 2026-11-07: P1-P3 measured (fact 4) · `apply_fix.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-4 and R4 · cold read: not triggered (d2, scripted) · no finding.

### Correction history ###
(none)
