---
name: 4dlab-graph
description: >
  DEPRECATED — retired 2026-06-09. Do NOT load this skill. Its responsibilities were split into
  three graphify-aligned skills after a documentation check found misaligned parts (a hard 18 KB
  chunk assumption, in-file vocab/entity markers, and an Option-3 patch that wrote fake EXTRACTED
  edges into graph.json). Use instead: 4dlab-code-prep (prepare .py source), 4dlab-wiki-prep
  (prepare .md wiki/prose), 4dlab-graphify-run (run graphify + verify, code or wiki). This file is
  kept only for historical reference and no longer triggers.
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
metadata:
  version: "1.0"
  argument-hint: "[operation] [module] — operations: prep, health, proof, criteria, patch, build, log"
  model: sonnet
  context: fork
---

> **⚠ DEPRECATED — retired 2026-06-09. Do not use.** Split into `4dlab-code-prep`,
> `4dlab-wiki-prep`, and `4dlab-graphify-run`. The proven-good parts (health/proof verification,
> the relation reference, the honesty rule, the proven wiki append-relations process) were carried
> into those skills; the misaligned parts (18 KB chunking, `KG_RELATION_VOCAB`/`ENTITY`/`TABLE`
> markers, the Option-3 EXTRACTED-edge patch) were dropped. Content below is historical only.

## Purpose

This skill manages the knowledge-graph lifecycle for 4DLab modules. It encodes the **proven GASLab workflow** — augmented chunked re-extraction + Option 3 deterministic patching — as a repeatable procedure for any module.

**Operations:**
- `prep [module]`     — **run first**: md-prep + KG-specific preparation of wiki files before extraction
- `health [module]`   — quick stats: nodes, edges, relation types, god nodes, isolated count
- `proof [module]`    — check proof-set edges from REEXTRACTION_SPEC against graph.json
- `criteria [module]` — run every numbered criterion (C1–C8) and report pass/fail
- `patch [module]`    — inject missing proof-set edges into graph.json (Option 3)
- `build [module]`    — orchestrate augmented chunked re-extraction
- `log [module]`      — write/update STEP1_VERIFICATION_LOG.md from latest state

**Recommended pipeline order:** `prep` → `build` → `proof` → `criteria` → `patch` → `log`

If no operation given, run `criteria` then `proof` as a combined health summary.

---

## Step 0 — Resolve the module root

Accept any of:
- A short name: `GASLab`, `DTCLab`, `DNALab`, `COMLab`, `OBDLab`
- A full path

**Base root:** `C:\Users\muto\claude\4DApp\4DLab\`

**Locate graphify-out** — try both path layouts (modules differ):
```bash
BASE="C:/Users/muto/claude/4DApp/4DLab"
MODULE="$1"   # e.g. GASLab

# Layout A (GASLab pattern)
GOUT_A="$BASE/$MODULE/graphify-out"
# Layout B (DTCLab pattern)
GOUT_B="$BASE/$MODULE/docs/wiki/graphify-out"

if [ -f "$GOUT_A/graph.json" ]; then
  GOUT="$GOUT_A"
  WIKI_DIR="$BASE/$MODULE/docs/wiki"
elif [ -f "$GOUT_B/graph.json" ]; then
  GOUT="$GOUT_B"
  WIKI_DIR="$BASE/$MODULE/docs/wiki"
else
  echo "No graph.json found for $MODULE. Run /4dlab-graph build $MODULE first."
  exit 1
fi

GRAPH_JSON="$GOUT/graph.json"
SPEC="$GOUT/REEXTRACTION_SPEC.md"
VLOG="$GOUT/STEP1_VERIFICATION_LOG.md"
```

---

## Step 0b — `prep` operation (run before `build`)

The `prep` operation transforms raw wiki `.md` files into graphify-ready input.
It runs in two phases so that extraction failures are prevented at the source,
not patched after the fact.

**When to run:** always before the first `build` on a new or heavily-edited wiki.
Re-run `prep` whenever a wiki section is added or restructured.

**Output locations:**
```
$GOUT/prepped/           — Phase 1 + Phase 2 cleaned wiki files
$GOUT/chunks/            — Phase 2 ≤18 KB chunks ready for graphify
$GOUT/REEXTRACTION_SPEC.md  — starter spec template (fill proof-set table)
```

---

### Phase 1 — Universal md-prep (structural cleanup)

Apply the seven md-prep rules to every wiki `.md` in `$WIKI_DIR`.
This eliminates tokenization failures before graphify ever sees the file.

```bash
MD_PREP="$BASE/_skills/doc/md-prep/scripts/optimize_markdown.py"
PREPPED_DIR="$GOUT/prepped"
mkdir -p "$PREPPED_DIR"

