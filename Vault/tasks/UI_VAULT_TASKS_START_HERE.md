# UI → Vault — PIPELINE PACK · START HERE

Read this first, every session, before any other action in the UI vault pack.
(Paste this file as message 1 of a fresh coder/author session.)

**Pack:** VAULT (UI design corpus) · **Corpus:** `apps/ui/` · **Authored:** 2026-06-28 (architect, Cowork)
**Pipeline spec:** `planning/LAB_TO_VAULT_PIPELINE_GUIDE.md`
**Vault plan:** `Vault/VAULT_IMPLEMENTATION_PLAN.md`
**Driving skill:** `4dlab-vault` (`_skills/graph/4dlab-vault/`)
**Sibling precedent:** the COMLab vault pack (`COM_VAULT_TASKS_START_HERE.md`) — same `4dlab-vault` machinery.

(Paths are relative to the workspace root `/agent_workspace`.)

> **One rule above all (signal/noise):** nothing — no vault frontmatter key, no framed note —
> ships unless a **named, existing consumer** reads it on a real code path. "Future use" is not a
> consumer. A note with an empty `consumers` list is not ready to ship → leave it `plain:`.

---

## 0. Why the UI is NOT a normal lab (read before touching the build script)

The pipeline guide is written for **labs** with four corpora (code · tests · wiki · docs) plus AST
graph tiers. **The UI has none of code / tests / wiki / graph** — it is a **doc-only design corpus**:

| Pipeline corpus/phase | UI status |
|---|---|
| code (`labs/<lab>/<lab>/`) | **absent** — `apps/ui/` is jsx/html mockups + a reference `.py`, not a graphed package |
| tests, wiki | **absent** |
| docs (the migrated content) | **`apps/ui/4DLab_UI_FieldMap.md` + `apps/ui/StreamliteUI.md`** — the field/consumer contract + the rendering-pattern notes |
| Phase-1 DOCS currency | **done** — `T-UI-SYNC-1` (in `apps/ui/tasks/`) reconciled the FieldMap to current schemas |
| Phase-2 prep / Phase-3 graphify | **waived** (prose Pass-3 waiver, mirrors COM/DTC/VIN); no AST corpus exists to graph |
| Phase-4 vault | **the whole job of this pack** |

`build_lab_vault.py` hard-requires `code_src + tests_src + wiki_src + docs_src + graph tiers`
(`scripts/build_lab_vault.py:290`) and resolves source under `repo/labs/<lab>`. A UI build aborts on
**all five** missing inputs. So unlike a lab, the UI needs a **build-script change first**
(`T-UI-VAULT-SUPPORT-1`) — a doc-only corpus mode — before the vault build (`T-UI-VAULT`) can run.
This is the one structural difference from the lab packs; everything downstream mirrors them.

**Owner decisions (2026-06-28):** doc-only corpus mode; home the tier at a **new `Vault/apps/ui/`**
area (not `Vault/labs/`); migrate **FieldMap + StreamliteUI.md** only (not the jsx/html mockups).

## 1. Scope trims applied to this pack

- **No CODE / TESTS / WIKI / GRAPH tracks.** Structurally absent — there is no package to clean,
  no suite to green, no wiki to prep, no AST tier to build. The four lab Phase-1/2/3 rows do not exist.
- **Prose graphs WAIVED** (mirror COM/DTC/VIN/DNA). The vault copies the two `.md` notes raw + injects
  architect-named frontmatter — no `v2_docs` prose graph. `required_graph_tiers` for the UI entry is
  **`()`** (empty). Liftable only if the owner later wants a UI docs graph (needs a Pass-3 backend).
- **Mockups EXCLUDED.** `UI design/*.jsx`, `*.html`, `*.css`, `sampleUI/`, `_sample_app_reference.py`
  are presentation artifacts, not consumer-bearing contract docs — out of this pack's scope.
- **DOCS currency is DONE.** `T-UI-SYNC-1` reconciled the FieldMap (`Status: done`). `StreamliteUI.md`
  is design-pattern prose (low drift); a spot-check at VAULT time is enough — no separate DOCS task.

