# labs/gaslab — GASLab v2 (Stage 1)

**Role:** idle (L1) + high-idle/2500rpm (L2) exhaust-gas chemistry emitter. Brettschneider lambda is
ground truth. Emits the `ChemicalSignature` (34-value surface) + DNA view across the JSON boundary.
**Build stage:** 1 — first to v2. Ledger: `tasks/PROGRESS.md`.
**Code origin (Q-A / D1):** fork of v1 `GASLab/gaslab/` lands here; v1 `GASLab/` is archived once this
v2 lab is built and green.
**Boundary:** no cross-lab Python imports — COMLab and `4dlabwired_v2` mirror the types locally.
**Signal/noise:** every field added here needs a named consumer in COMLab analytics or fault-atlas
routing. No consumer → it does not ship.

_Status: Migrated and verified green._