for WIKI in $(find "$WIKI_DIR" -name "*.md" \
    ! -path "*/graphify-out/*" ! -path "*/_archive*" ! -path "*/chunks/*"); do
  BASENAME=$(basename "$WIKI")
  python3 "$MD_PREP" "$WIKI" "$PREPPED_DIR/$BASENAME"
done
```

After the script runs, read each `*.report.json` in `$PREPPED_DIR/` and apply
the manual fixes flagged as `auto_fixed: false`:

- **R4 (math):** convert every ASCII fraction line to `$$ LaTeX $$` + inline
  fallback. GASLab formula example:
  ```
  $$\lambda = \frac{[CO_2] + [O_2]}{[CO] + [HC]}$$
  Inline fallback: lambda = ([CO2] + [O2]) / ([CO] + [HC])
  ```
- **R6 (diagrams):** replace box-drawing characters with numbered declarative
  sequences. Keep Mermaid for graphs with more than 3 nodes.
- **R7 (fences):** tag every bare ` ``` ` with the correct language.

Do not change technical content, thresholds, or domain facts during Phase 1.

---

### Phase 2 — KG ingestion preparation

Phase 2 takes the Phase 1 output and restructures it so graphify extracts
domain-specific edges rather than generic fallback relations.

#### 2a — Chunk into ≤18 KB files

Graphify truncates inputs above ~20 KB. Split each prepped wiki on `##`
boundaries, writing chunks to `$GOUT/chunks/`:

```python
import re, os, pathlib

CHUNK_MAX = 18_000  # bytes

def chunk_wiki(input_path: str, out_dir: str, basename: str):
    text = pathlib.Path(input_path).read_text(encoding="utf-8")
    sections = re.split(r'(?=^## )', text, flags=re.MULTILINE)
    current, chunk_n = '', 0
    os.makedirs(out_dir, exist_ok=True)
    for section in sections:
        if len((current + section).encode()) > CHUNK_MAX and current:
            chunk_n += 1
            out = os.path.join(out_dir, f"chunk_{chunk_n:02d}_{basename}")
            pathlib.Path(out).write_text(current, encoding="utf-8")
            print(f"  chunk_{chunk_n:02d}: {len(current.encode())} B → {out}")
            current = section
        else:
            current += section
    if current:
        chunk_n += 1
        out = os.path.join(out_dir, f"chunk_{chunk_n:02d}_{basename}")
        pathlib.Path(out).write_text(current, encoding="utf-8")
        print(f"  chunk_{chunk_n:02d}: {len(current.encode())} B → {out}")
```

Run for every file in `$PREPPED_DIR/`.

#### 2b — Embed relation vocabulary header

Prepend this comment block to **every chunk file**. It tells graphify which
relations to prefer over generic fallbacks:

```markdown
<!-- KG_RELATION_VOCAB
Preferred relations (use instead of generic conceptually_related_to):
  routes_to         — DTC range routes diagnosis to this tag
  gated_by          — entity activates only when this DNA flag is set
  monitored_by      — Mode 06 MID monitors this parameter
  escalates_to      — condition worsens, routes here
  tailpipe_signature_identical_to — same five-gas pattern, different differentiator
  differential_diagnosis_of — explicitly distinct from X in that…
  disambiguated_by  — test that splits two otherwise-identical faults
  sub_mode_of       — row in sub-mode table of the parent fault
  confirmed_by      — test that confirms this fault
  enumerates        — enum type → each of its values
  overrides         — rule overrides verdict of this node
  suppresses        — node suppresses verdicts of this node
  mirrors_contract_in — single source of truth cross-reference
  evaluates_state_of — enum evaluates state of this component
  describes         — structural/documentary relationship
  maps_to           — DTC code maps to this concept
NEVER use semantically_similar_to between two domain concept nodes.
-->
```

#### 2c — Mark entity candidates

For each key domain concept defined in the wiki (usually bolded or in a
vocabulary table), add an inline marker immediately before its definition:

```markdown
<!-- ENTITY: Brettschneider Lambda [formula] -->
**Brettschneider Lambda (λ):** the reference lambda equation used by GASLab…
```

Marker format: `<!-- ENTITY: Name [type] -->` where type is one of:
`formula`, `enum_value`, `component`, `fault_state`, `threshold`, `gate`.

