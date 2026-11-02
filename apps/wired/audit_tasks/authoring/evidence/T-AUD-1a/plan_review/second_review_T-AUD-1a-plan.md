# T-AUD-1a plan — second review (copied 2026-11-03 from C:/Cowork/files/codex_T-AUD-1a-plan.out, unedited below the rule)

Model: DeepSeek ds-flash, run by Linux Cowork (channel 017). Its own last line was REDESIGN; Linux Cowork ruled
APPROVE WITH CORRECTIONS (C1-C9, 017), which is the verdict of record for this file.

---

# Findings

1. **Planned gates write outside `### Files to touch ###` into a Cowork-owned directory**  
   **Severity:** HIGH  
   **Plan:** `T-AUD-1a.md:203`, `:206`, `:243`, `:246`  
   **Evidence:** G1 writes `C:/4DApp/recheck/T-AUD-1a/corpus_{before,after}.txt`; G4 runs `cp -r labs/comlab C:/4DApp/recheck/T-AUD-1a/comlab_src` and writes a wheel under `C:/4DApp/recheck/T-AUD-1a/wheel`. The task’s `### Files to touch ###` only authorizes repo paths plus `C:/4DApp/.venv` and `case_library.html` (`T-AUD-1a_app_usable(4).md:165-177`), and `### Out of scope ###` says “every file in `C:/4DApp` outside `repo/`: Cowork owns them” (`:185`). This is the task’s stop class (c).  
   **Settling command:** `grep -n "recheck\|Files to touch\|outside" /agent_workspace/export/winpc_setup/T-AUD-1a_review/T-AUD-1a_app_usable\(4\).md /agent_workspace/export/winpc_setup/T-AUD-1a_review/T-AUD-1a.md`

2. **The R2 replacement path references an unimported `vinlab` module**  
   **Severity:** HIGH  
   **Plan:** `T-AUD-1a.md:162`  
   **Evidence:** The plan says `decode_vin` = `vinlab.decode` and claims “vinlab is already imported here.” The only VINLab import in composition is `from vinlab import VINDecodeError` (`src/apps/wired/wired/composition.py:60`); there is no `import vinlab` or `decode_vin` binding. A literal implementation raises `NameError`, so the absent-triage probe cannot pass.  
   **Settling command:** `grep -n "vinlab\|decode_vin" /agent_workspace/export/winpc_setup/T-AUD-1a_review/src/apps/wired/wired/composition.py`

3. **The exact `ui_payload.py` snippet uses `re.compile` without importing `re`**  
   **Severity:** MEDIUM  
   **Plan:** `T-AUD-1a.md:175-176`  
   **Evidence:** The plan adds `_DTC_TOKEN_RE = re.compile(...)` and `_MID_RE = re.compile(...)`, but `src/apps/ui/ui_payload.py:1-8` imports only `dataclass` and `Any`. The module would fail at import with `NameError: name 're' is not defined`, breaking every UI test.  
   **Settling command:** `grep -nE '^import re$|^from re import|re\.compile' /agent_workspace/export/winpc_setup/T-AUD-1a_review/src/apps/ui/ui_payload.py` → no output for the base file.

4. **C9’s “misfire counts do not count” is contradicted by the §4 OBD-presence test**  
   **Severity:** HIGH  
   **Plan:** `T-AUD-1a.md:89` versus `:179-180`  
   **Evidence:** C9 says `per_cylinder_misfire_counts` “does not count as a ‘typed live OBD value’.” The proposed condition is `any(v is not None for k, v in obd.items() if k != "number_of_banks")`; the base builder sets `obd["per_cylinder_misfire_counts"]` from the misfire slider (`src/apps/ui/ui_payload.py:985-992`), so it is non-`None` and the OBD dict is sent. The plan’s OBD check then requires five live fields and returns `OBD_INPUT_INCOMPLETE` for a misfire-only form, which is the behavior C9 rejected.  
   **Settling command:** `sed -n '985,992p' /agent_workspace/export/winpc_setup/T-AUD-1a_review/src/apps/ui/ui_payload.py; sed -n '89p;179,180p' /agent_workspace/export/winpc_setup/T-AUD-1a_review/T-AUD-1a.md`

5. **The engine OBD check requires upstream O₂ even when the decoded sensor type is `NONE`**  
   **Severity:** HIGH  
   **Plan:** `T-AUD-1a.md:164` versus `:185`  
   **Evidence:** The UI validation correctly says O₂ is not required when O₂ type is `NONE`, and the builder skips the O₂ key in that case (`src/apps/ui/ui_payload.py:960-969`). The plan’s engine rule is “required = O₂ key + `_OBD_REQUIRED_KEYS` …” with no `NONE` branch. A form with `active_upstream_o2_type == "NONE"` and any other OBD value is therefore sent to the engine and aborted with `OBD_INPUT_INCOMPLETE`, although R5 says the required O₂ field is “for the decoded sensor type.”  
   **Settling command:** `grep -n 'o2_type != "NONE"\|pid_oxygen_sensor_volts' /agent_workspace/export/winpc_setup/T-AUD-1a_review/src/apps/ui/ui_payload.py`

6. **`test_r3_gaslab_unticked_no_gas_issue` cannot be a PIN under the plan’s own red gate**  
   **Severity:** MEDIUM  
   **Plan:** `T-AUD-1a.md:230`, `:239`  
   **Evidence:** The plan places this test in `test_t_aud_1a_validation.py` and labels it PIN with the rule “each PIN must pass on the base.” `validate_widgets` does not exist on the base (`grep` finds no `def validate_widgets` in `ui_payload.py`); a validation test importing it fails at collection on the base. It must be NEW, or the red-gate rule is unsatisfiable.  
   **Settling command:** `grep -n "def validate_widgets" /agent_workspace/export/winpc_setup/T-AUD-1a_review/src/apps/ui/ui_payload.py || echo absent`

