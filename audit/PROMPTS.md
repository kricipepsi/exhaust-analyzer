# Audit session prompts — round 1

Each block is the complete first message of one auditor session. A cloud session runs on
`kricipepsi/exhaust-analyzer` (claude.ai/code); a local session runs in the repo root. One target per
session. The order below is the architect's ranking (risk to a user-visible verdict first, cheap mechanical
passes early). Status and findings go in `audit/FINDINGS.md`, which only the architect edits.

---
### C1 — COMLab decision spine (highest risk)
```text
Read audit/AUDITOR.md and follow it exactly. Target: labs/comlab — the fusion/decision spine (package root labs/comlab/comlab/ unless stated):
comlab/core/fault_atlas_router.py (execute_triage_loop CC 174, route CC 70), labs/comlab/registry/integration_shim.py
(_score_rule CC 55), comlab/core/lab_pipeline_aggregator.py, comlab/schemas/. Claims: labs/comlab/wiki/, labs/comlab/docs/
(PRD, HLD, DLD, LLD, BDD, adr/), labs/comlab/docs/Vocabulary/SEMANTIC_CONTRACT.md. Attack: every verdict enum
(comlab/schemas/response.py DegradationLit, FaultFamilyLit, ConfidenceLit, HorizonLit) is reachable and routed;
abstain/margin logic at its boundaries; contradictory upstream verdicts (gas vs obd vs dtc vs symptom);
missing/partial inbound payloads (comlab/schemas/ingestion.py OrchestratorInboundRequest); era handling at the
1990/2010 edges; determinism (same input -> same output). Note: two comlab tests import apps/wired
(audit/reports/R0_baseline_20261017.md); run the suite with apps/wired installed.
```

### C4 — cross-lab contracts and the wired composition
```text
Read audit/AUDITOR.md and follow it exactly. Target: the boundaries between labs: apps/wired/wired/
composition.py (_run_obdlab CC 64), apps/wired/v7/ (load_corpus.row_to_raw_inputs CC 70, run_suite),
and each lab's output schema against the type COMLab expects (labs/comlab/comlab/schemas/ingestion.py).
Claims: labs/comlab/docs/CROSS_LAB_DEPENDENCIES.md, labs/comlab/docs/Vocabulary/*, each emitter lab's
docs/*_VOCABULARY.md, apps/wired/WIRING_PREP.md, AGENTS.md rule 5 and "emitter labs emit channels, not
verdicts". Attack: field-by-field schema drift between producer and consumer (names, enums, units,
optionality); values a producer can emit that the consumer rejects or silently drops; an emitter lab
that emits a verdict; end-to-end runs of single cases through the composition with edge inputs.
```

### C2 — GASLab resolution and rule engine
```text
Read audit/AUDITOR.md and follow it exactly. Target: labs/gaslab — gaslab/resolution.py
(apply_differentiators CC 133), gaslab/rule_engine.py (_definitive_match CC 50), gaslab/audits.py.
Claims: labs/gaslab/wiki/, labs/gaslab/docs/ (PRD/HLD/DLD/LLD/BDD/ADR, GAS_VOCABULARY.md),
gaslab/data/gas_lab_ontology.yaml. Attack: gas-reading boundaries (lambda, CO, HC, CO2, O2 at and
beyond the thresholds the wiki cites), physically impossible combinations, ties between rules,
rule-order dependence, every numeric threshold against its `# wiki: §` citation.
```

### D1 — wiki citations across all labs (mechanical)
```text
Read audit/AUDITOR.md and follow it exactly. Target: every `# wiki: §` citation in labs/ and apps/
(316 at R0; enumerate with `grep -rn "# wiki: §" --include=*.py labs apps`). For each: does the cited
wiki file and section exist, and does the section state the same value (number, unit, range) as the
literal on that code line? Also list numeric thresholds in labs/*/<pkg>/ that carry no citation
(AGENTS.md: "Numeric literals carry a wiki citation"). Write a script under audit/scratch/D1/ that
does the enumeration and resolution; report every mismatch as a finding and the script's totals.
```

### D3 — governance documents and ledgers (mechanical)
```text
Read audit/AUDITOR.md and follow it exactly. Target: the claims the repo makes about itself:
CLAUDE.md, AGENTS.md, 4DLab_CLAUDE.md, START_HERE.md, ROADMAP.md, DECISIONS.md, every
labs/*/tasks/PROGRESS.md and apps/*/**/*PROGRESS*.md, every *_START_HERE.md. Attack: paths that do not
resolve; environment claims that no longer hold (host, OS, interpreter, workspace root); rules that
contradict each other (e.g. AGENTS.md rule 5 vs labs/dnalab/docs/ADR_DNALab.md ADR-0002); ledger rows
marked `pending` whose spec file is missing or whose blockers are not `done`; `done` rows whose
deliverables are absent; task IDs used twice.
```

### C3 — OBDLab and DTCLab emitters
```text
Read audit/AUDITOR.md and follow it exactly. Target: labs/obdlab (core/sensor_signal_translator.py
translate CC 29, core/analytics_preconditions.py) and labs/dtclab (ranking.py rank_candidates CC 19,
core/routing_tag_mapper.py). Claims: each lab's wiki/, docs/ and *_VOCABULARY.md; AGENTS.md "emitter
labs emit channels, not verdicts". Attack: PID/unit conversions at range edges, missing or stale
sensor values, DTC codes outside the vocabulary, ranking ties and stability, channels that leak a
cross-lab verdict.
```

### C5 — public UI payload
```text
Read audit/AUDITOR.md and follow it exactly. Target: apps/ui/ui_payload.py (build_diagnose_payload
CC 115) and apps/ui/app.py (the published Streamlit app, root app.py shim, render.yaml). Claims: what
the UI tells a user must equal what COMLab decided. Attack: payload fields that misstate or drop the
verdict, confidence or horizon; inputs the form accepts that the labs reject; crash paths on empty
or partial inputs; anything that renders untrusted text unsafely.
```

### C6 — VINLab, DNALab, SymptomLab
```text
Read audit/AUDITOR.md and follow it exactly. Target: labs/vinlab (vinlab/ package; tools/ are offline
builders, lower priority), labs/dnalab, labs/symptomlab. Claims: each lab's wiki/ and docs/, including
labs/dnalab/docs/ADR_DNALab.md ADR-0002 (the one sanctioned cross-lab import). Attack: VIN decoding
for malformed, short, pre-1990/post-2010 and check-digit-invalid VINs; brand/engine resolution
ambiguity; DNA assembly with missing or contradictory VIN and symptom inputs; symptom validation edges.
```

### D2 — design chain per lab
```text
Read audit/AUDITOR.md and follow it exactly. Target: the document chain of one lab named by the
architect (default order: comlab, gaslab, obdlab, dtclab): PRD -> HLD -> DLD -> LLD -> BDD, its ADRs and
its *_VOCABULARY.md. Detection only. Attack: requirements with no design home; design statements the
code contradicts; BDD scenarios with no test; vocabulary terms or enum values that differ between the
vocabulary doc and the code's schema literals (diff them mechanically); figures that disagree between
documents. Every finding needs path:line plus the quoted text.
```
