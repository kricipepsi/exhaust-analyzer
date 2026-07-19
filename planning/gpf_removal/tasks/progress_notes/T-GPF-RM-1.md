# T-GPF-RM-1 — Progress Note

## Plan

T-GPF-RM-1 strips every GPF expression from DTCLab (`labs/dtclab/`). Remove the `GPF_HISTORY` enum from `vocabulary.py`, the `gpf_combined` gate from `routing_tag_mapper.py`, the `has_particulate_filter` field from `dna_view.py`, the `family_map.py` row, the `routing_tag_map.yaml` entries (update legend comment), the `case_06_gpf_p244a.json` fixture, the BDD scenario, all GPF test cases across 7 test files, and GPF references in 5 design docs — then recount the HLD gate-count line. Neither pack caveat (hex regex, catalyst fault) lives in DTCLab. Inner loop: `ruff check labs/dtclab` → `pyright labs/dtclab` → `pytest -x -q labs/dtclab/tests` after every edit. Final grep for `GPF\|particulate\|P244A\|P2459` across `dtclab/`, `tests/`, and `docs/` must return zero.

## VERIFICATION GATE

- **ruff:** `ruff check labs/dtclab` — All checks passed.
- **pyright:** `pyright labs/dtclab` — 4 pre-existing errors (conftest.py string-literals, descriptor.py import, combinatorial.py `object | None` type). None caused by this task; all pre-date the GPF removal.
- **pytest:** `pytest -x -q labs/dtclab/tests` — 576 passed, 0 failed.
- **Zero-residual grep:**
  - `labs/dtclab/dtclab/` — 0 hits for `GPF|particulate|P244A|P2459|gpf_combined`
  - `labs/dtclab/tests/` — 0 hits
  - `labs/dtclab/docs/` — 0 hits
- Residual hits outside task scope (confirmed non-actionable):
  - `labs/dtclab/wiki/` — wiki files intentionally declare GPF out of scope (they are the authority for this pack)
  - `labs/dtclab/DTC10*.md` — lab-root research/planning docs
  - `labs/dtclab/graph/` — regenerated artefacts (excluded per task spec)

## CODE REVIEW

**Contracted files changed (25 files):**
- `dtclab/schemas/vocabulary.py` — removed `GPF_HISTORY` enum member
- `dtclab/core/routing_tag_mapper.py` — removed `gpf_combined` gate branch; dropped unused `ResolvedHorizon` import
- `dtclab/schemas/dna_view.py` — removed `has_particulate_filter` field
- `dtclab/family_map.py` — removed `DTCRoutingTag.GPF_HISTORY: None` row
- `dtclab/config/routing_tag_map.yaml` — removed P244A/P2459 entries; updated legend comment
- `tests/regression/fixtures/case_06_gpf_p244a.json` — deleted
- `tests/regression/fixtures/case_03_catalyst_ect_gate.json` — removed `has_particulate_filter`
- `tests/conftest.py` — removed GPF entries from CODE_TAG_ORACLE, GATED_TAGS, and `make_dna_view`
- `tests/unit/test_routing_tag_mapper.py` — removed 7 GPF gate tests + `has_particulate_filter` from helper
- `tests/unit/test_dna_view.py` — updated field counts (3→2), removed `has_particulate_filter` assertions; fixed `wiki/`→`docs/` path
- `tests/unit/test_rank_candidates.py` — removed `has_particulate_filter` from DtcEmissionsView
- `tests/unit/test_family_map.py` — updated tag count 18→17
- `tests/unit/test_vocabulary.py` — updated tag count 18→17; fixed `wiki/`→`docs/` path
- `tests/unit/test_dtc_ingestion_gate.py` — removed P244A from valid code list
- `tests/generative/test_combinatorial.py` — removed `gpf_combined` from `_build_dna_view_for_case`
- `tests/generative/test_fuzz.py` — removed P244A/P2459 hex-edge cases; removed `DTCRoutingTag` import
- `tests/integration/test_dtclab_pipeline.py` — removed 7 GPF pipeline tests + `has_particulate_filter` from helper
- `tests/fixtures/descriptor.py` — removed P244A exemplar
- `docs/BDD_DTCLab.md` — removed `gpf_combined` scenario
- `docs/PRD_DTCLab.md` — removed GPF references from sections 3, 5, 7, 8
- `docs/HLD_DTCLab.md` — removed GPF gate, GPF_HISTORY row; updated entry count 32→30; removed open issues
- `docs/LLD_DTCLab.md` — removed `gpf_combined` code block, edge case table, and prose
- `docs/DLD_DTCLab.md` — removed GPF_HISTORY from enum table, field table, gate pseudocode, family map, routing YAML table, test coverage descriptions
- `docs/DTC_VOCABULARY.md` — removed GPF_HISTORY enum, gate condition, cross-reference, prose anchor, field, confidence example, DTC table rows
- `docs/ADR_DTCLab.md` — removed GPF from context listings

