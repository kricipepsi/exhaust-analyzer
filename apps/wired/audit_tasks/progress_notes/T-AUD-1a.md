# T-AUD-1a — progress note (app usable)

Task: `repo/apps/wired/audit_tasks/T-AUD-1a_app_usable(4).md` (plan: REQUIRED). Session 1 = readiness + plan, then
stop for Cowork's plan review. No production edit is made in this session.

## Baseline (First action, Preconditions, pinned values)

All commands from `C:/4DApp/repo`, `PYTHONDONTWRITEBYTECODE=1`, `PY=C:/4DApp/.venv/Scripts/python.exe`.

| check | command | observed | expected |
|---|---|---|---|
| branch | `git branch --show-current` | `fix/T-AUD-1a` | `fix/T-AUD-1a` |
| base | `git rev-parse --short HEAD`; `git rev-parse --short audit-r2` | `a4bd149`; `a4bd149` | the spec commit on `audit-r2` |
| tree | `git status --porcelain` | (empty) | empty |
| Preconditions | the `for p in …; do test -f` loop | `checked`, no `MISSING` | same |
| P1 | the 9 node ids, `\| tail -1` | `9 failed in 5.86s` | `9 failed` |
| P2 | `cd apps/ui && $PY -m pytest -p no:cacheprovider -q tests \| tail -1` | `2 failed, 6 passed in 1.67s` (both `ModuleNotFoundError: No module named 'registry'`) | `2 failed, 6 passed` |
| P4 | `$PY audit/tools/isolation.py \| tail -1` | `violations: 4` | `violations: 4` |

P3 (C1 42 / C4 10 / C5 13 expected-red) was not re-run in this session. It is a finish-line gate (Verification step 3);
the redispatch runs it before the first edit as the colour baseline.

Failure reason of each P1 probe today (`--tb=short`, `-s`):
- C1 `test_default_path_imports_in_deployed_layout`: `EXC ModuleNotFoundError No module named 'registry'`.
- C4 `test_f1_diagnose_runs_in_requirements_install`: `ModuleNotFoundError: No module named 'registry'`.
- C4 `test_f8_ui_payload_without_dna_module_is_accepted`: `SymptomValidationError: build_vehicle_dna: missing required
  triage keys: [...]`.
- C5 `test_f1_live_co2_message_apptest`: `rendered: ["Diagnostic calculation failed: 'co2'"]`.
- C5 `test_f1_blank_gas_matrix`: `KeyError: 'hc'|'co'|'co2'|'o2'|'nox'` for each blank, `ALL` and `MODULE_OFF`.
- C5 `test_f1_gaslab_untick_wipes_values`: `[None, None, None, None, None] == [120, 0.5, 14.5, 0.4, 30]`.
- C5 `test_f1_non_starter_needs_gas`: `KeyError: 'hc'`.
- C5 `test_f2_default_modules_minimum_form`: `PIDValidationError` (O₂, STFT, LTFT), `KeyError` (`engine_rpm`,
  `coolant_temp_c`), `FreezeFrameIncompleteError` (default `codes_cleared`-only DTC dict, and P0171 without FF).
- C5 `test_f13_free_text_tokens`: `DTCFormatError` on `P0171;P0420`, `P0171/P0420`, `(PENDING)`; `ValueError: Invalid
  MID key '21-01'`.

## Readiness challenge

- (a) Starting state matches the task: branch `fix/T-AUD-1a`, HEAD `a4bd149` = `audit-r2` (base), clean tree, P1/P2/P4
  as pinned (table above). Git: `git -C C:/4DApp/repo rev-parse --short HEAD` → `a4bd149`.
- (b) The tests fail for the intended reason: each of the 9 probes fails on the defect its finding names (list above):
  missing `registry` package (F-C1-5), triage-required crash (F-C4-9), gas `KeyError` (F-C5-1), OBD/FF raise (F-C5-2),
  token raise (F-C5-13), widget-state loss on untick (F-C5-1).
- (c) Independently derived decisive values: (1) `MAPPING` in
  `C:/4DApp/.venv/Lib/site-packages/__editable___comlab_0_1_0_finder.py` is `{'comlab': …}` only, so `registry` cannot
  import outside `labs/comlab` on `sys.path`; adding `registry*` to `packages.find` adds it to `MAPPING`. (2) The OBD
  required set measured by removing one field at a time is exactly R5's five (O₂ key per sensor type, `shrtft1`,
  `longft1`, `engine_rpm`, `coolant_temp_c`), plus `shrtft2`/`longft2` when `number_of_banks == 2`
  (`labs/obdlab/obdlab/core/trim_vector_aggregator.py:50-61`). An explicit `None` for RPM/ECT also raises
  (`ValidationError`), so an `is None` check is not stricter than the lab. (3) The FF mandatory set is DTCLab's
  `_MANDATORY_PIDS` (12, `labs/dtclab/dtclab/core/freeze_frame_extractor.py:15-28`), and `extract_freeze_frame` runs on
  **every** DTC dict (`data_fusion_sanitizer.py:95`), not only on a confirmed code. (4) `DTC_REGEX` =
  `^[BCPU][0-3][0-9A-F]{3}$` (`labs/dtclab/dtclab/schemas/vocabulary.py:109`) = R6; `MID_KEY_PATTERN` =
  `^MID_[0-9A-F]{2}_TID_[0-9A-F]{2}$` (`labs/dtclab/dtclab/schemas/mode06_result.py:11`). These match the probes' expectations.
- (d) No contradiction or missing decision blocks implementation. The open choices are listed under `## Plan` §0 for
  Cowork's ruling. None is a stop class (a)-(d).
