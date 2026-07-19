# PYSCN_EVAL_2026-06-29 — `pyscn` pre-wiring audit CLI evaluation

**Task:** `T-PYSCN-1`  
**Mode:** read-only audit; no source, graph, `Vault/`, hook, CI, or generated artifact changes.  
**Tool under test:** `uvx pyscn@latest`, observed as `pyscn 1.24.3` (`4419636`, built 2026-06-21, Go 1.25.5, linux/amd64).  
**Raw machine artifacts:** copied outside the repo as `/tmp/pyscn_<target>.json` where `analyze --json` produced JSON; run logs at `/tmp/pyscn_check_results.json`, `/tmp/pyscn_analyze_results.json`, `/tmp/pyscn_aggregate.json`.

## Verdict

**Wire in now as a non-blocking agent/code-audit tool for Python-bearing targets; do not add a blocking pre-commit or CI gate yet.** Current default `check --select deadcode,complexity,deps` fails 5 of 7 Python targets on existing complexity debt, while `labs/semantic` and `apps/wired` currently have no `*.py` files. Recommended T-PYSCN-2 wiring: agent/MCP command plus CI artifact/report first; promote to blocking CI only after the listed complexity baseline is either fixed or explicitly allowlisted.

Recommended command profile for T-PYSCN-2:

```bash
uvx pyscn@latest check --select deadcode,complexity,deps --max-complexity 25 --max-cycles 0 <python-target>
uvx pyscn@latest analyze --json <python-target>  # advisory metrics, including clones
```

- **Where:** agent/MCP server command + non-blocking CI report/artifact; not pre-commit yet.
- **Complexity threshold:** start advisory at default `>10`; candidate blocking threshold after cleanup/baseline is `--max-complexity 25`, because the current live tree has 31 production functions over 10 and 7 production functions over 25.
- **Cycles threshold:** `--max-cycles 0`; all analyzed Python targets currently report zero cycles.
- **Clones:** keep clones advisory from `analyze --json`; do **not** include clones in the blocking `check` gate. If clone checks are added later, split test-only clone groups from production/mixed groups and use `--skip-clones` for fast CI checks.
- **Target filter:** run only against targets with Python files until `labs/semantic` or `apps/wired` gains Python code.

## Orientation and scope checks

- Read `AGENTS.md`; applied rule 1 by querying existing `labs/<lab>/graph/v2_current/graph.json` files and did not rebuild or run `graphify`.
- Read `apps/wired/WIRING_PREP.md`; this evaluation is a pre-wiring gate and does not wire any hook/CI/config.
- Graph orientation query results: `gaslab`, `obdlab`, `dtclab`, `comlab`, `dnalab`, `vinlab`, and `symptomlab` each had a `v2_current` graph with 0 dangling edges; `semantic` has no `v2_current` graph. All queried graph files reported built commit prefix `f7544224`.
- `apps/wired` has no Python files in the current tree; `labs/semantic` also has no Python files in the current tree.

## Per-target metrics

`check` command: `uvx pyscn@latest check --select deadcode,complexity,deps <target>`  
`analyze` command: `uvx pyscn@latest analyze --json <target>` from `/tmp`, with JSON copied to `/tmp/pyscn_<target>.json` when emitted.

| Target | Python files analyzed | `check` exit | `analyze` exit | Status | Health | Grade | Functions >10 | Prod functions >10 | Dead code | Cycles | Clone groups | Clone pairs | Dup % |
|---|---:|---:|---:|---|---:|:---:|---:|---:|---:|---:|---:|---:|---:|
| `labs/gaslab` | 40 | 1 | 0 | ok | 59 | D | 4 | 3 | 0 | 0 | 22 | 157 | 30.0 |
| `labs/obdlab` | 46 | 1 | 0 | ok | 58 | D | 2 | 1 | 0 | 0 | 11 | 35 | 22.3 |
| `labs/dtclab` | 39 | 1 | 0 | ok | 62 | C | 1 | 1 | 0 | 0 | 8 | 14 | 17.0 |
| `labs/comlab` | 102 | 1 | 0 | ok | 46 | D | 8 | 7 | 0 | 0 | 68 | 747 | 30.0 |
| `labs/dnalab` | 11 | 0 | 0 | ok | 60 | C | 0 | 0 | 0 | 0 | 1 | 3 | 13.0 |
| `labs/vinlab` | 58 | 1 | 0 | ok | 60 | C | 21 | 19 | 0 | 0 | 17 | 41 | 15.1 |
| `labs/symptomlab` | 12 | 0 | 0 | ok | 67 | C | 0 | 0 | 0 | 0 | 2 | 5 | 16.2 |
| `labs/semantic` | 0 | 1 | 1 | no Python files | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| `apps/wired` | 0 | 1 | 1 | no Python files | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a |

