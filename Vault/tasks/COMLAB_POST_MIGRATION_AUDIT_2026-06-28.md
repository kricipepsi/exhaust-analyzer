# COMLab — Post-Migration Audit (tasks · lab · vault)

**Date:** 2026-06-28 · **Author:** architect (Cowork) · **Scope:** `labs/comlab`, `Vault/labs/comlab`, `Vault/tasks/*COM*`
**Trigger:** COMLab vault pack closed `done`, but its last three tasks (`GRAPH-AST`, `PATHS-1`, `VAULT`) ran **after** the Windows→Linux migration. This audit checks whether that introduced drift.
**Method:** independent re-verification against the working tree + git, not a re-read of the gate notes.

---

## Verdict

The **work product is sound and consistent** — the vault tier is fully built, the source matches the vault copy, and there is **no Windows/`4DLabV2/`/`.sandbox-py` residue** anywhere in COMLab code, tests, wiki, docs, the vault build script, or the COMLab skills.

The "trouble" is **git hygiene, not content**: the migration-era tasks left their artifacts in the **working tree, uncommitted**, and committed their *dependents* on top. At `HEAD` the committed COMLab vault tier **cannot be reproduced from a clean checkout** — its required graph tiers and shared `.base`/vocabulary dependencies are untracked. Nothing is lost on this machine; the risk is reproducibility and a clone/CI/another-coder pulling an inconsistent tree.

**One action closes it:** commit the GRAPH-AST artifacts + the shared vault infra. No code or vault rebuild needed.

---

## Verified solid (re-checked, not just claimed)

