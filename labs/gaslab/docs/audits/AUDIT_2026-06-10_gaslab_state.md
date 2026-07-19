# GASLab v2 — State-of-Codebase Audit

**Date:** 2026-06-10
**Scope:** `4DLabV2/labs/gaslab` (code, tests, ledger). Read-only assessment — no
code or ledger edits made. Document/ledger updates are a deliberate later pass
(owner direction: "we will update documents later, based on real code state").
**Method:** codingskills audit (`code-reviev`, `python-testing`, `verification-loop`)
run against Python 3.14 in the sandbox.

---

## Verdict

GASLab v2's **shipping code is in good shape**: the core test suite is fully
green, linter and type-checker are clean, and the cross-lab isolation rules are
honoured. The real issues are at the **edges** — the generative test tree does
not run out of the box, and a handful of schema fields (the slim DNA input slice
and two output gases) currently have no live reader. None of these block the
engine; they are housekeeping items, and most are already expected to resolve in
the COMLab v2 rework.

Two things are worth your attention before the next session:

1. A plain `pytest` from the lab folder is **red at collection** (4 errors) —
   the generative tests import a `harness` package with nothing to put it on the
   import path (no `conftest.py`, no install, no path setting). The documented
   "207 green" is the **core suite only**; the generative tree is silently
   excluded.
2. Three DNA-view input fields and two output gas fields are **orphans** (defined
   but read nowhere). One of them (`number_of_banks`) the ledger already says was
   *dropped* — but it's still in the code.

---

## 1. Inner loop (build / lint / type / test)

| Gate | Result |
|---|---|
| `ruff check .` (linter) | **PASS** — all checks passed, 0 warnings |
| `pyright` (type checker) | **PASS** — 0 errors, 0 warnings, 0 informations |
| `pytest` — core (`tests/unit`, `tests/test_cases.py`, `tests/fixtures`) | **PASS** — 207 passed, 1 skipped |
| `pytest` — default invocation (whole `tests/` tree) | **FAIL at collection** — 4 errors |
| `pytest` — generative tree (with `harness` on path) | **PASS** — 4 pass, 1 skipped (see timings) |

The 207-pass core figure matches the ledger's "207 GAS green" claim exactly, so
the ledger is honest about the core suite.

### 1a. Generative tests don't run out of the box — the main finding

`tests/generative/{boundary,combinatorial,noise,overlap}.py` each do
`from harness.generators... import ...`. That `harness` package is real and lives
at `4DLabV2/harness/harness/`, but the gaslab lab has **no mechanism to make it
importable**:

- no `conftest.py` anywhere in the lab (a `conftest.py` is pytest's per-folder
  setup file — the usual place to extend the import path),
- nothing in `pyproject.toml` under `[tool.pytest.ini_options]` to set a
  `pythonpath`,
- `harness` is not pip-installed into the environment.

So the canonical inner-loop command (`pytest -x -q`) **errors before running a
single test**:

```
ERROR tests/generative/test_boundary.py  - ModuleNotFoundError: No module named 'harness'
ERROR tests/generative/test_combinatorial.py
ERROR tests/generative/test_noise.py
ERROR tests/generative/test_overlap.py
!!! Interrupted: 4 errors during collection !!!
```

```
default `pytest` run
        │
        ▼
collect tests/generative/*  ──►  import harness  ──►  ModuleNotFoundError
        │                                                    │
        ▼                                                    ▼
core suite never runs                          whole run reported RED
```

With `PYTHONPATH=.../4DLabV2/harness` set, all four collect and **pass**. So this
is purely a wiring gap, not broken test logic. The fix is one small `conftest.py`
or a `pythonpath` line in `pyproject.toml` — but I've left that for the
document/code update pass per your direction.

### 1b. Generative tests are slow

Measured per file (sandbox, Python 3.14):

