# Pre-COMLab audit — 2026-06-16

**Scope:** every issue found in the labs before the COMLab (Stage 4) rework, per
`HANDOFF_2026-06-16.md`. **Coverage-first** — every finding listed, including low-severity
and low-confidence ones; a downstream pass should filter/rank. **Confidence** = how sure the
finding is real. **Severity** = impact if real.

**Method:** gates run with the repo's own toolchain — `ruff 0.15.17` (matches the repo's
`.ruff_cache`), `pyright 1.1.410`, `pytest` on **Python 3.14** via the existing `.sandbox-py`
interpreter (the labs require `>=3.11`). Labs editable-installed. Working tree cross-checked
against committed `HEAD` blobs, plus a repo-wide `py_compile` scan (834 `.py` files).

## Bottom line

The three emitter labs are **genuinely green** — re-verified this session:

| Lab | ruff | pyright | pytest |
|-----|------|---------|--------|
| GASLab | clean | 0/0/0 | **208 passed**, 2 skipped |
| OBDLab | clean | 0/0/0 | **388 passed**, 2 skipped |
| DTCLab | clean | 0/0/0 | **590 passed** |

No critical or high-severity defects survived verification. The remaining findings are
minor, mostly known, or environmental. **COMLab is not yet reworked (expected).**

---

## ⚠️ Methodology note — a stale-mount episode (read before trusting any transient)

Early in the audit the build sandbox reported **alarming, high-severity signals that proved
to be false** once the mount caught up. Documented here so they're not re-raised as real and
so a future session recognizes the pattern:

- **Apparent DTCLab corruption** — 4 files (`vocabulary.py`, `mode06_evaluator.py`,
  `freeze_frame.py`, `freeze_frame_extractor.py`) read as **truncated mid-line**; `import dtclab`
  failed; gates errored. On re-read minutes later the files were **complete**, matched `HEAD`,
  and the full gate passed (590 tests). The sandbox mount had been serving partially-synced copies.
- **Apparent corrupt git index** — `git status` failed with `index file corrupt`. After the
  mount synced, `git status` works normally.
- **Apparent missing author identity** — `git config` read empty; it now reads
  `4DLab automation <bot@4dlab.local>`.

