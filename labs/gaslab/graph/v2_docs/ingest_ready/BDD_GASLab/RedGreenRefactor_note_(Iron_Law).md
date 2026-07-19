
> **Context:** GASLab BDD v2.1 (2026-06-10) · Module: GASLab · Section: Red–Green–Refactor note (Iron Law) · Parent document: BDD_GASLab.md
## Red–Green–Refactor note (Iron Law)

Per `_skills/doc/BDD.md`, no production code in `gaslab/` ships without a failing test first. Each scenario above corresponds to one or more cases in the named `tests/unit/` module; the `tests/generative/` suite (boundary, combinatorial, fuzz, noise, overlap) then asserts these behaviours hold as **properties** across the synthetic grid, not just at the worked examples. A new fault or field follows the same cycle: write the scenario and its failing test, add the ontology entry and the named COMLab consumer, then make it green — never the reverse.


## Graph relations (explicit)

**Red–Green–Refactor note (Iron Law)** DESCRIBES **GASLab BDD v2.1**
**tests/generative/** VERIFIES **BDD scenarios as properties** -- boundary, combinatorial, fuzz, noise, overlap


