# T-VAULT-VOCAB-1 — progress note

## Plan

Add a single standalone OBD vocabulary note to the vault without re-introducing the triplication that
T-SEM-5 removed. A new shared `Vault/_vocabulary/OBD_VOCABULARY.md` is built **from the canonical**
`labs/semantic/vocabul/OBD_VOCABULARY.md` (body md5 `B14AFE09…`), carrying §4 frontmatter (`node_type: wiki`,
`lab: obdlab`, `module: semantic-vocabulary`, named `consumers`, `drift_guards`, `source`). An
architect-authored `assets/vault-map.vocabulary.yaml` supplies the semantic fields; `build_lab_vault.py` gains
an idempotent `--vocab` path that copies the canonical body and injects frontmatter into `_vocabulary/`. The
obdlab landing note template gains a `[[OBD_VOCABULARY]]` wikilink, and `_meta/PROVENANCE.md`
records the copy. Signal/noise: no new frontmatter field is introduced; the note carries 3 named consumers and
is itself consumed by `consumers.base` + the landing-note link. This is the vault-tooling lane — no lab
inner-loop/gate, no `graph.json` re-extraction.

## VERIFICATION GATE

### 1) Build dry-run then real

```
python3.14 build_lab_vault.py --vocab --repo <repo> --dry-run
python3.14 build_lab_vault.py --vocab --repo <repo>
```
**PASS** — dry-run resolves canonical source + md5; real build writes note + provenance. Idempotent on re-run.

### 2) Body md5 match (strip frontmatter, compare md5)

```
python3.14 -c "..." → BODY-MATCH canonical=B14AFE095EC0C2765B6FAEC2D23CA851 vault=B14AFE095EC0C2765B6FAEC2D23CA851
```
**PASS** — vault body byte-identical to canonical `labs/semantic/vocabul/OBD_VOCABULARY.md`.

### 3) Frontmatter valid + consumers non-empty

```
python3.14 -c "..."
→ FM-OK node_type=wiki consumers=3 lab=obdlab module=semantic-vocabulary source=labs/semantic/vocabul/OBD_VOCABULARY.md
```
**PASS** — `node_type: wiki` (reused, no new enum), 3 named consumers, all required fields present.

### 4) Idempotent re-run

```
python3.14 build_lab_vault.py --vocab → Done. (no error, no duplicate)
```
**PASS** — re-run updates in place, provenance not duplicated (marker guard).

### 5) Provenance recorded

```
_meta/PROVENANCE.md contains B14AFE095EC0C2765B6FAEC2D23CA851
```
**PASS** — source path, date, and body md5 recorded.

## CODE REVIEW

Files changed/created = 7:

1. **`_skills/graph/4dlab-vault/assets/vault-map.vocabulary.yaml`** (NEW) — architect-authored consumer map:
   OBD entry with 3 named consumers, canonical source path, semantic fields. GAS/DTC stubs commented.

2. **`_skills/graph/4dlab-vault/scripts/build_lab_vault.py`** — added `--vocab` flag + `build_vocabulary_area()`
   function. Reads `vault-map.vocabulary.yaml`, copies canonical body per entry, injects §4 frontmatter,
   appends provenance (idempotent via marker guard). `--lab` made optional when `--vocab` set.
   Added `hashlib` import. Fixed `_meta/` parent directory creation for provenance on first run.

3. **`_skills/graph/4dlab-vault/SKILL.md`** — workflow step 0 documents `_vocabulary/` build; copy table
   adds shared `_vocabulary/` row; assets list adds `vault-map.vocabulary.yaml`; step 4 description
   updated to mention `docs/` tier.

4. **`_skills/graph/4dlab-vault/assets/lab-landing.md.tmpl`** — "See the design docs in `wiki/`" → `docs/`
   (stale reference fix from T-VAULT-PATHS-1); added `[[OBD_VOCABULARY]]` wikilink section.

5. **`Vault/VAULT_IMPLEMENTATION_PLAN.md`** — §3 layout tree diagram `docs/` indentation fixed; §4
   description updated to note `_vocabulary/` notes reuse `node_type: wiki`; §8 follow-ups row
   marked DONE.

6. **`Vault/_vocabulary/OBD_VOCABULARY.md`** (NEW) — built by `--vocab`; canonical body + §4 frontmatter.

7. **`Vault/_meta/PROVENANCE.md`** (NEW) — created by `--vocab` build; records vocab source + md5.
