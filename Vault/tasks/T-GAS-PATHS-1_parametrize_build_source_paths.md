---
node_type: task
task_id: T-GAS-PATHS-1
status: pending
pack: VAULT
lab: gaslab
mode: graph-tooling / vault-tooling lane
blocked_by: []
consumers:
- build_lab_vault.py — vault frontmatter derivation
implements:
- vault-map.gaslab.yaml
tags:
- task
- vault
- gaslab
---


# T-GAS-PATHS-1 — Parametrize the vault build's per-lab source paths (GASLab layout)

**Status:** `pending` · **Pack:** VAULT (GASLab) · **Mode:** GRAPH-TOOLING / vault-tooling lane (not lab diagnostic code; no lab inner-loop/gate)
**Origin:** owner warning 2026-06-10 ("wiki is in labs/gaslab/wiki; there might be other broken-wrong paths") + OBDLab `T-VAULT-PATHS-1` model · **Blocked by:** —
**Consumer (signal/noise):** **The consumer is `build_lab_vault.py` itself** — it must resolve
GASLab's real source dirs or `T-GAS-VAULT` cannot run. No schema field is added; this fixes hardcoded
path constants so the existing build logic reads the right folders. The frontmatter the build injects
(read by the three `.base` views, plan §4) is unchanged — only *where it reads from* is corrected.

### Role note ###

`build_lab_vault.py` is vault tooling, not lab diagnostic code (plan §5) — no `gaslab/` inner-loop/gate.
Edit + a dry-run prove-out only. No graphify, no re-extraction.

### The defect (verified 2026-06-10) ###

`_skills/graph/4dlab-vault/scripts/build_lab_vault.py` hardcodes OBDLab's layout:

```
line 195:  wiki_src = lab_src / "research" / "chunks"          # GAS wiki is at labs/gaslab/wiki/
line 197:  graph    = lab_src / "graphify-out" / "graph.json"  # GAS graph is four-tier graph/v2_*/
line 237:  source_path = f"labs/{a.lab}/research/chunks/{note}" # wrong provenance string for GAS
```

The eligibility check (line ~200) lists these in `missing` and **`sys.exit`s** — so a GAS build aborts
before copying anything. GASLab's actual layout (see `GAS_VAULT_TASKS_START_HERE.md` §0): wiki =
`labs/gaslab/wiki/`; graph = the four-tier `labs/gaslab/graph/v2_{code,tests,wiki,docs}/graph.json`
built by T-GAS-GRAPH-AST/LLM; there is no single `graphify-out/graph.json`.

### Goal ###

Make the build resolve **each lab's** real source paths, so OBDLab keeps working unchanged and GASLab
resolves to `wiki/` + the four-tier graph dir. **OBDLab behaviour must be byte-identical** after this.

### Approach (coder picks one; state which in the Plan) ###

1. **Per-lab path config** — a small table keyed by lab slug (e.g. `LAB_SRC = {"obdlab": {...}, "gaslab": {...}}`)
   giving `wiki_subpath`, `graph_source`, and the `source_path` template; default to OBD's values.
2. **vault-map-driven** — read `wiki_subpath` / `graph_source` from `assets/vault-map.<lab>.yaml`
   (authored in T-GAS-VAULT), defaulting to OBD's paths when absent.

Either is fine; (1) is simpler and needs no map field. Whichever is chosen, the `source:` provenance
string (line 237) must reflect the lab's real folder (`labs/gaslab/wiki/<note>` for GAS).

### Graph-source note ###

The script reads one `graph.json` to inform frontmatter; GAS has four. Decide and record: either
point the per-lab `graph_source` at the tier most relevant to frontmatter derivation, or extend the
read to the four-tier dir. **Do not** re-extract any graph — read-only. If this needs more than a path
swap, scope only the minimal change that lets `--dry-run` resolve for GAS, and flag the rest as a
follow-up (do not enlarge the diff).

### Success criteria ###

1. `python build_lab_vault.py --lab obdlab --repo <repo>/4DLabV2 --dry-run` output is **unchanged**
   from before this task (OBD regression guard — capture before/after).
2. `python build_lab_vault.py --lab gaslab --repo <repo>/4DLabV2 --dry-run` **resolves** GASLab's
   `wiki/` + four-tier graph and lists a sane copy/inject plan (no spurious "missing" abort) **once the
   graphs exist** (i.e. after T-GAS-GRAPH-AST/LLM; until then the dry-run legitimately reports the
   graph as not-yet-built — that is the real eligibility gate, not a path bug).
3. The `source:` provenance string for a GAS wiki note reads `labs/gaslab/wiki/<note>`.
4. No graphify; no re-extraction; no `obdlab/` or `gaslab/` code/test edit.

### Out of scope ###

- Authoring `vault-map.gaslab.yaml` and running the real build — that is T-GAS-VAULT.
- Editing the pipeline guide's prose paths — flag as the owner follow-up in `GAS_VAULT_TASKS_START_HERE.md` §5; not a code task here.

### Files to touch ###

- `_skills/graph/4dlab-vault/scripts/build_lab_vault.py` (per-lab path resolution).
- Optionally `_skills/graph/4dlab-vault/reference/…` if a path note documents the per-lab override.

### Verification ###

```bash
cd <repo>/4DLabV2
python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab obdlab --repo "$PWD" --dry-run > /tmp/obd_after.txt
diff /tmp/obd_before.txt /tmp/obd_after.txt && echo "OK OBD unchanged"   # capture _before first
python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab gaslab --repo "$PWD" --dry-run | head -40
```

### Progress hook ###

`Vault/tasks/progress_notes/T-GAS-PATHS-1.md` opens with the confirmed `## Plan` (which approach,
graph-source decision); the run session fills `VERIFICATION GATE` (OBD dry-run unchanged; GAS dry-run
resolves wiki/+graph; provenance string correct) + `CODE REVIEW` (minimal diff, OBD untouched). Ledger
row → `done` only when both clean.
