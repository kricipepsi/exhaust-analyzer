# T-GTA-METHOD — per-lab map↔code trust audit (repeatable procedure)
**Pack:** GRAPH-TRUST (`GRAPH_TRUST_AUDIT.md`) · **Lane:** vault-tooling · **Mode:** STRICT
**Run once per lab** named in the pack ledger. Read-only on code; writes one report.
**Cross-check mode:** this audit is **read-only** — the same lab is deliberately run on
multiple coders (Codex/Agy/Claude). Write to `reports/<L>__<agent>.md` (your agent id:
`codex`/`agy`/`claude`) so the runs never collide; the union step merges them.
**Load skills:** `_skills/graph/4dlab-vault/SKILL.md`, `_skills/graph/4dlab-doc-prep/SKILL.md`.

## Goal
For lab `<L>`, classify **every** framed edge in `vault-map.<L>.yaml` (and the
matching live-note frontmatter) as LIVE / MISLABEL / ORPHAN / PENDING per the
taxonomy in `GRAPH_TRUST_AUDIT.md`, and write `reports/<L>__<agent>.md`. **Do not edit the
maps or notes** — this task discovers; the reconcile pass fixes.

## Procedure
1. Enumerate edges: for each framed note in `vault-map.<L>.yaml`, list every
   `consumers:` , `drift_guards:` , and `implements:` entry. (Cross-check the live
   note frontmatter matches the map.)
2. Resolve each entry against code — **verify, do not trust the label**:
   - `implements` / `drift_guards`: `test -f` the path exists.
   - `consumers` naming `file.py SYMBOL/field`: open the file and confirm the symbol
     **and** that it reads the named field/type. A reader of a *different* field than
     the edge claims = **MISLABEL**, not LIVE.
   - No reader of the field/type anywhere in the consuming module = **ORPHAN**.
   - `(pending T-…)` edges = **PENDING** (confirm the task id exists in a ledger).
   - Reader exists but is only called by tests (not yet by a pipeline) = **LIVE**
     (expected pre-wire; record the "unwired" note but classify LIVE).
   Record the exact `grep`/`file:line` evidence per edge.
3. Write `reports/<L>__<agent>.md`: a table `note | edge | class | evidence (file:line) |
   proposed fix`. Summarize counts (LIVE/MISLABEL/ORPHAN/PENDING) at the top.
4. **Self-check:** if `<L>` has a seeded case in the pack, confirm your classification
   matches it. A mismatch means your method is wrong — STOP and re-check before
   reporting.

## Files to touch
- create: `apps/vault/audit/reports/<L>__<agent>.md`
- (no edits to maps, notes, code, or graph)

## Out of scope
- Fixing anything (that is the reconcile pass / a per-lab reconcile spec). Note
  bodies. Any Python. Any graph rebuild. `Vault/`.

## Verification
1. Every edge in `vault-map.<L>.yaml` appears in `reports/<L>__<agent>.md` with a class +
   evidence; zero unclassified.
2. Every ORPHAN/MISLABEL row cites the grep/`file:line` that proves it (a reader that
   does/doesn't exist).
3. Seeded case (if any) reproduced.
4. `git --no-pager diff --stat` shows only `apps/vault/audit/reports/<L>__<agent>.md` added.

## Success criteria
`reports/<L>__<agent>.md` classifies every framed edge with code evidence; seeded case matches;
nothing outside `reports/` changed.

## Progress hook
Pack ledger row `T-GTA-<L>`: Status=done, Report=`reports/<L>__<agent>.md`,
Verification="N edges classified: a LIVE / b MISLABEL / c ORPHAN / d PENDING; seeded case OK".
