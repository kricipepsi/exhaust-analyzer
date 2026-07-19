---
name: 4dlab-code-prep
description: >
  Prepare 4DLab Python SOURCE CODE for graphify code-map ingestion (Pass 1 / tree-sitter AST,
  offline, no LLM). Audits a package for the formatting that controls code-map node/edge quality —
  explicit imports, __all__ surface, type hints, explicit enums, rationale comments — and probes
  what the local graphify build actually extracts before any edit.
  Use this skill whenever the user mentions a code map, source-code knowledge graph, "graphify the
  code", AST ingestion, /graphify <python-package>, preparing/cleaning code for ingestion, a
  v2_code / code-map build, or asks why a symbol/edge is missing from a code graph. Use it for
  GASLab, OBDLab, DTCLab, COMLab, DNALab source packages.
  This is the CODE counterpart to 4dlab-wiki-prep: 4dlab-wiki-prep prepares WIKI/PROSE (Pass 3, LLM
  semantic); THIS skill prepares SOURCE CODE (Pass 1, AST). If the input is .md/wiki/prose, use
  4dlab-wiki-prep. To actually run graphify after prep, use 4dlab-graphify-run. If the input is a
  .py package and you are preparing it, use this.
allowed-tools: Read, Grep, Glob, Bash, Write
metadata:
  version: "0.1"
  argument-hint: "[operation] [package-path] — operations: probe, audit, report"
  model: sonnet
  context: fork
---

## Purpose

graphify builds a **code map** by parsing source with **tree-sitter** locally — "Pass 1" in
graphify's own pipeline. Pass 1 extracts classes, functions, imports, call graphs, and inline
comments **with no LLM and no API calls**. For a *code-only* corpus graphify skips its semantic
LLM pass (Pass 3) entirely. So for 4DLab source packages, the quality of the resulting graph is
decided **purely by what tree-sitter can see statically in your code** — not by any prompt or
model.

This skill makes a package ingestion-ready for that AST pass. It does **not** rewrite your source
for you (mass auto-edits are unreviewable and risk fabricating structure). It **probes** what the
local graphify build really extracts, **audits** the package against the rules that control node/
edge quality, and emits a **fix plan** the coder applies with judgement.

Full rationale and the rule-to-mechanism evidence table live in
`labs/obdlab/GRAPHIFY_CODE_INGESTION_FORMATTING.md` — read it if you need the "why" behind a rule.

**Operations:**
- `probe`           — **run first**: build a throwaway sample, run scoped graphify on it, and record
                      what THIS graphify build actually emits (enum sub-nodes? rationale nodes from
                      `# WHY:` comments? from docstrings?). Grounds every later decision.
- `audit [package]` — scan the real package against the machine-checkable rules; emit violations
                      with `file:line` as the fix plan.
