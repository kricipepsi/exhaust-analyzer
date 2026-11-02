# P3 — test reachability (round P, instrument pipeline)

- target: P3 `reachability` — which passing tests exercise production behaviour, and which production code no test reaches
- git sha: `6f73135` (origin/audit-r1), session branch `claude/awesome-cori-1my5nl`
- date: 2026-10-26 · time spent: about 105 min (over the 90 min budget by about 15 min; see §5 for what did not run)
- instrument: `audit/scratch/P3/` — `run_suites.sh` (coverage runs), `p3_nodeids.py` (node-ID recorder),
  `reachability.py` (classifier and census), `controls/` (planted controls), two `test_probe_*.py` probes.
  Output `audit/scratch/P3/reachability.json` (per-test class and per-function coverage, for P4).

## 0. Setup, baseline and scope rulings

**Baseline.** `bash audit/tools/baseline.sh` on `6f73135` gives the same counts as
`audit/reports/baseline_20261017.txt` for all 8 packages (comlab `522 passed, 4 skipped, 2 errors`,
dnalab 27, dtclab 590, gaslab `208 passed, 2 skipped, 4 deselected`, obdlab `388/2s`, symptomlab 63,
vinlab `203/8s`, wired 11). Baseline differences:
- `apps/ui` is not in the baseline. Run alone it gives `2 failed, 6 passed` (`ModuleNotFoundError: registry`,
  which is F-C1-5). With `labs/comlab` on `PYTHONPATH`, as the prompt requires, it gives `8 passed`. All P3 runs
  use that path.
- **`labs/comlab/registry/tests/` is not in any baseline run.** `labs/comlab/pyproject.toml:40` sets
  `testpaths = ["tests"]`, so the comlab run never collects it. Run explicitly, it gives
  `5 failed, 489 passed` (see F-P3-1). P3 measures it as a tenth suite, `registry`.

**Scope rulings.**
- Production code means `labs/<lab>/<pkg>/` for the seven labs, plus `labs/comlab/registry/`, plus `apps/wired/wired/`
  and `apps/ui/{app.py,ui_payload.py}`. `labs/comlab/registry/` counts because the production verdict path imports it
  (`fault_atlas_router.py:1953`). `labs/comlab/registry/tools/` holds offline builders and is flagged `offline`.
- `labs/vinlab/tools` is not measured (offline, lower priority). `apps/wired/{v7,fl_tasks,harness,trace}` are scoring
  and harness tools: no production module imports them (`grep -rhoE "^(from|import) (v7|fl_tasks|harness|trace)\b"
  apps/wired/wired apps/ui/*.py` returns 0 lines), so they are not measured.
- `apps/vault` has no root README. Its three sub-READMEs (`audit/reports`, `eval/runs`,
  `vault_live_tasks/progress_notes`) describe output folders for the vault-framing pack. The tree has 69 files and all
  are `.md`, with no Python. **Ruling: excluded.** It contains no production code and no tests.
- Root `app.py` is a 15-line `runpy` shim into `apps/ui/app.py`. It is not measured separately.

## 1. Instrument: mechanism, units, population, blind spots, controls

**Coverage run** (`run_suites.sh`). Each of the 10 suites runs `pytest --cov=<all production dirs + all test dirs>
--cov-branch --cov-context=test`, with the `p3_nodeids` plugin recording node ID → outcome in the same process.
Every run measures every production directory, so cross-package reach is visible.
*Instrument defect found and fixed:* on Python 3.14, coverage 7.17 defaults to the `sysmon` core, which turns a line
off after its first hit. The first run therefore recorded only 151 contexts for 522 comlab tests, and per-test reach
would have been wrong. All runs since then use `COVERAGE_CORE=ctrace`. That run gives 434 comlab contexts; the other
88 comlab tests execute no measured line.

**Test classes** (`reachability.py`). Unit: one passing node ID (a parametrized case counts as one test).
Population: the 2,509 passing tests of the 10 suites, of which 2,020 are in the 9 baseline suites.
- Mechanism, coverage half: own-package production lines executed in the test's `run`, `setup` and `teardown`
  contexts. The comlab suite owns `comlab/` and `registry/`.