Apply markers only where the concept is **defined**, not every mention.

#### 2d — Reformat causal/routing tables

Tables that encode "if X then Y" logic are the primary source of edges.
Reformat them so graphify sees an explicit "Source → Target | Relation" pattern:

**Before:**
```markdown
| HC (ppm) | CO (%) | O₂ (%) | State |
|---|---|---|---|
| > 1200 | > 4.0 | < 0.5 | RICH_MISFIRE |
```

**After (add mapping comment row):**
```markdown
<!-- TABLE: fault_state_thresholds SOURCE=GasReading TARGET=ChemicalState RELATION=evaluates_state_of -->
| HC (ppm) | CO (%) | O₂ (%) | State |
|---|---|---|---|
| > 1200 | > 4.0 | < 0.5 | RICH_MISFIRE |
```

Add a `<!-- TABLE: ... -->` comment above every table that encodes a rule,
threshold map, or routing decision. Leave narrative/reference tables unchanged.

#### 2e — Generate REEXTRACTION_SPEC template

Write `$GOUT/REEXTRACTION_SPEC.md` if it does not already exist:

```markdown
# REEXTRACTION_SPEC — [MODULE]

**Generated:** [date]
**Wiki source:** [wiki files listed]
**Chunks:** [N chunks in $GOUT/chunks/]

---

## §1 — Extraction prompt addendum

Prepend to the graphify extraction prompt:

> [paste the KG_RELATION_VOCAB block here]
>
> TABLE ROW → EDGE RULE: for every table with a SOURCE/TARGET/RELATION
> comment, each data row is one edge. Map columns accordingly.
>
> ENTITY MARKERS: nodes with `<!-- ENTITY: Name [type] -->` comments are
> named entities — always create a node for them.
>
> TRUNCATION CANARY: confirm nodes appear from the final section of the
> wiki (§N). If the last section is absent from extracted nodes, report
> truncation — do not silently omit it.

---

## §2 — Proof-set edges

Fill this table after first extraction. Each row is one expected edge.
Run `/4dlab-graph proof [module]` to check.

| Source → Target | Relation | Wiki anchor |
|---|---|---|
| `` → `` | `` | §N |

**Pass threshold:** ≥ N/M

---

## §3 — Criteria

| # | Criterion | Condition | Threshold |
|---|---|---|---|
| C1 | Vocabulary surface | nodes from vocab file | ≥ 22 |
| C2 | No generic relations | semantically_similar_to between domain nodes | 0 |
| C3 | Proof-set recovery | found / total | ≥ threshold |
| C4 | Isolated nodes | non-leaf isolated | < 5 |
| C5 | Cross-file edges | edges across source_file boundaries | ≥ 10 |
```

If `REEXTRACTION_SPEC.md` already exists, **do not overwrite** — append a
`## §N — Prep run [date]` section noting what Phase 2 changed.

---

### Phase 2 completion check

After Phase 2, verify:

```bash
# Chunk count and sizes
ls -la "$GOUT/chunks/"
# All chunks should be ≤ 18 000 bytes
for f in "$GOUT/chunks/"*.md; do
  SIZE=$(wc -c < "$f")
  [ "$SIZE" -gt 18000 ] && echo "OVERSIZE: $f ($SIZE bytes)"
done

# Relation vocab header present in all chunks
grep -L "KG_RELATION_VOCAB" "$GOUT/chunks/"*.md | wc -l
# Should be 0

# REEXTRACTION_SPEC exists
[ -f "$GOUT/REEXTRACTION_SPEC.md" ] && echo "SPEC OK" || echo "SPEC MISSING"
```

Report any failures before proceeding to `build`.

---

## Step 1 — `health` operation

Load graph.json and print a summary. Use Python for JSON parsing.