- (e) Teach-back: the deliverable is two commits on `fix/T-AUD-1a`. Commit 1 makes `registry` an installed package and
  adds `LabPipelineAggregator.abort_incomplete`. Commit 2 makes `wired.diagnose` return a `FATAL_INCOMPLETE` /
  `invalid_input` verdict instead of raising on missing triage, gas, OBD or FF input, and makes the UI warn per field
  instead of running. The decisive check is Verification step 1 (`9 passed`), with step 3 keeping every other probe
  colour (C1 42, C4 10, C5 13 failed) and step 2 at `0 failed`.

## Assumptions worked past

1. `### Plan gate ###` item 3 asks for "the `composition.py` sites that raise today". Three of the five R3/R5 raises
   are inside the labs (OBDLab `PIDValidationError`, DTCLab `FreezeFrameIncompleteError`), not in `composition.py`. I
   quote the `composition.py` call site that hands the input to the lab, and the lab line that raises.
2. "`wired` only detects that a required input is missing (a mapping check with no fault logic)" (R0): I read
   "mapping check" as a key-presence check on the raw-input dict, done **before** the lab call. I rejected catching the
   lab exceptions in wired: `FreezeFrameIncompleteError` is not exported by `dtclab/__init__.py`, and a broad
   `except PIDValidationError` would also swallow bounds violations (the 3 corpus raises below), which are out of scope.
3. The P3 counts are pinned "on `audit-r2`". The redispatch re-runs them before the first edit and treats any
   difference as a stop (d).

## Plan

### 0. Choices the task leaves open (option taken / rejected / why)

| # | choice | taken | rejected | why |
|---|---|---|---|---|
| C1 | `abort_incomplete` horizon | derive from `metadata.resolved_horizon` exactly as `process()` does (`Horizon(...)`, `ValueError` → `Horizon.MODERN`, `lab_pipeline_aggregator.py:381-384`); keyword-only `horizon: Horizon \| None = None` override | a required `horizon` argument | 008 names no horizon; wired has none to pass. The override lets `_build_fatal_incomplete_output(request, abort, horizon)` keep its explicit horizon byte-for-byte |
| C2 | echo audit | keyword-only `echo: UserInputEchoAudit \| None = None`; `None` → the existing sentinel (`_echo_pass_through` body) | dropping the echo | the refactored private builder must still carry `request.user_input_echo_audit` verbatim (no verdict path change) |
| C3 | instance vs static | instance method (`self`), like `_build_fatal_incomplete_output` | `@staticmethod` (skips KG load) | matches R0's `LabPipelineAggregator.abort_incomplete(...)`; wired already constructs the aggregator on the run path |
| C4 | order of wired checks | gas → OBD → FF, all **before** any lab runs; the first incomplete section returns | one abort listing every section | one `error_code` per verdict (R3/R5 name one code each); gas is always required, so it is reported first |
| C5 | non-starter message (R4) | when `triage.get("engine_state") == "will_not_start"` and gas is incomplete, the message says non-start diagnosis without exhaust readings is not available yet, and lists the missing fields | a separate error code | R4 fixes the code as `GAS_INPUT_INCOMPLETE`; `will_not_start` is the same literal COMLab's router uses (`symptom_router.py:31`) |
| C6 | bank-2 trims | the wired OBD check also requires `shrtft2`, `longft2` when `number_of_banks == 2` | R5's five only | without it a 2-bank car still raises `PIDValidationError` (`trim_vector_aggregator.py:54-61`), which breaks "the engine never raises on a partial OBD set". UI stays at R5's five; the engine aborts on the bank-2 gap |
| C7 | DTC dict trigger (R5) | **letter of R5**: send `dtc` only when a valid code is typed or a MIL box is ticked | also send on a Mode 06 row or a typed FF value | R5 says "only". **Risk for Cowork:** today a form with 12 FF + a valid Mode 06 row and no code runs and sends Mode 06; under the letter, those values are omitted silently. Please rule; the change to the other option is one condition |
| C8 | FF required in UI | only when a confirmed code is typed (R5 letter) | whenever a DTC dict is sent | R5 letter. Engine side: DTCLab needs FF on every DTC dict, so MIL-only or pending-only forms return `FREEZE_FRAME_INCOMPLETE` from the engine (a result, not a crash) |
| C9 | misfire slider counts | `per_cylinder_misfire_counts` (symptom-derived) does not count as a "typed live OBD value" | it counts | it is not typed in the OBD panel; counting it would demand 5 OBD fields whenever a misfire cylinder is picked. Today that form raises, so no working case is lost. Advanced OBD numbers and the two advanced booleans do count |
| C10 | incomplete triage in UI | no warning (R2: the run continues with an empty `symptom_dna`) | warn on Tier 1 without Tier 2 | R2 makes it a valid run, and R7 blocks the run on any issue |
| C11 | invalid triage check in UI | `validate_widgets` calls `symptomlab.resolve(...)` (lazy import inside the function) on a complete triage and turns `SymptomValidationError` into a `FieldIssue("triage_tier_2", …)` | a UI copy of the tier table | R2 says the error is raised "inside the UI's validation". `apps/ui` is not under `labs/`, so rule 5 does not apply; probe `test_f12_ui_lab_import` scans `app.py` only, so its colour cannot change |
| C12 | stale result | when issues exist, `app.py` sets `st.session_state.diagnose_result = None` | keep the old result | an old verdict beside new field warnings misleads |
| C13 | gas keep-alive keys | shadow keys `_kept_<widget key>` for the 12 gas widget keys (`gas_hc`, `gas_co`, `gas_co2`, `gas_o2`, `gas_nox`, `gas_lambda`, and the six `_high` keys) | `on_change` callbacks | copied at the top of every run while the widget key exists; restored before the widget is created when the key is gone. `value=None` on these widgets, so Streamlit's "default value + Session State" warning does not fire |