| Test file | Cases | Wall time | Result |
|---|---|---|---|
| `test_overlap.py` | 561 pairs / 50k samples | 0.5 s | pass |
| `test_boundary.py` | 1020 | 25 s | pass |
| `test_combinatorial.py` | 1360 | 41 s | pass |
| `test_noise.py` | 34 curves | > 42 s (did not finish in the sandbox cap) | slowest |
| `test_fuzz.py` | — | — | skipped (stub: "not implemented in shared engine") |

At ~25 ms per case these are too heavy to belong in the fast inner loop. If they
stay in the default `pytest` path they'll dominate every run; they read more like
a nightly/`-m slow` marked tier. (`-m slow` = a pytest label you opt into, so the
quick loop can skip them.) Worth a decision later.

---

## 2. Signal/noise — consumer compliance

The governing rule: every field in a schema needs a **named, live consumer** (a
real reader in code), or it doesn't ship.

### 2a. Output payload (`GasLabPayload` → COMLab) — mostly wired

GASLab's output is consumed by COMLab (which mirrors the type locally, no
cross-lab import — correct). Field-by-field reader in `labs/comlab/comlab/`:

| Output field | Live consumer in COMLab |
|---|---|
| `chemical_state` | `core/fault_atlas_router.py` ✓ |
| `lambda_chem` | `analytics/power_loss_analytics.py`, `core/lab_pipeline_aggregator.py` ✓ |
| `lambda_measured` | `lab_pipeline_aggregator.py` → `core/perception_contradiction.py` ✓ |
| `gas_co` | `power_loss_analytics.py` ✓ |
| `gas_hc` | `power_loss_analytics.py` ✓ |
| `gas_o2` | `power_loss_analytics.py` ✓ |
| `sample_validity` | `lab_pipeline_aggregator.py`, `schemas/vocabulary.py` ✓ |
| `gas_co2` | **no analytic reader** — only mirrored in `schemas/ingestion.py` + forwarded via `model_dump()` |
| `gas_nox` | **no analytic reader** — same as above |

`gas_co2` and `gas_nox` are carried across the boundary (defined in COMLab's
ingestion mirror, forwarded whole) but no COMLab analytic reads them yet. Per
your note these are **consumer-deferred to the COMLab v2 rework**, not breaches —
recording them so the rework picks them up, not flagging them for removal.

### 2b. DNA input slice (`GasLabDnaView`, 13 fields) — three orphans

This is the slim DNA slice GASLab *consumes*. Three fields are declared but read
in **zero** live code paths:

| DNA-view field | Live read-sites in `gaslab/` | Status |
|---|---|---|
| `target_lambda_v112` | 4 | consumed ✓ |
| `confidence` | 12 | consumed ✓ |
| `co_high_idle` | 4 | consumed ✓ (CHI-1) |
| `co_low_idle` | 3 | consumed ✓ |
| `upstream_o2_type` | 2 | consumed ✓ (T-GV2-10) |
| `cylinder_count` | 1 (`rule_engine.py:290`) | consumed ✓ (T-GV2-15) |
| `euro_emission_category` | 1 | consumed ✓ (T-GV2-8) |
| `induction_type` | 1 | consumed ✓ (T-GV2-9) |
| `has_catalyst` | 1 | consumed ✓ |
| `egr_equipped` | 1 | consumed ✓ |
| `engine_displacement_liters` | 0 | **orphan** |
| `fuel_delivery_type` | 0 | **orphan** |
| `number_of_banks` | 0 | **orphan — and ledger says it was dropped** |

The slice's own docstring says "GASLab does not consume the full `VehicleDNA`,"
so carrying three never-read fields cuts against that intent. `number_of_banks`
is the sharp one — see §3.

---

## 3. Ledger vs. code reality

The `PROGRESS.md` ledger is detailed and largely matches the code. All GASLab v2
code tasks are `done`, the test count climbs 164 → 207 across the task history,
and the current core run is exactly 207. Two mismatches:

