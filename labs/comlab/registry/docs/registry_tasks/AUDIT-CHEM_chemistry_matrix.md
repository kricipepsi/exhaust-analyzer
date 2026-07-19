### Goal ###

Produce `registry/CHEMISTRY_COVERAGE.md` — a chemistry-state × fault-family matrix built from the 252-case curated corpus. Each row is a GASLab chemistry state observed in `corpus_curated.csv`; each column is one of the 16 fault families (13 existing + 3 new: `vacuum_leak`, `overheating`, `charging_system`). Each cell counts how many curated cases carry that chemistry and are labelled with that family. The matrix exposes which chemistry/family intersections have zero coverage, which chemistries lack rules entirely, and which families have insufficient chemistry diversity. The output includes a prioritized authoring order for the REG-V2-AUTHOR-{family} tasks, ordered by case volume and coverage-gap severity. This is a read-only audit — no Python code, no JSON rules.

### Success criteria ###

- `registry/CHEMISTRY_COVERAGE.md` exists and passes the document readability gate (no image placeholders, full read confirmed, formula content present).
- The matrix covers every unique GASLab chemistry state observed in the curated corpus (rows) × all 16 fault families present in `corpus_meta.json` (columns).
- Every cell contains a case count derived from `corpus_curated.csv` joined against the chemistry state emitted per case (from Jaeger traces or GASLab vocabulary mapping).
- The document identifies: (a) families with zero rules for their observed chemistries, (b) chemistries with zero matching rules, (c) families with only one chemistry signature.
- A prioritized authoring order table appears, ranking the 16 REG-V2-AUTHOR-{family} tasks by: case volume in curated corpus, chemistry coverage gap severity, and whether the family is new (no v1 rules exist).
- `REGISTRY_AUDIT.md` §2.2 chemistry-states table is cross-referenced — every v1 chemistry state is mapped to the curated corpus families it currently addresses vs. families it should also address.

### Context ###

AUDIT-CHEM is session 3 of the registry rebuild workstream per `JAEGER_FIX_IMPLEMENTATION_PLAN_2026-05-27.md` §10.1. It builds on AUDIT-CORPUS (curated 252 cases) and AUDIT-REG (v1 rule inventory, 11 chemistry states, REBUILD decision). The v1 architecture gates every rule on a hard-coded `gas_lab_state` — 60% of cases prune because their chemistry matches zero rules. The v2 registry replaces hard-coded gates with evidence-tier weights, but the authoring still needs to know which chemistry signatures appear in the corpus and which families they should route to. This matrix is the authoring spec that every REG-V2-AUTHOR-{family} task will reference.

Load skills: (none — read-only audit, no Python code)

### Deliverables ###

1. `registry/CHEMISTRY_COVERAGE.md` — chemistry × fault-family matrix with case counts, gap analysis, and prioritized authoring order. Structured sections:
   - Executive summary (one paragraph)
   - Chemistry states observed in the curated corpus (table: state name, case count, families currently labelled)
   - Full matrix (rows = chemistry states, columns = 16 fault families, cells = case count)
   - Gap analysis: families with zero coverage per chemistry, chemistries with zero rules, single-signature families
   - Cross-reference against REGISTRY_AUDIT.md §2.2 v1 chemistry states
   - Prioritized REG-V2-AUTHOR-{family} task order with one-line justification per family

### Files to touch ###

- `registry/CHEMISTRY_COVERAGE.md` (CREATE)
- `registry/CORPUS_AUDIT.md` (READ — for family case counts)
- `registry/REGISTRY_AUDIT.md` (READ — for v1 chemistry states)
- `registry/corpus_curated.csv` (READ — for case-level data)
- `registry/corpus_meta.json` (READ — for per-case dispositions and families)
- `COMLab/comlab/config/global_fault_registry.json` (READ — for v1 chemistry-state gating per rule)
- `GASLab/gaslab/contracts.py` (READ — for GASLab chemistry-state vocabulary)
- `4DLabWired/_jaeger/runs/20260527-044325/DIAGNOSTIC_CAPABILITY_ANALYSIS.md` (READ — for per-phase chemistry distribution in failing traces)

### Out of scope ###

- Writing any Python code, JSON rule files, or schema definitions (those are REG-V2-SCHEMA and REG-V2-AUTHOR-* tasks).
- Modifying `corpus_curated.csv` or `corpus_meta.json` (corpus is frozen after AUDIT-CORPUS).
- Authoring individual v2 rules — the matrix tells authors which families and chemistries to target, not the rule content.
- Re-running the harness or Jaeger — this task consumes existing trace data, it does not produce new runs.
- Evaluating whether the curated corpus labels are correct (that was AUDIT-CORPUS scope).

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Structural checks
python -c "assert __import__('pathlib').Path('registry/CHEMISTRY_COVERAGE.md').exists(), 'MISSING: CHEMISTRY_COVERAGE.md'"
python -c "import json; meta=json.load(open('registry/corpus_meta.json')); print(f'{meta[\"curated_count\"]} cases, {len(set(c[\"expected_top_fault_family\"] for c in meta[\"cases\"] if c[\"disposition\"]==\"keep\"))} families')"

# Document readability gate (per 4DLab/CLAUDE.md)
python -c "import pathlib; content=pathlib.Path('registry/CHEMISTRY_COVERAGE.md').read_text(); assert '![][' not in content, 'FAIL: image placeholders found'"

# Cross-reference: every family in corpus_meta.json appears in CHEMISTRY_COVERAGE.md
python -c "
import json, pathlib
meta = json.load(open('registry/corpus_meta.json'))
families = sorted(set(c['expected_top_fault_family'] for c in meta['cases'] if c['disposition'] == 'keep'))
content = pathlib.Path('registry/CHEMISTRY_COVERAGE.md').read_text()
missing = [f for f in families if f'`{f}`' not in content]
assert not missing, f'Families missing from CHEMISTRY_COVERAGE.md: {missing}'
print(f'All {len(families)} families referenced in coverage matrix.')
"

# Cross-reference: every v1 chemistry state from REGISTRY_AUDIT.md §2.2 is accounted for
python -c "
import pathlib
content = pathlib.Path('registry/CHEMISTRY_COVERAGE.md').read_text()
states = ['LEAN_MIXTURE','LEAN_MISFIRE','RICH_MIXTURE','RICH_MISFIRE','IGNITION_MISFIRE',
          'INCOMPLETE_OXIDATION','INCOMPLETE_COMBUSTION','CATALYST_OVERWHELMED','CATALYST_NOT_LIGHTING_OFF',
          'NORMAL_OPERATION','EXHAUST_AIR_LEAK','POA_SIGNATURE','WORN_PISTON_RINGS','WORN_VALVE_SEALS',
          'WORN_ENGINE','WRONG_VALVE_TIMING','VVT_FAILURE','COOLANT_LEAK_INTERNAL','GDI_HPFP_INTERNAL_SEAL_LEAK']
missing = [s for s in states if s not in content]
if missing:
    print(f'WARNING: v1 states not referenced: {missing}')
else:
    print(f'All {len(states)} v1 chemistry states referenced.')
"
```

All steps must pass.

### Progress hook ###

PROGRESS.md `AUDIT-CHEM`: Status=done, Files changed=1, Verification="Chemistry × fault-family matrix complete; prioritized authoring order ready for REG-V2-SCHEMA."
