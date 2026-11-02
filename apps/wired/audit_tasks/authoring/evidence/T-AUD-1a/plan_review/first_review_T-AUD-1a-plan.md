# T-AUD-1a plan — first review (Windows Cowork, 2026-11-02, reviewing-implementer-plan-gates)

Plan: `repo/apps/wired/audit_tasks/progress_notes/T-AUD-1a.md` § `## Plan` (written 22:39-22:49Z, base `a4bd149`).
The second-model review is Linux Cowork's (channel 016). This file is not an approval.

**Verdict: PROCEED after named corrections** (K1-K3 below), pending the second review.

## The seven checks
1. **Numbers re-derived.** The OBD required set (R5's five plus bank-2 trims), the 12 FF PIDs, `DTC_REGEX` and
   `MID_KEY_PATTERN` cite lab lines; I re-ran the FF anchor (`freeze_frame_extractor.py:15` `_MANDATORY_PIDS`, `:58`
   the missing-list). The registry inventory (16 `rules/*.json`) matches the grep the spec named. No number contradicts.
2. **Gates measure their property.** G4 (wheel contents) is right: editable installs ignore `package-data`, so the
   deployed-layout probes alone cannot catch a wrong `package-data` line. G1 (corpus census before/after, diff empty)
   measures "no stricter than the lab".
3. **Contradictions.** None between the plan and the spec. C7 is a real tension inside R5 (see K3).
4. **The convenient conclusion, tested hardest: C11.** Probe `test_f12_ui_lab_import` (F-C5-12, expected red, T-AUD-10)
   scans `apps/ui/app.py` only. C11 puts `import symptomlab` in `apps/ui/ui_payload.py`, which the probe cannot see.
   That passes the probe while adding the coupling the probe exists to remove (K1).
5. **Current artefact.** The plan quotes today's lines at `a4bd149`; MIL boxes default `False` (`app.py:589`, `:591`),
   so C8 cannot make a default form abort.
6. **Inputs' acceptance.** The R0 lab exception and `abort_incomplete` follow 008; Fork F-1 = A is stated (R4).
7. **Unsaid.** The wired copies of lab constants (`_TRIAGE_KEYS`, `_FREEZE_FRAME_KEYS`) have no drift check (K2).

## Corrections
- **K1 (CONCERN) — C11: no lab import in `apps/ui/`.** Validate the triage through wired, the UI's one engine entry:
  a public `wired.validate_triage(triage) -> str | None` in `composition.py` (calls `symptomlab.resolve`, returns the
  `SymptomValidationError` message or `None`), exported from `wired/__init__.py` if that is the import surface.
  `validate_widgets` calls it. The probe's population stays honest, and F-C5-12 does not grow.
  *Lost:* the lazy import in `ui_payload.py` (one function fewer in wired).
- **K2 (CONCERN) — constant drift.** `_TRIAGE_KEYS` copies `dnalab/assembly.py:32` and `_FREEZE_FRAME_KEYS` copies
  DTCLab's private `_MANDATORY_PIDS`. Add one PIN test per copy that asserts equality with the lab's value (a test may
  read a private name). *Lost:* nothing; importing a private lab name into production wired was the alternative.
- **K3 (ruling on C7) — keep typed Mode 06 rows.** Send the DTC dict when a valid code is typed, a MIL box is ticked,
  **or a valid Mode 06 row is present**. A user's valid input must not vanish silently. The FF rule is unchanged (C8):
  required in the UI only with a confirmed code; a Mode 06-only form without FF gets `FREEZE_FRAME_INCOMPLETE` from
  the engine, a result and not a crash. *Lost:* the letter of R5's "only"; R5 is corrected to this wording.

C1-C6, C8-C10, C12, C13 are accepted as written.