All three were **sandbox-mount sync artifacts, not repo defects** — verified by re-running
after the mount settled. If you see truncated files or a corrupt index in a fresh session,
re-read after a few seconds before acting. (This is the kind of transient the audit was meant
to surface either way, hence it's recorded rather than dropped.)

---

## Findings (verified real)

| ID | Finding | Confidence | Severity |
|----|---------|-----------|----------|
| **F-01** | **COMLab hard-depends on an out-of-tree `registry` package + the split-registry is still unreconciled.** `tests/unit/test_fault_atlas_router_v2.py::{test_v1_when_explicit_false,test_v2_when_explicit_true}` fail with `ModuleNotFoundError: No module named 'registry'` (they patch `registry.integration_shim.route_case_with_diagnostics`). No `registry/` dir exists in `C:\Workspace` — it lives in the parent 4DLab root, so these likely pass in the full env. But COMLab's Stage-4 rework lists "consolidate the two split registries" as a deliverable, and the dependency is real and external. Verify resolution in the real venv before Stage 4. *(345 passed / 12 skipped / 2 failed in isolation; other skips are missing `opentelemetry`/`jsonschema` sandbox deps and intentional harness skips.)* | **High** the dependency is out-of-tree; **Medium** it's a real failing test vs env gap | **Medium** |
| **F-02** | **Almost the entire workspace is uncommitted.** `HEAD` tracks only **12 files, all in `labs/dtclab/`**; `git status` shows **87 untracked entries** — all of GASLab, OBDLab, COMLab, every root doc, and the other labs. This follows the "commit by explicit path" rule, but it means the "green" emitter labs (Stages 1–3) have **no committed baseline** to revert to if the Stage-4 COMLab rework disturbs shared files. Consider a checkpoint commit of the settled emitters before starting. | **High** | **Medium** (by-design, but a real safety gap) |
| **F-03** | **Un-ignored clutter.** `.sandbox-py/` (local 3.14 interpreter) and `labs/vinlab/mysql_data/` (a live MySQL data dir incl. `#innodb_redo`) are **not** in `.gitignore` — both appear in `git status` untracked and would be swept up by a careless `git add -A`. Stray harness leftovers at repo root: `success.log` ("AGENT EXECUTION SUCCESSFUL…") and `task.sh`. | **High** | **Low** |
| **F-04** | Root `ROADMAP.md` stale — OBDLab row (L28) still reads `T-OBDV2-0 pending` and the stage table shows OBDLab/DTCLab not-done, though both are complete. Handoff already says "trust per-lab ledgers." | **High** | **Low** |
| **F-05** | `labs/dtclab/README.md` L11 still reads `Status: scaffold placeholder` though the lab is built + green. | **High** | **Low** |
| **F-06** | `dtclab/core/routing_tag_mapper.py:7` docstring says "17 tags" while the surface is 18 (`schemas/vocabulary.py:19` and `family_map.py:3` already say 18). Owned by unstarted `T-DTC-COMMENT-FIX`. | **Medium** | **Low** |
| **F-07** | OBDLab `pytest` emits a `PytestRemovedIn10Warning` — a class-scoped fixture defined as an instance method in `tests/regression/test_obdlab_regression.py`. Passes today; breaks under pytest 10. | **High** | **Low** |
| **F-08** | **DNALab's `pyright` gate is not clean** — 5 errors in `models.py`/`assembly.py`, all from the *sanctioned* `dnalab → vinlab + symptomlab` imports being unresolvable to the type-checker (`Import "vinlab.models"/"symptomlab.models" could not be resolved`; `resolve`/`decode` "unknown import symbol"). Runtime is fine (27 tests pass), so this is type-checker-only — but it means DNALab can't show 0/0/0 like the emitter labs. Likely a missing `py.typed` / `__all__` export marker on vinlab + symptomlab, or an accepted cross-lab-typing gap. | **Medium** | **Low** |

## Findings (checked and already resolved / not reproduced)

| ID | Finding | Confidence | Severity |
|----|---------|-----------|----------|
| **R-01** | Handoff's "first repair task" — the `ln`-corrupted forward-reg IDs in `comlab/tasks/PROGRESS.md` + `config/proposals/{proposals,entries}.yaml` — **could not be reproduced.** IDs are correct (`EP-DTC-NOSTART-1`, `T-COMV2-NOSTART-1`, `T-DTCV2-NOSTART-1`), and the producer ref `mode06_evaluator.py:evaluate_monitor` matches the real function. Looks already fixed; close the item. | **High** | **Info** |
| **R-02** | Handoff's open git item — **no author identity** — now reads `4DLab automation <bot@4dlab.local>`. Verify it's the intended identity; otherwise resolved. | **High** | **Info** |

---

## Verified green (exercised and clean)

- **GASLab / OBDLab / DTCLab** — full gate per the table above; DTCLab `import` + 590 tests OK.
- **VINLab** — `ruff` clean · `pyright` 0/0/0 · `pytest` **184 passed, 8 skipped**.
- **SymptomLab** — `ruff` clean · `pyright` 0/0/0 · `pytest` **63 passed**.
- **DNALab** — `ruff` clean · `pytest` **27 passed** (pyright: see F-08).
- **COMLab** — `ruff` clean (tests: F-01). **semantic** — `ruff` clean (no Python package).
- **Cross-lab-import rule** — repo-wide check clean: the *only* cross-lab imports are
  `dnalab → vinlab + symptomlab`, which is the explicitly sanctioned direction
  (`DNA_TASKS_START_HERE.md:14`). GASLab/OBDLab/DTCLab/COMLab import no sibling lab.
- **Repo-wide `py_compile`** (834 files) — only the 6 *intentional* skill-eval fixtures under
  `planning/skill_eval/trials/` (e.g. `task_05_bug_fix`) fail; no production code does.
- **Contract chain (DTCLab → COMLab no-start)** — `ff_fuel_spark_cut_at_crank` is computed in
  the extractor **and** declared on `FreezeFrameRecord` (L95); `MONITOR_ABORTED` is emitted;
  `comlab/comlab/core/fault_atlas_router.py` exists; the COMLab readers (`T-COMV2-*`) are
  forward-registered and correctly still `pending (S4)`. The documented "emit-S2 / consume-S4"
  orphans (`ve_pct`, `per_bank_trim_delta`, `lambda_perception_delta`, …) are expected
  divergence, not silent orphans.

## Not exhaustively audited (coverage caveats)

- **Numeric-literal `# wiki: §…` rule** — spot-checked (present where sampled), not verified
  across every literal in every lab.
- **`semantic` lab** — 2 ledger tasks remain open (`T-SEM-4`/`T-SEM-5`, authored not done);
  likely intentional for a supporting lab.
- The **stale-mount episode** means any single sandbox reading should be re-confirmed; the
  green results above were each observed after the mount had settled.
