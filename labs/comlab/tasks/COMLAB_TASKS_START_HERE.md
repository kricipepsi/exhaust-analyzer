# COMLab v2 — TASKS START HERE

Read this first, every session, before any other action. (Paste this file as message 1 of a fresh coder session.)

## 0. Do NOT run graphify (the recurring failure)

**No COMLab task touches the knowledge graph.** The graph is a frozen, verified artefact — never rebuilt here.

- **Forbidden:** `graphify`, `graphify update .`, `Skill(graphify)`, or any self-added "refresh the KG / keep the graph current" step. None are in any COMLab task spec.
- If you catch yourself about to run one: **STOP.** It is not part of the task.
- The coding-bootstrap KG pre-step resolves to **SKIP** for this lab.
- A build runs *only* inside a dedicated KG-lane task (`T-PREP-*`/`T-KG-*`) whose own Deliverables name `graph.json`. No COMLab task here is one.

## 1. Start sequence

1. Read this file.
2. Read `PROGRESS.md` — the Task log table is the source of truth. Run the **stale-ledger guard**: if a `done` row lacks a clean `progress_notes/<id>.md` — a **plan-at-top block** (headed `## Plan` *or* `## Scope Confirm` *or* `## Plan / Scope Confirm` — these are equivalent) **plus** the `VERIFICATION GATE` and `CODE REVIEW` blocks — or its deliverable is absent, or a `pending` row already has clean gates — **stop and surface it**, don't silently fix. (A differently-worded plan heading alone is **not** a real gap; if both gate blocks are present and the opening section is the confirmed plan/scope, the row is clean — the architect normalises the heading, the coder does not.)
3. **Python 3.14 ONLY.** Run every `python`/`pytest`/`pip` via the repo sandbox interpreter `.sandbox-py/bin/python3.14` (3.14.5). **Never** system `python3` (3.10 → `StrEnum` ImportError) or any 3.11/3.12/3.13 — no mixing. From `labs/comlab`: `PY=../../.sandbox-py/bin/python3.14`. If a stale read-only `__pycache__/*.pyc` shadows an edit, purge `__pycache__` before re-running.
4. Load the language + verification-loop + code-review skills (workspace `CLAUDE.md` inner loop). KG pre-step → SKIP (§0).
5. **Pick the task the ledger picks:** the first `pending` row whose Blocked-by are all `done`. Not a later one, not one you were handed. One task per session.
6. Post a one-paragraph scope confirm (field · guard · signal/noise consumer · files) before writing code, then **proceed** — don't idle for confirmation. Stop only for a *critical* ambiguity: no nameable consumer for a new field/enum, an unresolved files/scope question, or a cited literal/section that doesn't exist.

## 2. Non-negotiables

- **Fusion spine, built LAST:** COMLab consumes the four upstream labs' **verdicts** (`schemas/ingestion.py::OrchestratorInboundRequest`), not raw sensors. Its test harness therefore has **no master-row projection script** — full-chain master-row eval is the wired gate `apps/wired/harness/` (T-TH-12); do not duplicate it. The harness descriptor is **categorical** (`boxes={}`).
- **Harness scope (T-COMTST pack):** characterization + regression net only — no-crash + schema-valid + fail-closed + golden-master pins. **Accuracy/scoring is out of scope**, deferred behind Phase-0 **F1** (registry consolidation) + **GATE_DATA** per `wiki/12_corpus_eval_discipline.md`.
- **Signal/noise:** every new field/enum/fault needs a named existing consumer in COMLab analytics or fault-atlas routing — or a proposal shipping its consumer in the same change (`comlab/config/proposals/`). "Future use" is not a consumer.
- **No cross-lab Python imports** (mirror types locally). **Numeric literals carry a wiki cite** (`# wiki: §…`). Reports in `.md` only; archive, never delete.
- **Inner loop after every meaningful edit:** `ruff check .` → `pyright comlab/` → `"$PY" -m pytest -x -q`.
- **Folder convention:** `wiki/` is reserved for the lab wiki only; vocabulary/contract docs live in `docs/Vocabulary/`, design docs in `docs/`.

## 3. Done means

Both `VERIFICATION GATE` + `CODE REVIEW` blocks clean in `progress_notes/<id>.md` **and** any field the task contracted to consume is grep-confirmed read in a live path. Green pytest alone is not done. Flip the ledger row to `done`, then **STOP**. Git: owner commits by explicit path; never stage `graphify-out/`, `*.egg-info/`, or `__pycache__/`.
