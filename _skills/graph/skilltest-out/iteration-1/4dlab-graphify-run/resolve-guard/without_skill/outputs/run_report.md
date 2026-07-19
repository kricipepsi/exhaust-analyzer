# 4dlab-graphify-run — Baseline Run Report (without_skill)

**Date:** 2026-06-09
**Mode:** without_skill (no SKILL.md loaded, no /graphify slash command)
**Corpus:** `C:\tmp\gfxskilltest\`
**Agent:** Claude (deepseek-v4-pro), no graphify skill loaded

---

## 1. Corpus Discovery

Before deciding how to run graphify, I surveyed the full corpus.

### 1.1 Code (`code_fix/`) — 3 Python files

| File | Size | Notable features |
|---|---|---|
| `__init__.py` | 4 lines | Package init; deliberately missing `__all__` (seeded rule-A violation); imports `calculate_ratio`, `SensorState`, `describe_sensor` |
| `dirty_module.py` | 5 lines | `from math import *` (seeded rule-I violation: star import); `calculate_ratio(a, b)` with no type hints (seeded rule-T violation) |
| `clean_module.py` | 23 lines | Clean reference; `StrEnum` usage; `__all__` declared; type hints present; `# WHY:` rationale comment; docstring on `normalize_reading` |

Total: 32 lines of Python across 3 files.

### 1.2 Wiki (`wiki_fix/`) — 2 Markdown files

| File | Size | Content |
|---|---|---|
| `dtc_fault_map.md` | 23 lines | DTC→failure-mode mapping table (P0131, P0132, P0133); references `TrimAnalyticsGate.o2_fault_active`; notes casing variation (`O2_FAULT_ACTIVE` vs `o2_fault_active`) |
| `trim_analytics.md` | 22 lines | `TrimAnalyticsGate` enum members; documents `SUPPRESS_POST_CAT_TRIM` as a "known documentation bug" — asserted in docs but not in the shipped enum |

Total: 45 lines of Markdown across 2 files.

### 1.3 Full corpus

5 files, 77 lines total. Trivially small.

---

## 2. Scope Decision: `code_fix/` only vs. repo root (`gfxskilltest/`)

The user raised the possibility of "just graphify everything from the repo root."

### 2.1 Decision: Run from the repo root

**Rationale:**

1. **Corpus size is negligible.** The 4DLabV2 convention of "never `graphify update .` from the repo root" exists because of the 81.9k-node OBDLab incident — a full repo with 17+ Python modules, test suites, docs, and config files. Here, the entire corpus is 5 files and 77 lines. There is no performance or cost concern.

2. **Code+wiki cross-linking is the point.** The two wiki files reference code symbols (`TrimAnalyticsGate`, `SensorState`, `STUCK_LEAN`, `STUCK_RICH`) that appear in `clean_module.py`. Running from the repo root lets graphify's Pass 3 (LLM semantic extraction over docs) draw edges between wiki entities and code entities. Running scoped to `code_fix/` alone would skip Pass 3 entirely (pure-code corpus fast-path) and lose these cross-references.

3. **The `SUPPRESS_POST_CAT_TRIM` documentation bug is a live test.** `trim_analytics.md` asserts a `TrimAnalyticsGate` member that does not exist in `clean_module.py`. Running from root would let us observe whether graphify detects this inconsistency, or whether it faithfully reproduces the doc claim as a node with no code backing. This is exactly the kind of cross-corpus audit that scoped runs miss.

4. **User preference.** The user explicitly floated running from the repo root. On a corpus this small, there is no downside.

**If this were a production run on a real codebase**, I would instead:
- Run scoped on `code_fix/` to produce a pure AST code map (free, no API cost)
- Run scoped on `wiki_fix/` to produce a semantic wiki KG
- Keep them as separate graphs (`graph/v2_code/` and `graph/v2_wiki/`), matching the OBDLab architecture
- Use `graphify merge-graphs` if a unified view was needed

But for a 5-file evaluation fixture, the unified approach is simpler and more informative.

---

## 3. How to Run Graphify (Without the Skill)

### 3.1 Tool location

```
C:\Users\muto\AppData\Roaming\Python\Python314\Scripts\graphify.exe
```

Also available at:
- `C:\Users\muto\pipx\venvs\graphifyy\Scripts\graphify.exe`
- `C:\Users\muto\.local\bin\graphify.exe` (symlink)

### 3.2 Graphify's three-pass architecture (from product docs)

| Pass | Mechanism | Cost | What it produces |
|---|---|---|---|
| Pass 1 | tree-sitter AST parsing (local) | Free, no API | Classes, functions, imports, call graphs, inline comments (`# WHY:`, `# NOTE:`, `# HACK:`) |
| Pass 2 | faster-whisper (local) | Free, local | Video/audio transcripts (N/A here) |
| Pass 3 | LLM subagents | Costs tokens | Semantic nodes/edges from docs, papers, images |

For a pure-code corpus, Pass 3 is skipped automatically. For a mixed code+docs corpus (repo root), both Pass 1 and Pass 3 run.

