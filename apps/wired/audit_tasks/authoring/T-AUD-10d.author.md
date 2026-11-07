# T-AUD-10d — authoring sidecar (Windows Cowork, 2026-11-07)

Input: `audit/reports/R1_C5_20261017.md` F-C5-7; `labs/comlab/docs/COMLab_PRD.md` §5.1, 5.2, 5.6, 5.7;
`labs/comlab/wiki/04_horizon_eras.md` (era table). Rehearsal: `C:/4DApp/recheck/T-AUD-10d/`.

### Verified context ###
1. **Fields arrive today:** `execution_meta.resolved_horizon`, `execution_meta.lab_routing_directive` (4 bools),
   `fault_enrichment.impacted_subsystems`, `performance_analytics.severity_level` (`schemas/response.py`). Observed.
2. **Echo empty:** `wired.composition` never fills `user_input_echo_audit` (grep: no hit) → T-AUD-10e. Observed.
3. **Rehearsal** (restored): ui `61 → 65 passed`; the new test `4 passed`, `4 failed` on the base; wired `106`;
   ruff clean; `50 insertions(+)`; the audit render probe `rendered: {'horizon': True, 'gas skipped disclosure':
   True}` (it still names `user_input_echo_audit` and `is_fault_detected`). Observed.

### Rulings and the tradeoff that lost ###
- **R1 copy in helpers.** Lost: literals inline in `app.py` (no unit test reaches them).
- **R2 banner above both branches.** Lost: inside the verdict branch only (an abstained result still has a severity).
- **Split 10b → 10d (this) + 10e** (the echo: `wired` builds `UserInputEchoAudit` from the raw inputs; plus
  `is_fault_detected`). Lost: one row (the echo needs a `wired` change and its own ruling).
- Code row: second-model review at acceptance. Plan NONE, difficulty 2.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `65 passed`; `106 passed` |
| step 2 | SIMULATED | `4 passed`; base `4 failed` |
| step 3 | SIMULATED | ruff clean; `50 insertions(+)`; status clean after restore |
| step 4 | SIMULATED | `rendered: {'horizon': True, 'gas skipped disclosure': True}` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-10d: results pane shows severity banner, skipped-lab notices, horizon era and impacted subsystems (F-C5-7).

### Cold read ###
own pass 2026-11-07: P1-P3 measured (fact 3) · `apply_fix.py` exits on any unexpected count · traceability:
criteria 1-2 → steps 1-4 · cold read: not triggered (d2, scripted) · no finding.

### Correction history ###
(none)