### 1. `abort_incomplete` (R0, plan-gate item 1)

In `repo/labs/comlab/comlab/core/lab_pipeline_aggregator.py`, additive:

```python
def abort_incomplete(
    self,
    metadata: SessionMetadata,
    error_code: str,
    message: str,
    *,
    horizon: Horizon | None = None,
    echo: UserInputEchoAudit | None = None,
) -> OrchestratorFinalUIOutput:
```

- Body = today's `_build_fatal_incomplete_output` body with `meta = metadata`, `abort.error_code` → `error_code`,
  `abort.ui_remediation_message` → `message`, and `echo or <sentinel>`. `degradation_mode="FATAL_INCOMPLETE"`,
  `fault_family="invalid_input"`, `confidence_score=0.0`, same truncation limits. Raises nothing of its own
  (`ValidationError` only if `metadata` itself is invalid, which a `SessionMetadata` instance cannot be).
- It needs no `OrchestratorInboundRequest`: it reads only `metadata.session_id`, `metadata.vin_confidence`,
  `metadata.resolved_horizon`. Wired can call it when `gas_lab_output` (required, `ingestion.py:559`) cannot be built.
- `_build_fatal_incomplete_output(request, abort, horizon)` becomes one line:
  `return self.abort_incomplete(request.metadata, abort.error_code, abort.ui_remediation_message, horizon=horizon,
  echo=request.user_input_echo_audit)`. Imports gain `SessionMetadata`, `UserInputEchoAudit` if not already imported.

### 2. R1 packaging (plan-gate item 2)

Inventory (`grep -n "open(\|read_text\|Path(" labs/comlab/registry/integration_shim.py labs/comlab/registry/shim/*.py`):

```
labs/comlab/registry/integration_shim.py:103:_DEFAULT_RULES_DIR = Path(__file__).parent / "rules"
labs/comlab/registry/integration_shim.py:432:            data = json.loads(path.read_text(encoding="utf-8"))
labs/comlab/registry/integration_shim.py:1273:        self._rules_dir = Path(rules_dir)
```

Runtime data = the 16 `registry/rules/*.json` files (named at `integration_shim.py:108-125`; `ls rules | wc -l` → 16,
all `.json`, no subdirectory). Packages found under `registry`: `registry`, `registry.shim` (kept), `registry.tests`,
`registry.tools` (excluded). Exact edit to `[tool.setuptools.packages.find]` and `[tool.setuptools.package-data]`:

```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["comlab*", "registry*"]
exclude = ["tests*", "docs*", "scripts*", "registry.tests*", "registry.tools*"]

[tool.setuptools.package-data]
comlab = ["config/*.json", "config/*.yaml"]
registry = ["rules/*.json"]
```

No other key changes. Then `$PY -m pip install -r requirements.txt` from `C:/4DApp/repo` (writes only `.venv` and the
git-ignored `labs/comlab/comlab.egg-info`; risk: an isolated build fetches `setuptools`/`wheel`. If the host is
offline and it fails, that is a hand-back, not a workaround). Check: `MAPPING` in the comlab finder gains `'registry'`.

### 3. `composition.py` sites and the mapping checks (plan-gate item 3)

New module constants, each cited:
`_TRIAGE_KEYS = ("tier_1", "tier_2", "occurs_during", "engine_state", "load_state")` (`dnalab/assembly.py:32`);
`_GAS_LOW_IDLE_KEYS = ("hc", "co", "co2", "o2", "nox")` (the `GasReading(...)` fields at `composition.py:166-172`);
`_OBD_REQUIRED_KEYS = ("shrtft1", "longft1", "engine_rpm", "coolant_temp_c")` plus the O₂ key;
`_FREEZE_FRAME_KEYS` = the 12 of `freeze_frame_extractor.py:15-28` (`# wiki: DTC_VOCABULARY.md §12.1`).
One helper `_missing(inputs, keys) -> list[str]`: a key is missing when absent, `None`, or a blank string (the
existing blank idiom in this file: `str(v).strip() != ""`).

| rule | site raising today (quoted) | replacement mapping check |
|---|---|---|
| R2 | `vehicle_dna = build_vehicle_dna(vin, triage)` (`composition.py:97`) → raises in `dnalab/assembly.py:37-39` `raise SymptomValidationError(f"build_vehicle_dna: missing required triage keys: {missing}")` | `if all(k in triage for k in _TRIAGE_KEYS):` keep the current `build_vehicle_dna` path; `else:` `vin_dna = _as_dict(decode_vin(vin).to_json_payload())`, `symptom_dna = {}`. Both branches keep `except VINDecodeError: vin_dna = _build_fallback_vin_dna(vin)`. `decode_vin` = `vinlab.decode` (vinlab is already imported here; `VehicleDNA.to_json_payload()["vin_dna"]` is `self.vin_dna.to_json_payload()`, `dnalab/models.py:74`, so the dict is identical). Complete but invalid triage still raises from `diagnose`; the UI catches it first (C11) |
| R3/R4 | `hc=int(gas_inputs["hc"])`, `co=float(gas_inputs["co"])`, `co2=float(gas_inputs["co2"])`, `o2=float(gas_inputs["o2"])`, `nox=int(gas_inputs["nox"])` (`composition.py:166-172`) → `KeyError` | in `_diagnose`, after `metadata = _build_metadata(vin_dna)`: `missing_gas = _missing(gas_inputs, _GAS_LOW_IDLE_KEYS)`; if non-empty → `return aggregator.abort_incomplete(metadata, "GAS_INPUT_INCOMPLETE", <message listing missing_gas; non-start text per C5>)`. High idle: unchanged (`if all(gas_inputs.get(key) is not None for key in high_keys)`, `composition.py:177`) |
| R5 OBD | `obd_output = _run_obdlab(_as_dict(obd_inputs), vin_dna) if obd_inputs is not None else None` (`composition.py:117`) → raises in `o2_normalizer.py:112-115` (O₂), `trim_vector_aggregator.py:70+` (`_safe_float` on STFT/LTFT), `KeyError` on `engine_rpm`/`coolant_temp_c` | if `obd_inputs is not None`: O₂ key = `pid_wideband_equivalence_ratio` when `_build_obd_dna_view(vin_dna).upstream_o2_type == O2SensorType.WIDEBAND_LINEAR`, else `pid_oxygen_sensor_volts` (`o2_normalizer.py:89-96`); required = O₂ key + `_OBD_REQUIRED_KEYS` + (`shrtft2`, `longft2` if `obd_inputs.get("number_of_banks") == 2`); missing → `abort_incomplete(metadata, "OBD_INPUT_INCOMPLETE", …)` |
| R5 FF | `dtc_output = _run_dtclab(_as_dict(dtc_inputs)) if dtc_inputs is not None else None` (`composition.py:118`) → `freeze_frame_extractor.py:58-60` `raise FreezeFrameIncompleteError(missing)` | if `dtc_inputs is not None`: `_missing(_as_dict(dtc_inputs.get("raw_freeze_frame")), _FREEZE_FRAME_KEYS)` → `abort_incomplete(metadata, "FREEZE_FRAME_INCOMPLETE", …)` |

