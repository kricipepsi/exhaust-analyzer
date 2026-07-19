# REG-V2-INTEGRATE — Session handoff (v2)

**Session paused:** after File 5 complete and verified. All 5 deliverable
files + 1 unplanned shim-fix file are written and pass their inner loops.
The side-by-side cutover run has been executed once and **PASSES**.
**Reason for pause:** user requested a clean context break before the final
verification gate + ledger/commit step.
**Resume entry point:** Step 5 below (full task `### Verification ###` block),
then Steps 6–7 (cutover decision is already known — write it up — then ledger
+ commit).

---

## What is DONE this session (Files 1–5 + shim fix)

All inner loops = `py_compile` ✓ `ruff` ✓ `pyright` 0/0/0 ✓ `pytest` ✓.

1. **Shim loader refactor** — `registry/integration_shim.py`
   `_load_all_rulesets(rules_dir, expected_files=_EXPECTED_RULE_FILES)` and
   `RegistryV2Router.__init__(..., expected_files=...)` now accept
   `expected_files=None` to glob `*.json` (synthetic `tmp_path` fixtures).
   Production default unchanged (13 required files).

2. **File 2** — `registry/tests/test_integration_shim.py` — CREATE.
   **12 tests** (11 spec + 1 defensive `_DEFAULT_RULES_DIR` guard). All pass.
   Synthetic/real allocation per the locked table in the progress note.
   Test 7 (`test_cs_002_no_fire_on_missing_chemistry`) = the CS-002
   router-assumption gate, **real registry, PASSES** (MF-005 wins on
   `chem=None,dtcs=[P0562]`; CS-002 suppressed).

3. **File 3** — `COMLab/comlab/core/fault_atlas_router.py` — MODIFY.
   `import os` added; `self._use_v2_registry = os.environ.get("USE_V2_REGISTRY","0")=="1"`
   in `__init__`; lazy delegate at top of `route()`:
   `from registry.integration_shim import route_case; return OrchestratorFinalUIOutput(**route_case(sanitized))`.
   COMLab v1 regression: **277 passed, 4 skipped** (pre-existing skips).

4. **File 4** — `COMLab/tests/unit/test_fault_atlas_router_v2.py` — CREATE.
   ⚠ NOTE PATH: spec said `COMLab/comlab/core/tests/` but that dir does NOT
   exist — COMLab tests live at `COMLab/tests/unit/`. File placed there.
   **9 tests** (4 named + 6 parametrized garbage cases). All pass.
   `test_v1_default_when_env_unset` drives a real `route()` and asserts the
   shim is never called. Imports `_make_request`/`_sanitized` from sibling
   `tests.unit.test_fault_atlas_router`.

5. **Shim fix (unplanned, Option (a) — locked by user)** —
   `registry/shim/__init__.py` + `registry/shim/payload_mirrors.py` — CREATE,
   plus `registry/tests/test_payload_mirrors.py` — CREATE (**8 tests, pass**).
   **Root cause (REG-V2-INTEGRATE-SCHEMA-DRIFT):** shim emitted a dict whose
   `session_id` (any string / absent) and `user_input_echo_audit` (None)
   failed `OrchestratorFinalUIOutput(**dict)` reconstruction — `session_id` is
   `UUID4`-required, `user_input_echo_audit` is non-null-required.
   **Fix:** `resolve_session_id(payload)` → metadata session_id if valid UUID4,
   else **stable sentinel** `00000000-0000-4000-8000-000000000000` + a logged
   warning (NEVER a fresh per-call UUID — traceability).
   `resolve_user_input_echo_audit(payload)` → passthrough or schema sentinel
   `{submitted_at:<now ISO>, groups:[]}`. Wired into `_translate_to_output`.
   **An interim editor pass had inserted a `str(uuid.uuid4())` per-call default
   and a `1970-01-01` epoch echo stub — BOTH were replaced** by the helper
   calls (they violated the locked decision). Verified end-to-end: empty
   payload reconstructs to sentinel; real payload preserves session_id verbatim.

6. **File 5** — `4DLabWired/harness/run_side_by_side.py` — CREATE.
   Subprocess twin-run wrapper (v1 default, then `USE_V2_REGISTRY=1`), parses
   both `HARNESS_REPORT.md` outputs (summary regex + miss-list regex), writes
   `SIDE_BY_SIDE_REPORT.md`, exits 0/1/2.
   **Executed once, end-to-end: EXIT 0, CUTOVER GATE PASS.**

