# T-MIG-4 — Fork GASLab code into `labs/gaslab` (Phase 4 of the 4DLabV2 migration)

**Authored by:** architect · **Status:** `done` · **Blocked by:** — (Phases 0/3/5 done)
**Mode:** STRICT — both VERIFICATION GATE and CODE REVIEW blocks clean before `done`.
**Companion:** `MIGRATION_MANIFEST.md` (Phase 4 row) · `DECISIONS.md` (D1, D2, Q-A).

> This is a **coder** task: copy the live `gaslab` package into the v2 home, prove the suite is still
> green in isolation, repoint the editable install, then archive v1. It is a **pure relocation** — no
> diagnostic logic, schema field, enum, or threshold changes. Off-scope discoveries → Unplanned
> follow-ups table, **not** the diff.

---

## Blocker disposition (architect, 2026-06-05)

Coder implemented to the strict gate (ruff/pyright clean; **207 GAS green**; import resolves to the
fork; `test_composition.py` **48 passed**; content byte-identical to v1) and stopped before archive on
one external-consumer failure. **Ruling:**

- `TestSuite/gaslab_suite_runner.py` fails because it still passes **SAI fields**
  `secondary_air_injection_active` (→ `GasLabContext`, lines 113/120) and `secondary_air_equipped`
  (→ `GasLabDnaView`, lines 45/97) — **purged under T-GV2-11** (SAI now lives in DTCLab). Old **and**
  forked GASLab both lack them, so the runner has been broken **since the SAI purge** — pre-existing
  staleness surfaced by the move, **not caused by it**. Fixing it is a consumer-contract edit = **out of
  scope** here. Carved to **T-MIG-5**.
- The runner's *import* of `gaslab` resolves to the fork (the migration-relevant check); the binding
  consumer integration `test_composition.py` passes. **T-MIG-4 is UNBLOCKED** — proceed to step 6
  (archive v1) + step 7 (post-archive gate), then mark `done`.
- Copying `docs/wiki/{GAS_VOCABULARY,GAS_WIKI}.md` was a **required, correct** deviation — they are the
  **real** files (byte-identical), read by `tests/test_validators.py`. The spec's "exclude docs/" is
  amended: **include `docs/wiki/GAS_VOCABULARY.md` + `docs/wiki/GAS_WIKI.md`** (only these two).
- **Do not run graphify** (it was unavailable — fine; CLAUDE.md forbids re-running it; `graph.json` is
  canonical, re-aligns only via the instructed `T-GV2-KG` re-extraction). Drop that step.

## Objective

Make `labs/gaslab/` the **canonical** GASLab code (D1 fork-and-freeze, Q-A: v1 sunset), with
the full GASLab test suite green from the new location, and the live `gaslab` import repointed there so
the three external importers keep working. Then archive v1 `GASLab/`.

## Signal/noise

No schema field/enum/threshold is added or changed → the signal/noise gate is **trivially satisfied**
(nothing new ships). The task's job is to *preserve* every existing consumer relationship across the
move, not create one. If any step would require a code change beyond moving files + packaging, STOP and
flag it — that is out of scope.

## Pinned facts (do not re-derive)

- **Package import name stays `gaslab`.** Imports are already **absolute** (`from gaslab.contracts
  import …`) and `gaslab/__init__.py` already defines `__all__` (line 22). FolderStruct's
  absolute-imports / explicit-`__all__` requirements are therefore **already met** — **do not rewrite
  imports** and **do not rename the package**. Renaming would break the three external importers and
  every test for no benefit.
- **Source layout** (`GASLab/`): `gaslab/` package (incl. `gaslab/data/`), `tests/` (incl.
  `tests/fixtures/`, `tests/unit/`), `pyproject.toml` (name=`gaslab`, `packages.find include=["gaslab*"]`,
  `testpaths=["tests"]`). ~172 test functions; the ledger's green baseline is **207 GAS** (parametrized).