**3a. `number_of_banks` — ledger says dropped, code still has it.**
Row `T-GV2-14` (status `void`, bank-asymmetry re-homed to OBDLabV2) states:
"`number_of_banks` dropped from the GASLab DNA-view slice." In the actual code,
`dna_view.py:30` still declares `number_of_banks: int = Field(..., ge=1, le=4)`,
read nowhere. Because `T-GV2-14` was voided with no code change, the disposition
("drop it") was decided but never executed. This is both a ledger-vs-reality
drift **and** the exact orphan the void row argued against. Clean removal is the
obvious follow-up.

**3b. Generative collection break not reflected.**
The ledger's repeated "207 GAS green" is true for the core suite but is silent on
the generative tree, which doesn't collect under a default `pytest`. Anyone
trusting the ledger and running `pytest -x -q` will see red, not green. Worth a
one-line note in the ledger once the wiring is fixed.

Nothing was flipped to `done` with an unmet contract that I could find — the
two historic near-misses (T-GV2-4 / `co_high_idle`, FU-CYL / `cylinder_count`)
are both genuinely closed: their consumers now read in live paths
(`resolution.py`, `rule_engine.py:290`).

---

## 4. Code quality review

Hygiene is strong. Across all of `gaslab/` (1,992 lines, 11 modules):

- **No cross-lab Python imports** (comlab/obdlab/dtclab/dnalab/vinlab) — boundary rule honoured.
- **No imports from `ARCHIVE/`, `v2/`, `v6/`** — legacy rule honoured.
- **No bare/broad `except`**, no `print()` calls, no mutable default arguments, no `TODO/FIXME/HACK`.
- **Numeric-literal citations** are applied at the **rule-block level**: the first
  comparison in each multi-line `if (...)` carries a `# wiki:` / `# vocab:` tag and
  continuation lines inherit it. Under a strict per-line reading of "every literal
  cites a wiki" a few continuation lines (e.g. `rule_engine.py` L310–313, L325–328)
  lack their *own* inline cite, but the governing reference is present per block.
  This is consistent with the new `GW-ENH-3` citation-cleanup task authored today.

**One real smell — stale naming from the retired enum.** `rule_engine.py:295` is
still headed `# Wrong Valve Timing rule` and keys off `grammar.get("wrong_valve_timing_rule", ...)`,
but the enum `WRONG_VALVE_TIMING` was retired in T-GV2-1 and the branch now
returns `CAM_TIMING_RETARDED_MAF` / `CAM_TIMING_ADVANCED`. The behaviour is
correct and tested; only the rule name + grammar key still carry the old label,
which is a future-confusion hazard. Renaming touches the ontology grammar key too,
so it's a small deliberate task, not a drive-by edit.

---

## Unplanned follow-ups (not actioned this session)

| ID | Finding | Suggested disposition |
|---|---|---|
| AUD-1 | Generative tests fail collection under default `pytest` (no `conftest.py`/`pythonpath` for `harness`) | Add a `conftest.py` or `pyproject` `pythonpath`; one small task |
| AUD-2 | Generative suite very slow (25–42 s/file) | Mark `slow`/move to a nightly tier so the inner loop stays fast |
| AUD-3 | `number_of_banks` orphan still in `dna_view.py` despite T-GV2-14 "dropped" | Remove from the DNA slice (executes the void disposition) |
| AUD-4 | `engine_displacement_liters`, `fuel_delivery_type` orphans in DNA slice | Name a consumer or drop, per signal/noise |
| AUD-5 | `gas_co2`, `gas_nox` carried with no COMLab analytic reader | Consumer-deferred to COMLab v2 rework (owner-confirmed) — track, don't remove |
| AUD-6 | `wrong_valve_timing_rule` stale name/grammar key in `rule_engine.py` | Rename rule + ontology grammar key in one task |
| AUD-7 | Ledger "207 green" silent on generative collection break | One-line ledger note after AUD-1 |

---

## What's green and safe to build on

Core diagnostic engine (5-gas pipeline, 34-value `ChemicalSignature`, dual-RPM
routing, Brettschneider lambda) is fully tested (207 passing), lint/type clean,
and isolated correctly from the other labs. The findings above are all at the
test-harness wiring and schema-housekeeping layer — none touch the diagnostic
logic.