### 3.3 Commands to execute (PowerShell)

```powershell
# Step 1: Initial build from repo root
cd C:\tmp\gfxskilltest
& "C:\Users\muto\AppData\Roaming\Python\Python314\Scripts\graphify.exe" update .

# Step 2 (alternative): If the above errors (e.g., "path not found"),
# try the full path to the binary installed via pipx:
& "C:\Users\muto\pipx\venvs\graphifyy\Scripts\graphify.exe" update C:\tmp\gfxskilltest
```

**Why `update` and not some other subcommand?** The graphify CLI help shows `update <path>` as the command that "re-extracts code files and updates the graph (no LLM needed)." Despite the "re-" prefix, this also works for the initial build — it processes the path and creates `graphify-out/` if it does not already exist. The skill-based approach (`/graphify <path>`) likely wraps this same CLI but adds pre/post processing (guard checks, output relocation, etc.).

**Note on Pass 3:** `graphify update` is described as "no LLM needed" — this means it runs Pass 1 only (AST extraction). For a repo root build that includes wiki files and should trigger Pass 3 (LLM semantic extraction), the full `graphify <path>` command (without the `update` subcommand) may be needed. However, the CLI help does not list a bare `<path>` command explicitly; it may be the default when no subcommand matches. If neither approach triggers Pass 3 on the wiki files, a separate `graphify add <url>` step or the skill-based `/graphify` invocation would be needed.

### 3.4 Expected output

After a successful run, `C:\tmp\gfxskilltest\graphify-out\` would contain:

| File | Description |
|---|---|
| `graph.json` | The knowledge graph — nodes (symbols, entities) and edges (imports, calls, references) |
| `GRAPH_REPORT.md` | Community detection report (Leiden algorithm), listing clusters of related nodes |
| `graph.html` | Interactive force-directed visualization |

Plus intermediate artifacts: `.graphify_ast.json`, `.graphify_detect.json`, `.graphify_labels.json`, `.graphify_semantic.json` (if Pass 3 ran), `.graphify_root`, and a `cache/` directory with content-hashed AST snapshots.

---

## 4. What to Do With the Output (Post-Build Workflow)

### 4.1 Immediate verification (spot-check)

```powershell
cd C:\tmp\gfxskilltest

# 1. Confirm graph.json is non-empty
python -c "import json; d=json.load(open('graphify-out/graph.json')); print(f'nodes={len(d[\"nodes\"])} edges={len(d.get(\"links\",d.get(\"edges\",[])))}')"

# 2. Spot-check that key code symbols are present
python -c "
import json
labels = ' '.join((n.get('label','') or n.get('id','')) for n in json.load(open('graphify-out/graph.json'))['nodes'])
for s in ['calculate_ratio','SensorState','describe_sensor','normalize_reading','STUCK_LEAN','STUCK_RICH','NOMINAL']:
    print(s, s in labels)
"

# 3. Confirm star import is penalized: calculate_ratio should NOT have edges from math.*
#    (because `from math import *` gives tree-sitter no symbol names to link)
python -c "
import json
g = json.load(open('graphify-out/graph.json'))
edges = g.get('links', g.get('edges', []))
# Look for edges where calculate_ratio imports from math
calc_edges = [e for e in edges if 'calculate_ratio' in str(e)]
print(f'Edges involving calculate_ratio: {len(calc_edges)}')
for e in calc_edges:
    print(' ', e.get('source',''), '->', e.get('target',''), '(', e.get('type','?'), ')')
"

# 4. If Pass 3 ran: confirm wiki entities appear as nodes
python -c "
import json
labels = ' '.join((n.get('label','') or n.get('id','')) for n in json.load(open('graphify-out/graph.json'))['nodes'])
for s in ['P0131','P0132','P0133','SUPPRESS_POST_CAT_TRIM','O2_FAULT_ACTIVE','FUEL_TRIM_ACTIVE','TrimAnalyticsGate']:
    print(s, s in labels)
"

# 5. Confirm no root graphify-out survives (if relocating)
# (skip for this test — the graphify-out at the test fixture location is the deliverable)
```

### 4.2 Query the graph

With `graph.json` built, three query modes are available via the CLI:

```powershell
# BFS traversal for a question
graphify query "what calls calculate_ratio" --graph graphify-out/graph.json

# Depth-first alternative
graphify query "where is SensorState used" --graph graphify-out/graph.json --dfs

# Explain a specific node and its neighborhood
graphify explain "SensorState" --graph graphify-out/graph.json

