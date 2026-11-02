# P1 — static_sweep (round P, instrument pipeline)

- target: six static analysers over the production scope (pyright, bandit, vulture, deptry, import-linter, semgrep)
- git sha: `6f73135` (branch from `origin/audit-r1`)
- date: 2026-10-26
- time spent: about 35 min. All six analysers ran (semgrep only in part, see §Analyser status). Nothing was left unrun for lack of time.
- instrument: `audit/scratch/P1/sweep.py` → `audit/scratch/P1/sweep.json`. Labels: `adjudication.json`. Probes: `probes/test_p1_probes.py`. Contracts: `importlinter.ini`. Rules: `semgrep_rules.yml`. Controls: `controls/`.
- repro: `bash audit/tools/setup.sh && source .venv-audit/bin/activate && uv pip install bandit vulture deptry import-linter semgrep && npm i -g pyright && python audit/scratch/P1/sweep.py`

## Setup checks
- **Baseline:** `bash audit/tools/baseline.sh` gives the same pytest counts, erosion and isolation lines as `audit/reports/baseline_20261017.txt` for all 8 packages (comlab 522 passed / 4 skipped / 2 errors … apps/wired 11 passed; isolation 4). Only the git line and the timings differ.
- **F-C1-5 masking:** no P1 probe calls `diagnose()`, so no probe needs `labs/comlab` on `sys.path`. import-linter and the sweep put `labs/comlab` on `PYTHONPATH` so that `registry` resolves.

## Scope rulings
| path | ruling | reason |
|---|---|---|
| `labs/<lab>/<lab>/` ×7 | in, production | prompt |
| `labs/comlab/registry/` | in, production | `fault_atlas_router.py:1953` imports it on the default REG-V2 path |
| `apps/ui/{app,ui_payload,_sample_app_reference}.py` | in, production | prompt (`_sample_app_reference.py` is in the folder; it is imported by nothing) |
| `apps/wired/{wired,v7,fl_tasks,trace}/` | in, production | prompt names `apps/wired`; only `wired/` is packaged (`include = ["wired*"]`) |
| root `app.py` | in | it is the Render entry shim that runs `apps/ui/app.py` |
| `labs/vinlab/tools/` | in, tier `offline` | prompt: offline builders, lower priority |
| `apps/vault/` | **out** | It has no README (`ls apps/vault` shows `VAULT_LIVE_*.md`, `audit/`, `eval/`, `vault_live_tasks/`). `find apps/vault -name '*.py'` finds 0 files, so no Python analyser has anything to run on. |
| `*/tests/*`, `apps/wired/{_jaeger,harness}` | out | test and infrastructure code; `harness/` and `_jaeger/` hold no `.py` files in scope |

Population: **121 `.py` files** (23,821 LOC per bandit).

## Findings

### F-P1-1 — DNALab declares no dependencies but imports VINLab and SymptomLab at import time
severity: MEDIUM
kind: contract
anchor: `labs/dnalab/pyproject.toml` `[project]` has no `dependencies`; `labs/dnalab/dnalab/assembly.py:7-9`: "from symptomlab import resolve as _resolve_symptom" / "from vinlab import decode as _decode_vin"; `models.py:15-16`
claim violated: `labs/dnalab/docs/ADR_DNALab.md:15` ADR-0002 sanctions `dnalab → vinlab + symptomlab`. A sanctioned dependency still has to be declared, and the package's manifest does not declare it. Today only `apps/wired/pyproject.toml` (which lists `symptomlab` without importing it; deptry reports it DEP002) and the root `requirements.txt` install these two labs.
repro: `python -m pytest -q audit/scratch/P1/probes/test_p1_probes.py::test_dnalab_manifest_omits_vinlab_symptomlab`
probe: the test makes a fresh uv venv, runs `uv pip install <copy of labs/dnalab>`, then `python -c "import dnalab"`
observed: the install succeeds, then the import fails with `ModuleNotFoundError: No module named 'symptomlab'`
expected: installing `dnalab` gives an importable package (it declares `vinlab` and `symptomlab`)
sweep records: 5 (`deptry` DEP003 on `dnalab/assembly.py:7,8,9` and `models.py:15,16`)
user impact: none proven. The Render build installs every lab editable.

