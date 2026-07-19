---
node_type: task
task_id: T-VAULT-PATHS-1
status: pending
queue: next
pack: VAULT · **Mode:** STRICT
lab: obdlab
mode: strict
blocked_by: []
consumers:
- build_lab_vault.py — vault frontmatter derivation
- graph/v2_code — AST code graph
- graph/v2_tests — AST test graph
- graph/v2_docs — docs graph
- graph/v2_wiki — wiki graph
- _meta/PROVENANCE.md — reconcile
implements:
- vault-map.obdlab.yaml
tags:
- task
- vault
- obdlab
---

# T-VAULT-PATHS-1 — Fix docs/wiki convention + path references (4-tier vault model)

**Status:** `pending (next)` · **Pack:** VAULT · **Mode:** STRICT (vault-tooling lane — no lab inner-loop/gate)
**Origin:** owner request 2026-06-10 (docs/wiki mismatch + KG-wiki archive) · **Blocked by:** —
**Consumer (signal/noise):** **No schema field added.** Corrects the existing `source:` frontmatter field
(consumer: `_meta/PROVENANCE.md` + rebuild/reconcile per plan §4) and the build's per-tier copy paths so each
vault tier resolves to a real, finished graphified piece. Pure convention/path correctness.

### Role note (vault-tooling lane) ###

`build_lab_vault.py` is vault tooling, not lab diagnostic code — not subject to the lab inner-loop / 6-phase
gate (plan §5). Architect authors this spec; a **build session** executes it. No `obdlab/` lab code, no
`graph.json` re-extraction.

### Goal ###

Make the vault model internally consistent with the **four finished graphified pieces** that already exist,
and remove the legacy assumption that design docs live in `wiki/`. The confusion: the vault plan/skill/map
were written assuming `labs/obdlab/wiki/` holds the design docs and the build copies `wiki/`. In reality:

| Vault tier | Source folder | Graph piece | State |
|---|---|---|---|
| code | `labs/obdlab/obdlab/` | `graph/v2_code/` | finished |
| tests | `labs/obdlab/tests/` | `graph/v2_tests/` | finished |
| **wiki** | **`labs/obdlab/research/chunks/`** | `graph/v2_wiki/` (451 nodes) | finished |
| **docs** | **`labs/obdlab/docs/`** | `graph/v2_docs/` | **pending TODO-4 graphify** |

The obsolete `OBDLab_KG_Wiki.md` (old v1 baseline, `graph/v1_baseline/`) was **archived 2026-06-10** to
`ARCHIVE/2026-06-10_obsolete-wiki/`; the `v2_wiki` piece (`research/chunks`) supersedes it.

### Success criteria ###

1. **Convention recorded** in `VAULT_IMPLEMENTATION_PLAN.md` §2–§3 (and the vault `CLAUDE.md` when built):
   `docs/` = design documents (official); `research/chunks/` = wiki/domain corpus (graph-canonical — does
   **not** move); `wiki/` folder = **retired**.
2. **No reference in the vault plan / skill / map points a design doc** (`HLD/DLD/LLD/PRD/ADR/BDD`) **at
   `labs/obdlab/wiki/`** — all repointed to `labs/obdlab/docs/`. `grep -rn 'obdlab/wiki/' Vault/ _skills/graph/4dlab-vault/`
   returns nothing for design-doc paths.
3. **`vault-map.obdlab.yaml`:**
   - HLD/LLD/DLD/PRD `source` + cross-ref consumer paths → `labs/obdlab/docs/…`.
   - `OBDLab_KG_Wiki.md` `frame:` entry **removed** (archived/obsolete).
   - `OBDlab.md` `frame:` entry **removed** (superseded blueprint; handoff TODO-3 archives the file itself —
     out of scope here, but it must not be a framed vault node).
4. **`build_lab_vault.py`** copies each tier from its real source — `code←obdlab/`, `tests←tests/`,
   `wiki←research/chunks/`, `docs←docs/` — and frames design-doc notes with `source: labs/obdlab/docs/<note>`.
   No dependency on the now-empty `wiki/` folder; the "framed note not found: OBDLab_KG_Wiki" warning is gone.
   Dry-run default + idempotent preserved.
5. **Plan §2 corrected:** design docs are **not yet graphified** (the `graphify-out/manifest.json` ingest set
   is `research/chunks/**` + `vocabulary.py`, not the design docs); the docs tier (`graph/v2_docs/`) is
   produced by **TODO-4**, which gates the docs-tier vault copy.
6. **No `graph.json` re-extraction; `research/chunks/` not moved; `graphify-out/manifest.json` untouched.**

### Context ###

Files carrying the stale `wiki/`-for-design-docs assumption (from `grep`):

- `_skills/graph/4dlab-vault/assets/vault-map.obdlab.yaml` — lines ~20, 28, 29, 40, 97 (HLD/LLD/DLD refs);
  the `OBDLab_KG_Wiki.md` frame (~78–89) and `OBDlab.md` frame (~91–99).
