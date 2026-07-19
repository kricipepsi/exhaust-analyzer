### Goal ###
**LLM `extract` rollout — remaining docs tiers.** Repeat the T-GR-10 pilot procedure, one lab per
session, for the labs whose offline docs graphs are contains-only:
- `labs/dtclab/graph/v2_docs_llm/`
- `labs/vinlab/graph/v2_docs_llm/`
- `labs/dnalab/graph/v2_docs_llm/`
- `labs/comlab/graph/v2_docs_llm/` (comlab MAIN — NOT `labs/comlab/registry/`)
- `labs/comlab/registry/graph/v2_docs_llm/` — ONLY if the owner names it when unblocking this task
  (992-edge all-contains tier; same limitation, separate corpus).
Apply the **promotion decision the owner made on the T-GR-10 report** uniformly; if the pilot
changed the procedure (mode, backend, report format), inherit the amended version.
### Runner / backend ###
Nemo lane. `--backend deepseek` explicit, default mode, never `--deep`. Key from env only — never in
files. One lab per session, ledger order above.
### Success criteria (per lab) ###
1. Build per `4dlab-graphify-run` into that lab's `v2_docs_llm/` (scoped `/tmp` input, never repo
   root); no root `graphify-out/` survives.
2. Health: 0 dangling; EXTRACTED-dominant confidence split reported; predicate counts
   (`SUPERSEDES`/`CONSUMES`/`VERIFIES`/`MIRRORS_CONTRACT_IN`, lowercase accepted) reported —
   zeros stated honestly, not padded.
3. 3 predicate spot-checks resolve to correct chunk file+line via `graphify explain`.
4. Diff report vs that lab's canonical `v2_docs/` (CONFIRMED/GAP/NOISE per skill §5) appended to
   `REPORT_T-GR-11_llm_extract_rollout.md`; token/cost per lab recorded.
5. If the T-GR-10 decision was (A) adopt-as-tier: append a dated `v2_docs_llm` row per lab to
   `GRAPH_AUDIT_2026-06-28.md` and update the pack ledger's "predicate layer deferred" wording to
   point at the new tier. If (B) supplementary: audit row only, ledger wording unchanged.
6. No collateral: canonical `v2_docs/` and all other graphs byte-identical per lab.
### Out of scope ###
Never overwrite any canonical `v2_docs/`; never patch `graph.json`; never rebuild frozen graphs;
never `graphify-out/` at root; never `Vault/` writes; no key in files. gaslab is done in T-GR-10 —
do not re-run it.
### Verification ###
Run the T-GR-10 verification block with the lab path substituted, per lab, in the progress note.
### Progress hook ###
Ledger T-GR-11 → done when all named labs are built + reported; dual-gate note per session in
`../progress_notes/T-GR-11_<lab>.md`.
### Depends on ###
T-GR-10 done · **owner sign-off on the T-GR-10 report + explicit promotion decision (A/B/C)** ·
`DEEPSEEK_API_KEY` in env. Decision (C) = this task is waived, record it so.