```python
import json, sys, collections

with open(GRAPH_JSON) as f:
    g = json.load(f)

nodes = g.get('nodes', [])
links = g.get('links', [])
hyperedges = g.get('hyperedges', [])
communities = sorted(set(n.get('community', -1) for n in nodes))

# Relation type distribution
rels = collections.Counter(e.get('relation','?') for e in links)

# God nodes (highest degree)
degree = collections.Counter()
for e in links:
    degree[e['source']] += 1
    degree[e['target']] += 1

# Isolated nodes (degree 0, excluding hyperedge members)
he_members = set()
for he in hyperedges:
    he_members.update(he.get('members', []))
isolated = [n['id'] for n in nodes if degree[n['id']] == 0 and n['id'] not in he_members]

print(f"Nodes: {len(nodes)}  Links: {len(links)}  Hyperedges: {len(hyperedges)}")
print(f"Communities: {len(communities)}")
print(f"Isolated (excl. hyperedge): {len(isolated)}")
print()
print("Relation type distribution:")
for rel, count in rels.most_common():
    print(f"  {count:4d}  {rel}")
print()
print("God nodes (top 10 by degree):")
for node_id, deg in degree.most_common(10):
    label = next((n['label'] for n in nodes if n['id'] == node_id), node_id)
    print(f"  {deg:4d}  {label}")
print()
if isolated:
    print("Isolated nodes:")
    for nid in isolated:
        label = next((n['label'] for n in nodes if n['id'] == nid), nid)
        print(f"  - {label}  [{nid}]")
```

**Interpret findings:**
- Flag `conceptually_related_to` or `semantically_similar_to` in the relation list — these are signs the extractor used generic fallback relations instead of domain-specific ones. Each such edge is a candidate for relabelling.
- Isolated nodes > 10 (excluding leaf enums and Category-C singletons) = extraction gap.
- God node with > 25 edges and no `enumerates` = unexpected hub, investigate.

---

## Step 2 — `proof` operation

Parse the proof-set table from REEXTRACTION_SPEC.md and check each edge against graph.json.

```python
import json, re

# Parse proof-set edges from REEXTRACTION_SPEC.md
# The table has columns: Source → Target | Relation | Wiki anchor
# Detect table by looking for "| Source" or "| `" header lines

with open(SPEC) as f:
    spec_text = f.read()

with open(GRAPH_JSON) as f:
    g = json.load(f)

links = g.get('links', [])
nodes = g.get('nodes', [])

# Build label→id and id→label maps
label_to_ids = {}
for n in nodes:
    label_to_ids.setdefault(n['label'].lower(), []).append(n['id'])
    label_to_ids.setdefault(n['norm_label'].lower() if 'norm_label' in n else n['label'].lower(), []).append(n['id'])

# Edge set: (source_id, target_id, relation) and also (source_label, target_label, relation)
edge_set_ids = set((e['source'], e['target'], e['relation']) for e in links)
# Also build loose match on label substrings for fuzzy check
edge_tuples = [(e['source'], e['target'], e['relation']) for e in links]

def find_node_ids(label_fragment):
    """Find node IDs whose label contains the fragment (case-insensitive)."""
    frag = label_fragment.lower().strip('`').strip()
    return [n['id'] for n in nodes if frag in n['label'].lower()]

# Parse proof-set table rows  
# Pattern: | `Source` → `Target` | `relation` | wiki anchor |
# OR: | Source → Target | Relation | anchor |
proof_edges = []
in_table = False
for line in spec_text.split('\n'):
    # Detect proof-set table section
    if '| Source' in line or '|---|' in line or ('→' in line and '|' in line and '`' in line):
        in_table = True
    if in_table and line.strip().startswith('|') and '→' in line:
        # Extract source, target, relation from table row
        parts = [p.strip() for p in line.split('|') if p.strip()]
        if len(parts) >= 2:
            arrow_part = parts[0]
            # Handle "Source → Target" in first column
            if '→' in arrow_part:
                src_raw, tgt_raw = arrow_part.split('→', 1)
                src_raw = src_raw.strip().strip('`')
                tgt_raw = tgt_raw.strip().strip('`')
                relation = parts[1].strip().strip('`') if len(parts) > 1 else ''
                anchor = parts[2].strip() if len(parts) > 2 else ''
                proof_edges.append({'src': src_raw, 'tgt': tgt_raw, 'rel': relation, 'anchor': anchor})

if not proof_edges:
    print("Could not parse proof-set table from REEXTRACTION_SPEC.md.")
    print("Verify the table format has 'Source → Target | Relation | Anchor' columns.")
