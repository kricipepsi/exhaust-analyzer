# T-PREP-WIRE-1 — rings / PCV chemistry-contradiction triage

### Goal ###
Produce one **ruling document** that resolves the two GASLab->registry chemistry
contradictions which blocked the oil-burning cases `MW-001` (worn piston rings)
and `MW-008` (PCV) in the prior wiring. For EACH case, decide one of:
(a) **fix-now** — name the exact emitter/registry change and register it as a
task on the owning lab ledger (gaslab and/or registry); or (b) **accept
known-blocked** — record the reason and the expected wired behaviour so
`T-WIRE-2` can assert it as an expected non-route rather than stalling. The task
is `done` when the ruling file exists with a decision + rationale for both cases.
This task writes **no lab code** — it is an architect investigation whose output
is a ruling and (if fix-now) forward-registered ledger rows.

### Success criteria ###
- `wiring_prep_tasks/RINGS_PCV_TRIAGE_RULING.md` exists and contains, for each of
  MW-001 and MW-008: the contradiction in one sentence, the decision
  (`FIX-NOW` | `ACCEPT-KNOWN-BLOCKED`), the rationale, and the consequence for
  `T-WIRE-2` (expected route, or expected non-route + the assertion to write).
- If any case is `FIX-NOW`: a forward-registered row exists on the correct lab
  ledger (`labs/gaslab/tasks/PROGRESS.md` and/or
  `labs/comlab/registry/docs/REGISTRY_PROGRESS.md`) with a `deferred` status and
  a one-line scope — `apps/wired` never edits lab code itself.
- The ruling is reflected in `WIRED_PROGRESS.md` `T-WIRE-2` Notes (one-line
  cross-ref) so the oil-case runner author knows which cases to expect.

### Context ###
The prior wiring (archived `ARCHIVE/wiredV2/`) reached `done` on composition
(`T-WV2-1`) but `blocked` on the oil-case runner (`T-WV2-2`): 3/5 cases routed
(`MW-002/MW-003/MW-009`), and `MW-001`/`MW-008` were blocked by two cross-lab
mismatches recorded as unplanned follow-ups:
- **`U-WV2-1` (rings, MW-001):** the registry rule's evidence thresholds
  (`hc >= 200`, `co2 < 13`, `o2 >= 1.5` from low-idle) contradict GASLab's
  `WORN_PISTON_RINGS` clean-idle pattern (`HC <= 150`, `CO2 ~ 14`, `O2 ~ 0.2`).
  GASLab assigns the rings chemistry, but the registry rule evidence never fires.
- **`U-WV2-2` (PCV, MW-008):** the registry rule needs `high_idle_hc` gating to
  discriminate PCV, but GASLab re-classifies `POA_SIGNATURE -> INCOMPLETE_OXIDATION`
  when a high-idle reading is present — a chicken-and-egg: the rule needs
  high-idle to discriminate PCV; GASLab needs *no* high-idle to keep
  `POA_SIGNATURE`.

Pin the current numerics from the oil-case dossier, do not re-derive them:
`planning/oil_consumption/PROGRESS.md` (the `MW-00x` map + per-case dossier
numerics) and `planning/OIL_CASE_SIGNATURES_5FR.md`. Cross-lab dependency canon:
`labs/comlab/docs/CROSS_LAB_DEPENDENCIES.md`. The archived findings verbatim:
`ARCHIVE/wiredV2/wiredv2_tasks/` ledger "Unplanned follow-ups" (`U-WV2-1`,
`U-WV2-2`) and `ARCHIVE/wiredV2/wiredv2_tasks/progress_notes/T-WV2-2_oil_case_runner.md`.
READ-NARROW: grep the case IDs in the dossier and read ~60 lines around each;
do not whole-read the archived composition.

### Consumer (signal/noise) ###
N/A — no new field/enum/fault. This task emits a ruling document and, at most,
forward-registered `deferred` ledger rows whose own specs (authored later on the
lab ledgers) will carry the consumer obligation.

### Deliverables ###
1. `wiring_prep_tasks/RINGS_PCV_TRIAGE_RULING.md` — the ruling (both cases).
2. (conditional) forward-registered `deferred` rows on the owning lab ledger(s)
   for any `FIX-NOW` decision.
3. One-line cross-ref added to `WIRED_PROGRESS.md` `T-WIRE-2` Notes.

### Files to touch ###
- `apps/wired/wiring_prep_tasks/RINGS_PCV_TRIAGE_RULING.md` (CREATE)
- `labs/gaslab/tasks/PROGRESS.md` (MODIFY — only if a case is FIX-NOW)
- `labs/comlab/registry/docs/REGISTRY_PROGRESS.md` (MODIFY — only if FIX-NOW)
- `apps/wired/WIRED_PROGRESS.md` (MODIFY — one-line Notes cross-ref)

### Out of scope ###
Do not edit GASLab or registry *code* in this task — triage decides and
forward-registers; the actual emitter/registry fix is a separate lab task with
its own spec and gates. Do not change the wiring composition or runner here. Do
not rebuild any knowledge graph. Surgical-change rule: the only files this task
writes are the ruling doc and the named ledger rows.

### Verification ###
```bash
cd /agent_workspace
# Structural: the ruling exists and decides both cases
test -f apps/wired/wiring_prep_tasks/RINGS_PCV_TRIAGE_RULING.md
grep -Eiq "MW-001" apps/wired/wiring_prep_tasks/RINGS_PCV_TRIAGE_RULING.md
grep -Eiq "MW-008" apps/wired/wiring_prep_tasks/RINGS_PCV_TRIAGE_RULING.md
grep -Eiq "FIX-NOW|ACCEPT-KNOWN-BLOCKED" apps/wired/wiring_prep_tasks/RINGS_PCV_TRIAGE_RULING.md
# Cross-ref recorded
grep -q "T-PREP-WIRE-1" apps/wired/WIRED_PROGRESS.md
```
All steps must pass.

### Progress hook ###
PROGRESS.md `T-PREP-WIRE-1`: Status=done, Files changed={COUNT}, Verification="rings+PCV ruling recorded; FIX-NOW rows forward-registered where chosen"
