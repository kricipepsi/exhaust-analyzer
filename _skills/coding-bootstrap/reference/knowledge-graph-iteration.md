# Knowledge-graph build pattern — iterative loop

Use this reference when the source prompt describes building a **static knowledge graph** from an authoritative document (a wiki, a spec, an ontology) into a callable diagnostic / classifier / rule-engine module. The pattern is five stages that map cleanly to a `P0 + 5 phases` task pack.

Adapted and generalized from `4DLab/GasLabIteration.md`, which produced the GASLab v1.0 task pack at `4DLab/GASLab/gaslab_tasks/`. That task pack is the worked example for every section below.

---

## When to use this pattern

Use it when **all** of these hold:

- There is a single, authoritative source document (a wiki, a manual, a published ontology). If you have to merge contradictory sources at build time, this pattern is wrong — design the merge first, then come back.
- The knowledge is static at build time. The graph is compiled once and loaded as in-memory data; the module's behaviour changes when the source document changes, not when input data changes.
- The output is deterministic (a fault label, a routing tag, a classification) — not a free-text generation.
- The cost of a silent regression is high (production diagnostic, contract surface another module depends on). If the project can tolerate "redo this task", drop to lite mode and skip the stricter audits in stage 5.

Do **not** use it when:

- The ontology is still being discovered (you don't know the entity types yet). Build the ontology first, then start this loop.
- Inputs are streaming or the graph mutates at runtime. That is a different pattern (dynamic KG, with insertion / retraction).
- The deliverable is a free-text answer with retrieval. RAG is a different pattern.

---

## The five stages

Each stage corresponds to one phase in a `P0 + 5` task pack. P0 is the scaffold + archive task; stages 1–5 are phases 1–5.

### Stage 1 — Schema definition and guardrails

The structural rules come first. Without a schema, every later stage drifts.

What you produce in this stage:

- A typed schema for every node and edge type, in the project's primary language (Pydantic for Python, equivalent in others). Frozen dataclasses for inputs; Pydantic `BaseModel` for wire-format outputs with field constraints.
- Enums for every closed vocabulary (fault labels, validity verdicts, state buckets). Cite the section of the source document each enum derives from in the docstring.
- A version field on the on-disk schema (`version: "1.0"`) co-located with the code. When the schema changes, the version bumps; downstream consumers can pin.

What this looks like as a task: one task that ships the typed contract surface and at minimum one rejection test per envelope constraint. No domain logic in this phase. GASLab worked example: `T-P1-1_schemas_and_enums.md`.

### Stage 2 — Extraction and processing

Translate the authoritative document into clean, declarative data. Two sub-tasks usually:

- **Chemistry / pure-function core** — the formulas and validity gates the source document defines. These are *pure* functions: same inputs → same outputs, no I/O. Their tests are derived directly from worked examples in the source.
- **Declarative ontology file** — usually YAML, sometimes JSON. One entry per node (fault, rule, threshold), each entry carrying a `citation:` field that names the source-document section it derives from.

**Hand-craft over LLM-extract** when the source has intricate inter-entry grammar (override rules, seesaws, collisions, gating conditions). LLM extraction looks faster up front but generates a verification debt that costs more than the extraction saved. Worked example: GASLab YAML was hand-crafted from `GAS_WIKI §7` against `GAS_VOCABULARY §10` thresholds (`T-P2-2_yaml_ontology.md`).

LLM-extraction is acceptable when the source is shaped as a uniform table with no cross-entry dependencies. Even then, add a verification task that diffs the extracted output against the source.

### Stage 3 — Entity resolution and clustering

Sources almost always contain overlapping entries — two fault signatures that match identical gas profiles, two routing rules that match the same DTC pattern. Resolution detects the overlaps and attaches **differentiator edges** that the rule engine in Stage 4 uses to break ties deterministically.

What you produce:

- A pure `find_overlaps(ontology) -> list[tuple]` function.
- For each overlap pair the source document explicitly names, a differentiator edge in the YAML: either a DNA / context gate (`fuel_delivery_type == GDI`), a secondary-evidence requirement (`OIL_DIPSTICK_FUEL_SMELL`), or an operating-state differentiator (`clears_at_2500_rpm`).
- A test that proves every detected overlap has a non-empty resolution path.

If the source document names an overlap but does not name a differentiator, **stop**. Surface it to the architect's out-of-band patches table — the wiki itself needs the differentiator before the code can encode it.

GASLab worked example: `T-P3-1_entity_resolution.md`.

### Stage 4 — Graph assembly and storage

Wire the pure-function core (Stage 2) + the ontology (Stage 2) + the resolution layer (Stage 3) into a callable pipeline. The traversal order matters:

```
1. validity_gates      (chemistry / structural sanity)
   → on fail: emit SAMPLE_INVALID, stop. No further traversal.
2. reasoning_grammar   (override rules: collision, masking, etc.)
   → may short-circuit to a specific verdict.
3. fault / rule match  (bound matching across all entries)
   → produces a candidates list (often >1, hence stage 3).
4. apply_differentiators
   → reduces candidates to a single verdict (or "AMBIGUOUS" with a documented next step).
5. emit the wire-format payload.
```

The public entry point is one function: `process(reading, context) -> Payload`. Everything else is private. The module exposes the typed schemas from Stage 1 and this one function; nothing else.

GASLab worked example: `T-P4-1_rule_engine.md`.

### Stage 5 — Automated validation and feedback reasoning

The hallmark of the iterative pattern: use the assembled graph to validate itself. **Four audits** belong in this stage; each is a separate test in the validation suite.

1. **Collision audit** — for every pair of entries whose signature ranges overlap on every input dimension at the same operating state, assert that resolution can break the tie. No unresolved overlaps shall reach Stage 4 at runtime.

2. **Override-rule assertion** — for each override rule in the reasoning grammar (the source document's "masking rules", "tie-breakers", "priority overrides"), build a synthetic input that triggers the override and assert the verdict matches the source-document expectation. This is the assertion that prevents Stage 4 from silently bypassing Stage 2's grammar.

3. **Boundary permutation matrix** — a grid of synthetic inputs spanning the operating envelope produces a non-null verdict at every point. Either a concrete classification, or a documented "sample invalid" reason — never an uncaught exception or empty string. This is the proof that the graph has no orphan states.

4. **Source-drift guard** — every numeric threshold in the on-disk YAML matches the value in the source document's reference appendix (or wherever the canonical table lives). When the source document version bumps and a threshold changes, this test fails loudly. Without this guard, YAML drifts from the document and nobody notices for weeks.

GASLab worked example: `T-P5-1_validation_suite.md`.

---

## Mapping to a task pack

The pattern produces this shape every time:

| Phase | Stage | Typical task count | What ships |
|---|---|---|---|
| P0 | (setup) | 1 | Scaffold + archive of any prior build. |
| P1 | §1 Schema | 1 | Pydantic schemas, enums, frozen input dataclass. |
| P2 | §2 Extraction | 2 | Pure chemistry/logic core + hand-crafted YAML ontology. |
| P3 | §3 Resolution | 1 | Overlap detection + differentiator edges. |
| P4 | §4 Assembly | 1 | Rule engine + public `process()`. |
| P5 | §5 Validation | 1 | Four audits + drift guard. |

Total: 7 tasks. Shallow DAG: `P0 → P1 → {P2-1, P2-2} → P3 → P4 → P5`. Every task fits the half-session sizing rule (`breakdown-guide.md`).

The DAG is shallow on purpose. Wide phases (parallel P2-1, P2-2) keep the bottleneck count low; the user can only run one session at a time, so wide is fine.

---

## The almost-always-needed on-demand skill

Author one custom on-demand skill for this pattern: `<module>-source-provenance` (or `<module>-wiki-provenance` if the source is a wiki). It gates ≥ 3 tasks (every task from P1 onward that introduces a numeric literal), so it meets the threshold in `custom-skill-authoring.md`.

What the skill defines:

- The provenance comment grammar: every numeric literal in code carries an inline `# source: <DOC> §N.M` (or `# wiki:` / `# vocab:` / `# spec:` per project convention).
- The YAML provenance grammar: every fault / rule / threshold entry has a top-level `citation:` field.
- A wiki-section map: which source-document section owns which class of fact, so the coder doesn't have to grep the source on every literal.
- An audit rule that the module's `<module>-verification-loop` Phase 5 enforces.

Worked example: `4DLab/GASLab/_gaslab_skills/gaslab-wiki-provenance/SKILL.md`. Copy and re-scope when building the next KG module.

---

## Strict-mode coupling

Knowledge-graph builds are exactly the project profile `strict-vs-lite.md` recommends strict for: schema invariants the rule engine depends on, multi-phase work, silent-regression risk, > 10 tasks once expansion phases land. Do not run this pattern in lite mode. The Stage 5 audits depend on the `VERIFICATION GATE` / `CODE REVIEW` block discipline to land in `progress_notes/<task-id>.md`; without those blocks, the audits become advisory and drift accumulates.

---

## What this pattern does not produce

- No vector embeddings or semantic similarity. Stage 3 resolution uses **explicit edges** named in the source document, not learned similarity. (Embeddings are a future extension when the source no longer names every overlap.)
- No real-time learning loop. The graph is rebuilt when the source document changes, not when input data accumulates.
- No corpus-based accuracy benchmark. The Stage 5 boundary permutation matrix is the contract, not "how often did we agree with the human label." If a corpus benchmark is needed, it is a separate task downstream of this pattern, and it cites the source document for every disagreement.

---

## Cross-references

- `code-quality-principles.md` — the Karpathy four apply per-task; this reference is one layer up, the whole-build pattern.
- `breakdown-guide.md` — sizing rules for each task in the pack; the 7-task shape above is already half-session by construction.
- `custom-skill-authoring.md` — when to author the `<module>-source-provenance` skill (always, for this pattern).
- `strict-vs-lite.md` — strict-mode is mandatory for this pattern; the audits depend on the gate blocks.
- Worked example end-to-end: `4DLab/GASLab/` — read `GASLAB_START_HERE.md`, `GASLAB_PROGRESS.md`, the seven `gaslab_tasks/T-*.md`, and the four `_gaslab_skills/*/SKILL.md` files.