## 2. The chain (run in dependency order — one task per session)

```
PHASE 4  T-UI-VAULT-SUPPORT-1   doc-only corpus mode in build_lab_vault.py + register `ui` entry   coder/vault
              │
         T-UI-VAULT             vault-map.ui.yaml + dry-run + build into Vault/apps/ui/ + bases      author/vault
```

`T-UI-VAULT-SUPPORT-1` is the hard blocker on `T-UI-VAULT` (the build can't resolve a doc-only
corpus until the mode exists). No other ordering applies — there are only two tasks.

## 3. Pack ledger (source of truth — the next task is the first `pending` row whose Blocked-by are all `done`)

| ID | Task file | Status | Blocked by | Lane | Load skills (this task only) |
|---|---|---|---|---|---|
| T-UI-SYNC-1 | `apps/ui/tasks/T-UI-SYNC-1_fieldmap_consumer_audit.md` | done | — | coder | — (DOCS-currency precursor; reference only) |
| T-UI-VAULT-SUPPORT-1 | `T-UI-VAULT-SUPPORT-1_doc_only_corpus_mode.md` | done | — | coder/vault | **4dlab-vault** |
| T-UI-VAULT | `T-UI-VAULT_build_ui_vault.md` | done | T-UI-VAULT-SUPPORT-1 | author/vault | **4dlab-vault** |

**Each task loads ONLY the skills on its row.** No custom UI skill bundle is authored — two tasks is
below the ≥3-task trigger for an on-demand skill; both reuse the shared `4dlab-vault` skill.

## 4. Non-negotiables (carry from Vault rules)

- **Python 3.14 ONLY** via the shared venv: call `/agent_workspace/.venv-wired/bin/python` directly
  (never bare `python`/`python3` — system default is 3.12). `T-UI-VAULT-SUPPORT-1` runs the
  build-script's own checks (`ruff check` on the edited script); there is no lab inner-loop.
- **Regression guard on the build script.** Any edit to `build_lab_vault.py` must leave the seven
  existing labs' `--dry-run` output **byte-identical** before vs after (the `T-COM-PATHS-1` guard).
  The doc-only mode is **additive** — keyed off a new config entry, never a change to the lab path.
- **No graphify, ever, in this pack.** The UI has no AST corpus; `required_graph_tiers=()`. The KG
  pre-step resolves to **SKIP**. Frozen lab graphs are untouched.
- **`consumers` is architect-named, never auto-derived.** Empty list = not ready → leave `plain:`.
- **Signal/noise at the edge:** the FieldMap frames only because its consumer is real and existing —
  the wired screen `apps/4DLabWired/app.py` (which implements the field placement) and the lab schemas
  it contracts. Name that consumer in the map; do not fabricate.
- Reports in `.md` only; **archive, never delete**. Leave `ARCHIVE/ui1`, `ARCHIVE/UI` untouched.
- **One task per session.** Fill `VERIFICATION GATE` + `CODE REVIEW` in `progress_notes/<id>.md`
  (open with the confirmed `## Plan`), flip the ledger row to `done`, then STOP.

## 5. Follow-ups for the owner (not authored as pack tasks)

- **Reusable design-corpus mode.** `T-UI-VAULT-SUPPORT-1` adds a generic doc-only corpus path under
  `apps/`. If other app docs later want vault presence (e.g. `apps/4DLabWired/docs/HLD_Wiring_4DLab.md`),
  they reuse the same mode — register an entry, author a map. Not authored here (UI-only scope).
- **StreamliteUI.md currency.** It is rendering-pattern prose, lower drift risk than the FieldMap.
  `T-UI-VAULT` spot-checks it against current `app.py` rendering at frame time; if it has drifted
  materially, route a one-line architect doc fix (out-of-band) rather than enlarging this pack.
- A UI-vault-pack pointer is **not** added to `/agent_workspace/CLAUDE.md` — this pack is a
  self-contained paste-doc started from this file, exactly like its lab siblings in `Vault/tasks/`.
