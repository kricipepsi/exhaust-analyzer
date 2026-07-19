> **Context:** VINLab BDD v2.0 (2026-06-12) | Module: VINLab | Section: Preamble | Parent document: BDD_VINLab.md / shipped unit tests

# BDD — VINLab (v2)

**Status:** Current (scenarios grounded in the decoder behaviour + test fixtures)
**Reference:** HLD_VINLab v2.0 / DLD_VINLab v2.0 / LLD_VINLab v2.0
**Date:** 2026-06-11

Behaviour specification for VINLab's single public behaviour: **decode a 17-character
VIN into a typed `VinDNA`**. Scenarios are declarative (diagnostic/identity focus). The
truth is the decoder source + `tests/`; these scenarios capture executable-spec intent.

Ubiquitous language: *decode* = run `vinlab.decode()`; *in-scope* = petrol, model year
1990–2020; *graded* = assigned a `VinConfidence`; *passthrough* = a year character that
maps to `model_year = None`.

---


## Graph relations (explicit)

**BDD_VINLab.md** DESCRIBES **VINLab BDD v2.0 (2026-06-12)**