The aggregator is built once (`LabPipelineAggregator(enable_fatal_gates=enable_fatal_gates)`) and used for both
`abort_incomplete` and `process`. Bounds violations (`PIDValidationError: … outside bounds`) and `DTCFormatError` from
direct callers keep raising: out of scope (no R covers them; 3 corpus cases depend on it, §5).

### 4. UI (R3, R5, R6, R7)

`repo/apps/ui/ui_payload.py`:
- `@dataclass(frozen=True) class FieldIssue: field: str; message: str`.
- `_DTC_TOKEN_RE = re.compile(r"^[BCPU][0-3][0-9A-F]{3}$")` (`# wiki: dtclab DTC_REGEX, vocabulary.py:109`),
  `_MID_RE = re.compile(r"^MID_[0-9A-F]{2}_TID_[0-9A-F]{2}$")` (`# wiki: dtclab mode06_result.py:11`).
  `_split_dtc_tokens(text) -> tuple[list[str], list[str]]`: upper-case, drop `\([^)]*\)` notes, split on `[\s,;/]+`,
  return (valid, invalid).
- `build_diagnose_payload`: OBD dict sent only when `any(v is not None for k, v in obd.items() if k !=
  "number_of_banks")`; DTC codes from `_split_dtc_tokens` (valid only); Mode 06 rows only when `_MID_RE` matches; DTC
  dict sent only when `raw_dtcs` or `active_mil` or `mil_flashing` (C7), and then always with `codes_cleared` (mapping
  unchanged). Gas and triage building: unchanged. Never raises on widget input.
- `validate_widgets(widgets) -> list[FieldIssue]`, in this order: gas (GASLab ticked → each blank of the 5 low-idle
  widgets); triage (DNA ticked and all five triage keys present → `symptomlab.resolve`, C11); OBD (an `obd` dict would
  be sent → each blank of `obd_upstream_o2_val` (unless O₂ type `NONE`), `obd_shrtft1`, `obd_longft1`,
  `obd_engine_rpm`, `obd_coolant_temp_c`); DTC tokens (one issue per DTC field with invalid tokens, listed; one issue
  for invalid Mode 06 IDs, listed); FF (a valid confirmed code → each blank of the 12 FF widgets).
- `FIELD_HELP` for the six high-idle gas entries: append "High idle is used only when all five values (HC, CO, CO₂,
  O₂, NOx) are entered; a partial set is ignored." (R3).

`repo/apps/ui/app.py`:
- Import `validate_widgets`. In the Run block: `issues = validate_widgets(widgets)`; if issues → one
  `st.warning(f"{issue.field}: {issue.message}")` per issue (label text taken from the widget label where one exists),
  `st.session_state.diagnose_result = None`, no `build_diagnose_payload`/`diagnose` call. Else the current path,
  unchanged (the `try/except` stays for non-input faults).
- Gas keep-alive (C13): before the gas expanders, restore `_kept_<k>` → `<k>` when `<k>` is absent; at the top of the
  script, copy `<k>` → `_kept_<k>` when present.

### 5. Gates this plan adds (population checked / run over, false pass, false fail)

