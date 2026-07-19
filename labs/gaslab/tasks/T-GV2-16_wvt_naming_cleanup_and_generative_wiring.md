# T-GV2-16 — WVT naming cleanup + generative-test wiring

**Status:** done
**Blocked by:** — (all GASLab v2 code tasks `done`)
**Authored:** 2026-06-10 (architect) — origin: `docs/audits/AUDIT_2026-06-10_gaslab_state.md` (AUD-1, AUD-2, AUD-6)
**Stage:** 1 (GASLab v2) — post-migration maintenance
**Type:** naming cleanup + test infrastructure. **No diagnostic-logic change. No schema field/enum added or removed.**

---

## Signal/noise statement (gate)

This task **adds no field and no enum**. The renamed rule's consumer is
**unchanged**: `chemical_state` is read by COMLab `core/fault_atlas_router.py`.
The test wiring adds no schema surface. Signal/noise gate is therefore satisfied
trivially — there is nothing new to consume.

`number_of_banks`, `engine_displacement_liters`, `fuel_delivery_type` (DNA-view
orphans) and `gas_co2` / `gas_nox` (output, consumer-deferred to the COMLab v2
rework) are **explicitly out of scope** here — owner direction 2026-06-10.

---

## Scope

Two bundled maintenance items (owner chose a single combined task). Both are
non-logic: behaviour and test outcomes must be identical before/after, only
names and test plumbing change.

### Part A — WRONG_VALVE_TIMING naming cleanup (AUD-6)

The `WRONG_VALVE_TIMING` enum was retired in T-GV2-1; the rule now returns
`CAM_TIMING_RETARDED_MAF` / `CAM_TIMING_ADVANCED`. But the rule header, the
ontology grammar key, and two test names still carry the dead label. Rename to
match what the rule actually emits.

| # | File:line | Now | Change to |
|---|---|---|---|
| A1 | `gaslab/data/gas_lab_ontology.yaml:58` | key `wrong_valve_timing_rule:` | `cam_timing_rule:` — **keep** `citation`, `description`, `hc_threshold: 1000`, `o2_threshold: 2.0` byte-identical |
| A2 | `gaslab/rule_engine.py:295` | `# Wrong Valve Timing rule — wiki: GAS_WIKI §8.6 (priority 82)` | `# Cam-timing rule — wiki: GAS_WIKI §8.6 (priority 82)` |
| A3 | `gaslab/rule_engine.py:296` | `grammar.get("wrong_valve_timing_rule", {})` | `grammar.get("cam_timing_rule", {})` — keep the `1000` / `2.0` literal fallbacks **and** their `# wiki:` cites |
| A4 | `tests/unit/test_rule_engine.py:198` | `def test_wrong_valve_timing_emitted_for_canonical_signature` | `def test_cam_timing_emitted_for_canonical_signature` (+ update the L194 section banner and the "WVT" wording in the docstring; assertions already check `CAM_TIMING_RETARDED_MAF` — leave them) |
| A5 | `tests/unit/test_rule_engine.py:228` | `def test_wrong_valve_timing_priority_above_collision` | `def test_cam_timing_priority_above_collision` (+ L224 banner / docstring wording) |
| A6 | `tests/unit/test_validators.py:158` | dead string pair `("RICH_MISFIRE", "WRONG_VALVE_TIMING")` in `REASONING_RESOLVED` | **Investigate, then fix.** `WRONG_VALVE_TIMING` is no longer a `ChemicalSignature`. Determine what `REASONING_RESOLVED` is iterated against; replace with the live label this pair now represents — `("RICH_MISFIRE", "CAM_TIMING_RETARDED_MAF")` — **or** delete the pair if the collision-vs-cam-timing precedence is already covered by the renamed A4/A5 tests. **Hard rule: do not leave a dead enum string in a live test path.** |
| A7 | `tests/unit/test_validators.py:431` | comment "Gaps closed by T-P6-3 (WRONG_VALVE_TIMING via WVT rule)" | update wording for accuracy (low priority, same pass) |

**Do NOT touch** `tests/unit/test_contracts.py:32/35` — those assert
`WRONG_VALVE_TIMING` is **absent** from the enum. That assertion is correct and
must stay green; it is the guard that the retirement holds.

### Part B — generative-test wiring + slow tier (AUD-1, AUD-2)

The four `tests/generative/*` modules import `from harness.generators... import ...`,
but gaslab has no `tests/conftest.py` and no `pythonpath`, so a plain
`pytest` from the lab **errors at collection** (`ModuleNotFoundError: harness`).
obdlab/dtclab/comlab already solve this with a `tests/conftest.py` that puts the
shared harness root on `sys.path`.

