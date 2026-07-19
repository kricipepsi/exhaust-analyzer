---
node_type: task
task_id: T-VAULT-VOCAB-1
status: pending
queue: next
pack: VAULT · **Mode:** STRICT
lab: obdlab
mode: strict
blocked_by:
- T-SEM-5
consumers:
- build_lab_vault.py — vault frontmatter derivation
- consumers.base — signal/noise audit view
- COMLab analytics / fault-atlas routing
- /check-impact command
- /graph-find command
implements:
- vault-map.vocabulary.yaml
tags:
- task
- vault
- obdlab
---

# T-VAULT-VOCAB-1 — Standalone OBD vocabulary note in the vault (`_vocabulary/`)

**Status:** `pending (next)` · **Pack:** VAULT · **Mode:** STRICT (vault-tooling lane — see role note)
**Origin:** `Vault/VAULT_IMPLEMENTATION_PLAN.md` §2–§4, §8 + owner request 2026-06-10 · **Blocked by:** T-SEM-5 (`done`)
**Consumer (signal/noise):** **Adds no new frontmatter field** — reuses the §4 node schema, every field of which
already has a named consumer (the three `.base` views + `/check-impact` / `/graph-find`; see plan §4 table).
The **note itself** is consumed by: (a) the `consumers.base` signal/noise audit view (it carries ≥1 named
consumer), (b) the obdlab lab-landing note via a wikilink, (c) any vault query for OBD enum semantics. The
enums it documents have live code consumers — `vocabulary.py` → COMLab `fault_atlas_router`/analytics +
`T-COMV2-O2OFFSET-1`, DTCLab `freeze_frame_extractor` — so no proposal is needed.

### Role note (vault-tooling lane) ###

Per plan §5, `build_lab_vault.py` is **vault tooling, not lab diagnostic code**, and is **not** subject to the
lab inner-loop / 6-phase gate. This task is authored by the architect; a **build session** executes it (edits
the script, runs it dry-run-first, fills the gate blocks). No `gaslab/`/`obdlab/` lab code is touched.

### Goal ###

Give the vault a **single, standalone, graph-aware OBD vocabulary note** — the human-readable enum reference
(thresholds, narrowband bands, misfire-signature math) that the code AST cannot carry — without re-introducing
the triplication T-SEM-5 just removed. The note lives in a new shared `Vault/_vocabulary/` area (owner
decision 2026-06-10), is **sourced from the canonical `labs/semantic/vocabul/OBD_VOCABULARY.md`**, carries §4
frontmatter with named consumers, and is wikilinked from the obdlab landing note. The vault build is extended
to populate `_vocabulary/` idempotently.

### Success criteria ###

