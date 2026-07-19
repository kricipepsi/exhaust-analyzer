### Goal ###

Wire the v2 registry — 60 rules across 13 fault-family JSON files — into COMLab's `fault_atlas_router.py` via a translation shim in `registry/integration_shim.py`, gated behind the `USE_V2_REGISTRY` environment variable. Run side-by-side against the 281-case curated corpus and **gate cutover on v2 PASS count ≥ v1 PASS count**. The v1 path stays alive as rollback insurance; deletion is a separate later task. Also resolve the **CS-002 router-assumption gate** logged as unplanned-follow-up `CS-002-router-assumption` (line 62 of `REGISTRY_PROGRESS.md`): missing-chemistry + charging-DTC must NOT fire CS-002.

### Success criteria ###

- `registry/integration_shim.py` exists, parses, validates with pyright 0 errors, and imports only `stdlib + Pydantic + registry's own modules` (no imports from any lab, `comlab`, or `4DLabWired` — the registry self-contained invariant per `schema_v2.py` L4)
- At shim instantiation, all 13 rule files under `registry/rules/` load and validate against `RuleSet` from `registry/schema_v2.py`; load failure of any file is a fatal startup error with the file path in the message
- Shim exposes a single public entry point: `route_case(payload: dict) -> dict` returning the same dict shape `fault_atlas_router.py` produces for `OrchestratorFinalUIOutput` (the downstream consumers of the router output do **not** change in this task)
- `COMLab/comlab/core/fault_atlas_router.py` reads `os.environ.get("USE_V2_REGISTRY", "0")` at router instantiation; `"1"` (string) activates v2; anything else (unset, `"0"`, `""`) keeps v1 default
- When v2 is active, `fault_atlas_router.py` delegates to `registry.integration_shim.route_case(...)` and returns its output verbatim — no post-processing inside the COMLab router on the v2 path
- The harness `4DLabWired/harness/run_cases.py` respects `USE_V2_REGISTRY` (it already drives `wired.composition.diagnose()` which calls the router; no changes needed if the env-var read is at instantiation time — verify, do not assume)
- A new wrapper `4DLabWired/harness/run_side_by_side.py` runs the harness twice (v1 then v2), parses both `HARNESS_REPORT.md` outputs, and emits `4DLabWired/harness/SIDE_BY_SIDE_REPORT.md` containing: v1 PASS count, v2 PASS count, per-case divergence list (cases where v1 PASS but v2 FAIL, or v1 FAIL but v2 PASS), and a single-line cutover verdict
- **Cutover gate: v2 PASS count ≥ v1 PASS count on the 281-case curated corpus.** v1 baseline is 16.0 % (45/281) per `HARNESS_REPORT.md` 2026-05-27. If v2 PASS < v1 PASS, task closes with `Status=blocked` and the divergence report is attached to the progress note — do not flip to `done`
- **CS-002 router-assumption gate (mandatory unit test):** `registry/tests/test_integration_shim.py` includes `test_cs_002_no_fire_on_missing_chemistry`. Construct a payload with `{dtcs: ["P0562"], obd: {...minimal valid set...}, chemistry: None}` (or whatever sentinel the shim uses for "no chemistry observed"); assert the returned verdict's `fault_id` / `fault_family` is **not** `charging_system` / `CS-002`. If this test fails, the shim is using imputation semantics and CS-002 must be revised before cutover
- All existing registry tests pass (382 tests per the last progress note + however many test_integration_shim.py adds)
- All existing COMLab tests pass under v1 default (regression-safety)
- No new numeric literal in `integration_shim.py` lacks a `# wiki:` citation comment OR a `# convention:` comment naming the design doc that defines it
- The shim's evaluation algorithm is **documented in `registry/integration_shim.py`'s module docstring** — this is the first place v2's evaluation semantics are pinned down, and the rule-authoring discipline depends on it being explicit

### Context ###

**Why this is the payoff task.** All 13 REG-V2-AUTHOR-* tasks shipped (60 rules total, per `REGISTRY_PROGRESS.md` row REG-V2-AUTHOR-charging_system: *"Phase 5a 60/60 rules validate, 5b 189/189 refs resolve"*). The v1 router scores 16.0 % on the 281-case harness. The v2 rebuild is shelfware until COMLab can route through it. This task does the wiring, runs the side-by-side, and decides cutover.

