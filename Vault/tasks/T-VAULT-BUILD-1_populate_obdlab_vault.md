---
node_type: task
task_id: T-VAULT-BUILD-1
status: done
pack: VAULT
lab: obdlab
mode: strict
blocked_by: []
consumers:
- build_lab_vault.py — vault frontmatter derivation
- consumers.base — signal/noise audit view
- drift-guards.base — coverage view
- modules.base — module map view
- graph/v2_code — AST code graph
- _meta/PROVENANCE.md — reconcile
implements:
- graph/v2_code/graph.json
- graph/v2_tests/graph.json
- graph/v2_wiki/graph.json
- graph/v2_docs/graph.json
- vault-map.obdlab.yaml
tags:
- task
- vault
- obdlab
---

# T-VAULT-BUILD-1 — Populate the OBDLab vault (run build_lab_vault.py, 4 tiers)

**Status:** `done` · **Pack:** VAULT (OBDLab tier) · **Mode:** STRICT (vault-tooling lane — no lab inner-loop/gate)
**Origin:** plan §8 follow-up "Run the build to populate the OBD vault" → authored 2026-06-11 (architect)
**Blocked by:** — (all four graphified tiers present on disk — verified below; see Precondition)
**Consumer (signal/noise):** **No schema field added.** This task ships the populated `Vault/labs/obdlab/`
whose per-note frontmatter fields each have a named consumer in plan §4 — the three `.base` views
(`modules.base`, `consumers.base`, `drift-guards.base`) and the Obsidian graph view read every framed
field. No "future use" frontmatter; the build script's own signal/noise gate refuses any framed note with
an empty `consumers` list.

### Role note (vault-tooling lane) ###

`build_lab_vault.py` is vault tooling, not lab diagnostic code — not subject to the lab inner-loop / 6-phase
gate (plan §5). The architect authors this spec; a **build session** executes it. No `obdlab/` lab code is
touched, and **no `graph.json` re-extraction** is run (graphify is forbidden here — the four tier graphs are
already built and frozen).

### Goal ###

Run the OBDLab vault build end-to-end for the first time, producing `Vault/labs/obdlab/` with all four tiers
(code, tests, wiki, docs), consumer-aware frontmatter on the framed design-doc notes, the three `.base`
views installed, and refreshed `System-Map.md` + `_meta/PROVENANCE.md`. This closes the last step in plan §8
("Run the build to populate the OBD vault") now that every tier is graphified.

### Precondition (verified present 2026-06-11) ###