### F-P1-3 — The UI's Mode $06 dictionary path points under `apps/`, so every monitor's component caption reads "UNKNOWN"
severity: MEDIUM. The HIGH definition ("a wrong data value can reach a user") fits the wording, but this is a helper caption on the input form with no effect on the verdict, so I rate it MEDIUM rather than inflate it.
kind: correctness
anchor: `apps/ui/app.py:133`: `DICT_PATH = Path(__file__).parent.parent / "dtclab" / "dtclab" / "config" / "mode_06_hex_dictionary.json"`. The guard `if DICT_PATH.exists():` and the `except Exception: pass` at `:134-138` hide the miss.
claim violated: `apps/ui/app.py:131`: "# Load Mode $06 dictionary for live component lookup", and `:673-680` "Component name lookup" → `st.caption(f"Component: {mid_name}")`
repro: `python -m pytest -q audit/scratch/P1/probes/test_p1_probes.py::test_ui_mode06_dict_path_never_exists`
probe: evaluates the `DICT_PATH` expression from the AST with `__file__ = apps/ui/app.py`
observed: the path resolves to `apps/dtclab/dtclab/config/mode_06_hex_dictionary.json`, which does not exist. `MODE06_DICT` stays `{}`, so `MID_01_TID_..` shows "Component: UNKNOWN". The real file `labs/dtclab/dtclab/config/mode_06_hex_dictionary.json` maps `01` to "O2 Sensor Response B1S1".
expected: the caption names the monitored component, read from the DTCLab dictionary
sweep record: `semgrep` `p1-except-swallow` at `apps/ui/app.py:135`

### F-P1-2 — COMLab's tracing fallback tells the operator to install a `[tracing]` extra that does not exist; opentelemetry is declared nowhere
severity: LOW
kind: doc-drift
anchor: `labs/comlab/comlab/observability/_tracer.py:118`: `'pip install -e ".[tracing]" --break-system-packages. '`. The lazy imports are at `:107-113` and `:177`.
claim violated: `labs/comlab/pyproject.toml` `[project.optional-dependencies]` contains only `dev`
repro: `python -m pytest -q audit/scratch/P1/probes/test_p1_probes.py::test_comlab_tracing_extra_missing`
probe: `uv pip install "<copy of labs/comlab>[tracing]"` into a fresh venv, then `import opentelemetry.sdk`
observed: uv warns "comlab … does not have an extra named `tracing`", and the import fails with `No module named 'opentelemetry'`
expected: the documented command installs the OTel SDK and the OTLP exporter
sweep records: 6 (`deptry` DEP003 `opentelemetry` in `_tracer.py`). Related to R0-4, which is the same gap in `apps/wired`; this one is a different manifest and a different command.

### F-P1-4 — A VINLab offline builder splices the OPSI engine code into SQL without escaping
severity: LOW (offline builder; the OPSI CSVs are outside the repo, so I could not check whether any real code contains a quote)
kind: robustness
anchor: `labs/vinlab/tools/tecdoc_ktype_bridge.py:262`: `f"UPPER(REPLACE('{engine_code_hint}', ' ', ''))\n"`. The hint comes from `engine_code.upper()` at `:169` (OPSI `Nio_vozila_*.csv`).
claim violated: the other TecDoc builders bind their values (`tecdoc_cylinder_enricher.py:224` `cur.execute(sql, tuple(ktype_ids))`); `_get_cylinder_count` in the same file binds `%s`
repro: `python -m pytest -q audit/scratch/P1/probes/test_p1_probes.py::test_ktype_bridge_engine_code_unescaped`
probe: stubs `mysql.connector`, then calls `_build_layer_query("VW", 1600, 75, hint)`
observed: hint `AB'C` gives `REPLACE('AB'C', ' ', '')`, which sqlite3 rejects with OperationalError. Hint `X') OR ('1'='1` rewrites the WHERE clause.
expected: the hint is passed as a bound parameter
sweep record: `bandit` B608 at `tecdoc_ktype_bridge.py:237`

