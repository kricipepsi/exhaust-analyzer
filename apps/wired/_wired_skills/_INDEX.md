# wired Skill Bundle — Master Index

**Version:** 1.0
**Last updated:** 2026-06-28
**Bundle root:** `/agent_workspace/apps/wired/_wired_skills/`

This index is the only place a coder session needs to look to know which skills
exist, which are mandatory at session start, and which to load on demand.
`WIRED_START_HERE.md` reads this file during bootstrap.

**Scope of `wired` (this pack):** compose the CURRENT labs into COMLab's full
pipeline and prove one end-to-end diagnosis — the **oil-burning case**. There is
**no UI** (the UI is not reworked) and **no multi-case CSV harness** — a
single-case CLI runner only. Tracing (OpenTelemetry/Jaeger) is in scope.

**Authoritative source documents (read narrow — cite, don't whole-read):**
- `labs/comlab/comlab/schemas/ingestion.py` — `OrchestratorInboundRequest` + payload mirrors (line 488; mirrors 151/165/289/324)
- `labs/comlab/comlab/schemas/response.py` — `OrchestratorFinalUIOutput` (line 132; the verdict)
- `labs/comlab/registry/integration_shim.py` — the live REG-V2 verdict path
- `planning/oil_consumption/PROGRESS.md` — pinned oil-case dossier numerics + the MW-00x map
- `ARCHIVE/wiredV2/wiredv2/composition.py` — the prior composition (reference to ADAPT, never import)

`wired/` is composition-only: it maps lab outputs into COMLab payloads and holds
no diagnostic logic. Every mapped field names its COMLab consumer.

---

## Mandatory at every session start
| # | Skill | Path | Purpose |
|---|---|---|---|
| 1 | wired-python | `_wired_skills/wired-python/SKILL.md` | House style + per-file Inner Loop (py_compile -> ruff -> pyright -> pytest -x -q) + composition-only forbidden patterns. |
| 2 | wired-verification-loop | `_wired_skills/wired-verification-loop/SKILL.md` | 6-phase outer gate; produces the `VERIFICATION GATE` block in `wired_tasks/progress_notes/<task-id>.md`. |
| 3 | wired-code-review | `_wired_skills/wired-code-review/SKILL.md` | Per-diff self-review (incl. structural-craft WARNING axis); produces the `CODE REVIEW` block. Both blocks clean before any task -> `done`. |

The workspace `CLAUDE.md` / `AGENTS.md` are read implicitly and carry
workspace-wide rules (the five rules, lab isolation, signal/noise).

---

## On-demand domain skills
Load only when the task surface matches the **Load when…** rule.

| Skill | Status | Path | Load when… |
|---|---|---|---|
| wired-composition-contract | BUILT | `_wired_skills/wired-composition-contract/SKILL.md` | Any task that builds or modifies the lab->COMLab payload mapping, the `diagnose()` entry point, or the single-case runner that reads its verdict. **Gates T-WIRE-1, T-WIRE-2, T-WIRE-3.** |
| wired-signal-pack | BUILT | `_wired_skills/wired-signal-pack/SKILL.md` | Any v3 Phase-4 signal-pack task (`T-V3-P4-C*-PRE/SYNTH/A/B`): reveal contract, provisional-synthetic policy, dry-run self-check + FT-8 audit, commit/yardstick-mint mechanics, baseline pinning. **Gates every C-pack task from C3 onward.** |

---

## On-demand verification skills
| Skill | Status | Path | Load when… |
|---|---|---|---|
| (none authored — OTel tracing gates only T-WIRE-3, so its rules are inlined in that task's Context per the anti-orphan-skill rule) | — | — | — |

---

## Hard constraints (recap)
- **Composition-only.** `wired/` is the sole point importing multiple labs. No
  lab imports another lab or `wired/`. No diagnostic logic here.
- **Signal/noise.** Every field mapped lab->COMLab payload names its existing
  COMLab consumer in a `# consumer:` comment. "Future use" is not a consumer.
- **The deferred fusion path is gone.** Do not import or reference it.
- **Petrol-only, Euro 1–5 scope** (COMLab's reworked scope, ~1990–2010).
- **Python 3.14 only** via `/agent_workspace/.venv-wired` (inherited from root).
- **No legacy imports.** Never import from `ARCHIVE/`, `v2/`, `v6/`.
- A task does not flip to `done` until **both** the `VERIFICATION GATE` and
  `CODE REVIEW` blocks are clean in `wired_tasks/progress_notes/<task-id>.md`.

---

## Maintenance
When a future phase reveals a new surface gating >= 3 tasks with a non-obvious
read-only invariant (e.g. a real CSV accuracy harness, or the UI field contract
once the UI is reworked), author a new on-demand skill, add a row above, and
reference it from each affected task's `Load skills:` line. Do not author orphan
skills (one skill, one task) — inline single-task rules into that task's
`### Context ###`. See `_skills/coding-bootstrap/reference/custom-skill-authoring.md`.
