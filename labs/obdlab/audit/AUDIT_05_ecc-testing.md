# OBDLab audit — Lens 5/5: `ecc-subset` (testing & verification)

**Date:** 2026-06-08 · **Auditor role:** architect (read + report; no code edits) ·
**Skill:** `_skills/codingskills/ecc-subset` — four sub-lenses:
`python-testing`, `verification-loop`, `eval-harness`, `ai-regression-testing`.
**Subject:** OBDLab **test code** (`tests/`, 31 files, ~4,005 LOC).

> **Why tests are in scope.** Confirmed against the canonical KG: the 4DLabV2
> `graphify-out/graph.json` ingests **41 OBDLab test source files → 760 nodes** (test
> modules, `conftest`, fixtures, the 6 regression-case JSONs). `.graphifyignore` strips only
> caches, not tests. So test code is shipped, graph-visible content — auditable, and the
> owner's instruction "test code if it is ingested" applies.

---

## Sub-lens A — `python-testing` (pytest, fixtures, structure)

### 🟢 E-3 `[nit]` Empty `conftest.py`; fixtures duplicated across files
`tests/conftest.py` contains only `from __future__ import annotations` — no shared
fixtures. As a result the same DNA-view builder (`cylinder_count=4`, an `ObdLabDnaView`
with the standard fields) is reconstructed in ~10 test files
(`test_o2_normalizer`, `test_ve_engine`, `test_semantic_consistency_checker`,
`test_sensor_signal_translator`, `test_maf_linearity`, `test_ecu_perception_delta`,
integration smoke, …). python-testing lens: hoist a `dna_view` factory fixture (and a
`translator` fixture — the regression suite already uses one) into `conftest.py`.

### 🎉 E-4 `[praise]` Unit coverage is real and per-module
Every source module has a matching unit test with meaningful assertions (bounds, bank
asymmetry, ECU perception delta, MAF linearity, classify_top3, vocabulary completeness).
The regression suite (`tests/regression/`) is well-built: 6 JSON fixtures, parametrized,
a `model_dump_json → model_validate_json` round-trip check (L107), and an explicit
**DNA-confidence coverage** test asserting HIGH/NONE/PARTIAL fixtures all exist
(L115-126). The `pid_logset` wiring gate parametrizes real cases and asserts on
`rpm_state_bucket`, `ve_validity`, `trim_analytics_gate`, lambda, and trim, plus a
coverage-matrix/aggregate-rate test. This is a solid base — the gaps below are about the
*generative* and *eval* layers, not the unit layer.

---

## Sub-lens B — `verification-loop` (build → type → lint → test → diff)

### 🟡 (= P-1 / E-1 combined) The green bar overstates what is verified
The inner loop exists and is configured (`ruff` + `pyright` + `pytest`, `testpaths=["tests"]`),
but three things let a **green run mean less than it looks**:

| Gap | Evidence | Effect |
|-----|----------|--------|
| Thin ruleset | `pyproject.toml` `select=[E,F,I,N,W,UP]`; `pyright="basic"` | misses the CR/UB structural bugs (no `B`/`SIM`/`TRY`, no security scan) |
| No coverage threshold | no `--cov`/fail-under config | dead code (CR-1, CR-2) and skipped suites don't move a visible number |
| Skipped suites count as "passing" | 6 `@pytest.mark.skip` stubs (below) | `pytest -q` is green while whole categories run nothing |

verification-loop lens prescribes a **diff review + "does the gate actually exercise the
change"** step. The two 🔴 dead-code findings (CR-1 Physics Gate 3, CR-2 wideband offset)
are exactly what a "did the integration path execute this?" check would have caught — they
pass unit tests but never run in `translate()`.

> Note: this loop must be run in Windows `.venv-wired` (the real files). The sandbox mirror
> is truncated (see `AUDIT_01`), so a sandbox `pytest` would fail to import and is not a
> valid gate.

---

## Sub-lens C — `eval-harness` (EDD, pass@k, accuracy regression)