else:
    print(f"Proof-set: {len(proof_edges)} edges defined")
    print()
    missing = []
    found = []
    for pe in proof_edges:
        src_ids = find_node_ids(pe['src'])
        tgt_ids = find_node_ids(pe['tgt'])
        matched = False
        for e in links:
            src_match = e['source'] in src_ids or pe['src'].lower() in e['source'].lower()
            tgt_match = e['target'] in tgt_ids or pe['tgt'].lower() in e['target'].lower()
            rel_match = pe['rel'].lower() in e['relation'].lower() if pe['rel'] else True
            if src_match and tgt_match and rel_match:
                matched = True
                break
        if matched:
            found.append(pe)
        else:
            missing.append(pe)

    print(f"FOUND:   {len(found)}/{len(proof_edges)}")
    print(f"MISSING: {len(missing)}/{len(proof_edges)}")
    if missing:
        print()
        print("Missing edges (need Option 3 patch or re-extraction):")
        for pe in missing:
            anchor = f"  [{pe['anchor']}]" if pe['anchor'] else ''
            print(f"  ✗  {pe['src']}  --{pe['rel']}-->  {pe['tgt']}{anchor}")
    if found:
        print()
        print("Found edges:")
        for pe in found:
            print(f"  ✓  {pe['src']}  --{pe['rel']}-->  {pe['tgt']}")
```

**Pass threshold:** read from spec — typically ≥ 20/26 or ≥ 22/25. If the spec states a threshold, show pass/fail against it.

---

## Step 3 — `criteria` operation

Run each numbered criterion. Parse criterion definitions from REEXTRACTION_SPEC.md §3 (or §5 for DTCLab). Execute each check as a Python/bash test.

**Standard criteria across all 4DLab modules:**

### C-VOCAB — Vocabulary surface (C1 for both labs)
Count how many vocabulary terms from the wiki appear as nodes in graph.json.
```bash
# Read first vocab file found in wiki dir
VOCAB_FILE=$(find "$WIKI_DIR" -name "*VOCABULARY*" -o -name "*vocabulary*" | head -1)
# Count distinct concepts defined in the vocab file
# Criterion: typically ≥ 22 expected terms are present as nodes
```

### C-GENERIC-RELATIONS — No generic fallback relations between domain nodes
```python
BAD_RELATIONS = {'semantically_similar_to', 'conceptually_related_to'}
bad = [(e['source'], e['target'], e['relation']) for e in links if e['relation'] in BAD_RELATIONS]
# PASS if 0 bad relations between two domain nodes (non-structural pairs)
```

### C-PROOFSET — Proof-set recovery (run Step 2, check threshold)
```
# Threshold from spec: ≥ N/M. PASS if found >= threshold.
```

### C-ISOLATED — Isolated node count
```python
# PASS if non-leaf, non-Category-C isolated nodes < 5
# Leaf vocab nodes: enum members reached only via 'enumerates' edges
# Category-C singletons: explicitly listed in REEXTRACTION_SPEC §3/§5
```

### C-CROSSFILE — Cross-file coherence edges
```python
cross_file = [e for e in links 
              if e.get('source_file','') != e.get('source_file','')
              # OR: source node's source_file ≠ target node's source_file
             ]
# PASS if cross-file edges ≥ threshold (typically ≥ 10 or ≥ 21)
```

### Module-specific criteria (parsed from spec):
Read the REEXTRACTION_SPEC §3/§5 criteria section. For each criterion found:
- Parse the criterion name, condition, and pass threshold
- Run the appropriate check (grep on graph.json, Python count, etc.)
- Report PASS / FAIL with the actual value vs threshold

**DTCLab-specific:**
- C3: 17/17 routing tags have an incoming `routes_to` edge
- C4: 4/4 DNA gates present as `gated_by` edges to `DtcEmissionsView` fields
- C5: ≥3 MID groups as distinct nodes (hex tokens like `$A1`, `$A9`, `$21`)

**GASLab-specific:**
- Bridge preservation: `Exhaust Gas Triangle` betweenness ≥ 0.15, bridges ≥ 3 communities
- `NORMAL_OPERATION` node degree ≥ 3

**Report format:**
```
--=={ criteria: MODULE }==--

  C1  Vocabulary surface      PASS (22/22)
  C2  DTC code class          PASS
  C3  Routing-tag fan-out     FAIL (5/17)  — 12 tags have no incoming routes_to edge
  C4  DNA gate links          FAIL (0/4)   — no gated_by edges to DtcEmissionsView fields
  C5  MID group nodes         FAIL (0)     — hex token entities not extracted
  C6  Cross-file coherence    PASS (21 edges)
  Proof-set                   PASS (23/26)

  Overall: 4/6 PASS  — NEEDS ATTENTION

  Next action: Run /4dlab-graph patch MODULE for proof-set gaps.
               C3/C4/C5 require augmented re-extraction: /4dlab-graph build MODULE
