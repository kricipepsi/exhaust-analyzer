# DELTA pickup — START HERE (next session, fresh context)

**For:** the coder picking up `T-COMV2-DELTA-1`. **Written:** 2026-06-20 (architect). **Updated:** 2026-06-20 after session 2 (ran out of tokens mid-Pickup-A gate).
**Read order:** this file → `START_HERE.md` → `AGENTS.md` (five rules) → the epic `tasks/T-COMV2-DELTA-1_cross_lab_delta_module.md` → your assigned remaining sub-task. Post a scope-confirm before code.

---

## ▶ COPY-PASTE PROMPT FOR THE NEXT SESSION

```
You are a builder/coder on 4DLabV2. Continue task T-COMV2-DELTA-1 (cross-lab delta module),
resuming mid-Pickup-A. Fresh context.

BOOT: read labs/comlab/tasks/DELTA_PICKUP_START_HERE.md FIRST, then START_HERE.md, AGENTS.md
(five rules), the epic T-COMV2-DELTA-1, and sub-tasks 1B/1C (engine) + 1D (wiring).
Post a one-paragraph scope-confirm before any code.

STATE (architect-verified 2026-06-20): schemas done; comlab/analytics/delta_engine.py complete
(~25KB, all gates+profiles); entries.yaml COMLab-DELTA registered (:601); DEP-14 registered;
tests/unit/test_delta_engine.py WRITTEN (22 tests, parses clean) but NOT YET RUN GREEN.

YOUR FIRST ACTION — finish the Pickup-A gate (do not assume the tests pass):
1. Activate the shared venv: `source /agent_workspace/.venv-wired/bin/activate` (Py 3.14). Do NOT use system python3.12 — StrEnum
   ImportError. Purge stale __pycache__ if a .pyc shadows an edit.
2. Run:  ruff check . ; pyright comlab/ ; pytest tests/unit/test_delta_engine.py -q
3. Known-red baseline = ONLY the 2 registry failures in test_fault_atlas_router_v2.py (module
   'registry' absent from checkout — pre-existing, not yours). Anything else is in scope.
4. If any of the 22 delta tests fail: triage each as a test bug OR a real engine bug. A red here
   is the POINT of Pickup-A — the engine was written before its tests. Fix the cause; keep band
   policy unchanged (per-signal bands: ΔTrim @STRESS_IDLE, Δgas/ΔO2 @REGULATORY_HIGH_IDLE,
   ABSTAIN on mismatch). Any numeric literal you touch keeps/gets its # wiki: cite.
5. When green: fill VERIFICATION GATE + CODE REVIEW in progress_notes/ for 1A/1B/1C and flip
   those rows to done in PROGRESS.md.

THEN Pickup-B (sub-task T-COMV2-DELTA-1D): wire delta_signature into fault_atlas_router
execute_triage_loop Phase 5 — enable_delta flag (default-off), compute in route() v1 branch,
Phase 5 read score=max(score,confidence), thread the flag through lab_pipeline_aggregator,
add e2e single-point regression-lock + two-point activation. Consumer-read gate = two greps
(read site + the use_v2_registry=False branch). Single-point path byte-identical. Flip the epic
row to done. Then STOP.

DO NOT: run graphify / rebuild any KG; add cross-lab Python imports; touch the v2 registry shim
(that is the separate follow-up T-COMV2-DELTA-2 / COMLab-DELTA-V2); change USE_V2_REGISTRY default;
surface SINGLE_POINT into ExecutionMeta (live-activation follow-up).
```

---

## State on disk (architect-verified 2026-06-20 — trust this over memory)

**Done (sessions 1–2):**
- `comlab/schemas/vocabulary.py` — `SINGLE_POINT` mode (`:569`).
- `comlab/schemas/response.py` — `DegradationLit` widened (`:26`).
- `comlab/schemas/ingestion.py` — `SecondOperatingPointFrame` (`:370`) + `OrchestratorInboundRequest.second_operating_point` (`:463`).
- `comlab/analytics/delta_engine.py` — **complete** (25 KB): all models + `compute_delta_signature` + every gate/profile/assemble. Parses clean, 36 `wiki:`/`lld:` citations.
- `comlab/config/proposals/entries.yaml` — **`COMLab-DELTA` registered** (`:601`).
- `tests/unit/test_delta_engine.py` — **written** (20 KB, **22 tests**, parses clean, 28 `wiki:` cites): sentinel, architecture gate (incl. forced-induction inversion), 4 validity rejects, 4 ΔTrim profiles, 4 Δgas profiles, 3 abstain cases, 2 architecture-interplay cases. **NOT yet executed green** — see below.
- `docs/CROSS_LAB_DEPENDENCIES.md` — DEP-14 registered (architect).

