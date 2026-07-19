
> **Context:** DTCLab BDD v1.0 (2026-06-11) · Module: DTCLab · Section: Preamble · Parent document: BDD_DTCLab.md
# BDD — DTCLab
**Status:** Approved
**Version:** 1.0
**Date:** 2026-06-11
**Scope:** Behaviour specification for the DTCLab v2 pipeline and Phase-2 scorer

Format: Gherkin (`Given / When / Then`) per `_skills/doc/BDD.md`. Scenarios are declarative,
business-focused executable specifications — one behaviour each. Every scenario maps to shipped
behaviour and its backing test in `labs/dtclab/tests/`; the mapping is named under each feature so
the design→code→test spine stays explicit.

Convention reminder (the Iron Law): no production behaviour ships without a failing test first.
These scenarios are the source examples those tests encode.

---


## Graph relations (explicit)

**BDD_DTCLab.md** DESCRIBES **DTCLab BDD v1.0**
