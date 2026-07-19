---
node_type: lab-index
lab: obdlab
module: obd_live_lab
consumers:
  - "Vault/System-Map.md lab landing index"
drift_guards: []
tags: [obdlab, finished, lab-index]
source: "labs/obdlab/README.md"
---

# obdlab — finished lab

> [!note] Mirror, not source
> These notes are copied from `labs/obdlab/` at build time. Edit the lab and
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
`labs/obdlab/graph/` (not copied into the vault).