- Mechanism, data-flow half: an intraprocedural AST taint pass. Sources are calls to names imported from production
  modules, calls to local or helper-module functions and fixtures whose return is tainted (summaries computed
  recursively, factory fixtures included), and methods called on tainted objects. Taint propagates through
  assignment, unpacking, loops, `with … as`, container mutation (`append`, `update`, …), and control dependence
  (if/while tests and `except` handlers). Each assertion is classified VALUE (a production call value reaches it
  outside a shape wrapper), VALUE_CTOR (only a production constructor), SHAPE (only under `isinstance`, `type`,
  `hasattr`, `len`, `.keys()`, `is None` or `"k" in x`), CONST (a production constant), DOUBLE (a Mock or
  `.assert_called*`) or NONE. Covered forms: `assert`, `self.assert*`, `pytest.raises` (call and `with`) and `assert*`
  helper calls. **Only assertions whose line executed in that test's run context count**, because test files are
  measured too.
- Rules:
  - behaviour: own lines executed and at least one VALUE or VALUE_CTOR assertion.
  - interface: SHAPE assertions only. This also covers a shape assertion on a production symbol with 0 own lines,
    such as an importability test.
  - placeholder: 0 own lines, or executed assertions that are only CONST, DOUBLE or NONE, or no assertion line ran.
  - UNDECIDED: own lines executed but no assertion found; or a value assertion on a production call that ran
    **no** Python line (pydantic, enum or dataclass code that line coverage cannot see); or the test function was
    not found in the AST.
- Blind spots:
  - Taint is intraprocedural for test bodies, with helper and fixture summaries only to depth 3. `autouse` and
    `usefixtures` fixtures are not traced.
  - A side channel (spans, logs, captured stdout) is not a returned value, so tests asserting on emitted spans count
    as placeholder.
  - Truthiness `assert x.attr` counts as VALUE.
  - `"k" in CONST` counts as SHAPE, even when both sides are constants.
  - Imports that resolve through a test-time `sys.path` hack (for example `tools.build_corpus`) are not recognised
    as production.
  - Expression-level branches (`a if c else b`, `or`) are invisible to line and arc coverage. `_run_obdlab` has
    radon CC 64 but only 2 branch arcs.

**Function census.** Unit: one `def` (functions, methods and nested defs), enumerated by AST over the production
files (65 files, 361 functions). Coverage comes from the union of the 10 data files. *Reached* means at least one body
statement executed in some test's context; a function whose body ran only at import is `import_only` (0 such
functions). CC is radon `cc_visit`. Branch census population ("verdict-producing" functions): every function in
`fault_atlas_router.py`, `integration_shim.py`, `lab_pipeline_aggregator.py`, gaslab `rule_engine.py` and
`resolution.py`, dtclab `ranking.py` and wired `composition.py`, plus the 7 named functions: 125 functions with
1,254 branch arcs. Blind spot: verdict code outside that module list (obdlab normalisers, for example) is not in the
branch census; their function-level reach is in the JSON.

**Determinism.** `reachability.py` twice on the same data gives `cmp` identical. Two complete independent coverage
runs (`p3run4`, `p3run5`) analysed separately also give `cmp` identical (`CROSS-RUN-IDENTICAL`).

**Planted controls** (`controls/run_controls.sh` → `CONTROLS ALL PASS`, 11/11). These are a fake production package
`p3ctl` and seven tests, run through the same coverage and classifier path.
- Positive (must flag):
  - `test_planted_placeholder_constant` → placeholder ✔
  - `…_double` → placeholder ✔
  - `…_early_return` (the assert never runs) → placeholder ✔
  - `never_called` listed unreached ✔
  - the untaken `x < 0` branch listed ✔
- Clean (must not flag):
  - `test_clean_behaviour_value` → behaviour ✔
  - `test_clean_behaviour_control_dependent` → behaviour ✔
  - `verdict` reached ✔
  - the taken `x > 10` branch not listed ✔
  - interface controls → interface ✔ (2/2)

