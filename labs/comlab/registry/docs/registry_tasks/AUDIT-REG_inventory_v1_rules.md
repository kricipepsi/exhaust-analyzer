### Goal ###

Inventory every v1 fault-atlas rule (53 rules across 12 family JSON files under
`COMLab/comlab/config/kg/` plus the `global_fault_registry.json` orchestrator
entries) against the curated corpus (`registry/corpus_curated.csv`, 252 cases).
For each rule, determine which curated cases it fires on in the v1 harness and
which it should fire on per ground truth. Produce `registry/REGISTRY_AUDIT.md`
with the full rule inventory, a rule-case firing matrix, and a binary decision:
**patch v1** or **rebuild v2** — based on the evidence, not on prior assumptions.

### Success criteria ###

- `registry/REGISTRY_AUDIT.md` exists and its bottom-line recommendation table
  is populated (no TBDs).
- The rule inventory table lists every v1 rule ID, its fault family, its
  prune_conditions (gas state, OBD fields, DTC tags), and the curated case IDs
  it fires on.
- The firing matrix shows, for each of the 13 existing fault families, how many
  curated cases the family's rules correctly route to the right family vs
  misroute vs fail to fire at all.
- The patch vs rebuild decision cites specific evidence (e.g., "X of 53 rules
  have prune_conditions that can never match the curated corpus chemistry
  signatures" or "Y rules fire correctly but Z fire on the wrong family").
- No Python code is written in this task (read-only audit). No `schema_v2.py`,
  no `rules/*.json` are produced.
- `tests/` stays empty — verification is structural (file exists, sections
  complete, cross-references resolve).

### Context ###

AUDIT-CORPUS curated the 281-case master CSV down to 252 cases (241 kept + 11
new placeholders). The Jaeger analysis (`DIAGNOSTIC_CAPABILITY_ANALYSIS.md`)
showed 60% of MISMATCH cases have all 53 rules pruned before evaluation —
prune_conditions are the primary bottleneck. This task inspects those
prune_conditions rule by rule against the curated corpus chemistry signatures,
OBD fields, and DTC routing tags to determine whether the v1 rule set is
patchable (individual prune-condition fixes + a few new rules) or must be
rebuilt from the ground up (v2 schema, new evidence-tier model, all rules
re-authored). The decision gates the entire REG-V2-* phase.

Source: `JAEGER_FIX_IMPLEMENTATION_PLAN_2026-05-27.md` §10, session 2.
Builds on: AUDIT-CORPUS (`CORPUS_AUDIT.md`, `corpus_curated.csv`,
`corpus_meta.json`).

STRICT-ONLY: Load skills: (none — audit-only task, no code written)

### Deliverables ###

1. `registry/REGISTRY_AUDIT.md` — full rule inventory + firing matrix + patch vs
   rebuild decision with cited evidence.
2. `registry/REGISTRY_PROGRESS.md` — row update only (status, date, commit,
   verification summary, notes).

### Files to touch ###

- `registry/REGISTRY_AUDIT.md` (CREATE)
- `registry/REGISTRY_PROGRESS.md` (MODIFY — task row update)

### Out of scope ###

- No code is written. No `schema_v2.py`, no `rules/*.json`, no Python tooling.
- No rule authoring or editing. Rules are read from `COMLab/comlab/config/kg/`
  and `COMLab/comlab/config/global_fault_registry.json` but not modified.
- No harness re-run. Harness results are read from the existing Jaeger run
  artefacts but the harness is not executed.
- No corpus changes. `corpus_curated.csv` is read but not modified.
- No chemistry matrix. That is AUDIT-CHEM, the next session.
- No scoring-path analysis. Only rule prune_conditions and routing behaviour
  are in scope; confidence scoring, trim gates, and solo-survivor penalties
  are for later tasks.

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab

# Structural checks
python -c "import pathlib; p=pathlib.Path('registry/REGISTRY_AUDIT.md'); assert p.exists(), 'MISSING'; print(f'OK: {len(p.read_text())} chars')"

# Section completeness — every required section present
python -c "
import re
text = open('registry/REGISTRY_AUDIT.md').read()
required = ['Executive Summary', 'Rule Inventory', 'Firing Matrix', 'Patch vs Rebuild Decision']
for section in required:
    assert re.search(rf'##\s+\d+\.\s+{re.escape(section)}', text), f'MISSING SECTION: {section}'
print('OK: all required sections present')
"

# Rule count — must inventory every v1 rule (≥50)
python -c "
import re
text = open('registry/REGISTRY_AUDIT.md').read()
rule_ids = re.findall(r'ERR-\w+-\d+', text)
print(f'Rule IDs inventoried: {len(rule_ids)} (expect ≥50)')
"

# No TBD placeholders
python -c "
text = open('registry/REGISTRY_AUDIT.md').read()
tbds = [line.strip() for line in text.split('\n') if 'TBD' in line.upper()]
assert len(tbds) == 0, f'TBD placeholders found: {tbds}'
print('OK: no TBD placeholders')
"

# corpus_curated.csv cross-reference — every case ID in REGISTRY_AUDIT.md resolves
python -c "
import csv, re
with open('registry/corpus_curated.csv') as f:
    curated_ids = {row['case_id'] for row in csv.DictReader(f)}
text = open('registry/REGISTRY_AUDIT.md').read()
cited = set(re.findall(r'case_\d+|CASE-\d+|CSV-\d+|ECU-\d+|EXP-N\d+|EXT-\d+|MECH-\d+|PDF-[A-Z0-9]+-\d+|REAL-\d+|RULE-[A-Z]+-\d+|TC-\d+|YAML-[A-Z0-9_]+', text))
orphan = [c for c in cited if c in curated_ids is False and c in curated_ids]  # inverted
# Actually check which cited IDs are NOT in curated:
orphan = [c for c in cited if c not in curated_ids]
print(f'Case IDs cited: {len(cited)}, orphan refs: {len(orphan)}')
if orphan:
    print(f'ORPHAN: {orphan[:10]}')
"
```

All steps must pass.

### Progress hook ###

PROGRESS.md `AUDIT-REG`: Status=done, Files changed=1, Verification="Rule inventory + firing matrix complete; patch vs rebuild decision rendered."
