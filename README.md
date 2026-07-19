# 4DLabV2 — 4D petrol diagnostic engine (v2 production)

Flat, lab-isolated rebuild of the engine. Five labs under `labs/`, the apps that compose over them
under `apps/`, the generative test harness at `harness/`. Start at `START_HERE.md`; rules in
`AGENTS.md`; full rationale in `../v2-restructure/V2_WORKSPACE_STRUCTURE_PROPOSAL.md`.

Layout: `labs/<lab>/{<pkg>,tests,tasks,wiki,graph}` · `apps/{ui,wired}` · `harness/` · `docs/` ·
brain docs at root. Infra inherited from root `4DLab/CLAUDE.md`. Migration is phase-by-phase and
**archive-not-delete** — see `../v2-restructure/EXECUTION_LOG.md`.