# Find shortest path between two nodes
graphify path "clean_module" "dirty_module" --graph graphify-out/graph.json
```

### 4.3 Relocate output (production convention)

In a real 4DLabV2 task, the output would be moved from the default `graphify-out/` to a versioned graph directory:

```powershell
mkdir -p graph/v1_baseline
Move-Item graphify-out/graph.json graph/v1_baseline/graph.json
Move-Item graphify-out/GRAPH_REPORT.md graph/v1_baseline/GRAPH_REPORT.md
Move-Item graphify-out/graph.html graph/v1_baseline/graph.html
```

For this evaluation, the default `graphify-out/` at `C:\tmp\gfxskilltest\` is sufficient.

### 4.4 Keep the graph current (ongoing)

After code changes, run AST-only re-extraction (no API cost):

```powershell
graphify update C:\tmp\gfxskilltest
```

---

## 5. What I Would Look For (Signal/Noise Analysis)

### 5.1 Expected signal (should be present)

- **clean_module.py nodes:** `SensorState` (StrEnum class), each member (`NOMINAL`, `STUCK_LEAN`, `STUCK_RICH`), `normalize_reading`, `describe_sensor`
- **Import edges:** `__init__.py` imports `calculate_ratio` from `dirty_module`; imports `SensorState` and `describe_sensor` from `clean_module`
- **Call edges:** `describe_sensor` calls `SensorState.value`
- **Rationale nodes:** The `# WHY: guard against negative sensor values` comment and the `normalize_reading` docstring should produce `file_type: "rationale"` nodes
- **Enum member sub-nodes:** `STUCK_LEAN`, `STUCK_RICH`, `NOMINAL` as children of `SensorState`
- **Community structure:** Two clear clusters expected — `code_fix` community and `wiki_fix` community, possibly with cross-edges where wiki text references code symbols

### 5.2 Expected noise / absent signal (should be absent or degraded)

- **Star import penalty:** `calculate_ratio` should have NO import edges from `math.*` symbols (tree-sitter gets no names from `from math import *`). This is the graphify-level consequence of the seeded rule-I violation.
- **No `__all__` penalty:** Without `__all__` in `__init__.py`, god-node ranking should be weaker for the `code_fix` package — the package entry-point nodes may be ranked lower or absent.
- **Missing `SUPPRESS_POST_CAT_TRIM` from code:** The wiki claims this enum member exists, but `clean_module.py` does not define it. If Pass 3 creates a node for `SUPPRESS_POST_CAT_TRIM`, it should have no edge to the `SensorState` enum (the real enum in code), which is a detectable inconsistency. If Pass 3 does NOT create the node (because it only links to code-defined symbols), that is also informative — it means the wiki assertion is invisible to the graph.
- **Missing type hint on `calculate_ratio`:** The function signature `def calculate_ratio(a, b)` should lack type-reference edges to any type nodes (compare with `normalize_reading` which has `raw: float, offset: float = 0.0`).

### 5.3 Seeded violation → graph consequence mapping

| Violation | Rule | File | Expected graph consequence |
|---|---|---|---|
| Missing `__all__` | A | `__init__.py` | Weaker god-node ranking; package surface not explicit in graph |
| `from math import *` | I | `dirty_module.py` | No import edges from `math` symbols to `calculate_ratio` |
| No type hints on `calculate_ratio` | T | `dirty_module.py` | No type-reference edges on function parameters/return |

---

## 6. Safety Guards (Pre-Flight Checklist)

Before running graphify, I would verify:

1. **Working directory is correct.** Am I in the right directory? `C:\tmp\gfxskilltest` not some other repo root.
2. **No existing `graphify-out/` to clobber.** If a previous run left artifacts, either archive them or confirm overwrite is intentional.
3. **Binary is accessible.** Confirm the graphify executable exists at the expected path.
4. **No accidental repo-root run on the main 4DLabV2 repo.** The `cd` command must target the test fixture, not the real project. A root run on 4DLabV2 would regenerate the 81.9k-node graph and violate the OBDLab guard.
5. **Corpus content is frozen.** No other process is editing the fixture files during the run.

### Guard: "graphify everything from the repo root" is safe HERE but dangerous THERE

The key distinction:
- **This test fixture** (`C:\tmp\gfxskilltest\`): 5 files, 77 lines. Running from root is fine.
- **The real 4DLabV2 repo** (`C:\Users\muto\claude\4DApp\4DLab\4DLabV2\`): Thousands of files. Running from root is forbidden per the OBDLab T-KG-OBD-2 task spec — it produced an 81.9k-node graph and violated the "no graph rebuild" rule.

The guard is **always check what directory you are in** before running `graphify update .`. The `.` is the dangerous character — it delegates scope to `$PWD`, and getting `$PWD` wrong is the recurring failure mode.

---

## 7. Summary of Approach

1. **Survey the corpus** — understand what's there (code + wiki)
2. **Decide scope** — repo root, because the corpus is trivially small and wiki-code cross-referencing is valuable for this evaluation
3. **Run graphify** — `graphify update C:\tmp\gfxskilltest` from PowerShell, using the known binary path
4. **Verify the output** — spot-check key symbols, confirm seeded violations produce expected graph degradations, check that wiki entities appear
5. **Query the graph** — test `query`, `explain`, and `path` subcommands against the output
6. **Document findings** — record what worked, what was missing, and whether the graph correctly reflects the seeded violations
