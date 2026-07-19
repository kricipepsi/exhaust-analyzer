# T-RVAULT-6 — progress note

**Status:** `done` · **Pack:** VAULT (Registry) · completed 2026-06-28
Task spec: `labs/comlab/registry/docs/registry_tasks/T-RVAULT-6_vault_build.md` · Ledger: `labs/comlab/registry/docs/REGISTRY_PROGRESS.md`

## Plan

Build the registry vault corpus under `Vault/labs/comlab/registry/`:
- author `_skills/graph/4dlab-vault/assets/vault-map.registry.yaml` with non-empty hand-authored consumers for 53 doc-prepped registry notes;
- add the keyed `registry` corpus to `build_lab_vault.py` with `src_root=labs/comlab/registry`, `vault_dest=labs/comlab/registry`, and required graph tiers `v2_code`, `v2_tests`, `v2_docs`;
- dry-run, build, verify idempotency, verify Bases/frontmatter resolution.

---

## VERIFICATION GATE — T-RVAULT-6

| Phase | Check | Result | Detail |
|---|---|---|---|
| 1 | ruff lint + JSON parse | PASS | `ruff check _skills/graph/4dlab-vault/scripts/build_lab_vault.py` OK; 34 registry JSON files parsed (source + Vault copies). |
| 2 | pyright | PASS | `pyright --pythonpath /agent_workspace/.venv-wired/bin/python _skills/graph/4dlab-vault/scripts/build_lab_vault.py` OK / 0 errors. |
| 3 | unit tests | PASS | `pytest labs/comlab/registry/tests/ -x -q` = 494 passed; `pytest _skills/graph/4dlab-vault/tests/test_build_lab_vault.py -q` = 3 passed. |
| 4 | task verification | PASS | Map present; dry-run resolves `registry`; real build writes `Vault/labs/comlab/registry/{code,tests,docs}`; post-build idempotency command prints `idempotent`; required tiers present. |
| 5a | rule schema validity | PASS | Registry suite loaded/validated all 16 rulesets against `schema_v2.py`; no rule JSON changed. |
| 5b | case-ID resolution | PASS | Registry suite's per-family case-resolution tests passed; 0 orphan refs reported. |
| 5c | harness side-by-side | N/A | Vault-build task only; no routing or registry-rule behavior changed. |
| 6 | scope check | PASS | Touched only the vault map, vault build config, generated `Vault/labs/comlab/registry/**`, `Vault/System-Map.md`, `Vault/_meta/PROVENANCE.md`, and this task progress/ledger row. No graph rebuilds; no vocabulary build. |

**Overall: PASS**

### Vault/Bases check

- `vault_query.py --vault Vault consumers --missing` returned no missing framed-note consumers.
- Targeted registry frontmatter check: 53 registry framed notes; 0 missing consumers; 0 missing drift guards for implemented targets; 0 unresolved `implements`/`drift_guards` paths; all three required Bases (`modules.base`, `consumers.base`, `drift-guards.base`) present.
- Full `vault_query.py --vault Vault health` currently FAILS on unrelated pre-existing task-note consumers: `T-UI-VAULT`, `T-UI-VAULT-SUPPORT-1`. Registry signal/noise row is PASS (`148/148 framed notes name a consumer` after this build). This is not a registry blocker.

---

## CODE REVIEW — T-RVAULT-6

| Section | Item | Result | Note |
|---|---|---|---|
| A | No lab / COMLab / 4DLabWired imports | PASS | Vault tooling/map only; no new lab/app Python imports. Consumer strings name COMLab readers but do not import them. |
| A | No ARCHIVE / v2 / v6 imports | PASS | Search found no forbidden archive/v2/v6 imports or paths in changed script/map. |
| A | Rules-as-data discipline | PASS | Registry rules remain JSON; task only mirrors existing artefacts into Vault and injects frontmatter. |
| A | No diagnostic logic in Python escape hatches | N/A | No diagnostic logic changed. |
| B | Every rule has passes_cases list | N/A | No rule files changed; registry suite still passes. |
| B | Every passes_cases ID resolves in corpus_curated.csv | N/A | No rule files changed; registry suite case-resolution tests still pass. |
| B | Every numeric threshold has wiki citation | N/A | No rule thresholds changed. |
| B | No invented enum values | N/A | No registry schema/enums/rules changed. |
| B | No solo-survivor rules (≥2 competing rules per family) | N/A | No rule files changed. |
| C | All lines trace to Deliverables | PASS | Script change is the keyed `registry` corpus config/support; map, generated vault files, System-Map, and provenance are explicit deliverables. |
| C | No scope creep | PASS | Did not rebuild graphs, did not run `--vocab`, did not copy tasks or `_registry_skills` into the vault. |
| D | Public functions have tests | PASS | `copy_entries` is covered through the `registry` dry-run/build task verification; existing `test_build_lab_vault.py` remains green. |
| D | Every changed rule covered by ≥1 passing case | N/A | No rule files changed. |

**Blocking findings:** none

**Follow-up rows added to REGISTRY_PROGRESS.md:** none
