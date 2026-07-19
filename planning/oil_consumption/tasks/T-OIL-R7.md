# T-OIL-R7 — Refresh the GASLab vault tier to absorb the oil pack

### Goal ###

Bring the GASLab Obsidian vault tier up to date with the oil pack: inject the
proposal-only `06a`/GAS vocabulary-map deltas, rebuild the affected tier, and pass
the vault `health` gate. Done when `vault_query.py health` is clean and the oil
deltas appear in the `.base` views. Carry-over of the retired `T-OIL-VAULT`.

### Success criteria ###

- `python <vault>/vault_query.py health` exits 0 with no missing-frontmatter or
  broken-link errors for the oil entries.
- The `06a` frontmatter for the oil signatures (`PCV_STUCK_OPEN`,
  `TURBO_SEAL_OIL_LEAK`, `HEAD_GASKET_OIL_BREACH` — proposal-only) is present in the
  rebuilt tier and surfaced by the relevant `.base` view.
- No non-oil vault entry changes (diff scoped to oil).

### Context ###

Per the Obsidian-vault memory: the vault copies only finished labs' code+tests+wiki;
`graph.json` is never copied; the build had not been run at pack authoring time.
This row runs only the vault refresh for the oil deltas, after R6 has reconciled the
source docs/wiki. The vault map for GASLab is the input of record; the oil
signatures remain **proposal-only** (they do not extend the live `ChemicalSignature`
contract — T-OIL-2 canon gate).

STRICT-ONLY: Load skills: read the `4dlab-vault` skill before building (per memory).

### Consumer (signal/noise) ###

- **Consumer:** vault `.base` views + `vault_query.py health` read the injected
  `06a` frontmatter. No new engine field.

### Deliverables ###

1. GASLab `vault-map` / `06a` vocabulary-map deltas for the three oil signatures.
2. Rebuilt vault tier (oil-scoped) + green `health` gate.
3. Progress note: `Vault/tasks/T-GAS-VAULT-OIL_refresh_gaslab_vault_oil.md`.

### Files to touch ###

- GASLab vault map / `06a` source (MODIFY — coder pins path via the vault skill)
- rebuilt vault tier artefacts (GENERATED)
- `Vault/tasks/progress_notes/T-OIL-R7.md` (CREATE)

### Out of scope ###

Do not add VINLab/SymptomLab to the vault (that is `U-OIL-VAULT-1`, its own session).
Do not copy `graph.json`. Do not promote the oil signatures into the live
`ChemicalSignature` enum. No engine/registry changes. GRAPH GUARDRAIL: no graphify.

### Verification ###

```bash
cd /sessions/<vm>/mnt/4DLab
python3.14 <vault>/vault_query.py health
# Oil deltas present
grep -rq "TURBO_SEAL_OIL_LEAK\|PCV_STUCK_OPEN" <vault-06a-path>
```

All steps must pass.

### Progress hook ###

PROGRESS.md `T-OIL-R7`: Status=done, Files changed={COUNT}, Verification="vault health green; oil 06a proposal deltas present in rebuilt tier; diff oil-scoped"
