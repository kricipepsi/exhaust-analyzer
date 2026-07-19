---
node_type: task
task_id: T-DTC-PATHS-1
status: done
pack: VAULT
lab: dtclab
mode: graph-tooling / vault-tooling lane
blocked_by: []
consumers:
- build_lab_vault.py — vault frontmatter derivation
implements:
- vault-map.dtclab.yaml
tags:
- task
- vault
- dtclab
---


# T-DTC-PATHS-1 — Register DTCLab's source paths in the vault build (`LAB_SRC_PATHS`)

**Status:** `done` · **Pack:** VAULT (DTCLab) · completed 2026-06-11 · **Mode:** GRAPH-TOOLING / vault-tooling lane (not lab diagnostic code; no lab inner-loop/gate)
**Origin:** `build_lab_vault.py` `LAB_SRC_PATHS` has no `dtclab` entry · **Blocked by:** —
**Consumer (signal/noise):** **The consumer is `build_lab_vault.py` itself** — it must resolve DTCLab's
real source dirs or `T-DTC-VAULT` cannot run. No schema field is added; this adds one per-lab config
entry so the existing build logic reads the right folders. The injected frontmatter (read by the three
`.base` views) is unchanged — only *where it reads from* is corrected.

### Role note ###

`build_lab_vault.py` is vault tooling, not lab diagnostic code — no `dtclab/` inner-loop/gate. Edit + a
dry-run prove-out only. No graphify, no re-extraction.

### The defect (verified 2026-06-11) ###

`T-GAS-PATHS-1` already **parametrized** the script: per-lab overrides live in the `LAB_SRC_PATHS` dict,
defaulting to OBDLab's layout when a lab has no entry. Today it has only `obdlab` and `gaslab`:

```python
LAB_SRC_PATHS = {
    "obdlab": { "wiki_subpath": "research/chunks", ...,
                "required_graph_tiers": ("v2_code","v2_tests","v2_wiki","v2_docs") },
    "gaslab": { "wiki_subpath": "wiki", "wiki_source_template": "labs/{lab}/wiki/{note}",
                "required_graph_tiers": ("v2_code","v2_tests") },
}
```

`dtclab` is **absent**, so a DTC build falls through to the OBDLab default (`research/chunks` + four
graph tiers) and the eligibility check `sys.exit`s on the missing `research/chunks` dir and the missing
`v2_wiki`/`v2_docs` graphs. DTCLab's real layout is identical to GASLab's: wiki at `labs/dtclab/wiki/`,
and (per "skip graph testing") only the `v2_code` + `v2_tests` tiers are built.

### Goal ###

Add a `dtclab` entry to `LAB_SRC_PATHS` mirroring `gaslab`, so the build resolves `wiki/` and requires
only the two AST graph tiers. **OBDLab and GASLab behaviour must be byte-identical** after this.

### Exact change ###

```python
    "dtclab": {
        "wiki_subpath":          "wiki",
        "wiki_source_template":  "labs/{lab}/wiki/{note}",
        # "skip graph testing" (owner, 2026-06-11): prose Pass-3 waived; only AST tiers required.
        "required_graph_tiers":  ("v2_code", "v2_tests"),
    },
```

If the script reads a single `graph_source` for frontmatter (it currently keys off the tier dirs),
mirror whatever `gaslab` does — do **not** introduce a new mechanism. Read-only on all graphs; no
re-extraction. If more than a dict-entry add is needed, scope only the minimal change that lets
`--dry-run --lab dtclab` resolve, and flag the rest as a follow-up (do not enlarge the diff).

### Success criteria ###

1. `python build_lab_vault.py --lab obdlab --repo <repo>/4DLabV2 --dry-run` output is **unchanged**
   (OBD regression guard — capture before/after).
2. `python build_lab_vault.py --lab gaslab --repo <repo>/4DLabV2 --dry-run` output is **unchanged**
   (GAS regression guard).
3. `python build_lab_vault.py --lab dtclab --repo <repo>/4DLabV2 --dry-run` **resolves** DTCLab's `wiki/`
   and requires only `v2_code`/`v2_tests` (no spurious `research/chunks` or `v2_wiki`/`v2_docs` abort)
   **once the graphs exist** (i.e. after `T-DTC-GRAPH-AST`; until then the dry-run legitimately reports
   the graphs as not-yet-built — that is the real eligibility gate, not a path bug).
4. The `source:` provenance string for a DTC wiki note reads `labs/dtclab/wiki/<note>`.
5. No graphify; no re-extraction; no `obdlab`/`gaslab`/`dtclab` code/test edit.

### Out of scope ###

- Authoring `vault-map.dtclab.yaml` and running the real build — that is `T-DTC-VAULT`.
- Changing OBD/GAS entries · editing the pipeline guide prose (owner follow-up, START_HERE §5).

### Files to touch ###

- `_skills/graph/4dlab-vault/scripts/build_lab_vault.py` (one `LAB_SRC_PATHS` entry).

### Verification ###

```bash
cd <repo>/4DLabV2
for lab in obdlab gaslab; do
  python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab $lab --repo "$PWD" --dry-run > /tmp/${lab}_after.txt
  diff /tmp/${lab}_before.txt /tmp/${lab}_after.txt && echo "OK $lab unchanged"   # capture _before first
done
python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab dtclab --repo "$PWD" --dry-run | head -40
```

### Progress hook ###

`Vault/tasks/progress_notes/T-DTC-PATHS-1.md` opens with the confirmed `## Plan` (the dict entry); the run
session fills `VERIFICATION GATE` (OBD+GAS dry-runs unchanged; DTC dry-run resolves wiki/+two tiers;
provenance correct) + `CODE REVIEW` (minimal one-entry diff). Ledger row → `done` only when both clean.
