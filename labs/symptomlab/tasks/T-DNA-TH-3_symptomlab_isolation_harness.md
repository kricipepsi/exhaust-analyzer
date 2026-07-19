# T-DNA-TH-3 — symptomlab isolation harness (proposed method)

> **Pack home note:** DNA-family isolation harness sub-pack
> (`labs/dnalab/tasks/PROGRESS.md`; contract `labs/dnalab/tasks/DNA_ISOLATION_HARNESS.md`).
> Deliverables are symptomlab's; bootstrap still via `labs/dnalab/tasks/DNA_TASKS_START_HERE.md`.
> The owner was unsure how to isolate symptomlab — this row **is** the proposed method,
> below. If the owner rejects the method, this row stays `pending` and is not run.

### Proposed test method (the answer to "how do we test symptomlab in isolation") ###

symptomlab is a lookup-and-validate lab: `resolve()` builds a `SymptomValidator` from a
catalog YAML and validates a (tier_1, tier_2 + context) selection into a `SymptomDNA`.
The hard part the owner flagged is that its only real input is a **data file**
(`data/allowed_combinations.yaml`), and that file enforces a strict invariant —
`SymptomValidator.__init__` raises `ValueError` unless the catalog has **exactly 18
(tier_1, tier_2) pairs** (`SEMANTIC_CONTRACT.md §4.2`). So a test bound to the live
file breaks whenever that file is mid-edit or wrong (exactly the 17-vs-18 incident the
DNA ledger records).

**Method = catalog injection through the existing `allowed_path=` seam.** Check two
controlled YAML fixtures into `tests/fixtures/` and pass them explicitly, so the
validator/resolver logic is exercised against catalogs the test owns — never the live
production file:

```
test → resolve(tier_1, tier_2, …, allowed_path=GOOD_18_PAIR_FIXTURE)  → assert SymptomDNA
test → SymptomValidator(BAD_17_PAIR_FIXTURE)                          → assert ValueError raised
```

This gives full isolation with **no production change** — `resolve()` and
`SymptomValidator` already accept the path. It also makes the invariant itself a tested
behaviour (good catalog passes; off-count catalog fails closed), which is precisely the
class of bug that has bitten this lab.

Read `DNA_ISOLATION_HARNESS.md` first.

### Named signal/noise consumer ###

No schema field added — field-consumer rule N/A. Anti-orphan (test variant): both YAML
fixtures and any builders are consumed by named tests in this diff — the good-18 fixture
by `tests/unit/test_validator.py` + `test_resolve_isolation.py`, the bad-17 fixture by
the invariant negative test. No fixture ships unconsumed.

### Success criteria ###

- `tests/fixtures/` (CREATE): `allowed_combinations.good18.yaml` (a frozen, contract-
  valid 18-pair catalog — copy of the live good set, with a header comment citing
  `SEMANTIC_CONTRACT.md §4.2`) and `allowed_combinations.bad17.yaml` (a deliberately
  off-count catalog for the negative path). Add `tests/fixtures/__init__.py`.
- `tests/conftest.py` (MODIFY): fixtures `good_allowed_path` / `bad_allowed_path`
  returning those paths; a `make_symptom_dna(**overrides)` builder constructing a
  `SymptomDNA` directly for model tests. The existing cache-clear autouse fixture in
  `test_resolve_isolation.py` stays.
- Per-module isolation tests under `tests/unit/`:
  - `test_validator.py` (MOVE/EXTEND): the 18-pair invariant raises on the bad fixture;
    a valid pair from the good fixture validates; an unknown tier_1/tier_2 and a bad
    context value raise `SymptomValidationError`. All driven by injected fixtures.
  - `test_resolve_isolation.py` (KEEP/MOVE): keep the `allowed_path=` injection cases;
    ensure at least the core happy-path uses `good_allowed_path` (not the live default),
    so the test does not depend on the production file's current state.
  - `test_models.py` (MOVE): `SymptomDNA` round-trip / `from_json` via `make_symptom_dna`.
  - `test_symptomdna_from_json.py`, `test_drift_guard.py` (MOVE into `tests/unit/`).
- Slim layout: create `tests/unit/` (+ `__init__.py`); move the flat test files in.
- Isolated tests must pass **even if `symptomlab/data/allowed_combinations.yaml` is
  deleted or off-count** — prove it in the gate (temporarily rename the live file and
  rerun the isolated subset).
- Inner loop clean on every edited file; `pytest tests/` green.

### Files to touch ###

- `labs/symptomlab/tests/fixtures/allowed_combinations.good18.yaml` (CREATE)
- `labs/symptomlab/tests/fixtures/allowed_combinations.bad17.yaml` (CREATE)
- `labs/symptomlab/tests/fixtures/__init__.py` (CREATE)
- `labs/symptomlab/tests/conftest.py` (MODIFY — fixture-path fixtures + builder)
- `labs/symptomlab/tests/unit/__init__.py` (CREATE)
- `labs/symptomlab/tests/unit/test_validator.py` (MOVE + EXTEND)
- `labs/symptomlab/tests/unit/test_resolve_isolation.py` (MOVE + pin to good fixture)
- `labs/symptomlab/tests/unit/test_models.py` (MOVE)
- `labs/symptomlab/tests/unit/test_symptomdna_from_json.py` (MOVE)
- `labs/symptomlab/tests/unit/test_drift_guard.py` (MOVE)

### Out of scope ###

Editing `validator.py`, `models.py`, or `__init__.py` (no production change — if
isolation seems to need one, STOP and surface it). Changing the 18-pair invariant or
the live catalog contents (that is T-DNA-8/9 territory). dnalab/vinlab trees. Adding
`oil_consumption` or any vocabulary (T-DNA-9). The shared `harness/` engine.

### Blocked-by ###

— (independent; the good-18 fixture is a frozen copy, so it does not depend on the live
catalog's state).

### On completion ###

Both gates clean in `progress_notes/T-DNA-TH-3.md`; flip T-DNA-TH-3 → `done` in
`labs/dnalab/tasks/PROGRESS.md`. STOP (one task per session).

### Verification ###

```bash
cd $HOME/mnt/4DLab/labs/symptomlab
ruff check symptomlab/ tests/ && pyright symptomlab/ tests/
pytest tests/unit -q --tb=short
# prove isolation from the live data file:
mv symptomlab/data/allowed_combinations.yaml /tmp/_live.yaml
pytest tests/unit -q --tb=short -k "validator or resolve or models"
mv /tmp/_live.yaml symptomlab/data/allowed_combinations.yaml
pytest tests/ -q --tb=short
# anti-orphan: both fixtures are referenced by tests
grep -rn "good18\|bad17\|good_allowed_path\|bad_allowed_path" tests/
```