**Why the shim lives in `registry/`, not COMLab.** Per `REGISTRY_START_HERE.md` L40: *"Python in this workstream appears only as schema (Pydantic), loader, validator, and the integration shim."* The shim is explicitly part of the registry workstream's Python surface. The architectural rule preserved is: **registry never imports COMLab**; **COMLab may import `registry.integration_shim`** (one-way dependency, never reversed). This keeps the v2 rule data + v2 evaluation logic co-located, so future rule-authoring tasks have a single place to verify their evaluation assumptions.

**Why an env var, not a kwarg or config file.** Decided at spec-authoring time: env var is the cleanest mechanism for the side-by-side harness wrapper to flip routing between back-to-back runs of `diagnose()`, without touching the API of `diagnose()` itself (which has many callers) and without spinning up config-reading infrastructure that COMLab does not currently use. Read once at router instantiation (not per-call) so a single test process exercises a single path.

**Why v1 stays alive.** Cutover is a one-shot moment with no rollback story. Keeping v1 alive for one release means flipping the default flag back to v1 if v2 surfaces a regression in production that the 281-case harness did not catch. v1 deletion is a separate future task that runs only after v2 has been proven in production. Out-of-scope here.

**The evaluation-algorithm decision (load-bearing).** `schema_v2.py` defines the rule **data shape** (chemistry/OBD/DTC evidence at DEFINITIVE/SUGGESTIVE/GATING tiers, `base_weight`, `confidence_ceiling`, `competition_group`). It does **not** specify how those fields combine into a final verdict. Every REG-V2-AUTHOR-* spec has implicitly assumed an algorithm; this task is the first place that algorithm gets written down. The spec commits to the following minimal algorithm (any deviation requires updating this section and all 13 author tasks' competition arguments):

1. **Gate check (per rule).** For each rule, check every `GATING` evidence entry across `chemistry_evidence`, `obd_evidence`, `dtc_evidence`. If any GATING entry is unsatisfied by the observed payload, the rule does **not** fire (skip immediately). Missing data (e.g. `chemistry is None`) means the GATING entry is unsatisfied (**hard-absence semantics** — this is the assumption CS-002 depends on, and the test `test_cs_002_no_fire_on_missing_chemistry` enforces it)
2. **Score accumulation (per firing rule).** Start at `base_weight`. For each satisfied `DEFINITIVE` entry across the three evidence lists, add `+0.10`. For each satisfied `SUGGESTIVE` entry, add `+0.05`. (Numeric constants here: `convention: REG-V2-INTEGRATE spec §Context — initial evidence-tier increments; revisit if PASS rate plateaus`.)
3. **Ceiling clamp.** If the rule has `confidence_ceiling` set, the rule's score is `min(score, confidence_ceiling)`.
4. **Competition resolution.** Group firing rules by `competition_group`. Within each group, the rule with the highest clamped score wins; ties broken by `base_weight` desc, then `rule_id` asc (deterministic). Each group emits one verdict.
5. **Top-fault selection.** Across all groups' emitted verdicts, the one with the highest clamped score is the top fault (cross-group selection). Ties broken the same way.
6. **Output shape.** Translate the winning rule's `fault_family` and clamped score into the same `OrchestratorFinalUIOutput` shape `fault_atlas_router.py` returns for v1. `fault_id` = `<RULE_ID>` (e.g. `"CS-002"`); `fault_name` = `Rule.description`; `ui_diagnostic_string` = `Rule.description`; `confidence` = clamped score; perception/KG enrichment fields = passthrough defaults (v2 does not own these — same as v1 sentinel behaviour).

This is a deliberately simple algorithm; the spec commits to it as the **first** working algorithm, not the final one. If the cutover gate (v2 PASS ≥ v1 PASS) fails, the most likely cause is the algorithm undershooting — that triggers a separate REG-V2-INTEGRATE-TUNE task, not algorithm changes here.

**Translation problem: v1 vs v2 schema shapes.** v1's `RegistryRow` (per `fault_atlas_router.py` L85-96) carries `fault_id`, `cross_domain_matrix` (gas_lab_state, obd_live_pids, dtc_lab_status), `confidence_scoring` (base_weight, bonus_on_dtc_match), `routing_tag`, `perception_flag`. v2's `Rule` (per `schema_v2.py` L216-257) carries `rule_id`, `fault_family`, `chemistry_evidence`/`obd_evidence`/`dtc_evidence` (each tier-weighted), `base_weight`, `competition_group`, `confidence_ceiling`, `passes_cases`, `perception_flag`, `precondition`. The shim does **not** translate v2 rules into v1 RegistryRow objects and reuse v1's evaluator — that would lose tier semantics and competition discipline. The shim implements the algorithm above directly on the v2 `Rule` objects.

**Payload shape: what the shim consumes.** The shim consumes the same dict shape `fault_atlas_router.py` receives from `wired.composition.diagnose()` (the `OrchestratorInboundRequest` payload — see `fault_atlas_router.py` L23). The shim does not invent a new payload format; it parses the existing one into the chemistry / OBD / DTC observations its evaluation algorithm expects. Mapping:
- `payload.gas.state` → `ChemistryState` enum value (or `None` if not present — triggers hard-absence on GATING chemistry rules)
- `payload.obd.pids` → `dict[pid_name, value]` for `OBDEvidence` operator checks
- `payload.dtcs.codes` → `list[str]` for `DTCEvidence` membership checks

If the existing payload shape doesn't carry exactly these fields under exactly these names, the shim's parser maps them and the docstring documents the mapping. The shim does not import COMLab schemas — it uses `dict` indexing or local Pydantic mirrors.

**The CS-002 router-assumption gate (in detail).** Unplanned-follow-up `CS-002-router-assumption` (line 62 of `REGISTRY_PROGRESS.md`) says: *"CS-002 `NORMAL_OPERATION`-GATING assumes COMLab router treats missing chemistry as 'rule does not fire' (hard-absence), not 'default to NORMAL' (imputation)."* This task **implements** that assumption (step 1 of the algorithm above explicitly enforces hard-absence) and **verifies** it via `test_cs_002_no_fire_on_missing_chemistry`. Construct the test payload with `chemistry=None` (or whatever the shim's sentinel for no-observation is — to be defined in the shim) plus `dtcs=["P0562"]` plus a minimal valid OBD slice; assert the verdict is not `charging_system`. If the test passes, the follow-up row closes at task end. If it fails because some other rule incorrectly fires on missing chemistry, that's a separate bug to surface as a new unplanned-follow-up, not a fix in this task.

**What v1 currently scores.** 16.0 % PASS (45/281) per `HARNESS_REPORT.md` 2026-05-27 (cited in `REGISTRY_PROGRESS.md` line 84). v2's projected target is "≥ 75 %" (line 86), but the cutover gate is the weaker condition `v2 PASS ≥ v1 PASS`. Beating 16.0 % is the minimum bar; the rebuild's higher ambitions are a separate question.

Load skills: (none — no on-demand domain skills authored yet per `_INDEX.md`)

### Deliverables ###

1. `registry/integration_shim.py` — CREATE. Module docstring **must** include the evaluation algorithm verbatim from the Context section above. Public surface: a single class `RegistryV2Router` with constructor `__init__(rules_dir: Path = Path("registry/rules"))` (loads + validates all 13 rule files at construction; raises on any load failure with the file path in the message) and method `route_case(payload: dict) -> dict` (runs the 6-step algorithm, returns a dict matching `OrchestratorFinalUIOutput`'s field set). Convenience module-level function `route_case(payload: dict) -> dict` that lazily instantiates a singleton router on first call. No COMLab/lab imports.

2. `registry/tests/test_integration_shim.py` — CREATE. Tests:
   - `test_shim_loads_all_13_rule_files` — constructor succeeds, count of loaded rules == 60
   - `test_shim_raises_on_missing_rule_file` — temp-dir test: missing one of the 13 expected files raises with path in message
   - `test_shim_raises_on_invalid_rule_json` — temp-dir test: malformed JSON raises with path in message
   - `test_route_case_returns_correct_shape` — minimal payload returns a dict with the expected key set (fault_id, fault_name, confidence, ui_diagnostic_string)
   - `test_route_case_no_fault_when_no_rules_fire` — empty payload returns the `ERR-UNKNOWN-000` sentinel (matching v1's behaviour at `fault_atlas_router.py` L42)
   - `test_cs_001_fires_on_p0562` — payload with `dtcs=["P0562"]`, NORMAL chemistry, minimal OBD → verdict is `CS-001` / `charging_system` / confidence ≤ 0.85
   - `test_cs_002_no_fire_on_missing_chemistry` — **the mandatory gate test.** Payload with `dtcs=["P0562", "P0300"]`, `chemistry=None`, minimal OBD → verdict's `fault_family != "charging_system"` AND `fault_id != "CS-002"`. Assertion message must reference the unplanned-follow-up ID `CS-002-router-assumption` so a future failure is traceable
   - `test_cs_002_fires_on_normal_chemistry` — payload with `dtcs=["P0562", "P0300"]`, `chemistry="NORMAL_OPERATION"`, minimal OBD → verdict IS `CS-002` / `charging_system`. (Pairs with the previous test to prove the hard-absence semantics specifically, not a blanket "CS-002 never fires" bug)
   - `test_competition_resolution_picks_higher_ceiling` — synthetic 2-rule setup in the same competition_group with different ceilings; verify the higher one wins
   - `test_gating_obd_unsatisfied_does_not_fire` — payload that satisfies chemistry but not an OBD GATING entry → rule does not fire
   - `test_no_unauthorised_imports` — `ast` parse of `integration_shim.py`, assert no `import` or `from` statement names `comlab`, `gaslab`, `obdlab`, `dtclab`, `dnalab`, `4DLabWired`

3. `COMLab/comlab/core/fault_atlas_router.py` — MODIFY. Smallest possible diff:
   - Add `import os` (if not already present)
   - In the router's `__init__` (or wherever the per-instance config is read), read `os.environ.get("USE_V2_REGISTRY", "0")`. Store as `self._use_v2 = (value == "1")`
   - In the route entry method (`route()` or equivalent), if `self._use_v2`, `from registry.integration_shim import route_case as _v2_route_case; return _v2_route_case(payload)` (lazy import inside the branch so the v1 default path has zero registry dependency). Otherwise fall through to the existing v1 logic unchanged
   - No other changes to v1 code paths

4. `COMLab/comlab/core/tests/test_fault_atlas_router_v2.py` — CREATE (or extend an existing test file if `_v2.py` naming conflicts with a convention). Tests:
   - `test_v1_default_when_env_unset` — `os.environ.pop("USE_V2_REGISTRY", None)`; instantiate router; call `route(...)`; assert behaviour matches a known v1 fixture
   - `test_v2_active_when_env_set_to_1` — `os.environ["USE_V2_REGISTRY"] = "1"`; instantiate router; call `route(...)`; assert the call delegates (mock or spy on `registry.integration_shim.route_case`)
   - `test_v1_when_env_set_to_0` — explicit "0" stays on v1
   - `test_v1_when_env_set_to_garbage` — `"true"`, `"yes"`, `"on"` all stay on v1 (only literal `"1"` activates v2)
   - Each test must `monkeypatch` `os.environ` and clean up after itself

5. `4DLabWired/harness/run_side_by_side.py` — CREATE. Standalone script (`python3.14 4DLabWired/harness/run_side_by_side.py`). Behaviour:
   - Run 1: `os.environ.pop("USE_V2_REGISTRY", None)`; invoke harness; capture `HARNESS_REPORT.md`; copy to `HARNESS_REPORT_v1.md`; extract PASS count
   - Run 2: `os.environ["USE_V2_REGISTRY"] = "1"`; invoke harness; capture `HARNESS_REPORT.md`; copy to `HARNESS_REPORT_v2.md`; extract PASS count
   - Write `4DLabWired/harness/SIDE_BY_SIDE_REPORT.md` containing: v1 PASS / v2 PASS counts, per-case divergence table (case_id, v1 outcome, v2 outcome) for any case where the two disagree, and the cutover verdict line `**CUTOVER GATE: PASS**` or `**CUTOVER GATE: BLOCKED (v2 PASS=X < v1 PASS=Y)**`
   - Exit code 0 if gate passes, 1 if blocked (so the verification block below can shell-out and check)

### Files to touch ###

- `registry/integration_shim.py` (CREATE)
- `registry/tests/test_integration_shim.py` (CREATE)
- `COMLab/comlab/core/fault_atlas_router.py` (MODIFY — env-var read + lazy delegation only; do not touch v1 logic)
- `COMLab/comlab/core/tests/test_fault_atlas_router_v2.py` (CREATE)
- `4DLabWired/harness/run_side_by_side.py` (CREATE)

### Out of scope ###

- **v1 router deletion.** v1 stays alive as rollback insurance for one release; deletion is a separate future task that runs only after v2 has been proven in production
- **Changes to any v2 rule file** under `registry/rules/`. All 13 family files are frozen for this task. If the side-by-side run surfaces that a specific rule should change to pass a case, that's a follow-up REG-V2-AUTHOR-<family>-vN task, not in scope here
- **Changes to `registry/schema_v2.py`.** The schema is frozen. If the evaluation algorithm reveals a missing field (e.g. needs a per-rule precondition that's not expressible today), that's a separate REG-V2-SCHEMA-* task
- **Changes to the curated corpus** (`registry/corpus_curated.csv` or `4DLabWired/TestSuite/cases_petrol_master_v6.csv`). Corpus is frozen; the cutover gate evaluates against the existing 281 cases
- **Algorithm tuning.** The 6-step algorithm in Context is the *first* working algorithm. If `v2 PASS < v1 PASS`, the task closes `blocked` and a separate REG-V2-INTEGRATE-TUNE task adjusts increments/ceilings. Do not silently adjust the algorithm in this task to chase a passing gate
- **Downstream consumers of `OrchestratorFinalUIOutput`** in COMLab (analytics, KG enrichment, response assembly). The shim returns the same dict shape; nothing downstream changes
- **Performance / latency optimization.** Shim's job is correctness, not speed. Rule files load once at router instantiation
- **The `charging-system-alternator-gap` follow-up** (unplanned-follow-up line 63) — that's a wiki update + a future REG-V2-AUTHOR-charging_system-v2 task, not part of integration
- **REG-WIKI** (HTML rendering) — separate concern, parallel task in the ledger
- **Modifications to `wired.composition.diagnose()`** beyond confirming it respects router instantiation (which already reads the env var via the modified `fault_atlas_router.py`)

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Inner loop — Python files
python3.14 -m py_compile registry/integration_shim.py
python3.14 -m py_compile COMLab/comlab/core/fault_atlas_router.py
ruff check registry/integration_shim.py registry/tests/test_integration_shim.py --fix
pyright registry/integration_shim.py registry/tests/test_integration_shim.py

# Registry-side tests
pytest registry/tests/test_integration_shim.py -x -q
pytest registry/tests/ -x -q   # full registry regression (382+ tests)

# COMLab-side tests (regression-safety under v1 default)
unset USE_V2_REGISTRY 2>/dev/null
pytest COMLab/comlab/core/tests/ -x -q

# COMLab-side tests (v2-active path)
pytest COMLab/comlab/core/tests/test_fault_atlas_router_v2.py -x -q

# CS-002 router-assumption gate
pytest registry/tests/test_integration_shim.py::test_cs_002_no_fire_on_missing_chemistry -x -v
pytest registry/tests/test_integration_shim.py::test_cs_002_fires_on_normal_chemistry -x -v

# Side-by-side run + cutover gate
python3.14 4DLabWired/harness/run_side_by_side.py
# Exit code 0 = cutover gate PASS; exit code 1 = BLOCKED
echo "Side-by-side exit: $?"

# Cat the report so the PASS/FAIL line is in the session log
cat 4DLabWired/harness/SIDE_BY_SIDE_REPORT.md | head -30

# Mirror invariant — registry's DTCRoutingTag still has 20 members
python3.14 -c "
from registry.schema_v2 import DTCRoutingTag
n = len(list(DTCRoutingTag))
assert n == 20, f'DTCRoutingTag has {n} members, expected 20 (mirror invariant broken)'
print(f'DTCRoutingTag mirror intact: {n} members')
"

# Self-contained invariant — integration_shim has no forbidden imports
python3.14 -c "
import ast, pathlib
src = pathlib.Path('registry/integration_shim.py').read_text()
tree = ast.parse(src)
forbidden = {'comlab', 'gaslab', 'obdlab', 'dtclab', 'dnalab'}
for node in ast.walk(tree):
    if isinstance(node, (ast.Import, ast.ImportFrom)):
        names = [n.name for n in (node.names if isinstance(node, ast.Import) else [])]
        if isinstance(node, ast.ImportFrom):
            names = [node.module] if node.module else []
        for name in names:
            root = (name or '').split('.')[0]
            assert root not in forbidden and root != '4DLabWired', \
                f'integration_shim.py imports {name} — forbidden by registry self-contained rule'
print('integration_shim.py imports OK — no forbidden modules')
"
```

All steps must pass. If the side-by-side cutover gate is BLOCKED (exit 1), the task closes with `Status=blocked` and the divergence report is attached to the progress note — do **not** flip to `done`.

### Progress hook ###

`REGISTRY_PROGRESS.md` `REG-V2-INTEGRATE`: `Status=done` (if cutover gate passes) or `Status=blocked` (if v2 PASS < v1 PASS — attach divergence report to progress note). Files changed=5. Verification="v1 PASS=X (16.0% baseline) → v2 PASS=Y; cutover gate {PASS|BLOCKED}; CS-002 router-assumption gate {PASS|FAIL}".

At task close, regardless of cutover outcome, **close the unplanned-follow-up row `CS-002-router-assumption`** in `REGISTRY_PROGRESS.md` (line 62) — the assumption is now either verified-and-implemented (gate test passes) or surfaced-as-bug (gate test fails). Either way the follow-up is no longer "pending".
