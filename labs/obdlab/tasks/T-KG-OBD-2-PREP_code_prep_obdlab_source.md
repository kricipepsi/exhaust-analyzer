# T-KG-OBD-2-PREP — Code-prep `obdlab/obdlab` source for the code-map ingest

**Status:** `pending` · **Lab:** OBDLab (Stage 2) · **Mode:** STRICT
**Workstream:** graphify-skills rollout, **step 3** (build skills → eval skills (`T-GFXSKILL-2`) →
**apply `4dlab-code-prep` to real source** ← *this task* → ingest `T-KG-OBD-2`).
**Blocks:** `T-KG-OBD-2` (the code-map ingest must run against the prepped, then-frozen source).
**Soft prerequisite (advisory, not a ledger blocker):** `T-GFXSKILL-2` validates `4dlab-code-prep`
before the coder trusts it on real source. The skill's own `probe` (Step 1) also self-validates
docstring/enum behaviour, so this task is *runnable* without `T-GFXSKILL-2`; running the eval first
is the recommended hardening, not a hard gate (`T-GFXSKILL-2` is a tooling task, not an OBDLab row).

## Why this task exists

`T-KG-OBD-2` builds the OBDLab **code map** purely from what tree-sitter sees statically in the
source (graphify Pass 1; Pass 3 is skipped for a code-only corpus). The map's node/edge quality is
therefore decided **before** ingestion, by source legibility — not by any prompt or model. This task
applies the `4dlab-code-prep` skill (`probe` → `audit` → fix) so the imminent ingest captures the
intended symbols and edges instead of dropping them.

Full rule-to-mechanism evidence: `labs/obdlab/GRAPHIFY_CODE_INGESTION_FORMATTING.md`.

## Signal/noise — why the field-rule does not bite, and what *does*

This task **adds no schema field and emits no channel** — it only makes existing source legible to
the AST pass. So the field-level signal/noise rule ("every new field needs a named consumer") does
not apply, exactly as framed for `T-KG-OBD-2` (a code-map artefact, not a schema field).

The discipline that **does** apply is per-edit: **every source edit must map to a named graphify
Pass-1 consumer** from `GRAPHIFY_CODE_INGESTION_FORMATTING.md` §3, or it is churn and must not ship.
The named consumers are:

| Rule | Edit | Named graphify consumer |
|---|---|---|
| **I** | replace `from x import *` with explicit names | the `imports`/`calls` edge set (star imports give tree-sitter no names → edges lost/ambiguous) |
| **A** | add `__all__` to package `__init__.py` | god-node ranking + package entry-point nodes |
| **T** | annotate public signatures / schema attrs | type-reference edges (field ↔ vocabulary type node) |
| **C** | surface dynamic dispatch hiding call sites | the call graph (advisory — do not force-remove legitimate indirection) |
| **S** | name runtime-built symbols the team queries | node set + spot-check (runtime symbols never appear) |
| **E** | domain states → explicit `Enum`/`StrEnum` | enum-member sub-nodes — **only if `probe` Q1 = yes** |
| **R** | `# WHY:`/`# NOTE:`/`# HACK:` on non-obvious gates/equations | `rationale` nodes linked to the owning symbol — **only if `probe` Q2 = yes** |
| **D** | parameter-naming docstrings on formula/validation methods | `rationale` node attached to the method — **only if `probe` Q3 = yes** |

If a candidate edit cannot be tied to one of these rows, it does not ship (the workspace
"touch only what you must" rule).

## Scope

- **Target:** the production package `obdlab/obdlab/` (`core/`, `schemas/`) only. **Exclude**
  `tests/` (separate test-map graph, `T-KG-OBD-3`) and `research/` (wiki KG input, `T-KG-OBD-1`).
- **Run `4dlab-code-prep`** in order: `probe` → `audit` → (apply fixes) → `report` checklist.
- **`probe` answers are ALREADY KNOWN for graphify v0.8.13** (resolved 2026-06-09 by `T-GFXSKILL-2`;
  enum-member node behaviour is a property of the build, not the package, so it transfers):
  1. enum member sub-node? → **NO** ⇒ rule **E** is **DROPPED** (no consumer, no work).
  2. `# WHY:` → `rationale` node? → **YES** ⇒ rule **R** is **KEPT**.
  3. docstring → `rationale` node? → **YES** ⇒ rule **D** is **KEPT**.
  So this task ships **I/A/T/C/S + R + D**, and drops only **E**. (An earlier graphify-unavailable
  session conservatively dropped all of E/R/D — that is now superseded: R and D produce real nodes.)
  **Re-run the `/tmp/gfx_probe/` sample (scoped to `/tmp` ONLY) only to confirm the graphify
  extraction-engine/package is still `0.8.13`**; if it changed, re-derive all three answers and
  adjust scope. NB: the CLI banner reports a separate skill-text version (`0.8.36`) — that is *not*
  the gate; only the **engine/package `0.8.13`** governs the verdict (confirmed in `T-GFXSKILL-2`
  iteration-2 on Codex). `I/A/T/C/S` never need a probe.
