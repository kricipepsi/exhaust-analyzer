# ADR-0002: No cross-lab Python imports — mirror types over JSON

**Status:** Accepted

**Context.** COMLab consumes types that originate in GASLab, OBDLab, DTCLab, and
VINLab/DNALab. The tempting shortcut is `from obdlab import OBDLiveDataPayload`.
That couples release cycles: a change inside any producer would break COMLab's
import graph, and the four labs could no longer evolve independently.

**Decision.** COMLab performs **zero** cross-lab Python imports. Every producer
type it needs is **mirrored locally** as a Pydantic model in
`comlab/schemas/ingestion.py` (e.g. `GasLabPayload`, `OBDLiveDataPayload`,
`DTCLabPayload`, `FreezeFrameRecord`, `Mode06MonitorResult`) or as a local enum in
`comlab/schemas/vocabulary.py`. The cross-lab contract is the **JSON values**, not
the Python classes; duplicate enum declarations across labs are intentional and
accepted. The single sanctioned non-lab import is `registry.integration_shim`
(`fault_atlas_router.py`), a one-way dependency on the repo-root `registry/`
package — not a sibling lab.

**Consequences.**
- Positive: each lab is a fully isolated codebase; the boundary is a typed JSON
  document validated at COMLab's ingestion gate.
- Positive: enforceable mechanically (an import-isolation check fails on any
  `from gaslab|obdlab|dtclab|dnalab import …`).
- Negative: mirrored enums/shapes are declared twice and can drift — which is why
  a contract change is a coordinated cross-lab change (SEMANTIC_CONTRACT §10).
- Neutral: COMLab validates every inbound payload against its own mirror, so a
  producer that violates the contract is rejected with a stable `ERR-CONTRACT-*`.

**Alternatives considered.**
1. *A shared `common` package of contract types.* Rejected — reintroduces the
   shared release cadence the architecture exists to avoid.
2. *Generate mirrors from one schema at build time.* Deferred — adds a build step;
   the hand-maintained mirror plus the ingestion gate is sufficient at this scale.

**References.** `wiki/02_lab_input_contract.md`; `docs/Vocabulary/SEMANTIC_CONTRACT.md`
§1; `comlab/schemas/ingestion.py`; `pyproject.toml` (`[tool.pytest] pythonpath`
note on the sanctioned registry dependency); project `CLAUDE.md` boundary rule.