| gate | checked on (now) | will run over (command) | false pass | false fail | changes later steps? |
|---|---|---|---|---|---|
| G1 wired gas/OBD/FF/triage mapping checks | the probe widget sets above, and the 314-case v7 corpus census: `for cid,raw,*_ in load_corpus(): diagnose(raw)` → **311 ran, 3 raised** (`DTCFormatError 'GARBAGE'`, `PIDValidationError manifold_vacuum_kpa=999.0`, `coolant_temp_c=999.0`), 26.5 s | the same census before the first edit and after commit 2, writing per-case `fault_code` (or exception class) to `C:/4DApp/recheck/T-AUD-1a/corpus_{before,after}.txt`; `diff` must be empty | a check looser than the lab: the lab still raises (caught by the probes and the new parametrized tests per key) | a check stricter than the lab turns a running case into an abort: the census diff shows it (expected 0, because every abort replaces a case that raises today; RPM/ECT `None` measured to raise) | yes: the abort runs before any lab, so later lab steps never see incomplete input |
| G2 UI `validate_widgets` | the C5 widget sets (`c5_lib.base_widgets`) | `apps/ui/tests/test_t_aud_1a_validation.py` + C5 probes + `apps/ui/tests/test_ui.py` | a blank that the builder omits but no issue names: the engine abort still catches it (no crash), test per field | a warning on a form that should run: `test_f2` step 1 and `test_f1_*` through AppTest show it; `test_ui.py` E2E fixtures run through the builder | yes: issues stop the run (R7) |
| G3 token filters | the 5 `test_f13` strings | the new R6 tests + `test_f13` | a valid code dropped (test asserts both codes kept for each separator) | a non-code kept (test asserts `(PENDING)` and `21-01` absent from the payload) | yes: filtered payload reaches DTCLab |
| G4 wheel contents (R1) | not run yet | `cp -r labs/comlab C:/4DApp/recheck/T-AUD-1a/comlab_src` then `$PY -m pip wheel --no-deps --no-build-isolation -w C:/4DApp/recheck/T-AUD-1a/wheel C:/4DApp/recheck/T-AUD-1a/comlab_src`, list the zip: 16 `registry/rules/*.json` present, no `registry/tests/`, no `registry/tools/` | editable mode ignores package-data, so the deployed-layout probes alone would pass with a wrong `package-data` line: G4 covers that | none known | no (copy outside the clone) |

### 6. New tests (plan-gate item 4)

`repo/labs/comlab/tests/unit/test_abort_incomplete.py`:
- `test_abort_incomplete_fatal_incomplete_from_metadata_only` — NEW (no `abort_incomplete` on base).
- `test_abort_incomplete_unknown_horizon_defaults_modern` — NEW.
- `test_abort_incomplete_carries_echo_or_sentinel` — NEW.
- `test_fatal_gate_output_fields_pinned` — PIN (drives `process()` with `enable_fatal_gates=True` on an aborting
  request; asserts the `FATAL_INCOMPLETE` fields; passes on base and after the refactor).

`repo/apps/wired/tests/test_t_aud_1a_inputs.py`:
- R2: `test_r2_absent_triage_decodes_vin` (VIN `WME01MC01XH072806` → `vin_confidence == "PARTIAL"`,
  `resolved_horizon == "HORIZON_LEGACY"`) — NEW; `test_r2_incomplete_triage_runs_without_symptom` — NEW;
  `test_r2_undecodable_vin_keeps_fallback` — PIN.
- R3: `test_r3_missing_low_idle_gas_aborts[hc|co|co2|o2|nox]` — NEW; `test_r3_gas_absent_aborts` — NEW;
  `test_r3_partial_high_idle_is_ignored` — PIN.
- R4: `test_r4_non_starter_without_gas_aborts_with_message` — NEW.
- R5: `test_r5_partial_obd_aborts[<each of 5>]` — NEW; `test_r5_two_bank_obd_needs_bank2_trims` — NEW;
  `test_r5_wideband_obd_needs_equivalence_ratio` — NEW; `test_r5_dtc_without_freeze_frame_aborts` — NEW.

`repo/apps/ui/tests/test_t_aud_1a_validation.py`:
- R2: `test_r2_invalid_triage_is_field_issue` (`🚫 Vehicle Won't Start` + `Flat / sluggish always`, measured: rejected
  by `symptomlab.resolve`) — NEW.
- R3: `test_r3_blank_gas_field_is_field_issue` — NEW; `test_r3_gaslab_unticked_no_gas_issue` — PIN;
  `test_r3_gaslab_untick_keeps_values_apptest` — NEW.
- R5: `test_r5_untouched_obd_and_dtc_omitted` — NEW; `test_r5_one_obd_value_requires_five` — NEW;
  `test_r5_confirmed_code_requires_freeze_frame` — NEW; `test_r5_mil_only_sends_dtc_with_codes_cleared` — NEW.
- R6: `test_r6_dtc_separators_and_notes` — NEW; `test_r6_invalid_tokens_listed_and_omitted` — NEW;
  `test_r6_invalid_monitor_id_listed_and_omitted` — NEW.
- R7: `test_r7_blank_form_warns_and_skips_diagnose_apptest` — NEW (AppTest: `at.warning` non-empty, `at.error` empty,
  `diagnose_result` not set).

Red gate: each NEW test is run on the base before its production edit and must fail; each PIN must pass on the base.

### 7. Commands and the paths they write (redispatch)

1. Baseline: Verification step 3 (P3 colours) and the G1 census → `C:/4DApp/recheck/T-AUD-1a/corpus_before.txt`.
2. Commit 1: edit `labs/comlab/pyproject.toml`, `lab_pipeline_aggregator.py`; create
   `labs/comlab/tests/unit/test_abort_incomplete.py`; `$PY -m pip install -r requirements.txt` (writes `.venv`,
   git-ignored egg-info); G4 (writes only under `C:/4DApp/recheck/T-AUD-1a/`); COMLab gate block
   (`cd labs/comlab && $PY -m pytest -q -p no:cacheprovider`, expect `522 passed, 4 skipped, 2 errors` + the new
   tests; the registry suite by name, then `git checkout -- labs/comlab/registry/docs/case_library.html`); commit
   `fix(T-AUD-1a): package registry and add abort_incomplete` by explicit path.
3. Commit 2: edit `composition.py`, `ui_payload.py`, `app.py`; create the two test files; wired gate block
   (`cd apps/wired && $PY -m pytest -q -p no:cacheprovider`, UI tests, G1 census after); commit
   `fix(T-AUD-1a): input-incomplete aborts and UI field validation` by explicit path.
4. Finish line: Verification steps 1-6, task-end gate of `writing-4dapp-python-code`, `## Time`, RESULT.

## Fork F-1 statement (R4)

