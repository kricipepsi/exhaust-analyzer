# T-SYMGRAPH-VAULT — progress note

## Plan

Task picked: **T-SYMGRAPH-VAULT** — first `pending` ledger row, sole blocker
`T-SYMGRAPH-LLM` is `done`; all four graph tiers (`v2_code`, `v2_tests`, `v2_wiki`,
`v2_docs`) confirmed present under `labs/symptomlab/graph/`.

**Goal:** populate `Vault/labs/symptomlab/{code,tests,wiki,docs}/` + the shared
`Vault/_vocabulary/SYMPTOM_VOCABULARY.md` by authoring `vault-map.symptomlab.yaml`
(hand-authored consumers) and running `build_lab_vault.py`.

**Files to touch:**
1. `_skills/graph/4dlab-vault/assets/vault-map.symptomlab.yaml` (CREATE) — framed:
   4 design docs (PRD/HLD/LLD/DLD) + 5 wiki notes (00_index, 01_symptom_catalog,
   02_environmental_axes, 03_symptom_dna_payload, 04_catalog_changelog); `plain:`:
   ADR, BDD, SYMPTOM_VOCABULARY.
2. `_skills/graph/4dlab-vault/assets/vault-map.vocabulary.yaml` (MODIFY) — add the
   `SYMPTOM_VOCABULARY.md` entry.
3. **DEVIATION (unplanned, flagged FU-5):** `_skills/graph/4dlab-vault/scripts/build_lab_vault.py`
   `LAB_SRC_PATHS` — add a `symptomlab` entry (`wiki_subpath: wiki`, all four tiers
   required). The script has entries for obdlab/gaslab/dtclab but **none for
   symptomlab**; without it the build defaults to the OBDLab `research/chunks` layout
   and aborts on eligibility. SymptomLab's wiki is at `wiki/` exactly like
   gaslab/dtclab. There is no `T-SYMGRAPH-PATHS` task (the DTC equivalent owned the
   DTC script edit) — architect gap. The fix is a 4-line registration mirroring the
   existing entries; no logic change.
4. `Vault/System-Map.md` (MODIFY, hand) — add SymptomLab row + `_vocabulary` link +
   landing note. `Vault/_meta/PROVENANCE.md` auto-updated by the script.

**Consumer evidence (live readers, grep-confirmed — proposals excluded):**
- DNALab `labs/dnalab/dnalab/assembly.py` — `from symptomlab import resolve` →
  VehicleDNA Part B.
- DNALab `labs/dnalab/dnalab/models.py` — `SymptomDNA.from_json` → `VehicleDNA.symptom_dna`.
- COMLab `labs/comlab/comlab/core/symptom_router.py` — `route_symptom()` reads
  `environmental_conditions.engine_state` + `occurs_during`.
- SymptomLab internal: `validator.py:SymptomValidator.validate` / `__init__` (21-pair
  invariant), the live reader of `allowed_combinations.yaml`.
- COMLab-A/B/F/G are **proposals** (registry) — NOT framed as live consumers.

**Verification commands I'll run (task block):** four-tier existence loop, `--dry-run`,
build, `--vocab`, `grep "consumers: \[\]"` (expect clean), `test ! -e Vault/labs/symptomlab/graph.json`,
`ls Vault/labs/symptomlab/`. Plus `git status --porcelain labs/symptomlab/graph` to
confirm 0 collateral on graph dirs.

**Guard at risk:** "no collateral on graph dirs" — build only reads `graph/*/graph.json`,
never writes; confirmed by git status post-build.

---

## Verification (LITE) — clean

**1. Four graph tiers present (vault never extracts):**
```
OK: v2_code   OK: v2_tests   OK: v2_wiki   OK: v2_docs
```

**2. Dry-run → build → vocab:** all clean.
- Dry-run: 9 framed notes resolve (PRD c=2, HLD c=4, LLD c=3, DLD c=3, 00_index c=1,
  01_catalog c=2, 02_axes c=2, 03_payload c=3, 04_changelog c=1); 4 tiers planned; no errors.