- **`audit obdlab/obdlab`.** Emit the fix plan as `file:line | rule | found | fix`, grouped by rule,
  with per-rule counts. The skill does **not** edit source — the coder applies fixes with judgement.
- **Apply fixes** that map to a consumer above. Highest payoff first: rule **I** (kill any
  `from x import *`), then **A** (`__all__` on each package `__init__.py`), then **T**. `E/R/D` only
  for rules the probe kept. Keep the diff tight — no cosmetic restructuring beyond rules 1–9.
- **`report`.** Capture the non-greppable judgement checklist (one responsibility per module so
  Leiden communities stay clean; folders mirror architecture; stable descriptive names = stable node
  labels) and the before/after verification plan.

## Hard guards (the recurring failure mode)

- **The ONLY graphify invocation permitted is the `/tmp/gfx_probe/` sample run.** Never run graphify
  on `obdlab/obdlab`, never `graphify update .` from the repo root, never touch canonical
  `graphify-out/` or any `graph/*` dir. Building the real map is `T-KG-OBD-2`, not this task
  (`OBDLAB_TASKS_START_HERE.md` §0).
- **No behaviour change.** Legibility edits only: explicit imports, `__all__`, annotations,
  rationale comments/docstrings. No logic edits, no renames beyond what a kept rule names (renames
  churn the graph and the diff). If the audit surfaces a logic/bug finding, it goes to **Unplanned
  follow-ups**, not into this diff.
- **`4dlab-code-prep` makes no edits itself** — it audits and reports; the coder edits by hand.
- **No cross-lab imports introduced.** Any numeric literal added (none expected here) carries a wiki
  cite per the workspace rule.

## Inner loop (after every meaningful edit)

`ruff` → `pyright` → `pytest -x -q` from `labs/obdlab/`. The suite must stay green — these are
legibility edits, so a red test means an import/annotation change altered behaviour: revert and
re-think. Re-run the loop after each rule's batch of edits, not only at the end.

## Success criteria

- The three `probe` answers are recorded; `E/R/D` are in- or out-of-scope strictly per those answers.
- Every shipped edit maps to a named consumer in the table above (anti-churn).
- `from x import *` count in `obdlab/obdlab` is **0** after the task (rule I).
- Each package `__init__.py` under `obdlab/obdlab` either has `__all__` or the report names why not
  (rule A).
- Inner loop clean (`ruff`/`pyright`/`pytest -x -q` green); no behaviour change.
- A **before/after legibility note** (not a full graph build): the `audit` violation counts at start
  vs end, proving the prep closed them. The graph-level before/after node/edge proof is `T-KG-OBD-2`'s,
  not this task's.

## Deliverables

1. The applied source edits in `obdlab/obdlab/` (explicit imports, `__all__`, annotations,
   rationale tags/docstrings — only those tied to a consumer).
2. `tasks/progress_notes/T-KG-OBD-2-PREP.md` — `## Plan` → `VERIFICATION GATE` → `CODE REVIEW`,
   containing: the three `probe` answers, the `audit` fix plan with before/after counts, the
   consumer each edit served, and the clean inner-loop output.
3. `tasks/PROGRESS.md` — flip this row to `done` (atomic with the gate blocks).

## Files to touch

- `obdlab/obdlab/**` (legibility edits only, scoped to kept-rule consumers)
- `tasks/progress_notes/T-KG-OBD-2-PREP.md` (new)
- `tasks/PROGRESS.md` (this row → `done`)

## Out of scope

No graphify run except the `/tmp` probe. No `graph/*` writes (that is `T-KG-OBD-2`). No `tests/` or
`research/` edits. No logic/behaviour changes, no opportunistic refactors. No new schema fields/channels.

## Verification gate (coder fills)

```bash
cd <repo>/labs/obdlab
# rule I — no star imports survive
! grep -rn "import \*" obdlab/obdlab && echo "OK: no star imports" || { echo "FAIL: star import remains"; exit 1; }
# rule A — every package __init__.py declares __all__ (or report names the exception)
for f in $(find obdlab/obdlab -name __init__.py); do grep -q "__all__" "$f" || echo "REVIEW: no __all__ in $f"; done
# behaviour unchanged
ruff check obdlab/obdlab && pyright obdlab/obdlab && pytest -x -q
# no canonical graphify collateral from this task
test -d ../../graphify-out && echo "FAIL: root graphify-out exists" || echo "OK no root graphify-out"
git status --porcelain graph/ | grep . && echo "FAIL: a graph/* dir changed" || echo "OK graph/* untouched"
```

- All three `probe` answers recorded; `E/R/D` scoped strictly to `yes` answers.
- Each shipped edit cross-checked to a consumer in the §"Signal/noise" table (anti-churn).

## CODE REVIEW (coder fills)

(open the progress note with `## Plan`, then `VERIFICATION GATE`, then this block. Confirm: no
behaviour change, diff limited to kept-rule edits, suite green, only the `/tmp` probe ran graphify.)
