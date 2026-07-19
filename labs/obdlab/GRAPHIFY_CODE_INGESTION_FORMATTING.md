# Formatting Python source for optimal graphify ingestion

**Author:** architect · **Date:** 2026-06-09 · **Status:** verified against graphify source
**Verifies / supersedes:** `CodeIngestionPrep.md` (this file pins each rule to a documented
graphify mechanism and corrects two items).
**Sources:** graphify README + `docs/how-it-works.md` @ branch `v8`
(`https://github.com/safishamsi/graphify`).

> graphify ships **no** dedicated "how to format your code" guide — only the README and
> `how-it-works.md` (the pipeline) exist. Every rule below is therefore *derived* from a
> documented extraction mechanism, and each carries an evidence tag so the coder knows what
> is fact vs inference.

---

## 1. The premise, settled

The earlier open question — *does a code-only corpus get docstring/rationale extraction, or
only AST structure?* — is now answered from graphify's own pipeline doc.

graphify runs **three passes** (`how-it-works.md` §"The three passes"):

| Pass | Cost | What it extracts | Runs for OBDLab code corpus? |
|---|---|---|---|
| **Pass 1 — code structure** | free, offline, tree-sitter, no API | classes, functions, imports, **call graphs, and inline comments** | **YES** |
| Pass 2 — video/audio | local (faster-whisper) | transcripts | no (no media) |
| **Pass 3 — docs/papers/images** | LLM subagents, costs tokens | semantic nodes/edges from prose | **NO — skipped** |

Direct quotes:

- *"Tree-sitter parses your code files and extracts classes, functions, imports, call graphs,
  **and inline comments**. This runs locally with no LLM involved."* (Pass 1)
- *"Code files are not sent to the LLM semantic extractor in the normal pipeline. If a corpus
  contains only code files, Pass 3 is skipped entirely; semantic extraction is reserved for
  docs, papers, images, and transcripts."*
- Node `file_type` values include `code`, `document`, `paper`, `image`, **`rationale`** (graph
  format §).

**Conclusion — both prior docs were right, and they don't actually conflict:**

- T-KG-OBD-2's "AST extraction only (Part A); semantic subagents (Part B) skipped" is **correct**
  — Pass 3 is genuinely skipped for `obdlab/obdlab`.
- CodeIngestionPrep.md §3 (rationale comments / docstrings → nodes) is **also valid**, because
  inline-comment capture lives in **Pass 1 (the offline AST pass)**, *not* the skipped LLM pass.
  The `rationale` node type exists precisely for this.

**One residual nuance (the only thing left to confirm by sample):** `how-it-works.md` names
"inline comments" explicitly for Pass 1 and the README adds "docstrings"; it does not separately
itemise whether **docstrings** become `rationale` nodes in the offline pass for a *code-only*
corpus. Documentary evidence strongly says yes. The cheap confirmation (Step-1 sample run, below)
now shrinks from *"decide whether to do §3 at all"* to *"confirm docstrings route through Pass 1."*

> **PROBE VERDICT (graphify v0.8.13, run 2026-06-09 under `T-GFXSKILL-2`).** The Step-1 sample
> (below) has been run against the installed build. Results:
> - **Docstrings → `rationale` node: YES** — the residual nuance is resolved. Rule **D** keeps its
>   consumer; do the docstring work.
> - **`# WHY:`/`# NOTE:` comments → `rationale` node: YES** — rule **R** confirmed.
> - **Enum members → sub-node: NO** — this build does **not** emit a node per enum member, only the
>   enum *class* node. So rule **E** (formatting domain states as `Enum`/`StrEnum` to gain
>   member-level query nodes) has **no consumer in v0.8.13 and is DROPPED.** (Enum-member queries
>   against the code map will return nothing — record that expectation for `T-KG-OBD-2`.)
>
> This verdict is a property of the **graphify build**, not of any one package, so it transfers to
> every 4DLab code-prep run on this build. **Re-run the probe only if the graphify version changes.**
>
> **Which version number to watch.** Two decoupled versions exist in the environment: the
> **extraction engine / package = `0.8.13`** (this is what the verdict is tied to), and the
> **skill-text / CLI wrapper, which reports `0.8.36`** in its banner. Node extraction is the engine's
> job, so the gate is the **`0.8.13` package** — a `0.8.36` banner is *not* a reason to re-probe.
> Iteration-2 (`T-GFXSKILL-2`, Codex executor) re-ran the probe in this exact environment and the
> verdict held. Re-probe only if the **engine/package** version moves off `0.8.13`.