- Build: 4 tiers copied (code/tests/wiki/docs), 9 notes framed, `_symptomlab.md` landing
  written, 4 `.base` views installed, `## symptomlab` upserted to PROVENANCE.md.
- Vocab: `SYMPTOM_VOCABULARY.md` written (body md5 `D6EEFE3C359A0BF6BDE13D07C410620A`),
  joining OBD/GAS/DTC.

**3. Signal/noise — no empty consumers list:** `grep "consumers: \[\]"` on the map →
`CLEAN: no empty consumers list`. All 9 framed notes in the vault carry an injected
`consumers:` key (verified by regex over `Vault/labs/symptomlab/{wiki,docs}/*.md` → 9/9).

**4. No `graph.json` copied into the vault:** `OK: no graph.json in vault`.
`ls Vault/labs/symptomlab/` → `code/ docs/ tests/ wiki/ _symptomlab.md` (no `graph.json`).

**5. No collateral on graph dirs:** `git status --porcelain labs/symptomlab/graph` → empty
(graph tiers byte-unchanged; build only reads them).

**6. Vault health gate (scriptable proxy for the 3 bases):**
`vault_query.py --vault Vault health` → **WARN, exit 0 (PASS)**:
- `[OK] signal/noise: 58/58 framed notes name a consumer` (was 49 before this task; +9 symptomlab).
- `[OK] coverage: 0 notes implement code with no drift_guard`.
- `[OK] .base views: 4/4 present`.
- Single `[WARN]`: 3 pre-existing cross-ledger `blocked_by` refs (T-OIL-4/5, T-SEM-5) —
  unrelated to this task, present before it.

**7. Idempotency:** 2nd `--dry-run` produced an identical plan, nothing written.

**Obsidian render note:** the three `.base` views (`modules`, `consumers`, `drift-guards`)
are lab-agnostic and already render for OBD/GAS/DTC; SymptomLab's 9 notes carry the same
`lab`/`module`/`node_type`/`consumers` frontmatter, so they appear automatically. The
`vault_query.py health` gate is the scriptable mirror of those three bases (Obsidian CLI is
unreachable from the agent sandbox) and passed. Final visual confirmation in the Obsidian
desktop app is the owner's to do; `orphans`/`unresolved` are empty by the health gate.

## Deviation (FU-5) — build script path registration

`build_lab_vault.py` `LAB_SRC_PATHS` had entries for obdlab/gaslab/dtclab but **none for
symptomlab**. Without one the script defaults to the OBDLab `research/chunks` wiki layout and
aborts on eligibility (SymptomLab's wiki is at `wiki/`, like gaslab/dtclab). For DTCLab a
dedicated `T-DTC-PATHS-1` task owned the equivalent script edit; no `T-SYMGRAPH-PATHS` task
exists and none was listed as a blocker — an architect gap. Added a 4-line entry
(`wiki_subpath: wiki`, all four tiers required) mirroring the gaslab/dtclab entries exactly;
no logic change. Logged as FU-5 for owner review.

## Files delivered

- `_skills/graph/4dlab-vault/assets/vault-map.symptomlab.yaml` (CREATE)
- `_skills/graph/4dlab-vault/assets/vault-map.vocabulary.yaml` (MODIFY — SYMPTOM_VOCABULARY entry)
- `_skills/graph/4dlab-vault/scripts/build_lab_vault.py` (MODIFY — symptomlab LAB_SRC_PATHS entry; FU-5)
- `Vault/labs/symptomlab/{code,tests,wiki,docs}/` + `_symptomlab.md` (CREATE — build output)
- `Vault/_vocabulary/SYMPTOM_VOCABULARY.md` (CREATE — --vocab output)
- `Vault/System-Map.md` (MODIFY — SymptomLab row + SYMPTOM_VOCABULARY link)
- `Vault/_meta/PROVENANCE.md` (MODIFY — ## symptomlab section, auto by script)
- `Vault/_bases/*.base` (re-installed identical by script; no content change)