Option A ships: a non-starter with GASLab unticked returns `GAS_INPUT_INCOMPLETE` with a message that non-start
diagnosis without exhaust readings is not available yet. **The wiki behaviour (non-start diagnosis without gas) is not
delivered by this row.** T-AUD-4 owns option B (`gas_lab_output` optional), registered in `repo/audit/FIX_PLAN.md`.

## Time

| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| readiness + plan | 2026-11-02T22:39:17Z | 2026-11-02T22:49:14Z | 9 (`date -u -d` epoch difference / 60) | ABSENT (no context meter in this session) |
| redispatch: baselines | 2026-11-02T23:05:07Z | 2026-11-02T23:09:00Z | 3 | ABSENT |
| implementation (commit-1 + commit-2 work, all gates, note) | 2026-11-02T23:09:00Z (first code edit) | 2026-11-02T23:27:23Z | 18 | ABSENT |

The commit-1 / commit-2 boundary has no clock read, so the split between them is ABSENT (count 1 boundary, cause: not
read). The clock read at 23:20:40Z (before Verification step 1) is the only intermediate value.

The 90-minute stop rule was not reached (18 minutes from the first code edit). Wall-clock totals: session 1 = 9 min;
redispatch = 22 min (23:05:07 → 23:27:23).

## Redispatch (plan APPROVED, correction 01)

Start 2026-11-02T23:05:07Z. Base moved to `f999f42` (`git rev-parse --short audit-r2` → `f999f42`; branch
`fix/T-AUD-1a` at `f999f42`; `git status --porcelain` → only this note untracked). The correction has no
`### Plan-time digest ###` table, so there is nothing to recompute. Implementation follows `## Plan` with
correction 01: C1-C9 and K1-K3 replace the plan items they name (C7 → K3, C11 → K1).

Pre-edit baselines on `f999f42`:
- P3 (three commands, `timeout 290`): C1 `43 failed, 1 passed` (42 expected-red + 1 acceptance), C4 `12 failed`
  (10 + 2), C5 `19 failed` (13 + 6). This matches P3 plus the P1 acceptance probes.
- G1 census (`C:/4DApp/recheck/T-AUD-1a/census.py`): `314` cases, `311` ok →
  `C:/4DApp/recheck/T-AUD-1a/corpus_before.txt`.

First code edit: 2026-11-02T23:09:00Z (the 90-minute clock starts here).

## COMLab gate block (commit 1)

Red gate: `cd labs/comlab && $PY -m pytest -p no:cacheprovider -q tests/unit/test_abort_incomplete.py` on the base →
`3 failed, 1 passed` (the 3 NEW tests fail on `AttributeError: 'LabPipelineAggregator' object has no attribute
'abort_incomplete'`; the PIN passes). After the edit: `4 passed`.

| check | command | result |
|---|---|---|
| reinstall | `timeout 290 $PY -m pip install --no-input -r requirements.txt` | `Successfully installed comlab-0.1.0 … wired-0.1.0`; `MAPPING` gains `'registry': 'C:\\4DApp\\repo\\labs\\comlab\\registry'` |
| G4 wheel | `git ls-files` copy of `labs/comlab` → `C:/4DApp/recheck/T-AUD-1a/comlab_src`; `pip wheel --no-input --no-deps -w …/wheel …/comlab_src`; zip listing | `rules json 16`; `registry/tests 0`, `registry/tools 0`; registry modules `__init__`, `integration_shim`, `schema_v2`, `shim/__init__`, `shim/payload_mirrors` |
| comlab suite | `cd labs/comlab && $PY -m pytest -q --no-header -p no:cacheprovider --basetemp=C:/4DApp/recheck/T-AUD-1a/pt/comlab --continue-on-collection-errors` | `526 passed, 4 skipped, 2 errors` (baseline `522 passed, 4 skipped, 2 errors` + 4 new; the 2 errors are R0-2: `test_abstain_margin_002.py`, `test_tunable_reweight.py`) |
| registry suite | `… -q --basetemp=…/pt/registry registry/tests`, then `git checkout -- labs/comlab/registry/docs/case_library.html` | `5 failed, 489 passed` = the known F-P2-1 count (all 5 in `test_build_corpus.py`, missing data files) |
| deployed layout | C1 `test_default_path_imports_in_deployed_layout`, C4 `test_f1_diagnose_runs_in_requirements_install` | `2 passed` |
| compile / ruff / S | `py_compile`, `py -m ruff check`, `py -m ruff check --select S` on both files | ok; `All checks passed!`; production file S-clean; test file S101 only (`assert`), as the existing `test_fatal_gate_wiring.py` (18 × S101) |
| pyright | `py -m pyright --pythonpath C:/4DApp/.venv/Scripts/python.exe <both files>` | `0 errors` (1 error in my test helper, `str` for `VinConfidence`, fixed first) |
| anti-orphan | `grep -n "abort_incomplete(\|_echo_pass_through"` | `abort_incomplete` read by `_build_fatal_incomplete_output` (and by wired in commit 2); `_echo_pass_through` still read at lines 540, 611 |

Environment finding (not code): pytest's default `tmp_path` root
`C:\Users\Petra\AppData\Local\Temp\pytest-of-Petra\pytest-current` gives `PermissionError: [WinError 5]`. I did not
clean it (no broad cleanup); every suite that uses `tmp_path` runs with `--basetemp` under the RUNTIME scratch
`C:/4DApp/recheck/T-AUD-1a/pt/`. The first try without the parent folder gave 5 + 23 spurious `FileNotFoundError`
setup errors; with `mkdir -p` the counts above are clean.

## Plan stop

Stopped before the first edit, as the plan gate requires. No production file, test, or commit is changed. Cowork's
plan review in `corrections/` decides C1-C13, and the redispatch implements it.

