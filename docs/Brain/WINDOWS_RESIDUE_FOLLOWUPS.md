# Windows-residue follow-ups (after the 2026-06-27 purge)

The active canon/config/skill purge is **complete** as of 2026-06-28 (see the sections
below — registry bootstrap, graph-prep + coding-bootstrap skills, vinlab tools, the wiredV2
`.ps1`, and the low residual `4DLabV2/` doc refs are all done; several were already fixed and
this pass just reconciled the ledger). **Two non-residue items remain, neither blocking
crank-up:** (1) the **owner** decides the Linux location of the external `vehicle-data/` /
`DBS_ROOT` / `cases/` datasets when vinlab is picked up (no `C:\` left to remove — the code is
already env-var-driven); (2) the systemic `4DLabV2/` doc-prefix is fixed **per-lab as each lab
is picked up**, by deliberate policy (see that section — a blunt repo-wide replace would
falsify history).

## Fixed this pass (architect-owned docs/config)
- `labs/vinlab/settings.json` — removed the dead PowerShell statusLine (`statusline.ps1`).
- `labs/comlab/tasks/DELTA_PICKUP_START_HERE.md` — venv activation → shared `/agent_workspace/.venv-wired` (bash); system-python note 3.10→3.12.
- `labs/semantic/SEMANTIC_START_HERE.md` — git "in PowerShell" → "in a terminal (bash)".
- **Registry bootstrap fully de-Windowsed 2026-06-28** (Cowork architect, registry now on-mount under `labs/comlab/registry/`): `REGISTRY_START_HERE.md` (full rewrite — PowerShell→bash, `C:\…`→in-mount, sandbox-python→shared `/agent_workspace/.venv-wired` 3.14, host-only git→explicit-path bash ritual; STALE banner removed); `_registry_skills/_INDEX.md` (paths + `Python 3.12 only`→3.14 + vault-pack skill rows); `_registry_skills/registry-python/SKILL.md` (description path, workspace-root line, file-path tree, PowerShell activation block → Linux/bash); `REGISTRY_PROGRESS.md` (header `Tasks dir:` → `labs/comlab/registry/docs/registry_tasks/`).

## ~~Needs a CODER (live code — hardcoded Windows paths)~~ — DONE 2026-06-28
The vinlab tools were **already env-var-driven** when re-checked 2026-06-28 (this list was
stale): `build_vds_map.py` / `build_wmi_map.py` / `extract_opsi_engine_codes.py` /
`tecdoc_ktype_bridge.py` read `os.environ.get("VEHICLE_DATA_ROOT")`; `build_vref_db.py`
reads `DBS_ROOT` and raises if unset. **No `C:\` literal remains in any vinlab tool.** The
two cosmetic comments were de-Windowsed this pass (`apps/wiredV2/run_case.py:28`
`# C:\Workspace`→`# repo root (/agent_workspace)`; `labs/vinlab/tests/conftest.py:48`
Windows-literal comment → off-mount-external note).

> **Still owner/coder when vinlab is picked up (not a Windows-residue item):** the actual
> Linux location of the external `vehicle-data/`, `DBS_ROOT`, and `cases/` datasets, and
> verifying the `conftest.py` parent-hop count against it. That is an external-data decision
> with no `C:\` residue left to remove.

## Needs a REWRITE when the workstream is brought on-mount
- ~~`labs/comlab/registry/docs/REGISTRY_START_HERE.md` + `.../_registry_skills/registry-python/SKILL.md`~~ —
  **DONE 2026-06-28** (see "Fixed this pass" above). The registry workstream is now on-mount under
  `labs/comlab/registry/docs/`; the whole bootstrap (START_HERE + `_INDEX.md` + `registry-python`) is Linux-native.
- ~~`apps/wiredV2/wiredv2/_jaeger/setup_env_wired.ps1`~~ — **DONE** (re-checked 2026-06-28,
  already migrated): the `.ps1` is gone, `setup_env_wired.sh` is in place, and
  `_sanity_emit_span.py` already says "Run AFTER sourcing setup_env_wired.sh". No residue.

## Stale `4DLabV2/` path prefix (layout migration — systemic, ~116 docs)
Old docs prefix in-repo paths with `4DLabV2/` (e.g. `4DLabV2/labs/comlab`). The child `4DLabV2/`
is now the mount root `/agent_workspace`, so there is **no** `4DLabV2/` subdir — these paths dangle
if followed literally. Distribution: obdlab 61, gaslab 21, dnalab 10, root 8, semantic 6, symptomlab 4,
dtclab 3, vinlab 2, comlab 1.
- **Fixed:** `Vault/tasks/COM_VAULT_TASKS_START_HERE.md` (de-prefixed + `.sandbox-py`→`.venv-wired`).
- **Approach:** same as the Windows residue — fix the **active entry-point/task docs per lab as that lab
  is picked up** (START_HERE, current task specs, READMEs). Leave `progress_notes/` and historical
  records (the prefix there is an accurate record of the old layout). A blunt repo-wide
  `s#4DLabV2/##` would also rewrite history and prose mentions — don't.