### 🟡 E-5 No formal eval harness / pass@k; the regression + wiring gate are the closest thing
There is no eval-driven-development harness: no pass/fail criteria defined *before*
implementation, no `pass@k` reliability metric, no accuracy benchmark suite over a labelled
corpus. The `pid_logset` wiring gate's **aggregate-rate / coverage-matrix** test
(`test_pid_logset_wiring_gate.py` L105) is the nearest analogue and a good seed — it is, in
effect, a small eval. The regression fixtures are golden-file checks, not an eval metric.

This is **consistent with the recorded plan** (`project_4dlab_buildout`: the 11.7% harness
is a known structural gap; per-module suites are being built first) — so this is reported
as a *characterisation of current state*, not a surprise. The eval layer is deferred to the
harness build (T-TST-8 / harness v2), not missing by accident.

---

## Sub-lens D — `ai-regression-testing` (AI blind spots)

### 🟡 E-1 `[important]` The generative test layer is entirely skipped stubs
All five generative tests and the CSV-case test are 10-line `@pytest.mark.skip(reason=
"blocked: T-TST-8 obdlab harness")` stubs with `pass` bodies:

`tests/generative/test_boundary.py`, `test_combinatorial.py`, `test_fuzz.py`,
`test_noise.py`, `test_overlap.py`, and `tests/test_cases.py`.

The directory structure advertises boundary/fuzz/combinatorial/noise/overlap coverage that
**does not exist**. ai-regression-testing lens: this is the highest-risk shape for
AI-written code — the property/adversarial layer that would catch the model's own blind
spots is precisely the layer that is empty. (Tracked under T-TST-8; the audit's role is to
make the gap explicit and tie it to the two live bugs it would likely have caught.)

### 🟡 E-2 `[important]` Realised AI blind spot — "same author writes code and its test"
ai-regression-testing warns that when one model writes both the code and the test, both can
share the same wrong mental model. Two concrete instances in OBDLab:

- **Physics Gate 3 (CR-1):** the unit test *injects* `calculated_ve` (matching the author's
  assumption that it is present), so it passes — while the real pipeline never supplies it.
  The test encodes the same blind spot as the code.
- **Wideband offset (CR-2):** no test exercises the warm/closed-loop wideband-offset path
  end-to-end, so the enum-vs-string bug that kills it went unnoticed.

The mitigation this lens prescribes: an **integration-level** assertion (different author
mindset / different layer) that each documented fault path actually fires through
`translate()`. Both CR-1 and CR-2 specs (in `AUDIT_03`) include exactly this.

---

## Draft task specs (ecc / testing lens)

### T-OBDV2-AUDIT-ECC-1 — Integration "fault actually fires" assertions (E-2) **[highest test value]**
- **Files:** `tests/integration/test_pipeline_smoke.py` (extend), maybe a new
  `tests/integration/test_fault_paths.py`
- **Change:** for each documented fault, drive `SensorSignalTranslator.translate()` with raw
  inputs (not injected intermediate keys) and assert the fault surfaces in the payload:
  Physics-Gate-3 NA VE-ceiling (pairs with CR-1), `WIDEBAND_OFFSET_CANDIDATE` (pairs with
  CR-2), the VEValidity faults, the TrimAnalyticsGate failures.
- **Success:** the new tests **fail against today's code** for CR-1/CR-2 (proving they catch
  the dead paths), then pass once those fixes land. `pytest -x -q` green afterward.
- **Consumer:** the verification gate itself; no schema change.

### T-OBDV2-AUDIT-ECC-2 — Hoist shared fixtures to `conftest.py` (E-3)
- **Files:** `tests/conftest.py`, the ~10 unit test files
- **Change:** add `dna_view` factory + `translator` fixtures to `conftest.py`; replace the
  per-file duplicates. Touch only fixture construction, not assertions.
- **Success:** duplication removed; `pytest -x -q` green; no behavioural test change.
- **Consumer:** n/a (test hygiene).

### Deferred (not new tasks — already tracked)
- **E-1 (generative stubs)** and **E-5 (eval harness)** are the existing **T-TST-8 / harness
  v2** scope. No new task; the audit recommends T-TST-8 be sequenced **after** CR-1/CR-2 so
  the generated cases test live, not dead, fault paths.
