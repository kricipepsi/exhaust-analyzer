# T-SYMGRAPH-VAULT — Author `vault-map.symptomlab.yaml`, dry-run, build, install the vault tier

**Status:** pending · **Pack:** symptomlab_graph · **Mode:** LITE / architect-author + vault-tooling lane (no lab inner-loop/gate)
**Blocked by:** T-SYMGRAPH-LLM (needs `v2_wiki` + `v2_docs`); also requires T-SYMGRAPH-4 done (`v2_code` + `v2_tests`)

> **Lane:** vault tooling + architect authoring. The vault is a **read-mostly window** onto the
> finished lab — it **never re-extracts the graph**; it *reads* the four existing `graph.json`
> tiers to inform frontmatter. Build with `scripts/build_lab_vault.py`, always `--dry-run`
> first (idempotent — re-running updates in place, never duplicates).

### Goal ###

Populate `Vault/labs/symptomlab/` with all four tiers (`code/`, `tests/`, `wiki/`, `docs/`)
plus the shared `Vault/_vocabulary/SYMPTOM_VOCABULARY.md`, by authoring the consumer map
`vault-map.symptomlab.yaml` and running `build_lab_vault.py`. Proof of done: the four tiers
render in Obsidian, the three `.base` views resolve, `orphans`/`unresolved` are empty or
explained, and every shipped note has ≥ 1 **human-authored** named consumer.

### Success criteria ###

- `_skills/graph/4dlab-vault/assets/vault-map.symptomlab.yaml` exists, authored by hand —
  module / subsystem / implements / **consumers** / drift_guards per note. **`consumers` is
  never auto-derived from the graph** (that fabricates consumers and breaks signal/noise); an
  empty `consumers` list = that note is not ready to ship.
- `Vault/_vocabulary/SYMPTOM_VOCABULARY.md` built (via the `--vocab` path; add the symptomlab
  vocab to `vault-map.vocabulary.yaml`), joining the existing DTC/GAS/OBD vocab notes.
- `python scripts/build_lab_vault.py --dry-run` (symptomlab) reports the planned copy with no
  errors; the real build then copies `code/`+`tests/` (raw link targets) and `wiki/`+`docs/`
  (notes + injected frontmatter) into `Vault/labs/symptomlab/`.
- The three `.base` views (`modules.base`, `consumers.base`, `drift-guards.base`) render in
  Obsidian; `consumers.base` shows every symptomlab note with ≥ 1 named consumer;
  `orphans`/`unresolved` empty or explained.
- `_meta/PROVENANCE.md` + `System-Map.md` refreshed to include symptomlab.

### Context ###

This converges the four corpus tracks at the vault — the final pipeline phase. By now all four
graphs exist: `v2_code`/`v2_tests` (T-SYMGRAPH-4), `v2_wiki`/`v2_docs` (T-SYMGRAPH-LLM). The
build reads them to inject `module`/`implements`/`drift_guards` frontmatter; the architect
authors `consumers` by hand. Model the map and run on the sibling DNA-family lab DTCLab
(`Vault/tasks/T-DTC-VAULT_build_dtclab_vault.md`,
`_skills/graph/4dlab-vault/assets/vault-map.dtclab.yaml`).

**`SYMPTOM_VOCABULARY.md` handling:** it was excluded from doc-prep (T-SYMGRAPH-DOCPREP) on
purpose — it belongs in the cross-lab `_vocabulary/` tier, not the docs graph. This task is
where it lands, via `--vocab`.

**Load skills:** `_skills\graph\4dlab-vault\SKILL.md` — read end-to-end first (Phase-0
eligibility gate, the 6-step build, the `.base` install). Then read the DTCLab vault-map asset
as the template.

**READ-NARROW:** read the DTCLab vault-map + the DTC-VAULT task for shape; read the four
symptomlab `GRAPH_REPORT.md` summaries (not the `graph.json` blobs) to source `implements`/
`drift_guards`; author `consumers` from the design→code→test knowledge, not the graph.

### Consumer (signal/noise) ###

