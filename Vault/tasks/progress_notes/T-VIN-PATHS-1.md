# T-VIN-PATHS-1 — progress note

**Status:** `done` · **Pack:** VAULT (VINLab)
Task spec: `Vault/tasks/T-VIN-PATHS-1_register_vinlab_source_paths.md` · Pack ledger: `Vault/tasks/VIN_VAULT_TASKS_START_HERE.md`
Run: 2026-06-13 (coder, vault-tooling lane — no lab inner-loop/gate per task role note)

## Plan

Add one `vinlab` entry to `LAB_SRC_PATHS` in
`_skills/graph/4dlab-vault/scripts/build_lab_vault.py`, mirroring the `gaslab`/`dtclab`
entries verbatim: `wiki_subpath: "wiki"`, `wiki_source_template: "labs/{lab}/wiki/{note}"`,
`required_graph_tiers: ("v2_code", "v2_tests")` (prose Pass-3 waived — "skip graph testing").
Consumer (signal/noise): `build_lab_vault.py` itself — without the entry a VIN build falls
through to the OBDLab default (`research/chunks` + four graph tiers) and aborts. No schema
field added; only *where the build reads from* is corrected. Single dict-entry diff; the
existing build logic (line 259 `LAB_SRC_PATHS.get(...)`, line 261 `wiki_subpath`, line 308
`wiki_source_template`, line 263 `required_graph_tiers`) already consumes these keys — no new
mechanism introduced. Read-only on all graphs; no graphify, no re-extraction, no lab code/test edit.

## VERIFICATION GATE

All success criteria met (verified 2026-06-13 with `.venv-wired` Python 3.14.5, PyYAML 6.0.3).
Method: built a `before` copy of the script = current file minus exactly the `vinlab` block
(so the pre-existing uncommitted `symptomlab` entry is present in BOTH — it is not this task's
change and is left untouched per the git rule). Ran each lab's `--dry-run` on before vs after
with `--assets` pinned to the real assets dir so both compare apples-to-apples.

1. **Four existing labs unchanged (regression guard) — PASS.** `obdlab`, `gaslab`, `dtclab`,
   `symptomlab` dry-run outputs are identical before/after on every action line (copy / frame /
   install view / upsert / eligibility / provenance). The *only* byte difference is one
   console-capture artifact at index 2089 in the static `"Done. (dry-run — nothing written)"`
   line — em-dash U+2014 vs replacement U+FFFD, an OEM-codepage redirection artifact between two
   separate captures, on a line this edit never touches. Confirmed by char-level comparison.
2. **VIN dry-run resolves wiki/ + two AST tiers — PASS.** `--lab vinlab --dry-run` now passes the
   eligibility gate (all six real disk paths resolve: `labs/vinlab/vinlab/`, `tests/`, `wiki/`,
   `docs/`, `graph/v2_code/graph.json`, `graph/v2_tests/graph.json` — all `Test-Path = True`) and
   stops only at `No vault-map for 'vinlab'` (line 276). That map is `T-VIN-VAULT`'s deliverable,
   explicitly out of scope here. No spurious `research/chunks` or `v2_wiki`/`v2_docs` abort.
   Contrast (proof the entry is doing the work): the `before` version aborts earlier and
   differently — "not eligible — missing: …/research/chunks, …/v2_wiki/graph.json,
   …/v2_docs/graph.json" — the exact documented OBD-fall-through defect.
3. **Provenance string correct — PASS (by construction).** The `wiki_source_template` added is
   byte-identical to gaslab/dtclab's `"labs/{lab}/wiki/{note}"`, which the gaslab/dtclab
   regression runs proved emit `labs/<lab>/wiki/<note>`. A VIN wiki note therefore reads
   `source: labs/vinlab/wiki/<note>`. (Full string only renders once the vault-map names a wiki
   note, at `T-VIN-VAULT` — the template that produces it is verified here.)
4. **No graphify / no re-extraction / no lab edit — PASS.** Diff is one `LAB_SRC_PATHS` dict
   entry. Frozen `graph/v2_current/`, `graph/v1_baseline/` untouched; no `*/vinlab/` or `*/tests/`
   source edit; no graph rebuilt.

## CODE REVIEW

- **Minimal one-entry diff.** `git diff` shows only the additive `vinlab` block in
  `LAB_SRC_PATHS` (plus the pre-existing uncommitted `symptomlab` block, which is NOT this task's
  change and is left as-is per the workspace git rule). Nothing else in the file changed.
- **Mirrors the sibling entries exactly.** Keys, values, and comment style match `gaslab`/`dtclab`;
  no new key, no new code path, no signature change. The consuming sites (lines 259/261/263/308)
  were inspected and already read these keys generically — the entry slots in with zero logic edit.
- **Scope discipline / flagged follow-up (do not enlarge the diff).** Line 345
  `if a.lab in ("gaslab", "dtclab"):` appends a cosmetic "v2_wiki/v2_docs waived by owner
  direction" suffix to `PROVENANCE.md` for those two labs only. VINLab also waives those tiers, so
  for cosmetic parity `vinlab` could be added to that tuple. It is **not** a path-resolution gate
  (it only affects a provenance note's wording during the *real* build, not the dry-run or
  eligibility), so adding it would exceed this task's contracted one-entry change. **Flagged as a
  follow-up for `T-VIN-VAULT`** (the session that runs the real build and writes PROVENANCE.md),
  per the spec's "scope only the minimal change … flag the rest as a follow-up."
- No `consumers` auto-derived; no graphify side-effect; frozen graphs untouched.
