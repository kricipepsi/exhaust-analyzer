---
node_type: task
task_id: T-COM-PATHS-1
status: done
pack: VAULT
lab: comlab
mode: graph-tooling / vault-tooling lane
blocked_by: []
consumers:
- build_lab_vault.py — vault frontmatter derivation
implements:
- vault-map.comlab.yaml
tags:
- task
- vault
- comlab
---

# T-COM-PATHS-1 — Register COMLab's source paths in the vault build (`LAB_SRC_PATHS`)

**Status:** `done` (2026-06-28) · **Pack:** VAULT (COMLab) · **Mode:** GRAPH-TOOLING / vault-tooling lane (not lab diagnostic code; no lab inner-loop/gate)
**Origin:** `build_lab_vault.py` `LAB_SRC_PATHS` has no `comlab` entry · **Blocked by:** —
**Load skills:** **`4dlab-vault`**, `comlab-python` (Python house style for the one-line script edit).
**Consumer (signal/noise):** **The consumer is `build_lab_vault.py` itself** — it must resolve COMLab's real
source dirs or `T-COM-VAULT` cannot run. No schema field added; one per-lab config entry so the existing
build logic reads the right folders.

### Role note ###

`build_lab_vault.py` is vault tooling, not lab diagnostic code — no `comlab/` inner-loop/gate. Edit + a
dry-run prove-out only. No graphify, no re-extraction.

### The defect (verified 2026-06-26) ###

`LAB_SRC_PATHS` (in `_skills/graph/4dlab-vault/scripts/build_lab_vault.py`, ~line 44) has entries for
`obdlab`/`gaslab`/`dtclab`/`symptomlab`/`vinlab`/`dnalab` but **no `comlab`** — so a COM build falls through
to the OBDLab default (`research/chunks` + four graph tiers) and the eligibility check `sys.exit`s on the
missing `research/chunks` dir and the missing `v2_wiki`/`v2_docs` graphs. COMLab's real layout matches
GASLab/DTCLab: wiki at `labs/comlab/wiki/`, and (per the "skip graph testing" trim) only `v2_code` +
`v2_tests` tiers are built.

### Exact change ###

Add a `comlab` entry mirroring `dtclab` (~line 56):

```python
    "comlab": {
        "wiki_subpath":          "wiki",
        "wiki_source_template":  "labs/{lab}/wiki/{note}",
        # "skip graph testing" (owner, 2026-06-26): prose Pass-3 waived; only AST tiers required.
        # Liftable per T-COM-GRAPH-LLM → ("v2_code","v2_tests","v2_wiki","v2_docs").
        "required_graph_tiers":  ("v2_code", "v2_tests"),
    },
```

And add `comlab` to the provenance "waived" branch (~line 357) so PROVENANCE.md reads correctly:

```python
    if a.lab in ("gaslab", "dtclab", "vinlab", "dnalab", "comlab"):
        graph_note += "; v2_wiki/v2_docs waived by owner direction"
```

If the script reads a single `graph_source` for frontmatter (it currently keys off the tier dirs), mirror
whatever `dtclab` does — do **not** introduce a new mechanism. Read-only on all graphs; no re-extraction.
If more than these two edits are needed, scope only the minimal change that lets `--dry-run --lab comlab`
resolve, and flag the rest as a follow-up (do not enlarge the diff).

### Success criteria ###

1. `--dry-run --lab obdlab`, `--lab gaslab`, `--lab dtclab` outputs are **unchanged** (regression guard —
   capture before/after for at least obdlab + dtclab).
2. `--dry-run --lab comlab` **resolves** COMLab's `wiki/` and requires only `v2_code`/`v2_tests` (no spurious
   `research/chunks` or `v2_wiki`/`v2_docs` abort) **once the graphs exist** (i.e. after `T-COM-GRAPH-AST`;
   until then the dry-run legitimately reports the graphs as not-yet-built — that is the real eligibility
   gate, not a path bug).
3. The `source:` provenance string for a COMLab wiki note reads `labs/comlab/wiki/<note>`; PROVENANCE shows
   the "v2_wiki/v2_docs waived" note.
4. No graphify; no re-extraction; no lab code/test edit.

### Out of scope ###

- Authoring `vault-map.comlab.yaml` + the real build (→ `T-COM-VAULT`) · changing other labs' entries ·
  lifting the prose-graph waiver (→ `T-COM-GRAPH-LLM`). **GRAPH GUARDRAIL:** no graphify.

### Files to touch ###

- `_skills/graph/4dlab-vault/scripts/build_lab_vault.py` (one `LAB_SRC_PATHS` entry + one branch tuple).

### Verification ###

```bash
cd <repo>/4DLabV2
for lab in obdlab dtclab; do
  python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab $lab --repo "$PWD" --dry-run > /tmp/${lab}_after.txt
  diff /tmp/${lab}_before.txt /tmp/${lab}_after.txt && echo "OK $lab unchanged"   # capture _before first
done
python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab comlab --repo "$PWD" --dry-run | head -40
```

### Progress hook ###

`Vault/tasks/progress_notes/T-COM-PATHS-1.md` opens with the confirmed `## Plan` (the dict entry + branch
line); the run session fills `VERIFICATION GATE` (OBD+DTC dry-runs unchanged; COM dry-run resolves
wiki/+two tiers; provenance correct) + `CODE REVIEW` (minimal two-line diff). Ledger row → `done` only when
both clean.