**Hand checks, three tests per class.** These were read in the source and the class assigned by hand.
- behaviour 3/3 agree:
  - `gaslab::…test_each_hard_signature_appears[FLAT_CAMSHAFT-None]`
  - `dtclab::…test_cold_start_priority_over_idle`
  - `wired::…test_diagnose_returns_verdict` (agrees, but weak: it asserts only that `fault_code` is truthy)
- interface 2/3:
  - `vinlab::…test_schema_air_metering_architecture_shape` ✔
  - `comlab::…TestErrAbort001::test_sample_borderline_accepted` (`directive is not None`) ✔
  - `obdlab::…test_ckp_cmp_fault_dtcs_bounds` ✘ — a membership test of constants in a production constant; it should
    be placeholder (blind spot above).
- placeholder 1/3:
  - `obdlab::…test_bound_row_matches_wiki[…]` ✔ (it reads a JSON data file and makes no production call)
  - `comlab::…test_v2_route_emits_rank_span_with_expected_rule_tags` ✘ — it asserts on spans the router emitted,
    which is behaviour through a side channel.
  - `registry::…TestCaseMeta::test_invalid_source` ✘ — `CaseMeta` is imported through a path hack, so it is
    unrecognised; it should be UNDECIDED (declarative).
- UNDECIDED 2/3:
  - `comlab::…test_current_schema_version_accepted` ✔ (smoke: no assertion)
  - `obdlab::…test_model_validate_confidence_none` ✔ (pydantic only, no Python line)
  - `dtclab::…test_print_combinatorial_coverage` ✘ — it asserts `_TOTAL_CASES > 0`, a module constant; it should be
    placeholder.
- Total: 8 of 12 agree. Read the class counts below as ±(this error rate): the placeholder count is overstated where
  tests assert on side channels, and understated where constants are tested inside `in`.

## 2. Results

### 2.1 Test classes (passing tests; unit = node ID)

| suite | behaviour | interface | placeholder | UNDECIDED | total |
|---|---|---|---|---|---|
| comlab | 372 | 34 | 75 | 41 | 522 |
| dnalab | 22 | 4 | 1 | 0 | 27 |
| dtclab | 470 | 16 | 92 | 12 | 590 |
| gaslab | 143 | 23 | 20 | 22 | 208 |
| obdlab | 290 | 29 | 39 | 30 | 388 |
| symptomlab | 50 | 5 | 4 | 4 | 63 |
| vinlab | 171 | 12 | 14 | 6 | 203 |
| wired | 10 | 0 | 1 | 0 | 11 |
| ui | 5 | 1 | 2 | 0 | 8 |
| **9 baseline suites** | **1,533** | **124** | **248** | **115** | **2,020** |
| registry (orphan) | 317 | 91 | 70 | 11 | 489 |
| **all 10** | **1,850** | **215** | **318** | **126** | **2,509** |

Why tests landed in each class (all 10 suites):

| class | reason | tests |
|---|---|---|
| behaviour | an assertion data-flows from a production call | 1,810 |
| behaviour | constructor only | 40 |
| placeholder | no own-package line executed | 276 |
| placeholder | no assertion line executed | 22 |
| placeholder | only NONE assertions | 19 |
| placeholder | only CONST assertions | 1 |
| interface | shape assertions with own lines executed | 167 |
| interface | shape assertion on a production symbol, no own line | 48 |
| UNDECIDED | declarative value (no Python line ran) | 117 |
| UNDECIDED | smoke test, no assertion | 9 |

The **UNDECIDED remainder is 126 tests (5.0 %)**. The census does not classify them further.

### 2.2 Production functions no test reaches

Population: 361 functions in 65 files, 24 of which are unreached. 6 of the 24 are the offline
`registry/tools/build_corpus.py` builders. The other 18, ranked by radon CC:

