# OBDLab audit — Lens 3/5: `code-review` (Code Review Excellence)

**Date:** 2026-06-08 · **Auditor role:** architect (read + report; no code edits) ·
**Skill:** `_skills/codingskills/code-reviev` (logic & edge cases, security, performance,
maintainability, error handling; severity-labelled feedback).
**Subject:** `4DLabV2/labs/obdlab/obdlab/` real source (sandbox mirror was truncated and
not used — see `AUDIT_01`).

This report also hosts the **consolidated severity ranking** and the **Unplanned
follow-ups** table for all five lenses.

Severity key: 🔴 `[blocking]` · 🟡 `[important]` · 🟢 `[nit]` · 🎉 `[praise]`.

---

## Findings — line-by-line review

### 🔴 CR-1 `[blocking]` Physics Gate 3 never fires in the live pipeline
`core/semantic_consistency_checker.py` L144 reads `sanitized_pids["calculated_ve"]`, but
`translate()` runs the semantic checker at step [3] **before** VE is computed at step [4]
(`sensor_signal_translator.py` L114 vs L137), and never assigns `calculated_ve`. The gate
therefore always returns at the `is None` guard (L147). It is only ever exercised by
`tests/unit/test_semantic_consistency_checker.py`, which **injects** `calculated_ve`
directly (L52, L127-188). Green unit tests mask a dead integration gate.
→ Primary spec: **T-OBDV2-AUDIT-CR-1**. Cross-ref `AUDIT_02` UB-2, `AUDIT_05` E-2.

### 🔴 CR-2 `[blocking]` Wideband offset detector is dead — enum compared to wire string
`core/o2_normalizer.py` `_wideband_passthrough` gates the `WIDEBAND_OFFSET_CANDIDATE`
finding on `is_closed_loop = fuel_status == "Closed_Loop"` (L185). But by the time O2
normalisation runs, `PIDIngestionValidator._validate_and_map_fuel_system_status`
(L184-188) has already replaced `fuel_sys_status` with a **`FuelSystemStatus` enum**
(value `"CL"`). `FuelSystemStatus.CL == "Closed_Loop"` is `False`, so `is_closed_loop` is
always `False` and the offset branch (L189-191) can never run. The documented
`WIDEBAND_OFFSET_CANDIDATE` fault is unreachable in production.
- **Fix:** compare against `FuelSystemStatus.CL` (and read the canonical key), not the raw
  wire string. Add an integration assertion that a warm, closed-loop, off-stoich wideband
  reading yields `WIDEBAND_OFFSET_CANDIDATE`.

### 🟡 CR-3 `[important]` No-op `try/except` obscures the control flow
`semantic_consistency_checker.py` L52-74 — each gate is wrapped in a `try/except` that
only re-raises. Delete the scaffolding. (Primary spec in `AUDIT_02` UB-4 /
T-OBDV2-AUDIT-UB-3.)

### 🟡 CR-4 `[important]` `number_of_banks` default disagrees across modules
- `pid_ingestion_validator._validate_bounds` L232 → default **2**
- `pid_ingestion_validator._enforce_bank2_contract` L302 → default **2**
- `trim_vector_aggregator.aggregate` L45 → default **1**
- `sensor_signal_translator` (assembly) L221 → default **1**

When `number_of_banks` is absent, the validator treats the engine as **2-bank** (validates
`shrtft2`/`longft2` if present, and the null-contract early-returns) while the aggregator
and payload assembly treat it as **1-bank** (`shrtft2`/`longft2` → `None`). The two halves
of the pipeline disagree about the same vehicle. Pick one default (almost certainly **1**,
matching petrol-inline assumption) and use it everywhere, or require the field.

### 🟢 CR-5 `[nit/question]` Wideband out-of-range clamps to `NO_FAULT`
`o2_normalizer._wideband_passthrough` L165-176: a ratio below 0.7 or above 1.3 is clamped
and returned with mode `O2_CHANNEL_FAULT` but `O2FailureMode.NO_FAULT`. The narrowband
branch maps the analogous out-of-range to `STUCK_LEAN`/`STUCK_RICH` (L122-135). Is a
wideband channel pegged past its physical rail really "no fault"? Confirm against
OBDLab_KG_Wiki §11.2/§6.7 — if it should be a fault, the failure mode is being lost here.

