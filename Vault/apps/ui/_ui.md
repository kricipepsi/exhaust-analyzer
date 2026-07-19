---
node_type: lab-index
lab: ui
module: ui
consumers:
  - "Vault/System-Map.md lab landing index"
drift_guards: []
tags: [ui, finished, lab-index]
source: "labs/ui/README.md"
---

# ui — finished lab

> [!note] Mirror, not source
> These notes are copied from `labs/ui/` at build time. Edit the lab and
> rebuild — edits made here are overwritten on the next build.

## Module map
![[modules.base#All modules]]

## Design spine
PRD → HLD → LLD → DLD → code. See the design docs in `docs/`.

## Vocabulary
Shared vocabulary notes live in `_vocabulary/`: [[OBD_VOCABULARY]] and [[GAS_VOCABULARY]].

## Signal/noise audit
Every framed note must name a downstream consumer.
![[consumers.base#Consumer audit]]

## Coverage (drift guards)
![[drift-guards.base#Coverage]]

## Code & tests
Browse `code/` and `tests/`. The canonical graph stays at
`labs/ui/graph/` (not copied into the vault).
