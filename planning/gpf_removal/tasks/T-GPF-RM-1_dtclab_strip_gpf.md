# T-GPF-RM-1 — DTCLab: strip GPF (tag, gate, field, fixtures, docs)

**Pack:** GPF Removal · **Lab:** DTCLab · **Blocked by:** — · **Status:** pending
**Owner ruling:** GPF out of scope (1990–2010). Wiki authority: `labs/dtclab/wiki/08_forced_induction_gdi.md` + `11_proposals_register.md §11.4`.

## Scope (1 paragraph)

Remove every GPF expression from the isolated DTCLab codebase so the lab stops
emitting the `GPF_HISTORY` routing tag and stops reading the
`has_particulate_filter` flag. This is the first task in the pack because DTCLab
is the **emitter** — COMLab must not have its `GPF_HISTORY` enum removed
(T-GPF-RM-2) until DTCLab has stopped producing it, or COMLab would receive an
unknown tag. DTCLab is fully isolated (no cross-lab imports), so this task
touches only `labs/dtclab/` and its own docs. The DTCLab wiki already declares
GPF out of scope, so no wiki edit is needed here — only code, config, fixtures,
tests, and the six design docs that still describe the gate as live.

## Signal/noise / consumer

Removal task. After this task, `grep -rn "GPF\|particulate\|P244A\|P2459" labs/dtclab/dtclab labs/dtclab/tests`
must return **zero** live hits (graph artefacts under `labs/dtclab/graph/`
excluded — they regenerate, do not hand-edit). The fault-atlas/COMLab consumer
that `GPF_HISTORY` fed is being removed in T-GPF-RM-2; this task removes its
producer.

## Files to change

Code / config:
- `dtclab/schemas/vocabulary.py:35` — delete the `GPF_HISTORY` enum member.
- `dtclab/core/routing_tag_mapper.py:131-136` — delete the `gpf_combined` gate branch.
- `dtclab/schemas/dna_view.py:79` — delete `has_particulate_filter` field.
- `dtclab/family_map.py:70` — delete the `DTCRoutingTag.GPF_HISTORY: None` row.
- `dtclab/config/routing_tag_map.yaml:160-170` — delete the two GPF entries
  (`^P244A$` and `^P2459$`) **and** remove `gpf_combined` from the `dna_gate`
  legend comment at line 4.

Fixtures / BDD / tests:
- `tests/regression/fixtures/case_06_gpf_p244a.json` — delete the file; remove any
  manifest/index reference to it.
- `docs/BDD_DTCLab.md` (Scenario Outline ~L179-183, the `gpf_combined` outline
  using `P244A`) — delete the scenario.
- Whole DTCLab test tree — remove every GPF/`has_particulate_filter` case and any
  fixture builder that sets the flag. The files that currently reference it are:
  `tests/unit/test_dna_view.py`, `tests/unit/test_routing_tag_mapper.py`,
  `tests/unit/test_rank_candidates.py`, `tests/generative/test_combinatorial.py`,
  `tests/generative/test_fuzz.py`, `tests/integration/test_dtclab_pipeline.py`,
  `tests/conftest.py`, and `tests/fixtures/descriptor.py` (the `ModuleDescriptor`
  stub — drop `has_particulate_filter` from its schema/fault-box table). The
  remaining catalyst/EGR gate tests stay. Re-grep the tree after editing to
  confirm zero residual hits.

Design docs (strike the gate description, keep the doc coherent):
- `docs/PRD_DTCLab.md:51`, `docs/LLD_DTCLab.md:133-148`, `docs/HLD_DTCLab.md:90,192`,
  `docs/DLD_DTCLab.md:94,288-289`, `docs/DTC_VOCABULARY.md:136,144,436`.
- The DNA-gate tables in HLD/DLD/DTC_VOCABULARY now list **two** gates
  (`has_catalyst`, `egr_equipped`), not three. Update the "32 entries (27 ungated
  + 5 DNA-gated)" count in `HLD_DTCLab.md:88` to its new value after the two
  P244A/P2459 rows are gone (recount from `routing_tag_map.yaml`).

## Success criteria

- No `GPF`, `gpf_combined`, `has_particulate_filter`, `P244A`, or `P2459` token
  in `labs/dtclab/dtclab/`, `labs/dtclab/tests/`, or `labs/dtclab/docs/`.
- DTCLab `DTCRoutingTag` enum has one fewer member; nothing references the
  removed member (pyright clean).
- Routing-tag-map entry count and the HLD gate-count line agree.
- Numeric-literal citation rule unaffected (no new literals introduced).

## Inner loop (coder)

`ruff check labs/dtclab` → `pyright labs/dtclab` → `pytest -x -q labs/dtclab/tests`
after every meaningful edit.

## VERIFICATION GATE
_(coder fills — must be clean before flipping to done)_

## CODE REVIEW
_(coder fills — must be clean before flipping to done)_
