# T-AUD-1a — plan correction 01 (Windows Cowork, 2026-11-03): Plan APPROVED with corrections

Plan: `repo/apps/wired/audit_tasks/progress_notes/T-AUD-1a.md` § `## Plan` (base `a4bd149`).
Reviews: first review `repo/apps/wired/audit_tasks/authoring/evidence/T-AUD-1a/plan_review/first_review_T-AUD-1a-plan.md`
(Windows Cowork, K1-K3); second review `…/plan_review/second_review_T-AUD-1a-plan.md` (DeepSeek ds-flash run by Linux
Cowork, ruled APPROVE WITH CORRECTIONS in channel 017, C1-C9). This is the row's one plan return.

Implement the plan as written, with the changes below. Each one replaces the plan item it names.

## Second review (017)
- **C1.** Scratch writes for G1 and G4 go to `C:/4DApp/recheck/T-AUD-1a/`, now a RUNTIME line in `### Files to
  touch ###`. Nothing else is written outside `repo/`.
- **C2.** The VIN decode entry is `vinlab.decode` (`repo/labs/vinlab/vinlab/__init__.py`, `def decode(vin: str, *,
  data_dir: Path | None = None) -> VinDNA`). Import it explicitly in `composition.py`:
  `from vinlab import VINDecodeError, decode as decode_vin`. The R2 absent-triage test calls `diagnose` through it.
- **C3.** Add `import re` to `ui_payload.py`.
- **C4.** The OBD-presence test excludes `per_cylinder_misfire_counts` and `number_of_banks`. NEW test: a
  misfire-only form sends no OBD dict and never returns `OBD_INPUT_INCOMPLETE`.
- **C5 (amended by Cowork).** `O2SensorType` (`repo/labs/obdlab/obdlab/schemas/dna_view.py`) has no `NONE` member: its
  members are `NARROWBAND_0_TO_1V`, `WIDEBAND_LINEAR` and `WIDEBAND_NB_SIM`. `NONE` is only the UI choice
  `active_upstream_o2_type == "NONE"`, and OBDLab needs the O₂ key (your measurement (c)(2)). So:
  the engine keeps requiring the O₂ key for the decoded type (an abort, never a crash). In the UI, when an OBD dict
  would be sent and `active_upstream_o2_type == "NONE"`, `validate_widgets` returns a `FieldIssue` on
  `active_upstream_o2_type` saying OBDLab needs an upstream O₂ reading. NEW test: type `NONE` with every other OBD
  field typed → that field issue, no run. PIN test: OBDLab raises without the O₂ key on the base (the measurement).
- **C6.** `test_r3_gaslab_unticked_no_gas_issue` is NEW, not PIN.
- **C7.** `test_r5_mil_only_sends_dtc_with_codes_cleared` is PIN. Add a NEW R5 test that the base gets wrong (for
  example: the default OBD/DTC boxes ticked and untouched → no OBD and no DTC dict in the payload), shown red on base.
- **C8.** The R2 branch uses `_missing(triage, _TRIAGE_KEYS)` (absent, `None` or blank). NEW test: all five keys
  present, one blank → the empty-symptom path, no `SymptomValidationError`.
- **C9.** The high-idle check is `composition.py:176`.
- **Timeouts.** Every long gate command runs under `timeout 290` (the task's Verification now carries them). Run
  `$PY -m pip install --no-input -r requirements.txt` as one step.

## First review (Windows Cowork)
- **K1.** No lab import in `apps/ui/`. Add a public `validate_triage(triage: dict) -> str | None` to
  `repo/apps/wired/wired/composition.py` (calls `symptomlab.resolve`; returns the `SymptomValidationError` message, or
  `None`), export it in `repo/apps/wired/wired/__init__.py` (`__all__`), and have `validate_widgets` call it. This
  replaces C11's lazy `symptomlab` import in `ui_payload.py`.
- **K2.** One PIN test per copied lab constant: `_TRIAGE_KEYS` equals `dnalab/assembly.py`'s required triage keys, and
  `_FREEZE_FRAME_KEYS` equals DTCLab's `_MANDATORY_PIDS` (a test may read a private name).
- **K3.** The DTC dict is also sent when a valid Mode 06 row is present (R5 is corrected in the task file). C8 stands:
  FF is required in the UI only with a confirmed code; a Mode 06-only form without FF gets `FREEZE_FRAME_INCOMPLETE`
  from the engine.

C1-C6, C8-C10, C12 and C13 of your `### 0` table stand as written; C7 and C11 are replaced by K3 and K1.
Two commits as planned. The 90-minute clock starts at the first code edit.