1. **`Vault/_vocabulary/OBD_VOCABULARY.md` exists**, its **body is byte-identical to the canonical**
   `labs/semantic/vocabul/OBD_VOCABULARY.md` (md5 of the body, excluding injected frontmatter, equals the
   canonical's — currently `B14AFE09…`). Single-source preserved: the obdlab/comlab `.md` copies are **not**
   the source and are **not** duplicated into the vault.
2. The note carries valid §4 frontmatter:
   - `node_type: wiki` (the enum is fixed — no new value invented)
   - `lab: obdlab` · `module: semantic-vocabulary` · `subsystem: obd-enums`
     (anchors it to the in-vault obdlab group in `modules.base`; Bases filter on frontmatter, not folder)
   - `implements: ["labs/obdlab/code/schemas/vocabulary.py"]`
   - `consumers:` (architect-named, ≥1, non-empty):
     - `"comlab: fault_atlas_router (fuel_system_status routing)"`
     - `"comlab: T-COMV2-O2OFFSET-1 (O2FailureMode.WIDEBAND_OFFSET_CANDIDATE)"`
     - `"dtclab: freeze_frame_extractor (FuelSystemStatus open-loop derivation)"`
   - `drift_guards: ["labs/obdlab/tests/unit/test_vocabulary.py"]`
   - `source: "labs/semantic/vocabul/OBD_VOCABULARY.md"`
   - `tags: [vocabulary, obd, semantic, finished]`
3. The **obdlab lab-landing note** (`Vault/labs/obdlab/_OBDLab.md`, or `System-Map.md` if the landing note
   isn't built yet) contains a **resolving wikilink** to `[[OBD_VOCABULARY]]` — Obsidian shows **no
   unresolved link**.
4. The note appears as a row in **`consumers.base`** with its named consumers, and is visible/grouped in
   **`modules.base`** under obdlab → semantic-vocabulary. All three `.base` views still render.
5. The build is **idempotent and dry-run-safe**: a dedicated path (`build_lab_vault.py --vocab`, or a sibling
   `build_vocabulary.py`) reads an architect-authored `assets/vault-map.vocabulary.yaml`, copies the canonical
   body, injects only the mechanical frontmatter fields, and fills semantic fields from the map. Re-running
   updates in place, never duplicates.
6. `Vault/_meta/PROVENANCE.md` records the copy: source path, date (2026-06-10), and the canonical body md5.
7. **No `graph.json` re-extraction** is run (plan §7, CLAUDE.md HARD RULE).

### Context ###

Plan §2 settled that `vocabulary.py` is already graphified and rides in with the code copy — but that is the
*code* enum. The `.md` vocab carries domain prose the AST does not: narrowband V thresholds, the
`O₂ rise ≈ 21% ÷ N cylinders` misfire-signature math, per-§ diagnostic narrative. The vault-map currently
references `OBD_VOCABULARY.md` only as a **consumer string** ("comlab: OBD vocabulary anchor"), never as a
note — so it has no vault home today. T-SEM-5 (`done`) reconciled the canonical copy to shipped code and made
all three live `.md` copies md5-identical, so the canonical is now safe to source from.

`_vocabulary/` is a new shared top-level area (sibling of `_bases/`, `_meta/`), chosen over a per-lab
placement so the single cross-lab vocab authority does not sit inside one lab's folder, and so GAS/DTC vocab
notes can join it when those labs land (not in this task — see Out of scope).

### Deliverables ###

1. `Vault/_vocabulary/OBD_VOCABULARY.md` — canonical body + injected §4 frontmatter (above).
2. `_skills/graph/4dlab-vault/assets/vault-map.vocabulary.yaml` — architect-authored consumer map for the
   shared vocab area (OBD entry now; GAS/DTC stubs commented for later).
3. `_skills/graph/4dlab-vault/scripts/build_lab_vault.py` — add the idempotent `_vocabulary/` build path
   (`--vocab` flag or `build_vocabulary_area()`), dry-run default. **(builder edits/runs; vault-tooling lane.)**
4. `_skills/graph/4dlab-vault/SKILL.md` — document the `_vocabulary/` build step in §6 procedure.
5. `Vault/labs/obdlab/_OBDLab.md` **or** `Vault/System-Map.md` — add the `[[OBD_VOCABULARY]]` wikilink.
6. `Vault/_meta/PROVENANCE.md` — provenance row.
7. `Vault/VAULT_IMPLEMENTATION_PLAN.md` — §3 layout adds `_vocabulary/`; §4 notes the vocab note reuses
   `node_type: wiki`.

### Files to touch ###

- `Vault/_vocabulary/OBD_VOCABULARY.md` (new)
- `Vault/_meta/PROVENANCE.md`
- `Vault/labs/obdlab/_OBDLab.md` or `Vault/System-Map.md`
- `Vault/VAULT_IMPLEMENTATION_PLAN.md`
- `_skills/graph/4dlab-vault/assets/vault-map.vocabulary.yaml` (new)
- `_skills/graph/4dlab-vault/scripts/build_lab_vault.py`
- `_skills/graph/4dlab-vault/SKILL.md`

### Out of scope ###

- **GAS_VOCABULARY / DTC_VOCABULARY / SEMANTIC_CONTRACT vault notes** — add when GASLab/DTCLab land in the
  vault. Staging them now is speculative (only obdlab is finished/copied). `vault-map.vocabulary.yaml` may
  carry **commented** stubs only.
- **The docs/wiki path mismatch** (vault-map points at `labs/obdlab/wiki/HLD…` but the design docs + vocab
  live in `labs/obdlab/docs/`) — pre-existing defect, **flag as follow-up**, do not fix here. This task is
  robust to it because it sources vocab from `semantic/vocabul/`, not from any obdlab path.
- **Collapsing the lab-local `.md` vocab copies** — they stay (owner decision under T-SEM-5: keep all copies
  synced; comlab reworked later). This task adds the vault *representation* only.
- Any `node_type` enum change; any `graph.json` re-extraction; any lab code/test edit.
- Running the full lab vault build (`build_lab_vault.py --lab obdlab`) — that is the separate populate step
  (plan §8); this task only adds and exercises the `_vocabulary/` path.

### Verification (build session — vault-tooling lane, not lab inner-loop) ###

```bash
cd <repo>/4DLabV2
# 1) build dry-run first, then real
python3.14 _skills/graph/4dlab-vault/scripts/build_lab_vault.py --vocab --dry-run
python3.14 _skills/graph/4dlab-vault/scripts/build_lab_vault.py --vocab
# 2) single-source: vault body == canonical body (strip injected frontmatter, compare md5)
python3.14 - <<'PY'
import re,hashlib,pathlib
def body(p):
    t=pathlib.Path(p).read_text(encoding='utf-8')
    return re.sub(r'^---\n.*?\n---\n','',t,count=1,flags=re.S)
a=hashlib.md5(body('Vault/_vocabulary/OBD_VOCABULARY.md').encode()).hexdigest()
b=hashlib.md5(pathlib.Path('labs/semantic/vocabul/OBD_VOCABULARY.md').read_text(encoding='utf-8').encode()).hexdigest()
print('BODY-MATCH' if a==b else f'FAIL body diverges {a} {b}')
PY
# 3) frontmatter valid + consumers non-empty
python3.14 - <<'PY'
import yaml,pathlib,re
t=pathlib.Path('Vault/_vocabulary/OBD_VOCABULARY.md').read_text(encoding='utf-8')
fm=yaml.safe_load(re.match(r'---\n(.*?)\n---',t,re.S).group(1))
assert fm['node_type']=='wiki' and fm['consumers'], fm
print('FM-OK', fm['node_type'], len(fm['consumers']),'consumers')
PY
# 4) idempotent: re-run, expect no second file / no diff
python3.14 _skills/graph/4dlab-vault/scripts/build_lab_vault.py --vocab && echo "OK idempotent (in-place)"
```

Then open `Vault/` in Obsidian: confirm `[[OBD_VOCABULARY]]` resolves from the obdlab landing note, the note
shows in `consumers.base` with its named consumers, and `unresolved`/`orphans` are empty or explained.

### Progress hook ###

`Vault/tasks/progress_notes/T-VAULT-VOCAB-1.md` opens with the confirmed `## Plan`, then the build session
fills `VERIFICATION GATE` + `CODE REVIEW`. The plan §8 follow-ups row flips to `done` only when both blocks are
clean and the four checks above pass. Files changed = 7. Verification = "standalone `_vocabulary/OBD_VOCABULARY.md`
built from canonical (body md5 match), §4 frontmatter + named consumers, idempotent `--vocab` path, landing-note
wikilink resolves, provenance recorded; no graph re-extraction".