| Check | Result |
|---|---|
| Vault tier present | `Vault/labs/comlab/{code,tests,wiki,docs}` + `_comlab.md` landing note — full mirror (21 code modules, 15 wiki chunks, 6 design docs + 11 ADRs + Vocabulary, tests tree) |
| Source ↔ vault parity | The 4 edited `tests/**/__init__.py` docstrings are present **identically** in source and in the vault copy — the build captured post-edit source |
| Graph tiers built | `graph/v2_code/` and `graph/v2_tests/` exist with `{graph.json, GRAPH_REPORT.md, graph.html, cache/}`; no `graphify-out/` residue survives |
| Frozen graph intact | `graph/v1_baseline/` committed and clean (`git status` empty) |
| Path fix live + committed | `build_lab_vault.py` has the `comlab` `LAB_SRC_PATHS` entry (L81) + provenance waiver branch (L364); committed as `1884e57` |
| Tests | `pytest --collect-only` → **513 collected** (matches the 509-pass + 4-skip baseline after GRAPH-AST's 4 docstring additions) |
| System-Map / landing | COMLab row in `Vault/System-Map.md`; `_comlab.md` frontmatter well-formed |
| Residue scan | `C:\`, `4DLabV2/`, `.sandbox-py` → **zero hits** in comlab code/tests/wiki/docs, the build script, and `_comlab_skills/` |

---

## Findings — git-integrity gaps (the actual post-migration trouble)

### F1 — New graph tiers are uncommitted, but committed work depends on them · **HIGH**

`labs/comlab/graph/v2_code/` and `graph/v2_tests/` are **untracked** (`git status` → `??`) and appear in **no commit**:

```
git log --oneline -- labs/comlab/graph/v2_code   → (empty: never committed)
```

They are **not** gitignored (only `graphify-out/` is). Yet two committed artifacts depend on them:
- `PATHS-1` (`1884e57`) declares `required_graph_tiers: ("v2_code","v2_tests")` for comlab.
- `VAULT` (`d37da5c`) built the tier against those graphs and records them in System-Map/PROVENANCE.

**Consequence:** a clean checkout of `HEAD` has a COMLab vault config that requires two graph tiers that don't exist in the repo → a rebuild aborts; the provenance points at absent inputs. The GRAPH-AST progress note itself flags this ("`??` … never committed").

### F2 — T-COM-GRAPH-AST committed nothing; its dependents are committed on top · **HIGH**

The commit chain is **out of dependency order**. `PATHS-1` and `VAULT` are committed (`1884e57`, `d37da5c`), but there is **no GRAPH-AST commit**. Its entire output sits in the working tree:
- `labs/comlab/graph/v2_code/`, `v2_tests/` — untracked (F1)
- `labs/comlab/tests/__init__.py`, `tests/e2e/__init__.py`, `tests/fixtures/__init__.py`, `tests/unit/__init__.py` — **modified, uncommitted** (the inert one-line docstrings GRAPH-AST added to de-isolate the 4 package markers)
- `Vault/tasks/T-COM-GRAPH-AST_graphify_code_and_tests.md` — modified, uncommitted

### F3 — COMLab vault tier committed against untracked shared infra · **MEDIUM**

`Vault/labs/comlab/` **is** committed (in `d37da5c`), but everything it transcludes/links is **untracked**:

```
?? Vault/_bases/            (modules.base, consumers.base, drift-guards.base — the .base files _comlab.md embeds)
?? Vault/_vocabulary/       (OBD_VOCABULARY, GAS_VOCABULARY, … the landing note links; SEMANTIC_CONTRACT this task added)
?? Vault/labs/{dnalab,dtclab,gaslab,obdlab,symptomlab,vinlab}/   (all 6 sibling tiers)
```

So in a clean checkout the committed `_comlab.md` would dangle on `![[modules.base]]`, `![[consumers.base]]`, `![[drift-guards.base]]` and `[[OBD_VOCABULARY]]`. This is a partial-commit: one lab tier shipped to git ahead of the shared scaffolding it sits on.

### F4 — Broader repo mid-migration, largely uncommitted · **LOW (context, not COMLab-specific)**

`git status` shows the migration itself is uncommitted: `agents.md` deleted vs `AGENTS.md` untracked (the case rename CLAUDE.md mandates), plus many untracked root migration docs (`4DLab_CLAUDE.md`, `HANDOFF_*`, `CRANK_UP_*`) and most `Vault/tasks/progress_notes/*`. Not a COMLab defect, but it's the soil F1–F3 grew in: tasks ran green and were left unstaged.

---

## Open follow-ups (pre-existing, correctly recorded — not regressions)

These were known and deferred before this audit; listing so the picture is complete.

1. **Wiki SAI residual** — `wiki/03_vehicle_dna_pruning.md:52` (`ERR-LC-007`, "SAI stuck on"). Confirm it's an in-era residual (SAI fitted Euro 2–3), not a 2010–2020 perk leak. One-line architect wiki fix if it leaks. (Readiness audit + START_HERE §5.)
2. **Registry** — `labs/comlab/registry/` is out of pack scope, blocked on the F1 registry-consolidation owner decision; gets its own vault pack. Its `REGISTRY_START_HERE.md` still carries Windows-era bootstrap (banner added, rewrite pending on-mount).
3. **Prose-graph lift** — `T-COM-GRAPH-LLM` waived/liftable if a Pass-3 LLM backend is confirmed on the coder host (symptomlab precedent).
4. **Two behaviour-neutral `Base root: C:\…` lines** remain in `_skills/graph/4dlab-code-prep/SKILL.md:76` and `4dlab-doc-prep/SKILL.md:97` (reference-only; per `WINDOWS_RESIDUE_FOLLOWUPS.md`, fix on the next graph-skills pass).

---

## Recommended remediation (smallest diff that makes `HEAD` reproducible)

Single staging pass, no rebuild — success criterion is **"clean checkout reproduces the committed vault"**:

1. **Commit GRAPH-AST as its own commit, before what already sits on top is relied on:**
   - `labs/comlab/graph/v2_code/`, `labs/comlab/graph/v2_tests/` (the built tiers — F1)
   - the 4 `tests/**/__init__.py` docstring edits (F2)
   - `Vault/tasks/T-COM-GRAPH-AST_*.md`
   *(Confirm graph `cache/` dirs are wanted in-tree or add a scoped ignore — match whatever `v1_baseline` does.)*
2. **Commit the shared vault scaffolding** `Vault/_bases/` and `Vault/_vocabulary/` so the already-committed `_comlab.md` resolves (F3). Decide deliberately whether the 6 sibling `Vault/labs/*` tiers ship now or stay staged — but `_bases`/`_vocabulary` must land since comlab is already committed against them.
3. **Verify:** `git stash -u` → `build_lab_vault.py --lab comlab --dry-run` resolves (graphs found, no abort) and the `.base`/vocabulary links resolve → `git stash pop`. Or clone to a temp dir and dry-run.

No COMLab source, graph, or vault **content** needs to change — this is purely staging what the migration-era sessions produced but never committed.

---

## Evidence index

- `git status --porcelain` — F1/F2/F3/F4 working-tree state
- `git log --oneline` — `d37da5c`(VAULT) `1884e57`(PATHS-1) present; no GRAPH-AST commit; `git log -- …/v2_code` empty
- `grep -rI 'C:\\|4DLabV2/|.sandbox-py' labs/comlab/{comlab,tests,wiki,docs}` + build script + `_comlab_skills` → 0 hits
- `pytest --collect-only` → 513 · `build_lab_vault.py` L81/L364 · `Vault/labs/comlab/**` file inventory
- Gate notes cross-checked: `progress_notes/T-COM-{GRAPH-AST,PATHS-1,VAULT}.md`, `COMLAB_VAULT_READINESS_AUDIT_2026-06-26.md`
