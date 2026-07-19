# T-DNAV-PATHS-1 — progress note

**Status:** `done` · **Pack:** VAULT (DNALab)
Task spec: `Vault/tasks/T-DNAV-PATHS-1_register_dnalab_source_paths.md` · Pack ledger: `Vault/tasks/DNA_VAULT_TASKS_START_HERE.md`
Run: 2026-06-13 (coder, vault-tooling lane — no lab inner-loop/gate per task role note)

## Plan

Add one `dnalab` entry to `LAB_SRC_PATHS` in `_skills/graph/4dlab-vault/scripts/build_lab_vault.py`, mirroring the `gaslab`/`dtclab` entries verbatim: `wiki_subpath: "wiki"`, `wiki_source_template: "labs/{lab}/wiki/{note}"`, `required_graph_tiers: ("v2_code", "v2_tests")` (prose Pass-3 waived — "skip graph testing").
Consumer (signal/noise): `build_lab_vault.py` itself — without the entry a DNA build falls through to the OBDLab default (`research/chunks` + four graph tiers) and aborts. No schema field added; only *where the build reads from* is corrected. Single dict-entry diff; the existing build logic already consumes these keys — no new mechanism introduced. Read-only on all graphs; no graphify, no re-extraction, no lab code/test edit.

## VERIFICATION GATE

All success criteria met (verified 2026-06-13 with PowerShell and git status/diff).

1. **Four existing labs unchanged (regression guard) — PASS.** `obdlab`, `gaslab`, `dtclab`, `symptomlab`, and `vinlab` dry-run outputs are identical before/after on every action line (copy / frame / install view / upsert / eligibility / provenance). Verified by running dry-runs to file outputs before and after the edit, and comparing them using PowerShell `Compare-Object` which returned empty differences.
2. **DNALab dry-run resolves wiki/ + two AST tiers — PASS.** `--lab dnalab --dry-run` now passes the eligibility gate (all six real disk paths resolve: `labs/dnalab/dnalab/`, `tests/`, `wiki/`, `docs/`, `graph/v2_code/graph.json`, `graph/v2_tests/graph.json` — all `Test-Path = True`) and stops only at `No vault-map for 'dnalab'` (line 281). That map is `T-DNAV-VAULT`'s deliverable, explicitly out of scope here. No spurious `research/chunks` or `v2_wiki`/`v2_docs` abort.
3. **Provenance string correct — PASS (by construction).** The `wiki_source_template` added is byte-identical to gaslab/dtclab's `"labs/{lab}/wiki/{note}"`, which the gaslab/dtclab regression runs proved emit `labs/<lab>/wiki/<note>`. A DNA wiki note therefore reads `source: labs/dnalab/wiki/<note>`. (Full string only renders once the vault-map names a wiki note, at `T-DNAV-VAULT` — the template that produces it is verified here.)
4. **No graphify / no re-extraction / no lab edit — PASS.** Diff is one `LAB_SRC_PATHS` dict entry. Frozen `graph/v2_current/`, `graph/v1_baseline/` untouched; no `*/dnalab/` or `*/tests/` source edit; no graph rebuilt.

## CODE REVIEW

- **Minimal one-entry diff.** `git diff` shows only the additive `dnalab` block in `LAB_SRC_PATHS` (plus the pre-existing uncommitted `symptomlab` and `vinlab` blocks, which are NOT this task's change and are left as-is per the workspace git rule). Nothing else in the file changed.
- **Mirrors the sibling entries exactly.** Keys, values, and comment style match `gaslab`/`dtclab`; no new key, no new code path, no signature change. The consuming sites were inspected and already read these keys generically — the entry slots in with zero logic edit.
- **Scope discipline / flagged follow-up (do not enlarge the diff).** Line 351 `if a.lab in ("gaslab", "dtclab"):` appends a cosmetic "v2_wiki/v2_docs waived by owner direction" suffix to `PROVENANCE.md` for those two labs only. DNALab also waives those tiers, so for cosmetic parity `dnalab` could be added to that tuple. It is **not** a path-resolution gate (it only affects a provenance note's wording during the *real* build, not the dry-run or eligibility), so adding it would exceed this task's contracted one-entry change. **Flagged as a follow-up for `T-DNAV-VAULT`** (the session that runs the real build and writes PROVENANCE.md).
- No `consumers` auto-derived; no graphify side-effect; frozen graphs untouched.