---

## 2. What a code-map node/edge actually looks like

This bounds every rule: you can only "format for" relations graphify can emit. For code (Pass 1)
the relations are **structural** verb phrases — `calls`, `imports`, `implements` (graph format §).
Code EXTRACTED edges always carry `confidence = EXTRACTED`, `confidence_score = 1.0`.

> **Myth to kill:** the domain vocabulary in the `4dlab-graph` skill — `routes_to`, `gated_by`,
> `monitored_by`, `enumerates`, … — is **wiki-KG** vocabulary produced by the LLM pass over prose.
> It does **not** apply to the code map. Do not format code hoping to induce those edges; Pass 1
> emits `calls`/`imports`/`implements`, full stop.

---

## 3. The rules — each tied to its graphify consumer

Evidence tags: **[Documented]** = stated in README/how-it-works · **[Derived]** = logically forced
by a documented mechanism · **[Verify]** = plausible, confirm in the Step-1 sample.

### 3.1 Structure & imports (highest payoff)

1. **Explicit named imports; never `from x import *`.** **[Documented + Derived]**
   Pass 1 extracts `imports` and `calls` from the AST. A star import gives tree-sitter no names,
   so the caller→symbol edges it would have drawn are lost or ambiguous. Named imports →
   unambiguous EXTRACTED edges. *Consumer: the `imports`/`calls` edge set.*

2. **Declare public surface with `__all__` in each package `__init__.py`.** **[Derived]**
   graphify "analyzes folder layouts and file-level exports to determine structural dependencies"
   (README "What you get" / CodeIngestionPrep §1). `__all__` marks the ranked structural anchors
   (e.g. `sensor_signal_translator`). *Consumer: god-node ranking + package entry-point nodes.*

3. **Keep one clear responsibility per module; let folders mirror architecture.** **[Documented]**
   Communities come from the **Leiden algorithm** over edge density (`how-it-works.md`). Clean
   module boundaries → clean, well-labelled communities in `GRAPH_REPORT.md`. *Consumer: community
   detection.*

4. **Prefer direct call sites over dynamic dispatch / registries / `getattr` indirection.**
   **[Derived]** Pass 1 is static (tree-sitter, no execution tracing). A call routed through a
   dispatch table or `importlib` is invisible → the `calls` edge drops. *Consumer: call graph.*

5. **Avoid metaprogrammed/runtime-generated symbols for anything you want findable.** **[Derived]**
   Nodes are named symbols captured statically; the node `label` *is* the source name. Symbols
   built at runtime never appear (and so fail the T-KG-OBD-2 spot-check for `o2_normalizer`,
   `translate`, `OBDLivePayload`, …). *Consumer: node set + spot-check.*

### 3.2 Typing & enums

6. **Annotate fields/params/returns with concrete domain types.** **[Derived]**
   Tree-sitter captures type hints in the AST; `rpm_state_bucket: RpmStateBucket` ties the data
   model to the vocabulary type node. *Consumer: type-reference edges between schema and vocab.*

