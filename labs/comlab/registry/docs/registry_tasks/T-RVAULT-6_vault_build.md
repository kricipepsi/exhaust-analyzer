### Goal ###

Copy the registry into the vault as a code+tests+docs corpus under
`Vault/labs/comlab/registry/`, with consumer-aware frontmatter. Two parts: (a) author
`assets/vault-map.registry.yaml` (the architect-named consumer map), (b) register the
registry as a keyed corpus in `build_lab_vault.py` (it is a sub-package, not a top-level
lab — see Context), then `--dry-run` → build → confirm. Done when the registry tier
renders in Obsidian with the three `.base` views populated and `orphans`/`unresolved`
empty or explained.

### Success criteria ###

- `_skills/graph/4dlab-vault/assets/vault-map.registry.yaml` exists; every framed note
  has a **non-empty, hand-authored `consumers`** list naming a real code path (empty
  `consumers` = not shippable, copy as plain).
- `build_lab_vault.py` resolves a `registry` corpus (src `labs/comlab/registry/`, dest
  `Vault/labs/comlab/registry/`, tiers code/tests/docs, `required_graph_tiers =
  (v2_code, v2_tests, v2_docs)`), proven by `--dry-run` printing the intended copies
  with **no missing-source / missing-graph errors**.
- `python3 _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab registry --repo
  /agent_workspace` (after dry-run) creates `Vault/labs/comlab/registry/{code,tests,
  docs}/` with injected frontmatter; re-running is idempotent (no duplicates).
- `build_lab_vault.py`'s own test (`tests/test_build_lab_vault.py`) stays green.
- `System-Map.md` + `_meta/PROVENANCE.md` updated; the three `Vault/_bases/*.base`
  views render the registry notes; orphan/unresolved lists empty or explained.

### Context ###

Phase 4 from `planning/LAB_TO_VAULT_PIPELINE_GUIDE.md §6`. The vault is a read-mostly
window: it never re-extracts the graph, it *reads* the three `graph.json` (v2_code,
v2_tests, v2_docs from T-RVAULT-4/5) to inform frontmatter.

**The sub-package problem (architect probe 2026-06-28 — pin, do not rediscover):**
`build_lab_vault.py` keys source roots by `--lab` and assumes the lab layout
`labs/<lab>/<lab>/` for code. The registry is `labs/comlab/registry/` — a COMLab
sub-package, not a top-level lab. The script already has the precedent for a
non-`labs/<lab>` corpus: the **`apps/ui` doc-only keyed entry** (`src_root: apps/ui`,
explicit `docs_notes` list, custom `required_graph_tiers`). **Recommended approach:**
add a sibling keyed entry `registry` to that same config block — `src_root:
labs/comlab/registry`, code tier = the package `.py` + `rules/*.json`, tests tier =
`registry/tests/`, docs tier = the explicit list from T-RVAULT-1's
`VAULT_DOCS_MANIFEST.md`, `required_graph_tiers = (v2_code, v2_tests, v2_docs)`, and a
**`vault_dest` of `labs/comlab/registry`** so it nests under COMLab rather than
becoming a sibling lab. This is vault *tooling* (the script header states it is "NOT
lab diagnostic code, and not subject to the lab inner-loop/gates"), so it does not
touch the registry package and does not need the registry test suite.

> **OPEN DECISION for this task (surface, don't silently pick):** destination nesting.
> The recommendation above nests the registry at `Vault/labs/comlab/registry/`
> (registry is conceptually part of COMLab — COMLab reads its artefacts). The
> alternative is a sibling `Vault/labs/registry/`. If the sibling layout is wanted,
> the `vault_dest` and `System-Map` wiring change accordingly. Confirm with the owner
> before building if unsure — this is the one genuine fork in the task.

**`consumers` is human-authored, never auto-derived** (`§6`). Author each registry
note's consumer as its real reader: rule families and `schema_v2` are consumed by
COMLab at integration time via `integration_shim.py` / `shim/payload_mirrors.py` →
`fault_atlas_router.py` (behind `USE_V2_REGISTRY`). The direction is one-way (registry
never imports COMLab), so consumers are COMLab-internal readers of registry artefacts,
mirroring how `vault-map.comlab.yaml` frames notes. Vocabulary is intentionally NOT
contributed (owner decision 2026-06-28): registry enums mirror GAS/DTC vocab, which
already have `_vocabulary/` homes — do not run `--vocab` for the registry.

Load skills: `_skills/graph/4dlab-vault` (build steps + vault-map authoring).

### Consumer (signal/noise) ###

N/A — no new lab field/enum/fault. This task adds vault frontmatter + one tooling
config entry. The frontmatter's `consumers`/`drift_guards` are themselves the
signal/noise contract; each must name a real reader/test or the note ships as plain.

### Deliverables ###

1. `_skills/graph/4dlab-vault/assets/vault-map.registry.yaml` — consumer map.
2. `_skills/graph/4dlab-vault/scripts/build_lab_vault.py` — `registry` keyed corpus
   entry (MODIFY — config block only).
3. `Vault/labs/comlab/registry/{code,tests,docs}/` — built tier with frontmatter.
4. `Vault/System-Map.md` + `Vault/_meta/PROVENANCE.md` — registry rows.

### Files to touch ###

- `_skills/graph/4dlab-vault/assets/vault-map.registry.yaml` (CREATE)
- `_skills/graph/4dlab-vault/scripts/build_lab_vault.py` (MODIFY — corpus config only)
- `Vault/labs/comlab/registry/**` (CREATE — via build)
- `Vault/System-Map.md`, `Vault/_meta/PROVENANCE.md` (MODIFY)

### Out of scope ###

Do NOT re-extract or rebuild any graph — the vault only reads existing `graph.json`.
Do NOT auto-fill `consumers` from the graph. Do NOT run `--vocab` / add a registry
vocabulary (owner-declined). Do NOT change `build_lab_vault.py` beyond the corpus
config entry needed to resolve the registry (no refactor of the copy/ frontmatter
engine). Do NOT copy `graph.json`, caches, `tasks/`, or `_registry_skills/` into the
vault. Always `--dry-run` before the real build.

GRAPH GUARDRAIL (standing): the vault build reads `graph.json`; it does NOT run
graphify and does NOT modify any graph dir.

### Verification ###

```bash
cd /agent_workspace
# vault-map authored, consumers non-empty
test -f _skills/graph/4dlab-vault/assets/vault-map.registry.yaml && echo "map present"

# tooling test still green
python3 -m pytest _skills/graph/4dlab-vault/tests/test_build_lab_vault.py -q

# dry-run first (writes nothing)
python3 _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab registry --repo /agent_workspace --dry-run

# real build, then idempotency (second run = no new writes)
python3 _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab registry --repo /agent_workspace
python3 _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab registry --repo /agent_workspace --dry-run | grep -i "would write\|copy" || echo "idempotent"

# tiers exist
ls Vault/labs/comlab/registry/{code,tests,docs}
```

All steps must pass; then open the vault in Obsidian and confirm the three Bases render
the registry notes and orphans/unresolved are empty or explained.

### Progress hook ###

PROGRESS.md `T-RVAULT-6`: Status=done, Files changed={COUNT}, Verification="registry mirrored to Vault/labs/comlab/registry; bases render; idempotent"