**NOT done — remaining work, in order:**
1. **RUN `test_delta_engine.py` green** (the unfinished Pickup-A gate). The tests were written but never executed against the 3.14 venv — the architect can only confirm they *parse*, not that they *pass*. Since the 25 KB engine was written before its tests, treat the first run as real verification: a failure is likely a genuine engine bug, not just a test typo.
2. Fill `progress_notes/` gate blocks for 1A/1B/1C; flip those rows → `done`.
3. **Pickup-B (1D):** `comlab/core/fault_atlas_router.py` wiring (`enable_delta` flag + `route()` compute + Phase 5 read) — not started.
4. `comlab/core/lab_pipeline_aggregator.py` — flag not threaded.
5. `tests/e2e/` — no delta regression-lock / activation case.
6. Flip epic row → `done` after 1D.

---

## Environment (carry forward — don't re-investigate)

- **Working venv:** the shared `/agent_workspace/.venv-wired` (Py 3.14.6, pydantic 2.13, pytest 9.1, ruff, pyright). Activate it each bash session: `source /agent_workspace/.venv-wired/bin/activate`.
- **`.venv-wired` in `ARCHIVE/` is broken** (dead uv trampoline) — do not use.
- **Two pre-existing failures are NOT yours:** `test_fault_atlas_router_v2.py::test_v1/v2_when_explicit` → `ModuleNotFoundError: No module named 'registry'`. The `registry` module is absent from this checkout (same family as the missing `v2-restructure/`). Treat as a known-red baseline; do not chase. **This confirms the wiring target:** the v2 shim can't even run here, so v1 `execute_triage_loop` Phase 5 (`use_v2_registry=False`) is the only runnable — and correct — consumer. Wire there.

---

## Do it in this order (tests before wiring — load-bearing)

> **Why this order:** the engine is 25 KB of pure math with no tests. Wiring untested math into the live ranker (the coder's earlier #5-first order) is backwards. Lock the engine green first, *then* wire.

### Pickup-A — finish + lock the engine  (sub-tasks `1A` remainder + `1B`/`1C` tests)
1. **Baseline:** activate venv, run `ruff check . && pyright comlab/ && pytest -x -q`. Confirm only the 2 known `registry` failures are red. If the engine doesn't import, fix that first.
2. **`entries.yaml`** — append `COMLab-DELTA` per `T-COMV2-DELTA-1A` step 4 (consumer = `fault_atlas_router...execute_triage_loop  # Reader: T-COMV2-DELTA-1D`; status `proposed`).
3. **`tests/unit/test_delta_engine.py`** (NEW) — the fixture families from `T-COMV2-DELTA-1B` (sentinel, architecture, validity) **and** `T-COMV2-DELTA-1C` (ΔTrim/Δgas profiles, abstain, architecture null/inversion). Each fixture derived from `delta-relations/01–08` with a `# wiki:` cite; **no chunk coverage → no fixture**. Use the `test_symptom_prior.py` request-builder pattern (where session 1 stopped) as the template.
4. **Gate:** `pytest tests/unit/test_delta_engine.py -q` green; full suite still only the 2 known reds; `ruff`/`pyright` clean. This is where the 25 KB engine first earns trust — if a profile is wrong, it surfaces here, not in production. Fill `progress_notes/` + flip 1A/1B/1C rows.

### Pickup-B — wire it  (sub-task `1D`)
Follow `T-COMV2-DELTA-1D_router_wiring.md` exactly: `enable_delta` flag (default-off) + `route()` compute + Phase 5 read (`score = max(score, confidence)`) + aggregator thread + e2e (single-point regression-lock + two-point activation). **Consumer-read gate = two greps** (read site in Phase 5 + the `use_v2_registry=False` branch that reaches it). Single-point path must stay byte-identical. Flip the epic row → `done`.

(`T-COMV2-DELTA-2`, the v2-path activation, stays blocked until Pickup-B closes. Out of scope here.)

---

## Hard reminders (from `AGENTS.md` / epic)
- Per-signal bands locked: ΔTrim @ `STRESS_IDLE`, Δgas/ΔO₂ @ `REGULATORY_HIGH_IDLE`, **ABSTAIN on band mismatch**. Don't change the engine's band policy — verify the tests assert it.
- Every numeric literal carries a `# wiki:` cite. Reports `.md` only; archive, never delete.
- Don't run graphify / rebuild any KG. Don't add cross-lab Python imports.
- Default-off throughout; flipping `enable_delta` is the only behavioural change.