| CC | stmts | function | production caller? (`grep -rn --include=*.py`, tests excluded) |
|---|---|---|---|
| 5 | 10 | `apps/ui/app.py:244 _check_radio` (+ nested `_on_toggle`, CC 4) | Streamlit UI only (needs a running script) |
| 5 | 26 | `labs/comlab/comlab/observability/_tracer.py:92 _initialise_provider_once` | `_tracer.py:173` (OTel enabled only) |
| 4 | 6 | `apps/wired/wired/registry_guard.py:21 assert_registry_ready` (+ `_count_rules`) | **none** → F-P3-4 |
| 4 | 8 | `labs/comlab/comlab/analytics/power_loss_analytics.py:111 PowerLossAnalytics.derive_pre_cat_lambda` | none |
| 3 | 5 | `apps/wired/wired/composition.py:469 _derive_horizon` | only `apps/wired/fl_tasks/capture_upstream_evidence.py` (a tool) |
| 2 | 6 | `labs/comlab/comlab/core/lab_pipeline_aggregator.py:627 run_fallback_tree` | raises "not yet implemented (phase 3)"; dup-of F-C1-22 |
| 2 | 3 | `labs/comlab/registry/integration_shim.py:1345 route_case`, `:1366 render_ranked_rule` (module-level wrappers) | re-exported in `registry/__init__.py` only |
| 1 | 2 | `lab_pipeline_aggregator.py:646 sanitize_and_aggregate` | none |
| 1 | 1–2 | `_tracer._NoOpSpan.{set_status,record_exception,end}`, symptomlab `EnvironmentalConditions.to_json`, `SymptomDNA.to_json`, vinlab `VinDNA.to_json`, `tecdoc_query.open_vref_readonly` | none / exported only |

### 2.3 Named functions and untaken branches (union of all 10 suites)

| function | CC | stmts hit/total | tests reaching | suites | branch arcs untaken / total |
|---|---|---|---|---|---|
| `fault_atlas_router.py:922 FaultAtlasRouter.execute_triage_loop` | 174 | 367/405 | 114 | comlab | 38/260 |
| `fault_atlas_router.py:1937 FaultAtlasRouter.route` | 70 | 182/188 | 102 | comlab, ui, wired | 7/80 |
| `integration_shim.py:789 _score_rule` | 55 | **20/95** | 89 | comlab, registry, ui, wired | **60/68** |
| `gaslab/resolution.py:258 apply_differentiators` | 133 | 106/109 | 91 | gaslab, ui, wired | 6/80 |
| `gaslab/rule_engine.py:243 _definitive_match` | 50 | 46/51 | 86 | gaslab, ui, wired | 5/40 |
| `apps/ui/ui_payload.py:822 build_diagnose_payload` | 115 | 143/190 | 5 | ui | 54/152 |
| `apps/wired/wired/composition.py:285 _run_obdlab` | 64 | 5/6 | 1 | wired | 1/2 (CC is in expressions, invisible to arcs) |

Across the verdict population, 272 of 1,254 branch arcs are untaken. Ranked by untaken arcs, the next functions are
all in the registry shim's C-state layer:
- `_lean_root_cause_state` (C5): 13/14
- `_c4_signal_state` (C4): 7/8
- `_health_confirmation_state` (C9): 5/6
- `_sensor_dynamics_state` (C6): 5/6

Every arc is listed in `reachability.json → verdict_branches`.

## 3. Findings

### F-P3-1 — 494 registry rule tests are outside every suite run; 5 of them fail
severity: MEDIUM
kind: test-gap
anchor: `labs/comlab/pyproject.toml:40` — `testpaths = ["tests"]`
claim violated: `audit/reports/baseline_20261017.txt` reports `labs/comlab 522 passed`, and `AGENTS.md` ("Done" = …
`pytest -x -q`) treats the lab suite as the gate. Neither collects `labs/comlab/registry/tests/` (28 files, 494 tests:
the per-family REG-V2 rule tests, including `test_integration_shim.py` and `test_no_fault_rules.py`).
repro: `cd labs/comlab && python -m pytest -q -p no:cacheprovider registry/tests`
probe: `audit/scratch/P3/run_suites.sh` (suite `registry`); `nodeids_registry.json`
observed: `5 failed, 489 passed`. The five failures are `test_build_corpus.py` tests: `FileNotFoundError` on
`apps/wired/_jaeger/runs/20260527-044325/FAILURE_BLUEPRINT.md` and `apps/wired/harness/data/cases_petrol_master_v6.csv`.
The suite contributes 317 behaviour tests, and it is the only suite that reaches 8 functions
(`RegistryV2Router.route_case`, `.render_ranked_rule`, `.rules`, and 5 offline builders).
expected: the registry rule suite runs in the lab gate (or a declared one), and its failures are visible.

