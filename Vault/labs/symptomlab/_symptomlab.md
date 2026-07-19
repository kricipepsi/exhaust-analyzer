---
node_type: lab-index
lab: symptomlab
module: symptomlab
consumers:
  - "Vault/System-Map.md lab landing index"
drift_guards: []
tags: [symptomlab, finished, lab-index]
source: "labs/symptomlab/README.md"
---

# symptomlab — finished lab

> [!note] Mirror, not source
> These notes are copied from `labs/symptomlab/` at build time. Edit the lab and
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
`labs/symptomlab/graph/` (not copied into the vault).
