# T-AUD-1a — public app usable: registry importable, no crash on blank/unticked input (COMMIT)
**Pack:** audit (app-scoped fix rows of `audit/FIX_PLAN.md`) · **Blocked by:** — · **Lane:** coder
**Priority:** P0 (`FIX_PLAN.md` T-AUD-1, split 2026-11-02: 1a = app usable, 1b = deploy manifests; 1a runs first)
**Branch:** `fix/T-AUD-1a`, cut from `audit-r2`. Never `main` (`main` redeploys https://www.5-gasanalyzermot.com/).
No push, no merge: the architect reviews the branch first.
**Findings owned:** F-C1-5 (= F-C4-1), F-C4-9, F-C5-1 (= R1-L1), F-C5-2, F-C5-13, F-P2-1 (UI part only).
**Evidence:** `audit/reports/R1_C1_20261017.md` §F5, `R1_C4_20261017.md` §F-C4-1/F-C4-9, `R1_C5_20261017.md`
§F-C5-1/2/13, `P2_census_20261026.md` §F-P2-1.
STRICT-ONLY: Load skills: `labs/comlab/_comlab_skills/comlab-python/SKILL.md`,
`labs/comlab/_comlab_skills/comlab-verification-loop/SKILL.md`, `apps/wired/_wired_skills/wired-python/SKILL.md`,
`apps/wired/_wired_skills/wired-composition-contract/SKILL.md`, `apps/wired/_wired_skills/wired-verification-loop/SKILL.md`
(read all five before the first edit; a skill that contradicts this spec is a stop → ask the architect).
**Fork F-1 ruled A** (architect, 2026-11-02): see the Fork section.

## Why
The live app fails a normal first use (seen live 2026-10-17). It fails four ways, each one an uncaught exception that
shows as "Diagnostic calculation failed: …":
`'co2'` (blank gas field), `missing required triage keys` (no symptom picked), `PIDValidationError` /
`FreezeFrameIncompleteError` (default-ticked OBD/DTC boxes left empty), `DTCFormatError` (pasted scanner list). The
deployed REG-V2 default path also cannot import `registry` at all, so even a complete form fails.

## Write scope (exactly these files)
| file | change |
|---|---|
| `labs/comlab/pyproject.toml` | package `registry` with comlab: `packages.find` include `registry*` (exclude `registry.tests*`, `registry.tools*`); `package-data` for the files the registry reads at runtime (inventory them first: `grep -n "open(\|read_text\|Path(" labs/comlab/registry/integration_shim.py labs/comlab/registry/shim/*.py`). No other key changes (versions, deps, extras = T-AUD-1b / T-AUD-6). |
| `labs/comlab/comlab/core/lab_pipeline_aggregator.py` | **additive only**: a public factory `build_input_incomplete_output(metadata, horizon, error_code, message)` that returns the existing `FATAL_INCOMPLETE` shape (`_build_fatal_incomplete_output`, `degradation_mode="FATAL_INCOMPLETE"`, `fault_family="invalid_input"`, `# wiki: vocabulary.py:571`). Refactor `_build_fatal_incomplete_output` to call it. No change to any existing verdict path. |
| `apps/wired/wired/composition.py` | never raise on absent or partial input (rules R2-R4 below). |
| `apps/ui/ui_payload.py` | payload rules R3-R5; a new `validate_widgets(widgets) -> list[FieldIssue]` (field key, message). `build_diagnose_payload` never raises on user input. |
| `apps/ui/app.py` | before Run: call `validate_widgets`; any issue → `st.warning` per field (not `st.error`, not "Diagnostic calculation failed"), `diagnose()` not called. GASLab untick/re-tick keeps typed values (keep them in `st.session_state` under keys that survive unmount). |
| `apps/ui/tests/`, `apps/wired/tests/`, `labs/comlab/tests/unit/` | new tests per rule (below); keep existing tests unchanged. |
| `apps/wired/audit_tasks/progress_notes/T-AUD-1a.md`, `apps/wired/audit_tasks/PROGRESS.md` | gate blocks; ledger row → `done`. |
Nothing else: no wiki edit, no other lab, no registry code, no corpus, no `requirements.txt`, no `render.yaml`.

## Rules (what "fixed" means)
- **R1 registry importable (F-C1-5).** With only `pip install -r requirements.txt` (no `PYTHONPATH`, no `labs/comlab` on
  `sys.path`) and `sys.path[:0]=['.','apps/ui']`, `wired.diagnose(MW-002)` returns a verdict. Re-run
  `C:\4DApp\.venv\Scripts\python -m pip install -r requirements.txt` after the pyproject change.
- **R2 no symptom picked (F-C4-9).** Absent or incomplete `triage` is the documented absent-symptom case: a decodable VIN
  is still decoded (VIN DNA kept), `symptom_dna` is empty, the run continues. `VINDecodeError` keeps today's
  `_build_fallback_vin_dna` path. A complete but invalid triage still raises `SymptomValidationError` inside the UI's
  validation (field warning), never in the result pane.
- **R3 gas (F-C5-1).** Wiki: gas is the backbone for a running engine (`labs/comlab/wiki/07_pipeline_stages.md`
  §Degradation modes; only `will_not_start` suppresses GASLab, §RULE_LAB_SUPPRESSION).
  UI: GASLab ticked → the 5 low-idle fields are required; any blank → field warnings, no run. Engine
  (`composition.py`): low-idle gas incomplete or absent → **no `KeyError`**: return
  `build_input_incomplete_output(…, error_code="GAS_INPUT_INCOMPLETE", message=<the missing fields>)`. High idle keeps
  its all-or-nothing rule (`composition.py:174`), now stated in the field help.
  **Non-starter: see Fork F-1.**
- **R4 OBD / DTC boxes (F-C5-2).** An OBD dict is sent only when at least one live OBD value is typed (`number_of_banks`
  and `None` placeholders do not count); otherwise it is omitted → `GAS_DOMINANT` (wiki §Degradation modes). If any is
  typed, the 5 required OBD fields (upstream O₂ for the decoded sensor type, STFT B1, LTFT B1, RPM, ECT) are required
  in the UI. A DTC dict is sent only when a code is typed or a MIL box is ticked; the 12 freeze-frame PIDs are required
  only when a confirmed code is typed (FieldMap §10: a freeze frame exists only when a code set). The engine
  never raises on a partial OBD set or an incomplete freeze frame: it returns `build_input_incomplete_output` with
  `OBD_INPUT_INCOMPLETE` / `FREEZE_FRAME_INCOMPLETE` and the missing fields.
  `codes_cleared` is carried whenever a DTC dict is sent (mapping unchanged; F-P4-5 is not this row).
- **R5 free-text tokens (F-C5-13).** DTC fields split on `[\s,;/]+`; a parenthesised note (`(pending)`) is not a token;
  each token must match `^[BCPU][0-3][0-9A-F]{3}$` (FieldMap §9, DTCLab mode $03). Monitor IDs must match
  `MID_<HEX>_TID_<HEX>` (DTCLab wiki §13.1). Invalid tokens and rows → field warning listing them; they are
  excluded from the payload, so `build_diagnose_payload` cannot raise on them.

## Fork F-1 (architect ruling needed before code) — non-starter with GASLab unticked
`OrchestratorInboundRequest.gas_lab_output` is required (`labs/comlab/comlab/schemas/ingestion.py:559`), while the wiki
suppresses GASLab for `will_not_start`.
- **A (recommended for 1a):** the composition returns `build_input_incomplete_output(…, "GAS_INPUT_INCOMPLETE")` with
  a message saying non-start diagnosis without exhaust readings is not available yet. The probe
  `test_f1_non_starter_needs_gas` turns green because nothing raises, **but the wiki behaviour is not delivered**. The
  progress note must say so, and a residual line goes to T-AUD-4 (cross-lab inputs: make `gas_lab_output` optional
  when `suppress_gaslab`).
- **B:** make `gas_lab_output: GasLabPayload | None` in COMLab now, allowed only when the symptom router suppresses
  GASLab. This is the wiki-correct behaviour, but it touches the production verdict path (Stage A, prune, scoring
  all read `gas_lab_output`). Lost under A because 1a should stay out of COMLab's verdict logic (T-AUD-2 owns it).

## Probes — must turn green (acceptance)
| finding | probe (run from repo root) |
|---|---|
| F-C1-5 | `audit/scratch/C1/test_c1_era_pids_deploy.py::test_default_path_imports_in_deployed_layout` |
| F-C4-1 | `audit/scratch/C4/test_c4_probes.py::test_f1_diagnose_runs_in_requirements_install` |
| F-C4-9 | `audit/scratch/C4/test_c4_probes.py::test_f8_ui_payload_without_dna_module_is_accepted` |
| F-C5-1 | `audit/scratch/C5/test_c5_probes.py::test_f1_live_co2_message_apptest`, `::test_f1_blank_gas_matrix`, `::test_f1_gaslab_untick_wipes_values`, `::test_f1_non_starter_needs_gas` (Fork F-1) |
| F-C5-2 | `audit/scratch/C5/test_c5_probes.py::test_f2_default_modules_minimum_form` |
| F-C5-13 | `audit/scratch/C5/test_c5_probes.py::test_f13_free_text_tokens` |
| F-P2-1 (UI) | `apps/ui/tests/test_ui.py::test_e2e_mw002_fixture`, `::test_e2e_abstain_case`, and the whole `apps/ui/tests` suite |
Measured red on `audit-r2` 2026-11-02 (Windows): all 9 audit probes above fail; `apps/ui/tests` = 2 failed (the two
E2E tests), 6 passed.

## Expected red after this task (owned by other rows — do not fix, report any that flips)
- C1: every probe except the one above (42 of today's 43 red: T-AUD-2/3/4/9).
- C4: the other 10 (`test_f2`, `f3`, `f3b`, `f4`, `f5`, `f6[×2]`, `f7[×3]`: T-AUD-4).
- C5: the other 13 (`f3`, `f4`, `f5×2`, `f6×2`, `f7`, `f8`, `f9`, `f10×2`, `f11`, `f12`: T-AUD-3/4/10).
Any probe in these lists that changes colour must be named in the progress note with the reason. Do not accept a
side-effect fix silently.

## Gate (STRICT, both blocks in the progress note)
1. The 8 baseline suites (`bash audit/tools/baseline.sh`) have no new failure or error. Counts may rise only by the
   tests this task adds (list them). Erosion/isolation figures recorded.
2. `apps/ui/tests` all green; the 9 audit probes above green; the expected-red lists unchanged except as reported.
3. `ruff check` and `pyright` clean on every touched file.
4. `git status --porcelain` shows only the write scope. Restore `labs/comlab/registry/docs/case_library.html` if a
   registry suite rewrote it (CRLF on Windows; T-AUD-6).
5. Commit on `fix/T-AUD-1a` by explicit path, one commit, message `fix(T-AUD-1a): …`. No push.

## Out of scope
- T-AUD-1b: deploy manifests and constraints (F-P5-1, F-P5-2, F-P5-4): bare first-party deps, dnalab deps, lock file,
  `requirements.txt`, `render.yaml`.
- T-AUD-2/3/4/9/10 probes and behaviour (verdict correctness, output labels, cross-lab inputs, VIN decode, UI
  presentation); F-P4-5 `codes_cleared` mapping; the registry/v7 suites of F-P2-1 (T-AUD-6).
- After merge (not this task): the architect checks the live app loads and runs the four live failure inputs.

## Environment (Windows host, accepted 2026-11-02)
`C:\4DApp\.venv` (Python 3.14.6; Render pins 3.14.3). Every pytest run: `PYTHONDONTWRITEBYTECODE=1`,
`-p no:cacheprovider`. `.sh` tools in Git Bash with `/c/4DApp/.venv/Scripts` first on `PATH`. The C5 probes take ~2.5 min.
