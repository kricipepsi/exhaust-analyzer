---
node_type: lab-index
lab: gaslab
module: gaslab
consumers:
  - "Vault/System-Map.md lab landing index"
drift_guards: []
tags: [gaslab, finished, lab-index]
source: "labs/gaslab/README.md"
---

# gaslab — finished lab

> [!note] Mirror, not source
> These notes are copied from `labs/gaslab/` at build time. Edit the lab and
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
`labs/gaslab/graph/` (not copied into the vault).
