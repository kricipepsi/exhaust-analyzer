---
node_type: task
task_id: T-GAS-VAULT-OIL
status: authoring
pack: VAULT
lab: gaslab
mode: architect/author + vault-tooling lane
blocked_by:
- T-OIL-4
- T-OIL-5
consumers:
- build_lab_vault.py — vault frontmatter derivation
- consumers.base — signal/noise audit view
- drift-guards.base — coverage view
- modules.base — module map view
- vault_query.py health — re-runnable vault gate
implements:
- vault-map.gaslab.yaml
- Vault/labs/gaslab/wiki/06a_fault_atlas_oil_mechanical.md
- Vault/labs/gaslab/docs/GAS_VOCABULARY.md
tags:
- task
- vault
- gaslab
- oil
---

# T-GAS-VAULT-OIL — Refresh the GASLab vault tier to absorb the oil-consumption pack

**Status:** `authoring` · **Pack:** VAULT (GASLab) · **Mode:** architect/author + vault-tooling
lane (no `gaslab/` inner-loop/gate unless a later oil task changes GASLab code)
**Blocked by:** **T-OIL-4** (the COMLab oil-family routing rule exists — the *named consumer* for the
new content), **T-OIL-5** (gaslab wiki oil cases finalised so the copied bodies are current).

### Why this exists ###

The GASLab vault tier (`Vault/labs/gaslab/`) was built by **T-GAS-VAULT** on 2026-06-11 — *before*
the oil-consumption pack was reconciled. The oil pack does **not** add live GASLab enum members:
T-OIL-2 records `PCV_STUCK_OPEN`, `TURBO_SEAL_OIL_LEAK`, and `HEAD_GASKET_OIL_BREACH` as proposal-only
values that map to existing live emissions (`POA_SIGNATURE` / `COOLANT_LEAK_INTERNAL`). T-OIL-5 will
refresh the `06a_fault_atlas_oil_mechanical.md` and vocabulary bodies. The vault is a **read-mostly
mirror** — none of that appears in the vault until the GASLab tier is rebuilt with the proposal-only
framing.

> **Re-extraction rule.** Do not re-run GASLab `v2_code` / `v2_tests` graph extraction merely because
> T-OIL-2 completed; it made no live code or test changes. Re-extract only if T-OIL-4/T-OIL-5 or a
> later explicit owner task changes GASLab code/tests and authorizes that scoped graph refresh.

### Scope confirmation (1 paragraph) ###

Author the proposal-only oil deltas into `assets/vault-map.gaslab.yaml` so the `06a` oil content is
framed against a **named, existing** consumer from T-OIL-4, then re-run `build_lab_vault.py --lab gaslab`
(dry-run → apply) and close on the `vault_query.py health` gate. **Files:**
`_skills/graph/4dlab-vault/assets/vault-map.gaslab.yaml` (MODIFY), and the generated
`Vault/labs/gaslab/…`, `Vault/_meta/PROVENANCE.md`, `Vault/System-Map.md`. **No new vault field type**
— this is a content + framing refresh, not a schema change.

### Graphify scope ###

This task is **not** blanket authorization to re-run graph extraction. The default path is a vault-map
and vault rebuild only. If a later explicit task changes GASLab code/tests before this runs, re-extract
only the affected GASLab AST tier(s); do not touch the root FX graph, any other lab's graph, or
gaslab `v2_wiki` / `v2_docs`.

### The two vault-map deltas (the only authored edits) ###

`assets/vault-map.gaslab.yaml`, note **`06a_fault_atlas_oil_mechanical.md`** (subsystem
`mechanical-wear-atlas` — already framed). The new oil signatures land here, so:

1. **`implements`** — frame the proposal-only oil signatures through the GASLab wiki/vocabulary notes
   that record them, not through `contracts.py`. The canonical proposal names are `PCV_STUCK_OPEN`,
   `TURBO_SEAL_OIL_LEAK`, and `HEAD_GASKET_OIL_BREACH`.
2. **`drift_guards`** — use the COMLab T-OIL-4 routing tests and any GASLab wiki/vocabulary drift guards
   T-OIL-5 adds. Do not invent GASLab enum tests for proposal-only values.
3. **`consumers`** — add the **named, existing** oil consumer that T-OIL-4 shipped, e.g.
   `comlab: labs/comlab/comlab/core/fault_atlas_router.py oil-family routing` (mirror the exact path
   T-OIL-4 used). This is the signal/noise line — **do not** frame the new oil content against a
   consumer that does not yet exist; that is why this task is blocked on T-OIL-4.

No other framed note needs a delta unless T-OIL-2/5 added a *new* gaslab wiki note (e.g. a split
`06c_*`). If so, frame it the same way (named consumer or leave it in `plain:`). Do **not**
auto-derive consumers.

### Named signal/noise consumer (of this task) ###

The vault's three `.base` views + `vault_query.py health` are the live readers of the frontmatter this
task injects. The refresh is "consumed" the moment `health` reads the updated `06a` frontmatter and
reports the oil note framed with ≥1 named consumer and ≥1 drift-guard.

### Success criteria ###

- `vault-map.gaslab.yaml` `06a` carries the proposal-only oil `implements` + `drift_guards` + a **named existing**
  oil `consumers` line; no framed GAS note has an empty `consumers` list.
- `build_lab_vault.py --lab gaslab --dry-run` shows the planned copy/inject; the apply run copies the
  refreshed `06a` body + code/tests into `Vault/labs/gaslab/` and re-injects frontmatter (idempotent).
- `Vault/labs/gaslab/wiki/06a_fault_atlas_oil_mechanical.md` shows the new oil-case text **and** the
  updated consumer/drift frontmatter.
- `vault_query.py --vault Vault health` → PASS (signal/noise, coverage, ledger integrity, `.base`
  presence). This is the closing gate.
- `_meta/PROVENANCE.md` GASLab section re-stamped with today's build date.

### Files to touch ###

- `_skills/graph/4dlab-vault/assets/vault-map.gaslab.yaml` (MODIFY — `06a` / GAS vocabulary deltas only)
- `Vault/labs/gaslab/…` (generated), `Vault/_meta/PROVENANCE.md`, `Vault/System-Map.md` (build date)

### Out of scope ###

- Mirroring **VINLab** or **SymptomLab** into the vault — that is the separate downstream follow-up
  (see oil-pack PROGRESS U-OIL-VAULT-1); those labs are not in `System-Map.md` yet and need their own
  `vault-map.<lab>.yaml` authored first.
- Re-graphifying any other lab or the root FX graph; building any other vault tier; the COMLab/symptom
  sides of the oil pack (not mirrored — vault holds gaslab/dtclab/obdlab only).

### Verification ###

```bash
cd $HOME/mnt/4DLab/4DLabV2
# 1) build dry-run then apply
python3 _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab gaslab --repo "$PWD" --dry-run | head -40
python3 _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab gaslab --repo "$PWD"
# 2) the oil note is framed with a real consumer + guard
sed -n '1,20p' Vault/labs/gaslab/wiki/06a_fault_atlas_oil_mechanical.md
# 3) closing gate
python3 _skills/graph/4dlab-vault/scripts/vault_query.py --vault Vault health
```

### On completion ###

Both VERIFICATION GATE + CODE REVIEW blocks clean in
`Vault/tasks/progress_notes/T-GAS-VAULT-OIL.md`; flip the row to `done` in the oil-pack PROGRESS
(`T-OIL-VAULT`). Then STOP — one task per session. The VINLab/SymptomLab vault mirroring is a fresh
session with its own task.
