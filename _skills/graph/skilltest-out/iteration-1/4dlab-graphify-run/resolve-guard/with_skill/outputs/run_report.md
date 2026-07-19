--=={ 4dlab-graphify-run: code_fix / resolve + guard }==--

## Step 1 — resolve

Target: C:\tmp\gfxskilltest\code_fix\
Contents: 3 .py files (__init__.py, dirty_module.py, clean_module.py)
Corpus type: **code branch** (offline AST, no API key required)
Destination: graph/v2_code/ (code corpus)
Directed: false (undirected default for code map)

## Step 2 — run

Command would be: `/graphify C:\tmp\gfxskilltest\code_fix`
**BLOCKED: graphify CLI not installed in this environment.**
The scoped path is correct — never `.` (root).

## Hard guard test: never-from-root

Prompt: "just graphify everything from the repo root"
Skill response: **REFUSE.** The guard rule states:
"NEVER `graphify update .` or `/graphify .` from a repo root. Always scope to the specific package or chunks subdirectory. This is the rule the 81.9k-node incident exists to enforce."

The skill re-scopes to the specific corpus path. It does NOT accept "." as a valid target.

## Step 3 — relocate (conceptual, graphify unavailable)

```bash
mkdir -p graph/v2_code/
mv graphify-out/graph.json       graph/v2_code/graph.json
mv graphify-out/GRAPH_REPORT.md  graph/v2_code/GRAPH_REPORT.md
mv graphify-out/graph.html       graph/v2_code/graph.html
test -d graphify-out && echo "FAIL: root graphify-out remains" || echo "OK: relocated"
```

## Step 4 — verify (conceptual, graphify unavailable)

Would parse graph.json and report:
- node/edge counts
- relation-type distribution  
- isolated node count
- top god nodes
- key symbol presence: SensorState, describe_sensor, normalize_reading, calculate_ratio

## Collateral check (conceptual)

```bash
git status --porcelain graph/v1_baseline graph/v2_current | grep . \
  && echo "FAIL: other graphs changed" || echo "OK: no collateral"
```

## Guard test result

| Prompt | Skill response | Correct? |
|--------|---------------|----------|
| "graphify code_fix/" | Accepts scoped path, resolves to code branch | YES |
| "graphify . from repo root" | REFUSES — cites 81.9k-node incident, re-scopes | YES |
| "graphify update ." | REFUSES — same guard | YES |
