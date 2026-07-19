# agent_workspace — Project Memory

Scope: paste into the Cowork **project** Memory (context-memory) slot. Memory is *what
has happened* and *what was decided* — distinct from Instructions (*how* to work) and
Context (*static* orientation). This seeds the project so a fresh session re-enters the
loop without re-deriving the state.

## How to keep this memory (protocol)
Borrowed from the "anchored artifacts" idea — preserve structure, but anchor each entry
to its source so nothing is lossy:
- Record **Decisions, Facts, and Open loops** — not narrative. One line each.
- **Every decision carries its *why*** and a pointer to the canonical file (`DECISIONS.md`,
  a ledger row, a task note). The pointer is the anchor; the canonical file stays truth.
- **Distill, don't dump.** "T-GV2-14 voided from GASLab — gas can't see per-bank signal"
  beats pasting the whole thread. But keep the qualifier that carries the nuance.
- **Convert relative dates to absolute.** "last week" rots; `2026-06-28` doesn't.
- Update incrementally as tasks close; supersede stale rows, don't silently rewrite history.

## Decisions (ratified — source: `DECISIONS.md`)
- **v1 is sunset; fork-and-freeze is permanent** — each v1 lab is copied into
  `labs/<lab>` and the v1 original archived once the v2 lab is built and green.
  *Why:* v2 reworks the non-working v1 engine; it does not preserve it.
- **Bank-asymmetry (`T-GV2-14`) voided from GASLab, re-homed to OBDLab.** *Why:* a single
  tailpipe sample mixes both banks — gas chemistry physically can't emit a per-bank signal;
  per-bank trim (STFT/LTFT) can, with COMLab fusion as the consumer.
- **`apps/wired` uses type-mirror isolation (D-V2-9).** *Why:* labs stay decoupled — wired
  mirrors the lab *types* it needs and crosses boundaries via JSON, importing lab entry
  points only, never lab type modules. Full zero-import IPC is out of scope (no need, high cost).
- **All `*Simple/` lab variants archived (D-V2-10).** *Why:* dead experiments; only `wired`
  imported them, and that import was cut on copy.

## Facts (current state — source: `ROADMAP.md`, ledgers, `.agent/assignments.md`)
- **Stages 1–3 done:** GASLab, OBDLab, DTCLab complete. **COMLab is Stage 4 and runs LAST**,
  registry reconciled alongside it. *Why last:* it's the rank/prune spine that consumes every
  upstream channel — reworking it earlier tunes against a moving target.
- **The engine is ranking-bound at ~51.2%, not coverage-bound.** *Why it matters:* gains come
  from new *evidence channels* (DTC presence, OBD trim, baselines, symptom labels), not more
  rules or weight-tuning — weight nudging hits a ~45% reshuffle ceiling.
- **Graph tooling is up (`T-COM-GRAPH-AST` done 2026-06-28).** pkg `graphifyy 0.8.36` installed in
  `.venv-wired`; COMLab `graph/{v2_code,v2_tests}` built and healthy; `v1_baseline` untouched.
- **No git yet** — the owner is bringing the real `.git` later. Until then the only rollback is
  the Desktop backup `/home/m/Desktop/migration`. Never run `git init`.

## Open loops (as of 2026-06-29 — source: `.agent/assignments.md`)
- **Active coder assignment:** Codex → `T-VLIVE-3c` (dtclab map drift fix — `power_loss`
  orphan ×8 + perception mislabel). Spec: `apps/vault/audit/T-VLIVE-3c_...md`.
- **Read-only Graph-Trust audit:** `T-GTA-<lab>` runs on Codex + Agy + Claude in parallel
  (redundancy is intentional — discovery only, no map edits).
- **Next COMLab coder task:** `T-COM-PATHS-1`.
- **Wired app:** `T-WIRE-1` blocked until gaslab `T-GV2-2` is `done`. Vault-live pilot
  `T-VLIVE-1` runnable.
- **Windows residue:** ~85 files still carry PowerShell/`C:\` command examples; boot canon is
  Linux-correct, embedded examples fixed per-file as labs are picked up.
