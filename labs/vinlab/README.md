# labs/vinlab — VINLab v2

**Role:** VIN decode + vehicle DNA. Part of the DNA family but migrated as an
**independent module** (own folder, own `pyproject.toml`). Feeds the **COMLab prior**.
**Code origin:** fork of v1 `DNALab/VINLab/`; v1 archived once built and green (Phase 5).
**Boundary:** no cross-lab Python imports — COMLab mirrors the types it needs locally.
**Note:** VINLab tasks historically close only on a whole-repo green gate — carry that discipline.
`mysql_data/` (~484 MB) was copied verbatim for now; tests use the small sqlite `vinlab/data/vref.db`
and skip when data is absent. `mysql_data/` is a candidate for removal in Track-2 cleanup.

_Status: migrated 2026-06-06 (T-RM-2-DNA, sibling split). v1 process history left in `DNALab/VINLab/` for Phase-5 archive._
