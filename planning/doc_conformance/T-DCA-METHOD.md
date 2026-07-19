# T-DCA-METHOD — per-lab doc↔code conformance audit (repeatable procedure)
**Pack:** DOC-CONFORMANCE (`DOC_CONFORMANCE_PROGRESS.md`) · **Lane:** docs/audit · **Mode:** STRICT
**Run once per lab named in the pack ledger.** Read-only on **code AND docs**; writes one report.
**Sibling to** `apps/vault/audit/T-GTA-METHOD.md` — T-GTA audits the framed *graph edges*; this audits the
*content* of the design/contract docs (HLD/LLD, ADRs, Vocabulary) against code. Surfaced by the owner's
2026-06-29 doc-drift review (those doc classes were unaudited).
**Load skills:** `_skills/doc/ADR.md`, `_skills/graph/4dlab-vault/SKILL.md` (orientation only).

## Goal
For lab `<L>`, verify the **content** of its docs matches code, classifying every checked claim as
**MATCH / DRIFT / UNDOCUMENTED / SUPERSEDED / PENDING** (+ **DUP-DRIFT** for vocabulary). Write
`reports/<L>__<agent>.md`. **Do not edit docs or code** — this discovers; a reconcile pass fixes.

## What to audit (skip a class only if the lab lacks it)
1. **Vocabulary** — `labs/<L>/docs/*_VOCABULARY.md`, plus the duplicate copies at
   `labs/comlab/docs/Vocabulary/` and `labs/semantic/vocabul/`. The **test-anchored canonical** is the
   copy a `test_vocabulary*.py` parses (commonly `labs/semantic/vocabul/<X>_VOCABULARY.md`). For each enum
   member / coded value / threshold stated in the doc: confirm it exists in code
   (`labs/<L>/<L>/schemas/vocabulary.py` or `contracts.py`) AND that the three copies agree.
2. **ADR** — `labs/<L>/docs/adr/*` or `labs/<L>/docs/ADR_<L>.md`. For each ADR, confirm its decision still
   holds in code (e.g. "no cross-lab imports", "retire WRONG_VALVE_TIMING → 34 states", "YAML-driven
   routing tags"). An ADR the code now contradicts = **SUPERSEDED** (needs a superseding ADR, not a silent edit).
3. **HLD/LLD** — `labs/<L>/docs/HLD_<L>.md`, `LLD_<L>.md`. Prioritise the LLD "exact" sections (physical
   constants, thresholds, regex, formulas, error-code taxonomy, confidence weights): each stated literal
   must match the code literal. HLD: confirm module layout + COMLab integration points resolve to real files/symbols.

## Procedure
1. Enumerate claims: every vocab value/threshold, every ADR decision, every LLD "exact" literal.
2. Resolve each against code — verify, do not trust the doc: grep / query the lab graph
   (`labs/<L>/graph/v2_current/`, query-only) for the literal/enum/symbol; record `doc:line ↔ code:line`.
3. Classify with evidence. For vocabulary, also flag **DUP-DRIFT** when the three copies disagree and name
   which is the test-anchored canonical.
4. Write `reports/<L>__<agent>.md`: table `doc:line | claim | class | code evidence (file:line) | proposed fix`;
   counts + a one-line per-class verdict at the top.
5. **Self-check:** reproduce the seeded case(s) for `<L>` from the pack ledger. A mismatch means the method
   is wrong — STOP and re-check before reporting.

## Files to touch
- create: `planning/doc_conformance/reports/<L>__<agent>.md`
- (no edits to docs, code, graph, maps, or `Vault/`)

## Out of scope
Fixing anything (that is a reconcile pass / per-lab reconcile spec). Rewriting prose. Any Python. Any
`graphify` rebuild. `Vault/`. The framed-edge checks (those are T-GTA).

## Verification
1. Every doc class present in `<L>` is covered; every enumerated claim has a class + evidence; zero unclassified.
2. Every DRIFT / SUPERSEDED / DUP-DRIFT row cites the `doc:line` AND the `code:line` that proves it.
3. Seeded case(s) reproduced.
4. `git --no-pager diff --stat` shows only `planning/doc_conformance/reports/<L>__<agent>.md` added.

## Success criteria
`reports/<L>__<agent>.md` classifies every checked claim with code evidence; seeded cases match; nothing
outside `reports/` changed.

## Progress hook
Pack ledger row `T-DCA-<L>`: Status=done, Report=`reports/<L>__<agent>.md`,
Verification="N claims: a MATCH / b DRIFT / c SUPERSEDED / d DUP-DRIFT / e PENDING; seeded case OK".