### F-P3-2 — The registry's C2–C9 score-override cascade has no test; the C3 branch makes a "Fuel trim saturated" verdict at 0.90 from one KOEO MAP-baro value
severity: MEDIUM
kind: test-gap
anchor: `labs/comlab/registry/integration_shim.py:811-821` — `if c3_state == ControlPlausibilityState.CONTROL_REFERENCE_FAULT: if rule.rule_id in ["EF-001", "EF-002", "EF-003"]: … score_to_boost = raw_score if raw_score is not None else rule.base_weight; return min(score_to_boost + 0.10, 1.0)`
claims:
- `v3/v3_tasks/T-V3-P4-C3B_c3_signal_commit.md:32-33`: "any → `CONTROL_REFERENCE_FAULT` … On the state: boost
  EF-001/EF-002/EF-003 (+0.10 DEFINITIVE), prune SF-001/SF-002."
- `apps/wired/ship_tasks/reports/SHIP_UI_CONTRACT_2026-07-07.md:17`: "All 36 are real `diagnose()` inputs with
  named registry-shim consumer states". The UI exposes them (`apps/ui/app.py:729` `adv_koeo_map_baro_delta_kpa`).
repro: `cd labs/comlab && python -m pytest -q -p no:cacheprovider ../../audit/scratch/P3/test_probe_score_rule_c3.py -s`
probe: `audit/scratch/P3/test_probe_score_rule_c3.py`
observed:
- Coverage over all 10 suites (2,509 tests, 89 of which reach `_score_rule`): 60 of 68 branch arcs and 75 of 95
  statements in `_score_rule` are never taken. Every C3, C4, C5, C6, C9 and C2 override branch is dead to the
  suites, and the state functions are nearly so (`_lean_root_cause_state` 13/14, `_c4_signal_state` 7/8,
  `_health_confirmation_state` 5/6, `_sensor_dynamics_state` 5/6 arcs untaken). The only verification of these
  branches was the v7 corpus score (`v3/V3_PROGRESS.md:59-61`: C3 dry-run at top3_family 212/294, commit at 228/294).
- Driving the C3 branch with `koeo_map_baro_delta_kpa = 6.0`:
  - SF-001 and SF-002 → `None` (pruned, as the spec says).
  - EF-001 `quiet=None c3=0.9`, EF-002 `None→0.9`, EF-003 `None→0.85`: rules that do not fire on their own
    conditions become 0.85–0.90.
  - `RegistryV2Router().route_case({"obd_live_data": {"koeo_map_baro_delta_kpa": 6.0}})` → verdict
    `fault_code EF-001`, "Fuel trim saturated — positive (max enrichment)", `confidence 0.9`,
    `degradation_mode FULL_FUSION`, `HIGH_ASSURANCE`. No trim, gas or DTC data is present.
expected: each documented override branch has a test that drives it. For the architect: does "boost" allow a
non-firing rule to win from its `base_weight` (the code does this for every C-override: lines 814, 839, 850, 857,
864, 874, 886, and the C2 branches at 909, 915)? If not, the observed EF-001 verdict is a HIGH correctness defect.

