# DNA family — isolation test-harness contract

**Authored:** 2026-06-12 (architect) · **Pack home:** `labs/dnalab/tasks/`
**Applies to:** `T-DNA-TH-1` (dnalab), `T-DNA-TH-2` (vinlab), `T-DNA-TH-3` (symptomlab).
**Read with:** `DNA_TASKS_START_HERE.md` (bootstrap), `PROGRESS.md` (ledger).

This is the shared shape for the three test-harness rows. Each TH task gives a
DNA-family lab its **own, lab-local** harness so **every module can be exercised in
isolation** — driven by controlled inputs the test supplies, never by the real
sibling labs or the production data files. It is the data/lookup-lab analogue of the
fault-box template the continuous labs use (`planning/test_rollout/TEMPLATE.md`),
with the generative fault-box folders removed because these labs have no fault boxes.

## What "in isolation" means here (and why the current tests are not)

A module is tested **in isolation** when its test supplies every input directly and
the test fails **only** if *that module* is wrong — not if an unrelated sibling or a
shared data file is broken. Today the DNA family violates this in two places:

1. **dnalab assembly** hard-calls the real `vinlab.decode` and `symptomlab.resolve`.
   Its `conftest.py` builds the `sample_dna` fixture (a fixture = a ready-made test
   input object) by running the **whole real pipeline**. So a fault anywhere in
   vinlab *or* symptomlab — e.g. the live 17-vs-18 symptom-catalog mismatch the
   ledger already records — turns every dnalab test red, even though `assembly.py`
   is fine.
2. **vinlab / symptomlab** tests read the **packaged production data** (`vinlab/data/`,
   `symptomlab/data/allowed_combinations.yaml`) and external corpus CSVs, and `skip`
   when those are absent. That couples a unit test to a large shipped dataset and to
   the data file's current correctness.

```
NOW (coupled):                          TARGET (isolated):
 dnalab test                             dnalab test
   └─ build_vehicle_dna                    └─ build_vehicle_dna
        ├─ REAL vinlab.decode  ──┐              ├─ FAKE decode  (test double)
        └─ REAL symptomlab.resolve┘             └─ FAKE resolve (test double)
   (red if any sibling/data breaks)         (red ONLY if assembly logic is wrong)
```

## The "plugin" rule — test doubles plugged into existing seams (NO production change)

Owner decision (2026-06-12): isolation is achieved with **test-only doubles**, with
**no change to any production module**. A *test double* is a stand-in object the test
supplies in place of a real dependency. A *seam* (a named point where a dependency
can be swapped) already exists in every case — so the coder plugs the double into the
seam; they do **not** add new production parameters or abstractions.

| Lab | Existing seam (already in code — do not add new ones) | Double the test plugs in |
|---|---|---|
| dnalab | module-level names `dnalab.assembly._decode_vin` / `._resolve_symptom` | `monkeypatch.setattr(...)` to fake decode/resolve callables |
| vinlab | `decode(vin, *, data_dir=…)` and `lookup_engine_ref(db_path, …)` | a **lab-local minimal fixture `data_dir`** (tiny CSVs + tiny `vref.db`) |
| symptomlab | `resolve(…, allowed_path=…)` and `SymptomValidator(allowed_path)` | a **controlled minimal `allowed_combinations.yaml` fixture** |

`monkeypatch` is pytest's built-in tool for temporarily replacing a name during one
test; the replacement is undone automatically when the test ends. Because each seam
already takes the dependency as a path argument or an importable module attribute,
**no production file is edited by any TH task** (the one allowed exception: adding a
`tests/` subtree and `__init__.py` files, which are test code, not production code).

If a coder finds they *cannot* isolate a module without editing production code, they
**stop and surface it** as an Unplanned follow-up — they do not silently add a
dependency-injection (DI = passing a dependency in as an argument) seam. That would
be a scope change the owner has not approved.

## Slim data-lab template (the folder shape every TH task lays down)

```
labs/<lab>/tests/
├── conftest.py            # shared builders + fakes + fixture-path fixtures
├── fixtures/              # controlled, MINIMAL inputs this lab is tested against
│   ├── __init__.py
│   └── …                  # e.g. mini data_dir/, mini allowed_combinations.yaml
├── unit/                  # ONE test_<module>.py per production module — isolation tests
│   ├── __init__.py
│   └── test_<module>.py
└── (existing flat tests are MOVED into unit/, not rewritten)
```

What is deliberately **absent** vs the continuous-lab template: the whole
`generative/` folder (`test_boundary` / `test_noise` / `test_overlap` /
`test_combinatorial` / `test_fuzz`), the `fixtures/descriptor.py` `ModuleDescriptor`,
and any import of the shared engine in `harness/`. These labs decide nothing from
numeric fault boxes, so none of that applies — and "proprietary / lab-local" is the
point: **no import of `harness/`**, no cross-lab test imports beyond the allowed
`dnalab → vinlab + symptomlab` direction.

### conftest is the harness

The harness *is* a `conftest.py` of small, reusable **builders** (functions that
construct a valid input object with sensible defaults + keyword overrides) and
**fakes**, mirroring how the in-vault labs do it (`Vault/labs/dtclab/tests/conftest.py`
ships `make_dna_view`, `make_freeze_frame_raw`, `run_sanitize`). Examples this pack
will create: `make_vin_dna(**overrides)`, `make_symptom_dna(**overrides)`,
`fake_decode_returning(vin_dna)`, `make_mini_data_dir(tmp_path)`,
`write_mini_allowed_yaml(tmp_path)`.

## Signal/noise for test scaffolding (anti-orphan)

The schema-field consumer rule does not bite here — **no schema field is added**. The
spirit still holds, re-cast for tests: **every builder, fake, or fixture added must be
consumed by at least one named test in the same diff.** A builder no test calls is an
orphan and a signal/noise breach — it does not ship. State the consuming test for
each helper in the progress note's anti-orphan line.

## Numeric literals in vinlab fixtures

DNA-pack rule (`DNA_TASKS_START_HERE.md` §2): every numeric literal in `vinlab/`
carries a wiki/contract cite. Extends to **fixture expected values**: any expected
decode/overlay output asserted in a vinlab isolation test cites its source
(`SEMANTIC_CONTRACT.md` §, a wiki §, or the fixture row it was derived from). An
expected value with no citable source is marked `# characterization` (a regression
pin — locks current behaviour, not asserted-correct) in a comment, never presented as
ground truth.

## Coder flow per TH task (unchanged house procedure)

read skill → one-paragraph scope confirm (files, the modules covered, the named
consuming tests) → write tests → inner loop after **every** meaningful edit
(`ruff` → `pyright` → `pytest -x -q`, from the owning lab root) → `VERIFICATION GATE`
+ `CODE REVIEW` blocks both clean in `progress_notes/<id>.md` → flip the ledger row →
output the explicit-path commit block for the owner → STOP. One task per session.

graphify: **SKIP** (DNA-pack §3). Never touch `graph/` or `.sandbox-py/`.
