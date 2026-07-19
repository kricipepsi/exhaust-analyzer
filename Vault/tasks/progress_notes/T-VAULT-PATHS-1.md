# T-VAULT-PATHS-1 — progress note

## Plan

Align the vault plan, skill, and OBD map with the four finished graphified pieces and remove the
legacy "design docs live in wiki/" assumption. Source mapping becomes explicit per tier: code ← `obdlab/`
(v2_code), tests ← `tests/` (v2_tests), wiki ← `research/chunks/` (v2_wiki, already ingested), docs ← `docs/`
(v2_docs, pending TODO-4). Repoint every HLD/DLD/LLD/PRD reference in `vault-map.obdlab.yaml`, the plan, and
the skill reference files from `labs/obdlab/wiki/…` to `labs/obdlab/docs/…`; drop the `OBDLab_KG_Wiki.md`
frame (archived 2026-06-10) and the `OBDlab.md` superseded-blueprint frame; and rework `build_lab_vault.py` to
copy each tier from its real source folder with no dependency on the now-empty `wiki/`. Correct the plan §2
claim that the design docs are "already graphified" — the manifest shows only `research/chunks/**` +
`vocabulary.py`, so docs graphify is TODO-4 and gates the docs-tier copy. No `graph.json` re-extraction;
`research/chunks/` does not move; `graphify-out/manifest.json` stays untouched. Vault-tooling lane — no lab
inner-loop/gate.

## VERIFICATION GATE

### 1) No design-doc reference still points at wiki/

```
grep -rn 'obdlab/wiki/' Vault/ _skills/graph/4dlab-vault/ \
  | grep -E 'HLD|DLD|LLD|PRD|ADR|BDD'
```
**PASS** — zero design-doc paths reference `obdlab/wiki/`. The only remaining `obdlab/wiki/`
hit is the archive path in the §8 follow-ups table (`ARCHIVE/2026-06-10_obsolete-wiki/obdlab/wiki/`),
which is a historical archive note, not a design-doc reference.

### 2) KG-wiki + OBDlab frames gone from the map

```
grep -qE 'OBDLab_KG_Wiki|^\s*OBDlab\.md:' _skills/graph/4dlab-vault/assets/vault-map.obdlab.yaml
```
**PASS** — both frames removed. The vault-map now carries only 4 framed design docs (PRD, HLD, LLD, DLD).

### 3) Build dry-run resolves all 4 tier sources, no missing-note warning

```
python3.14 _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab obdlab \
  --repo C:\Users\muto\claude\4DApp\4DLab\4DLabV2 --dry-run
```
**PASS** — all 4 tiers resolve:
- `code ← labs/obdlab/obdlab/`
- `tests ← labs/obdlab/tests/`
- `wiki ← labs/obdlab/research/chunks/`
- `docs ← labs/obdlab/docs/`

Four design-doc frames route to `tier=docs` with `source: labs/obdlab/docs/<note>`.
Zero "not found" or "missing" warnings. Zero KG-wiki/OBDlab frames processed.

### 4) Graph provenance untouched

```
git diff --name-only -- 'labs/obdlab/graphify-out/' 'labs/obdlab/research/chunks/'
```
**PASS** — empty diff; graph and corpus untouched.

## CODE REVIEW

Files changed = 7. All changes are path/convention corrections. No schema fields added.
No graph re-extraction. No lab code touched.

1. **`_skills/graph/4dlab-vault/assets/vault-map.obdlab.yaml`** — 4 design-doc consumer
   cross-refs `wiki/` → `docs/`; `OBDLab_KG_Wiki.md` frame (lines 78-89) removed;
   `OBDlab.md` frame (lines 91-99) removed. Clean 4-frame map remains.

2. **`_skills/graph/4dlab-vault/scripts/build_lab_vault.py`** — `wiki_src` changed from
   `lab_src / "wiki"` to `lab_src / "research" / "chunks"`; `docs_src = lab_src / "docs"`
   added; eligibility now checks all 5 inputs (code, tests, wiki=research/chunks, docs, graph);
   4-tier copy (code/tests/wiki/docs); frontmatter injection routes by `node_type` — design
   docs (`prd|hld|lld|dld`) → `docs/` tier with `source: labs/<lab>/docs/<note>`, wiki →
   `wiki/` tier with `source: labs/<lab>/research/chunks/<note>`; provenance string updated;
   docstring updated. Python syntax check passes.

3. **`_skills/graph/4dlab-vault/SKILL.md`** — eligibility lists `research/chunks/` + `docs/`
   instead of `wiki/`; copy table shows 4 tiers with `wiki ← research/chunks/` and
   `docs ← docs/`; `wiki/` folder noted as retired.

4. **`_skills/graph/4dlab-vault/reference/frontmatter-schema.md`** — `source:` example
   `wiki/` → `docs/` (line 23).

5. **`_skills/graph/4dlab-vault/reference/obsidian-cli-optional.md`** — backlinks example
   `wiki/` → `docs/` (line 29).

6. **`_skills/graph/4dlab-vault/reference/obsidian-md-conventions.md`** — frontmatter
   `source:` example `wiki/` → `docs/` (line 11); callout provenance `wiki/` → `docs/`
   (line 36).

7. **`Vault/VAULT_IMPLEMENTATION_PLAN.md`** — §2 rewritten: 4-tier table, "not yet
   graphified" correction (design docs gated on TODO-4), archive note, `wiki/` folder
   retired; §3 layout diagram adds `docs/` tier, wiki comment → `research/chunks/`,
   "Not copied" text → `code/test/wiki/docs`; §4 `source:` example `wiki/` → `docs/`.
