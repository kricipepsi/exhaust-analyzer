# T-AUD-4t — authoring sidecar (Windows Cowork, 2026-11-06)

Survey: `C:/4DApp/recheck/scratch/survey_T-AUD-4t.md` (evidence-verifier). Rehearsal: `C:/4DApp/recheck/T-AUD-4t/`
(`apply_fix.py`, `rehearsal.patch`, `ast_same.py`).

### Verified context ###
1. **The ten fields are read only inside `execute_triage_loop` Phase-5 gates**, each `if self._enable_X and
   obd_live_data is not None:` (`fault_atlas_router.py`); `w_theo` is a span attribute only; `manifold_vacuum_kpa` is
   never read from the payload (`_resolve_pid` computes a PID of that name from freeze-frame baro minus MAP). Survey;
   Cowork re-read the guards (`grep -n "if self._enable_"`). Observed.
2. **Every `enable_*` flag defaults to False and no non-test code sets one** (`git grep` outside tests, audit/, Vault/
   finds only `fault_atlas_router.py`). Production reaches v1 only via env `USE_V2_REGISTRY=0`, and then with every
   gate off. Observed.
3. **Registry v2 has no reader of the ten fields** (no PID in `_PID_DISPATCH`, none in `rules/*.json`). Observed by the
   survey's greps.
4. **v1 is the evaluation baseline:** `apps/wired/HANDOFF_2026-06-30_NEXT_SESSION.md` T-V7-9 (`USE_V2_REGISTRY=0`
   fidelity diff), `fl_tasks` T-FL-1/T-FL-4. Observed.
5. **Rehearsal** (restored): comments and one docstring; `ast_same.py` prints `ast same` for both files, and a mutant
   (`enable_o2_offset` default True) prints `AST DIFFERS`; P1 counts 8 / 0 / 2 / 1; comlab 503/4/2 and wired 106 before
   and after; default `ruff` passes (the added text lengthens comment lines that already exceeded E501, which the
   project's ruff config does not select: 151 → 156 under `--select E501`). Observed.

### Rulings and the tradeoff that lost ###
- **Not ported to registry v2.** The gates never ran in production, even under v1; a port adds unvalidated diagnostic
  behaviour and moves verdicts, which is feature design, not an audit fix. Lost: whatever signal the gates carry.
- **Not retired.** The v1 loop is the evaluation baseline; deleting fields or gates breaks it and 17 test files. Lost:
  a smaller schema.
- **REVIEW_T-AUD-4a F2:** the reviewer's own fix for a non-default v1 ("record that explicitly") is applied at the PID
  site. Lost: aligning v1's source with `downstream_o2_v` (it would change the baseline).
- **Docs row:** no executable line changes (P2), so no second-model review (CLAUDE.md step 6: a docs row does not get
  one). Plan NONE, difficulty 1 (`--model claude-sonnet-5-5 --effort medium`).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `8`; `0`; `ingestion.py:2`, `fault_atlas_router.py:1`; two `ast same` (against `HEAD` before commit) |
| step 2 | SIMULATED | `503 passed, 4 skipped, 2 errors`; `106 passed` |
| step 3 | SIMULATED | `All checks passed!`; status clean after restore |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-4t: the ten v1-only OBD fields are labelled as feeding gates that are off by default.

### Cold read ###
own pass 2026-11-06: P1-P3 measured · `apply_fix.py` exits on any literal count other than 1 · counts: 8 `off by default`
= 7 field comments + the VE pair line (ecu_fuse, misfire, ltft_cell, w_theo, sensor_error, ve, fuelsys, o2) ·
traceability: criteria 1-3 → steps 1-3 · patched: explicit `BASE`; repo-wide baselines written · no finding.
cold read 2026-11-06 FOCUSED reader; trigger 1c grep hit (criterion 3 "only"); 0 findings, 0 patched — 3 calls.

### Correction history ###
(none)
