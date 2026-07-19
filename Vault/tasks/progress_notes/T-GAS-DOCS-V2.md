# T-GAS-DOCS-V2 — progress note

**Status:** `done` · **Pack:** VAULT (GASLab) · authored 2026-06-10 (architect)
Task spec: `Vault/tasks/T-GAS-DOCS-V2_*.md` · Pack ledger: `Vault/tasks/GAS_VAULT_TASKS_START_HERE.md`

## Plan
Scope: reconcile the six GASLab design docs under `labs/gaslab/docs/` to the live v2.1 AST surface, without lab code edits and without graphify. The docs corpus is consumed later by T-GAS-DOCPREP/T-GAS-GRAPH-LLM and ultimately by the vault build's frontmatter derivation plus Bases views, so only fields/values with named code readers stay current. The parity walk covers `contracts.py` (`ChemicalSignature`, `GasReading`, `GasLabPayload`), `dna_view.py` (`GasLabDnaView` 13-field slice), `process.py` (`GasLabContext` and payload pass-through), `rule_engine.py` (`target_lambda_v112`, cam timing, `reading_high`, `fuel_trim`), and `resolution.py` (`confidence`-gated `co_high_idle`, RPM-differential families). Owner direction: ADR/BDD are new docs and intentionally remain `Version: 1.0`; their `Code baseline: GASLab v2.1` and v2.1 content are the reconciliation signal.

## VERIFICATION GATE
- Header/parity check: HLD/DLD/LLD/PRD are `Version: 2.1` / PRD baseline v2.1; ADR/BDD intentionally remain `Version: 1.0` per owner direction because they are new docs, but both declare `Code baseline: GASLab v2.1 (34-value surface, dual-RPM input)`.
- Stale-value check: `WRONG_VALVE_TIMING` appears only in retired/superseded/taxonomy-change contexts, not as a live current enum value.
- AST parity spot-check: `DLD_GASLab.md` matches live `dna_view.py` / `rule_engine.py` for `target_lambda_v112`, `co_high_idle`, `confidence`, and the three `CAM_TIMING_*` branches.
- Scope check: no `gaslab/` code edits, no graphify, no graph artefact updates.

## CODE REVIEW
- Drift found/fixed: no content drift requiring design-doc edits after applying owner correction; the only attempted metadata bump was reverted because ADR/BDD version `1.0` is intentional.
- Confirmed v2.1 behaviours are already represented: 34-value `ChemicalSignature`, retired `WRONG_VALVE_TIMING`, dual-RPM `reading_high`, `fuel_trim`, `lambda_measured`, single `target_lambda_v112`, and `confidence`-gated `co_high_idle`.
- DOCPREP exclusions to carry forward: generic skill stubs, duplicate `GAS_VOCABULARY.md`, and `docs/audits/` should stay out of the six-design-doc ingest set.

> Flip the ledger row to `done` only when BOTH blocks above are clean (and any contracted consumer is
> grep-confirmed read in a live path).
