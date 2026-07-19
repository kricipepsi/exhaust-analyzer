# T-OIL-R7 — progress note

**Status:** `done` · **Pack:** oil_consumption (GASLab vault) · completed 2026-06-12 (coder)
Task spec: `4DLabV2/planning/oil_consumption/tasks/T-OIL-R7.md` · Pack ledger: `4DLabV2/planning/oil_consumption/PROGRESS.md`

## Plan
Refresh the GASLab Obsidian vault tier so it absorbs the oil pack's R6 source-doc
reconcile and R3a high-idle contract. The vault build (`build_lab_vault.py --lab
gaslab`) re-copies `labs/gaslab/{gaslab,tests,wiki,docs}` into `Vault/labs/gaslab/`
and re-injects the consumer-aware frontmatter from `vault-map.gaslab.yaml`, so the
oil deltas already present in the **source** propagate into the vault on rebuild.
The three oil signatures (`PCV_STUCK_OPEN`, `TURBO_SEAL_OIL_LEAK`,
`HEAD_GASKET_OIL_BREACH`) remain **proposal-only** — they are documented in `06a`
and `GAS_VOCABULARY.md`, not promoted into the live `ChemicalSignature` enum
(T-OIL-2 canon gate). No graphify, no `graph.json` copy, no engine/registry change.

## Oil-scoping (pre-build verification)
Before rebuilding, every GASLab source `.md`/code file was compared against its
vault copy with **line-endings normalized** (CRLF/LF churn was masking the real
diff). After normalization, only oil-pack files differed in content:

| File | Why it differs | Owning row |
|---|---|---|
| `wiki/06a_fault_atlas_oil_mechanical.md` | head-gasket reroute `POA_SIGNATURE` → `COOLANT_LEAK_INTERNAL` | R6 |
| `docs/GAS_VOCABULARY.md` | high-idle delta block + MW-001/002/003/008/009 rule-ID column | R6 + R3a |
| `gaslab/contracts.py` | `high_idle_{hc,co,co2,o2,nox,lambda}` optional fields | R3a |
| `gaslab/process.py` | emits the high-idle block from `reading_high` | R3a |
| `tests/unit/test_process.py` | `test_emits_high_idle_block` | R3a |

All five are oil-pack work; no unrelated GASLab drift was propagated. The three
non-gaslab modified vault files in `git status` (`_vocabulary/GAS_VOCABULARY.md`,
`_vocabulary/OBD_VOCABULARY.md`, `labs/obdlab/_obdlab.md`) are **pre-existing
uncommitted state** — the `--lab gaslab` build only writes under `labs/gaslab/`,
`_bases/`, and `_meta/PROVENANCE.md` — and were left untouched.

## VERIFICATION GATE
- Eligibility: `labs/gaslab/{gaslab,tests,wiki,docs}` + `graph/v2_code/graph.json`
  + `graph/v2_tests/graph.json` all present (GASLab prose Pass-3 owner-waived).
- Dry-run: `build_lab_vault.py --lab gaslab --repo <4DLabV2> --dry-run` planned the
  4 copies, 15 framed notes, 4 `.base` installs, gaslab provenance upsert — clean.
- Build: `build_lab_vault.py --lab gaslab --repo <4DLabV2>` completed successfully.
- Health gate: `vault_query.py --vault Vault health` → **exit 0** (verdict WARN).
  - `signal/noise: 46/46 framed notes name a consumer` [OK]
  - `coverage: 0 note(s) implement code with no drift_guard` [OK]
  - `.base views: 4/4 present` [OK]; `dependency cycles: none` [OK]
  - The single WARN (`blocked_by refs: 3 cross-ledger ref(s) — T-OIL-4, T-OIL-5,
    T-SEM-5`) is **pre-existing** and explicitly non-fatal by the script's design
    (cross-pack refs WARN, never FAIL). R7 changed **0** files under
    `Vault/tasks/`, so it did not introduce or alter that WARN.
- Oil deltas present in rebuilt tier:
  - `06a_fault_atlas_oil_mechanical.md` — 7 hits for
    `TURBO_SEAL_OIL_LEAK|PCV_STUCK_OPEN|HEAD_GASKET_OIL_BREACH`.
  - `docs/GAS_VOCABULARY.md` — 5 hits for `high_idle_hc|MW-008|MW-009`.
- Frontmatter intact: `06a` retains `node_type/lab/module/subsystem/implements/
  consumers/drift_guards/tags/source` from `vault-map.gaslab.yaml`.
- Proposal-only respected: oil signatures appear only as documented proposals in
  the wiki/vocabulary; no live `ChemicalSignature` enum change.

## CODE REVIEW
- No new code authored; this row is a vault rebuild that mirrors finished-lab
  source into `Vault/labs/gaslab/`. `vault-map.gaslab.yaml` already framed `06a`
  (subsystem `mechanical-wear-atlas`) with named COMLab consumers — unchanged.
- `git diff --stat` for the five oil-pack vault files: 85 insertions, 9 deletions,
  all additive oil/high-idle content. `PROVENANCE.md` gaslab section refreshed by
  the build's idempotent upsert.