## Blocked (soft: work complete, commits not made)

Record: `repo/apps/wired/audit_tasks/progress_notes/T-AUD-1a.blocker.json` (validator `OK`, 2 findings, both soft,
`stopped: false`).

1. **CONTRADICTION — the mandated commit identity is refused by `bash_guard`.** `C:/4DApp/AGENTS.md:119` mandates
   `git -c user.name=Claude -c user.email=noreply@anthropic.com commit …`. Every Bash command with that identity is
   refused. Settling command: `git -c user.name=Claude -c user.email=noreply@anthropic.com log -1 --oneline` →
   `PreToolUse:Bash hook error: bash_guard: a nested claude launch, --plugin-dir, CLAUDE_CODE_PLUGIN_DIRS or the
   dev-mods folder can load a mod; an implementer never names them`. A message file was also not possible:
   `impl_guard` refuses a Write-tool file under `C:/4DApp/recheck/T-AUD-1a/` (`… is denied: it is not in ### Files to
   touch ###`), although the task lists that folder as RUNTIME. **Interpretation:** no bypass (no PowerShell tool, no
   indirect spelling, no other identity). Both change sets are complete, gated, and left uncommitted on
   `fix/T-AUD-1a`. The R8 split is by path, so Cowork can make both commits from the working tree with no rework. The
   exact commands are in the RESULT.
2. **CONTRADICTION — criterion 3 (C4 stays at 10 failed) vs R5 (never raise on a partial OBD set).**
   `test_f3b_upstream_o2_override_reaches_obdlab` turned green. Its input is a WIDEBAND_AFR car with the wideband key
   removed and a NARROWBAND override; the override still does not reach OBDLab (F-C4-3, not fixed), so wired now
   returns `OBD_INPUT_INCOMPLETE … Enter: pid_wideband_equivalence_ratio` instead of the `PIDValidationError` crash.
   The probe asserts only "no exception". **This green is a false pass.** Any R5-compliant implementation makes it
   green unless the override is honoured (out of scope). I did not edit the probe.

## Wired gate block (commit 2)

Red gate on the base code (wired and UI code unchanged, commit-1 code in place):
- `cd apps/wired && $PY -m pytest … tests/test_t_aud_1a_inputs.py` → `21 failed, 4 passed`. The 21 NEW fail on
  `SymptomValidationError` (R2), `ImportError` (K1 `validate_triage`), `KeyError: 'hc'` (R3/R4), `PIDValidationError`
  / `KeyError` (R5 OBD), `FreezeFrameIncompleteError` (R5 FF). The 4 PINs pass (`test_r2_undecodable_vin_keeps_fallback`,
  `test_r3_partial_high_idle_is_ignored`, `test_r5_complete_obd_runs`, `test_r5_obd_lab_needs_o2_key`). The 2 K2 PINs
  (`test_k2_*`) fail on the base only by `ImportError` (the wired constants are new); they pin the lab-side values.
- `cd apps/ui && $PY -m pytest … tests/test_t_aud_1a_validation.py` → `14 failed, 2 passed`. The PIN
  `test_r5_mil_only_sends_dtc_with_codes_cleared` passes. `test_r5_mode06_row_sends_dtc` also passed on the base (the
  base sends a DTC dict whenever DTCLab is ticked), so I retagged it **PIN** (it pins K3 against the narrower R5
  letter).
- Two of my own test defects were fixed before trusting the gate: the non-starter Tier 2 code is
  `prolonged_crank_hard_start`; and `execution_meta.vin_confidence` is hard-coded `"HIGH"` by `process()`
  (`lab_pipeline_aggregator.py:518`, `:589`), so "VIN decoded" is asserted through `resolved_horizon`
  (`HORIZON_LEGACY` for `WME01MC01XH072806`; the fallback is `HORIZON_MODERN`). The hard-coded `HIGH` is out of scope
  (no edit).

After the edit:

