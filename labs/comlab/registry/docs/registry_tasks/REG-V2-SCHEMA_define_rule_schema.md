### Goal ###

Define the v2 rule schema as a Pydantic v2 model (`schema_v2.py`) plus a human-readable spec (`SCHEMA_V2_SPEC.md`). The schema replaces v1's hard-coded chemistry-gate architecture with an evidence-tier model where chemistry states, OBD PIDs, and DTCs each contribute weighted evidence rather than acting as mandatory prune keys. This is the only non-rule Python code in the registry workstream — it is the contract every REG-V2-AUTHOR-{family} task will write rules against.

### Success criteria ###

- `python -c "from registry.schema_v2 import Rule, EvidenceTier, ChemistryState, FaultFamily, DTCRoutingTag; print('imports ok')"` exits 0
- `python -c "import json, pathlib; from registry.schema_v2 import Rule; [Rule.model_validate_json(p.read_text()) for p in pathlib.Path('registry/rules').glob('*.json')]"` exits 0 for every rule file under `registry/rules/` (initially empty — passes vacuously after schema creation)
- `pyright registry/schema_v2.py` reports 0 errors
- `ruff check registry/schema_v2.py --fix` exits 0 with no remaining violations
- `python3.14 -m py_compile registry/schema_v2.py` exits 0
- `pytest registry/tests/ -x -q` passes (may be "no tests in scope" until a test file exists; record that)
- `SCHEMA_V2_SPEC.md` passes the document readability gate (no image placeholders, fully read, formulas present as text)

### Context ###

The v1 architecture (`COMLab/comlab/config/global_fault_registry.json`) gates every rule on a single hard-coded `gas_lab_state` — only 11 of 32 GASLab chemistry states appear across 53 rules. The two most common chemistry signatures in failing traces, `TIMING_RETARDED` (64 curated cases) and `SAMPLE_INVALID` (17 cases), have zero matching rules. This guarantees 100% prune for ~32% of the curated corpus before evaluation even begins (AUDIT-REG §1, CHEMISTRY_COVERAGE §1).

The v2 schema fixes this by decoupling evidence from gating:
- **Evidence tiers** (`definitive`, `suggestive`, `gating`) replace hard-coded chemistry-gate keys. A rule can accept multiple chemistry states, each at a different evidence weight.
- **Rule competition groups** replace v1's single-winner behavior. Multiple rules within a fault family can fire and compete by score; the router selects the highest-scoring rule.
- **Confidence ceilings** enforce the "no solo survivor" discipline: if only one rule in a competition group fires, its confidence is capped at a documented ceiling (default 0.70).
- **DTC evidence** replaces v1's `REQUIRE_MATCH` / `REQUIRE_DTC` prune strategy. DTC presence is evidence, not a gate — a rule can accumulate evidence from chemistry + PIDs even when expected DTCs are absent.

The output (`schema_v2.py`) is a Pydantic v2 model. It imports only stdlib + Pydantic. It is the single source of truth for vocabulary enums (ChemistryState, FaultFamily, EvidenceTier, DTCRoutingTag) that rule JSON files reference. The spec document (`SCHEMA_V2_SPEC.md`) is human-readable and serves as the authoring guide for the 13 REG-V2-AUTHOR tasks.

STRICT-ONLY: Load skills: (none — this task has no on-demand domain skills; the three mandatory skills cover it)

### Deliverables ###

1. `registry/SCHEMA_V2_SPEC.md` — Specification document describing: evidence-tier model, rule structure, competition groups, confidence ceilings, vocabulary enums, and a worked example rule. Authoring guide for the 13 REG-V2-AUTHOR tasks.
2. `registry/schema_v2.py` — Pydantic v2 model with: `EvidenceTier` (StrEnum), `ChemistryState` (StrEnum — 32 values mirroring GASLab `ChemicalSignature`), `FaultFamily` (StrEnum — 16 values), `DTCRoutingTag` (StrEnum — values from DTCLab vocabulary), `ChemistryEvidence`, `OBDEvidence`, `DTCEvidence`, `Rule` (top-level model), `RuleSet` (collection model with validation).
3. `registry/__init__.py` — Package init (may already exist; CREATE if missing).
4. `registry/tests/test_schema_v2.py` — Minimal test: imports resolve, a valid minimal rule validates, a rule missing `passes_cases` fails validation, enum membership is enforced.

### Files to touch ###

- `registry/SCHEMA_V2_SPEC.md` (CREATE)
- `registry/schema_v2.py` (CREATE)
- `registry/__init__.py` (CREATE if missing)
- `registry/tests/test_schema_v2.py` (CREATE)

### Out of scope ###

- No rule JSON files are authored — those belong to REG-V2-AUTHOR-{family} tasks.
- No integration with COMLab router — that belongs to REG-V2-INTEGRATE.
- No case-ID resolution tooling — that belongs to a later tooling task or the integration shim.
- No loader/validator CLI entry points — those are separate tooling tasks.
- No changes to any lab, COMLab, or 4DLabWired code.
- No imports from GASLab, DTCLab, or any lab — the ChemistryState and DTCRoutingTag enums are defined self-containedly within `schema_v2.py`, mirroring the source-of-truth enums without importing them.
- Do NOT author the `registry-rule-authoring` on-demand skill yet — that gates REG-V2-AUTHOR tasks and should be authored after this schema lands.

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Inner loop — schema_v2.py
python3.14 -m py_compile registry/schema_v2.py
ruff check registry/schema_v2.py --fix
pyright registry/schema_v2.py

# Inner loop — test file
python3.14 -m py_compile registry/tests/test_schema_v2.py
ruff check registry/tests/test_schema_v2.py --fix
pyright registry/tests/test_schema_v2.py

# Unit tests
pytest registry/tests/test_schema_v2.py -x -q

# Import check (all enums + model resolve)
python3.14 -c "from registry.schema_v2 import Rule, RuleSet, EvidenceTier, ChemistryState, FaultFamily, DTCRoutingTag; print('All imports OK'); print(f'Chemistry states: {len(ChemistryState)}'); print(f'Fault families: {len(FaultFamily)}'); print(f'Evidence tiers: {len(EvidenceTier)}')"

# Structural checks — spec doc exists and has required sections
python3.14 -c "import pathlib; spec = pathlib.Path('registry/SCHEMA_V2_SPEC.md').read_text(); assert 'Evidence Tier' in spec; assert 'Competition Group' in spec; assert 'Confidence Ceiling' in spec; assert 'Worked Example' in spec; print('Spec sections OK')"

# Document readability gate
python3.14 -c "import pathlib; spec = pathlib.Path('registry/SCHEMA_V2_SPEC.md').read_text(); assert '![][' not in spec, 'IMAGE PLACEHOLDER FOUND'; print('Doc gate: clean')"
```

All steps must pass.

### Progress hook ###

PROGRESS.md `REG-V2-SCHEMA`: Status=done, Files changed=4, Verification="schema_v2.py Pydantic model with 32 ChemistryState + 16 FaultFamily enums, evidence-tier model, spec doc with worked example"
