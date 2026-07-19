# Graph compilation guide — T-PREP phase

Use this reference when the source prompt describes building a **knowledge graph from a wiki**
as a prerequisite step before the main coding phases (P0–P5). This is the T-PREP phase
that precedes the `knowledge-graph-iteration.md` pattern.

---

## When T-PREP applies

Use it when **all** of these hold:

- The module has a wiki (`.md`) as its authoritative source document
- The module uses `graphify` to extract the KG (4DLab standard toolchain)
- No `graphify-out/graph.json` exists yet, or the existing graph failed quality criteria
- You are about to start P0 (scaffold) for a new module

T-PREP produces `graphify-out/graph.json` — the verified artefact that P1–P5 read. Without
a clean T-PREP, the schema stage (P1) has no reliable entity list to work from.

---

## The T-PREP workflow (4 steps)

```
Step 1  Read spec              graphify-out/REEXTRACTION_SPEC.md in the module root
Step 2  Vanilla extract        graphify --wiki <files>   (confirm truncation / table-skip)
Step 3  Augmented chunked run  split wiki → extract each chunk → merge → rebuild
Step 4  Option 3 patch         if proof-set < threshold: inject missing edges → rebuild
```

The pattern is documented in the 4dlab-graph skill. Two worked examples exist:

| Module | Status | Key lesson |
|---|---|---|
| GASLab | Complete (6/6 criteria PASS) | Augmented pass caught all 28 enumerates; 37 direction flips found post-hoc |
| DTCLab | In progress (T-PREP-1 active) | C3/C4/C5 failed after run 2; spec v2 written, run 3 pending |
| OBDLab | Pending (T-PREP-1 written) | First run; 28 fault profiles + 7 enum types are the truncation canary |

---

## Skill location

The full T-PREP skill is at:

```
_skills/graph/4dlab-graph/SKILL.md
```

It contains:
- Python health-check scripts (`health`, `proof`, `criteria` operations)
- Augmented extraction prompt rules template
- Option 3 deterministic patch script template
- STEP1_VERIFICATION_LOG.md output template
- Module path table for all 4DLab modules
- Domain relation vocabulary and bad-relation detection

---

## How T-PREP feeds the KG iteration pattern

```
T-PREP-1  (graph skill)
    └─ produces: graphify-out/graph.json  (verified)
         │
         ▼
P0  scaffold + archive
P1  schema — enums and Pydantic types derived from graph nodes
P2  extraction — YAML ontology seeded from graph edges
P3  entity resolution — overlapping nodes detected from graph
P4  assembly — rule engine wired from graph traversal order
P5  validation — drift guard compares code literals against source wiki
```

The graph is the canonical entity list for P1. If the graph has silent direction inversions
(e.g. `EnumValue --enumerates--> EnumClass` instead of the reverse), P1 will produce
enums with the wrong parent class. Fix direction issues in T-PREP before P0.

---

## Direction inversion — the most common silent failure

Both GASLab and DTCLab had systematic source↔target inversions for `enumerates`, `routes_to`,
and `references` edges. The original verification (networkx undirected traversal) masked them.
Always run the 4dlab-graph `health` operation with explicit direction checks before declaring
T-PREP complete. The skill's Python analysis script includes this check.

---

## Common structural defects by relation type

| Relation | Correct direction | Common inversion |
|---|---|---|
| `enumerates` | EnumClass → EnumValue | **EnumValue → EnumClass** (very common — extractor reverses subject/object) |
| `routes_to` | RoutingTag/Mode → Target | **Target → RoutingTag** (common in DTCLab routing-tag tables) |
| `gated_by` | AnalyticsNode → GateCondition | Usually correct |
| `computes` | ProcessingClass → DerivedNode | Usually correct |
| `cross_references` | WikiSection → VocabSection | Usually correct |

---

## Session task file template location

Each module's T-PREP task lives at `{MODULE}/prompt.md`:

```
GASLab/graphify-out/REEXTRACTION_SPEC.md  (spec)
DTCLab/prompt.md                          (T-PREP-1 task)
OBDLab/prompt.md                          (T-PREP-1 task — first run)
```

When starting a new module, copy the OBDLab `prompt.md` pattern and update:
- Module name + wiki paths
- Truncation canary nodes (what should appear in chunk_03)
- Proof-set edge count and criterion thresholds
