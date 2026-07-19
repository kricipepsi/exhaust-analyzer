# T-VLIVE-7 — Cross-lab verify + provenance (the pack gate)

**Pack:** VAULT-LIVE · **Lane:** vault-tooling / architect-authoring · **Mode:** STRICT
**Blocked by:** T-VLIVE-2, T-VLIVE-3, T-VLIVE-4, T-VLIVE-5, T-VLIVE-6
**Load skills:** `_skills/graph/4dlab-vault/reference/bases-and-views.md`.

## Goal
Confirm the whole live-tree transparency surface stands on its own — all six
framed labs (obdlab, gaslab, dtclab, dnalab, vinlab, symptomlab) appear in the
three `.base` views with **zero `MISSING` consumers** — write a live provenance
record, and hand the `Vault/` mirror archive to the architect.

## Context
Each per-lab task verified its own lab. This task is the **cross-lab gate**: it
checks the union, catches any lab that slipped, and records what was framed so the
architect can safely archive `Vault/` (Phase 4 of the harness plan). No new
framing here — verify + record only. If a lab is short, hand it back (don't fix it
here).

## Deliverables
1. `_bases/PROVENANCE.md` — one row per framed lab: framed-note count (docs +
   wiki), the live source folders, and the date. Mirrors the old
   `Vault/_meta/PROVENANCE.md` shape but points at **live** paths.
2. A one-paragraph **archive-readiness verdict** in the progress note: are the
   live bases authoritative without `Vault/`? (Yes → the architect runs the
   `Vault/`→`ARCHIVE/` move; No → list the gaps.)

## Files to touch
- create: `_bases/PROVENANCE.md`
- create: `apps/vault/vault_live_tasks/progress_notes/T-VLIVE-7.md`
- edit: `apps/vault/VAULT_LIVE_PROGRESS.md`

## Out of scope
- Framing any note (that's T-VLIVE-1…6); editing `.base` bodies, lab Python, or graphs.
- **Archiving `Vault/`** — that is the architect's move (coders are blocked from
  editing `Vault/`); this task only certifies it is safe.

## Verification
1. **Union audit:** across all six labs, `consumers.base` shows **zero `MISSING`**
   rows for live notes; every framed note resolves its named consumer.
   (Enumerate framed notes mechanically: grep `^node_type:` across
   `labs/*/docs` + `labs/*/wiki` + obdlab `research/chunks`; cross-check counts.)
2. `modules.base` groups all six labs; `drift-guards.base` shows each lab's
   `implements`→guards with no unexplained `NONE`.
3. `_bases/PROVENANCE.md` lists all six labs with non-zero framed counts.
4. No graph changed across any lab: `git status --porcelain -- labs/*/graph/` clean.
5. With `Vault/` excluded in `.obsidian/app.json` (from T-VLIVE-1), the views draw
   from live only — confirm no `Vault/...` paths appear in any view's rows.

## Success criteria
All six labs render in the three views on the live tree with zero `MISSING`
consumers, `_bases/PROVENANCE.md` records them, and the progress note states a
clear archive-readiness verdict for the architect.
