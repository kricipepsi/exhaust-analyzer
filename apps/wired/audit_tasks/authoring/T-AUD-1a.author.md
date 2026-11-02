# T-AUD-1a — authoring sidecar (Windows Cowork, 2026-11-02, re-authored in the loop format)

Source: the builder's spec at `ea8ef43`/`84da7a0` (`T-AUD-1a_app_usable.md`), Cowork rulings 006 (F-1 = A, C-1) and
008 (lab exception, COMLab-produced abort, two commits, R1 packaging), 007 (the old lab and wired skills no longer
govern; `writing-4dapp-python-code` replaces them), 016 (difficulty 4, plan REQUIRED).

### Verified context ###
1. **P1/P2 measured today on `84da7a0`** (`C:/4DApp/recheck/scratch/aud1a_probes_baseline.out`): the 9 acceptance
   probes → `9 failed in 7.20s`; `apps/ui/tests` → `2 failed, 6 passed` (both E2E, `ModuleNotFoundError`).
2. **`_build_fatal_incomplete_output` reads only `request.metadata`** from the request (`meta = request.metadata`;
   `meta.vin_confidence`), so a metadata-based `abort_incomplete` is feasible. Its `horizon` is a plan item.
3. **The T-AUD-4 residual line exists** in `repo/audit/FIX_PLAN.md` at `84da7a0` (grep `gas_lab_output.*optional`).
4. **`writing-4dapp-python-code` does not carry the 008 lab-boundary facts** (grep `aggregator|Forbidden` → none), so
   R0 states them with their sources.
5. **The editable install is git-ignored:** `git check-ignore -v labs/comlab/comlab.egg-info` → `.gitignore:4:*.egg-info/`.
6. **Anchors:** `wired-python/SKILL.md` line 52 `## Forbidden patterns (composition-only)`; composition
   `co2=float(gas_inputs["co2"])` (1 hit); pyproject `[tool.setuptools.packages.find]` and `[tool.setuptools.package-data]`.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | `9 failed in 7.20s` today (red before the row, as it must be) |
| step 2 | RAN | `2 failed, 6 passed in 1.90s` today |
| step 3 | RAN | C1 `43 failed, 1 passed`, C4 `12 failed`, C5 `19 failed in 141.48s` today = P3 (42, 10, 13) plus the 1, 2 and 6 acceptance probes |
| step 4 | DEFERRED | asserts `import ok`; fails today in the deployed layout (F-C1-5) |
| step 5 | DEFERRED | baseline identical to `baseline_20261017.txt` on this host (`C:/4DApp/baseline_20261102.txt`) |
| step 6 | DEFERRED | asserts 2 commits; 0 before the row |

### Exclusivity ###
None: T-AUD-1b is deferred behind this row and shares `labs/comlab/pyproject.toml`. No other row is open.

### Progress hook ###
T-AUD-1a: check 9 probes green, ui tests green, expected-red counts unchanged, two commits in R8 order.

### Cold read ###
own pass 2026-11-02: literals ok (8 anchors; `co2=float(gas_inputs["co2"])`, `## Forbidden patterns`, the def, both
pyproject tables, the FIX_PLAN residual: 1 each; `meta = request.metadata` and `gas_lab_output` 2 each, cited as sites,
not as unique) · counts: 9 probes in criterion 1 = 9 node ids in step 1; P3 re-measured today = 42/10/13 + 1/2/6 ·
traceability: criteria 1-6 → steps 1-6; every CREATE/MODIFY → a deliverable; RUNTIME writes (.venv, case_library.html)
tagged · section pairs: step 6 (only note + RESULT uncommitted) agrees with Deliverables 3-4 and R8 · closed sets:
"exactly 2 commits" = R8's two; "only `request.metadata`" = sidecar fact 2 · JUDGEMENT criteria: 0.
cold read 2026-11-02: skipped, plan-gated (the second plan review is Linux Cowork, 016).
