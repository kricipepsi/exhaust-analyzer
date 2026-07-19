---
node_type: task
task_id: T-UI-VAULT-SUPPORT-1
status: done
pack: VAULT (UI)
lab: ui
mode: coder/vault
blocked_by: []
consumers:
  - "build_lab_vault.py — vault frontmatter derivation"
  - "consumers.base — signal/noise audit view"
  - "T-UI-VAULT (doc-only mode enablement)"
implements:
  - "_skills/graph/4dlab-vault/scripts/build_lab_vault.py"
tags: [task, vault, ui]
---
# T-UI-VAULT-SUPPORT-1 — doc-only corpus mode in build_lab_vault.py + register the `ui` entry

**Pack:** VAULT (UI) · **Targets:** `_skills/graph/4dlab-vault/scripts/build_lab_vault.py` · **Blocked by:** — · **Status:** pending · **Lane:** coder/vault (vault-tooling; no lab inner-loop, no graphify)

## Scope (1 paragraph)

`build_lab_vault.py` can only ingest a finished **lab** — it hard-requires `code + tests + wiki +
docs + graph tiers` under `repo/labs/<lab>` and aborts if any is missing (`:290`). The UI is a
**doc-only design corpus** with none of those. Add a minimal, **additive** "design corpus" mode so a
registered doc-only entry resolves: source root under `apps/`, **docs tier only**, no code/tests/wiki,
`required_graph_tiers=()`, destination `Vault/apps/<name>/`. Register the `ui` entry using it. This is
**not** a rewrite of the lab path — the seven existing labs must behave byte-identically (regression
guard). No graphify, no re-extraction, no lab code touched.

## Signal/noise / consumer

Build-tooling — **no schema field or vault note ships here.** The named consumer of this change is the
**next task, `T-UI-VAULT`**, which runs `--lab ui --dry-run`/build against the new mode. (Same
consumer shape as `T-COM-PATHS-1`: a tooling enablement whose consumer is the vault build that uses it.)

## Exact change (minimal — additive, mirror the existing structure)

1. **New config entry** alongside `LAB_SRC_PATHS` (`:43`). Add a parallel registry (or a
   `corpus_kind` key on the entry) describing a design corpus. Suggested shape:
   ```python
   # apps/ design corpora (doc-only: no code/tests/wiki/graph). Keyed by name.
   APP_SRC_PATHS = {
       "ui": {
           "src_root":             "apps/ui",          # not labs/<lab>
           "docs_notes":           ["4DLab_UI_FieldMap.md", "StreamliteUI.md"],  # explicit list, not a glob
           "required_graph_tiers": (),                 # prose Pass-3 waived; no AST corpus
           "vault_area":           "apps",             # -> Vault/apps/ui/
       },
   }
   ```
2. **Source resolution branch** (`:277-287`). When `a.lab` is a design corpus, set `lab_src =
   repo / src_root`; skip `code_src/tests_src/wiki_src`; `tier_graphs = []`.
3. **Eligibility** (`:290`). For a design corpus, the `missing` set is **only** the listed
   `docs_notes` (each must exist under `src_root`) + the map — not code/tests/wiki/graphs.
4. **Copy** (`:311-315`). Copy only the listed docs into `lab_dst / "docs"` (or directly into the
   tier); do **not** call `copy_tree` on absent code/tests/wiki dirs.
5. **Destination + framing + provenance** (`:307`, `:322-327`, `:363-370`). Destination is
   `vault / vault_area / name` (`Vault/apps/ui/`). Route every framed note to the **docs** tier with
   `source: apps/ui/<note>`. Provenance section reads `source: apps/ui/ (design docs)` and
   `graphs required: none (doc-only design corpus)`.

Keep the diff to these regions. If more than this is needed to make `--lab ui --dry-run` resolve,
**scope only the minimal change** that does and flag the rest as a follow-up — do not enlarge the diff.
The `.base` install and landing-note steps are reused unchanged (the landing note `_ui.md` lands in
`Vault/apps/ui/`).

## Files to change

- `_skills/graph/4dlab-vault/scripts/build_lab_vault.py` — the five regions above.
- **No** vault content, **no** map (that is `T-UI-VAULT`), **no** lab code.

## Success criteria

- **Regression (criterion 1):** capture `--dry-run` for `obdlab` + `comlab` **before** and **after**;
  `diff` empty for both (byte-identical — the lab path is untouched).
- **UI resolves (criterion 2):** `--lab ui --dry-run` no longer aborts on missing code/tests/wiki/graph;
  it advances to the next real gate, `No vault-map for 'ui'` (which is `T-UI-VAULT`'s job). `grep` of
  the output for `code|tests|wiki|graph|not eligible` → none.
- **ruff** clean on the edited script.
- `git diff --stat` shows only `build_lab_vault.py`.

## Inner loop (coder)

Vault-tooling, not lab code — no `pytest`. After the edit:
```bash
cd /agent_workspace
PY=.venv-wired/bin/python
for lab in obdlab comlab; do
  $PY _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab $lab --repo "$PWD" --dry-run > /tmp/${lab}_before.txt
done
# ...make the edit...
for lab in obdlab comlab; do
  $PY _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab $lab --repo "$PWD" --dry-run > /tmp/${lab}_after.txt
  diff /tmp/${lab}_before.txt /tmp/${lab}_after.txt && echo "OK $lab unchanged"
done
$PY _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab ui --repo "$PWD" --dry-run | head -30   # expect: advances to "No vault-map for 'ui'"
ruff check _skills/graph/4dlab-vault/scripts/build_lab_vault.py
```

## VERIFICATION GATE
_(coder fills — OBD+COM dry-runs byte-identical; UI dry-run resolves the doc-only corpus and stops at the missing-map gate; ruff clean)_

## CODE REVIEW
_(coder fills — additive doc-only branch only; lab path untouched; no graphify; minimal diff)_