```

---

## Step 4 — `patch` operation (Option 3 — deterministic post-extraction patch)

This is the proven GASLab fallback: inject missing proof-set edges directly into graph.json.

**Only apply edges where:**
1. Both source and target nodes already exist in graph.json
2. The edge is in the proof-set with a specific wiki anchor (EXTRACTED, not inferred)
3. The edge does not already exist (after fuzzy matching)

```python
import json, datetime

with open(GRAPH_JSON) as f:
    g = json.load(f)

links = g.get('links', [])
nodes = g.get('nodes', [])

# [Run Step 2 proof check first to get `missing` list]

patches_applied = []
patches_skipped = []

for pe in missing:
    src_ids = find_node_ids(pe['src'])
    tgt_ids = find_node_ids(pe['tgt'])

    if not src_ids:
        patches_skipped.append({'edge': pe, 'reason': f"source node not found: {pe['src']}"})
        continue
    if not tgt_ids:
        patches_skipped.append({'edge': pe, 'reason': f"target node not found: {pe['tgt']}"})
        continue

    # Use the best matching node (exact match preferred)
    src_id = src_ids[0]
    tgt_id = tgt_ids[0]

    new_edge = {
        "relation": pe['rel'],
        "confidence": "EXTRACTED",
        "confidence_score": 1.0,
        "source_file": "option3_patch",
        "source_location": pe['anchor'],
        "weight": 1.0,
        "_src": src_id,
        "_tgt": tgt_id,
        "source": src_id,
        "target": tgt_id,
        "_patched_at": datetime.datetime.now().isoformat(),
        "_patch_reason": "proof-set edge missing after extraction; deterministic patch"
    }
    links.append(new_edge)
    patches_applied.append({'edge': pe, 'src_id': src_id, 'tgt_id': tgt_id})

g['links'] = links

# Write back
with open(GRAPH_JSON, 'w') as f:
    json.dump(g, f, indent=2)

print(f"Option 3 patch complete.")
print(f"  Applied: {len(patches_applied)} edges")
print(f"  Skipped: {len(patches_skipped)} (node not found in graph)")
print()
for p in patches_applied:
    pe = p['edge']
    print(f"  + {pe['src']} --{pe['rel']}--> {pe['tgt']}  [{pe['anchor']}]")
for p in patches_skipped:
    print(f"  ✗ SKIP: {p['reason']}")
print()
print("IMPORTANT: Run graphify community rebuild after patching:")
print("  cd MODULE_ROOT && graphify rebuild graphify-out/")
```

**After patching:** remind the user to run `graphify rebuild` or equivalent to regenerate communities, GRAPH_REPORT.md, and wiki articles from the updated graph.json.

---

## Step 5 — `build` operation (augmented chunked re-extraction)

This encodes the proven approach from GASLab T-PREP-1. Use when C3/C4/C5 fail — meaning the extractor truncated or skipped tables.

**Root cause diagnostic first:**
```bash
# Check how far the extractor got — look at the cache files
CACHE_DIR="$GOUT/cache/semantic"
if [ -d "$CACHE_DIR" ]; then
    echo "Cache files:"
    ls -la "$CACHE_DIR/"
    echo ""
    echo "Last section extracted from each wiki:"
    for f in "$CACHE_DIR"/*.json; do
        echo "--- $f ---"
        python3 -c "
import json
with open('$f') as fp:
    c = json.load(fp)
# Find the last section heading that appears in the nodes
nodes = c.get('nodes',[]) if isinstance(c,dict) else []
print(f'  Nodes in cache: {len(nodes)}')
"
    done
fi
```

**Chunking strategy (prevents tail truncation):**
```bash
# Split each wiki file into ≤20KB chunks before extraction
# This is the key fix for the §12 truncation problem

WIKI_FILES=$(find "$WIKI_DIR" -name "*.md" ! -path "*/graphify-out/*" ! -path "*/_archive*")

for WIKI in $WIKI_FILES; do
    BASENAME=$(basename "$WIKI" .md)
    SIZE=$(wc -c < "$WIKI")
    echo "$BASENAME: ${SIZE} bytes"
    if [ "$SIZE" -gt 20000 ]; then
        echo "  → NEEDS CHUNKING (>${SIZE} bytes)"
        # Split on section headers (## or ###)
        python3 -c "
import re, os
with open('$WIKI') as f:
    content = f.read()
