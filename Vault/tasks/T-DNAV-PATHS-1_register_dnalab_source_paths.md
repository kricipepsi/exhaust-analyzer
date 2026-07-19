---
node_type: task
task_id: T-DNAV-PATHS-1
status: done
pack: VAULT
lab: dnalab
mode: graph-tooling / vault-tooling lane
blocked_by: []
consumers:
- build_lab_vault.py — vault frontmatter derivation
implements:
- vault-map.dnalab.yaml
tags:
- task
- vault
- dnalab
---

# T-DNAV-PATHS-1 — Register DNALab's source paths in the vault build (`LAB_SRC_PATHS`)

**Status:** `pending` · **Pack:** VAULT (DNALab) · **Mode:** GRAPH-TOOLING / vault-tooling lane (not lab diagnostic code; no lab inner-loop/gate)
**Origin:** `build_lab_vault.py` `LAB_SRC_PATHS` has no `dnalab` entry · **Blocked by:** —
**Consumer (signal/noise):** **The consumer is `build_lab_vault.py` itself** — it must resolve DNALab's
real source dirs or `T-DNAV-VAULT` cannot run. No schema field is added; this adds one per-lab config
entry so the existing build logic reads the right folders. The injected frontmatter (read by the three
`.base` views) is unchanged — only *where it reads from* is corrected.

### Role note ###

`build_lab_vault.py` is vault tooling, not lab diagnostic code — no `dnalab/` inner-loop/gate. Edit + a
dry-run prove-out only. No graphify, no re-extraction.

### The defect (verified 2026-06-13) ###

`LAB_SRC_PATHS` is already parametrized (per-lab overrides default to OBDLab's layout when a lab has no
entry). Today it has `obdlab`, `gaslab`, `dtclab`, `symptomlab` — **`dnalab` is absent** (so is `vinlab`),
so a DNA build falls through to the OBDLab default (`research/chunks` + four graph tiers) and `sys.exit`s
on the missing `research/chunks` dir and the missing `v2_wiki`/`v2_docs` graphs. DNALab's real layout
matches GASLab/DTCLab: wiki at `labs/dnalab/wiki/`, and (per "skip graph testing") only `v2_code` +
`v2_tests` are built.

### Goal ###

Add a `dnalab` entry to `LAB_SRC_PATHS` mirroring `gaslab`/`dtclab`, so the build resolves `wiki/` and
requires only the two AST graph tiers. **OBDLab, GASLab, DTCLab, SymptomLab behaviour must be
byte-identical** after this.

### Exact change ###

```python
    "dnalab": {
        "wiki_subpath":          "wiki",
        "wiki_source_template":  "labs/{lab}/wiki/{note}",
        # "skip graph testing" (mirror VIN/GAS/DTC, 2026-06-13): prose Pass-3 waived; only AST tiers required.
        "required_graph_tiers":  ("v2_code", "v2_tests"),
    },
```

If the script reads a single `graph_source` for frontmatter (it currently keys off the tier dirs), mirror
whatever `gaslab`/`dtclab` does — do **not** introduce a new mechanism. Read-only on all graphs; no
re-extraction. If more than a dict-entry add is needed, scope only the minimal change that lets
`--dry-run --lab dnalab` resolve, and flag the rest as a follow-up (do not enlarge the diff).

### Success criteria ###

1. `--lab obdlab --dry-run`, `--lab gaslab --dry-run`, `--lab dtclab --dry-run`, `--lab symptomlab
   --dry-run` outputs all **unchanged** (regression guards — capture before/after).
2. `--lab dnalab --dry-run` **resolves** DNALab's `wiki/` and requires only `v2_code`/`v2_tests` (no
   spurious `research/chunks` or `v2_wiki`/`v2_docs` abort) **once the graphs exist** (after
   `T-DNAV-GRAPH-AST`; until then the dry-run legitimately reports the graphs as not-yet-built — the real
   eligibility gate, not a path bug).
3. The `source:` provenance string for a DNA wiki note reads `labs/dnalab/wiki/<note>`.
4. No graphify; no re-extraction; no `obdlab`/`gaslab`/`dtclab`/`symptomlab`/`dnalab` code/test edit.

### Out of scope ###

- Authoring `vault-map.dnalab.yaml` and running the real build — that is `T-DNAV-VAULT`.
- Adding the `vinlab` entry (that is the VIN pack's `T-VIN-PATHS-1`) · changing any other lab's entry ·
  editing the pipeline guide prose (owner follow-up, START_HERE §6).

### Files to touch ###

- `_skills/graph/4dlab-vault/scripts/build_lab_vault.py` (one `LAB_SRC_PATHS` entry).

### Verification ###

```bash
cd <repo>/4DLabV2
for lab in obdlab gaslab dtclab symptomlab; do
  python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab $lab --repo "$PWD" --dry-run > /tmp/${lab}_after.txt
  diff /tmp/${lab}_before.txt /tmp/${lab}_after.txt && echo "OK $lab unchanged"   # capture _before first
done
python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab dnalab --repo "$PWD" --dry-run | head -40
```

### Progress hook ###

`Vault/tasks/progress_notes/T-DNAV-PATHS-1.md` opens with the confirmed `## Plan` (the dict entry); the
run session fills `VERIFICATION GATE` (four existing labs' dry-runs unchanged; DNA dry-run resolves
wiki/+two tiers; provenance correct) + `CODE REVIEW` (minimal one-entry diff). Ledger row → `done` only
when both clean.