- **Copy these, exclude those.** Copy `gaslab/`, `tests/`, `pyproject.toml`. **Exclude**
  `gaslab.egg-info/`, every `__pycache__/`, `_gaslab_skills/`, `gaslab_tasks/`, `docs/`, the GASLab
  `*.md`, and `GASLab/graphify-out/` (not part of the package).
- **Three external importers of `gaslab`** (verified): `4DLabWired/wired/composition.py`,
  `TestSuite/gaslab_suite_runner.py`, `4DLabWired/_scratch/_p5_misfire_dump.py` (scratch). Because the
  import name is unchanged, these need **no source edits** — only the editable install must point at the
  new path before v1 is archived.

## Scope

**IN:** relocate the package + tests + pyproject to `labs/gaslab/`; prove green in the sandbox;
repoint the `gaslab` editable install; verify the 3 external importers; archive v1 `GASLab/`.
**OUT:** any rule/threshold/contract change; consumer *contract* reconciliation (that is Stage-4 / D2 —
`T-GV2-2`, `FU-1`, `FU-4`); touching COMLab/registry (they mirror types, they do not import `gaslab`);
bumping Python target in `pyproject.toml` (leave `py311` as-is unless a gate fails on it).

## Steps

1. **Read** the project skill `_skills/coding-bootstrap` and restore sandbox Python 3.14 (CLAUDE.md
   "Sandbox Python" block). Confirm `python3.14 --version`.
2. **Copy** into the existing `labs/gaslab/` (which already holds `README.md`):
   `gaslab/` (with `data/`), `tests/` (with `fixtures/`, `unit/`), `pyproject.toml`. Exclude the
   artefacts listed above. Result layout: `labs/gaslab/{gaslab/, tests/, pyproject.toml, README.md}`.
3. **Inner loop in the sandbox** from `labs/gaslab/`:
   `python3.14 -m pip install -e . --break-system-packages` → `ruff check .` → `pyright` →
   `pytest -x -q`. Target: **207 GAS green**, ruff/pyright clean. Run after the copy and after any fix.
4. **Repoint the editable install** so `import gaslab` resolves to the fork (this is the step that lets
   v1 be archived without breaking the 3 importers). In `.venv-wired` this is a **venv/uv action the
   owner runs in PowerShell**: `.venv-wired\Scripts\python -m pip install -e C:\Users\muto\claude\4DApp\4DLab\4DLabV2\labs\gaslab`
   (replaces the `GASLab/`-rooted editable). Surface this line to the owner; do not assume it ran.
5. **Verify the external importers** resolve `gaslab` to the new path. Binding check:
   `4DLabWired/tests/test_composition.py` **must pass** (done: 48). `TestSuite/gaslab_suite_runner.py`
   need only **import** from the fork — its downstream SAI failure is the pre-existing out-of-scope
   blocker (→ T-MIG-5), **not** a gate for this task. (`_p5_misfire_dump.py` is scratch — note only.)
6. **Archive v1** (Q-A): move `GASLab/` → `ARCHIVE/legacy_gaslab_v1/` (delete-permission already granted
   for the 4DLab folder). Add a one-line banner to `ARCHIVE/README.md`:
   "legacy_gaslab_v1 = retired v1 GASLab; canonical is labs/gaslab".
7. **Post-archive gate:** re-run step 3's `pytest` and step 5 once more with `GASLab/` gone, proving the
   fork is self-sufficient and the importers resolve to it.

## Success criteria

- `pytest -x -q` in `labs/gaslab/` = **207 GAS green**; `ruff`/`pyright` clean — **after** v1 is
  archived (step 7).
- `import gaslab` resolves to `labs/gaslab/gaslab/` (not the old path); `test_composition.py`
  passes; the suite runner imports from the fork (its SAI failure is carved to T-MIG-5, not a blocker).
- `GASLab/` no longer at repo root (now `ARCHIVE/legacy_gaslab_v1/`); no active code imports the old path.
- No diagnostic-logic diff: `git diff` of `gaslab/*.py` content vs the v1 copy = identical (only location
  changed). Confirm with a content diff in the verification block.

