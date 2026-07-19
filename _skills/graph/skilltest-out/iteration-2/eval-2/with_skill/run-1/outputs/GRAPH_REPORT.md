# Graph Report - code_fix  (2026-06-09)

## Corpus Check
- 4 files · ~196 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 16 nodes · 14 edges · 4 communities (3 shown, 1 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 3|Community 3]]

## God Nodes (most connected - your core abstractions)
1. `SensorState` - 2 edges
2. `normalize_reading()` - 2 edges
3. `describe_sensor()` - 2 edges
4. `Normalize O2 voltage into a 0..1 range.` - 1 edges
5. `Map a sensor state enum to the display string.` - 1 edges
6. `# WHY: clamp sensor noise before state classification.` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Communities (4 total, 1 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.33
Nodes (5): normalize_reading(), Normalize O2 voltage into a 0..1 range., # WHY: clamp sensor noise before state classification., SensorState, StrEnum

## Knowledge Gaps
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `describe_sensor()` connect `Community 3` to `Community 0`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **What connects `Normalize O2 voltage into a 0..1 range.`, `Map a sensor state enum to the display string.`, `# WHY: clamp sensor noise before state classification.` to the rest of the system?**
  _3 weakly-connected nodes found - possible documentation gaps or missing edges._