| check | command | result |
|---|---|---|
| wired new | `cd apps/wired && $PY -m pytest -p no:cacheprovider -q --basetemp=…/pt/wired tests/test_t_aud_1a_inputs.py` | `25 passed` |
| wired suite | `cd apps/wired && $PY -m pytest -q --no-header -p no:cacheprovider --basetemp=…/pt/wired --continue-on-collection-errors` | `36 passed` (baseline 11 + 25) |
| UI suite | `cd apps/ui && $PY -m pytest -p no:cacheprovider -q --basetemp=…/pt/ui tests` | `24 passed` (P2's 6 + the 2 E2E + 16 new) |
| G1 census | `census.py …/corpus_after.txt`; `diff corpus_before.txt corpus_after.txt` | `314 311 ok`; diff empty |
| compile / ruff | `py_compile`; `py -m ruff check` on the 6 commit-2 files | ok; `All checks passed!` |
| ruff S | `py -m ruff check --select S --ignore S101 <6 files>` | 1 hit: `apps/ui/app.py:139:5: S110` — pre-existing (`git show f999f42:apps/ui/app.py` → same hit at `:138:5`); production files S101-clean |
| pyright | `py -m pyright --pythonpath C:/4DApp/.venv/Scripts/python.exe <6 files>` | `0 errors, 0 warnings, 0 informations` |
| anti-orphan | `grep -rn <name> apps --include=*.py` minus the definition, for 20 new names | every name has ≥ 1 reader (`validate_widgets` 9, `validate_triage` 11, `_incomplete_input` 1, `GAS_WIDGET_KEYS` 2, …) |

## VERIFICATION GATE

Run from `C:/4DApp/repo`, Git Bash, `PY=C:/4DApp/.venv/Scripts/python.exe`, `PYTHONDONTWRITEBYTECODE=1`.

| step | expected | observed | verdict |
|---|---|---|---|
| 1. 9 acceptance probes | `9 passed`, no `failed`/`error` | `9 passed in 5.80s` | PASS |
| 2. `apps/ui/tests` | `0 failed`, ≥ 8 passed | `24 passed in 3.33s` | PASS |
| 3. C1 / C4 / C5 suites | C1 `42 failed`, C4 `10 failed`, C5 `13 failed` | C1 `42 failed, 2 passed`; C4 **`9 failed, 3 passed`**; C5 `13 failed, 6 passed` | C1 PASS, C5 PASS, **C4 FAIL by one probe**: `test_f3b_upstream_o2_override_reaches_obdlab` (false green, Blocked §2) |
| 4. import | `import ok` | `import ok` | PASS |
| 5. baseline + isolation | no new failure vs `baseline_20261017.txt`; `violations: 4` or fewer | exact command: 4 suites print `PermissionError: [WinError 5] … pytest-current` (environment, see COMLab gate block). Re-run with `PYTEST_ADDOPTS=--basetemp=C:/4DApp/recheck/T-AUD-1a/pt/base`: comlab `526 passed, 4 skipped, 2 errors`, dnalab 27, dtclab 590, gaslab `208 passed, 2 skipped, 4 deselected`, obdlab `388 passed, 2 skipped`, symptomlab 63, vinlab `203 passed, 8 skipped`, wired `36 passed` = baseline + 4 (comlab) + 25 (wired). `violations: 4` | PASS (with the basetemp re-run) |
| 6. git | exactly 2 commits; status = note + RESULT | `git log --oneline audit-r2..HEAD` → (empty); status lists the 6 modified + 4 new files + the note folder | **FAIL** (no commits: Blocked §1) |

Absence of the previous decisive failures: no `ModuleNotFoundError: No module named 'registry'` (C1, C4 f1, UI E2E);
no `KeyError: 'co2'`/`'hc'`; no `SymptomValidationError` for missing triage; no `PIDValidationError` /
`FreezeFrameIncompleteError` on partial input; no `DTCFormatError` on `;`, `/` or `(pending)`; untick/re-tick keeps
`[120, 0.5, 14.5, 0.4, 30]`.

Probe colour changes (criterion 3): the 9 acceptance probes red → green (intended). `test_f3b_upstream_o2_override_reaches_obdlab`
red → green (unintended, false pass, reason above). No other probe changed colour (C1 42 and C5 13 unchanged).

## CODE REVIEW

Task-end gate of `writing-4dapp-python-code`, items 1-10:
1. compile/ruff/S: PASS (S110 at `app.py:139` pre-existing; S101 only in tests, the repo convention).
2. pyright on the 9 touched `.py` files: `0 errors` (commit-1 pair and commit-2 six).
3. import sanity: `import ok`.
4. scoped tests: comlab `526 passed, 4 skipped, 2 errors` (R0-2); registry `5 failed, 489 passed` (known F-P2-1);
   wired `36 passed`; UI `24 passed`.
5. baseline: equal except this row's tests (basetemp re-run, above).
6. acceptance green; expected-red: one false green (`f3b`), named.
7. isolation: `violations: 4`.
8. anti-orphan: PASS (every new name read outside its definition; `abort_incomplete` read by
   `_build_fatal_incomplete_output` and `composition._diagnose`).
9. diff review: every changed line traces to R0-R7, K1, K3, C3-C5, C8, C13. `composition.py` adds `symptomlab` and
   `vinlab.decode` imports (composition is the one legal multi-lab point). No lab other than COMLab is edited. No
   probe edited.
10. `git status --porcelain`: only the write scope (no `case_library.html`; restored after each registry run).

Review axes: Scope PASS. Contracts PASS (no new COMLab payload field; the abort reuses the existing output model).
Provenance PASS (the FF keys carry `# wiki: DTC_VOCABULARY.md §12.1`; the regexes cite the DTCLab constants). Boundaries
PASS (no cross-lab import inside `labs/`; `apps/ui` imports no lab, only `wired`, per K1). Tests PASS (no network;
AppTest is headless).

**Verdict: BLOCKED** on two in-scope gates (step 6, no commits; step 3, C4 one probe). Neither is a code defect: both
are the spec findings in `## Blocked`. The code gates (1, 2, 4, 5) are clean.

## Decisions the task did not specify

- `--basetemp` under `C:/4DApp/recheck/T-AUD-1a/pt/` for every suite that uses `tmp_path` (environment, above).
- The non-start message is used whenever `triage.engine_state == "will_not_start"` and gas is incomplete (C5 of the
  plan).
- UI warnings show `issue.message` (a human label is part of the message); `issue.field` stays the widget key.
- `validate_widgets` reads triage from `build_diagnose_payload(widgets)` so the UI-to-internal mapping exists once.
- `test_r5_mode06_row_sends_dtc` retagged PIN (passes on base).

## Fork F-1 statement (R4), as delivered

A non-starter with GASLab unticked returns `GAS_INPUT_INCOMPLETE`: "Non-start diagnosis without exhaust gas readings
is not available yet. Enter the low-idle gas readings: hc, co, co2, o2, nox." **The wiki behaviour (non-start
diagnosis without gas) is not delivered by this row.** T-AUD-4 owns option B.

## Uncertainty

- The AppTest UI tests and probes exercise the warning path headless; I did not run `streamlit run` in a browser.
- MIL-only and pending-only forms pass UI validation (FF required in the UI only with a confirmed code, plan C8) and
  then return `FREEZE_FRAME_INCOMPLETE` from the engine. That is a result, not a crash, but a user meets it after Run.
- The G1 census covers the 314 v7 corpus rows only; the oil-case fixtures run through `apps/wired/tests` (36 passed).