## Parse failures and invalid inputs

- **Python parse failures:** none observed in emitted JSON errors for all analyzed Python-bearing targets.
- **Invalid-input targets:** `labs/semantic` and `apps/wired` returned exit 1 with `no Python files found in the specified paths`. This is a target-content mismatch, not a Python parse failure.

## Production-code findings

### Dead code

No dead-code findings were emitted for any Python-bearing target (`dead_code_count = 0`, `critical_dead_code = 0` everywhere JSON was produced).

### Dependency cycles

No dependency cycles were emitted for any Python-bearing target (`CyclicDependencies = 0`, `deps_modules_in_cycles = 0` everywhere JSON was produced).

### Cyclomatic complexity over default threshold (`>10`), production/tool code only

| Target | File:line | Symbol | Complexity | Cognitive | Risk |
|---|---|---|---:|---:|---|
| `comlab` | `labs/comlab/comlab/core/fault_atlas_router.py:917` | `FaultAtlasRouter.execute_triage_loop` | 144 | 785 | high |
| `gaslab` | `labs/gaslab/gaslab/resolution.py:258` | `apply_differentiators` | 53 | 143 | high |
| `vinlab` | `labs/vinlab/tools/tecdoc_cylinder_enricher.py:279` | `main` | 39 | 66 | high |
| `vinlab` | `labs/vinlab/tools/build_vref_db.py:386` | `_extract_tecdoc` | 38 | 79 | high |
| `vinlab` | `labs/vinlab/tools/tecdoc_cyl_from_attributes.py:192` | `main` | 37 | 82 | high |
| `comlab` | `labs/comlab/comlab/core/fault_atlas_router.py:1884` | `FaultAtlasRouter.route` | 31 | 119 | high |
| `vinlab` | `labs/vinlab/tools/tecdoc_cyl_from_codes.py:162` | `main` | 30 | 63 | high |
| `comlab` | `labs/comlab/registry/tools/render_case_library.py:26` | `main` | 26 | 67 | high |
| `gaslab` | `labs/gaslab/gaslab/rule_engine.py:243` | `_definitive_match` | 21 | 51 | high |
| `vinlab` | `labs/vinlab/tools/tecdoc_hardware_enricher.py:257` | `main` | 20 | 40 | high |
| `dtclab` | `labs/dtclab/dtclab/ranking.py:207` | `rank_candidates` | 19 | 44 | high |
| `vinlab` | `labs/vinlab/tools/build_vref_db.py:806` | `_enrich_from_csv` | 19 | 56 | high |
| `vinlab` | `labs/vinlab/tools/backfill_cylinder_count.py:116` | `run` | 17 | 32 | high |
| `obdlab` | `labs/obdlab/obdlab/core/sensor_signal_translator.py:71` | `SensorSignalTranslator.translate` | 16 | 44 | high |
| `comlab` | `labs/comlab/registry/integration_shim.py:519` | `_score_rule` | 15 | 24 | medium |
| `vinlab` | `labs/vinlab/tools/build_vref_db.py:768` | `_norm_euro_csv` | 15 | 26 | high |
| `vinlab` | `labs/vinlab/tools/tecdoc_ktype_bridge.py:116` | `extract_uncovered` | 15 | 91 | high |
| `vinlab` | `labs/vinlab/tools/build_vref_db.py:930` | `main` | 14 | 26 | high |
| `vinlab` | `labs/vinlab/tools/extract_opsi_engine_codes.py:76` | `extract` | 14 | 54 | high |
| `vinlab` | `labs/vinlab/vinlab/decoder.py:520` | `RobustVINDecoder.decode_vin_payload` | 14 | 25 | medium |
| `comlab` | `labs/comlab/comlab/core/fault_atlas_router.py:765` | `FaultAtlasRouter.evaluate_operator` | 13 | 17 | medium |
| `vinlab` | `labs/vinlab/tools/tecdoc_ktype_bridge.py:290` | `query_tecadoc` | 13 | 27 | high |
| `comlab` | `labs/comlab/comlab/core/fault_atlas_router.py:825` | `FaultAtlasRouter._prune_candidates` | 12 | 46 | high |
| `vinlab` | `labs/vinlab/tools/backfill_cylinder_count.py:42` | `parse_resolved_md` | 12 | 29 | high |
| `vinlab` | `labs/vinlab/tools/build_vds_map.py:150` | `_pass_c_pos8_legacy` | 12 | 20 | medium |
| `vinlab` | `labs/vinlab/tools/build_vref_db.py:192` | `_parse_overrides_stdlib` | 12 | 36 | high |
| `comlab` | `labs/comlab/registry/tools/build_corpus.py:452` | `main` | 11 | 13 | medium |
| `gaslab` | `labs/gaslab/gaslab/audits.py:47` | `find_uncovered_overlaps` | 11 | 32 | high |
| `vinlab` | `labs/vinlab/tools/build_vref_db.py:696` | `_merge_tecdoc_into_yaml` | 11 | 24 | medium |
| `vinlab` | `labs/vinlab/tools/tecdoc_ktype_bridge.py:403` | `main` | 11 | 16 | medium |
| `vinlab` | `labs/vinlab/vinlab/decoder.py:278` | `RobustVINDecoder._apply_vref_techmask` | 11 | 35 | high |

