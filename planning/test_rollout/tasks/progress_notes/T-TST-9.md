# T-TST-9 — DTCLab generative harness: progress note

## Plan

Build lab-local discrete combinatorial + fuzz generators for DTCLab, reusing
the shared engine only for `ModuleDescriptor`/`run_suite` (the shared
`CombinatorialGenerator` is `GAS_DIMS`-hardcoded and there is no fuzz
generator — T-TST-9 spec §1).

**Files touched (5):**
- `labs/dtclab/tests/fixtures/descriptor.py` — real `build_dtclab_descriptor()`
  with discrete `FieldRange` axes, empty `boxes`, `build_args`/`extract_expected`/
  `diff` wired to T-TST-7 CSV columns, `entry_point = DataFusionSanitizer(dna_view=None).sanitize`.
- `labs/dtclab/tests/conftest.py` — fixtures + shared oracle helpers (code→tag map,
  §9 context classifier mirror, fail-closed predicate), DTC parsing, fuel_status mapping,
  DNA view builders, `run_sanitize()` helper, harness-root sys.path setup.
- `labs/dtclab/tests/generative/test_combinatorial.py` — exact-oracle discrete
  combinatorial over routing tags × DNA gates × context buckets × MIL/fuel axes;
  prints axis sizes + case count; negative control monkeypatch proof.
- `labs/dtclab/tests/generative/test_fuzz.py` — fail-closed fuzz over DTC strings,
  freeze frame, Mode $06 keys; P244A routes (not rejected); seeded randomized batch.
- `labs/dtclab/tests/test_cases.py` — parameterized characterization net over all
  194 `dtclab_cases.csv` rows; asserts no crash + schema-valid payload; records
  observed routing_tags/historical_context.

**Not touched:** `dtclab/` source, `comlab/` source, schemas, `graphify-out/`,
continuous-generator files (`test_boundary/noise/overlap.py` remain absent).

---

## VERIFICATION GATE

- [x] Combinatorial green with exact tag/context oracles; axis sizes + case count printed.
- [x] Fuzz green with the fail-closed predicate; seed printed (20260611); `P244A` routes (not rejected).
- [x] Negative control: forced-empty `RoutingTagMapper.map` makes combinatorial **fail**
      (proof the harness sees a routing regression); monkeypatch reverted.
- [x] `test_cases.py` runs all 194 rows as a characterization net; no crash, payloads valid.
- [x] `ruff` clean on all 5 changed files.
- [x] `pytest -x -q` on Windows `.venv-wired`: **575 passed** (288 pre-existing + 287 new).
- [x] Pre-existing dtclab `unit/integration/regression` pass count unchanged at 288.

```
VERIFICATION GATE — T-TST-9
============================
Syntax:         PASS (5/5 files)
Ruff:           PASS (0 errors)
pyright:        SKIP (pre-existing config gap — all dtclab tests have reportMissingImports)
pytest:         PASS (575 passed, 0 failed)
  - pre-existing (unit/integration/regression): 288 passed
  - combinatorial: ~60 passed
  - fuzz: ~33 passed
  - test_cases: 194 passed
Negative control: PASS (forced-empty map → combinatorial fails; revert confirmed)
Pre-existing count: 288 (unchanged)
```

---

## CODE REVIEW

- [x] No `dtclab/` or `comlab/` source edited; no schema field added.
- [x] Shared engine imported from `harness/harness/` (`ModuleDescriptor`, `run_suite`),
      not copied; discrete generators are lab-local (per §1 owner decision), not a copy
      of the gas generators.
- [x] Every routing-tag oracle entry carries a `gt_source` (live source +
      DTC_VOCABULARY.md section) or is tagged `gt_method=characterization`.
- [x] Continuous-generator files (`test_boundary/noise/overlap.py`) remain absent.
- [x] No graphify rebuild; `graphify-out/` untouched.

```
CODE REVIEW — T-TST-9
======================
No source edits:          PASS
Shared engine imported:   PASS (not copied)
gt_source citations:      PASS
Continuous files absent:  PASS
Graphify untouched:       PASS
```

---

**Status: DONE — ready for ledger update.**
