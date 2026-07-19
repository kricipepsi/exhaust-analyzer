> **Context:** VINLab ADR v2.0 (2026-06-12) | Module: VINLab | Section: ADR-0001: Offline runtime — bake all reference data into vinlab/data/ | Parent document: ADR_VINLab.md

## ADR-0001: Offline runtime — bake all reference data into `vinlab/data/`

**Status:** Accepted (VINLab hard constraint)

### Context

The decode must run on a technician's device with no guaranteed connectivity. The full
reference corpus lives in MySQL (`mysql_data/`, ~484 MB), but a runtime MySQL/network
dependency is unacceptable on the shop floor.

### Decision

All runtime reference data is baked into `vinlab/data/` at build time: `wmi.csv`,
`years.csv`, `vds_engine_map.csv`, and a small SQLite `vref.db`. The runtime makes
**zero** network and **zero** MySQL calls. `mysql_data/` is retained for build-time
extraction only and is a Track-2 removal candidate.

### Consequences

- **Positive:** decode works fully offline and deterministically.
- **Positive:** tests run without a database server (skip when `vref.db` is absent).
- **Negative:** reference data is a build-time snapshot — staleness is a release
  concern, not a runtime one.
- **Neutral:** the ~484 MB `mysql_data/` copy sits in the tree pending cleanup.

### Alternatives Considered

1. **Runtime MySQL connection.** Rejected: violates the offline constraint.
2. **Bundle the full corpus as SQLite.** Rejected: too large for the device; the
   per-engine-code overlay only needs a slim `vref.db`.

---

## Graph relations (explicit)

**ADR-0001: Offline runtime — bake all reference data into vinlab/data/** DESCRIBES **VINLab ADR v2.0 (2026-06-12)**
**vinlab.__init__.decode** IMPLEMENTS **ADR-0001**
**labs/vinlab/tests/unit/test_standalone.py** VERIFIES **vinlab.__init__.decode**