The four finished, graphified tiers all exist — the lab is build-eligible **once the gate is corrected** (see
the builder note in Success criteria #1):

| Vault tier | Source folder (copied) | Graph proof (must exist) | State |
|---|---|---|---|
| code | `labs/obdlab/obdlab/` | `labs/obdlab/graph/v2_code/graph.json` | present |
| tests | `labs/obdlab/tests/` | `labs/obdlab/graph/v2_tests/graph.json` | present |
| wiki | `labs/obdlab/research/chunks/` (7 topic dirs) | `labs/obdlab/graph/v2_wiki/graph.json` | present |
| docs | `labs/obdlab/docs/` | `labs/obdlab/graph/v2_docs/graph.json` | present (TODO-4 closed) |

The legacy single `labs/obdlab/graphify-out/graph.json` was **retired** when the four-tier model landed and is
**absent**. The build's eligibility gate still references it (see #1) and would exit "not eligible" — this is
the only thing standing between the current tree and a populated vault.

### Success criteria ###

1. **Builder eligibility gate corrected to the four-tier model.** `build_lab_vault.py` currently sets
   `graph = lab_src / "graphify-out" / "graph.json"` (~line 197) and includes it in the `missing` list
   (~line 200). Replace that single-graph proof with the four tier proofs
   (`graph/v2_code/graph.json`, `graph/v2_tests/graph.json`, `graph/v2_wiki/graph.json`,
   `graph/v2_docs/graph.json`); the source-folder checks (`code_src/tests_src/wiki_src/docs_src`) stay. Also
   correct the PROVENANCE string (~line 276) that prints `canonical graph (not copied): …/graphify-out/graph.json`
   to point at `labs/obdlab/graph/` (the four tier dirs). Surgical: no other builder behaviour changes.
2. **Dry-run is clean.** `build_lab_vault.py --lab obdlab --dry-run` resolves all four tier sources, lists the
   framed design-doc notes with `consumers=<n≥1>` each, and prints **no** "not eligible", "not found", or
   "missing" line. No signal/noise breach (no framed note with empty `consumers`).
3. **Apply populates `Vault/labs/obdlab/`** with `code/`, `tests/`, `wiki/`, `docs/`, the `_obdlab.md` landing
   note, framed frontmatter on PRD/HLD/LLD/DLD (design docs, `tier=docs`), and `__pycache__`/`.pyc`/cache
   cruft excluded (the script's `IGNORE` set).
4. **The three `.base` views are installed** to `Vault/_bases/` and **render with rows** in Obsidian:
   `modules.base` groups OBD notes by module; `consumers.base` shows every framed note with ≥1 named consumer;
   `drift-guards.base` shows each `implements` target with its guarding test(s).
5. **`System-Map.md` and `_meta/PROVENANCE.md` refreshed** — provenance records the build date, the four
   source tiers, and the framed-note count; the canonical graphs are recorded as *not copied*.
6. **Idempotent:** a second `--lab obdlab` run produces no diff (re-frames in place, never duplicates).
7. **No re-extraction:** `git status --porcelain` shows **no** change under `labs/obdlab/graph/`,
   `labs/obdlab/research/chunks/`, or any `graphify-out/`; no graphify command was run.

### Context ###

- Vault layout target: plan §3. Frontmatter node schema + the §4 consumer table govern every framed field.
- Framing source of truth: `_skills/graph/4dlab-vault/assets/vault-map.obdlab.yaml` — PRD/HLD/LLD/DLD are
  framed there with named `consumers`; ADR/BDD and the vocab duplicate are **not** framed (copied as plain
  markdown), consistent with T-VAULT-DOCPREP-1's ingest exclusions. `consumers` are architect-authored, never
  auto-derived from any `graph.json`.
- `_vocabulary/OBD_VOCABULARY.md` already exists (T-VAULT-VOCAB-1, `--vocab` path) — out of scope here; the
  landing template already wikilinks it.
- The four tier graphs are *read for eligibility only*; the build copies `docs/`/`research/chunks/` as
  markdown and injects frontmatter from the vault-map — it does **not** read graph node data into notes.

### Deliverables ###

1. `_skills/graph/4dlab-vault/scripts/build_lab_vault.py` — eligibility gate → four-tier graph proofs;
   PROVENANCE string → `graph/` tiers. **(build session, vault-tooling lane)**
2. `Vault/labs/obdlab/` — populated 4-tier vault (code, tests, wiki, docs) + `_obdlab.md` landing note.
3. `Vault/_bases/{modules,consumers,drift-guards}.base` — installed.
4. `Vault/System-Map.md` (created/refreshed) + `Vault/_meta/PROVENANCE.md` (OBD section appended).
5. `Vault/tasks/progress_notes/T-VAULT-BUILD-1.md` — `VERIFICATION GATE` + `CODE REVIEW` filled by the build
   session.

### Files to touch ###

- `_skills/graph/4dlab-vault/scripts/build_lab_vault.py`
- `Vault/labs/obdlab/**` (generated)
- `Vault/_bases/*.base` (generated)
- `Vault/System-Map.md`, `Vault/_meta/PROVENANCE.md` (generated/refreshed)
- `Vault/tasks/progress_notes/T-VAULT-BUILD-1.md`

### Out of scope ###

- **Any graphify run / re-extraction** — forbidden; the four tier graphs are frozen artefacts.
- **Editing `vault-map.obdlab.yaml`** — framing is already correct (T-VAULT-PATHS-1). If the dry-run surfaces
  a genuinely missing consumer, log it to plan §8 follow-ups; do not invent one to satisfy the gate.
- **Pass-3 graph cross-checks** (T-VAULT-DOCGRAPH-2 / WIKIGRAPH-1 / CODEGRAPH-1) — separate quality tasks; the
  vault build does not depend on them.
- **Relocating `Vault/Obsidian*.md`** into `_skills/`, or copying `graph.json` into the vault — plan §8
  follow-ups, decided explicitly, not here.
- **Other labs** (GASLab has its own `T-GAS-VAULT`).
- Surgical rule: the only builder edit is the eligibility/PROVENANCE path correction. Any other drift → §8.

### Verification (build session — vault-tooling lane) ###

```bash
cd <repo>/4DLabV2
# 1) four tier graphs present; legacy single graph absent (eligibility precondition)
for g in v2_code v2_tests v2_wiki v2_docs; do test -f labs/obdlab/graph/$g/graph.json \
  && echo "OK $g" || { echo "FAIL missing $g/graph.json"; exit 1; }; done
test -e labs/obdlab/graphify-out/graph.json && echo "NOTE legacy graph still present" || echo "OK legacy graph absent"
# 2) dry-run resolves all tiers, no breach
python3.14 _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab obdlab --dry-run | tee /tmp/vb.txt
grep -qiE 'not eligible|not found|missing|signal/noise breach' /tmp/vb.txt \
  && { echo "FAIL build not clean"; exit 1; } || echo "OK dry-run clean"
# 3) apply, then re-run for idempotency (no diff on second run)
python3.14 _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab obdlab
python3.14 _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab obdlab | tee /tmp/vb2.txt
# 4) four tiers materialised + bases installed
ls Vault/labs/obdlab/{code,tests,wiki,docs}/ >/dev/null && ls Vault/labs/obdlab/_obdlab.md >/dev/null \
  && ls Vault/_bases/{modules,consumers,drift-guards}.base >/dev/null && echo "OK vault materialised"
# 5) no graph/corpus re-extraction
git status --porcelain -- labs/obdlab/graph/ labs/obdlab/research/chunks/ \
  && echo "(expect empty — no graph/corpus change)"
# 6) Obsidian (manual): open Vault/, confirm the 3 Bases render with rows and graph view shows OBD;
#    orphans/unresolved empty or explained.
```

All checks pass; OBD's code/tests/wiki/docs are browsable in Obsidian, the three Bases render, every framed
note carries ≥1 named consumer, and no re-extraction occurred.

### Progress hook ###

`Vault/tasks/progress_notes/T-VAULT-BUILD-1.md` opens with the confirmed `## Plan`; the build session fills
`VERIFICATION GATE` + `CODE REVIEW`. The plan §8 row flips to `done` only when both blocks are clean, the six
automated checks pass, and the manual Obsidian render (check 6) is confirmed.
