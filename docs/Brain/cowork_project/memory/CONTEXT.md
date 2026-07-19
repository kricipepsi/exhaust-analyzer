# agent_workspace — Project Context

Scope: paste into the Cowork **project** Context slot. Static orientation — the facts that
rarely change, so a fresh session knows *what it's looking at* before opening any ledger.
(Decisions and live state live in Memory; behavior rules live in Instructions.)

## What this is
**4DLabV2** — the v2 production rebuild of the **4D petrol diagnostic engine** (petrol only;
no diesel in v1). Workspace root is `/agent_workspace`. Layout is **flat and lab-isolated**:
each lab carries its own code, tests, tasks, wiki, and graph; the apps compose over them.

## The diagnostic pipeline (what the engine does)
Five layers, in order: **L1** idle gas → **L2** high-idle gas → **L3** DTCs → **L4** freeze
frame → **L5** live PIDs. Governing principle — **Truth-vs-Perception:** gas chemistry
(Brettschneider lambda) is ground truth; the ECU is perception. Where they diverge is signal.

## The labs (`labs/<lab>/`)
- **gaslab** — exhaust-gas chemistry emitter (Stage 1).
- **obdlab** — OBD trim / sensor signal emitter (Stage 2).
- **dtclab** — diagnostic trouble codes; the audit's #1 leverage point (Stage 3).
- **comlab** — the prune→rank→fuse spine; consumes every upstream channel (Stage 4, **last**).
- **dnalab / vinlab / symptomlab / semantic** — supporting channels (vehicle DNA, VIN decode,
  operator symptoms, semantics) that feed the COMLab prior; not a separate build stage.

Each emitter lab emits **channels, not verdicts** — cross-lab fault verdicts are COMLab
fusion, built last. **No cross-lab Python imports**; labs cross boundaries via JSON only.

## The apps (`apps/`)
- **wired** — composes the labs end-to-end into a single diagnostic case (→ COMLab).
- **vault** (vault-live) — frames the live tree for Obsidian transparency.
- **ui** — Streamlit front end (sample/reference stage).

## Roadmap sequence
**GASLab → OBDLab → DTCLab → COMLab (last)**, registry reconciled alongside COMLab.
*Why this order:* COMLab consumes every channel, so the emitters and research gates settle
first. Full plan: `ROADMAP.md`.

## Where truth lives (read these to orient)
- `START_HERE.md` → `ROADMAP.md` — boot sequence.
- `AGENTS.md` — the five rules (signal/noise, query-graph-before-grep, task-is-a-file,
  lab isolation, archive-not-delete).
- `CLAUDE.md` — architect entry point; session bootstrap table.
- `4DLab_CLAUDE.md` — infra (Python env, inner loop, git ritual) + load-bearing principles.
- `DECISIONS.md` — ratified architecture/business decisions.
- Per-lab: `labs/<lab>/wiki/` is domain truth; `labs/<lab>/tasks/PROGRESS.md` is the ledger
  (first `pending` row = next runnable task); `labs/<lab>/graph/` is the queryable code index.
- A repo is an **Obsidian vault** — navigate by `[[WikiLinks]]` and leave backlinks.

## Environment essentials
- **Linux Mint** host, case-sensitive filesystem (`AGENTS.md`, exact case).
- **Python 3.14.6** (uv-managed) at `/home/m/.local/bin/python3.14` — always invoke
  `python3.14` explicitly. Shared venv (isolated Python): `/agent_workspace/.venv-wired`
  (already built; never commit it).
- Machine-specific absolute paths live in `CLAUDE.local.md` (git-ignored).
- `Vault/` is an archived mirror — never edit it; edit the live `labs/<lab>/` source.
- Frozen graphs (pre-built code indexes) are **query-only** — never re-`graphify` them.
