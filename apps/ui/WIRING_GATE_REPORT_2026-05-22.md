# Wiring Gate Report — 4DLabWired (Streamlit)

**Date:** 2026-05-22
**Gate:** "Verify first" — run each lab's test suite + scan PROGRESS before wiring.
**Verdict:** **NO-GO for full wiring.** Two of five labs are not finished coding.
The integration point itself (COMLab orchestrator) has unimplemented analytics
and a pending validation suite.

Test runner: Python 3.11.15 (uv venv), pydantic 2.13.4, pytest. Each lab run in
isolation against its own `pyproject.toml` / `pythonpath`.

---

## Per-lab results

| Lab | Tests | Status | Notes |
|---|---|---|---|
| **GASLab** | 115 passed | ✅ clean | Ground-truth gas chemistry. Ready. |
| **DTCLab** | 262 passed | ✅ clean | Ready. |
| **VINLab** | 152 passed, 8 skipped | ✅ clean | DNA decode. Ready. |
| **SymptomLab** | 42 passed | ✅ clean | Ready. |
| **OBDLab** | 275 passed, **15 failed** | ⚠️ code passes, tests path-broken | All 15 failures are `FileNotFoundError` on `OBDLab/OBDLab_KG_Wiki.md`; the wiki actually lives at `OBDLab/graphify-out/OBDLab_KG_Wiki.md`. Enum/logic assertions pass *before* the file read. PROGRESS: Phase 0 done, Phase 1 not begun. |
| **COMLab** | 90 passed, 13 skipped, **3 files cannot collect** | ❌ unfinished | Final validation task **T-P5-1 pending**. 13 skipped = unimplemented features: `estimate_kinetic_loss` (phase 2), DTC regex validator / fallback tree / legacy graceful degradation (phase 3). 3 test files error out on missing `COMLab/docs/wiki/OBD_VOCABULARY.md` & `DTC_VOCABULARY.md` (present only in `ARCHIVECOMLab/`; live wiki is `COMLab/wiki/` without these two). |
| **DNALab** | 12 passed, **6 failed + 6 errors** | ❌ unfinished | Assembly integration fails: fixtures use symptom `(visible_exhaust_smoke / black_sooty_rich)` which SymptomLab now rejects (valid: `black_smoke`, `blue_oily_smell`, `white_sweet_smell`). PROGRESS confirms **T-DL-3 pending**, blocked by "SymptomLab H2 fix (`black_smoke`) must be merged." |

---

## Why this blocks wiring

The Streamlit UI's only legal integration point is the **COMLab orchestrator**
(no cross-lab imports). Two problems land directly on the wiring path:

1. **COMLab is the integration point and it is not done.** Power-loss analytics
   (`estimate_kinetic_loss`) and DTC validation/fallback are stubbed/skipped, and
   the validation suite (T-P5-1) hasn't run. Wiring UI fields whose consumer is a
   not-yet-implemented analytic violates the signal/noise rule — the consumer
   doesn't exist yet.
2. **DNALab assembly is not verified.** `VehicleDNA` gates nearly every conditional
   field in `FieldMap.md`. Its assembly integration test is red (vocabulary drift,
   T-DL-3 pending), so DNA-driven field visibility cannot be trusted end-to-end.

The OBDLab + COMLab wiki-path failures look like a repo reorg (wikis moved) that
left stale path constants in tests. They are not engine-logic failures and are out
of scope to fix here — flagged for the owning lab sessions.

---

## Ready vs. blocked

- **Ready to wire now:** GASLab, DTCLab, VINLab, SymptomLab, OBDLab (engine logic).
- **Blocking full wire-up:** COMLab (orchestrator incomplete: T-P5-1 + phase 2/3
  analytics), DNALab (T-DL-3 assembly fixes pending).

---

## Options

- **A — Wait.** Finish COMLab T-P5-1 + phase 2/3 analytics and DNALab T-DL-3 in
  their own lab sessions, then re-run this gate and wire clean. (Recommended:
  matches "all modules finished coding" precondition.)
- **B — Partial wire-up.** Wire only the ready labs (GAS/DTC/OBD/VIN/Symptom) into
  the Streamlit shell now, stub the COMLab outputs that aren't implemented, and
  backfill when COMLab/DNALab land. Risk: ships UI fields with no live consumer.
- **C — Override the gate.** Proceed to wire against COMLab as-is, accepting red
  tests and missing analytics. (Not recommended.)