Test-only over-threshold functions were excluded from the production table above: `labs/gaslab/tests/unit/test_validators.py:421`, `labs/obdlab/tests/pid_logset/test_pid_logset_wiring_gate.py:105`, `labs/comlab/tests/unit/test_vocabulary_sae_iso_conformance.py:92`, `labs/vinlab/tests/unit/test_csv_suite.py:160`, and `labs/vinlab/tests/unit/test_csv_suite.py:274`.

## Clone signal: test-vs-production split

Clone counts are useful as an advisory metric but noisy as a default gate. `pyscn check --select deadcode,complexity,deps` intentionally excluded clones; `analyze --json` still measured clones for this evaluation.

| Target | Clone groups | All-test groups | All-prod groups | Mixed groups | Test-only pairs | Prod-only pairs | Mixed pairs |
|---|---:|---:|---:|---:|---:|---:|---:|
| `gaslab` | 22 | 18 | 4 | 0 | 152 | 5 | 0 |
| `obdlab` | 11 | 7 | 4 | 0 | 29 | 6 | 0 |
| `dtclab` | 8 | 7 | 0 | 1 | 13 | 0 | 1 |
| `comlab` | 68 | 59 | 9 | 0 | 720 | 27 | 0 |
| `dnalab` | 1 | 1 | 0 | 0 | 3 | 0 | 0 |
| `vinlab` | 17 | 4 | 13 | 0 | 17 | 24 | 0 |
| `symptomlab` | 2 | 1 | 0 | 1 | 2 | 0 | 3 |

Interpretation:

- GASLab and COMLab duplication is dominated by test-only clone pairs/groups, matching the architect smoke-test concern.
- VINLab has the strongest production clone signal: 13 all-production clone groups and 24 prod-only pairs.
- DTCLab and SymptomLab each have a mixed test/production clone signal; these should be reviewed manually before treating as defects.

## Coverage gaps

`pyscn` does **not** cover unused package dependencies and does **not** enforce lab isolation / cross-lab import policy. Use `deptry` for unused dependencies and `tach` or `import-linter` for the rule-5 lab-isolation import boundary. `pyscn deps` means within-tree dependency cycles, not cross-package import policy.

## Recommendation details for T-PYSCN-2

1. Add an agent-visible command that runs `pyscn check --select deadcode,complexity,deps --max-cycles 0` on Python-bearing targets.
2. Keep CI non-blocking at first and publish JSON/Markdown artifacts outside source control; do not commit generated HTML/JSON.
3. Exclude or skip empty non-Python targets (`labs/semantic`, `apps/wired`) until they contain `*.py`.
4. Treat clone output as advisory and split all-test, all-production, and mixed groups in any report.
5. Promote to a blocking CI gate only after one of these is true:
   - the 31 current production complexity findings are reduced below the chosen threshold, or
   - T-PYSCN-2 adds an explicit baseline/allowlist so new regressions fail without blocking pre-existing debt.