---

## CUTOVER RESULT (already computed — do not re-derive, just re-verify)

```
| Path | Total | Passed | Failed | Errors | Accuracy |
| v1   | 281   | 45     | 203    | 33     | 16.0%    |
| v2   | 281   | 75     | 166    | 40     | 26.7%    |
| Δ    | —     | +30    | -37    | +7     | +10.7pp  |
```

- **CUTOVER GATE: PASS** (v2 PASS=75 ≥ v1 PASS=45). Decision = **`Status=done`**.
- 55 new wins (v1 FAIL→v2 PASS), 25 regressions (v1 PASS→v2 FAIL), net +30.
- +7 errors under v2 (33→40) — worth a one-line note in the progress note's
  divergence section; does NOT block the gate. Candidate detail for the
  optional `REG-V2-INTEGRATE-TUNE` follow-up (NOT filed as blocking — gate
  passed). The 25 regressions are also tuning fodder, not a blocker.
- Report at `4DLabWired/harness/SIDE_BY_SIDE_REPORT.md` (+ `_v1.md`, `_v2.md`).
- CS-002 router-assumption gate: **PASS**.

---

## Resume here next session

### Step 0 — Re-bootstrap
Follow `REGISTRY_START_HERE.md` steps 1–8. At step 8 read THIS handoff +
`progress_notes/REG-V2-INTEGRATE.md` + `REG-V2-INTEGRATE_wire_to_comlab.md`.
Sandbox `python3.14` is on PATH already (3.14.4).

### Step 1 — Sandbox PYTHONPATH (REQUIRED to run the harness/aggregator)
The harness needs every lab package on `PYTHONPATH`. From `4DLab/`:
```
PP="4DLabWired;GASLab;COMLab;OBDLab/code;DTCLab/code;DNALab;."
```
(Windows `;` separator; `python3.14` is the Windows-native interpreter even
in the bash tool. Plain `:`-joined PYTHONPATH does NOT work.)

### Step 2 — Re-run the full task `### Verification ###` block
Lines 116–173 of `REG-V2-INTEGRATE_wire_to_comlab.md`. Each step, from `4DLab/`:
```
python3.14 -m py_compile registry/integration_shim.py
python3.14 -m py_compile COMLab/comlab/core/fault_atlas_router.py
python3.14 -m ruff check registry/integration_shim.py registry/tests/test_integration_shim.py
python3.14 -m pyright registry/integration_shim.py registry/tests/test_integration_shim.py
python3.14 -m pytest registry/tests/test_integration_shim.py -x -q          # 12 pass
python3.14 -m pytest registry/tests/ -x -q                                  # full registry regression
PYTHONPATH="$PP" python3.14 -m pytest COMLab/tests/ -x -q                    # COMLab v1 (note: NOT COMLab/comlab/core/tests)
PYTHONPATH="$PP" python3.14 -m pytest COMLab/tests/unit/test_fault_atlas_router_v2.py -x -q  # 9 pass
# CS-002 gate (real registry):
python3.14 -m pytest registry/tests/test_integration_shim.py::test_cs_002_no_fire_on_missing_chemistry -x -v
python3.14 -m pytest registry/tests/test_integration_shim.py::test_cs_002_fires_on_normal_chemistry -x -v   # NOTE: this test name in File 2 is `test_cs_002_fires_on_normal_chemistry` (synthetic)
# Side-by-side (re-run to confirm exit 0; takes ~4–5 min for both passes):
PYTHONPATH="$PP" python3.14 4DLabWired/harness/run_side_by_side.py; echo "exit=$?"
# Mirror invariant:
python3.14 -c "from registry.schema_v2 import DTCRoutingTag; n=len(list(DTCRoutingTag)); assert n==20; print('DTCRoutingTag',n)"
# Self-contained AST scan (the spec's inline block, lines 156-172):
python3.14 -m pytest registry/tests/test_integration_shim.py::test_no_unauthorised_imports -x -q
```
Paste headline results into the progress note's VERIFICATION GATE block.

### Step 3 — Run the verification-loop 6-phase outer gate
Produce the structured `VERIFICATION GATE` block in
`progress_notes/REG-V2-INTEGRATE.md` (replace the `<not yet evaluated>`
placeholder). Phase 5 = rule-set integrity + side-by-side (done, exit 0).

