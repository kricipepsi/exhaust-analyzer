# T-PREP-WIRE-1 — progress note

## Plan
Architect triage (not a code task): verify the prior wiring's rings (MW-001/U-WV2-1)
and PCV (MW-008/U-WV2-2) chemistry contradictions against the **current** tree and
rule each FIX-NOW or ACCEPT-KNOWN-BLOCKED. Method: read GASLab `resolution.py` +
registry rule JSON + `corpus_curated.csv`; run rings/PCV payloads through live
`registry.integration_shim.route_case_with_diagnostics`. Deliverable: the ruling doc.

## Outcome — both ACCEPT-KNOWN-BLOCKED + cross-lab reconciles forward-registered
Full evidence in `../RINGS_PCV_TRIAGE_RULING.md`. Headlines:
- **Rings (MW-001):** real & current, and deeper than U-WV2-1 — GASLab and the registry
  hold **opposite HC-vs-RPM models** for worn rings (GASLab: low-HC *rising*; registry
  corpus: high-HC *dropping*). Live proof: GASLab-shaped rings (low HC 120) → `CF-001`,
  not MW-001. Needs an owner domain ruling + corpus re-validation → not a safe quick fix.
  Forward-registered `T-XLAB-RINGS-RECONCILE-1` (gaslab + registry ledgers).
- **PCV (MW-008):** registry side proven (routes when handed `POA_SIGNATURE`); GASLab's
  emission for a real HC-dropping PCV case is unverified (POA leaf needs HC>500 both).
  Forward-registered `T-XLAB-PCV-VERIFY-1` (gaslab ledger).

## Verification
- `RINGS_PCV_TRIAGE_RULING.md` exists; decides MW-001 and MW-008; uses FIX-NOW/ACCEPT-KNOWN-BLOCKED. ✓
- Forward-registered rows present on `labs/gaslab/tasks/PROGRESS.md`. ✓
- `T-WIRE-2` Notes in `WIRED_PROGRESS.md` carry the per-case expectation. ✓
No lab/registry code edited by this task (triage only).
