# T-OIL-R6 — Docs/wiki/dossier refresh to the shipped registry + proposals

### Goal ###

Reconcile the human-facing docs with what actually shipped: the five oil cases as
live registry rules (`MW-001/002/003/008/009`) plus the proposal-only KG
nodes/families/symptom rows. Update the semantic contract, the symptom/gas
vocabularies, and the `casesextra_new_cases.html` dossier cards so none of them
still imply the KG decides oil verdicts. Done when the docs match the registry and
the proposals registry, verified by a consistency check.

### Success criteria ###

- A reviewer diff shows: SEMANTIC_CONTRACT lists the oil tier_1/tier_2 vocabulary at
  the agreed count; the gas/symptom vocabularies name `MW-008`/`MW-009`; the dossier
  cards' "diagnostic logic" matches the rule gates shipped in R4/R5.
- `grep` check: no doc in the pack still states or implies oil verdicts come from the
  COMLab KG on the live path.
- All five `P_NEW_*` cards cross-reference their live `MW-00x` rule id.

### Context ###

Docs are the last reconcile step so they describe shipped reality, not intent.
Pinned targets: SEMANTIC_CONTRACT §4.2 (pair count), SYMPTOM_VOCABULARY, the gaslab
wiki oil cases, and `casesextra_new_cases.html` (the dossier card source in
`planning/OilburnCases.md` is the content of record). Reports stay in `.md`
(house rule) except the existing `.html` dossier card file, which is the platform's
own format and is edited in place.

STRICT-ONLY: Load skills: none.

### Consumer (signal/noise) ###

- N/A — documentation reconcile, no new schema field. Gate = docs match the shipped
  registry rules and proposals registry.

### Deliverables ###

1. SEMANTIC_CONTRACT doc — oil vocabulary + `MW-008/009` references.
2. SYMPTOM_VOCABULARY / gas vocabulary docs — same.
3. `casesextra_new_cases.html` (or its `.md` source) — five cards cross-referenced to
   `MW-00x`, diagnostic logic matched to shipped gates.

### Files to touch ###

- (coder pins exact doc paths via READ-NARROW) SEMANTIC_CONTRACT (MODIFY)
- SYMPTOM/gas vocabulary docs (MODIFY)
- dossier card file (MODIFY)

### Out of scope ###

No code, rule, schema, or proposals changes (R1–R5 own those). Do not invent new
cases or vocabulary. Do not convert any deliverable to `.docx`/`.pdf`. GRAPH
GUARDRAIL: no graphify.

### Verification ###

```bash
cd /sessions/<vm>/mnt/4DLab
# Consistency: every shipped oil rule id appears in the docs
for id in MW-001 MW-002 MW-003 MW-008 MW-009; do grep -rq "$id" <doc-paths> && echo "$id OK" || echo "$id MISSING"; done
# No doc claims KG decides oil verdicts on the live path
! grep -rin "KG .*decid\|knowledge graph.*verdict" <oil-doc-paths>
```

All steps must pass.

### Progress hook ###

PROGRESS.md `T-OIL-R6`: Status=done, Files changed={COUNT}, Verification="docs reconciled to shipped MW-001/002/003/008/009 + proposals; no live-KG-verdict claims remain"
