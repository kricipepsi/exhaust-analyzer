---
node_type: lab-index
lab: comlab
module: comlab
consumers:
  - "Vault/System-Map.md lab landing index"
drift_guards: []
tags: [comlab, finished, lab-index]
source: "labs/comlab/README.md"
---

# comlab — finished lab

> [!note] Mirror, not source
> These notes are copied from `labs/comlab/` at build time. Edit the lab and
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
`labs/comlab/graph/` (not copied into the vault).