### 🟢 CR-6 `[nit]` `ve_pct_raw or 0.0` collapses a legitimate zero
`sensor_signal_translator.py` L140 `ve_pct_val = ve_pct_raw or 0.0`. If VE ever computes to
exactly `0.0` (vs `None`), `or` treats it the same as "missing". Prefer
`ve_pct_val = 0.0 if ve_pct_raw is None else ve_pct_raw`. Low impact (0.0 and None already
both suppressed downstream via `ve_validity`), hence nit.

### 🎉 CR-7 `[praise]` Security & performance posture is clean
- **Security:** attack surface is a manual PID dict — no SQL, network, `eval`, subprocess,
  pickle, or secret handling. `yaml.safe_load` (not `yaml.load`) and `json.load` are used
  correctly. Bounds validation rejects non-numeric and out-of-range inputs before compute.
  Nothing to flag.
- **Performance:** per-payload work is O(small) — no N+1, no quadratic loops; `sorted()` in
  `ranking.py` is over ≤ a handful of candidates. No concern at this scale.
- **Edge handling:** the `None`-guarding across `VEEngine` branches and the bank-2 null
  contract are thorough and well-tested. Good defensive style.

---

## Consolidated severity ranking (all five lenses)

| # | Sev | Finding | Files | Lens(es) |
|---|-----|---------|-------|----------|
| CR-1 | 🔴 | Physics Gate 3 dead (calculated_ve never set pre-semantic) | semantic_consistency_checker, sensor_signal_translator | CR, UB, ECC |
| CR-2 | 🔴 | Wideband offset detector dead (enum == wire-string) | o2_normalizer | CR |
| UB-1 | 🔴 | Stateful orchestrator — two-point linearity leaks across calls | sensor_signal_translator | UB, ARCH, CR |
| CR-4 | 🟡 | `number_of_banks` default mismatch (2 vs 1) | pid_ingestion_validator, trim_vector_aggregator, sensor_signal_translator | CR |
| UB-3 | 🟡 | Fuel-status wire→enum map triplicated | pid_ingestion_validator, semantic_consistency_checker, analytics_preconditions | UB, PY |
| UB-4/CR-3 | 🟡 | No-op `try/except` in `evaluate` | semantic_consistency_checker | UB, CR |
| UB-5 | 🟡 | `_evidence_tier` dead calls + duplicate tier logic | ranking | UB |
| UB-6 | 🟡 | Inconsistent exception taxonomy (AssertionError; gate-4 ValueError) | exceptions, semantic_consistency_checker | UB |
| AR-1 | 🟡 | `ranking.py`/`family_map.py` have no live consumer (only archived *Simple) | ranking, family_map | ARCH (signal/noise) |
| AR-2 | 🟡 | Orphan vocab/schema members: `VERoutingMode`, `cylinder_count`, `O2FailureMode.{SLUGGISH,WRONG_CENTERLINE,HEATER_FAULT,DEAD}` | vocabulary, dna_view | ARCH (signal/noise) |
| P-1 | 🟡 | Inner-loop ruleset thinner than skill (no B/S; pyright basic) | pyproject.toml | PY, ECC |
| P-2 | 🟡 | Exception chaining lost (`raise ... from`) | pid_ingestion_validator | PY |
| E-1 | 🟡 | Generative test layer entirely skipped stubs | tests/generative, tests/test_cases.py | ECC |
| CR-5 | 🟢 | Wideband out-of-range → NO_FAULT (confirm intent) | o2_normalizer | CR |
| CR-6 | 🟢 | `ve_pct_raw or 0.0` collapses legit zero | sensor_signal_translator | CR |
| P-3 | 🟢 | Duplicated threshold constants (70/90) | o2_normalizer, analytics_preconditions | PY |
| P-4 | 🟢 | Dead `total_trim` param | o2_normalizer | PY |
| P-5 | 🟢 | Import-time YAML I/O | state_bucketing | PY |
| ARCH-3 | 🟢 | Doc-vs-code drift: `FAULT_VE_SENSOR_SKEW` 85% vs code 90% | vocabulary, ve_engine | ARCH, CR |
| E-3 | 🟢 | Fixtures duplicated across test files (empty conftest) | tests/* | ECC |

## Unplanned follow-ups (off the audit's own path — for the owner to triage)

| Item | Why noted | Suggested home |
|------|-----------|----------------|
| Sandbox mount serves **truncated** copies of ≥6 obdlab files | Breaks any sandbox `ruff/pyright/pytest`; risks false audits & bad diffs | Tooling/infra — run inner loop in Windows `.venv-wired`; investigate the mount sync |
| No coding skill loaded before the OBDLab coder ran (owner's original observation) | Process gap that this audit retro-covers | Coder-session bootstrap checklist (`OBDLAB_TASKS_START_HERE.md`) |
| `VEEngine._classify_validity` (FAULT_VE_SENSOR_SKEW) may duplicate Physics Gate 3's intent | Surfaced while resolving CR-1 | Fold into the CR-1 architect decision |
| `O2FailureMode.WIDEBAND_OFFSET_CANDIDATE` only produced by the (currently dead) CR-2 branch | Its sole producer is broken | Resolve with CR-2; then confirm a COMLab consumer |

---

## Draft task specs (code-review lens)

### T-OBDV2-AUDIT-CR-1 — Resolve Physics Gate 3 (CR-1) **[architect decision first]**
- **Files:** `core/semantic_consistency_checker.py`, `core/sensor_signal_translator.py`,
  `tests/integration/test_pipeline_smoke.py` (add a firing assertion),
  `tests/unit/test_semantic_consistency_checker.py`
- **Decision:** (a) move the NA VE-ceiling check to **after** VE computation and feed it
  `ve_pct`; or (b) delete gate 3 and rely on `VEValidity.FAULT_VE_SENSOR_SKEW`; or (c) keep
  both with a documented division of labour. Default per v2-forward-progress: (a), so the
  semantic stage actually enforces the §4 physics limit.
- **Success:** an **integration** test drives an NA engine to VE > 90% at STABILIZED_IDLE
  and asserts the gate fires (raises or sets the documented bucket); not just a unit test
  that injects `calculated_ve`. `pytest -x -q` green; anti-orphan grep shows `calculated_ve`
  is written in a live path or removed.
- **Consumer (signal/noise):** the §4 semantic-gate contract consumed by COMLab fault-atlas
  routing (gate-violation → COLD/INVALID handling). No new field; if option (a) needs
  `ve_pct` passed into the checker, that is an internal arg, not a schema field.

### T-OBDV2-AUDIT-CR-2 — Fix the dead wideband offset detector (CR-2)
- **Files:** `core/o2_normalizer.py`, `tests/unit/test_o2_normalizer.py` (+ integration)
- **Change:** compare `fuel_status` against `FuelSystemStatus.CL` (canonical), reading the
  canonical sanitized key; add a test that a warm/closed-loop/off-stoich/not-WOT/not-DFCO
  wideband reading yields `O2FailureMode.WIDEBAND_OFFSET_CANDIDATE`.
- **Success:** new test fails before the fix, passes after; `pytest -x -q` green.
- **Consumer (signal/noise):** `O2FailureMode.WIDEBAND_OFFSET_CANDIDATE` must have a named
  COMLab/fault-atlas consumer — **name it in the task file**, else the fix re-animates an
  orphan (ties to AR-2).

### T-OBDV2-AUDIT-CR-3 — Align `number_of_banks` default (CR-4)
- **Files:** `core/pid_ingestion_validator.py` (L232, L302) — and confirm aggregator/assembly
- **Change:** standardise on default **1** (or require the field with a clear error); update
  the two validator sites.
- **Success:** an input omitting `number_of_banks` produces a self-consistent single-bank
  payload (`shrtft2`/`longft2` = None, no bank-2 validation); regression fixture added;
  `pytest -x -q` green.
- **Consumer:** the bank-2 fields already ship to COMLab; this only fixes default agreement.
  No new field.