# Split on top-level sections
sections = re.split(r'(?=^## )', content, flags=re.MULTILINE)
print(f'  Sections: {len(sections)}')
total = 0
chunk_n = 0
current_chunk = ''
for s in sections:
    if len(current_chunk) + len(s) > 18000 and current_chunk:
        chunk_n += 1
        out_path = f'$GOUT/chunk_{chunk_n}_$BASENAME.md'
        with open(out_path, 'w') as fp:
            fp.write(current_chunk)
        print(f'  Chunk {chunk_n}: {len(current_chunk)} bytes → {out_path}')
        current_chunk = s
    else:
        current_chunk += s
if current_chunk:
    chunk_n += 1
    out_path = f'$GOUT/chunk_{chunk_n}_$BASENAME.md'
    with open(out_path, 'w') as fp:
        fp.write(current_chunk)
    print(f'  Chunk {chunk_n}: {len(current_chunk)} bytes → {out_path}')
"
    fi
done
```

**Augmented extraction prompt rules to prepend** (bake into graphify config or pass as --prompt-addendum):

```
AUGMENTED EXTRACTION RULES — prepend to your extraction prompt:

1. TABLE ROW → EDGE RULE:
   For every markdown table where the heading row implies a source→target relationship:
   - Each data row becomes an edge
   - Row cells map to: source entity, target entity, relation (from column header)
   - E.g., a routing table with columns "DTC Range | Routes to Tag":
     each row → edge(DTC_range_node --routes_to--> tag_node)

2. DNA GATE PHRASES:
   When prose says "X is gated by Y", "X requires Y to be set",
   "X only fires if DNA.Y is present" → edge(X --gated_by--> Y)

3. HEX TOKEN ENTITIES:
   Tokens matching $XX or $XXYY (e.g., $A1, $A9, $21, $01) are named entities.
   Create a node for each distinct hex token with type=MID_group.
   When prose says "MID $A1 monitors Y" → edge($A1_node --monitored_by--> Y)

4. SECTION COVERAGE CANARY:
   Confirm nodes appear from §13 and §14 (DTC_WIKI). If you reach end of
   input without seeing §13/§14 content, you have been truncated — report it.

5. RELATION VOCABULARY — prefer these over generic relations:
   routes_to, gated_by, monitored_by, escalates_to, tailpipe_signature_identical_to,
   differential_diagnosis_of, disambiguated_by, sub_mode_of, confirmed_by,
   enumerates, overrides, suppresses, mirrors_contract_in, describes, maps_to,
   evaluates_state_of, simplification_of, mistaken_for_via_<rule>, paired_under_<parent>
   Use conceptually_related_to ONLY as last resort when none of the above fit.
   NEVER use semantically_similar_to between two domain concept nodes.
```

**Run the extraction:**
```bash
cd "$BASE/$MODULE"

# Option A: graphify CLI with chunked inputs
graphify --wiki "$GOUT" --prompt-file "$GOUT/augmented_prompt.md" --max-tokens 128000

# Option B: if graphify supports directory extraction with chunking
graphify --wiki docs/wiki/ --chunk-size 18000 --prompt-file "$GOUT/augmented_prompt.md"

# Verify §13/§14 nodes appeared (truncation canary)
python3 -c "
import json
with open('$GRAPH_JSON') as f:
    g = json.load(f)
nodes = g.get('nodes',[])
# Check for nodes sourced from late sections
late = [n for n in nodes if any(x in n.get('source_location','') for x in ['§13','§14','§15'])]
print(f'Late-section nodes (§13/§14/§15): {len(late)}')
for n in late:
    print(f'  {n[\"label\"]}  [{n[\"source_location\"]}]')
if not late:
    print('WARNING: No §13/§14 nodes found. Truncation still occurring.')
    print('Try: split wiki manually and run extraction on each part.')
"
```

**If chunked extraction still misses C3/C4/C5:** fall through to `patch` operation (Option 3). The proven GASLab pattern shows Option 3 is safe and sufficient for proof-set edges that have exact wiki anchors.

**Escalation rule (from DTCLab prompt):**
> If C3/C4/C5 still fail AFTER both the augmented+chunked pass AND the Option 3 patch, STOP. That is a graphify chunk-merge bug. Surface it with the failing cache file. Do NOT run a third same-shape extraction.

---

## Step 6 — `log` operation

Generate or update STEP1_VERIFICATION_LOG.md.

```
# {MODULE} Bootstrap Step 1 — Verification Log

**Run date:** {today}
**Spec:** `{GOUT}/REEXTRACTION_SPEC.md`
**Graph state:** {N} nodes · {M} links · {H} hyperedges · {C} communities

---

## §1 — Option 3 deterministic edge additions

