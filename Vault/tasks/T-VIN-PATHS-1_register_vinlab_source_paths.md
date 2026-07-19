---
node_type: task
task_id: T-VIN-PATHS-1
status: done
pack: VAULT
lab: vinlab
mode: graph-tooling / vault-tooling lane
blocked_by: []
consumers:
- build_lab_vault.py — vault frontmatter derivation
implements:
- vault-map.vinlab.yaml
tags:
- task
- vault
- vinlab
---

# T-VIN-PATHS-1 — Register VINLab's source paths in the vault build (`LAB_SRC_PATHS`)

**Status:** `done` (2026-06-13) · **Pack:** VAULT (VINLab) · **Mode:** GRAPH-TOOLING / vault-tooling lane (not lab diagnostic code; no lab inner-loop/gate)
**Origin:** `build_lab_vault.py` `LAB_SRC_PATHS` has no `vinlab` entry · **Blocked by:** —
**Consumer (signal/noise):** **The consumer is `build_lab_vault.py` itself** — it must resolve VINLab's
real source dirs or `T-VIN-VAULT` cannot run. No schema field is added; this adds one per-lab config entry
so the existing build logic reads the right folders. The injected frontmatter (read by the three `.base`
views) is unchanged — only *where it reads from* is corrected.

### Role note ###

`build_lab_vault.py` is vault tooling, not lab diagnostic code — no `vinlab/` inner-loop/gate. Edit + a
dry-run prove-out only. No graphify, no re-extraction.

### The defect (verified 2026-06-12) ###

`LAB_SRC_PATHS` is already parametrized (per-lab overrides default to OBDLab's layout when a lab has no
entry). Today it has `obdlab`, `gaslab`, `dtclab`, `symptomlab` — **`vinlab` is absent**, so a VIN build
falls through to the OBDLab default (`research/chunks` + four graph tiers) and `sys.exit`s on the missing
`research/chunks` dir and the missing `v2_wiki`/`v2_docs` graphs. VINLab's real layout matches
GASLab/DTCLab: wiki at `labs/vinlab/wiki/`, and (per "skip graph testing") only `v2_code` + `v2_tests`
are built.

### Goal ###

Add a `vinlab` entry to `LAB_SRC_PATHS` mirroring `gaslab`/`dtclab`, so the build resolves `wiki/` and
requires only the two AST graph tiers. **OBDLab, GASLab, DTCLab, SymptomLab behaviour must be
byte-identical** after this.

### Exact change ###

```python
    "vinlab": {
        "wiki_subpath":          "wiki",
        "wiki_source_template":  "labs/{lab}/wiki/{note}",
        # "skip graph testing" (owner, 2026-06-12): prose Pass-3 waived; only AST tiers required.
        "required_graph_tiers":  ("v2_code", "v2_tests"),
    },
```

If the script reads a single `graph_source` for frontmatter (it currently keys off the tier dirs), mirror
whatever `gaslab`/`dtclab` does — do **not** introduce a new mechanism. Read-only on all graphs; no
re-extraction. If more than a dict-entry add is needed, scope only the minimal change that lets
`--dry-run --lab vinlab` resolve, and flag the rest as a follow-up (do not enlarge the diff).

### Success criteria ###

1. `--lab obdlab --dry-run`, `--lab gaslab --dry-run`, `--lab dtclab --dry-run`, `--lab symptomlab
   --dry-run` outputs all **unchanged** (regression guards — capture before/after).
2. `--lab vinlab --dry-run` **resolves** VINLab's `wiki/` and requires only `v2_code`/`v2_tests` (no
   spurious `research/chunks` or `v2_wiki`/`v2_docs` abort) **once the graphs exist** (after
   `T-VIN-GRAPH-AST`; until then the dry-run legitimately reports the graphs as not-yet-built — the real
   eligibility gate, not a path bug).
3. The `source:` provenance string for a VIN wiki note reads `labs/vinlab/wiki/<note>`.
4. No graphify; no re-extraction; no `obdlab`/`gaslab`/`dtclab`/`symptomlab`/`vinlab` code/test edit.

### Out of scope ###

- Authoring `vault-map.vinlab.yaml` and running the real build — that is `T-VIN-VAULT`.
- Changing any other lab's entry · editing the pipeline guide prose (owner follow-up, START_HERE §6).

### Files to touch ###

- `_skills/graph/4dlab-vault/scripts/build_lab_vault.py` (one `LAB_SRC_PATHS` entry).

### Verification ###

```bash
cd <repo>/4DLabV2
for lab in obdlab gaslab dtclab symptomlab; do
  python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab $lab --repo "$PWD" --dry-run > /tmp/${lab}_after.txt
  diff /tmp/${lab}_before.txt /tmp/${lab}_after.txt && echo "OK $lab unchanged"   # capture _before first
done
python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab vinlab --repo "$PWD" --dry-run | head -40
```

### Progress hook ###

`Vault/tasks/progress_notes/T-VIN-PATHS-1.md` opens with the confirmed `## Plan` (the dict entry); the run
session fills `VERIFICATION GATE` (four existing labs' dry-runs unchanged; VIN dry-run resolves wiki/+two
tiers; provenance correct) + `CODE REVIEW` (minimal one-entry diff). Ledger row → `done` only when both clean.