**The `consumers` field IS the signal/noise gate.** Each framed SymptomLab note ships only with
a **named, existing** downstream consumer — a code path, a sibling design doc, or a COMLab
analytic. The three `.base` views are the live readers: `modules.base` (groups `lab`→`module`),
`consumers.base` (the audit — every note must have ≥ 1 named consumer), `drift-guards.base`
(coverage). **Code path:** `scripts/build_lab_vault.py` reads the four `graph/v2_*/graph.json`
tiers + `vault-map.symptomlab.yaml` to derive frontmatter; the `.base` views query that
frontmatter in Obsidian. The parked-prior content is **not** pulled in here — it lives in the
COMLab proposals registry (`labs/comlab/comlab/config/proposals/entries.yaml`, entries
COMLab-A/B + the prior/chemistry entries added in T-SYMGRAPH-WIKI-AUTHOR) and ships only when
COMLab fusion consumes it (proposed→pinned→graduated).

> **Reference-only-note caveat (resolved):** the old `00_index.md` shipped with no consumer
> because it was reference-only. After T-SYMGRAPH-WIKI-AUTHOR it is a routing index over real
> notes that *do* have consumers, so it ships with consumer = "wiki navigation / vault index".
> If any live wiki note still lands with an empty `consumers` list at dry-run, STOP — it is not
> ready, route it back to T-SYMGRAPH-WIKI-AUTHOR.

### Deliverables ###

1. `_skills/graph/4dlab-vault/assets/vault-map.symptomlab.yaml` (CREATE) — the hand-authored
   consumer map.
2. `_skills/graph/4dlab-vault/assets/vault-map.vocabulary.yaml` (MODIFY) — add the symptomlab
   vocab entry.
3. `Vault/labs/symptomlab/{code,tests,wiki,docs}/` (CREATE — build output).
4. `Vault/_vocabulary/SYMPTOM_VOCABULARY.md` (CREATE — `--vocab` output).
5. `Vault/_bases/` (the three `.base` views, if not already lab-agnostic), `Vault/System-Map.md`
   + `Vault/_meta/PROVENANCE.md` (MODIFY — refresh to include symptomlab).
6. `planning/symptomlab_graph/tasks/progress_notes/T-SYMGRAPH-VAULT.md` (CREATE) — `## Plan` +
   `--dry-run` output + build output + the Obsidian render confirmation (3 bases + empty/explained
   orphans).

### Files to touch ###

- `_skills/graph/4dlab-vault/assets/vault-map.symptomlab.yaml` (CREATE)
- `_skills/graph/4dlab-vault/assets/vault-map.vocabulary.yaml` (MODIFY)
- `Vault/labs/symptomlab/` (CREATE — build output)
- `Vault/_vocabulary/SYMPTOM_VOCABULARY.md` (CREATE)
- `Vault/System-Map.md`, `Vault/_meta/PROVENANCE.md` (MODIFY)
- progress note (CREATE)

### Out of scope ###

No graph re-extraction — the vault only reads existing `graph.json`. No auto-derivation of
`consumers` (signal/noise breach). No copy of `graph.json`/`graphify-out/`, caches, or `tasks/`
into the vault (graph-awareness comes from injected frontmatter). No promotion of the
COMLab-proposal prior/chemistry content into the vault. No edits to other labs' vault tiers or
maps.

### Verification ###

```bash
cd C:\Users\muto\claude\4DApp\4DLab\4DLabV2

# Confirm all four graph tiers exist before building (vault never extracts)
for t in v2_code v2_tests v2_wiki v2_docs; do test -e labs/symptomlab/graph/$t/graph.json && echo "OK: $t" || echo "MISSING: $t"; done

# Dry-run first (idempotent), then build (exact CLI per 4dlab-vault/SKILL.md)
python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab symptomlab --dry-run
python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab symptomlab
python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --vocab     # SYMPTOM_VOCABULARY

# Signal/noise: no shipped note may have an empty consumers list
grep -rn "consumers: \[\]" _skills/graph/4dlab-vault/assets/vault-map.symptomlab.yaml ; echo "exit=$? (1 = clean)"

# Confirm graph.json was NOT copied into the vault
test ! -e Vault/labs/symptomlab/graph.json && echo "OK: no graph.json in vault"
ls Vault/labs/symptomlab/   # expect: code/ tests/ wiki/ docs/
```

Then open in Obsidian: confirm the three `.base` views render and `orphans`/`unresolved` are
empty or explained. Paste dry-run + build output + the render confirmation into the progress
note.

### Progress hook ###

PROGRESS `T-SYMGRAPH-VAULT`: Status=done, Files=vault-map + 4 tiers + vocab,
Verification="4 tiers copied, 3 bases render, no empty consumers, no graph.json in vault".