| # | Edge | Action | Reason |
|---|---|---|---|
{for each patched edge: | N | src --rel--> tgt | Applied / Skipped | reason |}

**Net edges added by §1:** {count}

---

## §2 — Rebuild

- Community detection: same parameters as prior pass; not tuned.
- GRAPH_REPORT.md: regenerated.
- Per-community wiki articles: {N} regenerated.

---

## §3 — Criteria verification

| # | Criterion | Result | Detail |
|---|---|---|---|
{for each criterion: | C1 | name | PASS/FAIL | detail |}

**Final: {N}/{M} PASS**

---

## §4 — Spot-check (random.seed=42, 5 edges)

{For 5 randomly sampled edges from the latest extraction:}
| # | Edge | Citation | Verdict |
|---|---|---|---|
{rows}

**Spot-check result: N/5 PASS**

---

## §5 — Step 1 status

| Gate | Result |
|---|---|
| Criteria | N / M PASS |
| Spot-check | 5 / 5 PASS |

**Step 1 {complete / ESCALATE}.**
```

---

## Domain Knowledge Reference

### 4DLab graphify-out structure
```
graph.json keys: directed, multigraph, graph, nodes, links, hyperedges
nodes[]: {id, label, file_type, source_file, source_location, community, norm_label}
links[]: {relation, confidence, confidence_score, source_file, source_location,
          weight, source, target, _src, _tgt}
hyperedges[]: {label, members[], extraction_type, confidence_score}
```

### Approved domain relation vocabulary
| Relation | Meaning |
|---|---|
| `routes_to` | DTC range routes diagnosis to this tag |
| `gated_by` | Entity only activates when this DNA flag is set |
| `monitored_by` | Mode 06 MID monitors this parameter |
| `escalates_to` | If condition worsens, routes here |
| `tailpipe_signature_identical_to` | Same five-gas pattern, different non-gas differentiator |
| `differential_diagnosis_of` | Explicitly "distinct from X in that…" |
| `disambiguated_by` | Test that splits two otherwise-identical faults |
| `sub_mode_of` | Row in a sub-mode table of the parent fault |
| `confirmed_by` | Test that confirms this fault |
| `enumerates` | Enum type → each of its values |
| `overrides` | Rule overrides verdict of this node |
| `suppresses` | Node suppresses verdicts of this node |
| `mirrors_contract_in` | Single source of truth cross-reference |
| `evaluates_state_of` | Enum evaluates state of this component |
| `describes` | Structural/documentary relationship |
| `maps_to` | DTC code maps to this concept |
| `paired_under_<parent>` | Two siblings of the same parent concept |
| `mistaken_for_via_<rule>` | Two nodes the named rule disentangles |

### Bad relations (signal extraction failure)
- `semantically_similar_to` between two domain nodes → relabel using table above
- `conceptually_related_to` between two domain nodes → relabel or investigate

### Module graphify-out paths
| Module | graph.json location |
|---|---|
| GASLab | `GASLab/graphify-out/graph.json` |
| DTCLab | `DTCLab/docs/wiki/graphify-out/graph.json` |
| Others | Check both layouts (Step 0) |

### Proven workflow (GASLab T-PREP-1 reference)
0. Run `prep` → clean wiki files, chunk to ≤18 KB, embed relation vocab, generate spec template
1. Run `build` → augmented chunked extraction using prepped chunks
2. Run `criteria` → identify failing criteria
3. If C-GENERIC-RELATIONS fails → relabel edges (Option 3 variant)
4. If proof-set < threshold → run `patch` for edges where both nodes exist
5. If C-TRUNCATION fails (§13/§14 nodes absent) → re-run `prep` (check chunking) then `build`
6. After any patch → remind user to run `graphify rebuild`
7. Run `criteria` again to confirm all pass
8. Run `log` to write STEP1_VERIFICATION_LOG.md

### Escalation rule
If a criterion still fails after:
- One augmented chunked extraction pass, AND
- One Option 3 deterministic patch

→ STOP and report. Do not loop. Surface the failing cache file. This is a graphify infrastructure bug, not a wiki or prompt issue.

---

## Output conventions

- Use `--=={ 4dlab-graph: MODULE / OPERATION }==--` as the section header
- Report criteria with ✓ PASS / ✗ FAIL and the actual value vs threshold
- For missing proof-set edges always include the wiki anchor so the user can verify
- Never invent edges — only patch edges that are in the proof-set with an anchor
- After any graph.json write: remind user to rebuild communities
