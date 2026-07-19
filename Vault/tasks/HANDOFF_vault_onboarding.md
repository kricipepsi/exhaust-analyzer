# HANDOFF — Vault onboarding for VINLab + SymptomLab (next session)

**Written:** 2026-06-12 (architect). **Why a handoff:** vault onboarding for two new
labs is substantial — its own session, fresh context. This note bootstraps it.

---

## Where things stand (done this session)

- **Oil-consumption pack** authored: `planning/oil_consumption/`
  (`OIL_CONSUMPTION_START_HERE.md` + `PROGRESS.md`). T-OIL-1 (symptom side) is `done`;
  T-OIL-2…5 are scoped `authoring` rows; **T-OIL-VAULT** (GASLab vault refresh) is
  authored & ready, blocked by T-OIL-2/4/5. Task file:
  `Vault/tasks/T-GAS-VAULT-OIL_refresh_gaslab_vault_oil.md`.
- **This handoff's task — U-OIL-VAULT-1** (oil-pack PROGRESS follow-ups table): add
  **VINLab** and **SymptomLab** to the vault. Not yet authored. Do it next session.

## The job

Today the vault mirrors **gaslab / dtclab / obdlab** only (`Vault/System-Map.md`).
The DNA-family labs are absent, so the T-OIL-1 symptom vocabulary will never surface
in the vault until VINLab + SymptomLab are onboarded. Onboarding each lab = the same
pipeline GASLab/DTCLab already went through:

```
  author vault-map.<lab>.yaml   (framed notes → module/implements/consumers/drift_guards)
        │                        consumers are HUMAN-authored, never auto-derived
        ▼
  ensure graph tiers exist      (graphify run — gated; see gotcha #2)
        ▼
  build_lab_vault.py --lab <lab>  (dry-run → apply)
        ▼
  add lab to System-Map.md + _meta/PROVENANCE.md
        ▼
  vault_query.py health → PASS   (closing gate)
```

## Start-of-session checklist (verify before authoring — do not assume)

1. **Eligibility per lab.** `build_lab_vault.py` requires, for each lab:
   `labs/<lab>/<lab>/` (code), `labs/<lab>/tests/`, a wiki dir, `labs/<lab>/docs/`,
   **and** the required `graph/<tier>/graph.json` files. Check what exists for
   `vinlab` and `symptomlab`. (SymptomLab has `symptomlab/wiki/`; confirm VINLab's
   wiki/docs/graph state.)
2. **GOTCHA — `LAB_SRC_PATHS`.** `build_lab_vault.py` only has path entries for
   `obdlab`/`gaslab`/`dtclab`. Any other lab **defaults to the OBDLab layout**: wiki at
   `research/chunks/` and **all four** graph tiers required (`v2_code`, `v2_tests`,
   `v2_wiki`, `v2_docs`). VINLab/SymptomLab keep wiki at `wiki/`, not `research/chunks/`,
   and may not have prose graphs. So onboarding almost certainly needs **new
   `LAB_SRC_PATHS` entries** for `vinlab` + `symptomlab` (wiki_subpath `wiki`, and an
   owner waiver for `v2_wiki`/`v2_docs` like GASLab/DTCLab got) — that is a small,
   reviewed edit to the vault tooling, not lab code.
3. **GOTCHA — graphify is gated.** Producing `v2_code`/`v2_tests` graphs means running
   the **`4dlab-graphify-run`** skill — only with explicit instruction, scoped to those
   two labs' two AST tiers. Get the owner's "yes, graphify vinlab + symptomlab" on the
   record in the task before running it.
4. **Naming overload (owner-flagged).** "DNALab" is the umbrella for three modules
   (`dna` = `dnalab/`, `vin` = `vinlab/`, `symptom` = `symptomlab/`). Decide the vault
   module/landing-note naming so it doesn't collide (see the tri-module audit U-7).
5. **VINLab strict-gate** (memory): VINLab closes only when the whole repo is green —
   keep the vault-tooling lane separate from that, but don't trip it.

## Likely task shape (to author next session)

A small pack, one row per lab (one task per session each):

| ID (proposed) | Title | Blocked-by |
|---|---|---|
| T-VAULT-SYMPTOM-PATHS | Add `symptomlab` (+`vinlab`) entries to `LAB_SRC_PATHS`; owner waiver for prose tiers | — |
| T-VAULT-SYMPTOM-1 | Author `vault-map.symptomlab.yaml`, graphify v2_code/v2_tests, build, System-Map, health | T-VAULT-SYMPTOM-PATHS |
| T-VAULT-VIN-1 | Author `vault-map.vinlab.yaml`, graphify v2_code/v2_tests, build, System-Map, health | T-VAULT-SYMPTOM-PATHS |

SymptomLab is the smaller/cleaner of the two (validator + models + small wiki) — do it
first as the template; VINLab is the heavy module (decoder ~644 lines) so its
`vault-map` (implements/drift_guards) is bigger.

## Key references

- Vault skill: `_skills/graph/4dlab-vault/SKILL.md` (build + `vault_query.py` read side).
- Build script + the `LAB_SRC_PATHS` table: `_skills/graph/4dlab-vault/scripts/build_lab_vault.py`.
- Existing template to copy: `_skills/graph/4dlab-vault/assets/vault-map.gaslab.yaml`
  and the build task `Vault/tasks/T-GAS-VAULT_build_gaslab_vault.md`.
- Tri-module audit (vin/symptom internals + consumers): `labs/dnalab/audits/AUDIT_2026-06-12_trimodule_dna_vin_symptom.md`.

## One rule, unchanged

Every framed vault note ships with a **named, existing** consumer (a `.base` view, a code
path, or a COMLab analytic). Empty `consumers` = not ready to frame → leave it `plain:`.
Never auto-derive consumers.