- `Vault/VAULT_IMPLEMENTATION_PLAN.md` — §2 (line ~53 "live inside labs/obdlab/wiki/"; the "already
  graphified" claim), §3 (line ~96 "copy of labs/obdlab/wiki/"), §4 (line ~128 `source:` example).
- `_skills/graph/4dlab-vault/scripts/build_lab_vault.py` — lines ~114, 118, 140–142 (single `wiki_src` copy),
  146–157 (`source: labs/<lab>/wiki/<note>`).
- `_skills/graph/4dlab-vault/reference/frontmatter-schema.md` (~23), `obsidian-cli-optional.md` (~29),
  `obsidian-md-conventions.md` (~11, 36) — `source:` examples.

Leave untouched (historical/done, not this task's mess): `T-OBDV2-7/9/10/11` progress notes' file:// links;
`SWEEP_MANIFEST.md`; `graphify-out/manifest.json` (extraction provenance — re-graphify is forbidden).

### Deliverables ###

1. `_skills/graph/4dlab-vault/assets/vault-map.obdlab.yaml` — design-doc paths → `docs/`; drop KG-wiki + OBDlab frames.
2. `_skills/graph/4dlab-vault/scripts/build_lab_vault.py` — per-tier source mapping (4 tiers). **(builder)**
3. `_skills/graph/4dlab-vault/SKILL.md` + `reference/*.md` — convention + `source:` examples → `docs/`.
4. `Vault/VAULT_IMPLEMENTATION_PLAN.md` — §2/§3/§4 corrected to the 4-tier table; §2 "already graphified" fixed.

### Files to touch ###

- `_skills/graph/4dlab-vault/assets/vault-map.obdlab.yaml`
- `_skills/graph/4dlab-vault/scripts/build_lab_vault.py`
- `_skills/graph/4dlab-vault/SKILL.md`
- `_skills/graph/4dlab-vault/reference/frontmatter-schema.md`
- `_skills/graph/4dlab-vault/reference/obsidian-cli-optional.md`
- `_skills/graph/4dlab-vault/reference/obsidian-md-conventions.md`
- `Vault/VAULT_IMPLEMENTATION_PLAN.md`

### Out of scope ###

- **Docs-tier graphify** (`graph/v2_docs/`) — that is TODO-4 (needs the doc-prep skill); this task only repoints
  references and the build, and records that the docs-tier copy is gated on TODO-4.
- **Archiving `OBDlab.md`** (the file) — handoff TODO-3; here we only drop its vault frame.
- **Moving `research/chunks/`** or re-running graphify — forbidden; the wiki piece stays canonical at source.
- Running the vault build; other labs' maps; `T-VAULT-VOCAB-1` (separate, the `_vocabulary/` tier).
- Surgical rule: every changed line is a path/convention correction. Other drift → plan §8 follow-ups.

### Verification (build session — vault-tooling lane) ###

```bash
cd <repo>/4DLabV2
# 1) no design-doc reference still points at wiki/
grep -rn 'obdlab/wiki/' Vault/ _skills/graph/4dlab-vault/ \
  | grep -E 'HLD|DLD|LLD|PRD|ADR|BDD' && { echo "FAIL design-doc still at wiki/"; exit 1; } || echo "OK no design-doc wiki refs"
# 2) KG-wiki + OBDlab frames gone from the map
grep -qE 'OBDLab_KG_Wiki|^\s*OBDlab\.md:' _skills/graph/4dlab-vault/assets/vault-map.obdlab.yaml \
  && { echo "FAIL stale frame remains"; exit 1; } || echo "OK frames dropped"
# 3) build dry-run resolves all 4 tier sources, no missing-note warning
python3.14 _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab obdlab --dry-run \
  | tee /tmp/vb.txt; grep -qi 'not found\|missing' /tmp/vb.txt && { echo "FAIL tier/source unresolved"; exit 1; } || echo "OK tiers resolve"
# 4) graph provenance untouched
git diff --name-only -- 'labs/obdlab/graphify-out/' 'labs/obdlab/research/chunks/' \
  && echo "(expect empty — no graph/corpus change)"
```

All checks pass; design-doc tier sources from `docs/`, wiki tier from `research/chunks/`, no re-extraction.

### Progress hook ###

`Vault/tasks/progress_notes/T-VAULT-PATHS-1.md` opens with the confirmed `## Plan`; build session fills
`VERIFICATION GATE` + `CODE REVIEW`. Plan §8 row flips to `done` only when both blocks clean and the four
checks pass. Files changed = 7. Verification = "4-tier source mapping wired (code/tests/wiki=research-chunks/
docs); all design-doc refs repointed wiki→docs; KG-wiki + OBDlab frames dropped; build dry-run resolves, no
missing-note warning; graph/corpus untouched".