- `report`          — emit the human-judgement checklist (the rules that can't be grepped) and the
                      consumer each fix produces.

If no operation is given, run `probe` then `audit` as a combined readiness summary.

---

## Boundary — code vs wiki (do not cross the streams)

This is the single most common mistake, so be explicit about which graph you are feeding.

| | **This skill — code map** | **`4dlab-wiki-prep` — wiki KG** |
|---|---|---|
| Input | `.py` source package | `.md` wiki / prose chunks |
| graphify pass | Pass 1 — tree-sitter AST, offline, no API | Pass 3 — LLM subagents, costs tokens |
| Edge types | `calls`, `imports`, `implements` (structural) | domain verbs: `routes_to`, `gated_by`, `monitored_by`, … |
| Prep lever | source legibility (imports, types, `__all__`) | explicit relation lines in text, canonical labels |
| Output graph | `graph/v2_code/` | `graph/v2_wiki/` |

The domain relation vocabulary (`routes_to`, `gated_by`, `enumerates`, …) belongs to the **wiki**
KG and is produced by the LLM pass over prose. **Do not** format code hoping to induce those edges
— Pass 1 emits only `calls`/`imports`/`implements`. Never inject relation-vocab headers, ENTITY
markers, or chunk boundaries into source; those are wiki-prep techniques and are noise in code.

---

## Step 0 — Resolve the target

Accept a package path (e.g. `obdlab/obdlab`) or a short lab name. **Base root:**
`/agent_workspace` (repo root). Scope strictly to the production package — exclude `tests/`
(a separate test-map graph) and `research/` (that is the wiki KG's input). Confirm the target is a
`.py` package; if it is wiki/prose, stop and point to `4dlab-wiki-prep`. This skill prepares source
but never runs graphify itself (except the `probe` sample); the actual build is `4dlab-graphify-run`.

---

## Step 1 — `probe` (run before any source edit)

The point: confirm what *this* graphify build extracts, so the audit only asks for work that
produces real nodes. README claims docstrings and `# WHY:`/`# NOTE:`/`# HACK:` comments become
`rationale` nodes and that enum members become sub-nodes — Pass 1 captures inline comments, so this
is expected, but **verify it for the installed build** rather than assume.

Create a throwaway sample (never touch canonical source or canonical `graphify-out/`):

```python
# /tmp/gfx_probe/sample_probe.py
from enum import StrEnum

class RpmStateBucket(StrEnum):
    STABILIZED_IDLE = "stabilized_idle"   # expect: enum-member sub-node

def calc_ve_standard(maf: float, map_kpa: float, rpm: float) -> float:
    """VE = (maf * R * T) / (map_kpa * Vd * rpm)."""  # expect: rationale node (docstring)
    # WHY: guard MAP=0 before division                <-- expect: rationale node (comment)
    return maf / map_kpa if map_kpa else 0.0
```

Run graphify scoped to the sample dir only (a code-only corpus → AST only, no API key needed),
then inspect the output `graph.json` and record three yes/no answers:

1. enum member `STABILIZED_IDLE` present as its own node? → governs rule **E** (explicit enums)
2. a `file_type: "rationale"` node for the `# WHY:` comment? → governs rule **R** (rationale tags)
3. a `rationale` node carrying the docstring/formula? → governs rule **D** (formula docstrings)

Report the three answers. **Any `no` removes that rule from the audit** — no consumer, no work
(signal/noise). `imports`/`calls`/`implements` and named symbols are always extracted, so rules
**I, A, T, C** below never need probing.

---

## Step 2 — `audit [package]` (machine-checkable rules → fix plan)

Grep/parse the package and report every violation as `file:line → rule → fix`. These are the rules
whose breach is objectively detectable. Each rule names the graphify consumer it protects.

- **I — Explicit named imports (highest payoff).** Flag every `from x import *`. Star imports give
  tree-sitter no names, so the caller→symbol `imports`/`calls` edges are lost or ambiguous.
  *Consumer: the import/call edge set.* Detect: `grep -rn "import \*"`.
- **A — Public surface via `__all__`.** Flag each package `__init__.py` with no `__all__`.
  graphify reads file-level exports to rank structural anchors. *Consumer: god-node ranking +
  entry-point nodes.*
- **T — Type hints on public signatures.** Flag exported `def`/method signatures with un-annotated
  params/returns, and class attributes without annotations in schema modules. Annotations are the
  edges that tie a field to its vocabulary type. *Consumer: type-reference edges.*
- **C — Static call sites.** Flag dynamic dispatch that hides calls from static analysis:
  `getattr(obj, name)(...)`, dispatch dicts of callables, `importlib`/`__import__`. Each hidden
  call is a missing `calls` edge. *Consumer: call graph.* (Report as advisory — some indirection is
  legitimate; do not demand removal, surface it.)
- **S — Statically named symbols.** Flag symbols built at runtime (factory-generated classes,
  `type(...)` constructions, names assigned in loops) that the team expects to query. The node
  `label` is the literal source name; runtime symbols never appear. *Consumer: node set +
  spot-check.*

For **E/R/D** (enums, rationale comments, formula docstrings): include in the audit **only if
Step-1 `probe` returned `yes`** for that rule. Then flag: domain states not defined as
`Enum`/`StrEnum` (**E**), non-obvious gates/equations without a `# WHY:`/`# NOTE:` tag (**R**),
and formula/validation methods without a parameter-naming docstring (**D**).

Emit the fix plan grouped by rule, with counts and `file:line`. Do **not** edit source — the coder
applies fixes; `__all__`, type, and rationale edits need human judgement, and a blanket auto-rewrite
is exactly the sprawling unreviewable diff the workspace rules forbid.

---

## Step 3 — `report` (judgement checklist + consumers)

Emit the non-greppable guidance for the coder: one responsibility per module so Leiden community
detection produces clean clusters; folders mirroring architecture; descriptive stable names (the
name *is* the node label, so renames churn the graph). Pair each with its consumer so the coder can
weigh each edit against the signal/noise rule, and list the post-prep verification (re-run
`/graphify <package>` into a fresh dir, diff node/edge counts and key-symbol presence against the
pre-prep baseline — that before/after is the proof the prep helped).

---

## Output conventions

- Section header: `--=={ 4dlab-code-ingest: PACKAGE / OPERATION }==--`
- `probe`: the three yes/no answers, then which of E/R/D stay in scope.
- `audit`: a table `file:line | rule | found | fix`, plus per-rule counts.
- Never auto-edit source. Never run `graphify update .` from a repo root — scope to the package or
  the `/tmp` sample. Never touch canonical `graphify-out/` or other `graph/*` dirs.
- Never invent a violation: if a rule can't be checked (E/R/D probed `no`), say so and skip it.

## Reference

- `labs/obdlab/GRAPHIFY_CODE_INGESTION_FORMATTING.md` — full rule-to-mechanism evidence table.
- graphify pipeline — `https://github.com/safishamsi/graphify/blob/v8/docs/how-it-works.md`.
