# HANDOFF — REG-V2-AUTHOR-ignition_fault (fresh coder session)

**Prepared:** 2026-06-21 by architect (Cowork). **Paste this whole file to start the new coder.**
Spec of record: `labs/comlab/tasks/REG-V2-AUTHOR-ignition_fault.md` — read it in full; this handoff
only adds *current state*, *the environment fix*, and *pre-flight cleanup* the two prior sessions got wrong.

---

## 0. Current state — start from zero, but a dirty tree

- The task has **zero deliverables done.** No `registry/rules/ignition_fault.json`, no
  `registry/tests/test_ignition_fault_rules.py`, no `ignition_fault.json` line in `integration_shim.py`.
  No commit exists for this task on `master`.
- A previous coder (gpt-oss) went **off-task**: its only commit `5efbb52` adds `ObdEmissionsView` to
  OBDLab — unrelated to this task. **Do not build on it; do not let it confuse you.** (Separately, that
  commit is shallow: `ObdLabDnaView` has no `emissions` field, so `apps/wired/composition.py`'s
  `emissions=obd_emissions` kwarg is silently dropped by pydantic. Not your task — flagged for the owner.)

## 1. PRE-FLIGHT — do these BEFORE writing code (the two prior sessions died here)

1. **Close every other agent/editor session on this repo.** A stale `.git/index.lock` was left holding
   the repo; until it clears, `git add`/`commit` fail. Confirm `C:\Workspace\.git\index.lock` is gone.
2. **Delete two stray probe files** left by the audit (untracked junk):
   `labs/comlab/registry/.sandbox_write_probe` and `probe_err.txt` (repo root).
3. **Repair the working tree** if dirty: `git status` should be clean for
   `labs/obdlab/obdlab/schemas/__init__.py` (it was seen truncated). If modified unintentionally,
   `git checkout -- labs/obdlab/obdlab/schemas/__init__.py`.

## 2. ENVIRONMENT — the wall both prior coders hit. Read this twice.

The toolchain is **Python 3.14.x + pydantic 2.13.4 + pytest 9.1.x + ruff + pyright**. The failure mode is
trying to get there on **native Windows**, where no prebuilt `pydantic-core` wheel exists yet for cp314,
so pip falls back to a Rust source build and dies.

- **DO NOT** "fix" this by writing a pydantic stub / faking `field_validator`. The task is graded on the
  RuleSet **validating against `schema_v2.RuleSet`** — a stub gives a false green. Forbidden.
- **DO NOT** downgrade/change the pydantic pin. It is `2.13.4`.
- **DO** run where the canonical interpreter works:
  - **Cowork / WSL / Linux:** `PY="$REPO/.sandbox-py/bin/python3.14"` runs pydantic 2.13.4 natively. ✅
    (Verified working 2026-06-21: py 3.14.5, pydantic 2.13.4, pytest 9.1.0, ruff 0.15.18, `registry` imports.)
  - **Native PowerShell only:** build a Windows-native 3.14 venv per
    `labs/comlab/tasks/COMLAB_PYTHON_ENV_SETUP.md` §B (install CPython 3.14 + Rust toolchain, or use a
    cp314 wheel once published). Do not fall back to DTCLab's venv.

**Gate commands (Linux/WSL/Cowork):**
```bash
REPO=/path/to/C/Workspace        # e.g. the mounted Workspace root
PY="$REPO/.sandbox-py/bin/python3.14"
cd "$REPO/labs/comlab"
"$PY" -m pip install -e .                         # editable install so imports resolve
"$PY" -m ruff check .
"$PY" -m pyright --pythonpath "$PY" registry/
"$PY" -m pytest registry/tests/ tests/ -q
```

## 3. Deliverables (mirror the existing pattern — paths verified to exist)

