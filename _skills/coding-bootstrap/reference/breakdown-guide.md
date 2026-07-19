# Breaking a monolith prompt into half-session tasks

A monolith build prompt usually has 5–15 numbered steps. Your job is to
re-group those steps into 4–8 tasks where each task can be completed *and
verified* in ≤ 50 % of a fresh session's context.

## The sizing rule

Per-task budget (for a non-thinking session at typical context size):

| Surface | Soft cap | Hard cap |
|---|---|---|
| Files touched (created + modified) | 5 | 12 |
| Lines of new/changed code | 300 | 800 |
| New tests written | 8 cases | 25 cases |
| External tools needed (DB, API, MCP) | 1 | 3 |
| Reasoning depth (architectural decisions made) | 2 | 5 |

If any **hard cap** would be crossed, split the task. If you hit two soft
caps, strongly consider splitting.

## Grouping heuristics

**Group when…**
- Two steps touch the same file (split the file across two tasks rarely
  works — you end up reading + re-reading it).
- One step is < 50 lines and the next is also small.
- Steps share a load-skill set (e.g., two YAML-population steps both load
  the schema skill).

**Split when…**
- A step involves a major design decision and another involves implementation
  using that decision — make the design its own task, output the decision
  as a `.md` file the next task reads.
- Discovery work (exploring a DB schema, mapping an API, reading docs) vs
  implementation. Discovery produces a `.md`; implementation reads the `.md`.
- Test-writing for a substantial module — tests are their own task. The
  test task reads the module's public interface, not its internals.
- One step crosses a technology boundary (Python code → SQL schema →
  YAML config). Each layer is its own task.

## The dependency graph

Tasks form a DAG, not a list. Every task lists its `Blocked by` IDs in
`PROGRESS.md`. The bootstrap picks the *first* row whose `Blocked by` set
is all `done` — so the graph determines execution order automatically.

Aim for a shallow graph: any task that blocks more than 3 others is a
bottleneck (the user can only run one session at a time). If you can
shrink the bottleneck or move its work earlier, do so.

## Naming convention

`T-<PHASE>-<N>_<slug>.md`

- `<PHASE>` — short code grouping related tasks: `P0`, `P1`, `VL` (VINLab),
  `FX` (fixes), `DOC` (documentation).
- `<N>` — 1-based ordinal within the phase.
- `<slug>` — 2–5 lowercased words separated by underscores describing the
  deliverable in noun-phrase form (`schema_exploration`, `models_dataclass`,
  not `do_schema` or `make_models`).

Examples (from V2):

- `T-P0-1_master_guides_egr_ecu.md`
- `T-P1-1_symptoms_yaml.md`
- `T-P3-3_digital_parser.md`
- `T-FX-1_dtc_map_restructure.md`

## Worked example — splitting a 10-step prompt

Source prompt: 10 steps building a Python module that reads a DB, builds a
dataclass, exposes a public API, and has tests.

Bad split (too coarse): 3 tasks of ~3–4 steps each. Each task touches 8+
files and runs against the hard cap. The middle task will overflow.

Good split (1 step ≈ 1 task is fine when steps are large; sometimes 2
small steps fuse):

| Task | Source steps | Why grouped/split |
|---|---|---|
| T-1 schema_discovery | Steps 1–2 | Both are pure discovery, output is a `.md` mapping file |
| T-2 module_scaffold | Steps 3–4 | Scaffold + dataclass; trivial directory + ~150 lines |
| T-3 db_query_layer | Step 6 | Three SQL functions, isolated, tests separately |
| T-4 inference_rules | Step 7 | Three small modules, single file each, shared theme |
| T-5 decoder_core | Steps 5+8 | Largest logic + public API that depends on T-2, T-3, T-4 |
| T-6 tests_and_verification | Steps 9+10 | Test suite for everything; runs the smoke test |

T-1 blocks T-3 (mapping is the SQL input). T-2 blocks T-3, T-4, T-5. T-3
and T-4 block T-5. T-5 blocks T-6. Shallow graph, clear order.

## Disclosure-first ordering (progressive disclosure)

Sizing and grouping decide *how big* each task is; disclosure decides *what
order* they reveal information in. Order the pack so each task surfaces what the
next decision needs before any task commits to that decision:

- **Disclosure upstream of commitment.** The task that reveals a
  decision-relevant unknown — a measured number, a residual, a feasibility — is
  `Blocked by`-upstream of the tasks whose scope depends on it.
- **Split disclose-from-commit.** If a task both discloses a fact and commits a
  policy calibrated on it (a threshold, re-tune, re-pin), split it: ship the
  disclosure, defer the commitment as a separate task blocked on it.
- **One live task at a time (iterative packs).** When the owner runs
  step-by-step, author only the next runnable task in full; keep the rest as
  named, forward-registered ledger rows until the prior task's disclosure lands.
- **Tier disclosure outputs.** Measurement/checkpoint tasks emit results
  essential-first: headline → per-bucket/summary → per-case detail (push detail
  to JSON), so the reader gets the decision in one line and drills down only on a surprise.

This is NN/g progressive disclosure (show the essential first, defer the
secondary layer until requested) applied to a task pack. See SKILL.md "Why this
works" constraint 4.

## When the source prompt is wrong

The source prompt may have ordering errors or missing prerequisites. Catch
these during the breakdown:

- Does Step N use a file Step N-1 didn't create? → either reorder or add a
  prerequisite task.
- Does the prompt assume an external tool (MCP server, env var) is set up?
  → call that out in `START_HERE.md` under "Prerequisites".
- Are success criteria vague? → translate them into concrete `Verification`
  commands in the affected task file. If you can't, surface the ambiguity
  to the user.

Do not silently fix prompt bugs. Note each one in the chat plan you post
before generating files.