## Inner loop (run after every meaningful edit)
```
cd labs/gaslab
python3.14 -m pip install -e . --break-system-packages
ruff check . && pyright && pytest -x -q
```

## VERIFICATION GATE — T-MIG-4
Phase 1 (syntax/lint): PASS - `python3.14 -m ruff check .` from `labs/gaslab` reported all checks passed.
Phase 2 (type check): PASS - `python3.14 -m pyright` from `labs/gaslab` reported 0 errors, 0 warnings, 0 informations.
Phase 3 (unit tests): PASS - `python3.14 -m pytest -x -q` from `labs/gaslab` reported 207 passed after `GASLab/` was archived.
Phase 4 (import resolution): PASS - `.venv-wired\Scripts\python.exe -c "import sys, pathlib; sys.path.insert(0, 'TestSuite'); import gaslab_suite_runner; import gaslab; print(pathlib.Path(gaslab.__file__).resolve())"` resolved to `4DLabV2\labs\gaslab\gaslab\__init__.py`.
Phase 5 (external importer): PASS - `.venv-wired\Scripts\python.exe -m pytest 4DLabWired\tests\test_composition.py -q` reported 48 passed, 2 pre-existing unknown-mark warnings.
Phase 6 (content/diff review): PASS - archived v1 `gaslab/` and forked `labs/gaslab/gaslab/` are content-identical for `.py`, `.yaml`, and `.gitkeep` files; changes are relocation plus the required two wiki fixture docs and archive banner.

Notes:
- `TestSuite/gaslab_suite_runner.py` import-only check passes and resolves to the fork. Its full CSV-runner SAI staleness is carved to T-MIG-5 and is not a T-MIG-4 gate.
- Graphify was not run per the blocker-disposition ruling above.

## CODE REVIEW — T-MIG-4
1. No logic/contract change: PASS - forked `gaslab/` code content is byte-identical to archived v1.
2. Scope compliance: PASS - changes are relocation, minimal wiki fixture copy required by tests, archive move, archive banner, and progress/task notes.
3. Import name preserved: PASS - package remains `gaslab`; no imports were rewritten.
4. External importers verified: PASS - `.venv-wired` resolves `gaslab` to the fork; `test_composition.py` passed; suite runner imports from the fork.
5. v1 archived: PASS - `GASLab/` is gone from repo root and exists at `ARCHIVE/legacy_gaslab_v1/`.
6. No cross-lab import introduced: PASS - no `gaslab/*.py` content changed.
7. Suite green post-archive: PASS - fork-local `pytest -x -q` reported 207 passed with `GASLab/` gone.

## Risks
- **R-A Two `gaslab` packages installed at once** (old + fork) → import ambiguity. Mitigate: repoint the
  editable install (step 4) and archive v1 (step 6) before the final gate (step 7).
- **R-B Importer breakage** if the package were renamed. Mitigate: name stays `gaslab` (do not rename).
- **R-C `mv GASLab` blocked / file lock** (as seen with the empty `GASLabV2/` husk). Mitigate: close
  editors holding GASLab files; delete-permission is enabled; copy→verify→remove if `mv` fails.
- **R-D `gaslab/data/` omitted** → ontology load fails at import/test. Mitigate: explicitly copy `data/`.

## Deliverables
`labs/gaslab/{gaslab/, tests/, pyproject.toml}`; `ARCHIVE/legacy_gaslab_v1/` (former `GASLab/`);
`ARCHIVE/README.md` banner; this task's progress note `…/tasks/progress_notes/T-MIG-4.md`.

## Commit (owner runs in PowerShell, explicit paths)
```powershell
cd C:\Users\muto\claude\4DApp\4DLab
git add `
  labs/gaslab/ `
  ARCHIVE/ `
  GASLab/ `
  planning/sprints/stage1_gaslab/tasks/T-MIG-4_gaslab_code_fork.md `
  planning/sprints/stage1_gaslab/tasks/progress_notes/T-MIG-4.md
git commit -m "T-MIG-4: fork GASLab -> labs/gaslab (Phase 4), archive v1 GASLab"
```