1. **CREATE `registry/rules/ignition_fault.json`** — RuleSet, **≥3 competing rules**,
   `competition_group: "ignition_fault"`. Mirror `registry/rules/misfire.json` field-for-field.
   Rule sketch (see spec §Deliverables for full detail):
   - IF-001 coil-driver: `IGNITION_MISFIRE` DEFINITIVE + coil DTC P0351–P0358 SUGGESTIVE + positive STFT → `ERR-IF-001` (must reproduce the e2e).
   - IF-002 weak spark / secondary breakdown: `IGNITION_MISFIRE` DEFINITIVE + high-HC, no coil DTC → `ERR-IF-002`/`-005`.
   - IF-003 CKP intermittent: CKP DTC P0335–P0340 SUGGESTIVE + intermittent → `ERR-IF-006`; coordinate with `non_starter` so both don't fire.
2. **EDIT `registry/integration_shim.py`** — add `"ignition_fault.json"` to `_EXPECTED_RULE_FILES`
   (the frozenset at line ~106; currently 15 entries, no ignition_fault).
3. **CREATE `registry/tests/test_ignition_fault_rules.py`** — mirror
   `registry/tests/test_lean_condition_rules.py`. Validate against `registry/schema_v2.py::RuleSet`,
   assert `IGNITION_MISFIRE` DEFINITIVE present, coil-DTC evidence present, case-ID resolution.

## 4. Domain decision — do NOT invent numbers

Numeric evidence thresholds (HC ppm, O₂ %, trim %, DTC ranges) are an **owner sign-off** item. House
rule: every numeric literal carries a `# wiki:` / `wiki_ref` citation. Source the values from, and cite:
- `comlab/.../vocabulary.py:234` and `lld §3.1` (spark-generation failure, pre-combustion — per spec one-liner),
- the family catalogue `labs/comlab/comlab/config/kg/ignition_fault.json` (codes ERR-IF-001..007),
- existing thresholds in `misfire.json` for the IGNITION_MISFIRE/DTC gating shape.
Propose concrete values **with citations** in your scope-confirm and get owner sign-off before finalizing.

## 5. Success criteria (done = ALL)

- `ignition_fault.json` parses, validates against `schema_v2.RuleSet`, ≥3 unique `rule_id`s.
- `"ignition_fault.json"` in `_EXPECTED_RULE_FILES`; the REVIVE-1 manifest==glob assertion still passes.
- **The 3 curated cases flip to `ignition_fault`** on the v2 path — `EXP-N026`, `CASE-035`, `case_036`
  (today → `rich_mixture`/`no_fault`). They live in `registry/corpus_curated.csv`. **This is the named consumer.**
- e2e `tests/e2e/test_diagnostic_engine.py::test_e2e_ignition_fault_coil_driver` (ERR-IF-001) still passes;
  `misfire` cases unaffected (no cannibalisation).
- ruff clean · pyright clean · `pytest registry/tests/ tests/ -q` → 0 failed.
- Fill `VERIFICATION GATE` + `CODE REVIEW` in `labs/comlab/tasks/progress_notes/REG-V2-AUTHOR-ignition_fault.md`;
  flip the ledger row in `labs/comlab/tasks/PROGRESS.md` → `done`. Then STOP.

## 6. Reference files (all verified present)

| Purpose | Path |
|---|---|
| Spec of record | `labs/comlab/tasks/REG-V2-AUTHOR-ignition_fault.md` |
| Mirror template (rules) | `registry/rules/misfire.json` |
| Mirror template (test) | `registry/tests/test_lean_condition_rules.py` |
| Schema | `registry/schema_v2.py` (`class RuleSet`) |
| Shim / manifest | `registry/integration_shim.py` (`_EXPECTED_RULE_FILES` ~L106) |
| Validation cases | `registry/corpus_curated.csv` |
| e2e | `tests/e2e/test_diagnostic_engine.py` |
| KG family catalogue | `labs/comlab/comlab/config/kg/ignition_fault.json` |
| Env setup | `labs/comlab/tasks/COMLAB_PYTHON_ENV_SETUP.md` |

## 7. Scope confirm to post before coding (per CLAUDE.md boot step 5)

One paragraph: field · guard · signal/noise consumer (the 3 cases) · files touched · proposed thresholds
with wiki refs. Unclear consumer/threshold → ask one question first, don't guess.
