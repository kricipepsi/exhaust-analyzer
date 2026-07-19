
> **Context:** GASLab ADR v2.1 (2026-06-10) · Module: GASLab · Section: ADR-0004: A declarative YAML ontology is the single source of fault signatures · Parent document: ADR_GASLab.md
## ADR-0004: A declarative YAML ontology is the single source of fault signatures

**Status:** Accepted

**Context.** Fault signatures (per-gas bounds, operating state, gates, differentiators) are knowledge, not control flow. Encoding them in Python scatters thresholds through branches and makes them hard to audit against the wiki.

**Decision.** All fault signatures live in `gas_lab_ontology.yaml`, loaded once by `ontology_loader.load_ontology()` with schema validation. The rule engine reads bounds and grammar from the ontology; it does not hard-code signatures. A wiki-drift guard (`audits.parse_vocabulary_thresholds`) compares the ontology's numeric thresholds against `GAS_VOCABULARY.md §10` on every CI run, so the YAML and the wiki cannot silently diverge.

**Consequences.**
- Positive: signatures are auditable in one declarative file; thresholds carry citations.
- Positive: adding/adjusting a fault is a data change plus a test, not a control-flow rewrite.
- Negative: the YAML and the wiki must be changed together or CI fails (by design).
- Neutral: a few genuinely procedural rules (priority overrides, RPM-differential gates) still live in code; the ontology supplies their thresholds.

**Alternatives considered.**
1. *Hard-code signatures as Python constants.* Rejected — not auditable, no drift guard possible.
2. *A database of signatures.* Rejected — adds I/O and infra for a small, static, version-controlled dataset.

**References.** `DLD_GASLab §8, §9, §11`; `ontology_loader.py`; `audits.py`.

---


## Graph relations (explicit)

**ADR-0004: A declarative YAML ontology is the single source of fault signatures** DESCRIBES **GASLab ADR v2.1**
**gas_lab_ontology.yaml** OWNED_BY **ontology_loader.py** -- single source of fault signatures
**audits.parse_vocabulary_thresholds()** VERIFIES **GAS_VOCABULARY.md** -- wiki-drift guard