### Step 4 — Run the code-review skill against the full diff
Produce the `CODE REVIEW` block. Diff spans the 6 files listed below. Watch
for: the locked algorithm constants unchanged (`0.10/0.05/1.0`); no COMLab
imports in `registry/`; every numeric literal carries `# wiki:`/`# convention:`.

### Step 5 — Write final progress note + ledger row (Status=done)
- Fill VERIFICATION GATE + CODE REVIEW blocks in
  `progress_notes/REG-V2-INTEGRATE.md`.
- Edit `REGISTRY_PROGRESS.md`: flip `REG-V2-INTEGRATE` `Status=done`, Files=6
  (spec said 5; +1 for the unplanned `payload_mirrors.py` schema-drift fix —
  note this in the row), Verification one-liner:
  `"v1 PASS=45 (16.0%) → v2 PASS=75 (26.7%); cutover gate PASS; CS-002 router-assumption gate PASS"`.
  Commit cell = literal `<COMMIT_HASH>`.
- **Close unplanned follow-up `CS-002-router-assumption`** (gate test passes).
- **File new unplanned follow-up `REG-V2-INTEGRATE-SCHEMA-DRIFT`** — one line:
  "shim output contract vs OrchestratorFinalUIOutput acceptance contract were
  not aligned (shim built against input shape, not output schema); fixed via
  registry/shim/payload_mirrors.py; future shim work must verify both ends."
- **File `REG-V2-INTEGRATE-SPEC-PATCH`** (zero-GATING firing predicate, already
  documented) per the existing progress note.
- Do NOT file `REG-V2-INTEGRATE-TUNE` as blocking (gate passed). Optionally
  log it as a non-blocking follow-up for the 25 regressions + 7 new errors.

### Step 6 — Emit the commit-and-patch PowerShell block (user pastes once)
Per `REGISTRY_START_HERE.md` §Session-end checklist Edit 11. Commit message:
`"REG-V2-INTEGRATE: wire v2 registry into COMLab behind USE_V2_REGISTRY; side-by-side cutover PASS (45→75)"`.

---

## Files created/modified this session (the diff)

```
M  registry/integration_shim.py                                  (loader refactor + payload_mirrors wiring)
C  registry/shim/__init__.py                                     (new package)
C  registry/shim/payload_mirrors.py                              (schema-drift fix — Option a)
C  registry/tests/test_integration_shim.py                       (12 tests)
C  registry/tests/test_payload_mirrors.py                        (8 tests)
M  COMLab/comlab/core/fault_atlas_router.py                      (env-var read + lazy v2 delegate)
C  COMLab/tests/unit/test_fault_atlas_router_v2.py               (9 tests)
C  4DLabWired/harness/run_side_by_side.py                        (cutover wrapper)
+  4DLabWired/harness/SIDE_BY_SIDE_REPORT.md  (+ _v1.md, _v2.md)  (run artefacts)
M  4DLabWired/harness/HARNESS_REPORT.md                          (overwritten by last run = v2 state)
```
No commits yet — wait for full task completion per Edit 11 commit-and-patch.

---

## Key facts for the resuming session

- **Locked algorithm constants (do NOT change):** `_TIER_BONUS_DEFINITIVE=0.10`,
  `_TIER_BONUS_SUGGESTIVE=0.05`, `_CONFIDENCE_HARD_CAP=1.0`.
- **Locked decisions:** zero-GATING firing predicate = Option 1 (require ≥1
  satisfied evidence row). Schema-drift = Option (a) (validate at boundary,
  default via payload_mirrors, NEVER model_construct/bypass).
- **Sentinel session_id is STABLE** `00000000-0000-4000-8000-000000000000` —
  never per-call UUID (traceability across the side-by-side harness).
- **`OrchestratorFinalUIOutput` requires** `session_id: UUID4` and a non-null
  `user_input_echo_audit: UserInputEchoAudit{submitted_at: datetime, groups: list}`.
- **Aggregator overwrites** session_id + echo with its own Stage-A values on
  the v2 path (`lab_pipeline_aggregator.process` L372-378), BUT `route()` must
  still reconstruct `OrchestratorFinalUIOutput` first (L339) — so the
  payload_mirrors fix is load-bearing regardless.
- **COMLab test dir is `COMLab/tests/unit/`** (NOT the spec's
  `COMLab/comlab/core/tests/`, which does not exist).
- **Harness run = ~2 min per pass**, ~4–5 min for the side-by-side wrapper.
```