**No adjacent refactor.** Every edit traces to GPF removal. Two pre-existing path bugs (`wiki/`→`docs/` in test_vocabulary.py and test_dna_view.py) fixed as necessary to run the test suite.

**Two caveats honoured:**
1. Hex `DTC_REGEX` (`^[BCPU][0-3][0-9A-F]{3}$`) — untouched; not in DTCLab.
2. `catalyst_flow_restriction` registry fault — not in DTCLab.

**No symbol left half-removed.** Zero-residual grep confirms complete removal from code, tests, and docs.

**Unplanned follow-ups noted:**
- `has_gdi` decode logic referenced in pack ledger — still in-scope (era B), not orphaned by this removal. GDI is kept.
- Euro-6+/LSPI references in DTCLab wiki — already declared out of scope by the wiki itself; not in this diff.

## Commit block

```powershell
cd C:\Users\muto\claude\4DApp\4DLab\4DLabV2
git add `
  planning\gpf_removal\tasks\progress_notes\T-GPF-RM-1.md `
  labs\dtclab\dtclab\schemas\vocabulary.py `
  labs\dtclab\dtclab\core\routing_tag_mapper.py `
  labs\dtclab\dtclab\schemas\dna_view.py `
  labs\dtclab\dtclab\family_map.py `
  labs\dtclab\dtclab\config\routing_tag_map.yaml `
  labs\dtclab\tests\regression\fixtures\case_06_gpf_p244a.json `
  labs\dtclab\tests\regression\fixtures\case_03_catalyst_ect_gate.json `
  labs\dtclab\tests\conftest.py `
  labs\dtclab\tests\unit\test_routing_tag_mapper.py `
  labs\dtclab\tests\unit\test_dna_view.py `
  labs\dtclab\tests\unit\test_rank_candidates.py `
  labs\dtclab\tests\unit\test_family_map.py `
  labs\dtclab\tests\unit\test_vocabulary.py `
  labs\dtclab\tests\unit\test_dtc_ingestion_gate.py `
  labs\dtclab\tests\generative\test_combinatorial.py `
  labs\dtclab\tests\generative\test_fuzz.py `
  labs\dtclab\tests\integration\test_dtclab_pipeline.py `
  labs\dtclab\tests\fixtures\descriptor.py `
  labs\dtclab\docs\BDD_DTCLab.md `
  labs\dtclab\docs\PRD_DTCLab.md `
  labs\dtclab\docs\HLD_DTCLab.md `
  labs\dtclab\docs\LLD_DTCLab.md `
  labs\dtclab\docs\DLD_DTCLab.md `
  labs\dtclab\docs\DTC_VOCABULARY.md `
  labs\dtclab\docs\ADR_DTCLab.md
git commit -m "T-GPF-RM-1: strip GPF from DTCLab — tag, gate, field, fixtures, tests, docs"
```