7. **`test_r5_mil_only_sends_dtc_with_codes_cleared` is mislabeled NEW—it passes on the base**  
   **Severity:** MEDIUM  
   **Plan:** `T-AUD-1a.md:233`, `:239`  
   **Evidence:** The base builder sends `dtc` with `codes_cleared=False` whenever `dtc_module` is ticked (and `active_mil=True` when the MIL box is ticked), without needing any new code (`src/apps/ui/ui_payload.py:1045-1057`). Running the base builder gives:
   `{'dtc': {'active_mil': True, 'codes_cleared': False}}`
   The test therefore passes on the base and cannot serve as the plan’s required red NEW test.  
   **Settling command:** `cd /agent_workspace/export/winpc_setup/T-AUD-1a_review/src/apps/ui && python3 -c "from ui_payload import build_diagnose_payload; print(build_diagnose_payload({'dtc_module':True,'dtc_active_mil':True}))"`

8. **The R2 completeness test checks key presence, not missing/blank values**  
   **Severity:** MEDIUM  
   **Plan:** `T-AUD-1a.md:153-162`  
   **Evidence:** The plan defines `_missing(inputs, keys)` as “absent, `None`, or a blank string,” but the R2 branch uses `if all(k in triage for k in _TRIAGE_KEYS):`. A triage dict with all five keys present but one or more `None`/blank values enters `build_vehicle_dna` and can still raise `SymptomValidationError`; R2 says absent **or incomplete** triage must be treated as the empty-symptom case.  
   **Settling command:** `nl -ba /agent_workspace/export/winpc_setup/T-AUD-1a_review/T-AUD-1a.md | sed -n '157,162p'`

9. **The high-idle check line citation is off by one**  
   **Severity:** LOW  
   **Plan:** `T-AUD-1a.md:163`  
   **Evidence:** The plan cites `composition.py:177` for `if all(gas_inputs.get(key) is not None ...)`; line 177 is `high_reading = GasReading(...)`. The actual check is line 176.  
   **Settling command:** `nl -ba /agent_workspace/export/winpc_setup/T-AUD-1a_review/src/apps/wired/wired/composition.py | sed -n '174,178p'`

# Answers to the Six Questions

1. **§1 shape/horizon:** The proposed body reuses all `_build_fatal_incomplete_output` fields and derivation, and the refactored private method passes its explicit horizon and echo through, so the output shape is preserved. The R2 path itself has the import/definition defect above.

2. **§2 packaging:** `include = ["comlab*", "registry*"]` plus `registry = ["rules/*.json"]` covers the only runtime file read found in the supplied `integration_shim.py` (`_DEFAULT_RULES_DIR`, glob, `read_text`). No missing package-data path is demonstrated. The 16-file `registry/rules` inventory and the presence of `registry/schema_v2.py`/`registry/shim` are **UNSETTLED** because those files are not in the supplied copy. The G4 wheel check is the right kind of check, but it writes outside the authorized tree.

3. **§3 composition checks:** C4’s stated gas → OBD → FF ordering does place the new checks before `_run_gaslab`, `_run_obdlab`, and `_run_dtclab`, and R2 bypasses `build_vehicle_dna` for missing triage. It does not cover the `None`/blank triage values (finding 8), the `vinlab` import (finding 2), or the O₂ `NONE` case (finding 5); high-idle blank strings also remain unchanged and can still reach `int("")`.

4. **§4 UI:** C7/C8 follow R5’s literal “only” rules and do not cause a crash; MIL-only and pending-only forms intentionally reach the engine and return `FREEZE_FRAME_INCOMPLETE`. However C9/§4 sends OBD for a misfire-only form (finding 4), O₂ `NONE` is blocked by the engine check (finding 5), and C7 silently drops FF/Mode-06-only data, as the plan itself notes.

5. **§5-6 tests:** The MIL-only NEW test cannot fail for its target defect because the base already sends that payload (finding 7); the gaslab-unticked PIN cannot pass on the base if it exercises `validate_widgets` (finding 6). A mutant that only checks key presence in triage would also pass the R2 test suite, missing blank/`None` values.

6. **§7 commands:** G1/G4 write outside `### Files to touch ###` into `C:/4DApp/recheck` (finding 1). They do not touch `main` and do not push. No command has an explicit five-minute timeout; `pip install -r requirements.txt` and the full `labs/comlab` pytest run are not shown to stay under five minutes, so that requirement is **UNSETTLED**.

# Checked

- Task specification `T-AUD-1a_app_usable(4).md`, especially `### Files to touch ###`, `### Out of scope ###`, `### Success criteria ###`, and `### Verification ###`.
- Plan `T-AUD-1a.md:75-254`.
- `src/labs/comlab/comlab/core/lab_pipeline_aggregator.py` (`_build_fatal_incomplete_output`, `process`, horizon derivation).
- `src/labs/comlab/pyproject.toml`, `src/requirements.txt`, and `src/labs/comlab/registry/integration_shim.py`.
- `src/apps/wired/wired/composition.py`, including `build_vehicle_dna`, gas, OBD, and FF call sites.
- `src/apps/ui/ui_payload.py`, including the existing payload builder and option-1 behavior on the base.
- `src/apps/ui/app.py` Run block and gas widget keys.
- `src/apps/ui/tests/test_ui.py`.
- Commands used included `grep`, `sed`, `nl`, `wc`, and a read-only `python3 -c` base-payload check.

REDESIGN
---

APPROVE WITH CORRECTIONS