### Already listed (dup-of)
| sweep records | tool / rule | dup-of | note |
|---|---|---|---|
| 6 | deptry DEP001 `registry` (`fault_atlas_router.py:1953`, `registry/__init__.py:13,19`, `integration_shim.py:83,94`, `shim/__init__.py:8`) | F-C1-5 / F-C4-1 | `registry` is in no manifest (`include = ["comlab*"]`); nothing new |
| 16 + 3 | deptry DEP003 / pyright reportMissingImports `opentelemetry*` in `apps/wired/{trace,v7}` | R0-4 | no manifest installs opentelemetry; the instrument adds the unguarded runtime imports in `trace/run_traced_case.py:21-25`, `trace/sanity_emit_span.py:13-17` and `v7/run_suite.py:40-45`, which are the same root cause |
| 0 | — | F-C5-12 | `apps/ui/app.py` imports `vinlab` directly; no P1 analyser flags this, because apps may import labs |

## Analyser status
| analyser | status | population | detail |
|---|---|---|---|
| pyright 1.1.414 (npm) | RAN | 121/121 files analysed | basic mode **plus** `reportPossiblyUnboundVariable=warning` (basic turns it off in 1.1.414, and the prompt asks for unbound errors; the positive control proves the override works). 11 files have unresolved imports (opentelemetry exporter, mysql, plotly/`engine`). Pyright typed those names as Unknown, which is a blind spot. |
| bandit 1.9.4 | RAN | 121 files, 23,821 LOC, 0 errors, 0 nosec | `-ll` (MEDIUM+); 0 HIGH, 12 MEDIUM |
| vulture 2.16 | RAN | 121 files | `--min-confidence 60`; 0 unparsed lines |
| deptry 0.25.1 | RAN | 12 roots, each checked against its own manifest (`DEPTRY_RUNS` in sweep.py) | `labs/vinlab/tools` checked against `requirements.txt`; `apps/ui` against the root `requirements.txt`; registry against comlab's pyproject. Root `app.py` not run (stdlib only, no manifest of its own). |
| import-linter 2.15 | RAN | 9 root packages, 122 modules, 208 dependencies | 9 contracts, all KEPT. `apps/ui` holds modules, not a package, so it is outside the graph (apps may import labs, so no contract needs it). |
| semgrep 1.182.1 | **INCOMPLETE** | 121/121 files scanned, 0 parse errors | **p/python ABSENT**: the session egress proxy refused `semgrep.dev:443` (`connect_rejected` ×4). Only the 6 local rules in `semgrep_rules.yml` ran. |

## Counts (mechanism · unit · population · blind spot)
Unit: one sweep record = one analyser diagnostic, with stable id `sha1(tool|rule|path|enclosing symbol|stripped line text|occurrence)`. Population: the 121 files above. 451 records in total.

| tool | CONFIRMED | DUPLICATE | FALSE-POSITIVE | UNDECIDED | UNADJUDICATED | blind spot |
|---|---|---|---|---|---|---|
| pyright | 0 | 3 | 20 | 3 | 0 | Unknown-typed names (`dict[str, Any]` payloads, unresolved imports) hide attribute and optional errors |
| bandit | 1 | 0 | 11 | 0 | 0 | MEDIUM+ only; LOW (40 records) not collected |
| vulture | 0 | 0 | 11 | 0 | **290** | text-level use: pydantic fields and enum members read by serialisation look unused (253 of the 290 are "unused variable") |
| deptry | 11 | 22 | 51 | 1 | 0 | a declared distribution that is not installed cannot be mapped to its import name (`mysql-connector-python` → `mysql`) |
| import-linter | 0 | 0 | 0 | 0 | 0 | `importlib` and string imports; tests outside packages |
| semgrep | 1 | 0 | 15 | 2 | **9** | 6 local rules only; p/python ABSENT |
| **total** | **13** | **25** | **108** | **6** | **299** | |

**UNADJUDICATED: 299 records.** 290 are vulture 60 % records (178 of them in verdict-producing code: comlab, gaslab, `ui_payload.py`, `composition.py`; by kind: 253 unused variable, 19 unused method, 13 unused function, 4 unused attribute, 1 unused property). The other 9 are semgrep `p1-syspath-mutation` hits in tooling (`apps/wired/{v7,fl_tasks}`, `wired/run_case.py:31`, `labs/vinlab/tools`). None of them is in the four priority classes the prompt orders adjudicated.

