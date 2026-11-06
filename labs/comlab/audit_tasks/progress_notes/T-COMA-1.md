# T-COMA-1 progress note: non_starter family gate + NS-NO-RULE abstain (F-C1-7)

Session 1 (plan phase). `plan: REQUIRED`. This session makes no edit to the clone. It stops after `## Plan`.

## Baseline (First action, Preconditions)

```
$ cd C:/4DApp/repo && git branch --show-current && git log --oneline -1 && git status --porcelain
fix/T-COMA-1
8092b4c spec(T-COMA-1): non_starter family gate + NS-NO-RULE abstain (F-C1-7); T-COMA-2/3 registered
(porcelain: empty)
$ git merge-base --is-ancestor c5371cc HEAD && echo ok   -> ok  (2e07e9c is also an ancestor)
$ <Preconditions loop>                                    -> checked   (no MISSING, no EXISTS line)
```
Base = `8092b4c`.

Base measurements (read-only; pytest `--basetemp` under `C:/4DApp/recheck/T-COMA-1/pt/*_base`):

| check | command (from the task's Verification, base tree) | result | pinned |
|---|---|---|---|
| audit probe | `pytest audit/scratch/C1/test_c1_stage_a.py -k will_not_start_does_not_score` | `1 failed, 10 deselected`. `assert 'rich_mixture' != 'rich_mixture'` at line 74. `suppress_gaslab: True verdict: RM-001 rich_mixture 1.0` | P7 base |
| rehearsed test file | `cd apps/wired && PYTHONPATH=tests pytest C:/4DApp/recheck/T-COMA-1/tests/test_t_coma_1_non_starter_family_gate.py` | `13 failed, 1 passed`. 3× EF-004, 3× CF-001, 6× MF-001 instead of NS-NO-RULE; case_006 II-002 instead of NS-004; the running PIN passes | P5 base |
| probe.py | `probe.py C:/4DApp/recheck/T-COMA-1/impl/corpus_base_mine.json` | 15 probes: stoich → ecu_fault EF-004, rich → catalyst_failure CF-001, lean/crank_lean/crank_rich → misfire MF-001, for all 3 `tier_2`; `corpus 314`; my dump equals Cowork's `corpus_base.json` (diff `[]`) | P1 |
| comlab | `cd labs/comlab && pytest --continue-on-collection-errors` | `531 passed, 4 skipped, 2 errors` | P6 |
| registry | `pytest registry/tests --deselect registry/tests/test_render_case_library.py` | `5 failed, 502 passed, 4 deselected`. All 5 failures are in `test_build_corpus.py` (TestParseBlueprint ×3, TestOutputContracts ×2) | P6 |
| wired / ui | `cd apps/wired && pytest`; `cd apps/ui && pytest` | `65 passed`; `38 passed` | P6 |

After these runs, `git status --porcelain` is empty.

## Readiness challenge

- (a) Starting state matches the task: branch `fix/T-COMA-1`, HEAD `8092b4c` (spec commit, a descendant of `c5371cc` and `2e07e9c`), clean tree, Preconditions `checked`. The rehearsal anchors in `apply_fix.py` are present: `integration_shim.py:150` `_NO_FAULT_REMEDIATION`, `:1171` `_translate_to_output`, `:1204` `if winner is None:`, `:1327` `obs = _build_observation(payload)`, `:1362` `return _translate_to_output(winner, payload), diagnostics`; `fault_atlas_router.py:1953` lazy import, `:2150` `if is_fault:`; `response.py:106`; `app.py:980-981`; wiki `07_pipeline_stages.md:173-174`. P1 and P6 base were measured (table above).
- (b) The tests fail for the intended reason. The rehearsed file gives `13 failed, 1 passed` on the base. Each failure is an idle-gas family (`ecu_fault`, `catalyst_failure`, `misfire`, `invalid_input`) that wins a `will_not_start` session. The audit probe fails on `v.fault_family != "rich_mixture"`, not on its `suppress_gaslab is True` precondition, which passes.
- (c) I derived the decisive values independently. (1) `_apply_competition` returns None only when `scored` is empty (`integration_shim.py` `if not scored: return None`). After the gate, NS-NO-RULE therefore means "no `non_starter` rule fired", and the router's prior, discriminator and delta loops run over an empty `scored_rules`, so confidence stays 0.0. (2) case_006: a spy on the base shim shows NS-004 scored at `0.75` (only NS rule, among 19 scored). The `non_starter` symptom prior `prior_weight: 0.10` (`comlab/config/symptom_prior.yaml:20`; ctxmod off by default) gives `0.85`. That is `>= ABSTAIN_FLOOR 0.80` (`fault_atlas_router.py:81`), and no other family is left for a margin check, so the result is NS-004 0.85, not abstained. This equals Cowork's `corpus_fix.json` and P4. (3) Mutant counts: gate off → 12 abstain tests + case_006 fail = `13 failed, 1 passed`. no_rule branch off → score 0.0 < floor gives `abstain_reason "floor"`, so the 12 abstain tests fail and case_006 + PIN pass = `12 failed, 2 passed`. Abstain verdict off → no-fault sentinel, so the 12 fail and case_006 (gate still prunes) + PIN pass = `12 failed, 2 passed`. All three equal P5.
- (d) No contradiction or missing decision prevents implementation. R1-R7 are specific and each anchor exists. The open choices are listed under `## Plan` › Choices.
- (e) Teach-back: when the routing directive marks `suppress_gaslab` (a `will_not_start` session), the v2 shim scores only `non_starter` rules and prunes every other rule as `family_gate`. If none fires, it returns the `NS-NO-RULE` `non_starter` verdict, which the router marks abstained with reason `no_rule` at confidence 0.0. The decisive check is the new 14-test file (`14 passed`; each P5 mutant fails its named tests) plus the audit probe C1 `will_not_start_does_not_score` (`1 passed`) and the corpus compare that changes exactly the 5 `will_not_start` cases.

## Assumptions worked past

- A1. The plan stop needs no RESULT file. The header says "stop before the first edit and hand back; this stop needs no blocker JSON", and the RESULT belongs to the finish line. I wrote only this note.
- A2. To run the rehearsed test file on the base, I ran it in place from `C:/4DApp/recheck/T-COMA-1/tests/` with `cd apps/wired && PYTHONPATH=tests`. I did not copy it into the clone, so the tree stayed clean.
- A3. P4's "case_006 … NS-004 (score 0.85)" is the post-prior verdict score. The shim score is 0.75 (readiness c). The test asserts only family + code. I took 0.85 as the verdict value and do not assert it in the test (R6 names the rehearsed file, which does not assert it).

## Plan

### Approach
Follow Cowork's rehearsal `apply_fix.py` (R1-R4) in shape. Write R5 and R7 by hand. Copy the rehearsed test file as R6. Then one commit, then the mutants, then `### Verification ###`.

### Signatures (new / changed)
- `integration_shim.NON_STARTER_NO_RULE_CODE: str = "NS-NO-RULE"` (public; consumer: `fault_atlas_router.py route()`).
- Private constants `_NON_STARTER_NO_RULE_NAME`, `_NON_STARTER_NO_RULE_REMEDIATION` (R2 strings verbatim), `_PRUNE_REASON_FAMILY_GATE = "family_gate"`, `_GATING_KEY_WILL_NOT_START = "engine_state:will_not_start"`.
- `def _non_starter_gate(payload: dict[str, Any]) -> bool`: `bool(getattr(payload.get("routing_directive"), "suppress_gaslab", False))`. No raise. No COMLab import (firewall kept).
- `def _translate_to_output(winner: tuple[Rule, float] | None, payload: dict[str, Any], non_starter_gate: bool = False) -> dict[str, Any]`: there is a new branch `winner is None and non_starter_gate` before the no-fault branch. The default `False` keeps every other caller (`render_ranked_rule`, tests) unchanged.
- `RegistryV2Router.route_case_with_diagnostics`: computes the gate once. When the gate is True, it appends each non-`NON_STARTER` rule to `pruned_rules` with the R1 reason/key and does not call `_score_rule` for it. It passes the gate to `_translate_to_output`. The return type is unchanged.
- `FaultAtlasRouter.route` (v2): `NON_STARTER_NO_RULE_CODE as _V2_NS_NO_RULE` is added to the existing lazy import. `if winner_rule_id == _V2_NS_NO_RULE: abstained, abstain_reason = True, "no_rule"`, then `elif is_fault:` keeps the floor/margin code as it is.
- `DiagnosticVerdict.abstain_reason: Optional[Literal["floor", "margin", "no_rule"]]`.

### Boundary cases
- `routing_directive` key absent (registry tests, direct shim callers): `getattr(None, …, False)` → gate False → behaviour unchanged.
- `routing_directive` present with `suppress_gaslab False` (running, cranking): gate False → unchanged.
- `routing_directive` as a plain dict (no producer in the repo; both producers, `lab_pipeline_aggregator.py:652` and `:676`, pass the `LabRoutingDirective` object): gate False. I accept this as a known false fail (below) because R1 mandates `getattr`.
- Gate True and a `non_starter` rule fires (case_006): normal winner path. The prior/discriminator/delta still run, but only over `non_starter` rules.
- Gate True and nothing fires: NS-NO-RULE. `scored_rules` is empty, so the prior "update winner score" block (needs non-empty `scored_rules`), the discriminator and the delta re-render do not run. `differential_siblings` = `[]`.
- v1 path (`use_v2_registry=False`): not touched (out of scope).

### Choices the task leaves open
| # | option taken | option rejected | why |
|---|---|---|---|
| C1 | The prune reason/key are named module constants beside the FT-3 prune vocabulary (`integration_shim.py:152-162`) | inline literals (rehearsal) | the neighbours name every prune literal with a `# consumer:` comment |
| C2 | The enrichment fields (`mechanical_failure_mode`, `ui_remediation_steps`) are set as locals in each verdict branch | nested conditional expressions keyed on `fault_code` (rehearsal) | a three-way chained ternary is hard to review. Output is identical: no-fault → today's strings; winner → `fault_name[:280]` / "See diagnostic verdict for next steps."; NS-NO-RULE → R2 name / R2 remediation |
| C3 | Add `NON_STARTER_NO_RULE_CODE` to the shim's `__all__` | leave `__all__` as is (rehearsal) | R2 calls it a public constant, and the router imports it |
| C4 | The router test is `winner_rule_id == _V2_NS_NO_RULE`, before `if is_fault` | test `fault_family == non_starter and confidence == 0` | R3 names `fault_code`; `winner_rule_id` is the `fault_code` (`fault_atlas_router.py:2136`) |
| C5 | R4 changes only the caption | also reword `st.info("No single confident verdict — top candidates:")` | R4 scopes the caption; the info line is recorded as a remaining risk |
| C6 | The R6 file is the rehearsed file, copied unchanged into `apps/wired/tests/` | rewrite it | R6 names "the 14 tests of the rehearsed file", and it already gave `13 failed, 1 passed` on the base |
| C7 | Mutants are in-tree edits after the commit, each undone with `git restore <path>` and `git diff --quiet` checked | a monkeypatch script under `recheck/` | `### Files to touch ###` authorises no script path; AGENTS: undo is git on the task branch |
| C8 | R7 text is verbatim, re-wrapped to the file's width (≤ 120 chars) | a single long line | matches the neighbouring paragraphs |

### Rules and gates this plan adds
1. **Family gate (R1).** Checked on: the 15 `probe.py` probes and the 314-case corpus (`load_corpus()`, of which 5 are `will_not_start`). Base measured this session; fix rehearsed by Cowork in `corpus_fix.json`. Runs over: every v2 `route()` call whose payload carries a `LabRoutingDirective` with `suppress_gaslab` True. `route_symptom` sets that exactly when `engine_state == "will_not_start"` (`symptom_router.py:68`). Command: `probe.py C:/4DApp/recheck/T-COMA-1/impl/corpus_fix.json`, then the JSON compare in Verification step 3. False pass (a session gated when it should not be): only a hand-built directive with `suppress_gaslab` True on a running engine. No such producer is in the repo. False fail (a non-starter not gated): `engine_state` missing (route_symptom routes neutral), the directive serialised to a dict, or the v1 path.
2. **NS-NO-RULE abstain (R2 + R3).** Checked on and runs over: the same population, restricted to gated sessions where no `non_starter` rule fires (corpus: 4 of 5; probes: 15 of 15). False pass (abstains when a rule should have fired): NS-001..003 never score because GASLab marks cranking samples INVALID (P2), and case_040's P0335 is not in NS-004's DTC list. The abstain is still honest, not a wrong family. T-COMA-3 owns this. False fail (a wrong verdict when it should abstain): none found. The code is emitted only when the gate is True and `scored` is empty, and the router keys only on that code.
3. **R5 fixture change.** It changes what the comlab suite runs against: `case_014_gas_dominant` then expects NS-NO-RULE / non_starter. The manifest test still holds: the families become {no_fault, rich_mixture, catalyst_failure, non_starter, misfire}, which is ≥3 besides no_fault, and GAS_DOMINANT is still present. `LOW_CERTAINTY` comes from the aggregator's horizon heuristic (`lab_pipeline_aggregator.py:210`), not from the shim's rating, so it stays.
4. **Step order that changes later steps.** The commit comes before the mutants. Each mutant is restored with `git restore` before the next one, and `git diff --quiet` must pass before the Verification run. The Verification run is on the committed tree.

### Commands and the paths they write (redispatch)
1. Edit the 7 in-scope files (R1-R5, R7) and create the R6 file. Writes only `### Files to touch ###` paths.
2. Inner loop: `$PY -m py_compile`, `C:/4DApp/.venv-loop/Scripts/ruff.exe check`, `py -m ruff check --select S`, `py -m pyright --pythonpath C:/4DApp/.venv/Scripts/python.exe` on the 5 `.py` files. Writes nothing.
3. Run the new file: `cd apps/wired && pytest -q -p no:cacheprovider tests/test_t_coma_1_non_starter_family_gate.py --basetemp=C:/4DApp/recheck/T-COMA-1/pt/new`. Expect `14 passed`.
4. `git add <7 paths>`, then on its own line `git -c user.name=Claude -c user.email=noreply@anthropic.com commit -m "fix(T-COMA-1): …"` on `fix/T-COMA-1`.
5. Mutants M1 (`_non_starter_gate` returns False), M2 (router `no_rule` branch removed), M3 (gate-True no-winner branch disabled). After each: the new file → `13F/1P`, `12F/2P`, `12F/2P`, failing names recorded; `git restore <path>`; `git diff --quiet`. pytest writes only under `C:/4DApp/recheck/T-COMA-1/pt/m{1,2,3}`.
6. `### Verification ###` steps 1-6 as written. The probe writes `C:/4DApp/recheck/T-COMA-1/impl/corpus_fix.json`. pytest writes `C:/4DApp/recheck/T-COMA-1/pt/*`.
7. Task-end extras: anti-orphan grep for `NON_STARTER_NO_RULE_CODE`, `_non_starter_gate`, `family_gate`, `no_rule`; `$PY audit/tools/isolation.py` (`violations: 4` or fewer); the deployed-layout import sanity.
8. Write this note's VERIFICATION GATE, CODE REVIEW and `## Time` blocks, and `results/RESULT_T-COMA-1.md`. Both stay uncommitted (criterion 5).

### Remaining risks (for review)
- F-C1-10 is unchanged: the prior re-sort can still write another rule's score into a `non_starter` verdict, now only among `non_starter` rules. T-AUD-2 keeps it.
- The UI abstain branch still says "No single confident verdict — top candidates:" above the NS-NO-RULE card (C5).
- The out-of-repo Jaeger analyser (`4DLabWired/_jaeger/analyse_failure_modes.py`, not in this clone: `git ls-files | grep analyse_failure_modes` is empty) will see a new `prune_reason` `family_gate`. This is telemetry only.
- No test exercises the R4 caption. The ui suite (`38 passed`) and the diff review are its only checks, unless Cowork asks for an AppTest probe.

## Plan round 2 (redispatch, 2026-11-06)

The plan was approved in `corrections/T-COMA-1_plan_correction_20261106.md` with the corrections K1-K4 (task § R8). That file has no `### Plan-time digest ###` table, so there is no digest to recompute.

Starting state: HEAD `e0d09ab spec(T-COMA-1): plan approved with corrections K1-K4 (R8)`, which descends from `c5371cc`; branch `fix/T-COMA-1`. `git status --porcelain` shows only `?? labs/comlab/audit_tasks/progress_notes/`, which is this note from session 1 (A4). Base = `e0d09ab`.

Changes to the plan:
- K1: no `py_compile` (it writes `__pycache__`). Syntax is checked by ruff and pyright only. This removes step 2's `py_compile`.
- K2: `audit/tools/isolation.py` must print the same 4 violation lines as the base (`test_abstain_margin_002.py:20`; `test_tunable_reweight.py:23`, `:24`, `:25`). I compare the lines themselves, not only the count.
- K3: the RESULT holds the full shim output for the `stoich` / `prolonged_crank_hard_start` probe payload through `RegistryV2Router().route_case_with_diagnostics`, compared with R2.
- K4 replaces C5: in the ABSTAIN branch with `abstain_reason == "no_rule"`, the `st.info` line reads "ℹ️ No confident non-start verdict:". Floor and margin keep their line. The R4 caption stands.

Assumption added:
- A4. The only untracked path at redispatch is this note, written in session 1 inside the write scope. It is not a baseline mismatch (stop d).
- A5. Cowork committed `cba05c1 spec(T-COMA-1): file the second plan review` at 08:43:46Z. That is 8 s after this session started at 08:43:38Z, and before my commit. It adds only `plan_review/second_review_T-COMA-1-plan.md`. It is the newest `spec(T-COMA-1):` commit, so I take it as the base. My commit `208eca3` has `cba05c1` as its parent.
- A6. Deviation from C6: the rehearsed test file failed Verification step 5's ruff (`I001`, import order). I applied ruff's `--fix` to that one file, which only reorders the imports. The tests are unchanged.

Implementation decisions:
- D1. Commit form: `bash_guard` refused the commit when it was chained after `cd … &&`. I ran it as a single `git -C C:/4DApp/repo … commit` command.
- D2. Mutants were in-tree `sed` edits after the commit. Each was undone with `git restore <path>`, and `git diff --quiet` printed `restored` after each one.

## Mutants (P5, R6 record)

Command for each: `cd apps/wired && pytest -q -p no:cacheprovider tests/test_t_coma_1_non_starter_family_gate.py --basetemp=C:/4DApp/recheck/T-COMA-1/pt/m{1,2,3} -rfE`.

| mutant | edit | result | failing tests (by name) |
|---|---|---|---|
| M1 family gate off | `_non_starter_gate` → `return False` | `13 failed, 1 passed` | all 12 `test_non_starter_without_a_matching_rule_abstains[{crank_lean,idle_lean,idle_rich,idle_stoich}-{prolonged_crank_hard_start,no_crank_silent,fast_crank_whining}]` + `test_non_starter_dtc_rule_wins` |
| M2 router `no_rule` branch off | `if winner_rule_id == _V2_NS_NO_RULE:` → `if False:` | `12 failed, 2 passed` | the same 12 `test_non_starter_without_a_matching_rule_abstains[…]` |
| M3 abstain verdict off | `if winner is None and non_starter_gate:` → `if False:` (no rule → no-fault sentinel) | `12 failed, 2 passed` | the same 12 `test_non_starter_without_a_matching_rule_abstains[…]` |

`test_running_session_is_not_gated` passes under all three mutants: it is a PIN. `test_non_starter_dtc_rule_wins` fails only under M1.

## VERIFICATION GATE

Run from `C:/4DApp/repo`, on `208eca3`, after the mutant restores (`git diff --quiet` was true).

| step | command | expected | observed | verdict |
|---|---|---|---|---|
| 1 | new file | `14 passed` | `14 passed in 2.57s` | PASS |
| 1 | comlab `--continue-on-collection-errors` | `531 passed, 4 skipped, 2 errors` | `531 passed, 4 skipped, 2 errors in 9.75s` (the base gave the same; the 2 errors are the known R0-2 collection errors) | PASS |
| 2 | registry without the render test | `5 failed, 502 passed, 4 deselected` | `5 failed, 502 passed, 4 deselected`. The 5 failures are the same `test_build_corpus.py` set as the base | PASS |
| 2 | wired | `79 passed` | `79 passed in 5.09s` (base 65 + 14 new) | PASS |
| 2 | ui | `38 passed` | `38 passed in 3.37s` | PASS |
| 3 | `probe.py …/impl/corpus_fix.json \| grep -c "NS-NO-RULE', True, True, 'no_rule', 0.0"` | `15` | `15` | PASS |
| 3 | base vs fix corpus compare | `['REAL-002', 'REAL-003', 'case_006', 'case_007', 'case_040']` | the same list. 314 keys each. My `corpus_fix.json` is identical to Cowork's rehearsed `corpus_fix.json` | PASS |
| 3 | `git status --porcelain` | only the note (and the RESULT) | `?? labs/comlab/audit_tasks/progress_notes/` | PASS |
| 4 | audit probe C1 `-k will_not_start_does_not_score` | `1 passed, 10 deselected` | `1 passed, 10 deselected in 1.07s`; `suppress_gaslab: True verdict: NS-NO-RULE non_starter 0.0` | PASS |
| 5 | `.venv-loop` ruff on the 5 `.py` files | `All checks passed!` | `All checks passed!` | PASS |
| 6 | `git log --oneline -4; git status --porcelain` | the spec commits + mine; only the note/RESULT | `208eca3 fix(T-COMA-1)…`, `cba05c1 spec…`, `e0d09ab spec…`, `8092b4c spec…`; status as in step 3 | PASS |

The previous decisive failure is gone. On the base, the probe failed with `assert 'rich_mixture' != 'rich_mixture'`, and the new file gave `13 failed` with idle-gas families. Both are now green.

Task-end extras (skill gate):
- `py -m ruff check` (system ruff 0.15.18) on the 5 files: `All checks passed!`. `--select S`: 1 × S110 at `apps/ui/app.py:139`, which is pre-existing (the base `app.py` gives 1 S finding too), and 5 × S101 `assert` in the new test file, which is expected in a pytest file. My edits add no S finding.
- pyright 1.1.410 with `--pythonpath C:/4DApp/.venv/Scripts/python.exe` on the 5 files: `0 errors, 0 warnings, 0 informations`.
- K1: `py_compile` was NOT RUN, by ruling K1.
- K2: `audit/tools/isolation.py` output is identical to the base output (`diff` empty). The 4 lines are `test_abstain_margin_002.py:20`, `test_tunable_reweight.py:23`, `:24`, `:25`; `violations: 4`.
- Deployed-layout import: `$PY -c "import sys; sys.path[:0]=['.','apps/ui']; from wired import diagnose"` → `import ok`.
- Anti-orphan: `NON_STARTER_NO_RULE_CODE` is read in `fault_atlas_router.py`. `_non_starter_gate`, `_PRUNE_REASON_FAMILY_GATE`, `_GATING_KEY_WILL_NOT_START`, `_NON_STARTER_NO_RULE_NAME` and `_NON_STARTER_NO_RULE_REMEDIATION` are each read in the shim apart from their definition. `"no_rule"` is produced by the router and read by `apps/ui/app.py:979`.
- `baseline.sh` and the repo-wide lab suites (dtclab, obdlab, gaslab, symptomlab, vinlab, dnalab): NOT RUN. The task marks them report-only and Cowork runs them at review. This row edits none of those labs.

Verdict: **CLEAN-WITH-FINDINGS**. Every in-scope gate passed. The red repo-wide counts have named pre-existing causes: the comlab 2 collection errors (R0-2) and the registry 5 `test_build_corpus.py` failures, both the same on the base (`## Baseline`).

## CODE REVIEW

Diff `cba05c1..208eca3` (7 files, +136/−20). I re-read each hunk.
1. Scope: every hunk traces to R1-R5, R7, K4 or R6. The v1 path, `_no_start_branch`, the GASLab cranking INVALID behaviour, the NS-004 DTC list and the `Vault/` copy are untouched. No drive-by refactor: the only restructure is the C2 per-branch enrichment locals, and its no-fault and winner outputs are byte-identical to the old ternaries (registry 502 and comlab 531 are unchanged).
2. Contracts: the new public constant carries `# consumer: fault_atlas_router.py route()`. The new prune constants carry consumer / wiki comments. No lab field is mapped into a payload.
3. Provenance: no new numeric boundary literal. The 0.0 confidence is R2's literal. The `[:280]` cap keeps its existing `# wiki:` citation.
4. Boundaries: the shim still imports no COMLab module. It reads the directive with `getattr` (R1). The router keeps the lazy import. No cross-lab import (isolation unchanged).
5. Tests: no network. The new file builds payloads with `_raw` and the corpus loader.
6. Craft (WARNING, none blocking): `_non_starter_gate` returns False for a dict-shaped `routing_directive`. No producer in the repo builds one (`lab_pipeline_aggregator.py:652`, `:676` pass the object), but a future serialiser would silently turn the gate off. This is recorded under remaining risks.

Findings: none blocking.

## Time

| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| plan | 2026-11-06T08:33:11Z | 2026-11-06T08:39:47Z | 6 | ABSENT (no context meter is exposed to this session) |
| implement (redispatch) | 2026-11-06T08:43:38Z | 2026-11-06T08:50:39Z | 7 | ABSENT (no context meter is exposed to this session) |
| revision 02 | 2026-11-06T08:53:24Z | 2026-11-06T08:54:54Z | 1 | ABSENT (no context meter is exposed to this session) |

## Revision 02

Task § R9 (spec commit `d6bdda5`). Only `apps/wired/tests/test_t_coma_1_non_starter_family_gate.py` changes:
- `test_running_session_is_not_gated` now asserts `(v.fault_family, v.fault_code) == ("ecu_fault", "EF-004")` and `not v.abstained`, in place of `!= "non_starter"`.
- `test_non_starter_dtc_rule_wins` also asserts `v.confidence_score == pytest.approx(0.85)`, `v.abstained is False` and `v.abstain_reason is None`.

Start: `fix/T-COMA-1` HEAD `d6bdda5`; porcelain held only the untracked note and RESULT. Commit: `2ba854b test(T-COMA-1): pin the running EF-004 verdict and the NS-004 score (R9)`, parent `d6bdda5`.

| step | command | expected | observed |
|---|---|---|---|
| 1 | `cd apps/wired && pytest -q -p no:cacheprovider tests/test_t_coma_1_non_starter_family_gate.py --basetemp=C:/4DApp/recheck/T-COMA-1/pt/r2new` | `14 passed` | `14 passed in 2.56s` |
| 2 (wired) | `cd apps/wired && pytest -q -p no:cacheprovider --basetemp=C:/4DApp/recheck/T-COMA-1/pt/r2wired` | `79 passed` | `79 passed in 5.20s` |
| 5 | `C:/4DApp/.venv-loop/Scripts/ruff.exe check <the 5 .py files>` | `All checks passed!` | `All checks passed!` |
| extra | pyright 1.1.410 on the test file | 0 errors | `0 errors, 0 warnings, 0 informations` |
| M1 | `_non_starter_gate` → `return False`, then `git restore` | `13 failed, 1 passed` | `13 failed, 1 passed`: the 12 `test_non_starter_without_a_matching_rule_abstains[…]` + `test_non_starter_dtc_rule_wins` |
| M2 / M3 | as in `## Mutants` | (not required by R9) | `12 failed, 2 passed` each, the same 12 tests as before |

After the mutants, `git diff --quiet` printed `restored` each time. `test_running_session_is_not_gated` passes under all three mutants. The new assertions pass on the fix, and they are pins of measured values, so they are not red-first tests. No production file changed in this revision.

Revision 02 time: | revision 02 | 2026-11-06T08:53:24Z | 2026-11-06T08:54:54Z | 1 | ABSENT (no context meter is exposed) |
