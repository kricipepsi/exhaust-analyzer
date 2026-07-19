---
node_type: lab-index
lab: dnalab
module: dnalab
consumers:
  - "Vault/System-Map.md lab landing index"
drift_guards: []
tags: [dnalab, finished, lab-index]
source: "labs/dnalab/README.md"
---

# dnalab — finished lab

> [!note] Mirror, not source
> These notes are copied from `labs/dnalab/` at build time. Edit the lab and
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
`labs/dnalab/graph/` (not copied into the vault).