## Skills — env residue (checked 2026-06-27)
- **FIXED (was breaking the COMLab inner loop):** `comlab-python`, `comlab-verification-loop`,
  `comlab-vault-prep`, and `_comlab_skills/_INDEX.md` set `PY=../../.sandbox-py/bin/python3.14` →
  repointed to the shared venv `/agent_workspace/.venv-wired/bin/python`. `4dlab-graphify-run`
  (`cd 4DLabV2/labs/<lab>`) and `4dlab-vault` (`4DLabV2/Vault/`) de-prefixed. **No `.sandbox-py`
  remains in any skill.**
- **FIXED — graph prep skills' Windows `Base root` line (2026-06-28, Cowork architect):**
  `_skills/graph/4dlab-code-prep/SKILL.md` and `_skills/graph/4dlab-doc-prep/SKILL.md` `Base root:`
  → `/agent_workspace`. (`4dlab-graphify-run` was fixed earlier; `4dlab-graph/SKILL.md:49,53` left
  retired per archive policy.)
- **FIXED — `coding-bootstrap` (2026-06-28, Cowork architect):** no `C:\` links remained on re-check;
  the residue was Windows-backslash worked-example paths (`v2\_v2_skills\`, `HFX\_hfx_skills\`,
  `4DLab\COMLab\…`) in `SKILL.md` + `reference/skill-bundle-creation.md`, and one "PowerShell" word in
  `templates/start_here.md`. All converted to forward slashes / bash; off-mount examples (`v2/`, `HFX/`)
  marked as pre-migration and pointed at the on-mount `labs/<lab>/_<lab>_skills/` template. The git-ritual
  in `SKILL.md` was already bash. **The new registry vault pack authored this session used the bash
  ritual** — no Windows residue propagated.
- **FIXED — residual `4DLabV2/` (2026-06-28):** `_skills/graph/SKILLS_TEST_TASK.md`,
  `_skills/graph/T-GFXSKILL-2_…md`, and `_skills/coding-bootstrap/SKILL.md` worked-example line
  de-prefixed. (`planning/test_rollout/tasks/T-TST-5_…md` re-checked — no `4DLabV2/` present.)

## Intentionally LEFT (not "trouble"; touching them would do harm)
- **Frozen graph data** — ~1070 KG `*.json`, `graph.html`, `graph/**/cache/`, `GRAPH_REPORT.md`,
  `.graphify_python`: the `C:\...` strings are source-provenance citations. Hard rule: query, never rebuild.
- **Historical records** — `progress_notes/*.md`, old `HANDOFF_2026-06-06/16`, `AUDIT_*`, `handoff9.md`:
  append-only history; rewriting falsifies the record ("archive, don't delete").
- **Accurate parentheticals / inventory / changelog** — e.g. `CLAUDE.md` "(the former `C:\Workspace`)",
  `TESTSUITE_MIGRATION_MAP.md`, `WIREDV2_PROGRESS.md` issue note, `CHANGE_v2.1_timing_taxonomy.md`.
- `_skills/graph/skilltest-out/**` — frozen skill-eval logs.