### F-P3-3 — `test_csv_cases_dtclab` passes 64 of its 194 rows without running any DTCLab code
severity: MEDIUM
kind: test-gap
anchor: `labs/dtclab/tests/test_cases.py:120-121` — `if not dtc_codes and ff is None: return`
claim violated: `labs/dtclab/tests/test_cases.py:1-6` — "All 194 rows … it asserts no crash + schema-valid payload".
`:111` — "Characterization net — no crash + schema-valid payload per CSV row."
repro: `bash audit/scratch/P3/run_suites.sh <out> && python audit/scratch/P3/reachability.py <out> r.json`, then
select `dtclab::tests/test_cases.py` with `own_lines == 0`
probe: `reachability.json` (`tests["dtclab::tests/test_cases.py::test_csv_cases_dtclab[*_noff_nodtc]"]`)
observed: 64 of 194 parametrized cases (every `*_noff_nodtc` row, e.g. `CSV-001_noff_nodtc`) execute 0 DTCLab
lines, and none of their assertion lines run (class placeholder). The ledger counts them as 64 passing tests.
expected: those rows exercise the "no DTC, no freeze frame" input (DTCLab's empty-input contract), or they are
skipped with a reason, not passed.

### F-P3-4 — The wired REG-V2 activation guard has no caller and no test
severity: LOW
kind: test-gap
anchor: `apps/wired/wired/registry_guard.py:21` — `def assert_registry_ready(rules_dir: Path | None = None) -> None:`
claim violated: `apps/wired/WIRED_PROGRESS.md:58` — "`registry_guard.py` must expect 73 rules (not 68) or harness
raises `RegistryActivationError`". The module docstring says "this guard keeps the wired package pinned to that count".
repro: `python -m pytest -q -p no:cacheprovider audit/scratch/P3/test_probe_registry_guard.py -s`
probe: `audit/scratch/P3/test_probe_registry_guard.py`
observed: `shipped rules=73 expected=73`, so `assert_registry_ready: passes`. `git grep assert_registry_ready -- '*.py'`
finds no caller outside its own definition and `__all__`, and no test reaches it. Rule-count drift would raise in
nothing.
expected: the guard runs on the wired path (or in a test), or the claim is withdrawn.

### Already listed (not new)

| observation in P3 | dup-of |
|---|---|
| `apps/ui` suite fails 2 without `labs/comlab` on `PYTHONPATH` | F-C1-5 / F-C4-1 |
| comlab 2 collection errors (`fl_tasks`, `v7`) | R0-2 |
| `run_fallback_tree` unreached ("not yet implemented (phase 3)"); aggregator tests skipped | F-C1-22 |
| aggregator Phase-5 evidence gates unreachable from production | F-C1-8 |
| C-column fields with no reader on the production path (13 OBD + 3 GAS) | F-C4-5 (P3 adds that the *shim's* C-state consumers that do read them have no test: F-P3-2) |
| BDD scenarios with no test | F-D2-16, F-D2-26 |
| KG⇆registry consistency gate missing | F-D2-5 |
| `test_tracing` needs opentelemetry | R0-4 (installed by `setup.sh`; passes here) |

## 4. Approaches that found nothing

- Named-function reach. `execute_triage_loop` (367/405 statements, 114 tests), `route` (182/188),
  `apply_differentiators` (106/109) and `_definitive_match` (46/51) are well reached. Their untaken arcs (38, 7, 6
  and 5) are in `reachability.json`. I did not map each one to a wiki rule, so no finding is raised on them. This is
  not a clean bill: the arcs are unadjudicated.
- `build_diagnose_payload`: 54/152 arcs untaken by the 5 UI tests. The UI findings F-C5-* already cover its defects.
  I wrote no new probe.
- Per-class name-claim scan: beyond F-P3-3 and the hand checks, I did not systematically compare test names with
  their class. The 215 interface and 318 placeholder tests are listed in the JSON for P4.

## 5. What ran and what did not

- Ran: baseline comparison, 10 suites under ctrace coverage with per-test contexts (two full runs), the classifier
  and census, planted controls (11/11), 12 hand checks, and 2 probes (`test_probe_score_rule_c3.py` 3 passed;
  `test_probe_registry_guard.py` 2 passed).
- Not run:
  - gaslab `slow` tests (4 deselected by `addopts = "-m 'not slow'"`): ABSENT from the census.
  - vinlab `tools/` and the `registry/tools` failures' data: not examined.
  - Branch census outside the 7 verdict modules: function-level reach only.
  - The interprocedural limits (depth 3, no autouse fixtures) are unmeasured as an error rate beyond the 12 hand
    checks.

findings: H=0 M=3 L=1