7. **Define domain states as explicit `Enum`/`StrEnum` classes.** **[Refuted for v0.8.13 — rule
   DROPPED]** The hypothesis was that enum members (`STABILIZED_IDLE`, `DUAL_MAF_MAP_CROSSCHECK`, …)
   become captured sub-nodes. The probe (v0.8.13) shows they do **not** — only the enum *class* node
   is emitted. There is therefore **no member-level consumer**, so per signal/noise this rule is not
   work: do not restructure code to expose enum members for the code map. (Explicit enums remain good
   engineering and the class node is still captured — just don't count on member nodes.)

### 3.3 Rationale (now in-scope — see §1)

8. **Tag non-obvious logic with uppercase `# NOTE:` / `# WHY:` / `# HACK:` comments.**
   **[Documented]** README: these inline comments "are extracted as separate nodes linked to the
   code they explain." Captured in Pass 1. Use them on the prioritised evaluation gates and the
   physical-bounds equations. *Consumer: `rationale` nodes + their link to the owning symbol.*

9. **Write docstrings on methods that encode formulas/validation, naming the parameters.**
   **[Confirmed YES for v0.8.13 — keep]** The probe shows docstrings route through Pass 1 as
   `rationale` nodes. Documenting `_calc_ve_standard` with `maf, map_kpa, rpm` indexes the
   relationship. *Consumer: `rationale` node attached to the method.*

---

## 4. Reconciliation with `CodeIngestionPrep.md`

| CodeIngestionPrep.md item | Verdict | Note |
|---|---|---|
| §1 explicit interfaces / `__all__` | **Confirm** | rules 1–2 |
| §1 avoid star imports | **Confirm** | rule 1 — highest payoff |
| §2 strong typing for entity linking | **Confirm** | rule 6 |
| §2 explicit enums → member sub-nodes | **Refuted (v0.8.13): members NOT extracted → rule 7 dropped** | only the enum class node is emitted; no member nodes |
| §3 `# WHY:`/`# NOTE:`/`# HACK:` rationale tags | **Confirm** | rule 8 — Pass 1 captures inline comments |
| §3 docstrings → semantic nodes | **Confirmed (v0.8.13): docstring → rationale node** | rule 9 — probe verified |
| **§4 test-file parallel naming / bidirectional mapping** | **Correct: out of scope here** | Tests are a **separate graph** (T-KG-OBD-3 → `graph/v2_tests/`); T-KG-OBD-2 ingests `obdlab/obdlab` only and **excludes** `tests/`. Apply §4 in the test-ingestion task, not the production code-map prep. |
| Implicit premise "graphify pulls rationale from code" | **Confirmed** | via Pass 1 inline-comment capture — see §1 |

---

## 5. The Step-1 sample check (10 minutes, before any source edit)

> **Already run for v0.8.13** (2026-06-09, `T-GFXSKILL-2`) — see the PROBE VERDICT box in §1:
> enum members **NO**, `# WHY:` **YES**, docstring **YES**. Repeat the steps below **only if the
> graphify build version changes**; otherwise take the verdict as given.

Run graphify on a throwaway file to confirm the two **[Verify]** items for *this* graphify build:

```python
# sample_probe.py
from enum import StrEnum

class RpmStateBucket(StrEnum):
    STABILIZED_IDLE = "stabilized_idle"   # enum member → expect a sub-node

def calc_ve_standard(maf: float, map_kpa: float, rpm: float) -> float:
    """VE = (maf * R * T) / (map_kpa * Vd * rpm).  # formula docstring → expect a rationale node."""
    # WHY: guard against MAP=0 before division   <-- expect a rationale node
    return maf / map_kpa if map_kpa else 0.0
```

Build it scoped (never `graphify update .` from root), then inspect `graph.json`:

- enum member `STABILIZED_IDLE` present as a node? → confirms rule 7 granularity.
- a node with `file_type: "rationale"` for the `# WHY:` line? → confirms rule 8.
- a `rationale` node carrying the docstring/formula? → confirms rule 9 (the residual nuance).

Record the three yes/no answers in the prep task's progress note. Anything that comes back **no**
drops from the prep scope (signal/noise: no consumer, no work).

---

## 6. What does NOT help (don't spend effort here)

- Inducing domain relations (`routes_to`, `gated_by`, …) in code — that vocabulary is wiki-only (§2).
- Loading the `4dlab-graph` skill for the code map — it is built for wiki prep and would misfire;
  T-KG-OBD-2 is a raw scoped `/graphify obdlab/obdlab` run with **no skill loaded**.
- Cosmetic restructuring beyond rules 1–9 — every edit must map to a rule's named consumer above,
  or it is churn against the "touch only what you must" rule.

---

## 7. Sources

- graphify README — `https://github.com/safishamsi/graphify` (passes overview, file_type list,
  "what you get": rationale-comment extraction, code-only = no API key).
- graphify pipeline — `https://github.com/safishamsi/graphify/blob/v8/docs/how-it-works.md`
  (three passes; Pass 3 skipped for code-only; Leiden communities; graph format).
- `labs/obdlab/CodeIngestionPrep.md` (the doc this guide verifies).
- `labs/obdlab/tasks/T-KG-OBD-2_graphify_ingest_code_map.md` (scope: production-only,
  tests excluded → separate `graph/v2_tests/` via T-KG-OBD-3).