Priority-class coverage: (1) pyright optional, unbound or attribute errors in verdict-producing code: **0 records exist**. All 5 records of those rules (3 possibly-unbound in `v7/run_suite.py`, 2 optional-iterable in `labs/vinlab/tools/build_vds_map.py`) sit in tooling, and all 5 are adjudicated. (2) bandit MEDIUM+: 12 of 12 adjudicated. (3) vulture 100 %: 4 of 4 adjudicated (all FALSE-POSITIVE: `_tracer.py` no-op signatures "# noqa: ARG002"; `brettschneider.py:22` "hcv … Reserved for future use; currently unused"; `build_vref_db.py:664` "if False  # YAML doesn't distinguish", and the YAML has no supercharger key). (4) deptry missing or undeclared (DEP001 27 + DEP003 40): 67 of 67 adjudicated. DEP002 (18) was also adjudicated, all FALSE-POSITIVE.

## Controls and determinism
| instrument | planted positive (must flag) | clean (must not flag) |
|---|---|---|
| pyright | `controls/positive/pos_pyright.py` → reportOptionalMemberAccess, reportPossiblyUnboundVariable, reportAttributeAccessIssue: **flagged** | `clean_pyright.py` → **0** |
| bandit | `pos_bandit.py` → B602, B506: **flagged** | `clean_bandit.py` → **0** |
| vulture | `pos_vulture.py` → unused argument and unreachable code (100 %): **flagged** | `clean_vulture.py` → **0** |
| deptry | `controls/deptry_pos` → DEP001 `no_such_dist_xyz`, DEP003 `yaml`: **flagged** | `deptry_clean` → **0** |
| semgrep | `pos_semgrep.py` → all 6 rules: **flagged** | `clean_semgrep.py` → **0** |
| import-linter | one violation planted per contract in a private copy of the 9 packages: **9/9 contracts BROKEN as planted** (e.g. `gaslab → comlab` breaks `emitters-not-comlab` and `iso-gaslab`; contracts are transitive, so `vinlab → comlab` also breaks `iso-dnalab`) | the unmodified copy keeps 9/9 contracts; the planted **sanctioned** `dnalab → vinlab` keeps 9/9 |

Before I added the override, the first sweep showed that pyright basic mode does **not** report possibly-unbound variables. The positive control caught this.

Determinism: `python audit/scratch/P1/sweep.py` was run twice (once to `sweep.json`, once to a scratchpad copy), and `cmp` found the two files **identical** (sha256 `eca2b248…c7efd4`, 7,407 lines).

## Isolation reconciliation (`audit/tools/isolation.py` vs import-linter)
- `isolation.py`: 4 violations, all in `labs/comlab/tests/unit/` (R0-2). **0 are in the production scope**. They fall outside import-linter's population (tests outside packages).
- import-linter: 0 contracts broken in production.
- A separate AST scan of the 121 production files (`own_isolation_scan`, the same rule, plus `ui_payload`/`v7`/`fl_tasks` as foreign targets): 0 cross-lab or lab→app imports.
- All three agree: `agree: true` in sweep.json.
- Coverage differences: `isolation.py` does not treat `registry` as comlab-owned and does not scan `apps/`. import-linter does not see `apps/ui` or tests.

## Approaches that found nothing
- pyright (basic + possibly-unbound) over `labs/comlab`, `labs/gaslab`, `apps/ui/ui_payload.py`, `apps/wired/wired/composition.py`: 0 optional, unbound or attribute errors. Blind spot: these modules move most data as `dict[str, Any]`, which pyright does not check. This silence is not evidence that the code is clean.
- import-linter, 9 contracts written from AGENTS rule 5 + ADR-0002 + "emitter labs do not import comlab": all KEPT, and each contract is proven able to fail (above).
- bandit MEDIUM+ over all production labs: 0 records outside `labs/vinlab/tools` and `apps/wired/trace` (offline and tooling only).
- deptry over dtclab, gaslab, obdlab, symptomlab and vinlab: 0 issues each.
- semgrep `p1-yaml-unsafe-load` and `p1-mutable-default`: 0 hits in production.
- Not examined: the 290 vulture 60 % records; the semgrep registry rules (ABSENT); test code; `apps/vault` (no Python).

findings: H=0 M=2 L=2