| # | Action |
|---|---|
| B1 | **Add `tests/conftest.py`** mirroring `labs/obdlab/tests/conftest.py`'s harness-root block — only the `sys.path` insertion is needed (gaslab does not need obdlab's CSV/fixture helpers): `_HARNESS_ROOT = Path(__file__).resolve().parent.parent.parent.parent / "harness"; sys.path.insert(0, str(_HARNESS_ROOT))` guarded by an `if not in sys.path`. Add a one-line docstring naming the purpose. |
| B2 | **Register a `slow` marker** in `pyproject.toml [tool.pytest.ini_options]`: `markers = ["slow: heavy generative cases (1000+ runs); excluded from the fast inner loop"]`. |
| B3 | **Decorate the active generative tests** `@pytest.mark.slow`: `test_boundary.py`, `test_combinatorial.py`, `test_noise.py`, `test_overlap.py`. (`test_fuzz.py` is already `@pytest.mark.skip` — leave it.) |
| B4 | **Set** `addopts = "-m 'not slow'"` in the same pytest section so the default `pytest -x -q` runs the fast core suite and **deselects** (not errors on) the generative tier. |

**Design note for owner (decision recorded, not re-asked):** B4 makes the
generative tier opt-in. The fast inner loop stays ~4.5 s and green; the full
generative tier runs explicitly via `pytest -m slow`. The verification gate for
*this* task must run **both** (see below) so we prove the wiring works, not just
that the default went green by hiding the tests.

**Boundary-rule note:** putting `harness` on `sys.path` inside a **test**
conftest is **not** a cross-lab Python import violation. The no-cross-lab-import
rule governs lab *source*; `harness` is shared test infrastructure, imported only
by test modules, and obdlab/dtclab/comlab set the precedent. Do not flag it.

---

## Files touched

```
gaslab/data/gas_lab_ontology.yaml            (A1)
gaslab/rule_engine.py                        (A2, A3)
tests/conftest.py                            (B1 — NEW)
tests/unit/test_rule_engine.py               (A4, A5)
tests/unit/test_validators.py                (A6, A7)
tests/generative/test_boundary.py            (B3)
tests/generative/test_combinatorial.py       (B3)
tests/generative/test_noise.py               (B3)
tests/generative/test_overlap.py             (B3)
pyproject.toml                               (B2, B4)
tasks/progress_notes/T-GV2-16.md             (NEW — gate blocks)
```

## Out of scope (do not touch)

- DNA-view orphans `number_of_banks` / `engine_displacement_liters` /
  `fuel_delivery_type` — owner-deferred (see audit AUD-3/AUD-4).
- `gas_co2` / `gas_nox` — stay as-is, consumer-deferred to COMLab v2 rework.
- Any threshold, predicate, or routing change. This task must not move a verdict.
- `graphify` / KG re-extraction — forbidden per `GASLAB_TASKS_START_HERE.md §0`.

---

## Verification gate (coder fills `progress_notes/T-GV2-16.md`)

Inner loop after each meaningful edit: `ruff` → `pyright` → `pytest -x -q`.

Done means **all** of:

1. `ruff check .` clean; `pyright` clean (0/0/0).
2. `pytest -x -q` green with the **same** counts as today — **207 passed, 1
   skipped**. Identical counts are the proof Part A changed no behaviour.
3. `pytest -m slow` green: 4 generative tests pass (note `test_noise.py` is the
   slowest, ~40 s+; `test_combinatorial.py` ~41 s; `test_boundary.py` ~25 s;
   `test_overlap.py` <1 s), `test_fuzz.py` skipped. This proves B1 wiring works.
4. `grep -rn "wrong_valve_timing\|WRONG_VALVE_TIMING" gaslab/ tests/` returns
   **only** the `test_contracts.py` retirement assertion (lines 32/35). No live
   rule/grammar/test-name use of the dead label remains.
5. Anti-orphan / boundary: no new schema field; no `harness` import added to any
   `gaslab/*.py` source file (test conftest only).

**Hard stops:** any pytest failure; core count drifts from 207/1; a verdict
changes; `WRONG_VALVE_TIMING` survives anywhere as a live label. Log a blocker,
do not flip to `done`.

## Commit (owner, PowerShell — by explicit path)

```powershell
cd C:\Users\muto\claude\4DApp\4DLab
git add `
  labs/gaslab/gaslab/data/gas_lab_ontology.yaml `
  labs/gaslab/gaslab/rule_engine.py `
  labs/gaslab/tests/conftest.py `
  labs/gaslab/tests/unit/test_rule_engine.py `
  labs/gaslab/tests/unit/test_validators.py `
  labs/gaslab/tests/generative/test_boundary.py `
  labs/gaslab/tests/generative/test_combinatorial.py `
  labs/gaslab/tests/generative/test_noise.py `
  labs/gaslab/tests/generative/test_overlap.py `
  labs/gaslab/pyproject.toml `
  labs/gaslab/tasks/progress_notes/T-GV2-16.md `
  labs/gaslab/tasks/PROGRESS.md `
  labs/gaslab/tasks/T-GV2-16_wvt_naming_cleanup_and_generative_wiring.md
git commit -m "T-GV2-16: WVT naming cleanup + generative-test conftest/slow wiring"
```
